"""Offline asynchronous contracts; no live database reads or publishing."""
import asyncio
import threading
import time
import unittest
from unittest.mock import patch
from test_regressions import TEMP, P, jobs, ch, api, FastMCP, TestClient
from prism import requests, progress, execution
import anyio


class RequestTests(unittest.TestCase):
    def setUp(self):
        self.old_conn, self.old_path = jobs._CONN, jobs.DB_PATH
        jobs._CONN, jobs.DB_PATH = None, ':memory:'
        self.registry = patch.dict(requests._REGISTRY)
        self.registry.start()
        self.gates = []

    def tearDown(self):
        for gate in self.gates:
            gate.set()
        for thread in threading.enumerate():
            if thread.name.startswith('job_'):
                thread.join(3)
        if jobs._CONN:
            jobs._CONN.close()
        jobs._CONN, jobs.DB_PATH = self.old_conn, self.old_path
        self.registry.stop()

    def gate(self):
        event = threading.Event()
        self.gates.append(event)
        return event

    def finish(self, rid):
        for thread in threading.enumerate():
            if thread.name == rid:
                thread.join(3)
                self.assertFalse(thread.is_alive())
        return requests.request_status(rid)

    def test_immediate_ack_cursor_and_original_result(self):
        gate, entered = self.gate(), threading.Event()
        expected = {'ok':True, 'data':{'answer':'Checked'}, 'feature':'research.citations'}
        def work(claim: str):
            progress.emit('database')
            ch.parallel([lambda: progress.emit('reading')])
            entered.set()
            gate.wait(3)
            return expected
        requests._REGISTRY['research.citations'] = work
        t = time.monotonic()
        start = requests.submit_request('research.citations', {'claim':'A claim'})
        self.assertLess(time.monotonic()-t, .5)
        self.assertTrue(entered.wait(2))
        state = requests.request_status(start['request_id'])
        self.assertEqual(state['status'], 'running')
        self.assertIn('seconds elapsed', state['heartbeat'])
        self.assertIn('Reading articles for you', state['message'])
        cursor = state['next_cursor']
        self.assertEqual(requests.request_status(start['request_id'], cursor)['events'], [])
        gate.set()
        done = self.finish(start['request_id'])
        self.assertEqual(done['result'], expected)
        self.assertEqual(done['status'], 'done')
        tail = requests.request_status(start['request_id'], cursor)
        self.assertTrue(all(e['sequence'] > cursor for e in tail['events']))
        self.assertEqual(tail['events'][-1]['stage'], 'done')

    def test_parallel_request_progress_is_isolated(self):
        gate = self.gate()
        reached = [threading.Event(),threading.Event()]
        def work(topic: str):
            stage = 'themes' if topic == 'news' else 'claims'
            ch.parallel([lambda: progress.emit(stage)])
            reached[0 if topic == 'news' else 1].set()
            gate.wait(3)
            return {'ok':True, 'data':{}}
        requests._REGISTRY['compose.sections'] = work
        ids = [requests.submit_request('compose.sections', {'topic':t})['request_id'] for t in ('news','draft')]
        self.assertTrue(all(event.wait(2) for event in reached))
        stages = [{e['stage'] for e in requests.request_status(rid)['events']} for rid in ids]
        self.assertIn('themes', stages[0]); self.assertNotIn('claims', stages[0])
        self.assertIn('claims', stages[1]); self.assertNotIn('themes', stages[1])

    def test_validation_and_no_publishing(self):
        def work(claim: str, limit: int = 4):
            return {'ok':True, 'data':{}}
        requests._REGISTRY['research.citations'] = work
        for feature,args in [('compose.article',{}), ('system.request',{}),
                             ('research.citations',[]), ('research.citations',{}),
                             ('research.citations',{'claim':'x','oops':1}),
                             ('research.citations',{'claim':'x','limit':'not an integer'})]:
            self.assertEqual(requests.submit_request(feature,args)['kind'], 'bad_request')
        self.assertEqual(requests.request_status('missing')['kind'], 'no_data')
        self.assertEqual(requests.request_status('missing',-1)['kind'], 'bad_request')
        self.assertEqual(jobs._conn().execute('SELECT count(*) FROM jobs').fetchone()[0],0)

    def test_section_never_spawns_nested_job(self):
        seen = []
        def work(topic: str, background: bool = True):
            seen.append(background)
            return {'ok':True, 'data':{}}
        requests._REGISTRY['compose.section'] = work
        self.finish(requests.submit_request('compose.section', {'topic':'Test', 'background':True})['request_id'])
        self.assertEqual(seen, [False])

    def test_failure_and_exception_have_human_status(self):
        failure = {'ok':False, 'error':{'kind':'no_data', 'reason':'No eligible sources'}}
        requests._REGISTRY['compose.sections'] = lambda topic: failure
        done = self.finish(requests.submit_request('compose.sections', {'topic':'Test'})['request_id'])
        self.assertEqual(done['result'], failure)
        self.assertEqual(done['status'], 'failed')
        self.assertEqual(done['events'][-1]['stage'], 'no_result')
        def crash(topic: str):
            raise RuntimeError('private backend details')
        requests._REGISTRY['compose.sections'] = crash
        failed = self.finish(requests.submit_request('compose.sections', {'topic':'Test'})['request_id'])
        self.assertEqual(failed['status'], 'failed')
        self.assertNotIn('private backend', str(failed))

    def test_queue_backpressure(self):
        gate, entered = self.gate(), threading.Event()
        def work(topic: str):
            entered.set(); gate.wait(3)
            return {'ok':True, 'data':{}}
        requests._REGISTRY['compose.sections'] = work
        with patch.object(jobs, 'MAX_RUNNING', 1), patch.object(jobs, 'MAX_QUEUED', 0):
            rid = requests.submit_request('compose.sections', {'topic':'one'})['request_id']
            self.assertTrue(entered.wait(2))
            self.assertFalse(requests.submit_request('compose.sections', {'topic':'two'})['available'])
            self.assertEqual(requests.request_status(rid)['status'], 'running')
            gate.set(); self.finish(rid)

    def test_bounded_history_and_duplicate_stages(self):
        for i in range(140):
            jobs.append_event('history', str(i), 'Checking sources')
        jobs.append_event('history', '139', 'Checking sources')
        history = jobs.events('history')
        self.assertEqual(len(history['events']), 128)
        self.assertTrue(history['buffer_truncated'])
        self.assertEqual(history['next_cursor'],140)
        self.assertEqual(jobs.events('history',140)['events'], [])

    def test_poll_works_while_data_workers_are_full(self):
        gate, entered = self.gate(), threading.Event()
        rid = self.finish(jobs.start('request:test', lambda: {'ok':True,'data':{}}, {}, progress_events=True)['job_id'])['request_id']
        def blocked():
            entered.set(); gate.wait(3)
        async def check():
            with patch.object(execution, '_DATA_LIMIT', anyio.CapacityLimiter(1)):
                busy = asyncio.create_task(execution.run(blocked))
                while not entered.is_set():
                    await asyncio.sleep(.001)
                try:
                    state = await asyncio.wait_for(execution.run(requests.request_status,rid), .5)
                    self.assertEqual(state['status'],'done')
                finally:
                    gate.set()
                    await busy
        asyncio.run(check())

    def test_rest_prefer_and_generic_object_transport(self):
        requests._REGISTRY['compose.sections'] = lambda topic: {'ok':True, 'data':{'topic':topic}}
        server = FastMCP('async-regression')
        api.install(server, P.REGISTRY)
        with TestClient(server.streamable_http_app()) as c:
            response = c.post('/v1/compose.sections', json={'topic':'Test'}, headers={'Prefer':'respond-async'})
            self.assertEqual(response.status_code,202, response.text)
            self.assertEqual(response.headers['Preference-Applied'], 'respond-async')
            rid = response.json()['data']['request_id']
            self.finish(rid)
            status = c.get(response.headers['Location'])
            self.assertEqual(status.status_code,200,status.text)
            self.assertEqual(status.json()['data']['result']['data']['topic'],'Test')
            generic = c.post('/v1/system.request',json={'feature':'compose.sections','args':{'topic':'Generic'}})
            self.assertEqual(generic.status_code,200,generic.text)
            self.finish(generic.json()['data']['request_id'])
            invalid = c.post('/v1/system.request',json={'feature':'compose.sections','args':[]})
            self.assertEqual(invalid.status_code,400,invalid.text)


if __name__ == '__main__':
    unittest.main()
