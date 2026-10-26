"""Benchmark pilot: plain models vs the same models with Prism, scored on the deliverable.

The rubric (benchmarks/rubric/benchmark_rubric.json, designed by Fable 5.1) scores a full report:
measured trend and comparison, charts traced to counted data, drill-down, exports, reproducibility,
references, accuracy, limits, the verdict and facet coverage. Script first: the ground pass computes
a ceiling for every script-checkable parameter; two blind judges (Claude Opus, GPT via codex) score
under those ceilings and may only lower them.

    python3 benchmarks/bench.py --pick 2                  # random scenarios (seed recorded)
    python3 benchmarks/bench.py --slugs a,b --stage all   # answers -> ground -> judge -> render -> pdf
"""
import argparse
import csv
import io
import json
import os
import random
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "showcase"))
sys.path.insert(0, ROOT)
from scenarios import BY_SLUG, SCENARIOS  # noqa: E402
import compare  # noqa: E402
import svgchart  # noqa: E402

RUBRIC = json.load(open(os.path.join(HERE, "rubric", "benchmark_rubric.json")))
SPEC = RUBRIC["deliverable_spec"]
PARAMS = {p["key"]: p for p in RUBRIC["parameters"]}
OUT = os.environ.get("BENCH_OUT") or os.path.join(ROOT, "benchmarks", "results")
RESP_MODEL = os.environ.get("BENCH_CLAUDE_MODEL") or compare.CLAUDE_MODEL
RESP_LABEL = os.environ.get("BENCH_CLAUDE_LABEL") or "Claude"
EX = os.path.join(ROOT, "docs", "examples")
TODAY = "2026-10-23"
SEED = 20261023
import prism  # noqa: F401,E402  (loads the untracked .env)
from urllib.parse import urlparse  # noqa: E402
_u = urlparse(os.environ.get("PRISM_CH_HOST", "http://localhost:8123"))
CH = f"{_u.scheme}://{os.environ.get('PRISM_CH_USER', 'default')}:{os.environ.get('PRISM_CH_PASSWORD', '')}@{_u.netloc}/"
CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome")
SETUPS = {"claude_bare": "Claude alone", "claude_prism": "Claude + Prism",
          "chatgpt_bare": "ChatGPT alone", "chatgpt_prism": "ChatGPT + Prism"}
SETUPS = {k: v.replace("Claude", RESP_LABEL) for k, v in SETUPS.items()
          if k in (os.environ.get("BENCH_SETUPS") or ",".join(SETUPS)).split(",")}
TREND_PATTERNS = ("pulse", "compare", "stance", "brief", "evidence", "radar", "history", "trending")


# ---------------------------------------------------------------- prompts

def calls_of(slug):
    d = json.load(open(os.path.join(EX, f"{slug}.json")))
    out, seen = [], {}
    for i, c in enumerate(d["calls"], 1):
        from prism import envelope
        r = envelope.public(c["response"] or {})
        feat = r.get("feature") or c["feature"]
        seen[feat] = seen.get(feat, 0) + 1
        out.append({"id": f"c{i}", "tool": c["tool"], "feature": feat, "n": seen[feat],
                    "args": c["args"], "response": r})
    return out


def applicable(pattern):
    return [k for k, p in PARAMS.items() if pattern in p["applies_to_patterns"]]


def spec_text(pattern):
    secs = []
    for s in SPEC["sections_in_order"]:
        need = s.get("required") or pattern in s.get("required_for_patterns", [])
        opt = pattern in s.get("optional_for", [])
        if not (need or opt):
            continue
        line = f"{s['heading']}{'' if need else ' (optional)'}"
        if s.get("lines"):
            line += "\n" + "\n".join(s["lines"]) + f"\n(at most {s['max_words']} words)"
        if s.get("rule"):
            line += f"\nRule: {s['rule']}"
        secs.append(line)
    facets = [re.sub(r"\s*\([^)]*\)", "", f) for f in RUBRIC["facet_checklists"].get(pattern, [])]
    g = SPEC["source_reference_grammar"]
    return f"""=== DELIVERABLE SPECIFICATION (identical for every respondent) ===
Write ONE markdown document, at most {SPEC['prose_cap_words']} words of prose (fenced blocks do not count).
Use these sections, in this order:

{chr(10).join(secs)}

The question's facets a complete answer covers (answer each with a sourced value, or say plainly that you
cannot measure it): {'; '.join(facets)}.

SOURCES. Every number carries an inline tag: [c1], [c2] ... for a Prism call (declared in the prism-calls
block), [r1], [r2] ... for an entry in ## References, or (est.) for an estimate from memory. An untagged
number is treated as unsourced. A chart or table whose values have no source and are not labelled
estimate is scored as invented. Source grammar: {g['call']}; {g['ref']}; {g['estimate']}.

CHARTS (at most {SPEC['counted_limits']['charts']}). A fenced block with the info word prism-chart holding JSON:
{{"id": "...", "kind": "line|bars|hbar|share", "title": "quantity and subject", "unit": "...",
  "window": {{"from": "YYYY-MM-DD", "to": "YYYY-MM-DD"}}, "x": {{"field": "period|year|label", "type": "temporal|ordinal"}},
  "series": [{{"name": "...", "source": "call:<feature>#<n> | ref:rN | estimate", "points": [["2019", 123], ["2020", 140]]}}],
  "caption": "one sentence stating the reading", "supports": "the sentence in your prose this chart backs, copied verbatim"}}

EXPORTS. One or more fenced CSV blocks whose info string is
  csv name=<file.csv> source=<call:feature#n | ref:rN | estimate> window=<from>..<to> unit=<unit> coverage=full|partial|unknown
followed by RFC 4180 CSV with a header row (empty cell for null, never 0). Mention each file name in the prose.
Then one fenced provenance block (JSON: {{"exported_at": "...", "calls": [{{"feature": "...", "args": {{}}, "window": {{}}}}]}}).

DRILL-DOWN. A fenced prism-calls block holding a JSON list. Entries with "used_for" declare the calls the
deliverable rests on (ids c1..); entries with "question" are 3-8 specific follow-up questions (ids f1..), each
with the Prism "feature" and "args" that would answer it, e.g.
{{"id": "f1", "question": "which papers drove the 2023 rise?", "feature": "research.browse", "args": {{"term": "...", "orientation": "critical", "limit": 8}}}}
Prism features include: research.evidence, research.counter_evidence, research.statistics, research.stance_trends,
research.browse, research.brief, research.radar, research.table, research.citations, news.trends, news.compare,
news.overview, news.geography, news.critical, news.sentiment, analysis.history, analysis.scenarios, research.geography.
"""


