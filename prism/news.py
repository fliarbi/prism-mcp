#!/usr/bin/env python3
"""news — the general Prism features, off the 238.6M-article news corpus.

This is what a Prism report renders, as functions: what a term's coverage looks
like over time, what is being said about it right now, what is CRITICAL right
now, what themes it sits in, who and where it involves, and who is publishing
it. Same corpus and same columns the product uses; standard envelope, no plan
gate, no report credits.

Three measured facts shape every function here.

ENRICHMENT LAGS INGEST, AND THE LAG LOOKS LIKE NEWS. Geography, organisation
and person labels are written by a pipeline that runs behind the crawler.
Measured 2026-08-22: articles carrying a resolved country run at 39-53% each
month through April 2026 and then fall to 4.8% in May. Nothing happened in May
— the enrichment has not caught up. Any feature reading those columns takes its
window from `enriched_until()` and states the fill rate, because "no Indian
coverage in May" is a fact about the pipeline that reads exactly like a fact
about the world.

COLUMN FILL RATES DIFFER BY AN ORDER OF MAGNITUDE. `tags` is on 100% of
articles, `sentiments` 99.8%, `categories` 99.1%, `subcats` 59%, `keywords`
29%, `country_pri` ~43%, `org_domains` ~31%. A theme panel built on `keywords`
describes a third of the corpus; built on `tags` it describes all of it. Every
distribution here divides by the number of articles that CARRY the column, not
by the number matched, and says which it used.

THE `text` COLUMN IS A LEDE, NOT THE ARTICLE. Measured 2026-08-22: median 315
characters, 99th percentile 443. The body lives in MongoDB; ClickHouse holds the
opening. So a text match is a LEDE match — high precision, because an article
whose opening names a term is about that term, and limited recall, because a
term first named in paragraph six is invisible to it. That is why every match
here ORs the lede with `tags`, Prism's own extracted subject labels, which are
written on 100% of articles: for "electric vehicle" over Jan-Apr 2026 the lede
lane finds 16,329 articles and the tag lane 15,005, and the union is what a
volume number should mean.

ONE ARTICLE, ONE POLARITY. `sentiments` is an array of up to three graded
labels, so per-label percentages sum past 100 and cannot be subtracted into a
ratio. The highest-scoring label wins, and the resulting negative:positive
ratio only means something against the corpus baseline, which is computed
alongside it.
"""
from __future__ import annotations

import re

from . import articles, cache, ch, freshness, progress

TTL = 3600              # news moves; a research profile does not
CRITICAL_PRIORITY = 7   # measured: 9 = geopolitics and disasters, 1 = boilerplate
DEFAULT_MONTHS = 24
MAX_FEED = 50

TOP_PRIORITY = "arraySort(x -> -x.2, priorities)[1].1"
GRANULARITY = {
    "daily": "toDate(datetime)",
    "weekly": "toMonday(datetime)",
    "monthly": "toStartOfMonth(datetime)",
    "quarterly": "toStartOfQuarter(datetime)",
    "yearly": "toStartOfYear(datetime)",
}


# ═══════════════════════════ term matching ═══════════════════════════════════
MATCH_MODES = ("auto", "mention", "central", "lede", "tagged", "entity")
DIGEST_TAGS = 45        # p90 of tags-per-article is 43; a round-up carries 48-89


_SUBCAT_CACHE: dict = {}


def resolved_subcats(term: str, k: int = 3) -> list:
    """The curated news subcategories this term resolves to, by vector match.

    The news lane matched a term against its literal tag and its lede text and
    nothing else, so "waterlogging in delhi" could find no subcategory while
    `urban flooding and drainage` carried 4,484 articles. Resolved once per
    term and cached; a miss costs one embedding call."""
    key = term.strip().lower()
    if key in _SUBCAT_CACHE:
        return _SUBCAT_CACHE[key]
    try:
        from . import vocab
        got = vocab.terms_for(term, "news_subcats", k=k, min_sim=0.55)
    except Exception:
        got = []
    _SUBCAT_CACHE[key] = got
    return got


def term_predicate(term: str, mode: str = "mention", extra_terms=None) -> str:
    """Match a term against an article, at a stated level of centrality.

    The level matters more than it looks. Rank every article that MENTIONS
    "electric vehicle" by priority and the top of the feed is "Daily brief: top
    national news for school assembly" — a round-up that names an EV policy in
    one line. Technically a match. Useless as a feed.

      mention  — lede text or tag. The counting lane: what a volume chart means.
      central  — the article is ABOUT this: it carries the term as one of its
                 own tags AND either opens with it or has it resolved as an
                 entity, and it is not a round-up (a digest carries 48-89 tags
                 against a median of 18). The feed lane. Tags alone are not
                 enough on a common name: a Kyiv geopolitics piece and a
                 Nashville crash report both carry the tag "tesla", and ranked
                 by priority they take over the feed.
      lede     — the term appears in the opening ~320 characters.
      tagged   — tag only, no digest guard.
      entity   — the term is a resolved organisation, person or place on the
                 article. Substring, because those arrays hold canonical names:
                 Tesla is stored as "tesla, inc." and an equality test finds
                 nothing at all — literally zero, on 13,174 articles that name it.

    Whichever is used comes back in the payload as `match_mode`, because two
    panels built on different modes have different denominators."""
    terms = [t.strip().lower() for t in ([term] + list(extra_terms or []))
             if t and t.strip()]
    if not terms:
        return "0"
    arr = ch.sql_arr(terms)
    tagged = f"hasAny(tags, {arr})"
    lede = ch.prose_match("assumeNotNull(text)", terms)
    if mode == "tagged":
        return f"({tagged})"
    if mode == "lede":
        return f"({lede})"
    if mode == "entity":
        subs = " OR ".join(
            f"arrayExists(x -> position(x, {ch.sql_str(t)}) > 0, {col})"
            for t in terms for col in ("Organization", "Person", "Place"))
        return f"({subs})"
    if mode in ("central", "entity_central"):
        ent = " OR ".join(
            f"arrayExists(x -> position(x, {ch.sql_str(t)}) > 0, {col})"
            for t in terms for col in ("Organization", "Person", "Place"))
        # A name that is also an object needs the entity lane, not the lede.
        # "Tesla" in a lede is as often the car somebody crashed as the company:
        # ranked by priority, a murder case and a mansion shooting take the feed.
        # The entity resolver knows "tesla, inc." from a parked Tesla.
        side = ent if mode == "entity_central" else f"({lede} OR {ent})"
        return f"({tagged} AND {side} AND length(tags) <= {DIGEST_TAGS})"
    return f"({lede} OR {tagged})"


def resolve_mode(term: str, mode: str = "auto") -> str:
    """Pick the match lane from what the term turns out to BE.

    A term the corpus has resolved as an organisation, person or place is
    matched through the entity arrays; anything else through its lede. This is
    the difference between a Tesla feed about the company and a Tesla feed about
    cars people crashed."""
    if mode and mode != "auto":
        return mode if mode in MATCH_MODES else "central"
    try:
        prof = resolve_term(term)
    except Exception:
        return "central"
    if prof.get("available") and prof.get("type") in ("organization", "person", "place"):
        return "entity_central"
    return "central"


