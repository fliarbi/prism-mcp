"""Topic intelligence pages: one tabbed analytical page per topic, across crime, infrastructure, business, finance,
energy, defence, technology and more, plus a written GitHub page and an animated GIF for each.

Tabs (each only when its data came back): Overview · Areas & themes · Places · People & organisations ·
Causes & impacts · Sections (two drill-downs) · Research & outlook · Month by month.

The GitHub page carries a written analysis: a summary and one paragraph per tab, written by the model from that
page's own data only; any sentence with a number not present in the data is removed (the number gate), and a
template sentence stands in when nothing survives.

    python3 showcase/topic_pages.py [--only cybercrime,...] [--workers 3] [--write-only]
Writes docs/topics/<slug>/{README.md, data.json, trend.gif, screenshot.jpg, page/index.html} and docs/topics/README.md.
"""
import argparse
import json
import os
import shutil
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
from disease_pages import CSS, vbar, vline, table  # noqa: E402

OUT = os.path.join(ROOT, "docs", "topics")
HOST = "https://fliarbi.com/demo/docs/prism-dashboards-3bb43e4c/topics"
ASSETS = os.path.join(HERE, "assets")

# slug: (title, domain, news term, two sections to drill into, research phrase, research claim or "")
TOPICS = {
    "cybercrime": ("Cybercrime", "Crime & public safety", "cybercrime", ["digital arrest", "upi"], "cybercrime", ""),
    "drug-trafficking": ("Drug trafficking", "Crime & public safety", "drug trafficking", ["border", "cartel"], "drug trafficking", ""),
    "road-accidents": ("Road accidents", "Crime & public safety", "road accident", ["drunk driving", "highway"], "road traffic accidents",
                       "Drunk driving increases the risk of road traffic accidents"),
    "metro-rail": ("Metro rail", "Infrastructure", "metro rail", ["delay", "fare"], "metro rail", ""),
    "urban-flooding": ("Urban flooding", "Infrastructure", "urban flooding", ["drainage", "monsoon"], "urban flooding",
                       "Impervious surfaces increase urban flooding"),
    "highways": ("Highways and expressways", "Infrastructure", "expressway", ["toll", "accident"], "highway infrastructure", ""),
    "data-centres": ("Data centres", "Infrastructure", "data center", ["power", "artificial intelligence"], "data centers",
                     "Data centers increase electricity demand"),
    "startup-funding": ("Startup funding", "Business", "startup funding", ["layoffs", "artificial intelligence"], "venture capital", ""),
    "quick-commerce": ("Quick commerce", "Business", "quick commerce", ["dark store", "zepto"], "quick commerce", ""),
    "electric-vehicles": ("Electric vehicles", "Business", "electric vehicle", ["battery", "subsidy"], "electric vehicles",
                          "Purchase subsidies increase electric vehicle adoption"),
    "semiconductors": ("Semiconductors", "Business", "semiconductor", ["india", "tariff"], "semiconductor manufacturing", ""),
    "inflation": ("Inflation", "Finance", "inflation", ["food prices", "interest rate"], "inflation",
                  "Interest rate increases reduce inflation"),
    "gold-price": ("Gold price", "Finance", "gold price", ["central bank", "rupee"], "gold price", ""),
    "bitcoin": ("Bitcoin", "Finance", "bitcoin", ["etf", "regulation"], "bitcoin", ""),
    "upi-payments": ("UPI and digital payments", "Finance", "upi", ["fraud", "international"], "digital payments", ""),
    "ipo-market": ("IPO market", "Finance", "ipo", ["sme", "listing"], "initial public offerings", ""),
    "solar-power": ("Solar power", "Energy & climate", "solar power", ["rooftop", "manufacturing"], "solar power",
                    "Solar power reduces electricity costs"),
    "heatwaves": ("Heatwaves", "Energy & climate", "heatwave", ["power demand", "deaths"], "heatwave",
                  "Heatwaves increase mortality"),
    "air-pollution": ("Air pollution", "Environment", "air pollution", ["stubble burning", "aqi"], "air pollution",
                      "Air pollution increases mortality"),
    "drone-warfare": ("Drone warfare", "Defence & geopolitics", "drone warfare", ["ukraine", "india"], "drone warfare", ""),
    "red-sea-shipping": ("Red Sea shipping", "Supply chain & trade", "red sea", ["houthi", "freight"], "maritime shipping", ""),
    "ai-regulation": ("AI regulation", "Technology & policy", "ai regulation", ["eu ai act", "copyright"], "artificial intelligence regulation", ""),
    "data-privacy": ("Data privacy", "Technology & policy", "data privacy", ["breach", "consent"], "data privacy", ""),
    "monsoon-agriculture": ("Monsoon and crops", "Agriculture", "monsoon", ["kharif", "rainfall deficit"], "monsoon rainfall",
                            "Monsoon rainfall deficits reduce crop yields"),
    "layoffs": ("Layoffs", "Education & labour", "layoffs", ["tech", "artificial intelligence"], "layoffs", ""),
}


