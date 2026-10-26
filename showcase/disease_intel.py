"""Disease intelligence reports, built entirely from Prism MCP calls, with one view per reader and a research-methods tab.

  * For policy makers: burden and attention. Research volume 2017-2025 with backtested scenarios to 2028, news
    coverage, where the disease is studied vs reported, causes and impacts named in coverage, the stories that matter.
  * For doctors: risk factors screened across rows with their effect sizes, the evidence behind one clinical claim
    (read and tiered), what disagrees with it, two interventions measured the same way, and the claims corpus
    (risk factors, protective factors, treatments) with its high-tier share.
  * For scientists: how the literature frames its findings year by year, the frontier (most-cited new work, framing
    shift, under-covered topics), the shape of the literature (orientation, contribution, topics), and the gaps.
  * Research exploration methods: nine ways to explore the research through Prism, each with the question it
    answers, the MCP call, the result for this disease, a reading of that result, and its limits.

Every panel is an MCP tool call (showcase/mcpcall.py); the report ends with the list of calls.

    python3 showcase/disease_intel.py [--only tuberculosis,...] [--workers 1] [--write-only]
Writes docs/diseases/<slug>/{README.md, data.json, writeup.json, mcp_calls.json, risk-factors.gif, charts/*.png,
screenshot.jpg, page/index.html} (the GitHub demo pages; page/ is hosted as the interactive copy), the
docs/diseases/README.md index and the disease section of the repo README.
"""
import argparse
import json
import os
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
from topic_pages import fmt  # noqa: E402
from intel_reports import _embed, donut, partial, BANNER  # noqa: E402
import mcpcall  # noqa: E402

OUT = os.path.join(ROOT, "docs", "diseases")
HOST = "https://fliarbi.com/demo/docs/prism-dashboards-3bb43e4c/diseases"
NOTICE = ("Research intelligence, not medical advice: counts, framings and effect sizes are measured from the research "
          "and news index and quoted from their sources; they do not replace clinical guidelines or a clinician's judgement.")
_SHOT = threading.Lock()

# term, risk claim (policy + methods), screening rows + question (doctors), clinical claim (evidence + counter),
# two interventions for the head-to-head, a number to look for (policy)
DISEASES = {
    "tuberculosis": dict(
        name="Tuberculosis", term="tuberculosis", risk="Diabetes increases the risk of tuberculosis",
        rows=["diabetes", "smoking", "HIV", "malnutrition", "alcohol use", "air pollution"],
        question="Does {row} increase the risk of tuberculosis?",
        clinical="Isoniazid preventive therapy reduces tuberculosis incidence in people with HIV",
        a="Xpert MTB/RIF improves the diagnosis of tuberculosis", b="Chest radiography screening detects tuberculosis",
        stat="Tuberculosis incidence"),
    "type-2-diabetes": dict(
        name="Type 2 diabetes", term="type 2 diabetes", risk="Obesity increases the risk of type 2 diabetes",
        rows=["obesity", "physical inactivity", "sugar-sweetened beverages", "short sleep duration", "smoking", "air pollution"],
        question="Does {row} increase the risk of type 2 diabetes?",
        clinical="SGLT2 inhibitors reduce hospitalisation for heart failure in type 2 diabetes",
        a="SGLT2 inhibitors reduce cardiovascular events in type 2 diabetes",
        b="GLP-1 receptor agonists reduce cardiovascular events in type 2 diabetes", stat="Prevalence of type 2 diabetes"),
    "breast-cancer": dict(
        name="Breast cancer", term="breast cancer", risk="Obesity increases the risk of breast cancer",
        rows=["obesity", "alcohol consumption", "hormone replacement therapy", "night shift work", "physical inactivity", "breastfeeding"],
        question="Is {row} associated with the risk of breast cancer?",
        clinical="Mammography screening reduces breast cancer mortality",
        a="Mammography screening reduces breast cancer mortality",
        b="Breast MRI screening improves cancer detection in high-risk women", stat="Breast cancer incidence"),
    "dengue": dict(
        name="Dengue", term="dengue", risk="Rising temperature increases dengue transmission",
        rows=["temperature", "rainfall", "urbanisation", "water storage containers", "climate change", "prior dengue infection"],
        question="Is {row} associated with dengue risk?",
        clinical="Wolbachia mosquito releases reduce dengue incidence",
        a="Wolbachia mosquito releases reduce dengue incidence", b="Dengue vaccination reduces hospitalisation for dengue",
        stat="Dengue incidence"),
    "hypertension": dict(
        name="Hypertension", term="hypertension", risk="High salt intake increases the risk of hypertension",
        rows=["salt intake", "obesity", "alcohol consumption", "physical inactivity", "air pollution", "psychological stress"],
        question="Does {row} increase the risk of hypertension?",
        clinical="Salt reduction lowers blood pressure",
        a="Salt reduction lowers blood pressure", b="Potassium supplementation lowers blood pressure",
        stat="Prevalence of hypertension"),
    "alzheimers-disease": dict(
        name="Alzheimer's disease", term="alzheimer", risk="Hypertension increases the risk of Alzheimer's disease",
        rows=["hypertension", "diabetes", "hearing loss", "physical inactivity", "air pollution", "low education"],
        question="Is {row} associated with the risk of Alzheimer's disease or dementia?",
        clinical="Anti-amyloid antibodies slow cognitive decline in Alzheimer's disease",
        a="Anti-amyloid antibodies slow cognitive decline in Alzheimer's disease",
        b="Physical exercise slows cognitive decline in older adults", stat="Prevalence of Alzheimer's disease"),
    "malaria": dict(
        name="Malaria", term="malaria", risk="Rainfall increases malaria transmission",
        rows=["rainfall", "temperature", "insecticide-treated bed net use", "proximity to water bodies", "poor housing", "deforestation"],
        question="Is {row} associated with malaria risk?",
        clinical="Insecticide-treated nets reduce malaria incidence",
        a="Insecticide-treated nets reduce malaria incidence", b="The RTS,S vaccine reduces clinical malaria in children",
        stat="Malaria incidence"),
    "copd": dict(
        name="COPD", term="chronic obstructive pulmonary disease", risk="Biomass fuel smoke increases the risk of COPD",
        rows=["smoking", "biomass fuel smoke", "outdoor air pollution", "occupational dust", "asthma", "tuberculosis"],
        question="Does {row} increase the risk of chronic obstructive pulmonary disease?",
        clinical="Pulmonary rehabilitation improves quality of life in COPD",
        a="Pulmonary rehabilitation improves quality of life in COPD", b="Inhaled corticosteroids reduce COPD exacerbations",
        stat="Prevalence of COPD"),
}

