#!/usr/bin/env python3
"""Read-only dependency profiler; in-memory wrappers, isolated result cache.

Production Python modules and the running service are never modified. Uses
real model/database reads; no posts, jobs, indexes or production caches written.
"""
import argparse
import copy
import functools
import hashlib
import json
import os
from pathlib import Path
import threading
import time


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--server-pid',type=int,required=True)
    parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--editor-lean',action='store_true',help='Use the WordPress statistics options without unused context or trend')
    a=parser.parse_args();a.output.mkdir(parents=True,exist_ok=False)
    # Preserve actual server settings without printing credentials.
    for item in Path(f'/proc/{a.server_pid}/environ').read_bytes().split(b'\0'):
        if item.startswith(b'PRISM_') and b'=' in item:
            key,value=item.decode().split('=',1);os.environ[key]=value
    import prism_mcp as server
    from prism import cache,ch,query,evidence,compose,stats,article,browse,news,vocab,llm,writer,availability
    memo={};lock=threading.RLock();local=threading.local();seq=0
    def get(key):
        with lock:
            item=memo.get(key)
            return copy.deepcopy(item[0]) if item and item[1]>time.time() else None
    def put(key,value,ttl=43200):
        with lock:memo[key]=(copy.deepcopy(value),time.time()+ttl)
    cache.get=get;cache.put=put
    start=time.monotonic();events=[];current={'case':None}
    def wrap(module,name):
        original=getattr(module,name)
        @functools.wraps(original)
        def timed(*args,**kwargs):
            nonlocal seq
            parent=getattr(local,'parent',None)
            with lock:seq+=1;sid=seq
            event={'id':sid,'parent':parent,'case':current['case'],
                   'name':module.__name__+'.'+name,'start':time.monotonic()-start,
                   'thread':threading.get_ident()}
            if module is ch and name=='_request':
                sql=args[0];event.update(sql=sql,sql_sha256=hashlib.sha256(sql.encode()).hexdigest())
            local.parent=sid
            try:
                out=original(*args,**kwargs)
                if isinstance(out,dict):
                    event['available']=out.get('available');event['cached']=out.get('cached')
                return out
            except Exception as e:
                event['error']=type(e).__name__+': '+str(e)[:500];raise
            finally:
                event['end']=time.monotonic()-start;event['seconds']=event['end']-event['start'];local.parent=parent
                with lock:
                    events.append(event)
                    with (a.output/'spans.jsonl').open('a') as f:f.write(json.dumps(event)+'\n')
        setattr(module,name,timed)
    # Thread propagation preserves causal parents across ch.parallel fanout.
    parallel=ch.parallel
    def fanout(fns,workers=6):
        parent=getattr(local,'parent',None)
        def bind(fn):
            def call():
                old=getattr(local,'parent',None);local.parent=parent
                try:return fn()
                finally:local.parent=old
            return call
        return parallel([bind(fn) for fn in fns],workers=workers)
    ch.parallel=fanout
    modules={
      query:['build','_spec','resolve_pole','_label_phrase_check','_cooccur_filter','audit','discover_terms','discover_mesh','_lane_counts','_volumes','topics','_rescue_phrases'],
      compose:['context','_context','_news_term','_apply_scope','section_candidates','write_section'],
      evidence:['fetch_docs','corpus_stance','stance','profile','disease_evidence'],
      stats:['find_statistics','series'],article:['extract_claims','batch_counts'],
      browse:['browse','variants'],news:['recent_news','critical_news','themes','trends','sentiment'],
      vocab:['embed'],llm:['text','call_json'],writer:['compose'],
      ch:['_request','coverage_of'],availability:['check_sql']}
    for module,names in modules.items():
        for name in names:
            if hasattr(module,name):wrap(module,name)
    cases=[
      ('sections-cold','compose.sections',{'topic':'retrieval practice in classrooms'}),
      ('section-shared-context','compose.section',{'topic':'retrieval practice in classrooms','section':'state_of_evidence','background':False}),
      ('sections-repeat','compose.sections',{'topic':'retrieval practice in classrooms'}),
      ('citations-cold','research.citations',{'claim':'Urban tree cover is associated with lower surface temperatures during summer heat waves.','limit':4,'style':'apa'}),
      ('statistics-cold','research.statistics',{'claim':'Drip irrigation reduces agricultural water consumption compared with flood irrigation.','limit':4,'include_trend':True}),
      ('statistics-repeat','research.statistics',{'claim':'Drip irrigation reduces agricultural water consumption compared with flood irrigation.','limit':4,'include_trend':True})]
    if a.editor_lean:
        for label,feature,args in cases:
            if feature == 'research.statistics':
                args.update(include_context=False,include_trend=False)
    manifest={'server_pid':a.server_pid,'cache':'isolated in-memory; no prior result reuse',
              'mode':'sequential calls, live dependencies, in-process API registry',
              'writer_model':writer.WRITER_MODEL,'reader_model':llm.MODEL,'cases':cases}
    (a.output/'manifest.json').write_text(json.dumps(manifest,indent=2))
    for label,feature,args in cases:
        current['case']=label;t=time.monotonic()
        fn=next(x['fn'] for x in server.REGISTRY.values() if x['feature']==feature)
        result=fn(**args)
        row={'case':label,'feature':feature,'args':args,'seconds':time.monotonic()-t,'response':result}
        with (a.output/'responses.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
        print(json.dumps({k:v for k,v in row.items() if k not in ['response','args']}|{'ok':result.get('ok'),'error':result.get('error')}),flush=True)
    print('COMPLETE',len(events),'spans',flush=True)


if __name__=='__main__':main()
