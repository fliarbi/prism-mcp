#!/usr/bin/env python3
"""ch — ClickHouse plumbing for the Prism research layer.

Every number this server returns is read live from the ClickHouse cluster
set in PRISM_CH_HOST. Nothing in this module interprets anything; it retrieves,
counts, and gates.

Four rules are baked in because each one has already produced a confidently
wrong answer on this cluster:

  * Strict shard reads are the default. Coverage measurements expire after
    30 seconds and also check the historical row floor. Passing these checks
    establishes reachability, not completeness of ingestion or enrichment.
  * Research and patent corpora are RIGHT-CENSORED. OpenAlex carries 37.5M
    works for 2025 and only 10.9M for 2026 so far (measured 2026-08-21), and
    the news corpus thins out after May 2026. Any series that runs to "now"
    reads as a collapse that never happened. Windows stop at a lag-safe bound.
  * OpenAlex also carries junk future years (2027-2050, a few hundred rows).
    Every year filter is two-sided.
  * A phrase is not a query. Title-matching one token drifts off the claim and
    onto the whole field; short tokens need word boundaries ('amr' matches
    AMRUT). Matching happens through the helpers here, never ad hoc.
"""
from __future__ import annotations

import os
import re
import time
import threading
from contextvars import copy_context
import urllib.error
import urllib.parse
import urllib.request
from concurrent.futures import ThreadPoolExecutor

# set in the environment or the untracked .env (see .env.example)
CH_HOST = os.environ.get("PRISM_CH_HOST", "http://localhost:8123")
CH_USER = os.environ.get("PRISM_CH_USER", "default")
CH_PASSWORD = os.environ.get("PRISM_CH_PASSWORD", "")

_PARAMS = {
    "user": CH_USER,
    "password": CH_PASSWORD,
    "skip_unavailable_shards": "1",
    "max_execution_time": "280",
    # [2026-09-01] MCP probes are programmatic consumers sharing ClickHouse
    # with interactive Prism reports — yield CPU to the user-facing queries.
    "priority": "10",
    "max_threads": "12",
}
CH_URL = CH_HOST + "/?" + urllib.parse.urlencode(_PARAMS)
CH_URL_STRICT = CH_HOST + "/?" + urllib.parse.urlencode(
    {**_PARAMS, "skip_unavailable_shards": "0"})

# ── right-censoring boundaries (measured 2026-08-21, see module docstring) ───
RESEARCH_FIRST_YEAR = 1950
RESEARCH_LAST_YEAR = 2025      # 2026 is 29% ingested
TYPED_FIRST_YEAR = 2017        # the typed corpus starts here — measured, real
PATENT_LAST_YEAR = 2024        # patents publish ~18 months after filing
NEWS_LAST_MONTH = "2026-06-01"  # exclusive; June 2026 is 15% of a normal month

# ── corpus registry: table, what it is, known size for the coverage gate ─────
CORPORA = {
    "research": {
        "table": "openalex.works_distributed",
        "what": "OpenAlex works with abstracts, topics, authors, venues, citations",
        "expected": 384_832_354,
    },
    "research_typed": {
        "table": "research.openalex_prism_distributed",
        "what": "OpenAlex works typed by Prism with orientation + contribution "
                "(2017+, no abstracts on this table)",
        "expected": 98_602_364,
    },
    "pubmed": {
        "table": "ncbi.pubmed_articles_distributed",
        "what": "PubMed with article_types (RCT / meta-analysis / guideline) "
                "and country",
        "expected": 40_957_072,
    },
    "arxiv": {
        "table": "arxiv.papers_distributed",
        "what": "arXiv preprints with abstracts and categories",
        "expected": 3_034_675,
    },
    "patents": {
        "table": "patents.patents_distributed",
        "what": "granted + published patents with CPC codes and assignees",
        "expected": 108_034_545,
    },
    "news": {
        "table": "marketai.marketai_distributed",
        "what": "news articles with full text, sentiment, subcats, geography",
        "expected": 238_603_270,
    },
    "disease_factors": {
        "table": "marketai.disease_factors",
        "what": "extracted disease-factor claims typed by relation, direction, "
                "study tier and evidence strength",
        "expected": 55_545_265,
    },
    "companies": {
        "table": "companies_data.company_master",
        "what": "company master with descriptions, sector tags, funding, geo",
        "expected": 5_052_397,
    },
}
TABLE = {k: v["table"] for k, v in CORPORA.items()}


