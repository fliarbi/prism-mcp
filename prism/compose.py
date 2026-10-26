#!/usr/bin/env python3
"""compose — writing with the corpus open: continuations, sections, articles.

The other modules answer questions about a claim. This one produces prose a
person will paste into a draft, so it does two things they do not.

IT READS BOTH CORPORA. Research says what is KNOWN; news says what is
HAPPENING. A paragraph about India's manufacturing policy that cites only 2019
papers is missing the last eighteen months entirely, and a paragraph built only
from news has no idea what is settled. Every context block here carries both,
plus the trend series, and every rendered paragraph names which corpus each
sentence came from.

IT RANKS BY EVIDENCE STRENGTH, NOT BY TOPIC INTEREST. A section is only worth
suggesting if the corpus can actually carry it. `section_candidates` scores each
one — papers, study-design tier, how contested, news volume, recency — and the
score decides both the order and whether the section is offered at all. A
section the corpus cannot support is returned as `blocked` with the reason,
never quietly written from nothing.

Everything composed here passes `writer.ground()`: numbers checked against the
supplied material, invented honorifics stripped, gendered pronouns for named
researchers flagged. A paragraph that fails comes back marked, not deleted —
how often the writer reaches is information the caller should have.
"""
from __future__ import annotations

import json
import re
import time

from . import (articles, browse, cache, ch, charts, cite, emphasis, evidence,
               llm, news, query, rotate, stats, writer)
from . import progress
from . import workflows

TTL = 21600
CTX_DOCS = 14          # abstracts handed to the writer per paragraph
SECTION_DOCS = 10
MAX_SECTIONS = 8


def _log(m):
    import sys
    print(f"[prism.compose] {m}", flush=True, file=sys.stderr)


def _usable_context(ctx):
    """A verified quotation can still be unrelated to the requested claim."""
    ctx = dict(ctx)
    research = dict(ctx.get('research') or {})
    research['documents'] = [d for d in research.get('documents', [])
                             if d.get('grounded') and d.get('quote') and
                             d.get('stance') in ('supports', 'contradicts', 'qualifies')]
    ctx['research'] = research
    n = ctx.get('news') or {}
    if not research['documents'] and not (n.get('recent') or n.get('critical')):
        ctx['available'] = False
        ctx['reason'] = ctx.get('reason') or 'No relevant source supports composition on this subject.'
    return ctx


# ═══════════════════════════ research + news context ═════════════════════════
def context(topic: str, claim: str | None = None, limit: int = CTX_DOCS,
            with_news: bool = True, with_trends: bool = True,
            with_analytics: bool = False) -> dict:
    # Sidebar sections and the subsequent write use one evidence bundle.
    # Keep the full 14-document bundle; never truncate away contrary evidence.
    return _usable_context(_context(topic.strip(), claim, max(CTX_DOCS, limit), with_news, with_trends, with_analytics))


@cache.singleflight
def _context(topic: str, claim: str | None = None, limit: int = CTX_DOCS,
             with_news: bool = True, with_trends: bool = True,
             with_analytics: bool = False) -> dict:
    """Everything a writer needs on one subject, from both corpora at once.

    The research half is read (stance-labelled, quotes verified) so the writer
    can attribute a finding rather than gesture at a literature. The news half
    is the last months, which no research corpus has yet: OpenAlex's usable
    window ends in 2025 and the news corpus runs to within weeks."""
    ck = cache.key("compose.context.v4", topic.lower(), (claim or "").lower(),
                   limit, with_news, with_trends, with_analytics, llm.MODEL, llm.EFFORT)
    hit = cache.get(ck)
    if hit:
        progress.emit('cached')
        return {**hit, "cached": True}

    # A claim-scoped query is more precise and more likely to resolve to
    # nothing. Falling back to the topic is not a nicety: without it a
    # continuation request returns an empty evidence block, and the writer —
    # correctly — refuses to write, which reads to a caller as the tool being
    # broken rather than the query being too narrow.
    scoped_query = f'Topic: {topic}. Claim: {claim}' if claim else topic
    qo = query.build(scoped_query, depth="quick")
    scoped = bool(claim)
    if not qo.get("available") and claim:
        qo = query.build(topic, depth="quick")
        scoped = False
    if not qo.get("available"):
        return {"available": False, "reason": qo.get("reason"), "topic": topic,
                "research": {}, "news": {}}

    jobs = [('docs', lambda: evidence.fetch_docs(qo, limit=limit))]
    if with_analytics:
        jobs.append(('mix', lambda: evidence.corpus_stance(qo)))
    if with_trends:
        jobs.append(('series', lambda: stats.series(qo, 'research_typed')))
    if with_analytics:
        jobs.append(('browse', lambda: browse.browse(topic, sort='cited', limit=8)))
    # News is matched on the whole phrase, and a scoped topic never carries the
    # whole phrase as a tag. Measured live: "waterlogging in delhi" returns 0
    # articles through the central lane while "waterlogging" returns 13,184.
    # So the news lane gets the SUBJECT and the scope is applied afterwards as
    # a filter on what came back — which is also the honest way round, since a
    # tag never says the article was about Delhi.
    def news_bundle():
        # Resolve news terms alongside research retrieval, not in front of it.
        term, scope = _news_term(topic)
        tasks = [('recent', lambda: news.recent_news(term, limit=30)),
                 ('critical', lambda: news.critical_news(term, limit=30))]
        if with_trends:
            tasks.append(('trend', lambda: news.trends(term, 'quarterly')))
        if with_analytics:
            tasks += [('themes', lambda: news.themes(term, limit=8)),
                      ('tone', lambda: news.sentiment(term, 'quarterly'))]
        return {'term':term, 'scope':scope, **dict(zip(
            [k for k,_ in tasks], ch.parallel([fn for _,fn in tasks], workers=5)))}
    if with_news:
        jobs.append(('news', news_bundle))
    res = dict(zip([k for k,_ in jobs], ch.parallel([fn for _,fn in jobs], workers=5)))
    docs, mix, brow, ser = res.get('docs') or [], res.get('mix') or {}, res.get('browse') or {}, res.get('series') or {}
    nr = res.get('news') or {}
    news_term, scope = nr.get('term', topic), nr.get('scope', '')
    recent, critical, themes = nr.get('recent'), nr.get('critical'), nr.get('themes')
    ntrend, ntone = nr.get('trend'), nr.get('tone')

    read = evidence.stance(qo, docs) if docs else []
    read = workflows.source_fit(qo['claim'], docs, read) if read else []
    grounded = [d for d in read if d.get("grounded") and
                d.get('stance') in ('supports', 'contradicts', 'qualifies')]

    rec_all = (recent or {}).get("articles") if (recent or {}).get("available") else []
    crit_all = (critical or {}).get("articles") if (critical or {}).get("available") else []
    rec_rows, crit_rows, scope_hit = _apply_scope(rec_all, crit_all, news_term, scope)
    out = {
        "available": bool(grounded or rec_rows or crit_rows),
        "analytics_deferred": not with_analytics,
        "topic": topic, "claim": claim if scoped else None,
        "claim_scoped": scoped,
        "claim_note": (None if scoped or not claim else
                       "the claim did not resolve against the corpus, so the "
                       "context below is about the topic as a whole"),
        "query": {"poles": qo.get("poles"), "lane": qo.get("lane"),
                  "lane_note": qo.get("lane_note"), "domain": qo.get("domain")},
        "research": {
            "documents": grounded,
            "read_tally": evidence.tally(read) if read else None,
            "stance_mix": {k: mix.get(k) for k in
                           ("papers", "sides", "contested_pct", "reading", "window")},
            "facets": (brow.get("facets") or {}) if brow.get("available") else None,
            "series": ser if ser.get("available") else None,
        },
        "news": {
            "term": news_term, "scope": scope, "scope_matched": scope_hit,
            "scope_note": (None if not scope else
                           (f"news searched for '{news_term}' and narrowed to "
                            f"articles that also name '{scope}'") if scope_hit else
                           (f"NOT SCOPED: no article in the corpus covers "
                            f"'{news_term}' in '{scope}'. The articles below are "
                            f"about '{news_term}' ELSEWHERE and must not be "
                            f"written about as if they happened in '{scope}'")),
            "recent": rec_rows,
            "critical": crit_rows,
            "themes": [r["label"] for r in
                       ((themes or {}).get("categories") or {}).get("rows", [])][:6],
            "trend": (ntrend or {}).get("trend"),
            "tone": {k: (ntone or {}).get(k) for k in
                     ("totals", "corpus_baseline_ratio", "reading")}
            if (ntone or {}).get("available") else None,
            "window": (recent or {}).get("window") if recent else None,
        } if with_news else None,
        "coverage": ch.coverage_of(["research_typed", "research"] +
                                   (["news"] if with_news else [])),
    }
    if not out["coverage"]["partial"]:
        cache.put(ck, out, TTL)
    return out


_NEWS_TERM_TTL = 43200
SCOPE_FLOOR = 3         # scoped articles below which the corpus is asked directly


def _news_term(topic: str) -> tuple:
    """(term the news lane should search, scope to filter by afterwards).

    Feeds match on the whole phrase and a scoped topic rarely carries the whole
    phrase as a tag. Measured live: "waterlogging in delhi" returns 0 articles
    through the feed lane while "waterlogging" returns 13,184.
    `browse.split_scope` will not split a one-word subject — deliberately, so
    it does not maul "increase in temperature" — so the split is decided HERE
    by measurement instead of by grammar: try the whole phrase, and only fall
    back to the head when the whole phrase finds nothing."""
    topic = (topic or "").strip()
    ck = cache.key("compose.news_term.v1", topic.lower())
    hit = cache.get(ck)
    if hit:
        return hit["term"], hit["scope"]

    def has_rows(t):
        """Ask the FEED lane, not the mention lane.

        `resolve_term` counts anything that mentions the term — 27 articles for
        "waterlogging in delhi". The feeds run the stricter central lane (the
        term must be one of the article's own tags) and return zero for the same
        string. Testing the loose lane and then reading from the strict one is
        how this produced an empty news panel while reporting the term as fine."""
        try:
            r = news.recent_news(t, limit=3)
            return bool(r.get("available") and (r.get("articles") or []))
        except Exception:
            return False

    term, scope = topic, None
    if not has_rows(topic) and re.search(r"\s+in\s+", topic, re.I):
        head, tail = re.split(r"\s+in\s+", topic, maxsplit=1, flags=re.I)
        head, tail = head.strip(), tail.strip()
        if head and has_rows(head):
            term, scope = head, tail
    cache.put(ck, {"term": term, "scope": scope}, _NEWS_TERM_TTL)
    return term, scope


def _names(row: dict, scope: str) -> bool:
    s = scope.strip().lower()
    return s in ((row.get("title") or "") + " " + (row.get("excerpt") or "") + " "
                 + " ".join(row.get("tags") or []) + " "
                 + str(row.get("country") or "")).lower()


def _scope_rank(rows: list, scope: str) -> list:
    """Scope in the HEADLINE first, then anywhere else.

    A national round-up that mentions Delhi in passing matches the same
    predicate as a story about Delhi, and ranked by priority alone the
    round-ups win — a Delhi feed came back led by Chennai and Kolkata. Whether
    the place is in the title is the cheapest signal that the story is about
    it."""
    s = scope.strip().lower()
    return sorted(rows or [], key=lambda r: (
        0 if s in (r.get("title") or "").lower() else 1,
        -(r.get("priority") or 0)))


