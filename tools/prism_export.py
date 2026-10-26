#!/usr/bin/env python3
"""Turn any Prism response into analysis-ready files: CSV, JSONL, Excel or BibTeX.

Every Prism feature returns the same envelope ({ok, feature, subject, data, window,
meta}); the tables inside `data` differ by feature. This tool knows where the
rows are in each one, flattens them, and writes them next to a small provenance
sidecar (feature, arguments, window, coverage, capture time), so an exported
spreadsheet still says what it is and when it was counted.

    # call the live server and export
    python3 tools/prism_export.py news.compare --arg terms='["tesla","byd"]' -o out/tesla_byd.csv
    python3 tools/prism_export.py research.evidence --arg claim="Metformin reduces cancer risk" -o out/metformin.xlsx

    # export a response you already saved (an envelope, or a showcase capture)
    python3 tools/prism_export.py --from docs/examples/ozempic-news-pulse.json -o out/ozempic/

    # citations as BibTeX
    python3 tools/prism_export.py research.citations --arg claim="Exercise reduces depression" --arg style=bibtex -o refs.bib

Server: $PRISM_URL (default http://127.0.0.1:8790). No third-party packages unless
you ask for .xlsx (openpyxl).
"""
import argparse
import csv
import json
import os
import sys
import time
import urllib.request

URL = os.environ.get("PRISM_URL", "http://127.0.0.1:8790")

# where the rows live, per feature: (table name, path into data, columns to keep or None for all)
TABLES = {
    "news.trends": [("monthly", ["points"], None)],
    "news.sentiment": [("tone", ["points"], None)],
    "news.geography": [("places", ["rows"], None)],
    "news.recent": [("articles", ["articles"], ["published", "title", "publisher", "url", "priority", "tone", "country"])],
    "news.critical": [("articles", ["articles"], ["published", "title", "publisher", "url", "priority", "tone", "country"])],
    "news.sources": [("publishers", ["publishers"], None)],
    "news.trending": [("rising", ["rows"], None), ("rising", ["topics"], None)],
    "news.themes": [("categories", ["categories", "rows"], None), ("subcategories", ["subcategories", "rows"], None),
                    ("tags", ["tags", "rows"], None)],
    "news.entities": [("organizations", ["organizations", "rows"], None), ("people", ["people", "rows"], None),
                      ("places", ["places", "rows"], None)],
    "news.compare": [("summary", ["rows"], ["term", "articles", "share_pct", "critical", "direction", "growth", "tone_ratio", "vs_baseline"]),
                     ("monthly", ["rows", "*", "points"], None)],
    "news.overview": [("monthly", ["trends", "points"], None), ("tone", ["sentiment", "points"], None),
                      ("places", ["geography", "rows"], None), ("subcategories", ["themes", "subcategories", "rows"], None),
                      ("organizations", ["entities", "organizations", "rows"], None), ("people", ["entities", "people", "rows"], None),
                      ("publishers", ["sources", "publishers"], None),
                      ("critical_articles", ["critical", "articles"], ["published", "title", "publisher", "url", "priority", "tone"])],
    "research.evidence": [("documents", ["documents"], ["year", "title", "venue", "tier", "stance", "quote", "doi", "url", "cited_by", "source"])],
    "research.counter_evidence": [("against", ["contradicting"], ["year", "title", "venue", "tier", "stance", "quote", "url"]),
                                  ("for", ["supporting"], ["year", "title", "venue", "tier", "stance", "quote", "url"])],
    "research.statistics": [("figures", ["stats"], None), ("research_per_year", ["research_series", "points"], None),
                            ("news_per_month", ["news_series", "points"], None)],
    "research.browse": [("papers", ["papers"], ["year", "title", "venue", "orientation", "contribution", "cited_by", "doi", "url"])],
    "research.stance_trends": [("by_year", ["points"], ["year", "total", "positive", "contested", "positive_pct", "contested_pct"])],
    "research.table": [("rows", ["rows"], None)],
    "research.citations": [("citations", ["citations"], None)],
    "research.source_ranking": [("ladder", ["ranked"], None), ("ladder", ["sources"], None)],
    "research.brief": [("established", ["what_is_established"], None), ("key_numbers", ["key_numbers"], None)],
    "research.audit": [("claims", ["claims"], None)],
    "historical_analysis": [("series", ["series"], None)],
    "trend_scenarios": [("scenarios", ["scenarios"], None)],
}
TOOL_TO_FEATURE = {"news_trends": "news.trends", "compare_terms": "news.compare", "prism_overview": "news.overview",
                   "find_evidence": "research.evidence", "find_counter_evidence": "research.counter_evidence",
                   "find_statistics": "research.statistics", "browse_research": "research.browse",
                   "stance_trends": "research.stance_trends", "research_table": "research.table",
                   "get_citations": "research.citations", "rank_sources": "research.source_ranking",
                   "research_brief": "research.brief", "research_audit": "research.audit",
                   "news_geography": "news.geography", "trending_topics": "news.trending",
                   "critical_news": "news.critical", "recent_news": "news.recent"}


def call(feature, args):
    req = urllib.request.Request(f"{URL}/v1/{feature}", data=json.dumps(args).encode(),
                                 headers={"content-type": "application/json"})
    with urllib.request.urlopen(req, timeout=900) as r:
        return json.loads(r.read())


