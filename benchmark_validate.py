#!/usr/bin/env python3
"""Validate completed task artifacts and write a content-hash inventory."""
import hashlib
import json
from pathlib import Path
import re

p=Path('out/usecases-50-20260912')
checks={}
for name,n in [('prism',50),('baseline',100),('augmented',20),('review',50)]:
    fs=list((p/name).glob('*.json'));assert len(fs)==n,(name,len(fs))
    for f in fs:json.loads(f.read_text())
    checks[name+'_records']=len(fs)
for f in (p/'prism').glob('*.json'):
    d=json.loads(f.read_text());assert d.get('first') and d.get('repeat'),f
ids=[c['id'] for c in json.loads((p/'dataset.json').read_text())['cases']]
assert sorted(ids)==list(range(1,51))
assert len(re.findall(r'^## \d', (p/'CASES.md').read_text(),re.M))==50
for f in p.glob('*.md'):
    for link in re.findall(r'\]\(([^)]+)\)',f.read_text()):
        if not link.startswith(('http:','https:','#')):
            assert (f.parent/link.split('#')[0]).exists(),(f,link)
wire=json.loads((p/'mcp-wire.json').read_text())
assert len(wire['list_tools']['names'])==58
assert wire['research_audit']['result']['structuredContent']['data']['claims_detected']==0
transport=json.loads((p/'transport.json').read_text())
assert transport['async_submit']['http']==202
assert transport['polls'][-1]['body']['data']['status']=='done'
assert transport['cursor_replay']['body']['data']['events']==[]
checks.update(prism_first_and_repeat=50,manual_case_assessments=50,mcp_tools=58,async_terminal='done',local_markdown_links='valid',experimental_judge_failed_cases=[36,49],quality_scores_accepted=False)
files={}
for f in sorted(p.rglob('*')):
    if f.is_file() and f.name!='manifest.json':
        data=f.read_bytes();files[str(f.relative_to(p))]={'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
(p/'manifest.json').write_text(json.dumps({'checks':checks,'files':files},indent=2))
print(json.dumps({'checks':checks,'artifact_files':len(files),'artifact_bytes':sum(x['bytes'] for x in files.values())},indent=2))
