#!/usr/bin/env python3
"""query — turning a sentence a writer typed into something a corpus can answer.

This module decides whether everything downstream is about the CLAIM or merely
about its subject area. Three measured facts drive the design.

1. A claim is a CONCEPT CLUSTER, not a phrase. Title-matching "groundwater
   depletion" over the research corpus returns 208 rows; expanding across the
   concept arrays returns 259,628. Nobody titles a paper about aquifer
   over-abstraction "groundwater depletion".

2. The expansion that makes COUNTING work is too loose to READ from. Ranked by
   citations, a concept-expanded groundwater query returns transcription-factor
   and solar-desalination papers. So reading is title-anchored on multi-word
   phrases; counting uses the arrays.

3. A claim has TWO POLES and ORing them dissolves it. "Coffee improves
   cardiovascular health" ORed across its phrases matches 341,078 papers,
   almost all of them cardiology papers with nothing to say about coffee. The
   same claim as subject AND outcome is a few thousand papers that are actually
   about the claim. This is the same rule the Prism problem pipeline learned as
   "industry terms must AND-narrow, never OR-widen" — an OR does not build a
   universe, it dissolves one.

So a query object carries both poles and both lanes, every phrase in it has
been counted against the live corpus before use, and the payload always names
which lane produced the rows. A phrase that matches nothing is dropped and
named; a phrase carrying almost the whole match is dropped and named, because
that is the signature of a field name that wandered in, and without the audit
it is invisible — the answer just looks full.
"""
from __future__ import annotations

import re
import time

from . import cache, ch, llm, vocab, progress

TTL = 86400           # a claim's concept cluster does not move day to day
MIN_PHRASE_ROWS = 3   # below this a phrase is a typo or a coinage, not a concept
DOMINANCE = 40        # a phrase matching this many times the runner-up is a field
MAX_SIDE = 5          # phrases kept per pole
MIN_AND = 25          # below this the intersection lane is too thin to stand on
# Concept expansion is the expensive half of every read: one arrayExists per
# array per phrase, per row. Measured 2026-08-21: title-only over the 98.6M-row
# typed table is 0.8s, the same predicate with arrays is 4.6s, and written with
# arrayConcat 16.7s. Counting expands the top EXPAND phrases per pole; reading
# and ranking still see every kept phrase.
EXPAND = 3

DOMAINS = ("health", "science", "technology", "business", "policy",
           "environment", "society", "other")
CLAIM_TYPES = ("prevalence", "causal", "trend", "comparison", "projection",
               "attribution", "definitional", "recommendation", "opinion")

_SYS = (
 "You name the concepts a factual claim is about so a research corpus can be "
 "searched for it. You never judge whether the claim is true, and you never "
 "state a fact of your own.\n"
 "Return JSON:\n"
 '{"subject": str,        // what the claim is about, 1-5 words\n'
 ' "domain": one of ' + "|".join(DOMAINS) + ',\n'
 ' "claim_type": one of ' + "|".join(CLAIM_TYPES) + ',\n'
 ' "assertion": "strong"|"hedged"|"neutral",\n'
 ' "subject_phrases": [str],   // the thing acted on/measured — 2-5 phrases\n'
 ' "outcome_phrases": [str],   // the effect, property or outcome asserted — '
 '0-5 phrases, [] if the claim asserts no outcome\n'
 ' "entities": [str],          // named orgs, products, people, datasets\n'
 ' "geo": str|null,            // country or region the claim is scoped to\n'
 ' "period": str|null,\n'
 ' "components": [str]}        // separable sub-assertions, 2-5\n'
 "\nTHE TWO POLES decide whether the search finds the claim or its whole field.\n"
 "* 'Coffee improves cardiovascular health' -> subject_phrases: coffee "
 "consumption, caffeine intake | subject_terms: coffee, caffeine | "
 "outcome_phrases: cardiovascular disease risk, coronary heart disease | "
 "outcome_terms: cardiovascular, heart disease, blood pressure.\n"
 "* 'Vitamin D deficiency is common worldwide' -> subject_phrases: vitamin d "
 "deficiency, hypovitaminosis d | subject_terms: vitamin d | outcome: [] "
 "(a prevalence claim asserts no effect).\n"
 "* 'AI will replace many accounting jobs' -> subject_phrases: accounting "
 "automation, artificial intelligence in accounting | subject_terms: "
 "accounting, bookkeeping | outcome_phrases: employment displacement, labour "
 "market displacement | outcome_terms: employment, automation of work.\n"
 "\nTERMS are matched against curated topic labels ('Coffee research and "
 "impacts', 'Heart rate and cardiovascular health'), so a broad word is right "
 "there. PHRASES are matched against titles, where a broad word is wrong.\n"
 "\nPHRASE RULES:\n"
 "* Multi-word only. A single word names a subject area, not a claim.\n"
 "* Use terms that appear in the TITLE or keyword list of a real paper: the "
 "standard scientific name, the common name, genuine synonyms.\n"
 "* Never a bare field name ('public health', 'machine learning') unless the "
 "claim is about the field itself. Never a generic ('recent study', 'global "
 "trend', 'urban lifestyle').\n"
 "COMPONENTS: the pieces that could be separately true. 'AI will replace many "
 "accounting jobs' -> ['AI automation of bookkeeping', 'AI automation of tax "
 "preparation', 'decline in accountant employment', 'complete occupational "
 "replacement'].")


GENERIC = set("""consumption intake use usage levels level status effects effect
risk risks health outcomes outcome impact impacts rates rate prevalence
incidence trends trend growth adoption research studies study analysis""".split())


_DASHES = str.maketrans({c: "-" for c in "\u2010\u2011\u2012\u2013\u2014\u2015\u2212\u00ad"})
_DASHES.update(str.maketrans({"\u2018": "'", "\u2019": "'", "\u201c": '"', "\u201d": '"', "\u00a0": " "}))


def _norm(s) -> str:
    """Plain ASCII punctuation. The model writes 'all\u2011cause mortality' and
    'post\u2011acute covid\u201119' with NON-BREAKING hyphens, which match no title
    in the corpus (all-cause mortality: 0 titles instead of thousands) and
    silently delete a whole pole of the claim."""
    return re.sub(r"\s+", " ", str(s or "").translate(_DASHES)).strip()


def _clean_terms(xs) -> list:
    """1-3 word topic terms. Generic heads are dropped: 'consumption' and
    'risk' match half the curated topic labels on the cluster and would turn
    the pole into the whole of medicine."""
    seen, out = set(), []
    for t in xs or []:
        tl = _norm(t).lower()
        if (not tl or tl in seen or len(tl) < 4 or len(tl.split()) > 3
                or tl in GENERIC):
            continue
        seen.add(tl)
        out.append(tl)
    return out[:MAX_SIDE]


def _derive_terms(phrases) -> list:
    """No terms from the model: take each phrase's non-generic head words. Worse
    than the model's, better than matching a title phrase against topic labels
    that never contain it."""
    out = []
    for ph in phrases or []:
        words = [w for w in ph.split() if w not in GENERIC and len(w) > 3]
        if words and words[0] not in out:
            out.append(words[0] if len(words) == 1 else " ".join(words[:2]))
    return out[:MAX_SIDE]


def _clean_side(xs) -> list:
    seen, out = set(), []
    for p in xs or []:
        pl = _norm(p).lower()
        if not pl or pl in seen or (" " not in pl and "-" not in pl):
            continue    # a bare token is what lets ranking drift onto the field
        seen.add(pl)
        out.append(pl)
    return out[:MAX_SIDE]


