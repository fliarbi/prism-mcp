"""Advanced disease pages: one tabbed analytical page per disease, built from Prism calls.

Tabs: Overview · Risk factors · Protective & prevention · Treatments · Causes & mechanisms · Evidence quality,
and, when the research and news index answers: Research & news · Geography · Month by month. A tab whose data
did not come back is left out rather than shown empty. Writes
    docs/diseases/<slug>/{README.md, data.json, risk-factors.gif, screenshot.jpg}
    docs/diseases/<slug>/page/index.html            (the interactive page, hosted as-is)

    python3 showcase/disease_pages.py [--only type-2-diabetes] [--refresh]
"""
import argparse
import json
import os
import sys
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
OUT = os.path.join(ROOT, "docs", "diseases")
HOST = "https://fliarbi.com/demo/docs/prism-dashboards-3bb43e4c/diseases"

DISEASES = {
    "type-2-diabetes": {"name": "Type 2 diabetes", "term": "type 2 diabetes", "claim": "Obesity increases the risk of type 2 diabetes",
                        "phrases": ["type 2 diabetes"]},
    "tuberculosis": {"name": "Tuberculosis", "term": "tuberculosis", "claim": "Diabetes increases the risk of tuberculosis",
                     "phrases": ["tuberculosis"]},
    "breast-cancer": {"name": "Breast cancer", "term": "breast cancer", "claim": "Obesity increases the risk of breast cancer",
                      "phrases": ["breast cancer"]},
}


def collect(slug, spec, refresh=False):
    import prism_mcp as m
    path = os.path.join(OUT, slug, "data.json")
    data = json.load(open(path)) if os.path.exists(path) and not refresh else {}

    def get(key, tool, **args):
        if data.get(key, {}).get("ok"):
            return
        try:
            data[key] = m.REGISTRY[tool]["fn"](**args)
        except Exception as e:
            data[key] = {"ok": False, "error": {"reason": str(e)}}
        print(f"  {slug} {key}: {data[key].get('ok')}", flush=True)
    get("profile", "disease_profile", disease=spec["term"])
    get("stance", "stance_trends", term=spec["term"])
    get("news", "news_trends", term=spec["term"], since="2024-06-01")
    get("geo", "global_comparison", claim=spec["claim"])
    get("history", "historical_analysis", subject_phrases=spec["phrases"], query_seconds=30)
    hid = ((data.get("history") or {}).get("data") or {}).get("history_id")
    if hid:
        get("scenarios", "trend_scenarios", history_id=hid, horizon=3)
    get("timeline", "deep_timeline", term=spec["term"], months=12)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(data, open(path, "w"), ensure_ascii=False, indent=1, default=str)
    return data


def ok(data, key):
    d = data.get(key) or {}
    return d.get("data") if d.get("ok") else None


# ─────────────────────────────────────────── HTML page ───────────────────────────────────────────
CSS = """
:root{--bg:#f7f6f2;--card:#fff;--ink:#14161a;--ink2:#555a66;--line:#e4e2da;--a:#2a78d6;--b:#eb6834;--c:#1baf7a}
@media (prefers-color-scheme:dark){:root{--bg:#111316;--card:#1a1d22;--ink:#eceef2;--ink2:#a7adb9;--line:#2a2e35}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:15px/1.55 -apple-system,Segoe UI,Helvetica,Arial,sans-serif}
.w{max-width:1100px;margin:0 auto;padding:24px 16px 60px}h1{font-size:28px;margin:0 0 4px}.sub{color:var(--ink2);margin:0 0 16px}
.kpis{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:10px;margin:14px 0 18px}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px}.kpi b{display:block;font-size:24px}.kpi span{color:var(--ink2);font-size:12.5px}
.tabs{display:flex;flex-wrap:wrap;gap:6px;border-bottom:1px solid var(--line);margin-bottom:16px}
.tabs button{background:none;border:0;border-bottom:3px solid transparent;padding:10px 12px;font:inherit;font-weight:600;color:var(--ink2);cursor:pointer}
.tabs button[aria-selected=true]{color:var(--ink);border-color:var(--a)}
.panel{display:none}.panel.on{display:block}
.card{background:var(--card);border:1px solid var(--line);border-radius:12px;padding:16px;margin-bottom:14px}
.card h3{margin:0 0 6px;font-size:16px}.note{color:var(--ink2);font-size:12.5px}
table{border-collapse:collapse;width:100%;font-size:13.5px}th,td{padding:6px 8px;border-bottom:1px solid var(--line);text-align:left}td.n{text-align:right;font-variant-numeric:tabular-nums}
.grid2{display:grid;grid-template-columns:1fr 1fr;gap:14px}@media(max-width:760px){.grid2{grid-template-columns:1fr}}
.m{border-left:3px solid var(--a);padding:6px 12px;margin:10px 0}.m .h{font-weight:700}.sig{font-size:11px;color:var(--ink2);text-transform:uppercase;letter-spacing:.05em}
.chart{width:100%;overflow-x:auto}
"""