def collect(slug, refresh=False):
    import prism_mcp as m
    title, dom, term, drills, phrase, claim = TOPICS[slug]
    path = os.path.join(OUT, slug, "data.json")
    data = json.load(open(path)) if os.path.exists(path) and not refresh else {}

    def get(key, tool, **args):
        d = data.get(key) or {}
        failed_panels = any(v == "panel failed" for v in (((d.get("data") or {}).get("panels_empty")) or {}).values())
        if d.get("ok") and not failed_panels:
            return
        try:
            data[key] = m.REGISTRY[tool]["fn"](**args)
        except Exception as e:
            data[key] = {"ok": False, "error": {"reason": str(e)}}
        print(f"  {slug} {key}: {data[key].get('ok')}", flush=True)
    get("overview", "prism_overview", term=term, since="2024-06-01")
    get("activities", "news_activities", term=term)
    get("states", "news_geography", term=term, level="state", limit=25)
    get("factors", "news_factors", topic=term)
    for i, d in enumerate(drills):
        get(f"drill{i}", "news_drill", term=term, scope=d)
    get("stance", "stance_trends", term=phrase)
    get("history", "historical_analysis", subject_phrases=[phrase], query_seconds=30)
    hid = ((data.get("history") or {}).get("data") or {}).get("history_id")
    if hid:
        get("scenarios", "trend_scenarios", history_id=hid, horizon=3)
    if claim:
        get("geo", "global_comparison", claim=claim)
    get("timeline", "deep_timeline", term=term, months=12)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(data, open(path, "w"), ensure_ascii=False, indent=1, default=str)
    return data


def D(data, key):
    d = data.get(key) or {}
    return d.get("data") if d.get("ok") else None


def fmt(x):
    return f"{x:,}" if isinstance(x, int) else str(x)


# ───────────────────────────────────────── facts for the writer ─────────────────────────────────────────
def _prev_month(to):
    """the window's end is exclusive: name the last month it covers"""
    if not to or len(to) < 7:
        return to
    y, m = int(to[:4]), int(to[5:7]) - 1
    if m == 0:
        y, m = y - 1, 12
    return f"{y:04d}-{m:02d}"