def centrality_rank(term: str) -> str:
    """How central the term is to an article, as an ORDER BY expression.

    `tags` is ordered by relevance, so the position of the term in that list is
    a usable prominence signal: first tag means the article is about it,
    twentieth means it came up. Articles that do not carry the tag at all sort
    last rather than being dropped, so a caller using a looser match mode still
    gets its most on-subject results first."""
    t = ch.sql_str((term or "").strip().lower())
    return f"if(has(tags, {t}), indexOf(tags, {t}), 999)"


def _bounds(since: str | None, until: str | None, months: int = DEFAULT_MONTHS) -> tuple:
    """A two-sided window, always. The upper bound defaults to the ingest-safe
    edge rather than to today: the newest month in the corpus holds a fraction
    of a normal month and closes every series with a cliff."""
    end = until or ch.NEWS_LAST_MONTH
    if since:
        start = since
    else:
        y, m = int(end[:4]), int(end[5:7])
        total = y * 12 + (m - 1) - months
        start = f"{total // 12:04d}-{total % 12 + 1:02d}-01"
    return start, end


def _window(start: str, end: str, granularity: str | None = None) -> dict:
    w = {"from": start, "to": end, "to_is_exclusive": True,
         "censored_at": ch.NEWS_LAST_MONTH,
         "why_censored": ("news ingest lags publication; the newest month holds "
                          "a fraction of a normal month and would close every "
                          "series with a collapse that did not happen")}
    if granularity:
        w["granularity"] = granularity
    measured = freshness.news()
    w['freshness'] = {k: measured.get(k) for k in
                      ('available', 'checked_at', 'age_seconds', 'default_until',
                       'cutoff_review_needed', 'note')}
    w['past_default_cutoff'] = end > ch.NEWS_LAST_MONTH
    return w


# ═══════════════════════════ enrichment bound ════════════════════════════════
def enriched_until(min_pct: float = 25.0) -> dict:
    """The last month whose geography and entity labels are actually written.

    Returns the bound plus the monthly fill rates behind it, so a caller can
    show why a geography panel stops earlier than a volume panel."""
    hit = cache.get(cache.key("news.enriched_until", min_pct))
    if hit:
        return {**hit, "cached": True}
    rows = ch.chq_rows(
        f"SELECT toString(toStartOfMonth(datetime)) m, count() n, "
        f"round(100*countIf(isNotNull(country_pri))/count(),1) geo, "
        f"round(100*countIf(notEmpty(Organization))/count(),1) org "
        f"FROM {ch.TABLE['news']} WHERE datetime >= addMonths(toDate('{ch.NEWS_LAST_MONTH}'), -14) "
        f"AND datetime < '{ch.NEWS_LAST_MONTH}' GROUP BY m ORDER BY m", timeout=280)
    months = [{"month": r[0], "articles": int(r[1]), "country_pct": float(r[2]),
               "organization_pct": float(r[3])} for r in rows]
    bound = ch.NEWS_LAST_MONTH
    for m in reversed(months):
        if m["country_pct"] >= min_pct:
            y, mm = int(m["month"][:4]), int(m["month"][5:7])
            t = y * 12 + mm            # exclusive bound = first day of next month
            bound = f"{t // 12:04d}-{t % 12 + 1:02d}-01"
            break
    out = {"available": True, "bound": bound, "min_pct": min_pct, "months": months,
           "note": ("geography and entity labels are written by a pipeline that "
                    "runs behind the crawler; months past this bound are ingested "
                    "but not yet labelled, and reading them as low coverage is "
                    "reading the pipeline, not the world")}
    cache.put(cache.key("news.enriched_until", min_pct), out, 21600)
    return out


# ═══════════════════════════ term resolution ═════════════════════════════════
def resolve_term(term: str, since: str | None = None, until: str | None = None) -> dict:
    """What kind of thing is this, and does Prism hold enough to report on it?

    Type comes from the corpus, not a model: an article's `Person`,
    `Organization` and `Place` arrays are resolved entity names, so whichever
    array carries the term most often is what the term is. A term nobody has
    resolved as an entity is a topic — which is a legitimate answer, not a
    failure, and most searches are topics."""
    term = (term or "").strip()
    if not term:
        return {"available": False, "reason": "no term given"}
    start, end = _bounds(since, until)
    ck = cache.key("news.resolve_term.v1", term.lower(), start, end)
    hit = cache.get(ck)
    if hit:
        return {**hit, "cached": True}
    m = term_predicate(term)
    low = ch.sql_str(term.lower())
    ent = ("arrayExists(x -> position(x, {v}) > 0, {col})")
    row = ch.chq_one(
        f"SELECT count() AS n, "
        f"countIf({ent.format(v=low, col='Person')}) AS person, "
        f"countIf({ent.format(v=low, col='Organization')}) AS org, "
        f"countIf({ent.format(v=low, col='Place')}) AS place, "
        f"countIf(hasAny(tags, {ch.sql_arr([term.lower()])})) AS tagged, "
        f"toString(min(datetime)) AS first_seen, toString(max(datetime)) AS last_seen, "
        f"countIf({TOP_PRIORITY} >= {CRITICAL_PRIORITY}) AS critical, "
        f"countIf(notEmpty(Organization) OR notEmpty(Person) OR notEmpty(Place)) AS enriched "
        f"FROM {ch.TABLE['news']} WHERE datetime >= '{start}' AND datetime < '{end}' "
        f"AND {m}", timeout=280)
    if not row or int(row[0] or 0) == 0:
        out = {"available": False,
               "reason": (f"no article between {start} and {end} mentions "
                          f"'{term}'"),
               "term": term}
        cache.put(ck, out, 900)
        return out
    n, person, org, place, tagged = (int(row[i] or 0) for i in range(5))
    enriched = int(row[8] or 0)
    kinds = {"person": person, "organization": org, "place": place}
    top = max(kinds, key=kinds.get)
    # Judge the type against the articles that CARRY entity labels, not against
    # every article that mentions the term. Entity enrichment runs behind the
    # crawler, so dividing by the full match makes every entity look like a
    # topic in any window that includes the unlabelled tail.
    kind = top if kinds[top] >= max(20, 0.02 * max(enriched, 1)) else "topic"
    out = {"available": True, "term": term, "type": kind,
           "type_evidence": {**kinds, "tagged_articles": tagged,
                             "entity_labelled_articles": enriched,
                             "how": ("the entity array that names this term most "
                                     "often, judged against the articles that "
                                     "carry entity labels at all; 'topic' when "
                                     "no array does")},
           "articles": n, "critical_articles": int(row[7] or 0),
           "first_seen": row[5], "last_seen": row[6],
           "window": _window(start, end),
           'coverage': ch.coverage_of(['news']),
           "reportable": n >= 25,
           "reportable_note": (None if n >= 25 else
                               "under 25 articles — panels below will be thin "
                               "and a distribution over them is noise")}
    cache.put(ck, out, TTL)
    return out


