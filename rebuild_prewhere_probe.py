#!/usr/bin/env python3
"""Small read-only A/B probe of early title filtering; no schema mutation."""
import json
import os
from pathlib import Path
import time
deployment = Path('out/rebuild-20260912/deployment.json')
source_pid = json.loads(deployment.read_text())['new_pid'] if deployment.exists() else 3073370
for item in Path(f'/proc/{source_pid}/environ').read_bytes().split(b'\0'):
    if item.startswith(b'PRISM_') and b'=' in item:
        k, v = item.decode().split('=', 1); os.environ[k] = v
from prism import ch, evidence, workflows

results = []
for subject, outcome in [('heat stress', 'productivity'), ('vertical farming', 'energy'), ('sodium-ion batteries', '')]:
    predicate = workflows._predicate([subject], [outcome] if outcome else [], 'title')
    prefix = f'SELECT {evidence._OA_COLS} FROM {ch.TABLE["research"]} PREWHERE publication_year BETWEEN 2020 AND 2025 '
    for mode in ('title_in_where', 'title_in_prewhere'):
        sql = prefix + (f'WHERE {predicate} AND ' if mode == 'title_in_where' else f'AND {predicate} WHERE ') + 'length(abstract)>=400 LIMIT 12'
        start = time.monotonic()
        try:
            rows = ch.chq_rows(sql, timeout=15)
            record = {'subject': subject, 'mode': mode, 'seconds': time.monotonic()-start, 'rows': len(rows), 'sql': sql+' FORMAT TabSeparated'}
        except Exception as exc:
            record = {'subject': subject, 'mode': mode, 'seconds': time.monotonic()-start, 'error': type(exc).__name__}
        results.append(record)
        print(json.dumps({k: v for k, v in record.items() if k != 'sql'}), flush=True)
Path('out/rebuild-20260912/prewhere-ab.json').write_text(json.dumps(results, indent=2))
time.sleep(8)  # allow the ordinary query-log flush; no SYSTEM command needed
sql = ("SELECT query,query_duration_ms,read_rows,read_bytes,memory_usage FROM system.query_log "
       "WHERE event_date=today() AND event_time>now()-INTERVAL 5 MINUTE "
       "AND type='QueryFinish' AND is_initial_query=1 AND query IN "
       + ch.sql_arr([r['sql'] for r in results if 'sql' in r]) + ' FORMAT JSONEachRow')
logs = [json.loads(x) for x in ch._request(sql, 15, True).splitlines() if x.strip()]
Path('out/rebuild-20260912/prewhere-query-log.json').write_text(json.dumps(logs, indent=2))