def facts(slug, data):
    title, dom, term, drills, phrase, claim = TOPICS[slug]
    F = {"topic": title, "domain": dom, "news_term": term}
    ov = D(data, "overview") or {}
    tr, se = ov.get("trends") or {}, ov.get("sentiment") or {}
    t = tr.get("trend") or {}
    F["overview"] = {"articles": tr.get("total"), "high_priority_stories": tr.get("critical_total"),
                     "high_priority_means": "stories in Prism's top priority bands (geopolitics, disasters, regulation, major incidents); NOT a measure of tone",
                     "direction": t.get("direction"), "last_third_vs_first_third": t.get("late_vs_early"),
                     "peak_month": (t.get("peak_period") or "")[:7],
                     "peak_articles": t.get("peak"), "window": f"{tr.get('from', '')[:7]} to {_prev_month(tr.get('to', ''))}",
                     "neg_per_pos": (se.get("totals") or {}).get("ratio"), "all_news_neg_per_pos": se.get("corpus_baseline_ratio"),
                     "tone_reading": se.get("reading")}
    th = ov.get("themes") or {}
    F["themes"] = [r["label"] for r in ((th.get("subcategories") or {}).get("rows") or [])[:6]]
    F["top_tags"] = [(r["label"], r["articles"]) for r in sorted(((th.get("tags") or {}).get("rows") or []), key=lambda r: -r["articles"])[:8]]
    ac = D(data, "activities") or {}
    F["areas_of_activity"] = sorted([(r["area"], r["articles"]) for r in ((ac.get("areas_of_activity") or {}).get("rows") or [])[:8]], key=lambda x: -x[1])[:6]
    geo = ov.get("geography") or {}
    F["countries"] = [(r["label"], r["articles"], r.get("lift")) for r in (geo.get("rows") or [])[:6]]
    st = D(data, "states") or {}
    F["states"] = [(r["label"], r["articles"], r.get("lift")) for r in (st.get("rows") or [])[:6]]
    en = ov.get("entities") or {}
    F["organisations"] = [r["label"] for r in ((en.get("organizations") or {}).get("rows") or [])[:6]]
    F["people"] = [r["label"] for r in ((en.get("people") or {}).get("rows") or [])[:6]]
    fa = D(data, "factors") or {}
    F["causes"] = [x["factor"] for x in (fa.get("causes") or [])[:6]]
    F["impacts"] = [x["factor"] for x in (fa.get("impacts") or [])[:6]]
    F["sections"] = []
    for i, d in enumerate(drills):
        dd = D(data, f"drill{i}")
        if dd:
            F["sections"].append({"section": d, "articles": dd["section"]["articles"], "share_of_topic_pct": dd["section"]["share_of_entity_pct"],
                                  "late_vs_early": dd["section"]["late_vs_early"], "neg_per_pos": dd["tone"]["section_neg_per_pos"],
                                  "topic_neg_per_pos": dd["tone"]["entity_neg_per_pos"]})
    sn = D(data, "stance") or {}
    fs = sn.get("framing_shift") or {}
    F["research"] = {"typed_papers": (sn.get("totals") or {}).get("papers") if isinstance(sn.get("totals"), dict) else None,
                     "framing_shift_points": fs.get("delta_pct_points"), "framing_reading": fs.get("reading")}
    sc = D(data, "scenarios") or {}
    F["outlook"] = [(x.get("year"), x.get("central"), x.get("lower_sensitivity"), x.get("upper_sensitivity")) for x in (sc.get("scenarios") or [])[:3]]
    tl = D(data, "timeline") or {}
    F["timeline_arc"] = tl.get("arc")
    F["turning_points"] = [(x.get("month"), x.get("why")) for x in (tl.get("turning_points") or [])[:3]]
    return F


_WRITE_SYS = """You are a senior intelligence analyst writing the text of a public analysis page from measured data.
Use ONLY the facts given. Every number you write must appear in the facts exactly. Plain, specific sentences; no hype,
no generic statements, no advice. Do not describe the data source. Write in British English.
Return JSON: {"summary": "4-5 sentences: what the topic's coverage shows, its direction, tone and what drives it",
"overview": "2-3 sentences", "areas": "2 sentences on the areas of activity, themes and top tags",
"places": "2 sentences on where coverage is placed (countries and Indian states)", "people": "1-2 sentences",
"causes": "2 sentences on causes and impacts", "sections": "2-3 sentences comparing the two sections",
"research": "2 sentences on research framing and the outlook, or empty if no research facts",
"timeline": "2 sentences on the arc and turning points, or empty if none"}"""