METHODS = [
    ("triangulation", "Evidence triangulation", "Is a clinical claim supported, and by how strong a design?",
     ["evidence", "counter", "rank"], "find_evidence reads and tiers the documents for the claim; find_counter_evidence looks for what disagrees; rank_sources orders the sources on the evidence ladder."),
    ("head_to_head", "Head-to-head claims", "Which of two interventions has more and stronger evidence?",
     ["compare"], "compare_claims measures both claims the same way: papers on both poles, the corpus stance mix, the documents read and the strongest source."),
    ("screening", "Cross-row screening", "Which risk factors carry a measured effect size, and how large?",
     ["table"], "research_table asks one question of many rows and returns, per row, a quoted figure with the sentence and source it came from, or says none was found."),
    ("framing", "Framing drift", "Is the literature becoming more hopeful or more cautious?",
     ["stance"], "stance_trends counts typed papers by orientation (promising, cautionary, critical, …) year by year."),
    ("frontier", "Frontier scan", "What is new, and what is the research not reaching?",
     ["radar"], "research_radar returns the most-cited new work since a start year, the framing shift between windows, and topics with many papers but little coverage."),
    ("gaps", "Gap mapping", "Which parts of a claim does the literature actually cover?",
     ["gaps"], "research_gaps splits a claim into components and checks each one for a literature."),
    ("history", "Count history and backtested scenarios", "Is research on this growing, and where could it be in three years?",
     ["history", "scenarios"], "historical_analysis counts title-matched papers per year in an explicit window; trend_scenarios backtests no-change and drift baselines one step ahead and extrapolates the better one, with a sensitivity band."),
    ("geography", "Geographic triangulation", "Where is it studied, published, reported and patented?",
     ["geo", "newsgeo"], "global_comparison returns four separate country lanes for the claim; news_geography adds where the coverage is about. The lanes answer different questions and are never added together."),
    ("facets", "Faceted browsing", "What kind of literature is it: empirical, review, position? Problem-identifying or promising?",
     ["browse"], "browse_research filters papers by how they frame their findings and returns facets by orientation, contribution, year and topic, sorted by citations."),
]


def D(data, key):
    d = data.get(key) or {}
    return d.get("data") if d.get("ok") else None


def collect(slug, refresh=False, workers=4):
    s = DISEASES[slug]
    path = os.path.join(OUT, slug, "data.json")
    data = json.load(open(path)) if os.path.exists(path) and not refresh else {}
    lock = threading.Lock()

    def get(key, tool, **args):
        d = data.get(key) or {}
        if d.get("ok") and key in (data.get("_mcp") or {}):
            return
        t0 = time.time()
        env = mcpcall.call(tool, args)
        rec = {"key": key, "tool": tool, "args": args, "seconds": round(time.time() - t0, 1), "ok": bool(env.get("ok"))}
        with lock:
            data[key] = env
            data.setdefault("_mcp", {})[key] = rec
        print(f"  {slug} {key}: {rec['ok']} {rec['seconds']}s", flush=True)
    jobs = [("profile", "disease_profile", dict(disease=s["term"])),
            ("brief", "research_brief", dict(topic=s["term"])),
            ("stance", "stance_trends", dict(term=s["term"])),
            ("browse", "browse_research", dict(term=s["term"], sort="citations", since=2020, limit=12)),
            ("radar", "research_radar", dict(topic=s["term"], since_year=2022)),
            ("gaps", "research_gaps", dict(claim=s["risk"])),
            ("history", "historical_analysis", dict(subject_phrases=[s["term"]], query_seconds=30)),
            ("geo", "global_comparison", dict(claim=s["risk"])),
            ("news", "news_trends", dict(term=s["term"], since="2024-06-01")),
            ("newsgeo", "news_geography", dict(term=s["term"], since="2024-06-01")),
            ("factors", "news_factors", dict(topic=s["term"])),
            ("critical", "critical_news", dict(term=s["term"], limit=8)),
            ("table", "research_table", dict(rows=s["rows"], question=s["question"])),
            ("evidence", "find_evidence", dict(claim=s["clinical"], limit=10)),
            ("counter", "find_counter_evidence", dict(claim=s["clinical"], limit=10)),
            ("rank", "rank_sources", dict(claim=s["risk"])),
            ("compare", "compare_claims", dict(claim_a=s["a"], claim_b=s["b"])),
            ("stats", "find_statistics", dict(claim=s["stat"])),
            ("timeline", "deep_timeline", dict(term=s["term"], months=12))]
    with ThreadPoolExecutor(workers) as ex:
        list(ex.map(lambda j: get(j[0], j[1], **j[2]), jobs))
    hid = (D(data, "history") or {}).get("history_id")
    if hid:
        get("scenarios", "trend_scenarios", history_id=hid, horizon=3)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    json.dump(data, open(path, "w"), ensure_ascii=False, indent=1, default=str)
    json.dump(list((data.get("_mcp") or {}).values()), open(os.path.join(OUT, slug, "mcp_calls.json"), "w"), indent=1, default=str)
    return data


# ─────────────────────────────────────────── derived views ───────────────────────────────────────────
def screening(data):
    """research_table rows: (factor, value, measures, papers, source title, year, url) for the answered rows"""
    out = []
    for r in (D(data, "table") or {}).get("rows") or []:
        src = r.get("top_source") or {}
        out.append({"row": r["row"], "answered": bool(r.get("available") and r.get("value")), "value": r.get("value"),
                    "measures": r.get("measures"), "population": r.get("population"), "papers": r.get("papers") or 0,
                    "sentence": r.get("sentence"), "source": src.get("title"), "year": src.get("year"), "url": src.get("url"),
                    "reason": r.get("reason")})
    return out


def evidence_view(data):
    ev, ct, rk = D(data, "evidence") or {}, D(data, "counter") or {}, D(data, "rank") or {}
    docs = ev.get("documents") or []
    verdicts = {}
    for d in docs:
        v = d.get("verdict") or d.get("stance") or "unread"
        verdicts[v] = verdicts.get(v, 0) + 1
    tiers = {}
    for d in docs:
        tiers[d.get("tier") or "other"] = tiers.get(d.get("tier") or "other", 0) + 1
    return {"documents": docs, "verdicts": verdicts, "tiers": tiers, "corpus_stance": ev.get("corpus_stance") or {},
            "counter_tally": (ct.get("tally") or {}).get("counts") or {}, "counter_mix": ct.get("corpus_mix") or {},
            "counter_reco": ct.get("recommendation"), "contradicting": ct.get("contradicting") or [],
            "ranked": rk.get("sources") or [], "by_tier": rk.get("by_tier") or {}}


def series(data):
    h = D(data, "history") or {}
    sc = D(data, "scenarios") or {}
    obs = [(str(x["year"]), x["value"]) for x in h.get("series") or []]
    fut = sc.get("scenarios") or []
    return obs, fut, sc


