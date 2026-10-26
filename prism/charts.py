#!/usr/bin/env python3
"""charts — Prism data as a PNG a publisher can embed anywhere.

An article that says "coverage peaks in July at 2,119 articles against 62 in
November" is asking the reader to hold twelve numbers in their head. A chart
does that work. Until now the rotation CHOSE a chart shape and nothing drew it,
so the choice was discarded and every published piece was text-only.

Rendered with PIL rather than matplotlib — matplotlib is not installed on this
box and a charting stack is a heavy dependency for eight shapes. Drawing them
directly also means the output matches the Prism palette exactly rather than
being a themed matplotlib figure, and there is no font-cache warm-up on first
call.

PNG, not SVG, deliberately: the target is an <img> in someone else's CMS, an
RSS reader, a newsletter, a social card. SVG breaks in about half of those.

DESIGN RULES, applied by `_frame`:
  * every chart carries its own window and source line — a chart that travels
    without its provenance is the thing this whole server exists to prevent
  * the highlighted values are the ones the prose talks about, nothing else
  * @2x pixel density, because these are read on phones
  * light and dark variants, because a publisher embeds into their own theme
"""
from __future__ import annotations

import hashlib
import io
import math
import os
import re
import subprocess
import time
import urllib.request

from PIL import Image, ImageDraw, ImageFont

# ── palette (the same monsoon set the published articles use) ────────────────
THEMES = {
    "light": {"bg": (242, 243, 239), "card": (255, 255, 255),
              "ink": (20, 26, 28), "soft": (85, 96, 95), "rule": (221, 224, 218),
              "deep": (28, 90, 102), "silt": (168, 95, 20), "flood": (140, 47, 30),
              "dim": (28, 90, 102, 110)},
    "dark": {"bg": (14, 19, 21), "card": (21, 27, 29),
             "ink": (230, 233, 228), "soft": (147, 160, 158), "rule": (38, 48, 47),
             "deep": (111, 179, 190), "silt": (216, 154, 76), "flood": (224, 138, 118),
             "dim": (111, 179, 190, 110)},
}
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
SCALE = 2                       # @2x — these are read on phones
W, H = 1000, 520                # logical size; actual output is SCALE times this

# ── hosting ─────────────────────────────────────────────────────────────────
FLIAR_HOST = os.environ.get("PRISM_CHART_HOST", "")
FLIAR_DIR = os.environ.get("PRISM_CHART_DIR",
                           "/var/www/html/fliar_site/fliar/assets/charts")
FLIAR_URL = os.environ.get("PRISM_CHART_URL", "https://fliarbi.com/assets/charts")
LOCAL_DIR = os.environ.get("PRISM_CHART_LOCAL",
                           os.path.join(os.path.dirname(os.path.dirname(
                               os.path.abspath(__file__))), "cache", "charts"))
os.makedirs(LOCAL_DIR, exist_ok=True)

KINDS = ("bars", "lollipop", "area", "heatstrip", "timeline", "ledger", "donut")


def _font(name: str, size: int):
    path = {"sans": "DejaVuSans.ttf", "bold": "DejaVuSans-Bold.ttf",
            "serif": "DejaVuSerif.ttf", "serif_bold": "DejaVuSerif-Bold.ttf",
            "mono": "DejaVuSansMono.ttf"}[name]
    return ImageFont.truetype(os.path.join(FONT_DIR, path), size * SCALE)


def _tw(d, text, font) -> int:
    return int(d.textlength(text, font=font))


