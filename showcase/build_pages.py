"""Build the demonstration pages, the category indexes and the comparison scoreboard.

    python3 showcase/build_pages.py

Reads  docs/examples/<slug>.json            (captured Prism responses)
       docs/comparisons/<slug>.json         (four answers + blind judge)
       docs/comparisons/live/<slug>.json    (live MCP sessions, flagships only)
Writes docs/use-cases/<category>/<slug>.md, docs/use-cases/<category>/README.md,
       docs/use-cases/README.md, docs/use-cases/img/<slug>-*.svg,
       docs/ENGINEERING_FLAGS.md, docs/use-cases/index.json
and rewrites the <!-- use-cases --> block in README.md.

Every number on a page is read from a saved response; nothing is typed by hand.
"""
import json
import os
import re
import sys
from collections import Counter, defaultdict
from datetime import datetime

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "showcase"))
sys.path.insert(0, ROOT)
import svgchart as sc  # noqa: E402
from scenarios import CATEGORIES, SCENARIOS  # noqa: E402

EX = os.path.join(ROOT, "docs", "examples")
V2 = os.path.join(ROOT, "benchmarks", "results", "full")
V2_PDF = "https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full"
LIVE = os.path.join(ROOT, "docs", "live_sessions")
UC = os.path.join(ROOT, "docs", "use-cases")
IMG = os.path.join(UC, "img")
CATNAME = {c[0]: c[1] for c in CATEGORIES}
CATBLURB = {c[0]: c[2] for c in CATEGORIES}
COND = [("claude_prism", "Claude + Prism"), ("chatgpt_prism", "ChatGPT + Prism"),
        ("claude_bare", "Claude alone"), ("chatgpt_bare", "ChatGPT alone")]
CRIT = ["specificity", "verifiability", "currency", "calibration", "accuracy"]


# ── helpers ────────────────────────────────────────────────────────────────
def load(path):
    from prism import envelope
    try:
        return envelope.public(json.load(open(path)))
    except Exception:
        return None


def n(v):
    if v is None:
        return "–"
    if isinstance(v, float) and not v.is_integer():
        return f"{v:,.1f}"
    return f"{int(v):,}"


def pct(v):
    return "–" if v is None else f"{v:.1f}%".replace(".0%", "%")


def mon(p):
    try:
        return datetime.strptime(str(p)[:10], "%Y-%m-%d").strftime("%b %Y")
    except Exception:
        return str(p)


def short_mon(p):
    try:
        return datetime.strptime(str(p)[:10], "%Y-%m-%d").strftime("%b %y")
    except Exception:
        return str(p)


def esc(s):
    return str(s or "").replace("|", "\\|").replace("\n", " ").strip()


def link(title, url):
    t = esc(title)[:120]
    return f"[{t}]({url})" if url else t


def window_of(resp):
    w = (resp or {}).get("window") or {}
    if w.get("from") and w.get("to"):
        return f"{w['from']} to {w['to']}" + (" (exclusive)" if w.get("to_is_exclusive") else "")
    return ""


def call(rec, tool):
    for c in (rec or {}).get("calls", []):
        if c["tool"] == tool:
            return c
    return None


def data(rec, tool):
    c = call(rec, tool)
    return ((c or {}).get("response") or {}).get("data") or {}


def ok(rec, tool):
    c = call(rec, tool)
    return bool(c and (c.get("response") or {}).get("ok"))


def err(rec, tool):
    c = call(rec, tool)
    e = ((c or {}).get("response") or {}).get("error") or {}
    return e.get("reason") or e.get("message") or e.get("kind") or "no data"


class Page:
    def __init__(self, slug):
        self.slug, self.md, self.charts, self.facts = slug, [], [], {}

    def chart(self, name, svg, alt):
        if svg and sc.save(svg, os.path.join(IMG, f"{self.slug}-{name}.svg")):
            self.md.append(f"![{alt}](../img/{self.slug}-{name}.svg)\n")
            self.charts.append(name)

    def add(self, s=""):
        self.md.append(s)


SRC = "Source: Prism MCP, live corpora · captured {date}"


# ── renderers per pattern ─────────────────────────────────────────────────
def r_pulse(p, rec, s, date):
    d = data(rec, "prism_overview")
    if not d:
        p.add(f"> Prism returned no overview: {err(rec, 'prism_overview')}\n")
        return
    prof, tr, se = d.get("profile") or {}, d.get("trends") or {}, d.get("sentiment") or {}
    th, en, geo, so = d.get("themes") or {}, d.get("entities") or {}, d.get("geography") or {}, d.get("sources") or {}
    term = s["args"]["term"]
    pts = [x for x in tr.get("points") or [] if not x.get("partial_period")]
    t = tr.get("trend") or {}
    tot = se.get("totals") or {}
    p.facts = {"articles": prof.get("articles"), "critical": prof.get("critical_articles")}
    p.add("### At a glance\n")
    p.add("| Measure | Value |\n| --- | ---: |")
    p.add(f"| Articles that mention “{term}”, {mon(tr.get('from'))} – {mon(pts[-1]['period']) if pts else ''} | {n(prof.get('articles'))} |")
    if prof.get("articles"):
        p.add(f"| Critical coverage (priority 7–9) | {n(prof.get('critical_articles'))} ({pct(100*(prof.get('critical_articles') or 0)/prof['articles'])}) |")
    if t.get("available"):
        p.add(f"| Peak month | {mon(t.get('peak_period'))} ({n(t.get('peak'))} articles) |")
        p.add(f"| Last third of the window vs first third | {t.get('late_vs_early')}× ({t.get('direction')}) |")
    if tot:
        p.add(f"| Negative · positive | {pct(tot.get('neg_pct'))} · {pct(tot.get('pos_pct'))} |")
        p.add(f"| Tone vs all news (negative-to-positive ratio) | {tot.get('ratio')} vs {se.get('corpus_baseline_ratio')} baseline: *{se.get('reading')}* |")
    p.add(f"| What Prism thinks “{term}” is | {prof.get('type')} |")
    p.add("")
    if pts:
        p.chart("trend", sc.line_chart(
            [("all coverage", [(short_mon(x["period"]), x["articles"]) for x in pts]),
             ("critical (priority 7+)", [(short_mon(x["period"]), x["critical"]) for x in pts])],
            f"“{term}”: monthly news coverage", f"{n(prof.get('articles'))} articles, {mon(pts[0]['period'])} – {mon(pts[-1]['period'])}",
            SRC.format(date=date)), f"Monthly coverage of {term}")
    sp = [x for x in se.get("points") or []]
    if sp:
        p.chart("tone", sc.line_chart(
            [("negative articles", [(short_mon(x["period"]), x.get("negative")) for x in sp]),
             ("positive articles", [(short_mon(x["period"]), x.get("positive")) for x in sp])],
            f"Tone of “{term}” coverage", f"one polarity per article · {se.get('reading')}", SRC.format(date=date)),
            f"Tone of {term} coverage")
    rows = (geo.get("rows") or [])[:10]
    if rows:
        p.chart("geo", sc.hbar_chart([(r["label"].title(), r["articles"]) for r in rows],
                                     f"Where “{term}” coverage is placed",
                                     f"{pct(geo.get('placed_pct'))} of matched articles carry a resolved place",
                                     SRC.format(date=date), cls="c3"), f"Countries in {term} coverage")
    cats = ((th.get("subcategories") or {}).get("rows") or (th.get("categories") or {}).get("rows") or [])[:10]
    if cats:
        p.chart("themes", sc.hbar_chart([(r["label"], r["articles"]) for r in cats],
                                        f"Top themes in “{term}” coverage", "Prism's curated themes, ranked by lift over all news",
                                        SRC.format(date=date), cls="c4"), f"Themes in {term} coverage")
    tg = ((th.get("tags") or {}).get("rows") or [])[:12]
    if tg:
        p.add("**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on "
              f"“{esc(term)}” coverage (they also name the companies, people and places it is written about with): " +
              ", ".join(f"{esc(r['label'])} ({n(r['articles'])})" for r in sorted(tg, key=lambda r: -r["articles"])) + "\n")
    p.add("### Who and what appears alongside it\n")
    p.add("| Organisations | People | Places |\n| --- | --- | --- |")
    o_ = [r["label"] for r in ((en.get("organizations") or {}).get("rows") or [])[:6]]
    pe = [r["label"] for r in ((en.get("people") or {}).get("rows") or [])[:6]]
    pl = [r["label"] for r in ((en.get("places") or {}).get("rows") or [])[:6]]
    for i in range(max(len(o_), len(pe), len(pl), 1)):
        p.add(f"| {esc(o_[i]) if i < len(o_) else ''} | {esc(pe[i]) if i < len(pe) else ''} | {esc(pl[i]) if i < len(pl) else ''} |")
    p.add("")
    pubs = (so.get("publishers") or [])[:6]
    if pubs:
        p.add(f"**Top publishers in a {so.get('sampled_articles')}-article sample:** " +
              ", ".join(f"{esc(x['publisher'])} ({pct(x['share_pct'])})" for x in pubs) + "\n")
    arts = ((d.get("critical") or {}).get("articles") or [])[:8]
    if arts:
        p.add("### Critical headlines\n")
        p.add("| Date | Headline | Publisher | Priority | Tone |\n| --- | --- | --- | ---: | --- |")
        for a in arts:
            p.add(f"| {str(a.get('published') or a.get('datetime') or '')[:10]} | {link(a.get('title'), a.get('url'))} | "
                  f"{esc(a.get('publisher'))} | {a.get('priority')} | {esc(a.get('tone') or a.get('polarity'))} |")
        p.add("")
    if pts:
        p.add("<details><summary>Monthly series (table view of the charts)</summary>\n")
        p.add("| Month | Articles | Critical | Negative | Positive |\n| --- | ---: | ---: | ---: | ---: |")
        for x in pts:
            p.add(f"| {mon(x['period'])} | {n(x['articles'])} | {n(x['critical'])} | {n(x['negative'])} | {n(x['positive'])} |")
        p.add("\n</details>\n")


