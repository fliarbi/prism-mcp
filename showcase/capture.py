"""Run each scenario's Prism tool plan against the live corpora and save the responses.

    python3 showcase/capture.py                 # every scenario not yet captured
    python3 showcase/capture.py --only slug,..  # named scenarios (re-capture)
    python3 showcase/capture.py --workers 4

Each scenario runs in its own subprocess (the registry holds module-level state),
and writes docs/examples/<slug>.json:
    {slug, captured_at, calls: [{tool, feature, args, seconds, response}]}
A call that raises is saved with its error; the page builder shows it as a gap,
because a missing answer is still an answer.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "showcase"))
OUT = os.path.join(ROOT, "docs", "examples")

NEWS_SINCE = "2024-06-01"


def plan(s: dict) -> list[tuple[str, dict]]:
    a, p = s["args"], s["pattern"]
    if p == "pulse":
        return [("prism_overview", {"term": a["term"], "since": NEWS_SINCE})]
    if p == "evidence":
        return [("find_evidence", {"claim": a["claim"], "limit": 10}),
                ("find_counter_evidence", {"claim": a["claim"], "limit": 8}),
                ("find_statistics", {"claim": a["claim"], "limit": 6})]
    if p == "stance":
        return [("stance_trends", {"term": a["term"]}),
                ("browse_research", {"term": a["term"], "orientation": "promising", "limit": 8})]
    if p == "brief":
        return [("research_brief", {"topic": a["topic"], "geo": a.get("geo", "")}),
                ("news_trends", {"term": a["term"], "since": NEWS_SINCE})]
    if p == "compare":
        return [("compare_terms", {"terms": a["terms"], "since": NEWS_SINCE})]
    if p == "claims":
        return [("compare_claims", {"claim_a": a["claim_a"], "claim_b": a["claim_b"]})]
    if p == "radar":
        return [("research_radar", {"topic": a["topic"], "since_year": a.get("since_year", 0)})]
    if p == "table":
        return [("research_table", {"rows": a["rows"], "question": a["table_question"]})]
    if p == "audit":
        return [("research_audit", {"text": a["text"], "deep": 3})]
    if p == "geo":
        return [("global_comparison", {"claim": a["claim"]}),
                ("news_geography", {"term": a["term"], "since": NEWS_SINCE})]
    if p == "trending":
        return [("trending_topics", {"days": a["days"], "category": a.get("category", ""), "limit": 15})]
    if p == "history":
        return [("historical_analysis", {"subject_phrases": a["subject_phrases"],
                                         "outcome_phrases": a.get("outcome_phrases"),
                                         "query_seconds": 30}),
                ("trend_scenarios", {"history_id": "$history_id", "horizon": 3})]
    if p == "citations":
        return [("get_citations", {"claim": a["claim"], "style": a["style"], "limit": 8}),
                ("rank_sources", {"claim": a["claim"], "limit": 8})]
    if p == "improve":
        return [("improve_claim", {"claim": a["claim"]}),
                ("evidence_card", {"claim": a["claim"]})]
    if p == "library":
        return [("library_gaps", {"items": a["items"], "subject": a["subject"]})]
    raise ValueError(p)


def run_one(slug: str) -> dict:
    """Runs inside the child process."""
    import prism_mcp as m
    from scenarios import BY_SLUG
    s = BY_SLUG[slug]
    calls, ctx = [], {}
    for tool, args in plan(s):
        refs = [k for k, v in args.items() if isinstance(v, str) and v.startswith("$")]
        args = {k: (ctx.get(v[1:]) if isinstance(v, str) and v.startswith("$") else v) for k, v in args.items()}
        entry = m.REGISTRY[tool]
        if any(args[k] is None for k in refs):
            # A dependent call whose input never arrived (the upstream call
            # failed): record the skip instead of sending a null argument.
            calls.append({"tool": tool, "feature": entry["feature"], "args": args, "seconds": 0,
                          "response": {"ok": False, "error": {"kind": "upstream",
                                       "reason": "skipped: the call this one depends on returned no result"}}})
            continue
        t0 = time.time()
        try:
            resp = entry["fn"](**args)
        except Exception as e:  # saved, never hidden
            resp = {"ok": False, "error": {"kind": "internal", "message": f"{type(e).__name__}: {e}"}}
        dt = round(time.time() - t0, 1)
        data = (resp or {}).get("data") or {}
        if isinstance(data, dict) and data.get("history_id"):
            ctx["history_id"] = data["history_id"]
        calls.append({"tool": tool, "feature": entry["feature"], "args": args, "seconds": dt, "response": resp})
    return {"slug": slug, "captured_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "calls": calls}


def child(slug):
    out = run_one(slug)
    os.makedirs(OUT, exist_ok=True)
    tmp = os.path.join(OUT, f".{slug}.json.part")
    with open(tmp, "w") as f:
        json.dump(out, f, ensure_ascii=False, indent=1, default=str)
    os.replace(tmp, os.path.join(OUT, f"{slug}.json"))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--child", default="")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    if a.child:
        child(a.child)
        return
    from scenarios import SCENARIOS
    slugs = [s["slug"] for s in SCENARIOS]
    if a.only:
        slugs = [x for x in a.only.split(",") if x]
    elif not a.force:
        slugs = [x for x in slugs if not os.path.exists(os.path.join(OUT, f"{x}.json"))]
    print(f"capturing {len(slugs)} scenarios with {a.workers} workers", flush=True)

    def go(slug):
        t0 = time.time()
        r = subprocess.run([sys.executable, __file__, "--child", slug], cwd=ROOT,
                           capture_output=True, text=True, timeout=1800)
        ok = r.returncode == 0
        print(f"{'ok ' if ok else 'ERR'} {slug} {time.time()-t0:.0f}s {'' if ok else r.stderr[-400:]}", flush=True)

    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(go, slugs))


if __name__ == "__main__":
    main()