# ═══════════════════════════ frame ═══════════════════════════════════════════
def _frame(title: str, subtitle: str, source: str, theme: str = "light"):
    """A titled card with the source line already placed.

    Returns (image, draw, plot_box). Every chart shares this so a set of them
    reads as one system, and so no chart can be drawn without its provenance."""
    C = THEMES[theme]
    img = Image.new("RGB", (W * SCALE, H * SCALE), C["bg"])
    d = ImageDraw.Draw(img)
    pad = 44 * SCALE
    d.rounded_rectangle([pad // 2, pad // 2, W * SCALE - pad // 2, H * SCALE - pad // 2],
                        radius=6 * SCALE, fill=C["card"], outline=C["rule"],
                        width=1 * SCALE)
    x0, y = pad, pad
    f_title = _font("serif_bold", 27)
    f_sub = _font("sans", 14)
    f_src = _font("mono", 11)
    # shrink the title until it fits the card instead of slicing it — a cut-off title is a broken chart
    for size in (27, 25, 23, 21, 19, 17):
        f_title = _font("serif_bold", size)
        if _tw(d, title, f_title) <= (W - 100) * SCALE:
            break
    d.text((x0, y), title, font=f_title, fill=C["ink"])
    y += 40 * SCALE
    if subtitle:
        for line in _wrap(d, subtitle, f_sub, (W - 100) * SCALE)[:2]:
            d.text((x0, y), line, font=f_sub, fill=C["soft"])
            y += 21 * SCALE
    y += 10 * SCALE
    src_y = H * SCALE - pad - 16 * SCALE
    d.text((x0, src_y), source[:120], font=f_src, fill=C["soft"])
    d.line([x0, src_y - 14 * SCALE, W * SCALE - pad, src_y - 14 * SCALE],
           fill=C["rule"], width=1 * SCALE)
    _brand(d, W * SCALE - pad, src_y, C)
    return img, d, (x0, y, W * SCALE - pad, src_y - 34 * SCALE)


BRAND = "Fliar BI · Prism"


def _brand(d, right_x: int, y: int, C: dict) -> None:
    """The mark, bottom-right, on every chart.

    A chart that leaves this system is the only part of it most readers will
    ever see, and it will be screenshotted, re-uploaded and cropped. The source
    line at bottom-left says where the data came from; this says who measured
    it. Set in the same quiet mono as the source so it reads as provenance, not
    as an advertisement — the accent colour on the dot is the only flourish."""
    f = _font("mono", 11)
    f_b = _font("bold", 11)
    parts = BRAND.split(" · ")
    dot_r = 3 * SCALE
    x = right_x
    x -= _tw(d, parts[1], f_b)
    d.text((x, y), parts[1], font=f_b, fill=C["ink"])
    x -= 14 * SCALE
    d.ellipse([x - dot_r, y + 7 * SCALE - dot_r, x + dot_r, y + 7 * SCALE + dot_r],
              fill=C["silt"])
    x -= 10 * SCALE + _tw(d, parts[0], f)
    d.text((x, y), parts[0], font=f, fill=C["soft"])


def _short_label(label: str, n: int) -> str:
    """Month names abbreviate to three letters; anything else keeps up to six characters when the
    axis is crowded (n > 8) and fourteen otherwise — "2023Q1" and "Radiomics" must survive intact."""
    s = str(label)
    if n > 8:
        return s[:3] if s.isalpha() and len(s) > 6 else s[:6]
    return s[:14]


def _wrap(d, text, font, max_w):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if _tw(d, t, font) <= max_w:
            cur = t
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


# ═══════════════════════════ shapes ══════════════════════════════════════════
def _series_chart(spec: dict, theme: str, kind: str):
    """bars | lollipop | area | heatstrip — one value per labelled period."""
    C = THEMES[theme]
    pts = spec["points"]
    hi = set(spec.get("highlight") or [])
    img, d, (x0, y0, x1, y1) = _frame(spec["title"], spec.get("subtitle", ""),
                                      spec.get("source", ""), theme)
    n = len(pts)
    peak = max((p["value"] for p in pts), default=1) or 1
    lab_h = 26 * SCALE
    # Headroom for the value label above the tallest bar. Without it the peak
    # label collides with the subtitle — the July bar in the Delhi chart
    # printed "2,119" straight through the standfirst.
    head_h = 24 * SCALE
    plot_h = (y1 - y0) - lab_h - head_h
    gap = 8 * SCALE
    slot = (x1 - x0) / n
    f_lab = _font("mono", 11)
    f_val = _font("bold", 12)

    for i, p in enumerate(pts):
        cx = x0 + slot * i + slot / 2
        frac = p["value"] / peak
        top = y1 - lab_h - plot_h * frac
        on = p["label"] in hi or p.get("highlight")
        col = C["silt"] if on else C["deep"]
        if kind == "bars":
            bw = max(6 * SCALE, slot - gap)
            d.rectangle([cx - bw / 2, top, cx + bw / 2, y1 - lab_h],
                        fill=col if on else C["deep"])
        elif kind == "lollipop":
            d.line([cx, y1 - lab_h, cx, top], fill=C["rule"], width=2 * SCALE)
            r = 7 * SCALE
            d.ellipse([cx - r, top - r, cx + r, top + r], fill=col)
        elif kind == "heatstrip":
            bw = slot - 2 * SCALE
            band = min(1.0, 0.16 + 0.84 * frac)
            fill = tuple(int(C["card"][k] + (col[k] - C["card"][k]) * band)
                         for k in range(3))
            d.rectangle([cx - bw / 2, y0 + plot_h * 0.18,
                         cx + bw / 2, y1 - lab_h], fill=fill)
        if on:
            v = f"{p['value']:,}"
            d.text((cx - _tw(d, v, f_val) / 2, top - 20 * SCALE), v,
                   font=f_val, fill=col)
        lab = _short_label(p["label"], n)
        d.text((cx - _tw(d, lab, f_lab) / 2, y1 - lab_h + 6 * SCALE), lab,
               font=f_lab, fill=C["soft"])

    if kind == "area":
        # redraw as a filled curve over the same geometry
        img2, d2, (a0, b0, a1, b1) = _frame(spec["title"], spec.get("subtitle", ""),
                                            spec.get("source", ""), theme)
        plot_h2 = (b1 - b0) - lab_h - head_h
        poly = [(a0, b1 - lab_h)]
        for i, p in enumerate(pts):
            cx = a0 + (a1 - a0) * (i / max(1, n - 1))
            poly.append((cx, b1 - lab_h - plot_h2 * (p["value"] / peak)))
        poly.append((a1, b1 - lab_h))
        overlay = Image.new("RGBA", img2.size, (0, 0, 0, 0))
        ImageDraw.Draw(overlay).polygon(poly, fill=C["dim"])
        img2 = Image.alpha_composite(img2.convert("RGBA"), overlay).convert("RGB")
        d2 = ImageDraw.Draw(img2)
        d2.line(poly[1:-1], fill=C["deep"], width=3 * SCALE, joint="curve")
        for i, p in enumerate(pts):
            cx = a0 + (a1 - a0) * (i / max(1, n - 1))
            cy = b1 - lab_h - plot_h2 * (p["value"] / peak)
            if p["label"] in hi or p.get("highlight"):
                r = 6 * SCALE
                d2.ellipse([cx - r, cy - r, cx + r, cy + r], fill=C["silt"])
                v = f"{p['value']:,}"
                d2.text((cx - _tw(d2, v, f_val) / 2, cy - 22 * SCALE), v,
                        font=f_val, fill=C["silt"])
            lab = _short_label(p["label"], n)
            d2.text((cx - _tw(d2, lab, f_lab) / 2, b1 - lab_h + 6 * SCALE), lab,
                    font=f_lab, fill=C["soft"])
        return img2
    return img


def _timeline_chart(spec: dict, theme: str):
    """A dated vertical timeline: date, marker, headline, one row per event.

    Horizontal was the obvious shape and it was wrong. Plotted along a time
    axis, the four July 2023 events landed on top of each other, their labels
    drifted onto neighbouring dots, and only two of six headlines had room —
    while two-thirds of the canvas sat empty above and below the axis. Twelve
    events with sentence-length labels are a LIST. Time still shows: the gap
    between rows is proportional, so a cluster reads as a cluster."""
    C = THEMES[theme]
    evs = sorted([e for e in spec["events"][:12] if e.get("date")],
                 key=lambda e: str(e.get("date")))
    img, d, (x0, y0, x1, y1) = _frame(spec["title"], spec.get("subtitle", ""),
                                      spec.get("source", ""), theme)
    if not evs:
        return img
    f_date = _font("mono", 11)
    f_head = _font("sans", 14)
    f_note = _font("mono", 10)
    date_w = 96 * SCALE
    rail_x = x0 + date_w + 14 * SCALE
    rows = len(evs)
    row_h = min(42 * SCALE, (y1 - y0) / max(1, rows))
    mx = max((e.get("weight") or 1) for e in evs) or 1
    d.line([rail_x, y0 + 6 * SCALE, rail_x, y0 + row_h * (rows - 1) + 8 * SCALE],
           fill=C["rule"], width=2 * SCALE)
    for i, e in enumerate(evs):
        cy = y0 + row_h * i + 8 * SCALE
        w = (e.get("weight") or 1) / mx
        r = (4 + 7 * w) * SCALE
        big = w >= 0.6
        d.text((x0, cy - 7 * SCALE), _short_date(str(e["date"])), font=f_date,
               fill=C["silt"] if big else C["soft"])
        d.ellipse([rail_x - r, cy - r, rail_x + r, cy + r],
                  fill=C["flood"] if big else C["deep"])
        tx = rail_x + 18 * SCALE
        head = (e.get("label") or "")[:76]
        d.text((tx, cy - 8 * SCALE), head, font=f_head, fill=C["ink"])
        if e.get("note"):
            nw = _tw(d, head, f_head)
            d.text((tx + nw + 10 * SCALE, cy - 6 * SCALE), str(e["note"])[:26],
                   font=f_note, fill=C["soft"])
    return img


def _ord(datestr: str) -> int:
    try:
        y, m, dd = str(datestr)[:10].split("-")
        return int(y) * 372 + int(m) * 31 + int(dd)
    except Exception:
        return 0


_MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct",
        "Nov", "Dec"]


