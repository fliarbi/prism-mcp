"""Offline behavioral regressions. No generation, database queries, or uploads."""
import asyncio
from contextlib import ExitStack
import io
import json
import os
import select
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
TEMP = tempfile.TemporaryDirectory(prefix='prism-regression-')
os.environ['PRISM_CACHE_DIR'] = TEMP.name
import httpx
from starlette.testclient import TestClient
from mcp.server.fastmcp import FastMCP
import prism_mcp as P
from prism import api, cache, ch, charts, envelope, evidence, freshness, jobs, llm, news, stats, writer


class GroundingTests(unittest.TestCase):
    def test_fabricated_quote_suffix_rejected(self):
        source = 'The research team measured output across twelve manufacturing facilities. No improvement was detected.'
        self.assertFalse(llm.verify_quote('The research team measured output across twelve manufacturing facilities and found a 97 percent improvement.', source))

    def test_elided_spans_must_all_match_in_order(self):
        source = 'The trial measured output carefully and found no improvement.'
        self.assertTrue(llm.verify_quote('The trial ... no improvement.', source))
        self.assertFalse(llm.verify_quote('The trial ... 15% improvement.', source))
        self.assertFalse(llm.verify_quote('no improvement ... The trial', source))
        self.assertFalse(llm.verify_quote('The trial ... yes', source))

    def test_real_quote_normalization(self):
        self.assertTrue(llm.verify_quote('Measured 1,284 participants.', 'Measured 1,284 participants.'))
        self.assertTrue(llm.verify_quote('A long-term change.', 'A long–term change.'))

    def test_small_percent_and_unit_mismatch_rejected(self):
        self.assertFalse(writer.ground('Output increased by 15%.', ['Output was measured.'])['grounded'])
        self.assertFalse(writer.ground('Output increased by 35%.', ['The trial had 35 participants.'])['grounded'])
        self.assertEqual(llm.ungrounded_numbers('Output increased by 35%.', ['Output increased by 35 percent.']), [])
        self.assertEqual(llm.ungrounded_numbers('The trial had 35 participants.', ['35 participants enrolled.']), [])

    def test_unverified_verdict_not_counted_as_support(self):
        doc = {'id': 'x', 'title': 'test', 'abstract': 'No improvement was detected.',
               'source': 'test', 'tier_rank': 2, 'cited_by': 0}
        with patch.object(llm, 'call_json', return_value={'verdicts': [
                {'id': 'x', 'stance': 'supports', 'quote': 'Output improved 35 percent.'}]}):
            out = evidence.stance({'claim': 'Output improved.'}, [doc])
        self.assertEqual(out[0]['stance'], 'unread')
        self.assertEqual(evidence.tally(out)['counts']['supports'], 0)
        self.assertEqual(evidence.tally(out)['ungrounded'], 1)

    def test_quantity_sign_is_not_discarded(self):
        self.assertTrue(llm.ungrounded_numbers('Output changed by -35%.', ['Output changed by 35%.']))
        self.assertEqual(llm.ungrounded_numbers('Output changed by -35%.', ['Output changed by −35 percent.']), [])


class TrendTests(unittest.TestCase):
    def test_annualized_monthly_and_quarterly_rates(self):
        for middle in ['2025-07-01', '2025-04-01']:
            out = stats.trend([{'period': '2025-01-01', 'n': 100},
                               {'period': middle, 'n': 150}, {'period': '2026-01-01', 'n': 200}])
            self.assertEqual(out['cagr_pct'], 100)

    def test_zero_is_falling_not_missing(self):
        out = stats.trend([{'period': '2024', 'n': 100}, {'period': '2025', 'n': 50}, {'period': '2026', 'n': 0}])
        self.assertEqual(out['direction'], 'falling')
        self.assertEqual(out['late_vs_early'], 0)

    def test_short_span_has_no_annual_claim(self):
        out = stats.trend([{'period': f'2025-0{i}-01', 'n': i * 100} for i in range(1, 4)])
        self.assertNotIn('cagr_pct', out)

    def test_missing_bucket_and_partial_boundaries(self):
        out = stats.fill_periods([{'period': '2025-01-01', 'n': 12}, {'period': '2025-03-01', 'n': 7}],
                                 'monthly', '2025-01-15', '2025-03-20')
        self.assertEqual([p['n'] for p in out], [12, 0, 7])
        self.assertEqual([p['partial_period'] for p in out], [True, False, True])