def _scope_search(term: str, scope: str, limit: int = 10) -> list:
    """Articles naming BOTH the subject and the scope — a search, not a filter.

    Filtering a feed cannot find what the feed did not return: a "waterlogging"
    feed ranked by priority came back full of Guwahati and Bengaluru and none of
    it named Delhi, so the filter fell through to unfiltered rows and a Delhi
    article would have been written from Assam floods. This asks the corpus the
    actual question instead."""
    where = [f"datetime >= addMonths(toDate('{ch.NEWS_LAST_MONTH}'), -30)",
             f"datetime < '{ch.NEWS_LAST_MONTH}'",
             news.term_predicate(term, "mention"),
             news.term_predicate(scope, "mention")]
    try:
        rows = ch.chq_rows(
            f"SELECT {news._FEED_COLS} FROM {ch.TABLE['news']} "
            f"WHERE {' AND '.join(where)} "
            f"ORDER BY {news.TOP_PRIORITY} DESC, datetime DESC LIMIT {limit}",
            timeout=280)
    except Exception:
        return []
    sig = {r[0]: {"datetime": r[1], "priority": int(r[2] or 0), "polarity": r[3],
                  "tone": r[4], "tags": news._arr(r[5]),
                  "categories": news._arr(r[6]), "country": r[7] or None}
           for r in rows}
    return [a for a in articles.resolve([r[0] for r in rows], sig) if a.get("url")]


def _apply_scope(recent_rows: list, critical_rows: list, term: str,
                 scope: str | None) -> tuple:
    """(recent, critical, scope_matched). Filter first, search if that is empty,
    and if BOTH come up dry say so rather than quietly serving the wrong place."""
    if not scope:
        return (recent_rows or [])[:8], (critical_rows or [])[:6], None
    rec = [r for r in (recent_rows or []) if _names(r, scope)]
    crit = [r for r in (critical_rows or []) if _names(r, scope)]
    # A floor, not a zero-check. Filtering a "waterlogging" feed for Delhi left
    # ONE article while the corpus holds 3,488 that name both — the feed simply
    # had not returned them. Anything under SCOPE_FLOOR is treated as "the
    # filter found nothing useful" and the corpus is asked directly.
    if len(rec) + len(crit) < SCOPE_FLOOR:
        found = _scope_search(term, scope, limit=14)
        if found:
            seen = {a.get("target_id") for a in rec + crit}
            fresh = [a for a in found if a.get("target_id") not in seen]
            crit = _scope_rank(
                crit + [a for a in fresh if (a.get("priority") or 0) >= 7], scope)[:6]
            ids = {a.get("target_id") for a in crit}
            rec = _scope_rank(
                rec + [a for a in fresh if a.get("target_id") not in ids], scope)[:8]
            return rec, crit, True
        # Nothing anywhere. Return the unscoped rows so the writer still has a
        # record to work from, but flagged — see `scope_note`.
        return (recent_rows or [])[:6], (critical_rows or [])[:4], False
    return _scope_rank(rec, scope)[:8], _scope_rank(crit, scope)[:6], True


def _news_block(ctx: dict, limit: int = 6) -> str:
    """News handed to the writer as dated, attributed lines — never as facts to
    paraphrase freely. A headline is a claim by a publisher, and the prose has
    to say so."""
    n = ctx.get("news") or {}
    rows = []
    if n.get("scope") and n.get("scope_matched") is False:
        rows.append(f"[WARNING] {n.get('scope_note')}")
    for a in (n.get("critical") or [])[:limit]:
        rows.append(f"[N] {a.get('published') or a.get('datetime')} · "
                    f"{a.get('publisher')} · PRIORITY {a.get('priority')} · "
                    f"{a.get('polarity')} · {a.get('title') or a.get('excerpt')}")
    for a in (n.get("recent") or [])[:limit]:
        rows.append(f"[N] {a.get('published') or a.get('datetime')} · "
                    f"{a.get('publisher')} · {a.get('title') or a.get('excerpt')}")
    if n.get("trend"):
        t = n["trend"]
        # State the direction and the endpoints as SEPARATE facts. Written as
        # "coverage falling, 771 → 1,032 per quarter" the writer produced
        # "coverage has fallen, declining from 771 to 1,032" — which passed the
        # number check, because both numbers were real, while saying the
        # opposite of what they show. Direction is computed on thirds and can
        # legitimately disagree with the endpoints; the prose must not merge them.
        rows.append(
            f"[TREND] news coverage per quarter went from {t.get('first')} in "
            f"{t.get('from')} to {t.get('last')} in {t.get('to')}. Over the whole "
            f"window the direction is {t.get('direction')} (computed by comparing "
            f"the first third of the period with the last, NOT the two endpoints "
            f"— do not describe the endpoints as a rise or fall).")
    if (n.get("tone") or {}).get("totals"):
        tone = n["tone"]
        rows.append(f"[TONE] negative:positive {tone['totals'].get('ratio')} "
                    f"against a corpus baseline of "
                    f"{tone.get('corpus_baseline_ratio')} — {tone.get('reading')}")
    return "\n".join(rows)


def _research_block(ctx: dict) -> str:
    r = ctx.get("research") or {}
    block = writer.pack_sources(r.get("documents") or [])
    mix = r.get("stance_mix") or {}
    if not ctx.get('analytics_deferred', True) and mix.get("papers"):
        block += (f"\n\n[CORPUS] {mix['papers']:,} typed papers match this subject "
                  f"({mix.get('window')}). Contested share "
                  f"{mix.get('contested_pct')}% — {mix.get('reading')}")
    ser = r.get("series")
    if ser and ser.get("trend"):
        t = ser["trend"]
        block += (f"\n[RESEARCH TREND] {t.get('first')} papers in {t.get('from')} → "
                  f"{t.get('last')} in {t.get('to')}, {t.get('direction')}")
    return block


def _sources_for_grounding(ctx: dict) -> list:
    out = [_research_block(ctx), _news_block(ctx)]
    for d in (ctx.get("research") or {}).get("documents") or []:
        out.append(d.get("quote") or "")
        out.append(d.get("abstract") or "")
    return [x for x in out if x]


# ═══════════════════════════ continue a paragraph ════════════════════════════
_CONT_SYS = (
 "You continue somebody else's article using ONLY the research and news "
 "supplied. You are a research writer, not a stylist: your value is that every "
 "sentence you add can be traced.\n\n" + writer.HOUSE_RULES + "\n\n"
 "OUTPUT — plain text, no markdown headings, no preamble:\n"
 "Write the paragraph that comes NEXT in the draft. One paragraph, 60-120 "
 "words. Open by attributing a specific finding using an ATTRIBUTION string "
 "exactly as supplied, then say what it found and what it means for the "
 "argument the draft is making. If a [N] news line is more recent than the "
 "research and bears on the point, use it and say which outlet reported it "
 "and when.\n"
 "Then a line containing only ---\n"
 "Then 3 DIFFERENT paragraphs that could each follow instead, same rules, each "
 "opening with a short label in square brackets naming what it does, e.g. "
 "[counter-evidence], [the numbers], [what is missing], [recent development], "
 "[mechanism], [geography]. Separate them with a line containing only ---")


@cache.remember(TTL, extra=lambda: (writer.WRITER_MODEL, llm.MODEL, llm.EFFORT))
def continue_paragraph(draft: str, topic: str = "", limit: int = CTX_DOCS,
                       with_news: bool = True) -> dict:
    """The next paragraph, plus three pre-generated alternatives.

    Every option comes back already written and already checked, because the
    point of pre-generating is that a writer picks rather than waits. Each
    carries its own grounding verdict, so an option that reached for a number
    is visibly marked rather than silently offered."""
    draft = (draft or "").strip()
    if not draft:
        return {"available": False, "reason": "no draft text given",
                "kind": "bad_request"}
    subject = (topic or "").strip()
    if not subject:
        tail = " ".join(draft.split()[-160:])
        got = llm.call_json(
            'Name the single subject this passage is about, 2-6 words. '
            'Return {"subject": str}.', tail, max_tokens=200)
        subject = str((got or {}).get("subject") or "").strip()
    if not subject:
        return {"available": False, "reason": "could not identify a subject",
                "kind": "not_resolvable"}

    last = _last_claim(draft)
    ctx = _usable_context(context(subject, claim=last, limit=limit, with_news=with_news))
    if not ctx.get("available"):
        return {"available": False, "reason": ctx.get("reason"), "subject": subject}
    docs = (ctx.get("research") or {}).get("documents") or []
    newsy = ((ctx.get("news") or {}).get("recent") or []) + \
            ((ctx.get("news") or {}).get("critical") or [])
    if not docs and not newsy:
        # Refuse here rather than hand the writer an empty evidence block. It
        # would refuse too — correctly — but a model apologising reads like a
        # broken tool, where this reads like the honest answer it is.
        return {"available": False, "subject": subject,
                "reason": ("neither corpus holds anything on this subject that "
                           "could support a paragraph"),
                "evidence_strength": _strength(ctx), "coverage": ctx.get("coverage")}

    tail = " ".join(draft.split()[-350:])
    user = (f"SUBJECT: {subject}\n\nTHE DRAFT SO FAR (continue from its end):\n"
            f"{tail}\n\nRESEARCH AVAILABLE:\n{_research_block(ctx)}\n\n"
            f"RECENT NEWS AVAILABLE:\n{_news_block(ctx) or '(none)'}")
    out = writer.compose(_CONT_SYS, user, max_tokens=3000)
    if not out.get("text"):
        return {"available": False, "reason": "the writer returned nothing",
                "subject": subject, "kind": "upstream"}

    srcs = _sources_for_grounding(ctx)
    blocks = _split_blocks(out["text"])
    if not blocks:
        return {"available": False, "reason": "unparseable composition",
                "subject": subject, "raw": out["text"][:400]}
    nxt = writer.ground(blocks[0], srcs)
    alts = []
    for b in blocks[1:4]:
        m = re.match(r"^\s*\[([^\]]{2,40})\]\s*(.*)$", b, re.S)
        label = (m.group(1).strip() if m else "alternative")
        body = (m.group(2).strip() if m else b)
        g = writer.ground(body, srcs)
        alts.append({"label": label, **g})

    return {
        "available": True, "subject": subject, "continues_claim": last,
        "next_paragraph": nxt,
        "alternatives": alts,
        "sources_used": [_src_ref(d) for d in
                         (ctx["research"].get("documents") or [])[:8]],
        "news_used": [{"title": a.get("title") or a.get("excerpt"),
                       "publisher": a.get("publisher"),
                       "published": a.get("published") or a.get("datetime"),
                       "url": a.get("url")}
                      for a in ((ctx.get("news") or {}).get("critical") or [])[:4]],
        "evidence_strength": _strength(ctx),
        "written_by": out.get("model"), "fallback": out.get("fallback"),
        "writer_note": out.get("note"),
        "lane": ctx["query"].get("lane"),
        "lane_note": ctx["query"].get("lane_note"),
        "coverage": ctx.get("coverage"),
        "how": ("attributions are rendered from the corpus's own author arrays "
                "and copied verbatim by the writer; no honorific is ever added, "
                "because an author list does not say what anyone is called"),
    }


