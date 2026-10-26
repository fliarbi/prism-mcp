#!/usr/bin/env python3
"""Provisional label-blinded rubric review, not independent factual certification."""
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
import json
from pathlib import Path
import random
import sys
import time
from prism import llm

RUBRIC='''You evaluate research-assistant outputs against the SAME user's task.
The participants are anonymized; do not infer or favor a provider. JSON and prose
are equally acceptable when they deliver the requested material. Some participants
have private corpus measurements while others have the public web. Evaluate scope
and usefulness without assuming either corpus or web search is complete.
This is provisional evaluation from supplied outputs, NOT independent verification
of the cited sources. A URL or confident statement is not proof of factual truth.
Do not claim to have fetched sources. Never use response length as a quality proxy.
For each participant score FOUR dimensions 0-3:
task_fit (addresses exact subject, population, geography, language and requested artifact);
attribution (specific relevant traceable sources and clear attachment to claims;
 for purely provided-data arithmetic/opinion tasks, correct use of given material counts);
scope (causality/quantifiers/units/date/coverage/uncertainty honestly handled);
actionability (usable research/editorial material rather than unrelated filler).
0=absent or seriously wrong; 1=major shortcomings; 2=useful with material caveats;
3=strong for this task. A safe refusal can score 3 on scope and 0-1 on actionability.
An unavailable private statistic is NOT a hallucination; substituting a different
population, outcome, entity or date as the answer is a substantive issue.
Quote short exact excerpts from the supplied outputs to justify major issues.
Report only issues established by the output or supplied task; uncertain source
claims go in needs_verification, not confirmed errors. Distinguish unavailable
data from false output. A grounded:true flag does not establish semantic support.
Return JSON {"ratings":[{"label":"A","task_fit":0,"attribution":0,"scope":0,
"actionability":0,"major_issue":false,"reason":"specific explanation",
"issue_quote":"exact excerpt or empty","needs_verification":["..."]}],
"comparison":"What different value, if any, did the outputs provide?"}.
Include exactly one rating for every supplied label. Do not include model names.'''


def compact(x):
    if isinstance(x,dict):return {k:compact(v) for k,v in x.items() if k not in ('written_by','model','writer_note','queue_seconds','execution_seconds','seconds','provider','fallback')}
    if isinstance(x,list):return [compact(v) for v in x]
    return x


def review(case,base):
    dest=base/'review'/f"{case['id']:02d}.json"
    if dest.exists():return {'id':case['id'],'resumed':True}
    prism=json.loads((base/'prism'/f"{case['id']:02d}.json").read_text())
    answers={'prism':compact(prism.get('first',{}).get('response') or {'unavailable':prism.get('error')})}
    for vendor in ['openai','anthropic']:
        r=json.loads((base/'baseline'/f"{case['id']:02d}-{vendor}.json").read_text())
        answers[vendor]=r['answer'] if not r['error'] else {'unavailable':r['error'],'partial_answer':r['answer']}
    order=list(answers);random.Random(20260912+case['id']).shuffle(order)
    labels=dict(zip('ABC',order));presented={label:answers[vendor] for label,vendor in labels.items()}
    payload={'task':case['question'],'checks':case['checks'],'outputs':presented}
    text=json.dumps(payload,ensure_ascii=False)
    if len(text)>180000:
        return {'id':case['id'],'error':'review_input_too_large'}
    began=time.monotonic();r=llm.call_json(RUBRIC,text,max_tokens=6500)
    if not r or not isinstance(r.get('ratings'),list):return {'id':case['id'],'error':'judge_failed'}
    if {x.get('label') for x in r['ratings']}!=set(labels):return {'id':case['id'],'error':'judge_label_mismatch'}
    for row in r['ratings']:
        row['participant']=labels[row['label']]
        for dim in ['task_fit','attribution','scope','actionability']:
            if type(row.get(dim)) is not int or not 0<=row[dim]<=3:return {'id':case['id'],'error':'invalid_rating'}
        row['total']=sum(row[d] for d in ['task_fit','attribution','scope','actionability'])
        quote=row.get('issue_quote') or ''
        raw=presented[row['label']]
        raw=raw if isinstance(raw,str) else json.dumps(raw,ensure_ascii=False)
        row['issue_quote_present']=not quote or quote in raw or quote.replace('\\n','\n') in raw
    r.update(id=case['id'],labels=labels,judge_model=llm.MODEL,seconds=time.monotonic()-began,
             status='provisional LLM review; independent source verification and manual adjudication separate',
             limitation='Judge is also Prism source-reading model; label blinding does not remove all stylistic/format bias.')
    dest.write_text(json.dumps(r,indent=2,ensure_ascii=False))
    return {'id':case['id'],'scores':{x['participant']:x['total'] for x in r['ratings']}}


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);p.add_argument('--watch',action='store_true');a=p.parse_args()
    (a.output/'review').mkdir(exist_ok=True)
    cases=json.loads((a.output/'dataset.json').read_text())['cases'];attempted=set()
    while True:
        ready=[c for c in cases if c['id'] not in attempted and all(f.exists() for f in [a.output/'prism'/f"{c['id']:02d}.json",a.output/'baseline'/f"{c['id']:02d}-openai.json",a.output/'baseline'/f"{c['id']:02d}-anthropic.json"])]
        with ThreadPoolExecutor(max_workers=2) as pool:
            fs={pool.submit(review,c,a.output):c['id'] for c in ready}
            for f in as_completed(fs):
                try:print(json.dumps(f.result()),flush=True)
                except Exception as e:print(json.dumps({'id':fs[f],'error':str(e)[:400]}),flush=True)
                attempted.add(fs[f])
        if not a.watch or len(attempted)==50:break
        time.sleep(5)
    print('REVIEW FINISHED',len(attempted),flush=True)


if __name__=='__main__':main()
