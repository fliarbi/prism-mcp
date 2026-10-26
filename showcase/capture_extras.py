"""Add deeper Prism capabilities to existing demonstration captures, without re-running the base calls.

Each page shows a different capability, so a reader sees that Prism is not only news trends: areas of
activity and company events, drilling into one section of an entity (partnerships, AI partnerships, EVs),
and the month-by-month reading. Calls are appended to docs/examples/<slug>.json (replacing an earlier call
with the same tool and arguments).

    python3 showcase/capture_extras.py [--only slug,...] [--workers 3]
"""
import argparse
import json
import os
import sys
import time
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
EX = os.path.join(ROOT, "docs", "examples")

EXTRAS = {
    "reliance-industries-pulse": [
        ("news_activities", {"term": "reliance industries", "domain": "ril.com"}),
        ("news_drill", {"term": "reliance industries", "scope": "partnership"}),
        ("news_drill", {"term": "reliance industries", "scope": "partnership, artificial intelligence"}),
        ("deep_timeline", {"term": "reliance industries", "months": 12}),
    ],
    "hdfc-bank-pulse": [
        ("news_activities", {"term": "hdfc bank", "domain": "hdfcbank.com"}),
        ("news_drill", {"term": "hdfc bank", "scope": "merger"}),
        ("news_drill", {"term": "hdfc bank", "scope": "digital"}),
    ],
    "tata-motors-pulse": [
        ("news_activities", {"term": "tata motors", "domain": "tatamotors.com"}),
        ("news_drill", {"term": "tata motors", "scope": "electric vehicle"}),
        ("news_drill", {"term": "tata motors", "scope": "jaguar land rover, tariff"}),
        ("deep_timeline", {"term": "tata motors", "scope": "electric vehicle", "months": 12}),
    ],
    "modi-vs-trump": [
        ("news_drill", {"term": "donald trump", "scope": "india"}),
        ("news_drill", {"term": "narendra modi", "scope": "tariff"}),
        ("deep_timeline", {"term": "donald trump", "scope": "india", "months": 12}),
    ],
    "infosys-tcs-wipro": [
        ("news_activities", {"term": "infosys", "domain": "infosys.com"}),
        ("news_drill", {"term": "infosys", "scope": "artificial intelligence"}),
        ("news_drill", {"term": "tcs", "scope": "artificial intelligence"}),
        ("news_drill", {"term": "wipro", "scope": "artificial intelligence"}),
    ],
    "bengaluru-pulse": [
        ("news_activities", {"term": "bengaluru"}),
        ("news_drill", {"term": "bengaluru", "scope": "water"}),
        ("news_drill", {"term": "bengaluru", "scope": "traffic"}),
        ("news_geography", {"term": "bengaluru", "level": "city"}),
    ],
    "mumbai-delhi-bengaluru": [
        ("news_drill", {"term": "delhi", "scope": "air pollution"}),
        ("news_drill", {"term": "mumbai", "scope": "air pollution"}),
        ("news_drill", {"term": "bengaluru", "scope": "air pollution"}),
    ],
    "isro-pulse": [
        ("news_activities", {"term": "isro"}),
        ("news_drill", {"term": "isro", "scope": "gaganyaan"}),
        ("deep_timeline", {"term": "isro", "months": 12}),
    ],
}


def run(slug):
    import prism_mcp as m
    path = os.path.join(EX, f"{slug}.json")
    rec = json.load(open(path))
    calls = rec.get("calls") or []
    for tool, args in EXTRAS[slug]:
        t0 = time.time()
        try:
            resp = m.REGISTRY[tool]["fn"](**args)
        except Exception as e:
            resp = {"ok": False, "error": {"kind": "internal", "reason": f"{type(e).__name__}: {e}"}}
        entry = {"tool": tool, "feature": m.REGISTRY[tool]["feature"], "args": args,
                 "seconds": round(time.time() - t0, 1), "response": resp, "extra": True}
        calls = [c for c in calls if not (c["tool"] == tool and c.get("args") == args)] + [entry]
        print(f"  {slug} {tool} {json.dumps(args)[:60]} ok={resp.get('ok')} {entry['seconds']}s", flush=True)
    rec["calls"] = calls
    rec["extras_captured_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    tmp = path + ".part"
    json.dump(rec, open(tmp, "w"), ensure_ascii=False, indent=1, default=str)
    os.replace(tmp, path)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=3)
    a = ap.parse_args()
    slugs = a.only.split(",") if a.only else list(EXTRAS)
    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(run, slugs))
    print("EXTRAS_DONE", flush=True)
