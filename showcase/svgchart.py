"""Static SVG charts for the showcase pages, readable in GitHub's light and dark themes.

Every chart is a self-contained SVG with its colours as CSS variables and a
prefers-color-scheme block, so the same file works on a light or dark README.
Palette: the validated default categorical order (blue, orange, aqua, yellow),
light and dark steps; text never wears a series colour. Each chart has a title
that names a single series and a legend once there are two or more; the page
under each chart repeats the numbers as a table (the accessible view).
"""
from html import escape

W = 760
STYLE = """<style>
svg{--bg:#fcfcfb;--ink:#0b0b0b;--ink2:#52514e;--ink3:#8a8984;--grid:#e6e5e0;--axis:#c9c8c2;
--s1:#2a78d6;--s2:#eb6834;--s3:#1baf7a;--s4:#eda100;--neu:#b9b8b1;--band:#2a78d633}
@media (prefers-color-scheme: dark){svg{--bg:#1a1a19;--ink:#f0efec;--ink2:#c3c2b7;--ink3:#8f8e86;--grid:#2e2e2b;
--axis:#4a4945;--s1:#3987e5;--s2:#d95926;--s3:#199e70;--s4:#c98500;--neu:#5c5b55;--band:#3987e540}}
text{font-family:-apple-system,BlinkMacSystemFont,"Segoe UI",Helvetica,Arial,sans-serif;fill:var(--ink)}
.t{font-size:17px;font-weight:600}.st{font-size:12.5px;fill:var(--ink2)}.src{font-size:11px;fill:var(--ink3)}
.ax{font-size:11px;fill:var(--ink2)}.lb{font-size:12px;fill:var(--ink)}.v{font-size:11.5px;fill:var(--ink2)}
.g{stroke:var(--grid);stroke-width:1}.a{stroke:var(--axis);stroke-width:1}
.c1{fill:var(--s1)}.c2{fill:var(--s2)}.c3{fill:var(--s3)}.c4{fill:var(--s4)}.cn{fill:var(--neu)}
.l1{stroke:var(--s1)}.l2{stroke:var(--s2)}.l3{stroke:var(--s3)}.l4{stroke:var(--s4)}
.ln{fill:none;stroke-width:2;stroke-linejoin:round;stroke-linecap:round}
.bg{fill:var(--bg);stroke:var(--grid)}
</style>"""


def _fmt(v):
    if v is None:
        return "–"
    if isinstance(v, float) and not v.is_integer():
        return f"{v:,.1f}"
    v = float(v)
    if abs(v) >= 1e6:
        return f"{v/1e6:,.1f}M"
    if abs(v) >= 1e4:
        return f"{v/1e3:,.0f}k"
    return f"{v:,.0f}"


def _nice(mx):
    if mx <= 0:
        return 1
    import math
    e = 10 ** math.floor(math.log10(mx))
    for m in (1, 1.2, 1.5, 2, 2.5, 3, 4, 5, 6, 8, 10):
        if m * e >= mx:
            return m * e
    return 10 * e


def _frame(h, title, subtitle, source, body, legend=""):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {h}" width="{W}" height="{h}" '
            f'role="img" aria-label="{escape(title)}">{STYLE}'
            f'<rect class="bg" x="0.5" y="0.5" width="{W-1}" height="{h-1}" rx="10"/>'
            f'<text class="t" x="24" y="34">{escape(title)}</text>'
            f'<text class="st" x="24" y="54">{escape(subtitle or "")}</text>{legend}{body}'
            f'<text class="src" x="24" y="{h-14}">{escape(source or "")}</text></svg>')


def _legend(names, y=72, x=24, shapes=None):
    out, cx = [], x
    for i, n in enumerate(names):
        cls = f"c{i+1}"
        out.append(f'<rect class="{cls}" x="{cx}" y="{y-9}" width="12" height="12" rx="3"/>'
                   f'<text class="lb" x="{cx+18}" y="{y+1}">{escape(n)}</text>')
        cx += 30 + 7.2 * len(n)
    return "".join(out)


