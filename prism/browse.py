#!/usr/bin/env python3
"""browse — reading the Prism research corpus directly, by stance.

The research tools elsewhere in this server answer a QUESTION ("is this claim
supported?"). This module answers a different one: "show me the work". It is
the browse surface over `research.openalex_prism_distributed` — 98.6M papers
that Prism has typed with an ORIENTATION (how the paper frames what it found)
and a CONTRIBUTION (what kind of work it is), which is what makes "promising
studies about X, most recent first" a query rather than a wish.

    orientation   breakthrough · promising · descriptive · comparative ·
                  cautionary · problem_identifying · critical
    contribution  empirical · review · methodological · theoretical · position

Three decisions this module makes differently from the claim tools, all of them
learned by getting it wrong first:

PRECISION BEATS RECALL WHEN BROWSING. The claim pipeline expands a subject
across the corpus's own topic labels, because a claim needs every paper that
bears on it. Browsing does not: expanded, "ease of doing business" becomes
"Economic Growth and Development" plus "International Business and FDI" and
returns 155,987 papers of general development economics. Anchored on the
phrase, it returns 223 papers that are actually about the ease of doing
business. `expand=True` is available and off by default.

A TRAILING "IN <X>" IS A SCOPE, NOT PART OF THE PHRASE. Nobody titles a paper
"ease of doing business in india"; searching the literal string finds one
result and reads as "there is no research on this". The term is split into a
subject and a scope, the scope is required to appear in the title, and if the
split finds nothing the whole string is tried instead — with the reading
reported, so a caller can override it. The scope need not be a place:
"generative ai in education" scopes to education the same way.

"IN INDIA" IS TWO DIFFERENT QUESTIONS. Research ABOUT a place says so in its
title; research FROM a place carries the affiliation. OpenAlex has no country
column on this cluster, so both are approximations and the payload names which
one produced the rows. Measured on this subject: the title lane finds 73
papers, the affiliation lane 9 — they are not interchangeable, and averaging
them would mean nothing.
"""
from __future__ import annotations

import re

from . import cache, ch, llm

TTL = 43200
ORIENTATIONS = ("breakthrough", "promising", "descriptive", "comparative",
                "cautionary", "problem_identifying", "critical")
CONTRIBUTIONS = ("empirical", "review", "methodological", "theoretical", "position")
POSITIVE = ("breakthrough", "promising")
CONTESTED = ("cautionary", "problem_identifying", "critical")
SORTS = {
    "recent": "publication_date DESC, cited_by_count DESC",
    "cited": "cited_by_count DESC, publication_year DESC",
    "stance": "stance_score DESC, cited_by_count DESC",
    "oldest": "publication_date ASC",
}
COLS = ("openalex_id, title, authors, venue_name, publication_year, "
        "toString(publication_date), doi, oa_url, cited_by_count, orientation, "
        "contribution, stance_score, arraySlice(oa_topics, 1, 4), "
        "arraySlice(institution_names, 1, 3)")

# Scope candidates. The named entries are the common cases; the trailing
# catch-all accepts any short qualifier ("education", "manufacturing"), because
# the split is VERIFIED against the corpus afterwards rather than trusted — a
# scope that finds nothing falls back to the whole phrase.
_PLACE_HINT = re.compile(
    r"^(india|china|usa|us|america|uk|britain|europe|africa|asia|germany|france|"
    r"japan|brazil|russia|canada|australia|indonesia|nigeria|pakistan|bangladesh|"
    r"vietnam|mexico|kenya|singapore|israel|italy|spain|korea|turkey|egypt|"
    r"south africa|saudi arabia|uae|emirates|the eu|latin america|southeast asia|"
    r"sub-saharan africa|[a-z ]{3,20})$")


