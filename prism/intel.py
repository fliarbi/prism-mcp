#!/usr/bin/env python3
"""intel — the composed answers: gaps, briefs, radar, tables, libraries.

Everything here is assembled from `query`, `evidence` and `stats`. The rules
those modules enforce still hold: numbers are computed or quoted, never
written; a lane is always named; a thin answer says it is thin instead of
padding itself out.

The one idea worth stating plainly, because it is what separates these tools
from a summariser: WHAT IS MISSING IS COMPUTED FROM THE CORPUS. A model asked
"what is this article missing?" will produce a fluent list of things articles
usually mention. Asking the corpus produces the topics that actually carry
literature next to this subject, ranked by how much, and the answer changes
when the literature changes.
"""
from __future__ import annotations

import re

from . import cache, ch, cite, evidence, llm, query, stats

TTL = 43200


# ═══════════════════════════ research gaps ═══════════════════════════════════
def research_gaps(qo: dict) -> dict:
    """Which parts of a claim the literature actually covers.

    A broad claim is rarely wholly right or wrong — it is a stack of
    sub-assertions with very different evidence behind each. 'AI will replace
    many accounting jobs' has a real literature on bookkeeping automation and
    almost none on whole-occupation replacement, and that difference is the
    single most useful thing a writer can be told about the sentence.

    All components are counted in ONE scan."""
    comps = [c for c in (qo.get("components") or []) if c]
    if not comps:
        return {"available": False,
                "reason": "this claim has no separable components to check"}
    subj = query.pole(qo, "subject")
    sel = []
    for i, c in enumerate(comps):
        words = [w for w in re.split(r"[^a-z0-9]+", c.lower()) if len(w) > 3]
        phrase = c.lower()
        pole = {"phrases": [phrase], "terms": words[:2]}
        sel.append(f"countIf({ch.m_typed(pole)}) AS c{i}")
    sel.append(f"countIf({query.predicate(qo, 'research_typed', lane='subject')}) AS base")
    try:
        row = ch.chq_one(
            f"SELECT {', '.join(sel)} FROM {ch.TABLE['research_typed']} WHERE "
            f"publication_year BETWEEN {ch.TYPED_FIRST_YEAR} AND "
            f"{ch.RESEARCH_LAST_YEAR}", timeout=280)
    except Exception as e:
        return {"available": False, "reason": f"{type(e).__name__}: {e}"}
    out = []
    for i, c in enumerate(comps):
        n = int(row[i] or 0)
        out.append({"component": c, "papers": n,
                    "evidence": "yes" if n >= 100 else "thin" if n >= 15 else "no",
                    "means": ("a literature exists on this piece" if n >= 100 else
                              "a handful of papers touch this" if n >= 15 else
                              "the corpus has effectively nothing on this piece")})
    base = int(row[-1] or 0)
    covered = [o for o in out if o["evidence"] == "yes"]
    missing = [o for o in out if o["evidence"] == "no"]
    return {"available": True, "claim": qo["claim"], "subject_papers": base,
            "components": out, "covered": len(covered), "unevidenced": len(missing),
            "weakest": missing or [o for o in out if o["evidence"] == "thin"],
            "window": f"{ch.TYPED_FIRST_YEAR}-{ch.RESEARCH_LAST_YEAR}",
            "note": ("counts are papers whose title or topic matches the component, "
                     "so a real literature under different words can read as thin — "
                     "check the phrasing before concluding a gap is real")}


# ═══════════════════════════ rewriting a claim ═══════════════════════════════
_IMPROVE_SYS = (
 "You rewrite one sentence so it says only what the evidence supports. You are "
 "given the measured evidence profile and real findings; you may use no other "
 "knowledge and you may write NO number that is not in the material given.\n"
 "Return JSON:\n"
 '{"assessment": str,          // <=30 words: what is wrong with the sentence as '
 'written, or "" if nothing is\n'
 ' "options": [{"text": str, "why": str}],   // 2-3 rewrites, strongest first\n'
 ' "verdict": "overstated"|"supported"|"contested"|"unsupported"}\n'
 "* Keep the writer's voice and length. You are correcting the strength of a "
 "claim, not rewriting the paragraph.\n"
 "* If the evidence is mixed, the rewrite should say so ('has been associated "
 "with', 'evidence is mixed'), not pick a side.\n"
 "* If the evidence supports the sentence as written, say so and return one "
 "option that is the original.")


