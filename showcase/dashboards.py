"""Dashboards built by an assistant from the Prism MCP: one brief in, a working HTML dashboard out.

Each dashboard is a single prompt given to Claude connected live to the Prism MCP. The model chooses its own
tools, builds the page, checks it with Prism's check_report, and returns the HTML. The session is recorded
(every tool call, its arguments and timing) so the page can show exactly how the dashboard was made.

    python3 showcase/dashboards.py [--only slug] [--model claude-opus-5-5]

Writes docs/dashboards/<slug>/{dashboard.html, session.json, README.md, screenshot.jpg} and the map files.
"""
import argparse
import json
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT = os.path.join(ROOT, "docs", "dashboards")

COMMON = """
HOW TO BUILD IT
- One self-contained HTML document inside a single ```html fenced block, nothing outside it.
- Charts: Vega-Lite 5 from cdn.jsdelivr.net (vega@5.30.0, vega-lite@5.21.0, vega-embed@6.26.0), each drawn with
  vegaEmbed('#<id>', spec) into an element with that id, with a pixel width (never "container") and the data inline.
- Maps: world countries from the relative URL world_india_official.geojson (properties.iso3, properties.name);
  Indian states from india_states_official.geojson (properties.name, and properties.key = the lower-case state
  label Prism returns, e.g. "delhi", "uttar pradesh"). Both draw India with its official outline. Use no other map file.
- Every number on the page names the Prism call it came from (a small source line under each panel is enough)
  and the window it was counted over. If a call returned nothing or a row is an artefact, say so on the page.
- Light and dark readable, works at phone width, a CSV download button for each table (built from the embedded data).
- Before you answer, run check_report on the finished page and fix everything it lists.
"""

DASHBOARDS = {
    "air-pollution-geo": {
        "title": "Air pollution: geo-intelligence dashboard",
        "use_case": "GEO intelligence",
        "prompt": """Build a geo-intelligence dashboard on AIR POLLUTION for an environmental policy team in India, using the
Prism tools. They want to see, on one screen and then below it, where the issue is being reported, where it is
studied, how India compares with the world, and which places and stories are driving it.

Panels:
1. Header KPI tiles: total coverage, India's share of placed coverage and its lift, how much coverage could be
   placed at all, and the research volume. Each tile states its window.
2. World map: the country each article is about, coloured by lift over the all-news baseline, with a ranked table
   (articles, share, lift).
3. India state map: coverage and lift by state. The state level returns places outside India too; show only
   Indian states on the map and list what you excluded.
4. City leaderboard: the Indian cities and the NCR cluster, with lift.
5. Trend: monthly coverage for India against the rest of the world, with the incomplete newest month handled.
6. Studied vs reported vs patented: the separate geography lanes for research and patents next to news, never
   added together, with India and three comparators.
7. The critical stories: date, publisher, headline and link.
8. Data quality: placement share, windows and censoring, and any artefacts you caught (labels that are not
   places, acronym collisions), so a reader trusts the map for the right reasons.
""",
    },
}


