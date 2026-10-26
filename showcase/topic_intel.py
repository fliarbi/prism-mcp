"""Topic intelligence reports: the topic pages (topic_pages.py) upgraded the way the company and disease reports were,
with every call made over MCP (showcase/mcpcall.py) and listed at the end.

On top of the existing tabs (coverage, areas and themes, places, people, causes and impacts, sections, month by month):
  * Themes over 5 years: news.themes per calendar year, 2021 to 2025, as a heatmap and a stacked share chart, plus an
    animated theme race (theme-race.gif).
  * Three reader views chosen by domain (e.g. crime: policy makers · police & enforcement · researchers). The first
    reader gets trajectory, scenarios, geography and the stories that matter; the second the evidence behind a claim,
    two claims head to head and a cross-row screen with quoted figures; the third the framing of the literature, the
    frontier and the gaps. Each view has its own written reading and action list.
  * Research methods: the nine research exploration methods (disease_intel.METHODS) run on the topic, each with its
    MCP call, result and an in-depth reading.

    python3 showcase/topic_intel.py [--only heatwaves,...] [--workers 1] [--calls 4] [--write-only]
Writes docs/topics/<slug>/{README.md, data.json, writeup.json, mcp_calls.json, trend.gif, theme-race.gif, charts/*.png,
screenshot.jpg, page/index.html} and docs/topics/README.md.
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
import topic_pages as tp  # noqa: E402
from topic_pages import TOPICS, OUT, HOST, ASSETS, D, fmt  # noqa: E402
from disease_pages import vbar, vline, table, shot  # noqa: E402
from intel_reports import YEARS, theme_years, heatmap, stacked, partial, BANNER  # noqa: E402
from disease_intel import (METHODS, screening, evidence_view, series, scenario_chart, stance_area, mix_bars, method_result,
                           _ul)  # noqa: E402
import disease_intel  # noqa: E402
import mcpcall  # noqa: E402

_SHOT = threading.Lock()
TOPIC_Q = {"triangulation": "Is a claim supported, and by how strong a design?",
           "screening": "Which rows carry a measured, quoted figure, and how large is it?"}
_TP_TABS = tp.tabs   # the original; build() swaps tp.tabs so tp.page() renders the upgraded tab list
_GIF = threading.Lock()

AUDIENCES = {
    "Crime & public safety": ["Policy makers", "Police & enforcement", "Researchers"],
    "Infrastructure": ["Planners & policy makers", "Builders & operators", "Researchers"],
    "Business": ["Investors", "Founders & operators", "Researchers"],
    "Finance": ["Regulators & policy makers", "Investors", "Researchers"],
    "Energy & climate": ["Policy makers", "Industry & utilities", "Scientists"],
    "Environment": ["Policy makers", "Public health & city officials", "Scientists"],
    "Defence & geopolitics": ["Policy makers", "Defence & security analysts", "Researchers"],
    "Supply chain & trade": ["Policy makers", "Shippers & businesses", "Researchers"],
    "Technology & policy": ["Regulators", "Companies & product teams", "Researchers"],
    "Agriculture": ["Policy makers", "Farmers & agribusiness", "Scientists"],
    "Education & labour": ["Policy makers", "Employers & HR", "Researchers"],
}

# slug: (research claim, claim A, claim B, screening rows, screening question)
RESEARCH = {
    "cybercrime": ("Security awareness training reduces phishing susceptibility", "Multi-factor authentication reduces account compromise",
                   "Security awareness training reduces phishing susceptibility",
                   ["phishing", "ransomware", "identity theft", "online fraud", "cyberbullying", "data breaches"], "How prevalent is {row}?"),
    "drug-trafficking": ("Drug law enforcement increases drug market violence", "Drug law enforcement increases drug market violence",
                         "Supply-side interdiction reduces drug availability",
                         ["cocaine", "heroin", "methamphetamine", "cannabis", "fentanyl", "opium"], "How large is the illicit market for {row}?"),
    "road-accidents": ("Drunk driving increases the risk of road traffic accidents", "Speed cameras reduce road traffic crashes",
                       "Helmet laws reduce motorcycle crash deaths",
                       ["drunk driving", "speeding", "mobile phone use while driving", "not wearing seat belts", "driver fatigue", "poor road design"],
                       "Does {row} increase the risk of road traffic crashes?"),
    "metro-rail": ("Metro rail reduces road traffic congestion", "Metro rail reduces road traffic congestion",
                   "Metro rail increases nearby property values",
                   ["traffic congestion", "air pollution", "property values", "commute time", "carbon emissions", "road accidents"],
                   "What is the effect of metro rail on {row}?"),
    "urban-flooding": ("Impervious surfaces increase urban flooding", "Green infrastructure reduces urban flooding",
                       "Drainage capacity upgrades reduce urban flooding",
                       ["impervious surfaces", "rainfall intensity", "drainage capacity", "wetland loss", "urbanisation", "climate change"],
                       "How does {row} affect urban flood risk?"),
    "highways": ("Highway expansion induces additional traffic", "Highway expansion induces additional traffic",
                 "Highway investment increases regional economic growth",
                 ["traffic volume", "economic growth", "road accidents", "land prices", "emissions", "travel time"],
                 "What is the effect of highway construction on {row}?"),
    "data-centres": ("Data centers increase electricity demand", "Data centers increase electricity demand", "Data centers increase water consumption",
                     ["electricity use", "water use", "carbon emissions", "cooling energy", "local employment", "grid stability"],
                     "What is the impact of data centers on {row}?"),
    "startup-funding": ("Venture capital funding increases startup survival", "Venture capital funding increases startup survival",
                        "Government grants increase startup innovation",
                        ["survival", "innovation", "employment growth", "patenting", "revenue growth", "exits"],
                        "What is the effect of venture capital on startup {row}?"),
    "quick-commerce": ("Online grocery delivery reduces in-store shopping", "Online grocery delivery reduces in-store shopping",
                       "Rapid delivery increases impulse purchases",
                       ["impulse buying", "delivery worker safety", "packaging waste", "small retailer sales", "urban traffic", "household spending"],
                       "What is the effect of rapid grocery delivery on {row}?"),
    "electric-vehicles": ("Purchase subsidies increase electric vehicle adoption", "Purchase subsidies increase electric vehicle adoption",
                          "Charging infrastructure increases electric vehicle adoption",
                          ["purchase subsidies", "charging infrastructure", "battery cost", "fuel prices", "range anxiety", "model availability"],
                          "How does {row} affect electric vehicle adoption?"),
    "semiconductors": ("Government subsidies increase domestic semiconductor manufacturing",
                       "Government subsidies increase domestic semiconductor manufacturing", "Export controls slow semiconductor technology diffusion",
                       ["subsidies", "export controls", "talent shortages", "water use", "supply chain disruption", "energy use"],
                       "What is the effect of {row} on semiconductor manufacturing?"),
    "inflation": ("Interest rate increases reduce inflation", "Interest rate increases reduce inflation", "Food price shocks increase headline inflation",
                  ["interest rates", "food prices", "oil prices", "exchange rates", "wages", "money supply"], "What is the effect of {row} on inflation?"),
    "gold-price": ("Gold is a hedge against inflation", "Gold is a hedge against inflation", "Gold is a safe haven during stock market crashes",
                   ["inflation", "interest rates", "the US dollar", "stock market volatility", "central bank purchases", "geopolitical risk"],
                   "What is the effect of {row} on the gold price?"),
    "bitcoin": ("Bitcoin is a hedge against inflation", "Bitcoin is a hedge against inflation", "Bitcoin ETF approval increases the bitcoin price",
                ["inflation", "stock market returns", "regulation announcements", "energy use", "ETF flows", "interest rates"],
                "How is bitcoin related to {row}?"),
    "upi-payments": ("Digital payments increase financial inclusion", "Digital payments increase financial inclusion", "Digital payments increase fraud risk",
                     ["financial inclusion", "fraud", "cash use", "small business sales", "tax compliance", "consumer spending"],
                     "What is the effect of digital payments on {row}?"),
    "ipo-market": ("IPOs are underpriced on the first trading day", "IPOs are underpriced on the first trading day",
                   "IPOs underperform the market in the long run",
                   ["underpricing", "long-run returns", "retail investor demand", "anchor investors", "market sentiment", "lock-up expiry"],
                   "What does research measure about IPO {row}?"),
    "solar-power": ("Solar power reduces electricity costs", "Solar power reduces electricity costs", "Rooftop solar reduces household electricity bills",
                    ["electricity costs", "carbon emissions", "grid stability", "land use", "employment", "panel prices"],
                    "What is the effect of solar power on {row}?"),
    "heatwaves": ("Heatwaves increase mortality", "Heatwaves increase mortality", "Heat action plans reduce heat-related deaths",
                  ["mortality", "hospital admissions", "labour productivity", "electricity demand", "crop yields", "violent crime"],
                  "What is the effect of heatwaves on {row}?"),
    "air-pollution": ("Air pollution increases mortality", "Air pollution increases mortality", "Air pollution reduces life expectancy",
                      ["mortality", "respiratory disease", "cardiovascular disease", "cognitive function", "labour productivity", "life expectancy"],
                      "What is the effect of air pollution on {row}?"),
    "drone-warfare": ("Drone strikes reduce militant violence", "Drone strikes reduce militant violence", "Drone strikes increase civilian casualties",
                      ["civilian casualties", "militant violence", "military costs", "public opinion", "escalation", "territorial control"],
                      "What is the effect of drone warfare on {row}?"),
    "red-sea-shipping": ("Red Sea attacks increase global shipping costs", "Red Sea attacks increase global shipping costs",
                         "Shipping disruptions increase consumer prices",
                         ["freight rates", "transit time", "insurance premiums", "inflation", "trade volumes", "carbon emissions"],
                         "What is the effect of Red Sea shipping disruption on {row}?"),
    "ai-regulation": ("AI regulation slows innovation", "AI regulation slows innovation", "AI regulation increases public trust in AI",
                      ["innovation", "public trust", "compliance costs", "algorithmic bias", "startup investment", "transparency"],
                      "What is the effect of AI regulation on {row}?"),
    "data-privacy": ("Privacy regulation reduces online advertising effectiveness", "Privacy regulation reduces online advertising effectiveness",
                     "The GDPR reduced data collection by websites",
                     ["advertising effectiveness", "data collection", "consumer trust", "data breaches", "innovation", "compliance costs"],
                     "What is the effect of privacy regulation on {row}?"),
    "monsoon-agriculture": ("Monsoon rainfall deficits reduce crop yields", "Monsoon rainfall deficits reduce crop yields",
                            "Irrigation reduces crop losses from drought",
                            ["rice yields", "wheat yields", "farm income", "food prices", "groundwater levels", "rural employment"],
                            "What is the effect of monsoon rainfall variability on {row}?"),
    "layoffs": ("Layoffs reduce the morale of remaining employees", "Layoffs reduce the morale of remaining employees", "Layoffs improve firm profitability",
                ["productivity", "morale", "mental health", "firm profitability", "stock price", "innovation"], "What is the effect of layoffs on {row}?"),
}


def collect(slug, refresh=False, workers=4):
    title, dom, term, drills, phrase, claim0 = TOPICS[slug]
    claim, a, b, rows, q = RESEARCH[slug]
    path = os.path.join(OUT, slug, "data.json")
    data = json.load(open(path)) if os.path.exists(path) and not refresh else {}
    lock = threading.Lock()

    def get(key, tool, **args):
        d = data.get(key) or {}
        failed = any(v == "panel failed" for v in (((d.get("data") or {}).get("panels_empty")) or {}).values())
        if d.get("ok") and not failed and (data.get("_mcp") or {}).get(key, {}).get("args") == args:
            return
        t0 = time.time()
        env = mcpcall.call(tool, args)
        rec = {"key": key, "tool": tool, "args": args, "seconds": round(time.time() - t0, 1), "ok": bool(env.get("ok"))}
        with lock:
            data[key] = env
            data.setdefault("_mcp", {})[key] = rec
        print(f"  {slug} {key}: {rec['ok']} {rec['seconds']}s", flush=True)
    jobs = [("overview", "prism_overview", dict(term=term, since="2024-06-01")),
            ("activities", "news_activities", dict(term=term)),
            ("states", "news_geography", dict(term=term, level="state", limit=25)),
            ("factors", "news_factors", dict(topic=term)),
            *[(f"drill{i}", "news_drill", dict(term=term, scope=d)) for i, d in enumerate(drills)],
            *[(f"themes_{y}", "news_themes", dict(term=term, since=f"{y}-01-01", until=f"{y + 1}-01-01", limit=25)) for y in YEARS],
            ("critical", "critical_news", dict(term=term, limit=8)),
            ("stance", "stance_trends", dict(term=phrase)),
            ("history", "historical_analysis", dict(subject_phrases=[phrase], query_seconds=30)),
            ("brief", "research_brief", dict(topic=phrase)),
            ("radar", "research_radar", dict(topic=phrase, since_year=2022)),
            ("browse", "browse_research", dict(term=phrase, sort="citations", since=2020, limit=12)),
            ("geo", "global_comparison", dict(claim=claim)),
            ("gaps", "research_gaps", dict(claim=claim)),
            ("evidence", "find_evidence", dict(claim=claim, limit=10)),
            ("counter", "find_counter_evidence", dict(claim=claim, limit=10)),
            ("rank", "rank_sources", dict(claim=claim)),
            ("compare", "compare_claims", dict(claim_a=a, claim_b=b)),
            ("table", "research_table", dict(rows=rows, question=q)),
            ("timeline", "deep_timeline", dict(term=term, months=12))]
    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(lambda j: get(j[0], j[1], **j[2]), jobs))
    hid = (D(data, "history") or {}).get("history_id")
    if hid:
        get("scenarios", "trend_scenarios", history_id=hid, horizon=3)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(data, open(path, "w"), ensure_ascii=False, indent=1, default=str)
    json.dump(list((data.get("_mcp") or {}).values()), open(os.path.join(OUT, slug, "mcp_calls.json"), "w"), indent=1, default=str)
    return data


# ─────────────────────────────────────────── text ───────────────────────────────────────────
_AUD_SYS = """You are writing a topic intelligence report from measured news and research data for three readers, named
in the facts as readers[0], readers[1], readers[2]. readers[0] cares about trajectory, scale, geography and what to act
on; readers[1] about what the evidence says on the claims that affect their decisions, how strong it is and what is
contested; readers[2] about how the literature frames itself, what is new and what is thin or missing. Use only the
facts. Quote figures exactly as given with what they measure; do not compute differences or percentages. A screening
row without a value means no figure was found, not no effect. Counts are of articles or papers in the index. Theme
shares are shares of the topic's themed coverage within each year. Never give investment, legal or medical advice.
Return JSON: {"themes_time": "3-4 sentences on how the themes moved from 2021 to 2025, naming each theme with its share in the first and last year exactly as given",
"aud0": "5-6 sentences for readers[0]", "aud0_points": ["4 to 5 short things to watch or act on"],
"aud1": "5-6 sentences for readers[1]", "aud1_points": ["4 to 5 short evidence points, each naming its source tier where given"],
"aud2": "5-6 sentences for readers[2]", "aud2_points": ["4 to 5 open questions the data points to"]}"""


def facts(slug, data, TY):
    title, dom = TOPICS[slug][:2]
    claim, a, b, rows, q = RESEARCH[slug]
    obs, fut, sc = series(data)
    E = evidence_view(data)
    cp = D(data, "compare") or {}
    rd, br, st, bf = D(data, "radar") or {}, D(data, "browse") or {}, D(data, "stance") or {}, D(data, "brief") or {}
    g, cr = D(data, "geo") or {}, D(data, "critical") or {}
    F = {"topic": title, "domain": dom, "readers": AUDIENCES[dom],
         "theme_share_by_year_pct": {str(y): {k: v for k, v in TY[y].items() if v} for y in TY},
         "research_volumes": {k: {"n": v.get("n"), "window": v.get("window"), "what": v.get("what")} for k, v in (bf.get("volumes") or {}).items()},
         "literature_mix": bf.get("what_is_contested"),
         "key_numbers": [{k: x.get(k) for k in ("value", "measures", "population")} for x in (bf.get("key_numbers") or [])[:6]],
         "research_per_year": dict(obs), "scenario_baseline": sc.get("selected_baseline"),
         "scenarios": [{k: round(f[k]) if k != "year" else f[k] for k in ("year", "central", "lower_sensitivity", "upper_sensitivity")} for f in fut],
         "stories_that_matter": [(str(x.get("published") or "")[:10], str(x.get("title") or "")[:140]) for x in (cr.get("articles") or [])[:6]],
         "where_studied": [(r.get("country"), r.get("papers")) for r in ((g.get("research_authorship") or {}).get("rows") or [])[:8]],
         "claim": claim, "claim_documents_by_verdict": E["verdicts"], "claim_documents_by_tier": E["tiers"],
         "claim_corpus_stance": {k: E["corpus_stance"].get(k) for k in ("papers", "sides", "contested_pct", "reading")},
         "counter_evidence": {"tally": E["counter_tally"], "recommendation": E["counter_reco"]},
         "claim_sources_by_tier": E["by_tier"], "claim_top_sources": [{k: x.get(k) for k in ("title", "year", "tier", "cited_by")} for x in E["ranked"][:4]],
         "head_to_head": {k: ({kk: cp[k].get(kk) for kk in ("claim", "papers_both_poles", "corpus_mix", "contested_pct", "documents_read", "strongest_source")}
                              if isinstance(cp.get(k), dict) else cp.get(k)) for k in ("a", "b", "verdict")},
         "screening_question": q, "screening": [{k: r[k] for k in ("row", "value", "measures", "population", "papers", "source", "year")} for r in screening(data)],
         "framing_by_year": [{"year": x["year"], "positive_pct": x.get("positive_pct"), "contested_pct": x.get("contested_pct")} for x in st.get("points") or []],
         "frontier_new_work": [{k: x.get(k) for k in ("title", "year", "venue", "cited_by", "orientation")} for x in (rd.get("new_work") or [])[:6]],
         "framing_shift": rd.get("framing_shift"),
         "gaps": [{"component": x["component"], "evidence": x["evidence"]} for x in (D(data, "gaps") or {}).get("components") or []],
         "facets": {k: (br.get("facets") or {}).get(k) for k in ("orientation", "contribution", "topics")},
         "most_cited_since_2020": [{k: x.get(k) for k in ("title", "year", "cited_by", "orientation", "contribution")} for x in (br.get("papers") or [])[:6]],
         "where_reported_by_country": [(r.get("label") or r.get("country"), r.get("articles")) for r in
                                       ((((D(data, "overview") or {}).get("geography") or {}).get("countries") or {}).get("rows") or [])[:8]]}
    return F


def write(slug, data, TY):
    from pagewriter import write as _w
    F = facts(slug, data, TY)
    text = _w(_AUD_SYS, F, ("themes_time", "aud0", "aud0_points", "aud1", "aud1_points", "aud2", "aud2_points"))
    M = {m[0]: {"method": m[1], "question": m[2], "how": m[4]} for m in METHODS}
    pick = {"triangulation": ("claim", "claim_documents_by_verdict", "claim_documents_by_tier", "claim_corpus_stance", "counter_evidence",
                              "claim_sources_by_tier", "claim_top_sources"),
            "head_to_head": ("head_to_head",), "screening": ("screening_question", "screening"), "framing": ("framing_by_year",),
            "frontier": ("frontier_new_work", "framing_shift"), "gaps": ("claim", "gaps"),
            "history": ("research_per_year", "scenarios", "scenario_baseline"), "geography": ("where_studied", "where_reported_by_country"),
            "facets": ("facets", "most_cited_since_2020")}
    for k, keys in pick.items():
        M[k]["result"] = {x: F[x] for x in keys}
    text.update(_w(disease_intel._METH_SYS.replace("for one disease", "for one topic").replace("for this disease", "for this topic"),
                   {"topic": F["topic"], "methods": M}, [m[0] for m in METHODS] + ["workflow"]))
    return F, text


# ─────────────────────────────────────────── new tabs ───────────────────────────────────────────
def new_tabs(slug, data, text, TY, keep):
    title, dom, term = TOPICS[slug][:3]
    claim, a, b, rows, q = RESEARCH[slug]
    R = AUDIENCES[dom]
    T = []
    if keep:
        cells = [{"year": str(y), "theme": k, "v": TY[y][k]} for y in YEARS for k in keep]
        T.append(("Themes over 5 years", f"<div class='card'><p>{escape(text.get('themes_time', ''))}</p>"
                  + heatmap("ti_th5", cells, "year", "theme", f"{title}: share of themed coverage by year", xs=[str(y) for y in YEARS], ys=keep)
                  + stacked("ti_thst", cells, "How the theme mix shifted, 2021 to 2025")
                  + "<p class='note'>Shares of the topic's themed news coverage within each calendar year (news.themes, one MCP call per year). "
                    "A blank cell means the theme was not among that year's top themes.</p></div>"))
    # reader 0: trajectory, scenarios, geography, the stories that matter
    obs, fut, sc = series(data)
    g, cr = D(data, "geo") or {}, D(data, "critical") or {}
    h = f"<p>{escape(text.get('aud0', ''))}</p>" + (("<h3>What to watch or act on</h3>" + _ul(text.get("aud0_points"))) if text.get("aud0_points") else "")
    if obs:
        h += scenario_chart("ti_sc", obs, fut, f"Research on {title.lower()} per year, with backtested scenarios")
        if fut:
            h += (f"<p class='note'>Baseline {escape(str(sc.get('selected_baseline')))}, chosen by one-step-ahead backtests. "
                  "The band is a sensitivity range, not a confidence interval; it extrapolates counts of papers.</p>")
    sa = ((g.get("research_authorship") or {}).get("rows") or [])[:10]
    if sa:
        h += vbar("ti_ws", [(r["country"], r["papers"]) for r in sa], f"Where the research is done (first author), claim: {claim}", "#2a78d6", xtitle="papers")
    if cr.get("articles"):
        h += "<h3>The stories that matter (by priority, not recency)</h3>" + table(
            [(str(x.get("published") or "")[:10], x.get("publisher") or "", str(x.get("title") or "")[:150], x.get("tone") or "") for x in cr["articles"][:8]], ["Date", "Outlet", "Headline", "Tone"])
    T.append((f"For {R[0].lower()}", "<div class='card'>" + h + "</div>"))
    # reader 1: evidence on the claims that affect their decisions
    SC, E, cp = screening(data), evidence_view(data), D(data, "compare") or {}
    h = f"<p>{escape(text.get('aud1', ''))}</p>" + (("<h3>Evidence points</h3>" + _ul(text.get("aud1_points"))) if text.get("aud1_points") else "")
    if isinstance(cp.get("a"), dict) and isinstance(cp.get("b"), dict):
        h += f"<h3>Head to head: {escape(cp.get('verdict') or '')}</h3>" + mix_bars("ti_hh", [(cp["a"]["claim"], cp["a"].get("corpus_mix")), (cp["b"]["claim"], cp["b"].get("corpus_mix"))],
                                                                                 "Stance mix of the papers on each claim")
        h += table([(x["claim"], x.get("papers_both_poles"), f"{x.get('contested_pct')}%", (x.get("strongest_source") or {}).get("tier") or "",
                     str((x.get("strongest_source") or {}).get("title") or "")[:110]) for x in (cp["a"], cp["b"])],
                   ["Claim", "Papers on both sides", "Contested", "Strongest tier", "Strongest source"])
    if SC:
        h += f"<h3>Screen: “{escape(q.replace('{row}', '…'))}”</h3>" + vbar("ti_scr", [(r["row"], r["papers"]) for r in SC], "Papers behind each row's answer", "#1baf7a", xtitle="papers")
        h += table([(r["row"], r["value"] or "no figure found", r["measures"] or (r["reason"] or ""), (r["source"] or "")[:100] + (f" ({r['year']})" if r["year"] else ""))
                    for r in SC], ["Row", "Figure (quoted)", "Measures", "Source"])
    if E["documents"]:
        h += f"<h3>Evidence for “{escape(claim)}”</h3><div style='display:flex;flex-wrap:wrap;gap:18px'>"
        h += disease_intel.donut("ti_dv", list(E["verdicts"].items()), "Documents read, by verdict") + disease_intel.donut("ti_dt", list(E["tiers"].items()), "…by tier") + "</div>"
        h += table([(d.get("verdict") or d.get("stance") or "", d.get("tier") or "", str(d.get("title") or "")[:130], d.get("year")) for d in E["documents"][:8]],
                   ["Verdict", "Tier", "Document", "Year"])
        if E["counter_reco"]:
            h += f"<p class='note'>Counter-evidence check: {escape(E['counter_reco'])}</p>"
    T.append((f"For {R[1].lower()}", "<div class='card'>" + h + "</div>"))
    # reader 2: framing, frontier, shape of the literature, gaps
    st, rd, br, gp = D(data, "stance") or {}, D(data, "radar") or {}, D(data, "browse") or {}, D(data, "gaps") or {}
    h = f"<p>{escape(text.get('aud2', ''))}</p>" + (("<h3>Open questions</h3>" + _ul(text.get("aud2_points"))) if text.get("aud2_points") else "")
    if st.get("points"):
        h += stance_area("ti_sa", st["points"], "How the literature frames its findings, by year")
    if rd.get("new_work"):
        h += "<h3>Frontier: most-cited work since 2022</h3>" + table([(str(x.get("title") or "")[:130], x["year"], x.get("venue") or "", x.get("cited_by") or 0, x.get("orientation") or "")
                                                                    for x in rd["new_work"][:8]], ["Paper", "Year", "Venue", "Cited by", "Framing"])
    fa = br.get("facets") or {}
    if fa.get("topics"):
        h += vbar("ti_tp", [(x["topic"], x["papers"]) for x in fa["topics"][:10]], "Topics inside the literature (since 2020)", "#2a78d6", xtitle="papers")
    if fa.get("orientation") or fa.get("contribution"):
        h += "<div style='display:flex;flex-wrap:wrap;gap:18px'>" + (disease_intel.donut("ti_fo", [(x["orientation"], x["papers"]) for x in fa.get("orientation") or []], "Papers by orientation") if fa.get("orientation") else "") \
             + (disease_intel.donut("ti_fc", [(x["contribution"], x["papers"]) for x in fa.get("contribution") or []], "…by contribution") if fa.get("contribution") else "") + "</div>"
    if gp.get("components"):
        h += f"<h3>Gap map for “{escape(claim)}”</h3>" + table([(x["component"], x["evidence"], x.get("means") or "") for x in gp["components"]], ["Component", "Literature?", "Means"])
    T.append((f"For {R[2].lower()}", "<div class='card'>" + h + "</div>"))
    # methods
    calls = data.get("_mcp") or {}
    h = ("<div class='card'><h3>Nine ways to explore the research, run on this topic</h3><p>Each method is one or two MCP calls: "
         "the question it answers, the call exactly as made, what came back and a reading of that result.</p>"
         + (f"<p><b>Chaining them.</b> {escape(text['workflow'])}</p>" if text.get("workflow") else "") + "</div>")
    for mid, name, qq, keys, how in METHODS:
        qq = TOPIC_Q.get(mid, qq)
        if not any((data.get(k) or {}).get("ok") for k in keys):
            continue
        cj = "\n".join(json.dumps({"tool": calls[k]["tool"], "arguments": calls[k]["args"]}, ensure_ascii=False) for k in keys if k in calls)
        h += (f"<div class='card'><div class='sig'>Method</div><h3>{escape(name)}</h3><p><b>Question.</b> {escape(qq)}</p><p><b>How.</b> {escape(how)}</p>"
              f"<pre class='code'>{escape(cj)}</pre>" + method_result(mid, data) + (f"<p><b>Reading.</b> {escape(text[mid])}</p>" if text.get(mid) else "") + "</div>")
    T.append(("Research methods", h))
    T.append(("Built with MCP", "<div class='card'><p>Every panel in this report is the result of one of these Prism MCP tool calls, made over MCP "
              "(streamable HTTP) as an assistant would make them.</p>"
              + table([(c["tool"], json.dumps(c["args"], ensure_ascii=False)[:120], f"{c['seconds']} s", "ok" if c["ok"] else "no data")
                       for c in calls.values()], ["MCP tool", "Arguments", "Time", "Result"]) + "</div>"))
    return T


def all_tabs(slug, data, text, TY, keep):
    old = [(n, h) for n, h in _TP_TABS(slug, data, text) if n != "Research & outlook"]   # its panels moved into the reader views
    new = new_tabs(slug, data, text, TY, keep)
    head = old[:2]                     # Overview, Areas & themes
    tail = [x for x in old[2:] if x[0] != "Month by month"]
    month = [x for x in old if x[0] == "Month by month"]
    themes = [x for x in new if x[0] == "Themes over 5 years"]
    rest = [x for x in new if x[0] != "Themes over 5 years"]
    return head + themes + rest[:3] + tail + [rest[3]] + month + rest[4:]


CHART_SHOTS = [("ti_th5", "themes-over-years"), ("ti_thst", "theme-mix"), ("ti_sc", "research-scenarios"), ("ti_ws", "where-studied"),
               ("ti_hh", "head-to-head"), ("ti_scr", "screen"), ("ti_dv", "evidence-verdicts"), ("ti_sa", "framing-by-year"), ("ti_tp", "research-topics")]


class shot_lock:
    """one headless Chrome at a time across processes too (two report builders at once left chart folders empty)"""
    def __enter__(self):
        import fcntl
        self.f = open("/tmp/prism_chart_shots.lock", "w")
        fcntl.flock(self.f, fcntl.LOCK_EX)

    def __exit__(self, *a):
        self.f.close()


def chart_pngs(slug):
    d = os.path.join(OUT, slug)
    shutil.rmtree(os.path.join(d, "charts"), ignore_errors=True)
    os.makedirs(os.path.join(d, "charts"))
    with _SHOT, shot_lock():
        subprocess.run(["node", os.path.join(HERE, "chart_shots.js"), os.path.join(d, "page", "index.html"), os.path.join(d, "charts"),
                        ",".join(f"{a}:{b}" for a, b in CHART_SHOTS)], capture_output=True, text=True, timeout=300)
    return [f for f in os.listdir(os.path.join(d, "charts")) if f.endswith(".png")]


def readme_extra(slug, data, text, names, pngs, TY, keep):
    """rewrite the topic README with the upgraded sections around topic_pages' own write-up"""
    title, dom, term = TOPICS[slug][:3]
    claim, a, b, rows, q = RESEARCH[slug]
    R = AUDIENCES[dom]
    img = lambda n, alt: [f"![{alt}](charts/{n}.png)", ""] if f"{n}.png" in pngs else []
    p = os.path.join(OUT, slug, "README.md")
    base = open(p).read()
    base = base.replace("*Prism topic intelligence*", f"*Prism topic intelligence for {', '.join(R[:2]).lower()} and {R[2].lower()}* · built from **{len(data.get('_mcp') or {})} MCP calls**")
    cut = base.find("![The interactive page](screenshot.jpg)")
    top, bottom = (base[:cut], base[cut:]) if cut > 0 else (base, "")
    import re
    top = re.sub(r"\(tabs: [^)]*\)", f"(tabs: {' · '.join(names)})", top, count=1)
    L = []
    if os.path.exists(os.path.join(OUT, slug, "theme-race.gif")) or keep:
        L += ["## Themes over five years", "", text.get("themes_time", ""), ""]
        if os.path.exists(os.path.join(OUT, slug, "theme-race.gif")):
            L += [f"![{title}: how its themes changed, 2021 to 2025, animated](theme-race.gif)", ""]
        L += img("themes-over-years", "Theme share by year") + img("theme-mix", "Theme mix over time")
        if keep:
            L += ["| Theme | " + " | ".join(str(y) for y in YEARS) + " |", "| --- |" + " ---: |" * len(YEARS)]
            L += [f"| {k} | " + " | ".join(f"{TY[y][k]}%" if TY[y][k] else "–" for y in YEARS) + " |" for k in keep] + [""]
    L += [f"## For {R[0].lower()}", "", text.get("aud0", ""), ""] + [f"- {x}" for x in text.get("aud0_points") or []] + [""]
    L += img("research-scenarios", "Research per year with scenarios") + img("where-studied", "Where the research is done")
    L += [f"## For {R[1].lower()}", "", text.get("aud1", ""), ""] + [f"- {x}" for x in text.get("aud1_points") or []] + [""]
    cp = D(data, "compare") or {}
    if isinstance(cp.get("a"), dict):
        L += [f"**Head to head:** {cp['a']['claim']} vs {cp['b']['claim']}: {cp.get('verdict')}.", ""] + img("head-to-head", "Head to head")
    SC = screening(data)
    if SC:
        L += [f"**Screen:** *{q.replace('{row}', '…')}* (one row per line below)", "", "| Row | Figure (quoted) | Measures | Source |", "| --- | --- | --- | --- |"]
        L += [f"| {r['row']} | {r['value'] or 'no figure found'} | {r['measures'] or ''} | {(r['source'] or '')[:90]}{' (%s)' % r['year'] if r['year'] else ''} |" for r in SC] + [""]
    L += img("evidence-verdicts", "Evidence by verdict")
    L += [f"## For {R[2].lower()}", "", text.get("aud2", ""), ""] + [f"- {x}" for x in text.get("aud2_points") or []] + [""]
    L += img("framing-by-year", "Framing by year") + img("research-topics", "Topics inside the literature")
    L += ["## Research exploration methods", "", "Nine ways to explore the research, each run on this topic; the interactive report shows each call and its result.", ""]
    if text.get("workflow"):
        L += [f"**Chaining them.** {text['workflow']}", ""]
    for mid, name, qq, keys, how in METHODS:
        qq = TOPIC_Q.get(mid, qq)
        if text.get(mid):
            L += [f"### {name}", "", f"*{qq}* `{'` + `'.join((data.get('_mcp') or {}).get(k, {}).get('tool', k) for k in keys)}`", "", text[mid], ""]
    calls = list((data.get("_mcp") or {}).values())
    L += ["## Built with MCP", "", f"Every number and chart on this page comes from these {len(calls)} Prism MCP tool calls, made over MCP (streamable HTTP). "
          "Arguments and timings: [mcp_calls.json](mcp_calls.json); responses: [data.json](data.json).", "", "| MCP tool | Calls |", "| --- | ---: |"]
    cnt = {}
    for c in calls:
        cnt[c["tool"]] = cnt.get(c["tool"], 0) + 1
    L += [f"| `{t}` | {n} |" for t, n in cnt.items()] + [""]
    bottom = re.sub(r"\*\*How this page is built\.\*\*.*?Data: \[data\.json\]\(data\.json\)\.\n\n", "", bottom, flags=re.S)
    banner = f"> **Partial index.** {BANNER}\n\n" if partial(data) else ""
    i = top.find("\n\n", top.find("trend.gif")) + 2 if "trend.gif" in top else 0
    top = top[:i] + banner + top[i:]
    open(p, "w").write(top + "\n".join(L) + "\n" + bottom)


