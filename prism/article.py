#!/usr/bin/env python3
"""article — reading a whole draft: what it claims, what it cites, what it left out.

The sidebar tools answer one sentence at a time. These answer the piece.

The engineering problem is arithmetic. A 900-word article carries 20-30 factual
claims, and checking each one the way `find_evidence` does — a naming call, a
retrieval, a reading — would be twenty minutes and a hundred model calls. So the
audit is built the other way round:

  ONE model call extracts every claim in the draft AND names each claim's search
  phrases, and ONE ClickHouse scan counts all of them at once, with a countIf
  per claim over a single pass of the typed corpus. Thirty claims cost one scan
  rather than thirty. Only the claims that come back thin or contested are worth
  a deep read, and the caller decides how many of those to pay for.

Citation quality is measured, not estimated: the DOIs already in the draft are
looked up in the corpus and tiered by the same ladder as everything else, so
"your three sources are a news article, a preprint and a review" is a fact about
the draft rather than an impression of it.

What is deliberately NOT here: a score for writing quality, a readability
index, or any judgement of style. Prism knows what the research says. It does
not know how the sentence should sound, and a research tool that starts
grading prose stops being trusted about evidence.
"""
from __future__ import annotations

import re

from . import cache, ch, evidence, llm, query, progress

MAX_CLAIMS = 40
SENT_MIN = 25          # chars; shorter than this is a heading or a fragment
_SENT_SPLIT = re.compile(r"(?<=[.!?])[\s ]+(?=[A-Z0-9“\"'])")
_TAG = re.compile(r"<[^>]+>")
_DOI = re.compile(r"\b10\.\d{4,9}/[-._;()/:a-z0-9]+", re.I)
_URL = re.compile(r"https?://[^\s)\"'<>\]]+", re.I)
_MARKER = re.compile(r"\[\d{1,3}\]|\(\s?\d{1,3}\s?\)|\[\^[^\]]+\]")


def sentences(text: str) -> list:
    """Sentences with their character offsets in the ORIGINAL text, so an editor
    can highlight exactly what was judged. HTML is stripped for reading but the
    offsets stay against what the caller sent."""
    import html
    text = text or ''
    chars, starts, ends = [], [], []
    for token in re.finditer(r'<[^>]+>|&(?:#\d+|#x[0-9a-fA-F]+|\w+);|[^<&]+|[<&]', text):
        raw = token.group()
        decoded = ' ' if raw.startswith('<') and raw.endswith('>') else html.unescape(raw)
        if decoded == raw:
            for i, char in enumerate(raw):
                chars.append(char); starts.append(token.start()+i); ends.append(token.start()+i+1)
        else:
            for char in decoded:
                chars.append(char); starts.append(token.start()); ends.append(token.end())
    plain = ''.join(chars)
    out, pos = [], 0
    for s in _SENT_SPLIT.split(plain):
        s = s.strip()
        if not s:
            continue
        idx = plain.find(s, pos)
        if idx >= 0:
            pos = idx + len(s)
        out.append({"text": s, "start": starts[idx] if idx >= 0 else None,
                    "end": ends[idx+len(s)-1] if idx >= 0 else None})
    return out


