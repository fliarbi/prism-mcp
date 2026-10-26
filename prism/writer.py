#!/usr/bin/env python3
"""writer — the composition leg: a model that WRITES, under the same gates.

Everything else in this server retrieves and measures. This module is the one
place a model produces prose a person will publish, so the gates are tighter
here, not looser:

  * Every factual sentence must trace to a supplied source. `ground()` checks
    each paragraph's numbers against the material it was given and reports the
    ones that are not there; the caller drops or flags them.
  * Attribution is built from OUR author arrays, never written by the model.
    `attribution()` renders "Dhawan and colleagues (2021)" from the stored
    names — the model is handed that string and told to use it verbatim.
  * NO HONORIFICS, EVER. "the study by Dr. Dhawan" is the form people ask for
    and it is a fabrication: an author array says whether someone wrote a
    paper, never whether they hold a doctorate, a chair or a clinical title.
    Guessing puts an invented credential in print under a real person's name.
    `_HONORIFIC` strips any the model reaches for and the payload says it did.

PROVIDER. The writer is configured to prefer Claude Opus, which is the right
model for long-context composition over forty abstracts. The Anthropic key at
news/providers/ai/claude has returned "credit balance is too low" since
2026-08-04, so today every call lands on Cerebras gpt-oss-120b and the payload
names which model actually wrote — a reader should never have to guess. Add
credit and it switches with no code change; set PRISM_WRITER_MODEL to pin one.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import threading

from . import llm, progress

# Benchmarked 2026-08-23 on identical retrieved material, 8 sections per model
# (trials/writer_bench.py). Sonnet 5 is the default because it was the only
# candidate clean on BOTH runs: Haiku invented a year (1936) and a claim the
# source never made ("heaviest rainfall"), Opus 5 inferred "since before
# Independence" from outside the corpus. Sonnet also writes tightest (277-word
# median vs 452) and fastest of the Claude models (13.3s/section vs 24.0).
# Opus 5 costs 3.4x Sonnet here for no measured gain on this task.
WRITER_MODEL = os.environ.get("PRISM_WRITER_MODEL", "claude-sonnet-5")
FALLBACK_NOTE = ("composed by the fallback writer — the preferred model "
                 "(%s) was unavailable" % WRITER_MODEL)
LAST = {"model": None, "seconds": None, "fallback_reason": None}
_PROVIDER_FAILURES = {}
_PROVIDER_LOCK = threading.Lock()
PROVIDER_FAILURE_TTL = 60


def _provider_block(model):
    with _PROVIDER_LOCK:
        hit = _PROVIDER_FAILURES.get(model)
        return hit[0] if hit and time.monotonic() < hit[1] else None


def _provider_failed(model, exc, reason):
    if 'credit balance' in str(exc).lower() or getattr(exc, 'status_code', None) in (401,403):
        with _PROVIDER_LOCK:
            _PROVIDER_FAILURES[model] = (reason, time.monotonic() + PROVIDER_FAILURE_TTL)

# Honorifics and post-nominals a model reaches for when asked to attribute a
# study to a person. Every one of them is a claim about a real named human that
# no corpus here can support.
_HONORIFIC = re.compile(
    r"\b(?:Dr|Prof|Professor|Mr|Mrs|Ms|Miss|Sir|Madam|Dame|Lord|Rev|Hon)\b\.?\s*",
    re.I)
_POSTNOM = re.compile(r",?\s*\b(?:PhD|Ph\.D\.?|MD|M\.D\.?|DPhil|ScD|MSc|MBBS)\b\.?",
                      re.I)
# Pronouns: an author array gives a surname, never a gender. A sentence that
# says "his study" about a real researcher can be wrong about a real person in
# a way the neutral form never is.
_PRONOUN = re.compile(r"\b(?:he|she|his|her|hers|him|himself|herself)\b", re.I)


def _log(m: str) -> None:
    print(f"[prism.writer] {m}", file=sys.stderr, flush=True)


# Models that REMOVED the `temperature` parameter. Sending it is a 400, not a
# warning — measured 2026-08-23 on claude-sonnet-5 and claude-opus-5:
# "`temperature` is deprecated for this model." Depth is controlled by
# `output_config.effort` instead, and run-to-run variation has to come from the
# PROMPT rather than from sampling. That is a better foundation for rotation
# anyway: prompt-driven variation is reproducible from a seed, sampling noise
# is not.
NO_TEMPERATURE = ("claude-opus-5", "claude-sonnet-5", "claude-fable-5",
                  "claude-opus-4-8", "claude-opus-4-7", "claude-sonnet-4-6",
                  "claude-opus-4-6", "claude-mythos-5")
EFFORT_FOR = {"low": "low", "medium": "medium", "high": "high"}


def _is_claude(model: str) -> bool:
    return str(model or "").startswith("claude")


def _anthropic_call(model: str, system: str, user: str, max_tokens: int,
                    temperature: float, effort: str = "high") -> str:
    """One Anthropic call, with the parameters this model actually accepts.

    `temperature` is silently dropped for the models that reject it rather than
    raising, because the caller's job is to ask for prose, not to track which
    generation of the API each model belongs to."""
    import anthropic as _sdk
    kw = {"model": model, "max_tokens": max_tokens, "system": system,
          "messages": [{"role": "user", "content": user}]}
    if model in NO_TEMPERATURE:
        kw["output_config"] = {"effort": EFFORT_FOR.get(effort, "high")}
    else:
        kw["temperature"] = min(max(temperature, 0.0), 1.0)
    r = _sdk.Anthropic(api_key=_claude_key()).messages.create(**kw)
    return "".join(b.text for b in r.content
                   if getattr(b, "type", "") == "text").strip()


def _claude_key() -> str:
    import os
    try:
        return open(os.environ.get("PRISM_CLAUDE_KEY_FILE", os.path.expanduser("~/news/providers/ai/claude/api.text"))).read().strip()
    except Exception:
        return os.environ.get("ANTHROPIC_API_KEY", "")


@progress.stage('writing')
def compose(system: str, user: str, max_tokens: int = 6000,
            temperature: float = 0.3, model: str | None = None,
            effort: str = "high") -> dict:
    """Prose from the configured writer, falling back if it is unavailable.

    Returns {text, model, seconds, fallback}. A composition that comes back
    empty is a failure the caller must surface, not paper over."""
    model = model or WRITER_MODEL
    preferred = model
    fallback_reason = _provider_block(model)
    if fallback_reason:
        model = ''
    t0 = time.time()
    if model.startswith("codex:") or model.startswith("gpt-5"):
        # OpenAI Codex CLI on the ChatGPT account — a strong writer that costs
        # no API credit. Non-interactive `codex exec`, prompt over stdin, the
        # answer read back from the last-message file.
        try:
            txt = _codex_call(model.replace("codex:", "", 1), system, user, max_tokens, effort)
            if txt:
                LAST.update(model=model, seconds=round(time.time() - t0, 1), fallback_reason=None)
                return {"text": txt, "model": model, "seconds": LAST["seconds"], "fallback": False}
        except Exception as e:
            _log(f"{model} unavailable ({type(e).__name__}: {str(e)[:100]}) — falling back")
            fallback_reason = f"{type(e).__name__}"
            _provider_failed(model, e, fallback_reason)
    if "/" in model or model.startswith("together:"):
        # A strong open-weight writer on Together, for when the Anthropic
        # account has no credit: the fast Cerebras model reads abstracts well
        # and writes prose badly (it lists findings and infers beyond them).
        try:
            txt = _together_call(model.replace("together:", "", 1), system, user,
                                 max_tokens, temperature)
            if txt:
                LAST.update(model=model, seconds=round(time.time() - t0, 1), fallback_reason=None)
                return {"text": txt, "model": model, "seconds": LAST["seconds"], "fallback": False}
        except Exception as e:
            _log(f"{model} unavailable ({type(e).__name__}: {str(e)[:80]}) — falling back")
            fallback_reason = f"{type(e).__name__}"
            _provider_failed(model, e, fallback_reason)
    if _is_claude(model):
        try:
            txt = _anthropic_call(model, system, user, max_tokens, temperature,
                                  effort)
            if txt:
                LAST.update(model=model, seconds=round(time.time() - t0, 1),
                            fallback_reason=None)
                return {"text": txt, "model": model, "seconds": LAST["seconds"],
                        "fallback": False}
        except Exception as e:
            msg = str(e)
            reason = ("no API credit" if "credit balance" in msg
                      else "temperature rejected" if "temperature" in msg
                      else f"{type(e).__name__}")
            _log(f"{model} unavailable ({reason}) — falling back")
            fallback_reason = reason
            _provider_failed(model, e, reason)
    txt = llm.text(system, user, max_tokens=max_tokens, temperature=temperature)
    seconds = round(time.time() - t0, 1)
    LAST.update(model=llm.MODEL, seconds=seconds, fallback_reason=fallback_reason)
    return {"text": (txt or "").strip(), "model": llm.MODEL,
            "seconds": seconds, "fallback": True,
            "fallback_reason": fallback_reason,
            "note": f'composed by the fallback writer — the preferred model ({preferred}) was unavailable' if fallback_reason else None}


CODEX_BIN = os.environ.get("PRISM_CODEX_BIN", os.path.expanduser("~/.nvm/versions/node/v22.19.0/bin/codex"))
CODEX_EFFORT = {"low": "low", "medium": "medium", "high": "high"}


def _codex_call(model: str, system: str, user: str, max_tokens: int, effort: str) -> str:
    """One answer from the Codex CLI, non-interactively.

    The CLI is an agent, not a completion endpoint: it will happily read the
    working directory and run commands. It is run in an empty scratch
    directory, read-only sandbox, ephemeral session, with the whole prompt
    on stdin and the final message captured to a file — so a writing call
    cannot touch anything and cannot be steered by files it finds."""
    import subprocess, tempfile
    with tempfile.TemporaryDirectory(prefix="prism-codex-") as d:
        out = os.path.join(d, "last.md")
        prompt = (f"{system}\n\n----\n\n{user}\n\n----\nWrite the answer only — no preamble, "
                  f"no commentary about the task, no tool use. Do not read or write files.")
        cmd = [CODEX_BIN, "exec", "-m", model, "-C", d, "-s", "read-only", "--ephemeral",
               "--skip-git-repo-check", "-o", out,
               "-c", f"model_reasoning_effort=\"{CODEX_EFFORT.get(effort, 'medium')}\"", "-"]
        r = subprocess.run(cmd, input=prompt, capture_output=True, text=True,
                           timeout=max(240, int(max_tokens / 10)))
        if not os.path.exists(out):
            raise RuntimeError((r.stderr or r.stdout or "")[-300:])
        txt = open(out).read().strip()
        if "usage limit" in txt.lower() or "not supported" in txt.lower():
            raise RuntimeError(txt[:200])
        return txt


TOGETHER_KEY_FILE = os.environ.get("PRISM_TOGETHER_KEY_FILE", os.path.expanduser("~/news/providers/ai/together/api.text"))
TOGETHER_URL = "https://api.together.xyz/v1/chat/completions"


def _together_call(model: str, system: str, user: str, max_tokens: int,
                   temperature: float) -> str:
    """One chat completion on Together, streamed.

    Streamed always: the serverless Qwen3.x-Plus models refuse a non-streaming
    request ("This model only supports streaming"), and streaming costs the
    others nothing. Delta text is concatenated; a reasoning model's thinking
    (a `reasoning` delta, or a <think> block) is discarded."""
    import urllib.request
    key = open(TOGETHER_KEY_FILE).read().strip()
    body = {"model": model, "max_tokens": int(max_tokens), "temperature": float(temperature),
            "stream": True,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}]}
    req = urllib.request.Request(TOGETHER_URL, data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {key}",
                                          "Content-Type": "application/json",
                                          "Accept": "text/event-stream",
                                          # the edge returns 403 to urllib's
                                          # default agent; curl's passes
                                          "User-Agent": "prism-mcp/1.0 (+fliarbi.com)"},
                                 method="POST")
    parts = []
    with urllib.request.urlopen(req, timeout=300) as resp:
        for raw in resp:
            line = raw.decode("utf-8", "replace").strip()
            if not line.startswith("data:"):
                continue
            data = line[5:].strip()
            if data == "[DONE]":
                break
            try:
                j = json.loads(data)
            except Exception:
                continue
            if "error" in j:
                raise RuntimeError(str(j["error"])[:200])
            for ch in j.get("choices") or []:
                d = ch.get("delta") or {}
                if d.get("content"):
                    parts.append(d["content"])
    txt = "".join(parts).strip()
    txt = re.sub(r"<think>.*?</think>\s*", "", txt, flags=re.S)
    return txt


# ═══════════════════════════ attribution ═════════════════════════════════════
def attribution(doc: dict) -> str:
    """"Dhawan and colleagues (2021)" — built from the stored author array.

    This is the string the model is handed and told to copy. It cannot invent
    an attribution because it is never asked to produce one."""
    from . import cite
    return cite.label(doc)


def source_line(doc: dict) -> str:
    """One line of provenance a writer can read: who, where, when, what kind."""
    bits = [attribution(doc)]
    if doc.get("venue"):
        bits.append(str(doc["venue"]))
    if doc.get("tier"):
        bits.append(f"{doc['tier'].replace('_', ' ')} evidence")
    if doc.get("cited_by") is not None:
        bits.append(f"{doc['cited_by']} citations")
    return " · ".join(b for b in bits if b)


# ═══════════════════════════ gates ═══════════════════════════════════════════
_STRAY_CJK = re.compile(
    r"(?<=[A-Za-z0-9])[\u3000-\u303F\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]+"
    r"|[\u3000-\u303F\u3400-\u4DBF\u4E00-\u9FFF\uF900-\uFAFF]+(?=[A-Za-z0-9])")


def strip_stray_script(text: str) -> tuple:
    """Remove CJK characters that leak into English prose.

    Observed live: a model wrote "if your recall窗 window is measured in hours"
    — the character is a token-level slip, not a quotation, and it is invisible
    to every other gate because it carries no figure and names no source. Only
    strays GLUED to Latin text — no space on either side — are removed, so a
    genuinely quoted CJK term ("the term 供应链 means supply chain") survives."""
    if not text:
        return text, 0
    out, n = _STRAY_CJK.subn("", text)
    if n:
        out = re.sub(r"[^\S\n]{2,}", " ", out)
    return out, n


def strip_honorifics(text: str) -> tuple:
    """Remove any invented title or post-nominal, and say how many were found."""
    n = len(_HONORIFIC.findall(text or "")) + len(_POSTNOM.findall(text or ""))
    out = _POSTNOM.sub("", _HONORIFIC.sub("", text or ""))
    # Collapse runs of SPACES, never newlines. `\s{2,}` here silently turned
    # every paragraph break into a space, so five sections of a live article
    # arrived as single unbroken blocks and the wall-of-text retry kept firing
    # on text that had been correctly formatted when it left the writer.
    out = re.sub(r"[^\S\n]{2,}", " ", out)
    return re.sub(r"\n{3,}", "\n\n", out).strip(), n


def gendered_terms(text: str) -> list:
    """Pronouns applied to a named researcher. Reported, never silently kept."""
    return sorted({m.group(0).lower() for m in _PRONOUN.finditer(text or "")})


_DASHES = str.maketrans({"\u2010": "-", "\u2011": "-", "\u2012": "-",
                         "\u2013": "-", "\u2014": "-", "\u2212": "-",
                         "\u202f": " ", "\u00a0": " "})
_PROPER = re.compile(r"\b(?!The\b|A\b|An\b|On\b|In\b|At\b|By\b|As\b|It\b|They\b|We\b|"
                     r"This\b|That\b|These\b|Those\b|But\b|And\b|For\b|"
                     r"When\b|While\b|After\b|Before\b|During\b|Three\b|"
                     r"Two\b|Four\b|Five\b)"
                     r"[A-Z][a-z]{2,}(?:\s+[A-Z][a-z]{2,})*\b")
_MONTH_WORDS = {"January", "February", "March", "April", "May", "June", "July",
                "August", "September", "October", "November", "December",
                "Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
                "Saturday", "Sunday"}


def unsourced_names(text: str, sources: list) -> list:
    """Proper nouns in generated text that appear in none of its sources.

    Numbers are not the only thing a model invents. Asked to name the scene an
    article should open on, it placed a real, correctly-dated incident — three
    students drowned in a flooded coaching centre — in the wrong part of the
    city, a district the sources never mention. A wrong place name in a lede is
    as damaging as a wrong figure and the number gate cannot see it.

    A SINGLE capitalised word at the start of a sentence is not evidence of a
    name: "Later", "Together" and "Vehicles" all opened sentences in a real
    draft and all three were flagged. Sentence-initial single words are only
    checked when they are not ordinary English, which in practice means they
    are skipped; a multi-word capitalised run is checked wherever it appears."""
    hay = " ".join(str(s) for s in (sources or [])).lower()
    if not hay:
        return []
    # Normalise the unicode hyphens the writers emit. Without this,
    # "Record‑Breaking" (U+2011) split at the hyphen and "Breaking Monsoon
    # Sparks Fatal Floods" was reported as an unsourced name on every model —
    # a heading, flagged as a fabrication.
    body = (text or "").translate(_DASHES)
    hay = hay.translate(_DASHES)
    # Markdown headings are structure, not claims. "## Sources" and "## Where
    # the evidence is thin" were being reported as fabricated names.
    body = re.sub(r"^#{1,6}[^\n]*$", "", body, flags=re.M)
    bad = []
    for m in _PROPER.finditer(body):
        name = m.group(0).strip()
        if name in _MONTH_WORDS or len(name) < 4:
            continue
        multiword = len(name.split()) > 1
        if not multiword:
            raw_before = body[:m.start()]
            before = raw_before.rstrip()
            # Sentence-initial, opening the text, opening a paragraph, or
            # opening a list item or a table cell: not a name claim.
            # "Haematoma" at the head of a bullet was flagged as a fabricated
            # person; "Proposing" opening the paragraph after a chart image
            # line was flagged too, because the newline test ran on a string
            # that had just had its newlines stripped, and the image line
            # ends in ")" which was not a terminator.
            if (not before or before[-1] in ".!?:;)\u201d\"|*-\u2014"
                    or raw_before.endswith("\n") or "\n" in raw_before[len(before):]):
                continue
        head = name.split()[0]
        if name.lower() in hay or head.lower() in hay:
            continue
        # "Bangladeshi" when the source says Bangladesh; "Belgian" for
        # Belgium; "Chinese" for China. A demonym is the sourced place in
        # another grammatical form, not a new name.
        low = head.lower()
        stems = [low[:-len(suf)] for suf in ("ian", "ese", "ish", "an", "i", "s")
                 if low.endswith(suf) and len(low) - len(suf) >= 4]
        if any(st in hay for st in stems):
            continue
        bad.append(name)
    return sorted(set(bad))


# "<Masthead> reported that … N articles/pieces/stories/mentions" — a newspaper
# being credited with one of our own coverage metrics. Seen live three times in
# one section.
_METRIC_ATTRIB = re.compile(
    r"\b(?:The\s+)?[A-Z][A-Za-z’\'-]+(?:\s+(?:of\s+)?[A-Z][A-Za-z’\'-]+){0,3}\s+"
    r"(?:reported|noted|highlighted|said|wrote|observed|added|found)\b[^.]{0,180}?"
    r"\b\d[\d,\s]*\s*(?:articles|pieces|stories|mentions|reports)\b", re.I)
# A job title attached to a person the corpus only names.
_TITLED = re.compile(r"\b(?:the\s+)?(?:mayor|chief minister|prime minister|"
                     r"president|governor|minister|commissioner|secretary|"
                     r"director|chairman|chairperson|ceo)\b['’]?s?\s+"
                     r"(?:prominent\s+)?role\b", re.I)


def misattributed_metrics(text: str) -> list:
    """Sentences crediting a publication with one of OUR measurements."""
    return [m.group(0)[:120] for m in _METRIC_ATTRIB.finditer(text or "")]


def invented_titles(text: str) -> list:
    return [m.group(0) for m in _TITLED.finditer(text or "")]


def ground(paragraph: str, sources: list) -> dict:
    """Is every number in this paragraph present in the material it was given?

    Returns the paragraph cleaned of invented honorifics plus a verdict a
    caller can act on: `grounded` false means a figure was written that no
    source carries, which is the one failure that must never reach a reader
    unflagged."""
    cleaned, strays = strip_stray_script(paragraph)
    cleaned, honorifics = strip_honorifics(cleaned)
    bad = llm.ungrounded_numbers(cleaned, sources)
    names = unsourced_names(cleaned, sources)
    misattrib = misattributed_metrics(cleaned)
    titles = invented_titles(cleaned)
    pron = gendered_terms(cleaned)
    return {"text": cleaned,
            "grounded": not bad and not names and not misattrib and not titles,
            "verification_scope": "Mechanical checks of quantities, names and attribution; not a semantic fact-check.",
            "semantic_support_verified": False,
            "ungrounded_numbers": bad, "unsourced_names": names,
            "misattributed_metrics": misattrib, "invented_titles": titles,
            "honorifics_removed": honorifics,
            "gendered_pronouns": pron,
            "note": ("a number here appears in no source — do not publish it "
                     "without checking" if bad else
                     f"names appearing in no source: {', '.join(names)}"
                     if names else None),
            "pronoun_note": ("this text applies a gendered pronoun to a named "
                             "researcher; an author list does not tell us anyone's "
                             "pronouns" if pron else None)}


_SENT_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(\u201c\"])")


def excise_ungrounded(text: str, sources: list) -> dict:
    """Remove every sentence that carries a figure no source holds.

    The second line of defence, and the one that ships. The first — telling
    the model not to — is not reliable: handed only verified quotes, Claude
    Opus 5 still wrote "HR 0.925; 95% CI 0.882–0.971; P = 0.002" against a
    real 2026 paper, reconstructing a plausible statistic from memory of the
    literature. Every part of it looked right; every part was invented. A gate
    that merely FLAGS that leaves a publishable-looking fabrication in the
    text. So the sentence goes, and the payload says which, so an editor can
    restore it from the actual paper if they want to.

    Cut at sentence level, never word level: removing a number from a sentence
    leaves a sentence that asserts something without it, which is worse."""
    paras = re.split(r"\n\s*\n", text or "")
    out, removed = [], []
    src_nums = set()
    for s in sources or []:
        src_nums |= llm.numbers_in(s if isinstance(s, str) else json.dumps(s, default=str))
    for para in paras:
        if para.lstrip().startswith("#") or not para.strip():
            out.append(para)
            continue
        kept = []
        for sent in _SENT_SPLIT.split(para):
            bad = [n for n in llm.numbers_in(sent) if n not in src_nums
                   and not (float(n) == int(float(n)) and
                            (1900 <= float(n) <= 2100 or float(n) <= 20))]
            if bad:
                removed.append({"sentence": sent.strip()[:240], "figures": bad})
            else:
                kept.append(sent)
        if kept:
            out.append(" ".join(kept))
    return {"text": "\n\n".join(out), "removed": removed}


def pack_sources(docs: list, chars: int = 900) -> str:
    """The evidence block handed to the writer.

    Each document arrives with its attribution string already rendered, its
    tier, and its verified quote. The model's job is to arrange and explain
    what is here — never to remember anything else."""
    out = []
    for i, d in enumerate(docs, 1):
        q = (d.get("quote") or "").strip()
        body = q or (d.get("abstract") or "")[:chars]
        label = 'VERIFIED QUOTE' if q and d.get('grounded') else 'SOURCE EXCERPT (not a verified verdict)'
        out.append(
            f"[S{i}] ATTRIBUTION: {attribution(d)}\n"
            f"     TITLE: {d.get('title')}\n"
            f"     WHERE: {source_line(d)}\n"
            f"     STANCE ON THE CLAIM: {d.get('stance', 'not assessed')}\n"
            f"     {label}: \"{body}\"")
    return "\n\n".join(out)


HOUSE_RULES = (
 "HOW TO WRITE HERE — these are not style preferences, they are what keeps the "
 "text publishable:\n"
 "* Every factual sentence traces to a supplied source. If the sources do not "
 "cover something, do not write it. A short paragraph is fine; an invented one "
 "is not.\n"
 "* Attribute by copying the ATTRIBUTION string EXACTLY as given: 'Dhawan and "
 "colleagues (2021) report that…'. Never add a title — no Dr, Prof, Mr or Ms. "
 "You know these people wrote a paper; you do not know what they are called or "
 "what degrees they hold, and printing a guess under a real person's name is a "
 "fabrication.\n"
 "* Never use he/she/his/her for a researcher. Use the surname or 'the study'.\n"
 "* Write NO number that is not in the material given. Not a rounded one, not a "
 "converted one, not an approximate one.\n"
 "* Where the evidence is mixed, say so in the prose. Do not resolve a real "
 "disagreement to make a cleaner sentence.\n"
 "* Match the draft's voice and reading level. You are continuing someone "
 "else's article, not starting your own.")