def improve_claim(qo: dict, prof: dict) -> dict:
    """A better-supported version of the writer's own sentence.

    The model sees only the measured profile and the verified findings, and
    every number it writes is checked against them. An option that reaches for
    a figure nobody measured is dropped, not printed with a caveat."""
    docs = [d for d in (prof.get("documents") or []) if d.get("grounded")][:10]
    mix = prof.get("corpus_stance") or {}
    tally = prof.get("tally") or {}
    material = {
        "claim": qo["claim"],
        "papers_on_subject": (qo.get("lane_counts") or {}).get("subject"),
        "papers_on_both_poles": (qo.get("lane_counts") or {}).get("intersection"),
        "corpus_mix": mix.get("sides"), "corpus_reading": mix.get("reading"),
        "documents_read": tally.get("counts"),
        "findings": [{"stance": d["stance"], "tier": d["tier"], "year": d.get("year"),
                      "quote": d.get("quote")} for d in docs],
    }
    src = [str(material)] + [d.get("quote") or "" for d in docs]
    out = llm.call_json(_IMPROVE_SYS, str(material), max_tokens=1500)
    if not out:
        return {"available": False, "reason": "the rewrite step returned nothing"}
    kept, dropped = [], []
    for o in (out.get("options") or [])[:3]:
        t = str(o.get("text") or "").strip()
        if not t:
            continue
        bad = llm.ungrounded_numbers(t, src)
        (dropped if bad else kept).append(
            {"text": t, "why": str(o.get("why") or "")[:160],
             **({"rejected_numbers": bad} if bad else {})})
    return {"available": bool(kept), "claim": qo["claim"],
            "verdict": out.get("verdict"), "assessment": out.get("assessment"),
            "options": kept, "rejected_options": dropped,
            "based_on": {"documents_read": tally.get("counts"),
                         "corpus_mix": mix.get("sides"),
                         "lane": qo.get("lane"), "lane_note": qo.get("lane_note")}}


# ═══════════════════════════ research brief ══════════════════════════════════
def research_brief(topic: str, geo: str | None = None) -> dict:
    """A structured brief on a subject: what is established, what is contested,
    the numbers, the direction of travel, and who is working on it.

    Every section is a separate measurement and each one can come back
    unavailable. A brief with three of six sections present is a true brief;
    one padded to six is not."""
    qo = query.build(topic, geo=geo, depth="full")
    if not qo.get("available"):
        return {"available": False, "reason": qo.get("reason"), "topic": topic}
    docs = evidence.fetch_docs(qo, limit=26)
    res = ch.parallel([
        lambda: evidence.corpus_stance(qo),
        lambda: stats.series(qo, "research_typed"),
        lambda: stats.series(qo, "news"),
        lambda: stats.geography(qo, country=geo),
        lambda: _institutions(qo),
    ], workers=5)
    mix, ser, news_ser, geo_rows, insts = res
    numbers = stats.find_statistics(qo, docs, subject_mode=True)
    # No document-level stance here, deliberately. Stance is measured AGAINST A
    # CLAIM, and a brief is asked about a SUBJECT: run it on "groundwater
    # depletion in India" and every paper is correctly labelled `unrelated`,
    # because a paper does not agree or disagree with a noun phrase. What a
    # brief needs instead is the study-design ladder, which is already on every
    # document, plus the corpus-wide orientation mix.
    established = [d for d in docs
                   if d["tier"] in ("meta_analysis", "guideline", "review")]
    newest = sorted([d for d in docs if d.get("year")],
                    key=lambda d: -(d["year"] or 0))[:6]
    return {
        "available": True, "topic": topic, "subject": qo.get("subject"),
        "lane": qo.get("lane"), "lane_note": qo.get("lane_note"),
        "volumes": qo.get("volumes"),
        "what_is_established": [{"title": d["title"], "year": d.get("year"),
                                 "tier": d["tier"], "why_tier": d.get("why_tier"),
                                 "cited_by": d.get("cited_by"), "venue": d.get("venue"),
                                 "url": d.get("url")} for d in established[:6]],
        "established_note": ("reviews, meta-analyses and guidelines matching this "
                             "subject — the papers whose job is to say what is "
                             "settled" if established else
                             "no review or guideline-tier paper matched this "
                             "subject in the reading corpus"),
        "what_is_contested": {"mix": mix.get("sides"), "reading": mix.get("reading"),
                              "contested_pct": mix.get("contested_pct"),
                              "papers": mix.get("papers")},
        "key_numbers": numbers.get("stats", []),
        "key_numbers_note": numbers.get("reason"),
        "key_number_candidates": numbers.get("candidates", [])[:6]
        if not numbers.get("stats") else [],
        "direction_of_travel": {"research": ser.get("trend"),
                                "news": news_ser.get("trend")},
        "geography": geo_rows,
        "who_works_on_it": insts,
        "most_recent": [{"title": d["title"], "year": d.get("year"),
                         "venue": d.get("venue"), "url": d.get("url")} for d in newest],
        "sources": cite.bibliography(
            sorted(docs, key=lambda d: (-d["tier_rank"], -(d.get("cited_by") or 0)))[:12],
            "apa"),
        "coverage": ch.coverage_of(["research_typed", "research", "news"]),
    }


