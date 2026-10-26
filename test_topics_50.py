#!/usr/bin/env python3
"""50 input types, 150 live requests; preserves every response and repeat timing.

Each input gets its assigned workflow, a citations/audit cross-check, then an
identical workflow repeat. Run with --output-dir NEW_DIRECTORY. No post import,
publication, chart upload or background generation is requested.
"""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import statistics
import threading
import time
import urllib.error
import urllib.request

ROOT=Path(__file__).resolve().parent
STYLES=['apa','vancouver','harvard','mla','chicago','bibtex','inline_link','footnote','numbered','source_card','wordpress']


def arguments(case,feature):
    topic,text=case['topic'],case['text']
    if feature=='compose.sections' or feature=='compose.titles':return {'topic':topic}
    if feature=='compose.section':return {'topic':topic,'section':'state_of_evidence','background':False}
    if feature=='compose.continue':return {'topic':topic,'draft':text}
    if feature=='research.citations':return {'claim':text,'limit':4,'style':STYLES[(case['id']-1)%len(STYLES)]}
    if feature=='research.audit':return {'text':text,'max_claims':12,'deep':0}
    if feature=='research.browse':return {'term':topic,'limit':4}
    if feature=='research.statistics':return {'claim':text,'limit':4,'include_trend':True}
    return {'claim':text,'limit':6}


