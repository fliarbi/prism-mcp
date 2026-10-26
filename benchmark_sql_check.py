#!/usr/bin/env python3
"""Read-only exact-match query-log evidence for the saved benchmark SQL."""
import json
import os
from pathlib import Path
p=Path('out/usecases-50-20260912')
for item in Path('/proc/3073370/environ').read_bytes().split(b'\0'):
    if item.startswith(b'PRISM_') and b'=' in item:
        k,v=item.decode().split('=',1);os.environ[k]=v
from prism import ch
slow=json.loads((p/'slow-sql.json').read_text())
queries=list(dict.fromkeys(s['sql'] for s in slow[:10]))
def literal(s):return "'"+s.replace('\\','\\\\').replace("'","\\'")+"'"
sql="SELECT query_id, query_duration_ms, read_rows, read_bytes, memory_usage, lower(hex(SHA256(query))) AS sql_sha256, event_time, is_initial_query FROM system.query_log WHERE event_date = today() AND event_time > now() - INTERVAL 3 HOUR AND type = 'QueryFinish' AND query IN ("+','.join(map(literal,queries))+') ORDER BY query_duration_ms DESC FORMAT JSONEachRow'
try:
    result=[json.loads(line) for line in ch._request(sql,30,True).splitlines() if line.strip()]
except Exception as e:result={'error':type(e).__name__+': '+str(e)[:500]}
(p/'clickhouse-query-log.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
schema={}
checks={
 'version':'SELECT version() FORMAT TabSeparated',
 'keys':"SELECT database,name,engine,partition_key,sorting_key,primary_key FROM system.tables WHERE (database='openalex' AND name IN ('works_local','works_distributed')) OR (database='research' AND name IN ('openalex_prism_local','openalex_prism_distributed')) FORMAT JSONEachRow",
 'indexes':"SELECT database,table,name,type,expr FROM system.data_skipping_indices WHERE (database='openalex' AND table='works_local') OR (database='research' AND table='openalex_prism_local') FORMAT JSONEachRow",
 'projections':"SELECT database,table,name,type,sorting_key FROM system.projections WHERE (database='openalex' AND table='works_local') OR (database='research' AND table='openalex_prism_local') FORMAT JSONEachRow",
}
example=next(s for s in slow if 'FROM openalex.works_distributed' in s['sql'])
checks['local_explain']='EXPLAIN indexes=1 '+example['sql'].replace('openalex.works_distributed','openalex.works_local').replace(' FORMAT TabSeparated','')
schema['explain_source_sha256']=example['sql_sha256']
for name,query in checks.items():
    try:schema[name]=ch._request(query,20,True)
    except Exception as e:schema[name]={'error':type(e).__name__+': '+str(e)[:300]}
(p/'clickhouse-schema.json').write_text(json.dumps(schema,indent=2))
print(json.dumps(schema,indent=2))