def _institutions(qo: dict, limit: int = 8) -> dict:
    """Institutions ranked by LIFT over their share of the whole corpus.

    Raw counts here are a trap that has already fired on this cluster: a venue
    abbreviation expanded into an institution name puts 'National Institute for
    Fusion Science' on 20.7M rows — 21% of the corpus — and it would top the
    list for any subject at all. Anything holding more than 2% of the corpus is
    plumbing, not a research group."""
    try:
        rows = ch.chq_rows(
            f"SELECT i, count() c FROM (SELECT arrayJoin(institution_names) i FROM "
            f"{ch.TABLE['research_typed']} WHERE publication_year BETWEEN "
            f"{ch.RESEARCH_LAST_YEAR - 8} AND {ch.RESEARCH_LAST_YEAR} AND "
            f"{query.predicate(qo, 'research_typed')} AND notEmpty(institution_names)) "
            f"GROUP BY i ORDER BY c DESC LIMIT 40", timeout=280)
    except Exception as e:
        return {"available": False, "reason": f"{type(e).__name__}: {e}"}
    if not rows:
        return {"available": False, "reason": "no institution names on these papers"}
    names = [r[0] for r in rows[:20]]
    sel = ", ".join(f"countIf(has(institution_names, {ch.sql_arr([n])}[1])) AS i{k}"
                    for k, n in enumerate(names))
    try:
        base = ch.chq_one(
            f"SELECT {sel}, count() FROM {ch.TABLE['research_typed']} WHERE "
            f"publication_year BETWEEN {ch.RESEARCH_LAST_YEAR - 8} AND "
            f"{ch.RESEARCH_LAST_YEAR}", timeout=280)
    except Exception:
        base = None
    out, corpus_n = [], int(base[-1]) if base else 0
    matched = sum(int(r[1]) for r in rows)
    for k, (name, c) in enumerate(rows[:20]):
        c = int(c)
        share_corpus = (int(base[k]) / corpus_n) if base and corpus_n else None
        if share_corpus and share_corpus > 0.02:
            continue          # corpus plumbing, not a research group
        lift = ((c / matched) / share_corpus) if share_corpus else None
        out.append({"institution": name, "papers": c,
                    "lift_vs_corpus": round(lift, 1) if lift else None})
    out.sort(key=lambda r: -(r["lift_vs_corpus"] or 0))
    return {"available": bool(out), "rows": out[:limit],
            "ranked_by": "lift over the institution's share of the whole corpus",
            "window": f"{ch.RESEARCH_LAST_YEAR - 8}-{ch.RESEARCH_LAST_YEAR}"}


