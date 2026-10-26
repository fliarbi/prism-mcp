"""Investor briefs: one tabbed decision page per listed company (US, UK, Europe, Japan, Korea), plus a written GitHub page
and an animated GIF.

What an investor or stock buyer gets is not a coverage chart but the inputs to a decision: is attention building or
fading, is the tone turning, are risk events (lawsuits, regulatory action, layoffs) rising against catalyst events (new
products, contracts, M&A), which risk and catalyst sections are growing inside the company's coverage, how it stands
against its peers, and what happened month by month. Decision inputs, not investment advice: news attention and tone
are not price forecasts.

Tabs: Signals · Coverage & tone · Events · Risks · Catalysts · Peers · Areas & people · Month by month.

    python3 showcase/investor_pages.py [--only apple,...] [--workers 3] [--write-only]
Writes docs/investors/<slug>/{README.md, data.json, writeup.json, signals.gif, screenshot.jpg, page/index.html}.
"""
import argparse
import json
import os
import shutil
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
from topic_pages import D, fmt, mapjs, _prev_month  # noqa: E402

OUT = os.path.join(ROOT, "docs", "investors")
HOST = "https://fliarbi.com/demo/docs/prism-dashboards-3bb43e4c/investors"
ASSETS = os.path.join(HERE, "assets")
DISCLAIMER = ("Decision inputs, not investment advice. News attention, tone and event counts describe what is being "
              "reported; they are not price forecasts and do not account for valuation, fundamentals or your circumstances.")
EVENTS_THROUGH = "2026-05-01"   # company-event linkage is complete to April 2026

PEERS = {"big_tech": ["apple", "microsoft", "amazon", "google"], "semis": ["nvidia", "amd", "intel", "tsmc"],
         "autos": ["tesla", "byd", "toyota", "volkswagen"], "banks": ["jpmorgan", "goldman sachs", "hsbc", "morgan stanley"],
         "consumer": ["unilever", "nestle", "procter & gamble"], "pharma": ["astrazeneca", "pfizer", "novartis", "eli lilly"],
         "electronics": ["samsung", "tsmc", "sk hynix", "intel"]}

# slug: (name, listing, news term, web domain, sector, peer group, risk sections, catalyst sections)
COMPANIES = {
    "apple": ("Apple", "United States · NASDAQ: AAPL", "apple", "apple.com", "Consumer technology", "big_tech",
              ["antitrust", "tariff"], ["artificial intelligence", "iphone"]),
    "microsoft": ("Microsoft", "United States · NASDAQ: MSFT", "microsoft", "microsoft.com", "Software and cloud", "big_tech",
                  ["antitrust", "outage"], ["openai", "azure"]),
    "nvidia": ("NVIDIA", "United States · NASDAQ: NVDA", "nvidia", "nvidia.com", "Semiconductors", "semis",
               ["export controls", "china"], ["data center", "blackwell"]),
    "amazon": ("Amazon", "United States · NASDAQ: AMZN", "amazon", "amazon.com", "E-commerce and cloud", "big_tech",
               ["layoffs", "antitrust"], ["aws", "artificial intelligence"]),
    "tesla": ("Tesla", "United States · NASDAQ: TSLA", "tesla", "tesla.com", "Automobiles", "autos",
              ["recall", "sales decline"], ["robotaxi", "optimus"]),
    "jpmorgan": ("JPMorgan Chase", "United States · NYSE: JPM", "jpmorgan", "jpmorganchase.com", "Banking", "banks",
                 ["lawsuit", "regulator"], ["investment banking", "acquisition"]),
    "hsbc": ("HSBC", "United Kingdom · LSE: HSBA", "hsbc", "hsbc.com", "Banking", "banks",
             ["fine", "restructuring"], ["asia", "wealth"]),
    "unilever": ("Unilever", "United Kingdom · LSE: ULVR", "unilever", "unilever.com", "Consumer goods", "consumer",
                 ["layoffs", "lawsuit"], ["demerger", "acquisition"]),
    "astrazeneca": ("AstraZeneca", "United Kingdom · LSE: AZN", "astrazeneca", "astrazeneca.com", "Pharmaceuticals", "pharma",
                    ["tariff", "trial"], ["fda approval", "cancer"]),
    "nestle": ("Nestlé", "Switzerland · SIX: NESN", "nestle", "nestle.com", "Food and beverages", "consumer",
               ["recall", "ceo"], ["acquisition", "coffee"]),
    "samsung": ("Samsung Electronics", "South Korea · KRX: 005930", "samsung", "samsung.com", "Electronics and memory", "electronics",
                ["strike", "tariff"], ["hbm", "galaxy"]),
    "toyota": ("Toyota", "Japan · TSE: 7203", "toyota", "global.toyota", "Automobiles", "autos",
               ["recall", "tariff"], ["hybrid", "electric vehicle"]),
}
_GIF_LOCK = threading.Lock()


