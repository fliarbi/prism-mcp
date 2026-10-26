"""Aggregate the full benchmark run into GitHub pages, a summary PDF and the hosted-file list.

    python3 benchmarks/bench_summary.py [--pdf-base URL]

Reads benchmarks/results/full/<slug>/{results,ground,answers}.json and writes:
    benchmarks/README.md                       the headline page (method, scores, tables, links)
    benchmarks/results/full/<slug>/README.md    one page per scenario: parameter table, findings, before/after
    benchmarks/results/full/summary.json        every number on those pages
    benchmarks/results/full/summary.pdf         the headline page as a PDF
"""
import argparse
import json
import os
import subprocess
import sys
from collections import defaultdict
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FULL = os.path.join(ROOT, "benchmarks", "results", "full")
os.environ["BENCH_OUT"] = FULL
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "showcase"))
import bench as v2  # noqa: E402
import svgchart as sc  # noqa: E402
from scenarios import CATEGORIES, SCENARIOS  # noqa: E402

ORDER = ["claude_bare", "claude_prism", "chatgpt_bare", "chatgpt_prism"]
NAME = {"claude_bare": "Claude alone", "claude_prism": "Claude + Prism",
        "chatgpt_bare": "ChatGPT alone", "chatgpt_prism": "ChatGPT + Prism"}
CAT = {c[0]: c[1] for c in CATEGORIES}


def load(slug, f):
    p = os.path.join(FULL, slug, f)
    return json.load(open(p)) if os.path.exists(p) else None


def mean(xs):
    xs = [x for x in xs if x is not None]
    return round(sum(xs) / len(xs), 1) if xs else None


def collect():
    rows = []
    for s in SCENARIOS:
        r, g, a = load(s["slug"], "results.json"), load(s["slug"], "ground.json"), load(s["slug"], "answers.json")
        if not (r and g and a):
            continue
        rows.append({"s": s, "r": r, "g": g, "a": a})
    return rows


def tables(rows):
    out = {"n": len(rows)}
    out["mean"] = {k: mean([x["r"]["setups"][k]["strict"] for x in rows]) for k in ORDER}
    out["mean_plain"] = {k: mean([x["r"]["setups"][k]["plain"] for x in rows]) for k in ORDER}
    wins = {}
    for m in ("claude", "chatgpt"):
        b, p = f"{m}_bare", f"{m}_prism"
        w = sum(1 for x in rows if x["r"]["setups"][p]["strict"] > x["r"]["setups"][b]["strict"])
        t = sum(1 for x in rows if x["r"]["setups"][p]["strict"] == x["r"]["setups"][b]["strict"])
        wins[m] = {"prism_wins": w, "ties": t, "bare_wins": len(rows) - w - t,
                   "mean_gain": mean([x["r"]["setups"][p]["strict"] - x["r"]["setups"][b]["strict"] for x in rows])}
    out["wins"] = wins
    out["best_overall"] = {k: sum(1 for x in rows if max(ORDER, key=lambda q: x["r"]["setups"][q]["strict"]) == k) for k in ORDER}
    cat, pat = defaultdict(list), defaultdict(list)
    for x in rows:
        cat[x["s"]["category"]].append(x)
        pat[x["s"]["pattern"]].append(x)
    out["by_category"] = {c: {"n": len(v), **{k: mean([x["r"]["setups"][k]["strict"] for x in v]) for k in ORDER}} for c, v in cat.items()}
    out["by_pattern"] = {p: {"n": len(v), **{k: mean([x["r"]["setups"][k]["strict"] for x in v]) for k in ORDER}} for p, v in pat.items()}
    par = {}
    for key, p in v2.PARAMS.items():
        app = [x for x in rows if key in x["r"]["setups"]["claude_bare"]["params"]]
        if not app:
            continue
        par[key] = {"name": p["name"], "weight": p["weight"], "n": len(app)}
        for k in ORDER:
            vals = [x["r"]["setups"][k]["params"][key] for x in app]
            prod = [v for v in vals if v >= 2]
            par[key][k] = {"mean": mean(vals), "produce_pct": round(100 * len(prod) / len(vals)), "quality": mean(prod)}
    out["by_parameter"] = par
    out["invention_rate"] = {k: round(100 * sum(1 for x in rows if x["r"]["setups"][k]["invented"]) / len(rows)) for k in ORDER}
    out["judge_mad"] = mean([x["r"]["judge_mad"] for x in rows if x["r"].get("judge_mad") is not None])
    out["traced_numbers"] = {k: (sum(x["g"][k]["numbers"]["traced"] for x in rows), sum(x["g"][k]["numbers"]["total"] for x in rows)) for k in ORDER}
    out["dois"] = {k: (sum(x["g"][k]["dois"]["found_in_corpus"] for x in rows), sum(x["g"][k]["dois"]["cited"] for x in rows)) for k in ORDER}
    out["seconds"] = {k: mean([x["a"][k]["seconds"] for x in rows]) for k in ORDER}
    return out