# ═══════════════════════════ term parsing ════════════════════════════════════
def split_scope(term: str) -> dict:
    """Separate the subject from a trailing place scope.

    "ease of doing business in india" -> subject "ease of doing business",
    scope "india". Nobody writes the whole string in a title, so searching it
    literally returns nothing and reads as an empty literature."""
    t = re.sub(r"\s+", " ", (term or "").strip())
    if " in " not in t.lower():
        return {"subject": t, "scope": None, "split": False}
    head, tail = re.split(r"\s+in\s+", t, maxsplit=1, flags=re.I)
    head, tail = head.strip(), tail.strip()
    if len(head.split()) < 2 or not _PLACE_HINT.match(tail.lower()):
        return {"subject": t, "scope": None, "split": False}
    return {"subject": head, "scope": tail, "split": True}


def _phrase_pred(phrases, expand: bool) -> str:
    """Title + keyword match. Keywords are included because a paper's own
    keyword list carries the phrase when the title paraphrases it; the wider
    topic-label expansion is opt-in."""
    phrases = [p.strip().lower() for p in phrases if p and p.strip()]
    if not phrases:
        return "1"
    a = ch.sql_arr(phrases)
    parts = [ch.prose_match("title", phrases),
             f"arrayExists(x -> multiSearchAnyCaseInsensitive(x, {a}), oa_keywords)"]
    if expand:
        parts.append(f"arrayExists(x -> multiSearchAnyCaseInsensitive(x, {a}), "
                     f"oa_topics)")
        parts.append(f"arrayExists(x -> multiSearchAnyCaseInsensitive(x, {a}), "
                     f"prism_keywords)")
    return "(" + " OR ".join(parts) + ")"


_VARIANT_SYS = (
 "You list the phrases a RESEARCH PAPER TITLE would use for a subject, so a "
 "corpus can be browsed for it. Return JSON {\"phrases\": [str]}.\n"
 "* 3-6 phrases, multi-word, lower case.\n"
 "* The standard term first, then the phrasings a paper on this actually uses: "
 "'ease of doing business' -> 'ease of doing business', 'business environment', "
 "'regulatory burden', 'investment climate', 'doing business index'.\n"
 "* No field names ('economics', 'public policy'), no generic words "
 "('study', 'analysis', 'impact'), no place names — the scope is handled "
 "separately.")


def variants(subject: str, limit: int = 6) -> dict:
    """Title phrasings for a subject, audited against the corpus before use.

    One phrase is not a literature. Browsing "ease of doing business" scoped to
    India on the exact string returns a single paper; adding the phrasings the
    field actually uses — business environment, investment climate, regulatory
    burden — returns the real body of work. Every variant is counted against
    titles first and dropped if nothing uses it, so a model's invention cannot
    quietly widen the result."""
    subject = (subject or "").strip()
    if not subject:
        return {"phrases": [], "audit": []}
    ck = cache.key("browse.variants.v1", subject.lower(), limit)
    hit = cache.get(ck)
    if hit:
        return hit
    out = llm.call_json(_VARIANT_SYS, f"SUBJECT: {subject}", max_tokens=600)
    cand, seen = [subject.lower()], {subject.lower()}
    for p in ((out or {}).get("phrases") or []):
        pl = re.sub(r"\s+", " ", str(p).strip().lower())
        if pl and pl not in seen and (" " in pl or "-" in pl) and len(pl) > 6:
            seen.add(pl)
            cand.append(pl)
    cand = cand[:limit]
    sel = ", ".join(f"countIf({ch.prose_match('title', [p])}) AS p{i}"
                    for i, p in enumerate(cand))
    try:
        row = ch.chq_one(
            f"SELECT {sel} FROM {ch.TABLE['research_typed']} WHERE "
            f"publication_year BETWEEN {ch.TYPED_FIRST_YEAR} AND "
            f"{ch.RESEARCH_LAST_YEAR}", timeout=280)
    except Exception:
        row = None
    audit = [{"phrase": p, "titles": int(row[i] or 0) if row else None}
             for i, p in enumerate(cand)]
    # The phrase the caller typed anchors the set. A "synonym" running far
    # ahead of it is a broader concept wearing a synonym's clothes: for "ease of
    # doing business" (207 titles) the model offers "business environment"
    # (2,557), and with it in the set the results become generic management
    # papers that happen to use the words. Ceiling: 8x the anchor, floor 500 so
    # a rare anchor does not reject its own real synonyms.
    anchor = next((a["titles"] or 0 for a in audit if a["phrase"] == subject.lower()), 0)
    ceiling = max(8 * anchor, 500)
    kept, dropped = [], []
    for a in audit:
        n = a["titles"] or 0
        if n < 3:
            dropped.append({**a, "why": "no paper title uses this phrasing"})
        elif a["phrase"] != subject.lower() and n > ceiling:
            dropped.append({**a, "why": (f"{n:,} titles against the subject's "
                                         f"{anchor:,} — a broader concept, not a "
                                         f"phrasing of this one")})
        else:
            kept.append(a["phrase"])
    kept = kept or [subject.lower()]
    res = {"phrases": kept, "audit": sorted(audit, key=lambda a: -(a["titles"] or 0)),
           "dropped": dropped, "anchor_titles": anchor, "ceiling": ceiling,
           "how": ("phrasings a paper title would use, counted against the corpus; "
                   "dropped when unused, or when far broader than the subject")}
    cache.put(ck, res, TTL)
    return res