# ═══════════════════════════ query execution ═════════════════════════════════
class CHError(RuntimeError):
    pass


def chq(sql: str, timeout: int = 300, strict: bool = True) -> str:
    """Run SQL, return the raw body.

    ClickHouse puts the real diagnosis in the response BODY of an error and
    urllib throws that body away with the HTTPError, so every SQL bug would
    otherwise surface as a bare 'HTTP Error 404'. Re-raise carrying it."""
    if strict and os.environ.get("PRISM_ALLOW_PARTIAL") == "1":
        # Operator switch for an index host outage: answer from the shards that respond. coverage_of() still
        # reports partial=True, so every payload says its counts are floors, and partial answers are never cached.
        strict = False
    if strict:
        from . import availability
        availability.check_sql(sql)
    return _request(sql, timeout, strict)


def _request(sql, timeout, strict):
    params = {**_PARAMS, 'skip_unavailable_shards': '0' if strict else '1',
              'max_execution_time': str(min(280, max(1, int(timeout))))}
    req = urllib.request.Request(CH_HOST + '/?' + urllib.parse.urlencode(params),
                                 data=sql.encode())
    try:
        return urllib.request.urlopen(req, timeout=timeout).read().decode()
    except urllib.error.HTTPError as e:
        body = ""
        try:
            body = e.read().decode(errors="replace")[:400].strip()
        except Exception:
            pass
        raise CHError(f"CH {e.code}: {body}\n  SQL: {' '.join(sql.split())[:300]}") from None


def chq_rows(sql: str, timeout: int = 300) -> list:
    """TabSeparated -> list[list[str]], with '\\N' decoded to None."""
    txt = chq(sql + " FORMAT TabSeparated", timeout=timeout)
    return [[None if c == "\\N" else _unescape(c) for c in ln.split("\t")]
            for ln in txt.split("\n") if ln != ""]


_ESC = {"\\n": "\n", "\\t": "\t", "\\r": "\r", "\\'": "'", "\\\\": "\\"}


def _unescape(s: str) -> str:
    if "\\" not in s:
        return s
    return re.sub(r"\\[ntr'\\]", lambda m: _ESC.get(m.group(0), m.group(0)), s)


def chq_one(sql: str, timeout: int = 300):
    r = chq_rows(sql, timeout=timeout)
    return r[0] if r else None


def chq_int(sql: str, timeout: int = 300) -> int:
    """A single integer. RAISES on failure — it does not fall back to 0.

    A count that returns 0 because the query timed out is indistinguishable, in
    the payload, from a count that returns 0 because the corpus holds nothing
    on the subject. One of those is a fact about the world and the other is a
    fact about the cluster, and printing the second as the first is the exact
    failure this server exists to avoid. `parallel()` turns a raised error into
    None, and None renders as "unavailable", not as zero."""
    r = chq_one(sql, timeout=timeout)
    if not r or r[0] in (None, ""):
        raise CHError("empty result for count query")
    return int(r[0])


def parallel(fns: list, workers: int = 6) -> list:
    """Run independent CH reads concurrently. A failing lane returns None
    rather than taking the whole answer down with it — a thin section is a
    fact about the corpus, an exception is a fact about the plumbing."""
    if not fns:
        return []
    with ThreadPoolExecutor(max_workers=min(workers, len(fns))) as ex:
        # Each task gets its own context, including its request's progress sink.
        futs = [ex.submit(copy_context().run, f) for f in fns]
        out = []
        for f in futs:
            try:
                out.append(f.result())
            except Exception as e:
                out.append(None)
                _LAST_ERRORS.append(f"{type(e).__name__}: {e}")
    return out


_LAST_ERRORS: list = []


def drain_errors() -> list:
    out = list(_LAST_ERRORS)
    _LAST_ERRORS.clear()
    return out


# ═══════════════════════════ SQL literals ════════════════════════════════════
def sql_str(x) -> str:
    return "'" + str(x).replace("\\", "\\\\").replace("'", "\\'") + "'"


