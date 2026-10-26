#!/usr/bin/env python3
"""cache — a small on-disk cache shared by every tool.

A writer's editor calls this server on selection, on save, and on publish. The
same claim gets asked about repeatedly within one drafting session, and a cold
evidence lookup is 5-15 seconds of ClickHouse over 384M rows. Cached, it is
milliseconds.

SQLite rather than a dict because the WordPress/HTTP deployment runs several
worker processes against one cache, and because a drafting session that spans
a lunch break should still be warm.

Nothing here caches a FAILURE. A thin result is a legitimate answer and is
cached; an exception or a partial-cluster read is not — otherwise a five-minute
shard outage would be served as fact for the next twelve hours.
"""
from __future__ import annotations

import hashlib
import copy
import functools
import inspect
import json
import os
import sqlite3
import threading
import time
from concurrent.futures import Future

CACHE_DIR = os.environ.get(
    "PRISM_CACHE_DIR", os.path.join(os.path.dirname(os.path.dirname(
        os.path.abspath(__file__))), "cache"))
os.makedirs(CACHE_DIR, exist_ok=True)
DB_PATH = os.path.join(CACHE_DIR, "prism_cache.db")

DEFAULT_TTL = int(os.environ.get("PRISM_CACHE_TTL", "43200"))   # 12h
_LOCK = threading.Lock()
_CONN = None
ENABLED = os.environ.get("PRISM_CACHE", "1") != "0"
_FLIGHTS = {}
_FLIGHT_LOCK = threading.Lock()


def singleflight(fn):
    """Share overlapping identical reads; exceptions are never retained."""
    signature = inspect.signature(fn)
    @functools.wraps(fn)
    def wrapped(*args, **kwargs):
        bound = signature.bind(*args, **kwargs)
        bound.apply_defaults()
        k = key('inflight-v1', fn.__module__, fn.__name__, bound.arguments)
        with _FLIGHT_LOCK:
            future = _FLIGHTS.get(k)
            owner = future is None
            if owner:
                future = _FLIGHTS[k] = Future()
        if not owner:
            return copy.deepcopy(future.result())
        try:
            value = fn(*args, **kwargs)
            future.set_result(copy.deepcopy(value))
            return value
        except BaseException as exc:
            future.set_exception(exc)
            raise
        finally:
            with _FLIGHT_LOCK:
                _FLIGHTS.pop(k, None)
    return wrapped


def remember(ttl, extra=lambda: None):
    """Reuse successful, fully covered, grounded editor results only."""
    def decorate(fn):
        signature = inspect.signature(fn)
        @singleflight
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            bound = signature.bind(*args, **kwargs)
            bound.apply_defaults()
            k = key('editor-result-v3', fn.__module__, fn.__name__, bound.arguments, extra())
            hit = get(k)
            if hit is not None:
                from . import progress
                progress.emit('cached')
                return {**hit, 'cached': True}
            out = fn(*args, **kwargs)
            if (isinstance(out, dict) and out.get('available')
                    and not (out.get('coverage') or {}).get('partial', True)
                    and out.get('grounded', True)
                    and all(x.get('grounded', True) for x in out.get('titles', []))
                    and (out.get('next_paragraph') or {}).get('grounded', True)):
                put(k, out, min(ttl, 60) if out.get('fallback') else ttl)
            return out
        return wrapped
    return decorate


def _conn():
    global _CONN
    if _CONN is None:
        _CONN = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=10)
        _CONN.execute("PRAGMA journal_mode=WAL")
        _CONN.execute("CREATE TABLE IF NOT EXISTS kv "
                      "(k TEXT PRIMARY KEY, v TEXT, exp REAL, made REAL)")
        _CONN.commit()
    return _CONN


def key(*parts) -> str:
    # Old cached verdicts and rates predate the stricter verification/math.
    # Version the namespace; retain existing data for recovery.
    raw = json.dumps(('correctness-20260912-v4', *parts), sort_keys=True, default=str)
    return hashlib.sha1(raw.encode()).hexdigest()


def get(k: str):
    if not ENABLED:
        return None
    try:
        with _LOCK:
            row = _conn().execute(
                "SELECT v, exp FROM kv WHERE k=?", (k,)).fetchone()
        if not row or row[1] < time.time():
            return None
        return json.loads(row[0])
    except Exception:
        return None


def put(k: str, value, ttl: int = DEFAULT_TTL) -> None:
    if not ENABLED:
        return
    try:
        with _LOCK:
            _conn().execute(
                "INSERT OR REPLACE INTO kv(k,v,exp,made) VALUES (?,?,?,?)",
                (k, json.dumps(value, default=str), time.time() + ttl, time.time()))
            _conn().commit()
    except Exception:
        pass


def memo(ttl: int, *parts):
    """Decorator-free helper: `hit = cache.memo(TTL, 'evidence', claim)` gives a
    (value, setter) pair so a caller can bail early on a hit."""
    k = key(*parts)
    return get(k), (lambda v: put(k, v, ttl))


def stats() -> dict:
    try:
        with _LOCK:
            n, live = _conn().execute(
                "SELECT count(), sum(exp > ?) FROM kv", (time.time(),)).fetchone()
        return {"path": DB_PATH, "entries": n or 0, "live": live or 0,
                "enabled": ENABLED}
    except Exception as e:
        return {"path": DB_PATH, "error": f"{type(e).__name__}: {e}"}


def purge(expired_only: bool = True) -> int:
    try:
        with _LOCK:
            c = _conn()
            cur = (c.execute("DELETE FROM kv WHERE exp < ?", (time.time(),))
                   if expired_only else c.execute("DELETE FROM kv"))
            c.commit()
            return cur.rowcount
    except Exception:
        return 0