def write(slug, data):
    F = facts(slug, data)
    from pagewriter import write as _w
    text = _w(_WRITE_SYS, F, ("summary", "overview", "areas", "places", "people", "causes", "sections", "research", "timeline"))
    ov = F["overview"]
    text.setdefault("summary", f"{F['topic']} drew {fmt(ov.get('articles'))} articles from {ov.get('window')}, "
                               f"{ov.get('direction') or 'with no clear direction'}; coverage runs {ov.get('neg_per_pos')} negative "
                               f"articles per positive one against {ov.get('all_news_neg_per_pos')} for all news.")
    return F, text


# ─────────────────────────────────────────── the HTML page ───────────────────────────────────────────
def mapjs(id_, url, key, values, title, w=700, h=380, proj="equalEarth"):
    spec = {"$schema": "https://vega.github.io/schema/vega-lite/v5.json", "width": w, "height": h,
            "title": {"text": title, "anchor": "start", "fontSize": 14},
            "data": {"url": url, "format": {"type": "json", "property": "features"}},
            "transform": [{"lookup": key, "from": {"data": {"values": values}, "key": "k", "fields": ["v"]}}],
            "projection": {"type": proj}, "mark": {"type": "geoshape", "stroke": "#fff", "strokeWidth": 0.4},
            "encoding": {"color": {"field": "v", "type": "quantitative", "title": "articles", "scale": {"scheme": "blues"}},
                         "tooltip": [{"field": "properties.name", "title": "place"}, {"field": "v", "title": "articles"}]},
            "config": {"background": None, "view": {"stroke": None}}}
    return f'<div class="chart" id="{id_}"></div><script>vegaEmbed("#{id_}",{json.dumps(spec)},{{actions:false}});</script>'