def sql_arr(xs) -> str:
    return "[" + ",".join(sql_str(x) for x in xs) + "]"


# ═══════════════════════════ matchers ════════════════════════════════════════
SHORT_PHRASE = 5     # at or below this length a phrase must match whole words


def prose_match(col: str, phrases) -> str:
    """Match phrases against a free-text column: long ones as substrings (the
    fast multi-search), short ones as whole words. 'amr' as a substring matches
    AMRUT, Amrit Bharat and Samriddhi — 1,557 rows against 12 real ones."""
    phrases = [p for p in (phrases or []) if p and p.strip()]
    long_ = [p for p in phrases if len(p) > SHORT_PHRASE]
    short = [p for p in phrases if len(p) <= SHORT_PHRASE]
    parts = []
    if long_:
        parts.append(f"multiSearchAnyCaseInsensitive({col}, {sql_arr(long_)})")
    if short:
        # lower() on BOTH sides. The column is lowercased in the match() call, so
        # an un-lowered alternative ('Tesla', 'AMR') can never fire — a silent
        # zero on every capitalised short term, which reads as "the corpus has
        # nothing" rather than as a bug.
        alt = "|".join(re.escape(p.lower()) for p in short)
        parts.append(f"match(lower({col}), {sql_str(r'\b(' + alt + r')\b')})")
    return "(" + " OR ".join(parts) + ")" if parts else "0"


def as_pole(x) -> dict:
    """Normalise a pole to {'phrases': [...], 'terms': [...]}.

    A pole of a claim is matched at two granularities, because the corpus
    indexes it at two granularities:

      * `phrases` are multi-word and match free TEXT — titles, article bodies,
        Prism's own generated keywords. Multi-word because a bare token in a
        title is a subject area, not a claim.
      * `terms` are one to three words and match only CURATED LABEL arrays —
        OpenAlex topics, MeSH headings. Those labels are already multi-word
        editorial names ('Heart rate and cardiovascular health', 'Coffee
        research and impacts'), so matching 'cardiovascular' against them is
        precise, while matching it against titles would not be.

    Measured on the coffee/cardiovascular claim (2026-08-21): phrases alone
    intersect at 33 papers, phrases + topic terms at 280 — and the 280 are on
    subject. The 33 is not precision, it is the corpus indexing the outcome
    under a topic name the phrase happened not to contain."""
    if isinstance(x, dict):
        ph = [p for p in (x.get("phrases") or []) if p]
        tm = [t for t in (x.get("terms") or []) if t]
    else:
        ph, tm = [p for p in (x or []) if p], []
    return {"phrases": ph, "terms": tm or ph}


def _labels(pole: dict, arrays) -> str:
    """OR of one arrayExists per curated-label array. Never arrayExists over
    arrayConcat: measured 2026-08-21, the same predicate written with
    arrayConcat takes 16.7s over the 98.6M-row typed table and 4.6s written as
    ORed arrayExists calls. arrayConcat materialises a new array per row and
    defeats short-circuiting. Same rows, 3.5x the time."""
    a = sql_arr(pole["terms"])
    return " OR ".join(
        f"arrayExists(x -> multiSearchAnyCaseInsensitive(x, {a}), {arr})"
        for arr in arrays)


def m_typed(pole, arrays: bool = True) -> str:
    """research.openalex_prism_distributed — the TYPED corpus.

    98.6M works carrying Prism's orientation and contribution labels. It is the
    only table that can say what a body of evidence CLAIMS rather than how much
    of it there is, and it is four times smaller than the reading corpus, so
    every count, mix and series in this server reads from here.

    Its window starts at 2017 (min publication_year, measured 2026-08-21). That
    is a real limit, not a bug, and it is why nothing here answers "the
    landmark 1998 paper" from this table — that question goes to
    openalex.works_distributed.

    `oa_keywords`/`oa_concepts` are deliberately NOT matched. They are OpenAlex
    concepts, and on a real coffee paper they read 'Medicine', 'Demography',
    'Confounding' — field furniture that matches everything. `oa_topics` and
    `prism_keywords` are the arrays that carry the subject."""
    pole = as_pole(pole)
    if not pole["phrases"] and not pole["terms"]:
        return "0"
    title = f"multiSearchAnyCaseInsensitive(title, {sql_arr(pole['phrases'])})" \
        if pole["phrases"] else "0"
    if not arrays:
        return f"({title})"
    parts = [title, _labels(pole, ("oa_topics",))]
    if pole["phrases"]:
        parts.append(f"arrayExists(x -> multiSearchAnyCaseInsensitive(x, "
                     f"{sql_arr(pole['phrases'])}), prism_keywords)")
    return "(" + " OR ".join(x for x in parts if x != "0") + ")"