# ═══════════════════════════ trends ══════════════════════════════════════════
@progress.stage('trends')
def trends(term: str, granularity: str = "monthly", since: str | None = None,
           until: str | None = None, country: str | None = None,
           scope: str | None = None) -> dict:
    """Coverage volume over time, with the critical and tone series beside it.

    Three series from one scan, because they answer three different questions
    that a single volume line gets asked to answer and cannot: how much is
    being written, how much of it is consequential (priority >= 7, the band
    where geopolitics and disasters sit), and which way the tone is running."""
    g = GRANULARITY.get((granularity or "monthly").lower())
    if not g:
        return {"available": False,
                "reason": f"granularity must be one of {list(GRANULARITY)}"}
    start, end = _bounds(since, until)
    ck = cache.key("news.trends.v2", term.lower(), granularity, start, end, country,
                   scope)
    hit = cache.get(ck)
    if hit:
        return {**hit, "cached": True}
    where = [f"datetime >= '{start}'", f"datetime < '{end}'", term_predicate(term)]
    if scope:
        where.append(term_predicate(scope, "mention"))
    if country:
        where.append(f"lower(assumeNotNull(country_pri)) = {ch.sql_str(country.lower())}")
    rows = ch.chq_rows(
        f"SELECT toString({g}) AS period, count() AS n, "
        f"countIf({TOP_PRIORITY} >= {CRITICAL_PRIORITY}) AS critical, "
        f"countIf({ch.POLARITY} = 'neg') AS neg, "
        f"countIf({ch.POLARITY} = 'pos') AS pos, "
        f"round(avg({TOP_PRIORITY}), 2) AS mean_priority "
        f"FROM {ch.TABLE['news']} WHERE {' AND '.join(where)} "
        f"GROUP BY period ORDER BY period", timeout=280)
    if not rows:
        return {"available": False, "reason": f"no coverage of '{term}' in this window"}
    points = [{"period": r[0], "articles": int(r[1]), "critical": int(r[2]),
               "negative": int(r[3]), "positive": int(r[4]),
               "mean_priority": float(r[5] or 0),
               "critical_pct": round(100 * int(r[2]) / int(r[1]), 1) if int(r[1]) else 0}
              for r in rows]
    from .stats import trend as _trend, fill_periods
    filled = fill_periods([{'period': p['period'], 'n': p['articles'], 'detail': p}
                           for p in points], granularity.lower(), start, end)
    points = [{**p.get('detail', {'period': p['period'], 'articles': 0, 'critical': 0,
                                 'negative': 0, 'positive': 0, 'mean_priority': None,
                                 'critical_pct': 0}), 'partial_period': p['partial_period']}
              for p in filled]
    total = sum(p["articles"] for p in points)
    complete = [p for p in points if not p['partial_period']]
    out = {"available": True, "term": term, "points": points, "total": total,
           "match_mode": "mention",
           "critical_total": sum(p["critical"] for p in points),
           "trend": _trend([{"period": p["period"], "n": p["articles"]} for p in complete]),
           "critical_trend": _trend([{"period": p["period"], "n": p["critical"]}
                                     for p in complete]),
           'growth_note': 'Zero-count periods included; partial boundary buckets excluded from growth.',
           "country": country,
           "granularity": granularity,
           **_window(start, end, granularity),
           "coverage": ch.coverage_of(["news"])}
    if not out["coverage"]["partial"]:
        cache.put(ck, out, TTL)
    return out


# ═══════════════════════════ feeds ═══════════════════════════════════════════
_FEED_COLS = (f"target_id, toString(datetime), {TOP_PRIORITY}, {ch.POLARITY}, "
              f"{ch.TOP_SENTIMENT}, arraySlice(tags, 1, 6), "
              f"arrayMap(x -> x.1, arraySlice(categories, 1, 3)), "
              f"assumeNotNull(country_pri)")


def _feed(term: str, where_extra: list, order: str, limit: int, start: str,
          end: str, feature: str, mode: str = "central") -> dict:
    limit = max(1, min(int(limit or 10), MAX_FEED))
    where = [f"datetime >= '{start}'", f"datetime < '{end}'",
             term_predicate(term, mode)]
    where += [w for w in where_extra if w]
    rows = ch.chq_rows(
        f"SELECT {_FEED_COLS} FROM {ch.TABLE['news']} WHERE {' AND '.join(where)} "
        f"ORDER BY {order} LIMIT {limit}", timeout=280)
    if not rows:
        return {"available": False, "reason": f"no matching article for '{term}'",
                **_window(start, end)}
    signals = {}
    for r in rows:
        signals[r[0]] = {"datetime": r[1], "priority": int(r[2] or 0),
                         "polarity": r[3], "tone": r[4],
                         "tags": _arr(r[5]), "categories": _arr(r[6]),
                         "country": r[7] or None}
    recs = articles.resolve([r[0] for r in rows], signals)
    linked = [r for r in recs if r.get("url")]
    resolved, seen, rejected = [], set(), 0
    for row in linked:
        # Stored NER/tag matches alone are not proof of centrality. This cheap
        # second check uses reader-visible material and never invokes a model.
        visible = ' '.join(str(row.get(k) or '') for k in ('title', 'excerpt'))[:1400]
        relevant = (mode not in ('central', 'entity_central') or bool(re.search(
            r'(?<!\w)' + re.escape(term.strip()) + r'(?!\w)', visible, re.I)))
        if not relevant or row['url'] in seen:
            rejected += 1
            continue
        seen.add(row['url'])
        resolved.append(row)
    return {"available": bool(resolved), "term": term, "articles": resolved,
            "returned": len(resolved), "requested": limit, "match_mode": mode,
            "match_mode_note": ("only articles the term is central to: it is one "
                                "of the article's own tags, and the article is "
                                "not a round-up. A looser match fills a "
                                "priority-ranked feed with national digests that "
                                "name the term once"
                                if mode in ("central", "entity_central") else None),
            "unresolved": len(rows) - len(linked),
            "relevance_or_duplicate_rejections": rejected,
            "entity_identity_verified": False,
            "identity_note": "Visible term matching does not disambiguate homonyms such as Apple; inspect article context.",
            "unresolved_note": ("some ids no longer have a record in the article "
                                "store — rotated out, not an error"
                                if len(rows) - len(linked) else None),
            **_window(start, end),
            "coverage": ch.coverage_of(["news"])}


def _arr(cell) -> list:
    if not cell:
        return []
    s = str(cell).strip()
    if s.startswith("[") and s.endswith("]"):
        return [x.strip().strip("'\"") for x in re.findall(r"'((?:[^'\\]|\\.)*)'", s)]
    return [s]


@progress.stage('articles')
def recent_news(term: str, limit: int = 10, since: str | None = None,
                until: str | None = None, country: str | None = None,
                min_priority: int | None = None, match: str = "auto") -> dict:
    """The latest coverage of a term, newest first, as readable article records."""
    start, end = _bounds(since, until, months=6)
    extra = []
    if country:
        extra.append(f"lower(assumeNotNull(country_pri)) = {ch.sql_str(country.lower())}")
    if min_priority:
        extra.append(f"{TOP_PRIORITY} >= {int(min_priority)}")
    return _feed(term, extra, f"datetime DESC", limit, start, end, "news.recent",
                 mode=resolve_mode(term, match))


