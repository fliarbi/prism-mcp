#!/usr/bin/env python3
"""llm — the model leg, and the gates that keep it honest.

The division of labour in this server is deliberate and absolute:

    ClickHouse produces every NUMBER. The model produces only LANGUAGE.

A research assistant that invents a prevalence figure is worse than no research
assistant, because the figure looks exactly like the real ones. So the model is
used for the three jobs it is actually good at — splitting prose into claims,
naming the concepts a claim is about, and characterising a set of abstracts —
and every output is passed through a gate that can fail:

  * `ungrounded_numbers()` — any number in generated prose that does not appear
    in the sources it was given is reported, and callers strip or reject it.
  * `verify_quote()` — a quoted sentence must actually occur in the abstract it
    is attributed to, after whitespace and unicode-dash normalisation.
  * `_parse()` — a JSON answer that does not parse degrades to None. The tool
    then returns `available: false` with a reason instead of prose about
    nothing.

Provider: Cerebras gpt-oss-120b, the same provider the Prism problem-page
pipeline uses. reasoning_effort is pinned to 'medium' — on a long prompt 'high'
spends the whole budget on reasoning tokens and returns a zero-word completion
with finish_reason=length, which reads as a silent failure. Anthropic is
available behind PRISM_LLM_CLAUDE=1 but is off by default: the key at
news/providers/ai/claude has returned 'credit balance is too low' since
2026-08-04, and a guaranteed-failing first leg only adds latency.
"""
from __future__ import annotations

import json
import os
import re
import sys
import time
import urllib.request

LLM_PATH = os.environ.get("PRISM_LLM_PATH", os.path.expanduser("~/automations/curation_test"))
MODEL = os.environ.get("PRISM_LLM_MODEL", "gpt-oss-120b")
EFFORT = os.environ.get("PRISM_LLM_EFFORT", "medium")
USE_CLAUDE = os.environ.get("PRISM_LLM_CLAUDE", "0") == "1"
CLAUDE_MODEL = os.environ.get("PRISM_CLAUDE_MODEL", "claude-opus-5")
TIMEOUT = int(os.environ.get("PRISM_LLM_TIMEOUT", "180"))

LAST = {"provider": None, "seconds": None, "finish": None}
# Process-wide token meter (prompt, completion, calls); read by tools/measure_costs.py to price features.
import threading as _threading
METER = {"prompt": 0, "completion": 0, "calls": 0}
_METER_LOCK = _threading.Lock()


def _log(m: str) -> None:
    print(f"[prism.llm] {m}", file=sys.stderr, flush=True)


def _llmlib():
    if LLM_PATH not in sys.path:
        sys.path.append(LLM_PATH)
    import llmlib as L
    return L


def _parse(raw: str):
    """First JSON object in the text, with one repair pass for trailing commas."""
    if not raw:
        return None
    m = re.search(r"\{.*\}", raw, re.S)
    if not m:
        return None
    body = m.group(0)
    try:
        return json.loads(body)
    except Exception:
        try:
            return json.loads(re.sub(r",\s*([}\]])", r"\1", body))
        except Exception:
            return None


def text(system: str, user: str, max_tokens: int = 4000,
         temperature: float = 0.2, effort: str = EFFORT) -> str | None:
    """Raw completion text, or None. Cerebras direct — llmlib's helper caps
    max_tokens lower than the reading calls here need and does not expose
    reasoning_effort, which is the setting that decides whether the answer is
    1,300 words or zero."""
    L = _llmlib()
    payload = {"model": MODEL, "max_tokens": max_tokens,
               "temperature": temperature, "reasoning_effort": effort,
               "messages": [{"role": "system", "content": system},
                            {"role": "user", "content": user}]}
    req = urllib.request.Request(
        L.CEREBRAS_URL, data=json.dumps(payload).encode(),
        headers={"Authorization": f"Bearer {L.CEREBRAS_API_KEY}",
                 "Content-Type": "application/json",
                 "User-Agent": "prism-mcp/1.0", "Accept": "application/json"})
    t0 = time.time()
    with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
        d = json.loads(r.read())
    u = d.get("usage") or {}
    with _METER_LOCK:
        METER["prompt"] += int(u.get("prompt_tokens") or 0)
        METER["completion"] += int(u.get("completion_tokens") or 0)
        METER["calls"] += 1
    raw = (d["choices"][0]["message"].get("content") or "").strip()
    fin = d["choices"][0].get("finish_reason")
    LAST.update(provider=MODEL, seconds=round(time.time() - t0, 1), finish=fin)
    if fin == "length" and not raw:
        _log("budget exhausted before any content — raise max_tokens or lower effort")
        return None
    return raw


def call_json(system: str, user: str, max_tokens: int = 4000,
              temperature: float = 0.0, effort: str = EFFORT, retry: bool = True):
    """A parsed JSON object, or None. Never raises: every tool that uses the
    model has a degraded path, and a research answer with no prose is far more
    useful than a stack trace."""
    system = system.rstrip() + "\nReturn ONLY a single JSON object. No prose outside it."
    if USE_CLAUDE:
        try:
            L = _llmlib()
            out = _parse(L.claude_text(system, user, max_tokens=max_tokens,
                                       temperature=temperature, model=CLAUDE_MODEL))
            if out is not None:
                LAST.update(provider=CLAUDE_MODEL)
                return out
        except Exception as e:
            _log(f"{CLAUDE_MODEL} unavailable ({type(e).__name__}) — cerebras")
    budgets = (max_tokens, int(max_tokens * 1.5)) if retry else (max_tokens,)
    for i, budget in enumerate(budgets, 1):
        try:
            out = _parse(text(system, user, max_tokens=budget,
                              temperature=temperature, effort=effort))
            if out is not None:
                return out
            _log(f"unparseable output (attempt {i})")
        except Exception as e:
            _log(f"call failed (attempt {i}): {type(e).__name__}: {e}")
    return None


