"""access — the public face of the server: one Fliar API key, metered in credits.

Prism accepts the same `rdr_` key as the Radar API and Prism News. Keys are checked with the Radar API
gateway (`/internal/keys/introspect`, reached over the private network with a shared secret) and every
feature call draws prepaid credits from the one Fliar API wallet the gateway keeps: credits are reserved
before the work (`/internal/credits/reserve`) and settled after it (`/internal/credits/settle`). A call that
fails, or answers "nothing here", is settled at zero, so a caller pays only for answers.

Off unless PRISM_PUBLIC=1. The loopback deployment the showcase and the benchmark use stays open.

    PRISM_PUBLIC=1
    PRISM_RADAR_KEYS_URL=http://<gateway private address>:8810
    PRISM_RADAR_KEYS_HOST=radar-api.fliarbi.com
    PRISM_RADAR_KEYS_SECRET=<the gateway's RADAR_INTROSPECT_SECRET>
    PRISM_KEYS_PAGE=https://fliarbi.com/radar/dashboard?tab=radarapi
"""
from __future__ import annotations

import asyncio
import hashlib
import json
import logging
import os
import re
import threading
import time
import urllib.error
import urllib.request

from . import pricing

log = logging.getLogger("prism.access")

PUBLIC = os.environ.get("PRISM_PUBLIC", "0") == "1"
KEYS_URL = os.environ.get("PRISM_RADAR_KEYS_URL", "").rstrip("/")
KEYS_HOST = os.environ.get("PRISM_RADAR_KEYS_HOST", "")
KEYS_SECRET = os.environ.get("PRISM_RADAR_KEYS_SECRET", "")
KEYS_PAGE = os.environ.get("PRISM_KEYS_PAGE", "https://fliarbi.com/radar/dashboard?tab=radarapi")
OPEN_PATHS = {"/livez", "/v1", "/v1/openapi.json", "/v1/pricing", "/install.sh", "/cli/prism"}

_cache: dict = {}            # sha256(key) -> (expires, info)
_lock = threading.Lock()
_active: dict = {}           # account -> running calls
_minute: dict = {}           # account -> [window_start, count]


class Refused(Exception):
    def __init__(self, status, kind, reason, retry=None):
        super().__init__(reason)
        self.status, self.kind, self.reason, self.retry = status, kind, reason, retry


def _post(path, body):
    headers = {"Content-Type": "application/json", "X-Introspect-Secret": KEYS_SECRET}
    if KEYS_HOST:
        headers["Host"] = KEYS_HOST
    req = urllib.request.Request(KEYS_URL + path, method="POST", data=json.dumps(body).encode(), headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=8) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read() or b"{}")
        except ValueError:
            return e.code, {}
    except (urllib.error.URLError, TimeoutError, ValueError) as e:
        log.error("gateway unavailable: %s", type(e).__name__)
        return 599, {}


def identify(key: str) -> dict:
    """The account behind an rdr_ key, cached for a minute. Never logs the key."""
    if not re.fullmatch(r"rdr_[a-f0-9]{64}", key or ""):
        raise Refused(401, "unauthorized", f"Send your Fliar API key as 'Authorization: Bearer rdr_…'. Create one at {KEYS_PAGE}")
    if not (KEYS_URL and KEYS_SECRET):
        raise Refused(503, "upstream", "Key checks are not configured on this server")
    h = hashlib.sha256(key.encode()).hexdigest()
    now = time.time()
    with _lock:
        hit = _cache.get(h)
        if hit and hit[0] > now:
            return hit[1]
    status, body = _post("/internal/keys/introspect", {"api_key": key})
    info = body.get("data") if status == 200 and body.get("ok") else None
    if not isinstance(info, dict):
        raise Refused(502, "upstream", "The key service did not answer; try again shortly", 5)
    if not info.get("active"):
        raise Refused(401, "unauthorized", f"Unknown, expired or revoked API key. Manage keys at {KEYS_PAGE}")
    with _lock:
        _cache[h] = (now + 60, info)
    return info


def admit(info: dict, feature: str) -> None:
    """Scope, rate and concurrency checks before any credit is reserved."""
    scopes = set(info.get("scopes") or [])
    if "*" not in scopes and not (feature.startswith("news.") and "news" in scopes):
        raise Refused(403, "scope_required", f"This key does not include Prism access; create a key with 'All data' at {KEYS_PAGE}")
    lv = info.get("level") or {}
    acct, now = info["account_id"], time.time()
    with _lock:
        w = _minute.get(acct)
        if not w or now - w[0] >= 60:
            w = _minute[acct] = [now, 0]
        if w[1] >= int(lv.get("rate_per_minute") or 60):
            raise Refused(429, "rate_limited", "Per-minute request limit reached for your usage level", int(60 - (now - w[0])) + 1)
        if _active.get(acct, 0) >= int(lv.get("concurrent_requests") or 3):
            raise Refused(429, "concurrency_limited", "Too many Prism calls running at once for your usage level", 5)
        w[1] += 1
        _active[acct] = _active.get(acct, 0) + 1