def critical_news(term: str, limit: int = 10, days: int = 120,
                  since: str | None = None, until: str | None = None,
                  match: str = "auto") -> dict:
    """The coverage that actually matters, not the coverage that is newest.

    Ranked by the article's own priority band first and recency second, and
    restricted to priority >= 7 — the band that, sampled on this corpus, holds
    geopolitics, regulation and disasters, against a band 1 that holds cookie
    notices and fixture lists. Tone is returned alongside so a caller can
    separate "big" from "bad"."""
    end = until or ch.NEWS_LAST_MONTH
    if since:
        start = since
    else:
        from datetime import date, timedelta
        e = date(int(end[:4]), int(end[5:7]), int(end[8:10]))
        start = str(e - timedelta(days=max(7, int(days or 120))))
    return _feed(term, [f"{TOP_PRIORITY} >= {CRITICAL_PRIORITY}"],
                 f"{TOP_PRIORITY} DESC, {centrality_rank(term)} ASC, datetime DESC",
                 limit, start, end, "news.critical",
                 mode=resolve_mode(term, match))


def article(target_id: str) -> dict:
    """One article by its id: the record plus everything Prism scored on it."""
    rows = ch.chq_rows(
        f"SELECT {_FEED_COLS}, arrayMap(x -> x.1, arraySlice(subcats, 1, 8)), "
        f"arrayMap(x -> x.1, arraySlice(classification, 1, 3)), "
        f"arrayMap(x -> x.1, arraySlice(moderation, 1, 4)), org_domains, "
        f"Organization, Person, Place "
        f"FROM {ch.TABLE['news']} WHERE target_id = {ch.sql_str(target_id)} LIMIT 1",
        timeout=120)
    if not rows:
        return {"available": False, "reason": "no article with that id in the corpus"}
    r = rows[0]
    sig = {"datetime": r[1], "priority": int(r[2] or 0), "polarity": r[3],
           "tone": r[4], "tags": _arr(r[5]), "categories": _arr(r[6]),
           "country": r[7] or None, "subcats": _arr(r[8]),
           "classification": _arr(r[9]), "moderation": _arr(r[10]),
           "source_domains": _arr(r[11]), "organizations": _arr(r[12]),
           "people": _arr(r[13]), "places": _arr(r[14])}
    recs = articles.resolve([target_id], {target_id: sig})
    if not recs or not recs[0].get("url"):
        return {"available": False,
                "reason": "scored in the corpus, but no record in the article store",
                "signals": sig}
    return {"available": True, "article": recs[0]}


# ═══════════════════════════ distributions ═══════════════════════════════════
BASELINE_DAYS = 30      # the corpus label distribution barely moves month to month
BASELINE_TTL = 86400


def _baseline(expr: str, carrier: str, end: str, limit: int = 4000) -> dict:
    """The corpus-wide distribution of a label column, cached for a day.

    This is the denominator behind every lift number, and computing it inside
    the same scan as the matched counts was what made a themes panel take 132
    seconds: it arrayJoins every article in the window, matched or not. The
    corpus distribution does not move meaningfully day to day, so it is
    computed once over a recent month and reused."""
    ck = cache.key("news.baseline.v1", expr, carrier, end, limit)
    hit = cache.get(ck)
    if hit:
        return hit
    rows = ch.chq_rows(
        f"SELECT label, count() c FROM (SELECT arrayJoin({expr}) AS label FROM "
        f"{ch.TABLE['news']} WHERE datetime >= addDays(toDate('{end}'), -{BASELINE_DAYS}) "
        f"AND datetime < '{end}' AND {carrier}) GROUP BY label ORDER BY c DESC "
        f"LIMIT {limit}", timeout=280)
    out = {"total": sum(int(r[1]) for r in rows),
           "counts": {r[0]: int(r[1]) for r in rows},
           "window_days": BASELINE_DAYS, "ends": end}
    cache.put(ck, out, BASELINE_TTL)
    return out


def _dist(term: str, expr: str, carrier: str, start: str, end: str, limit: int,
          mode: str = "mention", order: str = "lift", scope: str | None = None) -> dict:
    """A labelled distribution over the articles matching a term, with LIFT.

    Two queries, not one: the matched rows are filtered BEFORE the arrayJoin
    (cheap — it touches only the term's articles), and the corpus baseline
    comes from `_baseline` (cached). Raw counts alone rank the corpus rather
    than the term: 'business' is the top category of everything ever written,
    and lift is what isolates the labels unusually common FOR THIS TERM.

    `order='count'` for panels where the distribution itself is the answer —
    a geography map wants the biggest countries, not the most surprising ones."""
    m = term_predicate(term, mode)
    if scope:
        m = f"({m} AND {term_predicate(scope, 'mention')})"
    rows = ch.chq_rows(
        f"SELECT label, count() n FROM (SELECT arrayJoin({expr}) AS label FROM "
        f"{ch.TABLE['news']} WHERE datetime >= '{start}' AND datetime < '{end}' "
        f"AND {carrier} AND {m}) GROUP BY label ORDER BY n DESC LIMIT {limit * 6}",
        timeout=280)
    if not rows:
        return {"available": False, "reason": "no labelled article matches this term",
                "match_mode": mode}
    base = _baseline(expr, carrier, end)
    tot_m = sum(int(r[1]) for r in rows)
    out = []
    for label, n in rows:
        n = int(n)
        share = n / tot_m if tot_m else 0
        b = base["counts"].get(label, 0) / base["total"] if base["total"] else 0
        out.append({"label": label, "articles": n,
                    "share_pct": round(100 * share, 1),
                    "lift": round(share / b, 1) if b else None})
    if order == "count":
        out.sort(key=lambda x: -x["articles"])
    else:
        out.sort(key=lambda x: -((x["lift"] or 0) * (x["articles"] ** 0.5)))
    return {"available": True, "rows": out[:limit], "matched_labelled": tot_m,
            "match_mode": mode, "scope": scope,
            "ranked_by": ("lift over the label's corpus-wide share, weighted by "
                          "volume" if order != "count" else "article count"),
            "baseline": {"window_days": base["window_days"], "ends": base["ends"],
                         "note": "corpus label distribution, cached for a day"}}


@progress.stage('themes')
def themes(term: str, since: str | None = None, until: str | None = None,
           limit: int = 12, scope: str | None = None) -> dict:
    """What this term is ABOUT, across the three label systems Prism scores.

    Categories sit on 99% of articles, subcategories on 59%, and the article's
    own tags on 100%. All three are returned with the share of articles that
    carry each column, because a panel built on a column that is only present
    on a third of the corpus is describing a third of the corpus."""
    start, end = _bounds(since, until)
    ck = cache.key("news.themes.v2", term.lower(), start, end, limit, scope)
    hit = cache.get(ck)
    if hit:
        return {**hit, "cached": True}
    res = ch.parallel([
        lambda: _dist(term, "arrayMap(x -> x.1, categories)", "notEmpty(categories)",
                      start, end, limit, scope=scope),
        lambda: _dist(term, "arrayMap(x -> x.1, subcats)", "notEmpty(subcats)",
                      start, end, limit, scope=scope),
        lambda: _dist(term, "tags", "notEmpty(tags)", start, end, limit, scope=scope),
        lambda: _dist(term, "arrayMap(x -> x.1, classification)",
                      "notEmpty(classification)", start, end, limit, scope=scope),
    ], workers=4)
    cats, subs, tags, classif = res
    out = {"available": any((x or {}).get("available") for x in res), "term": term,
           "categories": cats, "subcategories": subs, "tags": tags,
           "taxonomy": classif,
           "fill_rates": {"categories": "99.1%", "subcategories": "59.2%",
                          "tags": "100%", "taxonomy": "96.2%",
                          "measured": "May 2026 slice",
                          "why": ("each distribution is computed over the "
                                  "articles carrying that column, so the "
                                  "denominators differ between panels")},
           **_window(start, end), "coverage": ch.coverage_of(["news"])}
    if not out["coverage"]["partial"]:
        cache.put(ck, out, TTL)
    return out