@progress.stage('scope')
def _spec(claim: str) -> dict | None:
    out = llm.call_json(_SYS, f"CLAIM:\n{claim}", max_tokens=1200)
    if not isinstance(out, dict):
        return None
    out["subject_phrases"] = _clean_side(out.get("subject_phrases"))
    out["outcome_phrases"] = _clean_side(out.get("outcome_phrases"))
    out["subject_terms"] = (_clean_terms(out.get("subject_terms"))
                            or _derive_terms(out["subject_phrases"]))
    out["outcome_terms"] = (_clean_terms(out.get("outcome_terms"))
                            or _derive_terms(out["outcome_phrases"]))
    out["components"] = [str(c).strip() for c in (out.get("components") or [])][:5]
    out["entities"] = [str(c).strip() for c in (out.get("entities") or [])][:8]
    if out.get("domain") not in DOMAINS:
        out["domain"] = "other"
    if out.get("claim_type") not in CLAIM_TYPES:
        out["claim_type"] = "definitional"
    return out


# ═══════════════════════════ vocabulary-first resolution ═════════════════════
VOCAB_MIN_SIM = 0.50     # below this a label is a neighbour, not the thing
VOCAB_K = 4


def disambiguate(poles: dict, health: bool) -> dict:
    """Settle homonyms using the OTHER pole, which is the one signal a single
    pole cannot manufacture.

    Three vocabularies agreed that "herniated disc surgery" was abdominal hernia
    repair and one said `Diskectomy`. Voting across vocabularies cannot break
    that tie — they share one embedding model, so they share its mistakes, and
    the majority was wrong. The corpus can break it: on PubMed, do papers under
    `Diskectomy` mention the outcome pole ("surgical adverse events",
    "postoperative complications")? Do papers under `Incisional Hernia`? Both
    do. But do papers under each ALSO mention the subject's own phrases —
    "herniated disc", "disc surgery"? Only `Diskectomy` does. So the test is:
    keep a label only if rows carrying it ALSO match the pole's own phrases
    somewhere in the text the corpus holds for them. It is the title test
    from before, run the right way round — FROM the label TO the phrase,
    across every row that carries the label, not from a handful of phrase
    titles to the label."""
    out = {}
    for which, pole in poles.items():
        phrases = [p for p in pole.get("phrases", []) if p]
        labels = pole.get("labels") or {}
        if not phrases:
            out[which] = labels
            continue
        cleaned = {}
        for name, ls in labels.items():
            cleaned[name] = _label_phrase_check(name, ls, phrases)
        out[which] = cleaned
    return out


@progress.stage('matching')
def _label_phrase_check(name: str, labels: list, phrases: list) -> list:
    """Of the rows carrying each label, what share mention the phrases?

    A label that is the subject has the phrases on a visible share of its rows
    (Diskectomy → "disc" on most). A homonym has them on almost none
    (Incisional Hernia → "disc" on ~0). Checked on the corpus's own text —
    title for research and PubMed, lede for news. Labels that match no phrase
    anywhere are dropped unless they are the ONLY label (then the phrase is
    what is wrong, and the label is the best signal left)."""
    if not labels:
        return []
    tbl = {"oa_topics": "research_typed", "prism_keywords": "research_typed",
           "mesh": "pubmed", "news_subcats": "news"}[name]
    col = vocab.COLUMN[name]
    arr = f"arrayMap(x -> x.1, {col})" if tbl == "news" else col
    text = "assumeNotNull(text)" if tbl == "news" else "title"
    where = {"news": "datetime >= '2024-01-01'",
             "pubmed": f"pub_year BETWEEN {ch.RESEARCH_LAST_YEAR - 10} AND {ch.RESEARCH_LAST_YEAR}",
             "research_typed": f"publication_year BETWEEN {ch.TYPED_FIRST_YEAR} AND {ch.RESEARCH_LAST_YEAR}"}[tbl]
    # The probe is STEMS, not words. "herniated disc surgery" must count a
    # title saying "disc herniation": the word probe ("herniated") hit 0.4% of
    # the right label's rows and 0.0% of the homonym's — an 18x ratio hidden
    # under every absolute floor. Stems ("herniat", "disc") hit far more of
    # the right rows and leave the ratio intact. Generic words are still
    # dropped, but a phrase reduced to nothing falls back to its own words.
    stems = _stems(phrases)
    probe = ch.prose_match(text, stems) if stems else ch.prose_match(text, phrases)
    sel = ", ".join(
        f"countIf(has({arr}, {ch.sql_str(l)})) AS n{i}, "
        f"countIf(has({arr}, {ch.sql_str(l)}) AND {probe}) AS m{i}"
        for i, l in enumerate(labels))
    try:
        row = ch.chq_one(f"SELECT {sel} FROM {ch.TABLE[tbl]} WHERE {where}", timeout=280)
    except Exception:
        return labels
    if not row:
        return labels
    scored = []
    for i, l in enumerate(labels):
        n, m = int(row[2 * i] or 0), int(row[2 * i + 1] or 0)
        scored.append((l, n, m, (m / n) if n else 0.0))
    # PURELY relative to the best label. Absolute shares are small even for
    # the right label — a MeSH heading sits on thousands of papers and the
    # subject phrase appears in a fraction of their titles. What separates a
    # homonym is that its share is an order of magnitude below the best.
    # RELATIVE to the best, not an absolute floor. Measured: "Spine and
    # Intervertebral Disc Pathology" has the subject words on 16.3% of its
    # 70k papers; "Hernia repair and management" on 0.7% of its 30k. An
    # absolute floor of 4% with a 3-row minimum let the 0.7% through on
    # volume. A homonym is a label whose share is a small FRACTION of the
    # best label's share, whatever the absolute numbers are.
    best_share = max((x[3] for x in scored), default=0.0)
    if best_share <= 0:
        return []
    kept = [(l, share) for l, n, m, share in scored
            if m >= 3 and share >= best_share * RELATIVE_SHARE]
    # Ordered by phrase share, best first. The next guard anchors on the first
    # label it is handed; handed in embedding order it anchored on "Hernia
    # repair" (0.61) and judged the real subject against the homonym.
    kept.sort(key=lambda x: -x[1])
    return [l for l, _ in kept]


_SHORT_STOP = {"with", "from", "into", "that", "this", "then", "than", "what",
               "when", "where", "have", "been", "were", "will", "your", "more",
               "most", "such", "also", "over", "very", "some", "many", "much"}
_GENERIC_WORDS = {"surgery", "surgical", "treatment", "therapy", "disease",
                  "study", "effects", "impact", "analysis", "research", "risk",
                  "complications", "outcomes", "patients", "management", "india",
                  "indian", "urban", "rural", "global", "national", "policy",
                  "through", "their", "about", "after", "before", "during",
                  "between", "children", "adults", "people", "recovery", "time"}


def _stems(phrases: list) -> list:
    """Crude stems of the content words: 'herniated'->'herniat', 'flooding'->
    'flood', 'batteries'->'batter'. Matched as substrings, so a stem must be
    long enough not to fire everywhere — five characters minimum."""
    import re as _re
    out = []
    for p in phrases:
        for w in _re.split(r"[^a-z0-9]+", p.lower()):
            # 4-letter words are kept as whole-word probes (prose_match word-
            # bounds anything <=5 chars). Dropping them lost "disc" — the one
            # word that separates disc herniation from abdominal hernia.
            if len(w) < 4 or w in _GENERIC_WORDS or w in _SHORT_STOP:
                continue
            if len(w) == 4:
                if w not in out:
                    out.append(w)
                continue
            for suf in ("ations", "ation", "ising", "izing", "ities", "ingly",
                        "ness", "ment", "ies", "ing", "ed", "es", "s", "al", "ly"):
                if w.endswith(suf) and len(w) - len(suf) >= 5:
                    w = w[:-len(suf)]
                    break
            if w not in out:
                out.append(w)
    return out[:6]


