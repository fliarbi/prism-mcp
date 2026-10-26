"""Measure what each Prism feature costs to run: wall seconds and model tokens, with the cache off.

Arguments come from real calls the showcase and benchmark sessions made (docs/examples, docs/benchmark/deep),
so every feature is measured on the kind of input it actually receives. Output: docs/engineering/feature_costs.json,
which tools/price_features.py turns into the credit table.

    PRISM_CACHE=0 python3 tools/measure_costs.py [--per 2]
"""
import argparse
import glob
import json
import os
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
os.environ.setdefault("PRISM_CACHE", "0")


def samples(per):
    seen = {}
    for f in sorted(glob.glob(os.path.join(ROOT, "docs", "examples", "*.json"))):
        for c in json.load(open(f)).get("calls") or []:
            if not any(isinstance(v, str) and v.startswith("$") for v in (c.get("args") or {}).values()):
                seen.setdefault(c["tool"], []).append(c["args"])
    for f in glob.glob(os.path.join(ROOT, "docs", "benchmark", "deep", "*", "runs.json")):
        for k, run in json.load(open(f)).items():
            if isinstance(run, dict):
                for c in run.get("calls") or []:
                    t = c["tool"].split("__")[-1].replace("prism.", "")
                    if isinstance(c.get("args"), dict):
                        seen.setdefault(t, []).append(c["args"])
    out = {}
    for t, args in seen.items():
        uniq = []
        for a in args:
            if a not in uniq:
                uniq.append(a)
        step = max(1, len(uniq) // per)
        out[t] = uniq[::step][:per]
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--per", type=int, default=2)
    a = ap.parse_args()
    import prism_mcp as m
    from prism import llm
    res = {}
    for tool, argsets in sorted(samples(a.per).items()):
        if tool not in m.REGISTRY or tool in ("check_report",):
            continue
        runs = []
        for args in argsets:
            p0, c0, n0 = llm.METER["prompt"], llm.METER["completion"], llm.METER["calls"]
            t0 = time.time()
            try:
                r = m.REGISTRY[tool]["fn"](**args)
                ok = bool(r.get("ok"))
            except Exception as e:
                ok = False
            runs.append({"seconds": round(time.time() - t0, 1), "ok": ok, "llm_calls": llm.METER["calls"] - n0,
                         "prompt_tokens": llm.METER["prompt"] - p0, "completion_tokens": llm.METER["completion"] - c0})
            print(tool, runs[-1], flush=True)
        res[tool] = {"feature": m.REGISTRY[tool]["feature"], "runs": runs}
        json.dump(res, open(os.path.join(ROOT, "docs", "engineering", "feature_costs.json"), "w"), indent=1)
    print("MEASURE_DONE", flush=True)


if __name__ == "__main__":
    main()