# ─────────────────────────────────────────── charts ───────────────────────────────────────────
def scenario_chart(id_, obs, fut, title):
    vals = [{"year": y, "v": v, "k": "observed"} for y, v in obs]
    if obs and fut:
        vals.append({"year": obs[-1][0], "v": obs[-1][1], "k": "scenario (central)"})
    vals += [{"year": str(f["year"]), "v": round(f["central"]), "k": "scenario (central)", "lo": round(f["lower_sensitivity"]),
              "hi": round(f["upper_sensitivity"])} for f in fut]
    band = [{"year": str(f["year"]), "lo": round(f["lower_sensitivity"]), "hi": round(f["upper_sensitivity"])} for f in fut]
    if obs and fut:
        band.insert(0, {"year": obs[-1][0], "lo": obs[-1][1], "hi": obs[-1][1]})
    return _embed(id_, {"width": 640, "height": 280, "title": {"text": title, "anchor": "start", "fontSize": 14},
                        "layer": [{"data": {"values": band}, "mark": {"type": "area", "opacity": 0.18, "color": "#eb6834"},
                                   "encoding": {"x": {"field": "year", "type": "ordinal", "title": None, "axis": {"labelAngle": 0}},
                                                "y": {"field": "lo", "type": "quantitative", "title": "papers per year"}, "y2": {"field": "hi"}}},
                                  {"data": {"values": vals}, "mark": {"type": "line", "point": True, "strokeWidth": 2},
                                   "encoding": {"x": {"field": "year", "type": "ordinal"}, "y": {"field": "v", "type": "quantitative"},
                                                "color": {"field": "k", "type": "nominal", "title": None, "scale": {"range": ["#2a78d6", "#eb6834"]}},
                                                "strokeDash": {"field": "k", "type": "nominal", "legend": None, "scale": {"range": [[1, 0], [5, 4]]}},
                                                "tooltip": [{"field": "year"}, {"field": "k"}, {"field": "v", "title": "papers"}]}}]})


def stance_area(id_, points, title):
    cells = [{"year": str(p["year"]), "o": o, "v": n} for p in points for o, n in (p.get("orientation") or {}).items()]
    order = ["breakthrough", "promising", "descriptive", "comparative", "problem_identifying", "cautionary", "critical"]
    return _embed(id_, {"width": 640, "height": 280, "title": {"text": title, "anchor": "start", "fontSize": 14}, "data": {"values": cells},
                        "mark": {"type": "area", "interpolate": "monotone"},
                        "encoding": {"x": {"field": "year", "type": "ordinal", "title": None, "axis": {"labelAngle": 0}},
                                     "y": {"field": "v", "type": "quantitative", "stack": "normalize", "title": "share of typed papers", "axis": {"format": "%"}},
                                     "color": {"field": "o", "type": "nominal", "title": None, "sort": order,
                                               "scale": {"domain": order, "range": ["#0f5fb8", "#2a78d6", "#9cc3ee", "#c9c8c2", "#eda100", "#eb6834", "#b8321a"]}},
                                     "order": {"field": "o"}, "tooltip": [{"field": "year"}, {"field": "o", "title": "orientation"}, {"field": "v", "title": "papers"}]}})


def mix_bars(id_, rows, title):
    """rows: [(label, {supporting, qualifying, contradicting, neutral})] as a normalised stacked bar per label"""
    order = ["supporting", "qualifying", "neutral", "contradicting"]
    cells = [{"c": lab, "s": k, "v": (m or {}).get(k, 0)} for lab, m in rows for k in order]
    return _embed(id_, {"width": 560, "height": 34 * len(rows) + 20, "title": {"text": title, "anchor": "start", "fontSize": 14},
                        "data": {"values": cells}, "mark": {"type": "bar", "cornerRadius": 2},
                        "encoding": {"y": {"field": "c", "type": "nominal", "title": None, "axis": {"labelLimit": 300}},
                                     "x": {"field": "v", "type": "quantitative", "stack": "normalize", "title": "share of papers on both sides of the claim", "axis": {"format": "%"}},
                                     "color": {"field": "s", "type": "nominal", "title": None, "sort": order,
                                               "scale": {"domain": order, "range": ["#1baf7a", "#eda100", "#c9c8c2", "#eb6834"]}},
                                     "order": {"field": "s"}, "tooltip": [{"field": "c"}, {"field": "s"}, {"field": "v", "title": "papers"}]}})


# ─────────────────────────────────────────── text ───────────────────────────────────────────
_AUD_SYS = """You are writing a disease intelligence report from measured research and news data, in three views. Policy
makers: burden, attention, geography, trajectory, what to fund or watch. Doctors: what the evidence says about risk
factors and one clinical claim, how strong the designs are, what is contested; never prescribe, never give individual
medical advice. Scientists: how the literature frames itself, what is new, what is thin or missing, where to look next.
Use only the facts given. Effect sizes must be quoted exactly as given, with what they measure. 'contested_pct' is the
share of typed papers that qualify or contradict. A row without a value means no figure was found, not no effect.
Counts are of papers or articles in the index, not of patients or cases. Do not compute differences or percentages.
Return JSON: {"summary": "5-6 sentences across all three views",
"policy": "5-6 sentences", "policy_actions": ["4 to 5 short, concrete things a policy maker could watch or commission"],
"doctor": "5-6 sentences", "doctor_points": ["4 to 5 short evidence points a clinician could use, each naming its source tier"],
"scientist": "5-6 sentences", "scientist_questions": ["4 to 5 open research questions the data points to"]}"""

_METH_SYS = """You are a research-methods editor. For each research exploration method below you get what it does and the
result it produced for one disease. For each, write a deep reading of the result: what it shows, how to read it, what
it does NOT show, and what a careful researcher would do next. Use only the facts given; quote numbers exactly; do not
compute new ones. If a method returned nothing useful, say what that absence means. Return JSON with one key per
method id: {"<id>": "4-6 sentences", ...} plus "workflow": "4-5 sentences on how to chain these methods for this disease"."""