LABEL_PHRASE_SHARE = 0.02   # (unused floor; kept for callers)
RELATIVE_SHARE = 0.20       # at least this fraction of the best label's share.
                            # Measured: Spine/IVD 11.76% vs Hernia repair 1.26%
                            # (9x) — a homonym. Diskectomy 1.3% vs Diskectomy,
                            # Percutaneous 3.1% (2.4x) — the same subject. The
                            # floor sits between them.


# ── LLM fallback: only where the embedding has nothing to say ────────────────
# Two shapes the vector path cannot handle, and they are the ONLY two the model
# is asked about:
#   1. an acronym or code ("AMR", "CBDC", "NPK") — an embedding of three
#      letters is noise; "AMR" matched `Mesoderm` at 0.50.
#   2. a term every vocabulary returns empty for — either nonsense, or phrased
#      so far from any label that nothing clears the floor.
# The model is asked one narrow question: expand or rephrase this into the
# 2-4 things a corpus label would call it — or say it is not a research
# subject. Its answer is then put back through the SAME vector path. The model
# never names a label directly; it only proposes text for the embedding to
# match. That keeps the guarantee intact: no label reaches a query that the
# corpus did not confirm carries the phrase.
_EXPAND_SYS = (
 'A term could not be matched against a research corpus\'s own subject labels. '
 'Return JSON {"expansions": [str], "is_subject": bool, "why": str}.\n'
 '* If it is an acronym, abbreviation or code, expand it: "AMR" -> '
 '["antimicrobial resistance", "antibiotic resistance"]. Give every plausible '
 'expansion if it is ambiguous ("AMR" is also "adaptive mesh refinement").\n'
 '* If it is a real subject phrased unusually, give 2-4 standard phrasings a '
 'paper title or a news desk would use.\n'
 '* If it is not a subject anyone researches or reports on — a personal '
 'reference, a nonsense string, a private name — set is_subject=false and '
 'return []. Do not invent a subject to be helpful.\n'
 '* Never return a phrase you would not expect to find in a library catalogue.')
ACRONYM = re.compile(r"^[A-Z0-9][A-Z0-9&./-]{1,7}$")


def _llm_expand(term: str) -> dict:
    got = llm.call_json(_EXPAND_SYS, f"TERM: {term}", max_tokens=400)
    if not isinstance(got, dict):
        return {"expansions": [], "is_subject": True, "why": "expander returned nothing"}
    ex = [str(x).strip().lower() for x in (got.get("expansions") or []) if str(x).strip()]
    return {"expansions": ex[:4], "is_subject": bool(got.get("is_subject", True)),
            "why": str(got.get("why") or "")[:160]}


@progress.stage('vocabulary')
def resolve_pole(phrases: list, health: bool, _depth: int = 0) -> dict:
    """Ask the corpora what THEY call this pole, by vector match.

    The step that was missing. Every label column each corpus carries —
    OpenAlex topics, Prism keywords, MeSH headings, news subcategories — is
    embedded once in `vocab`; the pole's phrases are embedded with the same
    model and matched by cosine. What comes back names the column to filter on,
    which is what turns a phrase into a predicate without a guess in the chain.
    `Diskectomy` surfaces at 0.65 for "herniated disc surgery" — the heading
    that three rounds of model-proposed phrasing never produced.

    Collision guard: a label is adopted only if it is ALSO a title neighbour
    of the phrases. Embeddings put "disc herniation" next to "hernia repair"
    (abdominal), which is a different surgery entirely; a label that matches
    the words but never co-occurs with them in a title is a homonym, and the
    title check is what separates the two."""
    phrases = [p for p in (phrases or []) if p]
    if not phrases:
        return {"oa_topics": [], "prism_keywords": [], "mesh": [], "news_subcats": []}
    q = " ; ".join(phrases[:3])
    names = ["oa_topics", "prism_keywords", "news_subcats"] + (["mesh"] if health else [])
    r = vocab.resolve(q, k=VOCAB_K * 2, min_sim=VOCAB_MIN_SIM, vocabs=names)
    out = {}
    for name in names:
        cands = [(m["label"], m["similarity"])
                 for m in (r.get("vocabularies", {}).get(name) or {}).get("matches", [])]
        # ORDER MATTERS. The phrase check (does this label's own corpus mention
        # the phrases?) runs FIRST, on every candidate, because it is the test
        # that actually separates a subject from its homonym. Anchoring on the
        # top-similarity label before that check threw away "Spine and
        # Intervertebral Disc Pathology" (0.54) in favour of "Hernia repair"
        # (0.61) — the homonym had the better embedding score, so it became
        # the anchor and the real subject was judged against it.
        survivors = _label_phrase_check(name, [l for l, _ in cands], phrases)
        sim_of = dict(cands)
        cands = [(l, sim_of[l]) for l in survivors]      # phrase-share order
        out[name] = _cooccur_filter(name, phrases, cands)[:VOCAB_K]
    out["_fallback"] = None
    empty = not any(v for k, v in out.items() if not k.startswith("_"))
    acronym = len(phrases) == 1 and bool(ACRONYM.match(phrases[0].strip()))
    # A result built ONLY on weak matches is as suspect as an empty one:
    # "zxqv flurbington protocol" adopted `zigbee protocol` at 0.525 and
    # "my neighbour's cat" adopted `legal aspects of cat ownership` at 0.56.
    # Nothing cleared the confident band, so the embedding is matching a
    # word, not a subject. Ask whether there is a subject here at all.
    best_sim = max((m["similarity"] for v in r.get("vocabularies", {}).values()
                    for m in v.get("matches", [])), default=0.0)
    weak_only = (not empty) and best_sim < WEAK_ONLY_SIM
    if (empty or acronym or weak_only) and _depth == 0:
        ex = _llm_expand(phrases[0] if len(phrases) == 1 else " ; ".join(phrases[:2]))
        if not ex["is_subject"]:
            return {k: [] for k in names} | {"_fallback": {"kind": "not_a_subject",
                                                           "why": ex["why"]}}
        if weak_only and not ex["expansions"]:
            # a real subject the model could not rephrase: keep the weak
            # matches, but say they are weak
            out["_fallback"] = {"kind": "weak", "best_similarity": round(best_sim, 3),
                                "why": ex["why"]}
            return out
        if ex["expansions"]:
            again = resolve_pole(ex["expansions"], health, _depth=1)
            if any(v for k, v in again.items() if not k.startswith("_")):
                again["_fallback"] = {"kind": "expanded", "from": phrases,
                                      "to": ex["expansions"], "why": ex["why"]}
                return again
    return out


STRONG_SIM = 0.70        # adopt on similarity alone above this
WEAK_ONLY_SIM = 0.60     # best match under this -> ask the model if it is a subject
WEAK_SIM = 0.55          # below this a candidate needs a label-to-label link
ANCHOR_SIM = 0.62        # the best label in a vocabulary becomes the anchor


