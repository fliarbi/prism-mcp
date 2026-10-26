#!/usr/bin/env python3
"""Read-only query-log check for the new bounded SQL path."""
import json
import os
from pathlib import Path
import statistics

deployment = Path('out/rebuild-20260912/deployment.json')
source_pid = json.loads(deployment.read_text())['new_pid'] if deployment.exists() else 3073370
for item in Path(f'/proc/{source_pid}/environ').read_bytes().split(b'\0'):
    if item.startswith(b'PRISM_') and b'=' in item:
        key, value = item.decode().split('=', 1); os.environ[key] = value
from prism import ch

sql = """SELECT query_id, query_duration_ms, read_rows, read_bytes, memory_usage,
lower(hex(SHA256(query))) AS sql_sha256 FROM system.query_log
WHERE event_date=today() AND event_time>now()-INTERVAL 1 HOUR
AND type='QueryFinish' AND is_initial_query=1
AND startsWith(query,'SELECT openalex_id, title, abstract')
AND position(query,'PREWHERE publication_year BETWEEN 2020 AND 2025')>0
ORDER BY event_time FORMAT JSONEachRow"""
rows = [json.loads(line) for line in ch._request(sql, 15, True).splitlines() if line.strip()]
result = {'version': ch._request('SELECT version()', 5, True).strip(), 'query': sql, 'rows': rows}
if rows:
    result['summary'] = {'queries': len(rows), **{
        key: {'median': statistics.median(float(r[key]) for r in rows),
              'max': max(float(r[key]) for r in rows)}
        for key in ('query_duration_ms', 'read_rows', 'read_bytes', 'memory_usage')}}
Path('out/rebuild-20260912/clickhouse.json').write_text(json.dumps(result, indent=2))
print(json.dumps(result.get('summary', {})))