def peers_data(group):
    import prism_mcp as m
    p = os.path.join(OUT, f"_peers_{group}.json")
    if os.path.exists(p):
        d = json.load(open(p))
        if d.get("ok"):
            return d
    d = m.REGISTRY["compare_terms"]["fn"](terms=PEERS[group], since="2024-06-01")
    os.makedirs(OUT, exist_ok=True)
    json.dump(d, open(p, "w"), ensure_ascii=False, default=str)
    return d


def collect(slug, refresh=False):
    import prism_mcp as m
    name, lst, term, dom, sector, group, risks, cats = COMPANIES[slug]
    path = os.path.join(OUT, slug, "data.json")
    data = json.load(open(path)) if os.path.exists(path) and not refresh else {}

    def get(key, tool, **args):
        d = data.get(key) or {}
        bad = any(v == "panel failed" for v in (((d.get("data") or {}).get("panels_empty")) or {}).values())
        if d.get("ok") and not bad:
            return
        try:
            data[key] = m.REGISTRY[tool]["fn"](**args)
        except Exception as e:
            data[key] = {"ok": False, "error": {"reason": str(e)}}
        print(f"  {slug} {key}: {data[key].get('ok')}", flush=True)
    get("overview", "prism_overview", term=term, since="2024-06-01")
    get("activities", "news_activities", term=term, domain=dom)
    for i, s in enumerate(risks):
        get(f"risk{i}", "news_drill", term=term, scope=s)
    for i, s in enumerate(cats):
        get(f"cat{i}", "news_drill", term=term, scope=s)
    get("timeline", "deep_timeline", term=term, months=12)
    data["peers"] = peers_data(group)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(data, open(path, "w"), ensure_ascii=False, indent=1, default=str)
    return data


def _sum(points, key, months):
    return sum((p.get(key) or 0) for p in points if p["period"][:7] in months)


def signals(slug, data):
    name, lst, term, dom, sector, group, risks, cats = COMPANIES[slug]
    ov = D(data, "overview") or {}
    tr, se = ov.get("trends") or {}, ov.get("sentiment") or {}
    pts = [p for p in tr.get("points") or [] if not p.get("partial_period")]
    S = {}
    if len(pts) >= 6:
        last3 = [p["period"][:7] for p in pts[-3:]]
        prev3 = [p["period"][:7] for p in pts[-6:-3]]
        a1, a0 = _sum(pts, "articles", last3), _sum(pts, "articles", prev3)
        S["attention"] = {"last_3_months": a1, "previous_3_months": a0, "ratio": round(a1 / a0, 2) if a0 else None,
                          "months": f"{last3[0]} to {last3[-1]} vs {prev3[0]} to {prev3[-1]}"}
        sp = se.get("points") or []
        n1, p1 = _sum(sp, "negative", last3), _sum(sp, "positive", last3)
        n0, p0 = _sum(sp, "negative", prev3), _sum(sp, "positive", prev3)
        S["tone"] = {"neg_per_pos_last_3": round(n1 / p1, 2) if p1 else None, "neg_per_pos_previous_3": round(n0 / p0, 2) if p0 else None,
                     "neg_per_pos_whole_window": (se.get("totals") or {}).get("ratio"), "all_news_neg_per_pos": se.get("corpus_baseline_ratio")}
    ev = ((D(data, "activities") or {}).get("company_events")) or {}
    if ev.get("available"):
        bm = [x for x in ev.get("by_month") or [] if x["period"] < EVENTS_THROUGH]
        months = [x["period"][:7] for x in bm][-12:]
        last6, prev6 = months[-6:], months[-12:-6]
        risk_t, cat_t = ev["risk_types"], ev["catalyst_types"]
        def tot(types, ms):
            return sum(sum(x.get(t, 0) for t in types) for x in bm if x["period"][:7] in ms)
        S["events"] = {"window": f"{last6[0]} to {last6[-1]} vs {prev6[0]} to {prev6[-1]}" if len(prev6) == 6 else None,
                       "risk_events_last_6": tot(risk_t, last6), "risk_events_previous_6": tot(risk_t, prev6),
                       "catalyst_events_last_6": tot(cat_t, last6), "catalyst_events_previous_6": tot(cat_t, prev6),
                       "earnings_events_last_6": tot(["earnings"], last6), "key_people_events_last_6": tot(["key people"], last6),
                       "risk_types": risk_t, "catalyst_types": cat_t}
    secs = []
    for kind, scopes, pre in (("risk", risks, "risk"), ("catalyst", cats, "cat")):
        for i, sc in enumerate(scopes):
            d = D(data, f"{pre}{i}")
            if d:
                secs.append({"kind": kind, "section": sc, "articles": d["section"]["articles"],
                             "share_of_company_pct": d["section"]["share_of_entity_pct"], "last_third_vs_first": d["section"]["late_vs_early"],
                             "neg_per_pos": d["tone"]["section_neg_per_pos"], "company_neg_per_pos": d["tone"]["entity_neg_per_pos"]})
    S["sections"] = secs
    pr = (data.get("peers") or {}).get("data") or {}
    rows = pr.get("rows") or []
    me = next((r for r in rows if r["term"] == term), None)
    S["peers"] = [{"company": r["term"], "articles": r["articles"], "share_pct": r["share_pct"], "growth": r["growth"],
                   "direction": r["direction"], "neg_per_pos": r["tone_ratio"]} for r in rows]
    if me:
        S["peer_rank_by_attention"] = 1 + sum(1 for r in rows if r["articles"] > me["articles"])
    return S


