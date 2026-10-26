#!/usr/bin/env python3
"""rotate — same facts, different article, every time somebody asks.

Two people requesting a piece on the same subject should not receive the same
text. Not because sameness is wrong, but because a syndication system that
hands identical copy to twenty publishers has produced one article, not twenty,
and every one of them is duplicate content.

So this module varies the PRESENTATION while holding the SUBSTANCE fixed:

    varies      the opening scene, the section order and mix, which chart
                shape carries the data, the register the piece is written in,
                the headline
    never       a number, a date, a quote, an attribution, or which facts are
                on the page

That distinction is the whole design. Rotation happens BEFORE the writer runs,
by changing what is asked for — not after, by rewording what came back, and not
by turning up the sampling temperature. Two reasons, and the second is the one
that matters:

  1. Claude Opus 5 and Sonnet 5 REMOVED the temperature parameter (a 400 as of
     2026-08-23), so sampling noise is not available on the models this server
     prefers.
  2. Temperature is not reproducible. A seed is. Given the same request id you
     get the same article back — which is what makes a rotation auditable, and
     what lets a caller re-fetch the piece they were served last week.

The seed is derived from whatever identifies the request (a caller id, a
publication, a date), so two publishers get different pieces and one publisher
asking twice gets the same piece.
"""
from __future__ import annotations

import hashlib
import json

# ── the dimensions that rotate ───────────────────────────────────────────────
# Each is a set of equally-truthful ways to present the same evidence. Nothing
# here changes what is true; it changes which true thing leads.

OPENINGS = [
    {"key": "scene", "brief": (
        "Open on the single most concrete moment in the evidence — a named day, "
        "a named place, a named consequence. One or two sentences of scene "
        "before any context.")},
    {"key": "pattern", "brief": (
        "Open on the shape of the thing: the rhythm, the repetition, the fact "
        "that this recurs. The specific incident comes second, as the example.")},
    {"key": "contrast", "brief": (
        "Open on a tension in the evidence — something that rose while "
        "something else fell, or a gap between what is reported and what is "
        "fixed. Name both halves in the first three sentences.")},
    {"key": "actor", "brief": (
        "Open on who is involved — the institutions and people the record "
        "keeps naming — and only then on what happened to them.")},
    {"key": "question", "brief": (
        "Open on the question the evidence raises and does not answer. Do not "
        "answer it in the opening; the piece is the answer.")},
    {"key": "consequence", "brief": (
        "Open on the downstream effect furthest from the obvious one — the "
        "thing a reader would not have predicted from the subject line.")},
]

REGISTERS = [
    {"key": "reported", "brief": (
        "A news feature. Plain declaratives, short paragraphs, the reporting "
        "doing the work. No rhetorical questions.")},
    {"key": "analytic", "brief": (
        "An analysis piece. Longer sentences, explicit reasoning, willing to "
        "say 'which suggests' and 'the more likely reading is'.")},
    {"key": "explanatory", "brief": (
        "An explainer. Assume the reader knows nothing; define as you go; use "
        "the second person sparingly to orient them.")},
    {"key": "dispatch", "brief": (
        "A dispatch. Present tense where the evidence allows, concrete nouns, "
        "the texture of the place foregrounded.")},
]

CHARTS = [
    {"key": "bars", "for": "season", "brief": "vertical bars, one per month"},
    {"key": "lollipop", "for": "season", "brief": "stems with dots at the value"},
    {"key": "area", "for": "season", "brief": "a filled area curve across the year"},
    {"key": "heatstrip", "for": "season", "brief": "a single row of intensity blocks"},
    {"key": "timeline", "for": "events", "brief": "a dated vertical timeline"},
    {"key": "beeswarm", "for": "events", "brief": "events plotted along a time axis"},
    {"key": "ledger", "for": "factors", "brief": "two facing columns"},
    {"key": "cards", "for": "factors", "brief": "a grid of small cards"},
]

# Which section lanes may lead. A piece that always leads on the same lane is
# the same piece; a piece that leads on a lane the evidence cannot carry is a
# worse piece. The planner still filters to what exists.
LEAD_LANES = ["events", "season", "causes", "impacts", "shift", "actors"]


def seed_of(subject: str, requester: str = "", salt: str = "") -> int:
    """A stable integer for this (subject, requester) pair.

    Same requester asking twice about the same subject gets the same article —
    which is what makes it re-fetchable. A different requester gets a different
    one. `salt` lets a caller deliberately ask for another take on the same
    subject without pretending to be somebody else."""
    raw = json.dumps([str(subject).strip().lower(), str(requester).strip().lower(),
                      str(salt)], sort_keys=True)
    return int(hashlib.sha256(raw.encode()).hexdigest()[:12], 16)


def _pick(seq: list, seed: int, offset: int):
    return seq[(seed >> (offset * 5)) % len(seq)] if seq else None


def plan(subject: str, requester: str = "", salt: str = "",
         available_lanes: list | None = None) -> dict:
    """The rotation for one request: opening, register, charts, lead lane.

    Deterministic in the seed and independent of the evidence, so it can be
    computed before any retrieval and logged with the response. The planner
    downstream still refuses any lane the corpus cannot support — rotation
    proposes, evidence disposes."""
    seed = seed_of(subject, requester, salt)
    lanes = [l for l in LEAD_LANES if not available_lanes or l in available_lanes]
    opening = _pick(OPENINGS, seed, 0)
    register = _pick(REGISTERS, seed, 1)
    lead = _pick(lanes or LEAD_LANES, seed, 2)
    season_charts = [c for c in CHARTS if c["for"] == "season"]
    event_charts = [c for c in CHARTS if c["for"] == "events"]
    factor_charts = [c for c in CHARTS if c["for"] == "factors"]
    return {
        "seed": seed,
        "subject": subject, "requester": requester or None, "salt": salt or None,
        "opening": opening, "register": register, "lead_lane": lead,
        "charts": {"season": _pick(season_charts, seed, 3),
                   "events": _pick(event_charts, seed, 4),
                   "factors": _pick(factor_charts, seed, 5)},
        "section_shuffle": (seed >> 30) % 3,
        "guarantee": ("presentation only — the facts, figures, quotes and "
                      "attributions are identical across every rotation of the "
                      "same subject"),
        "reproducible": ("the same subject and requester always produce this "
                         "same rotation; pass `salt` to ask for another take"),
    }


def brief(rot: dict) -> str:
    """The rotation as instructions the planner and writer can follow."""
    if not rot:
        return ""
    return (f"OPENING APPROACH ({rot['opening']['key']}): {rot['opening']['brief']}\n"
            f"REGISTER ({rot['register']['key']}): {rot['register']['brief']}\n"
            f"LEAD WITH THE '{rot['lead_lane']}' MATERIAL if the evidence "
            f"supports it.\n"
            f"These choices govern SHAPE ONLY. Every figure, date, quote and "
            f"attribution must be exactly what the material says — rotation "
            f"never changes a fact.")


def reorder(sections: list, rot: dict) -> list:
    """Rotate the middle of an article without breaking how it reads.

    The first section and the last stay put: a piece has to open on its
    strongest concrete material and close on what is unresolved, whatever
    rotation it drew. Only the middle is permuted, so the shape varies and the
    argument still lands."""
    if not sections or len(sections) < 4 or not rot:
        return sections
    head, mid, tail = sections[:1], sections[1:-1], sections[-1:]
    k = rot.get("section_shuffle", 0) % max(1, len(mid))
    return head + mid[k:] + mid[:k] + tail
