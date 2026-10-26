#!/usr/bin/env python3
"""smoke_test — call every tool against the live cluster and show what came back.

Run it after any change to the retrieval or the gates:

    python3 smoke_test.py            # all tools
    python3 smoke_test.py find_evidence rank_sources
    PRISM_CACHE=0 python3 smoke_test.py   # cold

It is a smoke test, not an assertion suite: the corpus moves, so it prints what
each tool returned and flags the two things that are always wrong — a tool that
raised, and a tool that returned `available: true` with nothing in it. Full
payloads are written to out/smoke_<tool>.json for reading.
"""
from __future__ import annotations

import json
import os
import sys
import time
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import prism_mcp as P

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "out")
os.makedirs(OUT, exist_ok=True)

DRAFT = (
    "Vitamin D deficiency has become increasingly common worldwide, particularly "
    "among people living in urban areas. Researchers have proven that low sun "
    "exposure is the leading cause. Coffee improves cardiovascular health, so many "
    "doctors now recommend it to older patients. India's healthcare market will "
    "reach $500 billion by 2030. Air pollution is associated with increased "
    "cardiovascular risk, according to several large cohort studies "
    "(https://doi.org/10.1016/S0140-6736(20)30752-2). Personally, I think this is "
    "the most important health story of the decade."
)
CLAIM = "Coffee improves cardiovascular health."

TERM = "electric vehicle"

# Every case reads through the ENVELOPE now: r["ok"], r["data"], r["error"].
CASES = [
    ("corpus_status", P.corpus_status, {},
     lambda r: r["corpora"]["research"]["rows"]),
    ("extract_claims", P.extract_claims, {"text": DRAFT}, lambda r: r["checkable"]),
    ("find_evidence", P.find_evidence, {"claim": CLAIM, "limit": 14},
     lambda r: (r["tally"] or {}).get("counts")),
    ("evidence_card", P.evidence_card, {"claim": CLAIM},
     lambda r: r["card"]["title"][:60]),
    ("find_counter_evidence", P.find_counter_evidence, {"claim": CLAIM},
     lambda r: f"{len(r['contradicting'])} against / {len(r['supporting'])} for"),
    ("research_gaps", P.research_gaps,
     {"claim": "AI will replace many accounting jobs."},
     lambda r: f"{r['covered']} covered / {r['unevidenced']} unevidenced"),
    ("find_statistics", P.find_statistics, {"claim": CLAIM},
     lambda r: [s["value"] for s in r.get("stats", [])][:3]),
    ("whats_missing", P.whats_missing, {"text": DRAFT, "subject": "vitamin D deficiency"},
     lambda r: [m["topic"] for m in r.get("missing", [])][:3]),
    ("rank_sources", P.rank_sources, {"claim": CLAIM}, lambda r: r["by_tier"]),
    ("get_citations", P.get_citations, {"claim": CLAIM, "style": "apa", "limit": 4},
     lambda r: r["entries"][0]["citation"][:70]),
    ("research_audit", P.research_audit, {"text": DRAFT},
     lambda r: (r["evidence_coverage"], r["by_status"])),
    ("research_radar", P.research_radar, {"topic": "Alzheimer's disease"},
     lambda r: ((r.get("research_trend") or {}).get("direction"),
                len(r.get("new_work") or []))),
    ("search_research", P.search_research, {"query_text": "microplastics in drinking water"},
     lambda r: r["found"]),
    ("compare_claims", P.compare_claims,
     {"claim_a": CLAIM, "claim_b": "Green tea improves cardiovascular health.",
      "read": False}, lambda r: r["verdict"]),
    ("improve_claim", P.improve_claim, {"claim": CLAIM},
     lambda r: (r.get("verdict"), (r.get("options") or [{}])[0].get("text", "")[:70])),
    ("research_brief", P.research_brief, {"topic": "groundwater depletion in India"},
     lambda r: len(r.get("key_numbers") or [])),
    ("research_table", P.research_table,
     {"rows": ["Tesla", "BYD"], "question": "electric vehicle battery range research"},
     lambda r: f"{r['answered']}/{r['of']}"),
    ("library_gaps", P.library_gaps,
     {"items": ["10.1016/S0140-6736(20)30752-2"], "subject": "air pollution health"},
     lambda r: len(r.get("highly_cited_missing") or [])),
    ("global_comparison", P.global_comparison,
     {"claim": "Air pollution increases cardiovascular risk", "country": "India"},
     lambda r: [x["country"] for x in r["news_coverage"]["rows"][:3]]),
    ("browse_research", P.browse_research,
     {"term": "ease of doing business in india", "orientation": "promising",
      "limit": 3},
     lambda r: (r["matched"], [f["orientation"] for f in r["facets"]["orientation"][:3]])),
    ("stance_trends", P.stance_trends, {"term": "generative ai in education"},
     lambda r: (r["papers"], r["framing_shift"]["reading"][:40])),
    # ── general Prism: the news corpus ──────────────────────────────────────
    ("resolve_term", P.resolve_term, {"term": "Tesla"},
     lambda r: (r["type"], r["articles"])),
    ("news_trends", P.news_trends, {"term": TERM, "granularity": "quarterly"},
     lambda r: (len(r["points"]), r["trend"]["direction"])),
    ("recent_news", P.recent_news, {"term": TERM, "limit": 3},
     lambda r: (r["articles"][0].get("title") or "")[:50]),
    ("critical_news", P.critical_news, {"term": TERM, "limit": 3},
     lambda r: [a.get("priority") for a in r["articles"]]),
    ("news_sentiment", P.news_sentiment, {"term": TERM},
     lambda r: (r["totals"]["ratio"], r["corpus_baseline_ratio"])),
    ("news_themes", P.news_themes, {"term": TERM},
     lambda r: [x["label"] for x in r["categories"]["rows"][:3]]),
    ("news_entities", P.news_entities, {"term": TERM},
     lambda r: [x["label"] for x in r["organizations"]["rows"][:3]]),
    ("news_geography", P.news_geography, {"term": TERM},
     lambda r: [x["label"] for x in r["rows"][:4]]),
    ("news_sources", P.news_sources, {"term": TERM},
     lambda r: [p["publisher"] for p in r["publishers"][:3]]),
    ("trending_topics", P.trending_topics, {"days": 14, "limit": 5},
     lambda r: [x["topic"][:28] for x in r["rising"][:3]]),
    ("compare_terms", P.compare_terms,
     {"terms": ["electric vehicle", "hydrogen fuel cell"]},
     lambda r: [(x["term"], x["articles"]) for x in r["rows"]]),
    ("prism_overview", P.prism_overview, {"term": "solar power"},
     lambda r: r["panels_available"]),
    ("get_article", P.get_article, {"target_id": "__from_feed__"},
     lambda r: (r["article"].get("title") or r["article"].get("excerpt") or "")[:50]),
    # ── composition ─────────────────────────────────────────────────────────
    ("continue_paragraph", P.continue_paragraph,
     {"draft": "To make the Make in India campaign succeed, the government's "
               "efforts have been modest and the evidence is contested.",
      "topic": "make in india"},
     lambda r: (r["written_by"], len(r["alternatives"]),
                r["next_paragraph"]["grounded"])),
    ("suggest_sections", P.suggest_sections, {"topic": "make in india"},
     lambda r: [s["key"] for s in r["sections"][:4]]),
    ("write_section", P.write_section,
     {"topic": "make in india", "section": "state_of_evidence"},
     lambda r: (r["grounded"], r["honorifics_removed"], len(r["sources"]))),
    ("suggest_titles", P.suggest_titles, {"topic": "solid state batteries"},
     lambda r: (r["titles"][0]["title"] or "")[:52]),
    ("write_article", P.write_article,
     {"topic": "solid state batteries", "max_sections": 2, "background": False},
     lambda r: (r["words"], r["grounding"]["sections_written"])),
    ("list_jobs", P.list_jobs, {}, lambda r: len(r["jobs"])),
    ("resolve_vocabulary", P.resolve_vocabulary,
     {"term": "herniated disc surgery complications"},
     lambda r: [m["label"] for m in r["best_overall"][:3]]),
    ("vocabulary_status", P.vocabulary_status, {},
     lambda r: sum(1 for v in r["status"].values() if v.get("built"))),
    ("list_features", P.list_features, {}, lambda r: r["count"]),
    ("article_store_status", P.article_store_status, {},
     lambda r: r.get("ring_nodes")),
]