def md_table(head, body):
    return "| " + " | ".join(head) + " |\n|" + "|".join("---" for _ in head) + "|\n" + "\n".join("| " + " | ".join(str(c) for c in r) + " |" for r in body)


def scenario_page(x, pdf_base):
    s, r, g = x["s"], x["r"], x["g"]
    ps = list(r["setups"]["claude_bare"]["params"])
    best = max(ORDER, key=lambda k: r["setups"][k]["strict"])
    L = [f"# {s['title']}", "", f"**Question.** {s['question'].splitlines()[0]}", "",
         f"**Category:** {CAT.get(s['category'], s['category'])} · **Pattern:** `{s['pattern']}` · **Why it is hard:** {s['special']}", ""]
    L += [md_table(["Score /100"] + [NAME[k] for k in ORDER],
                   [["Weighted (strict)"] + [f"**{r['setups'][k]['strict']}**" if k == best else r['setups'][k]['strict'] for k in ORDER],
                    ["Opus judge"] + [r["setups"][k]["by_judge"].get("opus") for k in ORDER],
                    ["GPT judge"] + [r["setups"][k]["by_judge"].get("gpt") for k in ORDER]]), ""]
    L += ["## Parameter scores (0-5)", "", md_table(["Parameter", "Weight"] + [NAME[k] for k in ORDER],
          [[v2.PARAMS[p]["name"], v2.PARAMS[p]["weight"]] + [r["setups"][k]["params"][p] for k in ORDER] for p in ps]), ""]
    L += ["## Script findings", "", md_table(["Check"] + [NAME[k] for k in ORDER], [
        ["Numbers traced to the corpus"] + [f"{g[k]['numbers']['traced']}/{g[k]['numbers']['total']}" for k in ORDER],
        ["Charts (traced share)"] + [", ".join("invented" if any(se["how"] in ("none", "badcall") for se in c.get("series", [])) else
                                               (f"{min((se['traced_share'] or 0) for se in c['series']):.0%}" if c.get("series") and all(se["how"] == "call" for se in c["series"]) else "memory")
                                               for c in g[k]["charts"]) or "none" for k in ORDER],
        ["DOIs that resolve"] + [f"{g[k]['dois']['found_in_corpus']}/{g[k]['dois']['cited']}" for k in ORDER],
        ["Follow-up queries that ran"] + [f"{g[k]['followups_ok']}/{len(g[k]['followups'])}" for k in ORDER],
        ["Invention gate"] + ["tripped" if g[k]["invented"] else "clear" for k in ORDER]]), ""]
    for w, v in (r.get("verdicts") or {}).items():
        L.append(f"**{'Claude Opus' if w == 'opus' else 'GPT'} judge:** {v}\n")
    L += ["## Before / after (first screen)", "", "| | Alone | With Prism |", "|---|---|---|",
          f"| Claude | ![](claude_bare_first.jpg) | ![](claude_prism_first.jpg) |",
          f"| ChatGPT | ![](chatgpt_bare_first.jpg) | ![](chatgpt_prism_first.jpg) |", ""]
    if pdf_base:
        L.append(f"Full deliverables, rendered: [PDF]({pdf_base}/{s['slug']}.pdf). Raw answers, ground pass and judge "
                 f"outputs: `answers.json`, `ground.json`, `judge_opus.json`, `judge_gpt.json` in this folder.")
    open(os.path.join(FULL, s["slug"], "README.md"), "w").write("\n".join(L) + "\n")


