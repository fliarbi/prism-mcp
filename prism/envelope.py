#!/usr/bin/env python3
"""envelope — one response shape for every Prism feature.

Prism is operated programmatically here: by an MCP client, by a WordPress
plugin over HTTP, by an n8n node, by a spreadsheet. None of those can adapt to
a different payload shape per feature, so every function in this server returns
the same envelope and every endpoint returns it verbatim:

    {
      "ok":      bool,
      "feature": "news.trends",          # stable dotted id, never renamed
      "subject": {...},                  # what was asked about
      "data":    {...},                  # the answer, feature-specific
      "window":  {...},                  # the period the answer covers
      "meta":    {...},                  # timing, coverage, corpora, caveats
      "error":   {"kind": ..., "reason": ...}   # only when ok is false
    }

`ok: false` is a normal outcome, not a failure of the server: the corpus holds
nothing on this term, or the claim is not research-shaped. It always carries a
`kind` a caller can branch on (`no_data`, `not_resolvable`, `bad_request`,
`upstream`) and a `reason` a human can read.

`window` and `meta.coverage` are mandatory rather than decorative. Every count
in this system is bounded by an ingest lag and a shard state, and a number
printed without them has been wrong on this cluster before — a research series
run to "today" reads as a collapse, and a count taken during a shard outage
reads as a decline. The envelope makes both impossible to drop by accident.
"""
from __future__ import annotations

import re
import time
import traceback
from pydantic import ValidationError

KINDS = ("no_data", "not_resolvable", "bad_request", "upstream", "internal")


def ok(feature: str, data, subject=None, window=None, meta=None) -> dict:
    return {"ok": True, "feature": feature, "subject": subject or {},
            "data": data, "window": window or {}, "meta": meta or {}}


def fail(feature: str, reason: str, kind: str = "no_data", subject=None,
         meta=None) -> dict:
    return {"ok": False, "feature": feature, "subject": subject or {},
            "data": None, "window": {},
            "error": {"kind": kind if kind in KINDS else "internal",
                      "reason": reason},
            "meta": meta or {}}


# ── keys the legacy (pre-envelope) tool bodies use for the same concepts ─────
_WINDOW_KEYS = ("window", "windows", "censored_at", "why_censored", "since",
                "granularity", "unit", "from", "to", "to_is_exclusive",
                "enrichment", "labelled_by", 'freshness', 'past_default_cutoff')
_META_KEYS = ("coverage", "coverage_note", "lane", "lane_note", "lane_counts",
              "cached", "_meta", "note", "how", "caveat", "how_to_read",
              "note_on_geo", "phrase_source", "corpus", "match_mode",
              "match_mode_note", "ranked_by", "baseline", "thresholds",
              "fill_note", "fill_rates", "coverage_note")


def standardise(feature: str, out, subject=None, seconds: float | None = None):
    """Lift a plain result dict into the envelope without rewriting its body.

    The feature functions were written to return flat dicts with `available`,
    `reason`, `coverage`, `lane` … Rather than rewrite every one of them (and
    every place they call each other), this reads that vocabulary and moves it
    where the envelope expects it. Anything it does not recognise stays in
    `data`, so a feature can add a field without touching this file."""
    if isinstance(out, dict) and "ok" in out and "feature" in out:
        return out                      # already an envelope; pass through
    if not isinstance(out, dict):
        return ok(feature, out, subject=subject,
                  meta={"seconds": round(seconds, 1) if seconds else None})

    body = dict(out)
    available = body.pop("available", True)
    reason = body.pop("reason", None)
    kind = body.get('kind') if body.get('kind') in KINDS else None
    window = {k: body.pop(k) for k in _WINDOW_KEYS if k in body}
    if "window" in window:              # {"window": "2017-2025"} reads badly
        window["period"] = window.pop("window")
    meta = {k: body.pop(k) for k in _META_KEYS if k in body}
    inner = meta.pop("_meta", None)
    if isinstance(inner, dict):
        meta.update(inner)
    if seconds is not None:
        meta["seconds"] = round(seconds, 1)
    subject = subject or {}
    for k in ("claim", "topic", "term", "subject", "query", "question"):
        if k in body and k not in subject:
            v = body.pop(k)
            if isinstance(v, (str, int, float)):
                subject[k] = v
            else:
                body[k] = v
    if not available:
        if kind:
            body.pop('kind', None)
        e = fail(feature, reason or "no data", kind=kind or _kind_of(reason),
                 subject=subject, meta=meta)
        e['window'] = window
        e["data"] = body or None        # keep diagnostics (phrase audit, etc.)
        return e
    return ok(feature, body, subject=subject, window=window, meta=meta)


def _kind_of(reason: str | None) -> str:
    r = (reason or "").lower()
    if "empty" in r or "no rows given" in r or "give " in r or 'must be' in r:
        return "bad_request"
    if "resolv" in r or "not a research-shaped" in r or "identify a subject" in r:
        return "not_resolvable"
    if "clickhouse" in r or "ch " in r or "timed out" in r or "error" in r:
        return "upstream"
    return "no_data"