_SEP = re.compile(r"\n\s*(?:-{3,}|\*{3,}|_{3,}|={3,})\s*\n")
_LABELLED = re.compile(r"(?=^\s*\[[^\]]{2,40}\])", re.M)


def _split_blocks(text: str) -> list:
    """Split a composition into its paragraph options.

    The separator is asked for, and about a third of the time the writer omits
    it and just labels each option instead. Splitting on the separator alone
    returned one option out of four on a live run — so fall back to splitting
    on the bracketed labels, then on blank lines."""
    parts = [b.strip() for b in _SEP.split(text or "") if b.strip()]
    if len(parts) >= 2:
        return parts
    parts = [b.strip() for b in _LABELLED.split(text or "") if b.strip()]
    if len(parts) >= 2:
        return parts
    return [b.strip() for b in re.split(r"\n\s*\n", text or "") if b.strip()]


def _heading_of(lines: list, default: str) -> tuple:
    """(heading, remaining lines).

    The prompt asks for a heading on line 1 and the writer skips it perhaps a
    third of the time, opening straight into prose. Taking line 1 regardless
    put a 90-word paragraph in the heading slot and dropped it from the body —
    so a line only counts as a heading if it LOOKS like one: short, and not a
    finished sentence."""
    if not lines:
        return default, []
    first = lines[0].strip().lstrip("#").strip()
    words = len(first.split())
    looks_like_heading = (words <= 12 and not first.endswith((".", "!", "?"))
                          and first.count(".") <= 1)
    if looks_like_heading:
        return first, lines[1:]
    return default, lines


def _src_ref(d: dict) -> dict:
    return {"attribution": writer.attribution(d), "title": d.get("title"),
            "year": d.get("year"), "venue": d.get("venue"), "tier": d.get("tier"),
            "stance": d.get("stance"), "quote": d.get("quote"),
            "url": d.get("url"), "doi": d.get("doi"),
            "citation": cite.render(d, "apa")}


def _last_claim(draft: str) -> str:
    sents = [s.strip() for s in re.split(r"(?<=[.!?])\s+", draft) if s.strip()]
    return sents[-1][:300] if sents else draft[:300]


# ═══════════════════════════ evidence strength ═══════════════════════════════
TIER_WEIGHT = {"meta_analysis": 6, "guideline": 6, "trial": 5, "observational": 4,
               "review": 4, "empirical": 3, "article": 3, "methodological": 2,
               "theoretical": 2, "preprint": 2, "case_report": 2,
               "commentary": 1, "news": 1, "patent": 1}


def _strength(ctx: dict) -> dict:
    """How well the corpus can carry writing on this — a number and a reason.

    Papers alone is the wrong measure: 20,000 papers of a whole field behind a
    specific claim is weaker than 40 papers actually about it. So the score
    combines how many documents were READ and grounded, the study-design tier
    they carry, whether recent news exists, and how contested the field is —
    and the payload always shows the parts."""
    r = ctx.get("research") or {}
    docs = r.get("documents") or []
    n = len(docs)
    tiers = [TIER_WEIGHT.get(d.get("tier"), 2) for d in docs]
    best = max(tiers) if tiers else 0
    mean = round(sum(tiers) / n, 1) if n else 0
    quoted = sum(1 for d in docs if d.get("quote"))
    nn = ctx.get("news") or {}
    news_n = len(nn.get("recent") or []) + len(nn.get("critical") or [])
    mix = r.get("stance_mix") or {}
    papers = mix.get("papers") or 0

    score = 0
    score += min(35, quoted * 5)              # documents actually read and quoted
    score += min(25, best * 4)                # the best design available
    score += min(15, int(mean * 3))           # the typical design
    score += min(15, news_n * 2)              # a current record to draw on
    score += 10 if papers >= 200 else (5 if papers >= 40 else 0)
    band = ("strong" if score >= 70 else "moderate" if score >= 45 else
            "thin" if score >= 25 else "insufficient")
    return {
        "score": score, "band": band,
        "documents_read": n, "with_verified_quote": quoted,
        "best_tier": max(docs, key=lambda d: TIER_WEIGHT.get(d.get("tier"), 0))
        .get("tier") if docs else None,
        "mean_tier_weight": mean,
        "typed_papers": papers, "contested_pct": mix.get("contested_pct"),
        "news_articles": news_n,
        "means": {"strong": "the corpus can carry a full section here",
                  "moderate": "enough for a paragraph or two, with hedging",
                  "thin": "one attributed finding at most",
                  "insufficient": "not enough to write from — do not offer this"}[band],
    }


# ═══════════════════════════ section candidates ══════════════════════════════
# The shapes an evidence-backed article section can take. Each names the LANE
# it is written from, so a section is only offered when the corpus that would
# have to carry it actually holds something. This is the list a writer would
# recognise as "the sections a researched piece has", not a template.
SECTION_KINDS = [
    {"key": "state_of_evidence", "title": "What the research actually shows",
     "needs": "research", "min_docs": 3,
     "brief": "the strongest findings, attributed, and how settled they are"},
    {"key": "counter_evidence", "title": "The case against",
     "needs": "contested", "min_docs": 2,
     "brief": "findings that contradict or qualify the article's position"},
    {"key": "numbers", "title": "The numbers",
     "needs": "figures", "min_docs": 2,
     "brief": "figures quoted verbatim from the literature, with their sources"},
    {"key": "recent", "title": "What has changed lately",
     "needs": "news", "min_docs": 3,
     "brief": "developments the research corpus has not caught up with yet"},
    # min_docs 1, not 0. At 0 a section is "available" with nothing behind it:
    # a solid-state-battery topic with zero matching news articles was still
    # offering "Where this is happening", which the writer would then have had
    # to invent. A section needs at least one real item to exist.
    {"key": "trend", "title": "How attention has moved",
     "needs": "trend", "min_docs": 1,
     "brief": "the research and news series, and what the shift means"},
    {"key": "geography", "title": "Where this is happening",
     "needs": "geo", "min_docs": 1,
     "brief": "which countries the coverage and the research are about"},
    {"key": "who", "title": "Who is working on this",
     "needs": "research", "min_docs": 4,
     "brief": "the institutions and groups the literature comes from"},
    {"key": "gaps", "title": "What nobody has answered",
     "needs": "research", "min_docs": 3,
     "brief": "the parts of the question the corpus does not cover"},
]


