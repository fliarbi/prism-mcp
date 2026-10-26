#!/usr/bin/env python3
"""api — the same features, over HTTP.

Every Prism feature in this server is one Python function. This module turns
that same set of functions into a REST surface, generated from their
signatures, so there is exactly one definition per feature and no second list
to keep in step: add a tool, and its endpoint, its parameter coercion and its
OpenAPI entry appear with it.

    GET  /v1/news.trends?term=electric+vehicle&granularity=monthly
    POST /v1/news.trends            {"term": "electric vehicle"}
    GET  /v1                        the index — every feature, its parameters
    GET  /v1/openapi.json           an OpenAPI 3.1 document for n8n / Zapier /
                                    ChatGPT actions / a WordPress plugin
    GET  /healthz                   liveness plus corpus availability

Responses are the same envelope MCP clients get, verbatim: `ok`, `feature`,
`subject`, `data`, `window`, `meta`, and `error` when `ok` is false. A caller
that reads the MCP output can read this one and vice versa.

HTTP status codes follow the envelope rather than replacing it: 200 when the
feature answered, 404 when it answered "nothing here", 400 on a bad parameter,
500 only when the server itself broke. The body is always the envelope, so a
client never has to parse two shapes.

There is no authentication here on purpose — this binds to loopback and belongs
behind the same front that fronts everything else on this host. Do not expose
it directly.
"""
from __future__ import annotations

import inspect
import json
import typing
import types
from pydantic import TypeAdapter
from . import envelope, execution

VERSION = "1.0"
STATUS_FOR_KIND = {"no_data": 404, "not_resolvable": 404, "bad_request": 400,
                   "upstream": 502, "internal": 500}


def _params(fn) -> list:
    """A feature's parameters, read off its signature. One source of truth."""
    out = []
    hints = typing.get_type_hints(fn)
    for name, p in inspect.signature(fn).parameters.items():
        if name.startswith("_") or p.kind in (p.VAR_POSITIONAL, p.VAR_KEYWORD):
            continue
        t = hints.get(name, str)
        nullable = False
        if typing.get_origin(t) in (typing.Union, types.UnionType):
            alternatives = typing.get_args(t)
            nullable = type(None) in alternatives
            concrete = [a for a in alternatives if a is not type(None)]
            if len(concrete) == 1:
                t = concrete[0]
        kind = "string"
        if t in (int,):
            kind = "integer"
        elif t in (float,):
            kind = "number"
        elif t in (bool,):
            kind = "boolean"
        elif t is list or typing.get_origin(t) is list:
            kind = "array"
        elif t is dict or typing.get_origin(t) is dict:
            kind = 'object'
        out.append({"name": name, "type": kind,
                    "nullable": nullable,
                    "schema": TypeAdapter(hints.get(name, str)).json_schema(),
                    "required": p.default is inspect.Parameter.empty,
                    "default": None if p.default is inspect.Parameter.empty
                    else p.default})
    return out


def _coerce(raw, kind: str):
    if raw is None:
        raise ValueError('null is not a valid value for this parameter')
    if kind == "integer":
        return int(raw)
    if kind == "number":
        return float(raw)
    if kind == "boolean":
        if isinstance(raw, bool):
            return raw
        value = str(raw).strip().lower()
        if value not in ('1', 'true', 'yes', 'on', '0', 'false', 'no', 'off'):
            raise ValueError('expected a boolean')
        return value in ('1', 'true', 'yes', 'on')
    if kind == "array":
        if isinstance(raw, list):
            return raw
        s = str(raw).strip()
        if s.startswith("["):
            try:
                parsed = json.loads(s)
                if not isinstance(parsed, list):
                    raise ValueError('expected a JSON array')
                return parsed
            except Exception:
                pass
        return [x.strip() for x in s.split(",") if x.strip()]
    if kind == 'object':
        value = json.loads(raw) if isinstance(raw, str) else raw
        if not isinstance(value, dict):
            raise ValueError('expected a JSON object')
        return value
    return str(raw)


def _summary(fn) -> str:
    doc = (fn.__doc__ or "").strip().split("\n")
    return doc[0] if doc else ""


def _description(fn) -> str:
    return (fn.__doc__ or "").strip()