def prompt(slug, setup):
    s = BY_SLUG[slug]
    common = SPEC["prompts"]["common"].format(today=TODAY)
    head = f"{common}\n\nQUESTION: {s['question']}\n\n{spec_text(s['pattern'])}\n"
    if setup.endswith("_bare"):
        return head + "\n" + SPEC["prompts"]["bare"] + " Do not run any commands or tools."
    blocks = []
    for c in calls_of(slug):
        r = c["response"]
        from prism import envelope
        body = envelope.public({"ok": r.get("ok"), "data": r.get("data"), "error": r.get("error"),
                                "window": r.get("window"), "meta": r.get("meta")})
        blocks.append(f"--- {c['id']}  feature={c['feature']}  (cite as call:{c['feature']}#{c['n']})  "
                      f"args={json.dumps(c['args'], ensure_ascii=False)}\n"
                      + json.dumps(body, ensure_ascii=False, separators=(",", ":"), default=str))
    return (head + "\n" + SPEC["prompts"]["prism_captured"] + " Do not run any commands.\n\n"
            "=== PRISM TOOL RESULTS (full responses) ===\n" + "\n\n".join(blocks))


# ---------------------------------------------------------------- answers

def answers(slug, force=False):
    path = os.path.join(OUT, slug, "answers.json")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    rec = json.load(open(path)) if os.path.exists(path) else {}
    lock = threading.Lock()

    def go(k):
        p = prompt(slug, k)
        for attempt in range(2):
            try:
                r = (compare.run_claude(p, model=RESP_MODEL, timeout=1800) if k.startswith("claude")
                     else compare.run_chatgpt(p, timeout=1800))
                r["prompt_chars"] = len(p)
                with lock:
                    rec[k] = r
                    json.dump(rec, open(path, "w"), ensure_ascii=False, indent=1)
                print(f"  {slug} {k} {r['seconds']}s {len(r['text'])} chars", flush=True)
                return
            except Exception as e:
                print(f"  {slug} {k} retry: {e}", flush=True)

    todo = [k for k in SETUPS if force or k not in rec]
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(go, todo))
    json.dump({k: prompt(slug, k) for k in SETUPS}, open(os.path.join(OUT, slug, "prompts.json"), "w"),
              ensure_ascii=False, indent=1)
    return rec


# ---------------------------------------------------------------- ground (script pass)

FENCE = re.compile(r"```([\w-]+)([^\n]*)\n(.*?)```", re.S)
NUM = re.compile(r"(?<![\w.#/])[-+]?\d[\d,]*(?:\.\d+)?%?")


def fences(text):
    return [(m.group(1).lower(), m.group(2).strip(), m.group(3)) for m in FENCE.finditer(text)]


def prose(text):
    return FENCE.sub("", text)


def sections(text):
    out, cur = {}, None
    for line in prose(text).splitlines():
        m = re.match(r"^##\s+(.*)", line)
        if m:
            cur = m.group(1).strip().lower()
            out.setdefault(cur, [])
        elif cur:
            out[cur].append(line)
    return {k: "\n".join(v) for k, v in out.items()}