def headline(T, rows, pdf_base):
    m = T["mean"]
    L = ["# Benchmark: what Prism adds to Claude and ChatGPT", "",
         f"Every one of the {T['n']} showcase scenarios, four respondents each: Claude (Sonnet) and ChatGPT (gpt-6-luna), "
         "each answering from memory and again with Prism's recorded tool results. Every respondent got the same "
         "deliverable specification (a decision-grade report with a verdict, measured trend, comparison, charts, "
         "drill-down, exports and references) and the same right to draw charts and tables from memory, labelled as "
         "estimates. The scoring rubric was designed by Fable 5.1; a script scores every checkable parameter first "
         "(number tracing, chart and CSV tracing, DOI lookup against the research index, follow-up execution), then two "
         "blind judges (Claude Opus, GPT) score under those ceilings and may only lower them.", "",
         "![scores](results/full/scoreboard.svg)", "",
         md_table(["", "Claude alone", "Claude + Prism", "ChatGPT alone", "ChatGPT + Prism"],
                  [["Mean score /100 (strict)"] + [m[k] for k in ORDER],
                   ["Mean score /100 (no gates)"] + [T["mean_plain"][k] for k in ORDER],
                   ["Best of the four, scenarios"] + [T["best_overall"][k] for k in ORDER],
                   ["Numbers traced to the corpus"] + [f"{T['traced_numbers'][k][0]:,}/{T['traced_numbers'][k][1]:,}" for k in ORDER],
                   ["DOIs that resolve"] + [f"{T['dois'][k][0]}/{T['dois'][k][1]}" for k in ORDER],
                   ["Invention gate tripped"] + [f"{T['invention_rate'][k]}%" for k in ORDER],
                   ["Mean answer time, s"] + [T["seconds"][k] for k in ORDER]]), "",
         "**Same model, with and without Prism:**", "",
         md_table(["Model", "Prism wins", "Ties", "Memory wins", "Mean gain (points)"],
                  [[("Claude" if mm == "claude" else "ChatGPT"), w["prism_wins"], w["ties"], w["bare_wins"], w["mean_gain"]]
                   for mm, w in T["wins"].items()]), "",
         f"Judge agreement: mean absolute difference {T['judge_mad']} points per parameter on the 0-5 scale. Both judges "
         "are of the same model families as the respondents; the script ceilings exist to limit that bias.", "",
         "## By parameter", "", "Mean score (0-5), and the capability matrix: share of scenarios where the setup "
         "produced something real (score ≥ 2) · mean quality when it did.", "",
         md_table(["Parameter", "Weight", "Scenarios"] + [NAME[k] for k in ORDER],
                  [[p["name"], p["weight"], p["n"]] + [f"{p[k]['mean']} ({p[k]['produce_pct']}% · {p[k]['quality'] or '—'})" for k in ORDER]
                   for p in T["by_parameter"].values()]), "",
         "## By category", "", md_table(["Category", "Scenarios"] + [NAME[k] for k in ORDER],
                                        [[CAT.get(c, c), v["n"]] + [v[k] for k in ORDER] for c, v in sorted(T["by_category"].items(), key=lambda kv: -kv[1]["claude_prism"])]), "",
         "## By pattern", "", md_table(["Pattern", "Scenarios"] + [NAME[k] for k in ORDER],
                                       [[f"`{p}`", v["n"]] + [v[k] for k in ORDER] for p, v in sorted(T["by_pattern"].items(), key=lambda kv: -kv[1]["claude_prism"])]), "",
         "## Where memory beat Prism", ""]
    lost = [x for x in rows if max(x["r"]["setups"]["claude_bare"]["strict"], x["r"]["setups"]["chatgpt_bare"]["strict"]) >=
            max(x["r"]["setups"]["claude_prism"]["strict"], x["r"]["setups"]["chatgpt_prism"]["strict"])]
    L.append(f"{len(lost)} of {T['n']} scenarios had a memory-only answer scoring at least as high as both Prism answers:" if lost
             else "In no scenario did a memory-only answer match the best Prism answer.")
    for x in lost:
        L.append(f"- [{x['s']['title']}](results/full/{x['s']['slug']}/README.md): " + ", ".join(
            f"{NAME[k]} {x['r']['setups'][k]['strict']}" for k in ORDER))
    L += ["", "## Every scenario", "", md_table(["Scenario", "Category"] + [NAME[k] for k in ORDER] + ["Details"],
          [[x["s"]["title"], CAT.get(x["s"]["category"], x["s"]["category"])] +
           [x["r"]["setups"][k]["strict"] for k in ORDER] +
           [f"[page](results/full/{x['s']['slug']}/README.md)" + (f" · [PDF]({pdf_base}/{x['s']['slug']}.pdf)" if pdf_base else "")]
           for x in rows]), "",
         "## Method", "",
         "- Rubric: `benchmarks/rubric/benchmark_rubric.json` (and `.md` for the reasoning), 11 parameters, weights per pattern.",
         "- Harness: `benchmarks/bench.py` (prompts, ground pass, judges, renderer), `benchmarks/bench_full.py` (this run), "
         "`benchmarks/bench_summary.py` (this page).",
         "- Prism setups received the scenario's recorded Prism calls in full (`docs/examples/<slug>.json`), so retrieval is "
         "held constant; deep live-MCP tiers are in `benchmarks/bench_deep.py`.",
         "- Gates: an unsourced chart, table or verdict number caps a deliverable at 40; the 'no gates' row shows scores without it.",
         ""]
    if pdf_base:
        L.append(f"Summary PDF: [{pdf_base}/summary.pdf]({pdf_base}/summary.pdf)")
    open(os.path.join(ROOT, "benchmarks", "README.md"), "w").write("\n".join(L) + "\n")


