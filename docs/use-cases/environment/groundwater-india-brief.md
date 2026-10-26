# Groundwater depletion in India

[Environment & disasters](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A geo-scoped environmental brief.  
> **Why it is hard.** Punjab and Haryana dominate; the brief should name the geography.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [groundwater-india-brief.json](../../examples/groundwater-india-brief.json).

**The question:**

> Give me a research brief on groundwater depletion in India.

## What Prism returned

| Corpus | Records | Window |
| --- | ---: | --- |
| research | 1,580 | 2017-2025 |
| readable papers | 22 | 1990-2025 |
| pubmed | 7 | 1990-2025 |
| news | 112 | 2019-01-01..2026-06-01 |
| patents | 0 | 2005-2024 |
| arxiv | 0 | 2005-2025 |

![Contested share](../img/groundwater-india-brief-contested.svg)

### Key numbers

| Figure | Measures | Source |
| --- | --- | --- |
| **50–79 %** | stations showing significant groundwater declines | [The Hindon River basin crisis: Anthropogenic and climatic impacts on groundwater depletion and public health risks](https://doi.org/10.1016/j.ejrh.2025.102661) |
| **∼1.5 cm/year** | groundwater depletion rate | [Summer Monsoon Drying Accelerates India's Groundwater Depletion Under Climate Change](https://doi.org/10.1029/2024ef004516) |
| **450 km 3** | net loss of groundwater | [Summer Monsoon Drying Accelerates India's Groundwater Depletion Under Climate Change](https://doi.org/10.1029/2024ef004516) |
| **−32.30 ± 0.34 km3** | pre‑monsoon groundwater storage depletion | [Strongly heterogeneous patterns of groundwater depletion in Northwestern India](https://doi.org/10.1016/j.jhydrol.2021.126492) |
| **−24.42 ± 0.34 km3** | post‑monsoon groundwater storage depletion | [Strongly heterogeneous patterns of groundwater depletion in Northwestern India](https://doi.org/10.1016/j.jhydrol.2021.126492) |
| **189 km 3** | groundwater storage loss | [Groundwater depletion in northern India: Impacts of the sub‐regional anthropogenic land‐use, socio‐politics and changing](https://doi.org/10.1002/hyp.14003) |

<details><summary>geography</summary>

```json
{
 "available": true,
 "research_authorship": {
  "what": "country of the first author's affiliation (the health literature index) — where the research is done, as far as an affiliation says",
  "rows": [
   {
    "country": "United States",
    "papers": 15
   },
   {
    "country": "China",
    "papers": 9
   },
   {
    "country": "India",
    "papers": 3
   },
   {
    "country": "United Kingdom",
    "papers": 2
   },
   {
    "country": "Chile",
    "papers": 1
   },
   {
    "country": "Canada",
    "papers": 1
   },
   {
    "country": "Ethiopia",
    "papers": 1
   }
  ]
 },
 "news_coverage": {
  "what": "country an article is about",
  "rows": [
   {
    "country": "india",
    "articles": 95
   },
   {
    "country": "united states",
    "articles": 31
   },
   {
    "country": "bangladesh",
    "articles": 4
   },
   {
    "country": "pakistan",
    "articles": 3
   },
   {
    "country": "saudi arabia",
    "articles": 3
   },
   {
    "country": "south korea",
    "articles": 2
   },
   {
    "country": "japan",
    "articles": 2
   },
   {
    "country": "sri lanka",
    "articles": 2
   },
   {
    "country": "china",
    "articles": 2
   },
   {
    "country": "morocco",
    "articles": 2
   },
   {
    "country": "oman",
    "articles": 1
   },
   {
    "country": "united arab emirates",
    "articles": 1
   }
  ]
 },
 "research_publication": {
  "what": "country of the publishing journal (the health literature index) — not where the study was done",
  "rows": [
   {
    "country": "United States",
    "papers": 14
   },
   {
    "country": "England",
    "papers": 14
   },
   {
    "country": "Netherlands",
    "papers": 5
   },
   {
    "country": "Switzerland",
    "papers": 3
   },
   {
    "country": "Germany",
    "papers": 1
   }
  ]
 },
 "patent_origin": {
  "what": "assignee country",
  "rows": [
   {
    "country": "KR",
    "patents": 1
   }
  ]
 },
 "note": "three different questions; do not add them together",
 "focus": {
  "country": "india",
  "news": {
   "n": 95,
   "of_top": 148,
   "share_pct": 64.2,
   "rank_in_top": 1
  },
  "research": {
   "n": 0,
   "of_top": 37,
   "share_pct": 0.0,
   "rank_in_top": null
  },
  "patents": {
   "n": 0,
   "of_top": 1,
   "share_pct": 0.0,
   "rank_in_top": null
  },
  "caveat": "shares are of the top rows shown, not of the whole corpus, and absence from the list means outside the top results rather than zero"
 }
}
```
</details>

![News coverage](../img/groundwater-india-brief-news.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/groundwater-india-brief-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 3.5 | 2.5 | 2.0 | 0.5 |
| Visualisation from counted data | 3.5 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 2.5 | 1.0 | 1.5 | 1.0 |
| Data export with provenance | 1.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.5 | 4.5 | 0.0 | 1.0 |
| Traceable references | 3.5 | 4.0 | 1.0 | 2.0 |
| Accuracy against the corpus | 4.0 | 3.5 | 2.5 | 2.0 |
| Calibration and limits | 4.0 | 4.0 | 3.0 | 3.0 |
| Decision-grade verdict | 4.0 | 4.0 | 2.5 | 2.5 |
| Facet coverage | 4.0 | 3.5 | 1.5 | 1.5 |
| **Score /100** | **71.8** | 70.5 | 30.7 | 25.1 |

**Claude Opus judge:** B and D both grounded their figures in the database, but B covered more ground. It carried the research trend with CAGR, the critical-share decomposition and the contested mix, and it flagged the off-topic California source. D had the cleanest single news series and export but misread the geography focus block. Only memory-based A named Punjab and Haryana explicitly, but its numbers are unverifiable estimates. C sidestepped the geography entirely.

**GPT judge:** A is the strongest decision brief because its figures, charts, and calls are traceable, and it quantifies the research and news trends while stating several relevant limits. Its main weakness is that it misses the requested Punjab and Haryana geography; D is also well sourced, but its trend measures broad news attention and its comparison joins estimates that are not like-for-like.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/groundwater-india-brief/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/groundwater-india-brief.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Give me a research brief on groundwater depletion in India.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.brief" \
  -H 'content-type: application/json' \
  -d '{"topic": "groundwater depletion", "geo": "india"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_brief']["fn"](**{'topic': 'groundwater depletion', 'geo': 'india'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `research_brief` (344.2 s) → `news_trends` (47.5 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
