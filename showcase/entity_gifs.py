"""Animated GIFs for the entity pages: the drill-down sections drawn month by month.

    python3 showcase/entity_gifs.py      -> docs/gallery/gifs/<slug>-<n>.gif
"""
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from gifs import lines_gif, bars_gif  # noqa: E402

OUT = os.path.join(ROOT, "docs", "gallery", "gifs")
GIFS = [("reliance-industries-pulse", "partnership, artificial intelligence"), ("tata-motors-pulse", "electric vehicle"),
        ("modi-vs-trump", "india"), ("infosys-tcs-wipro", "artificial intelligence")]


def drills(slug):
    rec = json.load(open(os.path.join(ROOT, "docs", "examples", f"{slug}.json")))
    return [c for c in rec["calls"] if c.get("extra") and c["tool"] == "news_drill" and (c.get("response") or {}).get("ok")]


def main():
    os.makedirs(OUT, exist_ok=True)
    made = []
    for slug, scope in GIFS:
        ds = [c for c in drills(slug) if ", ".join(c["response"]["data"]["scope"]) == scope]
        if not ds:
            continue
        series = []
        for c in ds:
            d = c["response"]["data"]
            series.append((f"{c['args']['term'].title()} → {scope}", [(p["period"][2:7].replace("-", "/"), p["section_articles"]) for p in d["points"]]))
        out = os.path.join(OUT, f"{slug}-drill.gif")
        lines_gif(series, f"Drill-down: {scope}", out, subtitle="Articles per month inside the entity's coverage")
        made.append(out)
    for slug in ("reliance-industries-pulse", "tata-motors-pulse"):
        rec = json.load(open(os.path.join(ROOT, "docs", "examples", f"{slug}.json")))
        act = [c for c in rec["calls"] if c.get("extra") and c["tool"] == "news_activities" and (c.get("response") or {}).get("ok")]
        if act:
            ev = act[0]["response"]["data"].get("company_events") or {}
            if ev.get("available"):
                out = os.path.join(OUT, f"{slug}-events.gif")
                bars_gif([(r["event_type"], r["events"]) for r in ev["rows"][:9]], f"{act[0]['args']['term'].title()}: company events",
                         out, subtitle=f"Events extracted from business news, {ev['total']:,} in total")
                made.append(out)
    print("\n".join(made))


if __name__ == "__main__":
    main()