def leaves(obj, acc):
    if isinstance(obj, dict):
        for v in obj.values():
            leaves(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            leaves(v, acc)
    elif isinstance(obj, bool):
        pass
    elif isinstance(obj, (int, float)):
        acc.add(float(obj))
    elif isinstance(obj, str):
        for m in re.finditer(r"\d[\d,]*(?:\.\d+)?", obj):
            try:
                acc.add(float(m.group(0).replace(",", "")))
            except ValueError:
                pass
    return acc


def num_val(tok):
    t = tok.replace(",", "").rstrip("%")
    try:
        return float(t)
    except ValueError:
        return None


def traces(v, index):
    """exact after rounding to the precision shown, or a share/percent of a leaf"""
    if v is None:
        return False
    dec = 0
    for x in index:
        if abs(x - v) < 1e-9 or abs(round(x, 1) - v) < 1e-9 or abs(round(x) - v) < 1e-9 and v >= 10:
            return True
        if abs(x * 100 - v) < 0.051 or abs(round(x * 100, 1) - v) < 1e-9:
            return dec == 0
    return False


def is_year(tok):
    return re.fullmatch(r"(19|20)\d\d", tok.rstrip(",")) is not None


def parse_info(info):
    return dict(re.findall(r"(\w+)=(\S+)", info))


_TOOL2FEAT = None


def feature_name(x):
    """a Prism feature id, also accepting the MCP tool name (historical_analysis -> analysis.history)"""
    global _TOOL2FEAT
    if _TOOL2FEAT is None:
        import prism_mcp as m
        _TOOL2FEAT = {k: v["feature"] for k, v in m.REGISTRY.items()}
    x = (x or "").strip().replace("prism.", "").replace("mcp__prism__", "")
    return _TOOL2FEAT.get(x, x)


def resolve(src, calls):
    """call:<feature>#<n> -> the recorded calls of that feature (the cited nth first), ref/estimate -> kind"""
    src = (src or "").strip()
    if src.startswith("call:"):
        m = re.match(r"call:([\w.]+)(?:#(\d+))?", src)
        if m:
            feat, n = feature_name(m.group(1)), int(m.group(2) or 1)
            cands = [c for c in calls if c["feature"] == feat]
            if cands:
                cands.sort(key=lambda c: c["n"] != n)
                return "call", cands
        return "badcall", None
    if src.startswith("ref:"):
        return "ref", None
    if src.lower().startswith("estimate"):
        return "estimate", None
    return "none", None


def _list_sums(o, acc):
    """totals of sibling numeric fields (rows[].papers summed): the denominators of shares a chart may plot"""
    if isinstance(o, dict):
        for v in o.values():
            _list_sums(v, acc)
    elif isinstance(o, list):
        rows = [x for x in o if isinstance(x, dict)]
        keys = {k for x in rows for k, v in x.items() if isinstance(v, (int, float)) and not isinstance(v, bool)}
        for k in keys:
            acc.add(float(sum(x.get(k) or 0 for x in rows if isinstance(x.get(k), (int, float)))))
        for x in o:
            _list_sums(x, acc)
    return acc


def derived_share(vals, idx, extra_den):
    """share of values that are 100*x/D for a leaf x and one denominator D (an index to a base year, a share of
    a total): the recomputable derivations the rubric accepts as grounded"""
    ints = {round(x) for x in idx if abs(x - round(x)) < 1e-9}
    best = 0
    for D in [d for d in (idx | extra_den) if d and d > 0][:6000]:
        ok = 0
        for v in vals:
            x = v * D / 100
            tol = D * 0.051 / 100 + 1e-9
            if tol > 2:  # too coarse to tell a real derivation from a coincidence
                break
            if any(abs(x - k) <= tol for k in range(int(x - tol), int(x + tol) + 2) if k in ints) or any(abs(x - y) <= tol for y in (idx if len(idx) < 400 else ())):
                ok += 1
        best = max(best, ok / len(vals) if vals else 0)
        if best >= 0.999:
            break
    return best


def best_share(cands, vals):
    """grounded share against the best-matching call of the cited feature, and whether it was the cited one"""
    best, which = -1, 0
    vals = [float(v) for v in vals if v is not None]
    for i, c in enumerate(cands):
        idx = leaves(c["response"].get("data"), set())
        leaves({k: v for k, v in (c["response"].get("meta") or {}).items() if k not in ("seconds", "queue_seconds", "execution_seconds", "trace")}, idx)
        sh = sum(1 for v in vals if traces(v, idx)) / len(vals) if vals else 0
        if sh < 0.9 and vals:
            sh = max(sh, derived_share(vals, idx, _list_sums(c["response"].get("data"), set())))
        if sh > best:
            best, which = sh, i
    return max(best, 0), which == 0


def doi_lookup(dois):
    if not dois:
        return {}
    q = ",".join("'" + d.replace("'", "") + "'" for d in dois)
    sql = (f"SELECT lower(doi), publication_year, title FROM openalex.works_distributed "
           f"WHERE lower(doi) IN ({q}) FORMAT JSONEachRow")
    try:
        r = subprocess.run(["curl", "-s", "-m", "300", CH, "--data-binary", sql], capture_output=True, text=True,
                           timeout=320)
        rows = [json.loads(x) for x in r.stdout.splitlines() if x.startswith("{")]
        return {x["lower(doi)"]: x for x in rows}
    except Exception:
        return {}


_DOI_CACHE = {}


def doi_resolves(d):
    if d not in _DOI_CACHE:
        try:
            r = subprocess.run(["curl", "-s", "-o", "/dev/null", "-w", "%{http_code}", "-m", "20",
                                "https://doi.org/api/handles/" + d], capture_output=True, text=True, timeout=30)
            _DOI_CACHE[d] = r.stdout.strip() == "200"
        except Exception:
            _DOI_CACHE[d] = False
    return _DOI_CACHE[d]


def run_followups(entries, budget=150):
    import prism_mcp as m
    feat2tool = {v["feature"]: k for k, v in m.REGISTRY.items()}
    res = []
    for e in entries[:8]:
        tool = feat2tool.get(feature_name(e.get("feature")))
        row = {"id": e.get("id"), "feature": e.get("feature"), "question": e.get("question"), "args": e.get("args")}
        if not tool:
            row.update(ok=False, why="unknown feature")
            res.append(row)
            continue
        box = {}

        args = e.get("args") or {}
        if isinstance(args, str):
            try:
                args = json.loads(args)
            except Exception:
                args = {}
        if not isinstance(args, dict):
            args = {}

        def call():
            try:
                box["r"] = m.REGISTRY[tool]["fn"](**args)
            except Exception as ex:
                box["r"] = {"ok": False, "error": {"message": f"{type(ex).__name__}: {ex}"}}
        th = threading.Thread(target=call, daemon=True)
        t0 = time.time()
        th.start()
        th.join(budget)
        r = box.get("r")
        if r is None:
            row.update(ok=False, why=f"no answer in {budget}s")
        else:
            data = r.get("data")
            row.update(ok=bool(r.get("ok")), nonempty=bool(data),
                       why=(r.get("error") or {}).get("message") or (r.get("error") or {}).get("reason") or "",
                       seconds=round(time.time() - t0, 1),
                       sample=json.dumps(data, ensure_ascii=False, default=str)[:700] if data else "")
        res.append(row)
    return res


def ground(slug, setup, text, calls, pattern=None, applies=None):
    pattern = pattern or BY_SLUG[slug]["pattern"]
    prism = setup.endswith("_prism")
    index = set()
    for c in calls if prism else []:
        leaves(c["response"].get("data"), index)
        leaves(c["response"].get("window"), index)
        meta = dict(c["response"].get("meta") or {})
        for k in ("seconds", "queue_seconds", "execution_seconds", "trace"):
            meta.pop(k, None)
        leaves(meta, index)  # lane notes and lane counts carry the subject/outcome volumes
    secs = sections(text)
    fs = fences(text)
    f = {"invented": [], "notes": []}

    # charts
    charts = []
    for kind, info, body in fs:
        if kind != "prism-chart":
            continue
        try:
            ch = json.loads(body)
        except Exception:
            charts.append({"malformed": True})
            continue
        sers = []
        for se in ch.get("series") or []:
            how, call = resolve(se.get("source"), calls if prism else [])
            pts = se.get("points") or []
            vals = [p[1] for p in pts if isinstance(p, (list, tuple)) and len(p) > 1 and isinstance(p[1], (int, float))]
            if how == "call":
                share, cited = best_share(call, vals)
                if not cited:
                    f["notes"].append(f"chart '{ch.get('title')}' values match a different call of the cited feature than #n")
            else:
                share = None
            if how in ("none", "badcall"):
                f["invented"].append(f"chart '{ch.get('title')}' series '{se.get('name')}' source={se.get('source')!r}")
            sers.append({"name": se.get("name"), "how": how, "points": len(vals), "traced_share": share})
        sup = (ch.get("supports") or "").lower()
        used = bool(sup) and sup[:60] in prose(text).lower()
        charts.append({"id": ch.get("id"), "title": ch.get("title"), "kind": ch.get("kind"),
                       "temporal": (ch.get("x") or {}).get("type") == "temporal" or (ch.get("x") or {}).get("field") in ("period", "year"),
                       "has_window": bool(ch.get("window")), "has_unit": bool(ch.get("unit")),
                       "supports_found": used, "series": sers})

    def chart_score(c):
        if c.get("malformed"):
            return 0
        hows = [x["how"] for x in c["series"]]
        if not hows or any(h in ("none", "badcall") for h in hows):
            return 0
        if all(h == "call" for h in hows):
            sh = min(x["traced_share"] or 0 for x in c["series"])
            if sh >= 0.999 and c["has_window"] and c["has_unit"] and c["supports_found"]:
                return 5
            if sh >= 0.9:
                return 2 if not (c["has_window"] and c["has_unit"]) else 4
            return 0
        return 1  # estimate or cited-unverifiable
    cs = [chart_score(c) for c in charts if not c.get("malformed")]
    ceil = {"chart": min(cs) if cs else 0}

    tchart = [c for c, sc in zip([c for c in charts if not c.get("malformed")], cs) if c["temporal"]]
    if not tchart:
        ceil["trend"] = 1 if re.search(r"\b(ris|grow|declin|fall|increas|decreas|flat|stable)", secs.get("trend", ""), re.I) else 0
    else:
        best = max(chart_score(c) for c in tchart)
        ceil["trend"] = {0: 0, 1: 1 if all(x["how"] == "estimate" for c in tchart for x in c["series"]) else 2,
                         2: 2, 4: 5, 5: 5}.get(best, best)

    # exports
    tables = []
    for kind, info, body in fs:
        if kind != "csv":
            continue
        a = parse_info(info)
        try:
            rows = list(csv.reader(io.StringIO(body.strip())))
        except Exception:
            rows = []
        how, call = resolve(a.get("source"), calls if prism else [])
        cells = [x for r in rows[1:] for x in r if num_val(x) is not None and not is_year(x)]
        if how == "call":
            share = best_share(call, [num_val(x) for x in cells])[0] if cells else 1.0
        else:
            share = None
        if how in ("none", "badcall") and cells:
            f["invented"].append(f"csv {a.get('name')} source={a.get('source')!r}")
        prov = all(k in a for k in ("name", "source", "window", "unit", "coverage"))
        tables.append({"name": a.get("name"), "how": how, "rows": max(0, len(rows) - 1), "numeric_cells": len(cells),
                       "traced_share": share, "full_provenance": prov,
                       "named_in_prose": bool(a.get("name")) and a.get("name") in prose(text),
                       "zero_for_null": False})
    if not tables:
        ceil["export"] = 0
    else:
        def tsc(t):
            if t["how"] in ("none", "badcall"):
                return 0 if t["numeric_cells"] else 1
            if t["how"] != "call":
                return 1
            if (t["traced_share"] or 0) >= 0.999 and t["full_provenance"]:
                return 5 if t["named_in_prose"] else 3
            return 2 if (t["traced_share"] or 0) >= 0.9 else 0
        ceil["export"] = min(tsc(t) for t in tables)
    has_prov = any(k == "provenance" or (k == "json" and "exported_at" in b) for k, _, b in fs)

    # prism-calls / drill-down
    pc = []
    for kind, info, body in fs:
        if kind == "prism-calls":
            try:
                pc = json.loads(body)
            except Exception:
                f["notes"].append("prism-calls block is not valid JSON")
    fups = [e for e in pc if isinstance(e, dict) and e.get("question")]
    declared = [e for e in pc if isinstance(e, dict) and e.get("used_for")]
    if prism:
        real = {c["feature"] for c in calls}
        ghost = [e.get("feature") for e in declared if feature_name(e.get("feature")) not in real]
        if ghost:
            f["notes"].append(f"declared calls that were never made: {ghost}")
    fu = run_followups(fups) if fups else []
    good = sum(1 for r in fu if r.get("ok") and r.get("nonempty"))
    layer = bool(re.search(r"\|.*\|", secs.get("drill-down", "") + secs.get("evidence", "")))
    if prism:
        ceil["drilldown"] = 5 if good >= 3 else (3 if good >= 1 or layer else 2 if layer else 1)
    else:
        ceil["drilldown"] = 3 if good >= 3 else (2 if layer or good else 1)

    # numbers in prose -> repro
    body = prose(text)
    nums = []
    DATEY = re.compile(r"\b(?:19|20)\d\d-\d\d(?:-\d\d)?\b|\b(?:19|20)\d\d\s*[-–]\s*(?:19|20)?\d\d\b")
    for line in body.splitlines():
        if re.match(r"^\s*-?\s*\[r\d+\]", line):
            continue  # reference entries carry volumes/pages, not claims
        clean = DATEY.sub(lambda m: " " * len(m.group(0)), line)
        for m in NUM.finditer(clean):
            tok = m.group(0).rstrip(",")
            if is_year(tok) or re.fullmatch(r"\d", tok):
                continue
            end = re.search(r"\.(\s|$)", clean[m.end():])
            tail = clean[m.end():m.end() + (end.start() + 25 if end else len(clean))]
            tagged = re.search(r"[\[(](c|r)\d+[\])]|\(est", tail)
            nums.append({"tok": tok, "val": num_val(tok), "traced": prism and traces(num_val(tok), index),
                         "tagged": bool(tagged), "est": "(est" in tail, "ctx": line.strip()[:140]})
    # derived numbers: a difference, ratio or percent change between two values the deliverable already traced
    if prism:
        base = [x["val"] for x in nums if x["traced"] and x["val"] is not None][:200]
        der = set()
        for i, a1 in enumerate(base):
            for b1 in base[i + 1:]:
                for v in (a1 - b1, b1 - a1, a1 + b1):
                    der.add(round(v, 1))
                for x, y in ((a1, b1), (b1, a1)):
                    if y:
                        der.update({round(x / y, 1), round(x / y, 2), round(100 * (x - y) / y), round(100 * (x - y) / y, 1)})
        for x in nums:
            if not x["traced"] and x["val"] is not None and (round(x["val"], 1) in der or round(x["val"], 2) in der or round(x["val"]) in der):
                x["traced"], x["derived"] = True, True
    n = len(nums)
    traced = sum(1 for x in nums if x["traced"])
    untagged = [x for x in nums if not x["tagged"] and not x["traced"]]
    tr = traced / n if n else 0
    if prism:
        args_listed = bool(declared) and all(e.get("args") is not None for e in declared)
        ceil["repro"] = 5 if tr >= 0.9 and args_listed else 4 if tr >= 0.9 else 3 if tr >= 0.6 else 2
    else:
        ceil["repro"] = 1 if n and len(untagged) / n < 0.2 else (1 if not n else 0)
    # comparison: numbers in the Comparison section
    cmp_nums = [x for x in nums if x["ctx"] and x["ctx"] in secs.get("comparison", "")]
    if not secs.get("comparison"):
        ceil["comparison"] = 0
    elif prism:
        ct = sum(1 for x in cmp_nums if x["traced"]) / len(cmp_nums) if cmp_nums else 0
        ceil["comparison"] = 5 if ct >= 0.6 else 3 if cmp_nums else 1
    else:
        ceil["comparison"] = 2 if cmp_nums else 1

    # references -> DOIs checked against the 401M-work corpus
    dois = set()
    for d in re.findall(r"10\.\d{4,9}/[^\s\"'<>\]\[,;]+", text):
        d = d.rstrip(".:")
        while d.endswith(")") and d.count("(") < d.count(")"):
            d = d[:-1]
        dois.add(d.rstrip(".").lower())
    dois = sorted(dois)
    found = doi_lookup(dois)
    # not in the 401M-work corpus: ask doi.org whether the identifier exists at all
    for d in [x for x in dois if x not in found]:
        if doi_resolves(d):
            found[d] = {"publication_year": None, "title": "", "via": "doi.org"}
    refsec = secs.get("references", "")
    missing = [d for d in dois if d not in found]
    yr_bad = []
    for d, row in found.items():
        for line in text.splitlines():
            if d in line.lower():
                ys = [int(y) for y in re.findall(r"\b(19\d\d|20\d\d)\b", line)]
                if row.get("publication_year") and ys and all(abs(y - int(row["publication_year"])) > 1 for y in ys):
                    yr_bad.append(d)
                break
    if not refsec.strip():
        ceil["refs"] = 0
    elif not dois:
        ceil["refs"] = 2 if re.search(r"https?://", refsec) else 1
    elif missing or yr_bad:
        ceil["refs"] = 1 if (len(missing) + len(yr_bad)) else 3
        if (len(missing) + len(yr_bad)) / len(dois) > 0.5:
            ceil["refs"] = 0
    else:
        ceil["refs"] = 5

    # limits and verdict structure
    meth = secs.get("method and limits", "")
    end_dated = bool(re.search(r"20\d\d-\d\d", meth))
    gap = bool(re.search(r"(month|day|year)s? (to|before|until|since|between)|gap|to today|as of", meth, re.I))
    ceil["limits"] = 5 if meth and end_dated and gap else 3 if meth else 1
    v = secs.get("verdict", "")
    lines_ok = all(re.search(rf"^\s*-\s*\**{k}", v, re.I | re.M) for k in
                   ("Answer", "Decision", "Confidence", "What would change"))
    vwords = len(v.split())
    first = list(secs)[:1] == ["verdict"]
    ceil["verdict"] = 5 if lines_ok and vwords <= 150 and first else 3 if v else 0
    vnums = [x for x in nums if x["ctx"] and x["ctx"] in v]
    if any(not x["tagged"] and not x["traced"] for x in vnums):
        f["invented"].append("an untagged number in the Verdict: " + ", ".join(x["tok"] for x in vnums if not x["tagged"] and not x["traced"]))
        ceil["verdict"] = 0
    ceil["accuracy"] = 5
    ceil["facets"] = 5 if prism else 3

    ap = applies or applicable(pattern)
    ceil = {k: v for k, v in ceil.items() if k in ap}
    return {"setup": setup, "words_prose": len(body.split()), "charts": charts, "tables": tables,
            "provenance_block": has_prov, "followups": fu, "followups_ok": good,
            "numbers": {"total": n, "traced": traced, "derived": sum(1 for x in nums if x.get("derived")), "untagged_untraced": len(untagged),
                        "untagged_examples": [x["tok"] + " — " + x["ctx"][:90] for x in untagged[:8]]},
            "dois": {"cited": len(dois), "found_in_corpus": len(found), "not_found": missing[:12], "year_mismatch": yr_bad},
            "verdict_structure": {"four_lines": lines_ok, "words": vwords, "first": first},
            "limits": {"method_section": bool(meth), "end_date": end_dated, "gap_to_today": gap},
            "invented": f["invented"], "notes": f["notes"], "ceiling": ceil}


# ---------------------------------------------------------------- judges

JUDGE = """You are one of two blind judges in a public benchmark of decision-grade research deliverables.
Today is {today}. {n} respondents answered the same question with the same deliverable specification. Some had a
research database, some answered from memory; do not guess which. Labels {labels} are in random order.

QUESTION: {question}
WHAT MAKES IT HARD: {special}

THE RUBRIC (score each applicable parameter 0-5 using these anchors exactly):
{rubric}

SCRIPT PASS. Before you, a script parsed each deliverable, traced its numbers, charts and CSV cells against the
recorded database responses, executed its proposed follow-up calls, and looked up every DOI in a 401M-work
research corpus. It gives each script-checkable parameter a CEILING. You may score BELOW a ceiling, with a
reason, never above it. accuracy, verdict support and facet reading are yours to judge (still at or below
their ceiling).
{ground}

REFERENCE RECORD (the database responses the database-backed respondents were given; use it to check facts.
A memory-only respondent is not penalised for lacking it, only for contradicting it or inventing specifics):
{reference}

{answers}

Return ONLY JSON:
{{"scores": {{"A": {{"<param>": n, ...}}, ... one entry per label ...}},
 "reasons": {{"A": {{"<param>": "short reason"}}, ...}},
 "errors": {{"A": ["contradictions or fabricated specifics"], ...}},
 "best": "<label>",
 "verdict": "two or three sentences: what separated the deliverables for a decision-maker"}}"""


def rubric_text(pattern):
    out = []
    for k in applicable(pattern):
        p = PARAMS[k]
        anc = "; ".join(f"{s}={p['scale_anchors'][s]}" for s in sorted(p["scale_anchors"]))
        out.append(f"- {k} (weight {p['weight']}): {p['definition']}\n  anchors: {anc}\n  anti-gaming: {p['anti_gaming']}")
    return "\n".join(out)


def reference(slug):
    parts = []
    for c in calls_of(slug):
        r = c["response"]
        body = {"ok": r.get("ok"), "data": compare.compact(r.get("data"), list_cap=12) if r.get("data") else None,
                "window": r.get("window"), "meta_note": (r.get("meta") or {}).get("caveat")}
        parts.append(f"--- {c['id']} {c['feature']} args={json.dumps(c['args'], ensure_ascii=False)}\n"
                     + json.dumps(body, ensure_ascii=False, separators=(",", ":"), default=str)[:22000])
    return "\n".join(parts)


def judge(slug, which):
    d = os.path.join(OUT, slug)
    ans = json.load(open(os.path.join(d, "answers.json")))
    gr = json.load(open(os.path.join(d, "ground.json")))
    s = BY_SLUG[slug]
    order = list(SETUPS)
    random.Random(f"{slug}-{which}").shuffle(order)
    labels = dict(zip("ABCD", order))
    gtxt = "\n".join(f"{l}: ceilings={json.dumps(gr[k]['ceiling'])}; numbers {gr[k]['numbers']['traced']}/"
                     f"{gr[k]['numbers']['total']} traced, {gr[k]['numbers']['untagged_untraced']} untagged; "
                     f"DOIs {gr[k]['dois']['found_in_corpus']}/{gr[k]['dois']['cited']} found in corpus "
                     f"(not found: {gr[k]['dois']['not_found'][:5]}); follow-ups ok {gr[k]['followups_ok']}/"
                     f"{len(gr[k]['followups'])}; invented: {gr[k]['invented'][:4]}; notes: {gr[k]['notes']}"
                     for l, k in labels.items())
    atxt = "\n\n".join(f"=== DELIVERABLE {l} ===\n{ans[k]['text']}" for l, k in labels.items())
    p = JUDGE.format(today=TODAY, n=len(labels), labels=", ".join(labels), question=s["question"], special=s["special"], rubric=rubric_text(s["pattern"]),
                     ground=gtxt, reference=reference(slug), answers=atxt)
    for attempt in range(3):
        try:
            out = (compare.run_claude(p, model="opus", timeout=1800)["text"] if which == "opus"
                   else compare.run_chatgpt(p, timeout=1800)["text"])
            j = json.loads(re.search(r"\{.*\}", out, re.S).group(0))
            break
        except Exception as e:
            print(f"  judge {which} retry {slug}: {e}", flush=True)
            j = None
    if not j:
        raise RuntimeError(f"judge {which} failed for {slug}")
    res = {"labels": labels, "raw": j, "scores": {}, "lowered": {}, "clamped": {}}
    for l, k in labels.items():
        sc = {}
        for prm in applicable(s["pattern"]):
            v = j["scores"].get(l, {}).get(prm)
            cap = gr[k]["ceiling"].get(prm, 5)
            v = cap if v is None else int(v)
            if v > cap:
                res["clamped"].setdefault(k, []).append(f"{prm} {v}->{cap}")
                v = cap
            sc[prm] = v
        res["scores"][k] = sc
    json.dump(res, open(os.path.join(d, f"judge_{which}.json"), "w"), ensure_ascii=False, indent=1)
    return res


def weighted(sc, invented):
    w = sum(PARAMS[k]["weight"] for k in sc)
    v = 100 * sum(PARAMS[k]["weight"] * s for k, s in sc.items()) / (5 * w)
    return round(min(v, 40) if invented else v, 1), round(v, 1)


def results(slug):
    d = os.path.join(OUT, slug)
    gr = json.load(open(os.path.join(d, "ground.json")))
    js = {w: json.load(open(os.path.join(d, f"judge_{w}.json"))) for w in ("opus", "gpt") if
          os.path.exists(os.path.join(d, f"judge_{w}.json"))}
    out = {}
    for k in SETUPS:
        per = {}
        for prm in applicable(BY_SLUG[slug]["pattern"]):
            vals = [j["scores"][k][prm] for j in js.values()]
            per[prm] = round(sum(vals) / len(vals), 1)
        strict, plain = weighted(per, bool(gr[k]["invented"]))
        out[k] = {"params": per, "strict": strict, "plain": plain, "invented": bool(gr[k]["invented"]),
                  "by_judge": {w: weighted(j["scores"][k], bool(gr[k]["invented"]))[0] for w, j in js.items()}}
    diffs = [abs(js["opus"]["scores"][k][p] - js["gpt"]["scores"][k][p]) for k in SETUPS
             for p in applicable(BY_SLUG[slug]["pattern"])] if len(js) == 2 else []
    res = {"slug": slug, "setups": out, "judge_mad": round(sum(diffs) / len(diffs), 2) if diffs else None,
           "verdicts": {w: j["raw"].get("verdict") for w, j in js.items()},
           "errors": {w: {j["labels"][l]: v for l, v in (j["raw"].get("errors") or {}).items() if l in j["labels"]}
                      for w, j in js.items()},
           "reasons": {w: {j["labels"][l]: v for l, v in (j["raw"].get("reasons") or {}).items() if l in j["labels"]}
                       for w, j in js.items()},
           "clamped": {w: j["clamped"] for w, j in js.items()}}
    json.dump(res, open(os.path.join(d, "results.json"), "w"), ensure_ascii=False, indent=1)
    return res


# ---------------------------------------------------------------- render

PAGE_CSS = """
:root{--bg:#ffffff;--ink:#14161a;--ink2:#4b5160;--ink3:#8a8f9c;--line:#e3e5ea;--card:#f6f7f9;--accent:#2a78d6;--bad:#c4321d;--good:#1a8f62}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif}
.wrap{max-width:900px;margin:0 auto;padding:28px 32px 40px}
.bar{display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid var(--ink);padding-bottom:10px;margin-bottom:18px}
.bar .who{font-weight:700;font-size:20px}.bar .q{color:var(--ink2);font-size:13px;max-width:560px;text-align:right}
h2{font-size:18px;margin:26px 0 8px;border-bottom:1px solid var(--line);padding-bottom:4px}
table{border-collapse:collapse;margin:10px 0;font-size:13px;width:100%}th,td{border:1px solid var(--line);padding:5px 8px;text-align:left;vertical-align:top}
th{background:var(--card)}code{background:var(--card);padding:1px 4px;border-radius:3px;font-size:12.5px}
.chart{margin:12px 0}.chart img,.chart svg{max-width:100%}.cap{font-size:12.5px;color:var(--ink2);margin-top:2px}
.tag{font-size:11px;font-weight:600;padding:1px 6px;border-radius:9px;border:1px solid var(--line);color:var(--ink2);margin-left:6px}
.tag.inv{color:var(--bad);border-color:var(--bad)}.tag.ok{color:var(--good);border-color:var(--good)}
.csvh{font-size:12px;color:var(--ink2);margin-top:12px}details{margin:8px 0;font-size:12.5px}pre{white-space:pre-wrap;background:var(--card);padding:8px;border-radius:4px;font-size:11.5px}
"""


def render_chart(ch, tag):
    series = []
    for se in ch.get("series") or []:
        pts = [(str(p[0]), p[1]) for p in se.get("points") or [] if isinstance(p, (list, tuple)) and len(p) > 1
               and isinstance(p[1], (int, float))]
        if pts:
            series.append((f"{se.get('name')} [{se.get('source')}]", pts))
    sub = f"{ch.get('unit', '')} · window {json.dumps(ch.get('window'))}"
    kind = ch.get("kind")
    svg = None
    if series and (kind == "line" or ((ch.get("x") or {}).get("type") == "temporal" and kind not in ("hbar",))):
        xs = [p[0] for p in series[0][1]]
        aligned = [(n, [(x, dict(pts).get(x)) for x in xs]) for n, pts in series]
        svg = svgchart.line_chart(aligned, ch.get("title", ""), sub, "source: " + ", ".join(
            str(se.get("source")) for se in ch.get("series") or []))
    elif series:
        svg = svgchart.hbar_chart(sorted(series[0][1], key=lambda r: -(r[1] or 0)), ch.get("title", ""), sub,
                                  "source: " + str((ch.get("series") or [{}])[0].get("source")))
    if not svg:
        return f"<div class='chart'><b>{escape(str(ch.get('title')))}</b> (no plottable points){tag}</div>"
    svg = re.sub(r"@media \(prefers-color-scheme: dark\)\{.*?\}\}", "", svg, flags=re.S)
    return f"<div class='chart'>{svg}<div class='cap'>{escape(str(ch.get('caption', '')))}{tag}</div></div>"


def render(slug, setup):
    import markdown
    ans = json.load(open(os.path.join(OUT, slug, "answers.json")))[setup]["text"]
    gr = json.load(open(os.path.join(OUT, slug, "ground.json")))[setup]
    charts = iter(gr["charts"])
    tables = iter(gr["tables"])
    stash = []

    def repl(m):
        kind, info, body = m.group(1).lower(), m.group(2).strip(), m.group(3)
        if kind == "prism-chart":
            g = next(charts, {})
            try:
                ch = json.loads(body)
            except Exception:
                html = "<div class='chart'><span class='tag inv'>malformed chart block</span></div>"
            else:
                hows = {x["how"] for x in g.get("series", [])}
                if hows & {"none", "badcall"}:
                    t = "<span class='tag inv'>unsourced: scored as invented</span>"
                elif hows == {"call"}:
                    sh = min((x["traced_share"] or 0) for x in g["series"])
                    t = f"<span class='tag ok'>traced to corpus: {sh:.0%} of points</span>"
                else:
                    t = "<span class='tag'>from memory (estimate / cited, not checkable)</span>"
                html = render_chart(ch, t)
        elif kind == "csv":
            g = next(tables, {})
            a = parse_info(info)
            rows = list(csv.reader(io.StringIO(body.strip())))
            t = ("<span class='tag inv'>unsourced</span>" if g.get("how") in ("none", "badcall") else
                 f"<span class='tag ok'>cells traced: {g['traced_share']:.0%}</span>" if g.get("how") == "call"
                 else "<span class='tag'>from memory</span>")
            head = "".join(f"<th>{escape(x)}</th>" for x in (rows[0] if rows else []))
            trs = "".join("<tr>" + "".join(f"<td>{escape(x)}</td>" for x in r) + "</tr>" for r in rows[1:16])
            more = f"<div class='cap'>… {len(rows) - 16} more rows</div>" if len(rows) > 16 else ""
            html = (f"<div class='csvh'>⬇ <b>{escape(a.get('name', 'table.csv'))}</b> · source {escape(a.get('source', '—'))}"
                    f" · window {escape(a.get('window', '—'))} · unit {escape(a.get('unit', '—'))}{t}</div>"
                    f"<table><tr>{head}</tr>{trs}</table>{more}")
        else:
            label = {"prism-calls": "Calls and follow-up queries (executable)", "provenance": "Provenance"}.get(kind, kind)
            html = f"<details open><summary>{escape(label)}</summary><pre>{escape(body.strip()[:2500])}</pre></details>"
        stash.append(html)
        return f"\n\nSTASH{len(stash) - 1}END\n\n"

    md = FENCE.sub(repl, ans)
    html = markdown.markdown(md, extensions=["tables"])
    html = re.sub(r"(?:<p>)?STASH(\d+)END(?:</p>)?", lambda m: stash[int(m.group(1))], html)
    page = (f"<!doctype html><html><head><meta charset='utf-8'><title>{escape(SETUPS[setup])}</title>"
            f"<style>{PAGE_CSS}</style></head><body><div class='wrap'><div class='bar'><div class='who'>"
            f"{escape(SETUPS[setup])}</div><div class='q'>{escape(BY_SLUG[slug]['question'])}</div></div>"
            f"{html}</div></body></html>")
    path = os.path.join(OUT, slug, f"{setup}.html")
    open(path, "w").write(page)
    return path


def shot(html_path, png, height=None):
    h = height or 20000
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--hide-scrollbars",
                    "--blink-settings=preferredColorScheme=1", f"--screenshot={png}",
                    f"--window-size=964,{h}", "file://" + html_path], capture_output=True, timeout=120)
    if height is None:  # trim the blank tail of a full-page shot
        from PIL import Image, ImageChops
        im = Image.open(png).convert("RGB")
        bg = Image.new("RGB", im.size, (255, 255, 255))
        box = ImageChops.difference(im, bg).getbbox()
        if box:
            im.crop((0, 0, im.width, min(im.height, box[3] + 30))).save(png)
    return png