# ═══════════════════════════ research radar ══════════════════════════════════
def radar(topic: str, since_year: int | None = None, geo: str | None = None) -> dict:
    """What changed lately on a subject the writer is working on.

    Six independent measurements, each of which can be absent: new work, the
    direction of the research and news series, whether a named country diverges
    from the world, whether recent framing has shifted against older framing,
    and which parts of the literature the news is not covering."""
    qo = query.build(topic, geo=geo, depth="quick")
    if not qo.get("available"):
        return {"available": False, "reason": qo.get("reason"), "topic": topic}
    since = since_year or (ch.RESEARCH_LAST_YEAR - 1)
    res = ch.parallel([
        lambda: _new_work(qo, since) or [
            {"title": d["title"], "year": d.get("year"), "venue": d.get("venue"), "tier": d["tier"],
             "url": d.get("url")} for d in (evidence.fetch_docs(qo, limit=10, want_recent=True) or [])
            if (d.get("year") or 0) >= since],
        lambda: stats.series(qo, "research_typed"),
        lambda: stats.series(qo, "news"),
        lambda: _framing_shift(qo, since),
        lambda: stats.attention_gap(qo),
        lambda: stats.geography(qo, country=geo) if geo else {"available": False},
    ], workers=6)
    docs, ser, news_ser, shift, gap, geo_rows = res
    return {
        "available": True, "topic": topic, "subject": qo.get("subject"),
        "since": since,
        "new_work": (docs or [])[:10],
        "new_work_how": ("the most-cited typed papers published since the start year whose title "
                         "carries one of the subject's own phrases"),
        "research_trend": (ser or {}).get("trend"),
        "news_trend": (news_ser or {}).get("trend"),
        "framing_shift": shift,
        "under_covered": (gap or {}).get("under_covered"),
        "geography": geo_rows if geo else None,
        "coverage": ch.coverage_of(["research_typed", "news"]),
        "how_to_read": ("nothing here says the claim changed — it says the "
                        "literature moved. A rising cautionary share is a reason "
                        "to re-read, not a verdict"),
    }


def _new_work(qo: dict, since: int, limit: int = 10) -> list:
    """Recent work that the field is actually reading.

    The radar used to list whatever the evidence fetcher's recency lanes
    returned, which on "mrna vaccine" was HPV, RSV-protein and adenoviral
    vaccine papers (PubMed matched the MeSH heading 'Vaccines'), and on
    quantum computing a handful of minor 2025 papers while the error-correction
    milestones were absent. New work is now the most-cited typed papers since
    `since` whose TITLE carries a subject phrase, with their orientation."""
    phrases = query.pole(qo, "subject")["phrases"]
    if not phrases:
        return []
    T = ch.TABLE["research_typed"]
    rows = ch.chq_rows(
        f"SELECT title, publication_year, toString(venue_name), doi, oa_url, cited_by_count, orientation "
        f"FROM {T} WHERE publication_year BETWEEN {since} AND {ch.RESEARCH_LAST_YEAR} "
        f"AND multiSearchAnyCaseInsensitive(title, {ch.sql_arr(phrases)}) "
        f"ORDER BY cited_by_count DESC LIMIT {limit * 3}", timeout=280) or []
    out, seen = [], set()
    for t, y, v, doi, url, cites, orient in rows:
        k = re.sub(r"[^a-z0-9]+", "", (t or "").lower())[:80]
        if k in seen:
            continue
        seen.add(k)
        out.append({"title": t, "year": int(y), "venue": v or None, "cited_by": int(cites or 0),
                    "orientation": orient or None,
                    "url": f"https://doi.org/{doi}" if doi else (url or None)})
    return out[:limit]


