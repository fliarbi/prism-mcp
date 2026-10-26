#!/usr/bin/env python3
"""deep — what an entity does, a section inside it, a month-by-month reading, and a disease profile.

Four capabilities that go past a volume chart:

  activities()  the AREAS OF ACTIVITY an entity's coverage falls into (the industry taxonomy every article is
                classified under, not the topical tags), and, for a company with a known domain, what its
                news EVENTS are (earnings, M&A, contracts, new products, lawsuits ...).
  drill()       one SECTION inside an entity, in the same scope: "Reliance Industries" AND "partnership", or
                AND "partnership" AND "artificial intelligence". Volume and its share of the entity's
                coverage month by month, tone against the entity's own, the tags and activity areas inside the
                section, and the dated events.
  timeline()    the ULTRA reading: Prism takes the month's highest-priority stories one month at a time, reads
                their openings, and writes what happened and why it mattered, each statement tied to the
                stories it came from; then the arc across the months.
  disease()     a DISEASE profile from the extracted health-claims corpus: risk factors, protective factors,
                causes, treatments and mechanisms, each counted with the share from high-tier studies, plus the
                claim series by year and the study-tier mix.

Every count comes from ClickHouse; the model only reads and writes, and its prose passes the number gate.
"""
from __future__ import annotations

import re
from concurrent.futures import ThreadPoolExecutor

from . import cache, ch, llm, news

TTL = 6 * 3600
HIGH_TIERS = ("review_meta", "clinical_rct", "clinical")
# spelling variants of one factor counted together (the label shown is the first spelling met)
_CANON = {"obese": "obesity", "being overweight": "overweight", "smoker": "smoking", "smokers": "smoking",
          "cigarette smoking": "smoking", "tobacco use": "smoking", "physical inactivity": "sedentary lifestyle",
          "lack of physical activity": "sedentary lifestyle", "family history of diabetes": "family history",
          "alcohol": "alcohol consumption", "alcohol use": "alcohol consumption", "dense breasts": "dense breast tissue",
          "high blood pressure": "hypertension", "older age": "age", "ageing": "age", "aging": "age",
          "hiv infection": "hiv", "hiv/aids": "hiv", "diabetes mellitus": "diabetes", "diabetes mellitus (dm)": "diabetes",
          "type 2 diabetes mellitus": "type 2 diabetes", "untreated": "untreated tb", "undernutrition": "malnutrition",
          "excess weight": "overweight", "family history of breast cancer": "family history",
          "brca1 mutation": "brca mutations", "brca2 mutation": "brca mutations", "brca mutation": "brca mutations",
          "brca1": "brca mutations", "brca2": "brca mutations", "chemo": "chemotherapy"}
_GENERIC_TAXONOMY = ("/News/", "/Finance/Investing", "/Sensitive Subjects", "/People & Society/Other")


def _pretty(path: str) -> str:
    return " › ".join(p for p in path.strip("/").split("/") if p and p != "Other")


def _scope_terms(scope) -> list:
    if isinstance(scope, (list, tuple)):
        parts = scope
    else:
        parts = re.split(r"[,;+]| AND ", str(scope or ""))
    return [p.strip().lower() for p in parts if p and p.strip()][:4]


def _pred(term: str, scope_terms: list) -> str:
    p = news.term_predicate(term, "mention")
    for s in scope_terms:
        p = f"({p} AND {news.term_predicate(s, 'mention')})"
    return p