def facts(slug, data):
    s = DISEASES[slug]
    p, b = D(data, "profile") or {}, D(data, "brief") or {}
    st = D(data, "stance") or {}
    obs, fut, sc = series(data)
    E = evidence_view(data)
    cp = D(data, "compare") or {}
    rd = D(data, "radar") or {}
    br = D(data, "browse") or {}
    g = D(data, "geo") or {}
    ng = D(data, "newsgeo") or {}
    nw = D(data, "news") or {}
    fc = D(data, "factors") or {}
    tl = D(data, "timeline") or {}
    pts = st.get("points") or []
    F = {"disease": s["name"],
         "volumes": {k: {"n": v.get("n"), "window": v.get("window"), "what": v.get("what")} for k, v in (b.get("volumes") or {}).items()},
         "literature_mix": (b.get("what_is_contested") or {}),
         "established_reviews": [{k: x.get(k) for k in ("title", "year", "tier", "cited_by", "venue")} for x in (b.get("what_is_established") or [])[:5]],
         "key_numbers": [{k: x.get(k) for k in ("value", "measures", "population")} for x in (b.get("key_numbers") or [])[:6]],
         "claims_corpus": {"claims": p.get("claims"), "high_tier_share_pct": p.get("high_tier_share_pct"),
                           "risk_factors": [(x["factor"], x["claims"], x["high_tier_pct"]) for x in (p.get("risk_factors") or [])[:8]],
                           "protective_factors": [(x["factor"], x["claims"], x["high_tier_pct"]) for x in (p.get("protective_factors") or [])[:6]],
                           "treatments": [(x["factor"], x["claims"], x["high_tier_pct"]) for x in (p.get("treatments") or [])[:6]]},
         "research_per_year": dict(obs), "scenarios": [{k: round(f[k]) if k != "year" else f[k] for k in ("year", "central", "lower_sensitivity", "upper_sensitivity")} for f in fut],
         "scenario_baseline": sc.get("selected_baseline"),
         "framing_by_year": [{"year": x["year"], "positive_pct": x.get("positive_pct"), "contested_pct": x.get("contested_pct")} for x in pts],
         "screening_question": s["question"], "screening": [{k: r[k] for k in ("row", "value", "measures", "population", "papers", "source", "year")} for r in screening(data)],
         "clinical_claim": s["clinical"], "clinical_documents_by_verdict": E["verdicts"], "clinical_documents_by_tier": E["tiers"],
         "clinical_corpus_stance": {k: E["corpus_stance"].get(k) for k in ("papers", "sides", "contested_pct", "reading")},
         "counter_evidence": {"tally": E["counter_tally"], "recommendation": E["counter_reco"]},
         "risk_claim": s["risk"], "risk_claim_sources_by_tier": E["by_tier"],
         "risk_claim_top_sources": [{k: x.get(k) for k in ("title", "year", "tier", "cited_by")} for x in E["ranked"][:4]],
         "head_to_head": {k: ({kk: cp[k].get(kk) for kk in ("claim", "papers_both_poles", "corpus_mix", "contested_pct", "documents_read", "strongest_source")}
                              if isinstance(cp.get(k), dict) else cp.get(k)) for k in ("a", "b", "verdict")},
         "frontier_new_work": [{k: x.get(k) for k in ("title", "year", "venue", "cited_by", "orientation")} for x in (rd.get("new_work") or [])[:6]],
         "framing_shift": rd.get("framing_shift"),
         "under_covered_topics": [(x["topic"], x["papers"]) for x in (rd.get("under_covered") or [])[:6]],
         "gaps": [{"component": x["component"], "evidence": x["evidence"]} for x in (D(data, "gaps") or {}).get("components") or []],
         "facets": {k: (br.get("facets") or {}).get(k) for k in ("orientation", "contribution", "topics")},
         "most_cited_since_2020": [{k: x.get(k) for k in ("title", "year", "cited_by", "orientation", "contribution")} for x in (br.get("papers") or [])[:6]],
         "where_studied": [(r.get("country"), r.get("papers")) for r in ((g.get("research_authorship") or {}).get("rows") or [])[:8]],
         "where_reported": [(r.get("country") or r.get("label"), r.get("articles")) for r in (ng.get("rows") or [])[:8]],
         "news_articles": nw.get("total"), "news_window": f"{(nw.get('from') or '')[:7]} to {(nw.get('to') or '')[:7]}",
         "news_causes": [x["factor"] for x in (fc.get("causes") or [])[:8]], "news_impacts": [x["factor"] for x in (fc.get("impacts") or [])[:8]],
         "news_arc": tl.get("arc")}
    return F


def write(slug, data):
    from pagewriter import write as _w
    F = facts(slug, data)
    text = _w(_AUD_SYS, F, ("summary", "policy", "policy_actions", "doctor", "doctor_points", "scientist", "scientist_questions"))
    M = {m[0]: {"method": m[1], "question": m[2], "how": m[4]} for m in METHODS}
    pick = {"triangulation": ("clinical_claim", "clinical_documents_by_verdict", "clinical_documents_by_tier", "clinical_corpus_stance",
                              "counter_evidence", "risk_claim_sources_by_tier", "risk_claim_top_sources"),
            "head_to_head": ("head_to_head",), "screening": ("screening_question", "screening"), "framing": ("framing_by_year",),
            "frontier": ("frontier_new_work", "framing_shift", "under_covered_topics"), "gaps": ("risk_claim", "gaps"),
            "history": ("research_per_year", "scenarios", "scenario_baseline"), "geography": ("where_studied", "where_reported"),
            "facets": ("facets", "most_cited_since_2020")}
    for k, keys in pick.items():
        M[k]["result"] = {x: F[x] for x in keys}
    text.update(_w(_METH_SYS, {"disease": F["disease"], "methods": M}, [m[0] for m in METHODS] + ["workflow"]))
    return F, text


# ─────────────────────────────────────────── page ───────────────────────────────────────────
def _ul(items):
    return "<ul>" + "".join(f"<li>{escape(str(x))}</li>" for x in items or []) + "</ul>" if items else ""


def _src(title, year, url):
    t = escape(str(title or "")[:150]) + (f" ({year})" if year else "")
    return f"<a href='{escape(url)}'>{t}</a>" if url else t