def _cooccur_filter(name: str, phrases: list, cands: list) -> list:
    """Keep the labels that belong to THIS subject, not to its homonym.

    The first version of this guard had its logic backwards in the one case
    that mattered. It tested whether a candidate label co-occurred with the
    PHRASES on titles — and when the phrases matched no title at all (the
    model-phrased-it-wrong case, which is the case this whole module exists
    for) it fell back to keeping everything. So "herniated disc surgery", 3
    titles, adopted `Incisional Hernia` alongside `Diskectomy`; and `coffea`
    (the plant genus) rode in behind `Coffee`. The guard was strictest where
    the phrases were good and loosest where they were bad.

    The test that actually separates a subject from its homonym is LABEL TO
    LABEL: does this candidate co-occur, in the label column itself, with the
    strongest candidate? `Diskectomy` and `Postoperative Complications` sit on
    the same papers; `Diskectomy` and `Incisional Hernia` almost never do. That
    needs no title phrase at all, so it works exactly where the old test gave
    up. Three tiers:

      sim >= STRONG_SIM     adopted outright — the embedding is not ambiguous
                            up here ("adhd medications" 0.874 was being dropped
                            by the old 8%-of-titles floor)
      WEAK_SIM .. STRONG    adopted if it shares >= 5% of the anchor's rows
      < WEAK_SIM            dropped
    """
    if not cands:
        return []
    strong = [l for l, sim in cands if sim >= STRONG_SIM]
    # The anchor is the first candidate handed in — which, after the phrase
    # check, is the label with the best phrase share, not the best embedding
    # score. It is always adopted: it passed the one test that matters.
    anchor = cands[0][0] if cands else None
    if anchor and anchor not in strong:
        strong = [anchor] + strong
    middle = [(l, sim) for l, sim in cands if WEAK_SIM <= sim < STRONG_SIM
              and l not in strong]
    if not anchor or not middle:
        return strong + [l for l, _ in middle] if not anchor else strong
    tbl = {"oa_topics": "research_typed", "prism_keywords": "research_typed",
           "mesh": "pubmed", "news_subcats": "news"}[name]
    col = vocab.COLUMN[name]
    arr = f"arrayMap(x -> x.1, {col})" if tbl == "news" else col
    where = {"news": "datetime >= '2024-01-01'",
             "pubmed": f"pub_year BETWEEN {ch.RESEARCH_LAST_YEAR - 10} AND {ch.RESEARCH_LAST_YEAR}",
             "research_typed": f"publication_year BETWEEN {ch.TYPED_FIRST_YEAR} AND {ch.RESEARCH_LAST_YEAR}"}[tbl]
    sel = ", ".join(f"countIf(has({arr}, {ch.sql_str(l)})) AS c{i}"
                    for i, (l, _) in enumerate(middle))
    try:
        row = ch.chq_one(
            f"SELECT {sel}, count() FROM {ch.TABLE[tbl]} WHERE {where} "
            f"AND has({arr}, {ch.sql_str(anchor)})", timeout=280)
    except Exception:
        return strong
    if not row or int(row[-1] or 0) == 0:
        return strong
    anchor_rows = int(row[-1])
    kept = list(strong)
    for i, (l, sim) in enumerate(middle):
        if int(row[i] or 0) >= max(3, 0.05 * anchor_rows):
            kept.append(l)
    return kept


# ═══════════════════════════ phrase audit ════════════════════════════════════
def audit(phrases: list, terms: list) -> dict:
    """Count every phrase and every term IN ONE SCAN.

    Phrases are counted against titles, terms against the topic array — each
    against the column it will actually be matched on, or the audit would pass
    a phrase that is about to match nothing. Title-only over the 98.6M-row
    typed table is 0.8s for five phrases; the scan is the cost and the
    aggregations are free, so this is one query, never N."""
    phrases = [p for p in phrases if p]
    terms = [t for t in terms if t]
    if not phrases and not terms:
        return {}
    sel = []
    for i, ph in enumerate(phrases):
        sel.append(f"countIf(multiSearchAnyCaseInsensitive(title, {ch.sql_arr([ph])})) "
                   f"AS ph{i}")
    for i, tm in enumerate(terms):
        sel.append(f"countIf(arrayExists(x -> multiSearchAnyCaseInsensitive(x, "
                   f"{ch.sql_arr([tm])}), oa_topics)) AS tm{i}")
    sql = (f"SELECT {', '.join(sel)} FROM {ch.TABLE['research_typed']} "
           f"WHERE publication_year BETWEEN {ch.TYPED_FIRST_YEAR} "
           f"AND {ch.RESEARCH_LAST_YEAR}")
    row = ch.chq_one(sql, timeout=280)
    out = {}
    if not row:
        return {p: None for p in phrases + terms}
    for i, ph in enumerate(phrases):
        out[ph] = int(row[i] or 0)
    # A term derived from a phrase is often the SAME string ('all-cause mortality'
    # is both). Keyed by name alone, the term's topic-label count (0) overwrote
    # the phrase's title count (7,557) and the gate dropped a phrase that
    # matches thousands of titles, deleting the claim's whole outcome pole.
    for i, tm in enumerate(terms):
        out[TERM_KEY + tm] = int(row[len(phrases) + i] or 0)
        out.setdefault(tm, out[TERM_KEY + tm])
    return out


TERM_KEY = "term::"

_REL_STOP = {"and", "the", "of", "in", "on", "for", "with", "health", "effects", "effect", "impacts",
             "impact", "studies", "study", "research", "analysis", "risk", "factors", "outcomes"}


def _lexically_related(labels: list, phrases: list) -> list:
    """Keep the labels that share a content word (prefix of 4+ letters) with
    any of the pole's phrases. An empty phrase list keeps everything."""
    if not phrases:
        return labels
    words = {w[:5] for p in phrases for w in re.findall(r"[a-z0-9.]{3,}", p.lower()) if w not in _REL_STOP}
    keep = []
    for lab in labels:
        lw = {w[:5] for w in re.findall(r"[a-z0-9.]{3,}", lab.lower()) if w not in _REL_STOP}
        if lw & words:
            keep.append(lab)
    return keep


def _gate(names: list, counts: dict, kind: str) -> tuple:
    """Keep what describes the claim; name what does not, and why."""
    def n_of(n):
        if kind == "term" and TERM_KEY + n in counts:
            return counts[TERM_KEY + n]
        return counts.get(n)
    rows = [{"phrase": n, "n": n_of(n), "kind": kind} for n in names]
    live = sorted([r for r in rows if (r["n"] or 0) >= MIN_PHRASE_ROWS],
                  key=lambda r: -(r["n"] or 0))
    dropped = [{**r, "why": ("no paper title contains this phrase" if kind == "phrase"
                             else "no curated topic label contains this term")}
               for r in rows if (r["n"] or 0) < MIN_PHRASE_ROWS]
    if kind == "phrase" and len(live) >= 2 and live[1]["n"] and \
            live[0]["n"] / live[1]["n"] > DOMINANCE:
        dropped.append({**live[0], "why": (
            f"carries {live[0]['n'] / live[1]['n']:.0f}x the next phrase — reads "
            "as a field name rather than this claim")})
        live = live[1:]
    return [r["phrase"] for r in live], dropped


DISCOVER_MAX = 3        # topic labels adopted per pole
DISCOVER_FLOOR = 0.30   # a label must hold this share of the top label's count.
                        # At 0.20 an air-pollution pole also adopted "climate
                        # change and health impacts" — adjacent, not the same
                        # subject, and it multiplied the pole's count by 87.