def _short_date(d: str) -> str:
    try:
        y, m, dd = str(d)[:10].split("-")
        return f"{int(dd)} {_MON[int(m)-1]} {y[2:]}"
    except Exception:
        return str(d)


def _ledger_chart(spec: dict, theme: str):
    """Two facing columns — causes against consequences."""
    C = THEMES[theme]
    img, d, (x0, y0, x1, y1) = _frame(spec["title"], spec.get("subtitle", ""),
                                      spec.get("source", ""), theme)
    f_h = _font("mono", 12)
    f_i = _font("sans", 15)
    f_m = _font("mono", 10)
    mid = (x0 + x1) / 2
    d.line([mid, y0, mid, y1], fill=C["rule"], width=1 * SCALE)
    for col, (heading, rows, colour) in enumerate(
            [(spec.get("left_title", "Causes"), spec.get("left", []), C["flood"]),
             (spec.get("right_title", "Consequences"), spec.get("right", []), C["deep"])]):
        cx = x0 if col == 0 else mid + 24 * SCALE
        wmax = (mid - x0 - 24 * SCALE)
        y = y0
        d.text((cx, y), heading.upper(), font=f_h, fill=colour)
        y += 26 * SCALE
        for r in rows[:6]:
            d.rectangle([cx, y + 4 * SCALE, cx + 3 * SCALE, y + 20 * SCALE],
                        fill=colour)
            for line in _wrap(d, r.get("label", ""), f_i, wmax - 14 * SCALE)[:2]:
                d.text((cx + 12 * SCALE, y), line, font=f_i, fill=C["ink"])
                y += 20 * SCALE
            note = r.get("note") or ""
            if note:
                d.text((cx + 12 * SCALE, y), note[:52], font=f_m, fill=C["soft"])
                y += 17 * SCALE
            y += 8 * SCALE
    return img