def m_research(pole, arrays: bool = True) -> str:
    """openalex.works_distributed — the full-history READING corpus (384.8M,
    back to 1900) and the only one carrying abstracts.

    `arrays=False` when you intend to READ the documents rather than count
    them: the label expansion that makes counting work is too loose to rank on
    — ranked by citations it returns transcription-factor and
    solar-desalination papers for a groundwater query. Its `keywords` column is
    the same concept furniture as the typed table's and is not matched."""
    pole = as_pole(pole)
    if not pole["phrases"] and not pole["terms"]:
        return "0"
    title = f"multiSearchAnyCaseInsensitive(title, {sql_arr(pole['phrases'])})" \
        if pole["phrases"] else "0"
    if not arrays:
        return f"({title})"
    return "(" + " OR ".join(x for x in (title, _labels(pole, ("topics",)))
                             if x != "0") + ")"


def m_pubmed(pole, arrays: bool = True) -> str:
    """PubMed. MeSH headings are curated by humans and are the best label array
    on the cluster, so terms match there."""
    pole = as_pole(pole)
    if not pole["phrases"] and not pole["terms"]:
        return "0"
    title = f"multiSearchAnyCaseInsensitive(title, {sql_arr(pole['phrases'])})" \
        if pole["phrases"] else "0"
    if not arrays:
        return f"({title})"
    return "(" + " OR ".join(x for x in (title, _labels(pole, ("mesh_terms",)))
                             if x != "0") + ")"


def m_arxiv(pole, arrays: bool = True) -> str:
    return prose_match("title", as_pole(pole)["phrases"])


def m_news(pole, arrays: bool = True, text_col: str = "assumeNotNull(text)") -> str:
    """News is free text with no curated labels, so both granularities match the
    body — but through prose_match, which sends anything <=5 characters down the
    word-boundary path. A long phrase alone is too strict here: 'indian startup
    ecosystem' as an exact string appears in almost no article, while 'startup
    ecosystem' appears in 7,724 (measured 2026-08-21). Journalists do not write
    in search phrases."""
    pole = as_pole(pole)
    return prose_match(text_col, pole["phrases"] + pole["terms"])


def m_patents(pole, arrays: bool = True, cpc=()) -> str:
    pole = as_pole(pole)
    phrases = pole["phrases"] + pole["terms"]
    parts = []
    if phrases:
        parts.append(prose_match("title", phrases))
    for c in cpc or []:
        parts.append(f"arrayExists(x -> startsWith(x, {sql_str(c)}), cpc_codes)")
    return "(" + " OR ".join(parts) + ")" if parts else "0"


def m_companies(pole, arrays: bool = True) -> str:
    phrases = as_pole(pole)["phrases"]
    if not phrases:
        return "0"
    a = sql_arr(phrases)
    subs = " OR ".join(f"position(x,{sql_str(t)})>0" for t in phrases)
    hit = [f"multiSearchAnyCaseInsensitive(concat(short_description,' ',"
           f"detailed_description), {a})"]
    hit += [f"arrayExists(x -> {subs}, {c})"
            for c in ("feeds_other", "sub_category", "practice_area")]
    return "(" + " OR ".join(hit) + ")"


# ── news sentiment ──────────────────────────────────────────────────────────
# `sentiments` is Array(Tuple(label, score)) and one article carries up to three
# labels at once, so per-label percentages sum well past 100 and cannot be
# subtracted into a ratio. One article, one polarity: highest-scoring label wins.
TOP_SENTIMENT = "arraySort(x -> -x.2, sentiments)[1].1"
POLARITY = (f"if(position({TOP_SENTIMENT}, 'neg') > 0, 'neg', "
            f"if(position({TOP_SENTIMENT}, 'pos') > 0, 'pos', 'neutral'))")