def run(slug, model):
    os.environ["BENCH_CLAUDE_MODEL"] = model
    sys.path.insert(0, os.path.join(ROOT, "benchmarks"))
    import bench_deep
    import bench  # noqa: F401  (bench_deep reads the respondent model through it)
    d = os.path.join(OUT, slug)
    os.makedirs(d, exist_ok=True)
    for f in ("world_india_official.geojson", "india_states_official.geojson"):
        shutil.copy(os.path.join(HERE, "assets", f), os.path.join(d, f))
    spec = DASHBOARDS[slug]
    prompt = f"Today is {bench_deep.TODAY}. You are connected to the Prism MCP server.\n\n{spec['prompt']}\n{COMMON}"
    r = bench_deep.run_claude(prompt, True)
    html = bench_deep.extract_html(r["text"])
    open(os.path.join(d, "dashboard.html"), "w").write(html)
    calls = [{"n": i + 1, "tool": c["tool"], "args": c.get("args"), "start_s": c.get("start"),
              "seconds": c.get("seconds"), "returned": "end" in c, "ok": '"ok":true' in (c.get("result") or "").replace(" ", "")[:200]}
             for i, c in enumerate(r["calls"])]
    json.dump({"slug": slug, "model": r["model"], "prompt": prompt, "timing": r["timing"], "calls": calls},
              open(os.path.join(d, "session.json"), "w"), ensure_ascii=False, indent=1)
    rc = bench_deep.render_check(os.path.join(d, "dashboard.html"), os.path.join(d, "screenshot_full.png"))
    from prism import report_check
    chk = report_check.check(html)
    json.dump({"render": rc, "check_report": chk}, open(os.path.join(d, "check.json"), "w"), indent=1)
    shots(d)
    readme(slug, spec, r, calls, rc, chk, d)
    print(f"{slug}: {r['timing']['wall_seconds']}s, {len(calls)} calls, {rc['rendered_views']} views, "
          f"{len(rc['console_errors'])} console errors, ready={chk['ready']}", flush=True)


def shots(d):
    from PIL import Image
    im = Image.open(os.path.join(d, "screenshot_full.png")).convert("RGB")
    top = im.crop((0, 0, im.width, min(im.height, 1500)))
    top.resize((1000, int(top.height * 1000 / top.width))).save(os.path.join(d, "screenshot.jpg"), quality=78, optimize=True)
    full = im.resize((700, int(im.height * 700 / im.width)))
    full.save(os.path.join(d, "screenshot_full.jpg"), quality=60, optimize=True)
    os.remove(os.path.join(d, "screenshot_full.png"))


def readme(slug, spec, r, calls, rc, chk, d):
    tm = r["timing"]
    L = [f"# {spec['title']}", "",
         f"**Use case:** {spec['use_case']} · **Built by:** {r['model']} connected live to the Prism MCP · "
         f"**Time:** {tm['wall_seconds']/60:.1f} min, {len(calls)} Prism calls", "",
         "[Open the live dashboard](dashboard.html) (open it from a web server or the hosted copy so the map files load).", "",
         "![Dashboard, first screen](screenshot.jpg)", "",
         "## The brief", "", "One prompt, given verbatim:", "", "```text", spec["prompt"].strip(), "```", "",
         "Plus the build rules every dashboard gets (Vega-Lite, the official-outline map files, a source line under "
         "every panel, CSV downloads, and a `check_report` pass before answering). Full prompt: `session.json`.", "",
         "## How the assistant built it", "", "The model chose these Prism tools itself, in this order:", "",
         "| # | Tool | Arguments | Seconds |", "|---:|---|---|---:|"]
    for c in calls:
        a = json.dumps(c["args"], ensure_ascii=False)
        L.append(f"| {c['n']} | `{c['tool']}` | `{a[:110]}{'…' if len(a) > 110 else ''}` | {c['seconds'] if c['seconds'] is not None else '—'} |")
    L += ["", "## Checks on the finished page", "",
          f"- Charts rendered in headless Chrome: **{rc['rendered_views']}**, zero-width: {rc.get('zero_width_views', 0)}, console errors: {len(rc['console_errors'])}",
          f"- Prism `check_report`: {'ready, nothing to fix' if chk['ready'] else 'issues: ' + '; '.join(chk['issues'])}",
          f"- India appears with its official outline (J&K including PoK, Gilgit-Baltistan and Aksai Chin; Ladakh is drawn inside J&K in the state file).", "",
          "## The whole page", "", "![Dashboard, full page](screenshot_full.jpg)", ""]
    open(os.path.join(d, "README.md"), "w").write("\n".join(L) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--model", default="claude-opus-5-5")
    a = ap.parse_args()
    for slug in (a.only.split(",") if a.only else DASHBOARDS):
        run(slug, a.model)


if __name__ == "__main__":
    main()