def render(spec: dict, theme: str = "light") -> bytes:
    """spec -> PNG bytes. `spec['kind']` is one of KINDS."""
    global H
    kind = spec.get("kind", "bars")
    _h = H
    if kind == "timeline":
        # A twelve-row list needs more vertical room than a bar chart.
        H = max(520, 190 + 42 * min(12, len(spec.get("events") or [])))
    if kind not in KINDS:
        raise ValueError(f"kind must be one of {KINDS}")
    if kind in ("bars", "lollipop", "area", "heatstrip"):
        img = _series_chart(spec, theme, kind)
    elif kind == "timeline":
        img = _timeline_chart(spec, theme)
    elif kind == "ledger":
        img = _ledger_chart(spec, theme)
    else:
        img = _series_chart(spec, theme, "bars")
    H = _h
    buf = io.BytesIO()
    img.save(buf, format="PNG", optimize=True)
    return buf.getvalue()


# ═══════════════════════════ hosting ═════════════════════════════════════════
def _digest(spec: dict, theme: str) -> str:
    """Content hash. The same data renders to the same URL, so republishing an
    unchanged chart costs nothing and an article's image links stay stable."""
    import json as _j
    raw = _j.dumps({"spec": spec, "theme": theme}, sort_keys=True, default=str)
    return hashlib.sha1(raw.encode()).hexdigest()[:16]


