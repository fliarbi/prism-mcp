"""Company intelligence reports, built entirely from Prism MCP calls.

Every panel comes from a tool call made over MCP (showcase/mcpcall.py), and the report ends with the list of calls it
was built from. On top of the investor signals (investor_pages.py) the report adds:

  * Themes over five years: news.themes per calendar year, 2021 to 2025, as a heatmap and a stacked share chart,
    plus an animated theme race.
  * Business lenses: product, finance, marketing, legal, leadership, partnerships and AI, each a news.drill inside
    the company's coverage: its share month by month and its weight in the mix.
  * Versus peers: the same themes for each peer (news.themes) side by side, and attention on one scale (news.compare).
  * Mix: donuts of company events by type, tone, and the peer group's share of attention.
  * Events, risks and catalysts, areas of activity and people, and the month-by-month reading.

    python3 showcase/intel_reports.py [--only nvidia,...] [--workers 2] [--write-only]
Writes docs/investors/<slug>/{README.md, data.json, writeup.json, mcp_calls.json, theme-race.gif, signals.gif,
charts/*.png, screenshot.jpg, page/index.html}.
"""
import argparse
import json
import os
import shutil
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from html import escape

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
from disease_pages import CSS, vbar, vline, table, shot  # noqa: E402
from topic_pages import fmt, _prev_month  # noqa: E402
from investor_pages import (COMPANIES, PEERS, DISCLAIMER, EVENTS_THROUGH, HOST, OUT, signals, signal_rows)  # noqa: E402
import mcpcall  # noqa: E402

YEARS = [2021, 2022, 2023, 2024, 2025]
LENSES = [("Product", "launch"), ("Finance", "earnings"), ("Marketing", "marketing"), ("Legal & regulatory", "lawsuit"),
          ("Leadership", "ceo"), ("Partnerships", "partnership"), ("AI", "artificial intelligence")]
_GIF = threading.Lock()
_SHOT = threading.Lock()  # two headless Chromes at once left the chart folders empty


def D(data, key):
    d = data.get(key) or {}
    return d.get("data") if d.get("ok") else None


def collect(slug, refresh=False):
    name, lst, term, dom, sector, group, risks, cats = COMPANIES[slug]
    path = os.path.join(OUT, slug, "data.json")
    data = json.load(open(path)) if os.path.exists(path) and not refresh else {}
    log = []

    def get(key, tool, **args):
        d = data.get(key) or {}
        bad = any(v == "panel failed" for v in (((d.get("data") or {}).get("panels_empty")) or {}).values())
        if d.get("ok") and not bad and key in (data.get("_mcp") or {}):
            log.append(data["_mcp"][key])
            return
        t0 = time.time()
        data[key] = mcpcall.call(tool, args)
        rec = {"key": key, "tool": tool, "args": args, "seconds": round(time.time() - t0, 1), "ok": bool(data[key].get("ok"))}
        data.setdefault("_mcp", {})[key] = rec
        log.append(rec)
        print(f"  {slug} {key}: {rec['ok']} {rec['seconds']}s", flush=True)
    get("overview", "prism_overview", term=term, since="2024-06-01")
    get("activities", "news_activities", term=term, domain=dom)
    for y in YEARS:
        get(f"themes_{y}", "news_themes", term=term, since=f"{y}-01-01", until=f"{y + 1}-01-01", limit=25)
    for p in PEERS[group]:
        if p != term:
            get(f"peer_themes_{p}", "news_themes", term=p, since="2024-06-01", limit=25)
    for lab, sc in LENSES:
        get(f"lens_{lab}", "news_drill", term=term, scope=sc)
    for i, s in enumerate(risks):
        get(f"risk{i}", "news_drill", term=term, scope=s)
    for i, s in enumerate(cats):
        get(f"cat{i}", "news_drill", term=term, scope=s)
    get("peers", "compare_terms", terms=PEERS[group], since="2024-06-01")
    get("timeline", "deep_timeline", term=term, months=12)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(data, open(path, "w"), ensure_ascii=False, indent=1, default=str)
    json.dump(log, open(os.path.join(OUT, slug, "mcp_calls.json"), "w"), indent=1)
    return data