def vbar(id_, rows, title, color="#2a78d6", second=None, xtitle="claims"):
    vals = [{"label": r[0], "value": r[1], **({"high": r[2]} if second else {})} for r in rows]
    layer = [{"mark": {"type": "bar", "color": color, "cornerRadiusEnd": 3},
              "encoding": {"x": {"field": "value", "type": "quantitative", "title": xtitle}}}]
    if second:
        layer.append({"mark": {"type": "bar", "color": "#eb6834", "cornerRadiusEnd": 3},
                      "encoding": {"x": {"field": "high", "type": "quantitative"}}})
    spec = {"$schema": "https://vega.github.io/schema/vega-lite/v5.json", "width": 520, "height": max(120, 26 * len(vals)),
            "title": {"text": title, "anchor": "start", "fontSize": 14}, "data": {"values": vals},
            "encoding": {"y": {"field": "label", "type": "nominal", "sort": {"field": "value", "order": "descending"}, "title": None},
                         "tooltip": [{"field": "label"}, {"field": "value", "title": "claims"}] + ([{"field": "high", "title": "high-tier claims"}] if second else [])},
            "layer": layer, "config": {"background": None, "view": {"stroke": None}}}
    return f'<div class="chart" id="{id_}"></div><script>vegaEmbed("#{id_}",{json.dumps(spec)},{{actions:false}});</script>'


def vline(id_, series, title, ytitle):
    vals = [{"x": x, "y": y, "s": s} for s, pts in series for x, y in pts]
    spec = {"$schema": "https://vega.github.io/schema/vega-lite/v5.json", "width": 760, "height": 260,
            "title": {"text": title, "anchor": "start", "fontSize": 14}, "data": {"values": vals},
            "mark": {"type": "line", "point": True, "strokeWidth": 2},
            "encoding": {"x": {"field": "x", "type": "ordinal", "title": None}, "y": {"field": "y", "type": "quantitative", "title": ytitle},
                         "color": {"field": "s", "type": "nominal", "title": None, "scale": {"range": ["#2a78d6", "#eb6834", "#1baf7a"]}},
                         "tooltip": [{"field": "s"}, {"field": "x"}, {"field": "y"}]},
            "config": {"background": None, "view": {"stroke": None}}}
    return f'<div class="chart" id="{id_}"></div><script>vegaEmbed("#{id_}",{json.dumps(spec)},{{actions:false}});</script>'


def table(rows, head):
    return "<table><tr>" + "".join(f"<th>{escape(h)}</th>" for h in head) + "</tr>" + "".join(
        "<tr>" + "".join(f"<td class='n'>{c:,}</td>" if isinstance(c, int) else f"<td>{escape(str(c))}</td>" for c in r) + "</tr>"
        for r in rows) + "</table>"


