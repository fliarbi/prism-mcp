#!/usr/bin/env python3
"""Summarize saved measurements; never use the experimental judge as truth."""
import collections
import hashlib
import json
from pathlib import Path
import statistics

root=Path(__file__).resolve().parent
p=root/'out/usecases-50-20260912'
def read(f): return json.loads(f.read_text())
def dist(xs):
    xs=sorted(xs)
    if not xs:return {'n':0}
    def quant(q):
        t=(len(xs)-1)*q;i=int(t)
        return xs[i]+(xs[min(i+1,len(xs)-1)]-xs[i])*(t-i)
    return {'n':len(xs),'median':statistics.median(xs),'p90':quant(.9),'p95':quant(.95),'max':max(xs),'mean':statistics.mean(xs)}
def union(spans):
    end=-1;total=0
    for s in sorted(spans,key=lambda s:s['start']):
        total+=max(0,s['end']-max(end,s['start']));end=max(end,s['end'])
    return total
cases=[];stages=collections.defaultdict(list);sql=[]
for f in sorted((p/'prism').glob('*.json')):
    d=read(f)
    if 'first' not in d:
        cases.append({'id':d.get('id'),'error':d.get('error'),'completed':False});continue
    first=d['first'];sp=[s for s in d['spans'] if s['phase']=='first'];qs=[s for s in sp if s['name']=='prism.ch._request']
    events=sorted([(s['start'],1) for s in qs]+[(s['end'],-1) for s in qs]);n=peak=0
    for _,change in events:n+=change;peak=max(peak,n)
    stage={}
    for name in set(s['name'] for s in sp):
        ss=[s for s in sp if s['name']==name];stage[name]=union(ss);stages[name].append(stage[name])
    for s in qs:sql.append({'case_id':d['id'],**s})
    rr=first['response'];repeat=d.get('repeat',{})
    cases.append({'id':d['id'],'group':d['case']['group'],'feature':d['case']['feature'],'name':d['case']['name'],'completed':bool(repeat),'first_seconds':first['seconds'],'repeat_seconds':repeat.get('seconds'),'ok':rr.get('ok'),'error':rr.get('error'),'sql_calls':len(qs),'sql_union_seconds':union(qs),'sql_sum_seconds':sum(s['seconds'] for s in qs),'sql_peak_concurrent':peak,'stage_union_seconds':stage,'progress_events':len([x for x in d['progress'] if x['phase']=='first'])})
valid=[c for c in cases if 'first_seconds' in c]
byfeature={}
for feature in sorted(set(c['feature'] for c in valid)):
    cs=[c for c in valid if c['feature']==feature]
    byfeature[feature]={'first':dist([c['first_seconds'] for c in cs]),'repeat':dist([c['repeat_seconds'] for c in cs if c['repeat_seconds'] is not None]),'ok':sum(bool(c['ok']) for c in cs),'sql_calls':dist([c['sql_calls'] for c in cs])}
models={}
for condition in ['baseline','augmented']:
    models[condition]={}
    for vendor in ['openai','anthropic']:
        runs=[read(f) for f in sorted((p/condition).glob('*-'+vendor+'.json'))];details=[]
        for d in runs:
            transcript=d.get('transcript',[]);tools=[]
            for e in transcript:
                if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='web_search':tools.append(e['item'].get('action',{}).get('type','unknown'))
                if e.get('type')=='assistant':
                    tools += [b.get('name') for b in e.get('message',{}).get('content',[]) if b.get('type')=='tool_use']
            terminal=d.get('terminal',{});errors=[e for e in transcript if e.get('type') in ['error','turn.failed']]
            details.append({'id':d['id'],'seconds':d['seconds'],'error':d.get('error'),'exit_code':d.get('exit_code'),'terminal_error':terminal.get('is_error',False),'transcript_errors':errors,'answer_words':len(d.get('answer','').split()),'empty_answer':not bool(d.get('answer','').strip()),'requested_model':d['requested_model'],'returned_models':list(terminal.get('modelUsage',{})),'tool_calls':dict(collections.Counter(tools)),'usage':terminal.get('usage') or next((e.get('usage') for e in reversed(transcript) if e.get('type')=='turn.completed'),None),'provider_list_cost_usd':terminal.get('total_cost_usd')})
        models[condition][vendor]={'seconds':dist([d['seconds'] for d in details]),'answer_words':dist([d['answer_words'] for d in details]),'errors':sum(bool(d['error'] or d['terminal_error'] or d['empty_answer'] or d['exit_code']) for d in details),'runs':details}
source=[]
for f in (p/'source-checks-v2').glob('*.json'):
    if f.name!='associations.json':source.append(read(f))
summary={'complete_prism':sum(c.get('completed',False) for c in cases),'first':dist([c['first_seconds'] for c in valid]),'repeat':dist([c['repeat_seconds'] for c in valid if c['repeat_seconds'] is not None]),'ok':sum(bool(c['ok']) for c in valid),'non_ok':[{k:c[k] for k in ['id','feature','error']} for c in valid if not c['ok']],'sql_calls':dist([c['sql_calls'] for c in valid]),'sql_union_seconds':dist([c['sql_union_seconds'] for c in valid]),'sql_union_fraction_pooled':sum(c['sql_union_seconds'] for c in valid)/sum(c['first_seconds'] for c in valid),'by_feature':byfeature,'by_group':{g:dist([c['first_seconds'] for c in valid if c['group']==g]) for g in sorted(set(c['group'] for c in valid))},'stage_union_seconds':{name:dist(xs) for name,xs in stages.items()},'cases':cases,'models':models,'source_identity_checks':len(source),'source_status':dict(collections.Counter(str(s.get('status')) for s in source)),'source_keys':list(source[0]) if source else [],'code_sha256':{str(f.relative_to(root)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [root/'prism_mcp.py',*sorted((root/'prism').glob('*.py')),*sorted(root.glob('benchmark*.py')),root/'profile_usecase.py']},'warnings':['Exploratory seeded stratified sample, single generation per condition.','No automated judge quality scores accepted.','Prism handler timings exclude Python startup; CLI timings include setup.','SQL intervals overlap; sums are not elapsed wall time.','OpenAI requested model is recorded, but its JSON stream does not independently report a returned model identifier.','Metadata resolution is not source support verification.']}
(p/'summary.json').write_text(json.dumps(summary,indent=2,ensure_ascii=False))
(p/'slow-sql.json').write_text(json.dumps(sorted(sql,key=lambda s:s['seconds'],reverse=True)[:25],indent=2,ensure_ascii=False))
print(json.dumps({k:summary[k] for k in ['complete_prism','first','repeat','ok','non_ok','sql_calls','sql_union_fraction_pooled','by_group','source_identity_checks','source_status']},indent=2))
for condition,vs in models.items():
    for v,m in vs.items():print(condition,v,json.dumps({k:m[k] for k in ['seconds','errors','answer_words']}))