def doc_rows(docs, k=8):
    out = ["| Year | Study | Tier | Reads as | Verbatim finding |", "| ---: | --- | --- | --- | --- |"]
    for x in docs[:k]:
        q = esc(x.get("quote"))
        q = (q[:260] + "…") if len(q) > 260 else q
        out.append(f"| {x.get('year') or ''} | {link(x.get('title'), x.get('url'))}<br><sub>{esc(x.get('venue'))}</sub> | "
                   f"{esc(x.get('tier'))} | {esc(x.get('stance'))} | {q or '–'} |")
    return "\n".join(out) + "\n"


def r_evidence(p, rec, s, date):
    ev, ce, st = data(rec, "find_evidence"), data(rec, "find_counter_evidence"), data(rec, "find_statistics")
    if not ok(rec, "find_evidence"):
        p.add(f"> **Prism could not resolve this claim:** {err(rec, 'find_evidence')}\n")
    vol = ev.get("volumes") or st.get("volumes") or {}
    if vol:
        p.add("### How much evidence exists\n")
        p.add("| Corpus | Records on both sides of the claim | Window |\n| --- | ---: | --- |")
        for k, lab in [("research", "Typed research papers"), ("readable_papers", "Papers with abstracts"),
                       ("pubmed", "PubMed records"), ("news", "News articles"), ("patents", "Patents"), ("arxiv", "arXiv preprints")]:
            if k in vol:
                p.add(f"| {lab} | {n(vol[k].get('n'))} | {vol[k].get('window')} |")
        p.add("")
        p.chart("volumes", sc.hbar_chart([(lab, (vol.get(k) or {}).get("n")) for k, lab in
                                          [("research", "Typed research"), ("readable_papers", "With abstracts"),
                                           ("pubmed", "PubMed"), ("news", "News"), ("patents", "Patents"), ("arxiv", "arXiv")]
                                          if (vol.get(k) or {}).get("n")],
                                         "Evidence volume by corpus", f"lane: {(vol.get('research') or {}).get('lane')} (intersection = papers on both sides of the claim)",
                                         SRC.format(date=date)), "Evidence volume by corpus")
    cs = ev.get("corpus_stance") or ce.get("corpus_mix") or {}
    if cs.get("sides"):
        sd = cs["sides"]
        p.chart("sides", sc.share_bar([("supporting", sd.get("supporting"), "c1"), ("qualifying", sd.get("qualifying"), "c4"),
                                       ("contradicting", sd.get("contradicting"), "c2"), ("neutral", sd.get("neutral"), "cn")],
                                      "How the literature frames the claim",
                                      f"{n(cs.get('papers'))} papers, {cs.get('window')} · {cs.get('reading')}", SRC.format(date=date)),
                "Framing of the literature")
        p.add(f"*{cs.get('caveat') or ''}* Contested share: **{pct(cs.get('contested_pct'))}**.\n")
    docs = ev.get("documents") or []
    if docs:
        t = ev.get("tally") or {}
        c = t.get("counts") or {}
        p.add("### The strongest evidence, read\n")
        if ev.get("read_note"):
            p.add(f"> {esc(ev['read_note'])}.\n")
        p.add(f"Prism read {t.get('read')} sources: **{c.get('supports', 0)} support, {c.get('contradicts', 0)} contradict, "
              f"{c.get('qualifies', 0)} qualify** (tier-weighted {json.dumps(t.get('tier_weighted'))}). Each quote is copied from "
              f"the abstract and verified against it; {t.get('ungrounded', 0)} candidate quotes failed that check and were dropped.\n")
        p.add(doc_rows(docs))
        tiers = Counter(x.get("tier") for x in docs)
        p.chart("tiers", sc.hbar_chart(tiers.most_common(), "Study designs among the sources read",
                                       "a meta-analysis outranks a cohort, a cohort outranks a case report",
                                       SRC.format(date=date), cls="c3"), "Study designs")
    contra = ce.get("contradicting") or []
    p.add("### What disagrees\n")
    if contra:
        p.add(doc_rows(contra, 6))
    else:
        p.add("Prism's counter-evidence pass found no source that directly contradicts the claim among those it read"
              + (f" (tally {json.dumps((ce.get('tally') or {}).get('counts'))})" if ce.get("tally") else "") + ".\n")
    if ce.get("recommendation"):
        p.add(f"> {esc(ce['recommendation'])}\n")
    stats = st.get("stats") or []
    if stats:
        p.add("### Numbers you can quote\n")
        p.add("| Figure | Measures | Population | Source |\n| --- | --- | --- | --- |")
        for x in stats[:6]:
            src = x.get("source") or {}
            p.add(f"| **{esc(x.get('value'))}** | {esc(x.get('measures'))} | {esc(x.get('population'))} | "
                  f"{link(src.get('title'), src.get('url'))} {src.get('year') or ''} |")
        p.add("")
    rs = st.get("research_series") or {}
    if rs.get("points"):
        p.chart("research-series", sc.line_chart(
            [("papers per year", [(x["period"], x["n"]) for x in rs["points"]])],
            "Research output on this claim, per year", f"{rs.get('window')} · lane: {rs.get('lane')}",
            SRC.format(date=date)), "Research output per year")
    he = ev.get("health_evidence") or {}
    if he.get("rows"):
        p.add(f"**Extracted disease-factor claims** ({n(he.get('claims'))} claims; {esc(he.get('what'))}): "
              + ", ".join(f"{r['relation']}/{r['direction']} ({r['study_tier']}) ×{r['claims']}" for r in he["rows"][:6]) + "\n")