def discover_terms(phrases: list, limit: int = DISCOVER_MAX) -> list:
    """Ask the corpus what it calls this, instead of guessing.

    The failure this fixes was silent and total. For "air pollution is
    associated with increased cardiovascular risk" the model proposed the topic
    term 'air pollution' — which matches ZERO curated topic labels, because
    OpenAlex files that literature under 'Air Quality and Health Impacts' and
    'Air Quality Monitoring and Forecasting'. The pole lost its label lane, the
    intersection fell to 11 papers, and the claim was reported as
    unestablishable when the corpus holds thousands of papers on it.

    So: match the pole's phrases against TITLES, which is cheap and precise,
    read the topic labels those papers actually carry, and adopt the dominant
    ones. The vocabulary comes from the corpus, it is right by construction in
    any field, and it needs no per-domain configuration.

    The floor matters: without it a coffee query adopts 'Nutritional Studies
    and Diet' and quietly becomes a query about nutrition."""
    phrases = [p for p in phrases if p]
    if not phrases:
        return []
    sql = (f"SELECT t, count() c FROM (SELECT arrayJoin(oa_topics) t FROM "
           f"{ch.TABLE['research_typed']} WHERE publication_year BETWEEN "
           f"{ch.RESEARCH_LAST_YEAR - 8} AND {ch.RESEARCH_LAST_YEAR} AND "
           f"{ch.m_typed({'phrases': phrases, 'terms': []}, arrays=False)} "
           f"AND notEmpty(oa_topics)) GROUP BY t ORDER BY c DESC LIMIT 12")
    try:
        rows = [(r[0], int(r[1])) for r in ch.chq_rows(sql, timeout=280)]
    except Exception:
        return []
    if not rows:
        return []
    top = rows[0][1]
    return [t for t, c in rows[:limit] if c >= top * DISCOVER_FLOOR]


MESH_FURNITURE = {"humans", "male", "female", "adult", "middle aged", "aged",
                  "young adult", "adolescent", "child", "animals", "mice", "rats",
                  "retrospective studies", "prospective studies", "treatment outcome",
                  "follow-up studies", "cohort studies", "risk factors",
                  "time factors", "aged, 80 and over", "united states", "china",
                  "incidence", "prevalence", "surveys and questionnaires"}
# Anatomical-region headings that sit on every paper in a field. `Lumbar
# Vertebrae` is on 1,874 discectomy papers AND on every fusion, fracture and
# stenosis paper — adopting it as a subject heading turned a discectomy query
# into a lumbar-surgery query. Kept as a second-tier heading only when nothing
# more specific exists.
MESH_REGION = {"lumbar vertebrae", "cervical vertebrae", "thoracic vertebrae",
               "spine", "knee joint", "hip joint", "shoulder joint", "brain",
               "heart", "liver", "kidney", "lung", "abdomen", "pelvis"}
MESH_MIN_SHARE = 0.12   # a heading must be on this share of matched papers
MESH_MIN_SEED = 40      # titles the discovery must be computed over to be trusted


def discover_mesh(phrases: list, limit: int = 4) -> list:
    """Ask PubMed what IT calls this, instead of guessing.

    The failure this fixes produced a nine-source article on herniated disc
    surgery in which two sources were about the subject. The model phrased the
    subject "herniated disc surgery" (3 PubMed titles) when the literature says
    "discectomy" (1,935) and "disc herniation"; and the outcome pole matched
    OpenAlex topic labels against MeSH headings — two different vocabularies,
    so that clause could never fire. Meanwhile MeSH had already indexed 1,692
    on-subject papers under `Postoperative Complications`, `Diskectomy` and
    `Reoperation`. The same lesson as `discover_terms`, for the other corpus:
    match the phrases against titles, read the headings those papers carry,
    adopt the dominant ones. Demographic and study-design furniture is dropped
    — "Humans" and "Retrospective Studies" are on every paper."""
    phrases = [p for p in phrases if p]
    if not phrases:
        return []

    def _scan(ph):
        sql = (f"SELECT m, count() c FROM (SELECT arrayJoin(mesh_terms) m FROM "
               f"{ch.TABLE['pubmed']} WHERE pub_year BETWEEN {ch.RESEARCH_LAST_YEAR - 10} "
               f"AND {ch.RESEARCH_LAST_YEAR} AND {ch.prose_match('title', ph)} "
               f"AND notEmpty(mesh_terms)) GROUP BY m ORDER BY c DESC LIMIT 24")
        total = ch.chq_int(
            f"SELECT count() FROM {ch.TABLE['pubmed']} WHERE pub_year BETWEEN "
            f"{ch.RESEARCH_LAST_YEAR - 10} AND {ch.RESEARCH_LAST_YEAR} AND "
            f"{ch.prose_match('title', ph)}", timeout=280)
        return [(r[0], int(r[1])) for r in ch.chq_rows(sql, timeout=280)], total

    try:
        rows, total = _scan(phrases)
    except Exception:
        return []
    # A discovery computed over eight titles is a discovery computed over
    # noise: three case reports of iliac-artery injury during disc surgery made
    # `Iliac Artery` look like a subject heading, and every vascular
    # meta-analysis in PubMed followed it in. Widen the seed — the heading
    # found on the first pass that is clearly the subject, used as a title
    # phrase — and rediscover over a real population.
    if total < MESH_MIN_SEED and rows:
        lead = next((m for m, c in rows if m.lower() not in MESH_FURNITURE
                     and m.lower() not in MESH_REGION), None)
        if lead:
            try:
                seed = [w.lower() for w in re.split(r"[,\s]+", lead) if len(w) > 4][:2]
                rows2, total2 = _scan(phrases + seed)
                if total2 > total:
                    rows, total = rows2, total2
            except Exception:
                pass
    rows = [(m, c) for m, c in rows if m.lower() not in MESH_FURNITURE]
    if not rows:
        return []
    total = total or 1
    specific = [(m, c) for m, c in rows if m.lower() not in MESH_REGION
                and c / total >= MESH_MIN_SHARE]
    region = [(m, c) for m, c in rows if m.lower() in MESH_REGION
              and c / total >= MESH_MIN_SHARE]
    chosen = specific[:limit] or region[:1]
    if not chosen:
        return []
    top = chosen[0][1]
    return [m for m, c in chosen if c >= top * DISCOVER_FLOOR]


# ═══════════════════════════ predicates ══════════════════════════════════════
_MATCHERS = {
    "research_typed": ch.m_typed,
    "research": ch.m_research,
    "pubmed": ch.m_pubmed,
    "arxiv": ch.m_arxiv,
    "news": ch.m_news,
    "patents": ch.m_patents,
    "companies": ch.m_companies,
}


def pole(qo: dict, which: str) -> dict:
    p = (qo.get("poles") or {}).get(which) or {}
    return {"phrases": list(p.get("phrases") or []),
            "terms": list(p.get("terms") or []),
            "mesh": list(p.get("mesh") or [])}


def has_outcome(qo: dict) -> bool:
    o = pole(qo, "outcome")
    return bool(o["phrases"] or o["terms"])


def predicate(qo: dict, corpus: str, mode: str = "count",
              lane: str | None = None) -> str:
    """The WHERE clause for this claim on this corpus.

    LANE. 'intersection' requires BOTH poles and is the default whenever the
    claim has two poles and the intersection is thick enough to characterise.
    'subject' is the recall lane: what a prevalence claim uses, and what a
    two-pole claim falls back to when the intersection cannot support an
    answer. `qo['lane']` records which one produced the numbers in a payload,
    because "papers about coffee and heart disease" and "papers about heart
    disease" are different claims and only one of them is the writer's.

    MODE. 'count' expands both poles across curated label arrays — that is what
    makes a volume real rather than a title-string tally. 'read' anchors the
    SUBJECT pole on the title and still expands the outcome pole, because a
    document worth showing a writer is one that is ABOUT their subject, while
    the outcome only has to be present. Requiring both poles in the title is
    what took a coffee/cardiovascular read down to 13 papers out of 297."""
    m = _MATCHERS.get(corpus, ch.m_research)
    lane = lane or qo.get("lane") or "subject"
    subj, outc = pole(qo, "subject"), pole(qo, "outcome")
    if corpus == "pubmed":
        # PubMed indexes MeSH, not OpenAlex topics. Handing it topic labels was
        # a clause that could never match — which is how the pubmed lanes
        # quietly returned nothing on a subject they hold 1,692 papers on.
        subj = {"phrases": subj["phrases"], "terms": subj["mesh"]}
        outc = {"phrases": outc["phrases"], "terms": outc["mesh"]}
    if mode == "count":
        subj = {"phrases": subj["phrases"][:EXPAND], "terms": subj["terms"][:EXPAND]}
        outc = {"phrases": outc["phrases"][:EXPAND], "terms": outc["terms"][:EXPAND]}
    # Read mode anchors the subject on the TITLE because OpenAlex's label arrays
    # are too loose to read from. MeSH is not loose — it is assigned by
    # indexers, one heading per concept — so on PubMed the subject may use its
    # headings in read mode too. Title-only left 2 readable papers on a subject
    # MeSH had filed 1,692 under `Diskectomy` and `Intervertebral Disc
    # Displacement`.
    subj_sql = m(subj, mode == "count" or (corpus == "pubmed" and bool(subj["terms"])))
    if lane == "intersection" and (outc["phrases"] or outc["terms"]):
        out = f"({subj_sql} AND {m(outc, True)})"
    elif lane == "outcome" and (outc["phrases"] or outc["terms"]):
        out = m(outc, mode == "count")
    elif not (subj["phrases"] or subj["terms"]):
        out = m(outc, mode == "count")
    else:
        out = subj_sql
    g = geo_clause(qo.get("geo"), corpus)
    return f"({out} AND {g})" if g else out


