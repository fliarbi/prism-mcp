#!/usr/bin/env python3
"""reader — the gate that asks whether a human can read this.

Every other gate in Prism protects the reader from being LIED to: no number
that is not in a source, no name that is not in a source, no honorific, no
pronoun. None of them protects the reader from being BORED, LOST, or talked at
by a machine describing its own search. A piece passed every gate and opened
with "On the evidence retrieved here, a distributed ledger earns its keep in a
narrow band of problems" — grounded, attributed, unreadable.

Two instruments, kept apart because they catch different things:

  leaks()   — deterministic. A list of phrases that only a pipeline would
              write ("retrieved", "corpus", "the evidence does not answer",
              "counter-evidence step"). A regex cannot be talked out of it.

  read()    — a model, cast as ONE specific human reader taken from the
              brief's audience, reading the draft cold. It reports where it
              got lost, in the draft's own words, and whether it would have
              kept reading past the first paragraph. Its report goes back to
              the writer as feedback, and the writer revises. That loop is
              the feature; the score is just how the loop knows to stop.

The reader never sees the sources. A reader who has the sources judges
fidelity; a reader who does not judges readability, and that is the one
question nobody else in the pipeline is asking.
"""
from __future__ import annotations

import re

from . import llm, writer

import os as _os
READER_MODEL = _os.environ.get("PRISM_READER_MODEL", "claude-sonnet-5")   # not the writer's model: a different reader
                                    # disagrees with the writer more honestly

# ── the deterministic gate ─────────────────────────────────────────────────
# Phrases that describe the machinery. Each one has appeared in a delivered
# piece. A reader who meets them learns that a program wrote this and that
# the program was thinking about its own search, not about the reader.
_LEAK = [
    r"\bretriev(?:ed|al|es|ing)\b",
    r"\bcorpus\b|\bcorpora\b",
    r"\bthe (?:retrieved |available )?(?:evidence|literature|sources?|material|results?) "
    r"(?:do(?:es)? not|did not|cannot|could not) (?:answer|cover|address|support|tell|settle)",
    r"\bcounter-?evidence\b",
    r"\bevidence (?:step|base|set|pool)\b",
    r"\bdocuments? (?:examined|retrieved|returned|read|pulled|were read|we read)\b",
    r"\bread in full\b",
    r"\bclassified as\b",
    r"\b(?:we|a) searched\b|\bsearch(?:ed)? (?:specifically|returned)\b",
    r"\breturned (?:here|no|one|two|three|nothing)\b",
    r"\b(?:positive|negative|mixed|cautionary|promising) framing\b",
    r"\borientation breakdown\b",
    r"\bin (?:the|this) (?:retrieved|present|returned) (?:set|material)\b",
    r"\bthe (?:browse|evidence|numbers|chart|counter|factors) (?:step|card|lane)\b",
    r"\b(?:typed|readable) (?:papers|corpus)\b",
    r"\btally\b",
    r"\bthe (?:RESULTS|SHAPE|BRIEF)\b",
    r"\bthe (?:supplied|provided|available|given|cited|selected) (?:sources?|reading|material|papers|studies|reads)\b",
    r"\bthe reads\b|\b(?:none|one|two|three|six|all) of the reads\b",
    r"\bin this (?:set|batch|sample) of (?:papers|studies|sources)\b",
    r"\bthese (?:papers|studies|sources|reads) (?:cannot|can't|do not|don't) tell (?:us|you)\b",
    r"\bthese reads\b|\b(?:this|the) reading set\b|\bthis set of (?:papers|reads|studies)\b",
    r"\b(?:the|this) (?:material|evidence) (?:gives|provides|contains|offers) no\b",
]
_LEAK_RE = re.compile("|".join(_LEAK), re.I)

# The same gap, said once, is honesty. Said in every section it is a machine
# apologising. Count the distinct sentences that say "nobody knows / not
# covered / does not answer" in any phrasing.
_GAP_RE = re.compile(
    r"\b(?:do(?:es)? not|did not|don't|doesn't|cannot|could not|never|no (?:source|study|paper|evidence)) "
    r"(?:answer|cover|address|document|report|test|measure|compare|settle|tell)"
    r"|\bnot (?:answered|covered|addressed|documented|tested|measured)\b"
    r"|\b(?:is|remains) (?:untested|unanswered|unknown|unmeasured)\b", re.I)

# Academic attribution a general reader cannot use: "Wu and colleagues (2023)".
_ACADEMIC_RE = re.compile(r"\b[A-Z][A-Za-z'’-]+(?: and [A-Z][A-Za-z'’-]+)?"
                          r"(?: and colleagues| et al\.?)? \((?:19|20)\d{2}\)")


