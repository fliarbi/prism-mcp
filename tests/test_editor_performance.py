"""Editor contracts and latency regressions with deterministic dependencies.

These fixtures prove application behavior; they do not certify live corpus or
model availability. All cache and job data stays in a temporary directory.
"""
import asyncio
import copy
import json
import os
from pathlib import Path
import tempfile
import threading
import time
import unittest
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch, MagicMock

from test_regressions import TEMP  # one cache root, including subprocess tests
import httpx
from starlette.testclient import TestClient
import prism_mcp as P
from prism import availability, cache, ch, compose, evidence, execution, query, writer, llm


def context_fixture():
    docs = [{'id':f'test:{i}', 'title':'Output trial', 'authors':['Ava Smith'],
             'year':2024, 'venue':'Test Journal', 'source':'openalex', 'type':'article',
             'tier':'randomized_trial', 'tier_rank':8, 'strength':'strong',
             'cited_by':1, 'url':f'https://example.org/{i}', 'doi':None,
             'abstract':'The trial measured output. No improvement was detected.',
             'quote':'No improvement was detected.', 'grounded':True,
             'stance':'qualifies', 'institutions':[]} for i in range(4)]
    return {'available':True, 'topic':'output', 'query':{},
            'research':{'documents':docs, 'stance_mix':{}, 'series':None},
            'news':{'recent':[], 'critical':[]}, 'coverage':{'partial':False}}


class AvailabilityTests(unittest.TestCase):
    def test_only_all_dead_replicas_fail_a_required_shard(self):
        topology = ({'test.table':'cluster'}, {'cluster':{'1':[('a',1),('b',1)]}})
        with patch.object(availability, '_topology', return_value=topology), \
             patch.object(availability, '_reachable', side_effect=lambda x:x[0]=='b'):
            availability.require_tables(['test.table'])
        with patch.object(availability, '_topology', return_value=topology), \
             patch.object(availability, '_reachable', return_value=False):
            with self.assertRaises(ch.CHError): availability.require_tables(['test.table'])
            availability.require_tables(['unrelated.local_table'])

    def test_topology_reads_once_and_maps_actual_cluster(self):
        with patch.object(availability, '_TOPOLOGY', ({},{},0)), \
             patch.object(ch, '_request', side_effect=["test\ttable\tDistributed(\\'c\\', \\'d\\', \\'t\\', rand())\n", 'c\t1\t127.0.0.1\t9000\n']) as read:
            first = availability._topology()
            self.assertEqual(first[0]['test.table'],'c')
            self.assertEqual(first, availability._topology())
            self.assertEqual(read.call_count,2)

    def test_failure_probe_recovers_after_short_ttl(self):
        address=('test.invalid',9000)
        with patch.object(availability, '_PROBES', {}), \
             patch.object(availability.time, 'monotonic', return_value=100), \
             patch.object(availability.socket, 'create_connection', side_effect=OSError('offline')) as connect:
            self.assertFalse(availability._reachable(address))
            self.assertFalse(availability._reachable(address))
            self.assertEqual(connect.call_count,1)
            with patch.object(availability.time, 'monotonic', return_value=104), \
                 patch.object(availability.socket, 'create_connection', return_value=MagicMock()):
                self.assertTrue(availability._reachable(address))

    def test_outage_stops_before_model_or_false_no_data(self):
        with patch.object(cache,'get',return_value=None), \
             patch.object(availability,'require_tables',side_effect=ch.CHError('storage offline')), \
             patch.object(query,'_spec') as model:
            r=P.get_citations('A claim')
            self.assertFalse(r['ok'])
            self.assertEqual(r['error']['kind'],'upstream')
            model.assert_not_called()

    def test_coverage_parallel_and_failure_expiry(self):
        with patch.object(ch,'_COV_CACHE',{}), patch.object(ch,'chq_int',side_effect=ch.CHError('offline')) as read:
            ch.coverage('news'); ch.coverage('news')
            self.assertEqual(read.call_count,1)
            with patch.object(ch.time,'time',return_value=time.time()+4):
                ch.coverage('news')
            self.assertEqual(read.call_count,2)
        def slow(name):
            time.sleep(.06)
            return {'corpus':name,'partial':False}
        with patch.object(ch,'coverage',side_effect=slow):
            start=time.monotonic(); r=ch.coverage_of(list(ch.CORPORA))
            self.assertLess(time.monotonic()-start,.3)
            self.assertEqual(len(r['tables']),8)