def r_stance(p, rec, s, date):
    st, br = data(rec, "stance_trends"), data(rec, "browse_research")
    pts = st.get("points") or []
    if not pts:
        p.add(f"> Prism returned no stance series: {err(rec, 'stance_trends')}\n")
    else:
        p.add(f"**{n(st.get('papers'))} papers** matched (phrases: {', '.join(st.get('phrases') or [])}).\n")
        p.chart("stance", sc.line_chart(
            [("positive framing %", [(x["year"], x.get("positive_pct")) for x in pts]),
             ("contested framing %", [(x["year"], x.get("contested_pct")) for x in pts])],
            f"How research on “{s['args']['term']}” is framed, by year",
            "share of each year's papers whose own framing is promising/breakthrough vs cautionary/critical",
            SRC.format(date=date), fmt=lambda v: f"{v:.0f}%"), "Framing by year")
        tot = st.get("totals") or {}
        p.chart("orientation", sc.hbar_chart(sorted(tot.items(), key=lambda kv: -kv[1]),
                                             "Papers by orientation", "the label Prism puts on each paper's own framing",
                                             SRC.format(date=date), cls="c3"), "Papers by orientation")
        p.add("| Year | Papers | Positive | Contested |\n| ---: | ---: | ---: | ---: |")
        for x in pts:
            p.add(f"| {x['year']} | {n(x['total'])} | {pct(x.get('positive_pct'))} | {pct(x.get('contested_pct'))} |")
        p.add("")
    papers = br.get("papers") or []
    if papers:
        p.add(f"### Most recent promising studies ({n(br.get('matched'))} matched)\n")
        p.add("| Year | Paper | Venue | Contribution |\n| ---: | --- | --- | --- |")
        for x in papers[:8]:
            p.add(f"| {x.get('year')} | {link(x.get('title'), x.get('url'))} | {esc(x.get('venue'))} | {esc(x.get('contribution'))} |")
        p.add("")


def r_brief(p, rec, s, date):
    b = data(rec, "research_brief")
    if not b:
        p.add(f"> Prism returned no brief: {err(rec, 'research_brief')}\n")
    vol = b.get("volumes") or {}
    if vol:
        p.add("| Corpus | Records | Window |\n| --- | ---: | --- |")
        for k, v in vol.items():
            p.add(f"| {k.replace('_', ' ')} | {n(v.get('n'))} | {v.get('window')} |")
        p.add("")
    est = b.get("what_is_established") or []
    if est:
        p.add("### What is established\n\n| Year | Review or guideline | Tier | Cited by |\n| ---: | --- | --- | ---: |")
        for x in est[:8]:
            p.add(f"| {x.get('year')} | {link(x.get('title'), x.get('url'))} | {esc(x.get('tier'))} | {n(x.get('cited_by'))} |")
        p.add("")
    con = b.get("what_is_contested") or {}
    if con.get("mix"):
        m = con["mix"]
        p.chart("contested", sc.share_bar([("supporting", m.get("supporting"), "c1"), ("qualifying", m.get("qualifying"), "c4"),
                                           ("contradicting", m.get("contradicting"), "c2"), ("neutral", m.get("neutral"), "cn")],
                                          "What is contested", f"{n(con.get('papers'))} papers · {con.get('reading')}",
                                          SRC.format(date=date)), "Contested share")
    kn = b.get("key_numbers") or []
    if kn:
        p.add("### Key numbers\n\n| Figure | Measures | Source |\n| --- | --- | --- |")
        for x in kn[:6]:
            src = x.get("source") or {}
            p.add(f"| **{esc(x.get('value'))}** | {esc(x.get('measures'))} | {link(src.get('title'), src.get('url'))} |")
        p.add("")
    for k in ("who", "geography", "who_is_working_on_it"):
        if b.get(k):
            p.add(f"<details><summary>{k.replace('_', ' ')}</summary>\n\n```json\n{json.dumps(b[k], ensure_ascii=False, indent=1)[:2500]}\n```\n</details>\n")
    nt = data(rec, "news_trends")
    pts = [x for x in nt.get("points") or [] if not x.get("partial_period")]
    if pts:
        p.chart("news", sc.line_chart([("news articles", [(short_mon(x["period"]), x["articles"]) for x in pts]),
                                       ("critical", [(short_mon(x["period"]), x["critical"]) for x in pts])],
                                      f"“{s['args']['term']}” in the news", f"{n(nt.get('total'))} articles", SRC.format(date=date)),
                "News coverage")


def r_compare(p, rec, s, date):
    d = data(rec, "compare_terms")
    rows = d.get("rows") or []
    if not rows:
        p.add(f"> Prism returned no comparison: {err(rec, 'compare_terms')}\n")
        return
    p.add("| Term | Articles | Share | Critical | Growth (late vs early) | Negative-to-positive | vs all news |\n"
          "| --- | ---: | ---: | ---: | ---: | ---: | ---: |")
    for r in rows:
        p.add(f"| **{esc(r['term'])}** | {n(r.get('articles'))} | {pct(r.get('share_pct'))} | {n(r.get('critical'))} | "
              f"{r.get('growth')}× ({r.get('direction')}) | {r.get('tone_ratio')} | {r.get('vs_baseline')}× |")
    p.add("")
    series = []
    for r in rows[:4]:
        pts = [x for x in r.get("points") or [] if not x.get("partial_period")]
        series.append((r["term"], [(short_mon(x["period"]), x["articles"]) for x in pts]))
    p.chart("compare", sc.line_chart(series, "Monthly coverage, one scale", " vs ".join(d.get("terms") or []),
                                     SRC.format(date=date)), "Comparison over time")
    p.chart("share", sc.hbar_chart([(r["term"], r.get("articles")) for r in rows], "Total coverage in the window",
                                   f"{n(d.get('combined_articles'))} articles combined (terms can co-occur)", SRC.format(date=date)),
            "Total coverage")
    meta = (call(rec, "compare_terms") or {}).get("response", {}).get("meta", {})
    if meta.get("caveat"):
        p.add(f"> {esc(meta['caveat'])}\n")


def r_claims(p, rec, s, date):
    d = data(rec, "compare_claims")
    if not d:
        p.add(f"> Prism returned no comparison: {err(rec, 'compare_claims')}\n")
        return
    sides = [d.get("a") or {}, d.get("b") or {}]
    p.add("| | Claim | Papers on both sides | Read: supports / contradicts / qualifies / unrelated | Contested | Strongest source |\n"
          "| --- | --- | ---: | --- | ---: | --- |")
    for i, x in enumerate(sides):
        r = x.get("documents_read") or {}
        ss = x.get("strongest_source") or {}
        p.add(f"| {'AB'[i]} | {esc(x.get('claim'))} | {n(x.get('papers_both_poles'))} | {r.get('supports', 0)} / {r.get('contradicts', 0)} / "
              f"{r.get('qualifies', 0)} / {r.get('unrelated', 0)} | {pct(x.get('contested_pct'))} | {link(ss.get('title'), ss.get('url'))} "
              f"({ss.get('year')}, {esc(ss.get('tier'))}, {esc(ss.get('stance'))}) |")
    p.add("")
    for i, x in enumerate(sides):
        m = x.get("corpus_mix") or {}
        p.chart(f"claim-{'ab'[i]}", sc.share_bar(
            [("supporting", m.get("supporting"), "c1"), ("qualifying", m.get("qualifying"), "c4"),
             ("contradicting", m.get("contradicting"), "c2"), ("neutral", m.get("neutral"), "cn")],
            f"Claim {'AB'[i]}: {x.get('claim')}"[:78], f"{n(sum(v or 0 for v in m.values()))} typed papers on both sides of the claim",
            SRC.format(date=date)), f"Claim {'AB'[i]} framing")
    if d.get("verdict"):
        p.add(f"> **Prism's comparison:** {esc(d['verdict'])}\n")
    p.add("*A larger pool is not stronger evidence: the counts say how much research frames each claim, the read "
          "documents say what the strongest sources found.*\n")