def tabs(slug, data, text):
    import pycountry
    title, dom, term, drills, phrase, claim = TOPICS[slug]
    ov = D(data, "overview") or {}
    T = []
    tr, se = ov.get("trends") or {}, ov.get("sentiment") or {}
    pts = [x for x in tr.get("points") or [] if not x.get("partial_period")]
    if pts:
        h = vline("tr", [("all coverage", [(x["period"][:7], x["articles"]) for x in pts]),
                         ("high-priority stories", [(x["period"][:7], x["critical"]) for x in pts])], "Monthly coverage", "articles")
        sp = se.get("points") or []
        h2 = vline("tn", [("negative", [(x["period"][:7], x.get("negative")) for x in sp]),
                          ("positive", [(x["period"][:7], x.get("positive")) for x in sp])], "Tone of the coverage", "articles") if sp else ""
        T.append(("Overview", f"<div class='card'><p>{escape(text.get('overview', ''))}</p>{h}{h2}</div>"))
    ac = D(data, "activities") or {}
    th = ov.get("themes") or {}
    areas = ((ac.get("areas_of_activity") or {}).get("rows") or [])[:10]
    if areas or th:
        parts = [f"<p>{escape(text.get('areas', ''))}</p>"]
        if areas:
            parts.append(vbar("ar", [(r["area"], r["articles"]) for r in areas], "Areas of activity (industry taxonomy)", "#1baf7a"))
        subs = ((th.get("subcategories") or {}).get("rows") or [])[:10]
        if subs:
            parts.append(vbar("th", [(r["label"], r["articles"]) for r in subs], "Top themes", "#eda100"))
        tags = sorted(((th.get("tags") or {}).get("rows") or []), key=lambda r: -r["articles"])[:12]
        if tags:
            parts.append("<h3>Top tags (what the themes are built from)</h3>" + table([(r["label"], r["articles"]) for r in tags], ["Tag", "Articles"]))
        T.append(("Areas & themes", "<div class='card'>" + "".join(parts) + "</div>"))
    geo, st = ov.get("geography") or {}, D(data, "states") or {}
    if geo.get("rows") or (st or {}).get("rows"):
        vals = []
        for r in geo.get("rows") or []:
            try:
                vals.append({"k": pycountry.countries.lookup(r["label"]).alpha_3, "v": r["articles"]})
            except LookupError:
                pass
        h = f"<p>{escape(text.get('places', ''))}</p>"
        if vals:
            h += mapjs("wm", "world_india_official.geojson", "properties.iso3", vals, "Countries the coverage is about")
        srows = [r for r in (st or {}).get("rows") or []]
        if srows:
            h += mapjs("im", "india_states_official.geojson", "properties.key", [{"k": r["label"], "v": r["articles"]} for r in srows],
                       "Indian states the coverage is about (other places the state level returns are ignored)", w=520, h=560, proj="mercator")
        h += table([(r["label"].title(), r["articles"], f"{r.get('lift')}×") for r in (geo.get("rows") or [])[:10]], ["Country", "Articles", "Lift"])
        T.append(("Places", "<div class='card'>" + h + "</div>"))
    en = ov.get("entities") or {}
    org = ((en.get("organizations") or {}).get("rows") or [])[:10]
    ppl = ((en.get("people") or {}).get("rows") or [])[:10]
    if org or ppl:
        T.append(("People & organisations", f"<div class='card'><p>{escape(text.get('people', ''))}</p><div class='grid2'>"
                  f"<div>{table([(r['label'], r['articles']) for r in org], ['Organisation', 'Articles'])}</div>"
                  f"<div>{table([(r['label'], r['articles']) for r in ppl], ['Person', 'Articles'])}</div></div>"
                  "<p class='note'>Machine-assigned entity labels; check the articles before inferring affiliations.</p></div>"))
    fa = D(data, "factors")
    if fa:
        rows = lambda xs: "".join(f"<tr><td><b>{escape(x['factor'])}</b></td><td>“{escape(x['quote'][:220])}”</td><td>{escape(x.get('date') or '')}</td><td>{escape(x.get('publisher') or '')}</td></tr>" for x in xs)
        T.append(("Causes & impacts", f"<div class='card'><p>{escape(text.get('causes', ''))}</p><h3>Causes</h3><table><tr><th>Cause</th><th>Quote</th><th>Date</th><th>Publisher</th></tr>{rows(fa.get('causes') or [])}</table>"
                  f"<h3>Impacts</h3><table><tr><th>Impact</th><th>Quote</th><th>Date</th><th>Publisher</th></tr>{rows(fa.get('impacts') or [])}</table>"
                  "<p class='note'>Every factor is quoted verbatim from a high-priority report's opening; unverifiable ones were discarded.</p></div>"))
    secs = [(d, D(data, f"drill{i}")) for i, d in enumerate(drills)]
    secs = [(d, x) for d, x in secs if x]
    if secs:
        h = f"<p>{escape(text.get('sections', ''))}</p>" + vline("dr", [(f"{d}: % of {term} coverage", [(p['period'][:7], p.get('section_share_pct') or 0) for p in x['points']]) for d, x in secs],
                                                                  "Sections inside the topic, share of its monthly coverage", "%")
        for d, x in secs:
            h += (f"<h3>{escape(term)} → {escape(d)}</h3><p>{fmt(x['section']['articles'])} articles ({x['section']['share_of_entity_pct']}% of the topic), "
                  f"{x['section']['late_vs_early']}× late vs early; {x['tone']['section_neg_per_pos']} negative per positive vs {x['tone']['entity_neg_per_pos']} for the topic.</p>"
                  + table([(e["date"], e["reports_that_day"], e["opening"][:160]) for e in (x.get("events") or [])[:5]], ["Day", "Outlets", "Reported"]))
        T.append(("Sections", "<div class='card'>" + h + "</div>"))
    sn, sc = D(data, "stance"), D(data, "scenarios")
    if sn or sc:
        h = f"<p>{escape(text.get('research', ''))}</p>"
        if sn and sn.get("points"):
            h += vline("st", [("positive %", [(str(x["year"]), x.get("positive_pct")) for x in sn["points"]]),
                              ("contested %", [(str(x["year"]), x.get("contested_pct")) for x in sn["points"]])], "How the research frames its findings", "% of typed papers")
        if sc and sc.get("scenarios"):
            h += table([(x.get("year"), x.get("central"), x.get("lower_sensitivity"), x.get("upper_sensitivity")) for x in sc["scenarios"]],
                       ["Year", "Central (papers)", "Lower", "Upper"]) + "<p class='note'>Backtested projection of the research series; bounds are sensitivity, not probability.</p>"
        T.append(("Research & outlook", "<div class='card'>" + h + "</div>"))
    tl = D(data, "timeline")
    if tl and tl.get("months_read"):
        ms = "".join(f"<div class='m'><div class='sig'>{escape(x['month'])} · {x.get('articles', 0):,} articles · {escape(str(x.get('signal') or ''))}</div>"
                     f"<div class='h'>{escape(x.get('headline') or '')}</div>" + "".join(f"<div>• {escape(p['text'])}</div>" for p in x.get("points") or []) + "</div>"
                     for x in tl["months"] if x.get("available"))
        T.append(("Month by month", f"<div class='card'><h3>The arc</h3><p>{escape(tl.get('arc') or '')}</p><p>{escape(text.get('timeline', ''))}</p></div><div class='card'>{ms}</div>"))
    return T