def truncated(text: str, require_sources: bool = True) -> str | None:
    """Why the piece looks cut off, or None.

    A revision came back ending "Removing it is what a distributed ledger" —
    no full stop, no Sources section — and the reader said "finish the piece"
    three rounds running while the verdict, which never looked, passed it.
    Two deterministic tests: the piece must carry the Sources section the
    writer is told to close with, and its last line of prose must end like a
    sentence ends."""
    t = (text or "").rstrip()
    if not t:
        return "empty"
    if require_sources and not re.search(r"^#{1,3}\s*Sources\b", t, re.M):
        return "no Sources section — the piece did not reach its end"
    body = re.split(r"^#{1,3}\s*Sources\b", t, flags=re.M)[0].rstrip()
    last = [ln for ln in body.split("\n") if ln.strip()][-1].strip() if body.strip() else ""
    if last and not re.search(r"[.!?\"\u201d)\]*_]$", last) and not last.startswith("!["):
        return f"last sentence is unfinished: \u201c…{last[-60:]}\u201d"
    return None


def leaks(text: str, require_sources: bool = True) -> dict:
    """Every process-phrase, gap-sentence and academic attribution in the text."""
    if not text:
        return {"process": [], "gaps": [], "academic": [], "clean": True,
                "truncated": "empty"}
    # A quoted finding is the source's words, not the writer's. "can reduce
    # the data retrieval pressure" — a study's own sentence — tripped the
    # 'retrieval' pattern and sent a finished piece round the loop three
    # more times. Quoted spans are blanked before the scan.
    unquoted = re.sub(r"[\"\u201c][^\"\u201d]{3,400}[\"\u201d]", '""', text)
    # headings are structure, not sentences: a flagged sentence that began
    # right after a heading took the heading with it when it was excised
    unquoted = re.sub(r"^#{1,6}[^\n]*$", "", unquoted, flags=re.M)
    sents = re.split(r"(?<=[.!?])\s+|\n{2,}", unquoted)
    process = [s.strip()[:160] for s in sents if _LEAK_RE.search(s)]
    gaps = [s.strip()[:160] for s in sents if _GAP_RE.search(s)]
    academic = _ACADEMIC_RE.findall(text)
    cut = truncated(text, require_sources=require_sources)
    return {"process": process, "gaps": gaps, "academic": academic,
            "process_count": len(process), "gap_count": len(gaps),
            "academic_count": len(academic), "truncated": cut,
            "clean": not process and len(gaps) <= 2 and len(academic) <= 2 and not cut}


# ── the human reader ───────────────────────────────────────────────────────
_READER_SYS = (
 "You are a reader, not an editor and not a reviewer. You are going to read a "
 "piece cold, the way a person does: on a phone, with other things to do, "
 "with no idea who wrote it or how. You know nothing about the subject beyond "
 "what an ordinary {audience} would know.\n\n"
 "Read it ONCE, top to bottom, and report what happened to you as you read. "
 "Be specific and quote the piece's own words. Be honest the way a friend is "
 "honest: if you were bored, say where; if you were lost, say at which "
 "sentence; if you stopped, say why.\n\n"
 "Return JSON and nothing else:\n"
 "{{\n"
 ' "about": str,            // what this piece is about, in YOUR words, one sentence. '
 'If you genuinely cannot say, write "I could not tell".\n'
 ' "kept_reading": bool,    // would you have read past the first paragraph?\n'
 ' "why": str,              // one sentence on why / why not\n'
 ' "understood": int,       // 0-10. 10 = I could explain it to someone at dinner. '
 '5 = I got the gist but could not say what it was based on. 2 = words went past me.\n'
 ' "lost_at": [str],        // up to 5 VERBATIM passages (10-25 words each) where you '
 'stopped understanding or stopped caring\n'
 ' "unexplained": [str],    // terms or names used as if you should know them, and you did not\n'
 ' "machine_voice": [str],  // up to 5 VERBATIM passages where it sounds like a program '
 'describing its own search or its own sources rather than a person telling you something\n'
 ' "repeats": [str],        // things it says more than once in different words\n'
 ' "story": {{"opens_with_something_real": bool, "one_thread": bool, "ending": bool, "note": str}},\n'
 ' "fix_first": [str]       // the 3 changes that would have made the biggest difference '
 'to you, concrete, in order\n'
 "}}\n\n"
 "Do not suggest adding facts. Do not comment on whether claims are true; you "
 "cannot know. Your whole job is what it was like to read.")


def read(text: str, audience: str = "general reader", model: str | None = None) -> dict:
    """One human reader's report on the draft. Never sees the sources."""
    sys_ = _READER_SYS.format(audience=audience or "general reader")
    # The first reader ran on the fast open-weight model and died on round
    # three of a long piece — "budget exhausted before any content", the
    # known long-prompt trap. A reader that cannot finish the piece is not a
    # reader. Sonnet reads the whole thing every time.
    res = writer.compose(sys_, f"THE PIECE:\n\n{text}", max_tokens=2500,
                         model=model or READER_MODEL, effort="medium")
    got = llm._parse(res.get("text") or "")
    if not isinstance(got, dict):
        return {"available": False, "reason": "reader returned nothing usable",
                "model": res.get("model")}
    out = {
        "available": True, "model": res.get("model"),
        "about": str(got.get("about") or "")[:300],
        "kept_reading": bool(got.get("kept_reading")),
        "why": str(got.get("why") or "")[:300],
        "understood": int(got.get("understood") or 0),
        "lost_at": [str(x)[:220] for x in (got.get("lost_at") or [])][:5],
        "unexplained": [str(x)[:80] for x in (got.get("unexplained") or [])][:10],
        "machine_voice": [str(x)[:220] for x in (got.get("machine_voice") or [])][:5],
        "repeats": [str(x)[:160] for x in (got.get("repeats") or [])][:5],
        "story": got.get("story") if isinstance(got.get("story"), dict) else {},
        "fix_first": [str(x)[:240] for x in (got.get("fix_first") or [])][:3],
    }
    out["could_not_tell"] = "could not tell" in out["about"].lower()
    return out


