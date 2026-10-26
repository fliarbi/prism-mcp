#!/usr/bin/env python3
"""Read-only editor endpoint timing matrix. Does not publish or start jobs.

Usage: python3 benchmark_editor.py --base http://127.0.0.1:8790 --repeat 3
Optional --output stores samples and response envelopes (refuses overwrite).
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import statistics
import time
import urllib.error
import urllib.request

TOPIC='electric vehicle charging in India'
CLAIM='Coffee improves cardiovascular health.'
CASES=[
    ('compose.sections',{'topic':TOPIC}),
    ('compose.section',{'topic':TOPIC,'section':'state_of_evidence'}),
    ('compose.continue',{'topic':TOPIC,'draft':'Charging infrastructure shapes electric vehicle adoption in India.'}),
    ('compose.titles',{'topic':TOPIC}),
    ('research.citations',{'claim':CLAIM,'limit':4}),
    ('research.statistics',{'claim':CLAIM,'limit':4}),
    ('research.evidence',{'claim':CLAIM,'limit':6}),
    ('research.counter_evidence',{'claim':CLAIM}),
    ('research.evidence_card',{'claim':CLAIM}),
    ('research.browse',{'term':TOPIC,'limit':3}),
    ('research.audit',{'text':CLAIM}),
    ('news.trends',{'term':'electric vehicle','granularity':'quarterly'}),
    ('news.recent',{'term':'electric vehicle','limit':3}),
    ('system.jobs',{'limit':3}),
    ('system.features',{}),
    ('system.status',{}),
]


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base',default='http://127.0.0.1:8790')
    p.add_argument('--repeat',type=int,default=3)
    p.add_argument('--workers',type=int,default=4)
    p.add_argument('--timeout',type=float,default=40)
    p.add_argument('--output',type=Path)
    a=p.parse_args()
    if a.output and a.output.exists(): p.error('output already exists')
    def call(case):
        feature,args=case
        started=time.monotonic()
        req=urllib.request.Request(a.base.rstrip('/')+'/v1/'+feature,
            data=json.dumps(args).encode(),headers={'Content-Type':'application/json'})
        try:
            try: response=urllib.request.urlopen(req,timeout=a.timeout)
            except urllib.error.HTTPError as e: response=e
            with response:
                data=json.load(response)
                result={'http':response.code,'ok':data.get('ok'),'response':data}
        except Exception as e: result={'http':None,'ok':False,'transport_error':str(e)}
        result.update(feature=feature,seconds=round(time.monotonic()-started,4))
        return result
    samples=[]
    for trial in range(a.repeat):
        with ThreadPoolExecutor(max_workers=a.workers) as pool:
            for r in pool.map(call,CASES):
                r['trial']=trial+1; samples.append(r)
                print(json.dumps({k:v for k,v in r.items() if k!='response'}),flush=True)
    summaries=[]
    for feature,_ in CASES:
        rows=[r for r in samples if r['feature']==feature]
        times=sorted(r['seconds'] for r in rows)
        summaries.append({'feature':feature,'median_seconds':statistics.median(times),
                          'p95_seconds':times[math.ceil(.95*len(times))-1],
                          'statuses':[r['http'] for r in rows],
                          'successes':sum(bool(r['ok']) for r in rows)})
    report={'checked_at':datetime.now(timezone.utc).isoformat(),'base':a.base,
            'concurrency':a.workers,'samples':samples,'summary':summaries}
    if a.output:
        with a.output.open('x') as f: json.dump(report,f,indent=2)
    print(json.dumps({'summary':summaries},indent=2))


if __name__=='__main__': main()