def tabs(slug, data, text):
    s = DISEASES[slug]
    p, b = D(data, "profile") or {}, D(data, "brief") or {}
    T = []
    # Summary
    vol = b.get("volumes") or {}
    mix = (b.get("what_is_contested") or {}).get("mix") or {}
    kn = b.get("key_numbers") or []
    est = b.get("what_is_established") or []
    h = f"<p>{escape(text.get('summary', ''))}</p>"
    if mix:
        h += donut("d0", list(mix.items()), "How the literature frames its findings")
    if kn:
        h += "<h3>Key numbers, each with its source sentence</h3>" + table(
            [(x.get("value"), x.get("measures") or "", _plain_src(x.get("source"))) for x in kn[:8]], ["Figure", "Measures", "Source"])
    if est:
        h += "<h3>What is established (reviews, meta-analyses, guidelines)</h3>" + table(
            [(str(x.get("title") or "")[:120], x.get("year"), x.get("tier"), x.get("cited_by")) for x in est[:6]], ["Paper", "Year", "Tier", "Cited by"])
    h += "<p class='note'>" + escape(NOTICE) + "</p>"
    T.append(("Summary", "<div class='card'>" + h + "</div>"))

    # Policy makers
    obs, fut, sc = series(data)
    nw = D(data, "news") or {}
    g, ng = D(data, "geo") or {}, D(data, "newsgeo") or {}
    fc, cr = D(data, "factors") or {}, D(data, "critical") or {}
    h = f"<p>{escape(text.get('policy', ''))}</p>" + (("<h3>What to watch or commission</h3>" + _ul(text.get("policy_actions"))) if text.get("policy_actions") else "")
    if obs:
        h += scenario_chart("sc", obs, fut, f"Research on {s['name'].lower()} per year, with backtested scenarios to {fut[-1]['year'] if fut else ''}")
        if fut:
            h += (f"<p class='note'>Scenario baseline: {escape(str(sc.get('selected_baseline')))}, chosen by one-step-ahead backtests "
                  "(expanding window). The band is a sensitivity range, not a confidence interval; it extrapolates counts of papers, not cases.</p>")
    pts = [x for x in nw.get("points") or [] if not x.get("partial_period")]
    if pts:
        h += vline("nw", [("articles", [(x["period"][:7], x["articles"]) for x in pts]),
                          ("high-priority stories", [(x["period"][:7], x.get("critical") or 0) for x in pts])], "News coverage per month", "articles")
    lanes = []
    sa = ((g.get("research_authorship") or {}).get("rows") or [])[:10]
    if sa:
        lanes.append(vbar("ws", [(r["country"], r["papers"]) for r in sa], f"Where it is studied (first author), claim: {s['risk']}", "#2a78d6", xtitle="papers"))
    nr = [r for r in (ng.get("rows") or []) if (r.get("country") or r.get("label"))][:10]
    if nr:
        lanes.append(vbar("wr", [(r.get("country") or r.get("label"), r.get("articles") or 0) for r in nr], "Where the coverage is about", "#eb6834", xtitle="articles"))
    if lanes:
        h += "<div class='grid2'>" + "".join(f"<div>{x}</div>" for x in lanes) + "</div><p class='note'>Different lanes answer different questions; they are never added together.</p>"
    if fc.get("causes") or fc.get("impacts"):
        h += ("<div class='grid2'><div><h3>Causes named in the coverage</h3>" + table([(x["factor"], x.get("date", "")[:10], x.get("publisher") or "") for x in (fc.get("causes") or [])[:8]], ["Cause", "Date", "Outlet"])
              + "</div><div><h3>Impacts named in the coverage</h3>" + table([(x["factor"], x.get("date", "")[:10], x.get("publisher") or "") for x in (fc.get("impacts") or [])[:8]], ["Impact", "Date", "Outlet"])
              + f"</div></div><p class='note'>Each factor is quoted from an article; {fc.get('read_articles', 0)} articles were read and quotes not found in their article were rejected.</p>")
    if cr.get("articles"):
        h += "<h3>The stories that matter (by priority, not recency)</h3>" + table(
            [(str(a.get("published") or "")[:10], a.get("publisher") or "", str(a.get("title") or "")[:150], a.get("tone") or "") for a in cr["articles"][:8]], ["Date", "Outlet", "Headline", "Tone"])
    T.append(("For policy makers", "<div class='card'>" + h + "</div>"))

    # Doctors
    SC = screening(data)
    E = evidence_view(data)
    cp = D(data, "compare") or {}
    h = f"<p>{escape(text.get('doctor', ''))}</p>" + (("<h3>Evidence points</h3>" + _ul(text.get("doctor_points"))) if text.get("doctor_points") else "")
    if SC:
        h += f"<h3>Risk-factor screen: “{escape(s['question'])}”</h3>"
        h += vbar("scr", [(r["row"], r["papers"]) for r in SC], "Papers behind each row's answer", "#1baf7a", xtitle="papers")
        h += table([(r["row"], r["value"] or "no figure found", r["measures"] or (r["reason"] or ""), r["population"] or "", _src(r["source"], r["year"], None) if r["source"] else "")
                    for r in SC], ["Factor", "Effect size (quoted)", "Measures", "Population", "Source"])
    if E["documents"]:
        h += f"<h3>Clinical claim: “{escape(s['clinical'])}”</h3>"
        h += "<div style='display:flex;flex-wrap:wrap;gap:18px'>" + donut("dv", list(E["verdicts"].items()), "Documents read, by verdict") + donut("dt", list(E["tiers"].items()), "Documents read, by tier") + "</div>"
        h += table([(d.get("verdict") or d.get("stance") or "", d.get("tier") or "", str(d.get("title") or "")[:130], d.get("year"), d.get("cited_by") or 0)
                    for d in E["documents"][:10]], ["Verdict", "Tier", "Document", "Year", "Cited by"])
        cs = E["corpus_stance"]
        if cs.get("sides"):
            h += f"<p>Across {fmt(cs.get('papers'))} papers on both sides of the claim: {escape(str(cs.get('reading') or ''))} ({cs.get('contested_pct')}% qualify or contradict).</p>"
        if E["counter_reco"]:
            h += f"<p class='note'>Counter-evidence check: {escape(E['counter_reco'])}</p>"
    if isinstance(cp.get("a"), dict) and isinstance(cp.get("b"), dict):
        h += f"<h3>Head to head: {escape(cp.get('verdict') or '')}</h3>"
        h += mix_bars("hh", [(cp["a"]["claim"], cp["a"].get("corpus_mix")), (cp["b"]["claim"], cp["b"].get("corpus_mix"))], "Stance mix of the papers on each claim")
        h += table([(x["claim"], x.get("papers_both_poles"), f"{x.get('contested_pct')}%", (x.get("strongest_source") or {}).get("tier") or "",
                     str((x.get("strongest_source") or {}).get("title") or "")[:110]) for x in (cp["a"], cp["b"])],
                   ["Claim", "Papers on both sides", "Contested", "Strongest tier", "Strongest source"])
    if p.get("risk_factors"):
        h += "<h3>The claims corpus: risk factors, protective factors, treatments</h3><div class='grid2'><div>"
        h += vbar("rf", [(x["factor"], x["claims"], x["high_tier"]) for x in p["risk_factors"][:10]], "Risk factors", "#2a78d6", second=True)
        h += "</div><div>" + vbar("tx", [(x["factor"], x["claims"], x["high_tier"]) for x in (p.get("treatments") or [])[:10]], "Treatments", "#1baf7a", second=True)
        h += "</div></div><p class='note'>Orange: claims from high-tier studies (reviews and meta-analyses, randomised trials, clinical studies).</p>"
    h += "<p class='note'>" + escape(NOTICE) + "</p>"
    T.append(("For doctors", "<div class='card'>" + h + "</div>"))

    # Scientists
    st, rd, br = D(data, "stance") or {}, D(data, "radar") or {}, D(data, "browse") or {}
    gp = D(data, "gaps") or {}
    h = f"<p>{escape(text.get('scientist', ''))}</p>" + (("<h3>Open questions the data points to</h3>" + _ul(text.get("scientist_questions"))) if text.get("scientist_questions") else "")
    if st.get("points"):
        h += stance_area("sa", st["points"], "How the literature frames its findings, by year")
        h += vline("sp", [("positive %", [(str(x["year"]), x.get("positive_pct")) for x in st["points"]]),
                          ("contested %", [(str(x["year"]), x.get("contested_pct")) for x in st["points"]])], "Positive vs contested share", "% of typed papers")
    fs = rd.get("framing_shift") or {}
    if rd.get("new_work"):
        h += "<h3>Frontier: most-cited work since 2022</h3>" + table([(str(x.get("title") or "")[:130], x["year"], x.get("venue") or "", x.get("cited_by") or 0, x.get("orientation") or "") for x in rd["new_work"][:8]],
                                                                    ["Paper", "Year", "Venue", "Cited by", "Framing"])
        if fs.get("available"):
            h += f"<p>Framing shift: {escape(fs.get('reading') or '')} ({fs.get('delta_pct_points')} percentage points in the cautionary share, recent vs earlier window).</p>"
    if rd.get("under_covered"):
        h += vbar("uc", [(x["topic"], x["papers"]) for x in rd["under_covered"][:8]], "Under-covered: research topics with many papers and little coverage", "#eda100", xtitle="papers")
    fa = br.get("facets") or {}
    if fa:
        h += "<div style='display:flex;flex-wrap:wrap;gap:18px'>"
        if fa.get("orientation"):
            h += donut("fo", [(x["orientation"], x["papers"]) for x in fa["orientation"]], "Papers since 2020, by orientation")
        if fa.get("contribution"):
            h += donut("fc", [(x["contribution"], x["papers"]) for x in fa["contribution"]], "…by contribution")
        h += "</div>"
        if fa.get("topics"):
            h += vbar("tp", [(x["topic"], x["papers"]) for x in fa["topics"][:10]], "Topics inside the literature (since 2020)", "#2a78d6", xtitle="papers")
    if br.get("papers"):
        h += "<h3>Most-cited papers since 2020</h3>" + table([(str(x.get("title") or "")[:130], x["year"], x.get("cited_by") or 0, x.get("orientation") or "", x.get("contribution") or "") for x in br["papers"][:10]],
                                                            ["Paper", "Year", "Cited by", "Orientation", "Contribution"])
    if gp.get("components"):
        h += f"<h3>Gap map for “{escape(s['risk'])}”</h3>" + table([(x["component"], x["evidence"], x.get("means") or "") for x in gp["components"]], ["Component", "Literature?", "Means"])
    T.append(("For scientists", "<div class='card'>" + h + "</div>"))

    # Methods
    calls = data.get("_mcp") or {}
    h = ("<div class='card'><h3>Nine ways to explore the research, run on this disease</h3><p>Each method below is one or two MCP calls. "
         "The card gives the question it answers, the call exactly as made, what came back, a reading of that result and its limits.</p>"
         + (f"<p><b>Chaining them.</b> {escape(text['workflow'])}</p>" if text.get("workflow") else "") + "</div>")
    for mid, name, q, keys, how in METHODS:
        if not any((data.get(k) or {}).get("ok") for k in keys):
            continue
        cj = "\n".join(json.dumps({"tool": calls[k]["tool"], "arguments": calls[k]["args"]}, ensure_ascii=False) for k in keys if k in calls)
        h += (f"<div class='card'><div class='sig'>Method</div><h3>{escape(name)}</h3><p><b>Question.</b> {escape(q)}</p>"
              f"<p><b>How.</b> {escape(how)}</p><pre class='code'>{escape(cj)}</pre>"
              + method_result(mid, data)
              + (f"<p><b>Reading.</b> {escape(text[mid])}</p>" if text.get(mid) else "") + "</div>")
    T.append(("Research methods", h))

    tl = D(data, "timeline")
    if tl and tl.get("months_read"):
        ms = "".join(f"<div class='m'><div class='sig'>{escape(x['month'])} · {x.get('articles', 0):,} articles · {escape(str(x.get('signal') or ''))}</div>"
                     f"<div class='h'>{escape(x.get('headline') or '')}</div>" + "".join(f"<div>• {escape(pt['text'])}</div>" for pt in x.get("points") or []) + "</div>"
                     for x in tl["months"] if x.get("available"))
        T.append(("Month by month", f"<div class='card'><h3>The year in the news</h3><p>{escape(tl.get('arc') or '')}</p></div><div class='card'>{ms}</div>"))
    T.append(("Built with MCP", "<div class='card'><p>Every panel in this report is the result of one of these Prism MCP tool calls, made over MCP "
              "(streamable HTTP) as an assistant would make them.</p>"
              + table([(c["tool"], json.dumps(c["args"], ensure_ascii=False)[:120], f"{c['seconds']} s", "ok" if c["ok"] else "no data")
                       for c in calls.values()], ["MCP tool", "Arguments", "Time", "Result"]) + "</div>"))
    return T