def _framing_shift(qo: dict, since: int) -> dict:
    """Has the recent literature's framing moved against the older literature?

    Same orientation labels, two windows, compared as shares. A rise in the
    cautionary and critical share is the measurable version of "your statement
    may conflict with newer evidence"."""
    where = query.predicate(qo, "research_typed")
    try:
        rows = ch.chq_rows(
            f"SELECT if(publication_year >= {since}, 'recent', 'earlier') w, "
            f"orientation, count() c FROM {ch.TABLE['research_typed']} WHERE "
            f"publication_year BETWEEN {ch.TYPED_FIRST_YEAR} AND "
            f"{ch.RESEARCH_LAST_YEAR} AND {where} GROUP BY w, orientation", timeout=280)
    except Exception as e:
        return {"available": False, "reason": f"{type(e).__name__}: {e}"}
    win = {"recent": {}, "earlier": {}}
    for w, o, c in rows:
        win[w][o] = int(c)
    out = {}
    for w, d in win.items():
        tot = sum(d.values())
        if not tot:
            continue
        neg = sum(n for o, n in d.items()
                  if evidence.ORIENTATION_SIDE.get(o) in ("qualifying", "contradicting"))
        out[w] = {"papers": tot, "cautionary_pct": round(100 * neg / tot, 1)}
    if len(out) < 2 or min(v["papers"] for v in out.values()) < 30:
        return {"available": False,
                "reason": "not enough papers in one of the windows to compare framing"}
    delta = out["recent"]["cautionary_pct"] - out["earlier"]["cautionary_pct"]
    return {"available": True, "windows": out, "delta_pct_points": round(delta, 1),
            "reading": ("recent work is markedly more cautious than earlier work"
                        if delta >= 8 else
                        "recent work is markedly more positive than earlier work"
                        if delta <= -8 else "framing is broadly unchanged"),
            "caveat": "orientation labels the paper's own framing, not the truth"}


# ═══════════════════════════ table research ══════════════════════════════════
def research_table(rows: list, question: str, limit_rows: int = 25) -> dict:
    """Research one column across many rows — the spreadsheet case.

    Each row is answered independently and honestly: a row the corpus cannot
    answer comes back null with a reason, never with a plausible fill. That is
    the whole point of doing this in a research layer rather than in a language
    model — a spreadsheet of invented numbers is indistinguishable from a
    spreadsheet of real ones once it is pasted somewhere else."""
    rows = [str(r).strip() for r in (rows or []) if str(r).strip()][:limit_rows]
    if not rows:
        return {"available": False, "reason": "no rows given"}
    out = []

    def work(entity):
        def run():
            claim = f"{entity}: {question}"
            qo = query.build(claim, depth="quick")
            if not qo.get("available"):
                return {"row": entity, "value": None, "available": False,
                        "reason": qo.get("reason")}
            docs = evidence.fetch_docs(qo, limit=8)
            # A row must be PRESENT in its own sources. Without this check the
            # research lane answers "Tesla" and "BYD" with the same generic
            # battery paper — a column of identical rows that each look sourced.
            tok = [w for w in re.split(r"[^A-Za-z0-9]+", entity) if len(w) > 2]
            # EVERY distinctive word of the row, not any: with `any`, the row
            # 'lithium iron phosphate' matched every lithium paper and took its
            # figure (609.4, unitless) from a solid-state catholyte study.
            on_row = [d for d in docs if all(
                w.lower() in ((d.get("title") or "") + " " + (d.get("abstract") or "")
                              ).lower() for w in tok)] if tok else docs
            if on_row:
                # The row must be in the source AND the source must be about the
                # QUESTION. Measured on "immune checkpoint inhibitor response rate":
                # melanoma's figure came from a colitis-toxicity meta-analysis and
                # NSCLC's from a proton-pump-inhibitor interaction study — each named
                # the row, neither measured a response rate.
                qkw = _question_keywords(question)
                def about_q(text):
                    t = (text or "").lower()
                    return not qkw or any(k in t for k in qkw)
                on_q = [d for d in on_row if about_q((d.get("title") or "") + " " + (d.get("abstract") or ""))]
                if not on_q:
                    top = on_row[0]
                    return {"row": entity, "available": True, "corpus": "research", "value": None,
                            "measures": None, "papers": 0,
                            "top_source": {"title": top["title"], "year": top.get("year"),
                                           "tier": top["tier"], "url": top.get("url")},
                            "reason": f"{len(on_row)} papers name this row but none addresses "
                                      f"'{question}' in its abstract"}
                st = stats.find_statistics(qo, on_q, limit=4)
                fit = [x for x in (st.get("stats") or [])
                       if about_q((x.get("measures") or "") + " " + (x.get("sentence") or ""))]
                top = ((fit[0].get("source") or {}) if fit else {}) or on_q[0]
                return {"row": entity, "available": True, "corpus": "research",
                        "value": fit[0].get("value") if fit else None,
                        "measures": fit[0].get("measures") if fit else None,
                        "population": fit[0].get("population") if fit else None,
                        "sentence": fit[0].get("sentence") if fit else None,
                        "papers": len(on_q),
                        "top_source": {"title": top.get("title"), "year": top.get("year"),
                                       "tier": top.get("tier"), "url": top.get("url")},
                        "reason": None if fit else
                        "papers on this row address the question but none states a matching figure in its abstract"}
            return _news_row(entity, question, docs)
        return run

    got = ch.parallel([work(r) for r in rows], workers=4)
    for r, g in zip(rows, got):
        out.append(g or {"row": r, "value": None, "available": False,
                         "reason": "lookup failed"})
    answered = sum(1 for o in out if o.get("value"))
    return {"available": True, "question": question, "rows": out,
            "answered": answered, "of": len(out),
            "note": ("a null value means the corpus does not state one — it is "
                     "not a zero and it is not an invitation to guess")}