def line_chart(series, title, subtitle="", source="", fmt=_fmt, x_every=None):
    """series: [(name, [(xlabel, value), ...])] sharing x labels. Up to 4 series."""
    series = [s for s in series if s[1]][:4]
    if not series:
        return None
    h, top = 330, (92 if len(series) > 1 else 74)
    left, right, bottom = 64, W - 24, h - 58
    xs = [p[0] for p in series[0][1]]
    n = len(xs)
    mx = _nice(max((v or 0) for _, pts in series for _, v in pts) or 1)
    def X(i): return left + (right - left) * (i / max(1, n - 1))
    def Y(v): return bottom - (bottom - top) * ((v or 0) / mx)
    body = []
    for k in range(5):
        v = mx * k / 4
        y = Y(v)
        body.append(f'<line class="{"a" if k == 0 else "g"}" x1="{left}" x2="{right}" y1="{y:.1f}" y2="{y:.1f}"/>'
                    f'<text class="ax" x="{left-8}" y="{y+4:.1f}" text-anchor="end">{fmt(v)}</text>')
    step = x_every or max(1, round(n / 8))
    for i, xl in enumerate(xs):
        if i % step == 0 or i == n - 1:
            body.append(f'<text class="ax" x="{X(i):.1f}" y="{bottom+18}" text-anchor="middle">{escape(str(xl))}</text>')
    for si, (name, pts) in enumerate(series):
        d = " ".join(f'{"M" if i == 0 else "L"}{X(i):.1f},{Y(v):.1f}' for i, (_, v) in enumerate(pts))
        body.append(f'<path class="ln l{si+1}" d="{d}"/>')
        # direct label at the peak of each series, value only
        pi = max(range(len(pts)), key=lambda i: pts[i][1] or 0)
        body.append(f'<circle class="c{si+1}" cx="{X(pi):.1f}" cy="{Y(pts[pi][1]):.1f}" r="4.5" '
                    f'stroke="var(--bg)" stroke-width="2"/>'
                    f'<text class="v" x="{X(pi):.1f}" y="{Y(pts[pi][1])-10:.1f}" text-anchor="middle">{fmt(pts[pi][1])}</text>')
    legend = _legend([s[0] for s in series], y=76) if len(series) > 1 else ""
    return _frame(h, title, subtitle, source, "".join(body), legend)


def hbar_chart(rows, title, subtitle="", source="", fmt=_fmt, cls="c1", max_rows=10, suffix=""):
    """rows: [(label, value)] largest first."""
    rows = [r for r in rows if r[1] is not None][:max_rows]
    if not rows:
        return None
    bh, gap, top = 22, 8, 74
    h = top + len(rows) * (bh + gap) + 40
    lw = min(250, max(90, 7 * max(len(str(r[0])) for r in rows)))
    left, right = 24 + lw, W - 80
    mx = max(r[1] for r in rows) or 1
    body = [f'<line class="a" x1="{left}" x2="{left}" y1="{top-6}" y2="{top+len(rows)*(bh+gap)-gap+6}"/>']
    for i, (lab, v) in enumerate(rows):
        y = top + i * (bh + gap)
        w = max(2, (right - left) * v / mx)
        lab = str(lab)
        lab = lab if len(lab) <= 38 else lab[:36] + "…"
        body.append(f'<text class="lb" x="{left-10}" y="{y+bh/2+4}" text-anchor="end">{escape(lab)}</text>'
                    f'<rect class="{cls}" x="{left}" y="{y}" width="{w:.1f}" height="{bh}" rx="4"/>'
                    f'<text class="v" x="{left+w+8:.1f}" y="{y+bh/2+4}">{fmt(v)}{suffix}</text>')
    return _frame(h, title, subtitle, source, "".join(body))


def share_bar(parts, title, subtitle="", source=""):
    """parts: [(label, value, cls)] drawn as one 100% bar with a legend; cls in c1..c4,cn."""
    parts = [p for p in parts if p[1]]
    tot = sum(p[1] for p in parts)
    if not tot:
        return None
    h, left, right, y = 170, 24, W - 24, 92
    body, x = [], left
    for lab, v, cls in parts:
        w = (right - left) * v / tot
        body.append(f'<rect class="{cls}" x="{x:.1f}" y="{y}" width="{max(0, w-2):.1f}" height="30" rx="4"/>')
        if w > 46:
            body.append(f'<text class="v" x="{x+w/2:.1f}" y="{y+48}" text-anchor="middle">{100*v/tot:.0f}%</text>')
        x += w
    leg, cx = [], 24
    for lab, v, cls in parts:
        leg.append(f'<rect class="{cls}" x="{cx}" y="{67}" width="12" height="12" rx="3"/>'
                   f'<text class="lb" x="{cx+18}" y="{77}">{escape(lab)} ({_fmt(v)})</text>')
        cx += 44 + 7.2 * (len(lab) + len(_fmt(v)))
    return _frame(h, title, subtitle, source, "".join(body), "".join(leg))


