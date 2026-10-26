#!/usr/bin/env python3
"""waves — the serial depth of one profiled tool call.

Groups the CH/LLM spans of a profile_tool.py JSON into waves (maximal sets of
overlapping spans). Each wave is one step on the critical path; the number of
waves times the per-query floor is the latency no amount of parallel hardware
removes.  python3 tools/perf/waves.py prof.json"""
import json, sys
d = json.load(open(sys.argv[1]))
sp = sorted([s for s in d["spans"] if not s.get("sql", "").startswith("SELECT query_id")],
            key=lambda s: s["t0"])
waves, cur = [], None
for s in sp:
    if cur and s["t0"] < cur["t1"]:
        cur["t1"] = max(cur["t1"], s["t1"]); cur["n"] += 1; cur["kinds"].add(s["kind"])
        cur["gb"] += s.get("read_bytes", 0) / 1e9
    else:
        cur = {"t0": s["t0"], "t1": s["t1"], "n": 1, "kinds": {s["kind"]}, "gb": s.get("read_bytes", 0) / 1e9}
        waves.append(cur)
print(f"{d['summary']['tool']}: wall {d['summary']['wall_s']}s, {len(waves)} serial waves, "
      f"{sum(1 for s in sp if s['kind']=='ch')} CH queries, {d['summary']['ch_read_gb']} GB read")
for w in waves:
    print(f"  {w['t0']:6.1f}-{w['t1']:6.1f} {w['t1']-w['t0']:5.1f}s  x{w['n']:<3} {'+'.join(sorted(w['kinds'])):7} {w['gb']:6.1f} GB")