def main() -> int:
    if '--contracts' in sys.argv:
        import subprocess
        return subprocess.call([sys.executable, '-m', 'unittest', 'discover',
                                '-s', str(os.path.join(os.path.dirname(__file__), 'tests')), '-v'])
    want = set(sys.argv[1:])
    rows, failed = [], 0
    for name, fn, kw, summarise in CASES:
        if want and name not in want:
            continue
        if kw.get("target_id") == "__from_feed__":
            # get_article needs a real id, and ids rotate. Take one from a feed
            # rather than pinning a literal that will 404 next month.
            feed = P.recent_news(term=TERM, limit=1)
            got = ((feed.get("data") or {}).get("articles") or [{}])[0]
            if not got.get("target_id"):
                rows.append((name, "SKIP", 0.0, "no feed article to resolve"))
                continue
            kw = {"target_id": got["target_id"]}
        t0 = time.time()
        try:
            out = fn(**kw)
            secs = round(time.time() - t0, 1)
            with open(os.path.join(OUT, f"smoke_{name}.json"), "w") as f:
                json.dump(out, f, indent=1, default=str)
            if not isinstance(out, dict):
                raise TypeError(f"returned {type(out).__name__}, not a dict")
            if "ok" not in out or "feature" not in out:
                raise TypeError("response is not an envelope — every feature must "
                                "return {ok, feature, subject, data, window, meta}")
            ok = bool(out.get("ok"))
            body = out.get("data") if ok else out
            try:
                summary = (summarise(body) if ok
                           else (out.get("error") or {}).get("reason", ""))
            except Exception as e:
                summary = f"[summary failed: {type(e).__name__}: {e}]"
                ok = False
            rows.append((name, "ok" if ok else "EMPTY", secs, summary))
            failed += 0 if ok else 1
        except Exception as e:
            secs = round(time.time() - t0, 1)
            rows.append((name, "FAIL", secs, f"{type(e).__name__}: {e}"))
            traceback.print_exc()
            failed += 1
    w = max(len(r[0]) for r in rows) if rows else 10
    print("\n" + "=" * 100)
    for name, status, secs, summary in rows:
        print(f"{name:<{w}}  {status:<5} {secs:>6}s  {str(summary)[:70]}")
    print("=" * 100)
    print(f"{len(rows) - failed}/{len(rows)} tools returned content   "
          f"(payloads in {OUT}/)")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