# ─────────────────────────────────────────── derived views ───────────────────────────────────────────
def theme_years(data, top=10):
    """{year: {theme: share%}} over the category theme layer, top themes by total articles across years"""
    per = {}
    for y in YEARS:
        rows = (((D(data, f"themes_{y}") or {}).get("categories")) or {}).get("rows") or []
        tot = sum(r["articles"] for r in rows) or 1
        per[y] = {r["label"]: (r["articles"], round(100 * r["articles"] / tot, 1)) for r in rows}
    totals = {}
    for y in per:
        for k, (n, _) in per[y].items():
            totals[k] = totals.get(k, 0) + n
    keep = [k for k, _ in sorted(totals.items(), key=lambda kv: -kv[1]) if k not in ("business", "news")][:top]
    return {y: {k: (per[y][k][1] if k in per[y] else None) for k in keep} for y in per}, keep


def peer_themes(data, slug, top=10):
    name, lst, term, dom, sector, group = COMPANIES[slug][:6]
    tabs = {term: ((D(data, "overview") or {}).get("themes") or {}).get("categories") or {}}
    for p in PEERS[group]:
        if p != term:
            tabs[p] = ((D(data, f"peer_themes_{p}") or {}).get("categories")) or {}
    share = {}
    for co, t in tabs.items():
        rows = t.get("rows") or []
        tot = sum(r["articles"] for r in rows) or 1
        share[co] = {r["label"]: round(100 * r["articles"] / tot, 1) for r in rows}
    allk = {}
    for co in share:
        for k, v in share[co].items():
            allk[k] = allk.get(k, 0) + v
    keep = [k for k, _ in sorted(allk.items(), key=lambda kv: -kv[1]) if k not in ("business", "news")][:top]
    return {co: {k: share[co].get(k) for k in keep} for co in share}, keep


def lenses(data):
    out = []
    for lab, sc in LENSES:
        d = D(data, f"lens_{lab}")
        if d:
            out.append({"lens": lab, "scope": sc, "articles": d["section"]["articles"], "share_pct": d["section"]["share_of_entity_pct"],
                        "late_vs_early": d["section"]["late_vs_early"], "neg_per_pos": d["tone"]["section_neg_per_pos"],
                        "points": [(p["period"][:7], p.get("section_share_pct") or 0) for p in d["points"]],
                        "top_tags": [r["label"] for r in (d.get("top_tags") or [])[:6]]})
    return out


# ─────────────────────────────────────────── charts (Vega-Lite) ───────────────────────────────────────────
def _embed(id_, spec):
    spec = {"$schema": "https://vega.github.io/schema/vega-lite/v5.json", "config": {"background": None, "view": {"stroke": None}}, **spec}
    return f'<div class="chart" id="{id_}"></div><script>vegaEmbed("#{id_}",{json.dumps(spec)},{{actions:false}});</script>'


def heatmap(id_, cells, x, y, title, xs=None, ys=None, w=640, h=None, scheme="blues"):
    ys = ys or sorted({c[y] for c in cells})
    cells = [c for c in cells if c.get("v") is not None]   # a theme not in that column's top list is left blank
    return _embed(id_, {"width": w, "height": h or 26 * len(ys), "title": {"text": title, "anchor": "start", "fontSize": 14},
                        "data": {"values": cells},
                        "encoding": {"x": {"field": x, "type": "ordinal", "title": None, "sort": xs, "axis": {"labelAngle": 0}},
                                     "y": {"field": y, "type": "ordinal", "title": None, "sort": ys}},
                        "layer": [{"mark": {"type": "rect", "cornerRadius": 3},
                                   "encoding": {"color": {"field": "v", "type": "quantitative", "title": "% of themed coverage",
                                                          "scale": {"scheme": scheme}}, "tooltip": [{"field": x}, {"field": y}, {"field": "v", "title": "%"}]}},
                                  {"mark": {"type": "text", "fontSize": 10.5},
                                   "encoding": {"text": {"field": "v", "type": "quantitative", "format": ".1f"},
                                                "color": {"condition": {"test": "datum.v > 12", "value": "white"}, "value": "#14161a"}}}]})