_Q_STOP = {"research", "studies", "study", "effect", "effects", "impact", "about", "which", "what", "percent",
           "rates", "rate", "ratio", "level", "levels", "change", "climate", "between", "among", "their", "these",
           "those", "percent", "percentage", "number", "amount", "value", "values"}


def _question_keywords(question: str) -> list:
    """Distinctive word stems of the column's question ('respons', 'density',
    'yield'), used to check that a source and a figure are about it."""
    words = [w for w in re.findall(r"[a-z][a-z0-9]{3,}", (question or "").lower()) if w not in _Q_STOP]
    if not words:
        return []
    # The MEASURE is the last distinctive word ("...response rate" -> response,
    # "...energy density Wh/kg" -> density, "...crop yield percent" -> yield).
    # The words before it name the subject, which every candidate paper already
    # matches, so they cannot tell an on-question source from an off-question one.
    w = words[-1]
    return [w[:7] if len(w) > 8 else w]


def _news_row(entity: str, question: str, research_docs: list) -> dict:
    """The research corpus does not name every company, and for a row like
    "Tesla" the news corpus is where the record actually is.

    Figures are extracted from article text through the same two gates as
    everywhere else — the value must appear in its own sentence and the
    sentence in the article — but the tier is `news`, the bottom of the ladder.
    A number from here is a REPORTED figure, not a measured one, and every row
    that comes back this way says so."""
    words = [w for w in re.split(r"[^A-Za-z0-9]+", question) if len(w) > 3][:4]
    try:
        rows = ch.chq_rows(
            f"SELECT toString(toDate(datetime)), substring(assumeNotNull(text),1,1600) "
            f"FROM {ch.TABLE['news']} WHERE datetime >= '2023-01-01' AND datetime < "
            f"'{ch.NEWS_LAST_MONTH}' AND {ch.prose_match('assumeNotNull(text)', [entity])} "
            f"AND {ch.prose_match('assumeNotNull(text)', words) if words else '1'} "
            f"ORDER BY datetime DESC LIMIT 6", timeout=200)
    except Exception:
        rows = []
    if not rows:
        return {"row": entity, "value": None, "available": False, "corpus": None,
                "reason": ("neither the research corpus nor the news corpus has "
                           "anything naming this row alongside the question"),
                "research_docs_off_row": len(research_docs)}
    docs = [{"id": f"news:{i}", "title": f"{entity} coverage, {r[0]}", "year":
             int(r[0][:4]), "abstract": r[1], "tier": "news", "strength": "very_low",
             "venue": "news", "url": None, "source": "news"}
            for i, r in enumerate(rows)]
    st = stats.find_statistics({"claim": f"{entity}: {question}"}, docs, limit=2)
    top = (st.get("stats") or [{}])[0] if st.get("available") else {}
    return {"row": entity, "available": True, "corpus": "news",
            "value": top.get("value"), "measures": top.get("measures"),
            "articles": len(rows),
            "top_source": {"date": rows[0][0], "tier": "news", "strength": "very_low",
                           "excerpt": (top.get("sentence") or rows[0][1])[:240]},
            "reason": ("answered from news coverage, not research — a figure here "
                       "is what an article reported, not what a study measured")
            if top.get("value") else
            ("news names this row but no article states a figure the question asks "
             "for")}