def entities(term: str, kind: str = "all", since: str | None = None,
             until: str | None = None, limit: int = 10,
             scope: str | None = None) -> dict:
    """The organisations, people and places that appear alongside this term.

    Bounded by `enriched_until()` rather than by the ingest edge: the entity
    columns stop being written before the corpus stops growing, and a
    co-occurrence panel run past that bound reports a collapse in everyone's
    prominence."""
    bound = enriched_until()
    start, end = _bounds(since, until or bound["bound"])
    if end > bound["bound"]:
        end = bound["bound"]
    ck = cache.key("news.entities.v2", term.lower(), kind, start, end, limit, scope)
    hit = cache.get(ck)
    if hit:
        return {**hit, "cached": True}
    # Places come from `country_all`/`cities_all`, NOT the `Place` array: sampled
    # live, Place holds 'bentley', 'toyota', 'ferrari' and 'rud' — the resolver
    # files brands and fragments there, and a places panel built on it is wrong
    # in a way a reader cannot see.
    want = {"organization": [("organizations", "Organization")],
            "person": [("people", "Person")],
            "place": [("places", "country_all")]}.get((kind or "all").lower(),
                                                      [("organizations", "Organization"),
                                                       ("people", "Person"),
                                                       ("places", "country_all")])
    # Places rank by count, not lift: a distribution over countries is a map,
    # and lift promotes whichever small country the resolver misfired on — an EV
    # query puts Central African Republic first, because 'car' collides with CAR.
    # Scope matters more here than anywhere. An unscoped entity panel on a
    # Delhi story returned BMC, Greater Hyderabad Municipal Corporation and
    # Eknath Shinde — every one of them real, none of them Delhi, because the
    # term "waterlogging" is national and the panel never asked about the place.
    res = ch.parallel([(lambda col=col: _dist(term, col, f"notEmpty({col})", start,
                                              end, limit,
                                              order="count" if col.endswith("_all")
                                              else "lift", scope=scope))
                       for _, col in want], workers=3)
    out = {"available": any((x or {}).get("available") for x in res), "term": term,
           "scope": scope,
           "entity_types_verified": False,
           "entity_quality_note": "These are upstream machine-assigned entity labels, not verified identities. Wrong types and incidental co-occurrences are possible; do not infer affiliations or prominence without article-level checks.",
           **{name: res[i] for i, (name, _) in enumerate(want)},
           **_window(start, end),
           "enrichment": {"bound": bound["bound"], "note": bound["note"],
                          "recent_fill": bound["months"][-3:]},
           "how": ("organisations and people are resolved entity names (stored "
                   "canonically: Tesla is 'tesla, inc.'); places come from the "
                   "geography columns, because the Place array also holds brands"),
           "coverage": ch.coverage_of(["news"])}
    if not out["coverage"]["partial"]:
        cache.put(ck, out, TTL)
    return out


def geography(term: str, level: str = "country", since: str | None = None,
              until: str | None = None, limit: int = 15) -> dict:
    """Where the coverage of this term is placed: country, state or city.

    This is the country an ARTICLE IS ABOUT, resolved by the pipeline — not
    where it was published and not where a phenomenon is. Same enrichment bound
    as `entities`, and the fill rate is returned with the rows."""
    col = {"country": "country_all", "state": "states_all",
           "city": "cities_all"}.get((level or "country").lower())
    if not col:
        return {"available": False,
                "reason": "level must be country, state or city"}
    bound = enriched_until()
    start, end = _bounds(since, until or bound["bound"])
    if end > bound["bound"]:
        end = bound["bound"]
    ck = cache.key("news.geography.v1", term.lower(), level, start, end, limit)
    hit = cache.get(ck)
    if hit:
        return {**hit, "cached": True}
    dist = _dist(term, col, f"notEmpty({col})", start, end, limit, order="count")
    fill = ch.chq_one(
        f"SELECT countIf({term_predicate(term)}) AS matched, "
        f"countIf({term_predicate(term)} AND notEmpty({col})) AS placed "
        f"FROM {ch.TABLE['news']} WHERE datetime >= '{start}' AND datetime < '{end}'",
        timeout=280)
    matched, placed = (int(fill[0] or 0), int(fill[1] or 0)) if fill else (0, 0)
    out = {"available": dist.get("available", False), "term": term, "level": level,
           "rows": dist.get("rows", []), "ranked_by": dist.get("ranked_by"),
           "placed_articles": placed, "matched_articles": matched,
           "placed_pct": round(100 * placed / matched, 1) if matched else None,
           "what": ("the place an article is ABOUT, as resolved by the pipeline "
                    "— not where it was published"),
           "ranked_by": "article count; `lift` is on each row for comparison",
           "caveat": ("place resolution has acronym collisions — an EV query "
                      "returns Central African Republic on articles about cars. "
                      "Rows far down the list with a high lift and a low count "
                      "are the ones to distrust"),
           **_window(start, end),
           "enrichment": {"bound": bound["bound"], "note": bound["note"]},
           "coverage": ch.coverage_of(["news"])}
    if not out["coverage"]["partial"]:
        cache.put(ck, out, TTL)
    return out


def sources(term: str, since: str | None = None, until: str | None = None,
            limit: int = 15, sample: int = 300, scope: str | None = None) -> dict:
    """Who is publishing this, how concentrated that is — and who it names.

    Two different things that are easy to confuse, kept apart:

      publishers — the outlet that ran the article. NOT in ClickHouse: the
        signal table has no publisher column, so this resolves a recent SAMPLE
        of matching articles against the article store and counts hosts. It is
        a sample and says so.
      organisations_mentioned — `org_domains`, which is what the pipeline
        LINKED IN the article. Sampled live it returns nintendo.com and
        atari.com on a retro-gaming piece: those are the subjects, not the
        publisher. Reported under its own name so nobody reads it as a
        publisher list.

    Concentration is the point of the panel. A term whose coverage is 60% one
    outlet is a term whose "trend" may be one newsroom's editorial line, and a
    volume chart handed over without that number is misleading."""
    start, end = _bounds(since, until)
    ck = cache.key("news.sources.v3", term.lower(), start, end, limit, sample, scope)
    hit = cache.get(ck)
    if hit:
        return {**hit, "cached": True}
    sample = max(50, min(int(sample or 300), 800))
    mode = resolve_mode(term)

    def ids():
        pred = term_predicate(term, mode)
        if scope:
            pred = f"({pred} AND {term_predicate(scope, 'mention')})"
        rows = ch.chq_rows(
            f"SELECT target_id FROM {ch.TABLE['news']} WHERE datetime >= '{start}' "
            f"AND datetime < '{end}' AND {pred} "
            f"ORDER BY datetime DESC LIMIT {sample}", timeout=280)
        return [r[0] for r in rows]

    res = ch.parallel([ids, lambda: _dist(term, "org_domains",
                                          "notEmpty(org_domains)", start, end,
                                          limit, mode="mention", scope=scope)],
                      workers=2)
    target_ids, mentioned = res[0] or [], res[1] or {"available": False}
    recs = articles.resolve(target_ids) if target_ids else []
    hosts: dict = {}
    for r in recs:
        h = (r.get("publisher") or "").lower().lstrip(".")
        if h:
            hosts[h] = hosts.get(h, 0) + 1
    n = sum(hosts.values())
    pubs = [{"publisher": k, "articles": v,
             "share_pct": round(100 * v / n, 1) if n else None}
            for k, v in sorted(hosts.items(), key=lambda kv: -kv[1])[:limit]]
    top3 = round(sum(p["share_pct"] or 0 for p in pubs[:3]), 1) if pubs else None
    out = {"available": bool(pubs or mentioned.get("available")), "term": term,
           "publishers": pubs, "sampled_articles": n, "sample_requested": sample,
           "distinct_publishers_in_sample": len(hosts),
           "concentration": {"top_publisher_pct": pubs[0]["share_pct"] if pubs else None,
                             "top3_pct": top3,
                             "reading": ("coverage is concentrated in a handful of "
                                         "outlets — read the volume trend as their "
                                         "editorial attention as much as the world's"
                                         if (top3 or 0) >= 50 else
                                         "coverage is spread across many outlets")},
           "organisations_mentioned": mentioned,
           "how": ("publishers are counted from the most recent sample of matching "
                   "articles resolved against the article store, not from the whole "
                   "window; organisations_mentioned is a different column entirely"),
           "match_mode": mode,
           **_window(start, end), "coverage": ch.coverage_of(["news"])}
    if not out["coverage"]["partial"]:
        cache.put(ck, out, TTL)
    return out