def page(slug, data, text):
    title, dom, term = TOPICS[slug][:3]
    ov = D(data, "overview") or {}
    tr, se = ov.get("trends") or {}, ov.get("sentiment") or {}
    t = tr.get("trend") or {}
    T = tabs(slug, data, text)
    btn = "".join(f'<button role="tab" aria-selected="{str(i == 0).lower()}" data-t="{i}">{escape(n)}</button>' for i, (n, _) in enumerate(T))
    pan = "".join(f'<section class="panel{" on" if i == 0 else ""}" data-p="{i}">{h}</section>' for i, (_, h) in enumerate(T))
    k = [(fmt(tr.get("total")), "articles, " + escape(f"{tr.get('from', '')[:7]} to {_prev_month(tr.get('to', ''))}")),
         (escape(str(t.get("direction") or "—")), f"last third vs first: {t.get('late_vs_early')}×"),
         (escape(str((t.get('peak_period') or '')[:7])), f"peak month ({fmt(t.get('peak'))} articles)"),
         (str((se.get("totals") or {}).get("ratio")), f"negative per positive (all news {se.get('corpus_baseline_ratio')})"),
         (fmt(tr.get("critical_total")), "high-priority stories")]
    kp = "".join(f"<div class='kpi'><b>{a}</b><span>{b}</span></div>" for a, b in k)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(title)} · Prism topic intelligence</title><style>{CSS}</style>