def r_radar(p, rec, s, date):
    d = data(rec, "research_radar")
    if not d:
        p.add(f"> Prism returned no radar: {err(rec, 'research_radar')}\n")
        return
    rt, nt, fs = d.get("research_trend") or {}, d.get("news_trend") or {}, d.get("framing_shift") or {}
    d = {**d, "since": d.get("since") or s["args"].get("since_year")}
    p.add("### Direction of travel\n")
    p.add("| Series | Window | First → last | Peak | Late third vs early third | Direction |\n| --- | --- | --- | --- | ---: | --- |")
    for lab, t in (("Research papers (typed corpus)", rt), ("News articles", nt)):
        if t.get("available"):
            p.add(f"| {lab} | {t.get('from')} – {t.get('to')} | {n(t.get('first'))} → {n(t.get('last'))} | "
                  f"{n(t.get('peak'))} ({t.get('peak_period')}) | {t.get('late_vs_early')}× | {t.get('direction')} |")
    p.add("")
    if fs.get("available"):
        w = fs.get("windows") or {}
        p.add(f"**Framing shift since {d.get('since')}:** cautionary share {pct((w.get('earlier') or {}).get('cautionary_pct'))} "
              f"before vs {pct((w.get('recent') or {}).get('cautionary_pct'))} since ({fs.get('delta_pct_points'):+} points): "
              f"*{fs.get('reading')}*.\n")
    new = d.get("new_work") or []
    if new:
        p.add(f"### New work since {d.get('since')}\n\n*{esc(d.get('new_work_how'))}*\n")
        p.add("| Year | Paper | Venue | Orientation | Cited by |\n| ---: | --- | --- | --- | ---: |")
        for x in new[:10]:
            p.add(f"| {x.get('year')} | {link(x.get('title'), x.get('url'))} | {esc(x.get('venue'))} | {esc(x.get('orientation'))} | {n(x.get('cited_by'))} |")
        p.add("")
        p.chart("new-work", sc.hbar_chart([((x.get("title") or "")[:36], x.get("cited_by")) for x in new[:8]],
                                          f"Most-cited new work since {d.get('since')}", "citations per paper",
                                          SRC.format(date=date)), "Most-cited new work")
    uc = d.get("under_covered") or []
    if uc:
        p.add("### What the research covers and the news does not\n")
        p.add("| Research topic | Papers | News articles |\n| --- | ---: | ---: |")
        for x in uc[:8]:
            p.add(f"| {esc(x.get('topic'))} | {n(x.get('papers'))} | {n(x.get('articles'))} |")
        p.add("")
        p.chart("under-covered", sc.hbar_chart([(x.get("topic"), x.get("papers")) for x in uc[:8]],
                                               "Research topics the news is not covering", "papers in the topic; news articles naming it ≈ 0",
                                               SRC.format(date=date), cls="c4"), "Under-covered topics")

def r_table(p, rec, s, date):
    d = data(rec, "research_table")
    rows = d.get("rows") or []
    if not rows:
        p.add(f"> Prism returned no table: {err(rec, 'research_table')}\n")
        return
    p.add(f"Answered **{d.get('answered')} of {d.get('of')}** rows. A blank value means the corpus does not state one; it is never filled in.\n")
    p.add("| Row | Value | Measures | Papers | Top source |\n| --- | --- | --- | ---: | --- |")
    for r in rows:
        ts = r.get("top_source") or {}
        p.add(f"| **{esc(r.get('row'))}** | {esc(r.get('value')) or '–'} | {esc(r.get('measures'))} | {n(r.get('papers'))} | "
              f"{link(ts.get('title'), ts.get('url')) if isinstance(ts, dict) else esc(ts)} |")
    p.add("")
    p.chart("papers", sc.hbar_chart([(r.get("row"), r.get("papers")) for r in rows if r.get("papers")],
                                    "Papers behind each row", s["args"]["table_question"], SRC.format(date=date)), "Papers per row")
    csv = ["row,value,measures,papers,top_source_title,top_source_url"]
    for r in rows:
        ts = r.get("top_source") or {}
        ts = ts if isinstance(ts, dict) else {"title": ts}
        vals = [r.get("row"), r.get("value"), r.get("measures"), r.get("papers"), ts.get("title"), ts.get("url")]
        csv.append(",".join('"' + str(v if v is not None else "").replace('"', '""') + '"' for v in vals))
    p.add("**Export:** the same rows as CSV, straight from the response:\n\n```csv\n" + "\n".join(csv) + "\n```\n")


def r_audit(p, rec, s, date):
    d = data(rec, "research_audit")
    claims = d.get("claims") or []
    if not claims:
        p.add(f"> Prism returned no audit: {err(rec, 'research_audit')}\n")
        return
    p.add(f"**{d.get('claims_detected')} claims detected**, {d.get('research_checkable')} checkable by research. "
          f"Evidence coverage {pct(d.get('evidence_coverage'))}: *{esc(d.get('evidence_coverage_means'))}*\n")
    p.add("| # | Claim | Status | Papers on both sides | Searched as | What could be wrong |\n| ---: | --- | --- | ---: | --- | --- |")
    for i, c in enumerate(claims, 1):
        searched = " + ".join(filter(None, [", ".join(c.get("subject_phrases") or []), ", ".join(c.get("outcome_phrases") or [])]))
        p.add(f"| {i} | {esc(c.get('claim'))} | **{esc(c.get('status'))}** | {n(c.get('both_poles_papers'))} | {esc(searched)} | {esc(c.get('risk'))} |")
    p.add("")
    st = d.get("by_status") or {}
    p.chart("status", sc.hbar_chart(sorted(st.items(), key=lambda kv: -kv[1]), "Claim status across the draft",
                                    "claim_covered = papers cover both sides; no_literature = no title matches the claim's phrasing",
                                    SRC.format(date=date), cls="c4"), "Claim status")
    means = d.get("status_means") or {}
    if means:
        p.add("<details><summary>What each status means</summary>\n\n" + "\n".join(f"- **{k}**: {esc(v)}" for k, v in means.items()) + "\n</details>\n")
    deep = d.get("deep_reads") or []
    if deep:
        p.add("### Deep reads of the weakest claims\n")
        for dr in deep[:3]:
            if not isinstance(dr, dict):
                continue
            t = (dr.get("tally") or {}).get("counts") or dr.get("documents_read") or {}
            p.add(f"**{esc(dr.get('claim'))}**: {t.get('supports', 0)} support, {t.get('contradicts', 0)} contradict, {t.get('qualifies', 0)} qualify")
            docs = [x for x in (dr.get("documents") or []) if x.get("stance") in ("supports", "contradicts", "qualifies")]
            if docs:
                p.add("\n" + doc_rows(docs, 4))
            else:
                p.add("")

def r_geo(p, rec, s, date):
    g, ng = data(rec, "global_comparison"), data(rec, "news_geography")
    if not g and not ng:
        p.add(f"> Prism returned no geography: {err(rec, 'global_comparison')}\n")
        return
    p.add("Four different questions, kept apart because they measure different things: where the **authors** are, "
          "where the **journal** is published, where the **news** is about, and where the **patent applicants** are.\n")
    blocks = [("research_authorship", "Where the research is done", "first-author affiliation country (PubMed)", "papers", "c1"),
              ("research_publication", "Where it is published", "country of the publishing journal (PubMed)", "papers", "c4"),
              ("patent_origin", "Who patents it", "assignee country", "patents", "c3")]
    cols = []
    for key, title, sub, unit, cls in blocks:
        rows = ((g.get(key) or {}).get("rows") or [])[:10]
        if rows:
            cols.append((title, [(r.get("country"), r.get(unit)) for r in rows]))
            p.chart(key.replace("_", "-"), sc.hbar_chart([(str(r.get("country") or "").title(), r.get(unit)) for r in rows],
                                                         title, sub, SRC.format(date=date), cls=cls), title)
    nrows = (ng.get("rows") or [])[:10]
    if nrows:
        cols.append(("Where it is reported", [(r["label"], r["articles"]) for r in nrows]))
        p.chart("news-geo", sc.hbar_chart([(r["label"].title(), r["articles"]) for r in nrows], "Where it is reported",
                                          f"news articles by the place they are about · {pct(ng.get('placed_pct'))} of matched articles placed",
                                          SRC.format(date=date), cls="c2"), "News by country")
    if cols:
        p.add("| Rank | " + " | ".join(c[0] for c in cols) + " |\n| ---: | " + " | ".join("---" for _ in cols) + " |")
        for i in range(max(len(c[1]) for c in cols)):
            p.add(f"| {i+1} | " + " | ".join((f"{str(c[1][i][0]).title()} ({n(c[1][i][1])})" if i < len(c[1]) else "") for c in cols) + " |")
        p.add("")
    if g.get("note"):
        p.add(f"> {esc(g['note'])}\n")