def _plain_src(src):
    src = src or {}
    return f"{str(src.get('title') or '')[:90]} ({src.get('year') or ''}, {src.get('tier') or ''})" if src.get("title") else ""


def method_result(mid, data):
    """a compact result block per method (the full charts live in the audience tabs)"""
    if mid == "triangulation":
        E = evidence_view(data)
        return ("<p><b>Result.</b> Documents read: " + ", ".join(f"{k} {v}" for k, v in E["verdicts"].items()) + ". Risk-claim sources by tier: "
                + ", ".join(f"{k} {v}" for k, v in E["by_tier"].items()) + ".</p>"
                + table([(x["rank"], x.get("tier") or "", x.get("strength") or "", str(x.get("title") or "")[:120], x.get("year")) for x in E["ranked"][:6]],
                        ["Rank", "Tier", "Strength", "Source", "Year"]))
    if mid == "head_to_head":
        cp = D(data, "compare") or {}
        if isinstance(cp.get("a"), dict):
            return mix_bars("m_hh", [(cp["a"]["claim"], cp["a"].get("corpus_mix")), (cp["b"]["claim"], cp["b"].get("corpus_mix"))], "Stance mix on each claim") + f"<p><b>Verdict.</b> {escape(cp.get('verdict') or '')}</p>"
    if mid == "screening":
        SC = screening(data)
        return f"<p><b>Result.</b> {sum(r['answered'] for r in SC)} of {len(SC)} rows came back with a quoted figure.</p>" + table(
            [(r["row"], r["value"] or "no figure found") for r in SC], ["Row", "Figure"])
    if mid == "framing":
        st = D(data, "stance") or {}
        return vline("m_st", [("positive %", [(str(x["year"]), x.get("positive_pct")) for x in st.get("points") or []]),
                             ("contested %", [(str(x["year"]), x.get("contested_pct")) for x in st.get("points") or []])], "Framing by year", "% of typed papers")
    if mid == "frontier":
        rd = D(data, "radar") or {}
        return table([(str(x.get("title") or "")[:120], x["year"], x.get("cited_by") or 0) for x in (rd.get("new_work") or [])[:5]], ["New work", "Year", "Cited by"])
    if mid == "gaps":
        gp = D(data, "gaps") or {}
        return table([(x["component"], x["evidence"]) for x in gp.get("components") or []], ["Component", "Literature?"])
    if mid == "history":
        obs, fut, _ = series(data)
        return scenario_chart("m_sc", obs, fut, "Papers per year and scenarios")
    if mid == "geography":
        g = D(data, "geo") or {}
        rows = ((g.get("research_authorship") or {}).get("rows") or [])[:6]
        return table([(r["country"], r["papers"]) for r in rows], ["Studied in (first author)", "Papers"])
    if mid == "facets":
        fa = (D(data, "browse") or {}).get("facets") or {}
        return table([(x["orientation"], x["papers"], f"{x.get('share_pct')}%") for x in fa.get("orientation") or []], ["Orientation", "Papers", "Share"])
    return ""