HAS_SENTIMENT = "length(sentiments) > 0"


def tone_of(counts: dict) -> dict:
    """{'neg':n,'pos':n,'neutral':n} -> shares + ratio. The ratio only means
    anything against the corpus baseline (~0.6 neg:pos), so callers pass both."""
    neg, pos, neu = (int(counts.get(k) or 0) for k in ("neg", "pos", "neutral"))
    tot = neg + pos + neu
    if not tot:
        return {}
    return {"neg": neg, "pos": pos, "neutral": neu, "n": tot,
            "neg_pct": round(100 * neg / tot, 1),
            "pos_pct": round(100 * pos / tot, 1),
            "ratio": round(neg / pos, 2) if pos else None}


# ═══════════════════════════ coverage gating ═════════════════════════════════
_COV_CACHE: dict = {}
_COV_LOCKS = {name: threading.Lock() for name in CORPORA}
COVERAGE_TTL = float(os.environ.get('PRISM_COVERAGE_TTL', '30'))
COVERAGE_FAILURE_TTL = 3


def coverage(corpus: str) -> dict:
    """Is the table that owns this number actually all there right now?

    Strict reads fail if a shard is unavailable. Measurements expire after
    COVERAGE_TTL seconds; a row-count baseline alone cannot prove shard health."""
    spec = CORPORA.get(corpus)
    if not spec:
        return {"corpus": corpus, "partial": True, "pct": None, "unknown": True}
    with _COV_LOCKS[corpus]:
        hit = _COV_CACHE.get(corpus)
        ttl = COVERAGE_FAILURE_TTL if hit and hit.get('error') else COVERAGE_TTL
        if hit and time.time() - hit['checked_at'] < ttl:
            age = time.time() - hit['checked_at']
            return {**hit, 'age_seconds': round(age, 2),
                    'expires_in_seconds': round(max(0, ttl - age), 2)}
        return _measure_coverage(corpus, spec)


def _measure_coverage(corpus, spec):
    exp = spec["expected"]
    try:
        n = chq_int(f"SELECT count() FROM {spec['table']}", timeout=10)
    except Exception as e:
        out = {"corpus": corpus, "table": spec["table"], "rows": None,
                "expected": exp, "pct": None, "partial": True,
                'checked_at': time.time(), 'expires_in_seconds': 0,
                "error": f"{type(e).__name__}: {e}"}
        _COV_CACHE[corpus] = out
        return out
    pct = round(100.0 * n / exp, 1) if exp else 100.0
    d = {"corpus": corpus, "table": spec["table"], "rows": n, "expected": exp,
         "pct": pct, "partial": bool(exp) and n < exp,
         'checked_at': time.time(), 'age_seconds': 0,
         'expires_in_seconds': COVERAGE_TTL, 'strict_shard_read': True,
         'completeness': 'reachability and historical row floor, not an ingest completeness proof'}
    _COV_CACHE[corpus] = d
    return d


def coverage_of(corpora) -> dict:
    """Coverage block for a payload: one entry per corpus the answer touched,
    plus a single `partial` flag the client can render as a warning."""
    names = list(dict.fromkeys(corpora))
    def check(c):
        try:
            return coverage(c)
        except Exception as e:
            return {"corpus": c, "error": f"{type(e).__name__}: {e}",
                      "partial": True, "pct": None}
    with ThreadPoolExecutor(max_workers=max(1, min(8, len(names)))) as pool:
        out = dict(zip(names, pool.map(check, names)))
    return {"tables": out,
            "partial": any(v.get("partial") for v in out.values()),
            "note": ("one or more shards are unavailable — counts below are "
                     "floors, not totals" if any(v.get("partial") for v in out.values())
                     else "all listed tables passed strict shard reads and historical row floors")}


def floor(n, cov: dict):
    """Render a count honestly: 12,856 or '>=12,856' when the cluster is thin."""
    if n is None:
        return None
    s = f"{int(n):,}"
    return ">=" + s if cov.get("partial") else s