def dig(obj, path):
    """Follow a path; '*' fans out over a list and tags each row with its parent's term."""
    if not path:
        return obj if isinstance(obj, list) else []
    k, rest = path[0], path[1:]
    if k == "*":
        out = []
        for parent in obj or []:
            for row in dig(parent, rest) or []:
                out.append({"term": parent.get("term"), **row} if isinstance(row, dict) else row)
        return out
    return dig((obj or {}).get(k), rest) if isinstance(obj, dict) else []


def flat(row):
    out = {}
    for k, v in (row or {}).items():
        if isinstance(v, dict):
            for kk, vv in v.items():
                out[f"{k}.{kk}"] = json.dumps(vv, ensure_ascii=False) if isinstance(vv, (dict, list)) else vv
        elif isinstance(v, list):
            out[k] = "; ".join(str(x) for x in v)
        else:
            out[k] = v
    return out


def tables(env):
    feature = env.get("feature")
    data = env.get("data") or {}
    got = {}
    for name, path, cols in TABLES.get(feature, []):
        rows = dig(data, path)
        if rows and name not in got:
            rows = [flat(r) if isinstance(r, dict) else {"value": r} for r in rows]
            if cols:
                rows = [{c: r.get(c) for c in cols} for r in rows]
            got[name] = rows
    if not got:   # unknown feature: export the first list of objects we find
        for k, v in data.items():
            if isinstance(v, list) and v and isinstance(v[0], dict):
                got[k] = [flat(r) for r in v]
                break
    return got


def provenance(env, args):
    return {"feature": env.get("feature"), "subject": env.get("subject"), "arguments": args,
            "window": env.get("window"), "coverage": ((env.get("meta") or {}).get("coverage") or {}).get("note"),
            "exported_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "server": URL}


def write(out, env, args):
    tabs = tables(env)
    if not tabs:
        sys.exit(f"nothing tabular in {env.get('feature')}: ok={env.get('ok')} error={env.get('error')}")
    if out.endswith(".bib"):
        cites = (env.get("data") or {}).get("citations") or []
        open(out, "w").write("\n\n".join((c.get("citation") or c.get("text") or "") if isinstance(c, dict) else str(c)
                                         for c in cites) + "\n")
        return [out]
    if out.endswith(".xlsx"):
        from openpyxl import Workbook
        wb = Workbook()
        wb.remove(wb.active)
        for name, rows in tabs.items():
            ws = wb.create_sheet(name[:31])
            cols = list(dict.fromkeys(k for r in rows for k in r))
            ws.append(cols)
            for r in rows:
                ws.append([r.get(c) for c in cols])
        ws = wb.create_sheet("provenance")
        for k, v in provenance(env, args).items():
            ws.append([k, json.dumps(v, ensure_ascii=False) if isinstance(v, (dict, list)) else v])
        wb.save(out)
        return [out]
    written = []
    as_dir = out.endswith("/") or len(tabs) > 1 and not out.endswith((".csv", ".jsonl"))
    base = out if as_dir else os.path.dirname(out) or "."
    os.makedirs(base, exist_ok=True)
    for name, rows in tabs.items():
        if as_dir:
            path = os.path.join(base, f"{name}.csv")
        else:
            stem, ext = os.path.splitext(out)
            path = out if len(tabs) == 1 or name == next(iter(tabs)) else f"{stem}.{name}{ext}"
        cols = list(dict.fromkeys(k for r in rows for k in r))
        if path.endswith(".jsonl"):
            with open(path, "w") as f:
                for r in rows:
                    f.write(json.dumps(r, ensure_ascii=False) + "\n")
        else:
            with open(path, "w", newline="") as f:
                w = csv.DictWriter(f, fieldnames=cols)
                w.writeheader()
                w.writerows(rows)
        written.append(path)
    side = os.path.join(base, "provenance.json") if as_dir else os.path.splitext(out)[0] + ".provenance.json"
    json.dump(provenance(env, args), open(side, "w"), indent=1, ensure_ascii=False)
    return written + [side]


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("feature", nargs="?")
    ap.add_argument("--arg", action="append", default=[], help="key=value (JSON values allowed)")
    ap.add_argument("--from", dest="src", help="export a saved envelope or showcase capture instead of calling")
    ap.add_argument("-o", "--out", required=True)
    a = ap.parse_args()
    if a.src:
        saved = json.load(open(a.src))
        if "calls" in saved:   # a showcase capture: export every call into one directory
            outs = []
            for c in saved["calls"]:
                env = c["response"]
                env.setdefault("feature", TOOL_TO_FEATURE.get(c["tool"], c.get("feature")))
                if env.get("feature") not in TABLES:
                    env["feature"] = TOOL_TO_FEATURE.get(c["tool"], env["feature"])
                sub = os.path.join(a.out, c["tool"]) + "/"
                try:
                    outs += write(sub, env, c["args"])
                except SystemExit as e:
                    print(e)
            print("\n".join(outs))
            return
        env, args = saved, {}
    else:
        args = {}
        for kv in a.arg:
            k, v = kv.split("=", 1)
            try:
                args[k] = json.loads(v)
            except json.JSONDecodeError:
                args[k] = v
        env = call(a.feature, args)
    print("\n".join(write(a.out, env, args)))


if __name__ == "__main__":
    main()