# ═══════════════════════════ claim detection ═════════════════════════════════
_CLAIM_SYS = (
 "You mark which sentences of a draft make a factual claim that evidence could "
 "check, and you name what each claim is about so a research corpus can be "
 "searched. You never say whether a claim is true.\n"
 "Return JSON:\n"
 '{"claims": [{"n": int,               // the sentence number given to you\n'
 '  "claim": str,          // the claim as a STANDALONE sentence: resolve "it", '
 '"this", "they" from the surrounding sentences. Add no fact that is not '
 'already in the draft, and no number that is not already in that sentence.\n'
 '  "type": "prevalence"|"causal"|"trend"|"comparison"|"projection"|'
 '"attribution"|"definitional",\n'
 '  "assertion": "strong"|"hedged",  // "proves"/"will" vs "may"/"suggests"\n'
 '  "checkable_by": "research"|"record"|"neither",  // see below; this one '
 'matters most\n'
 '  "subject_phrases": [str],        // 1-3 MULTI-WORD phrases as a paper TITLE '
 'would name the subject ("coffee consumption", "caffeine intake"). Never a single '
 'word, and never verbs, quantities or filler from the sentence ("coffee is", '
 '"drinking three cups a day" are wrong)\n'
 '  "subject_terms": [str],          // 1-2 topic words\n'
 '  "outcome_phrases": [str],        // [] when the claim asserts no outcome\n'
 '  "outcome_terms": [str],\n'
 '  "risk": str}]}         // <=15 words: what could be wrong with it as written\n'
 "\nMARK a sentence only if it asserts something about the world that research, "
 "statistics or records could confirm or refute. Skip opinions, instructions, "
 "questions, transitions and statements about the article itself.\n"
 "\nCHECKABLE_BY decides whether a RESEARCH corpus could ever settle it, and it "
 "matters more than the claim itself:\n"
 "* research — a general pattern, effect, trend or quantity that scholars study: "
 "'tenant turnover raises rental costs', 'rooftop solar reduces delivery losses'.\n"
 "* record — true or false, but only a company filing, a news report or a "
 "register could say: who runs a named charity, what a named app's feature does, "
 "what one firm announced, what happened on one date in one place.\n"
 "* neither — a definition internal to the article, a product description, a "
 "personal experience, or a value judgement.\n"
 "Anything naming a specific private organisation, product, app or person as its "
 "SUBJECT is 'record', not 'research'. A research corpus has no papers about who "
 "the Chief Ninja at a named charity is, and reporting that as unsupported would "
 "be a statement about the corpus, not about the claim.\n"
 "A sentence with a number in it is almost always a claim. A sentence with "
 "'proves', 'the leading cause', 'will reach' is a claim AND a risk.")


@cache.singleflight
@progress.stage('claims')
def extract_claims(text: str, max_claims: int = MAX_CLAIMS) -> dict:
    """Every checkable claim in a draft, with offsets and search phrases.

    The standalone rewrite is gated: it may not introduce a number that is not
    in the source sentence. Without that gate the resolver quietly invents the
    figure the sentence was gesturing at, and every downstream check then runs
    against a claim the writer never made."""
    ck = cache.key('audit.extraction.v3', text, max_claims, _CLAIM_SYS, llm.MODEL, llm.EFFORT)
    hit = cache.get(ck)
    if hit:
        progress.emit('cached')
        return {**hit, 'cached':True}
    sents = [s for s in sentences(text) if len(s["text"]) >= SENT_MIN]
    if not sents:
        return {"available": False, "reason": "no sentences long enough to check",
                "claims": []}
    packed = "\n".join(f"{i+1}. {s['text']}" for i, s in enumerate(sents[:120]))
    out = llm.call_json(_CLAIM_SYS, f"DRAFT SENTENCES:\n{packed}", max_tokens=6000)
    if not out or not isinstance(out.get("claims"), list):
        return {"available": False,
                "reason": "the claim-detection step returned nothing usable",
                "sentences": len(sents), "claims": []}
    claims, rewritten, ungated = [], 0, 0
    for c in out["claims"][:max_claims]:
        try:
            i = int(c.get("n", 0)) - 1
        except (TypeError, ValueError):
            continue
        if not (0 <= i < len(sents)):
            continue
        src = sents[i]
        text_c = str(c.get("claim") or src["text"]).strip()
        extra = llm.numbers_in(text_c) - llm.numbers_in(src["text"])
        if extra:
            text_c = src["text"]      # the resolver added a figure — use the original
            rewritten += 1
        subj_ph, dropped_ph = _clean_phrases(c.get("subject_phrases"))
        out_ph, dropped_out = _clean_phrases(c.get("outcome_phrases"))
        if not subj_ph and out_ph:
            # A single concept ('coffee', 'caffeine') is too broad ALONE, but the
            # audit counts it only together with the outcome, which keeps it on
            # the claim. Restore it rather than leave the claim without a subject.
            back = [d["phrase"] for d in dropped_ph if d.get("why", "").startswith("single word")]
            subj_ph = back[:2]
            dropped_ph = [d for d in dropped_ph if d["phrase"] not in subj_ph]
        ungated += len(dropped_ph) + len(dropped_out)
        kind = str(c.get("checkable_by") or "research").lower()
        if kind not in ("research", "record", "neither"):
            kind = "research"
        claims.append({
            "claim": text_c, "sentence": src["text"], "start": src["start"],
            "end": src["end"], "type": c.get("type"), "assertion": c.get("assertion"),
            "checkable_by": kind,
            "risk": str(c.get("risk") or "")[:120] or None,
            "subject_phrases": subj_ph, "outcome_phrases": out_ph,
            "dropped_phrases": dropped_ph + dropped_out,
            "subject_terms": [str(x).lower() for x in (c.get("subject_terms") or [])],
            "outcome_terms": [str(x).lower() for x in (c.get("outcome_terms") or [])],
        })
    by_kind = {}
    for c in claims:
        by_kind[c["checkable_by"]] = by_kind.get(c["checkable_by"], 0) + 1
    result = {"available": True, "claims": claims, "sentences": len(sents),
            "checkable": len(claims), "by_checkable_by": by_kind,
            "single_word_phrases_dropped": ungated,
            "reverted_rewrites": rewritten,
            "note": ("claims are sentences that assert something checkable; "
                     "offsets are character positions in the text you sent")}
    cache.put(ck, result, 3600)
    return result


