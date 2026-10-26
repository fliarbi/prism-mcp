#!/usr/bin/env python3
"""Small MCP-wire check; not included in the 50-case latency distribution."""
import asyncio
import json
from pathlib import Path
import time
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

async def main():
    out={}
    async with streamablehttp_client('http://127.0.0.1:8790/mcp',timeout=30,sse_read_timeout=30) as (read,write,_):
        async with ClientSession(read,write) as session:
            t=time.monotonic();init=await session.initialize();out['initialize']={'seconds':time.monotonic()-t,'result':init.model_dump(mode='json')}
            t=time.monotonic();listing=await session.list_tools();out['list_tools']={'seconds':time.monotonic()-t,'names':[x.name for x in listing.tools],'next_cursor':listing.nextCursor}
            for name,args in [('request_status',{'request_id':'benchmark-does-not-exist-20260912'}),('research_audit',{'text':'I prefer shorter articles and a friendly tone.'})]:
                if name not in out['list_tools']['names']:
                    out[name]={'skipped':'tool name not in live list'};continue
                t=time.monotonic();r=await session.call_tool(name,args);out[name]={'seconds':time.monotonic()-t,'result':r.model_dump(mode='json')}
    Path('out/usecases-50-20260912/mcp-wire.json').write_text(json.dumps(out,indent=2,ensure_ascii=False))
    print(json.dumps(out,ensure_ascii=False)[:6000])

asyncio.run(main())