def section_candidates(topic: str, ctx: dict | None = None) -> dict:
    """Which sections this topic can support, ranked by what the corpus holds.

    A section is offered because the evidence for it exists, not because an
    outline says an article should have one. Each candidate carries the score
    behind it and, when it cannot be supported, the reason — so a caller can
    show a greyed-out section with "only 1 paper" rather than silently hiding
    a hole in the coverage."""
    ctx = _usable_context(ctx or context(topic, limit=CTX_DOCS))
    progress.emit('sections')
    if not ctx.get("available"):
        return {"available": False, "reason": ctx.get("reason"), "topic": topic}
    r, n = ctx.get("research") or {}, ctx.get("news") or {}
    docs = r.get("documents") or []
    mix = r.get("stance_mix") or {}
    against = [d for d in docs if d.get("stance") in ("contradicts", "qualifies")]
    figures = [d for d in docs if d.get("quote") and re.search(r"\d", d["quote"])]
    news_rows = (n.get("recent") or []) + (n.get("critical") or [])
    insts = [i for d in docs for i in (d.get("institutions") or [])]
    have = {
        "research": len(docs), "contested": len(against), "figures": len(figures),
        "news": len(news_rows), "trend": 1 if (n.get("trend") or r.get("series")) else 0,
        "geo": 1 if news_rows else 0,
    }
    # A trend section can stand on the RESEARCH series alone when the news lane
    # is empty — "attention has moved" is a claim about the literature too.
    if not have["trend"] and (r.get("series") or {}).get("available"):
        have["trend"] = 1
    base = _strength(ctx)
    out, blocked = [], []
    for k in SECTION_KINDS:
        got = have.get(k["needs"], 0)
        if k["key"] == "who":
            got = len(set(insts))
        if k["key"] == "gaps":
            got = len(docs)
        if got < k["min_docs"]:
            blocked.append({**{a: k[a] for a in ("key", "title", "brief")},
                            "available": False, "have": got,
                            "needs_at_least": k["min_docs"],
                            "reason": f"only {got} of the {k['min_docs']} "
                                      f"{k['needs']} items this section needs"})
            continue
        score = min(100, base["score"] // 2 + min(50, got * 8))
        out.append({**{a: k[a] for a in ("key", "title", "brief")},
                    "available": True, "evidence_items": got,
                    "strength_score": score,
                    "strength": ("strong" if score >= 70 else
                                 "moderate" if score >= 45 else "thin")})
    out.sort(key=lambda s: -s["strength_score"])
    return {"available": bool(out), "topic": topic,
            "sections": out[:MAX_SECTIONS], "blocked": blocked,
            "overall_strength": base,
            "contested_pct": mix.get("contested_pct"),
            "how": ("a section is offered only when the corpus that would have "
                    "to carry it holds enough; the blocked list says what was "
                    "short and by how much"),
            "coverage": ctx.get("coverage")}


_SECTION_SYS = (
 "You write ONE section of a researched article from supplied material only.\n\n"
 + writer.HOUSE_RULES + "\n\n"
 "OUTPUT — plain text:\n"
 "Line 1: the section heading, no markdown hashes.\n"
 "Then 2-4 paragraphs, 90-150 words each, separated by a blank line.\n"
 "Open the section with an attributed finding, not with a definition or a "
 "throat-clearing sentence about why the topic matters.")

_SECTION_BRIEF = {
    "state_of_evidence": "Set out the strongest findings and say how settled "
                         "they are. Name the study designs where you have them.",
    "counter_evidence": "Give the findings that contradict or qualify the "
                        "position, fairly. Do not resolve the disagreement.",
    "numbers": "Build the section around the figures in the material. Every "
               "number must be copied exactly from a quote you were given.",
    "recent": "Cover what has happened recently, from the [N] news lines. Name "
              "the outlet and the date for each. Say plainly that these are "
              "reports, not findings.",
    "trend": "Explain how attention has moved, using the [TREND] and [CORPUS] "
             "lines. Say what a rise in cautionary framing does and does not mean.",
    "geography": "Say where this is concentrated, using the news geography and "
                 "the institutions in the sources.",
    "who": "Say who is producing this research, from the institutions on the "
           "sources. Do not rank them by importance.",
    "gaps": "Say what the corpus does NOT cover — the questions the material "
            "leaves open. Do not speculate about the answers.",
}


@cache.remember(TTL, extra=lambda: (writer.WRITER_MODEL, llm.MODEL, llm.EFFORT))
def write_section(topic: str, section: str, ctx: dict | None = None,
                  angle: str = "", avoid_openers: list | None = None,
                  retries: int = 1, model: str = "") -> dict:
    """One section, fully written and checked — the "one click to add" payload.

    Returns prose ready to insert plus the sources behind it, so a caller can
    drop the section into a draft and its bibliography in one action."""
    kind = next((k for k in SECTION_KINDS if k["key"] == section), None)
    if not kind:
        return {"available": False, "kind": "bad_request",
                "reason": f"unknown section; expected one of "
                          f"{[k['key'] for k in SECTION_KINDS]}"}
    ctx = _usable_context(ctx or context(topic, limit=SECTION_DOCS))
    if not ctx.get("available"):
        return {"available": False, "reason": ctx.get("reason"), "topic": topic}
    candidates = section_candidates(topic, ctx)
    blocked = next((s for s in candidates.get('blocked', []) if s['key'] == section), None)
    if blocked:
        return {'available': False, 'kind': 'no_data', 'topic': topic,
                'reason': blocked['reason'], 'coverage': ctx.get('coverage')}
    docs = (ctx.get("research") or {}).get("documents") or []
    if section == "counter_evidence":
        docs = [d for d in docs if d.get("stance") in ("contradicts", "qualifies")]
    avoid = ""
    if avoid_openers:
        # Sections are written independently from the same source set, so left
        # alone they all open on the strongest quote — three sections of one
        # article opened with the identical Kellens sentence. Naming what has
        # been used is cheaper and more reliable than deduplicating afterwards.
        avoid = ("ALREADY USED AS AN OPENING IN THIS ARTICLE — do not open with "
                 "any of these, and do not repeat their wording:\n"
                 + "\n".join(f"  - {o[:150]}" for o in avoid_openers) + "\n\n")
    user = (f"TOPIC: {topic}\nSECTION: {kind['title']}\n"
            f"WHAT THIS SECTION DOES: {_SECTION_BRIEF.get(section, kind['brief'])}\n"
            + (f"ANGLE THE ARTICLE TAKES: {angle}\n" if angle else "") + avoid +
            f"\nRESEARCH AVAILABLE:\n{writer.pack_sources(docs)}\n\n"
            f"CORPUS AND TREND LINES:\n{_research_block(ctx)[-1200:]}\n\n"
            f"RECENT NEWS AVAILABLE:\n{_news_block(ctx) or '(none)'}")
    def _opens_repeated(txt: str) -> bool:
        """Did it open with a sentence already used to open another section?

        Asking in the prompt is not enough — told plainly not to, the writer
        opened three sections of one article with the identical Kellens
        sentence. Compared on the first twelve words, which survives light
        rephrasing."""
        if not avoid_openers or not txt:
            return False
        head = " ".join(re.sub(r"\s+", " ", txt).strip().split()[:12]).lower()
        return any(head and head[:70] in o.lower() for o in avoid_openers)

    def _body_of(txt: str) -> str:
        """The prose after the heading line. A reply that is ONLY a heading
        shipped as a successful empty section — ok:true, body "" — and the
        caller rendered "Prism returned nothing usable". Heading-only is a
        failed completion and must retry like an empty one."""
        ls = [l for l in (txt or "").split("\n") if l.strip()]
        _, bl = _heading_of(ls, kind["title"])
        return "\n".join(bl).strip()

    out = writer.compose(_SECTION_SYS, user, max_tokens=4000, model=model or None)
    for _ in range(max(0, retries)):
        if _body_of(out.get("text") or "") and not _opens_repeated(out["text"]):
            break
        if out.get("text") and not _body_of(out["text"]):
            _log(f"section '{section}' returned only a heading ({out.get('model')}) — retrying")
        elif out.get("text"):
            _log(f"section '{section}' reused an opening — retrying")
        else:
            # An empty completion is transient far more often than it is a real
            # refusal — the lead section of a live article came back empty once
            # and the piece published without it. Retry before dropping.
            _log(f"section '{section}' came back empty ({out.get('model')}) — retrying")
        out = writer.compose(_SECTION_SYS, user, max_tokens=4000, temperature=0.45, model=model or None)
    if not _body_of(out.get("text") or ""):
        return {"available": False, "kind": "upstream",
                "reason": (f"the writer ({out.get('model')}) returned "
                           f"{'only a heading' if out.get('text') else 'nothing'}, twice — "
                           "try the button again; if it repeats, the evidence for this "
                           "topic may be too thin to write from")}
    srcs = _sources_for_grounding(ctx)
    lines = out["text"].strip().split("\n")
    heading, body_lines = _heading_of(lines, kind["title"])
    body_raw = "\n\n".join(l.strip() for l in
                            re.split(r"\n\s*\n", "\n".join(body_lines)) if l.strip())
    g = writer.ground(body_raw, srcs)
    used = docs if section != "counter_evidence" else docs
    return {"available": True, "topic": topic, "section": section,
            "heading": heading, "body": g["text"],
            "paragraphs": [p for p in g["text"].split("\n\n") if p.strip()],
            "grounded": g["grounded"],
            "verification_scope": g.get('verification_scope'),
            "semantic_support_verified": False,
            "ungrounded_numbers": g["ungrounded_numbers"],
            "honorifics_removed": g["honorifics_removed"],
            "gendered_pronouns": g["gendered_pronouns"],
            "note": g.get("note") or g.get("pronoun_note"),
            "sources": [_src_ref(d) for d in used[:10]],
            "bibliography": cite.bibliography(used[:10], "apa"),
            "news_used": [{"title": a.get("title") or a.get("excerpt"),
                           "publisher": a.get("publisher"),
                           "published": a.get("published") or a.get("datetime"),
                           "url": a.get("url")}
                          for a in ((ctx.get("news") or {}).get("critical") or [])[:5]],
            "evidence_strength": _strength(ctx),
            "written_by": out.get("model"), "fallback": out.get("fallback"),
            "writer_note": out.get("note"),
            "coverage": ctx.get("coverage")}


# ═══════════════════════════ titles ══════════════════════════════════════════
_TITLE_SYS = (
 "You propose titles for a researched article, from the evidence supplied.\n"
 "Return JSON: {\"titles\": [{\"title\": str, \"angle\": str, \"rests_on\": str}]}\n"
 "* 5 titles. Each must be answerable FROM THE MATERIAL GIVEN — not a title "
 "you would like to be true.\n"
 "* `angle` — one line on what the article would argue.\n"
 "* `rests_on` — which supplied finding or trend the title depends on. Quote "
 "the attribution string.\n"
 "* No number in a title unless it appears in the material.\n"
 "* No colons-plus-subtitle formula on every one; vary the shape.")


@cache.remember(TTL, extra=lambda: (writer.WRITER_MODEL, llm.MODEL, llm.EFFORT))
def suggest_titles(topic: str, ctx: dict | None = None) -> dict:
    """Titles the corpus can actually deliver on, each with its evidence.

    A title is a promise about what the article will show. Generating them
    from the retrieved evidence rather than from the topic means the promise
    is one the sources can keep."""
    ctx = _usable_context(ctx or context(topic, limit=CTX_DOCS))
    if not ctx.get("available"):
        return {"available": False, "reason": ctx.get("reason"), "topic": topic}
    user = (f"TOPIC: {topic}\n\nRESEARCH AVAILABLE:\n{_research_block(ctx)}\n\n"
            f"RECENT NEWS:\n{_news_block(ctx) or '(none)'}")
    out = llm.call_json(_TITLE_SYS, user, max_tokens=1500)
    srcs = _sources_for_grounding(ctx)
    titles = []
    for t in ((out or {}).get("titles") or [])[:6]:
        title = str(t.get("title") or "").strip()
        if not title:
            continue
        clean, hon = writer.strip_honorifics(title)
        bad = llm.ungrounded_numbers(' '.join((clean, str(t.get('angle') or ''),
                                             str(t.get('rests_on') or ''))), srcs)
        titles.append({"title": clean, "angle": str(t.get("angle") or "")[:200],
                       "rests_on": str(t.get("rests_on") or "")[:200],
                       "grounded": False,
                       "numeric_check_passed": not bad,
                       "verification_scope": "Numbers checked; title promises require editorial review.",
                       "ungrounded_numbers": bad,
                       "honorifics_removed": hon})
    return {"available": bool(titles), "topic": topic, "titles": titles,
            "evidence_strength": _strength(ctx),
            "reason": None if titles else "the title step returned nothing usable",
            "coverage": ctx.get("coverage")}


# ═══════════════════════════ whole article ══════════════════════════════════
def write_article(title: str = "", topic: str = "", sections: list | None = None,
                  angle: str = "", max_sections: int = 5, progress=None,
                  requester: str = "", salt: str = "", emphasise: bool = True,
                  model: str = "") -> dict:
    """A complete researched article: title, sections, bibliography.

    Sections are chosen by what the corpus can carry — `section_candidates`
    ranks them and the strongest `max_sections` are written — so the shape of
    the article follows the evidence rather than a template. Each section is
    written and grounded independently; one that fails its check is kept and
    flagged rather than dropped, because an article silently missing its
    counter-evidence section is worse than one that says the check failed.

    `progress` is called with (done, total, label) so a background job can
    report where it is."""
    topic = (topic or title or "").strip()
    if not topic:
        return {"available": False, "kind": "bad_request",
                "reason": "give a title or a topic"}
    t0 = time.time()
    ctx = _usable_context(context(topic, limit=CTX_DOCS))
    if not ctx.get("available"):
        return {"available": False, "reason": ctx.get("reason"), "topic": topic}

    # ROUTE FIRST. A topic with a strong general literature and no local
    # literature is a NEWS story, and writing it from papers produces an
    # article about the general subject wearing a local title — which is
    # exactly what happened to "waterlogging in delhi" before this existed.
    r = route(topic, ctx)
    if r.get("mode") == "news" and not sections:
        out = news_article(topic, title=title, max_sections=max_sections,
                           progress=progress, requester=requester, salt=salt,
                           emphasise=emphasise, model=model)
        out["route"] = r
        return out
    if r.get("mode") == "thin":
        return {"available": False, "topic": topic, "route": r,
                "reason": ("neither the research corpus nor the news corpus can "
                           "support an article on this")}

    cand = section_candidates(topic, ctx)
    chosen = sections or [s["key"] for s in (cand.get("sections") or [])][:max_sections]
    if not chosen:
        return {"available": False, "topic": topic,
                "reason": "the corpus cannot support any section on this topic",
                "blocked": cand.get("blocked"),
                "evidence_strength": cand.get("overall_strength")}

    if not title:
        tt = suggest_titles(topic, ctx)
        good = [t for t in (tt.get("titles") or []) if t["grounded"]]
        title = (good or tt.get("titles") or [{}])[0].get("title") or topic.title()
        title_source = "suggested from the evidence"
    else:
        title_source = "given"

    # Written in EVIDENCE order (strongest first, which is what the caller
    # chose) but assembled in READING order: what is known, then what is
    # contested, then the numbers, then what changed, then who and what is
    # missing. An article that opens on "What has changed lately" because that
    # section scored highest reads like notes, not a piece.
    order = {k: i for i, k in enumerate(
        ["state_of_evidence", "counter_evidence", "numbers", "trend", "recent",
         "geography", "who", "gaps"])}
    written, openers = [], []
    for i, key in enumerate(chosen, 1):
        if progress:
            progress(i - 1, len(chosen), key)
        sec = write_section(topic, key, ctx=ctx, angle=angle,
                            avoid_openers=openers, model=model)
        if sec.get("available"):
            first = (sec.get("paragraphs") or [""])[0]
            if first:
                openers.append(first[:180])
            written.append(sec)
        else:
            written.append({"section": key, "available": False,
                            "reason": sec.get("reason")})
    written.sort(key=lambda s: order.get(s.get("section"), 99))
    if progress:
        progress(len(chosen), len(chosen), "done")

    ok = [s for s in written if s.get("available")]
    all_docs, seen = [], set()
    for s in ok:
        for d in s.get("sources") or []:
            k = d.get("doi") or d.get("title")
            if k and k not in seen:
                seen.add(k)
                all_docs.append(d)
    body = "\n\n".join(f"## {s['heading']}\n\n{s['body']}" for s in ok)
    words = len(body.split())
    return {
        "available": bool(ok), "title": title, "title_source": title_source,
        "topic": topic, "angle": angle or None,
        "markdown": f"# {title}\n\n{body}",
        "sections": written,
        "section_plan": cand.get("sections"),
        "sections_not_possible": cand.get("blocked"),
        "words": words,
        "bibliography": [d.get("citation") for d in all_docs],
        "sources": all_docs,
        "evidence_strength": cand.get("overall_strength"),
        "grounding": {"sections_written": len(ok),
                      "sections_flagged": sum(1 for s in ok if not s.get("grounded")),
                      "ungrounded_numbers": [n for s in ok
                                             for n in (s.get("ungrounded_numbers") or [])],
                      "honorifics_removed": sum(s.get("honorifics_removed") or 0
                                                for s in ok)},
        "written_by": (ok[0].get("written_by") if ok else None),
        "fallback": any(s.get("fallback") for s in ok),
        "seconds": round(time.time() - t0, 1),
        "coverage": ctx.get("coverage"),
        "how": ("sections are chosen by what the corpus can carry, written "
                "independently, and each checked against its own sources"),
    }


# ═══════════════════════════ is the research even on-subject? ════════════════
def locality(ctx: dict, scope: str) -> dict:
    """Do the retrieved papers actually mention the place the topic is about?

    This is the check whose absence produced a "waterlogging in Delhi" article
    written entirely from global flood-risk reviews. The strength score said
    "strong" because ten papers were read and quoted; not one of them was about
    Delhi. Volume of on-SUBJECT literature says nothing about whether any of it
    is on-PLACE, and for a local story the second is what matters."""
    docs = (ctx.get("research") or {}).get("documents") or []
    if not scope or not docs:
        return {"checked": False}
    s = scope.strip().lower()
    hits = [d for d in docs
            if s in ((d.get("title") or "") + " " + (d.get("abstract") or "") + " "
                     + " ".join(d.get("institutions") or []) + " "
                     + " ".join(d.get("topics") or [])).lower()]
    pct = round(100 * len(hits) / len(docs), 1)
    return {"checked": True, "scope": scope, "documents": len(docs),
            "mentioning_scope": len(hits), "pct": pct,
            "on_place": bool(hits),
            "reading": (f"{len(hits)} of {len(docs)} retrieved papers mention "
                        f"{scope}" if hits else
                        f"NONE of the {len(docs)} retrieved papers mention {scope} "
                        f"— the research corpus has no local literature here, so a "
                        f"research-led article would be about the general subject "
                        f"wearing a local title")}


def route(topic: str, ctx: dict | None = None) -> dict:
    """Decide whether this topic is a research story or a news story.

    Three outcomes, and the middle one is the interesting case:
      research  — a real literature exists and it is on-place.
      news      — the literature is absent or off-place, but the news corpus
                  has the events, the season and the trend. Write from news.
      thin      — neither. Say so; do not write.
    """
    ctx = ctx or context(topic, limit=CTX_DOCS)
    if not ctx.get("available"):
        return {"available": False, "reason": ctx.get("reason"), "topic": topic}
    scope = (ctx.get("news") or {}).get("scope") or browse.split_scope(topic)["scope"]
    loc = locality(ctx, scope) if scope else {"checked": False}
    strength = _strength(ctx)
    nn = ctx.get("news") or {}
    news_items = len(nn.get("recent") or []) + len(nn.get("critical") or [])
    research_usable = (strength["with_verified_quote"] >= 3
                       and (not loc.get("checked") or loc.get("on_place")))
    if research_usable:
        mode = "research"
    elif news_items >= 3:
        mode = "news"
    else:
        mode = "thin"
    return {"available": True, "topic": topic, "mode": mode, "scope": scope,
            "locality": loc, "research_strength": strength,
            "news_items": news_items,
            "why": {
                "research": "the literature exists and is about this place",
                "news": ("the research corpus has nothing on-place, but the news "
                         "corpus has the events, the season and the trend — so "
                         "the article is built from the record, not the literature"),
                "thin": "neither corpus can support an article on this",
            }[mode]}


# ═══════════════════════════ news-led report ═════════════════════════════════
def news_context(topic: str, months: int = 60) -> dict:
    """Every news card a report on this subject needs, in one pass.

    Season, trend, events, what is growing inside the coverage, who is named,
    where, tone, publishers. This is the news equivalent of `context()` and is
    what a local story is written from when no local literature exists."""
    term, scope = _news_term(topic)
    ck = cache.key("compose.news_context.v1", topic.lower(), months)
    hit = cache.get(ck)
    if hit:
        return {**hit, "cached": True}
    # EVERY card takes the scope. Passing it to some and not others is how a
    # Delhi report ended up naming Mumbai's BMC and Karnataka's chief minister:
    # the feeds were scoped, the entity and publisher panels were not.
    res = ch.parallel([
        lambda: news.seasonality(term, scope=scope),
        lambda: news.trends(term, "quarterly", scope=scope),
        lambda: news.events(term, limit=12, scope=scope),
        lambda: news.keyword_growth(term, "subcats", scope=scope),
        lambda: news.keyword_growth(term, "tags", scope=scope, min_recent=25),
        lambda: news.sentiment(term, "quarterly", scope=scope),
        lambda: news.entities(term, "all", limit=10, scope=scope),
        lambda: news.sources(term, limit=10, scope=scope),
        lambda: news.themes(term, limit=10, scope=scope),
    ], workers=9)
    keys = ["season", "trend", "events", "growth_subcats", "growth_tags",
            "tone", "entities", "sources", "themes"]
    out = {k: (v or {"available": False}) for k, v in zip(keys, res)}
    out.update({"available": any(v.get("available") for v in out.values()),
                "topic": topic, "term": term, "scope": scope,
                "coverage": ch.coverage_of(["news"])})
    if not out["coverage"]["partial"]:
        cache.put(ck, out, TTL)
    return out


_FACTOR_SYS = (
 "You extract the CAUSES and the IMPACTS named in news article openings.\n"
 "Return JSON: {\"causes\": [{\"factor\": str, \"quote\": str, \"doc_id\": str}], "
 "\"impacts\": [{\"factor\": str, \"quote\": str, \"doc_id\": str}]}\n"
 "* `factor` — at most 8 words, the thing itself: 'blocked storm drains', "
 "'Yamuna crossing the danger mark', 'flight delays'.\n"
 "* `quote` — the sentence it came from, copied VERBATIM from the article "
 "opening you were given. It is checked; an unfindable quote is discarded.\n"
 "* Only what the text states. Do not add a cause you believe is true.\n"
 "* A cause makes the thing happen. An impact is what it does to people.\n"
 "* At most 8 of each, most frequently named first.")


def factors(topic: str, nctx: dict | None = None, limit: int = 60) -> dict:
    """Causes and impacts, extracted from what the coverage actually says.

    The news `text` column is the article's opening ~320 characters, which is
    where a report states what happened and why. Every extracted factor keeps
    the sentence it came from and is verified against it, so "blocked drains"
    is traceable to an outlet and a date rather than to general knowledge."""
    nctx = nctx or news_context(topic)
    term, scope = nctx.get("term"), nctx.get("scope")
    where = [f"datetime >= addMonths(toDate('{ch.NEWS_LAST_MONTH}'), -48)",
             f"datetime < '{ch.NEWS_LAST_MONTH}'",
             news.term_predicate(term, "mention"),
             f"{news.TOP_PRIORITY} >= 6"]
    if scope:
        where.append(news.term_predicate(scope, "mention"))
    try:
        rows = ch.chq_rows(
            f"SELECT target_id, toString(toDate(datetime)), "
            f"substringUTF8(assumeNotNull(text), 1, 420) FROM {ch.TABLE['news']} "
            f"WHERE {' AND '.join(where)} ORDER BY {news.TOP_PRIORITY} DESC, "
            f"datetime DESC LIMIT {limit}", timeout=280)
    except Exception as e:
        return {"available": False, "reason": f"{type(e).__name__}: {e}"}
    if not rows:
        return {"available": False, "reason": "no coverage to extract from"}
    by_id = {r[0]: {"date": r[1], "text": r[2]} for r in rows}
    packed = "\n\n".join(f"[{r[0]}] ({r[1]}) {r[2]}" for r in rows)
    out = llm.call_json(_FACTOR_SYS, f"SUBJECT: {topic}\n\nARTICLE OPENINGS:\n{packed}",
                        max_tokens=9000)
    if not out:
        return {"available": False, "reason": "the extraction step returned nothing"}

    def keep(items):
        good, dropped = [], []
        for it in (items or [])[:10]:
            did = str(it.get("doc_id") or "").strip()
            src = by_id.get(did)
            q = str(it.get("quote") or "").strip()
            f = str(it.get("factor") or "").strip()[:80]
            if not (src and q and f):
                dropped.append({"factor": f, "why": "no source named"})
                continue
            if not llm.verify_quote(q, src["text"]):
                dropped.append({"factor": f, "why": "quote not found in that article"})
                continue
            good.append({"factor": f, "quote": q, "date": src["date"],
                         "target_id": did})
        return good, dropped

    causes, c_drop = keep(out.get("causes"))
    impacts, i_drop = keep(out.get("impacts"))
    ids = [x["target_id"] for x in causes + impacts]
    # resolve() also returns per-node error rows, which carry no target_id.
    recs = {a["target_id"]: a for a in (articles.resolve(ids) if ids else [])
            if a.get("target_id")}
    for x in causes + impacts:
        a = recs.get(x["target_id"]) or {}
        x["publisher"] = a.get("publisher")
        x["url"] = a.get("url")
        x["headline"] = a.get("title")
    return {"available": bool(causes or impacts), "topic": topic,
            "causes": causes, "impacts": impacts,
            "rejected": c_drop + i_drop,
            "read_articles": len(rows),
            "how": ("extracted from the opening of each high-priority report and "
                    "verified against it; a factor whose quote could not be found "
                    "is discarded, not shown"),
            "coverage": ch.coverage_of(["news"])}


# ═══════════════════════════ the news-led article ════════════════════════════
# The MATERIAL a section can be built from. Not an outline — an inventory. What
# an article is actually made of is decided per topic by `plan_story`, because
# a fixed six-section template produces the same shaped piece about every
# subject, which is what a reader recognises as machine-written.
SECTION_LANES = {
    "season": "the month-by-month rhythm: when this happens and how sharply",
    "events": "specific dated incidents, how many newsrooms covered each",
    "causes": "what the reporting says makes it happen, quoted",
    "impacts": "what it does to people, quoted",
    "shift": "how the story's composition has changed over time",
    "actors": "the institutions and people the coverage names",
    "tone": "how the coverage reads against ordinary news",
    "places": "where inside the region it concentrates",
}

_PLAN_SYS = (
 "You plan a magazine-quality news feature from the evidence a reporter has "
 "gathered. You are choosing the SHAPE of one specific article, not filling in "
 "a template.\n"
 'Return JSON: {"angle": str, "lede": str, "sections": [{"heading": str, '
 '"lanes": [str], "thrust": str}]}\n'
 "* `angle` — one sentence: what THIS piece argues that a generic piece would "
 "not. Draw it from the evidence, not from general knowledge.\n"
 "* `lede` — one sentence naming the concrete scene or moment the article "
 "should open on. Pick the single most human thing in the material: a named "
 "day, a named place, a named consequence. Never a statistic.\n"
 "* 4-6 sections. `heading` is a real headline, 3-8 words, specific to this "
 "subject — never 'Introduction', 'Overview', 'Analysis' or 'Conclusion'.\n"
 "* `lanes` — which material each section draws on, from the list given. A "
 "section may combine two.\n"
 "* `thrust` — one sentence on what that section has to establish.\n"
 "* Order them so the piece READS: open on the concrete, explain the "
 "mechanism, widen to the pattern, close on what is unresolved. Do not put the "
 "statistics section first.\n"
 "* Choose lanes by what the evidence can carry. Leaving a lane out is a "
 "decision, not an omission.")


def plan_story(topic: str, nctx: dict, fx: dict, rot: dict | None = None) -> dict:
    """Decide what THIS article is, before writing a word of it.

    Without this step every topic produced the same six sections in the same
    order, opening on a seasonality statistic — the shape a reader recognises
    as generated. The planner sees a compressed inventory of what was actually
    found and chooses an angle, an opening scene and a structure from it, so
    two topics with different evidence come out as different articles."""
    s = nctx.get("season") or {}
    ev = (nctx.get("events") or {}).get("events") or []
    gs = (nctx.get("growth_subcats") or {}).get("rising") or []
    ent = ((nctx.get("entities") or {}).get("organizations") or {}).get("rows") or []
    tone = nctx.get("tone") or {}
    inventory = {
        "topic": topic,
        "available_lanes": {k: v for k, v in SECTION_LANES.items()
                            if _lane_has(k, nctx, fx)},
        "season": ({"reading": s.get("reading"), "peak": s["peak"]["name"],
                    "peak_articles": s["peak"]["articles"],
                    "trough": s["trough"]["name"],
                    "ratio": s.get("peak_to_trough")} if s.get("available") else None),
        "biggest_events": [{"date": e.get("date"),
                            "outlets": e.get("reports_that_day"),
                            "headline": e.get("title") or e.get("excerpt")}
                           for e in ev[:8]],
        "causes": [c["factor"] for c in (fx.get("causes") or [])],
        "impacts": [c["factor"] for c in (fx.get("impacts") or [])],
        "fastest_growing_themes": [{"theme": g["label"], "growth": g["growth_x"]}
                                   for g in gs[:6]],
        "most_named": [{"name": e["label"], "articles": e["articles"]}
                       for e in ent[:6]],
        "tone": tone.get("reading"),
    }
    inv_text = json.dumps(inventory, default=str)[:9000]
    if rot:
        inv_text = rotate.brief(rot) + "\n\nEVIDENCE INVENTORY:\n" + inv_text
    out = llm.call_json(_PLAN_SYS, inv_text, max_tokens=2000, temperature=0.6)
    # The lede is prose about real people and places, so it is gated like prose.
    lede = str((out or {}).get("lede") or "").strip()
    lede_bad = writer.unsourced_names(lede, [inv_text])
    if lede_bad:
        _log(f"plan lede named {lede_bad} — not in the evidence; dropping detail")
        lede = ""
    secs = []
    for sec in ((out or {}).get("sections") or [])[:6]:
        lanes = [l for l in (sec.get("lanes") or [])
                 if l in SECTION_LANES and _lane_has(l, nctx, fx)]
        head = str(sec.get("heading") or "").strip()
        if lanes and head:
            secs.append({"heading": head[:80], "lanes": lanes,
                         "thrust": str(sec.get("thrust") or "")[:220]})
    if not secs:
        # The planner is the only step here with no cheap fallback, so it gets
        # one: whatever lanes exist, in reading order.
        order = ["events", "causes", "impacts", "season", "shift", "actors"]
        secs = [{"heading": SECTION_LANES[k].split(":")[0].capitalize(),
                 "lanes": [k], "thrust": SECTION_LANES[k]}
                for k in order if _lane_has(k, nctx, fx)][:5]
    if rot:
        secs = rotate.reorder(secs, rot)
    return {"available": bool(secs), "angle": str((out or {}).get("angle") or "")[:300],
            "lede": lede[:300], "rotation": rot,
            "lede_rejected": bool(lede_bad),
            "lede_rejected_names": lede_bad,
            "sections": secs, "planned_by": llm.MODEL,
            "inventory_lanes": list(inventory["available_lanes"])}


def _lane_has(lane: str, nctx: dict, fx: dict) -> bool:
    g1 = (nctx.get("growth_subcats") or {}).get("rising") or []
    g2 = (nctx.get("growth_tags") or {}).get("rising") or []
    return {
        "season": bool((nctx.get("season") or {}).get("available")),
        "events": bool((nctx.get("events") or {}).get("events")),
        "causes": bool(fx.get("causes")),
        "impacts": bool(fx.get("impacts")),
        "shift": bool(g1 or g2),
        "actors": bool(((nctx.get("entities") or {}).get("organizations") or {})
                       .get("rows")),
        "tone": bool((nctx.get("tone") or {}).get("available")),
        "places": bool(((nctx.get("entities") or {}).get("places") or {}).get("rows")),
    }.get(lane, False)


_NEWS_ART_SYS = (
 "You are a features writer at a serious newspaper. You write ONE section of a "
 "reported piece, from evidence a researcher has handed you. There is no "
 "academic literature on this subject in this place, so everything rests on "
 "dated reporting.\n\n" + writer.HOUSE_RULES + "\n\n"
 "WRITE PROSE, NOT A READOUT. This is the difference between the piece being "
 "publishable and being a spreadsheet with sentences around it:\n"
 "* Lead every paragraph with something that HAPPENED or something that IS "
 "TRUE, then support it with a figure. Never lead with the figure. 'The "
 "Yamuna crossed 206 metres on 10 July 2023 and the evacuations began' — not "
 "'115 outlets covered the Yamuna reaching 206 metres'.\n"
 "* AT MOST TWO numbers per paragraph. A third is one too many; cut it. You "
 "are choosing which figures earn their place, not listing what you were "
 "given.\n"
 "* Never write a coverage count as if it were the news. How many outlets ran "
 "a story is evidence of how big the story was — say 'the story ran "
 "everywhere' or 'nearly two hundred outlets carried it', and only when the "
 "scale itself is the point.\n"
 "* Vary sentence length. A short one lands after three long ones.\n"
 "* No sentence may begin with a bare statistic, a percentage or a domain name.\n\n"
 "CITE LIKE A NEWSPAPER:\n"
 "* Use the PUBLICATION name given, never the domain: 'The Indian Express "
 "reported on 10 April 2026 that…', never 'indianexpress.com (2026-04-10) "
 "report that…'.\n"
 "* Write dates as '10 April 2026'.\n"
 "* DO NOT USE QUOTATION MARKS around anything from the material. The corpus "
 "stores article text LOWERCASED and truncated, so what you were given is not "
 "the publication's exact wording — presenting it as a direct quote "
 "misrepresents how the outlet actually wrote it. Paraphrase in your own "
 "sentence and attribute: 'The Times of India reported heavy rain across Delhi "
 "on 30 September 2025', never: The Times of India reported that \"heavy rains "
 "lash delhi\".\n"
 "* A headline is not a sentence. Never paste one into your prose in its "
 "original title case; say what it reported.\n"
 "* A headline is a claim by a publisher. Attribute it; never assert it "
 "yourself.\n\n"
 "THE MATERIAL IS TAGGED FOR YOU, NOT FOR THE READER. Lines begin with markers "
 "— [SEASON], [MONTH], [EVENT], [CAUSE], [IMPACT], [RISING], [TREND], [TONE], "
 "[ORGANIZATION], [PUBLISHER] — and are written as key=value fields. NEVER "
 "write a marker or a field into the prose, in any form: not after a dash, not "
 "in brackets, not in parentheses. Lines marked [... NOTE] are instructions to "
 "you and must never appear in the article.\n"
 "* Coverage counts measure ATTENTION, not severity. More articles about "
 "flight delays does not make flight delays the worst harm.\n"
 "* NEVER attribute one of this analysis's own measurements to a publication. "
 "Article counts, growth multiples, month shares, tone ratios and naming "
 "frequencies are OUR figures. Write 'a review of the coverage shows…' or "
 "state them plainly — never 'The Hindustan Times reported that Rahul Gandhi "
 "featured in thirty-eight pieces'.\n"
 "* Never give anyone a job title. You know a name appeared in the coverage; "
 "you do not know what office they hold, and calling someone the mayor when "
 "they are not is a factual error about a real person.\n"
 "* Never write a death toll, a rainfall figure or a cost that is not in the "
 "material.\n\n"
 "OUTPUT — plain text:\n"
 "Line 1: the section heading you were given, unchanged.\n"
 "Then EXACTLY 2 to 4 paragraphs of 90-150 words each, separated by a BLANK "
 "LINE. A single unbroken block is not acceptable — a reader needs the breaks "
 "to follow the argument.")


_MONTHS_LONG = ["January", "February", "March", "April", "May", "June", "July",
                "August", "September", "October", "November", "December"]


def _pretty_date(d) -> str:
    """2023-07-10 -> 10 July 2023. Handed to the writer already formatted, so a
    newspaper date is the path of least resistance rather than a rule it has to
    remember."""
    try:
        y, m, day = str(d)[:10].split("-")
        return f"{int(day)} {_MONTHS_LONG[int(m) - 1]} {y}"
    except Exception:
        return str(d)


# Lines that are OUR measurement of the coverage, not anything a newsroom
# published. Handed over unlabelled, the writer attributed them to whichever
# masthead was nearest: "The Indian Express reported that rainfall statistics
# appeared in 516 articles" — the Indian Express reported no such thing. This
# banner is repeated at the top of every block that contains them.
_METRIC_BANNER = (
    "[HOW TO ATTRIBUTE THE LINES BELOW] Lines marked [SEASON], [MONTH], "
    "[TREND], [RISING], [FADING], [TONE], [ORGANIZATION], [PERSON] and "
    "[PUBLISHER] are THIS ANALYSIS's own measurements of the news coverage. NO "
    "OUTLET PUBLISHED THEM. Never write 'The Times of India reported that X "
    "appeared in 516 articles'. Attribute them to the analysis itself — 'a "
    "review of five years of coverage shows…', 'across the corpus…' — or state "
    "them without attribution. Only [EVENT], [CAUSE] and [IMPACT] lines carry a "
    "publication, and only those may be attributed to one.")


def _news_material(nctx: dict, fx: dict, want: str) -> str:
    """The block a news section is written from — only the cards it needs."""
    L = []
    if want in ("season", "growth", "entities"):
        L.append(_METRIC_BANNER)
    s, t = nctx.get("season") or {}, nctx.get("trend") or {}
    if want == "season" and s.get("available"):
        L.append(f"[SEASON] {s['reading']}. Peak {s['peak']['name']} "
                 f"{s['peak']['articles']} articles; trough {s['trough']['name']} "
                 f"{s['trough']['articles']}; peak-to-trough ratio "
                 f"{s['peak_to_trough']}x. Top three months: "
                 f"{', '.join(s['top_three_months'])} = {s['concentration_pct']}% "
                 f"of all coverage. Window {s.get('from')} to {s.get('to')}.")
        L += [f"[MONTH] {m['name']}: {m['articles']} articles "
              f"({m['share_pct']}%), {m['critical']} high-priority"
              for m in (s.get("months") or [])]
    if want == "events":
        evs = sorted((nctx.get("events") or {}).get("events", [])[:14],
                     key=lambda e: e.get("date") or "")
        for e in evs:
            L.append(f"[EVENT] date={_pretty_date(e.get('date'))} | "
                     f"publication={articles.masthead(e.get('publisher'))} | "
                     f"outlets_that_day={e.get('reports_that_day')} | "
                     f"what={e.get('title') or e.get('excerpt')}")
    if want == "factors":
        for tag, key in (("CAUSE", "causes"), ("IMPACT", "impacts")):
            rows = sorted(fx.get(key) or [],
                          key=lambda c: -articles.authority(c.get("publisher")))
            for c in rows:
                L.append(f"[{tag}] factor={c['factor']} | "
                         f"publication={articles.masthead(c.get('publisher'))} | "
                         f"date={_pretty_date(c['date'])} | "
                         f"reported=\"{c['quote']}\"")
    if want == "growth":
        for key in ("growth_subcats", "growth_tags"):
            g = nctx.get(key) or {}
            for r in (g.get("rising") or [])[:8]:
                L.append(f"[RISING {g.get('labelled_by')}] theme={r['label']} | "
                         f"earlier={r['earlier']} | recent={r['recent']} | "
                         f"growth={r['growth_x']}x")
            for r in (g.get("fading") or [])[:4]:
                L.append(f"[FADING {g.get('labelled_by')}] theme={r['label']} | "
                         f"earlier={r['earlier']} | recent={r['recent']} | "
                         f"change={r['growth_x']}x")
        if t.get("available"):
            tr = t.get("trend") or {}
            # Data on the data line; the caution on its own line. Written as one
            # sentence the writer copied the caution — instruction text and all —
            # straight into the published paragraph.
            L.append(f"[TREND] first_quarter={tr.get('first')} | "
                     f"first_period={tr.get('from')} | last_quarter={tr.get('last')} | "
                     f"last_period={tr.get('to')} | direction={tr.get('direction')}")
            L.append("[TREND NOTE] direction compares the first third of the "
                     "window with the last third, not the two endpoints. Do not "
                     "call the endpoints a rise or a fall.")
    if want == "entities":
        ent = nctx.get("entities") or {}
        for grp in ("organizations", "people"):
            for r in ((ent.get(grp) or {}).get("rows") or [])[:8]:
                L.append(f"[{grp[:-1].upper()}] name={r['label']} | "
                         f"articles={r['articles']}")
        src = nctx.get("sources") or {}
        for p in (src.get("publishers") or [])[:5]:
            L.append(f"[PUBLISHER] host={p['publisher']} | "
                     f"share_of_sample={p['share_pct']}%")
    tone = nctx.get("tone") or {}
    if tone.get("available"):
        tt = tone.get("totals") or {}
        L.append(f"[TONE] negative_to_positive={tt.get('ratio')} | "
                 f"corpus_baseline={tone.get('corpus_baseline_ratio')} | "
                 f"reading={tone.get('reading')}")
    return "\n".join(L)


_MARKER = re.compile(
    r"\[(?:SEASON|MONTH|EVENT|CAUSE|IMPACT|RISING[^\]]*|FADING[^\]]*|TREND[^\]]*|"
    r"TONE|ORGANIZATION|PERSON|PUBLISHER)\]\s*", re.I)

# The writer echoes its own source lines into the prose in four shapes, all seen
# live: inside parentheses, after an em-dash, bare mid-sentence, and
# re-formatted into its own pipe-delimited table. Each pattern is anchored on
# something only a RAW FIELD contains — a `key=value`, a "named in N articles"
# tail, two or more pipes, or the instruction text from a [... NOTE] line — so
# ordinary prose with a parenthesis or a dash survives. Being too greedy here is
# worse than leaving an echo: an over-wide pattern ate a whole sentence in
# testing.
_PAREN = re.compile(r"\s*\((?:[^()]|\([^()]*\))*\)")
_ECHO_HINT = re.compile(r"named in \d|\w+=|→|of a sample|NOT the endpoints|"
                        r"first third vs last third", re.I)
_ECHO_DASH = re.compile(r"\s*[—–]\s*[a-z0-9 ().'’&/-]{2,60}:\s*"
                        r"(?:named in \d[\d,]*\s*articles|\d+(?:\.\d+)?%[^.]{0,40})",
                        re.I)
_ECHO_BARE = re.compile(r"(?:,\s*(?:with|and)\s+|\s+with\s+)?"
                        r"[a-z0-9 ().'’&/-]{2,50}:\s*named in \d[\d,]*\s*articles",
                        re.I)
_ECHO_PIPE = re.compile(r"[^.!?\n]{0,90}\|[^.!?\n]{0,50}\|[^.!?\n]{0,80}"
                        r"(?=\s*(?:\n|$))")
_KV = re.compile(r"\b(?:name|theme|host|articles|earlier|recent|growth|change|"
                 r"first_quarter|last_quarter|first_period|last_period|direction|"
                 r"share_of_sample|negative_to_positive|corpus_baseline|reading|"
                 r"date|publication|outlets_that_day|what|factor|reported)"
                 r"\s*=\s*", re.I)
_NONE_ATTR = re.compile(r"\bNone\s*\((\d{4}[-\u2011]\d{2}[-\u2011]\d{2})\)\s*"
                        r"report(?:s|ed)?\b", re.I)
_ORPHAN = re.compile(r"(?:^|(?<=\n))\s*(?:reports?|notes?|records?|indicates?|"
                     r"shows?)\s+that\s+", re.I)


def _clean_markers(text: str) -> str:
    """Remove internal source markers and echoed raw fields from the prose.

    Told plainly not to, the writer still opened a section with "[SEASON]
    reports that 65.3% of coverage falls in July" — reading the label on its own
    input as the name of a publication — and elsewhere pasted an entire
    instruction line into a published paragraph. The instruction stays in the
    prompt; this makes it true."""
    t = _PAREN.sub(lambda m: "" if _ECHO_HINT.search(m.group(0)) else m.group(0),
                   text or "")
    t = _MARKER.sub("", t)
    t = _ECHO_DASH.sub("", t)
    t = _ECHO_BARE.sub("", t)
    t = _ECHO_PIPE.sub("", t)
    t = _KV.sub("", t)
    t = _NONE_ATTR.sub(r"one outlet reported on \1", t)
    t = re.sub(r"\bNone\b(?=\s*\()", "one outlet", t)
    t = _ORPHAN.sub("", t)
    t = re.sub(r"\s+([.,;])", r"\1", t)
    t = re.sub(r"([.,;])\1+", r"\1", t)
    return re.sub(r"[ \t]{2,}", " ", t).strip()


def build_charts(topic: str, nctx: dict, fx: dict, rot: dict,
                 publish: bool = True) -> dict:
    """Render and host the charts this article's evidence can support.

    The rotation already CHOSE a shape for each card — until this existed that
    choice was computed and thrown away, and every published piece was
    text-only while the prose asked readers to hold twelve numbers in their
    head. Charts are keyed by the lane they illustrate so a section can claim
    the one that belongs to it."""
    out, specs = {}, {}
    term = nctx.get("term") or topic
    scope = nctx.get("scope")
    label = f"{scope} {term}".strip() if scope else term
    season_kind = (rot.get("charts", {}).get("season") or {}).get("key", "bars")
    specs["season"] = charts.from_season(nctx.get("season") or {}, label,
                                         kind=season_kind)
    specs["events"] = charts.from_events(
        (nctx.get("events") or {}).get("events") or [], label,
        window=(nctx.get("season") or {}).get("from", ""))
    specs["causes"] = specs["impacts"] = charts.from_factors(fx, label)
    specs["shift"] = charts.from_growth(nctx.get("growth_subcats") or {}, label)
    seen = {}
    for lane, spec in specs.items():
        if not spec:
            continue
        key = spec.get("title", "") + spec.get("kind", "")
        if key in seen:                     # causes and impacts share one ledger
            out[lane] = seen[key]
            continue
        try:
            got = charts.publish(spec, slug=f"{label}-{lane}", upload=publish)
        except Exception as e:
            out[lane] = {"available": False,
                         "reason": f"{type(e).__name__}: {e}"}
            continue
        got['available'] = bool(got.get('verified')) if publish else True
        got["lane"] = lane
        seen[key] = got
        out[lane] = got
    return out


def news_article(topic: str, title: str = "", max_sections: int = 6,
                 progress=None, temperature: float = 0.55,
                 requester: str = "", salt: str = "", emphasise: bool = True,
                 model: str = "", with_charts: bool = True) -> dict:
    """A reported feature built from the record when no local literature exists.

    Same contract as `write_article` — grounded, attributed, checked — but the
    evidence is dated reporting rather than papers, and the SHAPE is decided per
    topic by `plan_story` rather than by a template. Two topics with different
    evidence come out as different articles: different angle, different opening,
    different sections in a different order.

    Temperature is deliberately higher than the analytic tools use. Those must
    return the same answer twice; a feature that reads identically on every
    rerun is the failure this whole path is trying to avoid."""
    t0 = time.time()
    nctx = news_context(topic)
    if not nctx.get("available"):
        return {"available": False, "topic": topic,
                "reason": "the news corpus holds nothing on this subject"}
    fx = factors(topic, nctx)
    rot = rotate.plan(topic, requester=requester, salt=salt,
                      available_lanes=[k for k in SECTION_LANES
                                       if _lane_has(k, nctx, fx)])
    chart_set = build_charts(topic, nctx, fx, rot) if with_charts else {}
    plan = plan_story(topic, nctx, fx, rot)
    if not plan.get("available"):
        return {"available": False, "topic": topic,
                "reason": "no news card on this subject has enough behind it"}
    sections_plan = plan["sections"][:max_sections]

    if not title:
        title = _news_title(topic, nctx, fx, plan)

    written, openers = [], []
    for i, sec in enumerate(sections_plan, 1):
        if progress:
            progress(i - 1, len(sections_plan), sec["heading"])
        material = "\n".join(
            _news_material(nctx, fx, _LANE_WANT.get(l, l)) for l in sec["lanes"])
        avoid = ("OPENINGS ALREADY USED IN THIS ARTICLE — do not reuse the "
                 "sentence or its shape:\n"
                 + "\n".join(f"  - {o[:140]}" for o in openers) + "\n\n"
                 if openers else "")
        lede = (f"THE ARTICLE OPENS ON: {plan['lede']}\n" if i == 1 and plan.get("lede")
                else "")
        user = (f"SUBJECT: {topic}\n"
                f"{rotate.brief(rot)}\n"
                f"THE ANGLE OF THE WHOLE PIECE: {plan.get('angle')}\n"
                f"THIS SECTION'S HEADING: {sec['heading']}\n"
                f"WHAT THIS SECTION MUST ESTABLISH: {sec['thrust']}\n"
                f"{lede}\n{avoid}MATERIAL — use nothing else:\n{material}")
        out = writer.compose(_NEWS_ART_SYS, user, max_tokens=3500,
                             temperature=temperature, model=model or None)
        # A misattributed metric is a factual error about a named publication,
        # so it earns a retry that says what went wrong rather than a flag on
        # the way out.
        for _ in range(2):
            txt = out.get("text") or ""
            problems = (writer.misattributed_metrics(txt)
                        + writer.invented_titles(txt))
            # A 400-word single block is a real defect, not a style quibble:
            # two live sections came back as unbroken walls of text.
            wall = (txt and len(txt.split()) > 190
                    and len([b for b in re.split(r"\n\s*\n", txt) if b.strip()]) < 3)
            if txt and not problems and not wall:
                break
            note = ""
            if problems:
                note += ("\n\nYOUR PREVIOUS ATTEMPT FAILED A CHECK. Do not "
                         "repeat these — they credit a publication with a figure "
                         "it never published, or give someone a title:\n"
                         + "\n".join(f"  - {p}" for p in problems[:4]))
            if wall:
                note += ("\n\nYOUR PREVIOUS ATTEMPT WAS ONE UNBROKEN BLOCK. "
                         "Break it into 2-4 paragraphs separated by blank lines.")
            out = writer.compose(_NEWS_ART_SYS, user + note, max_tokens=3500,
                                 temperature=min(0.8, temperature + 0.15),
                                 model=model or None)
        if not out.get("text"):
            written.append({"section": sec["heading"], "available": False,
                            "reason": "the writer returned nothing"})
            continue
        # Keep the BLANK LINES. Filtering them out before splitting on them
        # destroyed every paragraph break the writer produced — four sections in
        # a row came back as single unbroken blocks, and the "wall of text"
        # retry kept firing on text that had been fine when it arrived.
        raw = out["text"].replace("\r\n", "\n")
        head_line, _, rest = raw.partition("\n")
        heading, _ = _heading_of([head_line.strip()], sec["heading"])
        body_src = rest if heading != sec["heading"] or head_line.strip() == heading \
            else raw
        body = "\n\n".join(
            " ".join(x.split()) for x in re.split(r"\n\s*\n", body_src) if x.strip())
        body = _clean_markers(body)
        g = writer.ground(body, [material])
        paras = [p for p in g["text"].split("\n\n") if p.strip()]
        # Emphasis runs AFTER grounding, never before. The formatter can only
        # add markup — it is verified by stripping it and comparing character
        # for character — so a paragraph that passed its fact checks cannot be
        # changed by being made scannable.
        emph = None
        if emphasise and paras:
            emph = emphasis.mark_section(paras)
            paras = emph["paragraphs"]
        if paras:
            openers.append(emphasis.strip(paras[0])[:180])
        # A section claims the chart for the first lane it draws on, and only
        # the first section to want a given chart gets it — the same image
        # repeated down a page is worse than no image.
        chart = None
        for lane in sec["lanes"]:
            c = chart_set.get(lane)
            if c and c.get("available") and not c.get("_claimed"):
                c["_claimed"] = True
                chart = {k: c[k] for k in
                         ("url", "images", "embed_html", "embed_markdown",
                          "kind", "slug", "uploaded")}
                break
        written.append({"section": heading, "lanes": sec["lanes"],
                        "available": True, "heading": heading, "chart": chart,
                        "body": "\n\n".join(paras), "paragraphs": paras,
                        "emphasis": ({k: emph[k] for k in
                                      ("marked", "rejected", "reasons")}
                                     if emph else None),
                        "grounded": g["grounded"],
                        "ungrounded_numbers": g["ungrounded_numbers"],
                        "unsourced_names": g.get("unsourced_names"),
                        "misattributed_metrics": g.get("misattributed_metrics"),
                        "invented_titles": g.get("invented_titles"),
                        "honorifics_removed": g["honorifics_removed"],
                        "stat_density": _stat_density(g["text"]),
                        "written_by": out.get("model"),
                        "fallback": out.get("fallback")})
    if progress:
        progress(len(sections_plan), len(sections_plan), "done")

    ok_secs = [x for x in written if x.get("available")]
    parts = []
    for x in ok_secs:
        parts.append(f"## {x['heading']}\n\n{x['body']}")
        if x.get("chart"):
            parts.append(x["chart"]["embed_markdown"])
    body = "\n\n".join(parts)
    cited = ([{"date": e.get("date"), "publication": articles.masthead(e.get("publisher")),
               "headline": e.get("title") or e.get("excerpt"), "url": e.get("url"),
               "outlets_that_day": e.get("reports_that_day")}
              for e in (nctx.get("events") or {}).get("events", [])[:14]]
             + [{"date": c["date"], "publication": articles.masthead(c.get("publisher")),
                 "headline": c.get("headline"), "url": c.get("url")}
                for c in (fx.get("causes") or []) + (fx.get("impacts") or [])])
    seen, sources = set(), []
    for c in sorted(cited, key=lambda x: str(x.get("date") or "")):
        k = c.get("url")
        if k and k not in seen:
            seen.add(k)
            sources.append(c)
    dens = [x["stat_density"] for x in ok_secs if x.get("stat_density") is not None]
    return {
        "available": bool(ok_secs), "mode": "news", "title": title, "topic": topic,
        "angle": plan.get("angle"), "lede": plan.get("lede"),
        "rotation": rot,
        "charts": {k: {kk: v[kk] for kk in ("url", "kind", "uploaded", "slug")}
                   for k, v in chart_set.items() if v.get("available")},
        "charts_note": ("rendered from the same measurements the prose cites and "
                        "hosted on fliarbi.com; each carries its own window and "
                        "source line so it stays checkable if it travels alone"),
        "emphasis": {"paragraphs_marked": sum((x.get("emphasis") or {}).get("marked", 0)
                                              for x in ok_secs),
                     "paragraphs_rejected": sum((x.get("emphasis") or {}).get("rejected", 0)
                                                for x in ok_secs),
                     "guarantee": ("markup only — verified by stripping it and "
                                   "comparing to the checked text character for "
                                   "character")},
        "markdown": f"# {title}\n\n{body}",
        "sections": written, "words": len(body.split()),
        "plan": plan,
        "cards_used": {"season": (nctx.get("season") or {}).get("available"),
                       "events": len((nctx.get("events") or {}).get("events") or []),
                       "causes": len(fx.get("causes") or []),
                       "impacts": len(fx.get("impacts") or []),
                       "rising_themes": len(((nctx.get("growth_subcats") or {})
                                             .get("rising") or []))},
        "season": nctx.get("season"), "events": (nctx.get("events") or {}).get("events"),
        "factors": {"causes": fx.get("causes"), "impacts": fx.get("impacts")},
        "sources": sources,
        "readability": {
            "numbers_per_100_words": round(sum(dens) / len(dens), 1) if dens else None,
            "target": "under 4 — above that the section reads as a readout",
            "worst_section": max(ok_secs, key=lambda x: x.get("stat_density") or 0)
            .get("heading") if ok_secs else None},
        "grounding": {"sections_written": len(ok_secs),
                      "sections_flagged": sum(1 for x in ok_secs
                                              if not x.get("grounded")),
                      "ungrounded_numbers": [n for x in ok_secs
                                             for n in (x.get("ungrounded_numbers") or [])],
                      "unsourced_names": sorted({n for x in ok_secs
                                                 for n in (x.get("unsourced_names") or [])}),
                      "misattributed_metrics": [m for x in ok_secs
                                                for m in (x.get("misattributed_metrics") or [])],
                      "invented_titles": sorted({t for x in ok_secs
                                                 for t in (x.get("invented_titles") or [])}),
                      "honorifics_removed": sum(x.get("honorifics_removed") or 0
                                                for x in ok_secs)},
        "written_by": ok_secs[0].get("written_by") if ok_secs else None,
        "fallback": any(x.get("fallback") for x in ok_secs),
        "seconds": round(time.time() - t0, 1),
        "why_news_led": ("written from dated reporting because the research "
                         "corpus holds no literature on this subject in this "
                         "place — see compose.route"),
        "coverage": nctx.get("coverage"),
    }


# lane -> which material block it needs
_LANE_WANT = {"season": "season", "events": "events", "causes": "factors",
              "impacts": "factors", "shift": "growth", "actors": "entities",
              "tone": "growth", "places": "entities"}

_NUMBER = re.compile(r"\b\d[\d,.]*\b")


def _stat_density(text: str) -> float:
    """Numbers per 100 words — the measurable version of "this reads like a
    spreadsheet". A section over about 4 is reciting its inputs rather than
    using them."""
    words = len((text or "").split())
    return round(100 * len(_NUMBER.findall(text or "")) / words, 1) if words else 0.0


def _news_title(topic: str, nctx: dict, fx: dict, plan: dict | None = None) -> str:
    s = nctx.get("season") or {}
    got = llm.call_json(
        'Propose one headline for a reported feature. Return {"title": str}. '
        'A real newspaper headline: concrete, at most 10 words, no colon-and-'
        'subtitle formula, no number that is not in the material, and not a '
        'label like "An Analysis of X".',
        f"SUBJECT: {topic}\n"
        f"ANGLE: {(plan or {}).get('angle')}\n"
        f"OPENS ON: {(plan or {}).get('lede')}\n"
        f"SEASON: {s.get('reading')}\n"
        f"CAUSES: {[c['factor'] for c in (fx.get('causes') or [])][:5]}\n"
        f"IMPACTS: {[c['factor'] for c in (fx.get('impacts') or [])][:5]}",
        max_tokens=300, temperature=0.6)
    t = str((got or {}).get("title") or "").strip()
    clean, _ = writer.strip_honorifics(t)
    # A "title" that is just the topic back is the fallback showing through, not
    # a headline. One retry at higher temperature before accepting it.
    if not clean or clean.lower().strip() == topic.lower().strip():
        again = llm.call_json(
            'Write one newspaper headline. Return {"title": str}. It must NOT '
            'simply restate the subject — name what happened or what is at '
            'stake. Concrete, at most 10 words, no colon-subtitle formula.',
            f"SUBJECT: {topic}\nANGLE: {(plan or {}).get('angle')}\n"
            f"OPENS ON: {(plan or {}).get('lede')}\n"
            f"CAUSES: {[c['factor'] for c in (fx.get('causes') or [])][:5]}\n"
            f"IMPACTS: {[c['factor'] for c in (fx.get('impacts') or [])][:5]}",
            max_tokens=300, temperature=0.8)
        t2 = str((again or {}).get("title") or "").strip()
        c2, _ = writer.strip_honorifics(t2)
        if c2 and c2.lower().strip() != topic.lower().strip():
            return c2
    return clean or topic.title()
