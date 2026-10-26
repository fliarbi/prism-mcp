"""Animated GIFs of Prism visualisations: lines that draw themselves, bars that grow into their ranking.

Palette and marks follow the showcase charts (blue, orange, aqua, yellow; 2px lines; light surface). Every GIF
ends on a held final frame with the source line, so it reads as a chart, not a loop of motion.

    from gifs import lines_gif, bars_gif
    lines_gif([("Narendra Modi", [("2024-06", 23000), ...]), ...], "Monthly coverage", "out.gif")
"""
import math

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.animation import FuncAnimation, PillowWriter  # noqa: E402

PAL = ["#2a78d6", "#eb6834", "#1baf7a", "#eda100"]
INK, INK2, GRID, BG = "#0b0b0b", "#52514e", "#e6e5e0", "#fcfcfb"


def _fig(title, subtitle, w=7.2, h=4.0):
    fig, ax = plt.subplots(figsize=(w, h), dpi=100)
    fig.patch.set_facecolor(BG)
    ax.set_facecolor(BG)
    fig.text(0.04, 0.95, title, fontsize=14, fontweight="bold", color=INK, va="top")
    if subtitle:
        fig.text(0.04, 0.885, subtitle, fontsize=9.5, color=INK2, va="top")
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.spines["bottom"].set_color("#c9c8c2")
    ax.tick_params(colors=INK2, labelsize=8.5, length=0)
    return fig, ax


def _fmt(v):
    return f"{v/1e6:.1f}M" if v >= 1e6 else f"{v/1e3:.0f}k" if v >= 1e3 else f"{v:.0f}"


def lines_gif(series, title, path, subtitle="", source="Source: Prism MCP", frames=40, hold=14):
    """series: [(name, [(label, value), ...])] sharing x labels (up to 4)."""
    series = [s for s in series if s[1]][:4]
    xs = [p[0] for p in series[0][1]]
    n = len(xs)
    top = max(v for _, pts in series for _, v in pts) * 1.15
    fig, ax = _fig(title, subtitle)
    fig.subplots_adjust(left=0.1, right=0.97, top=0.78, bottom=0.16)
    ax.set_xlim(0, n - 1)
    ax.set_ylim(0, top)
    ax.yaxis.grid(True, color=GRID, lw=1)
    ax.set_axisbelow(True)
    ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda v, _: _fmt(v)))
    step = max(1, round(n / 7))
    ax.set_xticks(range(0, n, step))
    ax.set_xticklabels([xs[i] for i in range(0, n, step)])
    fig.text(0.04, 0.03, source, fontsize=8, color="#8a8984")
    lines = [ax.plot([], [], color=PAL[i], lw=2.2, solid_capstyle="round", label=name)[0]
             for i, (name, _) in enumerate(series)]
    dots = [ax.plot([], [], "o", color=PAL[i], ms=6, mec=BG, mew=1.5)[0] for i in range(len(series))]
    labels = [ax.text(0, 0, "", fontsize=9, color=INK2, va="bottom", ha="left") for _ in series]
    if len(series) > 1:
        ax.legend(loc="upper left", bbox_to_anchor=(0, 1.13), ncol=len(series), frameon=False, fontsize=9,
                  labelcolor=INK)

    def draw(f):
        k = min(n, max(1, math.ceil(n * min(1, (f + 1) / frames))))
        for i, (_, pts) in enumerate(series):
            ys = [v for _, v in pts[:k]]
            lines[i].set_data(range(k), ys)
            dots[i].set_data([k - 1], [ys[-1]])
            labels[i].set_position((min(k - 1, n - 1.8), ys[-1] + top * 0.02))
            labels[i].set_text(_fmt(ys[-1]))
        return lines + dots + labels
    anim = FuncAnimation(fig, draw, frames=frames + hold, interval=70, blit=False)
    anim.save(path, writer=PillowWriter(fps=14))
    plt.close(fig)
    return path


