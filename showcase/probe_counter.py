"""Probe the counter-evidence tool on one claim: python3 showcase/probe_counter.py "claim" """
import sys, json, time
sys.path.insert(0, __import__("os").path.dirname(__import__("os").path.dirname(__import__("os").path.abspath(__file__))))
import prism_mcp as m
t = time.time()
r = m.REGISTRY["find_counter_evidence"]["fn"](claim=sys.argv[1], limit=12)
d = r.get("data") or {}
print("ok", r.get("ok"), r.get("error"), round(time.time() - t), "s")
print("tally", json.dumps((d.get("tally") or {}).get("counts")))
for x in d.get("contradicting", []):
    print(" AGAINST", x.get("stance"), x.get("year"), x.get("tier"), x.get("lane"), "|", x.get("title", "")[:80], "|", (x.get("quote") or "")[:160])
for x in d.get("supporting", [])[:4]:
    print(" FOR", x.get("year"), x.get("tier"), "|", x.get("title", "")[:80])
print("rec", d.get("recommendation"))