# ═══════════════════════════ batch evidence check ════════════════════════════
@progress.stage('database')
def batch_counts(claims: list) -> list:
    """One ClickHouse scan for every claim in the draft.

    Two countIf aggregates per claim — the subject lane and the both-poles lane
    — over a single pass of the typed corpus. Thirty claims cost one scan of
    98.6M rows instead of thirty, which is the difference between an audit that
    runs while the writer waits and one that does not."""
    if not claims:
        return []
    sel, meta = [], []
    for i, c in enumerate(claims):
        qo = {"poles": {"subject": {"phrases": c["subject_phrases"],
                                    "terms": c["subject_terms"]},
                        "outcome": {"phrases": c["outcome_phrases"],
                                    "terms": c["outcome_terms"]}}}
        subj = query.predicate(qo, "research_typed", lane="subject")
        sel.append(f"countIf({subj}) AS s{i}")
        if c["outcome_phrases"] or c["outcome_terms"]:
            both = query.predicate(qo, "research_typed", lane="intersection")
            sel.append(f"countIf({both}) AS b{i}")
            meta.append(True)
        else:
            meta.append(False)
    sql = (f"SELECT {', '.join(sel)} FROM {ch.TABLE['research_typed']} WHERE "
           f"publication_year BETWEEN {ch.TYPED_FIRST_YEAR} AND {ch.RESEARCH_LAST_YEAR}")
    try:
        row = ch.chq_one(sql, timeout=280)
    except Exception as e:
        return [{"error": f"{type(e).__name__}: {e}"} for _ in claims]
    out, k = [], 0
    for has_outcome in meta:
        subj = int(row[k] or 0)
        k += 1
        both = None
        if has_outcome:
            both = int(row[k] or 0)
            k += 1
        out.append({"subject_papers": subj, "both_poles_papers": both})
    return out


GENERIC_HEAD = set("""users user people customers clients tenants landlords
turnover revenue costs cost sessions courses parents children reports media
companies business businesses services products features tools apps platforms
data results growth quality performance experience time money value market
markets industry teams staff members providers area areas thing things""".split())


_PAD = set("""is are was were be been being also too still just even a an the this that these those
it its has have had does do did can could may might will would should raises raise raised lowers lower
reduces reduce increases increase causes cause prevents prevent cures cure improves improve helps help
drinking eating taking using one two three four five six several many cups cup day daily per week
of for in on to with by from risk risks prevention onset development healthiness""".split())