def _geo_pred(scope: str, mode: str) -> str:
    """about  — the place is named in the title: research ABOUT there.
    from    — the place is in an affiliation: research FROM there.

    Different questions with different answers, and `institution_names` is
    written on 62.6% of rows, so the affiliation lane is also thinner by
    construction."""
    s = scope.strip().lower()
    if mode == "from":
        return (f"arrayExists(x -> positionCaseInsensitive(x, {ch.sql_str(s)}) > 0, "
                f"institution_names)")
    # A word-BOUNDARY match on the place name loses the adjective, and the
    # adjective is how titles are written: "Evidence from Indian States",
    # "Chinese manufacturing". `\bindia` catches india, indian, india's. It can
    # also catch a longer place (indiana), which the payload says out loud
    # rather than pretending precision it does not have.
    return f"match(lower(title), {ch.sql_str(r'\b' + re.escape(s))})"


def _where(subject_phrases, scope, geo_mode, expand, since, until,
           orientation, contribution, min_citations) -> list:
    y0 = max(int(since or ch.TYPED_FIRST_YEAR), ch.TYPED_FIRST_YEAR)
    y1 = min(int(until or ch.RESEARCH_LAST_YEAR), ch.RESEARCH_LAST_YEAR)
    w = [f"publication_year BETWEEN {y0} AND {y1}",
         _phrase_pred(subject_phrases, expand)]
    if scope:
        w.append(_geo_pred(scope, geo_mode))
    if orientation:
        vals = [o for o in _as_list(orientation) if o in ORIENTATIONS]
        if vals:
            w.append(f"orientation IN {ch.sql_arr(vals)}")
    if contribution:
        vals = [c for c in _as_list(contribution) if c in CONTRIBUTIONS]
        if vals:
            w.append(f"contribution IN {ch.sql_arr(vals)}")
    if min_citations:
        w.append(f"cited_by_count >= {int(min_citations)}")
    return w, (y0, y1)


def _as_list(x) -> list:
    if isinstance(x, str):
        return [v.strip().lower() for v in x.split(",") if v.strip()]
    return [str(v).strip().lower() for v in (x or [])]


def _paper(r: list) -> dict:
    doi = (r[6] or "").replace("https://doi.org/", "")
    return {"id": r[0], "title": (r[1] or "").strip(),
            "authors": _arr(r[2])[:8], "venue": r[3] or None,
            "year": int(r[4]) if r[4] else None, "date": r[5],
            "doi": doi or None,
            "url": (f"https://doi.org/{doi}" if doi else
                    (r[7] or f"https://openalex.org/{r[0]}")),
            "cited_by": int(r[8] or 0), "orientation": r[9],
            "contribution": r[10],
            "stance_score": round(float(r[11]), 3) if r[11] not in (None, "") else None,
            "topics": _arr(r[12]), "institutions": _arr(r[13])}


