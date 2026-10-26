#!/usr/bin/env python3
"""profile_tool — where one Prism tool call spends its time.

Runs a registered tool in-process with the cache off and records every
ClickHouse request and every model call as a span (start, end, thread). CH
spans carry a query_id so read_rows / bytes / memory can be joined from
system.query_log afterwards.

  python3 tools/perf/profile_tool.py find_evidence '{"claim": "...", "limit": 10}' [out.json]
"""
import json, os, sys, threading, time, uuid
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, ROOT)
os.environ.setdefault("PRISM_CACHE", "0")

from prism import ch, llm  # noqa: E402

T0 = time.time()
SPANS = []
# Extra CH settings for an A/B run, e.g.
#   PROF_CH_EXTRA='connect_timeout_with_failover_ms=100&connections_with_failover_max_tries=2'
import urllib.parse as _up
_EXTRA = dict(_up.parse_qsl(os.environ.get("PROF_CH_EXTRA", "")))
_L = threading.Lock()
_orig_request = ch._request
_orig_text = llm.text


def _request(sql, timeout, strict):
    qid = "prof-" + uuid.uuid4().hex[:16]
    params_sql = sql
    t = time.time()
    err = None
    # inject a query_id by patching the params dict for this call only
    import urllib.parse, urllib.request
    params = {**ch._PARAMS, 'skip_unavailable_shards': '0' if strict else '1',
              'max_execution_time': str(min(280, max(1, int(timeout)))), 'query_id': qid,
              **_EXTRA}
    req = urllib.request.Request(ch.CH_HOST + '/?' + urllib.parse.urlencode(params), data=sql.encode())
    try:
        out = urllib.request.urlopen(req, timeout=timeout).read().decode()
        return out
    except Exception as e:
        err = f"{type(e).__name__}: {str(e)[:200]}"
        raise ch.CHError(err) from None
    finally:
        with _L:
            SPANS.append({"kind": "ch", "qid": qid, "t0": round(t - T0, 3), "t1": round(time.time() - T0, 3),
                          "thread": threading.current_thread().name, "sql": " ".join(params_sql.split())[:600],
                          "error": err})


def _text(system, user, max_tokens=4000, temperature=0.2, effort=llm.EFFORT):
    t = time.time()
    err = None
    out = None
    try:
        out = _orig_text(system, user, max_tokens=max_tokens, temperature=temperature, effort=effort)
        return out
    except Exception as e:
        err = f"{type(e).__name__}: {str(e)[:200]}"
        raise
    finally:
        with _L:
            SPANS.append({"kind": "llm", "t0": round(t - T0, 3), "t1": round(time.time() - T0, 3),
                          "thread": threading.current_thread().name, "prompt_chars": len(system) + len(user),
                          "max_tokens": max_tokens, "effort": effort, "finish": llm.LAST.get("finish"),
                          "out_chars": len(out or ""), "error": err, "sys": system[:80]})


ch._request = _request
llm.text = _text

import prism_mcp  # noqa: E402


def main():
    name, args = sys.argv[1], json.loads(sys.argv[2])
    out_path = sys.argv[3] if len(sys.argv) > 3 else None
    fn = prism_mcp.REGISTRY[name]["fn"]
    t = time.time()
    env = fn(**args)
    wall = time.time() - t
    time.sleep(8)  # query_log flushes ~7.5 s late
    qids = [s["qid"] for s in SPANS if s["kind"] == "ch"]
    stats = {}
    if qids:
        rows = ch.chq_rows(
            "SELECT query_id, query_duration_ms, read_rows, read_bytes, memory_usage, result_rows "
            "FROM system.query_log WHERE type IN ('QueryFinish','ExceptionWhileProcessing') "
            f"AND event_date >= today()-1 AND query_id IN {ch.sql_arr(qids)}", timeout=60)
        stats = {r[0]: {"ms": int(r[1]), "read_rows": int(r[2]), "read_bytes": int(r[3]),
                        "mem": int(r[4]), "result_rows": int(r[5])} for r in rows}
    for s in SPANS:
        if s["kind"] == "ch":
            s.update(stats.get(s["qid"], {}))
    ch_spans = [s for s in SPANS if s["kind"] == "ch"]
    llm_spans = [s for s in SPANS if s["kind"] == "llm"]

    def union(spans):
        iv = sorted((s["t0"], s["t1"]) for s in spans)
        tot, cur = 0.0, None
        for a, b in iv:
            if cur is None or a > cur[1]:
                if cur: tot += cur[1] - cur[0]
                cur = [a, b]
            else:
                cur[1] = max(cur[1], b)
        if cur: tot += cur[1] - cur[0]
        return round(tot, 1)
    summary = {
        "tool": name, "args": args, "wall_s": round(wall, 1), "ok": env.get("ok"),
        "ch_calls": len(ch_spans), "ch_sum_s": round(sum(s["t1"] - s["t0"] for s in ch_spans), 1),
        "ch_wall_s": union(ch_spans),
        "ch_read_rows": sum(s.get("read_rows", 0) for s in ch_spans),
        "ch_read_gb": round(sum(s.get("read_bytes", 0) for s in ch_spans) / 1e9, 2),
        "llm_calls": len(llm_spans), "llm_sum_s": round(sum(s["t1"] - s["t0"] for s in llm_spans), 1),
        "llm_wall_s": union(llm_spans),
        "either_wall_s": union(ch_spans + llm_spans),
    }
    print(json.dumps(summary, indent=1))
    print("\nTOP CH by duration:")
    for s in sorted(ch_spans, key=lambda s: s["t1"] - s["t0"], reverse=True)[:12]:
        print(f"  {s['t1']-s['t0']:6.1f}s  @{s['t0']:6.1f}  rows={s.get('read_rows',0):>12,}  "
              f"{(s.get('read_bytes',0)/1e9):6.2f}GB  {s['sql'][:200]}")
    print("\nLLM calls:")
    for s in sorted(llm_spans, key=lambda s: s["t0"]):
        print(f"  {s['t1']-s['t0']:6.1f}s  @{s['t0']:6.1f}  in={s['prompt_chars']:>6} out={s['out_chars']:>6} "
              f"max={s['max_tokens']} fin={s['finish']} {s['thread'][:18]}  {s['sys'][:60]!r}")
    if out_path:
        json.dump({"summary": summary, "spans": SPANS, "envelope_meta": env.get("meta")},
                  open(out_path, "w"), indent=1, default=str)


if __name__ == "__main__":
    main()