# ═══════════════════════════ library gaps ════════════════════════════════════
def library_gaps(items: list, subject: str | None = None, limit: int = 12) -> dict:
    """What a reference library is missing, measured against the corpus.

    Resolve the library to real works, take the topics those works actually
    carry, then find the most-cited and most-recent papers under those topics
    that the library does not hold. The 'themes' are the corpus's labels, so
    this works on any collection without configuration."""
    items = [str(i).strip() for i in (items or []) if str(i).strip()][:200]
    if not items:
        return {"available": False, "reason": "empty library"}
    dois = [i.lower().replace("https://doi.org/", "") for i in items
            if re.match(r"^(https?://doi\.org/)?10\.\d{4,9}/", i, re.I)]
    titles = [i for i in items if i.lower().replace("https://doi.org/", "") not in dois]
    have, topics = [], {}
    if dois:
        try:
            for r in ch.chq_rows(
                    f"SELECT openalex_id, title, publication_year, topics, "
                    f"cited_by_count FROM {ch.TABLE['research']} WHERE lower(doi) IN "
                    f"{ch.sql_arr(dois[:80])} LIMIT 120", timeout=280):
                have.append({"id": r[0], "title": r[1], "year": int(r[2] or 0) or None})
                for t in evidence._arr(r[3]):
                    topics[t] = topics.get(t, 0) + 1
        except Exception:
            pass
    if titles:
        try:
            for r in ch.chq_rows(
                    f"SELECT openalex_id, title, publication_year, topics FROM "
                    f"{ch.TABLE['research']} WHERE publication_year BETWEEN 1990 AND "
                    f"{ch.RESEARCH_LAST_YEAR} AND "
                    f"{ch.prose_match('title', [t[:70] for t in titles[:12]])} "
                    f"LIMIT 200", timeout=280):
                have.append({"id": r[0], "title": r[1], "year": int(r[2] or 0) or None})
                for t in evidence._arr(r[3]):
                    topics[t] = topics.get(t, 0) + 1
        except Exception:
            pass
    if not topics:
        if not subject:
            return {"available": False,
                    "reason": ("none of these items resolved to a work in the "
                               "corpus — pass DOIs, or name the subject")}
        qo = query.build(subject, depth="quick")
        topics = {t["topic"]: t["papers"] for t in query.topics(qo, limit=8)}
    top_topics = [t for t, _ in sorted(topics.items(), key=lambda kv: -kv[1])[:6]]
    have_ids = {h["id"] for h in have}
    have_titles = {re.sub(r"[^a-z0-9]+", "", (h["title"] or "").lower())[:70]
                   for h in have}
    pred = (f"arrayExists(x -> x IN {ch.sql_arr(top_topics)}, topics)")
    missing, emerging = [], []
    try:
        for r in ch.chq_rows(
                f"SELECT openalex_id, title, publication_year, venue_name, doi, "
                f"cited_by_count FROM {ch.TABLE['research']} WHERE publication_year "
                f"BETWEEN 2015 AND {ch.RESEARCH_LAST_YEAR} AND {pred} "
                f"ORDER BY cited_by_count DESC LIMIT {limit * 3}", timeout=280):
            key = re.sub(r"[^a-z0-9]+", "", (r[1] or "").lower())[:70]
            if r[0] in have_ids or key in have_titles:
                continue
            missing.append({"title": r[1], "year": int(r[2] or 0) or None,
                            "venue": r[3], "doi": r[4] or None,
                            "cited_by": int(r[5] or 0),
                            "url": f"https://doi.org/{r[4]}" if r[4] else None})
    except Exception as e:
        return {"available": False, "reason": f"{type(e).__name__}: {e}"}
    try:
        for r in ch.chq_rows(
                f"SELECT title, publication_year, doi, cited_by_count FROM "
                f"{ch.TABLE['research']} WHERE publication_year BETWEEN "
                f"{ch.RESEARCH_LAST_YEAR - 1} AND {ch.RESEARCH_LAST_YEAR} AND {pred} "
                f"ORDER BY cited_by_count DESC LIMIT {limit}", timeout=280):
            key = re.sub(r"[^a-z0-9]+", "", (r[0] or "").lower())[:70]
            if key in have_titles:
                continue
            emerging.append({"title": r[0], "year": int(r[1] or 0) or None,
                             "doi": r[2] or None, "cited_by": int(r[3] or 0)})
    except Exception:
        pass
    return {"available": True, "resolved": len(have), "of_items": len(items),
            "themes": [{"topic": t, "in_library": topics[t]} for t in top_topics],
            "highly_cited_missing": missing[:limit],
            "recent_missing": emerging[:limit],
            "how": ("themes are the OpenAlex topics your resolved items carry; "
                    "'missing' is ranked by citations within those topics and "
                    "excludes anything already resolved from your list"),
            "coverage": ch.coverage_of(["research"])}