def stacked(id_, cells, title):
    cells = [dict(c, v=c.get("v") or 0) for c in cells]
    return _embed(id_, {"width": 640, "height": 300, "title": {"text": title, "anchor": "start", "fontSize": 14}, "data": {"values": cells},
                        "mark": {"type": "area", "interpolate": "monotone"},
                        "encoding": {"x": {"field": "year", "type": "ordinal", "title": None, "axis": {"labelAngle": 0}},
                                     "y": {"field": "v", "type": "quantitative", "stack": "normalize", "title": "share of the top themes", "axis": {"format": "%"}},
                                     "color": {"field": "theme", "type": "nominal", "scale": {"scheme": "tableau10"}, "title": None},
                                     "tooltip": [{"field": "year"}, {"field": "theme"}, {"field": "v", "title": "%"}]}})


def donut(id_, parts, title):
    vals = [{"k": k, "v": v} for k, v in parts if v]
    return _embed(id_, {"width": 260, "height": 260, "title": {"text": title, "anchor": "start", "fontSize": 13},
                        "data": {"values": vals}, "mark": {"type": "arc", "innerRadius": 62, "stroke": "#fff", "strokeWidth": 1.5},
                        "encoding": {"theta": {"field": "v", "type": "quantitative", "stack": True},
                                     "color": {"field": "k", "type": "nominal", "scale": {"scheme": "tableau10"}, "title": None},
                                     "tooltip": [{"field": "k"}, {"field": "v"}]}})


# ─────────────────────────────────────────── text ───────────────────────────────────────────
_WRITE_SYS = """You are a senior equity-research analyst writing a company intelligence report from measured news and
company-event data, for investors and stock buyers. Frame everything as inputs to a decision (what is building, what is
fading, how the story has changed, how it differs from rivals, what to watch), NEVER as a recommendation: no buy, sell,
hold, target price or "investors should". News attention, themes and tone are not price signals. 'High-priority stories'
means the top priority bands, not tone. Theme shares are shares of the company's themed coverage within each year.
Return JSON: {"summary": "5-6 sentences", "signals": "3 sentences", "themes_time": "3-4 sentences on how the themes moved from 2021 to 2025: name each theme with its share in the first and last year exactly as given (e.g. 'gaming fell from 12.4% in 2021 to 2.4% in 2025'); do not compute differences",
"lenses": "3 sentences comparing the business lenses (product, finance, marketing, legal, leadership, partnerships, AI)",
"peers": "3 sentences on how its themes and attention differ from its peers", "mix": "2 sentences on the event, tone and attention mix",
"events": "2-3 sentences", "risks": "2 sentences", "catalysts": "2 sentences", "areas": "2 sentences", "timeline": "2-3 sentences",
"watch": ["4 to 6 short items to watch next"]}"""


def write(slug, data, S, TY, keep, PT, pkeep, LZ):
    from pagewriter import write as _w
    name, lst, term, dom, sector = COMPANIES[slug][:5]
    ov = D(data, "overview") or {}
    tr = ov.get("trends") or {}
    en = ov.get("entities") or {}
    ac = D(data, "activities") or {}
    tl = D(data, "timeline") or {}
    F = {"company": name, "listing": lst, "sector": sector,
         "window": f"{tr.get('from', '')[:7]} to {_prev_month(tr.get('to', ''))}", "articles": tr.get("total"),
         "high_priority_stories": tr.get("critical_total"), "signals": S,
         "theme_share_by_year_pct": {str(y): {k: v for k, v in TY[y].items() if v} for y in TY},
         "theme_share_vs_peers_pct": PT,
         "business_lenses": [{k: x[k] for k in ("lens", "articles", "share_pct", "late_vs_early", "neg_per_pos", "top_tags")} for x in LZ],
         "areas_of_activity": [r["area"] for r in ((ac.get("areas_of_activity") or {}).get("rows") or [])[:6]],
         "organisations": [r["label"] for r in ((en.get("organizations") or {}).get("rows") or [])[:6]],
         "people": [r["label"] for r in ((en.get("people") or {}).get("rows") or [])[:6]],
         "latest_events": {r["event_type"]: (r.get("examples") or [{}])[0].get("headline", "")[:200]
                           for r in (((ac.get("company_events") or {}).get("rows")) or [])[:6]},
         "timeline_arc": tl.get("arc"), "turning_points": tl.get("turning_points")}
    keys = ("summary", "signals", "themes_time", "lenses", "peers", "mix", "events", "risks", "catalysts", "areas", "timeline", "watch")
    return F, _w(_WRITE_SYS, F, keys)