_WRITE_SYS = """You are a senior equity-research analyst writing the text of an investor decision page about a listed company,
from measured news and company-event data. Your reader is an investor or stock buyer deciding what to watch. Frame
everything as inputs to a decision (what is building, what is fading, what to weigh, what to watch), NEVER as a
recommendation: do not say buy, sell, hold, overweight, target price or "investors should". News attention and tone are
not price signals; say so where it matters. 'High-priority stories' means stories in the top priority bands, not tone.
Return JSON: {"summary": "4-5 sentences: the decision-relevant picture", "signals": "3 sentences reading the momentum signals",
"coverage": "2 sentences", "events": "2-3 sentences on risk vs catalyst events and earnings/leadership news",
"risks": "2-3 sentences on the risk sections", "catalysts": "2-3 sentences on the catalyst sections",
"peers": "2 sentences on the company against its peers", "areas": "2 sentences on areas of activity and who appears with it",
"timeline": "2-3 sentences on the year's arc and turning points", "watch": ["3 to 5 short items an investor should watch next"]}"""


def write(slug, data, S):
    from pagewriter import write as _w
    name, lst, term, dom, sector = COMPANIES[slug][:5]
    ov = D(data, "overview") or {}
    tr = ov.get("trends") or {}
    th = ov.get("themes") or {}
    ac = D(data, "activities") or {}
    en = ov.get("entities") or {}
    tl = D(data, "timeline") or {}
    F = {"company": name, "listing": lst, "sector": sector, "window": f"{tr.get('from', '')[:7]} to {_prev_month(tr.get('to', ''))}",
         "articles": tr.get("total"), "high_priority_stories": tr.get("critical_total"), "signals": S,
         "areas_of_activity": [r["area"] for r in ((ac.get("areas_of_activity") or {}).get("rows") or [])[:6]],
         "top_tags": [r["label"] for r in sorted(((th.get("tags") or {}).get("rows") or []), key=lambda r: -r["articles"])[:10]],
         "organisations": [r["label"] for r in ((en.get("organizations") or {}).get("rows") or [])[:6]],
         "people": [r["label"] for r in ((en.get("people") or {}).get("rows") or [])[:6]],
         "latest_events": {r["event_type"]: (r.get("examples") or [{}])[0].get("headline", "")[:200]
                           for r in (((ac.get("company_events") or {}).get("rows")) or [])[:6]},
         "timeline_arc": tl.get("arc"), "turning_points": tl.get("turning_points")}
    text = _w(_WRITE_SYS, F, ("summary", "signals", "coverage", "events", "risks", "catalysts", "peers", "areas", "timeline", "watch"))
    return F, text