# ════════════════════════════════════ activities ════════════════════════════════════
def activities(term: str, domain: str = "", since: str | None = None, until: str | None = None,
               limit: int = 12) -> dict:
    start, end = news._bounds(since, until)
    ck = cache.key("deep.activities.v2", term.lower(), domain.lower(), start, end, limit)
    hit = cache.get(ck)
    if hit:
        return {**hit, "cached": True}
    tax, subs, tags = ch.parallel([
        lambda: news._dist(term, "arrayMap(x -> x.1, classification)", "notEmpty(classification)",
                           start, end, limit * 4),
        lambda: news._dist(term, "arrayMap(x -> x.1, subcats)", "notEmpty(subcats)", start, end, limit),
        lambda: news._dist(term, "tags", "notEmpty(tags)", start, end, limit, order="count"),
    ], workers=3)
    areas = []
    for r in (tax or {}).get("rows") or []:
        if any(r["label"].startswith(g) for g in _GENERIC_TAXONOMY):
            continue
        areas.append({**r, "area": _pretty(r["label"]), "path": r["label"]})
    areas = areas[:limit]
    out = {"available": bool(areas or (subs or {}).get("available")), "term": term,
           "areas_of_activity": {"rows": areas, "what": ("the industry taxonomy each article is classified under, "
                                                         "with generic news and investing classes removed; lift is "
                                                         "the area's share for this entity over its share of all news")},
           "activity_topics": {"rows": (subs or {}).get("rows") or [],
                               "what": "Prism's curated subcategories: the narrower topics inside those areas"},
           "top_tags": {"rows": (tags or {}).get("rows") or [],
                        "what": ("the articles' own tags, ranked by count: the internal labels behind every "
                                 "'themes' panel, and the co-mentioned companies, people and places")},
           **news._window(start, end), "coverage": ch.coverage_of(["news"])}
    if domain:
        out["company_events"] = _events_by_type(domain, start, end)
    if not out["coverage"]["partial"]:
        cache.put(ck, out, TTL)
    return out


def _json_list(cell) -> list:
    import json
    try:
        v = json.loads(cell) if isinstance(cell, str) else cell
    except ValueError:
        return []
    return [x for x in (v or []) if isinstance(x, (list, tuple)) and len(x) >= 2]


def _events_by_type(domain: str, start: str, end: str) -> dict:
    d = ch.sql_str(domain.lower().strip())
    try:
        rows = ch.chq_rows(
            f"SELECT event_type, count() n, uniqExact(target_id) docs, "
            f"toJSONString(arraySlice(groupArray((toString(toDate(news_publish_datetime)), headline)), 1, 3)) ex "
            f"FROM (SELECT * FROM companies_data.company_events_flat WHERE domain = {d} "
            f"AND news_publish_datetime >= '{start}' AND news_publish_datetime < '{end}' "
            f"ORDER BY news_publish_datetime DESC) GROUP BY event_type ORDER BY n DESC", timeout=120)
    except Exception as e:
        return {"available": False, "reason": f"{type(e).__name__}"}
    if not rows:
        return {"available": False, "reason": f"no company events recorded for {domain} in the window"}
    total = sum(int(r[1]) for r in rows)
    monthly = ch.chq_rows(
        f"SELECT toString(toStartOfMonth(news_publish_datetime)) m, event_type, count() FROM companies_data.company_events_flat "
        f"WHERE domain = {d} AND news_publish_datetime >= '{start}' AND news_publish_datetime < '{end}' "
        f"GROUP BY m, event_type ORDER BY m", timeout=120)
    by_month = {}
    for m, et, n in monthly:
        by_month.setdefault(m, {})[et.replace("_", " ")] = int(n)
    return {"available": True, "domain": domain, "total": total,
            "by_month": [{"period": m, **v} for m, v in sorted(by_month.items())],
            "risk_types": ["lawsuit", "regulatory", "layoffs"],
            "catalyst_types": ["new product", "contracts", "ma", "asset acquisition", "job creation", "fda approval"],
            "rows": [{"event_type": r[0].replace("_", " "), "events": int(r[1]), "articles": int(r[2]),
                      "share_pct": round(100 * int(r[1]) / total, 1),
                      "examples": [{"date": e[0], "headline": e[1]} for e in _json_list(r[3])]} for r in rows],
            "what": ("company events extracted from business news and linked to the company's web domain; "
                     "the linkage is complete to May 2026")}