def screens(slug):
    d = os.path.join(OUT, slug)
    for k in SETUPS:
        p = render(slug, k)
        shot(p, os.path.join(d, f"{k}_first.png"), height=2500)
        shot(p, os.path.join(d, f"{k}_full.png"))


# ---------------------------------------------------------------- pdf

def slices(png, h=1250):
    from PIL import Image
    im = Image.open(png)
    out = []
    for i, y in enumerate(range(0, im.height, h)):
        p = png.replace(".png", f"_s{i}.png")
        im.crop((0, y, im.width, min(im.height, y + h))).save(p)
        out.append(p)
    return out


def pdf(slugs, pick_note, out=None):
    R = {s: json.load(open(os.path.join(OUT, s, "results.json"))) for s in slugs}
    G = {s: json.load(open(os.path.join(OUT, s, "ground.json"))) for s in slugs}
    order = [k for k in ["claude_bare", "claude_prism", "chatgpt_bare", "chatgpt_prism"] if k in SETUPS]
    css = PAGE_CSS + """
@page{size:A4;margin:14mm}.wrap{max-width:none;padding:0}.pb{page-break-before:always}
h1{font-size:30px;margin:0 0 6px}.lead{font-size:15px;color:var(--ink2);max-width:720px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:18px 0}.kpi{background:var(--card);border-radius:8px;padding:12px}
.kpi .n{font-size:30px;font-weight:700}.kpi .l{font-size:12px;color:var(--ink2)}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:10px}.pair img{width:100%;border:1px solid var(--line)}
.pair .h{font-weight:700;font-size:13px;margin-bottom:4px}.full img{width:100%;border:1px solid var(--line);display:block}
.small{font-size:12px;color:var(--ink2)} td.num{text-align:right;font-variant-numeric:tabular-nums} .hi{font-weight:700}
.barw{background:var(--line);height:8px;border-radius:4px;width:120px;display:inline-block;vertical-align:middle}
.barf{background:var(--accent);height:8px;border-radius:4px}
"""
    avg = {k: round(sum(R[s]["setups"][k]["strict"] for s in slugs) / len(slugs), 1) for k in order}
    h = [f"<h1>{os.environ.get('BENCH_TITLE') or 'Benchmark pilot: plain models vs Prism'}</h1><div class='lead'>{len(slugs)} scenario(s), {len(order)} respondents, "
         f"one deliverable spec: a decision-grade report with a verdict, measured trend, comparison, charts, "
         f"drill-down, exports and references. Scored on 11 parameters designed by Fable 5.1, script first, then two "
         f"blind judges (Claude Opus and GPT) who may only lower the script's ceilings. Run {TODAY}.</div>",
         "<div class='kpis' style='grid-template-columns:repeat(%d,1fr)'>" % len(order) + "".join(f"<div class='kpi'><div class='n'>{avg[k]}</div><div class='l'>{SETUPS[k]}"
                                        f"<br>mean score /100</div></div>" for k in order) + "</div>"]
    h.append("<table><tr><th>Scenario</th>" + "".join(f"<th>{SETUPS[k]}</th>" for k in order) + "<th>Judge gap*</th></tr>")
    for s in slugs:
        r = R[s]["setups"]
        best = max(order, key=lambda k: r[k]["strict"])
        h.append(f"<tr><td><b>{s}</b><br><span class='small'>{escape(BY_SLUG[s]['question'])}</span></td>" + "".join(
            f"<td class='num{' hi' if k == best else ''}'>{r[k]['strict']}{' ⚠' if r[k]['invented'] else ''}"
            f"<br><span class='small'>Opus {r[k]['by_judge'].get('opus')} · GPT {r[k]['by_judge'].get('gpt')}</span></td>"
            for k in order) + f"<td class='num'>{R[s]['judge_mad']}</td></tr>")
    h.append("</table><div class='small'>Score = weighted 0-100 over the parameters that apply to the scenario's pattern, "
             "mean of the two judges. ⚠ = invention gate tripped (an unsourced chart, table or verdict number), score "
             "capped at 40. *Judge gap = mean absolute difference between the two judges per parameter (0-5 scale). "
             f"{escape(pick_note)}</div>")
    h.append("<h2>What was measured</h2><table><tr><th>Parameter</th><th>Weight</th><th>How it is checked</th></tr>" + "".join(
        f"<tr><td><b>{p['name']}</b><br><span class='small'>{escape(p['definition'][:220])}</span></td>"
        f"<td class='num'>{p['weight']}</td><td class='small'>{escape(p['verification']['method'])}</td></tr>"
        for p in RUBRIC["parameters"]) + "</table>")
    h.append("<div class='small'>Every respondent got the same specification and the same right to draw charts and "
             "tables; plain models were told to label memory values as estimates or cite a reference. An honest "
             "estimate earns 1 on measured parameters with no accuracy penalty; an unsourced value earns 0.</div>")

    for s in slugs:
        r, g = R[s], G[s]
        sc = BY_SLUG[s]
        h.append(f"<div class='pb'></div><h1 style='font-size:24px'>{escape(sc['title'] if 'title' in sc else s)}</h1>"
                 f"<div class='lead'><b>Question:</b> {escape(sc['question'])}<br><b>Why it is hard:</b> "
                 f"{escape(sc['special'])}<br><b>Pattern:</b> {sc['pattern']} · <b>Category:</b> {sc['category']}</div>")
        ps = list(r["setups"]["claude_bare"]["params"])
        h.append("<table><tr><th>Parameter (0-5)</th>" + "".join(f"<th>{SETUPS[k]}</th>" for k in order) + "</tr>")
        for p in ps:
            vals = [r["setups"][k]["params"][p] for k in order]
            h.append(f"<tr><td>{PARAMS[p]['name']} <span class='small'>w{PARAMS[p]['weight']}</span></td>" + "".join(
                f"<td class='num{' hi' if v == max(vals) else ''}'>{v}</td>" for v in vals) + "</tr>")
        h.append("<tr><td><b>Weighted /100</b></td>" + "".join(
            f"<td class='num hi'>{r['setups'][k]['strict']}</td>" for k in order) + "</tr></table>")
        h.append("<h2>Script findings</h2><table><tr><th></th>" + "".join(f"<th>{SETUPS[k]}</th>" for k in order) + "</tr>")
        rows = [("Numbers traced to the corpus", lambda x: f"{x['numbers']['traced']}/{x['numbers']['total']}"),
                ("Untagged, untraced numbers", lambda x: str(x["numbers"]["untagged_untraced"])),
                ("Charts (traced share)", lambda x: ", ".join(
                    "inv" if any(se["how"] in ("none", "badcall") for se in c.get("series", [])) else
                    (f"{min((se['traced_share'] or 0) for se in c['series']):.0%}" if c.get("series") and all(
                        se["how"] == "call" for se in c["series"]) else "memory") for c in x["charts"]) or "none"),
                ("CSV exports (traced share)", lambda x: ", ".join(
                    f"{t['traced_share']:.0%}" if t["how"] == "call" else t["how"] for t in x["tables"]) or "none"),
                ("DOIs found in 401M-work corpus", lambda x: f"{x['dois']['found_in_corpus']}/{x['dois']['cited']}"),
                ("Follow-up calls that ran and returned data", lambda x: f"{x['followups_ok']}/{len(x['followups'])}"),
                ("Verdict: four lines, first, ≤150 words", lambda x: "yes" if x["verdict_structure"]["four_lines"] and x["verdict_structure"]["first"] and x["verdict_structure"]["words"] <= 150 else "no"),
                ("Invention gate", lambda x: "TRIPPED" if x["invented"] else "clear")]
        for name, fn in rows:
            h.append(f"<tr><td>{name}</td>" + "".join(f"<td class='num'>{escape(fn(g[k]))}</td>" for k in order) + "</tr>")
        h.append("</table>")
        for w, v in r["verdicts"].items():
            h.append(f"<p><b>{'Claude Opus' if w == 'opus' else 'GPT'} judge:</b> {escape(v or '')}</p>")
        errs = {k: sorted(set(sum((r["errors"].get(w, {}).get(k) or [] for w in r["errors"]), [])))[:4] for k in order}
        if any(errs.values()):
            h.append("<h2>Errors the judges found</h2><table>" + "".join(
                f"<tr><td style='width:150px'><b>{SETUPS[k]}</b></td><td class='small'>{'<br>'.join(escape(str(e)) for e in errs[k]) or '—'}</td></tr>"
                for k in order) + "</table>")
        d = os.path.join(OUT, s)
        for m, mk in ((RESP_LABEL, "claude"), ("ChatGPT", "chatgpt")):
            if mk + "_bare" not in SETUPS:
                continue
            h.append(f"<div class='pb'></div><h2>Before / after: {m} — first screen</h2><div class='pair'>"
                     f"<div><div class='h'>BEFORE · {m} alone · {r['setups'][mk + '_bare']['strict']}/100</div>"
                     f"<img src='file://{d}/{mk}_bare_first.png'></div>"
                     f"<div><div class='h'>AFTER · {m} + Prism · {r['setups'][mk + '_prism']['strict']}/100</div>"
                     f"<img src='file://{d}/{mk}_prism_first.png'></div></div>")
    h.append("<div class='pb'></div><h1 style='font-size:24px'>Appendix: full deliverables</h1><div class='lead'>Each "
             "deliverable rendered by the same template. Tags on charts and tables come from the script pass.</div>")
    for s in slugs:
        for k in order:
            h.append(f"<div class='pb'></div><h2>{s} · {SETUPS[k]} · {R[s]['setups'][k]['strict']}/100</h2>")
            for p in slices(os.path.join(OUT, s, f"{k}_full.png")):
                h.append(f"<div class='full'><img src='file://{p}'></div>")
    html = (f"<!doctype html><html><head><meta charset='utf-8'><title>Benchmark pilot</title><style>{css}</style>"
            f"</head><body><div class='wrap'>{''.join(h)}</div></body></html>")
    hp = (out or os.path.join(OUT, "benchmark_v2_pilot.pdf"))[:-4] + ".html"
    open(hp, "w").write(html)
    pp = out or os.path.join(OUT, "benchmark_v2_pilot.pdf")
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={pp}", "file://" + hp], capture_output=True, timeout=300)
    return pp