def r_trending(p, rec, s, date):
    d = data(rec, "trending_topics")
    rows = d.get("rising") or []
    if not rows:
        p.add(f"> Prism returned no trending list: {err(rec, 'trending_topics')}\n")
        return
    p.add(f"Last {s['args']['days']} days against the {s['args']['days']} days before, category *{(d.get('filters') or {}).get('category') or 'all'}*.\n")
    p.add("| Rising topic | Articles now | Window before | Growth |\n| --- | ---: | ---: | ---: |")
    for r in rows[:15]:
        p.add(f"| {esc(r.get('topic'))} | {n(r.get('articles'))} | {n(r.get('previous'))} | {r.get('growth_x')}×{' (new)' if r.get('new') else ''} |")
    p.add("")
    p.chart("rising", sc.hbar_chart(sorted([(r.get("topic"), r.get("growth_x")) for r in rows[:12]], key=lambda kv: -(kv[1] or 0)), "Fastest-rising topics",
                                    "growth multiple against the previous window", SRC.format(date=date), cls="c3",
                                    fmt=lambda v: f"{v:,.1f}", suffix="×"), "Rising topics")
    big = d.get("biggest") or []
    if big:
        p.add("**Biggest topics in the window:** " + ", ".join(f"{esc(r.get('topic'))} ({n(r.get('articles'))})" for r in big[:8]) + "\n")
        p.chart("biggest", sc.hbar_chart([(r.get("topic"), r.get("articles")) for r in big[:10]], "Biggest topics by volume",
                                         "articles in the window", SRC.format(date=date)), "Biggest topics")

def r_history(p, rec, s, date):
    h, sc_ = data(rec, "historical_analysis"), data(rec, "trend_scenarios")
    ser = h.get("series") or []
    if not ser:
        p.add(f"> Prism returned no series: {err(rec, 'historical_analysis')}\n")
        return
    scen = [(x["year"], x.get("central"), x.get("lower_sensitivity"), x.get("upper_sensitivity")) for x in sc_.get("scenarios") or []]
    p.chart("history", sc.range_chart([(x["year"], x["value"]) for x in ser], scen,
                                      f"Research records per year: {', '.join(s['args']['subject_phrases'])}",
                                      f"observed through {sc_.get('observed_through')} · baseline: {sc_.get('selected_baseline')}",
                                      SRC.format(date=date)), "History and scenarios")
    p.add("| Year | Records | Kind |\n| ---: | ---: | --- |")
    for x in ser:
        p.add(f"| {x['year']} | {n(x['value'])} | observed |")
    for y, c, lo, hi in scen:
        p.add(f"| {y} | {n(c)} (range {n(lo)}–{n(hi)}) | scenario |")
    p.add("")
    bt = sc_.get("backtest") or {}
    if bt:
        p.add(f"**Backtest:** {bt.get('method')}; mean absolute error {json.dumps(bt.get('mae'))}. "
              f"The selected baseline is the one that forecast past years best, not the one that looks most exciting.\n")
    lim = (h.get("limitations") or []) + (sc_.get("limitations") or [])
    if lim:
        p.add("**Limitations Prism attaches:**\n" + "\n".join(f"- {esc(x)}" for x in lim) + "\n")
    prov = h.get("provenance") or {}
    if prov.get("sql"):
        p.add(f"<details><summary>The exact query behind the series</summary>\n\n```sql\n{prov['sql']}\n```\n</details>\n")


def r_citations(p, rec, s, date):
    c, rk = data(rec, "get_citations"), data(rec, "rank_sources")
    ents = c.get("entries") or c.get("rendered") or []
    if ents:
        p.add(f"### {(c.get('style') or s['args']['style']).upper()} citations, rendered from stored metadata\n")
        for x in ents[:8]:
            p.add(f"{x.get('n') or ''}. {esc(x.get('citation'))} <sub>[{esc(x.get('tier'))}, {esc(x.get('strength'))}]</sub>")
        p.add("")
        marks = c.get("inline_markers") or []
        if marks:
            p.add("Inline markers: " + " · ".join(f"`{esc(m.get('inline'))}`" for m in marks[:6]) + "\n")
    else:
        p.add(f"> No citations returned: {err(rec, 'get_citations')}\n")
    src = rk.get("sources") or []
    if src:
        p.add("### Source ladder\n\n| Rank | Source | Tier | Why this tier carries the weight it does |\n| ---: | --- | --- | --- |")
        for x in src[:8]:
            p.add(f"| {x.get('rank')} | {link(x.get('title'), x.get('url'))} ({x.get('year')}) | {esc(x.get('tier'))} | {esc(x.get('why_tier'))} |")
        p.add("")
        bt = rk.get("by_tier") or {}
        p.chart("ladder", sc.hbar_chart(sorted(bt.items(), key=lambda kv: -kv[1]), "Sources by study design",
                                        "the ladder ranks meta-analyses and guidelines above trials, cohorts, reviews and preprints",
                                        SRC.format(date=date), cls="c3"), "Source tiers")

def r_improve(p, rec, s, date):
    im, card = data(rec, "improve_claim"), data(rec, "evidence_card")
    p.add(f"**Original:** “{s['args']['claim']}”  \n**Prism's verdict:** **{esc(im.get('verdict'))}**: {esc(im.get('assessment'))}\n")
    opts = im.get("options") or []
    if opts:
        p.add("| Better-supported rewrite | Why |\n| --- | --- |")
        for o in opts[:4]:
            p.add(f"| “{esc(o.get('text'))}” | {esc(o.get('why'))} |")
        p.add("")
    elif not im:
        p.add(f"> No rewrite returned: {err(rec, 'improve_claim')}\n")
    b = im.get("based_on") or {}
    if b:
        r = b.get("documents_read") or {}
        p.add(f"Based on {sum(r.values()) if r else 0} documents read ({r.get('supports', 0)} support, {r.get('contradicts', 0)} contradict, "
              f"{r.get('qualifies', 0)} qualify, {r.get('unrelated', 0)} unrelated). Lane: *{esc(b.get('lane_note') or b.get('lane'))}*.\n")
    cd = card.get("card") or {}
    if cd.get("title"):
        p.add("### Evidence card\n")
        p.add(f"| | |\n| --- | --- |\n| Source | {link(cd.get('title'), cd.get('url'))} |\n| Year · venue | {cd.get('year')} · {esc(cd.get('venue'))} |\n"
              f"| Design | {esc(cd.get('tier'))} ({esc(cd.get('why_tier'))}) |\n| Reads as | {esc(cd.get('stance'))} |\n| Verbatim | {esc(cd.get('quote'))} |\n")
        if card.get("citation"):
            p.add(f"**Citation:** {esc(card['citation'] if isinstance(card['citation'], str) else json.dumps(card['citation']))}\n")
    elif not ok(rec, "evidence_card"):
        p.add(f"> **No evidence card:** {err(rec, 'evidence_card')}. Prism does not promote an unrelated paper to 'strongest evidence'.\n")

def r_library(p, rec, s, date):
    d = data(rec, "library_gaps")
    if not d:
        p.add(f"> Prism returned no gap analysis: {err(rec, 'library_gaps')}\n")
        return
    p.add(f"Prism resolved the list against **{n(d.get('resolved'))}** corpus records for {d.get('of_items')} items.\n")
    th = d.get("themes") or []
    if th:
        p.add("| Theme the list covers | Records in the list's neighbourhood |\n| --- | ---: |")
        for t in th[:8]:
            p.add(f"| {esc(t.get('topic'))} | {n(t.get('in_library'))} |")
        p.add("")
        p.chart("themes", sc.hbar_chart([(t.get("topic"), t.get("in_library")) for t in th[:8]], "What the reading list covers",
                                        "", SRC.format(date=date), cls="c3"), "Themes covered")
    for key, lab in (("highly_cited_missing", "Highly cited work the list is missing"), ("recent_missing", "Recent work the list is missing")):
        rows = d.get(key) or []
        if rows:
            p.add(f"### {lab}\n\n| Year | Paper | Cited by |\n| ---: | --- | ---: |")
            for x in rows[:10]:
                p.add(f"| {x.get('year')} | {link(x.get('title'), x.get('url') or (('https://doi.org/' + x['doi']) if x.get('doi') else None))} | {n(x.get('cited_by'))} |")
            p.add("")


# ── deeper capabilities appended by capture_extras.py ──────────────────────────
CAPABILITY = {"news_activities": "Areas of activity and company events", "news_drill": "Drill into a section",
              "deep_timeline": "Month-by-month ultra research", "news_geography": "City-level geography"}