class ReuseTests(unittest.TestCase):
    def test_default_context_skips_unused_analytics(self):
        docs=context_fixture()['research']['documents']
        with patch.object(cache,'get',return_value=None), patch.object(cache,'put'), \
             patch.object(query,'build',return_value={'available':True,'claim':'test'}), \
             patch.object(evidence,'fetch_docs',return_value=docs), \
             patch.object(evidence,'corpus_stance',return_value={}), \
             patch.object(evidence,'stance',return_value=docs), \
             patch.object(compose.workflows,'source_fit',return_value=docs), \
             patch.object(compose.browse,'browse',return_value={}) as browse_call, \
             patch.object(compose.stats,'series',return_value={}), \
             patch.object(ch,'coverage_of',return_value={'partial':False}), \
             patch.object(compose,'_news_term',return_value=('test',None)), \
             patch.object(compose.news,'recent_news',return_value={}), \
             patch.object(compose.news,'critical_news',return_value={}), \
             patch.object(compose.news,'trends',return_value={}), \
             patch.object(compose.news,'themes',return_value={}) as themes_call, \
             patch.object(compose.news,'sentiment',return_value={}) as sentiment_call:
            first=compose.context('analytics fixture')
            self.assertTrue(first['available']); self.assertTrue(first['analytics_deferred'])
            browse_call.assert_not_called(); themes_call.assert_not_called(); sentiment_call.assert_not_called()
            full=compose.context('analytics fixture',with_analytics=True)
            self.assertFalse(full['analytics_deferred'])
            self.assertEqual(browse_call.call_count,1); self.assertEqual(themes_call.call_count,1)
            self.assertEqual(sentiment_call.call_count,1)

    def test_editor_statistics_skip_extra_scans_but_preserve_defaults(self):
        with patch.object(P,'_qo',return_value={'available':True}) as build, \
             patch.object(evidence,'fetch_docs',return_value=[]) as fetch, \
             patch.object(P.stats,'find_statistics',return_value={'available':True,'stats':[]}) as extract, \
             patch.object(P.stats,'series',return_value={}) as series:
            lean=P.find_statistics('test',include_context=False,include_trend=False)
            self.assertTrue(lean['ok']); self.assertTrue(lean['data']['context_deferred'])
            self.assertEqual(build.call_args.kwargs['depth'],'quick'); series.assert_not_called()
            self.assertEqual(fetch.call_count,1); self.assertEqual(extract.call_count,1)
            P.find_statistics('test')
            self.assertEqual(build.call_args.kwargs['depth'],'full'); self.assertEqual(series.call_count,2)

    def test_verified_statistics_cache_invalidates_changed_sources(self):
        docs=[{'id':'test:stat','title':'Water trial','year':2024,'abstract':'Water consumption fell by 25% in this trial.'}]
        result={'stats':[{'doc_id':'test:stat','value':'25%','sentence':docs[0]['abstract']}]}
        with patch.object(llm,'call_json',return_value=result) as model:
            first=P.stats.find_statistics({'claim':'statistics caching fixture'},docs)
            second=P.stats.find_statistics({'claim':'statistics caching fixture'},docs)
            self.assertTrue(first['available']); self.assertTrue(second['cached'])
            self.assertEqual(model.call_count,1)
            changed=copy.deepcopy(docs); changed[0]['abstract']='Water consumption fell by 15% in this trial.'
            last=P.stats.find_statistics({'claim':'statistics caching fixture'},changed)
            self.assertEqual(model.call_count,2); self.assertFalse(last['available'])

    def test_unrelated_verified_quotes_cannot_support_composition(self):
        ctx=context_fixture()
        ctx['research']['documents']=[{**d,'stance':'unrelated'} for d in ctx['research']['documents']]
        with patch.object(compose,'context',return_value=ctx),patch.object(writer,'compose') as model:
            for result in [P.write_section('unrelated test','state_of_evidence'),
                           P.suggest_sections('unrelated test'),
                           P.continue_paragraph('A draft.','unrelated test')]:
                self.assertFalse(result['ok'])
            model.assert_not_called()

    def test_stance_reused_across_limits_but_not_changed_claim_or_source(self):
        docs=context_fixture()['research']['documents'][:2]
        def verdicts(*args,**kwargs):
            return {'verdicts':[{'id':d['id'],'stance':'qualifies','quote':d['quote']} for d in docs]}
        with patch.object(llm,'call_json',side_effect=verdicts) as model:
            evidence.stance({'claim':'stance reuse test'},docs[:1])
            evidence.stance({'claim':'stance reuse test'},docs)
            evidence.stance({'claim':'stance reuse test'},docs)
            self.assertEqual(model.call_count,2)
            evidence.stance({'claim':'different stance claim'},docs)
            self.assertEqual(model.call_count,3)
            changed=copy.deepcopy(docs); changed[0]['abstract']='The source changed.'
            result=evidence.stance({'claim':'stance reuse test'},changed)
            self.assertEqual(model.call_count,4)
            self.assertFalse(next(v for v in result if v['id']==docs[0]['id'])['grounded'])

    def test_unavailable_section_does_not_generate(self):
        ctx=context_fixture()
        ctx['research']['documents']=[{**d,'stance':'supports'} for d in ctx['research']['documents']]
        with patch.object(compose,'context',return_value=ctx),patch.object(writer,'compose') as model:
            result=P.write_section('no counter evidence test','counter_evidence')
            self.assertFalse(result['ok']); model.assert_not_called()

    def test_concurrent_identical_reads_run_once_and_return_independent_data(self):
        calls=[]
        @cache.singleflight
        def work(x=1):
            calls.append(x); time.sleep(.1); return {'items':[x]}
        with ThreadPoolExecutor(max_workers=8) as pool:
            results=list(pool.map(lambda _:work(),range(8)))
        self.assertEqual(calls,[1]); results[0]['items'].append(2)
        self.assertEqual(results[1],{'items':[1]})

    def test_failures_are_not_retained(self):
        calls=[]
        @cache.singleflight
        def work():
            calls.append(1); raise RuntimeError('offline')
        for _ in range(2):
            with self.assertRaises(RuntimeError): work()
        self.assertEqual(len(calls),2)

    def test_partial_and_ungrounded_results_are_never_memoized(self):
        @cache.remember(60)
        def work(mode):
            return {'available':True,'coverage':{'partial':mode=='partial'},'grounded':mode!='bad'}
        with patch.object(cache,'get',return_value=None), patch.object(cache,'put') as save:
            work('partial'); work('bad'); save.assert_not_called()
            work('good'); self.assertEqual(save.call_count,1)

    def test_section_preserves_paragraphs_and_reuses_grounded_completion(self):
        ctx=context_fixture()
        with patch.object(compose,'context',return_value=ctx), \
             patch.object(writer,'compose',return_value={'text':'Findings\n\nThe trial measured output.\n\nNo improvement was detected.','model':'test'}) as generate:
            a=P.write_section('editor-test-unique','state_of_evidence')
            b=P.write_section('editor-test-unique','state_of_evidence')
            self.assertTrue(a['ok'],a)
            self.assertTrue(a['data']['grounded'],a)
            self.assertEqual(len(a['data']['paragraphs']),2)
            self.assertTrue(a['data']['bibliography']['entries'])
            self.assertEqual(generate.call_count,1)
            self.assertTrue(b['meta']['cached'])

    def test_outline_and_section_share_full_context(self):
        docs=context_fixture()['research']['documents']
        q={'available':True,'claim':'shared context test','poles':{}}
        with patch.object(query,'build',return_value=q) as build, \
             patch.object(evidence,'fetch_docs',return_value=docs), \
             patch.object(evidence,'corpus_stance',return_value={}), \
             patch.object(evidence,'stance',return_value=docs) as read, \
             patch.object(compose.workflows,'source_fit',return_value=docs), \
             patch.object(compose.browse,'browse',return_value={}), \
             patch.object(compose.stats,'series',return_value={}), \
             patch.object(ch,'coverage_of',return_value={'partial':False}), \
             patch.object(compose,'_news_term') as news_term:
            compose.context('shared context test',limit=10,with_news=False)
            second=compose.context('shared context test',limit=14,with_news=False)
            self.assertTrue(second['cached'])
            self.assertEqual(build.call_count,1); self.assertEqual(read.call_count,1)
            news_term.assert_not_called()

    def test_supplied_profile_docs_do_not_trigger_retrieval(self):
        docs=context_fixture()['research']['documents']
        with patch.object(cache,'get',return_value=None), patch.object(cache,'put'), \
             patch.object(evidence,'fetch_docs') as fetch, \
             patch.object(evidence,'corpus_stance',return_value={}), \
             patch.object(ch,'coverage_of',return_value={'partial':False}):
            r=evidence.profile({'available':True,'claim':'test'},docs=docs,read=False)
            self.assertEqual(r['documents'],docs); fetch.assert_not_called()


