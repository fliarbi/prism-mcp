"""Probe find_evidence on one claim: python3 showcase/probe_evidence.py "claim" """
import sys, json, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
import prism_mcp as m
t = time.time()
r = m.REGISTRY["find_evidence"]["fn"](claim=sys.argv[1], limit=10)
d = r.get("data") or {}
q = d.get("query") or {}
print("ok", r.get("ok"), r.get("error"), round(time.time() - t), "s", "lane", (r.get("meta") or {}).get("lane"), (r.get("meta") or {}).get("lane_note"))
print("poles", json.dumps(q.get("poles"))[:600])
print("tally", json.dumps((d.get("tally") or {}).get("counts")))
for x in d.get("documents", [])[:10]:
    print(" ", x.get("stance"), x.get("year"), x.get("tier"), x.get("lane"), "|", x.get("title", "")[:90])