class CoverageTests(unittest.TestCase):
    def setUp(self):
        ch._COV_CACHE.clear()

    def test_expiry_rechecks_backend(self):
        n = ch.CORPORA['news']['expected']
        with patch.object(ch, 'chq_int', side_effect=[n, ch.CHError('offline')]) as read:
            first = ch.coverage('news')
            self.assertFalse(first['partial'])
            with patch.object(ch.time, 'time', return_value=first['checked_at'] + ch.COVERAGE_TTL + 1):
                self.assertTrue(ch.coverage('news')['partial'])
            self.assertEqual(read.call_count, 2)

    def test_missing_rows_and_unknown_corpus_not_healthy(self):
        with patch.object(ch, 'chq_int', return_value=int(ch.CORPORA['news']['expected'] * .91)):
            self.assertTrue(ch.coverage('news')['partial'])
        self.assertTrue(ch.coverage('not_a_corpus')['partial'])

    def test_strict_shard_reads_are_default(self):
        response = unittest.mock.MagicMock()
        response.read.return_value = b'1'
        with patch.object(ch.urllib.request, 'urlopen', return_value=response) as get:
            ch.chq('SELECT 1')
        self.assertIn('skip_unavailable_shards=0', get.call_args.args[0].full_url)

    def test_cutoff_measurement_keeps_incomplete_tail(self):
        rows = [['2026-04-01', '3000000'], ['2026-05-01', '2000000'], ['2026-06-01', '400000']]
        with patch.object(cache, 'get', return_value=None), patch.object(cache, 'put'), patch.object(ch, 'chq_rows', return_value=rows):
            out = freshness.news()
        self.assertFalse(out['cutoff_review_needed'])
        self.assertEqual(out['default_until'], '2026-06-01')
        self.assertEqual(out['tail'][0]['fraction_of_baseline'], .16)


class DeliveryTests(unittest.TestCase):
    def test_wrapper_exposes_upload_failure(self):
        with patch.object(charts, 'publish', return_value={'uploaded': False, 'verified': False, 'upload_error': 'offline'}):
            out = P.make_chart(title='Test', points='A:1')
        self.assertFalse(out['ok'])
        self.assertEqual(out['error']['kind'], 'upstream')

    def publish_with(self, actual):
        response = io.BytesIO(actual)
        response.status = 200
        with tempfile.TemporaryDirectory() as d, patch.object(charts, 'LOCAL_DIR', d), \
                patch.object(charts, 'render', return_value=b'png-test'), \
                patch.object(charts.subprocess, 'run'), \
                patch.object(charts.urllib.request, 'urlopen', return_value=response):
            return charts.publish({'kind': 'bars', 'title': 'test'}, themes=('light',))

    def test_public_byte_mismatch_is_not_delivered(self):
        out = self.publish_with(b'wrong')
        self.assertFalse(out['available'])
        self.assertFalse(out['verified'])
        self.assertIsNone(out['url'])
        self.assertEqual(out['embed_markdown'], '')

    def test_public_exact_bytes_are_delivered(self):
        out = self.publish_with(b'png-test')
        self.assertTrue(out['available'])
        self.assertTrue(out['verified'])
        self.assertTrue(out['url'])