def _dedupe(rows) -> list:
    """The corpus holds the same paper more than once — different OpenAlex ids,
    identical title. A browse page showing one paper twice looks broken even
    when the count behind it is right."""
    out, seen = [], set()
    for r in rows:
        p = _paper(r)
        key = re.sub(r"[^a-z0-9]+", "", (p["title"] or "").lower())[:90]
        if key and key in seen:
            continue
        seen.add(key)
        out.append(p)
    return out


def _arr(cell) -> list:
    if not cell:
        return []
    s = str(cell).strip()
    if s.startswith("[") and s.endswith("]"):
        return [x.strip().strip("'\"") for x in re.findall(r"'((?:[^'\\]|\\.)*)'", s)]
    return [s]


# ═══════════════════════════ browse ══════════════════════════════════════════
def browse(term: str, orientation: str = "", contribution: str = "",
           geo: str = "", geo_mode: str = "about", since: int = 0, until: int = 0,
           sort: str = "recent", limit: int = 20, expand: bool = False,
           min_citations: int = 0, also: list | None = None) -> dict:
    """List papers on a subject, filtered by how they frame what they found.

    "Promising studies about the ease of doing business in India, newest first"
    is `browse(term='ease of doing business in india', orientation='promising')`.

    Returns the papers plus facets — the orientation and contribution mix, the
    year histogram, the dominant topics, venues and institutions — so the next
    query is visible from this one rather than guessed."""
    parsed = split_scope(term)
    subject = parsed["subject"]
    scope = (geo or parsed["scope"] or "").strip() or None
    var = None
    if also:
        phrases = [subject] + list(also)
    else:
        var = variants(subject)
        phrases = var["phrases"]
    sort_sql = SORTS.get((sort or "recent").lower(), SORTS["recent"])
    limit = max(1, min(int(limit or 20), 100))
    geo_mode = "from" if str(geo_mode).lower() in ("from", "affiliation") else "about"

    ck = cache.key("browse.v2", subject.lower(), scope, geo_mode, orientation,
                   contribution, since, until, sort, limit, expand, min_citations,
                   tuple(also or ()), tuple(phrases))
    hit = cache.get(ck)
    if hit:
        return {**hit, "cached": True}

    where, (y0, y1) = _where(phrases, scope, geo_mode, expand, since, until,
                             orientation, contribution, min_citations)
    W = " AND ".join(where)
    # Facets are computed WITHOUT the stance filters. Faceting the filtered set
    # tells a reader that 100% of promising papers are promising; faceting the
    # subject tells them there are also 29 problem-identifying ones next door,
    # which is the whole reason to show facets on a browse page.
    base_where, _ = _where(phrases, scope, geo_mode, expand, since, until,
                           None, None, min_citations)
    BW = " AND ".join(base_where)
    T = ch.TABLE["research_typed"]

    # If the phrase carries a scope that finds nothing, the split was wrong —
    # try the whole string before reporting an empty literature.
    n = ch.chq_int(f"SELECT count() FROM {T} WHERE {W}", timeout=280)
    fallback = None
    if n == 0 and parsed["split"]:
        w2, _ = _where([term], None, geo_mode, expand, since, until, orientation,
                       contribution, min_citations)
        W2 = " AND ".join(w2)
        n2 = ch.chq_int(f"SELECT count() FROM {T} WHERE {W2}", timeout=280)
        if n2:
            fallback = ("the phrase was read as a whole rather than split at "
                        f"'in {parsed['scope']}'")
            W, n, scope = W2, n2, None
    if n == 0:
        return {"available": False,
                "reason": (f"no paper in the typed corpus matches "
                           f"'{subject}'" + (f" scoped to {scope}" if scope else "")
                           + (" — try expand=true, or a broader phrase"
                              if not expand else "")),
                "subject": subject, "scope": scope,
                "window": f"{y0}-{y1}"}

    res = ch.parallel([
        lambda: ch.chq_rows(f"SELECT {COLS} FROM {T} WHERE {W} ORDER BY {sort_sql} "
                            f"LIMIT {limit}", timeout=280),
        lambda: ch.chq_rows(f"SELECT orientation, count() c FROM {T} WHERE {BW} "
                            f"GROUP BY orientation ORDER BY c DESC", timeout=280),
        lambda: ch.chq_rows(f"SELECT contribution, count() c FROM {T} WHERE {BW} "
                            f"GROUP BY contribution ORDER BY c DESC", timeout=280),
        lambda: ch.chq_rows(f"SELECT publication_year y, count() c FROM {T} WHERE "
                            f"{BW} GROUP BY y ORDER BY y", timeout=280),
        lambda: ch.chq_rows(f"SELECT t, count() c FROM (SELECT arrayJoin(oa_topics) t "
                            f"FROM {T} WHERE {BW} AND notEmpty(oa_topics)) GROUP BY t "
                            f"ORDER BY c DESC LIMIT 10", timeout=280),
        lambda: ch.chq_rows(f"SELECT k, count() c FROM (SELECT arrayJoin(oa_keywords) k "
                            f"FROM {T} WHERE {BW} AND notEmpty(oa_keywords)) GROUP BY k "
                            f"ORDER BY c DESC LIMIT 12", timeout=280),
    ], workers=6)
    rows, orient, contrib, years, topics, keywords = res
    mix = {r[0]: int(r[1]) for r in (orient or [])}
    total = sum(mix.values()) or n
    return {
        "available": bool(rows),
        "subject": subject, "scope": scope, "geo_mode": geo_mode if scope else None,
        "scope_means": ({"about": ("the scope word must appear in the paper's "
                                   "title — work ABOUT it. The scope need not be "
                                   "a place: 'in education' scopes the same way"),
                         "from": ("the scope appears in an affiliation — work "
                                  "FROM there. Only meaningful for a place, and "
                                  "institution names are on 62.6% of rows")
                         }[geo_mode] if scope else None),
        "matched": n, "matched_note": ("papers matching every filter; the "
                                       "orientation facet below counts the whole "
                                       "subject, so you can see what the filter "
                                       "excluded"),
        "returned": len(_dedupe(rows or [])),
        "papers": _dedupe(rows or []),
        "facets": {
            "orientation": [{"orientation": k, "papers": v,
                             "share_pct": round(100 * v / total, 1)}
                            for k, v in mix.items()],
            "contribution": [{"contribution": r[0], "papers": int(r[1])}
                             for r in (contrib or [])],
            "by_year": [{"year": int(r[0]), "papers": int(r[1])} for r in (years or [])],
            "topics": [{"topic": r[0], "papers": int(r[1])} for r in (topics or [])],
            "keywords": [{"keyword": r[0], "papers": int(r[1])}
                         for r in (keywords or [])],
        },
        "stance_summary": {
            "positive_pct": round(100 * sum(mix.get(k, 0) for k in POSITIVE) / total, 1)
            if total else None,
            "contested_pct": round(100 * sum(mix.get(k, 0) for k in CONTESTED) / total, 1)
            if total else None,
        },
        "filters": {"orientation": _as_list(orientation) or None,
                    "contribution": _as_list(contribution) or None,
                    "sort": sort, "expand": expand,
                    "min_citations": min_citations or None},
        "term_split": parsed, "fallback": fallback,
        "phrases": phrases,
        "phrase_audit": (var or {}).get("audit"),
        "scope_match": ("word-prefix on the title, so the adjective form counts "
                        "('indian', \"india's\", 'educational') — a longer word "
                        "sharing the prefix can slip in (india/indiana)"
                        if scope and geo_mode == "about" else None),
        "window": f"{y0}-{y1}",
        "vocabulary": {"orientation": list(ORIENTATIONS),
                       "contribution": list(CONTRIBUTIONS), "sort": list(SORTS)},
        "how": ("matched on the phrase in title and paper keywords" +
                (" plus the corpus topic labels (expand=true)" if expand else
                 " — set expand=true to widen to the whole concept cluster")),
        "caveat": ("orientation labels how a paper FRAMES its finding, not whether "
                   "the finding is true; and this corpus starts in 2017"),
        "coverage": ch.coverage_of(["research_typed"]),
    }