def page(slug, data, text):
    s = DISEASES[slug]
    T = tabs(slug, data, text)
    b = D(data, "brief") or {}
    vol = b.get("volumes") or {}
    btn = "".join(f'<button role="tab" aria-selected="{str(i == 0).lower()}" data-t="{i}">{escape(n)}</button>' for i, (n, _) in enumerate(T))
    pan = "".join(f'<section class="panel{" on" if i == 0 else ""}" data-p="{i}">{h}</section>' for i, (_, h) in enumerate(T))
    kp = "".join(f"<div class='kpi'><b>{fmt(v.get('n'))}</b><span>{escape(str(v.get('what')))} ({escape(str(v.get('window')))})</span></div>"
                 for k, v in vol.items() if k in ("research", "pubmed", "news", "patents") and v.get("n"))
    con = (b.get("what_is_contested") or {}).get("contested_pct")
    if con is not None:
        kp += f"<div class='kpi'><b>{con}%</b><span>of typed papers qualify or contradict</span></div>"
    calls = len(data.get("_mcp") or {})
    extra = ".code{background:#f0efe9;border-radius:8px;padding:10px;font:12px/1.45 ui-monospace,Menlo,monospace;white-space:pre-wrap;overflow-x:auto}@media (prefers-color-scheme:dark){.code{background:#22262c}}a{color:var(--a)}"
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{escape(s['name'])} · Prism disease intelligence</title><style>{CSS}{extra}</style>
<script src="https://cdn.jsdelivr.net/npm/vega@5.30.0"></script><script src="https://cdn.jsdelivr.net/npm/vega-lite@5.21.0"></script><script src="https://cdn.jsdelivr.net/npm/vega-embed@6.26.0"></script></head>
<body><div class="w"><p class="note">Prism disease intelligence · for policy makers, doctors and scientists · built from {calls} MCP calls</p><h1>{escape(s['name'])}</h1>
<p class="sub">{escape(text.get('summary', ''))}</p>{('<p class="m"><b>Partial index.</b> ' + escape(BANNER) + '</p>') if partial(data) else ''}<div class="kpis">{kp}</div><div class="tabs" role="tablist">{btn}</div>{pan}
<p class="note">{escape(NOTICE)} Source: Prism MCP. Built {time.strftime('%Y-%m-%d')}.</p></div>
<script>document.querySelectorAll('.tabs button').forEach(b=>b.onclick=()=>{{document.querySelectorAll('.tabs button').forEach(x=>x.setAttribute('aria-selected',x===b));document.querySelectorAll('.panel').forEach(x=>x.classList.toggle('on',x.dataset.p===b.dataset.t));window.dispatchEvent(new Event('resize'));}});</script>
</body></html>""", [n for n, _ in T]


CHART_SHOTS = [("sc", "research-scenarios"), ("nw", "news-coverage"), ("ws", "where-studied"), ("scr", "risk-screen"), ("dv", "verdicts"),
               ("hh", "head-to-head"), ("rf", "risk-factors"), ("sa", "framing-by-year"), ("uc", "under-covered"), ("tp", "topics")]


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
    os.makedirs(os.path.join(d, "charts"), exist_ok=True)
    with _SHOT, shot_lock():
        subprocess.run(["node", os.path.join(HERE, "chart_shots.js"), os.path.join(d, "page", "index.html"), os.path.join(d, "charts"),
                        ",".join(f"{a}:{b}" for a, b in CHART_SHOTS)], capture_output=True, text=True, timeout=300)
    return [f for f in os.listdir(os.path.join(d, "charts")) if f.endswith(".png")]


def readme(slug, data, text, names, pngs):
    s = DISEASES[slug]
    img = lambda n, alt: [f"![{alt}](charts/{n}.png)", ""] if f"{n}.png" in pngs else []
    calls = list((data.get("_mcp") or {}).values())
    SC = screening(data)
    E = evidence_view(data)
    cp = D(data, "compare") or {}
    L = [f"# {s['name']}: disease intelligence", "",
         f"*For policy makers, doctors and scientists* · built from **{len(calls)} Prism MCP calls** · "
         f"**[Open the interactive report]({HOST}/{slug}/)** (tabs: {' · '.join(names)})", "",
         *([f"![{s['name']}: risk factors, animated](risk-factors.gif)", ""] if os.path.exists(os.path.join(OUT, slug, "risk-factors.gif")) else []),
         *([f"> **Partial index.** {BANNER}", ""] if partial(data) else []), text.get("summary", ""), "",
         "## For policy makers", "", text.get("policy", ""), ""]
    L += [f"- {x}" for x in text.get("policy_actions") or []] + [""] + img("research-scenarios", "Research per year with scenarios") + img("news-coverage", "News coverage") + img("where-studied", "Where it is studied")
    L += ["## For doctors", "", text.get("doctor", ""), ""] + [f"- {x}" for x in text.get("doctor_points") or []] + [""]
    if SC:
        L += [f"**Risk-factor screen:** *{s['question']}*", "", "| Factor | Effect size (quoted) | Measures | Source |", "| --- | --- | --- | --- |"]
        L += [f"| {r['row']} | {r['value'] or 'no figure found'} | {r['measures'] or ''} | {(r['source'] or '')[:90]}{' (%s)' % r['year'] if r['year'] else ''} |" for r in SC] + [""]
    L += img("risk-screen", "Risk-factor screen") + img("verdicts", "Documents by verdict")
    if E["documents"]:
        L += [f"**Clinical claim:** *{s['clinical']}*. Documents read: " + ", ".join(f"{k} {v}" for k, v in E["verdicts"].items()) + ".", ""]
    if isinstance(cp.get("a"), dict):
        L += [f"**Head to head:** {cp['a']['claim']} vs {cp['b']['claim']}: {cp.get('verdict')}.", ""] + img("head-to-head", "Head to head")
    L += img("risk-factors", "Risk factors in the claims corpus")
    L += ["## For scientists", "", text.get("scientist", ""), ""] + [f"- {x}" for x in text.get("scientist_questions") or []] + [""]
    L += img("framing-by-year", "Framing by year") + img("under-covered", "Under-covered topics") + img("topics", "Topics")
    L += ["## Research exploration methods", "", "Nine ways to explore the research, each run on this disease. The interactive report shows each call and its result.", ""]
    if text.get("workflow"):
        L += [f"**Chaining them.** {text['workflow']}", ""]
    for mid, name, q, keys, how in METHODS:
        if text.get(mid):
            L += [f"### {name}", "", f"*{q}* `{'` + `'.join((data.get('_mcp') or {}).get(k, {}).get('tool', k) for k in keys)}`", "", text[mid], ""]
    L += ["## Built with MCP", "", f"Every number and chart above comes from these {len(calls)} Prism MCP tool calls, made over MCP (streamable HTTP). "
          "The list with arguments and timings is in [mcp_calls.json](mcp_calls.json); the responses are in [data.json](data.json).", "",
          "| MCP tool | Time | Result |", "| --- | ---: | --- |"]
    L += [f"| `{c['tool']}` | {c['seconds']} s | {'ok' if c['ok'] else 'no data'} |" for c in calls] + ["", f"> {NOTICE}", ""]
    open(os.path.join(OUT, slug, "README.md"), "w").write("\n".join(L) + "\n")


def build(slug, refresh=False, write_only=False, workers=4):
    data = json.load(open(os.path.join(OUT, slug, "data.json"))) if write_only else collect(slug, refresh, workers)
    wp = os.path.join(OUT, slug, "writeup.json")
    if write_only and os.path.exists(wp):
        text = json.load(open(wp))["text"]
    else:
        F, text = write(slug, data)
        json.dump({"facts": F, "text": text}, open(wp, "w"), ensure_ascii=False, indent=1, default=str)
    p = D(data, "profile") or {}
    if p.get("risk_factors"):
        from gifs import bars_gif
        bars_gif([(x["factor"], x["claims"]) for x in p["risk_factors"][:10]], f"{DISEASES[slug]['name']}: what increases the risk",
                 os.path.join(OUT, slug, "risk-factors.gif"), subtitle="Extracted health claims per risk factor; orange = from high-tier studies",
                 second=[(x["factor"], x["high_tier"]) for x in p["risk_factors"][:10]], second_label="high-tier studies")
    from pagewriter import clean
    text = clean(text)
    html, names = page(slug, data, text)
    pd = os.path.join(OUT, slug, "page")
    os.makedirs(pd, exist_ok=True)
    open(os.path.join(pd, "index.html"), "w").write(html)
    pngs = chart_pngs(slug)
    readme(slug, data, text, names, pngs)
    with _SHOT:
        shot(os.path.join(pd, "index.html"), os.path.join(OUT, slug, "screenshot.jpg"))
    print(f"{slug}: tabs {names}; charts {len(pngs)}; text keys {sorted(text)}", flush=True)
    return names


def index():
    L = ["# Disease intelligence", "",
         "One report per disease with a view for each reader: **policy makers** (burden, attention, geography, trajectory), "
         "**doctors** (risk factors with quoted effect sizes, the evidence behind a clinical claim, what disagrees, two "
         "interventions head to head) and **scientists** (framing over time, the frontier, the shape of the literature, the "
         "gaps). Each report also runs **nine research exploration methods** on its disease and reads each result in depth. "
         "Every panel is an MCP tool call.", "", f"> {NOTICE}", "",
         "| Disease | MCP calls | Risk factors with a quoted effect size | Interactive report |", "| --- | ---: | ---: | --- |"]
    for slug, s in DISEASES.items():
        f = os.path.join(OUT, slug, "data.json")
        if os.path.exists(os.path.join(OUT, slug, "README.md")):
            d = json.load(open(f))
            SC = screening(d)
            L.append(f"| [{s['name']}]({slug}/README.md) | {len(d.get('_mcp') or {})} | {sum(r['answered'] for r in SC)} of {len(SC)} | [open]({HOST}/{slug}/) |")
    open(os.path.join(OUT, "README.md"), "w").write("\n".join(L) + "\n")


def home():
    """the disease section of the repo README: an animated GIF per disease, linked to its GitHub demo page"""
    cells = []
    for slug, s in DISEASES.items():
        d = os.path.join(OUT, slug)
        if not os.path.exists(os.path.join(d, "README.md")):
            continue
        data = json.load(open(os.path.join(d, "data.json")))
        SC = screening(data)
        cells.append(f'<td width="25%"><a href="docs/diseases/{slug}/README.md"><img src="docs/diseases/{slug}/risk-factors.gif" alt="{s['name']} risk factors"></a>'
                     f'<br><b><a href="docs/diseases/{slug}/README.md">{s['name']}</a></b>: {len(data.get('_mcp') or {})} MCP calls; '
                     f'{sum(r['answered'] for r in SC)} of {len(SC)} risk factors with a quoted effect size · <a href="{HOST}/{slug}/">interactive</a></td>')
    rows = "".join("<tr>" + "".join(cells[i:i + 4]) + "</tr>" for i in range(0, len(cells), 4))
    block = ("<!-- diseases:start -->\n## Disease intelligence\n\n"
             "One report per disease with a view for each reader. **Policy makers:** research volume with backtested scenarios, "
             "news coverage, where the disease is studied and reported, causes and impacts named in the news. **Doctors:** risk "
             "factors screened with quoted effect sizes, the evidence behind a clinical claim and what disagrees with it, two "
             "interventions head to head. **Scientists:** how the literature frames its findings year by year, the frontier, the "
             "shape of the literature and its gaps. Each report also runs **nine research exploration methods** (evidence "
             "triangulation, head-to-head claims, cross-row screening, framing drift, frontier scan, gap mapping, count history "
             "with scenarios, geographic triangulation, faceted browsing) and reads each result in depth. All from MCP calls.\n\n"
             f"<table>{rows}</table>\n\n[All disease reports](docs/diseases/README.md)\n<!-- diseases:end -->")
    import re
    p = os.path.join(ROOT, "README.md")
    r = open(p).read()
    if "<!-- diseases:start -->" in r:
        r = re.sub(r"<!-- diseases:start -->.*?<!-- diseases:end -->", lambda _: block, r, flags=re.S)
    else:
        r = re.sub(r"## Disease intelligence\n.*?\[All disease pages\]\(docs/diseases/README.md\)", lambda _: block, r, flags=re.S)
    open(p, "w").write(r)


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
    ap.add_argument("--workers", type=int, default=1, help="diseases in parallel")
    ap.add_argument("--calls", type=int, default=4, help="MCP calls in parallel per disease")
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--write-only", action="store_true")
    a = ap.parse_args()
    slugs = a.only.split(",") if a.only else list(DISEASES)
    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(lambda s: safe_build(s, a.refresh, a.write_only, a.calls), slugs))
    index()
    home()
    print("DISEASE_INTEL_DONE", flush=True)
