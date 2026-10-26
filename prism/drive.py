#!/usr/bin/env python3
"""drive — Prism's own analyst, and the public surface that hides how it works.

Two things live here, and keeping them apart is the whole point.

ON-SIDE DRIVE is Prism doing the thinking itself: an Opus-powered planner that
takes a brief ("a 1,500-word feature on X for a business audience"), decides
what to retrieve, retrieves it, decides what the piece is, writes it, checks
it, and returns a finished product. The caller never sees a tool name. This is
what gets metered and billed — one drive, one credit.

CLIENT-SIDE POWER is the other direction: a client's own agent does the
planning and calls Prism for capabilities. That client needs to know WHAT Prism
can do and what shape the answers take. It must not learn HOW: which tables,
which phrase-expansion tricks, which gates, what the retrieval lanes are called,
why the typed corpus starts in 2017. `surface()` is the public contract —
capabilities described by outcome, not by mechanism — and `redact()` strips
every internal field from a payload before it leaves.

The rule that decides what is internal: if a competitor could read it and
shorten their path to building the same thing, it does not leave. Corpus
sizes, table names, lane names, phrase audits, coverage tables, the names of
the gates, timing breakdowns, model names — all internal. The finding, the
sources, the figures, the window the figures cover, and whether the answer is
whole or partial — all public, because those are what make the answer
trustworthy and a client cannot use them without them.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time

from . import (cache, ch, charts, compose, emphasis, evidence, jobs, llm, news,
               query, reader, rotate, writer)

DRIVE_MODEL = os.environ.get("PRISM_DRIVE_MODEL", "claude-opus-5")
DRIVE_EFFORT = os.environ.get("PRISM_DRIVE_EFFORT", "high")


def _log(m):
    print(f"[prism.drive] {m}", file=sys.stderr, flush=True)


# ═══════════════════════════ the public surface ══════════════════════════════
# What a client-side planner is told Prism can do. Outcomes, not mechanisms.
# Nothing here names a table, a corpus size, a lane, a gate or a model.
CAPABILITIES = [
    {"id": "evidence", "does": "Find what research says about a claim — the "
                                "strongest sources, what each found, whether "
                                "they agree — with verified quotes.",
     "input": {"claim": "one sentence asserting something checkable"},
     "returns": "sources with verdict, quote, citation; an overall reading"},
    {"id": "counter", "does": "Find what disagrees with a claim and how mixed "
                               "the evidence is.",
     "input": {"claim": "str"}, "returns": "contradicting and supporting "
                                           "sources; a wording recommendation"},
    {"id": "numbers", "does": "Figures a writer can use, each with the sentence "
                               "and source it came from.",
     "input": {"claim": "str"}, "returns": "figures with provenance; trend series"},
    {"id": "browse", "does": "Browse research on a subject by how it frames its "
                              "findings — promising, cautionary, critical.",
     "input": {"subject": "str", "stance": "optional", "since": "optional year"},
     "returns": "papers with stance labels; the stance mix over time"},
    {"id": "coverage", "does": "How a subject is being covered in the news: "
                                "volume over time, tone, what is rising, who is "
                                "named, where.",
     "input": {"subject": "str", "place": "optional"},
     "returns": "trend, tone against baseline, themes, entities, geography"},
    {"id": "season", "does": "Whether a subject is seasonal and when its "
                              "season is.",
     "input": {"subject": "str", "place": "optional"},
     "returns": "month-of-year profile, peak, trough, concentration"},
    {"id": "events", "does": "The datable incidents inside a subject's "
                              "coverage, ranked by how many outlets ran each.",
     "input": {"subject": "str", "place": "optional"},
     "returns": "dated events with headline, outlet, weight"},
    {"id": "factors", "does": "Causes and consequences the reporting names, "
                               "each verified against its source.",
     "input": {"subject": "str"}, "returns": "causes and impacts with quotes"},
    {"id": "audit", "does": "Check a draft: which claims a research corpus can "
                             "adjudicate, which it backs, which it does not.",
     "input": {"text": "the draft"}, "returns": "per-claim status; coverage score"},
    {"id": "continue", "does": "The next paragraph of a draft plus alternatives, "
                                "each sourced and checked.",
     "input": {"draft": "str"}, "returns": "paragraph options with sources"},
    {"id": "section", "does": "One whole article section, sourced, ready to "
                               "insert.", "input": {"subject": "str", "kind": "str"},
     "returns": "heading, paragraphs, bibliography"},
    {"id": "article", "does": "A complete researched article on a subject, with "
                               "charts, sources and a rotation so two callers "
                               "get different pieces.",
     "input": {"subject": "str", "requester": "your id", "length": "optional"},
     "returns": "title, sections, charts, sources; a job id if long"},
    {"id": "chart", "does": "Data as a hosted chart image, light and dark. "
                             "Pick the card that matches where the piece's "
                             "numbers come from: `stance` (how a whole research "
                             "literature leans) and `verdicts` (what the papers "
                             "read against one claim actually said) for a "
                             "research-led piece; `season`, `events`, `factors`, "
                             "`growth` for a piece led by news coverage. A "
                             "research subject with no news angle has no season "
                             "or events.",
     "input": {"subject+card": "card is one of stance, verdicts, season, "
                               "events, factors, growth — or pass raw points"},
     "returns": "image URL, embed HTML"},
    {"id": "cite", "does": "Citations in APA, Vancouver, Harvard, MLA, Chicago, "
                            "BibTeX, inline, footnote, source card.",
     "input": {"claim": "str", "style": "str"}, "returns": "formatted citations"},
]

# Maps public capability ids to the real tool names. Internal; never returned.
_ROUTE = {
    "evidence": "find_evidence", "counter": "find_counter_evidence",
    "numbers": "find_statistics", "browse": "browse_research",
    "coverage": "prism_overview", "season": "news_seasonality",
    "events": "news_events", "factors": "compose_factors", "audit": "research_audit",
    "continue": "continue_paragraph", "section": "write_section",
    "article": "write_article", "chart": "make_chart", "cite": "get_citations",
}

# What the public payload may carry. Everything else is stripped.
PUBLIC_KEYS = {
    "ok", "feature", "subject", "data", "window", "error",
    # meta fields a client needs to trust an answer
    "partial", "seconds", "written_by",
}
# Inside `data`, these never leave.
INTERNAL_DATA_KEYS = {
    "phrase_audit", "dropped", "poles", "lane", "lane_counts", "lane_note",
    "lane_counts", "corpus_topics", "volumes", "query", "coverage",
    "match_mode", "match_mode_note", "ranked_by", "baseline", "thresholds",
    "how", "method", "fill_rates", "fill_note", "enrichment", "scope_note",
    "scope_match", "term_split", "fallback", "rescued", "rescue_note",
    "phrase_source", "discovered_terms", "vocabulary", "phrases",
    "caveat", "note", "rotation", "plan", "cards_used", "why_news_led",
    "route", "tier_rank", "why_tier", "type_evidence", "reportable_note",
    "writer_note", "fallback_reason", "grounding", "readability", "emphasis",
    "status_means", "by_checkable_by", "single_word_phrases_dropped",
    "evidence_coverage_means", "stance_summary", "inventory_lanes",
    "planned_by", "labelled_by", "windows", "lane_note", "scope_matched",
    "coverage_note", "unresolved_note", "charts_note", "established_note",
    "key_numbers_note", "key_number_candidates", "sections_not_possible",
    "section_plan", "research_strength", "locality",
    # per-source rows: `source` and `id` name the corpus ("openalex:W…",
    # "pubmed:…"); `claimed_quote` is the gate's rejected candidate; `lane`
    # is which retrieval lane found it.
    "source", "id", "claimed_quote", "lane", "confidence", "institutions",
    "abstract", "contribution", "orientation", "stance_score", "topics",
    "mean_stance", "contested_pct", "sides",
}
# Names of the tables, the models, and the internal lanes — scrubbed from any
# string value that survives the key filter.
_SCRUB = re.compile(
    r"\b(?:openalex|marketai|clickhouse|pubmed_articles|works_distributed|"
    r"openalex_prism|news_chunks2|inferences_analysis2|gpt-oss-120b|cerebras|"
    r"claude-[a-z0-9-]+|typed corpus|research_typed|concept[- ]expansion|"
    r"arrayExists|multiSearchAny|prose_match|_distributed)\b", re.I)


def surface() -> dict:
    """The contract a client-side planner builds against."""
    return {
        "service": "Fliar BI · Prism",
        "capabilities": CAPABILITIES,
        "envelope": {"ok": "bool", "feature": "str", "subject": "what was asked",
                     "data": "the answer", "window": "the period every figure "
                     "covers", "partial": "true when the answer is a floor, "
                     "not a total", "error": "kind + reason when ok is false"},
        "guarantees": [
            "every figure states the period it covers",
            "every quote is verbatim from its source and verified",
            "every attribution is rendered from stored author data, never "
            "written by a model; no honorific is ever added",
            "where the corpus has nothing, the answer says so rather than "
            "filling the gap",
            "two callers on the same subject receive different articles; the "
            "same caller receives the same one",
        ],
        "planning": ("call capabilities in any order; `evidence` and `coverage` "
                     "are the usual first calls, `article` is the usual last. "
                     "Use `audit` on your own draft before publishing it."),
    }


def redact(payload, depth: int = 0):
    """Strip everything a client should not learn from a response.

    Applied to every payload that leaves through the client surface. A key
    filter at the top level and inside `data`, then a string scrub for anything
    that names a table, a model or an internal technique in prose. Recursive,
    because the internal vocabulary appears at every depth — a source row
    carries `tier_rank`, a section carries `lanes`."""
    if isinstance(payload, dict):
        out = {}
        for k, v in payload.items():
            if depth == 0 and k == "meta":
                m = v or {}
                cov = (m.get("coverage") or {})
                out["partial"] = bool(cov.get("partial"))
                if "seconds" in m:
                    out["seconds"] = m["seconds"]
                continue
            if k in INTERNAL_DATA_KEYS or k.startswith("_"):
                continue
            out[k] = redact(v, depth + 1)
        return out
    if isinstance(payload, list):
        return [redact(x, depth + 1) for x in payload]
    if isinstance(payload, str):
        return _SCRUB.sub("Prism", payload)
    return payload


# ═══════════════════════════ on-side drive ═══════════════════════════════════
_PLAN_SYS = (
 "You are Prism's research director. A client has sent a brief. Decide what "
 "Prism should retrieve and build to deliver it, using only the capabilities "
 "listed. You are planning the WORK, not writing the piece.\n\n"
 "Return JSON:\n"
 '{"deliverable": "article"|"brief"|"meta_analysis"|"audit"|"answer",\n'
 ' "subject": str,                  // the one subject everything hangs on\n'
 ' "place": str|null,               // geographic scope if the brief has one\n'
 ' "claims": [str],                 // 0-5 checkable claims the brief implies\n'
 ' "steps": [{"capability": str, "args": {}, "why": str}],   // 3-8 in order\n'
 ' "length_words": int,\n'
 ' "audience": str,\n'
 ' "shape": {                        // how the deliverable is BUILT for this reader\n'
 '    "questions": [str],            // 4-7 questions the reader actually has, in '
 'the order they would ask them. These become the section headings.\n'
 '    "format": ["short_answer_first"|"bullets"|"table"|"numbered_steps"|'
 '"callouts"|"prose"],  // devices that suit this audience; a patient wants '
 'bullets and a short answer first, a policy reader wants prose\n'
 '    "reading_level": "general"|"informed"|"expert",\n'
 '    "must_answer": str},           // the one question the brief is really asking\n'
 ' "notes": str}                    // what to watch for, one line\n\n'
 "A meta_analysis deliverable means: several claims or a subject examined across "
 "the research record, what is settled, what is contested, where the gaps are — "
 "not a single article. Plan `evidence` on each claim plus `browse` on the "
 "subject for that.\n"
 "Prefer fewer, better-chosen steps. Do not plan a step whose output you will "
 "not use.\n"
 "The SHAPE matters as much as the steps. A patient asking about surgical "
 "complications wants: how common, which ones, how serious, what raises the "
 "risk, what to watch for afterwards — as bullets and short sections, not "
 "essays. Write `questions` as that reader would phrase them.")


def plan(brief: str, model: str | None = None) -> dict:
    """Opus reads the brief and plans the drive."""
    caps = "\n".join(f"- {c['id']}: {c['does']} input={json.dumps(c['input'])}"
                     for c in CAPABILITIES)
    got = writer.compose(_PLAN_SYS, f"CAPABILITIES:\n{caps}\n\nBRIEF:\n{brief}",
                         max_tokens=2500, model=model or DRIVE_MODEL,
                         effort=DRIVE_EFFORT)
    parsed = llm._parse(got.get("text") or "")
    if not parsed:
        return {"available": False, "reason": "the planner returned nothing usable",
                "planned_by": got.get("model")}
    steps = [s for s in (parsed.get("steps") or []) if s.get("capability") in _ROUTE]
    # The planner sometimes leaves `subject` null when every step carries its
    # own claim. A drive with no subject cannot scope `browse` or `coverage`,
    # so take it from the first step that names one, then from the brief.
    if not parsed.get("subject"):
        for st in steps:
            a = st.get("args") or {}
            cand = a.get("subject") or a.get("topic") or a.get("claim")
            if cand:
                parsed["subject"] = str(cand)[:120]
                break
    if not parsed.get("subject"):
        parsed["subject"] = " ".join(brief.split()[:12])
    return {"available": bool(steps), **parsed, "steps": steps[:8],
            "planned_by": got.get("model"), "fallback": got.get("fallback")}


def _collect_charts(results: list) -> list:
    """Every hosted chart a step produced, deduped by image URL."""
    out, seen = [], set()
    for r in results:
        if r.get("step") != "chart" or not r.get("ok"):
            continue
        data = ((r.get("result") or {}).get("data")) or {}
        url = (((data.get("images") or {}).get("light")) or {}).get("url")
        if not url or url in seen:
            continue
        seen.add(url)
        spec = data.get("spec_used")
        if isinstance(spec, str):
            try:
                import ast as _ast
                spec = _ast.literal_eval(spec)
            except Exception:
                spec = {}
        spec = spec or {}
        out.append({"slug": data.get("slug"), "kind": data.get("kind"),
                    "title": spec.get("title"), "subtitle": spec.get("subtitle"),
                    "source": spec.get("source"), "alt": spec.get("alt"),
                    "markdown": data.get("embed_markdown"),
                    "embed": data.get("embed_html"),
                    "images": data.get("images")})
    return out


def _run_step(step: dict, ctx: dict) -> dict:
    """Execute one planned capability against the real tools."""
    import prism_mcp as P            # late import: prism_mcp imports this module
    cap, args = step["capability"], dict(step.get("args") or {})
    subj = args.pop("subject", None) or args.pop("topic", None) or ctx.get("subject")
    place = args.pop("place", None) or ctx.get("place")
    topic = f"{subj} in {place}" if place and subj and place.lower() not in subj.lower() else subj
    try:
        if cap == "evidence":
            return P.find_evidence(claim=args.get("claim") or subj, limit=12)
        if cap == "counter":
            return P.find_counter_evidence(claim=args.get("claim") or subj)
        if cap == "numbers":
            return P.find_statistics(claim=args.get("claim") or subj)
        if cap == "browse":
            r = P.browse_research(term=topic, orientation=args.get("stance", ""),
                                  since=int(args.get("since") or 0), limit=12)
            if not r.get("ok"):
                # The planner hands browse a claim-shaped phrase ("coffee
                # consumption and cardiovascular risk") and no title contains
                # it. Browse wants a SUBJECT; retry on the head noun phrase.
                head = re.split(r"\s+(?:and|affects?|on|in|versus|vs)\s+",
                                topic, maxsplit=1)[0]
                if head and head != topic:
                    r = P.browse_research(term=head, orientation=args.get("stance", ""),
                                          since=int(args.get("since") or 0),
                                          limit=12, expand=True)
            return r
        if cap == "coverage":
            return P.prism_overview(term=topic)
        if cap == "season":
            term, scope = compose._news_term(topic)
            return {"ok": True, "feature": "news.season",
                    "data": news.seasonality(term, scope=scope)}
        if cap == "events":
            term, scope = compose._news_term(topic)
            return {"ok": True, "feature": "news.events",
                    "data": news.events(term, scope=scope, limit=12)}
        if cap == "factors":
            return {"ok": True, "feature": "compose.factors",
                    "data": compose.factors(topic)}
        if cap == "audit":
            return P.research_audit(text=args.get("text") or ctx.get("draft") or "")
        if cap == "cite":
            return P.get_citations(claim=args.get("claim") or subj,
                                   style=args.get("style", "apa"))
        if cap == "chart":
            # The planner picks a card, but a card can be empty for this
            # subject — a research claim has no news season. Rather than ship
            # a chartless article (which is what happened before this), fall
            # through the other cards until one holds something.
            want = args.get("card") or "stance"
            # A plan with two chart steps means two different pictures. Without
            # this, both fell through to the same first-working card and the
            # second was deduped away — two retrievals, one chart.
            used = ctx.setdefault("_cards_used", [])
            order = ([want] if want not in used else []) + \
                    [c for c in ("stance", "verdicts", "season", "events",
                                 "factors", "growth") if c != want and c not in used]
            last = None
            for card in order:
                r = P.make_chart(topic=topic, card=card,
                                 kind=args.get("kind", "bars"))
                img = (((r or {}).get("data") or {}).get("images") or {})
                if (r or {}).get("ok") and (img.get("light") or {}).get("url"):
                    used.append(card)
                    return r
                last = r
            return last or {"available": False,
                            "reason": "no card holds anything for this subject"}
        if cap == "article":
            return P.write_article(topic=topic, background=False,
                                   requester=ctx.get("requester", ""),
                                   max_sections=int(args.get("sections") or 5))
        if cap == "section":
            return P.write_section(topic=topic, section=args.get("kind", "state_of_evidence"))
        if cap == "continue":
            return P.continue_paragraph(draft=args.get("draft") or ctx.get("draft") or "",
                                        topic=topic)
    except Exception as e:
        return {"ok": False, "feature": cap,
                "error": {"kind": "internal", "reason": f"{type(e).__name__}: {e}"}}
    return {"ok": False, "feature": cap, "error": {"kind": "bad_request",
                                                  "reason": "unknown capability"}}


# ═══════════════════════════ writing for a person ═══════════════════════════
# The first version of this stage handed a model the retrieval results as JSON
# and a list of the reader's questions as headings, and told it to say "the
# retrieved evidence does not answer this" wherever a question went uncovered.
# It did exactly that. The delivered piece opened "On the evidence retrieved
# here, a distributed ledger earns its keep…", said "retrieved" eleven times,
# cited "Wu and colleagues (2023)" to a reader who has never heard of Wu, and a
# cold reader scored it 4/10 and would not have read past the first paragraph.
# Every gate passed. None of them was asking the reader's question.
#
# Three changes. The piece gets a STORY PLAN before a word is written — a hook
# that is a real thing from the material, one thread, an ending. The writer is
# told who it is writing for and forbidden the vocabulary of the machinery.
# And a READER reads the draft cold and sends it back until it reads.

# What the material's step names mean to a writer. The writer must never see
# "counter" or "tally" — it will write them.
_STEP_PLAIN = {
    "browse": "recent studies on the subject",
    "evidence": "studies checked against a specific claim",
    "counter": "studies that disagree with a claim, or qualify it",
    "numbers": "figures with the sentence each one came from",
    "factors": "causes and consequences found in reporting",
    "coverage": "how much has been published and when",
    "season": "when in the year this gets attention",
    "events": "the events that drew the most coverage",
    "chart": "a chart already drawn from the material",
    "cite": "formatted citations",
}

_VOICE = (
 "VOICE. You are a person who has read all of this and is telling a friend "
 "what you found. Plain words. The concrete thing before the general point. "
 "Paragraphs of two to four sentences. Explain every technical term in the "
 "sentence that first uses it, in a short phrase — not in a glossary, not in "
 "a later paragraph. Someone who knows only the word in the title must be "
 "able to follow every sentence.\n\n"
 "NEVER DESCRIBE HOW THIS WAS MADE. There is no 'retrieved', no 'corpus', no "
 "'evidence step', no 'documents examined', no 'lane', no 'tally', no "
 "'framing', no 'the material', no 'the sources do not cover'. You are not "
 "reporting on a search; you are telling the reader about the world. If "
 "something genuinely is not known, say it ONCE, in plain words — 'Nobody has "
 "published a head-to-head test of this' — in the one place the reader would "
 "ask, and never raise it again. A reader must not be able to tell that a "
 "program gathered what you know.\n\n"
 "SOURCES, for this reader. Say what a source IS, not who wrote it: 'a 2023 "
 "study in IEEE Transactions on Intelligent Transportation Systems found…', "
 "'researchers at Queensland University of Technology built…', 'a World Bank "
 "report from 2017 describes…'. Use the venue, the institution and the year "
 "exactly as the material gives them. Never write 'Surname and colleagues "
 "(2023)'. Never make a paper's title the subject of a verb. When a finding's "
 "own words are good, quote them; otherwise say it plainly. One good finding "
 "told well beats five thin ones listed.\n\n"
 "CHARTS. Where the plan places a chart, put its markdown image line on its "
 "own line exactly as given, introduce it with one sentence saying what the "
 "reader is looking at, and do not recite its values afterwards.\n\n"
 "THE LINES THAT CANNOT BE CROSSED. Write no number that is not in the "
 "material — not rounded, not converted, not approximate. Name no person, "
 "place, company or institution that is not in the material. No Dr, Prof, "
 "Mr, Ms. No he/she for a researcher. Where studies disagree, say so in a "
 "sentence. Close with a 'Sources' section listing, as given, every source "
 "you drew on.")

_STORY_SYS = (
 "You are a writer planning a piece for one human reader, from material a "
 "researcher handed you. You are NOT writing yet. You are deciding what the "
 "story is.\n\n"
 "Return JSON:\n"
 "{\n"
 ' "title": str,        // the headline, as a reader would see it — specific, plain, no colon-explainer\n'
 ' "about": str,        // what the piece is about, one sentence a stranger understands\n'
 ' "reader": str,       // who exactly is reading, and what they want from this\n'
 ' "hook": str,         // the OPENING: one concrete thing FROM THE MATERIAL — a real '
 'case, a specific finding, a number with a face on it. Quote or closely paraphrase '
 'it. Not a definition, not a summary, not "in recent years". If the material has '
 'no concrete opening, pick its single most surprising finding.\n'
 ' "thread": str,       // the one argument carried from the hook to the end\n'
 ' "sections": [{"heading": str, "says": str, "uses": [str], "chart": str|null}],  '
 '// 4-6. Headings in plain words — a question only if that is how people talk. '
 '`says`: two or three sentences of what this section tells the reader. `uses`: '
 'which items in the material, by title. `chart`: the slug of a chart that belongs '
 'here, or null.\n'
 ' "unknown": str|null, // the ONE thing the material genuinely does not settle that '
 'the reader would want to know — to be said once, plainly, in the section where they '
 'would ask. null if none matters.\n'
 ' "ending": str,       // what the reader walks away with — a decision, a test, a way '
 'of seeing. One or two sentences.\n'
 ' "terms": [{"term": str, "plain": str}]   // every technical term the piece will '
 'need, with how to say it in the same sentence the first time\n'
 "}\n\n"
 "Keep it tight: `says` is two sentences, `uses` is titles only, no commentary "
 "outside the JSON.\n"
 "THE HOOK AND EVERY `says` LIVE IN THE READER'S WORLD, never in the research "
 "process. Not 'we asked the literature', not 'the studies show a gap', not "
 "'I went looking' — a thing that happened, a finding with a face on it, a "
 "number attached to a real case. The reader must never learn that anyone "
 "searched for anything.\n"
 "The reader's questions (QUESTIONS) are what they want answered — answer them "
 "inside the story; do not make them the headings. The hook must be real and "
 "must be in the material. A story that opens with an abstraction has already "
 "lost this reader.")

_WRITE_SYS = (
 "You are writing the piece a client asked for, for one person: the READER "
 "named in the STORY PLAN. Begin with the plan's `title` as a markdown H1 "
 "line. Follow the plan: open with its hook — the first "
 "sentence is something real, not a definition and not a summary — carry its "
 "thread, use its sections, say its `unknown` once where it puts it, end where "
 "it ends. Use its `terms` the first time each term appears.\n\n" + _VOICE)

_REVISE_SYS = (
 "A reader read your draft cold — no idea who wrote it or how — and reported "
 "what happened to them as they read. Their notes are below, with the "
 "passages quoted. Rewrite the piece so that reader would not have had those "
 "problems. You may cut, reorder, re-open, re-explain and re-attribute freely. "
 "You may NOT add a fact, a number or a name that is not in the MATERIAL. "
 "Keep the charts where they are useful. Do not fix it by making it shorter — "
 "fix it by making it clearer; the length should stay close to the draft's. "
 "If the reader kept reading past the opening, keep the opening. Return the "
 "whole piece, not a diff.\n\n" + _VOICE)

MAX_REVISIONS = 3        # reads = revisions + 1


def _pack_material(results: list) -> str:
    """The retrieval results, redacted and relabelled in plain words."""
    items = []
    for r in results:
        if not r["ok"]:
            continue
        items.append({"what": _STEP_PLAIN.get(r["step"], r["step"]),
                      "material": _strip_stubs(redact(r["result"]))})
    return json.dumps(items, default=str)[:60000]


def _story_plan(brief: str, p: dict, material: str, chart_list: list,
                model: str | None) -> dict:
    shape = p.get("shape") or {}
    charts_txt = json.dumps([{"slug": c.get("slug"), "title": c.get("title"),
                              "shows": c.get("subtitle")} for c in chart_list])
    got = writer.compose(_STORY_SYS,
                         f"BRIEF:\n{brief}\n\nAUDIENCE: {p.get('audience')}\n"
                         f"THE ONE QUESTION: {shape.get('must_answer')}\n"
                         f"QUESTIONS: {json.dumps(shape.get('questions') or [])}\n"
                         f"LENGTH: ~{p.get('length_words')} words\n"
                         f"CHARTS AVAILABLE: {charts_txt}\n\n"
                         f"MATERIAL:\n{material}",
                         max_tokens=6000, model=model or DRIVE_MODEL,
                         effort=DRIVE_EFFORT)
    # A plan cut off mid-sentence by the token cap is not JSON. The first run
    # lost its whole story plan this way — 4,600 characters, no closing brace
    # — and the writer wrote without one. Budget raised; and a plan that still
    # fails to parse is reported rather than silently replaced by nothing.
    plan_ = llm._parse(got.get("text") or "") or {}
    if not plan_.get("hook"):
        _log(f"story plan unusable ({len(got.get('text') or '')} chars, "
             f"keys={list(plan_.keys())[:6]})")
        plan_["_unusable"] = True
    plan_["planned_by"] = got.get("model")
    return plan_


def _write(brief: str, p: dict, story: dict, material: str, chart_list: list,
           model: str | None) -> dict:
    chart_md = "\n".join(f"- {c.get('slug')}: {c.get('markdown')}"
                         for c in chart_list if c.get("markdown"))
    return writer.compose(_WRITE_SYS,
                          f"BRIEF:\n{brief}\n\nLENGTH: ~{p.get('length_words')} words\n\n"
                          f"STORY PLAN:\n{json.dumps(story, indent=1)}\n\n"
                          f"CHART IMAGE LINES (use exactly):\n{chart_md or '(none)'}\n\n"
                          f"MATERIAL:\n{material}",
                          max_tokens=16000, model=model or DRIVE_MODEL,
                          effort=DRIVE_EFFORT)


def _revise(draft: str, notes: str, story: dict, material: str, chart_list: list,
            model: str | None) -> dict:
    chart_md = "\n".join(f"- {c.get('slug')}: {c.get('markdown')}"
                         for c in chart_list if c.get("markdown"))
    return writer.compose(_REVISE_SYS,
                          f"READER'S NOTES:\n{notes}\n\n"
                          f"STORY PLAN (still the plan):\n{json.dumps(story, indent=1)}\n\n"
                          f"CHART IMAGE LINES (use exactly):\n{chart_md or '(none)'}\n\n"
                          f"YOUR DRAFT:\n{draft}\n\n"
                          f"MATERIAL:\n{material}",
                          max_tokens=16000, model=model or DRIVE_MODEL,
                          effort=DRIVE_EFFORT)


def run(brief: str, requester: str = "", draft: str = "", model: str | None = None,
        progress=None) -> dict:
    """The whole drive: plan, execute, synthesise, check.

    What the caller gets back is a deliverable and the sources behind it. What
    they do not get is the plan's internals — they asked Prism to do the
    thinking, and the thinking is the product."""
    t0 = time.time()
    if progress:
        progress(0, 3, "planning")
    p = plan(brief, model=model)
    if not p.get("available"):
        return {"available": False, "reason": p.get("reason"), "brief": brief}
    ctx = {"subject": p.get("subject"), "place": p.get("place"),
           "requester": requester, "draft": draft}

    results = []
    n = len(p["steps"])
    for i, step in enumerate(p["steps"], 1):
        if progress:
            progress(i, n + 2, f"{step['capability']}")
        r = _run_step(step, ctx)
        results.append({"step": step["capability"], "why": step.get("why"),
                        "ok": bool((r or {}).get("ok")),
                        "result": r})

    # An article deliverable IS the article — the composer already did the
    # synthesis, with its gates. Everything else is synthesised here by the
    # drive model from the retrieved results.
    art = next((r["result"] for r in results
                if r["step"] == "article" and r["ok"]), None)
    shape = p.get("shape") or {}
    general = (shape.get("reading_level") or "general") == "general"
    # The article composer's sections ("How attention has moved", "Who is
    # working on this") are the shape of a reported feature. A patient asking
    # about complications does not want to know who is working on it. For a
    # general reader the shaped synthesis answers their questions instead; the
    # composer's article is still kept under `feature` if it ran.
    story, material, chart_list = None, "", []
    if p.get("deliverable") == "article" and art and not general:
        deliverable = art.get("data") or {}
        body_md = deliverable.get("markdown", "")
        synth_by = deliverable.get("written_by")
        sources = deliverable.get("sources") or []
    else:
        if progress:
            progress(n + 1, n + 2, "planning the story")
        material = _pack_material(results)
        chart_list = [c for c in _collect_charts(results) if c]
        story = _story_plan(brief, p, material, chart_list, model)
        if progress:
            progress(n + 1, n + 2, "writing")
        got = _write(brief, p, story, material, chart_list, model)
        body_md = got.get("text") or ""
        synth_by = got.get("model")
        deliverable = None
        sources = _collect_sources(results)

    srcs = [json.dumps(r["result"], default=str) for r in results]
    # Excise first, then ground what is left. A deliverable that ships with a
    # flagged fabrication still in it is a deliverable that ships with a
    # fabrication; the flag is for the editor, the cut is for the reader.
    ex = writer.excise_ungrounded(body_md, srcs)
    g = writer.ground(ex["text"], srcs)

    # THE READER LOOP. Only for pieces the drive wrote itself (the composer's
    # article has its own shape). A cold reader reports what reading it was
    # like; the writer revises against those notes; the grounding gates run
    # again on every revision, because a rewrite can invent as easily as a
    # draft. Stops when the reader is satisfied AND the regex finds no
    # machine-voice, or after MAX_REVISIONS.
    rounds, best = [], None
    if deliverable is None and body_md:
        audience = p.get("audience") or "general reader"
        for rnd in range(MAX_REVISIONS + 1):
            if progress:
                progress(n + 2, n + 2, f"reader round {rnd + 1}")
            lk = reader.leaks(g["text"])
            rep = reader.read(g["text"], audience=audience)
            v = reader.verdict(rep, lk, g)
            rounds.append({"round": rnd + 1, "pass": v["pass"], "why": v["why"],
                           "understood": rep.get("understood"),
                           "kept_reading": rep.get("kept_reading"),
                           "about": rep.get("about"),
                           "machine_voice": lk["process_count"],
                           "academic_attributions": lk["academic_count"],
                           "fix_first": rep.get("fix_first"),
                           "words": len(g["text"].split())})
            # A revision can come back WORSE — one run went 6/10 → 4/10 and
            # the reader stopped after the first paragraph of the rewrite.
            # Deliver the best draft the reader saw, not the last one.
            key = (1 if v["pass"] else 0,
                   0 if lk.get("truncated") else 1,
                   1 if g["grounded"] else 0,
                   1 if rep.get("kept_reading") else 0,
                   int(rep.get("understood") or 0),
                   -lk["process_count"], -lk["academic_count"])
            if best is None or key > best[0]:
                best = (key, ex, g, rnd + 1)
            if v["pass"] or rnd == MAX_REVISIONS:
                break
            notes = reader.feedback_text(rep, lk, g)
            got = _revise(g["text"], notes, story, material, chart_list, model)
            if not (got.get("text") or "").strip():
                break
            ex = writer.excise_ungrounded(got["text"], srcs)
            g = writer.ground(ex["text"], srcs)
        if best is not None:
            _, ex, g, delivered_round = best
            for r in rounds:
                r["delivered"] = (r["round"] == delivered_round)
    if progress:
        progress(n + 2, n + 2, "done")
    return {
        "available": bool(body_md), "brief": brief,
        "publishable": g["grounded"],
        "publishable_note": (None if g["grounded"] else
                             "a figure or name in this deliverable could not be "
                             "traced to the retrieved evidence — see `checks`. "
                             "Do not publish without removing it."),
        "deliverable": p.get("deliverable"), "subject": p.get("subject"),
        "place": p.get("place"), "audience": p.get("audience"),
        "shape": shape,
        "story": (story if deliverable is None else None),
        "reader_rounds": rounds,
        "reads": (rounds[-1] if rounds else None),
        "feature": ((art or {}).get("data") or {}).get("markdown")
        if (art and general) else None,
        "markdown": g["text"], "words": len(g["text"].split()),
        "sources": sources[:40],
        # Charts come from EITHER path: the composer attaches its own when the
        # deliverable is an article, and standalone `chart` steps produce them
        # when the drive synthesises. Reading only the first is why a
        # synthesised piece shipped with every chart rendered, hosted, and
        # then dropped on the floor.
        "charts": ((deliverable or {}).get("charts")
                   or [c for c in (_collect_charts(results)) if c]),
        "checks": {"sentences_removed": ex["removed"],
                   "removed_count": len(ex["removed"]),
                   "invented_figures_remaining": g["ungrounded_numbers"],
                   "unsourced_names": g["unsourced_names"],
                   "honorifics_removed": g["honorifics_removed"],
                   "clean": g["grounded"],
                   "how": ("any sentence carrying a figure that no retrieved "
                           "source holds was removed before delivery; the "
                           "removed sentences are listed so an editor can "
                           "restore one from the actual paper")},
        "steps_run": [{"capability": r["step"], "ok": r["ok"]} for r in results],
        "planned_by": p.get("planned_by"), "written_by": synth_by,
        "seconds": round(time.time() - t0, 1),
        "billing": {"unit": "drive", "steps": len(results),
                    "note": "one drive = one credit; gating is the caller's "
                            "responsibility until billing lands here"},
    }


STUB_CHARS = 200


def _strip_stubs(payload):
    """Remove sources whose abstract is a stub before the writer sees them.

    The failure this prevents happened on the first live drive: a real 2026
    meta-analysis on coffee and heart failure carried a 44-character abstract,
    and Opus — handed the author name, the title, and an empty evidence slot —
    wrote "HR 0.925; 95% CI 0.882–0.971; P = 0.002". Every part of that is
    plausible and every part is fabricated. The number gate caught it, but a
    gate that fires after the fact is the second line of defence. The first is
    not giving the writer a credible name with nothing behind it."""
    if isinstance(payload, dict):
        out = {}
        for k, v in payload.items():
            if k in ("documents", "papers", "sources") and isinstance(v, list):
                v = [d for d in v if not isinstance(d, dict)
                     or len((d.get("quote") or d.get("abstract") or "")) >= STUB_CHARS
                     or d.get("quote")]
            out[k] = _strip_stubs(v)
        return out
    if isinstance(payload, list):
        return [_strip_stubs(x) for x in payload]
    return payload


def _collect_sources(results: list) -> list:
    out, seen = [], set()
    for r in results:
        d = (r.get("result") or {}).get("data") or {}
        for row in (d.get("documents") or d.get("sources") or d.get("papers")
                    or d.get("events") or []):
            if not isinstance(row, dict):
                continue
            key = row.get("doi") or row.get("url") or row.get("title")
            if key and key not in seen:
                seen.add(key)
                out.append({k: row.get(k) for k in
                            ("title", "year", "venue", "url", "doi", "publisher",
                             "date", "attribution", "stance", "tier")
                            if row.get(k) is not None})
    return out