<script src="https://cdn.jsdelivr.net/npm/vega@5.30.0"></script><script src="https://cdn.jsdelivr.net/npm/vega-lite@5.21.0"></script><script src="https://cdn.jsdelivr.net/npm/vega-embed@6.26.0"></script></head>
<body><div class="w"><p class="note">{escape(dom)} · Prism topic intelligence</p><h1>{escape(title)}</h1><p class="sub">{escape(text.get('summary', ''))}</p>
<div class="kpis">{kp}</div><div class="tabs" role="tablist">{btn}</div>{pan}
<p class="note">Source: Prism MCP. Windows are stated on each panel; the newest incomplete month is excluded. Built {time.strftime('%Y-%m-%d')}.</p></div>
<script>document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b));document.querySelectorAll('.panel').forEach(x=>x.classList.toggle('on',x.dataset.p===b.dataset.t));window.dispatchEvent(new Event('resize'));}});</script>
</body></html>""", [n for n, _ in T]


def readme(slug, data, F, text, tab_names):
    title, dom, term, drills = TOPICS[slug][:4]
    ov = F["overview"]
    L = [f"# {title}", "", f"*{dom} · Prism topic intelligence* · **[Open the interactive page]({HOST}/{slug}/)** "
         f"(tabs: {' · '.join(tab_names)})", "", f"![{title}: monthly coverage, animated](trend.gif)", "",
         text.get("summary", ""), "",
         "| Articles | Direction (last third vs first) | Peak month | Negative per positive | High-priority stories |", "| ---: | --- | --- | ---: | ---: |",
         f"| {fmt(ov.get('articles'))} ({ov.get('window')}) | {ov.get('direction')} ({ov.get('last_third_vs_first_third')}×) | {ov.get('peak_month')} "
         f"({fmt(ov.get('peak_articles'))}) | {ov.get('neg_per_pos')} (all news {ov.get('all_news_neg_per_pos')}) | {fmt(ov.get('high_priority_stories'))} |", ""]
    sec = [("Coverage over time", "overview"), ("Areas of activity and themes", "areas"), ("Where it is reported", "places"),
           ("People and organisations", "people"), ("Causes and impacts", "causes"), ("Sections inside the topic", "sections"),
           ("Research and outlook", "research"), ("Month by month", "timeline")]
    for h, k in sec:
        has_table = (k == "areas" and (F["areas_of_activity"] or F["top_tags"])) or (k == "places" and F["countries"]) or \
                    (k == "causes" and (F["causes"] or F["impacts"])) or (k == "sections" and F["sections"])
        if not text.get(k) and not has_table:
            continue
        L += [f"## {h}", ""] + ([text[k], ""] if text.get(k) else [])
        if k == "areas" and (F["areas_of_activity"] or F["top_tags"]):
            if F["areas_of_activity"]:
                L += ["| Area of activity | Articles |", "| --- | ---: |"] + [f"| {a} | {fmt(n)} |" for a, n in F["areas_of_activity"]] + [""]
            if F["top_tags"]:
                L += ["**Top tags (what the themes are built from):** " + ", ".join(f"{a} ({fmt(n)})" for a, n in F["top_tags"]), ""]
        if k == "places" and F["countries"]:
            L += ["| Country | Articles | Lift | | Indian state | Articles | Lift |", "| --- | ---: | ---: | --- | --- | ---: | ---: |"]
            for i in range(max(len(F["countries"]), len(F["states"]))):
                c = F["countries"][i] if i < len(F["countries"]) else ("", "", "")
                s_ = F["states"][i] if i < len(F["states"]) else ("", "", "")
                L.append(f"| {str(c[0]).title()} | {fmt(c[1])} | {c[2] or ''}{'×' if c[2] else ''} | | {str(s_[0]).title()} | {fmt(s_[1])} | {s_[2] or ''}{'×' if s_[2] else ''} |")
            L.append("")
        if k == "causes" and (F["causes"] or F["impacts"]):
            L += [f"**Causes named in the coverage:** {', '.join(F['causes'])}", "", f"**Impacts:** {', '.join(F['impacts'])}", ""]
        if k == "sections" and F["sections"]:
            L += ["| Section | Articles | Share of the topic | Late vs early | Negative per positive |", "| --- | ---: | ---: | ---: | ---: |"]
            L += [f"| {term} → {x['section']} | {fmt(x['articles'])} | {x['share_of_topic_pct']}% | {x['late_vs_early']}× | {x['neg_per_pos']} (topic {x['topic_neg_per_pos']}) |" for x in F["sections"]] + [""]
        if k == "timeline" and F["turning_points"]:
            L += [f"- **{m}:** {w}" for m, w in F["turning_points"]] + [""]
    L += ["![The interactive page](screenshot.jpg)", "",
          "**How this page is built.** One Prism call per tab: `news.overview` (coverage, tone, themes, tags, places, people), "
          "`news.activities` (areas of activity), `news.geography` at state level, `news.factors` (causes and impacts, each quoted "
          "verbatim), `news.drill` for each section, `research.stance_trends` and `analysis.history` + `analysis.scenarios` for "
          "research and outlook, and `analysis.timeline` for the month-by-month reading. The text above was written from this "
          "page's data only; sentences with numbers not in the data were removed. Data: [data.json](data.json).", "",
          f"Try it: `prism entity \"{term}\"` · `prism call news.drill term='{term}' scope='{drills[0]}'` · `prism call analysis.timeline term='{term}'`", ""]
    open(os.path.join(OUT, slug, "README.md"), "w").write("\n".join(L) + "\n")


import threading
_GIF_LOCK = threading.Lock()   # matplotlib is not thread-safe


def gif(slug, data):
    with _GIF_LOCK:
        _gif(slug, data)


def _gif(slug, data):
    from gifs import lines_gif
    title = TOPICS[slug][0]
    tr = (D(data, "overview") or {}).get("trends") or {}
    pts = [x for x in tr.get("points") or [] if not x.get("partial_period")]
    if not pts:
        return
    lines_gif([("all coverage", [(x["period"][2:7].replace("-", "/"), x["articles"]) for x in pts]),
               ("high-priority stories", [(x["period"][2:7].replace("-", "/"), x["critical"]) for x in pts])],
              title, os.path.join(OUT, slug, "trend.gif"), subtitle="News coverage per month, June 2024 to May 2026")


def build(slug, refresh=False, write_only=False):
    from disease_pages import shot
    data = json.load(open(os.path.join(OUT, slug, "data.json"))) if write_only else collect(slug, refresh)
    if not D(data, "overview"):
        print(f"{slug}: no overview, skipped", flush=True)
        return None
    F, text = write(slug, data)
    d = os.path.join(OUT, slug)
    os.makedirs(os.path.join(d, "page"), exist_ok=True)
    for f in ("world_india_official.geojson", "india_states_official.geojson"):
        shutil.copy(os.path.join(ASSETS, f), os.path.join(d, "page", f))
    html, names = page(slug, data, text)
    open(os.path.join(d, "page", "index.html"), "w").write(html)
    json.dump({"facts": F, "text": text}, open(os.path.join(d, "writeup.json"), "w"), ensure_ascii=False, indent=1, default=str)
    gif(slug, data)
    readme(slug, data, F, text, names)
    shot(os.path.join(d, "page", "index.html"), os.path.join(d, "screenshot.jpg"))
    print(f"{slug}: tabs {names}", flush=True)
    return names


def index():
    by = {}
    for slug, (title, dom, *_rest) in TOPICS.items():
        if os.path.exists(os.path.join(OUT, slug, "README.md")):
            by.setdefault(dom, []).append((slug, title))
    L = ["# Topic intelligence", "", "Topic intelligence reports, one per topic, built from MCP calls: coverage and tone, areas of activity and the top tags behind "
         "the themes, places on world and India maps, people and organisations, causes and impacts quoted from the reports, two "
         "sections drilled into, themes over five years, three reader views chosen by domain, the nine research exploration "
         "methods with in-depth readings, and a month-by-month reading. Each page has a written analysis.", ""]
    for dom, items in by.items():
        L += [f"## {dom}", "", "| Topic | GitHub page | Interactive page |", "| --- | --- | --- |"]
        L += [f"| {t} | [analysis]({s}/README.md) | [open]({HOST}/{s}/) |" for s, t in items] + [""]
    open(os.path.join(OUT, "README.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--write-only", action="store_true")
    a = ap.parse_args()
    slugs = a.only.split(",") if a.only else list(TOPICS)
    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(lambda s: build(s, a.refresh, a.write_only), slugs))
    index()
    print("TOPICS_DONE", flush=True)
