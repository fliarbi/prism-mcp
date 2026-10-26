#!/usr/bin/env python3
"""Offline quality/latency review of the 50-input live run; never calls APIs.

Heuristics are review flags, not factual truth labels. Raw responses remain
untouched. The report separates first/cross/repeat and successful/censored
latencies, since blending warm calls or client timeouts is misleading.
"""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import re
import statistics


def distribution(rows):
    values=sorted(r['seconds'] for r in rows)
    if not values:return {'n':0}
    return {'n':len(values),'median_seconds':round(statistics.median(values),4),
            'p90_seconds':values[max(0,math.ceil(.9*len(values))-1)],
            'max_seconds':values[-1]}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('directory',type=Path)
    a=p.parse_args()
    rows=[json.loads(line) for line in (a.directory/'responses.jsonl').read_text().splitlines()]
    manifest=json.loads((a.directory/'manifest.json').read_text())
    cases={c['id']:c for c in manifest['cases']}
    flags=[]
    for row in rows:
        response=row.get('response') or {}
        if not response.get('ok'):continue
        data=response.get('data') or {};feature=row['feature'];issues=[]
        if feature=='research.evidence':
            docs=data.get('documents') or []
            if not any(d.get('grounded') and d.get('stance') in ('supports','qualifies','contradicts') for d in docs):
                issues.append('No verified relevant document verdict: not useful evidence merely because ok=true')
        if feature=='research.counter_evidence':
            if not data.get('contradicting'):
                issues.append('No counter-evidence returned; distinguish honest empty result from a counter-evidence success')
        if feature=='research.statistics':
            stats=data.get('stats') or []
            if not stats:issues.append('No extracted statistics')
            for stat in stats:
                if not stat.get('sentence') or not stat.get('source'):
                    issues.append('Statistic missing source sentence or attribution')
                # This is only a lexical check against the returned sentence,
                # not independent verification against the stored abstract.
                value=str(stat.get('value') or '')
                if value and value not in str(stat.get('sentence') or ''):
                    issues.append('Statistic value is not an exact substring of its returned sentence')
        if feature=='research.citations':
            rendered=data.get('rendered') or []
            if any(c.get('stance')=='unread' for c in rendered):
                issues.append('Citation includes unread source: relevance/support is not verified and should be visible in the UI')
        if feature in ('compose.section','compose.continue'):
            paragraphs=[data] if feature=='compose.section' else [data.get('next_paragraph') or {}]+(data.get('alternatives') or [])
            for paragraph in paragraphs:
                body=paragraph.get('body') or paragraph.get('text') or ''
                if feature=='compose.continue' and not 60 <= len(body.split()) <= 120:
                    issues.append('Continuation length outside the writer prompt target of 60-120 whitespace-delimited words')
                if paragraph.get('grounded') and re.search(
                    r'does not (?:address|assess)|do not address|outside (?:pollination|the topic)|'
                    r'not (?:vitamin D|about the subject)|no relevant finding|rather than vitamin D|'
                    r'cannot (?:establish whether|support a finding)|cannot evaluate|'
                    r'koi finding assess nahi|support nahi kar sakta',body,re.I):
                    issues.append('Grounded output explicitly disclaims topic relevance: manual review required')
        if feature=='compose.titles':
            for title in data.get('titles') or []:
                if title.get('grounded') and re.search(r'\b(?:to address|aims? to|objective)\b',title.get('rests_on') or '',re.I):
                    issues.append('Grounded title cites a study aim rather than an outcome: manual review required')
        if feature=='research.audit':
            if row['case_id']==49 and response.get('feature')!='research.audit':
                issues.append('Embedded instruction escaped endpoint response contract')
            if row['case_id']==30:
                citations=data.get('citations') or {}
                if any('10.0000/prism-test-nonexistent' in json.dumps(x) for x in citations.get('resolved_in_corpus') or []):
                    issues.append('Invented DOI incorrectly resolved')
        if issues:flags.append({'case':row['case_id'],'type':cases[row['case_id']]['type'],
                                'feature':feature,'stage':row['stage'],'flags':sorted(set(issues))})
    timing={}
    for stage in ('first','cross_check','repeat'):
        subset=[r for r in rows if r['stage']==stage]
        timing[stage]={'all_client_observations':distribution(subset),
                       'completed_http_responses':distribution([r for r in subset if r.get('http') is not None]),
                       'timeouts_or_transport_errors':sum(r.get('http') is None for r in subset)}
    pairs=[]
    for case_id in cases:
        stages={r['stage']:r for r in rows if r['case_id']==case_id}
        first,repeat=stages.get('first'),stages.get('repeat')
        if first and repeat and first.get('response',{}).get('ok') and repeat.get('response',{}).get('ok'):
            pairs.append({'case':case_id,'feature':first['feature'],
                          'first_seconds':first['seconds'],'repeat_seconds':repeat['seconds'],
                          'ratio':round(first['seconds']/max(repeat['seconds'],.0001),2)})
    report={'requests':len(rows),'completed_cases':sum(r['stage']=='repeat' for r in rows),
            'timing':timing,'successful_pairs':pairs,'quality_flags':flags,
            'endpoint_stage_timing':{
                feature:{stage:distribution([r for r in rows if r['feature']==feature and r['stage']==stage and r.get('http') is not None])
                         for stage in ('first','cross_check','repeat')}
                for feature in sorted({r['feature'] for r in rows})},
            'unique_cases_flagged':len({f['case'] for f in flags}),
            'first_endpoint_outcomes':dict(Counter(r['outcome'] for r in rows if r['stage']=='first')),
            'limitations':['Cold means first request in this suite; existing shared caches were not cleared.',
                           'Three concurrent cases share infrastructure; measurements are not isolated service times.',
                           'Timeouts are censored client observations; server work can continue after disconnect.',
                           'Automated quality flags require manual interpretation; absence of a flag is not proof of factual accuracy.',
                           'deep=0 audit measures literature coverage, not a deep verification of every claim.']}
    output=a.directory/'quality-and-latency.json'
    with output.open('x') as f:json.dump(report,f,indent=2,ensure_ascii=False)
    print(json.dumps({k:v for k,v in report.items() if k!='successful_pairs'},indent=2,ensure_ascii=False))


if __name__=='__main__':main()