def scoreboard(T):
    svg = sc.hbar_chart([(NAME[k], T["mean"][k]) for k in sorted(ORDER, key=lambda k: -T["mean"][k])],
                        "Mean benchmark score by setup", f"{T['n']} scenarios, 0-100, mean of two blind judges",
                        "source: benchmarks/results/full")
    sc.save(svg, os.path.join(FULL, "scoreboard.svg"))


def summary_pdf(T, rows):
    import markdown
    md = open(os.path.join(ROOT, "benchmarks", "README.md")).read()
    md = md.replace("](results/full/scoreboard.svg)", f"](file://{FULL}/scoreboard.svg)")
    html = markdown.markdown(md, extensions=["tables"])
    css = v2.PAGE_CSS + "@page{size:A4;margin:12mm}.wrap{max-width:none;padding:0}table{font-size:11px}img{max-width:100%}"
    hp = os.path.join(FULL, "summary.html")
    open(hp, "w").write(f"<!doctype html><html><head><meta charset='utf-8'><style>{css}</style></head><body><div class='wrap'>{html}</div></body></html>")
    subprocess.run([v2.CHROME, "--headless=new", "--no-sandbox", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={os.path.join(FULL, 'summary.pdf')}", "file://" + hp], capture_output=True, timeout=300)
    os.remove(hp)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf-base", default="")
    a = ap.parse_args()
    rows = collect()
    T = tables(rows)
    json.dump(T, open(os.path.join(FULL, "summary.json"), "w"), ensure_ascii=False, indent=1)
    scoreboard(T)
    for x in rows:
        scenario_page(x, a.pdf_base)
    headline(T, rows, a.pdf_base)
    summary_pdf(T, rows)
    print(f"{T['n']} scenarios; mean {T['mean']}; wins {T['wins']}")


if __name__ == "__main__":
    main()