def _clean_phrases(xs) -> tuple:
    """Multi-word only, and no bare generic head. Same rule `query._clean_side`
    enforces, applied here too because the audit builds its own predicates and
    was bypassing it.

    Measured on 20 random Medium articles before this gate: 35 claims carried a
    single-token phrase, and 'turnover' alone matched 1,001,796 papers. A count
    like that is not evidence about a claim, it is the size of a field."""
    keep, dropped = [], []
    seen = set()
    for x in xs or []:
        p = re.sub(r"\s+", " ", str(x).strip().lower())
        # Sentence padding at the ends ("coffee is", "coffee also", "caffeine
        # raises") is what the multi-word rule pushed the model into, and those
        # strings match almost no titles: the coffee audit reported
        # no_literature on heart disease and blood pressure. Strip it, and a
        # single concept that is left becomes '<concept> consumption'-style
        # only if the model offered nothing better (handled by the gate below).
        words = p.split()
        while words and words[-1] in _PAD:
            words.pop()
        while words and words[0] in _PAD:
            words.pop(0)
        p = " ".join(words)
        if not p or p in seen:
            continue
        seen.add(p)
        if " " not in p and "-" not in p:
            dropped.append({"phrase": p, "why": "single word — matches a field, "
                                                "not this claim"})
        elif p in GENERIC_HEAD:
            dropped.append({"phrase": p, "why": "generic noun"})
        else:
            keep.append(p)
    return keep, dropped


# What the audit can actually conclude at this depth, named honestly. The old
# vocabulary said "supported"/"unsupported", and on real articles both were
# wrong in the same direction: a claim about who runs a named charity came back
# "supported by 168,826 papers" because its phrases collided with a field, and
# a product-feature sentence came back "unsupported", which reads as "false"
# when the truth is that no research corpus was ever going to settle it.
STATUS_ORDER = ["not_research", "no_literature", "thin_literature",
                "literature_exists", "claim_covered", "unchecked"]
# THIS IS A SCREEN, NOT A VERDICT, and the wording has to keep saying so.
# The screen matches a claim's OWN WORDING against paper titles in one scan for
# the whole article. `research.evidence` resolves the same claim properly —
# naming its concepts, discovering the corpus's own labels for them, reading
# abstracts — and the two legitimately disagree. Measured live on "rooftop
# solar eliminates delivery losses": the screen finds 2 papers matching that
# wording, the deep read finds 9,216 under "photovoltaic system optimization"
# and "smart grid energy management". The screen is not wrong; it answers a
# narrower question, cheaply, so the deep read can be spent where it matters.
STATUS_MEANS = {
    "not_research": ("only a record — a filing, a register or a news report — "
                     "could settle this. Prism's research corpus has no opinion, "
                     "and that is not the same as the claim being wrong"),
    "no_literature": ("no paper title matches this claim's own wording. The "
                      "field may still cover it under different words — run "
                      "research.evidence on the claim to find out"),
    "thin_literature": ("a handful of paper titles match this wording — too few "
                        "to rest an assertion on without reading them"),
    "literature_exists": ("research exists on this subject — which is not the "
                          "same as research agreeing with the claim; "
                          "research.evidence reads it"),
    "claim_covered": ("papers cover BOTH sides of the claim, so the literature "
                      "speaks to it directly"),
    "unchecked": "the corpus lane failed for this claim",
}
GENERIC_FLOOR = 20000    # a one-pole count above this is a field, not a claim


