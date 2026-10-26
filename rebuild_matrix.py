#!/usr/bin/env python3
"""50 seeded, literal-scope live research probes; NOT an app/model benchmark.

Two concurrent clients, first + repeat, 4 returned sources, at most 12 abstracts
read per case. Topics and aliases are fixed before execution. Inspect results:
success and quote matching are not semantic accuracy scores.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import json
from pathlib import Path
import random
import statistics
import time
import httpx

CASES = [
 ('health','intermittent fasting','weight loss','Intermittent fasting improves weight loss compared with continuous calorie restriction.'),
 ('health','exercise','depression','Exercise reduces depressive symptoms in adults.'),
 ('health','coffee','mortality','Coffee consumption is associated with all-cause mortality.'),
 ('health','screen time','sleep','Screen time affects sleep in adolescents.'),
 ('health','air pollution','asthma','Air pollution increases asthma risk in children.'),
 ('health','probiotics','depression','Probiotics improve depressive symptoms.'),
 ('health','vitamin D','fracture','Vitamin D supplementation prevents fractures in older adults.'),
 ('health','vaccination','autism','Vaccination causes autism.'),
 ('health','antibiotic resistance','wastewater','Wastewater contributes to antibiotic resistance transmission.'),
 ('health','mindfulness','anxiety','Mindfulness reduces anxiety symptoms.'),
 ('climate','urban heat','trees','Urban trees reduce heat exposure.'),
 ('climate','heat stress','productivity','Occupational heat stress reduces human worker productivity.'),
 ('climate','offshore wind','biodiversity','Offshore wind development affects marine biodiversity.'),
 ('climate','electric vehicles','emissions','Electric vehicles have zero lifecycle emissions.'),
 ('climate','carbon capture','energy','Carbon capture has an energy penalty.'),
 ('climate','microplastics','soil','Microplastics affect soil ecosystems.'),
 ('climate','sea level','migration','Sea level rise contributes to human migration.'),
 ('climate','coral','bleaching','Marine heatwaves increase coral bleaching.'),
 ('climate','wildfire','air quality','Wildfire smoke harms air quality.'),
 ('climate','hydrogen','water','Green hydrogen production increases water demand.'),
 ('technology','sodium-ion batteries','','Sodium-ion batteries can support stationary energy storage.'),
 ('technology','retrieval augmented generation','','Retrieval augmented generation eliminates hallucinations.'),
 ('technology','quantum','battery','Quantum batteries have a charging advantage under specific conditions.'),
 ('technology','large language models','bias','Large language models exhibit social bias.'),
 ('technology','small language models','','Small language models outperform larger models on all tasks.'),
 ('technology','perovskite','stability','Perovskite solar cells face stability challenges.'),
 ('technology','federated learning','privacy','Federated learning guarantees privacy.'),
 ('technology','autonomous vehicles','safety','Autonomous vehicles improve road safety.'),
 ('technology','desalination','energy','Desalination efficiency reduces total plant energy consumption.'),
 ('technology','blockchain','supply chain','Blockchain improves supply-chain traceability.'),
 ('work_education','four-day','work','A reduced-hours four-day workweek improves productivity.'),
 ('work_education','remote work','productivity','Remote work increases productivity in every workplace.'),
 ('work_education','retrieval practice','','Retrieval practice improves long-term retention.'),
 ('work_education','class size','achievement','Smaller classes improve student achievement.'),
 ('work_education','school','nutrition','School nutrition programs improve learning.'),
 ('work_education','automation','employment','Automation eliminates all employment.'),
 ('work_education','minimum wage','employment','Minimum wage increases reduce employment.'),
 ('work_education','universal basic income','','Universal basic income affects labor supply.'),
 ('work_education','gender','pay gap','Occupational segregation contributes to the gender pay gap.'),
 ('work_education','gamification','learning','Gamification improves student learning outcomes.'),
 ('agriculture','biochar','water retention','Biochar improves soil water retention.'),
 ('agriculture','drip irrigation','water','Drip irrigation efficiency reduces total basin water consumption.'),
 ('agriculture','cover crops','soil carbon','Cover crops increase soil carbon stocks.'),
 ('agriculture','organic farming','yield','Organic farming always produces higher yields.'),
 ('agriculture','pesticide','pollinator','Pesticide exposure harms pollinators.'),
 ('agriculture','agroforestry','biodiversity','Agroforestry improves farmland biodiversity.'),
 ('agriculture','precision agriculture','','Precision agriculture reduces input use.'),
 ('agriculture','drought','wheat','Drought reduces wheat yield.'),
 ('agriculture','vertical farming','energy','Vertical farming consumes less energy than open-field farming.'),
 ('agriculture','soil salinity','crop','Soil salinity reduces crop productivity.'),
]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8791)
    parser.add_argument('--dest', default='out/rebuild-20260912/matrix50')
    args = parser.parse_args()
    dest = Path(args.dest); dest.mkdir(parents=True, exist_ok=True)
    cases = list(enumerate(CASES, 1)); random.Random(20260912).shuffle(cases)
    def run(item):
        index, (group, subject, outcome, claim) = item
        path = dest/f'{index:02d}.json'
        if path.exists():
            return json.loads(path.read_text())
        body = {'claim': claim, 'subject_phrases': [subject],
                'outcome_phrases': [outcome] if outcome else [], 'limit': 4}
        result = {'id': index, 'group': group, 'args': body}
        with httpx.Client(base_url=f'http://127.0.0.1:{args.port}', timeout=90) as client:
            for label in ('first', 'repeat'):
                start = time.monotonic()
                try:
                    response = client.post('/v1/research.packet', json=body)
                    result[label] = {'seconds': time.monotonic()-start, 'http': response.status_code,
                                     'response': response.json()}
                except Exception as exc:
                    result[label] = {'seconds': time.monotonic()-start, 'error': str(exc)}
                path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
            data = result['first'].get('response', {}).get('data') or {}
            if data.get('packet_id'):
                result['passages'] = client.post('/v1/research.packet_read', json={
                    'packet_id': data['packet_id'], 'limit': 8, 'chars_per_source': 12000}).json()
                path.write_text(json.dumps(result, indent=2, ensure_ascii=False))
        print(index, group, round(result['first']['seconds'], 2),
              result['first'].get('response', {}).get('ok'), data.get('on_claim_sources'), flush=True)
        return result
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = [f.result() for f in as_completed([pool.submit(run, c) for c in cases])]
    def metrics(label):
        xs = sorted(r[label]['seconds'] for r in results)
        return {'median': statistics.median(xs), 'p95_nearest_rank': xs[47], 'max': max(xs)}
    summary = {'n': len(results), 'concurrency': 2, 'seed': 20260912,
               'first': metrics('first'), 'repeat': metrics('repeat'),
               'ok': sum(r['first'].get('response', {}).get('ok', False) for r in results),
               'cases_with_on_claim_verdicts': sum(bool((r['first'].get('response', {}).get('data') or {}).get('on_claim_sources')) for r in results),
               'caveat': 'New bounded research-only workload with explicit aliases. Not equivalent to the original 50 mixed endpoints or a ChatGPT/Claude app comparison. On-claim verdicts are model labels, not adjudicated accuracy.'}
    (dest/'summary.json').write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary), flush=True)


if __name__ == '__main__':
    main()