def assess(case,feature,status,r):
    issues=[]
    if not isinstance(r,dict) or not isinstance(r.get('ok'),bool):return 'invalid_response',['missing boolean ok']
    for k in ('feature','subject','data','window','meta'):
        if k not in r:issues.append('missing '+k)
    if r.get('feature')!=feature:issues.append('feature mismatch')
    if not r['ok']:
        kind=(r.get('error') or {}).get('kind')
        if not kind:issues.append('missing error kind')
        if kind=='internal' or status==500:return 'application_error',issues
        if kind=='upstream':return 'upstream_blocked',issues
        if case.get('expect')=='rejection':return 'expected_rejection',issues
        return 'no_result',issues
    if case.get('expect')=='rejection':issues.append('empty input accepted')
    d=r.get('data') or {}
    if not isinstance(d,dict):return 'invalid_response',issues+['data is not an object']
    if feature=='research.audit':
        claims=d.get('claims')
        if not isinstance(claims,list):return 'invalid_response',issues+['claims is not a list']
        if d.get('claims_detected')!=len(claims):issues.append('claim count mismatch')
        for c in claims:
            start,end=c.get('start'),c.get('end')
            if not isinstance(start,int) or not isinstance(end,int):issues.append('claim has no source offsets')
            elif case['text'][start:end]!=c.get('sentence'):issues.append('source offsets do not match input')
        unchecked=(d.get('by_status') or {}).get('unchecked',0)
        if unchecked:return 'partial_audit',sorted(set(issues))
        if not claims:return 'no_claims',sorted(set(issues))
    if (r.get('meta',{}).get('coverage') or {}).get('partial'):return 'partial_result',issues
    if feature=='compose.section':
        if not d.get('body') or not d.get('paragraphs'):issues.append('empty section')
        if not (d.get('bibliography') or {}).get('entries'):issues.append('section missing bibliography')
        if d.get('grounded') is not True:return 'flagged_generation',issues
    elif feature=='compose.continue':
        p=d.get('next_paragraph')
        if not isinstance(p,dict) or not p.get('text'):issues.append('invalid continuation shape')
        if not isinstance(p,dict) or p.get('grounded') is not True:return 'flagged_generation',issues
    elif feature=='research.citations':
        entries=d.get('entries') or []
        if not entries:issues.append('empty successful citations')
        if len(entries)>4:issues.append('citation limit exceeded')
        if any(not e.get('citation') for e in entries):issues.append('blank citation')
    elif feature=='compose.sections' and not d.get('sections'):issues.append('empty successful sections')
    elif feature=='compose.titles':
        if not d.get('titles'):issues.append('empty successful titles')
        elif any(t.get('grounded') is not True for t in d['titles']):return 'flagged_generation',issues
    return ('contract_issue' if issues else 'usable_response'),sorted(set(issues))


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--base',default='http://127.0.0.1:8790')
    p.add_argument('--workers',type=int,default=3)
    p.add_argument('--timeout',type=float,default=120)
    p.add_argument('--output-dir',type=Path,required=True)
    a=p.parse_args()
    dataset=ROOT/'tests/topics_50.json';cases=json.loads(dataset.read_text())
    assert len(cases)==50 and len({c['id'] for c in cases})==50
    a.output_dir.mkdir(parents=True,exist_ok=False)
    manifest={'started_at':datetime.now(timezone.utc).isoformat(),'base':a.base,
              'workers':a.workers,'timeout_seconds':a.timeout,
              'dataset_sha256':hashlib.sha256(dataset.read_bytes()).hexdigest(),
              'mode':'live dependencies, no replay or mocks','cases':cases}
    (a.output_dir/'manifest.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
    lock=threading.Lock();results=[]
    def call(case,feature,stage):
        args=arguments(case,feature);t=time.monotonic()
        req=urllib.request.Request(a.base.rstrip('/')+'/v1/'+feature,data=json.dumps(args).encode(),headers={'Content-Type':'application/json'})
        sample={'case_id':case['id'],'type':case['type'],'feature':feature,'stage':stage,'args':args}
        try:
            try:response=urllib.request.urlopen(req,timeout=a.timeout)
            except urllib.error.HTTPError as e:response=e
            with response:raw=response.read();status=response.code
            sample['http']=status
            try:r=json.loads(raw)
            except (ValueError,UnicodeError):r={'raw':raw[:1000].decode(errors='replace')}
            sample['response']=r
            sample['outcome'],sample['issues']=assess(case,feature,status,r)
        except Exception as e:
            sample.update(http=None,outcome='transport_error',issues=[str(e)])
        sample['seconds']=round(time.monotonic()-t,4)
        with lock:
            results.append(sample)
            with (a.output_dir/'responses.jsonl').open('a') as f:f.write(json.dumps(sample,ensure_ascii=False)+'\n')
        return sample
    def run_case(case):
        feature=case['endpoint']
        cross='research.audit' if feature=='research.citations' else 'research.citations'
        rows=[call(case,feature,'first'),call(case,cross,'cross_check'),call(case,feature,'repeat')]
        print(json.dumps({'case':case['id'],'type':case['type'],'results':[{k:r[k] for k in ('feature','stage','seconds','outcome','issues')} for r in rows]},ensure_ascii=False),flush=True)
    with ThreadPoolExecutor(max_workers=a.workers) as pool:
        for f in as_completed([pool.submit(run_case,c) for c in cases]):f.result()
    summary={'finished_at':datetime.now(timezone.utc).isoformat(),'cases':50,'requests':len(results),
             'outcomes':dict(Counter(r['outcome'] for r in results)),
             'http_statuses':dict(Counter(str(r['http']) for r in results)),
             'issues':[{'case':r['case_id'],'feature':r['feature'],'stage':r['stage'],'issues':r['issues']} for r in results if r['issues']],
             'endpoints':[]}
    for feature in sorted({r['feature'] for r in results}):
        rows=[r for r in results if r['feature']==feature];times=sorted(r['seconds'] for r in rows)
        summary['endpoints'].append({'feature':feature,'requests':len(rows),'median_seconds':statistics.median(times),
                                     'max_seconds':max(times),'outcomes':dict(Counter(r['outcome'] for r in rows))})
    (a.output_dir/'summary.json').write_text(json.dumps(summary,indent=2))
    lines=['# Prism MCP: 50 diverse input tests','',
           'Live dependencies; no mocks or archived evidence. Timed-out client requests are not treated as cancelled server work.',
           'Response usefulness is assessed separately from HTTP/JSON validity. A usable response is not an independent factual accuracy certification.','',
           '## Outcomes','',f"{len(results)} requests across 50 inputs and {len(summary['endpoints'])} endpoints.",'',
           '| Outcome | Requests |','|---|---:|']
    lines += [f'| {k} | {v} |' for k,v in summary['outcomes'].items()]
    lines += ['','## Per-input results','','| # | Input type | Primary endpoint | First seconds / outcome | Repeat seconds / outcome | Cross-check outcome |','|---:|---|---|---|---|---|']
    for c in cases:
        rows={r['stage']:r for r in results if r['case_id']==c['id']}
        first,repeat,cross=rows['first'],rows['repeat'],rows['cross_check']
        lines.append(f"| {c['id']} | {c['type']} | {c['endpoint']} | {first['seconds']} / {first['outcome']} | {repeat['seconds']} / {repeat['outcome']} | {cross['outcome']} |")
    lines += ['','## Files','','- `manifest.json`: every input and invocation settings.',
              '- `responses.jsonl`: all inputs, complete response envelopes, timings and checks.',
              '- `summary.json`: endpoint statistics and exact issues.','']
    (a.output_dir/'REPORT.md').write_text('\n'.join(lines))
    print(json.dumps(summary,indent=2),flush=True)


if __name__=='__main__':main()