# ─────────────────────────────────────────── page ───────────────────────────────────────────
def tabs(slug, data, S, text, TY, keep, PT, pkeep, LZ):
    name, lst, term, dom, sector, group, risks, cats = COMPANIES[slug]
    ov = D(data, "overview") or {}
    T = []
    sr = signal_rows(S)
    watch = "".join(f"<li>{escape(str(w))}</li>" for w in (text.get("watch") or []))
    T.append(("Summary", f"<div class='card'><p>{escape(text.get('signals', ''))}</p>{table(sr, ['Signal', 'Measured', 'Direction'])}"
              f"{'<h3>What to watch</h3><ul>' + watch + '</ul>' if watch else ''}<p class='note'>{escape(DISCLAIMER)}</p></div>"))
    if keep:
        cells = [{"year": str(y), "theme": k, "v": TY[y][k]} for y in YEARS for k in keep]
        T.append(("Themes over 5 years", f"<div class='card'><p>{escape(text.get('themes_time', ''))}</p>"
                  + heatmap("th5", cells, "year", "theme", f"{name}: share of themed coverage by year", xs=[str(y) for y in YEARS], ys=keep)
                  + stacked("thst", cells, "How the theme mix shifted, 2021 to 2025")
                  + "<p class='note'>Shares of the company's themed news coverage within each calendar year (news.themes, one call per year). "
                    "A blank cell means the theme was not among that year's top themes.</p></div>"))
    if LZ:
        h = (f"<p>{escape(text.get('lenses', ''))}</p>"
             + vbar("lz", [(f"{x['lens']} ({x['scope']})", x["articles"]) for x in LZ], "Business lenses: articles inside the company's coverage", "#2a78d6", xtitle="articles")
             + vline("lzt", [(x["lens"], x["points"]) for x in LZ[:5]], "Lens share of monthly coverage", "% of the company's coverage")
             + table([(x["lens"], x["articles"], f"{x['share_pct']}%", f"{x['late_vs_early']}×", x["neg_per_pos"], ", ".join(x["top_tags"][:4])) for x in LZ],
                     ["Lens", "Articles", "Share of coverage", "Last third vs first", "Negative per positive", "Top tags inside"]))
        T.append(("Business lenses", "<div class='card'>" + h + "</div>"))
    if pkeep:
        cos = list(PT)
        cells = [{"company": c.title(), "theme": k, "v": PT[c][k]} for c in cos for k in pkeep]
        pr = ((data.get("peers") or {}).get("data") or {}).get("rows") or []
        h = (f"<p>{escape(text.get('peers', ''))}</p>"
             + heatmap("pt", cells, "company", "theme", "Themes against competitors (share of themed coverage, mid-2024 to mid-2026)",
                       xs=[c.title() for c in cos], ys=pkeep, w=520, scheme="oranges")
             + (vline("pa", [(r["term"].title(), [(p["period"][:7], p.get("articles") or 0) for p in r["points"] if not p.get("partial_period")]) for r in pr],
                      "Attention on one scale", "articles") if pr else "")
             + table([(r["term"].title(), r["articles"], f"{r['share_pct']}%", f"{r['growth']}× ({r['direction']})", r["tone_ratio"]) for r in pr],
                     ["Company", "Articles", "Share of the group", "Growth", "Negative per positive"]))
        T.append(("Versus peers", "<div class='card'>" + h + "</div>"))
    ev = ((D(data, "activities") or {}).get("company_events")) or {}
    tot = ((ov.get("sentiment") or {}).get("totals")) or {}
    pr = ((data.get("peers") or {}).get("data") or {}).get("rows") or []
    donuts = []
    if ev.get("available"):
        donuts.append(donut("d1", [(r["event_type"], r["events"]) for r in ev["rows"][:8]], "Company events by type"))
    if tot:
        donuts.append(donut("d2", [("negative", tot.get("neg")), ("positive", tot.get("pos")), ("neutral", tot.get("neutral"))], "Tone of coverage"))
    if pr:
        donuts.append(donut("d3", [(r["term"].title(), r["articles"]) for r in pr], "Share of the peer group's attention"))
    if donuts:
        T.append(("Mix", f"<div class='card'><p>{escape(text.get('mix', ''))}</p><div style='display:flex;flex-wrap:wrap;gap:18px'>" + "".join(donuts) + "</div></div>"))
    if ev.get("available"):
        bm = [x for x in ev.get("by_month") or [] if x["period"] < EVENTS_THROUGH]
        types = [r["event_type"] for r in ev["rows"][:6]]
        cells = [{"m": x["period"][:7], "t": t, "v": x.get(t, 0)} for x in bm for t in types]
        h = (f"<p>{escape(text.get('events', ''))}</p>"
             + _embed("evs", {"width": 680, "height": 260, "title": {"text": "Company events per month, by type (to April 2026)", "anchor": "start", "fontSize": 14},
                              "data": {"values": cells}, "mark": "bar",
                              "encoding": {"x": {"field": "m", "type": "ordinal", "title": None}, "y": {"field": "v", "type": "quantitative", "title": "events"},
                                           "color": {"field": "t", "type": "nominal", "scale": {"scheme": "tableau10"}, "title": None},
                                           "tooltip": [{"field": "m"}, {"field": "t"}, {"field": "v"}]}})
             + table([(r["event_type"], r["events"], f"{(r.get('examples') or [{}])[0].get('date', '')}: {str((r.get('examples') or [{}])[0].get('headline', ''))[:170]}") for r in ev["rows"][:10]],
                     ["Event type", "Events", "Latest example"]))
        T.append(("Events", "<div class='card'>" + h + "</div>"))
    rc = []
    for label, pre, scopes in (("Risk", "risk", risks), ("Catalyst", "cat", cats)):
        for i, s_ in enumerate(scopes):
            d = D(data, f"{pre}{i}")
            if d:
                rc.append((label, s_, d))
    if rc:
        h = (f"<p>{escape(text.get('risks', ''))} {escape(text.get('catalysts', ''))}</p>"
             + vline("rc", [(f"{l}: {s_}", [(p['period'][:7], p.get('section_share_pct') or 0) for p in d['points']]) for l, s_, d in rc],
                     "Risk and catalyst sections, share of monthly coverage", "%"))
        for l, s_, d in rc:
            h += (f"<h3>{l}: {escape(s_)}</h3><p>{fmt(d['section']['articles'])} articles ({d['section']['share_of_entity_pct']}%), last third vs first "
                  f"{d['section']['late_vs_early']}×; {d['tone']['section_neg_per_pos']} negative per positive.</p>"
                  + table([(e["date"], e["reports_that_day"], e["opening"][:160]) for e in (d.get("events") or [])[:4]], ["Day", "Outlets", "Reported"]))
        T.append(("Risks & catalysts", "<div class='card'>" + h + "</div>"))
    tr, se = ov.get("trends") or {}, ov.get("sentiment") or {}
    pts = [x for x in tr.get("points") or [] if not x.get("partial_period")]
    if pts:
        T.append(("Coverage & tone", "<div class='card'>" + vline("tr", [("all coverage", [(x["period"][:7], x["articles"]) for x in pts]),
                                                                        ("high-priority stories", [(x["period"][:7], x["critical"]) for x in pts])], "Monthly news coverage", "articles")
                  + vline("tn", [("negative per positive", [(x["period"][:7], x.get("ratio")) for x in se.get("points") or []])], "Tone, month by month", "ratio") + "</div>"))
    ac = D(data, "activities") or {}
    areas = ((ac.get("areas_of_activity") or {}).get("rows") or [])[:10]
    en = ov.get("entities") or {}
    if areas or en:
        T.append(("Areas & people", f"<div class='card'><p>{escape(text.get('areas', ''))}</p>"
                  + (vbar("ar", [(r["area"], r["articles"]) for r in areas], "Areas of activity (industry taxonomy)", "#1baf7a", xtitle="articles") if areas else "")
                  + "<div class='grid2'><div>" + table([(r["label"], r["articles"]) for r in ((en.get("organizations") or {}).get("rows") or [])[:8]], ["Organisation", "Articles"])
                  + "</div><div>" + table([(r["label"], r["articles"]) for r in ((en.get("people") or {}).get("rows") or [])[:8]], ["Person", "Articles"]) + "</div></div></div>"))
    tl = D(data, "timeline")
    if tl and tl.get("months_read"):
        ms = "".join(f"<div class='m'><div class='sig'>{escape(x['month'])} · {x.get('articles', 0):,} articles · {escape(str(x.get('signal') or ''))}</div>"
                     f"<div class='h'>{escape(x.get('headline') or '')}</div>" + "".join(f"<div>• {escape(p['text'])}</div>" for p in x.get("points") or []) + "</div>"
                     for x in tl["months"] if x.get("available"))
        T.append(("Month by month", f"<div class='card'><h3>The year in one paragraph</h3><p>{escape(tl.get('arc') or '')}</p><p>{escape(text.get('timeline', ''))}</p></div><div class='card'>{ms}</div>"))
    calls = list((data.get("_mcp") or {}).values())
    T.append(("Built with MCP", "<div class='card'><p>Every panel in this report is the result of one of these Prism MCP tool calls, made over MCP "
              "(streamable HTTP) exactly as an assistant would make them.</p>"
              + table([(c["tool"], json.dumps(c["args"], ensure_ascii=False)[:110], f"{c['seconds']} s", "ok" if c["ok"] else "no data") for c in calls],
                      ["MCP tool", "Arguments", "Time", "Result"]) + "</div>"))
    return T


