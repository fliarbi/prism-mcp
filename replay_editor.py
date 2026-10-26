#!/usr/bin/env python3
"""Real writer / REST replay on archived evidence; never publishes to WordPress.

This deliberately replaces retrieval with a previously stored bundle. Results
and timings are NOT a claim about fresh retrieval or current corpus coverage.
"""
import argparse
import copy
import json
import os
from pathlib import Path
import sqlite3
import tempfile
import time
from unittest.mock import patch


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--topic',default='electric vehicle charging in India')
    a=p.parse_args()
    if a.output.exists(): p.error('output exists')
    source=Path(__file__).parent/'cache/prism_cache.db'
    with sqlite3.connect(f'file:{source}?mode=ro',uri=True) as c:
        row=c.execute("SELECT v,made FROM kv WHERE json_extract(v,'$.topic')=? "
                      "AND json_type(v,'$.research.documents')='array' ORDER BY made DESC LIMIT 1",(a.topic,)).fetchone()
    if not row: p.error('no archived evidence bundle for topic')
    ctx=json.loads(row[0])
    with tempfile.TemporaryDirectory(prefix='prism-editor-replay-') as tmp:
        os.environ['PRISM_CACHE_DIR']=tmp
        import prism_mcp as P
        from prism import compose,evidence
        from mcp.server.fastmcp import FastMCP
        from starlette.testclient import TestClient
        server=FastMCP('archived-replay')
        P.api.install(server,P.REGISTRY)
        report={'mode':'archived evidence + live writer; no fresh retrieval',
                'topic':a.topic,'source_cache_made':row[1],
                'documents':len(ctx['research']['documents']),'samples':[]}
        profile={'available':True,'documents':ctx['research']['documents'],'coverage':ctx.get('coverage')}
        cases=[('compose.sections',{'topic':a.topic}),
               ('research.citations',{'claim':a.topic,'style':'apa','limit':4}),
               ('compose.section',{'topic':a.topic,'section':'state_of_evidence'}),
               ('compose.continue',{'topic':a.topic,'draft':f'Research on {a.topic} needs careful interpretation across study designs.'}),
               ('compose.titles',{'topic':a.topic})]
        with TestClient(server.streamable_http_app()) as client, \
             patch.object(compose,'context',side_effect=lambda *args,**kw:copy.deepcopy(ctx)), \
             patch.object(P,'_qo',return_value={'available':True,'claim':a.topic}), \
             patch.object(evidence,'profile',return_value=profile):
            for feature,args in cases:
                for trial in (1,2):
                    t=time.monotonic(); r=client.post('/v1/'+feature,json=args); result=r.json()
                    sample={'feature':feature,'trial':trial,'http':r.status_code,
                            'seconds':round(time.monotonic()-t,4),'response':result}
                    report['samples'].append(sample)
                    d=result.get('data') or {}
                    print(json.dumps({k:v for k,v in sample.items() if k!='response'} | {
                        'ok':result.get('ok'),'grounded':d.get('grounded',(d.get('next_paragraph') or {}).get('grounded')),
                        'cached':result.get('meta',{}).get('cached'),'model':d.get('written_by')}),flush=True)
        with a.output.open('x') as f: json.dump(report,f,indent=2,default=str)


if __name__=='__main__':main()
