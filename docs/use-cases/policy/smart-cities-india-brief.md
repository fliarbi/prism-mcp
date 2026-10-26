# Smart Cities Mission brief

[Policy & regulation](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A geo-scoped policy brief.  
> **Why it is hard.** Many papers mention smart cities generically; India scope must be enforced.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [smart-cities-india-brief.json](../../examples/smart-cities-india-brief.json).

**The question:**

> Give me a research brief on smart cities in India.

## What Prism returned

| Corpus | Records | Window |
| --- | ---: | --- |
| research | 323 | 2017-2025 |
| readable papers | 7 | 1990-2025 |
| pubmed | 1 | 1990-2025 |
| news | 251 | 2019-01-01..2026-06-01 |
| patents | 0 | 2005-2024 |
| arxiv | 0 | 2005-2025 |

![Contested share](../img/smart-cities-india-brief-contested.svg)

### Key numbers

| Figure | Measures | Source |
| --- | --- | --- |
| **95%** | encryption efficiency | [Advanced Human–Computer Interaction and Virtual Reality in Smart City Development](https://doi.org/10.4018/979-8-3373-1315-3.ch013) |
| **92%** | gesture recognition accuracy | [Advanced Human–Computer Interaction and Virtual Reality in Smart City Development](https://doi.org/10.4018/979-8-3373-1315-3.ch013) |
| **15ms** | gesture recognition delay | [Advanced Human–Computer Interaction and Virtual Reality in Smart City Development](https://doi.org/10.4018/979-8-3373-1315-3.ch013) |

<details><summary>geography</summary>

```json
{
 "available": true,
 "research_authorship": {
  "what": "country of the first author's affiliation (the health literature index) — where the research is done, as far as an affiliation says",
  "rows": [
   {
    "country": "United States",
    "papers": 2
   },
   {
    "country": "India",
    "papers": 1
   },
   {
    "country": "Canada",
    "papers": 1
   },
   {
    "country": "United Kingdom",
    "papers": 1
   },
   {
    "country": "Indonesia",
    "papers": 1
   },
   {
    "country": "Czech Republic",
    "papers": 1
   }
  ]
 },
 "news_coverage": {
  "what": "country an article is about",
  "rows": [
   {
    "country": "india",
    "articles": 221
   },
   {
    "country": "united states",
    "articles": 46
   },
   {
    "country": "singapore",
    "articles": 23
   },
   {
    "country": "china",
    "articles": 16
   },
   {
    "country": "united arab emirates",
    "articles": 15
   },
   {
    "country": "taiwan",
    "articles": 14
   },
   {
    "country": "vietnam",
    "articles": 13
   },
   {
    "country": "malaysia",
    "articles": 12
   },
   {
    "country": "indonesia",
    "articles": 10
   },
   {
    "country": "japan",
    "articles": 6
   },
   {
    "country": "south korea",
    "articles": 6
   },
   {
    "country": "saudi arabia",
    "articles": 5
   }
  ]
 },
 "research_publication": {
  "what": "country of the publishing journal (the health literature index) — not where the study was done",
  "rows": [
   {
    "country": "United States",
    "papers": 2
   },
   {
    "country": "Switzerland",
    "papers": 2
   },
   {
    "country": "England",
    "papers": 2
   },
   {
    "country": "Netherlands",
    "papers": 1
   }
  ]
 },
 "patent_origin": {
  "what": "assignee country",
  "rows": []
 },
 "note": "three different questions; do not add them together",
 "focus": {
  "country": "india",
  "news": {
   "n": 221,
   "of_top": 387,
   "share_pct": 57.1,
   "rank_in_top": 1
  },
  "research": {
   "n": 0,
   "of_top": 7,
   "share_pct": 0.0,
   "rank_in_top": null
  },
  "patents": {
   "n": 0,
   "of_top": 0,
   "share_pct": null,
   "rank_in_top": null
  },
  "caveat": "shares are of the top rows shown, not of the whole corpus, and absence from the list means outside the top results rather than zero"
 }
}
```
</details>

![News coverage](../img/smart-cities-india-brief-news.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/smart-cities-india-brief-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 4.0 | 1.0 | 0.5 |
| Measured comparison | 4.0 | 4.0 | 1.5 | 2.0 |
| Visualisation from counted data | 3.0 | 3.5 | 1.0 | 1.0 |
| Exploration and drill-down | 2.5 | 1.0 | 1.0 | 1.0 |
| Data export with provenance | 2.0 | 3.5 | 1.0 | 1.0 |
| Reproducibility | 4.0 | 4.5 | 1.0 | 1.0 |
| Traceable references | 3.5 | 3.0 | 0.5 | 1.5 |
| Accuracy against the corpus | 2.5 | 4.0 | 3.5 | 3.0 |
| Calibration and limits | 4.0 | 3.0 | 3.5 | 3.0 |
| Decision-grade verdict | 3.0 | 4.0 | 3.0 | 3.5 |
| Facet coverage | 3.5 | 3.5 | 1.0 | 1.5 |
| **Score /100** | 65.3 | **71.4** | 34.7 | 35.8 |

**Claude Opus judge:** B and D both grounded every number in the recorded database responses, while A and C relied on memory; C labelled its estimates honestly, and A dressed unverifiable figures in generic citations. D edged ahead of B by covering the facets B omitted: the research trend, the critical-share decomposition and institutions. D also flagged the off-topic key numbers and the geography artefact. B had the cleaner full-series chart and export.

**GPT judge:** B is the strongest decision brief: its traced series, comparisons, exports, and reproducibility make the evidence usable, while it limits its conclusion to what the corpus can establish. C is similarly rich but misstates two central geography figures; A and D offer more limited, largely unmeasured coverage.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/smart-cities-india-brief/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/smart-cities-india-brief.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Give me a research brief on smart cities in India.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.brief" \
  -H 'content-type: application/json' \
  -d '{"topic": "smart cities", "geo": "india"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_brief']["fn"](**{'topic': 'smart cities', 'geo': 'india'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `research_brief` (120.5 s) → `news_trends` (1.1 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