def tabs(slug, spec, data):
    p = ok(data, "profile")
    T = []

    def fac(key, title, color="#2a78d6"):
        rows = [(x["factor"], x["claims"], x["high_tier"]) for x in (p.get(key) or [])[:12]]
        if not rows:
            return ""
        return (vbar(f"{key}-c", rows, title, color, second=True) +
                "<p class='note'>Orange: claims from high-tier studies (reviews and meta-analyses, randomised trials, clinical studies).</p>" +
                table([(r[0], r[1], r[2], f"{x['high_tier_pct']}%") for r, x in zip(rows, p[key])], ["Factor", "Claims", "High-tier", "High-tier share"]))
    full = [x for x in p["series"] if x["year"] < 2026]   # the newest year is incomplete: noted, not plotted
    yrs = [(str(x["year"]), x["claims"]) for x in full]
    hi = [(str(x["year"]), x["high_tier"]) for x in full]
    T.append(("Overview", f"""<div class="card">{vline('ov', [('all claims', yrs), ('high-tier claims', hi)], 'Extracted health claims per year (complete years)', 'claims')}
<p class="note">{escape(p['series_note'])}. {escape(p['what'])}</p></div>
<div class="grid2"><div class="card"><h3>How claims relate to {escape(spec['name'].lower())}</h3>{table(sorted(p['by_relation'].items(), key=lambda kv: -kv[1]), ['Relation', 'Claims'])}</div>
<div class="card"><h3>Top risk factors at a glance</h3>{table([(x['factor'], x['claims'], f"{x['high_tier_pct']}%") for x in p['risk_factors'][:8]], ['Risk factor', 'Claims', 'High-tier share'])}</div></div>"""))
    T.append(("Risk factors", f"<div class='card'>{fac('risk_factors', 'What increases the risk')}</div>"))
    pp = fac("protective_factors", "What protects", "#1baf7a")
    if pp:
        T.append(("Protective & prevention", f"<div class='card'>{pp}</div>"))
    T.append(("Treatments", f"<div class='card'>{fac('treatments', 'Treatments named in the claims', '#2a78d6')}</div>"))
    cm = fac("causes", "Causes") + fac("mechanisms", "Mechanisms")
    if cm:
        T.append(("Causes & mechanisms", f"<div class='card'>{cm}</div>"))
    T.append(("Evidence quality", f"""<div class="grid2"><div class="card"><h3>Study tiers behind the claims</h3>{table(sorted(p['study_tiers'].items(), key=lambda kv: -kv[1]), ['Study tier', 'Claims'])}
<p class="note">{p['high_tier_share_pct']}% of all claims come from reviews, meta-analyses, randomised trials or clinical studies.</p></div>
<div class="card"><h3>Evidence strength</h3>{table(sorted(p['evidence_strength'].items(), key=lambda kv: -kv[1]), ['Strength', 'Claims'])}
<h3 style="margin-top:14px">Where the claims come from</h3>{table(sorted(p['sources'].items(), key=lambda kv: -kv[1]), ['Source type', 'Claims'])}</div></div>"""))
    st, nw = ok(data, "stance"), ok(data, "news")
    if st or nw:
        parts = []
        if st and st.get("points"):
            parts.append(vline("st", [("positive share %", [(str(x["year"]), x.get("positive_pct")) for x in st["points"]]),
                                      ("contested share %", [(str(x["year"]), x.get("contested_pct")) for x in st["points"]])],
                               "How the research frames its findings", "% of typed papers"))
        if nw and nw.get("points"):
            parts.append(vline("nw", [("articles", [(x["period"][:7], x.get("articles")) for x in nw["points"]])],
                               "News coverage per month", "articles"))
        T.append(("Research & news", "<div class='card'>" + "".join(parts) + "</div>"))
    g = ok(data, "geo")
    if g:
        lanes = []
        for k, lab in (("research_authorship", "Where it is studied (first author)"), ("research_publication", "Where it is published (journal)"),
                       ("news_coverage", "Where it is reported (news about)"), ("patent_origin", "Where it is patented")):
            rows = ((g.get(k) or {}).get("rows") or [])[:10]
            if rows:
                lanes.append(f"<div class='card'><h3>{lab}</h3>" + table([(r.get("country") or r.get("label"), r.get("papers") or r.get("articles") or r.get("patents") or 0) for r in rows], ["Country", "Count"]) + "</div>")
        if lanes:
            T.append(("Geography", "<div class='grid2'>" + "".join(lanes) + "</div><p class='note'>Four different questions; never added together.</p>"))
    tl = ok(data, "timeline")
    if tl and tl.get("months_read"):
        ms = "".join(f"<div class='m'><div class='sig'>{escape(x['month'])} · {x.get('articles', 0):,} articles · {escape(str(x.get('signal') or ''))}</div>"
                     f"<div class='h'>{escape(x.get('headline') or '')}</div>" + "".join(f"<div>• {escape(pt['text'])}</div>" for pt in x.get("points") or []) + "</div>"
                     for x in tl["months"] if x.get("available"))
        T.append(("Month by month", f"<div class='card'><h3>The arc</h3><p>{escape(tl.get('arc') or '')}</p></div><div class='card'>{ms}</div>"))
    return T