def partial(data):
    """True when any MCP response was answered while part of the index was offline"""
    return any(((v.get("meta") or {}).get("coverage") or {}).get("partial") for k, v in data.items()
               if isinstance(v, dict) and k != "_mcp")


BANNER = ("Built while part of the news index was offline: counts and shares here are lower bounds (floors), "
          "and will be rebuilt in full when the index is complete.")


def page(slug, data, S, text, *views):
    name, lst, term, dom, sector = COMPANIES[slug][:5]
    T = tabs(slug, data, S, text, *views)
    btn = "".join(f'<button role="tab" aria-selected="{str(i == 0).lower()}" data-t="{i}">{escape(n)}</button>' for i, (n, _) in enumerate(T))
    pan = "".join(f'<section class="panel{" on" if i == 0 else ""}" data-p="{i}">{h}</section>' for i, (_, h) in enumerate(T))
    kp = "".join(f"<div class='kpi'><b>{escape(str(c or '—'))}</b><span>{escape(a)}: {escape(b)}</span></div>" for a, b, c in signal_rows(S)[:4])
    calls = len((data.get("_mcp") or {}))
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(name)} · Prism intelligence report</title><style>{CSS}</style>
<script src="https://cdn.jsdelivr.net/npm/vega@5.30.0"></script><script src="https://cdn.jsdelivr.net/npm/vega-lite@5.21.0"></script><script src="https://cdn.jsdelivr.net/npm/vega-embed@6.26.0"></script></head>
<body><div class="w"><p class="note">{escape(lst)} · {escape(sector)} · Prism intelligence report · built from {calls} MCP calls</p><h1>{escape(name)}</h1>
<p class="sub">{escape(text.get('summary', ''))}</p>{('<p class="m"><b>Partial index.</b> ' + escape(BANNER) + '</p>') if partial(data) else ''}<div class="kpis">{kp}</div><div class="tabs" role="tablist">{btn}</div>{pan}
<p class="note">{escape(DISCLAIMER)} Source: Prism MCP. Built {time.strftime('%Y-%m-%d')}.</p></div>
<script>document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b));document.querySelectorAll('.panel').forEach(x=>x.classList.toggle('on',x.dataset.p===b.dataset.t));window.dispatchEvent(new Event('resize'));}});</script>
</body></html>""", [n for n, _ in T]


CHART_SHOTS = [("th5", "themes-over-years"), ("thst", "theme-mix"), ("lz", "business-lenses"), ("pt", "themes-vs-peers"),
               ("d1", "events-donut"), ("d2", "tone-donut"), ("d3", "peer-share-donut"), ("evs", "events-by-month")]


class shot_lock:
    """one headless Chrome at a time across processes too (two report builders at once left chart folders empty)"""
    def __enter__(self):
        import fcntl
        self.f = open("/tmp/prism_chart_shots.lock", "w")
        fcntl.flock(self.f, fcntl.LOCK_EX)

    def __exit__(self, *a):
        self.f.close()


def chart_pngs(slug):
    """screenshot each chart element of the page for the GitHub report (one tab at a time)"""
    d = os.path.join(OUT, slug)
    os.makedirs(os.path.join(d, "charts"), exist_ok=True)
    js = os.path.join(HERE, "chart_shots.js")
    with _SHOT, shot_lock():
        subprocess.run(["node", js, os.path.join(d, "page", "index.html"), os.path.join(d, "charts"),
                           ",".join(f"{a}:{b}" for a, b in CHART_SHOTS)], capture_output=True, text=True, timeout=300)
    return [f for f in os.listdir(os.path.join(d, "charts")) if f.endswith(".png")]


def readme(slug, data, S, F, text, names, pngs, TY, keep, PT, pkeep, LZ):
    name, lst, term, dom, sector, group, risks, cats = COMPANIES[slug]
    img = lambda n, alt: [f"![{alt}](charts/{n}.png)", ""] if f"{n}.png" in pngs else []
    calls = list((data.get("_mcp") or {}).values())
    L = [f"# {name}: intelligence report", "", f"*{lst} · {sector}* · built from **{len(calls)} Prism MCP calls** · "
         f"**[Open the interactive report]({HOST}/{slug}/)** (tabs: {' · '.join(names)})", "",
         f"![{name}: how its themes changed, 2021 to 2025, animated](theme-race.gif)", "",
         *([f"> **Partial index.** {BANNER}", ""] if partial(data) else []), text.get("summary", ""), "",
         "## Signals", "", text.get("signals", ""), "", "| Signal | Measured | Direction |", "| --- | --- | --- |"]
    L += [f"| {a} | {b} | {c} |" for a, b, c in signal_rows(S)] + [""]
    if text.get("watch"):
        L += ["**What to watch:**", ""] + [f"- {w}" for w in text["watch"]] + [""]
    if keep:
        L += ["## Themes over five years", "", text.get("themes_time", ""), ""] + img("themes-over-years", "Theme share by year") + img("theme-mix", "Theme mix over time")
        L += ["| Theme | " + " | ".join(str(y) for y in YEARS) + " |", "| --- |" + " ---: |" * len(YEARS)]
        L += [f"| {k} | " + " | ".join(f"{TY[y][k]}%" if TY[y][k] else "–" for y in YEARS) + " |" for k in keep] + [""]
    if LZ:
        L += ["## Business lenses", "", text.get("lenses", ""), ""] + img("business-lenses", "Business lenses")
        L += ["| Lens | Articles | Share of coverage | Last third vs first | Negative per positive | Top tags inside |", "| --- | ---: | ---: | ---: | ---: | --- |"]
        L += [f"| {x['lens']} (*{x['scope']}*) | {fmt(x['articles'])} | {x['share_pct']}% | {x['late_vs_early']}× | {x['neg_per_pos']} | {', '.join(x['top_tags'][:4])} |" for x in LZ] + [""]
    if pkeep:
        L += ["## Versus peers", "", text.get("peers", ""), ""] + img("themes-vs-peers", "Themes against competitors")
        cos = list(PT)
        L += ["| Theme | " + " | ".join(c.title() for c in cos) + " |", "| --- |" + " ---: |" * len(cos)]
        L += [f"| {k} | " + " | ".join(f"{PT[c][k]}%" if PT[c][k] else "–" for c in cos) + " |" for k in pkeep] + [""]
    if any(f"{n}.png" in pngs for n in ("events-donut", "tone-donut", "peer-share-donut")):
        L += ["## Mix", "", text.get("mix", ""), "", "| | | |", "| --- | --- | --- |",
              "| " + " | ".join(f"![{n}](charts/{n}.png)" if f"{n}.png" in pngs else "" for n in ("events-donut", "tone-donut", "peer-share-donut")) + " |", ""]
    for h, k in (("Company events", "events"), ("Risks", "risks"), ("Catalysts", "catalysts"), ("Areas of activity and people", "areas"), ("The year, month by month", "timeline")):
        if text.get(k):
            L += [f"## {h}", "", text[k], ""] + (img("events-by-month", "Events by month") if k == "events" else [])
    L += ["## Built with MCP", "", f"Every number and chart above comes from these {len(calls)} Prism MCP tool calls, made over MCP "
          "(streamable HTTP) as an assistant would make them. The full list with arguments and timings is in "
          "[mcp_calls.json](mcp_calls.json); the responses are in [data.json](data.json).", "",
          "| MCP tool | Calls | What it gave this report |", "| --- | ---: | --- |"]
    what = {"prism_overview": "coverage, tone, themes, places and people", "news_activities": "areas of activity and company events by month",
            "news_themes": "themes per year, and each peer's themes", "news_drill": "business lenses, risk and catalyst sections",
            "compare_terms": "peers on one scale", "deep_timeline": "the month-by-month reading"}
    counts = {}
    for c in calls:
        counts[c["tool"]] = counts.get(c["tool"], 0) + 1
    L += [f"| `{t}` | {n} | {what.get(t, '')} |" for t, n in counts.items()] + ["", f"> {DISCLAIMER}", ""]
    open(os.path.join(OUT, slug, "README.md"), "w").write("\n".join(L) + "\n")


def race_gif(slug, TY, keep):
    from gifs import race_gif as _race
    with _GIF:
        _race({str(y): [(k, TY[y][k] or 0) for k in keep] for y in YEARS}, f"{COMPANIES[slug][0]}: themes, 2021 to 2025",
              os.path.join(OUT, slug, "theme-race.gif"), subtitle="Share of themed news coverage, % per year")


def build(slug, refresh=False, write_only=False):
    data = json.load(open(os.path.join(OUT, slug, "data.json"))) if write_only else collect(slug, refresh)
    if not D(data, "overview"):
        print(f"{slug}: no overview, skipped", flush=True)
        return None
    S = signals(slug, data)
    TY, keep = theme_years(data)
    PT, pkeep = peer_themes(data, slug)
    LZ = lenses(data)
    wp = os.path.join(OUT, slug, "writeup.json")
    if write_only and os.path.exists(wp) and json.load(open(wp)).get("report"):
        w = json.load(open(wp))
        F, text = w["facts"], w["text"]
    else:
        F, text = write(slug, data, S, TY, keep, PT, pkeep, LZ)
    d = os.path.join(OUT, slug)
    os.makedirs(os.path.join(d, "page"), exist_ok=True)
    html, names = page(slug, data, S, text, TY, keep, PT, pkeep, LZ)
    open(os.path.join(d, "page", "index.html"), "w").write(html)
    json.dump({"report": True, "facts": F, "signals": S, "text": text}, open(wp, "w"), ensure_ascii=False, indent=1, default=str)
    if keep:
        race_gif(slug, TY, keep)
    pngs = chart_pngs(slug)
    readme(slug, data, S, F, text, names, pngs, TY, keep, PT, pkeep, LZ)
    shot(os.path.join(d, "page", "index.html"), os.path.join(d, "screenshot.jpg"))
    print(f"{slug}: tabs {names}; charts {len(pngs)}", flush=True)
    return names


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--write-only", action="store_true")
    a = ap.parse_args()
    slugs = a.only.split(",") if a.only else list(COMPANIES)
    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(lambda s: build(s, a.refresh, a.write_only), slugs))
    print("REPORTS_DONE", flush=True)
