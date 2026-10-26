"""Home-page block: an animated-GIF grid of topic and disease pages, each GIF linking to its written GitHub page.

    python3 showcase/readme_topics.py     (rewrites README.md between <!-- topics:start --> and <!-- topics:end -->)
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from topic_pages import TOPICS, HOST  # noqa: E402

FEATURED = ["cybercrime", "metro-rail", "startup-funding", "inflation", "electric-vehicles", "heatwaves",
            "red-sea-shipping", "ai-regulation", "upi-payments"]


def main():
    have = [s for s in TOPICS if os.path.exists(os.path.join(ROOT, "docs", "topics", s, "trend.gif"))]
    feat = [s for s in FEATURED if s in have] + [s for s in have if s not in FEATURED]
    cells = []
    for s in feat[:9]:
        title, dom = TOPICS[s][:2]
        w = json.load(open(os.path.join(ROOT, "docs", "topics", s, "writeup.json")))
        f = w["facts"].get("topic") or w["facts"]   # v2 write-ups nest the topic facts
        ov = f["overview"]
        cells.append(f'<td width="33%" valign="top"><a href="docs/topics/{s}/README.md"><img src="docs/topics/{s}/trend.gif" alt="{title}, animated"></a>'
                     f'<br><b><a href="docs/topics/{s}/README.md">{title}</a></b> · {dom}<br>'
                     f'<sub>{ov.get("articles"):,} articles · {ov.get("direction")} · {ov.get("neg_per_pos")} negative per positive · '
                     f'<a href="{HOST}/{s}/">interactive</a></sub></td>')
    rows = "".join("<tr>" + "".join(cells[i:i + 3]) + "</tr>" for i in range(0, len(cells), 3))
    by = {}
    for s in have:
        by.setdefault(TOPICS[s][1], []).append(f"[{TOPICS[s][0]}](docs/topics/{s}/README.md)")
    listing = "\n".join(f"- **{d}:** " + " · ".join(v) for d, v in by.items())
    block = f"""<!-- topics:start -->
## Topic intelligence: {len(have)} analytical pages

Each page is a topic intelligence report built from MCP calls: coverage and tone, the areas of activity and the top
tags behind its themes, **themes over five years** (heatmap, stacked mix and an animated theme race), world and India
maps, people and organisations, causes and impacts quoted from the reports, two sections drilled into, and a
month-by-month reading. On top of that, **three reader views** chosen by domain (for crime: policy makers, police &
enforcement, researchers; for finance: regulators, investors, researchers): trajectory with backtested scenarios and the
stories that matter; the evidence behind a claim, two claims head to head and a screen with quoted figures; the framing
of the literature, the frontier and its gaps. Each page also runs the **nine research exploration methods** and reads
each result in depth. Every GIF opens the GitHub page, and every page links to its interactive version.

<table>{rows}</table>

{listing}

[All topic pages](docs/topics/README.md) · [Disease pages](docs/diseases/README.md)
<!-- topics:end -->"""
    p = os.path.join(ROOT, "README.md")
    s = open(p).read()
    if "<!-- topics:start -->" in s:
        s = re.sub(r"<!-- topics:start -->.*?<!-- topics:end -->", lambda m: block, s, flags=re.S)
    else:
        s = s.replace("## Disease intelligence", block + "\n\n## Disease intelligence", 1)
    open(p, "w").write(s)
    print(f"{len(have)} topics, {len(cells)} in the grid")


if __name__ == "__main__":
    main()
