# Google antitrust coverage

[Legal & compliance](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Litigation and enforcement monitoring.  
> **Why it is hard.** Google search ruling (2024) and remedies (2025) are post-training for many models.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [antitrust-big-tech.json](../../examples/antitrust-big-tech.json).

**The question:**

> What is the news saying about the antitrust cases against Google: search, ad tech and the remedies?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “google antitrust”, Jun 2024 – May 2026 | 103 |
| Critical coverage (priority 7–9) | 87 (84.5%) |
| Peak month | Aug 2024 (15 articles) |
| Last third of the window vs first third | 0.13× (falling) |
| Negative · positive | 70.9% · 23.3% |
| Tone vs all news (negative-to-positive ratio) | 3.04 vs 0.58 baseline: *markedly more negative than ordinary news coverage* |
| What Prism thinks “google antitrust” is | topic |

![Monthly coverage of google antitrust](../img/antitrust-big-tech-trend.svg)

![Tone of google antitrust coverage](../img/antitrust-big-tech-tone.svg)

![Countries in google antitrust coverage](../img/antitrust-big-tech-geo.svg)

![Themes in google antitrust coverage](../img/antitrust-big-tech-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “google antitrust” coverage (they also name the companies, people and places it is written about with): google (102), apple (49), doj (37), microsoft (31), chrome (27), android (24), safari (17), the department of justice (16), big tech (10), iphones (9), google search (9), alphabet (9)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| adtech | sundar pichai | united states |
| bing | abhay and rani bang | south korea |
| united states department of justice | wayne gretzky | colombia |
| google | marc benioff | india |
| sirius satellite radio | pavel durov | china |
| news corp | jim cramer | spain |

**Top publishers in a 8-article sample:** appleworld.today (37.5%), techjuice.pk (12.5%), progressivepolicy.org (12.5%), tomshardware.com (12.5%), beebom.com (12.5%), beforeitsnews.com (12.5%)

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 2 | 2 | 2 | 0 |
| Jul 2024 | 5 | 4 | 5 | 0 |
| Aug 2024 | 15 | 13 | 12 | 3 |
| Sep 2024 | 14 | 14 | 12 | 1 |
| Oct 2024 | 13 | 12 | 11 | 2 |
| Nov 2024 | 4 | 4 | 4 | 0 |
| Dec 2024 | 1 | 1 | 1 | 0 |
| Jan 2025 | 1 | 1 | 0 | 1 |
| Feb 2025 | 0 | 0 | 0 | 0 |
| Mar 2025 | 2 | 2 | 1 | 1 |
| Apr 2025 | 6 | 5 | 4 | 2 |
| May 2025 | 13 | 9 | 8 | 4 |
| Jun 2025 | 6 | 5 | 3 | 3 |
| Jul 2025 | 4 | 2 | 1 | 1 |
| Aug 2025 | 0 | 0 | 0 | 0 |
| Sep 2025 | 10 | 9 | 5 | 5 |
| Oct 2025 | 1 | 1 | 1 | 0 |
| Nov 2025 | 1 | 0 | 0 | 0 |
| Dec 2025 | 1 | 1 | 1 | 0 |
| Jan 2026 | 0 | 0 | 0 | 0 |
| Feb 2026 | 1 | 0 | 0 | 0 |
| Mar 2026 | 1 | 1 | 1 | 0 |
| Apr 2026 | 0 | 0 | 0 | 0 |
| May 2026 | 2 | 1 | 1 | 1 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/antitrust-big-tech-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.0 | 4.0 | 1.0 | 0.5 |
| Visualisation from counted data | 3.0 | 3.0 | 1.0 | 0.0 |
| Exploration and drill-down | 2.5 | 2.5 | 1.0 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.5 | 4.5 | 1.0 | 1.0 |
| Traceable references | 1.0 | 2.0 | 1.0 | 0.5 |
| Accuracy against the corpus | 3.5 | 4.0 | 2.5 | 3.0 |
| Calibration and limits | 4.0 | 4.0 | 3.0 | 3.0 |
| Decision-grade verdict | 3.5 | 3.5 | 2.5 | 2.0 |
| Facet coverage | 4.0 | 3.5 | 1.5 | 0.5 |
| **Score /100** | 68.3 | **70.5** | 31.0 | 22.7 |

**Claude Opus judge:** A and B both read the measured corpus correctly: a 103-article volume that peaked in August 2024 and faded, with tone 5.24x more negative than baseline. A edges ahead with richer decomposition (critical share, secondary bumps) and by flagging label anomalies such as Colombia and incidental people. Both are honest that ad tech is effectively unmeasured and that the five months before today are missing. C gives useful case milestones from memory, but nothing about what the news measured; D offers almost nothing.

**GPT judge:** C gives the broadest traceable picture of coverage, tone, themes and headlines, and clearly flags the stale window and thin publisher sample. A is more restrained, but neither establishes what current reporting says about the search and ad-tech remedies; C’s unsupported links between tags or volume bumps and case coverage keep its conclusion tentative.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/antitrust-big-tech/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/antitrust-big-tech.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is the news saying about the antitrust cases against Google: search, ad tech and the remedies?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "google antitrust", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'google antitrust', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