@progress.stage('sentiment')
def sentiment(term: str, granularity: str = "monthly", since: str | None = None,
              until: str | None = None, scope: str | None = None) -> dict:
    """Tone over time, against the corpus baseline.

    The baseline is the whole point: news in general runs negative, so a term at
    1.3 negative-to-positive is not "mostly negative", it is twice as negative
    as ordinary coverage. Both numbers are computed in the same window and the
    same way."""
    g = GRANULARITY.get((granularity or "monthly").lower())
    if not g:
        return {"available": False,
                "reason": f"granularity must be one of {list(GRANULARITY)}"}
    start, end = _bounds(since, until)
    ck = cache.key("news.sentiment.v2", term.lower(), granularity, start, end, scope)
    hit = cache.get(ck)
    if hit:
        return {**hit, "cached": True}
    m = term_predicate(term)
    if scope:
        m = f"({m} AND {term_predicate(scope, 'mention')})"
    rows = ch.chq_rows(
        f"SELECT toString({g}) AS period, "
        f"countIf(matched AND pol = 'neg') n_neg, countIf(matched AND pol = 'pos') n_pos, "
        f"countIf(matched AND pol = 'neutral') n_neu, "
        f"countIf(pol = 'neg') c_neg, countIf(pol = 'pos') c_pos "
        f"FROM (SELECT datetime, ({m}) AS matched, {ch.POLARITY} AS pol "
        f"      FROM {ch.TABLE['news']} WHERE datetime >= '{start}' "
        f"      AND datetime < '{end}' AND {ch.HAS_SENTIMENT}) "
        f"GROUP BY period ORDER BY period", timeout=280)
    if not rows:
        return {"available": False, "reason": f"no scored article mentions '{term}'"}
    points, tot = [], {"neg": 0, "pos": 0, "neutral": 0}
    c_neg = c_pos = 0
    for period, n, p, u, cn, cp in rows:
        n, p, u, cn, cp = int(n), int(p), int(u), int(cn), int(cp)
        tot["neg"] += n
        tot["pos"] += p
        tot["neutral"] += u
        c_neg += cn
        c_pos += cp
        if n + p + u == 0:
            continue
        points.append({"period": period, "negative": n, "positive": p,
                       "neutral": u, "ratio": round(n / p, 2) if p else None})
    tone = ch.tone_of(tot)
    baseline = round(c_neg / c_pos, 2) if c_pos else None
    out = {"available": bool(points), "term": term, "points": points,
           "totals": tone, "corpus_baseline_ratio": baseline,
           "vs_baseline": (round(tone["ratio"] / baseline, 2)
                           if tone.get("ratio") and baseline else None),
           "reading": _tone_reading(tone.get("ratio"), baseline),
           "how": ("one article, one polarity: the highest-scoring of its up-to-"
                   "three sentiment labels. Per-label percentages sum past 100 "
                   "and cannot be subtracted into a ratio"),
           "granularity": granularity, **_window(start, end, granularity),
           "coverage": ch.coverage_of(["news"])}
    if not out["coverage"]["partial"]:
        cache.put(ck, out, TTL)
    return out


def _tone_reading(ratio, baseline) -> str | None:
    if not ratio or not baseline:
        return None
    x = ratio / baseline
    if x >= 1.5:
        return "markedly more negative than ordinary news coverage"
    if x >= 1.15:
        return "somewhat more negative than ordinary news coverage"
    if x <= 0.66:
        return "markedly more positive than ordinary news coverage"
    if x <= 0.87:
        return "somewhat more positive than ordinary news coverage"
    return "about as negative as ordinary news coverage"


# ═══════════════════════════ trending ════════════════════════════════════════
LABEL_COLUMNS = {
    "subcats": ("arrayMap(x -> x.1, subcats)", "notEmpty(subcats)"),
    "tags": ("tags", "notEmpty(tags)"),
    "categories": ("arrayMap(x -> x.1, categories)", "notEmpty(categories)"),
}


