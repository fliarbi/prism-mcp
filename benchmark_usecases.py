#!/usr/bin/env python3
"""Seeded, resumable research-usefulness benchmark. Never publishes or edits production."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import time

ROOT=Path(__file__).resolve().parent
SEED=20260912


def candidates():
    rows=[]
    def add(group,name,feature,args,question,checks):
        rows.append(dict(candidate_id=len(rows)+1,group=group,name=name,feature=feature,args=args,question=question,checks=checks))
    evidence=[
      ('learning','Spaced retrieval practice improves long-term retention compared with rereading.','Distinguish retention from immediate test performance.'),
      ('agriculture','Drip irrigation reduces irrigation water use compared with flood irrigation.','Distinguish water withdrawals, consumption and crop yield.'),
      ('urban heat','Urban trees reduce daytime surface temperatures during heat waves.','Do not equate land-surface temperature with air temperature.'),
      ('workplace','A four-day workweek improves employee wellbeing without reducing organizational productivity.','Discuss selection bias and limits of generalization.'),
      ('software','Retrieval-augmented generation eliminates hallucinations in language models.','Reject the absolute claim; retrieval does not guarantee factuality.'),
      ('nutrition','Intermittent fasting causes greater long-term weight loss than continuous calorie restriction.','Distinguish superiority from comparable outcomes; no personal medical advice.')]
    for name,claim,check in evidence:
        add('evidence',name,'research.evidence',{'claim':claim,'limit':6},f'Assess this claim using research, give relevant sources and explain limitations: {claim}',check)
    opposition=[
      ('education quantifier','Homework improves achievement for every primary-school pupil.','An average improvement cannot establish every pupil benefits.'),
      ('remote work','Remote work always increases productivity.','Identify task, measurement and selection differences.'),
      ('EV lifecycle','Electric vehicles have zero lifecycle greenhouse-gas emissions.','Distinguish tailpipe emissions from manufacturing and electricity.'),
      ('correlation','Coffee drinkers have lower mortality, therefore prescribing coffee will extend life.','Association does not establish an intervention effect.'),
      ('negation','Exercise does not improve depression symptoms in every adolescent.','Average benefit is not a contradiction of not every.'),
      ('climate','One unusually cold winter disproves long-term global warming.','Separate weather variability from long-run climate trends.')]
    for name,claim,check in opposition:
        add('counterarguments',name,'research.counter_evidence',{'claim':claim,'limit':6},f'Find evidence that contradicts or qualifies this claim. Explain precisely which part is challenged: {claim}',check)
    citations=[
      ('APA teaching','Testing practice improves delayed retention.','apa'),
      ('Vancouver exercise','Resistance training improves muscle strength in older adults.','vancouver'),
      ('BibTeX databases','Column-oriented databases are efficient for analytical workloads.','bibtex'),
      ('Hindi groundwater','भारत में भूजल का अत्यधिक दोहन कृषि की स्थिरता को प्रभावित करता है।','apa'),
      ('Spanish urbanism','Las zonas verdes urbanas se asocian con un mejor bienestar psicológico.','apa'),
      ('fabricated technology','A randomized trial proved that quantum banana batteries doubled human lifespan in 2025.','apa')]
    for name,claim,style in citations:
        add('references',name,'research.citations',{'claim':claim,'style':style,'limit':4},f'Find up to four relevant research references in {style} format for: {claim} Include DOI or source URLs; do not invent references.', 'Verify source identity and direct relevance; explicitly decline the fabricated premise.' if name=='fabricated technology' else 'References must exist and address the claim; disclose sources not actually read.')
    stats=[
      ('solar learning','Solar photovoltaic module prices have fallen as cumulative production increased.'),
      ('building retrofit','Building insulation reduces household heating energy consumption.'),
      ('water treatment','Membrane filtration removes microplastics from drinking water.'),
      ('mangroves','Mangrove restoration reduces coastal storm damage.'),
      ('AI efficiency','Quantizing large language models reduces inference memory requirements.'),
      ('provided spreadsheet','In this supplied dataset, revenue was 100 in 2023 and 120 in 2024. Calculate the percentage increase using only these two values.')]
    for name,claim in stats:
        add('figures',name,'research.statistics',{'claim':claim,'limit':4,'include_context':False,'include_trend':False},f'Find useful figures for this statement, with original source sentences, units and limitations: {claim}', 'The provided-data answer is 20%; literature search cannot validate these invented business records.' if name=='provided spreadsheet' else 'Each number must match its source sentence; distinguish population, units and outcome.')
    outlines=[
      ('education explainer','retrieval practice for adult language learning','compose.sections'),
      ('climate headlines','cool roofs for urban heat adaptation','compose.titles'),
      ('policy outline','congestion pricing and urban traffic','compose.sections'),
      ('technology headlines','small language models on edge devices','compose.titles'),
      ('regional outline','rainwater harvesting in Bengaluru','compose.sections'),
      ('niche headlines','biochar for soil water retention','compose.titles')]
    for name,topic,feature in outlines:
        add('editorial_planning',name,feature,{'topic':topic},f'Propose evidence-supported {"article sections" if feature.endswith("sections") else "headlines"} for {topic}. Explain the evidence or limitation behind each option.', 'Suggestions must fit the exact topic and geography; a study objective is not a finding.')
    writing=[
      ('classroom section','formative feedback in higher education','compose.section',''),
      ('housing section','ventilation and indoor carbon dioxide in schools','compose.section',''),
      ('recycling section','mechanical recycling of polyethylene terephthalate','compose.section',''),
      ('generic last sentence','urban cycling infrastructure and road safety','compose.continue','Protected cycle lanes aim to make everyday journeys safer. This is an important issue.'),
      ('Hinglish continuation','drip irrigation in smallholder farms','compose.continue','Chhote kisano ke liye paani bachana zaroori hai. Drip irrigation ke fayde aur limitations samajhna chahiye.'),
      ('causal continuation','heat exposure and labor productivity','compose.continue','Hotter working conditions are associated with lower output in several settings. That does not mean every workplace faces the same effect.')]
    for name,topic,feature,draft in writing:
        args={'topic':topic,'section':'state_of_evidence','background':False} if feature.endswith('section') else {'topic':topic,'draft':draft}
        add('writing',name,feature,args,f'Write {"one evidence-led article section" if feature.endswith("section") else "the next paragraph"} about {topic}, with sources and limitations. '+(f'Continue this draft: {draft}' if draft else ''),'Relevant source-backed prose; preserve topic, uncertainty and requested language; do not substitute neighboring topics.')
    audits=[
      ('HTML offsets','<p>Regular <strong>physical activity</strong> is associated with lower mortality.</p><p>This observation alone proves exercise will extend every individual life.</p>'),
      ('opinion only','I love rainy mornings. In my opinion, blue is the nicest color. Please make this article cheerful.'),
      ('business records','Our fictional startup earned $7.4 million yesterday. Our private dashboard shows 92% retention. Verify these numbers without access to our records.'),
      ('arithmetic contradiction','In this synthetic trial 12 of 40 participants improved. Therefore 60% improved. This demonstrates that all future patients will recover.'),
      ('mixed causality','Students assigned retrieval practice scored higher on delayed tests in some studies. Therefore rereading never works and every student should stop using it.'),
      ('citation spoof','A 2025 Nature study (doi:10.0000/prism-fictional-2025) proved electric cars have no environmental impacts. This means battery manufacturing creates zero emissions.')]
    for name,draft in audits:
        add('draft_review',name,'research.audit',{'text':draft,'max_claims':8,'deep':0},f'Audit this draft. Separate opinion, arithmetic, unverifiable private records and research claims; identify overstatement and invalid citations: {draft}','No fake verification of private records; 12/40=30%, not 60%; validate any cited DOI; literature coverage is not a truth score.')
    discovery=[
      ('critical AI literature','research.browse',{'term':'retrieval augmented generation','orientation':'critical','limit':6},'Find critical research on retrieval-augmented generation and explain the main limitations.'),
      ('regional agriculture','research.browse',{'term':'groundwater depletion','geo':'India','limit':6},'Find research about groundwater depletion in India, distinguishing study location from author affiliation.'),
      ('new battery research','research.radar',{'topic':'sodium ion batteries','since_year':2024},'What changed in sodium-ion battery research since 2024? Give sources and the latest date actually covered.'),
      ('topic omission','research.missing',{'text':'Urban heat policies should plant more trees. Trees provide shade.','subject':'urban heat adaptation','limit':5},'What important evidence-backed urban-heat adaptation topics are missing from a draft that discusses only tree shade?'),
      ('research versus attention','research.geography',{'claim':'Offshore wind power is expanding.','country':'United Kingdom'},'Compare UK offshore-wind research and news attention with other countries. Do not equate document counts with installed capacity.'),
      ('paper strength','research.source_ranking',{'claim':'School-based physical activity improves child wellbeing.','limit':6},'Rank sources on school-based physical activity and child wellbeing, explaining study design and strength.')]
    for name,feature,args,question in discovery:
        add('research_discovery',name,feature,args,question,'Return sources or measurements answering the requested filter; disclose coverage and time bounds.')
    monitor=[
      ('company coverage','news.recent',{'term':'Nvidia','limit':5},'Show the five latest available news articles about Nvidia, with dates and source links.'),
      ('entity ambiguity','news.recent',{'term':'Apple','limit':5},'Find recent news about Apple the technology company, not apples the fruit.'),
      ('important regulation','news.critical',{'term':'artificial intelligence regulation','limit':5},'Find important developments in artificial-intelligence regulation, prioritize significance over recency and show source dates.'),
      ('brand comparison','news.compare',{'terms':['Tesla','BYD'],'granularity':'quarterly','since':'2025-01-01','until':'2026-06-01'},'Compare Tesla and BYD news attention from January 2025 through May 2026. Separate media attention from vehicle sales.'),
      ('freshness challenge','news.recent',{'term':'semiconductor','since':'2026-09-01','until':'2026-09-13','limit':5},'What semiconductor developments were reported from 1 to 12 September 2026? If your data does not reach those dates, say so.'),
      ('trending topics','news.trending',{'days':30,'limit':5},'Which news subjects are rising most in the latest available 30-day window? Define rising and state the actual data window.')]
    for name,feature,args,question in monitor:
        add('news_monitoring',name,feature,args,question,'Real resolvable article links and dates; historical coverage must not be passed off as current; disclose sampling and window.')
    insights=[
      ('tone baseline','news.sentiment',{'term':'nuclear energy','granularity':'quarterly'},'How has the tone of nuclear-energy news changed? Compare with the corpus baseline; do not claim this measures public opinion.'),
      ('distinctive themes','news.themes',{'term':'electric vehicle','limit':5},'Which themes are disproportionately associated with electric-vehicle coverage, rather than merely popular everywhere?'),
      ('publisher dominance','news.sources',{'term':'cryptocurrency','limit':5,'sample':100},'Which publishers dominate cryptocurrency coverage? Disclose the sample and distinguish publishers from companies mentioned.'),
      ('geographic coverage','news.geography',{'term':'drought','level':'country','limit':5},'Which countries feature most in drought news? Do not equate coverage counts with drought severity.'),
      ('associated organizations','news.entities',{'term':'generative ai','kind':'all','limit':5},'Which organizations and people are most associated with generative-AI news? Explain what co-occurrence does and does not imply.'),
      ('attention history','news.trends',{'term':'hydrogen','granularity':'quarterly','since':'2024-01-01','until':'2026-06-01'},'How did hydrogen news attention change between January 2024 and May 2026? Separate volume, importance and tone.')]
    for name,feature,args,question in insights:
        add('news_insights',name,feature,args,question,'Correct denominators, dates, baseline and interpretation; no unsupported inference from coverage to real-world prevalence.')
    return rows


def make_dataset(output):
    rng=random.Random(SEED);pool=candidates();chosen=[]
    for group in dict.fromkeys(r['group'] for r in pool):
        chosen.extend(rng.sample([r for r in pool if r['group']==group],5))
    rng.shuffle(chosen)
    for i,r in enumerate(chosen,1):r['id']=i
    output.mkdir(parents=True,exist_ok=True)
    manifest={'seed':SEED,'sampling':'5 randomly sampled cases from each of 10 strata, then shuffled; hand-authored 60-case sampling frame, not representative of all users',
              'created_at':datetime.now(timezone.utc).isoformat(),'pool':pool,'cases':chosen,
              'rules':{'max_case_seconds':240,'prism_workers':2,'cache':'isolated fresh application cache per case; immediate repeat separately',
                       'no_production_edits':True,'no_publication':True,'no_posthoc_replacement':True,
                       'success':'Relevant, attributable, appropriately scoped material that helps complete the requested task; ok:true alone is not success',
                       'rubric':'Task fit, source support, uncertainty/scope, usefulness; each 0-3; latency/availability separate; no fabricated precision'}}
    (output/'dataset.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False))
    print('DATASET',len(chosen),'cases',len({r['feature'] for r in chosen}),'endpoints',flush=True)
    return manifest


def run_prism(output,pid):
    manifest=json.loads((output/'dataset.json').read_text());(output/'prism').mkdir(exist_ok=True)
    def one(case):
        dest=output/'prism'/f"{case['id']:02d}.json"
        if dest.exists():return {'id':case['id'],'resumed':True}
        tick=time.monotonic()
        cmd=[sys.executable,str(ROOT/'profile_usecase.py'),'--dataset',str(output/'dataset.json'),'--id',str(case['id']),'--server-pid',str(pid),'--output',str(dest)]
        try:
            r=subprocess.run(cmd,capture_output=True,text=True,timeout=240)
            if r.returncode or not dest.exists():
                dest.write_text(json.dumps({'id':case['id'],'error':'worker_error','stderr':r.stderr[-2500:],'seconds':time.monotonic()-tick},indent=2))
        except subprocess.TimeoutExpired:
            dest.write_text(json.dumps({'id':case['id'],'error':'case_deadline','seconds':time.monotonic()-tick},indent=2))
        result=json.loads(dest.read_text())
        return {'id':case['id'],'feature':case['feature'],'seconds':round(time.monotonic()-tick,2),'ok':(result.get('first',{}).get('response') or {}).get('ok'),'error':result.get('error')}
    with ThreadPoolExecutor(max_workers=2) as pool:
        for f in as_completed([pool.submit(one,c) for c in manifest['cases']]):print(json.dumps(f.result()),flush=True)
    print('PRISM COMPLETE',flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('action',choices=['dataset','prism']);p.add_argument('--output',type=Path,required=True);p.add_argument('--server-pid',type=int,default=3073370);a=p.parse_args()
    if a.action=='dataset':make_dataset(a.output)
    else:run_prism(a.output,a.server_pid)
