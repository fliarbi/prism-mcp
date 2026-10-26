"""Home-page block: investor briefs for global public companies, a GIF grid and one signals table.

    python3 showcase/readme_investors.py   (rewrites README.md between <!-- investors:start --> and <!-- investors:end -->)
"""
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
from investor_pages import COMPANIES, HOST, DISCLAIMER, signal_rows  # noqa: E402

FEATURED = ["apple", "nvidia", "tesla", "jpmorgan", "hsbc", "astrazeneca"]


def main():
    have = [s for s in COMPANIES if os.path.exists(os.path.join(ROOT, "docs", "investors", s, "writeup.json"))]
    W = {s: json.load(open(os.path.join(ROOT, "docs", "investors", s, "writeup.json"))) for s in have}
    cells = []
    for s in [x for x in FEATURED if x in have][:6]:
        name, lst = COMPANIES[s][:2]
        cells.append(f'<td width="33%" valign="top"><a href="docs/investors/{s}/README.md"><img src="docs/investors/{s}/{'theme-race.gif' if os.path.exists(os.path.join(ROOT, 'docs', 'investors', s, 'theme-race.gif')) else 'signals.gif'}" alt="{name}: themes and events"></a>'
                     f'<br><b><a href="docs/investors/{s}/README.md">{name}</a></b><br><sub>{lst} · <a href="{HOST}/{s}/">interactive</a></sub></td>')
    grid = "".join("<tr>" + "".join(cells[i:i + 3]) + "</tr>" for i in range(0, len(cells), 3))
    rows = []
    for s in have:
        S = W[s]["signals"]
        sig = {a: (b, c) for a, b, c in signal_rows(S)}
        a = sig.get("Attention", ("", "—"))
        t = sig.get("Tone", ("", "—"))
        r = sig.get("Risk events (lawsuits, regulatory, layoffs)", ("", "—"))
        c = sig.get("Catalyst events (products, contracts, M&A)", ("", "—"))
        secs = sorted(S.get("sections") or [], key=lambda x: -(x.get("last_third_vs_first") or 0))
        top = f"{secs[0]['section']} ({secs[0]['last_third_vs_first']}×)" if secs else "—"
        att = (S.get("attention") or {}).get("ratio")
        rows.append(f"| [{COMPANIES[s][0]}](docs/investors/{s}/README.md) | {COMPANIES[s][1]} | {a[1]} ({att}×) | {t[1]} | {r[1]} | {c[1]} | {top} |")
    block = f"""<!-- investors:start -->
## Investor briefs: global public companies

For investors and stock buyers, Prism turns a company's coverage into decision inputs: is attention building or fading,
is the tone turning, are risk events (lawsuits, regulatory action, layoffs) rising against catalyst events (new
products, contracts, M&A), which risk and catalyst sections are growing inside its coverage, how it stands against its
peers, and what happened month by month. Each brief has a written analysis and a "what to watch" list.

<table>{grid}</table>

| Company | Listing | Attention, last 3 months vs 3 before | Tone | Risk events, 6 months | Catalyst events, 6 months | Fastest-growing section |
| --- | --- | --- | --- | --- | --- | --- |
{chr(10).join(rows)}

> {DISCLAIMER}

[All investor briefs](docs/investors/README.md) · Indian listed companies: [Reliance Industries](docs/use-cases/entities/reliance-industries-pulse.md),
[HDFC Bank](docs/use-cases/entities/hdfc-bank-pulse.md), [Tata Motors](docs/use-cases/entities/tata-motors-pulse.md), [Infosys vs TCS vs Wipro](docs/use-cases/entities/infosys-tcs-wipro.md)
<!-- investors:end -->"""
    p = os.path.join(ROOT, "README.md")
    s = open(p).read()
    if "<!-- investors:start -->" in s:
        s = re.sub(r"<!-- investors:start -->.*?<!-- investors:end -->", lambda m: block, s, flags=re.S)
    else:
        s = s.replace("## More than a news trend", block + "\n\n## More than a news trend", 1)
    s = s.replace("### Public companies\n", "### Indian public companies\n", 1)
    open(p, "w").write(s)
    print(f"{len(have)} briefs in the table, {len(cells)} in the grid")


if __name__ == "__main__":
    main()