def page(slug, spec, data, text=None):
    text = text or {}
    p = ok(data, "profile")
    T = tabs(slug, spec, data)
    btn = "".join(f'<button role="tab" aria-selected="{str(i == 0).lower()}" data-t="{i}">{escape(t)}</button>' for i, (t, _) in enumerate(T))
    pan = "".join(f'<section class="panel{" on" if i == 0 else ""}" data-p="{i}">{h}</section>' for i, (_, h) in enumerate(T))
    top = max(p["risk_factors"], key=lambda x: x["claims"]) if p["risk_factors"] else {}
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(spec['name'])} · Prism disease intelligence</title><style>{CSS}</style>
<script src="https://cdn.jsdelivr.net/npm/vega@5.30.0"></script><script src="https://cdn.jsdelivr.net/npm/vega-lite@5.21.0"></script><script src="https://cdn.jsdelivr.net/npm/vega-embed@6.26.0"></script></head>
<body><div class="w"><h1>{escape(spec['name'])}</h1><p class="sub">{escape(text.get('summary') or 'Prism disease intelligence: risk factors, protection, treatments and the evidence behind them, measured from extracted health claims, research and news.')}</p>
<div class="kpis"><div class="kpi"><b>{p['claims']:,}</b><span>extracted health claims</span></div>
<div class="kpi"><b>{p['high_tier_share_pct']}%</b><span>from high-tier studies</span></div>
<div class="kpi"><b>{p['by_relation'].get('risk_factor', 0):,}</b><span>risk-factor claims</span></div>
<div class="kpi"><b>{escape(top.get('factor', '—'))}</b><span>most-claimed risk factor</span></div>
<div class="kpi"><b>{p.get('growth_late_vs_early') or '—'}×</b><span>claims, last 3 years vs first 3</span></div></div>
<div class="tabs" role="tablist">{btn}</div>{pan}
<p class="note">Source: Prism MCP. Counts are extracted claims, not papers. Built {data.get('built', '')}.</p></div>
<script>document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b));document.querySelectorAll('.panel').forEach(x=>x.classList.toggle('on',x.dataset.p===b.dataset.t));window.dispatchEvent(new Event('resize'));}});</script>
</body></html>"""


_WRITE_SYS = """You are a senior health-intelligence analyst writing the text of a public analysis page from measured data.
Use ONLY the facts given. Every number you write must appear in the facts exactly. The counts are extracted claims
from papers and articles, not papers or patients: say "claims" where you cite them. Plain, specific sentences; no
advice, no hype. British English. Return JSON: {"summary": "4-5 sentences: how large and how fast-growing the claim base is, the top risk factors, the main treatments, and how much rests on high-tier studies", "risk": "2-3 sentences on risk factors and
how much of each comes from high-tier studies", "protective": "2 sentences", "treatments": "2 sentences",
"causes": "1-2 sentences on causes and mechanisms", "evidence": "2 sentences on the evidence-quality mix and its trend"}"""


def write(spec, data):
    p = ok(data, "profile")
    F = {"disease": spec["name"], "claims": p["claims"], "high_tier_share_pct": p["high_tier_share_pct"],
         "by_relation_ranked": sorted(p["by_relation"].items(), key=lambda kv: -kv[1]), "growth_late_vs_early": p.get("growth_late_vs_early"),
         "claims_by_year": [(x["year"], x["claims"]) for x in p["series"] if x["year"] < 2026],
         "study_tiers": p["study_tiers"], "evidence_strength": p["evidence_strength"]}
    for k in ("risk_factors", "protective_factors", "treatments", "causes", "mechanisms"):
        F[k] = [(x["factor"], x["claims"], x["high_tier_pct"]) for x in (p.get(k) or [])[:8]]
    from pagewriter import write as _w
    text = _w(_WRITE_SYS, F, ("summary", "risk", "protective", "treatments", "causes", "evidence"))
    text.setdefault("summary", f"{p['claims']:,} extracted health claims name {spec['name'].lower()}; {p['high_tier_share_pct']}% come from high-tier studies.")
    return text


def readme(slug, spec, data, tab_names, text=None):
    text = text or {}
    p = ok(data, "profile")
    L = [f"# {spec['name']}: disease intelligence", "",
         f"**[Open the interactive page]({HOST}/{slug}/)** · tabs: {' · '.join(tab_names)}", "",
         f"![Risk factors for {spec['name'].lower()}, all claims vs high-tier](risk-factors.gif)", "",
         text.get("summary", ""), "",
         f"| Extracted health claims | From high-tier studies | Risk-factor claims | Treatment claims | Claims, last 3 years vs first 3 |",
         "| ---: | ---: | ---: | ---: | ---: |",
         f"| {p['claims']:,} | {p['high_tier_share_pct']}% | {p['by_relation'].get('risk_factor', 0):,} | {p['by_relation'].get('treatment', 0):,} | {p.get('growth_late_vs_early')}× |", ""]
    words = {"risk_factors": "risk", "protective_factors": "protective", "treatments": "treatments", "causes": "causes"}
    for key, title in (("risk_factors", "Risk factors"), ("protective_factors", "Protective factors"), ("treatments", "Treatments"),
                       ("causes", "Causes"), ("mechanisms", "Mechanisms")):
        rows = p.get(key) or []
        if rows:
            if text.get(words.get(key, "")):
                L += [f"## {title}", "", text[words[key]], ""]
            L += [f"<details{' open' if key == 'risk_factors' else ''}><summary><b>{title}: the numbers</b></summary>", "",
                  "| Factor | Claims | High-tier claims | High-tier share |", "| --- | ---: | ---: | ---: |"]
            L += [f"| {x['factor']} | {x['claims']:,} | {x['high_tier']:,} | {x['high_tier_pct']}% |" for x in rows[:10]]
            L += ["", "</details>", ""]
    if text.get("evidence"):
        L += ["## Evidence quality", "", text["evidence"], ""]
    L += ["<details><summary><b>Evidence quality: the numbers</b></summary>", "", "| Study tier | Claims |", "| --- | ---: |"]
    L += [f"| {k} | {v:,} |" for k, v in sorted(p["study_tiers"].items(), key=lambda kv: -kv[1])]
    L += ["", "</details>", "", "![Interactive page, first screen](screenshot.jpg)", "",
          f"How it is built: `research.disease` (the profile), plus `research.stance_trends`, `news.trends`, "
          f"`research.geography`, `analysis.history` + `analysis.scenarios` and `analysis.timeline` for the research, "
          f"news, geography and month-by-month tabs. {p['what']}", ""]
    open(os.path.join(OUT, slug, "README.md"), "w").write("\n".join(L) + "\n")


def build(slug, refresh=False):
    import time
    from gifs import bars_gif
    spec = DISEASES[slug]
    data = collect(slug, spec, refresh)
    data["built"] = time.strftime("%Y-%m-%d")
    p = ok(data, "profile")
    d = os.path.join(OUT, slug)
    os.makedirs(os.path.join(d, "page"), exist_ok=True)
    rows = [(x["factor"], x["claims"]) for x in p["risk_factors"][:10]]
    bars_gif(rows, f"{spec['name']}: what increases the risk", os.path.join(d, "risk-factors.gif"),
             subtitle="Extracted health claims per risk factor; orange = from high-tier studies",
             second=[(x["factor"], x["high_tier"]) for x in p["risk_factors"][:10]], second_label="high-tier studies")
    text = write(spec, data)
    json.dump(text, open(os.path.join(d, "writeup.json"), "w"), ensure_ascii=False, indent=1)
    html = page(slug, spec, data, text)
    open(os.path.join(d, "page", "index.html"), "w").write(html)
    names = [t for t, _ in tabs(slug, spec, data)]
    readme(slug, spec, data, names, text)
    shot(os.path.join(d, "page", "index.html"), os.path.join(d, "screenshot.jpg"))
    print(f"{slug}: tabs {names}", flush=True)
    return names


def shot(html, jpg):
    import subprocess
    from PIL import Image
    chrome = os.path.expanduser("~/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome")
    png = jpg[:-4] + ".png"
    subprocess.run([chrome, "--headless=new", "--no-sandbox", "--hide-scrollbars", "--virtual-time-budget=15000",
                    "--blink-settings=preferredColorScheme=1", f"--screenshot={png}", "--window-size=1200,1250",
                    "file://" + html], capture_output=True, timeout=120)
    Image.open(png).convert("RGB").save(jpg, quality=76, optimize=True)
    os.remove(png)


def index():
    L = ["# Disease intelligence", "",
         "Tabbed analytical pages, one per disease: risk factors, protective factors, treatments, causes and mechanisms, "
         "each counted with the share from high-tier studies; the evidence-quality mix; and, from the research and news "
         "index, how the research frames its findings, news coverage, where the disease is studied vs reported, and a "
         "month-by-month reading of the year.", "", "| Disease | Claims | High-tier share | Interactive page |", "| --- | ---: | ---: | --- |"]
    for slug, spec in DISEASES.items():
        f = os.path.join(OUT, slug, "data.json")
        if os.path.exists(f):
            p = ok(json.load(open(f)), "profile")
            L.append(f"| [{spec['name']}]({slug}/README.md) | {p['claims']:,} | {p['high_tier_share_pct']}% | [open]({HOST}/{slug}/) |")
    open(os.path.join(OUT, "README.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--refresh", action="store_true")
    a = ap.parse_args()
    for slug in (a.only.split(",") if a.only else DISEASES):
        build(slug, a.refresh)
    index()