class EditorTransportTests(unittest.TestCase):
    def test_failed_provider_cooldown_expires_and_does_not_hide_transient_errors(self):
        with patch.object(writer,'_PROVIDER_FAILURES',{}), \
             patch.object(writer,'_anthropic_call',side_effect=RuntimeError('credit balance is too low')) as primary, \
             patch.object(llm,'text',return_value='Fallback prose.'):
            first=writer.compose('sys','text',model='claude-test')
            second=writer.compose('sys','different text',model='claude-test')
            self.assertTrue(first['fallback']); self.assertEqual(second['fallback_reason'],'no API credit')
            self.assertEqual(primary.call_count,1)
            expiry=writer._PROVIDER_FAILURES['claude-test'][1]
            with patch.object(writer.time,'monotonic',return_value=expiry+1):
                writer.compose('sys','retry',model='claude-test')
            self.assertEqual(primary.call_count,2)
            writer._provider_failed('transient',TimeoutError('temporary timeout'),'timeout')
            self.assertIsNone(writer._provider_block('transient'))

    def test_article_model_override_reaches_section_writer(self):
        ctx=context_fixture()
        with patch.object(compose,'context',return_value=ctx), \
             patch.object(compose,'route',return_value={'mode':'research'}), \
             patch.object(writer,'compose',return_value={'text':'Findings\n\nNo improvement was detected.','model':'chosen-model'}) as model:
            result=P.write_article(title='Model override test',topic='output',sections='state_of_evidence',background=False,model='chosen-model')
            self.assertTrue(result['ok'],result)
            self.assertEqual(model.call_args.kwargs['model'],'chosen-model')

    def test_background_section_poll_returns_grounded_result(self):
        ctx=context_fixture()
        with patch.object(compose,'context',return_value=ctx), \
             patch.object(writer,'compose',return_value={'text':'Findings\n\nNo improvement was detected.','model':'test'}):
            start=P.write_section('background fixture','state_of_evidence',background=True)
            self.assertTrue(start['ok'],start)
            jid=start['data']['job_id']
            deadline=time.monotonic()+2
            while time.monotonic()<deadline:
                result=P.job_status(jid)
                if result['data']['status'] in ('done','failed'):break
                time.sleep(.01)
            self.assertEqual(result['data']['status'],'done',result)
            self.assertTrue(result['data']['result']['grounded'])

    def test_citation_validation_precedes_retrieval(self):
        with patch.object(P,'_qo') as query_call:
            for args in [{'style':'invented'},{'limit':0},{'limit':51}]:
                r=P.get_citations('Test',**args)
                self.assertEqual(r['error']['kind'],'bad_request')
            query_call.assert_not_called()

    def test_citation_styles_have_real_entries(self):
        docs=context_fixture()['research']['documents']
        with patch.object(P,'_qo',return_value={'available':True}), \
             patch.object(evidence,'profile',return_value={'documents':docs,'coverage':{'partial':False}}):
            for style in P.cite.STYLES:
                r=P.get_citations('Test',style,2)
                self.assertTrue(r['ok'],r)
                self.assertEqual(len(r['data']['entries']),2)
                self.assertTrue(all(e['citation'] for e in r['data']['entries']))

    def test_job_poll_does_not_queue_behind_composition(self):
        async def scenario():
            import anyio
            release=threading.Event()
            started=threading.Event()
            def slow(): started.set(); release.wait(2)
            def job_status(): return {'ok':True,'feature':'system.job','data':{}}
            with patch.object(execution,'_DATA_LIMIT',anyio.CapacityLimiter(1)):
                task=asyncio.create_task(execution.run(slow))
                while not started.is_set(): await asyncio.sleep(.005)
                try:
                    t=time.monotonic()
                    result=await asyncio.wait_for(execution.run(job_status),.3)
                    self.assertLess(time.monotonic()-t,.3)
                    self.assertIn('queue_seconds',result['meta'])
                finally: release.set(); await task
        asyncio.run(scenario())

    def test_populated_rest_responses_use_plugin_shapes(self):
        ctx=context_fixture()
        from mcp.server.fastmcp import FastMCP
        server=FastMCP('editor-test')
        P.api.install(server,P.REGISTRY)
        with TestClient(server.streamable_http_app()) as client, \
             patch.object(compose,'context',return_value=ctx), \
             patch.object(writer,'compose',return_value={'text':'The trial measured output.\n\n---\n\nNo improvement was detected.','model':'test'}):
            r=client.post('/v1/compose.continue',json={'draft':'Output was studied.','topic':'rest fixture'})
            self.assertEqual(r.status_code,200,r.text)
            self.assertIsInstance(r.json()['data']['next_paragraph'],dict)
            r=client.post('/v1/compose.sections',json={'topic':'rest fixture'})
            self.assertEqual(r.status_code,200,r.text)
            self.assertTrue(r.json()['data']['sections'])


if __name__=='__main__': unittest.main()
