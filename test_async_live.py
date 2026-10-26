#!/usr/bin/env python3
"""Live read-only editor request/progress QA. No posts, uploads or schema changes."""
import argparse
import asyncio
import json
import statistics
import time
from pathlib import Path
import httpx


async def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output',type=Path,required=True)
    a=parser.parse_args()
    a.output.mkdir(parents=True,exist_ok=False)
    cases=[
        ('compose.sections',{'topic':'retrieval practice in classrooms'}),
        ('compose.section',{'topic':'retrieval practice in classrooms','section':'state_of_evidence'}),
        ('research.citations',{'claim':'Urban tree cover is associated with lower surface temperatures during summer heat waves.','limit':4}),
        ('research.statistics',{'claim':'Drip irrigation reduces agricultural water consumption compared with flood irrigation.','include_context':False,'include_trend':False,'limit':4}),
        ('news.themes',{'term':'electric vehicle','limit':4}),
        ('news.sentiment',{'term':'electric vehicle','granularity':'quarterly'}),
    ]
    summaries=[]
    async with httpx.AsyncClient(base_url='http://127.0.0.1:8790',timeout=30) as client:
        for i,(feature,args) in enumerate(cases):
            began=time.monotonic()
            if i%2:
                response=await client.post('/v1/'+feature,json=args,headers={'Prefer':'respond-async'})
                assert response.status_code==202,response.text
                assert 'Location' in response.headers
            else:
                response=await client.post('/v1/system.request',json={'feature':feature,'args':args})
                assert response.status_code==200,response.text
            ack=time.monotonic()-began
            start=response.json()
            assert start['ok'],start
            rid=start['data']['request_id']
            polls=[];events=[];cursor=0
            while time.monotonic()-began < 300:
                tick=time.monotonic()
                r=await client.get('/v1/system.request_status',params={'request_id':rid,'after':cursor})
                seconds=time.monotonic()-tick
                assert r.status_code==200,r.text
                state=r.json()['data']
                fresh=state['events']
                assert all(e['sequence']>cursor for e in fresh),state
                assert state['next_cursor']>=cursor,state
                cursor=state['next_cursor'];events.extend(fresh)
                polls.append({'seconds':seconds,'status':state['status'],'cursor':cursor})
                if state['status'] in ('done','failed'):
                    break
                await asyncio.sleep(.5)
            else:
                raise RuntimeError(f'Request still running after 300s: {rid}; do not resubmit')
            result=state.get('result') or {}
            assert isinstance(result.get('ok'),bool),state
            assert events, state
            row={'feature':feature,'request_id':rid,'ack_seconds':ack,
                 'total_seconds':time.monotonic()-began,'status':state['status'],
                 'result_ok':result['ok'],'poll_count':len(polls),
                 'poll_median_ms':statistics.median(p['seconds'] for p in polls)*1000,
                 'poll_max_ms':max(p['seconds'] for p in polls)*1000,
                 'stages':[e['stage'] for e in events]}
            summaries.append(row)
            (a.output/f'{i+1}-{feature}.json').write_text(json.dumps({'summary':row,'ack':start,'polls':polls,'events':events,'terminal':state},indent=2))
            print(json.dumps(row),flush=True)
        # Input/allowlist rejection never creates a generation or publication job.
        for feature,args in [('compose.article',{}),('system.request',{}),('research.citations',{'claim':'test','limit':'invalid'})]:
            r=await client.post('/v1/system.request',json={'feature':feature,'args':args})
            assert r.status_code==400,r.text
        assert (await client.get('/v1/system.request_status',params={'request_id':'missing'})).status_code==404
        assert (await client.get('/v1/system.request_status',params={'request_id':'missing','after':-1})).status_code==400
        assert (await client.get('/livez')).status_code==200
        index=(await client.get('/v1')).json()
        (a.output/'index.json').write_text(json.dumps(index,indent=2))
    (a.output/'summary.json').write_text(json.dumps(summaries,indent=2))
    print('COMPLETE: six live requests, cursor/status contracts and rejection checks',flush=True)


if __name__=='__main__':
    asyncio.run(main())