def _status(c: dict, counts: dict) -> tuple:
    """What the corpus can honestly say about this claim, from counts alone.

    The order of these tests is the whole fix. A claim is first asked whether a
    research corpus could EVER settle it; only then is it counted. Counting
    first is what produced "Phionna McInnes is the Chief Ninja at We Too!" —
    supported, 168,826 papers — on a real article: the phrases collided with a
    field and the count was reported as backing.

    And a one-pole count is never called support. It says a literature exists
    on the subject, which is a different sentence from the claim being right.
    """
    if counts.get("error"):
        return "unchecked", "the corpus lane failed for this claim"
    kind = c.get("checkable_by", "research")
    if kind == "neither":
        return "not_research", ("a definition, a product description or a "
                                "judgement — nothing to check against")
    if kind == "record":
        return "not_research", STATUS_MEANS["not_research"]
    if not c.get("subject_phrases") and not c.get("outcome_phrases"):
        return "not_research", ("every search phrase for this claim was a single "
                                "generic word, which matches a field rather than "
                                "the claim")

    subj = counts.get("subject_papers") or 0
    both = counts.get("both_poles_papers")
    if both is not None:
        if both == 0:
            return ("no_literature",
                    f"{subj:,} papers match the subject wording, none that also "
                    f"match the outcome this claim asserts")
        if both < 25:
            return ("thin_literature",
                    f"only {both} papers match both sides of this claim's wording")
        return "claim_covered", f"{both:,} papers cover both sides of this claim"

    # One pole only. A large count here is a subject area, not a claim.
    if subj == 0:
        return "no_literature", "no paper title matches this claim's wording"
    if subj > GENERIC_FLOOR:
        return ("not_research",
                f"the search phrases matched {subj:,} papers — that is the size "
                f"of a field, not evidence about this sentence. The claim is "
                f"probably about something specific a corpus does not index")
    if subj < 25:
        return "thin_literature", f"only {subj} paper titles match this wording"
    return "literature_exists", f"{subj:,} papers match this subject"


# ═══════════════════════════ citations already in the draft ══════════════════
_NEWSY = ("news", "times", "post", "bbc", "cnn", "reuters", "bloomberg", "guardian",
          "forbes", "medium.com", "substack", "blog", "wordpress")
_SCHOLARLY = ("doi.org", "pubmed", "ncbi.nlm.nih", "arxiv", "nature.com",
              "sciencedirect", "springer", "wiley", "bmj", "thelancet", "jamanetwork",
              "cell.com", "plos", "frontiersin", "mdpi", "oup.com", "cambridge.org")
_OFFICIAL = (".gov", ".gov.", "who.int", "worldbank", "oecd", "europa.eu", "un.org",
             "nih.gov", "cdc.gov", "imf.org")


def inspect_citations(text: str) -> dict:
    """What the draft already cites, and how strong those sources are.

    DOIs are looked up in the corpus and tiered by the same ladder as every
    other source, so this is a measurement. Bare URLs can only be classified by
    host, which is a weaker signal and is labelled as such; anything
    unrecognised stays 'unclassified' rather than being guessed into a tier."""
    dois = list(dict.fromkeys(d.rstrip(".,);") for d in _DOI.findall(text or "")))
    urls = [u for u in _URL.findall(text or "") if not _DOI.search(u)]
    markers = len(_MARKER.findall(text or ""))
    resolved = []
    lookup_error = None
    if dois:
        progress.emit('references')
        lst = ch.sql_arr([d.lower() for d in dois[:40]])
        try:
            rows = ch.chq_rows(
                f"SELECT lower(doi), title, publication_year, venue_name, work_type, "
                f"cited_by_count FROM {ch.TABLE['research']} WHERE lower(doi) IN {lst} "
                f"LIMIT 60", timeout=15)
            for r in rows:
                tier = evidence._tier_of("openalex", work_type=r[4] or "", title=r[1] or "")
                resolved.append({"doi": r[0], "title": r[1], "year": int(r[2] or 0) or None,
                                 "venue": r[3], "tier": tier,
                                 "strength": evidence.strength_of(tier),
                                 "cited_by": int(r[5] or 0)})
        except Exception as exc:
            lookup_error = f'{type(exc).__name__}: citation lookup did not complete'
    found = {d["doi"] for d in resolved}
    hosts = []
    for u in urls[:40]:
        h = re.sub(r"^https?://(www\.)?", "", u).split("/")[0].lower()
        kind = ("scholarly" if any(k in h for k in _SCHOLARLY) else
                "official" if any(k in h for k in _OFFICIAL) else
                "news_or_blog" if any(k in h for k in _NEWSY) else "unclassified")
        hosts.append({"host": h, "kind": kind, "url": u})
    tiers = {}
    for d in resolved:
        tiers[d["tier"]] = tiers.get(d["tier"], 0) + 1
    for h in hosts:
        tiers[h["kind"]] = tiers.get(h["kind"], 0) + 1
    return {
        "available": bool(dois or urls or markers),
        "dois": len(dois), "resolved_in_corpus": resolved,
        "unresolved_dois": [d for d in dois if d.lower() not in found],
        "lookup_error": lookup_error,
        "verification_note": "Corpus resolution is not publisher validation or proof of claim support. Unresolved does not mean fabricated.",
        "links": hosts, "inline_markers": markers,
        "by_kind": dict(sorted(tiers.items(), key=lambda kv: -kv[1])),
        "note": ("DOIs are tiered from the corpus; bare links are classified by "
                 "host only, which is weaker evidence about a source's strength"),
    }


