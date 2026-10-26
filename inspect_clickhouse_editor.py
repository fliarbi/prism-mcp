#!/usr/bin/env python3
"""Read-only query-plan/date-pruning experiment; does not alter production SQL."""
import json
import time
from pathlib import Path
from prism import ch

root=Path('out/async-progress-profile-20260912')
logs=json.loads((root/'clickhouse-query-log.json').read_text())
original=next(r['query'] for r in logs if 'SELECT orientation, contribution' in r['query'])
needle='WHERE publication_year BETWEEN 2017 AND 2025'
assert needle in original
candidate=original.replace(needle,"WHERE publication_date >= '2017-01-01' AND publication_date < '2026-01-01' AND publication_year BETWEEN 2017 AND 2025")
schema=ch.chq("SELECT name,type,default_kind,default_expression FROM system.columns WHERE database='research' AND table='openalex_prism_local' AND name IN ('publication_year','publication_date') FORMAT JSONEachRow",timeout=10)
integrity=ch.chq("SELECT countIf(publication_year != toYear(publication_date)) mismatches, countIf(isNull(publication_date)) missing_dates, count() n FROM research.openalex_prism_distributed FORMAT JSONEachRow",timeout=20)
plans={label:ch.chq('EXPLAIN indexes=1 '+sql,timeout=10) for label,sql in [('original',original),('candidate',candidate)]}
rows=[]
for label in ['original','candidate','candidate','original']:
    tick=time.monotonic()
    result=ch.chq(original if label=='original' else candidate,timeout=25)
    row={'variant':label,'seconds':time.monotonic()-tick,'result':result}
    rows.append(row)
    print(json.dumps({k:v for k,v in row.items() if k!='result'}),flush=True)
identical_bytes=len({r['result'] for r in rows})==1
# SQL orders by count only. Equal-count rows may change order even when the
# query is repeated unchanged; compare the full multiset, retaining duplicates.
identical=len({tuple(sorted(r['result'].splitlines())) for r in rows})==1
out={'read_only':True,'deployed':False,'schema':schema,'date_integrity':integrity,
     'original_sql':original,'candidate_sql':candidate,'plans':plans,'runs':rows,
     'identical_bytes':identical_bytes,'identical_result_rows':identical,
     'caveat':'Date/year equality is observed, not enforced by a materialized column or constraint. Require an ingestion invariant before enabling the additional filter.'}
(root/'date-pruning-experiment.json').write_text(json.dumps(out,indent=2))
print(json.dumps({'identical_results':identical,'date_integrity':integrity,'candidate_plan':plans['candidate']}),flush=True)