def range_chart(observed, scenarios, title, subtitle="", source=""):
    """observed: [(year, value)]; scenarios: [(year, central, low, high)]."""
    if not observed:
        return None
    h, top = 330, 92
    left, right, bottom = 64, W - 24, h - 58
    allx = [o[0] for o in observed] + [s[0] for s in scenarios]
    n = len(allx)
    mx = _nice(max([o[1] or 0 for o in observed] + [s[3] or s[1] or 0 for s in scenarios]) or 1)
    slot = (right - left) / n
    def Y(v): return bottom - (bottom - top) * ((v or 0) / mx)
    body = []
    for k in range(5):
        v = mx * k / 4
        body.append(f'<line class="{"a" if k == 0 else "g"}" x1="{left}" x2="{right}" y1="{Y(v):.1f}" y2="{Y(v):.1f}"/>'
                    f'<text class="ax" x="{left-8}" y="{Y(v)+4:.1f}" text-anchor="end">{_fmt(v)}</text>')
    for i, (yr, v) in enumerate(observed):
        x = left + i * slot + slot * 0.18
        body.append(f'<rect class="c1" x="{x:.1f}" y="{Y(v):.1f}" width="{slot*0.64:.1f}" height="{bottom-Y(v):.1f}" rx="4"/>'
                    f'<text class="ax" x="{x+slot*0.32:.1f}" y="{bottom+18}" text-anchor="middle">{yr}</text>')
    for j, (yr, c, lo, hi) in enumerate(scenarios):
        i = len(observed) + j
        x = left + i * slot + slot * 0.18
        lo, hi = lo if lo is not None else c, hi if hi is not None else c
        body.append(f'<rect fill="var(--band)" x="{x:.1f}" y="{Y(hi):.1f}" width="{slot*0.64:.1f}" height="{max(2, Y(lo)-Y(hi)):.1f}" rx="4"/>'
                    f'<line class="l2" stroke-width="3" x1="{x:.1f}" x2="{x+slot*0.64:.1f}" y1="{Y(c):.1f}" y2="{Y(c):.1f}"/>'
                    f'<text class="ax" x="{x+slot*0.32:.1f}" y="{bottom+18}" text-anchor="middle">{yr}</text>')
    legend = ('<rect class="c1" x="24" y="67" width="12" height="12" rx="3"/><text class="lb" x="42" y="77">observed</text>'
              '<rect class="c2" x="130" y="71" width="14" height="4" rx="2"/><text class="lb" x="150" y="77">scenario central</text>'
              '<rect fill="var(--band)" x="276" y="67" width="12" height="12" rx="3"/><text class="lb" x="294" y="77">sensitivity range</text>')
    return _frame(h, title, subtitle, source, "".join(body), legend)


def scoreboard(totals, title, subtitle="", source="", scale=25):
    """totals: {condition: score/scale}. Claude = slot 1, ChatGPT = slot 2; memory-only bars are hollow."""
    order = [("claude_prism", "Claude + Prism", "c1", True), ("chatgpt_prism", "ChatGPT + Prism", "c2", True),
             ("claude_bare", "Claude alone", "c1", False), ("chatgpt_bare", "ChatGPT alone", "c2", False)]
    rows = [(lab, totals.get(k), cls, solid) for k, lab, cls, solid in order if totals.get(k) is not None]
    if not rows:
        return None
    bh, gap, top = 24, 9, 96
    h = top + len(rows) * (bh + gap) + 40
    left, right = 170, W - 80
    body = []
    for k in range(6):
        x = left + (right - left) * k / 5
        body.append(f'<line class="g" x1="{x:.1f}" x2="{x:.1f}" y1="{top-6}" y2="{top+len(rows)*(bh+gap)-gap+4}"/>'
                    f'<text class="ax" x="{x:.1f}" y="{top-12}" text-anchor="middle">{k*scale//5}</text>')
    for i, (lab, v, cls, solid) in enumerate(rows):
        y = top + i * (bh + gap)
        w = (right - left) * v / scale
        col = cls.replace("c", "--s")
        rect = (f'<rect class="{cls}" x="{left}" y="{y}" width="{w:.1f}" height="{bh}" rx="4"/>' if solid else
                f'<rect x="{left+1}" y="{y+1}" width="{max(0, w-2):.1f}" height="{bh-2}" rx="4" fill="none" '
                f'stroke="var({col})" stroke-width="2" stroke-dasharray="5 3"/>')
        body.append(f'<text class="lb" x="{left-10}" y="{y+bh/2+4}" text-anchor="end">{escape(lab)}</text>{rect}'
                    f'<text class="v" x="{left+w+8:.1f}" y="{y+bh/2+4}">{v}/{scale}</text>')
    return _frame(h, title, subtitle, source, "".join(body))


def save(svg, path):
    if svg:
        with open(path, "w") as f:
            f.write(svg)
        return True
    return False