# ══════════════════════════════════════ drill ═══════════════════════════════════════
def drill(term: str, scope, since: str | None = None, until: str | None = None, limit: int = 10) -> dict:
    sc = _scope_terms(scope)
    if not sc:
        return {"available": False, "reason": "give a scope: a phrase inside the entity, e.g. 'partnership'"}
    start, end = news._bounds(since, until)
    ck = cache.key("deep.drill.v1", term.lower(), "|".join(sc), start, end, limit)
    hit = cache.get(ck)
    if hit:
        return {**hit, "cached": True}
    whole, inner = news.term_predicate(term, "mention"), _pred(term, sc)
    pol = ch.POLARITY
    rows = ch.chq_rows(
        f"SELECT toString(toStartOfMonth(datetime)) m, count() n, countIf({inner}) s, "
        f"countIf({inner} AND {pol} = 'neg') sneg, countIf({inner} AND {pol} = 'pos') spos, "
        f"countIf({pol} = 'neg') neg, countIf({pol} = 'pos') pos "
        f"FROM {ch.TABLE['news']} WHERE datetime >= '{start}' AND datetime < '{end}' AND {whole} "
        f"GROUP BY m ORDER BY m", timeout=280)
    if not rows:
        return {"available": False, "reason": f"no coverage of '{term}' in the window"}
    pts, tot, sec, sn, sp, n_, p_ = [], 0, 0, 0, 0, 0, 0
    for m, n, s, sneg, spos, neg, pos in rows:
        n, s = int(n), int(s)
        tot, sec, sn, sp, n_, p_ = tot + n, sec + s, sn + int(sneg), sp + int(spos), n_ + int(neg), p_ + int(pos)
        pts.append({"period": m, "entity_articles": n, "section_articles": s,
                    "section_share_pct": round(100 * s / n, 2) if n else None})
    if not sec:
        return {"available": False, "reason": f"no '{term}' coverage also mentions {' + '.join(sc)}",
                "entity_articles": tot}
    sec_ratio = round(sn / sp, 2) if sp else None
    ent_ratio = round(n_ / p_, 2) if p_ else None
    third = max(1, len(pts) // 3)
    early = sum(p["section_articles"] for p in pts[:third])
    late = sum(p["section_articles"] for p in pts[-third:])
    tags, tax = ch.parallel([
        lambda: _scoped_dist(inner, "tags", "notEmpty(tags)", start, end, limit),
        lambda: _scoped_dist(inner, "arrayMap(x -> x.1, classification)", "notEmpty(classification)",
                             start, end, limit * 3),
    ], workers=2)
    tax = [dict(r, area=_pretty(r["label"])) for r in tax if not any(r["label"].startswith(g) for g in _GENERIC_TAXONOMY)][:limit]
    ev = _events(inner, start, end, limit)
    out = {"available": True, "term": term, "scope": sc,
           "section": {"articles": sec, "share_of_entity_pct": round(100 * sec / tot, 2), "entity_articles": tot,
                       "late_vs_early": round(late / early, 2) if early else None,
                       "peak": max(pts, key=lambda p: p["section_articles"])},
           "tone": {"section_neg_per_pos": sec_ratio, "entity_neg_per_pos": ent_ratio,
                    "reading": (None if not (sec_ratio and ent_ratio) else
                                "the section is covered more negatively than the entity as a whole"
                                if sec_ratio > ent_ratio * 1.15 else
                                "the section is covered more positively than the entity as a whole"
                                if sec_ratio < ent_ratio / 1.15 else "the section's tone is in line with the entity's")},
           "points": pts, "top_tags": tags, "areas_of_activity": tax, "events": ev,
           "how": ("an article is in the section when it mentions the entity and every scope phrase (lede or tag); "
                   "share is of the entity's own monthly coverage, so a busy month for the entity does not read as "
                   "growth of the section"),
           **news._window(start, end), "coverage": ch.coverage_of(["news"])}
    if not out["coverage"]["partial"]:
        cache.put(ck, out, TTL)
    return out


def _scoped_dist(pred: str, expr: str, carrier: str, start: str, end: str, limit: int) -> list:
    rows = ch.chq_rows(
        f"SELECT label, count() n FROM (SELECT arrayJoin({expr}) AS label FROM {ch.TABLE['news']} "
        f"WHERE datetime >= '{start}' AND datetime < '{end}' AND {carrier} AND {pred}) "
        f"GROUP BY label ORDER BY n DESC LIMIT {limit * 4}", timeout=280)
    base = news._baseline(expr, carrier, end)
    tot = sum(int(r[1]) for r in rows) or 1
    out = []
    for label, n in rows:
        n = int(n)
        b = base["counts"].get(label, 0) / base["total"] if base["total"] else 0
        out.append({"label": label, "articles": n, "share_pct": round(100 * n / tot, 1),
                    "lift": round((n / tot) / b, 1) if b else None})
    return out[:limit * 2]


def _events(pred: str, start: str, end: str, limit: int) -> list:
    rows = ch.chq_rows(
        f"SELECT toString(toDate(datetime)) d, count() n, argMax(target_id, {news.TOP_PRIORITY}) tid, "
        f"max({news.TOP_PRIORITY}) p, argMax(substringUTF8(assumeNotNull(text), 1, 300), {news.TOP_PRIORITY}) t "
        f"FROM {ch.TABLE['news']} WHERE datetime >= '{start}' AND datetime < '{end}' AND {pred} "
        f"AND {news.TOP_PRIORITY} >= 6 GROUP BY d ORDER BY n DESC, p DESC LIMIT {limit}", timeout=280)
    return [{"date": r[0], "reports_that_day": int(r[1]), "target_id": r[2], "priority": int(r[3]),
             "opening": (r[4] or "").strip()} for r in rows]


# ═════════════════════════════════════ timeline ═════════════════════════════════════
_MONTH_SYS = """You are a research analyst reading one month of the most widely reported stories about a subject.
Each story is given as [id] (date) opening text. Write what happened that month and why it mattered, using ONLY
these stories. Every point must name the story ids it rests on. Do not add numbers that are not in the openings.
Return JSON: {"headline": "one sentence: the month in a line", "points": [{"text": "...", "ids": ["..."]}] (2 to 4),
"why_it_matters": "one or two sentences", "signal": "new|escalating|steady|easing|turning point"}"""

_ARC_SYS = """You are a research analyst. You are given month-by-month summaries of a subject's most reported
stories. Write the arc across the months using only those summaries: what changed, the turning points (name the
months), and what to watch next. Do not add numbers that are not in the summaries.
Return JSON: {"arc": "4 to 6 sentences", "turning_points": [{"month": "YYYY-MM", "why": "..."}], "watch": ["...", "..."]}"""


def _months(end: str, n: int) -> list:
    y, m = int(end[:4]), int(end[5:7])
    out = []
    for _ in range(n):
        m -= 1
        if m == 0:
            y, m = y - 1, 12
        out.append(f"{y:04d}-{m:02d}-01")
    return list(reversed(out))


def _next(month: str) -> str:
    y, m = int(month[:4]), int(month[5:7]) + 1
    if m == 13:
        y, m = y + 1, 1
    return f"{y:04d}-{m:02d}-01"


def timeline(term: str, scope=None, months: int = 12, until: str | None = None, per_month: int = 6) -> dict:
    sc = _scope_terms(scope)
    months = max(3, min(int(months or 12), 24))
    end = (until or ch.NEWS_LAST_MONTH)[:7] + "-01"
    ck = cache.key("deep.timeline.v1", term.lower(), "|".join(sc), end, months, per_month)
    hit = cache.get(ck)
    if hit:
        return {**hit, "cached": True}
    pred = _pred(term, sc)
    plan = _months(end, months)

    def read(month):
        evs = _events(pred, month, _next(month), per_month)
        vol = ch.chq_rows(f"SELECT count() FROM {ch.TABLE['news']} WHERE datetime >= '{month}' "
                          f"AND datetime < '{_next(month)}' AND {pred}", timeout=200)
        n = int(vol[0][0]) if vol else 0
        if not evs:
            return {"month": month[:7], "articles": n, "available": False, "reason": "no high-priority stories"}
        packed = "\n\n".join(f"[{e['target_id']}] ({e['date']}) {e['opening']}" for e in evs)
        out = llm.call_json(_MONTH_SYS, f"SUBJECT: {term}{' — ' + ', '.join(sc) if sc else ''}\nMONTH: {month[:7]}\n\n{packed}",
                            max_tokens=2500) or {}
        ids = {e["target_id"] for e in evs}
        pts = []
        for p in (out.get("points") or [])[:4]:
            good = [i for i in (p.get("ids") or []) if i in ids]
            txt = str(p.get("text") or "").strip()
            if good and txt and not llm.ungrounded_numbers(txt, [packed]):
                pts.append({"text": txt, "ids": good})
        return {"month": month[:7], "articles": n, "available": bool(pts),
                "headline": out.get("headline") if not llm.ungrounded_numbers(str(out.get("headline") or ""), [packed]) else None,
                "points": pts, "why_it_matters": out.get("why_it_matters"), "signal": out.get("signal"),
                "stories": [{"date": e["date"], "target_id": e["target_id"], "reports_that_day": e["reports_that_day"],
                             "opening": e["opening"][:220]} for e in evs]}

    with ThreadPoolExecutor(4) as ex:
        read_months = list(ex.map(read, plan))
    good = [m for m in read_months if m.get("available")]
    arc = {}
    if good:
        digest = "\n".join(f"{m['month']}: {m.get('headline') or ''} " + " ".join(p["text"] for p in m["points"])
                           for m in good)
        arc = llm.call_json(_ARC_SYS, f"SUBJECT: {term}\n\n{digest}", max_tokens=2500) or {}
        if llm.ungrounded_numbers(str(arc.get("arc") or ""), [digest]):
            arc["arc_note"] = "numbers not present in the monthly readings were removed"
            arc["arc"] = llm.strip_numbers(str(arc.get("arc") or ""))
    out = {"available": bool(good), "term": term, "scope": sc, "months_read": len(good), "months": read_months,
           "arc": arc.get("arc"), "turning_points": arc.get("turning_points") or [], "watch": arc.get("watch") or [],
           "how": ("for each month, the days most outlets reported on the subject (high-priority stories, one per "
                   "day) are read from their openings; every point cites the stories it came from, and prose with "
                   "numbers not present in those openings is dropped"),
           "window": {"from": plan[0], "to": end, "to_is_exclusive": True, "months": months},
           "coverage": ch.coverage_of(["news"])}
    if good and not out["coverage"]["partial"]:
        cache.put(ck, out, 24 * 3600)
    return out


# ══════════════════════════════════════ disease ═════════════════════════════════════
def disease(name: str, since_year: int = 2015, limit: int = 12) -> dict:
    nm = name.strip().lower()
    if len(nm) < 3:
        return {"available": False, "reason": "give a disease name"}
    ck = cache.key("deep.disease.v4", nm, since_year, limit)
    hit = cache.get(ck)
    if hit:
        return {**hit, "cached": True}
    T = ch.TABLE["disease_factors"]
    w = f"positionCaseInsensitive(disease, {ch.sql_str(nm)}) > 0"
    hi = ", ".join(ch.sql_str(t) for t in HIGH_TIERS)
    rel, top, years, tiers, strength, src = ch.parallel([
        lambda: ch.chq_rows(f"SELECT relation, count() FROM {T} WHERE {w} GROUP BY relation ORDER BY 2 DESC", timeout=200),
        lambda: ch.chq_rows(
            f"SELECT relation, direction, lower(factor) f, count() c, countIf(study_tier IN ({hi})) h "
            f"FROM {T} WHERE {w} AND lower(factor) NOT IN ({ch.sql_str(nm)}, 'disease', 'symptoms', 'treatment', "
            f"'outbreak', 'death', 'cases', 'patients', 'infection') "
            f"GROUP BY relation, direction, f ORDER BY c DESC LIMIT 400", timeout=200),
        lambda: ch.chq_rows(f"SELECT toYear(pub_date) y, count(), countIf(study_tier IN ({hi})) FROM {T} WHERE {w} "
                            f"AND toYear(pub_date) >= {int(since_year)} GROUP BY y ORDER BY y", timeout=200),
        lambda: ch.chq_rows(f"SELECT study_tier, count() FROM {T} WHERE {w} GROUP BY study_tier ORDER BY 2 DESC", timeout=200),
        lambda: ch.chq_rows(f"SELECT evidence_strength, count() FROM {T} WHERE {w} GROUP BY evidence_strength ORDER BY 2 DESC", timeout=200),
        lambda: ch.chq_rows(f"SELECT source, count() FROM {T} WHERE {w} GROUP BY source ORDER BY 2 DESC", timeout=200),
    ], workers=6)
    if not rel:
        return {"available": False, "reason": f"no extracted health claims name '{name}'"}
    total = sum(int(r[1]) for r in rel)
    groups = {"risk_factors": ("risk_factor", "increases"), "protective_factors": ("protective", None),
              "causes": ("cause", None), "treatments": ("treatment", None), "mechanisms": ("mechanism", None),
              "associations": ("association", None)}
    panels = {}
    for key, (r_, d_) in groups.items():
        rows = [x for x in top if x[0] == r_ and (d_ is None or x[1] == d_)]
        merged = {}
        for _, _, f, c, h in rows:
            k = re.sub(r"s$", "", _CANON.get(f, f))
            m = merged.setdefault(k, {"factor": f, "claims": 0, "high_tier": 0})
            m["claims"] += int(c)
            m["high_tier"] += int(h)
        lst = sorted(merged.values(), key=lambda x: -x["claims"])[:limit]
        for x in lst:
            x["high_tier_pct"] = round(100 * x["high_tier"] / x["claims"], 1) if x["claims"] else None
        panels[key] = lst
    yr = [{"year": int(y), "claims": int(c), "high_tier": int(h)} for y, c, h in years]
    complete = [p for p in yr if p["year"] < 2026]
    out = {"available": True, "disease": name, "claims": total,
           "by_relation": {r[0]: int(r[1]) for r in rel}, **panels,
           "series": yr, "series_note": "2026 is incomplete; extraction runs behind publication",
           "growth_late_vs_early": (round(sum(p["claims"] for p in complete[-3:]) / max(1, sum(p["claims"] for p in complete[:3])), 2)
                                    if len(complete) >= 6 else None),
           "study_tiers": {r[0]: int(r[1]) for r in tiers},
           "high_tier_share_pct": round(100 * sum(int(r[1]) for r in tiers if r[0] in HIGH_TIERS) / total, 1),
           "evidence_strength": {r[0]: int(r[1]) for r in strength},
           "sources": {r[0]: int(r[1]) for r in src},
           "what": ("extracted claims, not papers: each names a factor, its relation to the disease and, for risk "
                    "factors, a direction; one paper or article can yield several, and a restated finding counts "
                    "each time it is restated. high_tier = review/meta-analysis, RCT or clinical study."),
           "coverage": ch.coverage_of(["disease_factors"])}
    if not out["coverage"]["partial"]:
        cache.put(ck, out, TTL)
    return out
