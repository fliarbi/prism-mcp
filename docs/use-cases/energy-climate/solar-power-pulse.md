# Solar power coverage

[Energy & climate](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A sector pulse for an energy investor.  
> **Why it is hard.** Product reviews mention 'solar' constantly; centrality matching keeps them out.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [solar-power-pulse.json](../../examples/solar-power-pulse.json).

**The question:**

> What does the news say about solar power: trend, tone, places, companies?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “solar power”, Jun 2024 – May 2026 | 58,907 |
| Critical coverage (priority 7–9) | 45,058 (76.5%) |
| Peak month | Apr 2026 (3,609 articles) |
| Last third of the window vs first third | 1.15× (flat) |
| Negative · positive | 12.1% · 87.3% |
| Tone vs all news (negative-to-positive ratio) | 0.14 vs 0.58 baseline: *markedly more positive than ordinary news coverage* |
| What Prism thinks “solar power” is | organization |

![Monthly coverage of solar power](../img/solar-power-pulse-trend.svg)

![Tone of solar power coverage](../img/solar-power-pulse-tone.svg)

![Countries in solar power coverage](../img/solar-power-pulse-geo.svg)

![Themes in solar power coverage](../img/solar-power-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “solar power” coverage (they also name the companies, people and places it is written about with): solar power (51,639), renewable energy (28,914), sustainability (21,889), mw (12,781), energy efficiency (12,119), energy policy (7,693), solar (5,817), clean energy (4,893), solar energy (4,715), energy storage (3,834), energy transition (3,024), epc (2,525)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| solar power | lorde | united states |
| renewable energy | pralhad joshi | india |
| green energy | gautam adani | china |
| enphase energy | ed miliband | united kingdom |
| adani green energy | anil ambani | australia |
| hydropower | charli xcx | germany |

**Top publishers in a 216-article sample:** renewablesnow.com (7.9%), pv-magazine.com (5.1%), pv-tech.org (3.2%), powerphilippines.com (2.3%), saurenergy.com (2.3%), mercomindia.com (1.9%)

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 2,050 | 1,563 | 212 | 1,827 |
| Jul 2024 | 2,498 | 1,873 | 240 | 2,239 |
| Aug 2024 | 2,304 | 1,814 | 267 | 2,023 |
| Sep 2024 | 2,438 | 1,961 | 227 | 2,197 |
| Oct 2024 | 2,373 | 1,834 | 236 | 2,116 |
| Nov 2024 | 2,599 | 2,067 | 512 | 2,070 |
| Dec 2024 | 2,218 | 1,778 | 263 | 1,945 |
| Jan 2025 | 2,629 | 2,047 | 293 | 2,313 |
| Feb 2025 | 2,493 | 1,811 | 300 | 2,176 |
| Mar 2025 | 2,352 | 1,773 | 269 | 2,073 |
| Apr 2025 | 2,406 | 1,701 | 355 | 2,034 |
| May 2025 | 1,958 | 1,480 | 236 | 1,708 |
| Jun 2025 | 1,812 | 1,282 | 216 | 1,585 |
| Jul 2025 | 2,315 | 1,517 | 310 | 1,990 |
| Aug 2025 | 2,257 | 1,556 | 387 | 1,853 |
| Sep 2025 | 2,272 | 1,733 | 279 | 1,980 |
| Oct 2025 | 2,194 | 1,701 | 266 | 1,910 |
| Nov 2025 | 2,200 | 1,737 | 200 | 1,981 |
| Dec 2025 | 2,313 | 1,921 | 213 | 2,087 |
| Jan 2026 | 2,419 | 1,963 | 268 | 2,140 |
| Feb 2026 | 3,146 | 2,455 | 302 | 2,818 |
| Mar 2026 | 3,051 | 2,237 | 375 | 2,651 |
| Apr 2026 | 3,609 | 2,891 | 488 | 3,095 |
| May 2026 | 3,001 | 2,363 | 426 | 2,545 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/solar-power-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 3.5 | 4.0 | 0.5 | 0.0 |
| Measured comparison | 4.0 | 4.0 | 0.0 | 0.0 |
| Visualisation from counted data | 4.0 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 3.0 | 3.5 | 1.0 | 2.0 |
| Data export with provenance | 3.0 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.0 | 1.0 | 1.0 |
| Traceable references | 1.0 | 1.0 | 0.5 | 0.5 |
| Accuracy against the corpus | 2.5 | 3.5 | 2.5 | 3.0 |
| Calibration and limits | 4.0 | 4.0 | 3.0 | 2.5 |
| Decision-grade verdict | 3.5 | 4.0 | 2.5 | 2.5 |
| Facet coverage | 5.0 | 4.0 | 1.0 | 0.5 |
| **Score /100** | 67.6 | **72.3** | 27.2 | 23.8 |

**Claude Opus judge:** A and B both deliver traced volume, tone-vs-baseline, geography and company answers with the proper window and censoring. B edges ahead because it flags the Lorde/Charli XCX name collisions and the undefined 'critical' field. A has the more complete exports, but its single chart omits tone. C refuses honestly, and D offers only off-question memory estimates, so neither supports a news-based decision.

**GPT judge:** A is the most decision-ready: it gives a measured, bounded account of volume, tone, places, and organizations, with traceable exports and a cautious interpretation. C covers more facets but overstates the trend as rising and leaves the export incomplete; B and D correctly acknowledge missing measurements but cannot answer the question from grounded news data.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/solar-power-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/solar-power-pulse.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What does the news say about solar power: trend, tone, places, companies?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "solar power", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'solar power', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