# ---------------------------------------------------------------- main

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pick", type=int, default=0)
    ap.add_argument("--slugs", default="")
    ap.add_argument("--stage", default="all")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    meta_p = os.path.join(OUT, "pilot.json")
    if a.pick:
        pool = [s for s in SCENARIOS if s["pattern"] in TREND_PATTERNS]
        slugs = [s["slug"] for s in random.Random(SEED).sample(pool, a.pick)]
        note = (f"Scenarios drawn with random.Random({SEED}).sample() from the {len(pool)} scenarios whose pattern "
                f"has a time dimension ({', '.join(TREND_PATTERNS)}).")
        json.dump({"slugs": slugs, "note": note}, open(meta_p, "w"), indent=1)
    elif a.slugs:
        slugs = a.slugs.split(",")
        note = "Scenarios chosen by hand."
    else:
        m = json.load(open(meta_p))
        slugs, note = m["slugs"], m["note"]
    print("scenarios:", slugs, flush=True)
    st = a.stage
    for s in slugs:
        if st in ("all", "answers"):
            answers(s, a.force)
        if st in ("all", "ground"):
            ans = json.load(open(os.path.join(OUT, s, "answers.json")))
            calls = calls_of(s)
            with ThreadPoolExecutor(4) as ex:
                gr = dict(zip(SETUPS, ex.map(lambda k: ground(s, k, ans[k]["text"], calls), SETUPS)))
            json.dump(gr, open(os.path.join(OUT, s, "ground.json"), "w"), ensure_ascii=False, indent=1, default=str)
            print(f"  ground {s}: " + "; ".join(f"{k} {v['ceiling']}" for k, v in gr.items()), flush=True)
        if st in ("all", "judge"):
            with ThreadPoolExecutor(2) as ex:
                list(ex.map(lambda w: judge(s, w), ("opus", "gpt")))
            r = results(s)
            print(f"  results {s}: " + ", ".join(f"{k} {v['strict']}" for k, v in r["setups"].items()), flush=True)
        if st in ("all", "render"):
            screens(s)
    if st in ("all", "pdf", "render"):
        print("pdf:", pdf(slugs, note), flush=True)
    print("BENCH_V2_DONE", flush=True)


if __name__ == "__main__":
    main()