def geo_clause(geo: str | None, corpus: str) -> str:
    """Scope a claim to a place. Measured on 'childhood obesity in India': the
    geo argument was stored on the query object and never applied, so the brief
    reported 168,958 research papers and 267,064 PubMed records (the world's
    obesity literature) with India's share at zero. A paper is about the place
    when its title names it (word prefix, so 'Indian' counts) or its authors'
    institutions are there; a news article when the place it is about is."""
    g = re.sub(r"[^a-z ]", "", (geo or "").lower()).strip()
    if not g:
        return ""
    if corpus == "news":
        return f"(country_pri = '{g}' OR has(country_all, '{g}'))"
    title = f"match(lower(title), '\\b{g}')"
    if corpus in ("research", "research_typed"):
        return f"({title} OR arrayExists(x -> positionCaseInsensitive(x, '{g}') > 0, institution_names))"
    if corpus == "pubmed":
        return f"({title} OR arrayExists(x -> positionCaseInsensitive(x, '{g}') > 0, affiliations))"
    if corpus in ("arxiv", "patents"):
        return title
    return ""


def all_phrases(qo: dict) -> list:
    return pole(qo, "subject")["phrases"] + pole(qo, "outcome")["phrases"]


def read_pole(qo: dict) -> dict:
    """The pole used for READING documents: the subject side, whose phrases are
    what a paper about this claim actually puts in its title."""
    s = pole(qo, "subject")
    return s if s["phrases"] else pole(qo, "outcome")


# ═══════════════════════════ volumes ═════════════════════════════════════════
def _lane_counts(qo: dict) -> dict:
    """How many papers each lane sees. This measurement chooses the lane, so it
    runs before anything reads a document."""
    T = ch.TABLE["research_typed"]
    y = (f"publication_year BETWEEN {ch.TYPED_FIRST_YEAR} "
         f"AND {ch.RESEARCH_LAST_YEAR}")
    subj = predicate(qo, "research_typed", lane="subject")
    if not has_outcome(qo):
        n = ch.chq_int(f"SELECT count() FROM {T} WHERE {y} AND {subj}", timeout=280)
        return {"subject": n, "intersection": None}
    both = predicate(qo, "research_typed", lane="intersection")
    outc = predicate(qo, "research_typed", lane="outcome")
    row = ch.chq_one(f"SELECT countIf({subj}), countIf({outc}), countIf({both}) "
                     f"FROM {T} WHERE {y}", timeout=280)
    if not row:
        return {"subject": 0, "outcome": 0, "intersection": 0}
    return {"subject": int(row[0] or 0), "outcome": int(row[1] or 0),
            "intersection": int(row[2] or 0)}


@progress.stage('corpus_totals')
def _volumes(qo: dict) -> dict:
    """What each corpus holds for this claim, every number labelled with the
    window it was counted over. A research count starting in 2017 and a news
    count starting in 2019 are not comparable, and the payload must not let a
    caller treat them as if they were."""
    T = ch.TABLE

    def q(sql, timeout=280):
        return lambda: ch.chq_int(sql, timeout=timeout)

    r = ch.parallel([
        q(f"SELECT count() FROM {T['research_typed']} WHERE publication_year BETWEEN "
          f"{ch.TYPED_FIRST_YEAR} AND {ch.RESEARCH_LAST_YEAR} AND "
          f"{predicate(qo, 'research_typed')}"),
        q(f"SELECT count() FROM {T['research']} WHERE publication_year BETWEEN 1990 "
          f"AND {ch.RESEARCH_LAST_YEAR} AND "
          f"{predicate(qo, 'research', mode='read')} AND length(abstract) > 400"),
        q(f"SELECT count() FROM {T['pubmed']} WHERE pub_year BETWEEN 1990 AND "
          f"{ch.RESEARCH_LAST_YEAR} AND {predicate(qo, 'pubmed')}"),
        q(f"SELECT count() FROM {T['news']} WHERE datetime >= '2019-01-01' "
          f"AND datetime < '{ch.NEWS_LAST_MONTH}' AND {predicate(qo, 'news')}"),
        q(f"SELECT count() FROM {T['patents']} WHERE publication_year BETWEEN 2005 "
          f"AND {ch.PATENT_LAST_YEAR} AND {predicate(qo, 'patents')}"),
        q(f"SELECT count() FROM {T['arxiv']} WHERE publication_year BETWEEN 2005 "
          f"AND {ch.RESEARCH_LAST_YEAR} AND {predicate(qo, 'arxiv')}"),
    ])
    lane = qo.get("lane")
    return {
        "research": {"n": r[0], "window": f"{ch.TYPED_FIRST_YEAR}-{ch.RESEARCH_LAST_YEAR}",
                     "lane": lane, "what": "Prism-typed research papers"},
        "readable_papers": {"n": r[1], "window": f"1990-{ch.RESEARCH_LAST_YEAR}",
                            "lane": lane,
                            "what": "papers carrying a real abstract, title-anchored"},
        "pubmed": {"n": r[2], "window": f"1990-{ch.RESEARCH_LAST_YEAR}", "lane": lane,
                   "what": "PubMed records — study designs available here"},
        "news": {"n": r[3], "window": f"2019-01-01..{ch.NEWS_LAST_MONTH}", "lane": lane,
                 "what": "news articles mentioning this"},
        "patents": {"n": r[4], "window": f"2005-{ch.PATENT_LAST_YEAR}", "lane": lane,
                    "what": "patents whose title matches"},
        "arxiv": {"n": r[5], "window": f"2005-{ch.RESEARCH_LAST_YEAR}", "lane": lane,
                  "what": "preprints"},
    }


def topics(qo: dict, limit: int = 12) -> list:
    """The corpus's OWN name for this cluster.

    OpenAlex assigns every work a curated topic, so the topics dominating a
    claim's slice are what the field actually calls this. Coverage, gaps and
    radar navigate by these rather than by phrases a model invented — which is
    what makes "what are you missing" answerable from data rather than from
    imagination."""
    sql = (f"SELECT t, count() c FROM (SELECT arrayJoin(oa_topics) t FROM "
           f"{ch.TABLE['research_typed']} WHERE publication_year BETWEEN "
           f"{ch.TYPED_FIRST_YEAR} AND {ch.RESEARCH_LAST_YEAR} AND "
           f"{predicate(qo, 'research_typed')} AND notEmpty(oa_topics)) "
           f"GROUP BY t ORDER BY c DESC LIMIT {limit}")
    try:
        return [{"topic": r[0], "papers": int(r[1])} for r in ch.chq_rows(sql, 280)]
    except Exception:
        return []