class JobTests(unittest.TestCase):
    def setUp(self):
        self.old = jobs._CONN
        jobs._CONN = None
        self.path = jobs.DB_PATH
        jobs.DB_PATH = ':memory:'

    def tearDown(self):
        if jobs._CONN:
            jobs._CONN.close()
        jobs._CONN = self.old
        jobs.DB_PATH = self.path

    def finished(self, result):
        jid = result['job_id']
        for thread in threading.enumerate():
            if thread.name == jid:
                thread.join(3)
        return jobs.status(jid)

    def test_false_result_is_failed_and_retryable(self):
        out = self.finished(jobs.start('test', lambda: {'available': False, 'reason': 'no result'}, {}))
        self.assertEqual(out['status'], 'failed')
        self.assertTrue(out['retryable'])
        self.assertIn('result', out)

    def test_expiry_archives_without_deleting(self):
        out = self.finished(jobs.start('test', lambda: {'available': True}, {}))
        with patch.object(jobs.time, 'time', return_value=time.time() + jobs.KEEP_SECONDS + 1):
            self.assertFalse(jobs.status(out['job_id'])['available'])
            self.assertEqual(jobs.recent()['jobs'], [])
        self.assertEqual(jobs._conn().execute('SELECT count(*) FROM jobs').fetchone()[0], 1)

    def test_dead_owner_is_recoverable_without_automatic_replay(self):
        calls = []
        jobs.register('retry-test', lambda: calls.append(1) or {'available': True})
        c = jobs._conn()
        c.execute('INSERT INTO jobs(id,kind,status,args,created,updated,owner) VALUES (?,?,?,?,?,?,?)',
                  ('dead', 'retry-test', 'running', '{}', time.time(), time.time(), jobs._identity()))
        c.commit()
        with patch.object(jobs, '_owner_alive', return_value=False):
            state = jobs.status('dead')
        self.assertEqual(state['status'], 'failed')
        self.assertEqual(calls, [])
        new = self.finished(jobs.retry('dead'))
        self.assertEqual(new['status'], 'done')
        self.assertEqual(calls, [1])

    def test_execution_slot_is_shared_with_another_process(self):
        env = dict(os.environ, PRISM_JOB_WORKERS='1', PYTHONPATH=str(ROOT))
        script = "from prism import jobs; print('waiting',flush=True); s=jobs._slot(); print('acquired',flush=True); s.close()"
        with patch.object(jobs, 'MAX_RUNNING', 1):
            slot = jobs._slot()
            child = subprocess.Popen([sys.executable, '-u', '-c', script], env=env,
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            try:
                self.assertEqual(child.stdout.readline().strip(), 'waiting')
                self.assertFalse(select.select([child.stdout], [], [], .15)[0])
                slot.close()
                output, err = child.communicate(timeout=5)
                self.assertIn('acquired', output, err)
            finally:
                slot.close()
                if child.poll() is None:
                    child.terminate()
                    child.communicate(timeout=5)

    def test_exited_process_is_not_a_live_owner(self):
        child = subprocess.run([sys.executable, '-c', 'from prism import jobs; print(jobs._identity())'],
                               env=dict(os.environ, PYTHONPATH=str(ROOT)), capture_output=True, text=True, check=True)
        self.assertFalse(jobs._owner_alive(child.stdout.strip()))


class TransportTests(unittest.TestCase):
    def setUp(self):
        server = FastMCP('regression')
        api.install(server, P.REGISTRY)
        self.app = server.streamable_http_app()

    def test_error_envelopes(self):
        with TestClient(self.app) as c:
            cases = [('/v1/news.trends', {'term': None}, 400),
                     ('/v1/news.trends', {}, 400),
                     ('/v1/news.trends', {'term': 'test', 'granularity': 'invalid'}, 400),
                     ('/v1/client.call', {'capability': 'bad'}, 400),
                     ('/v1/system.jobs', {'limit': 'bad'}, 400)]
            for path, args, status in cases:
                r = c.post(path, json=args)
                self.assertEqual(r.status_code, status, r.text)
                self.assertTrue({'ok', 'feature', 'subject', 'data', 'window', 'meta', 'error'} <= r.json().keys())
            self.assertEqual(c.post('/v1/system.features', content='[').status_code, 400)

    def test_upstream_exception_classified(self):
        def broken():
            raise ch.CHError('offline')
        self.assertEqual(envelope.guard('test', broken)['error']['kind'], 'upstream')

    def test_all_registered_features_have_routes_and_schemas(self):
        with TestClient(self.app) as c:
            index = c.get('/v1').json()['features']
            schema = c.get('/v1/openapi.json').json()
            self.assertEqual(len(index), len(P.REGISTRY))
            routes = {r.path for r in self.app.routes}
            for name, spec in P.REGISTRY.items():
                self.assertIn('/v1/' + spec['feature'], routes)
                self.assertIn('/v1/' + name, routes)
                self.assertIn('/v1/' + spec['feature'], schema['paths'])
            self.assertEqual(schema['paths']['/v1/news.compare']['post']['requestBody']['content']
                             ['application/json']['schema']['properties']['terms']['items'], {'type': 'string'})

    def test_slow_data_does_not_block_index(self):
        entered = threading.Event()
        def slow(term: str):
            entered.set()
            time.sleep(.5)
            return envelope.ok('test.slow', {'value': term})
        server = FastMCP('concurrency-test')
        api.install(server, {'slow': {'fn': slow, 'feature': 'test.slow', 'group': 'test'}})
        async def check():
            async with httpx.AsyncClient(transport=httpx.ASGITransport(app=server.streamable_http_app()), base_url='http://localhost') as c:
                data = asyncio.create_task(c.get('/v1/test.slow?term=test'))
                while not entered.is_set():
                    await asyncio.sleep(.005)
                start = time.monotonic()
                self.assertEqual((await c.get('/v1')).status_code, 200)
                self.assertLess(time.monotonic() - start, .2)
                self.assertEqual((await data).status_code, 200)
        asyncio.run(check())

    def test_mcp_lists_all_tools_and_marks_bad_calls(self):
        async def check():
            tools = await P.mcp.list_tools()
            self.assertEqual({t.name for t in tools}, set(P.REGISTRY))
            out = await P.mcp.call_tool('client_call', {'capability': 'bad'})
            self.assertTrue(out.isError)
            self.assertEqual(out.structuredContent['error']['kind'], 'bad_request')
        asyncio.run(check())

    def test_stdio_protocol(self):
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client
        async def check():
            async with stdio_client(StdioServerParameters(command=sys.executable,
                    args=[str(ROOT / 'prism_mcp.py')], env=dict(os.environ))) as io:
                async with ClientSession(io[0], io[1]) as session:
                    await session.initialize()
                    tools = await session.list_tools()
                    self.assertEqual({t.name for t in tools.tools}, set(P.REGISTRY))
                    out = await session.call_tool('client_call', {'capability': 'bad'})
                    self.assertTrue(out.isError)
                    self.assertEqual(out.structuredContent['error']['kind'], 'bad_request')
        asyncio.run(check())


if __name__ == '__main__':
    unittest.main()
