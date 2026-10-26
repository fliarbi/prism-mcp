#!/usr/bin/env python3
"""Systematic DOI identity spot-checks; metadata existence is not claim support."""
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
import json
from pathlib import Path
import re
import time
from urllib.parse import quote
import httpx

DOI=re.compile(r'10\.\d{4,9}/[^\s<>"\\\[\]`*]+',re.I)


def dois(value):
    found=[]
    def walk(x):
        if isinstance(x,dict):
            for k,v in x.items():
                if k in ('doi','url','citation') and isinstance(v,str):
                    for d in DOI.findall(v):
                        d=d.rstrip('.,;]}')
                        # Keep balanced parentheses that are part of a DOI.
                        while d.count(')')>d.count('('):d=d[:-1]
                        if d.lower() not in [y.lower() for y in found]:found.append(d)
                elif isinstance(v,(dict,list)):walk(v)
        elif isinstance(x,list):
            for y in x:walk(y)
        elif isinstance(x,str):
            for d in DOI.findall(x):
                d=d.rstrip('.,;]}')
                while d.count(')')>d.count('('):d=d[:-1]
                if d.lower() not in [y.lower() for y in found]:found.append(d)
    walk(value)
    return found


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--watch',action='store_true');p.add_argument('--directory',default='source-checks-v2');a=p.parse_args()
    target=a.output/a.directory;target.mkdir(exist_ok=True)
    attempted=set()
    while True:
        associations=[]
        for f in sorted((a.output/'prism').glob('*.json')):
            try:r=json.loads(f.read_text())
            except ValueError:continue
            for d in dois(r.get('first',{}).get('response'))[:2]:associations.append({'id':r['id'],'participant':'prism','doi':d})
        for f in sorted((a.output/'baseline').glob('*.json')):
            try:r=json.loads(f.read_text())
            except ValueError:continue
            for d in dois(r['answer'])[:2]:associations.append({'id':r['id'],'participant':r['vendor'],'doi':d})
        (target/'associations.json').write_text(json.dumps(associations,indent=2))
        unique=list(dict.fromkeys(row['doi'].lower() for row in associations))
        def check(d):
            import hashlib
            dest=target/(hashlib.sha256(d.encode()).hexdigest()[:20]+'.json')
            if dest.exists():return
            old=a.output/'source-checks'/dest.name
            if old.exists():
                prior=json.loads(old.read_text())
                if prior.get('status')==200:
                    prior['reused_initial_success']=True
                    dest.write_text(json.dumps(prior,indent=2));return
            tick=time.monotonic()
            try:
                r=httpx.get('https://api.crossref.org/works/'+quote(d,safe=''),headers={'User-Agent':'PrismResearchBenchmark/1.0'},timeout=20)
                row={'doi':d,'status':r.status_code,'seconds':time.monotonic()-tick}
                if r.status_code==200:
                    x=r.json()['message'];row.update(title=x.get('title'),publisher=x.get('publisher'),type=x.get('type'),published=x.get('published'),url=x.get('URL'),returned_doi=x.get('DOI'))
                elif r.status_code==404:row['note']='Not found in Crossref; another registration agency or identifier parsing may apply. Not by itself proof of fabrication.'
            except Exception as e:row={'doi':d,'error':type(e).__name__,'seconds':time.monotonic()-tick}
            dest.write_text(json.dumps(row,indent=2))
            time.sleep(.5)
        with ThreadPoolExecutor(max_workers=1) as pool:
            for _ in pool.map(check,[d for d in unique if d not in attempted]):pass
        attempted.update(unique)
        complete=len(list((a.output/'baseline').glob('*.json')))==100 and len(list((a.output/'prism').glob('*.json')))==50
        print('DOI identities checked',len(attempted),'associations',len(associations),flush=True)
        if not a.watch or complete:break
        time.sleep(30)


if __name__=='__main__':main()