def trending_topics(days: int = 14, limit: int = 20, by: str = "subcats",
                    category: str | None = None, country: str | None = None,
                    min_articles: int = 40, min_previous: int = 5) -> dict:
    """What is rising right now, corpus-wide — Prism's front page.

    A rising topic is one whose coverage grew against the immediately preceding
    window of the same length, not one with a big count: the biggest counts are
    the same evergreen subjects every week. Both windows end at the ingest-safe
    bound, so a half-ingested current week cannot manufacture a spike.

    `by` defaults to the CURATED subcategory labels rather than raw article
    tags, and the difference is the whole panel. Run over `tags`, the top of
    last fortnight's rising list is "bbc learning", "feifei", "transcript note"
    and "dailyhunt" — page furniture and syndication artefacts the tagger
    picked up. Run over `subcats`: virtual-reality headsets, smart glasses,
    reusable launch vehicles, liquid cooling. Tags remain available for a
    caller who wants raw vocabulary.

    `min_previous` is the other half of the filter: a label with nothing behind
    it in the previous window has no growth rate, only a burst, and bursts are
    usually one syndicated story."""
    from datetime import date, timedelta
    col = LABEL_COLUMNS.get((by or "subcats").lower())
    if not col:
        return {"available": False,
                "reason": f"`by` must be one of {list(LABEL_COLUMNS)}"}
    expr, carrier = col
    end = date(int(ch.NEWS_LAST_MONTH[:4]), int(ch.NEWS_LAST_MONTH[5:7]), 1)
    days = max(3, min(int(days or 14), 120))
    mid, start = end - timedelta(days=days), end - timedelta(days=days * 2)
    ck = cache.key("news.trending.v2", days, limit, by, category, country,
                   min_articles, min_previous)
    hit = cache.get(ck)
    if hit:
        return {**hit, "cached": True}
    extra = []
    if category:
        extra.append(f"hasAny(arrayMap(x -> x.1, categories), "
                     f"{ch.sql_arr([category.lower()])})")
    if country:
        extra.append(f"lower(assumeNotNull(country_pri)) = {ch.sql_str(country.lower())}")
    cond = (" AND " + " AND ".join(extra)) if extra else ""
    rows = ch.chq_rows(
        f"SELECT label, countIf(recent) AS now_n, countIf(NOT recent) AS prev_n "
        f"FROM (SELECT arrayJoin({expr}) AS label, datetime >= '{mid}' AS recent "
        f"      FROM {ch.TABLE['news']} WHERE datetime >= '{start}' AND datetime < "
        f"      '{end}' AND {carrier}{cond}) "
        f"GROUP BY label HAVING now_n >= {int(min_articles)} "
        f"ORDER BY now_n DESC LIMIT 6000", timeout=280)
    if not rows:
        return {"available": False, "reason": "no labelled coverage in this window"}
    scored = []
    for label, now_n, prev_n in rows:
        now_n, prev_n = int(now_n), int(prev_n)
        scored.append({"topic": label, "articles": now_n, "previous": prev_n,
                       "growth_x": round(now_n / prev_n, 2) if prev_n else None,
                       "new": prev_n == 0})
    rising = sorted([r for r in scored
                     if r["previous"] >= min_previous and (r["growth_x"] or 0) > 1.2],
                    key=lambda r: -((r["growth_x"] or 0) * (r["articles"] ** 0.5)))
    fresh = sorted([r for r in scored
                    if r["previous"] < min_previous and r["articles"] >= min_articles * 2],
                   key=lambda r: -r["articles"])
    out = {"available": True, "rising": rising[:limit],
           "newly_covered": fresh[:limit],
           "biggest": sorted(scored, key=lambda r: -r["articles"])[:limit],
           "labelled_by": by,
           "window": {"current": [str(mid), str(end)],
                      "previous": [str(start), str(mid)], "days": days},
           "filters": {"category": category, "country": country},
           "thresholds": {"min_articles": min_articles, "min_previous": min_previous},
           "how": ("growth against the previous window of equal length, weighted "
                   "by volume; labels with nothing behind them are held back as "
                   "'newly_covered' rather than ranked as infinite growth"),
           "coverage": ch.coverage_of(["news"])}
    if not out["coverage"]["partial"]:
        cache.put(ck, out, TTL)
    return out


# ═══════════════════════════ composite report ════════════════════════════════
def overview(term: str, since: str | None = None, until: str | None = None,
             granularity: str = "monthly") -> dict:
    """Everything Prism renders for one term, in one call.

    Nine measurements in parallel — the same panels the product shows — each
    carrying its own availability. A panel the corpus cannot support is absent
    with a reason rather than padded, and the composite still returns."""
    prof = resolve_term(term, since, until)
    if not prof.get("available"):
        return {"available": False, "reason": prof.get("reason"), "term": term}
    res = ch.parallel([
        lambda: trends(term, granularity, since, until),
        lambda: sentiment(term, granularity, since, until),
        lambda: themes(term, since, until),
        lambda: entities(term, "all", since, until),
        lambda: geography(term, "country", since, until),
        lambda: sources(term, since, until),
        lambda: recent_news(term, 8, since, until),
        lambda: critical_news(term, 8),
    ], workers=8)
    keys = ["trends", "sentiment", "themes", "entities", "geography", "sources",
            "recent", "critical"]
    panels = {k: (v or {"available": False, "reason": "panel failed"})
              for k, v in zip(keys, res)}
    return {"available": True, "term": term, "profile": prof, **panels,
            "panels_available": [k for k, v in panels.items() if v.get("available")],
            "panels_empty": {k: v.get("reason") for k, v in panels.items()
                             if not v.get("available")},
            "coverage": ch.coverage_of(["news"])}


def compare_terms(terms: list, granularity: str = "monthly",
                  since: str | None = None, until: str | None = None) -> dict:
    """Two to four terms, the same measurements, one window — Prism's "X vs Y".

    Share of the combined coverage is reported alongside each term's own volume,
    because the interesting question is usually which of them the world is
    paying attention to, not how many articles each got."""
    terms = [t.strip() for t in (terms or []) if t and t.strip()][:4]
    if len(terms) < 2:
        return {"available": False, "reason": "give at least two terms",
                "kind": "bad_request"}
    res = ch.parallel([(lambda t=t: trends(t, granularity, since, until))
                       for t in terms] +
                      [(lambda t=t: sentiment(t, granularity, since, until))
                       for t in terms], workers=8)
    n = len(terms)
    series = {t: (res[i] or {}) for i, t in enumerate(terms)}
    tones = {t: (res[n + i] or {}) for i, t in enumerate(terms)}
    total = sum((s.get("total") or 0) for s in series.values())
    rows = []
    for t in terms:
        s, tone = series[t], tones[t]
        rows.append({
            "term": t, "articles": s.get("total"),
            "share_pct": round(100 * (s.get("total") or 0) / total, 1) if total else None,
            "critical": s.get("critical_total"),
            "direction": (s.get("trend") or {}).get("direction"),
            "growth": (s.get("trend") or {}).get("late_vs_early"),
            "tone_ratio": (tone.get("totals") or {}).get("ratio"),
            "vs_baseline": tone.get("vs_baseline"),
            "points": s.get("points", []),
            "available": s.get("available", False),
        })
    leader = max([r for r in rows if r["articles"]], key=lambda r: r["articles"],
                 default=None)
    return {"available": any(r["available"] for r in rows), "terms": terms,
            "rows": rows, "combined_articles": total,
            "most_covered": leader["term"] if leader else None,
            "granularity": granularity,
            **_window(*_bounds(since, until), granularity),
            "caveat": ("more coverage is attention, not importance, and a term "
                       "that is also a common word will over-count — check each "
                       "term's own volume against its sources panel"),
            "coverage": ch.coverage_of(["news"])}


# ═══════════════════════════ seasonality ═════════════════════════════════════
MONTHS = ["January", "February", "March", "April", "May", "June", "July",
          "August", "September", "October", "November", "December"]


