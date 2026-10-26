#!/usr/bin/env python3
"""One isolated-cache case, profiling real dependencies; no production mutation."""
import argparse
import copy
from contextvars import ContextVar
import functools
import hashlib
import json
import os
from pathlib import Path
import threading
import time

p=argparse.ArgumentParser();p.add_argument('--dataset',type=Path,required=True);p.add_argument('--id',type=int,required=True);p.add_argument('--server-pid',type=int,required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
for item in Path(f'/proc/{a.server_pid}/environ').read_bytes().split(b'\0'):
    if item.startswith(b'PRISM_') and b'=' in item:
        k,v=item.decode().split('=',1);os.environ[k]=v
import prism_mcp as P
from prism import cache,ch,query,evidence,compose,stats,article,browse,news,vocab,llm,writer,availability,progress
memo={};lock=threading.RLock();spans=[];updates=[];seq=0;began=time.monotonic();phase='first';parent=ContextVar('profile_parent',default=None)
def get(k):
    with lock:
        x=memo.get(k)
        return copy.deepcopy(x[0]) if x and x[1]>time.time() else None
def put(k,v,ttl=43200):
    with lock:memo[k]=(copy.deepcopy(v),time.time()+ttl)
cache.get=get;cache.put=put
def wrap(module,name):
    original=getattr(module,name)
    @functools.wraps(original)
    def timed(*args,**kw):
        global seq
        with lock:seq+=1;sid=seq
        row={'id':sid,'parent':parent.get(),'phase':phase,'name':module.__name__+'.'+name,'start':time.monotonic()-began}
        if module is ch and name=='_request':row['sql']=args[0];row['sql_sha256']=hashlib.sha256(args[0].encode()).hexdigest()
        token=parent.set(sid)
        try:
            out=original(*args,**kw)
            if isinstance(out,dict):row.update(available=out.get('available'),cached=out.get('cached'))
            return out
        except Exception as e:
            row['error']=type(e).__name__+': '+str(e)[:500];raise
        finally:
            parent.reset(token);row['end']=time.monotonic()-began;row['seconds']=row['end']-row['start']
            with lock:spans.append(row)
    setattr(module,name,timed)
for module,names in {
 query:['build','_spec','resolve_pole','_label_phrase_check','_cooccur_filter','audit','discover_terms','discover_mesh','_lane_counts','_volumes','topics','_rescue_phrases'],
 compose:['context','_context','_news_term','_apply_scope','section_candidates','write_section','continue_paragraph'],
 evidence:['fetch_docs','corpus_stance','stance','profile','disease_evidence'],
 stats:['find_statistics','series'],article:['extract_claims','batch_counts','audit'],browse:['browse','variants'],
 news:['recent_news','critical_news','themes','trends','sentiment','sources','entities','geography','compare_terms','trending_topics'],
 vocab:['embed'],llm:['text','call_json'],writer:['compose'],ch:['_request','coverage_of'],availability:['check_sql']}.items():
    for name in names:
        if hasattr(module,name):wrap(module,name)
case=next(c for c in json.loads(a.dataset.read_text())['cases'] if c['id']==a.id)
fn=next(s['fn'] for s in P.REGISTRY.values() if s['feature']==case['feature'])
result={'id':a.id,'case':case,'models':{'reader':llm.MODEL,'writer':writer.WRITER_MODEL},'transport':'in-process live API registry, not network latency'}
for phase in ['first','repeat']:
    tick=time.monotonic()
    with progress.track(lambda stage,message:updates.append({'phase':phase,'stage':stage,'message':message,'seconds':time.monotonic()-began})):
        response=fn(**case['args'])
    result[phase]={'seconds':time.monotonic()-tick,'response':response}
    result.update(spans=spans,progress=updates)
    a.output.write_text(json.dumps(result,indent=2,ensure_ascii=False,default=str))
print(json.dumps({'id':a.id,'ok':result['first']['response']['ok'],'seconds':result['first']['seconds']}))