IMPL = {"news_drill": ("news.drill", "prism/deep.py", "drill(term, scope, since, until, limit)",
                       "an article is in the section when it mentions the entity and every scope phrase; the section's monthly "
                       "volume is divided by the entity's own, its tone compared with the entity's, and its busiest days listed"),
        "news_activities": ("news.activities", "prism/deep.py", "activities(term, domain, since, until, limit)",
                            "the industry taxonomy each article is classified under (generic news classes removed), the curated "
                            "subcategories inside it, the top tags, and, with a web domain, the company's news events by type"),
        "deep_timeline": ("analysis.timeline", "prism/deep.py", "timeline(term, scope, months, until, per_month)",
                          "for each month, the days most outlets reported the subject are read from their openings and summarised "
                          "with citations; then the arc across the months"),
        "news_geography": ("news.geography", "prism/news.py", "geography(term, level, since, until, limit)",
                           "the place each article is about, at country, state or city level, with lift over all news")}


def run_block(tool, args):
    """How to run a section: the function behind it and the same call over MCP, REST, Python and the CLI."""
    feat, path, sig, how = IMPL[tool]
    a = json.dumps(args, ensure_ascii=False)
    cli = " ".join(f"{k}='{v}'" for k, v in args.items())
    py = ", ".join(f"{k}={json.dumps(v, ensure_ascii=False)}" for k, v in args.items())
    code = ""
    if tool == "news_drill":
        import inspect
        sys.path.insert(0, ROOT)
        from prism import deep
        code = ("The scoping itself is this function: the entity's own match, narrowed by every scope phrase, so the "
                "section is always a subset of the entity's coverage:\n\n```python\n" + inspect.getsource(deep._pred).strip() +
                "\n```\n\n")
    return (f"<details{' open' if tool == 'news_drill' else ''}><summary><b>How to run this:</b> <code>{feat}</code> (MCP tool <code>{tool}</code>)</summary>\n\n"
            f"The function is `{sig}` in [`{path}`](../../../{path}), registered as the `{feat}` feature in "
            f"[`prism_mcp.py`](../../../prism_mcp.py): {how}.\n\n" + code +
            f"**MCP** (Claude, ChatGPT, Cursor, any MCP client): call the tool `{tool}` with\n\n```json\n{a}\n```\n\n"
            f"**REST**\n\n```bash\ncurl -s -X POST \"$PRISM_URL/v1/{feat}\" -H \"Authorization: Bearer $FLIAR_API_KEY\" \\\n"
            f"  -H 'content-type: application/json' -d '{a}' | jq '.data'\n```\n\n"
            f"**Python**\n\n```python\nimport prism_mcp\nr = prism_mcp.REGISTRY[\"{tool}\"][\"fn\"]({py})\nprint(r[\"data\"], r[\"window\"])\n```\n\n"
            f"**CLI**\n\n```bash\nprism call {feat} {cli}\n```\n\n</details>\n")

def r_extras(p, rec, s, date):
    extra = [c for c in rec.get("calls") or [] if c.get("extra")]
    if not extra:
        return
    caps = []
    for c in extra:
        lab = CAPABILITY.get(c["tool"])
        if lab and lab not in caps:
            caps.append(lab)
    p.add("## Beyond the news trend\n")
    for kind in ("drill", "events"):
        if os.path.exists(os.path.join(ROOT, "docs", "gallery", "gifs", f"{s['slug']}-{kind}.gif")):
            p.add(f"![{kind}, animated](../../gallery/gifs/{s['slug']}-{kind}.gif)\n")
    p.add("This page also shows: " + " · ".join(f"**{x}**" for x in caps) + ". Each section below is one Prism call; "
          "the call is printed under it so you can run it on any other company, person, place or phrase.\n")
    for i, c in enumerate(extra):
        d = ((c.get("response") or {}).get("data")) or {}
        a = c.get("args") or {}
        call_line = run_block(c["tool"], a) if c["tool"] in IMPL else ""
        if not (c.get("response") or {}).get("ok"):
            continue
        if c["tool"] == "news_activities":
            p.add(f"### Areas of activity: {esc(a['term'])}\n")
            areas = ((d.get("areas_of_activity") or {}).get("rows") or [])[:10]
            if areas:
                p.chart(f"x{i}-areas", sc.hbar_chart([(r["area"], r["articles"]) for r in areas],
                        f"What “{a['term']}” does, by industry area", "articles per area; generic news and investing classes removed",
                        SRC.format(date=date), cls="c3"), f"Areas of activity for {a['term']}")
                p.add("| Area of activity | Articles | Lift over all news |\n| --- | ---: | ---: |")
                for r in areas:
                    p.add(f"| {esc(r['area'])} | {n(r['articles'])} | {r.get('lift')}× |")
                p.add("")
            topics = ((d.get("activity_topics") or {}).get("rows") or [])[:8]
            if topics:
                p.add("**Activity topics inside those areas:** " + ", ".join(esc(r["label"]) for r in topics) + "\n")
            ev = d.get("company_events") or {}
            if ev.get("available"):
                p.chart(f"x{i}-events", sc.hbar_chart([(r["event_type"], r["events"]) for r in ev["rows"][:10]],
                        f"Company events: {ev['domain']}", f"{n(ev['total'])} events extracted from business news",
                        SRC.format(date=date), cls="c2"), f"Company events for {ev['domain']}")
                p.add("| Event type | Events | Latest example |\n| --- | ---: | --- |")
                for r in ev["rows"][:8]:
                    exs = r.get("examples") or [{}]
                    p.add(f"| {esc(r['event_type'])} | {n(r['events'])} | {esc(exs[0].get('date', ''))}: {esc(str(exs[0].get('headline', ''))[:150])} |")
                p.add("")
            p.add(call_line + "\n")
        elif c["tool"] == "news_drill":
            sec, tone = d.get("section") or {}, d.get("tone") or {}
            scope = " + ".join(d.get("scope") or [])
            p.add(f"### Drill-down: {esc(a['term'])} → {esc(scope)}\n")
            p.add(f"**{n(sec.get('articles'))}** articles about {esc(a['term'])} also mention {esc(scope)}: "
                  f"**{sec.get('share_of_entity_pct')}%** of its coverage; last third of the window vs first: "
                  f"**{sec.get('late_vs_early')}×**. Tone: {tone.get('section_neg_per_pos')} negative per positive in the section "
                  f"vs {tone.get('entity_neg_per_pos')} for {esc(a['term'])} overall ({esc(tone.get('reading') or '')}).\n")
            pts = d.get("points") or []
            if pts:
                p.chart(f"x{i}-drill", sc.line_chart([(f"{scope}, % of {a['term']} coverage",
                        [(short_mon(x["period"]), x.get("section_share_pct") or 0) for x in pts])],
                        f"{a['term']} → {scope}", "share of the entity's monthly coverage that is about this section",
                        SRC.format(date=date)), f"{scope} share of {a['term']} coverage")
            tg = (d.get("top_tags") or [])[:10]
            if tg:
                p.add("**Inside the section, the top tags are:** " + ", ".join(f"{esc(r['label'])} ({n(r['articles'])})" for r in tg) + "\n")
            evs = (d.get("events") or [])[:6]
            if evs:
                p.add("| Day | Outlets that day | What was reported |\n| --- | ---: | --- |")
                for e in evs:
                    p.add(f"| {e['date']} | {e['reports_that_day']} | {esc(e['opening'][:180])} |")
                p.add("")
            p.add(call_line + "\n")
        elif c["tool"] == "deep_timeline":
            scope = " + ".join(d.get("scope") or [])
            p.add(f"### Month by month: Prism reads {esc(a['term'])}{' → ' + esc(scope) if scope else ''}\n")
            p.add("Prism took the days most outlets reported the subject, one month at a time, read the stories' openings, "
                  "and wrote what happened and why it mattered; every point cites the stories it rests on.\n")
            if d.get("arc"):
                p.add(f"> **The arc.** {esc(d['arc'])}\n")
            for tp in (d.get("turning_points") or [])[:4]:
                p.add(f"- **Turning point, {esc(str(tp.get('month')))}:** {esc(str(tp.get('why')))}")
            p.add("")
            p.add("| Month | Articles | Signal | What happened |\n| --- | ---: | --- | --- |")
            for mth in d.get("months") or []:
                if mth.get("available"):
                    pts_ = " ".join(x["text"] for x in mth.get("points") or [])
                    p.add(f"| {mth['month']} | {n(mth.get('articles'))} | {esc(str(mth.get('signal') or ''))} | "
                          f"**{esc(mth.get('headline') or '')}** {esc(pts_)[:400]} |")
            p.add("")
            if d.get("watch"):
                p.add("**What to watch:** " + "; ".join(esc(str(w)) for w in d["watch"][:4]) + "\n")
            p.add(call_line + "\n")
        elif c["tool"] == "news_geography":
            rows = (d.get("rows") or [])[:10]
            if rows:
                p.chart(f"x{i}-geo", sc.hbar_chart([(r["label"].title(), r["articles"]) for r in rows],
                        f"Where “{a['term']}” coverage is placed: {a.get('level', 'country')} level",
                        f"lift over all news shown in the table", SRC.format(date=date), cls="c3"), "City-level geography")
                p.add(call_line + "\n")

