# Layoffs in the news

[Education & labour](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Labour-market sentiment monitoring.  
> **Why it is hard.** Tech layoffs dominate headlines out of proportion to labour data.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [layoffs-pulse.json](../../examples/layoffs-pulse.json).

**The question:**

> How much layoff coverage has there been, which companies and places, and what is the tone?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “layoffs”, Jun 2024 – May 2026 | 115,198 |
| Critical coverage (priority 7–9) | 50,954 (44.2%) |
| Peak month | Apr 2026 (10,411 articles) |
| Last third of the window vs first third | 1.61× (rising) |
| Negative · positive | 50.8% · 44.9% |
| Tone vs all news (negative-to-positive ratio) | 1.13 vs 0.58 baseline: *markedly more negative than ordinary news coverage* |
| What Prism thinks “layoffs” is | organization |

![Monthly coverage of layoffs](../img/layoffs-pulse-trend.svg)

![Tone of layoffs coverage](../img/layoffs-pulse-tone.svg)

![Countries in layoffs coverage](../img/layoffs-pulse-geo.svg)

![Themes in layoffs coverage](../img/layoffs-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “layoffs” coverage (they also name the companies, people and places it is written about with): layoffs (37,712), nba (13,081), nfl (11,406), nhl (6,986), super bowl (4,198), employee engagement (4,043), restructuring (3,485), employee benefits (3,444), the eastern conference (3,027), lions (2,733), stanley cup (2,711), doge (2,566)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| afc | fubotv | united states |
| fubotv | sam darnold | canada |
| nfc | joey logano | united kingdom |
| nba playoffs | patrick mahomes | india |
| los angeles chargers | derrick henry | australia |
| detroit lions | tyrese haliburton | spain |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 2,276 | 1,021 | 1,151 | 1,014 |
| Jul 2024 | 2,078 | 1,026 | 1,129 | 851 |
| Aug 2024 | 2,209 | 1,107 | 1,185 | 940 |
| Sep 2024 | 3,483 | 1,535 | 1,708 | 1,658 |
| Oct 2024 | 4,838 | 1,436 | 1,625 | 2,964 |
| Nov 2024 | 3,823 | 1,312 | 1,463 | 2,120 |
| Dec 2024 | 3,133 | 1,111 | 1,347 | 1,675 |
| Jan 2025 | 5,207 | 1,753 | 2,082 | 2,838 |
| Feb 2025 | 6,310 | 3,913 | 4,176 | 1,908 |
| Mar 2025 | 5,776 | 3,564 | 3,799 | 1,774 |
| Apr 2025 | 8,532 | 3,350 | 3,923 | 4,272 |
| May 2025 | 7,341 | 2,497 | 3,192 | 3,709 |
| Jun 2025 | 2,610 | 1,297 | 1,485 | 1,029 |
| Jul 2025 | 4,145 | 2,347 | 2,967 | 1,095 |
| Aug 2025 | 5,776 | 2,039 | 2,689 | 2,870 |
| Sep 2025 | 4,037 | 2,022 | 2,209 | 1,688 |
| Oct 2025 | 4,908 | 2,962 | 3,071 | 1,683 |
| Nov 2025 | 3,511 | 1,732 | 1,708 | 1,591 |
| Dec 2025 | 3,026 | 1,397 | 1,587 | 1,319 |
| Jan 2026 | 4,280 | 1,889 | 2,283 | 1,842 |
| Feb 2026 | 4,175 | 2,530 | 2,764 | 1,298 |
| Mar 2026 | 4,573 | 2,292 | 2,463 | 1,881 |
| Apr 2026 | 10,411 | 3,698 | 4,677 | 5,223 |
| May 2026 | 8,740 | 3,124 | 3,716 | 4,469 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/layoffs-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 1.0 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 1.0 | 0.0 |
| Visualisation from counted data | 4.5 | 0.0 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 2.5 | 1.5 | 1.0 |
| Data export with provenance | 4.5 | 4.5 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 4.5 | 1.0 | 0.5 |
| Traceable references | 1.0 | 1.0 | 1.0 | 0.0 |
| Accuracy against the corpus | 4.5 | 4.5 | 3.0 | 4.0 |
| Calibration and limits | 4.5 | 4.0 | 2.5 | 3.0 |
| Decision-grade verdict | 3.0 | 4.0 | 3.0 | 3.0 |
| Facet coverage | 4.0 | 4.0 | 1.0 | 1.0 |
| **Score /100** | **80.7** | 63.0 | 32.7 | 25.4 |

**Claude Opus judge:** D and B both measured the same corpus correctly. D went further: it decomposed volume into critical share and caught the sports contamination of the 'layoffs' match. It also caught the acronym collision and the May 2026 enrichment collapse, and it shipped valid charts and a full regenerate recipe. B was accurate and well caveated, but its chart is malformed and it is thinner on drill-down. A and C had no data. A offered off-question layoff totals from memory, honestly labelled; C declined entirely.

**GPT judge:** C best equips a decision-maker: it quantifies the volume and tone trends, shows the critical-share pattern, and surfaces the sports-heavy noise and place-coverage limits. B is careful and reproducible, but its chart and trend ceilings sharply limit the evidence presentation; C’s main weaknesses are its overlong verdict and a one-day gap calculation error.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/layoffs-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/layoffs-pulse.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How much layoff coverage has there been, which companies and places, and what is the tone?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "layoffs", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'layoffs', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