def _arrow(new, old):
    if new is None or old is None or old == 0:
        return "—"
    r = new / old
    return "rising" if r >= 1.15 else "falling" if r <= 0.87 else "steady"


def signal_rows(S):
    rows = []
    a = S.get("attention")
    if a:
        rows.append(("Attention", f"{fmt(a['last_3_months'])} articles in the last 3 months vs {fmt(a['previous_3_months'])} before ({a['ratio']}×)",
                     _arrow(a["last_3_months"], a["previous_3_months"])))
    t = S.get("tone")
    if t and t.get("neg_per_pos_last_3") is not None:
        rows.append(("Tone", f"{t['neg_per_pos_last_3']} negative per positive, vs {t['neg_per_pos_previous_3']} before (all news {t['all_news_neg_per_pos']})",
                     {"rising": "more negative", "falling": "less negative", "steady": "steady", "—": "—"}[_arrow(t["neg_per_pos_last_3"], t["neg_per_pos_previous_3"])]))
    e = S.get("events")
    if e:
        rows.append(("Risk events (lawsuits, regulatory, layoffs)", f"{e['risk_events_last_6']} in the last 6 months vs {e['risk_events_previous_6']} before",
                     _arrow(e["risk_events_last_6"], e["risk_events_previous_6"])))
        rows.append(("Catalyst events (products, contracts, M&A)", f"{e['catalyst_events_last_6']} in the last 6 months vs {e['catalyst_events_previous_6']} before",
                     _arrow(e["catalyst_events_last_6"], e["catalyst_events_previous_6"])))
    for x in S.get("sections") or []:
        rows.append((f"{x['kind'].title()} section: {x['section']}", f"{x['share_of_company_pct']}% of coverage, last third vs first {x['last_third_vs_first']}×",
                     _arrow(x["last_third_vs_first"], 1)))
    if S.get("peer_rank_by_attention"):
        rows.append(("Attention rank among peers", f"#{S['peer_rank_by_attention']} of {len(S['peers'])}", ""))
    return rows