def build(slug, refresh=False, write_only=False, workers=4):
    data = json.load(open(os.path.join(OUT, slug, "data.json"))) if write_only else collect(slug, refresh, workers)
    if not D(data, "overview"):
        print(f"{slug}: no overview, skipped", flush=True)
        return None
    TY, keep = theme_years(data)
    keep = [k for k in keep if sum(1 for y in YEARS if TY[y][k]) >= 2]
    wp = os.path.join(OUT, slug, "writeup.json")
    if write_only and os.path.exists(wp) and json.load(open(wp)).get("v") == 2:
        text = json.load(open(wp))["text"]
    else:
        F0, text = tp.write(slug, data)
        F1, t1 = write(slug, data, TY)
        text.update(t1)
        json.dump({"v": 2, "facts": {"topic": F0, "intel": F1}, "text": text}, open(wp, "w"), ensure_ascii=False, indent=1, default=str)
    from pagewriter import clean
    text = clean(text)
    d = os.path.join(OUT, slug)
    os.makedirs(os.path.join(d, "page"), exist_ok=True)
    for f in ("world_india_official.geojson", "india_states_official.geojson"):
        shutil.copy(os.path.join(ASSETS, f), os.path.join(d, "page", f))
    tp.tabs = lambda s, dt, tx: all_tabs(s, dt, tx, TY, keep)
    try:
        html, names = tp.page(slug, data, text)
    finally:
        tp.tabs = _TP_TABS
    extra = (".code{background:#f0efe9;border-radius:8px;padding:10px;font:12px/1.45 ui-monospace,Menlo,monospace;white-space:pre-wrap;overflow-x:auto}"
             "@media (prefers-color-scheme:dark){.code{background:#22262c}}")
    html = html.replace("</style>", extra + "</style>", 1).replace("· Prism topic intelligence</p>",
                                                                   f"· Prism topic intelligence · built from {len(data.get('_mcp') or {})} MCP calls</p>", 1)
    if partial(data):
        html = html.replace('<div class="kpis">', f'<p class="m"><b>Partial index.</b> {escape(BANNER)}</p><div class="kpis">', 1)
    open(os.path.join(d, "page", "index.html"), "w").write(html)
    F0 = tp.facts(slug, data)
    tp.gif(slug, data)
    if keep:
        from gifs import race_gif
        with _GIF:
            race_gif({str(y): [(k, TY[y][k] or 0) for k in keep[:8]] for y in YEARS}, f"{TOPICS[slug][0]}: themes, 2021 to 2025",
                     os.path.join(d, "theme-race.gif"), subtitle="Share of themed news coverage, % per year")
    tp.readme(slug, data, F0, text, names)
    pngs = chart_pngs(slug)
    readme_extra(slug, data, text, names, pngs, TY, keep)
    with _SHOT:
        shot(os.path.join(d, "page", "index.html"), os.path.join(d, "screenshot.jpg"))
    print(f"{slug}: tabs {names}; charts {len(pngs)}", flush=True)
    return names


def safe_build(*a):
    """one report's failure is logged and the batch goes on"""
    import traceback
    try:
        return build(*a)
    except Exception:
        print(f"{a[0]}: BUILD FAILED\n{traceback.format_exc()}", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=1)
    ap.add_argument("--calls", type=int, default=4)
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--write-only", action="store_true")
    a = ap.parse_args()
    slugs = a.only.split(",") if a.only else list(TOPICS)
    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(lambda s: safe_build(s, a.refresh, a.write_only, a.calls), slugs))
    tp.index()
    print("TOPIC_INTEL_DONE", flush=True)