# ═══════════════════════════ build ═══════════════════════════════════════════
@cache.singleflight
def build(claim: str, subject_phrases: list | None = None,
          outcome_phrases: list | None = None, subject_terms: list | None = None,
          outcome_terms: list | None = None, domain: str | None = None,
          geo: str | None = None, depth: str = "full",
          refresh: bool = False) -> dict:
    """claim -> a validated query object.

    depth='quick' skips the cross-corpus volume counts and the topic read. It
    is what an editor sidebar calling on every selection should use: it still
    audits every phrase and chooses the lane, which is everything retrieval
    depends on. depth='full' adds the numbers a research card prints.

    Passing phrases overrides the model entirely — a plugin can let the writer
    correct the search terms — and they are audited exactly the same way."""
    claim = _norm(claim)
    if not claim:
        return {"available": False, "reason": "empty claim"}
    ck = cache.key("query.build.v14", claim.lower(), subject_phrases, outcome_phrases,
                   subject_terms, outcome_terms, domain, geo, depth)
    if not refresh:
        hit = cache.get(ck)
        if hit:
            progress.emit('cached')
            return {**hit, "cached": True}

    # A disconnected cluster is not an unresolvable claim. Check before model
    # naming, phrase rescue, or vocabulary expansion can multiply the wait.
    from . import availability
    progress.emit('database')
    availability.require_tables([ch.TABLE['research'], ch.TABLE['research_typed']])
    progress.emit('query')

    spec = {"subject": claim[:60], "domain": domain or "other",
            "claim_type": "definitional", "assertion": "neutral",
            "subject_phrases": [], "outcome_phrases": [], "subject_terms": [],
            "outcome_terms": [], "entities": [], "components": [], "geo": geo,
            "period": None, "source": "caller"}
    if subject_phrases:
        spec["subject_phrases"] = _clean_side(subject_phrases)
        spec["outcome_phrases"] = _clean_side(outcome_phrases)
        spec["subject_terms"] = (_clean_terms(subject_terms)
                                 or _derive_terms(spec["subject_phrases"]))
        spec["outcome_terms"] = (_clean_terms(outcome_terms)
                                 or _derive_terms(spec["outcome_phrases"]))
    else:
        # The naming call fails now and then under load, and the bigram fallback
        # it drops to is much worse: the metformin claim re-captured during a busy
        # hour came back as 'metformin reduces' / 'reduces cancer' with no outcome
        # pole and read kidney and pregnancy papers. Two retries with backoff first.
        got = _spec(claim)
        for wait in (3, 10):
            if got:
                break
            time.sleep(wait)
            got = _spec(claim)
        if got:
            spec.update({k: v for k, v in got.items() if v not in (None, "")})
            spec["source"] = "model"
        else:
            # Degraded but not useless: the sentence's own bigrams still find
            # the obvious papers, and the payload says the naming step did not
            # run, so a caller can retry rather than quietly trust it.
            spec["subject_phrases"] = _fallback_phrases(claim)
            spec["subject_terms"] = _derive_terms(spec["subject_phrases"])
            spec["source"] = "fallback"
    if domain:
        spec["domain"] = domain
    if geo:
        spec["geo"] = geo

    # VOCABULARY FIRST. The corpora's own labels for each pole, by vector
    # match, verified by title co-occurrence. These become the `terms` (topic
    # labels) and `mesh` lists that the predicates filter on; the model's own
    # terms are kept only as a fallback for a pole the vocabulary cannot place.
    health_guess = spec.get("domain") == "health"
    vres = ch.parallel([lambda: resolve_pole(spec["subject_phrases"], health_guess),
                        lambda: resolve_pole(spec["outcome_phrases"], health_guess)],
                       workers=2)
    v_subj, v_out = vres[0] or {}, vres[1] or {}
    # Disambiguate each pole's labels against that pole's OWN phrases, by
    # walking from the label to the rows that carry it. This is where the
    # abdominal-hernia homonym finally dies.
    # (the phrase check now runs inside resolve_pole, on every candidate)
    spec["subject_terms"] = ([t.lower() for t in (v_subj or {}).get("oa_topics", [])]
                             or spec["subject_terms"])
    spec["outcome_terms"] = ([t.lower() for t in (v_out or {}).get("oa_topics", [])]
                             or spec["outcome_terms"])
    spec["_vocab"] = {"subject": v_subj, "outcome": v_out}
    counts = audit(spec["subject_phrases"] + spec["outcome_phrases"],
                   spec["subject_terms"] + spec["outcome_terms"])
    s_ph, d1 = _gate(spec["subject_phrases"], counts, "phrase")
    o_ph, d2 = _gate(spec["outcome_phrases"], counts, "phrase")
    s_tm, d3 = _gate(spec["subject_terms"], counts, "term")
    o_tm, d4 = _gate(spec["outcome_terms"], counts, "term")

    # A pole with no surviving label term has lost half its reach: it can only
    # match titles, and the intersection of two title-only poles is nearly
    # empty. Ask the corpus for its own labels instead. Both poles at once.
    health = spec.get("domain") == "health"
    disc = ch.parallel([
        (lambda: discover_terms(s_ph)) if (s_ph and not s_tm) else (lambda: []),
        (lambda: discover_terms(o_ph)) if (o_ph and not o_tm) else (lambda: []),
        (lambda: discover_mesh(s_ph)) if (health and s_ph) else (lambda: []),
        (lambda: discover_mesh(o_ph)) if (health and o_ph) else (lambda: []),
    ], workers=4)
    s_discovered, o_discovered = [x.lower() for x in (disc[0] or [])], \
        [x.lower() for x in (disc[1] or [])]
    # A discovered label must share a word with the pole it is standing in for.
    # Discovery reads the labels on papers whose TITLES carry the phrase, and for
    # a generic outcome those labels describe the co-occurring subject: papers
    # titled "...all-cause mortality" are mostly diet cohorts, so the outcome of
    # "PM2.5 increases mortality" became 'nutritional studies and diet' and the
    # reading list filled with PM2.5 papers about nutrition. 'air pollution' ->
    # 'air quality and health impacts' still passes on 'air'.
    s_discovered = _lexically_related(s_discovered, s_ph)
    o_discovered = _lexically_related(o_discovered, o_ph)
    s_mesh = list((spec.get("_vocab") or {}).get("subject", {}).get("mesh") or []) \
        or list(disc[2] or [])
    o_mesh = list((spec.get("_vocab") or {}).get("outcome", {}).get("mesh") or []) \
        or list(disc[3] or [])
    # The same check on MeSH headings: 'loss of lean muscle mass' resolved to
    # 'Body Dissatisfaction' by vector similarity.
    s_mesh = _lexically_related(s_mesh, s_ph)
    o_mesh = _lexically_related(o_mesh, o_ph)
    s_tm = s_tm + s_discovered
    o_tm = o_tm + o_discovered

    qo = {
        "claim": claim, "subject": spec.get("subject"), "domain": spec.get("domain"),
        "claim_type": spec.get("claim_type"), "assertion": spec.get("assertion"),
        "geo": spec.get("geo"), "period": spec.get("period"),
        "entities": spec.get("entities") or [],
        "components": spec.get("components") or [],
        "poles": {"subject": {"phrases": s_ph, "terms": s_tm, "mesh": s_mesh},
                  "outcome": {"phrases": o_ph, "terms": o_tm, "mesh": o_mesh}},
        "phrase_source": spec.get("source"),
        "vocabulary": {k: {kk: vv for kk, vv in (v or {}).items() if not kk.startswith("_")}
                       for k, v in (spec.get("_vocab") or {}).items()},
        "fallback": spec.get("_fallbacks"),
        "discovered_terms": {"subject": s_discovered, "outcome": o_discovered,
                             "mesh_subject": s_mesh, "mesh_outcome": o_mesh,
                             "how": ("topic labels (and, on a health claim, MeSH "
                                     "headings) the corpus itself puts on papers "
                                     "whose titles match this pole")},
        "phrase_audit": sorted(
            [{"phrase": k, "n": v} for k, v in counts.items() if not k.startswith(TERM_KEY)],
            key=lambda r: -(r["n"] or 0)),
        "dropped": d1 + d2 + d3 + d4,
        "depth": depth,
    }
    nas = (spec.get("_fallbacks") or {}).get("subject") or {}
    if nas.get("kind") == "not_a_subject":
        out = {**qo, "available": False, "lane": None,
               "reason": f"not a research subject — {nas.get('why')}"}
        cache.put(ck, out, 3600)
        return out
    if not (s_ph or s_tm) and not (o_ph or o_tm):
        # RESCUE. Every proposed phrase missing does not mean the corpus is
        # empty — it usually means the model named the concept in words the
        # literature does not use. Measured live on "waterlogging in delhi":
        # the model offered "urban waterlogging", "rainwater accumulation" and
        # "flood events", all zero, while the corpus holds 2,202 titles under
        # "urban flood" and 1,917 under "waterlogging". Ask for the phrasings a
        # paper title would actually use, audited the same way, before
        # reporting a real subject as unresolvable.
        rescue = _rescue_phrases(spec.get("subject") or claim, claim)
        if rescue:
            r_counts = audit(rescue, [])
            s_ph, r_drop = _gate(rescue, r_counts, "phrase")
            qo["phrase_audit"] = sorted(
                [{"phrase": k, "n": v} for k, v in {**counts, **r_counts}.items() if not k.startswith(TERM_KEY)],
                key=lambda r: -(r["n"] or 0))
            qo["dropped"] = qo["dropped"] + r_drop
            qo["rescued"] = bool(s_ph)
            qo["rescue_note"] = ("the first phrasing matched nothing; these are "
                                 "the words the corpus itself uses for this "
                                 "subject" if s_ph else None)
            if s_ph:
                s_tm = s_tm or []
                qo["poles"] = {"subject": {"phrases": s_ph, "terms": s_tm},
                               "outcome": {"phrases": o_ph, "terms": o_tm}}
    if not (s_ph or s_tm) and not (o_ph or o_tm):
        out = {**qo, "available": False, "lane": None, "reason": (
            "no search phrase for this claim matches the research corpus — it "
            "may be too specific, too recent, or not a research-shaped claim")}
        cache.put(ck, out, 3600)
        return out
    if not (s_ph or s_tm):
        # SUBJECT RESCUE. Only the outcome survived, but the subject usually
        # exists under a plainer name than the one the model proposed. Measured
        # on "Semaglutide causes loss of lean muscle mass": the model offered
        # "semaglutide treatment"/"semaglutide therapy" (0 titles each) while
        # MeSH had already placed the drug and the corpus holds thousands of
        # titles naming "semaglutide" alone. Try the bare names first (the
        # subject, the named entities, the MeSH headings), then the model's
        # title-style rephrasings, audited like every other phrase.
        bare = []
        for x in [spec.get("subject")] + list(spec.get("entities") or []) + list(s_mesh or []):
            x = _norm(x).lower()
            if x and len(x) <= 60 and x not in bare and x not in o_ph:
                bare.append(x)
        cand = bare + [_norm(p).lower() for p in (_rescue_phrases(spec.get("subject") or claim, claim) or [])
                       if _norm(p).lower() not in bare]
        if cand:
            r_counts = audit(cand, [])
            s_ph, r_drop = _gate(cand, r_counts, "phrase")
            qo["phrase_audit"] = sorted(
                [{"phrase": k, "n": v} for k, v in {**counts, **r_counts}.items() if not k.startswith(TERM_KEY)],
                key=lambda r: -(r["n"] or 0))
            qo["dropped"] = qo["dropped"] + r_drop
            if s_ph:
                qo["rescued"] = True
                qo["rescue_note"] = ("the proposed subject phrasing matched no titles; "
                                     "these are the names the corpus itself uses")
                qo["poles"]["subject"] = {"phrases": s_ph, "terms": s_tm, "mesh": s_mesh}
    if not (s_ph or s_tm):          # only the outcome pole survived the audit
        return {**qo, 'available': False, 'lane': None,
                'reason': 'The subject did not resolve. The surviving outcome cannot replace it; supply explicit subject aliases.'}

    # ── choose the lane, then say so ────────────────────────────────────────
    qo["lane"] = "intersection" if has_outcome(qo) else "subject"
    lanes = _lane_counts(qo)
    if qo["lane"] == "intersection" and (lanes.get("intersection") or 0) < MIN_AND:
        qo["lane_note"] = (
            f"only {lanes.get('intersection')} papers cover both sides of this "
            f"claim, so the evidence below is about "
            f"{', '.join(pole(qo, 'subject')['phrases'][:2] or pole(qo, 'subject')['terms'][:2])} "
            f"alone and does not establish the connection the claim asserts")
        qo["lane"] = "subject"
    elif qo["lane"] == "intersection":
        qo["lane_note"] = (
            f"{lanes['intersection']:,} papers cover both sides of the claim, out "
            f"of {lanes['subject']:,} on the subject and {lanes.get('outcome', 0):,} "
            f"on the outcome")
    qo["lane_counts"] = lanes
    qo["available"] = True

    if depth != "quick":
        both = ch.parallel([lambda: _volumes(qo), lambda: topics(qo)], workers=2)
        qo["volumes"] = both[0] or {}
        qo["corpus_topics"] = both[1] or []
    qo["coverage"] = ch.coverage_of(
        ["research_typed"] if depth == "quick"
        else ["research_typed", "research", "pubmed", "news", "patents"])
    if not qo["coverage"]["partial"]:
        if qo.get("phrase_source") != "fallback":   # a degraded build must not stick for 12 hours
            cache.put(ck, qo, TTL)
    return qo