RENDER = {"pulse": r_pulse, "evidence": r_evidence, "stance": r_stance, "brief": r_brief, "compare": r_compare,
          "claims": r_claims, "radar": r_radar, "table": r_table, "audit": r_audit, "geo": r_geo,
          "trending": r_trending, "history": r_history, "citations": r_citations, "improve": r_improve,
          "library": r_library}

PROMPT_HINT = {
    "pulse": "Use Prism to profile the news coverage of {x}.",
    "evidence": "Use Prism to find evidence and counter-evidence for: {x}",
    "stance": "Use Prism to show how research on {x} is framed over time.",
    "brief": "Use Prism to write a research brief on {x}.",
    "compare": "Use Prism to compare news coverage of {x}.",
    "claims": "Use Prism to compare the evidence for two claims: {x}",
    "radar": "Use Prism's research radar on {x}.",
    "table": "Use Prism to answer one question across these rows: {x}",
    "audit": "Use Prism to audit this draft before publishing: {x}",
    "geo": "Use Prism to show where {x} is studied and reported.",
    "trending": "Use Prism to list rising topics in {x} news.",
    "history": "Use Prism to build the research history and 3-year scenarios for {x}.",
    "citations": "Use Prism to give {x}",
    "improve": "Use Prism to rewrite this so it says what the evidence supports: {x}",
    "library": "Use Prism to find what this reading list is missing: {x}",
}


def subject_of(s):
    a = s["args"]
    return (a.get("term") or a.get("claim") or a.get("topic") or ", ".join(a.get("terms") or [])
            or (f"{a.get('claim_a')} / {a.get('claim_b')}" if a.get("claim_a") else "")
            or ", ".join(a.get("subject_phrases") or []) or ", ".join(a.get("rows") or a.get("items") or []) or s["title"])


def recipes(p, rec, s):
    first = (rec.get("calls") or [{}])[0]
    tool, args = first.get("tool"), first.get("args") or {}
    feature = first.get("feature")
    qs = json.dumps(args, ensure_ascii=False)
    p.add("## Run it yourself\n")
    p.add("**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:\n")
    p.add(f"```text\n{s['question']}\n```\n")
    p.add(f"**Over REST** (same function, same envelope):\n\n```bash\ncurl -s -X POST \"$PRISM_URL/v1/{feature}\" \\\n"
          f"  -H 'content-type: application/json' \\\n  -d '{qs}' | jq '.data'\n```\n")
    p.add("**From Python**, in-process:\n\n```python\nimport prism_mcp\n"
          f"r = prism_mcp.REGISTRY[{tool!r}][\"fn\"](**{args!r})\nprint(r[\"ok\"], r[\"window\"], r[\"meta\"][\"coverage\"][\"note\"])\n```\n")
    calls = rec.get("calls") or []
    if len(calls) > 1:
        p.add("Tool calls this page is built from: " + " → ".join(f"`{c['tool']}` ({c['seconds']} s)" for c in calls) + "\n")


V2NAME = {"claude_bare": "Claude alone", "claude_prism": "Claude + Prism", "chatgpt_bare": "ChatGPT alone",
          "chatgpt_prism": "ChatGPT + Prism"}
V2ORDER = ["claude_prism", "chatgpt_prism", "claude_bare", "chatgpt_bare"]


def benchmark_v2(p, s):  # the benchmark section of a page
    """the current benchmark: a full decision-grade report, scored 0-100 by script ceilings and two blind judges"""
    r = load(os.path.join(V2, s["slug"], "results.json"))
    if not r:
        return None
    st = r["setups"]
    tot = {k: st[k]["strict"] for k in V2ORDER}
    best = max(V2ORDER, key=lambda k: tot[k])
    p.add("## Claude and ChatGPT, with and without Prism\n")
    p.add("Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, "
          "exports, references), once from memory and once with this page's Prism results. A script traced every "
          "number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. "
          "[How the benchmark works](../../../benchmarks/README.md)\n")
    p.chart("benchmark", sc.scoreboard(tot, "Benchmark score (out of 100)", "11-parameter rubric · script ceilings, then two blind judges",
                                       "Prism answers used this page's tool results; 'alone' answers used model memory only", scale=100),
            "Benchmark scores")
    params = list(st["claude_bare"]["params"])
    sys.path.insert(0, os.path.join(ROOT, "benchmarks"))
    from bench import PARAMS as V2P
    p.add("| Parameter (0-5) | " + " | ".join(V2NAME[k] for k in V2ORDER) + " |\n| --- | " + " | ".join("---:" for _ in V2ORDER) + " |")
    for prm in params:
        p.add(f"| {V2P[prm]['name']} | " + " | ".join(str(st[k]['params'][prm]) for k in V2ORDER) + " |")
    p.add("| **Score /100** | " + " | ".join(f"**{tot[k]}**" if k == best else str(tot[k]) for k in V2ORDER) + " |\n")
    for w, v in (r.get("verdicts") or {}).items():
        p.add(f"**{'Claude Opus' if w == 'opus' else 'GPT'} judge:** {esc(v)}\n")
    p.add(f"Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/{s['slug']}/README.md) · "
          f"[full report PDF]({V2_PDF}/{s['slug']}.pdf)\n")
    lift = max(tot["claude_prism"], tot["chatgpt_prism"]) - max(tot["claude_bare"], tot["chatgpt_bare"])
    return {"totals": tot, "best": best, "lift": lift}


def comparison(p, s):
    return benchmark_v2(p, s)


def live_block(p, s):
    lv = load(os.path.join(LIVE, f"{s['slug']}.json"))
    if not lv:
        return False
    p.add("## Live MCP session\n")
    p.add("Here each model was given only the question and a live connection to the Prism MCP server, and chose its own calls.\n")
    for k, lab in (("claude_live", "Claude"), ("chatgpt_live", "ChatGPT")):
        a = lv.get(k)
        if not a:
            continue
        calls = a.get("tool_calls") or []
        if a.get("no_tool_calls"):
            p.add(f"**{lab}** made no Prism calls in this session (twice): the MCP server did not come up in time, "
                  "so its answer below is from memory and is shown only for completeness.\n")
            p.add(f"<details><summary>{lab}'s answer</summary>\n\n{a.get('text')}\n\n</details>\n")
            continue
        p.add(f"**{lab}** ({a.get('model')}, {a.get('seconds')} s) called {len(calls)} Prism tool{'s' if len(calls) != 1 else ''}:\n")
        if calls:
            p.add("| # | Tool | Arguments | Result |\n| ---: | --- | --- | --- |")
            for i, t in enumerate(calls, 1):
                p.add(f"| {i} | `{t.get('tool')}` | `{esc(json.dumps(t.get('args'), ensure_ascii=False))[:160]}` | "
                      + ("started, but the client ended its turn before it returned |" if t.get("returned") is False else
                         f"{'ok' if t.get('ok') else 'see payload'} · {n(t.get('chars'))} chars |"))
            p.add("")
        p.add(f"<details><summary>{lab}'s answer</summary>\n\n{a.get('text')}\n\n</details>\n")
    return True