def seasonality(term: str, since: str | None = None, until: str | None = None,
                scope: str | None = None) -> dict:
    """Is this a seasonal story, and when is its season?

    Coverage collapsed onto month-of-year across several years. For a
    monsoon-driven subject this is the single most useful card the news corpus
    holds and no research corpus can produce it: Delhi waterlogging runs 2,257
    articles in July against 149 in January, a 15x swing that IS the story.

    A `concentration` figure says how much of the year's coverage falls in the
    top three months, which separates a genuinely seasonal subject from one
    that merely had a bad month once."""
    start, end = _bounds(since, until, months=60)
    ck = cache.key("news.seasonality.v1", term.lower(), start, end, scope)
    hit = cache.get(ck)
    if hit:
        return {**hit, "cached": True}
    where = [f"datetime >= '{start}'", f"datetime < '{end}'",
             term_predicate(term, "mention")]
    if scope:
        where.append(term_predicate(scope, "mention"))
    rows = ch.chq_rows(
        f"SELECT toMonth(datetime) m, count() c, "
        f"countIf({TOP_PRIORITY} >= {CRITICAL_PRIORITY}) crit "
        f"FROM {ch.TABLE['news']} WHERE {' AND '.join(where)} "
        f"GROUP BY m ORDER BY m", timeout=280)
    if not rows:
        return {"available": False, "reason": f"no coverage of '{term}' to profile"}
    by = {int(r[0]): (int(r[1]), int(r[2])) for r in rows}
    total = sum(v[0] for v in by.values())
    months = [{"month": m, "name": MONTHS[m - 1], "articles": by.get(m, (0, 0))[0],
               "critical": by.get(m, (0, 0))[1],
               "share_pct": round(100 * by.get(m, (0, 0))[0] / total, 1) if total else 0}
              for m in range(1, 13)]
    ranked = sorted(months, key=lambda x: -x["articles"])
    top3 = sum(x["articles"] for x in ranked[:3])
    peak, trough = ranked[0], ranked[-1]
    conc = round(100 * top3 / total, 1) if total else 0
    return {
        "available": True, "term": term, "scope": scope, "months": months,
        "peak": peak, "trough": trough,
        "peak_to_trough": round(peak["articles"] / trough["articles"], 1)
        if trough["articles"] else None,
        "top_three_months": [x["name"] for x in ranked[:3]],
        "concentration_pct": conc,
        "seasonal": conc >= 45,
        "reading": (f"strongly seasonal — {conc}% of coverage falls in "
                    f"{', '.join(x['name'] for x in ranked[:3])}" if conc >= 45
                    else f"only mildly seasonal — the top three months hold {conc}% "
                         f"of coverage, close to the {round(300/12, 1)}% a flat "
                         f"year would give"),
        "total": total, **_window(start, end, "month-of-year"),
        "how": ("every article in the window collapsed onto its calendar month, "
                "so several years of the same season stack together"),
        "coverage": ch.coverage_of(["news"]),
    }


# ═══════════════════════════ keyword growth ══════════════════════════════════
def keyword_growth(term: str, by: str = "subcats", since: str | None = None,
                   until: str | None = None, limit: int = 15,
                   min_recent: int = 12, scope: str | None = None) -> dict:
    """Which sub-themes inside a topic are growing, and which are fading.

    Not the same question as `trending_topics`, which ranks the whole corpus.
    This one stays inside a single subject's coverage and asks what has changed
    WITHIN it — for Delhi waterlogging, flight-delay coverage grew 16.5x while
    the baseline drainage vocabulary barely moved, which is a story about
    airports, not about drains."""
    col = LABEL_COLUMNS.get((by or "subcats").lower())
    if not col:
        return {"available": False, "reason": f"`by` must be one of {list(LABEL_COLUMNS)}"}
    expr, carrier = col
    start, end = _bounds(since, until, months=60)
    mid = _midpoint(start, end)
    ck = cache.key("news.keyword_growth.v1", term.lower(), by, start, end, limit,
                   min_recent, scope)
    hit = cache.get(ck)
    if hit:
        return {**hit, "cached": True}
    where = [f"datetime >= '{start}'", f"datetime < '{end}'",
             term_predicate(term, "mention"), carrier]
    if scope:
        where.append(term_predicate(scope, "mention"))
    rows = ch.chq_rows(
        f"SELECT label, countIf(recent) now_n, countIf(NOT recent) prev_n FROM "
        f"(SELECT arrayJoin({expr}) label, datetime >= '{mid}' recent FROM "
        f"{ch.TABLE['news']} WHERE {' AND '.join(where)}) GROUP BY label "
        f"HAVING now_n + prev_n >= 5 ORDER BY now_n DESC LIMIT 3000", timeout=280)
    if not rows:
        return {"available": False, "reason": "no labelled coverage of this term"}
    scored = []
    for label, now_n, prev_n in rows:
        now_n, prev_n = int(now_n), int(prev_n)
        scored.append({"label": label, "recent": now_n, "earlier": prev_n,
                       "growth_x": round(now_n / prev_n, 2) if prev_n else None,
                       "new": prev_n == 0})
    rising = sorted([r for r in scored if r["recent"] >= min_recent
                     and (r["growth_x"] or 0) > 1.3],
                    key=lambda r: -((r["growth_x"] or 0) * (r["recent"] ** 0.5)))
    fading = sorted([r for r in scored if r["earlier"] >= min_recent
                     and (r["growth_x"] is not None) and r["growth_x"] < 0.7],
                    key=lambda r: (r["growth_x"] or 9))
    return {"available": bool(rising or fading), "term": term, "scope": scope,
            "labelled_by": by,
            "rising": rising[:limit], "fading": fading[:limit],
            "steady": sorted([r for r in scored if r["recent"] >= min_recent
                              and r["growth_x"] and 0.8 <= r["growth_x"] <= 1.25],
                             key=lambda r: -r["recent"])[:6],
            "windows": {"earlier": [start, mid], "recent": [mid, end]},
            **_window(start, end),
            "how": ("counts inside this subject's own coverage, split at the "
                    "midpoint of the window — not against the whole corpus"),
            "coverage": ch.coverage_of(["news"])}


def _midpoint(start: str, end: str) -> str:
    from datetime import date
    a = date(int(start[:4]), int(start[5:7]), 1)
    b = date(int(end[:4]), int(end[5:7]), 1)
    t = (a.year * 12 + a.month - 1 + b.year * 12 + b.month - 1) // 2
    return f"{t // 12:04d}-{t % 12 + 1:02d}-01"


# ═══════════════════════════ events ══════════════════════════════════════════
def events(term: str, limit: int = 12, since: str | None = None,
           until: str | None = None, scope: str | None = None,
           min_priority: int = CRITICAL_PRIORITY) -> dict:
    """The datable events inside a topic's coverage, deduped by day.

    A story like this is a sequence of incidents, and a raw feed shows the same
    incident from six outlets. Grouping by day and keeping the highest-priority
    report of each gives a timeline a writer can narrate instead of a list they
    have to deduplicate by hand."""
    start, end = _bounds(since, until, months=48)
    where = [f"datetime >= '{start}'", f"datetime < '{end}'",
             term_predicate(term, "mention"),
             f"{TOP_PRIORITY} >= {int(min_priority)}"]
    if scope:
        where.append(term_predicate(scope, "mention"))
    rows = ch.chq_rows(
        f"SELECT toString(toDate(datetime)) d, count() n, "
        f"argMax(target_id, {TOP_PRIORITY}) tid, max({TOP_PRIORITY}) p, "
        f"countIf({ch.POLARITY} = 'neg') neg "
        f"FROM {ch.TABLE['news']} WHERE {' AND '.join(where)} "
        f"GROUP BY d ORDER BY n DESC, p DESC LIMIT {max(limit * 2, 24)}",
        timeout=280)
    if not rows:
        return {"available": False,
                "reason": f"no high-priority coverage of '{term}'"}
    sig = {r[2]: {"date": r[0], "reports_that_day": int(r[1]),
                  "priority": int(r[3]), "negative_reports": int(r[4])}
           for r in rows}
    recs = articles.resolve(list(sig.keys()), sig)
    got = [r for r in recs if r.get("url")]
    got.sort(key=lambda r: -(r.get("reports_that_day") or 0))
    return {"available": bool(got), "term": term, "scope": scope,
            "events": got[:limit],
            "ranked_by": ("how many outlets covered that day, then priority — "
                          "a day many newsrooms ran is an event, a day one did "
                          "is a story"),
            **_window(start, end),
            "coverage": ch.coverage_of(["news"])}