def bars_gif(rows, title, path, subtitle="", source="Source: Prism MCP", frames=30, hold=16, unit="",
             second=None, second_label=""):
    """rows: [(label, value)] largest first (up to 10). `second`: optional [(label, value)] drawn as an inner
    darker bar (e.g. the high-tier part of each total)."""
    rows = rows[:10]
    labs = [r[0] for r in rows][::-1]
    vals = [r[1] for r in rows][::-1]
    sec = dict(second or [])
    fig, ax = _fig(title, subtitle, h=max(3.4, 0.42 * len(rows) + 1.6))
    fig.subplots_adjust(left=0.32, right=0.93, top=0.8, bottom=0.12)
    mx = max(vals) * 1.18
    ax.set_xlim(0, mx)
    ax.set_yticks(range(len(labs)))
    ax.set_yticklabels([l if len(l) <= 34 else l[:32] + "…" for l in labs], fontsize=9, color=INK)
    ax.set_xticks([])
    fig.text(0.04, 0.025, source, fontsize=8, color="#8a8984")
    bars = ax.barh(range(len(labs)), [0] * len(labs), color=PAL[0], height=0.62)
    inner = ax.barh(range(len(labs)), [0] * len(labs), color=PAL[1], height=0.62) if sec else None
    txt = [ax.text(0, i, "", va="center", fontsize=8.5, color=INK2) for i in range(len(labs))]
    if sec:
        from matplotlib.patches import Patch
        ax.legend(handles=[Patch(color=PAL[0], label="all claims"), Patch(color=PAL[1], label=second_label)],
                  loc="lower right", frameon=False, fontsize=8.5)

    def draw(f):
        t = min(1, (f + 1) / frames)
        e = 1 - (1 - t) ** 3
        for i, b in enumerate(bars):
            v = vals[i] * e
            b.set_width(v)
            if inner is not None:
                inner[i].set_width(sec.get(labs[i], 0) * e)
            txt[i].set_position((v + mx * 0.01, i))
            txt[i].set_text(f"{_fmt(vals[i] * e) if vals[i] >= 1000 else round(vals[i] * e)}{unit}")
        return list(bars) + txt
    anim = FuncAnimation(fig, draw, frames=frames + hold, interval=70, blit=False)
    anim.save(path, writer=PillowWriter(fps=14))
    plt.close(fig)
    return path


def race_gif(frames_by_label, title, path, subtitle="", source="Source: Prism MCP", steps=10, hold=8):
    """A bar-chart race: frames_by_label = {"2021": [(label, value), ...], "2022": [...], ...} (same labels each frame).
    Bars glide between frames and re-sort; the frame label is drawn large in the corner."""
    keys = list(frames_by_label)
    labels = [l for l, _ in frames_by_label[keys[0]]]
    vals = [{l: v for l, v in frames_by_label[k]} for k in keys]
    mx = max(max(v.values()) for v in vals) * 1.18 or 1
    n = len(labels)
    fig, ax = _fig(title, subtitle, h=max(3.6, 0.42 * n + 1.7))
    fig.subplots_adjust(left=0.3, right=0.93, top=0.8, bottom=0.08)
    fig.text(0.04, 0.02, source, fontsize=8, color="#8a8984")
    big = fig.text(0.9, 0.12, "", fontsize=30, fontweight="bold", color="#c9c8c2", ha="right")
    colors = {l: PAL[i % len(PAL)] for i, l in enumerate(labels)}
    seq = []
    for i in range(len(keys) - 1):
        for s in range(steps):
            t = s / steps
            seq.append((keys[i] if t < 0.5 else keys[i + 1], {l: vals[i][l] * (1 - t) + vals[i + 1][l] * t for l in labels}))
    seq += [(keys[-1], vals[-1])] * hold

    def draw(f):
        ax.clear()
        ax.set_facecolor(BG)
        for s_ in ("top", "right", "left", "bottom"):
            ax.spines[s_].set_visible(False)
        lab, cur = seq[f]
        order = sorted(labels, key=lambda l: cur[l])
        ax.barh(range(n), [cur[l] for l in order], color=[colors[l] for l in order], height=0.66)
        ax.set_yticks(range(n))
        ax.set_yticklabels([l if len(l) <= 30 else l[:28] + "…" for l in order], fontsize=9, color=INK)
        ax.set_xlim(0, mx)
        ax.set_xticks([])
        ax.tick_params(length=0)
        for i, l in enumerate(order):
            ax.text(cur[l] + mx * 0.01, i, f"{cur[l]:.1f}%", va="center", fontsize=8.5, color=INK2)
        big.set_text(lab)
        return []
    anim = FuncAnimation(fig, draw, frames=len(seq), interval=90, blit=False)
    anim.save(path, writer=PillowWriter(fps=11))
    plt.close(fig)
    return path
