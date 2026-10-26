#!/usr/bin/env python3
"""stats — the numbers, and only numbers that exist.

Two kinds of statistic reach a writer from here, and they are kept apart on
purpose because they fail in different ways.

COMPUTED series come from ClickHouse aggregates: papers per year, articles per
month, patents per year, and the growth rates derived from them in Python. They
are exact, and their only failure mode is the window — a research series that
runs to "now" reads as a collapse, because the current year is a third
ingested. Every series here stops at a lag-safe bound and says where it stopped.

EXTRACTED statistics come out of paper abstracts verbatim. The model is allowed
to CHOOSE which sentence answers the claim and to say what the number measures.
It is not allowed to write the number: every returned figure must occur in the
sentence it was taken from, and the sentence must occur in the abstract it is
attributed to. A statistic that fails either check is dropped and counted in
`rejected`, because the interesting fact about a research assistant is not that
it produced ten numbers but how many it had to throw away.
"""
from __future__ import annotations

import re
from datetime import date, timedelta

from . import cache, ch, llm, query, progress

TTL = 43200
_SENT = re.compile(r"(?<=[.!?])\s+")
_HAS_STAT = re.compile(
    r"(\d+(?:\.\d+)?\s?%|\bper cent\b|percent|\bCI\b|\bOR\b|\bRR\b|\bHR\b|"
    r"\bp\s?[=<]\s?0?\.\d+|\b\d{2,}(?:[,.]\d+)*\s?(?:million|billion|thousand|"
    r"people|patients|participants|cases|deaths|years|kg|km|tonnes|USD|\$))", re.I)


# ═══════════════════════════ computed series ═════════════════════════════════
@cache.singleflight
@progress.stage('trends')
def series(qo: dict, corpus: str = "research_typed") -> dict:
    """A yearly (or monthly, for news) count for this claim, right-censored.

    OpenAlex holds 37.5M works for 2025 and 10.9M for 2026 so far; the news
    corpus thins from ~2.2M articles in May 2026 to 15k in July. A series that
    runs to today shows a cliff that is an artefact of ingest, and a writer
    told "research on this collapsed in 2026" would be told something false."""
    if not qo.get("available"):
        return {"available": False, "reason": "claim not resolvable"}
    if corpus == "news":
        sql = (f"SELECT toString(toStartOfMonth(datetime)) m, count() c FROM "
               f"{ch.TABLE['news']} WHERE datetime >= '2019-01-01' AND datetime < "
               f"'{ch.NEWS_LAST_MONTH}' AND {query.predicate(qo, 'news')} "
               f"GROUP BY m ORDER BY m")
        unit, window = "month", f"2019-01..{ch.NEWS_LAST_MONTH} (exclusive)"
    elif corpus == "patents":
        sql = (f"SELECT toString(publication_year) y, count() c FROM "
               f"{ch.TABLE['patents']} WHERE publication_year BETWEEN 2010 AND "
               f"{ch.PATENT_LAST_YEAR} AND {query.predicate(qo, 'patents')} "
               f"GROUP BY y ORDER BY y")
        unit, window = "year", f"2010-{ch.PATENT_LAST_YEAR}"
    else:
        sql = (f"SELECT toString(publication_year) y, count() c FROM "
               f"{ch.TABLE['research_typed']} WHERE publication_year BETWEEN "
               f"{ch.TYPED_FIRST_YEAR} AND {ch.RESEARCH_LAST_YEAR} AND "
               f"{query.predicate(qo, 'research_typed')} GROUP BY y ORDER BY y")
        unit, window = "year", f"{ch.TYPED_FIRST_YEAR}-{ch.RESEARCH_LAST_YEAR}"
    corpus_key = corpus if corpus in ('news', 'patents') else 'research_typed'
    coverage = ch.coverage_of([corpus_key])
    if coverage['partial']:
        return {'available':False, 'reason':'The database is temporarily unavailable.', 'coverage':coverage}
    ck = cache.key('stats.series.v2', sql)
    hit = cache.get(ck)
    if hit:
        progress.emit('cached')
        return {**hit, 'cached':True, 'lane':qo.get('lane'), 'coverage':coverage}
    try:
        rows = [{"period": r[0], "n": int(r[1])} for r in ch.chq_rows(sql, 280)]
    except Exception as e:
        return {"available": False, "reason": f"{type(e).__name__}: {e}"}
    if not rows:
        return {"available": False, "reason": "nothing in this corpus matches"}
    start = '2019-01-01' if corpus == 'news' else f"{2010 if corpus == 'patents' else ch.TYPED_FIRST_YEAR}-01-01"
    end = ch.NEWS_LAST_MONTH if corpus == 'news' else f"{(ch.PATENT_LAST_YEAR if corpus == 'patents' else ch.RESEARCH_LAST_YEAR) + 1}-01-01"
    rows = fill_periods(rows, 'monthly' if corpus == 'news' else 'yearly', start, end)
    out = {"available": True, "corpus": corpus, "unit": unit, "window": window,
            "lane": qo.get("lane"), "points": rows, "total": sum(r["n"] for r in rows),
            "trend": trend(rows),
            "censored_at": (ch.NEWS_LAST_MONTH if corpus == "news" else
                            str(ch.PATENT_LAST_YEAR if corpus == "patents"
                                else ch.RESEARCH_LAST_YEAR)),
            "why_censored": ("the newest period is excluded because ingest lags "
                             "publication; including it would print a collapse "
                             "that did not happen")}
    cache.put(ck, out, 300)
    return {**out, 'coverage':coverage}