def release(info: dict) -> None:
    with _lock:
        acct = info["account_id"]
        _active[acct] = max(0, _active.get(acct, 0) - 1)


def reserve(info: dict, feature: str, units: int) -> str:
    status, body = _post("/internal/credits/reserve", {"account_id": info["account_id"], "feature": f"prism:{feature}"[:80],
                                                       "units": int(units)})
    rid = (body.get("data") or {}).get("request_id") if status == 200 and body.get("ok") else None
    if rid:
        return rid
    if status == 599:
        raise Refused(502, "upstream", "The credit service did not answer; try again shortly", 5)
    reason = ((body.get("error") or {}).get("message") or (body.get("error") or {}).get("reason")
              or "Not enough prepaid credits")
    raise Refused(402 if status in (402, 403) else 429 if status == 429 else 402, "credits_required",
                  f"{reason}. This call costs {units} credits; add prepaid credits at {KEYS_PAGE}")


def settle(request_id: str, actual: int) -> None:
    status, _ = _post("/internal/credits/settle", {"request_id": request_id, "actual": max(0, int(actual))})
    if status != 200:
        log.error("credit settlement %s failed (HTTP %s)", request_id, status)


def _bearer(scope) -> str:
    for k, v in scope.get("headers") or []:
        k = k.decode().lower()
        if k == "authorization":
            v = v.decode()
            return v[7:].strip() if v.lower().startswith("bearer ") else v.strip()
        if k == "x-api-key":
            return v.decode().strip()
    return ""


def _error(status, kind, reason, retry=None):
    body = json.dumps({"ok": False, "feature": "access", "subject": {}, "data": None, "window": {}, "meta": {},
                       "error": {"kind": kind, "reason": reason}}).encode()
    headers = [(b"content-type", b"application/json")]
    if retry:
        headers.append((b"retry-after", str(int(retry)).encode()))
    return status, headers, body