# ═══════════════════════════ comparing two claims ════════════════════════════
def compare_claims(a: str, b: str, read: bool = True) -> dict:
    """Two claims, the same measurements, side by side — and no winner declared
    unless the numbers declare one."""
    qa, qb = [query.build(x, depth="full") for x in (a, b)]
    profs = ch.parallel([
        lambda: evidence.profile(qa, read=read, limit=14) if qa.get("available") else
        {"available": False, "reason": qa.get("reason")},
        lambda: evidence.profile(qb, read=read, limit=14) if qb.get("available") else
        {"available": False, "reason": qb.get("reason")},
    ], workers=2)
    pa, pb = profs[0] or {}, profs[1] or {}

    def side(q, p):
        t = (p.get("tally") or {}).get("counts") or {}
        mix = p.get("corpus_stance") or {}
        return {"claim": q.get("claim"), "available": p.get("available", False),
                "lane": q.get("lane"), "lane_note": q.get("lane_note"),
                "papers_both_poles": (q.get("lane_counts") or {}).get("intersection"),
                "papers_subject": (q.get("lane_counts") or {}).get("subject"),
                "documents_read": t, "corpus_mix": mix.get("sides"),
                "contested_pct": mix.get("contested_pct"),
                "top_tier": max([d.get("tier_rank", 0)
                                 for d in (p.get("documents") or [])] or [0]),
                "strongest_source": next(
                    (({"title": d["title"], "tier": d["tier"], "year": d.get("year"),
                       "url": d.get("url"), "stance": d.get("stance")})
                     for d in (p.get("documents") or [])), None)}
    A, B = side(qa, pa), side(qb, pb)
    verdict = "not comparable"
    if A["available"] and B["available"]:
        sa = (A["documents_read"].get("supports", 0), A["papers_both_poles"] or
              A["papers_subject"] or 0, A["top_tier"])
        sb = (B["documents_read"].get("supports", 0), B["papers_both_poles"] or
              B["papers_subject"] or 0, B["top_tier"])
        verdict = ("the first claim has more evidence behind it" if sa > sb else
                   "the second claim has more evidence behind it" if sb > sa else
                   "the two are backed about equally")
    return {"available": A["available"] or B["available"], "a": A, "b": B,
            "verdict": verdict,
            "caveat": ("more evidence is not the same as more true — a heavily "
                       "studied claim can be heavily contested, which is what the "
                       "contested share is for")}
