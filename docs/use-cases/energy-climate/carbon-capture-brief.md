# Carbon capture brief

[Energy & climate](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A structured brief for a climate-tech memo.  
> **Why it is hard.** Patents and research tell different stories; the brief shows both.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [carbon-capture-brief.json](../../examples/carbon-capture-brief.json).

**The question:**

> Give me a research brief on carbon capture and storage.

## What Prism returned

| Corpus | Records | Window |
| --- | ---: | --- |
| research | 118,216 | 2017-2025 |
| readable papers | 1,667 | 1990-2025 |
| pubmed | 219 | 1990-2025 |
| news | 1,515 | 2019-01-01..2026-06-01 |
| patents | 168 | 2005-2024 |
| arxiv | 7 | 2005-2025 |

### What is established

| Year | Review or guideline | Tier | Cited by |
| ---: | --- | --- | ---: |
| 2021 | [A review of CO<sub>2</sub> adsorbents performance for different carbon capture technology processes conditions](https://doi.org/10.1002/ghg.2112) | review | 164 |
| 2024 | [CO2 sequestration in subsurface geological formations: A review of trapping mechanisms and monitoring techniques](https://doi.org/10.1016/j.earscirev.2024.104793) | review | 153 |
| 2022 | [Carbonic anhydrase to boost CO2 sequestration: Improving carbon capture utilization and storage (CCUS)](https://doi.org/10.1016/j.chemosphere.2022.134419) | review | 107 |
| 2018 | [CO2 Sequestration by Mineral Carbonation: A Review](https://doi.org/10.30955/gnj.002597) | review | 73 |
| 2023 | [Dimensional change of cement paste subjected to carbonation in CO2 sequestration and utilization context: A critical rev](https://doi.org/10.1016/j.jcou.2023.102444) | review | 67 |
| 2023 | [Reactivity of Basaltic Minerals for CO2 Sequestration via In Situ Mineralization: A Review](https://doi.org/10.3390/min13091154) | review | 57 |

![Contested share](../img/carbon-capture-brief-contested.svg)

### Key numbers

| Figure | Measures | Source |
| --- | --- | --- |
| **40% and 93.7%** | efficiency of capture and sequestration of CO2 by microalgae | [Progress in Microalgae Application for CO2 Sequestration](https://doi.org/10.1016/j.clce.2022.100044) |
| **~20%** | porosity decrease | [Aquifer-on-a-Chip: understanding pore-scale salt precipitation dynamics during CO2 sequestration](https://doi.org/10.1039/c3lc00031a) |
| **~2%** | velocity of salt precipitation front relative to superficial CO2 velocity | [Aquifer-on-a-Chip: understanding pore-scale salt precipitation dynamics during CO2 sequestration](https://doi.org/10.1039/c3lc00031a) |
| **a billion metric tons or more** | annual CO2 sequestration required | [CO2 Sequestration in Deep Sedimentary Formations](https://doi.org/10.2113/gselements.4.5.325) |
| **250 fold increase** | increase over the amount sequestered today | [CO2 Sequestration in Deep Sedimentary Formations](https://doi.org/10.2113/gselements.4.5.325) |

<details><summary>geography</summary>

```json
{
 "available": true,
 "research_authorship": {
  "what": "country of the first author's affiliation (the health literature index) — where the research is done, as far as an affiliation says",
  "rows": [
   {
    "country": "China",
    "papers": 51
   },
   {
    "country": "United States",
    "papers": 36
   },
   {
    "country": "India",
    "papers": 26
   },
   {
    "country": "Canada",
    "papers": 12
   },
   {
    "country": "South Korea",
    "papers": 9
   },
   {
    "country": "United Kingdom",
    "papers": 8
   },
   {
    "country": "Saudi Arabia",
    "papers": 6
   },
   {
    "country": "Italy",
    "papers": 5
   },
   {
    "country": "Germany",
    "papers": 5
   },
   {
    "country": "Spain",
    "papers": 5
   },
   {
    "country": "South Africa",
    "papers": 4
   },
   {
    "country": "Sweden",
    "papers": 3
   }
  ]
 },
 "news_coverage": {
  "what": "country an article is about",
  "rows": [
   {
    "country": "united states",
    "articles": 338
   },
   {
    "country": "united kingdom",
    "articles": 122
   },
   {
    "country": "canada",
    "articles": 73
   },
   {
    "country": "norway",
    "articles": 31
   },
   {
    "country": "india",
    "articles": 29
   },
   {
    "country": "australia",
    "articles": 27
   },
   {
    "country": "japan",
    "articles": 24
   },
   {
    "country": "sweden",
    "articles": 17
   },
   {
    "country": "germany",
    "articles": 12
   },
   {
    "country": "south korea",
    "articles": 12
   },
   {
    "country": "united arab emirates",
    "articles": 12
   },
   {
    "country": "singapore",
    "articles": 11
   }
  ]
 },
 "research_publication": {
  "what": "country of the publishing journal (the health literature index) — not where the study was done",
  "rows": [
   {
    "country": "United States",
    "papers": 75
   },
   {
    "country": "England",
    "papers": 61
   },
   {
    "country": "Netherlands",
    "papers": 39
   },
   {
    "country": "Germany",
    "papers": 25
   },
   {
    "country": "Switzerland",
    "papers": 15
   },
   {
    "country": "Egypt",
    "papers": 1
   },
   {
    "country": "Australia",
    "papers": 1
   },
   {
    "country": "India",
    "papers": 1
   },
   {
    "country": "China",
    "papers": 1
   }
  ]
 },
 "patent_origin": {
  "what": "assignee country",
  "rows": [
   {
    "country": "US",
    "patents": 163
   },
   {
    "country": "",
    "patents": 32
   },
   {
    "country": "SA",
    "patents": 11
   },
   {
    "country": "IL",
    "pate
```
</details>

![News coverage](../img/carbon-capture-brief-news.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/carbon-capture-brief-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 3.5 | 1.0 | 1.0 |
| Measured comparison | 4.5 | 4.0 | 2.0 | 0.5 |
| Visualisation from counted data | 3.5 | 2.5 | 1.0 | 1.0 |
| Exploration and drill-down | 3.0 | 1.0 | 1.5 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 1.0 |
| Reproducibility | 4.5 | 3.5 | 0.0 | 0.0 |
| Traceable references | 4.0 | 4.0 | 1.5 | 1.5 |
| Accuracy against the corpus | 4.0 | 3.0 | 3.5 | 2.5 |
| Calibration and limits | 4.0 | 4.5 | 3.5 | 3.5 |
| Decision-grade verdict | 4.0 | 3.5 | 3.5 | 3.0 |
| Facet coverage | 3.5 | 3.0 | 1.0 | 1.0 |
| **Score /100** | **78.3** | 65.0 | 36.5 | 30.1 |

**Claude Opus judge:** C was the only deliverable that grounded volumes, stance mix, both trend windows and three-lens geography in traced numbers. It also caught the 1,515 vs 10,735 news-count anomaly and placed its limits next to the numbers. D was clean and well referenced, but it misread the tool's 2.2x thirds ratio as endpoint growth and left the available geography data unused. A and B were honest memory briefs with estimate labels that a decision-maker could not verify. None of the four seriously developed the patents-vs-research contrast the question flagged.

**GPT judge:** D is the strongest decision brief: it shows the research and patent corpus alongside traced research growth and a recent, slightly declining news series, while keeping the different windows distinct. Its partial monthly export and limited interpretation of what patent counts mean are the main gaps; B is more cautious but has no executed drill-down and less complete chart coverage.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/carbon-capture-brief/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/carbon-capture-brief.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Give me a research brief on carbon capture and storage.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.brief" \
  -H 'content-type: application/json' \
  -d '{"topic": "carbon capture", "geo": ""}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_brief']["fn"](**{'topic': 'carbon capture', 'geo': ''})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `research_brief` (154.1 s) → `news_trends` (8.0 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