PASS_UNDERSTOOD = 7     # reader score at or above which the loop may stop


def verdict(report: dict, leak: dict, ground: dict | None = None) -> dict:
    """Combine the human report with the deterministic scan into one decision.

    The loop stops only when BOTH are satisfied. A charming draft that still
    says "retrieved" fails; a draft with no leaks that a reader could not
    summarise fails."""
    if not report.get("available"):
        # no reader → the regex alone decides, conservatively
        return {"pass": leak["clean"], "why": "reader unavailable; regex only"}
    reasons = []
    if leak.get("truncated"):
        reasons.append(f"cut off: {leak['truncated']}")
    gnum = (ground or {}).get("ungrounded_numbers") or []
    gnam = (ground or {}).get("unsourced_names") or []
    if gnum:
        reasons.append(f"figures not in the material: {', '.join(map(str, gnum[:5]))}")
    if gnam:
        reasons.append(f"names not in the material: {', '.join(map(str, gnam[:5]))}")
    if leak["process"]:
        reasons.append(f"{len(leak['process'])} sentences describe the machinery")
    if leak["gap_count"] > 2:
        reasons.append(f"says what is unknown {leak['gap_count']} times — once is honesty")
    if leak["academic_count"] > 2:
        reasons.append(f"{leak['academic_count']} 'Surname (year)' attributions a general reader cannot use")
    if report["could_not_tell"]:
        reasons.append("the reader could not say what the piece is about")
    if not report["kept_reading"]:
        reasons.append("the reader would not have read past the first paragraph")
    if report["understood"] < PASS_UNDERSTOOD:
        reasons.append(f"understood {report['understood']}/10")
    st = report.get("story") or {}
    if st and not st.get("opens_with_something_real", True):
        reasons.append("opens with an abstraction, not something real")
    return {"pass": not reasons, "why": "; ".join(reasons) or "reader satisfied"}


def feedback_text(report: dict, leak: dict, ground: dict | None = None) -> str:
    """The reader's report, rendered as notes a writer can act on."""
    lines = []
    if leak.get("truncated"):
        lines.append(f"THE PIECE IS CUT OFF ({leak['truncated']}). Deliver the whole "
                     f"piece through to the Sources section.")
    # Grounding failures first: these are the ones that block delivery. The
    # loop once ran four rounds with "85" flagged every time and never told
    # the writer — the heading said "85 percent", the source said 85.1%.
    for x in (ground or {}).get("ungrounded_numbers") or []:
        lines.append(f"FIGURE NOT IN THE MATERIAL: {x} — use the exact figure the "
                     f"material gives, or no figure. Do not round.")
    for x in (ground or {}).get("unsourced_names") or []:
        lines.append(f"NAME NOT IN THE MATERIAL: {x} — remove it.")
    if report.get("available"):
        lines.append(f"READER ({report['understood']}/10, "
                     f"{'kept reading' if report['kept_reading'] else 'STOPPED after the first paragraph'}): "
                     f"{report['why']}")
        lines.append(f"What they think it is about: \"{report['about']}\"")
        for x in report.get("fix_first") or []:
            lines.append(f"FIX FIRST: {x}")
        for x in report.get("lost_at") or []:
            lines.append(f"LOST HERE: \"{x}\"")
        for x in report.get("machine_voice") or []:
            lines.append(f"SOUNDS LIKE A MACHINE: \"{x}\"")
        if report.get("unexplained"):
            lines.append("NEVER EXPLAINED: " + ", ".join(report["unexplained"]))
        if report.get("repeats"):
            lines.append("REPEATED: " + " | ".join(report["repeats"]))
        st = report.get("story") or {}
        if st.get("note"):
            lines.append(f"STORY: {st['note']}")
    for s in (leak.get("process") or [])[:8]:
        lines.append(f"PROCESS PHRASE (must go): \"{s}\"")
    if leak.get("gap_count", 0) > 2:
        lines.append(f"GAP SAID {leak['gap_count']} TIMES — say it once, where it matters, then move on.")
    if leak.get("academic_count", 0) > 2:
        lines.append("ACADEMIC ATTRIBUTION: " + ", ".join(leak["academic"][:6])
                     + " — say what the source IS (a 2023 study in <journal>; researchers at "
                       "<institution>; a World Bank report), not who.")
    return "\n".join(lines)
