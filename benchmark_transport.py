#!/usr/bin/env python3
"""Bounded live REST smoke checks, separate from 50 handler timings."""
import json
from pathlib import Path
import time
import httpx

dest=Path('out/usecases-50-20260912/transport.json');out={}
with httpx.Client(base_url='http://127.0.0.1:8790',timeout=30) as client:
    def request(method,path,**kwargs):
        t=time.monotonic();r=client.request(method,path,**kwargs)
        try:body=r.json()
        except ValueError:body=r.text[:300]
        return {'http':r.status_code,'seconds':time.monotonic()-t,'body':body,'preference_applied':r.headers.get('Preference-Applied')}
    out['catalog']=request('GET','/v1')
    out['async_submit']=request('POST','/v1/news.sentiment',headers={'Prefer':'respond-async'},json={'term':'nuclear energy','since':'2024-06-01','until':'2026-06-01'})
    payload=out['async_submit']['body'];data=payload.get('data') or payload;rid=data.get('request_id')
    out['polls']=[]
    if rid:
        cursor=0
        for _ in range(60):
            row=request('GET','/v1/system.request_status',params={'request_id':rid,'after':cursor});out['polls'].append(row)
            d=row['body'].get('data') or {};cursor=d.get('next_cursor',cursor)
            dest.write_text(json.dumps(out,indent=2,ensure_ascii=False))
            if d.get('status') in ['done','failed']:break
            time.sleep(1)
        out['cursor_replay']=request('GET','/v1/system.request_status',params={'request_id':rid,'after':cursor})
        out['invalid_cursor']=request('GET','/v1/system.request_status',params={'request_id':rid,'after':-1})
    out['unsupported_readonly']=request('POST','/v1/system.request',json={'feature':'news.geography','args':{'term':'drought'}})
    out['missing_id']=request('GET','/v1/system.request_status',params={'request_id':'benchmark-does-not-exist-20260912'})
dest.write_text(json.dumps(out,indent=2,ensure_ascii=False))
print(json.dumps({k:{'http':v['http'],'seconds':v['seconds'],'body':v['body']} for k,v in out.items() if k not in ['catalog','polls','cursor_replay']},ensure_ascii=False)[:3000])
print('polls',len(out['polls']),'final',out['polls'][-1]['body'].get('data',{}).get('status') if out['polls'] else None)