def build_page(s, scen_index):
    rec = load(os.path.join(EX, f"{s['slug']}.json"))
    if not rec:
        return None
    date = rec.get("captured_at", "")[:10]
    p = Page(s["slug"])
    cat = s["category"]
    p.add(f"# {s['title']}\n")
    p.add(f"[{CATNAME[cat]}](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)\n")
    first = (rec.get("calls") or [{}])[0].get("response") or {}
    cov = ((first.get("meta") or {}).get("coverage") or {}).get("note") or ""
    p.add(f"> **Intelligence requirement.** {s['requirement']}  \n> **Why it is hard.** {s['special']}  \n"
          f"> **Data.** Captured {date} from the live Prism MCP server · {window_of(first) or 'research corpus windows below'}"
          f"{' · ' + cov if cov else ''}. Saved responses: [{s['slug']}.json](../../examples/{s['slug']}.json).\n")
    p.add("**The question:**\n\n> " + s["question"].replace("\n", "\n> ") + "\n")
    p.add("## What Prism returned\n")
    RENDER[s["pattern"]](p, rec, s, date)
    r_extras(p, rec, s, date)
    res = comparison(p, s)
    live = live_block(p, s)
    recipes(p, rec, s)
    p.add(EXPORT_FOOTER.get(s["pattern"], EXPORT_FOOTER["default"]))
    os.makedirs(os.path.join(UC, cat), exist_ok=True)
    with open(os.path.join(UC, cat, f"{s['slug']}.md"), "w") as f:
        f.write("\n".join(p.md).replace("\n\n\n", "\n\n"))
    return {"slug": s["slug"], "category": cat, "title": s["title"], "pattern": s["pattern"], "date": date,
            "charts": len(p.charts), "live": live, "cmp": res, "question": s["question"]}


EXPORT_FOOTER = {
    "default": ("## Take it further\n\n- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so "
                "`jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).\n"
                "- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a "
                "question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).\n"),
}


# ── indexes ────────────────────────────────────────────────────────────────
PATTERN_LABEL = {"pulse": "news pulse", "evidence": "evidence + counter-evidence", "stance": "stance trend",
                 "brief": "research brief", "compare": "news comparison", "claims": "claim vs claim", "radar": "research radar",
                 "table": "evidence table / export", "audit": "draft audit", "geo": "geography", "trending": "trending scan",
                 "history": "history + scenarios", "citations": "citations", "improve": "claim rewrite", "library": "library gaps"}


def stars(r):
    c = r.get("cmp")
    if not c:
        return "–"
    t = c["totals"]
    return f"{max(t['claude_prism'], t['chatgpt_prism'])} vs {max(t['claude_bare'], t['chatgpt_bare'])}"


def write_indexes(pages):
    bycat = defaultdict(list)
    for r in pages:
        bycat[r["category"]].append(r)
    for cat, rows in bycat.items():
        L = [f"# {CATNAME[cat]}\n", f"[All use cases](../README.md) · [Prism MCP](../../../README.md)\n", CATBLURB[cat] + "\n",
             "| Demonstration | Pattern | Best with Prism vs best alone (/100) | Live MCP |", "| --- | --- | ---: | :---: |"]
        for r in rows:
            L.append(f"| [{r['title']}]({r['slug']}.md) | {PATTERN_LABEL[r['pattern']]} | {stars(r)} | {'✓' if r['live'] else ''} |")
        open(os.path.join(UC, cat, "README.md"), "w").write("\n".join(L) + "\n")
    L = ["# Prism MCP: use cases\n", "[Prism MCP](../../README.md) · [How the benchmark works](../../benchmarks/README.md) · "
         "[Research analysis](../RESEARCH_ANALYSIS.md) · [Data export](../DATA_EXPORT.md)\n",
         f"{len(pages)} demonstrations across {len(bycat)} domains. Every page runs real Prism tools against the live "
         "corpora, saves the raw responses, draws its charts from them, and puts Claude and ChatGPT side by side with and without Prism.\n"]
    for cat, name, blurb in CATEGORIES:
        rows = bycat.get(cat) or []
        if not rows:
            continue
        L.append(f"## [{name}]({cat}/README.md)\n\n{blurb}\n")
        L.append("| Demonstration | Pattern | Best with Prism vs best alone (/100) |\n| --- | --- | ---: |")
        for r in rows:
            L.append(f"| [{r['title']}]({cat}/{r['slug']}.md) | {PATTERN_LABEL[r['pattern']]} | {stars(r)} |")
        L.append("")
    open(os.path.join(UC, "README.md"), "w").write("\n".join(L) + "\n")
    json.dump(pages, open(os.path.join(UC, "index.json"), "w"), indent=1, ensure_ascii=False)


def flags_doc(pages):
    fixes = load(os.path.join(ROOT, "showcase", "fixes.json")) or {}
    L = ["# Engineering flags\n",
         "[Benchmark](../benchmarks/README.md) · [Use cases](use-cases/README.md)\n",
         "What building and benchmarking the showcase found in the MCP server: the fixes applied, with the change, "
         "and the issues still open.\n",
         "## Fixes applied\n"]
    for f in fixes.get("applied", []):
        L.append(f"- **{f['title']}** ({', '.join(f.get('scenarios', []))}): {f['change']}  \n  `{f.get('file', '')}`")
    if fixes.get("open"):
        L += ["", "## Known issues, not yet fixed\n"]
        for f in fixes["open"]:
            L.append(f"- **{f['title']}** ({', '.join(f.get('scenarios', []))}): {f['note']}")
    open(os.path.join(ROOT, "docs", "ENGINEERING_FLAGS.md"), "w").write("\n".join(L) + "\n")


def readme_block(pages, board):
    bycat = defaultdict(list)
    for r in pages:
        bycat[r["category"]].append(r)
    L = ["<!-- use-cases:start -->",
         f"## {len(pages)} live demonstrations, {len(bycat)} domains\n",
         "Each page asks a real intelligence question, runs Prism tools against the live corpora, draws the charts "
         "from the saved responses, and benchmarks **Claude and ChatGPT with and without Prism**. "
         "[Browse all](docs/use-cases/README.md) · [How the benchmark works](benchmarks/README.md)\n"]
    v2s = load(os.path.join(V2, "summary.json"))
    if v2s:
        m, w = v2s["mean"], v2s["wins"]
        sc.save(sc.scoreboard(m, f"Benchmark: mean score across {v2s['n']} scenarios", "decision-grade reports · script ceilings, then two blind judges",
                              "benchmarks/README.md", scale=100), os.path.join(IMG, "_scoreboard.svg"))
        L[-1] = L[-1].replace("[How the benchmark works](benchmarks/README.md)", "[How the benchmark works](benchmarks/README.md)")
        L.append("![Benchmark scores](docs/use-cases/img/_scoreboard.svg)\n")
        L.append(f"With Prism, the same model scored higher in **{w['claude']['prism_wins']} of {v2s['n']}** scenarios for Claude "
                 f"(mean {m['claude_bare']} → **{m['claude_prism']}** out of 100) and **{w['chatgpt']['prism_wins']} of {v2s['n']}** for ChatGPT "
                 f"({m['chatgpt_bare']} → **{m['chatgpt_prism']}**). Most of the gain is measurement and traceability; the accuracy "
                 f"criterion alone rose less. [Full results](benchmarks/README.md)\n")

    L.append("| Domain | Pages | Start with |\n| --- | ---: | --- |")
    for cat, name, _ in CATEGORIES:
        rs = bycat.get(cat) or []
        if rs:
            L.append(f"| **[{name}](docs/use-cases/{cat}/README.md)** | {len(rs)} | " +
                     " · ".join(f"[{r['title']}](docs/use-cases/{cat}/{r['slug']}.md)" for r in rs[:3]) + " |")
    L.append("<!-- use-cases:end -->")
    path = os.path.join(ROOT, "README.md")
    txt = open(path).read()
    block = "\n".join(L)
    if "<!-- use-cases:start -->" in txt:
        txt = re.sub(r"<!-- use-cases:start -->.*?<!-- use-cases:end -->", lambda m: block, txt, flags=re.S)
        open(path, "w").write(txt)


def main():
    os.makedirs(IMG, exist_ok=True)
    pages = []
    for s in SCENARIOS:
        try:
            r = build_page(s, None)
        except Exception as e:
            import traceback
            traceback.print_exc()
            print("FAILED", s["slug"], e)
            r = None
        if r:
            pages.append(r)
    write_indexes(pages)
    board = None
    flags_doc(pages)
    readme_block(pages, board)
    print(f"{len(pages)} pages, {sum(p['charts'] for p in pages)} charts, "
          f"{sum(1 for p in pages if p.get('cmp'))} compared, {sum(1 for p in pages if p['live'])} live")


if __name__ == "__main__":
    main()