def publish(spec: dict, themes=("light", "dark"), slug: str = "",
            upload: bool = True) -> dict:
    """Render and host. Returns the embeddable URLs.

    Both themes by default: a publisher embedding into a dark page should not
    get a white slab. The light URL is the one to use in an <img>; the pair is
    there for a <picture> element.

    Upload is scp to the Fliar web root. If it fails the render still succeeded
    — the payload carries the local paths and says the upload did not happen,
    because a chart that exists locally is recoverable and a silent failure is
    not."""
    slug = re.sub(r"[^a-z0-9]+", "-", (slug or spec.get("title", "chart")).lower()
                  ).strip("-")[:48] or "chart"
    out = {"slug": slug, "kind": spec.get("kind"), "images": {},
           "uploaded": False, 'verified': False}
    local = []
    for theme in themes:
        png = render(spec, theme=theme)
        name = f"{slug}-{_digest(spec, theme)}-{theme}.png"
        path = os.path.join(LOCAL_DIR, name)
        with open(path, "wb") as f:
            f.write(png)
        local.append((name, path))
        out["images"][theme] = {"file": name, "local_path": path,
                                "bytes": len(png),
                                "url": f"{FLIAR_URL}/{name}"}
    if upload and not FLIAR_HOST:
        out["note"] = "Rendered locally; set PRISM_CHART_HOST to publish chart images."
    elif upload:
        try:
            subprocess.run(["ssh", "-o", "ConnectTimeout=10",
                            "-o", "StrictHostKeyChecking=no", FLIAR_HOST,
                            f"mkdir -p {FLIAR_DIR}"], check=True,
                           capture_output=True, timeout=40)
            subprocess.run(["scp", "-o", "ConnectTimeout=10",
                            "-o", "StrictHostKeyChecking=no",
                            *[p for _, p in local], f"{FLIAR_HOST}:{FLIAR_DIR}/"],
                           check=True, capture_output=True, timeout=90)
            out["uploaded"] = True
            for name, path in local:
                with open(path, 'rb') as source_file:
                    expected = source_file.read()
                with urllib.request.urlopen(f'{FLIAR_URL}/{name}', timeout=30) as response:
                    actual = response.read(len(expected) + 1)
                    if response.status != 200 or actual != expected:
                        raise RuntimeError(f'public chart byte verification failed: {name}')
            out['verified'] = True
        except Exception as e:
            out["upload_error"] = f"{type(e).__name__}: {e}"
            out["note"] = 'Rendered locally; public delivery has not been verified.'
    out['available'] = out['verified'] if upload else True
    if not out['verified']:
        for item in out['images'].values():
            item['candidate_url'] = item.pop('url')
            item['url'] = None
    primary = out["images"].get("light") or list(out["images"].values())[0]
    out["url"] = primary["url"]
    out["embed_html"] = _embed(out, spec) if out['verified'] else ''
    out["embed_markdown"] = f'![{spec.get("title", "chart")}]({out["url"]})' if out['verified'] else ''
    return out


