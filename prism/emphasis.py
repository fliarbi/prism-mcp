#!/usr/bin/env python3
"""emphasis — a separate pass that marks up prose, and cannot change it.

Bold and italic are the difference between a wall of text and a scannable one,
but they are also the easiest place for a second model pass to quietly rewrite
what the first one wrote. So this gate is built around one invariant, checked
on every paragraph:

    STRIP THE MARKUP AND YOU MUST GET THE ORIGINAL TEXT BACK, CHARACTER FOR
    CHARACTER.

If that fails, the markup is discarded and the plain paragraph is returned. The
formatter is therefore incapable of changing a number, softening a claim,
fixing a typo or dropping a caveat — the only thing it can do is decide which
existing words are emphasised. A caller gets `verified: true` or the original
text; never a silent edit.

WHAT GETS MARKED, and why these and not more:
  * bold   — the finding a reader would quote: a figure that carries the point,
             the name of the thing that failed.
  * italic — a term being introduced, a publication name, a phrase used as a
             phrase rather than for its meaning.
  * pull   — one sentence per section worth setting as a pull quote.
Over-marking is the common failure: a paragraph with six bold phrases has
emphasised nothing. The gate enforces a density ceiling as well as the identity
check.
"""
from __future__ import annotations

import re

from . import llm, writer

MAX_BOLD_PER_PARA = 2
MAX_ITALIC_PER_PARA = 2
MIN_WORDS_TO_MARK = 35        # a short paragraph does not need emphasis
MAX_MARKED_WORD_RUN = 9       # bolding a whole clause is shouting

_MD = re.compile(r"\*\*(.+?)\*\*|\*(.+?)\*|__(.+?)__|_(.+?)_", re.S)


def strip(text: str) -> str:
    """Remove markdown emphasis, leaving the words untouched."""
    prev = None
    out = text or ""
    while prev != out:
        prev = out
        out = _MD.sub(lambda m: next(g for g in m.groups() if g is not None), out)
    return out


def _norm(s: str) -> str:
    """Whitespace-insensitive comparison. The formatter is allowed to normalise
    a double space; it is not allowed to change a word."""
    return re.sub(r"\s+", " ", (s or "")).strip()


