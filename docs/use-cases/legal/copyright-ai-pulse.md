# AI copyright lawsuits

[Legal & compliance](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** IP-litigation tracking for an AI company.  
> **Why it is hard.** NYT v OpenAI and the Anthropic authors settlement are recent; recency is the test.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [copyright-ai-pulse.json](../../examples/copyright-ai-pulse.json).

**The question:**

> What is the coverage of copyright lawsuits against AI companies?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “ai copyright”, Jun 2024 – May 2026 | 386 |
| Critical coverage (priority 7–9) | 162 (42%) |
| Peak month | Feb 2026 (161 articles) |
| Last third of the window vs first third | 6.59× (rising) |
| Negative · positive | 81.9% · 14.8% |
| Tone vs all news (negative-to-positive ratio) | 5.54 vs 0.58 baseline: *markedly more negative than ordinary news coverage* |
| What Prism thinks “ai copyright” is | topic |

![Monthly coverage of ai copyright](../img/copyright-ai-pulse-trend.svg)

![Tone of ai copyright coverage](../img/copyright-ai-pulse-tone.svg)

![Countries in ai copyright coverage](../img/copyright-ai-pulse-geo.svg)

![Themes in ai copyright coverage](../img/copyright-ai-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “ai copyright” coverage (they also name the companies, people and places it is written about with): meta (222), u.s (156), cap (156), nil (155), games (155), the super bowl (155), olympic (155), las vegas (155), copyright (62), paul mccartney (29), intellectual property (22), uk government (21)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| aerovironment | kate bush | united states |
| ncl | elton john | colombia |
| university of washington | peter kyle | united kingdom |
| paralympic | paul mccartney | india |
| meta | damon albarn | canada |
| southern university at new orleans | dua lipa | japan |

**Top publishers in a 1-article sample:** globalfintechseries.com (100%)

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 2 | 2 | 2 | 0 |
| Jul 2024 | 1 | 0 | 1 | 0 |
| Aug 2024 | 2 | 2 | 1 | 1 |
| Sep 2024 | 5 | 4 | 5 | 0 |
| Oct 2024 | 2 | 1 | 1 | 0 |
| Nov 2024 | 3 | 2 | 1 | 2 |
| Dec 2024 | 6 | 6 | 3 | 3 |
| Jan 2025 | 13 | 12 | 10 | 3 |
| Feb 2025 | 21 | 14 | 20 | 0 |
| Mar 2025 | 24 | 14 | 16 | 8 |
| Apr 2025 | 7 | 2 | 3 | 4 |
| May 2025 | 23 | 19 | 20 | 3 |
| Jun 2025 | 22 | 17 | 16 | 6 |
| Jul 2025 | 6 | 3 | 5 | 1 |
| Aug 2025 | 10 | 9 | 4 | 6 |
| Sep 2025 | 15 | 6 | 6 | 2 |
| Oct 2025 | 9 | 7 | 7 | 2 |
| Nov 2025 | 6 | 5 | 5 | 1 |
| Dec 2025 | 12 | 9 | 6 | 6 |
| Jan 2026 | 9 | 3 | 4 | 2 |
| Feb 2026 | 161 | 1 | 156 | 5 |
| Mar 2026 | 15 | 13 | 13 | 1 |
| Apr 2026 | 4 | 4 | 3 | 1 |
| May 2026 | 8 | 7 | 8 | 0 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/copyright-ai-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 5.0 | 4.5 | 2.0 | 0.0 |
| Visualisation from counted data | 4.0 | 3.0 | 1.0 | 0.5 |
| Exploration and drill-down | 2.5 | 3.0 | 1.5 | 1.0 |
| Data export with provenance | 4.0 | 4.0 | 1.0 | 1.0 |
| Reproducibility | 5.0 | 4.0 | 0.0 | 1.0 |
| Traceable references | 1.0 | 1.0 | 1.5 | 0.0 |
| Accuracy against the corpus | 4.0 | 4.0 | 2.5 | 2.0 |
| Calibration and limits | 4.5 | 4.0 | 3.0 | 2.5 |
| Decision-grade verdict | 4.0 | 4.0 | 2.5 | 1.0 |
| Facet coverage | 4.5 | 4.0 | 1.0 | 0.5 |
| **Score /100** | **79.3** | 72.5 | 30.9 | 18.2 |

**Claude Opus judge:** A and C both grounded the answer in the traced news series and correctly said it measures topic attention, not lawsuits. A went further: it identified the Feb 2026 spike as an off-topic syndicated cluster (and the Colombia artefact) and recomputed trend and tone without it, making it decision-grade. D supplied the recent litigation facts from labelled memory but measured no coverage, and B declined entirely.

**GPT judge:** B is the strongest decision aid: it quantifies the news trend, exposes the anomalous February spike, and separates topic mentions from actual lawsuit counts. A is also careful about that core limitation, but B better uses the critical-series decomposition and covers more of the available facets.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/copyright-ai-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/copyright-ai-pulse.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is the coverage of copyright lawsuits against AI companies?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "ai copyright", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'ai copyright', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