def _embed(out: dict, spec: dict) -> str:
    """A <picture> that respects the reader's theme, with a real alt and a
    caption carrying the source. Self-contained: no CSS required."""
    light = (out["images"].get("light") or {}).get("url", "")
    dark = (out["images"].get("dark") or {}).get("url", light)
    alt = (spec.get("alt") or spec.get("subtitle") or spec.get("title", "chart"))
    cap = spec.get("source", "")
    return (
        '<figure style="margin:2rem 0">'
        '<picture>'
        f'<source srcset="{dark}" media="(prefers-color-scheme: dark)">'
        f'<img src="{light}" alt="{_esc(alt)}" loading="lazy" '
        'style="width:100%;height:auto;border-radius:4px">'
        '</picture>'
        + (f'<figcaption style="font-size:.8rem;color:#666;margin-top:.5rem">'
           f'{_esc(cap)}</figcaption>' if cap else "")
        + "</figure>")


def _esc(s: str) -> str:
    import html as _h
    return _h.escape(str(s or ""))


# ═══════════════════════════ Prism data -> chart spec ════════════════════════
def from_season(season: dict, term: str = "", kind: str = "bars") -> dict:
    """`news.seasonality` -> a month-of-year chart."""
    if not (season or {}).get("available"):
        return {}
    top3 = set(season.get("top_three_months") or [])
    return {
        "kind": kind,
        "title": f"When {term or 'this'} peaks, and when it goes quiet".strip(),
        "subtitle": (f"Articles by calendar month, {season.get('from')} to "
                     f"{season.get('to')}. {season.get('reading', '')}"),
        "source": (f"Prism news corpus · {season.get('total', 0):,} articles · "
                   f"counts are floors"),
        "alt": (f"Bar chart of monthly article counts. Peak "
                f"{season['peak']['name']} at {season['peak']['articles']:,}; "
                f"trough {season['trough']['name']} at "
                f"{season['trough']['articles']:,}."),
        "points": [{"label": m["name"], "value": m["articles"]}
                   for m in season.get("months", [])],
        "highlight": list(top3),
    }


def from_events(events: list, term: str = "", window: str = "") -> dict:
    """`news.events` -> a dated timeline."""
    rows = [e for e in (events or []) if e.get("date")]
    if not rows:
        return {}
    return {
        "kind": "timeline",
        "title": "The days the newsrooms agreed on",
        "subtitle": (f"High-priority reports on {term}, sized by how many "
                     f"outlets ran the story that day."),
        "source": f"Prism news corpus · {len(rows)} events{(' · ' + window) if window else ''}",
        "alt": f"Timeline of {len(rows)} dated events with outlet counts.",
        "events": [{"date": e.get("date"),
                    "weight": e.get("reports_that_day") or 1,
                    "label": (e.get("title") or e.get("excerpt") or "")[:76],
                    "note": (f"{e.get('reports_that_day')} outlets"
                             if e.get("reports_that_day") else "")}
                   for e in rows],
    }


def from_factors(factors: dict, term: str = "") -> dict:
    """`compose.factors` -> a causes/consequences ledger."""
    causes = (factors or {}).get("causes") or []
    impacts = (factors or {}).get("impacts") or []
    if not (causes or impacts):
        return {}
    from . import articles as _a

    def row(c):
        pub = _a.masthead(c.get("publisher")) if c.get("publisher") else "one outlet"
        return {"label": c.get("factor", ""), "note": f"{pub} · {c.get('date', '')}"}
    return {
        "kind": "ledger",
        "title": "What the reporting says",
        "subtitle": ("Extracted from the opening of each high-priority report "
                     "and verified against it."),
        "source": (f"Prism news corpus · {len(causes)} causes, "
                   f"{len(impacts)} consequences"),
        "alt": f"Two columns: {len(causes)} causes and {len(impacts)} consequences.",
        "left_title": "Why it happens", "right_title": "What it does",
        "left": [row(c) for c in causes], "right": [row(c) for c in impacts],
    }