# ── public naming: no third-party index names in what callers see ───────────
# The research works corpus is served as the Prism research index. Record ids,
# table names and descriptions are rewritten on the way out so a report built
# from Prism cites DOIs and Prism ids, never the upstream index it was built from.
_PUBLIC = [
    (re.compile(r"https?://(?:api\.)?openalex\.org/(W\d+)", re.I), r"prism:\1"),
    (re.compile(r"\bopenalex:(W\d+)", re.I), r"prism:\1"),
    (re.compile(r"\bresearch\.openalex_prism(?:_distributed)?\b", re.I), "Prism typed research index"),
    (re.compile(r"\bopenalex\.\w+", re.I), "Prism research index"),
    (re.compile(r"\bOpenAlex (topic|work type|venue|concept|keyword|field)", re.I), r"research \1"),
    (re.compile(r"\bOpenAlex (works?|records?|papers?|titles?|ids?)\b", re.I), r"Prism research index \1"),
    (re.compile(r"\bOpenAlex\b", re.I), "Prism research index"),
]


def public_text(s: str) -> str:
    if "openalex" not in s.lower():
        return s
    for pat, rep in _PUBLIC:
        s = pat.sub(rep, s)
    return s


def public(o, key=None):
    """Recursively apply the public naming to every string (and dict key) in a response."""
    if isinstance(o, str):
        if key == "source" and o.lower() == "openalex":
            return "research"
        if key in ("url", "link", "href") and re.match(r"https?://(?:api\.)?openalex\.org/", o, re.I):
            return None  # no public link for an index record; callers fall back to the DOI or the Prism id
        return public_text(o)
    if isinstance(o, dict):
        out = {public_text(k) if isinstance(k, str) else k: public(v, k) for k, v in o.items()}
        for k in ("url", "link", "href"):
            if k in o and out.get(k) is None and isinstance(o[k], str) and o.get("doi"):
                d = str(o["doi"]).replace("https://doi.org/", "")
                out[k] = f"https://doi.org/{d}"
        return out
    if isinstance(o, list):
        return [public(v) for v in o]
    return o


import os as _os
PUBLIC_API = _os.environ.get("PRISM_PUBLIC", "0") == "1"
# On the public API no response names a store, table, host or upstream source.
_PUBLIC_EXTRA = [
    (re.compile(r"\b(?:CHError|URLError|OperationalError|ServerSelectionTimeoutError)\b:?\s*"), ""),
    (re.compile(r"/home/\S+"), "the server"),
    (re.compile(r"\b[a-z_]+\.[a-z0-9_]+_distributed\b"), "the index"),
    (re.compile(r"\b(?:192\.168|10\.\d+|100\.\d+)\.\d+\.\d+(?::\d+)?\b"), "an index node"),
    (re.compile(r"\bClickHouse\b", re.I), "the index"),
    (re.compile(r"\bPubMed\b"), "the health literature index"),
    (re.compile(r"\bMeSH\b"), "subject headings"),
    (re.compile(r"\bshards?\b", re.I), "index partition"),
    (re.compile(r"\bmongo\w*\b", re.I), "article store"),
    (re.compile(r"\b(?:Cerebras|gpt-oss-120b|Together AI|together:\S+|codex:\S+)", re.I), "the model"),
]
_DROP_META = {"trace", "cached", "cache_key", "queue_seconds", "execution_seconds"}


def _public_strings(o, key=None):
    if isinstance(o, str):
        for pat, rep in _PUBLIC_EXTRA:
            o = pat.sub(rep, o)
        return o
    if isinstance(o, dict):
        return {k: _public_strings(v, k) for k, v in o.items() if k not in ("table", "host", "hosts", "nodes", "node")}
    if isinstance(o, list):
        return [_public_strings(v) for v in o]
    return o


def public_api(env: dict) -> dict:
    """Extra scrub for the public deployment: no internal names, hosts, traces or cache keys."""
    if not isinstance(env, dict):
        return env
    meta = {k: v for k, v in (env.get("meta") or {}).items() if k not in _DROP_META}
    cov = meta.get("coverage")
    if isinstance(cov, dict):
        meta["coverage"] = {"partial": bool(cov.get("partial")),
                            "note": "part of the index was unavailable; counts are lower bounds" if cov.get("partial")
                            else "the whole index answered"}
    env = dict(env, meta=meta)
    return _public_strings(env)


def guard(feature: str, fn, /, *args, _subject=None, **kwargs) -> dict:
    out = public(_guard(feature, fn, *args, _subject=_subject, **kwargs))
    return public_api(out) if PUBLIC_API else out


def _guard(feature: str, fn, /, *args, _subject=None, **kwargs) -> dict:
    """Run a feature and return an envelope whatever happens.

    A tool that raises is a bug, but a caller mid-draft should get a readable
    `ok:false` rather than a transport-level error that their plugin renders as
    a blank sidebar. The traceback goes to `meta.trace` so it is still
    diagnosable from the response."""
    t0 = time.time()
    try:
        return standardise(feature, fn(*args, **kwargs), subject=_subject,
                           seconds=time.time() - t0)
    except ValidationError as e:
        return fail(feature, str(e), kind='bad_request', subject=_subject)
    except Exception as e:
        from .ch import CHError
        from urllib.error import URLError
        kind = 'upstream' if isinstance(e, (CHError, URLError, TimeoutError, ConnectionError)) else 'internal'
        return fail(feature, f"{type(e).__name__}: {e}", kind=kind,
                    subject=_subject,
                    meta={"seconds": round(time.time() - t0, 1),
                          "trace": traceback.format_exc()[-1200:]})