def tabs(slug, data, S, text):
    name, lst, term, dom, sector, group, risks, cats = COMPANIES[slug]
    ov = D(data, "overview") or {}
    T = []
    sr = signal_rows(S)
    watch = "".join(f"<li>{escape(str(w))}</li>" for w in (text.get("watch") or []))
    T.append(("Signals", f"<div class='card'><p>{escape(text.get('signals', ''))}</p>{table([(a, b, c) for a, b, c in sr], ['Signal', 'Measured', 'Direction'])}"
              f"{'<h3>What to watch</h3><ul>' + watch + '</ul>' if watch else ''}<p class='note'>{escape(DISCLAIMER)}</p></div>"))
    tr, se = ov.get("trends") or {}, ov.get("sentiment") or {}
    pts = [x for x in tr.get("points") or [] if not x.get("partial_period")]
    if pts:
        h = vline("tr", [("all coverage", [(x["period"][:7], x["articles"]) for x in pts]),
                         ("high-priority stories", [(x["period"][:7], x["critical"]) for x in pts])], "Monthly news coverage", "articles")
        sp = se.get("points") or []
        if sp:
            h += vline("tn", [("negative per positive", [(x["period"][:7], x.get("ratio")) for x in sp]),
                              ("all-news baseline", [(x["period"][:7], se.get("corpus_baseline_ratio")) for x in sp])], "Tone, month by month", "negative per positive")
        T.append(("Coverage & tone", f"<div class='card'><p>{escape(text.get('coverage', ''))}</p>{h}</div>"))
    ev = ((D(data, "activities") or {}).get("company_events")) or {}
    if ev.get("available"):
        bm = [x for x in ev.get("by_month") or [] if x["period"] < EVENTS_THROUGH]
        rk = [(x["period"][:7], sum(x.get(t, 0) for t in ev["risk_types"])) for x in bm]
        ct = [(x["period"][:7], sum(x.get(t, 0) for t in ev["catalyst_types"])) for x in bm]
        er = [(x["period"][:7], x.get("earnings", 0)) for x in bm]
        h = (f"<p>{escape(text.get('events', ''))}</p>" + vline("ev", [("risk events", rk), ("catalyst events", ct), ("earnings", er)],
             "Company events per month (to April 2026)", "events") +
             table([(r["event_type"], r["events"], f"{(r.get('examples') or [{}])[0].get('date', '')}: {str((r.get('examples') or [{}])[0].get('headline', ''))[:170]}")
                    for r in ev["rows"][:10]], ["Event type", "Events", "Latest example"]))
        T.append(("Events", "<div class='card'>" + h + "</div>"))
    for label, pre, scopes, key in (("Risks", "risk", risks, "risks"), ("Catalysts", "cat", cats, "catalysts")):
        secs = [(s_, D(data, f"{pre}{i}")) for i, s_ in enumerate(scopes)]
        secs = [(s_, d) for s_, d in secs if d]
        if not secs:
            continue
        h = f"<p>{escape(text.get(key, ''))}</p>" + vline(pre, [(f"{s_}: % of {name} coverage", [(p["period"][:7], p.get("section_share_pct") or 0) for p in d["points"]]) for s_, d in secs],
                                                          f"{label} inside {name}'s coverage", "% of the company's monthly coverage")
        for s_, d in secs:
            h += (f"<h3>{escape(name)} → {escape(s_)}</h3><p>{fmt(d['section']['articles'])} articles ({d['section']['share_of_entity_pct']}% of the company's coverage), "
                  f"last third vs first {d['section']['late_vs_early']}×; {d['tone']['section_neg_per_pos']} negative per positive vs {d['tone']['entity_neg_per_pos']} for {escape(name)}.</p>"
                  + table([(e["date"], e["reports_that_day"], e["opening"][:170]) for e in (d.get("events") or [])[:5]], ["Day", "Outlets", "Reported"]))
        T.append((label, "<div class='card'>" + h + "</div>"))
    if S.get("peers"):
        h = f"<p>{escape(text.get('peers', ''))}</p>" + table([(p["company"].title(), p["articles"], f"{p['share_pct']}%", f"{p['growth']}× ({p['direction']})", p["neg_per_pos"]) for p in S["peers"]],
                                                              ["Company", "Articles", "Share of the group", "Growth", "Negative per positive"])
        pr = ((data.get("peers") or {}).get("data") or {}).get("rows") or []
        if pr:
            h += vline("pe", [(r["term"].title(), [(p["period"][:7], p.get("articles") or 0) for p in r["points"] if not p.get("partial_period")]) for r in pr],
                       "Peers: monthly coverage on one scale", "articles")
        T.append(("Peers", "<div class='card'>" + h + "</div>"))
    ac = D(data, "activities") or {}
    en = ov.get("entities") or {}
    areas = ((ac.get("areas_of_activity") or {}).get("rows") or [])[:10]
    if areas or en:
        h = f"<p>{escape(text.get('areas', ''))}</p>"
        if areas:
            h += vbar("ar", [(r["area"], r["articles"]) for r in areas], "Areas of activity (industry taxonomy)", "#1baf7a")
        h += ("<div class='grid2'><div>" + table([(r["label"], r["articles"]) for r in ((en.get("organizations") or {}).get("rows") or [])[:8]], ["Organisation", "Articles"]) +
              "</div><div>" + table([(r["label"], r["articles"]) for r in ((en.get("people") or {}).get("rows") or [])[:8]], ["Person", "Articles"]) + "</div></div>")
        T.append(("Areas & people", "<div class='card'>" + h + "</div>"))
    tl = D(data, "timeline")
    if tl and tl.get("months_read"):
        ms = "".join(f"<div class='m'><div class='sig'>{escape(x['month'])} · {x.get('articles', 0):,} articles · {escape(str(x.get('signal') or ''))}</div>"
                     f"<div class='h'>{escape(x.get('headline') or '')}</div>" + "".join(f"<div>• {escape(p['text'])}</div>" for p in x.get("points") or []) + "</div>"
                     for x in tl["months"] if x.get("available"))
        T.append(("Month by month", f"<div class='card'><h3>The year in one paragraph</h3><p>{escape(tl.get('arc') or '')}</p><p>{escape(text.get('timeline', ''))}</p></div><div class='card'>{ms}</div>"))
    return T


