"""Call Prism the way an assistant does: over MCP (streamable HTTP), one tool call per request, every call logged.

    from mcpcall import call, LOG
    env = call("news_themes", {"term": "nvidia", "since": "2021-01-01", "until": "2022-01-01"})

Returns the tool's envelope (structuredContent). LOG holds {tool, args, seconds, ok} for each call, so a report can
print exactly which MCP calls it was built from.
"""
import asyncio
import json
import os
import threading
import time

URL = os.environ.get("PRISM_MCP_URL", "http://127.0.0.1:8790/mcp")
LOG = []
_lock = threading.Lock()


async def _call(tool, args, timeout):
    from mcp import ClientSession
    from mcp.client.streamable_http import streamablehttp_client
    async with streamablehttp_client(URL, timeout=60, sse_read_timeout=timeout) as (r, w, _):
        async with ClientSession(r, w) as s:
            await s.initialize()
            res = await s.call_tool(tool, args)
            sc = getattr(res, "structuredContent", None)
            if isinstance(sc, dict) and "ok" in sc:
                return sc
            for c in res.content or []:
                try:
                    return json.loads(getattr(c, "text", "") or "")
                except ValueError:
                    continue
            return {"ok": False, "error": {"reason": "no structured result"}}


def call(tool, args, timeout=900, retries=1):
    t0 = time.time()
    env = None
    for attempt in range(retries + 1):
        try:
            env = asyncio.run(_call(tool, args, timeout))
            break
        except Exception as e:
            env = {"ok": False, "error": {"kind": "transport", "reason": f"{type(e).__name__}: {e}"}}
    with _lock:
        LOG.append({"tool": tool, "args": args, "seconds": round(time.time() - t0, 1), "ok": bool(env.get("ok")),
                    "feature": env.get("feature")})
    return env