def available() -> dict:
    try:
        L = _llmlib()
        return {"provider": MODEL, "configured": bool(L.CEREBRAS_API_KEY),
                "effort": EFFORT, "claude_leg": USE_CLAUDE}
    except Exception as e:
        return {"provider": MODEL, "configured": False,
                "error": f"{type(e).__name__}: {e}"}


# ═══════════════════════════ grounding gates ═════════════════════════════════
_THIN = "     "
_GROUPED = re.compile(rf"(?<=\d)[{_THIN}](?=\d{{3}}\b)")
_DASHES = str.maketrans({"‐": "-", "‑": "-", "‒": "-",
                         "–": "-", "—": "-", "−": "-",
                         "‘": "'", "’": "'", "“": '"',
                         "”": '"'})
# No trailing \b. With one, a decimal immediately followed by a letter loses
# its fractional part: "34.2x" in the source material parsed as "34", so prose
# citing 34.2 was reported as an invented figure. Every growth multiple in this
# system is written that way ("3.82x", "7.75x"), which made the number gate
# cry wolf on exactly the figures it was meant to protect.
_NUM = re.compile(r"(?<![\w.])[+-]?\d[\d,]*(?:\.\d+)?(?![\d.])")


def norm(s: str) -> str:
    """Whitespace, unicode dashes and thin-space digit grouping normalised, so
    '1 284' from a PDF-derived abstract and '1,284' from the model compare
    equal and a real quote is not rejected as invented."""
    s = (s or "").translate(_DASHES)
    s = _GROUPED.sub("", s)
    return re.sub(r"\s+", " ", s).strip()


def numbers_in(s: str) -> set:
    """Every number in a string, normalised: 1,284 / 1284 / 1284.0 all agree."""
    out = set()
    for m in _NUM.finditer(norm(s)):
        t = m.group(0).replace(",", "")
        try:
            f = float(t)
        except ValueError:
            continue
        out.add(str(int(f)) if f == int(f) else str(f))
    return out


def ungrounded_numbers(prose: str, sources) -> list:
    """Numbers the model wrote that appear in none of its sources.

    Check units as well as values. Small percentages and years are still
    factual claims; they must occur in the supplied material too. This is a
    quantity check, not a claim of semantic entailment."""
    if not prose:
        return []
    source_text = "\n".join(s if isinstance(s, str) else json.dumps(s, default=str)
                            for s in sources or [])
    src = numbers_in(source_text)
    bad = []
    for n in numbers_in(prose):
        if n in src:
            continue
        bad.append(n)
    source_quantities = _quantities(source_text)
    for value, unit in _quantities(prose):
        if (value, unit) not in source_quantities:
            bad.append(f"{value} {unit}")
    return sorted(set(bad))


_QUANTITY = re.compile(
    r"(?<![\w.])(?P<currency>[$€£₹])?\s*(?P<number>[+-]?\d[\d,]*(?:\.\d+)?)\s*"
    r"(?P<unit>%|percent\b|per cent\b|percentage points?\b|"
    r"million\b|billion\b|thousand\b|kg\b|mg\b|km\b|years?\b|"
    r"months?\b|days?\b|participants?\b|patients?\b|cases?\b|"
    r"deaths?\b|people\b|USD\b|INR\b|x\b)?", re.I)


def _quantities(text: str) -> set:
    out = set()
    for m in _QUANTITY.finditer(norm(text)):
        unit = (m.group('unit') or '').lower()
        if unit in ('percent', 'per cent'):
            unit = '%'
        unit = {'years': 'year', 'months': 'month', 'days': 'day',
                'participants': 'participant', 'patients': 'patient',
                'cases': 'case', 'deaths': 'death',
                'percentage points': 'percentage point'}.get(unit, unit)
        unit = (m.group('currency') or '') + unit
        if unit:
            values = numbers_in(m.group('number'))
            if values:
                out.add((next(iter(values)), unit))
    return out


def strip_numbers(s: str) -> str:
    """For prose that is meant to characterise rather than quantify — the page
    prints the computed number next to it, and two numbers that disagree is the
    failure this prevents."""
    return _NUM.sub("[n]", s or "")


def verify_quote(quote: str, source_text: str) -> bool:
    """Did this sentence actually occur in that abstract?

    Every span must occur in source order. Shared opening words do not verify
    an invented ending. Ellipses may omit text but cannot reorder source spans
    or exempt short fragments from verification."""
    q, s = norm(quote).lower(), norm(source_text).lower()
    if not q or not s:
        return False
    if q in s:
        return True
    if "..." in q or "\u2026" in q:
        segs = [x.strip() for x in re.split(r"\.\.\.|\u2026", q) if x.strip()]
        offset = 0
        for span in segs:
            pos = s.find(span, offset)
            if pos < 0:
                return False
            offset = pos + len(span)
        return bool(segs)
    return False