def _rescue_phrases(subject: str, claim: str) -> list:
    """Phrasings the corpus actually uses, when the model's did not land.

    `browse.variants` asks the question differently — "what would a paper TITLE
    say" rather than "what is this claim about" — and audits every candidate
    against titles before returning it. Imported lazily: browse does not import
    query, but keeping the edge out of module load makes the direction of the
    dependency obvious."""
    from . import browse
    seen, out = set(), []
    for seed in (subject, claim):
        if not seed:
            continue
        try:
            got = browse.variants(seed)
        except Exception:
            continue
        for a in got.get("audit") or []:
            p = a["phrase"]
            if (a.get("titles") or 0) >= MIN_PHRASE_ROWS and p not in seen:
                seen.add(p)
                out.append(p)
        if out:
            break
    return out[:MAX_SIDE]


_STOP = set("""a an the of in on for to and or with by from into at as is are was
were be been being it its this that these those has have had will would can could
may might should more most many much very often increasingly particularly about
over under between among across during than then which who whom whose""".split())


def _fallback_phrases(claim: str) -> list:
    """No model: the sentence's own bigrams and trigrams. Crude, and the payload
    says so — but a writer who asked for evidence gets papers back rather than
    an apology."""
    core = [w for w in re.findall(r"[a-z][a-z\-']+", claim.lower())
            if w not in _STOP and len(w) > 2]
    out = []
    for n in (3, 2):
        for i in range(len(core) - n + 1):
            g = " ".join(core[i:i + n])
            if g not in out:
                out.append(g)
    return out[:6]
