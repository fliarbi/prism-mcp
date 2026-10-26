#!/usr/bin/env python3
"""Summarize diagnostic spans and read matching ClickHouse query-log records."""
import json
from pathlib import Path
import sys
from prism import ch

directory=Path(sys.argv[1])
spans=[json.loads(line) for line in (directory/'spans.jsonl').read_text().splitlines()]
responses=[json.loads(line) for line in (directory/'responses.jsonl').read_text().splitlines()]
summary=[]
for response in responses:
    rows=[s for s in spans if s['case']==response['case']]
    sql=[s for s in rows if s['name']=='prism.ch._request']
    points=sorted([(s['start'],1) for s in sql]+[(s['end'],-1) for s in sql])
    active=peak=0;union=0;previous=0
    for timestamp,change in points:
        if active:union+=timestamp-previous
        active+=change;peak=max(peak,active);previous=timestamp
    summary.append({'case':response['case'],'seconds':response['seconds'],
                    'sql_calls':len(sql),'peak_concurrent_sql':peak,
                    'sql_sum_seconds':sum(s['seconds'] for s in sql),
                    'sql_active_union_seconds':union,
                    'sql_errors':sum('error' in s for s in sql),
                    'stages':[{k:s[k] for k in ['id','parent','name','start','end','seconds']}
                              for s in rows if s['name']!='prism.ch._request']})
with (directory/'summary.json').open('x') as f:json.dump(summary,f,indent=2)
chosen=sorted([s for s in spans if s['case']=='sections-cold' and s['name']=='prism.ch._request'],
              key=lambda s:s['seconds'],reverse=True)[:6]
sql=("SELECT query_duration_ms, read_rows, read_bytes, memory_usage, query FROM system.query_log "
     "WHERE event_time > now() - INTERVAL 30 MINUTE AND type = 'QueryFinish' AND query IN ("+
     ','.join(ch.sql_str(s['sql']) for s in chosen)+") ORDER BY event_time DESC LIMIT 12 FORMAT JSONEachRow")
logs=[json.loads(line) for line in ch.chq(sql,timeout=25).splitlines()]
with (directory/'clickhouse-query-log.json').open('x') as f:json.dump(logs,f,indent=2)
print(json.dumps([{k:v for k,v in s.items() if k!='stages'} for s in summary],indent=2))
print('Matching query log records:',len(logs))