# ═══════════════════════════ the audit ═══════════════════════════════════════
def research_audit(text: str, deep: int = 0, max_claims: int = MAX_CLAIMS) -> dict:
    """The whole-draft pass: claims, how well each is backed, what is cited.

    `deep` runs a full evidence read on that many of the weakest claims — the
    ones where knowing what the literature actually found changes what the
    writer should do. Zero by default: the cheap pass already separates "no
    literature exists" from "a literature exists", and that is most of the
    value at a fraction of the time."""
    got = extract_claims(text, max_claims=max_claims)
    if not got.get("available"):
        return {**got, "available": False}
    claims = got["claims"]
    counts = batch_counts(claims)
    rows = []
    for c, n in zip(claims, counts):
        status, why = _status(c, n)
        rows.append({**c, **n, "status": status, "why": why})

    cits = inspect_citations(text)
    tally = {}
    for r in rows:
        tally[r["status"]] = tally.get(r["status"], 0) + 1
    # Coverage is computed over the claims research could ADJUDICATE. Including
    # the ones no corpus was ever going to settle makes an article about a
    # charity's staff look 90% unsupported, which says nothing true about it.
    checkable = sum(v for k, v in tally.items()
                    if k not in ("not_research", "unchecked"))
    _ = STATUS_ORDER
    strong = tally.get("claim_covered", 0)
    exists = tally.get("literature_exists", 0)
    thin = tally.get("thin_literature", 0)
    coverage = (round(100 * (strong + 0.7 * exists + 0.3 * thin) / checkable)
                if checkable else None)
    cited = cits["dois"] + len([l for l in cits["links"]
                                if l["kind"] in ("scholarly", "official")])
    cite_cov = min(100, round(100 * cited / checkable)) if checkable else None

    # Worth a retrieval: a research-shaped claim whose literature is thin or
    # absent. A `not_research` claim is skipped entirely — spending a search on
    # it is how a tool ends up inventing a citation for a product feature.
    weakest = sorted([r for r in rows
                      if r["status"] in ("no_literature", "thin_literature") or
                      (r.get('checkable_by') == 'research' and
                       (r.get('type') == 'causal' or re.search(
                           r'\b(all|every|always|never|proves?|zero|no impacts?)\b',
                           r.get('claim', ''), re.I)))],
                     key=lambda r: (not bool(r.get('risk')), r["status"] != "no_literature",
                                    r.get("both_poles_papers") or
                                    r.get("subject_papers") or 0))
    deep_reads = []
    for r in weakest[:max(0, int(deep))]:
        qo = query.build(r["claim"], subject_phrases=r["subject_phrases"],
                         outcome_phrases=r["outcome_phrases"],
                         subject_terms=r["subject_terms"],
                         outcome_terms=r["outcome_terms"], depth="quick")
        prof = evidence.profile(qo, read=True, limit=12) if qo.get("available") else \
            {"available": False, "reason": qo.get("reason")}
        deep_reads.append({"claim": r["claim"], "status": r["status"],
                           "tally": prof.get("tally"),
                           "corpus_stance": (prof.get("corpus_stance") or {}).get("reading"),
                           "documents": (prof.get("documents") or [])[:6]})

    return {
        "available": True,
        "claims_detected": len(rows),
        "research_checkable": checkable,
        "not_research": tally.get("not_research", 0),
        "by_status": tally,
        "status_means": STATUS_MEANS,
        "by_checkable_by": got.get("by_checkable_by"),
        "single_word_phrases_dropped": got.get("single_word_phrases_dropped"),
        "evidence_coverage": coverage,
        "method": (
            "one model call extracts every claim and one ClickHouse scan counts "
            "them all, so a whole article costs two round trips. Matching is on "
            "the claim's OWN WORDING against paper titles — deliberately literal. "
            "research.evidence resolves a claim properly (naming its concepts, "
            "discovering the corpus's labels for them, reading abstracts) and "
            "will find work this screen misses. Use `deep` to run it here on the "
            "weakest claims."),
        "evidence_coverage_means": (
            "share of the RESEARCH-CHECKABLE claims with a literature behind "
            "them, weighted by how directly it speaks to the claim. Claims only "
            "a record could settle are excluded rather than counted as failures. "
            "It is not a truth score: it says a body of work exists, not that "
            "the work agrees"),
        "citation_coverage": None,
        "citation_presence_ratio": cite_cov,
        "citation_coverage_means": "Not measured. Presence of a DOI or link does not verify a source or its support for a claim.",
        "citations": cits,
        "citation_issues": [{'doi': d, 'status': 'unchecked' if cits.get('lookup_error') else 'not_resolved_in_corpus',
                             'action': 'Verify this reference with the publisher before using it.'}
                            for d in cits.get('unresolved_dois', [])],
        "claims": rows,
        "needs_attention": weakest[:10],
        "deep_reads": deep_reads,
        "coverage": ch.coverage_of(["research_typed", "research"]),
    }


