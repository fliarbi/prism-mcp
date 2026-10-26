"""Turn measured feature costs into the credit table in prism/pricing.py.

Cost of one call = compute + model:
    compute  = median wall seconds x COMPUTE_USD_PER_S   (the share of the index cluster a call occupies)
    model    = estimated model tokens x MODEL_USD_PER_TOKEN (reading, naming and writing calls)
Price = cost x MARGIN, rounded up to the next credit tier, at 1 credit = US$0.01 (84 paise), never below 1.

Wall seconds come from docs/engineering/feature_timings.json (real uncached calls recorded in the showcase,
benchmark and dashboard sessions); token estimates are per feature below and are replaced by measured values
from docs/engineering/feature_costs.json whenever tools/measure_costs.py has run on a healthy cluster.

    python3 tools/price_features.py      # prints the table and writes prism/pricing_table.json
"""
import json
import math
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

CREDIT_USD = 0.01
COMPUTE_USD_PER_S = 0.0003     # conservative: 2x a cluster-month spread over its realistic concurrent capacity
MODEL_USD_PER_TOKEN = 0.75e-6  # blended reading/writing rate, output-token price as the ceiling
MARGIN = 3.0
TIERS = (1, 2, 3, 5, 8, 12, 20, 30, 50, 80)

# model tokens per call (prompt + completion), estimated from each feature's reading and writing passes
TOKENS = {
    "research.evidence": 25000, "research.counter_evidence": 12000, "research.statistics": 8000,
    "research.brief": 30000, "research.radar": 15000, "research.audit": 20000, "research.table": 20000,
    "research.compare": 40000, "research.improve": 15000, "research.evidence_card": 15000,
    "research.citations": 2000, "research.library_gaps": 6000, "research.stance_trends": 400,
    "research.browse": 600, "research.geography": 500, "research.gaps": 10000, "research.missing": 10000,
    "research.search": 1000, "research.plan": 3000, "research.claims": 3000, "research.source_ranking": 2000,
    "research.packet": 20000, "research.packet_read": 0, "analysis.history": 500, "analysis.scenarios": 0,
    "news.overview": 2000, "news.critical": 1000, "news.recent": 500,
    "compose.article": 40000, "compose.section": 12000, "compose.sections": 6000, "compose.titles": 3000,
    "compose.continue": 6000, "compose.context": 8000, "compose.emphasise": 3000, "compose.quick_story": 12000,
    "compose.chart": 0, "compose.report_check": 0, "drive.plan": 4000,
    "news.activities": 0, "news.drill": 0, "news.factors": 8000, "analysis.timeline": 60000, "research.disease": 0,
}
# features never measured in a recorded session: wall seconds by analogy
SECONDS_DEFAULT = {"news": 15, "research": 40, "analysis": 10, "compose": 60, "system": 1, "drive": 30}
SECONDS_OVERRIDE = {"news.factors": 45, "news.activities": 20, "news.drill": 30, "analysis.timeline": 180, "research.disease": 3,
                    "compose.article": 240, "compose.section": 90, "compose.quick_story": 120,
                    "compose.report_check": 15, "compose.chart": 10, "news.article": 3, "news.sentiment": 20,
                    "news.entities": 20, "news.sources": 20}


def tier(credits):
    return next((t for t in TIERS if t >= credits), TIERS[-1])


def build():
    import prism_mcp as m
    from prism import pricing
    timings = json.load(open(os.path.join(ROOT, "docs", "engineering", "feature_timings.json")))
    by_feature = {v["feature"]: v for v in timings.values()}
    measured = {}
    p = os.path.join(ROOT, "docs", "engineering", "feature_costs.json")
    if os.path.exists(p):
        for v in json.load(open(p)).values():
            good = [r for r in v["runs"] if r["ok"]]
            if good:
                measured[v["feature"]] = sum(r["prompt_tokens"] + r["completion_tokens"] for r in good) / len(good)
    rows = {}
    for name, spec in m.REGISTRY.items():
        f, g = spec["feature"], spec["group"]
        if f in pricing.BLOCKED:
            continue
        secs = by_feature.get(f, {}).get("median_s") or SECONDS_OVERRIDE.get(f) or SECONDS_DEFAULT.get(g, 20)
        toks = measured.get(f, TOKENS.get(f, 0))
        cost = secs * COMPUTE_USD_PER_S + toks * MODEL_USD_PER_TOKEN
        credits = max(1, tier(math.ceil(cost * MARGIN / CREDIT_USD)))
        rows[f] = {"credits": credits, "est_cost_usd": round(cost, 4), "seconds": secs, "tokens": int(toks),
                   "price_usd": round(credits * CREDIT_USD, 2), "margin_x": round(credits * CREDIT_USD / cost, 1) if cost else None}
    return rows


if __name__ == "__main__":
    rows = build()
    for f, r in sorted(rows.items(), key=lambda kv: -kv[1]["credits"]):
        print(f"{f:28s} {r['credits']:3d} credits  ${r['price_usd']:.2f}  cost ${r['est_cost_usd']:.4f}  {r['seconds']:>6}s {r['tokens']:>6} tok  x{r['margin_x']}")
    json.dump({"credit_usd": CREDIT_USD, "compute_usd_per_s": COMPUTE_USD_PER_S, "model_usd_per_token": MODEL_USD_PER_TOKEN,
               "margin": MARGIN, "features": {f: r["credits"] for f, r in rows.items()}, "detail": rows},
              open(os.path.join(ROOT, "prism", "pricing_table.json"), "w"), indent=1)