def verify(original: str, marked: str) -> dict:
    """Is `marked` exactly `original` plus emphasis?"""
    stripped = strip(marked)
    same = _norm(stripped) == _norm(original)
    bold = len(re.findall(r"\*\*(.+?)\*\*", marked or "", re.S))
    ital = len(re.findall(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", marked or "", re.S))
    runs = [len(m.group(1).split()) for m in
            re.finditer(r"\*\*(.+?)\*\*", marked or "", re.S)]
    too_long = [r for r in runs if r > MAX_MARKED_WORD_RUN]
    return {"identical": same, "bold": bold, "italic": ital,
            "over_marked": bold > MAX_BOLD_PER_PARA or ital > MAX_ITALIC_PER_PARA,
            "long_runs": too_long,
            "diff": None if same else _first_diff(_norm(original), _norm(stripped))}


def _first_diff(a: str, b: str) -> str:
    for i, (x, y) in enumerate(zip(a, b)):
        if x != y:
            return f"at char {i}: original {a[max(0,i-25):i+25]!r} vs marked {b[max(0,i-25):i+25]!r}"
    return f"length {len(a)} vs {len(b)}: tail {a[len(b):][:60]!r}" if len(a) > len(b) \
        else f"length {len(a)} vs {len(b)}: added {b[len(a):][:60]!r}"


_SYS = (
 "You add emphasis to prose that is already written and already fact-checked. "
 "You are a typesetter, not an editor.\n\n"
 "ABSOLUTE RULE: return the paragraph with the SAME WORDS in the SAME ORDER. "
 "Add only ** ** and * *. Change nothing else — not a number, not a name, not "
 "a comma, not a tense. Your output is checked by stripping the markup and "
 "comparing it to the input character for character; if it differs, your work "
 "is thrown away.\n\n"
 "WHAT TO MARK:\n"
 f"* **bold** — at most {MAX_BOLD_PER_PARA} per paragraph. The finding a "
 "reader would quote: the figure that carries the point, or the thing that "
 "failed. Bold a PHRASE, never a whole sentence and never more than "
 f"{MAX_MARKED_WORD_RUN} words.\n"
 f"* *italic* — at most {MAX_ITALIC_PER_PARA} per paragraph. A term being "
 "introduced, or a publication name.\n"
 "* Mark nothing at all if nothing in the paragraph stands out. An unmarked "
 "paragraph is a valid answer and better than a decorated one.\n"
 "* Never bold a whole opening clause; never mark two adjacent phrases.\n\n"
 "Return ONLY the marked paragraph. No preamble, no explanation, no quotes "
 "around it.")


FORMATTER_MODEL = None      # None = the configured writer (Sonnet 5)


def mark_paragraph(text: str, model: str | None = None) -> dict:
    """One paragraph, marked up and verified. Falls back to the original."""
    text = (text or "").strip()
    if len(text.split()) < MIN_WORDS_TO_MARK:
        return {"text": text, "marked": False, "verified": True,
                "reason": "too short to need emphasis"}
    # `effort="low"` and a generous budget. Marking up a paragraph is a
    # mechanical task, and at the default medium effort gpt-oss-120b spent the
    # whole 400-token budget on reasoning and returned an empty completion —
    # every paragraph came back "the formatter returned nothing". The work
    # needs tokens for the OUTPUT, not for deliberation.
    budget = max(1200, len(text.split()) * 8)
    got = writer.compose(_SYS, text, max_tokens=budget, temperature=0.0,
                         model=model or None, effort="low")
    raw = got.get("text")
    if not raw:
        return {"text": text, "marked": False, "verified": False,
                "reason": "the formatter returned nothing"}
    raw = raw.strip().strip("`").strip()
    v = verify(text, raw)
    if not v["identical"]:
        return {"text": text, "marked": False, "verified": False,
                "reason": "the formatter changed the words, not just the markup",
                "diff": v["diff"]}
    if v["over_marked"] or v["long_runs"]:
        # Rather than reject, thin it: keep the first allowed marks and unwrap
        # the rest. Over-marking is a judgement failure, not a truth failure.
        raw = _thin(raw)
        v = verify(text, raw)
        if not v["identical"]:
            return {"text": text, "marked": False, "verified": False,
                    "reason": "thinning the markup broke the text"}
    return {"text": raw, "marked": v["bold"] + v["italic"] > 0, "verified": True,
            "bold": v["bold"], "italic": v["italic"]}


def _thin(marked: str) -> str:
    """Keep the first N bold and italic marks; unwrap the rest."""
    def limiter(pattern, limit):
        count = {"n": 0}

        def repl(m):
            count["n"] += 1
            inner = m.group(1)
            if count["n"] > limit or len(inner.split()) > MAX_MARKED_WORD_RUN:
                return inner
            return m.group(0)
        return pattern, repl

    pat, repl = limiter(re.compile(r"\*\*(.+?)\*\*", re.S), MAX_BOLD_PER_PARA)
    out = pat.sub(repl, marked)
    pat, repl = limiter(re.compile(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", re.S),
                        MAX_ITALIC_PER_PARA)
    return pat.sub(repl, out)


def mark_section(paragraphs: list, model: str | None = None) -> dict:
    """A section's paragraphs, marked in parallel, each independently verified.

    One paragraph failing its check does not cost the others their emphasis —
    it just comes back plain."""
    from . import ch
    if not paragraphs:
        return {"paragraphs": [], "marked": 0, "rejected": 0}
    outs = ch.parallel([(lambda p=p: mark_paragraph(p, model)) for p in paragraphs],
                       workers=4)
    kept, rejected, reasons = [], 0, []
    for src, got in zip(paragraphs, outs):
        if not got:
            kept.append(src)
            rejected += 1
            reasons.append("formatter call failed")
            continue
        kept.append(got["text"])
        if not got.get("verified"):
            rejected += 1
            reasons.append(got.get("reason", "unverified"))
    return {"paragraphs": kept,
            "marked": sum(1 for g in outs if g and g.get("marked")),
            "rejected": rejected, "reasons": reasons[:4],
            "guarantee": ("every marked paragraph was verified by stripping the "
                          "markup and comparing it to the original character for "
                          "character; any that differed was returned unmarked")}