# ═══════════════════════════ what the draft is missing ═══════════════════════
def whats_missing(text: str, subject: str | None = None, limit: int = 12) -> dict:
    """Topics the literature on this subject covers that the draft does not.

    The candidate topics come from the CORPUS — the OpenAlex topics attached to
    papers on this subject, ranked by how much literature each carries — not
    from a model's sense of what an article ought to mention. Presence in the
    draft is then tested in Python by matching the topic's own words against
    the text, so the answer is two measurements and no opinion."""
    subject = (subject or "").strip()
    if not subject:
        head = " ".join((_TAG.sub(" ", text or "")).split()[:120])
        got = llm.call_json(
            "Name the single subject this text is about, as 2-5 words. "
            'Return {"subject": str}.', head, max_tokens=200)
        subject = str((got or {}).get("subject") or "").strip()
    if not subject:
        return {"available": False, "reason": "could not identify a subject"}
    qo = query.build(subject, depth="quick")
    if not qo.get("available"):
        return {"available": False, "reason": qo.get("reason"), "subject": subject}
    tops = query.topics(qo, limit=limit * 3)
    if not tops:
        return {"available": False, "reason": "no topics on this subject",
                "subject": subject}
    body = re.sub(r"[^a-z0-9 ]+", " ", (_TAG.sub(" ", text or "")).lower())
    body_words = set(body.split())
    covered, missing = [], []
    for t in tops:
        words = [w for w in re.sub(r"[^a-z0-9 ]+", " ", t["topic"].lower()).split()
                 if len(w) > 3 and w not in ("and", "with", "from", "their", "other",
                                             "studies", "research", "analysis")]
        if not words:
            continue
        hit = sum(1 for w in words if w in body_words)
        row = {"topic": t["topic"], "papers": t["papers"],
               "matched_words": hit, "of_words": len(words)}
        (covered if hit >= max(1, len(words) // 2) else missing).append(row)
    return {
        "available": True, "subject": subject, "lane": qo.get("lane"),
        "covered": covered[:limit], "missing": missing[:limit],
        "coverage_pct": round(100 * len(covered) / (len(covered) + len(missing)), 1)
        if (covered or missing) else None,
        "how": ("topics are the corpus's own labels on papers about this subject, "
                "ranked by volume; 'covered' means the draft already uses the "
                "topic's words, which is a shallow test and can miss a synonym"),
        "coverage_note": ch.coverage_of(["research_typed"]),
    }