class Gate:
    """ASGI middleware: key check on every request, credits on every feature call (REST and MCP tools/call)."""

    def __init__(self, app, registry):
        self.app = app
        self.feature_of = {}
        for name, spec in registry.items():
            self.feature_of[f"/v1/{spec['feature']}"] = spec["feature"]
            self.feature_of[f"/v1/{name}"] = spec["feature"]
        self.tool_feature = {name: spec["feature"] for name, spec in registry.items()}

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        path = scope.get("path", "")
        for root in {scope.get("root_path", ""), os.environ.get("PRISM_ROOT_PATH", "")}:
            if root and (path == root or path.startswith(root + "/")):
                path = path[len(root):] or "/"
                break
        if path in OPEN_PATHS:
            return await self.app(scope, receive, send)
        if path == "/healthz" or path == "/readyz":
            return await self._reply(send, *_error(404, "not_found", "Not found"))
        try:
            info = await asyncio.to_thread(identify, _bearer(scope))
        except Refused as r:
            return await self._reply(send, *_error(r.status, r.kind, r.reason, r.retry))
        if path.startswith("/v1/"):
            feature = self.feature_of.get(path)
            if not feature:
                return await self._reply(send, *_error(404, "not_found", "Unknown feature; see /v1"))
            return await self._metered(scope, receive, send, info, feature, None)
        if path.rstrip("/") == "/mcp":
            body = b""
            more = True
            while more:
                msg = await receive()
                body += msg.get("body", b"")
                more = msg.get("more_body", False)
            try:
                rpc = json.loads(body or b"{}")
            except ValueError:
                rpc = {}
            replay = _replayer(body)
            if isinstance(rpc, dict) and rpc.get("method") == "tools/call":
                tool = ((rpc.get("params") or {}).get("name") or "")
                feature = self.tool_feature.get(tool)
                if not feature or feature in pricing.BLOCKED:
                    return await self._reply(send, *_error(404, "not_found", f"Unknown tool: {tool}"))
                return await self._metered(scope, replay, send, info, feature, tool)
            if isinstance(rpc, dict) and rpc.get("method") == "tools/list":
                return await self._filtered_list(scope, replay, send)
            return await self.app(scope, replay, send)
        return await self._reply(send, *_error(404, "not_found", "Not found"))

    async def _metered(self, scope, receive, send, info, feature, tool):
        if feature in pricing.BLOCKED:
            return await self._reply(send, *_error(404, "not_found", "This feature is not available on the public API"))
        for k, v in scope.get("headers") or []:
            if k.decode().lower() == "prefer" and b"respond-async" in v.lower():
                return await self._reply(send, *_error(400, "bad_request", "Asynchronous requests are not available on the public API"))
        units = pricing.credits(feature)
        try:
            admit(info, feature)
        except Refused as r:
            return await self._reply(send, *_error(r.status, r.kind, r.reason, r.retry))
        if not units:
            try:
                return await self.app(scope, receive, send)
            finally:
                release(info)
        try:
            try:
                rid = await asyncio.to_thread(reserve, info, feature, units)
            except Refused as r:
                return await self._reply(send, *_error(r.status, r.kind, r.reason, r.retry))
            state = {"status": 500, "chunks": [], "headers": []}

            async def capture(msg):
                if msg["type"] == "http.response.start":
                    state["status"] = msg["status"]
                    state["headers"] = list(msg.get("headers") or [])
                elif msg["type"] == "http.response.body":
                    state["chunks"].append(msg.get("body", b""))
            ok = False
            try:
                await self.app(scope, receive, capture)
                body = b"".join(state["chunks"])
                ok = state["status"] == 200 and (tool is None or _tool_ok(body))
            finally:
                await asyncio.to_thread(settle, rid, units if ok else 0)
            headers = [h for h in state["headers"] if h[0].lower() != b"content-length"]
            headers += [(b"content-length", str(len(body)).encode()),
                        (b"x-prism-credits", str(units if ok else 0).encode())]
            await send({"type": "http.response.start", "status": state["status"], "headers": headers})
            await send({"type": "http.response.body", "body": body})
        finally:
            release(info)

    async def _filtered_list(self, scope, receive, send):
        state = {"status": 200, "chunks": [], "headers": []}

        async def capture(msg):
            if msg["type"] == "http.response.start":
                state["status"], state["headers"] = msg["status"], list(msg.get("headers") or [])
            elif msg["type"] == "http.response.body":
                state["chunks"].append(msg.get("body", b""))
        await self.app(scope, receive, capture)
        body = b"".join(state["chunks"])
        body = _filter_tools(body, {t for t, f in self.tool_feature.items() if f in pricing.BLOCKED})
        headers = [h for h in state["headers"] if h[0].lower() != b"content-length"] + [(b"content-length", str(len(body)).encode())]
        await send({"type": "http.response.start", "status": state["status"], "headers": headers})
        await send({"type": "http.response.body", "body": body})

    @staticmethod
    async def _reply(send, status, headers, body):
        await send({"type": "http.response.start", "status": status, "headers": headers + [(b"content-length", str(len(body)).encode())]})
        await send({"type": "http.response.body", "body": body})


def _replayer(body):
    sent = {"done": False}

    async def receive():
        if not sent["done"]:
            sent["done"] = True
            return {"type": "http.request", "body": body, "more_body": False}
        await asyncio.sleep(3600)
        return {"type": "http.disconnect"}
    return receive


def _payloads(body: bytes):
    """JSON-RPC messages in a plain JSON or an SSE-framed MCP response."""
    text = body.decode("utf-8", "replace")
    if text.lstrip().startswith("{"):
        yield text
        return
    for line in text.splitlines():
        if line.startswith("data:"):
            yield line[5:].strip()


def _tool_ok(body: bytes) -> bool:
    for p in _payloads(body):
        try:
            msg = json.loads(p)
        except ValueError:
            continue
        res = msg.get("result") if isinstance(msg, dict) else None
        if isinstance(res, dict):
            sc = res.get("structuredContent")
            if isinstance(sc, dict) and "ok" in sc:
                return bool(sc["ok"])
            return not res.get("isError")
    return False


def _filter_tools(body: bytes, hidden: set) -> bytes:
    text = body.decode("utf-8", "replace")

    def fix(p):
        try:
            msg = json.loads(p)
            tools = msg["result"]["tools"]
            msg["result"]["tools"] = [t for t in tools if t.get("name") not in hidden]
            return json.dumps(msg)
        except Exception:
            return p
    if text.lstrip().startswith("{"):
        return fix(text).encode()
    out = [("data: " + fix(line[5:].strip())) if line.startswith("data:") else line for line in text.splitlines()]
    return ("\n".join(out) + ("\n" if text.endswith("\n") else "")).encode()