# ═══════════════════════════ stance over time ════════════════════════════════
def stance_trends(term: str, geo: str = "", geo_mode: str = "about",
                  since: int = 0, until: int = 0, expand: bool = False,
                  also: list | None = None) -> dict:
    """How the framing of a literature has moved, year by year.

    This is what "promising studies trends about X" actually asks for: not how
    many papers exist, but how the balance between promising, descriptive,
    cautionary and critical work has shifted. Shares are reported alongside
    counts, because a rising count of cautionary papers means nothing if every
    kind of paper is rising."""
    parsed = split_scope(term)
    subject = parsed["subject"]
    scope = (geo or parsed["scope"] or "").strip() or None
    geo_mode = "from" if str(geo_mode).lower() in ("from", "affiliation") else "about"
    ck = cache.key("browse.stance_trends.v1", subject.lower(), scope, geo_mode,
                   since, until, expand, tuple(also or ()))
    hit = cache.get(ck)
    if hit:
        return {**hit, "cached": True}

    phrases = ([subject] + list(also)) if also else variants(subject)["phrases"]
    where, (y0, y1) = _where(phrases, scope, geo_mode, expand,
                             since, until, None, None, 0)
    W = " AND ".join(where)
    rows = ch.chq_rows(
        f"SELECT publication_year y, orientation, count() c, "
        f"round(avg(stance_score), 3) FROM {ch.TABLE['research_typed']} "
        f"WHERE {W} GROUP BY y, orientation ORDER BY y", timeout=280)
    if not rows:
        return {"available": False,
                "reason": (f"no typed paper matches '{subject}'" +
                           (f" scoped to {scope}" if scope else "")),
                "subject": subject}
    by_year: dict = {}
    for y, o, c, sc in rows:
        y = int(y)
        d = by_year.setdefault(y, {"year": y, "total": 0, "orientation": {},
                                   "stance_score": None})
        d["orientation"][o] = int(c)
        d["total"] += int(c)
    points = []
    for y in sorted(by_year):
        d = by_year[y]
        pos = sum(d["orientation"].get(k, 0) for k in POSITIVE)
        con = sum(d["orientation"].get(k, 0) for k in CONTESTED)
        points.append({**d,
                       "positive": pos, "contested": con,
                       "positive_pct": round(100 * pos / d["total"], 1) if d["total"] else None,
                       "contested_pct": round(100 * con / d["total"], 1) if d["total"] else None})
    thin = [p["year"] for p in points if p["total"] < 20]
    from .stats import trend as _trend
    totals: dict = {}
    for p in points:
        for k, v in p["orientation"].items():
            totals[k] = totals.get(k, 0) + v
    series = {k: _trend([{"period": str(p["year"]),
                          "n": p["orientation"].get(k, 0)} for p in points])
              for k in totals}
    early = points[:max(1, len(points) // 3)]
    late = points[-max(1, len(points) // 3):]

    def _share(block, keys):
        tot = sum(p["total"] for p in block) or 1
        return round(100 * sum(p["orientation"].get(k, 0) for p in block
                               for k in keys) / tot, 1)

    shift = round(_share(late, CONTESTED) - _share(early, CONTESTED), 1)
    return {
        "available": True, "subject": subject, "scope": scope,
        "geo_mode": geo_mode if scope else None, "phrases": phrases,
        "points": points, "totals": totals,
        "papers": sum(totals.values()),
        "per_orientation_trend": series,
        "framing_shift": {
            "early_contested_pct": _share(early, CONTESTED),
            "late_contested_pct": _share(late, CONTESTED),
            "delta_pct_points": shift,
            "reading": ("recent work is markedly more cautious than earlier work"
                        if shift >= 8 else
                        "recent work is markedly more positive than earlier work"
                        if shift <= -8 else "the balance of framing is broadly unchanged"),
        },
        "thin_years": thin,
        "thin_note": ("years with under 20 papers — a share computed on them is "
                      "noise" if thin else None),
        "window": f"{y0}-{y1}",
        "term_split": parsed,
        "caveat": ("orientation is how a paper frames its own finding, not a "
                   "verdict; and a rising count means little without the share "
                   "beside it, which is why both are here"),
        "coverage": ch.coverage_of(["research_typed"]),
    }