def trend(points: list) -> dict:
    """Direction and rate, computed here rather than described by a model.

    CAGR over a count series is only meaningful when both ends are non-trivial,
    so a series starting at 2 papers reports the multiple instead — 2 to 20 is
    'ten times', not '115% a year', and the second reads as precision that
    isn't there."""
    pts = [p for p in points if p["n"] is not None]
    if len(pts) < 3:
        return {"available": False, "reason": "fewer than three periods"}
    first, last = pts[0], pts[-1]
    span = len(pts) - 1
    def year_fraction(period):
        s = str(period)
        if re.fullmatch(r"\d{4}", s):
            return float(s)
        d = date.fromisoformat(s[:10] if len(s) >= 10 else s + '-01')
        start = date(d.year, 1, 1)
        return d.year + (d - start).days / (date(d.year + 1, 1, 1) - start).days
    try:
        years = year_fraction(last['period']) - year_fraction(first['period'])
    except (TypeError, ValueError, OverflowError):
        years = None
    head = sum(p["n"] for p in pts[:max(1, len(pts) // 3)])
    tail = sum(p["n"] for p in pts[-max(1, len(pts) // 3):])
    out = {"available": True, "from": first["period"], "to": last["period"],
           "first": first["n"], "last": last["n"], "peak": max(p["n"] for p in pts),
           "peak_period": max(pts, key=lambda p: p["n"])["period"],
           "early_third": head, "late_third": tail}
    out['elapsed_years'] = round(years, 6) if years is not None else None
    if first["n"] >= 10 and last["n"] >= 10 and span >= 2 and years and years >= 1:
        out["cagr_pct"] = round(100 * ((last["n"] / first["n"]) ** (1 / years) - 1), 1)
        out['rate_unit'] = 'annual'
    elif first["n"] > 0:
        out["multiple"] = round(last["n"] / first["n"], 1)
    ratio = (tail / head) if head else None
    out["direction"] = ("rising" if ratio is not None and ratio > 1.25 else
                        "falling" if ratio is not None and ratio < 0.8 else
                        "rising" if head == 0 and tail > 0 else "flat")
    out["late_vs_early"] = round(ratio, 2) if ratio is not None else None
    return out


def fill_periods(points, granularity, start, end):
    """Fill zero buckets after a successful aggregate; mark partial boundaries."""
    lo, hi = date.fromisoformat(start), date.fromisoformat(end)
    bucket = lo
    if granularity == 'weekly':
        bucket -= timedelta(days=bucket.weekday())
    elif granularity in ('monthly', 'quarterly', 'yearly'):
        month = 1 if granularity == 'yearly' else (lo.month - 1) // 3 * 3 + 1 if granularity == 'quarterly' else lo.month
        bucket = date(lo.year, month, 1)
    lookup = {str(p['period']): p for p in points}
    year_labels = bool(points) and all(len(str(p['period'])) == 4 for p in points)
    out = []
    while bucket < hi:
        if granularity in ('daily', 'weekly'):
            following = bucket + timedelta(days=1 if granularity == 'daily' else 7)
        else:
            step = {'monthly': 1, 'quarterly': 3, 'yearly': 12}[granularity]
            m = bucket.year * 12 + bucket.month - 1 + step
            following = date(m // 12, m % 12 + 1, 1)
        key = str(bucket.year) if year_labels else bucket.isoformat()
        out.append({**lookup.get(key, {'period': key, 'n': 0}),
                    'partial_period': bucket < lo or following > hi})
        bucket = following
    return out


# ═══════════════════════════ geography ═══════════════════════════════════════
def geography(qo: dict, country: str | None = None, limit: int = 12) -> dict:
    """Where this claim is true, or at least where it is studied and reported.

    Three different columns, three different meanings, and the payload keeps
    them apart: news `country_pri` is where an article is ABOUT, PubMed
    `country` is where the journal is published, and patent
    `assignee_countries` is where the applicant is. None of them is "where the
    phenomenon is", and a chart that blends them says something nobody
    measured.

    OpenAlex has no country column on this cluster, which is why research
    geography here is PubMed-only and says so. Since 2026-10-22 it also reads
    the first author's AFFILIATION country (`research_authorship`): on dengue,
    journal country ranked the US, England and the Netherlands first, while
    the authors are in India, the US, Brazil and Thailand."""
    if not qo.get("available"):
        return {"available": False, "reason": "claim not resolvable"}
    # Rank countries over the WHOLE claim, not the claim scoped to one country:
    # `country` picks the focus row, it must not filter the table it is ranked in.
    qo = {**qo, "geo": None}
    T = ch.TABLE

    def rows(sql, timeout=280):
        return lambda: ch.chq_rows(sql, timeout=timeout)

    res = ch.parallel([
        rows(f"SELECT assumeNotNull(country_pri) c, count() n FROM {T['news']} "
             f"WHERE datetime >= '2019-01-01' AND datetime < '{ch.NEWS_LAST_MONTH}' "
             f"AND {query.predicate(qo, 'news')} AND isNotNull(country_pri) "
             f"GROUP BY c ORDER BY n DESC LIMIT {limit}"),
        rows(f"SELECT country, count() n FROM {T['pubmed']} WHERE pub_year BETWEEN "
             f"2000 AND {ch.RESEARCH_LAST_YEAR} AND {query.predicate(qo, 'pubmed')} "
             f"AND country != '' GROUP BY country ORDER BY n DESC LIMIT {limit}"),
        rows(f"SELECT c, count() n FROM (SELECT arrayJoin(assignee_countries) c FROM "
             f"{T['patents']} WHERE publication_year BETWEEN 2010 AND "
             f"{ch.PATENT_LAST_YEAR} AND {query.predicate(qo, 'patents')}) "
             f"GROUP BY c ORDER BY n DESC LIMIT {limit}"),
    ], workers=3)
    auth = ch.chq_rows(
        f"SELECT c, count() n FROM (SELECT trim(BOTH ' .;' FROM arrayElement(splitByChar(',', "
        f"replaceRegexpAll(affiliations[1], '(?i)electronic address.*$|\\\\S+@\\\\S+', '')), -1)) c "
        f"FROM {T['pubmed']} WHERE pub_year BETWEEN 2000 AND {ch.RESEARCH_LAST_YEAR} AND "
        f"{query.predicate(qo, 'pubmed')} AND length(affiliations) > 0) WHERE c != '' "
        f"GROUP BY c ORDER BY n DESC LIMIT 80", timeout=280) or []
    agg = {}
    for c, n in auth:
        k = _country_name(c)
        if k:
            agg[k] = agg.get(k, 0) + int(n)
    authors = [{"country": k, "papers": v} for k, v in sorted(agg.items(), key=lambda kv: -kv[1])[:limit]]
    news = [{"country": r[0], "articles": int(r[1])} for r in (res[0] or [])]
    pm = [{"country": r[0], "papers": int(r[1])} for r in (res[1] or [])]
    pat = [{"country": r[0], "patents": int(r[1])} for r in (res[2] or [])]
    out = {"available": bool(news or pm or pat or authors),
           "research_authorship": {"what": "country of the first author's affiliation (PubMed) — "
                                   "where the research is done, as far as an affiliation says",
                                   "rows": authors},
           "news_coverage": {"what": "country an article is about", "rows": news},
           "research_publication": {"what": "country of the publishing journal "
                                    "(PubMed) — not where the study was done",
                                    "rows": pm},
           "patent_origin": {"what": "assignee country", "rows": pat},
           "note": "three different questions; do not add them together"}
    if country:
        out["focus"] = _country_focus(country, news, pm, pat)
    return out


_COUNTRY_ALIASES = {
    "usa": "United States", "us": "United States", "u.s.a": "United States", "united states of america": "United States",
    "united states": "United States", "uk": "United Kingdom", "u.k": "United Kingdom", "england": "United Kingdom",
    "scotland": "United Kingdom", "wales": "United Kingdom", "great britain": "United Kingdom",
    "brasil": "Brazil", "pr china": "China", "p.r. china": "China", "people's republic of china": "China",
    "p. r. china": "China", "republic of korea": "South Korea", "korea": "South Korea", "the netherlands": "Netherlands",
    "viet nam": "Vietnam", "türkiye": "Turkey", "turkiye": "Turkey", "méxico": "Mexico", "españa": "Spain",
    "italia": "Italy", "deutschland": "Germany", "russian federation": "Russia", "iran (islamic republic of)": "Iran",
}


def _country_name(raw: str) -> str | None:
    """Normalise the tail of an affiliation string to a country name, or None
    when the tail is clearly not one (a postcode, a department, a long phrase)."""
    c = (raw or "").strip().strip(".;:").strip()
    if not c or len(c) > 40 or any(ch.isdigit() for ch in c) or len(c.split()) > 4:
        return None
    return _COUNTRY_ALIASES.get(c.lower(), c)


def _country_focus(country: str, news, pm, pat) -> dict:
    c = country.strip().lower()

    def share(rows, key):
        tot = sum(r[key] for r in rows) or 0
        me = next((r[key] for r in rows if (r["country"] or "").lower() == c), 0)
        rank = next((i + 1 for i, r in enumerate(rows)
                     if (r["country"] or "").lower() == c), None)
        return {"n": me, "of_top": tot, "share_pct": round(100 * me / tot, 1) if tot else None,
                "rank_in_top": rank}
    return {"country": country, "news": share(news, "articles"),
            "research": share(pm, "papers"), "patents": share(pat, "patents"),
            "caveat": ("shares are of the top rows shown, not of the whole "
                       "corpus, and absence from the list means outside the top "
                       "results rather than zero")}


# ═══════════════════════════ extracted statistics ════════════════════════════
def stat_sentences(docs: list, limit: int = 24) -> list:
    """Every sentence in the retrieved abstracts that actually carries a figure.

    Done in Python before the model sees anything: it means the model's job is
    to pick among real sentences rather than to remember numbers, and it means
    a claim with no numeric evidence in its literature returns an empty list
    instead of a plausible invention."""
    out = []
    for d in docs:
        for s in _SENT.split(d.get("abstract") or ""):
            s = s.strip()
            if 40 <= len(s) <= 400 and _HAS_STAT.search(s):
                out.append({"doc_id": d["id"], "title": d["title"], "year": d.get("year"),
                            "tier": d.get("tier"), "venue": d.get("venue"),
                            "url": d.get("url"), "sentence": s})
    out.sort(key=lambda x: -(x.get("year") or 0))
    return out[:limit]


_STAT_SYS = (
 "You select which of these real sentences answer a claim with a number, and "
 "you label what each number measures. You NEVER write a number of your own and "
 "you NEVER round, convert or combine: every figure you return must appear "
 "character-for-character in the sentence you took it from.\n"
 "Return JSON:\n"
 '{"stats": [{"doc_id": str, "value": str, "measures": str, "population": str|null, '
 '"period": str|null, "sentence": str, "caveat": str|null}]}\n'
 "* value — copied exactly, with its unit or interval ('47.5%', '0.60 (95%CI: "
 "0.46, 0.79)').\n"
 "* measures — at most 12 words: what the figure is of.\n"
 "* sentence — the source sentence, verbatim.\n"
 "* caveat — the limitation the sentence itself states, or null. Never invent one.\n"
 "Return at most 8, most useful first. Skip sentences whose number is a sample "
 "size or a p-value with nothing attached.")


@cache.singleflight
@progress.stage('numbers')
def find_statistics(qo: dict, docs: list, limit: int = 8,
                    subject_mode: bool = False) -> dict:
    """Numbers a writer can actually put in a paragraph, each with its source.

    Every returned figure is checked twice: the sentence must occur in the
    abstract it is attributed to, and the value must occur in the sentence. The
    rejects are counted in the payload rather than hidden, because that count
    is the honest measure of how much of this to trust."""
    ck = cache.key('statistics.extraction.v1', qo.get('claim'), docs, limit,
                   subject_mode, _STAT_SYS, llm.MODEL, llm.EFFORT)
    hit = cache.get(ck)
    if hit:
        progress.emit('cached')
        return {**hit, 'cached':True}
    sents = stat_sentences(docs)
    if not sents:
        return {"available": False,
                "reason": ("no sentence in the retrieved abstracts carries a "
                           "figure — this claim's literature is qualitative, or "
                           "the numbers are in tables rather than abstracts"),
                "searched_documents": len(docs)}
    packed = "\n\n".join(f"[{s['doc_id']}] ({s.get('year')}) {s['sentence']}"
                         for s in sents)
    # A subject is not a claim. Asked which sentences "answer" the claim
    # "groundwater depletion in India", the selection step correctly answers
    # none — a noun phrase makes no assertion for a figure to bear on. When the
    # caller is briefing a subject rather than checking a claim, the question
    # becomes which figures characterise it.
    head = (f"SUBJECT: {qo['claim']}\nSelect the figures that best characterise "
            f"this subject." if subject_mode else f"CLAIM: {qo['claim']}")
    out = llm.call_json(_STAT_SYS, f"{head}\n\nSENTENCES:\n{packed}",
                        max_tokens=4000)
    if out is None:
        return {"available": False, "stats": [],
                "reason": ("the selection step returned nothing parseable — the "
                           "candidate sentences below are real and can be read "
                           "directly"), "candidate_sentences": len(sents),
                "candidates": sents[:12]}
    by_doc = {}
    for d in docs:
        by_doc[d["id"]] = d
        by_doc[d["id"].split(":", 1)[-1]] = d
    kept, rejected = [], []
    for st in ((out or {}).get("stats") or []):
        d = by_doc.get(str(st.get("doc_id", "")).strip())
        sent = str(st.get("sentence") or "").strip()
        val = str(st.get("value") or "").strip()
        if not d or not sent or not val:
            rejected.append({"value": val, "why": "no source document named"})
            continue
        if not llm.verify_quote(sent, d.get("abstract") or ""):
            rejected.append({"value": val, "why": "sentence not found in that abstract"})
            continue
        if llm.numbers_in(val) and not (llm.numbers_in(val) <= llm.numbers_in(sent)):
            rejected.append({"value": val, "why": "figure not present in its own source sentence"})
            continue
        kept.append({
            "value": val, "measures": str(st.get("measures") or "")[:120],
            "population": st.get("population"), "period": st.get("period"),
            "caveat": st.get("caveat"), "sentence": sent,
            "source": {"id": d["id"], "title": d["title"], "year": d.get("year"),
                       "venue": d.get("venue"), "tier": d.get("tier"),
                       "strength": d.get("strength"), "url": d.get("url"),
                       "doi": d.get("doi")},
        })
    kept.sort(key=lambda k: -(k["source"].get("year") or 0))
    if not kept and not rejected:
        return {"available": False, "stats": [], "rejected": [],
                "reason": ("the retrieved abstracts carry figures, but none of "
                           "them measures what this "
                           + ("subject is about" if subject_mode else "claim asserts")),
                "candidate_sentences": len(sents), "candidates": sents[:12]}
    result = {"available": bool(kept), "stats": kept[:limit], "rejected": rejected,
            "candidate_sentences": len(sents),
            "note": ("every figure is copied from the source sentence shown and "
                     "verified against the abstract it came from")}
    if kept:
        cache.put(ck, result, TTL)
    return result


# ═══════════════════════════ attention gap ═══════════════════════════════════
def attention_gap(qo: dict, limit: int = 8) -> dict:
    """Topics inside this claim's research cluster that the news is not covering.

    A genuine editorial signal, and computable: rank the cluster's OpenAlex
    topics by paper count, then measure how much news coverage each topic name
    draws. The topics with real literature and thin coverage are where a writer
    has something to say that nobody has said."""
    tops = query.topics(qo, limit=14)
    if not tops:
        return {"available": False, "reason": "no topics on this cluster"}
    sel = ", ".join(
        f"countIf({ch.prose_match('assumeNotNull(text)', [t['topic'].lower()])}) AS t{i}"
        for i, t in enumerate(tops))
    try:
        row = ch.chq_one(
            f"SELECT {sel} FROM {ch.TABLE['news']} WHERE datetime >= '2023-01-01' "
            f"AND datetime < '{ch.NEWS_LAST_MONTH}'", timeout=280)
    except Exception as e:
        return {"available": False, "reason": f"{type(e).__name__}: {e}"}
    rows = []
    for i, t in enumerate(tops):
        news_n = int(row[i] or 0) if row else 0
        rows.append({"topic": t["topic"], "papers": t["papers"], "articles": news_n,
                     "articles_how": "ledes containing the exact OpenAlex topic label — a taxonomy string, "
                                     "not news vocabulary; 0 means the label never appears, NOT that the subject is uncovered",
                     "papers_per_article": round(t["papers"] / news_n, 1) if news_n
                     else None})
    under = sorted([r for r in rows if r["papers"] >= 50],
                   key=lambda r: -(r["papers_per_article"] or 1e9))
    return {"available": True, "topics": rows, "under_covered": under[:limit],
            "window": "news 2023-01-01 onward; papers 2017 onward",
            "what": ("a high papers-per-article ratio means the research exists "
                     "and the coverage does not"),
            "caveat": ("`articles` matches the literal topic label in ~320-char ledes. Before writing "
                       "'no coverage', re-count with the subject's own news terms (news.trends on e.g. "
                       "'ai drug discovery'): on 2026-08-25 a label with articles=0 had 318 such mentions")}