def install(mcp, registry: dict) -> None:
    """Mount /v1 on the MCP server's own HTTP app.

    One process serves MCP at /mcp and REST at /v1, so a WordPress plugin and a
    Claude client are talking to the same cache, the same corpus handles and the
    same code path."""
    import json as _stdjson
    from starlette.responses import JSONResponse, Response

    class _SafeJSON(JSONResponse):
        """Serialise with default=str.

        A payload that renders over MCP and 500s over REST is the worst kind of
        bug in a two-surface server: it looks like the feature is broken rather
        than the transport. One datetime from the article store was enough to
        do it, so nothing here is allowed to fail on an exotic type."""

        def render(self, content) -> bytes:
            return _stdjson.dumps(content, ensure_ascii=False,
                                  allow_nan=False, default=str).encode("utf-8")

    def _json(payload, status=200):
        return _SafeJSON(payload, status_code=status)

    def _status_of(env: dict) -> int:
        if env.get("ok"):
            return 200
        return STATUS_FOR_KIND.get((env.get("error") or {}).get("kind"), 500)

    def _make(name: str, spec: dict):
        fn, params = spec["fn"], _params(spec["fn"])

        async def handler(request):
            try:
                given = dict(request.query_params)
                if request.method == "POST":
                    try:
                        body = await request.json()
                    except Exception as e:
                        raise ValueError('body must be valid JSON') from e
                    if not isinstance(body, dict):
                        raise ValueError('body must be a JSON object')
                    given.update(body)
                kwargs, unknown = {}, []
                known = {p["name"]: p for p in params}
                for k, v in given.items():
                    if k in known:
                        kwargs[k] = (None if v is None and known[k].get('nullable')
                                     else _coerce(v, known[k]["type"]))
                    else:
                        unknown.append(k)
                missing = [p["name"] for p in params
                           if p["required"] and p["name"] not in kwargs]
                if missing:
                    return _json(envelope.fail(spec['feature'],
                        f"missing required parameter(s): {', '.join(missing)}",
                        kind='bad_request', meta={'parameters': params}), 400)
                prefer_async = 'respond-async' in request.headers.get('prefer', '').lower()
                if prefer_async:
                    # Existing synchronous clients are unchanged. REST clients
                    # can opt in on the SAME endpoint; MCP uses system.request.
                    from . import requests as editor_requests
                    submitted = await execution.run(editor_requests.submit_request,
                                                     spec['feature'], kwargs)
                    env = envelope.standardise(spec['feature'], submitted)
                else:
                    env = await execution.run(fn, **kwargs)
                if unknown and isinstance(env, dict):
                    env.setdefault("meta", {})["ignored_parameters"] = unknown
                response = _json(env, 202 if prefer_async and env.get('ok') else
                                 _status_of(env if isinstance(env, dict) else {}))
                if prefer_async and env.get('ok'):
                    response.headers['Preference-Applied'] = 'respond-async'
                    response.headers['Location'] = env['data']['poll']
                return response
            except (ValueError, TypeError) as e:
                return _json(envelope.fail(spec['feature'], f'{type(e).__name__}: {e}',
                    kind='bad_request', meta={'parameters': params}), 400)
            except Exception as e:
                return _json(envelope.fail(spec['feature'], f'{type(e).__name__}: {e}',
                    kind='internal'), 500)

        handler.__name__ = f"rest_{name}"
        return handler

    for name, spec in registry.items():
        mcp.custom_route(f"/v1/{spec['feature']}", methods=["GET", "POST"],
                         name=f"feature_{name}")(_make(name, spec))
        # the tool name is an alias for the dotted feature id, so a caller who
        # knows the MCP tool can hit the endpoint without a lookup
        if name != spec["feature"]:
            mcp.custom_route(f"/v1/{name}", methods=["GET", "POST"],
                             name=f"alias_{name}")(_make(name, spec))

    from . import pricing, access

    def _listed(items):
        return [(n, s) for n, s in items if not (access.PUBLIC and s["feature"] in pricing.BLOCKED)]

    import os as _os
    from starlette.responses import PlainTextResponse
    _repo = _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__)))

    @mcp.custom_route("/install.sh", methods=["GET"], name="install_sh")
    async def install_sh(request):
        return PlainTextResponse(open(_os.path.join(_repo, "scripts", "install.sh")).read(),
                                 media_type="text/x-shellscript", headers={"Cache-Control": "no-cache"})

    @mcp.custom_route("/cli/prism", methods=["GET"], name="cli_prism")
    async def cli_prism(request):
        return PlainTextResponse(open(_os.path.join(_repo, "cli", "prism")).read(),
                                 media_type="text/x-python", headers={"Cache-Control": "no-cache"})

    @mcp.custom_route("/v1/pricing", methods=["GET"], name="pricing")
    async def pricing_route(request):
        return _json(pricing.catalog())

    @mcp.custom_route("/v1", methods=["GET"], name="index")
    async def index(request):
        return _json({
            "service": "prism", "version": VERSION,
            "envelope": ["ok", "feature", "subject", "data", "window", "meta",
                         "error"],
            "transports": {"rest": "/v1/<feature>", "mcp": "/mcp",
                           "openapi": "/v1/openapi.json"},
            "features": [
                {"feature": s["feature"], "tool": n, "group": s["group"],
                 "summary": _summary(s["fn"]),
                 "endpoint": f"/v1/{s['feature']}", "credits": pricing.credits(s["feature"]),
                 "parameters": _params(s["fn"])}
                for n, s in _listed(sorted(registry.items(), key=lambda kv: kv[1]["feature"]))],
        })

    @mcp.custom_route("/v1/openapi.json", methods=["GET"], name="openapi")
    async def openapi(request):
        paths = {}
        for name, spec in _listed(registry.items()):
            params = _params(spec["fn"])
            props = {p["name"]: {**p['schema'],
                                  **({} if p["default"] is None
                                                       else {"default": p["default"]})}
                     for p in params}
            required = [p["name"] for p in params if p["required"]]
            paths[f"/v1/{spec['feature']}"] = {
                "get": {
                    "operationId": name,
                    "summary": _summary(spec["fn"]),
                    "description": _description(spec["fn"]) + f"\n\nCost: {pricing.credits(spec['feature'])} credits per successful call.",
                    "tags": [spec["group"]],
                    "parameters": [
                        {"name": p["name"], "in": "query",
                         "required": p["required"],
                         "schema": props[p["name"]]} for p in params],
                    "responses": {"200": {"description": "envelope",
                                          "content": {"application/json": {
                                              "schema": {"$ref": "#/components/schemas/Envelope"}}}},
                                  "404": {"description": "the corpus holds nothing for this input"},
                                  "400": {"description": "bad parameter"}},
                },
                "post": {
                    "operationId": f"{name}_post",
                    "summary": _summary(spec["fn"]),
                    "tags": [spec["group"]],
                    "requestBody": {"content": {"application/json": {"schema": {
                        "type": "object", "properties": props,
                        "required": required}}}},
                    "parameters": [{"name":"Prefer", "in":"header", "required":False,
                                    "schema":{"type":"string"},
                                    "description":"respond-async returns a request ID for supported editor features"}],
                    "responses": {"200": {"description": "envelope"},
                                  "202": {"description":"request accepted; poll data.poll for progress and result"}},
                },
            }
        return _json({
            "openapi": "3.1.0",
            "info": {"title": "Prism Research Layer",
                     "version": VERSION,
                     "description": (
                         "Prism's research and news corpora as callable features. "
                         "Every response uses one envelope; every number states "
                         "the window it was measured over and whether the cluster "
                         "was fully available when it was measured.")},
            "servers": [{"url": (request.scope.get("root_path") or "") + "/"}],
            "paths": paths,
            **({"security": [{"bearer": []}]} if access.PUBLIC else {}),
            "components": {**({"securitySchemes": {"bearer": {"type": "http", "scheme": "bearer",
                                                                "description": "Fliar API key (rdr_...)"}}} if access.PUBLIC else {}),
                           "schemas": {"Envelope": {
                "type": "object",
                "properties": {
                    "ok": {"type": "boolean"},
                    "feature": {"type": "string"},
                    "subject": {"type": "object"},
                    "data": {},
                    "window": {"type": "object"},
                    "meta": {"type": "object"},
                    "error": {"type": ["object", "null"],
                              "properties": {"kind": {"type": "string"},
                                             "reason": {"type": "string"}}},
                },
                "required": ["ok", "feature", "subject", "data", "window", "meta"]}}},
        })

    @mcp.custom_route("/healthz", methods=["GET"], name="healthz")
    async def healthz(request):
        from . import ch
        try:
            cov = await execution.run(ch.coverage_of, list(ch.CORPORA), health=True)
            body = {"ok": not cov["partial"], "service": "prism",
                    "features": len(registry), "coverage": cov}
            return _json(body, 200 if not cov["partial"] else 503)
        except Exception as e:
            return _json({"ok": False, "error": f"{type(e).__name__}: {e}"}, 503)

    @mcp.custom_route('/livez', methods=['GET'], name='livez')
    async def livez(request):
        return _json({'ok': True, 'service': 'prism', 'features': len(registry)})

    @mcp.custom_route('/readyz', methods=['GET'], name='readyz')
    async def readyz(request):
        from . import ch, articles, llm
        def check():
            cov = ch.coverage_of(list(ch.CORPORA))
            store = articles.health(all_nodes=True)
            model = llm.available()
            return {'ok': not cov['partial'] and store.get('available', False)
                          and model.get('configured', False),
                    'coverage': cov, 'article_store': store,
                    'model': {**model, 'check': 'configuration only; no generation probe'}}
        try:
            out = await execution.run(check, health=True)
            return _json(out, 200 if out['ok'] else 503)
        except Exception as e:
            return _json({'ok': False, 'error': str(e)}, 503)