def from_growth(growth: dict, term: str = "", limit: int = 8) -> dict:
    """`news.keyword_growth` -> rising sub-themes as a bar chart."""
    rising = (growth or {}).get("rising") or []
    if not rising:
        return {}
    rows = rising[:limit]
    return {
        "kind": "bars",
        "title": "What the story is becoming about",
        "subtitle": (f"Sub-themes inside {term} coverage, by growth against the "
                     f"first half of the window."),
        "source": f"Prism news corpus · {len(rising)} rising themes",
        "alt": "Bar chart of the fastest-growing sub-themes.",
        "points": [{"label": r["label"][:16], "value": r["recent"]} for r in rows],
        "highlight": [rows[0]["label"][:16]] if rows else [],
    }


# ── research cards ───────────────────────────────────────────────────────────
# Every card above reads the news corpus. A research-led piece — a claim tested
# against the literature rather than a place tested against its coverage — had
# no card at all, so it silently shipped without a chart. These two read the
# research payloads instead.

_STANCE_LABEL = {"problem_identifying": "problem-finding",
                 "breakthrough": "breakthrough", "promising": "promising",
                 "descriptive": "descriptive", "comparative": "comparative",
                 "cautionary": "cautionary", "critical": "critical"}


def from_stance(stance: dict, term: str = "", limit: int = 7) -> dict:
    """`corpus_stance` -> how a literature leans, as a bar chart.

    This is the chart a reader needs most on a hyped subject: a field can be
    enormous and still be almost entirely promising rather than tested. Bars
    are ordered by size, and the cautionary/critical end is highlighted
    because that is the part a vendor deck leaves out."""
    o = (stance or {}).get("orientation") or {}
    rows = [(k, v) for k, v in o.items() if v]
    if not rows or (stance or {}).get("available") is False:
        return {}
    rows.sort(key=lambda x: -x[1])
    rows = rows[:limit]
    total = sum(v for _, v in (o or {}).items()) or 1
    crit = [_STANCE_LABEL.get(k, k) for k, _ in rows if k in ("cautionary", "critical")]
    papers = stance.get("papers") or total
    return {
        "kind": "bars",
        "title": "How this literature leans",
        "subtitle": (f"Every typed paper on {term}, by what the work is doing — "
                     f"not by what it concludes."),
        "source": (f"Fliar BI · Prism research corpus · {papers:,} papers · "
                   f"{stance.get('window', '')}"),
        "alt": ("Bar chart of research orientation: "
                + ", ".join(f"{_STANCE_LABEL.get(k, k)} {v:,}" for k, v in rows) + "."),
        "points": [{"label": _STANCE_LABEL.get(k, k)[:16], "value": v} for k, v in rows],
        "highlight": [c[:16] for c in crit],
    }


def from_verdicts(tally: dict, term: str = "") -> dict:
    """`tally.counts` -> what the documents actually read said about the claim.

    Deliberately separate from `from_stance`: that chart describes a whole
    literature's posture, this one describes the handful of papers that were
    read against one specific claim. Conflating the two is how "135,000 papers"
    becomes "135,000 papers agree"."""
    c = (tally or {}).get("counts") or {}
    order = [("supports", "supported"), ("qualifies", "qualified"),
             ("contradicts", "contradicted"), ("unrelated", "did not address")]
    pts = [{"label": lab, "value": int(c.get(k) or 0)} for k, lab in order]
    if not any(p["value"] for p in pts):
        return {}
    read = (tally or {}).get("read") or sum(p["value"] for p in pts)
    return {
        "kind": "bars",
        "title": "What the papers actually said",
        "subtitle": (f"Documents retrieved against the claim about {term}, "
                     f"by what each one was found to do with it."),
        "source": (f"Fliar BI · Prism · {sum(p['value'] for p in pts)} documents "
                   f"retrieved, {read} read in full"),
        "alt": ("Bar chart: "
                + ", ".join(f"{p['label']} {p['value']}" for p in pts) + "."),
        "points": pts,
        "highlight": ["did not address"] if c.get("unrelated") else [],
    }