def page(slug, data, S, text):
    name, lst, term, dom, sector = COMPANIES[slug][:5]
    T = tabs(slug, data, S, text)
    btn = "".join(f'<button role="tab" aria-selected="{str(i == 0).lower()}" data-t="{i}">{escape(n)}</button>' for i, (n, _) in enumerate(T))
    pan = "".join(f'<section class="panel{" on" if i == 0 else ""}" data-p="{i}">{h}</section>' for i, (_, h) in enumerate(T))
    k = [(c, f"{a}: {b}") for a, b, c in signal_rows(S)[:4]]
    kp = "".join(f"<div class='kpi'><b>{escape(str(v or '—'))}</b><span>{escape(n)}</span></div>" for v, n in k)
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(name)} · Prism investor brief</title><style>{CSS}</style>
<script src="https://cdn.jsdelivr.net/npm/vega@5.30.0"></script><script src="https://cdn.jsdelivr.net/npm/vega-lite@5.21.0"></script><script src="https://cdn.jsdelivr.net/npm/vega-embed@6.26.0"></script></head>
<body><div class="w"><p class="note">{escape(lst)} · {escape(sector)} · Prism investor brief</p><h1>{escape(name)}</h1><p class="sub">{escape(text.get('summary', ''))}</p>
<div class="kpis">{kp}</div><div class="tabs" role="tablist">{btn}</div>{pan}
<p class="note">{escape(DISCLAIMER)} Source: Prism MCP. Built {time.strftime('%Y-%m-%d')}.</p></div>
<script>document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b));document.querySelectorAll('.panel').forEach(x=>x.classList.toggle('on',x.dataset.p===b.dataset.t));window.dispatchEvent(new Event('resize'));}});</script>
</body></html>""", [n for n, _ in T]


def readme(slug, data, S, F, text, names):
    name, lst, term, dom, sector, group, risks, cats = COMPANIES[slug]
    L = [f"# {name}: investor brief", "", f"*{lst} · {sector}* · **[Open the interactive brief]({HOST}/{slug}/)** (tabs: {' · '.join(names)})", "",
         f"![{name}: risk vs catalyst events and coverage, animated](signals.gif)", "", text.get("summary", ""), "",
         "## Signals", "", text.get("signals", ""), "", "| Signal | Measured | Direction |", "| --- | --- | --- |"]
    L += [f"| {a} | {b} | {c} |" for a, b, c in signal_rows(S)] + [""]
    if text.get("watch"):
        L += ["**What to watch:**", ""] + [f"- {w}" for w in text["watch"]] + [""]
    for h, k in (("Coverage and tone", "coverage"), ("Company events", "events"), ("Risk sections", "risks"),
                 ("Catalyst sections", "catalysts"), ("Peers", "peers"), ("Areas of activity and people", "areas"), ("The year, month by month", "timeline")):
        if not text.get(k):
            continue
        L += [f"## {h}", "", text[k], ""]
        if k in ("risks", "catalysts"):
            secs = [x for x in S.get("sections") or [] if x["kind"] == ("risk" if k == "risks" else "catalyst")]
            if secs:
                L += ["| Section | Articles | Share of coverage | Last third vs first | Negative per positive |", "| --- | ---: | ---: | ---: | ---: |"]
                L += [f"| {name} → {x['section']} | {fmt(x['articles'])} | {x['share_of_company_pct']}% | {x['last_third_vs_first']}× | {x['neg_per_pos']} (company {x['company_neg_per_pos']}) |" for x in secs] + [""]
        if k == "peers" and S.get("peers"):
            L += ["| Company | Articles | Share | Growth | Negative per positive |", "| --- | ---: | ---: | --- | ---: |"]
            L += [f"| {p['company'].title()} | {fmt(p['articles'])} | {p['share_pct']}% | {p['growth']}× ({p['direction']}) | {p['neg_per_pos']} |" for p in S["peers"]] + [""]
        if k == "events":
            ev = ((D(data, "activities") or {}).get("company_events")) or {}
            if ev.get("available"):
                L += ["| Event type | Events | Latest example |", "| --- | ---: | --- |"]
                L += [f"| {r['event_type']} | {fmt(r['events'])} | {(r.get('examples') or [{}])[0].get('date', '')}: {str((r.get('examples') or [{}])[0].get('headline', ''))[:160]} |"
                      for r in ev["rows"][:8]] + [""]
    L += ["![The interactive brief](screenshot.jpg)", "", f"> {DISCLAIMER}", "",
          "**How this brief is built.** `news.overview` (coverage, tone, themes, people), `news.activities` with the company's "
          f"web domain `{dom}` (areas of activity and company events by month), `news.drill` for each risk and catalyst section, "
          "`news.compare` for the peer group and `analysis.timeline` for the month-by-month reading. Momentum compares the last "
          "three complete months with the three before; event momentum compares the last six complete months of event linkage "
          "with the six before. The text was written from this brief's data only; sentences with numbers not in the data were "
          "removed. Data: [data.json](data.json).", "",
          f"Try it: `prism entity \"{term}\"` · `prism call news.drill term='{term}' scope='{risks[0]}'` · "
          f"`prism call news.activities term='{term}' domain='{dom}'`", ""]
    open(os.path.join(OUT, slug, "README.md"), "w").write("\n".join(L) + "\n")


def gif(slug, data):
    from gifs import lines_gif
    name = COMPANIES[slug][0]
    ev = ((D(data, "activities") or {}).get("company_events")) or {}
    out = os.path.join(OUT, slug, "signals.gif")
    with _GIF_LOCK:
        if ev.get("available"):
            bm = [x for x in ev.get("by_month") or [] if x["period"] < EVENTS_THROUGH]
            lines_gif([("risk events", [(x["period"][2:7].replace("-", "/"), sum(x.get(t, 0) for t in ev["risk_types"])) for x in bm]),
                       ("catalyst events", [(x["period"][2:7].replace("-", "/"), sum(x.get(t, 0) for t in ev["catalyst_types"])) for x in bm])],
                      f"{name}: risk vs catalyst events", out, subtitle="Company events per month from business news (to April 2026)")
        else:
            tr = (D(data, "overview") or {}).get("trends") or {}
            pts = [x for x in tr.get("points") or [] if not x.get("partial_period")]
            lines_gif([("coverage", [(x["period"][2:7].replace("-", "/"), x["articles"]) for x in pts])], name, out, subtitle="News coverage per month")


def build(slug, refresh=False, write_only=False):
    data = json.load(open(os.path.join(OUT, slug, "data.json"))) if write_only else collect(slug, refresh)
    if not D(data, "overview"):
        print(f"{slug}: no overview, skipped", flush=True)
        return None
    S = signals(slug, data)
    wp = os.path.join(OUT, slug, "writeup.json")
    if write_only and os.path.exists(wp):        # re-render without rewriting the text
        w = json.load(open(wp))
        F, text = w["facts"], w["text"]
    else:
        F, text = write(slug, data, S)
    if not text.get("watch"):
        text["watch"] = []
    d = os.path.join(OUT, slug)
    os.makedirs(os.path.join(d, "page"), exist_ok=True)
    for f in ("world_india_official.geojson", "india_states_official.geojson"):
        shutil.copy(os.path.join(ASSETS, f), os.path.join(d, "page", f))
    html, names = page(slug, data, S, text)
    open(os.path.join(d, "page", "index.html"), "w").write(html)
    json.dump({"facts": F, "signals": S, "text": text}, open(os.path.join(d, "writeup.json"), "w"), ensure_ascii=False, indent=1, default=str)
    gif(slug, data)
    readme(slug, data, S, F, text, names)
    shot(os.path.join(d, "page", "index.html"), os.path.join(d, "screenshot.jpg"))
    print(f"{slug}: tabs {names}", flush=True)
    return names


def index():
    L = ["# Investor briefs: global public companies", "", "One decision page per listed company: attention and tone momentum, risk events "
         "against catalyst events, the risk and catalyst sections growing inside its coverage, its peers on one scale, and the year "
         "month by month, each with a written analysis.", "", f"> {DISCLAIMER}", "",
         "| Company | Listing | Sector | Brief | Interactive |", "| --- | --- | --- | --- | --- |"]
    for slug, c in COMPANIES.items():
        if os.path.exists(os.path.join(OUT, slug, "README.md")):
            L.append(f"| {c[0]} | {c[1]} | {c[4]} | [brief]({slug}/README.md) | [open]({HOST}/{slug}/) |")
    open(os.path.join(OUT, "README.md"), "w").write("\n".join(L) + "\n")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--write-only", action="store_true")
    a = ap.parse_args()
    slugs = a.only.split(",") if a.only else list(COMPANIES)
    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(lambda s: build(s, a.refresh, a.write_only), slugs))
    index()
    print("INVESTORS_DONE", flush=True)
