# Antimicrobial resistance brief

[Medical & clinical evidence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A structured one-page brief built from measurements, ready for a policy memo.  
> **Why it is hard.** Volumes differ by orders of magnitude between corpora; the brief must say which lane each number is from.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [antimicrobial-resistance-brief.json](../../examples/antimicrobial-resistance-brief.json).

**The question:**

> Give me a research brief on antimicrobial resistance: what is established, what is contested, key numbers and trend.

## What Prism returned

| Corpus | Records | Window |
| --- | ---: | --- |
| research | 281,319 | 2017-2025 |
| readable papers | 22,949 | 1990-2025 |
| pubmed | 14,849 | 1990-2025 |
| news | 27,092 | 2019-01-01..2026-06-01 |
| patents | 158 | 2005-2024 |
| arxiv | 18 | 2005-2025 |

### What is established

| Year | Review or guideline | Tier | Cited by |
| ---: | --- | --- | ---: |
| 2010 | [Effect of antibiotic prescribing in primary care on antimicrobial resistance in individual patients: systematic review a](https://doi.org/10.1136/bmj.c2096) | meta_analysis | 2,018 |
| 2022 | [Global burden of bacterial antimicrobial resistance in 2019: a systematic analysis](https://doi.org/10.1016/s0140-6736(21)02724-0) | review | 15,473 |
| 2015 | [Antimicrobial resistance: a global multifaceted phenomenon](https://doi.org/10.1179/2047773215y.0000000030) | review | 3,264 |
| 2020 | [Antimicrobial Resistance in ESKAPE Pathogens](https://doi.org/10.1128/cmr.00181-19) | review | 2,039 |
| 2014 | [Antimicrobial resistance: risk associated with antibiotic overuse and initiatives to reduce the problem](https://doi.org/10.1177/2042098614554919) | review | 2,027 |
| 2019 | [&lt;p&gt;Antimicrobial Resistance: Implications and Costs&lt;/p&gt;](https://doi.org/10.2147/idr.s234610) | review | 1,957 |

![Contested share](../img/antimicrobial-resistance-brief-contested.svg)

### Key numbers

| Figure | Measures | Source |
| --- | --- | --- |
| **10 million deaths per year** | projected deaths per year globally | [Antimicrobial Resistance (AMR)](https://doi.org/10.3389/bjbs.2023.11387) |
| **4·95 million (3·62-6·57)** | deaths associated with bacterial AMR | [Global burden of bacterial antimicrobial resistance in 2019: a systematic analysis](https://doi.org/10.1016/s0140-6736(21)02724-0) |
| **1·27 million (95% UI 0·911-1·71)** | deaths attributable to bacterial AMR | [Global burden of bacterial antimicrobial resistance in 2019: a systematic analysis](https://doi.org/10.1016/s0140-6736(21)02724-0) |
| **929 000 (660 000-1 270 000)** | deaths attributable to AMR from six leading pathogens | [Global burden of bacterial antimicrobial resistance in 2019: a systematic analysis](https://doi.org/10.1016/s0140-6736(21)02724-0) |
| **3·57 million (2·62-4·78)** | deaths associated with AMR from six leading pathogens | [Global burden of bacterial antimicrobial resistance in 2019: a systematic analysis](https://doi.org/10.1016/s0140-6736(21)02724-0) |
| **3.6% of all ARGs** | proportion of ARGs that are human-associated, mobile | [An omics-based framework for assessing the health risk of antimicrobial resistance genes](https://doi.org/10.1038/s41467-021-25096-3) |

<details><summary>geography</summary>

```json
{
 "available": true,
 "research_authorship": {
  "what": "country of the first author's affiliation (the health literature index) — where the research is done, as far as an affiliation says",
  "rows": [
   {
    "country": "United States",
    "papers": 1554
   },
   {
    "country": "China",
    "papers": 1294
   },
   {
    "country": "United Kingdom",
    "papers": 951
   },
   {
    "country": "India",
    "papers": 687
   },
   {
    "country": "Brazil",
    "papers": 467
   },
   {
    "country": "Italy",
    "papers": 419
   },
   {
    "country": "Canada",
    "papers": 401
   },
   {
    "country": "Spain",
    "papers": 366
   },
   {
    "country": "Australia",
    "papers": 349
   },
   {
    "country": "Germany",
    "papers": 298
   },
   {
    "country": "Iran",
    "papers": 284
   },
   {
    "country": "South Korea",
    "papers": 281
   }
  ]
 },
 "news_coverage": {
  "what": "country an article is about",
  "rows": [
   {
    "country": "united states",
    "articles": 638
   },
   {
    "country": "united kingdom",
    "articles": 495
   },
   {
    "country": "india",
    "articles": 469
   },
   {
    "country": "nigeria",
    "articles": 106
   },
   {
    "country": "australia",
    "articles": 75
   },
   {
    "country": "canada",
    "articles": 53
   },
   {
    "country": "china",
    "articles": 50
   },
   {
    "country": "switzerland",
    "articles": 47
   },
   {
    "country": "france",
    "articles": 44
   },
   {
    "country": "ghana",
    "articles": 43
   },
   {
    "country": "germany",
    "articles": 34
   },
   {
    "country": "singapore",
    "articles": 30
   }
  ]
 },
 "research_publication": {
  "what": "country of the publishing journal (the health literature index) — not where the study was done",
  "rows": [
   {
    "country": "England",
    "papers": 4211
   },
   {
    "country": "United States",
    "papers": 3677
   },
   {
    "country": "Switzerland",
    "papers": 2341
   },
   {
    "country": "Netherlands",
    "papers": 1270
   },
   {
    "country": "Germany",
    "papers": 424
   },
   {
    "country": "India",
    "papers": 233
   },
   {
    "country": "Canada",
    "papers": 225
   },
   {
    "country": "New Zealand",
    "papers": 192
   },
   {
    "country": "China",
    "papers": 173
   },
   {
    "country": "Brazil",
    "papers": 152
   },
   {
    "country": "Italy",
    "papers": 137
   },
   {
    "country": "Japan",
    "papers": 124
   }
  ]
 },
 "patent_origin": {
  "what": "assignee country",
  "rows": [
   {

```
</details>

![News coverage](../img/antimicrobial-resistance-brief-news.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/antimicrobial-resistance-brief-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 3.0 | 1.5 | 0.0 |
| Measured comparison | 4.5 | 4.0 | 2.0 | 2.0 |
| Visualisation from counted data | 1.0 | 3.0 | 1.0 | 0.0 |
| Exploration and drill-down | 3.5 | 1.0 | 1.5 | 1.0 |
| Data export with provenance | 1.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.5 | 4.0 | 1.0 | 1.0 |
| Traceable references | 4.0 | 4.0 | 1.5 | 3.0 |
| Accuracy against the corpus | 4.5 | 3.5 | 2.5 | 4.0 |
| Calibration and limits | 4.5 | 4.0 | 3.5 | 3.0 |
| Decision-grade verdict | 4.0 | 3.5 | 3.5 | 3.5 |
| Facet coverage | 4.5 | 3.5 | 1.5 | 1.5 |
| **Score /100** | **74.0** | 67.2 | 38.1 | 36.0 |

**Claude Opus judge:** B was the only deliverable that met the question's hard part. It labelled every volume with its lane and window, kept the two news series apart, read the flat 1.13 news trend correctly and caught the tool's anomalies. D was traced but thin and misread two fields. A and C were memory-only; C was honest, while A carried a probably wrong 1990 baseline.

**GPT judge:** C gives the broadest grounded brief: it separates corpus lanes, burden definitions, and framing; traces research and news trends; and calls out conflicting trend summaries and missing outcome data. Its chart-window and export provenance errors keep it from a clean decision-grade result, while B is more internally tidy but leaves more of the available evidence and trend detail unused.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/antimicrobial-resistance-brief/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/antimicrobial-resistance-brief.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Give me a research brief on antimicrobial resistance: what is established, what is contested, key numbers and trend.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.brief" \
  -H 'content-type: application/json' \
  -d '{"topic": "antimicrobial resistance", "geo": ""}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_brief']["fn"](**{'topic': 'antimicrobial resistance', 'geo': ''})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `research_brief` (189.2 s) → `news_trends` (14.7 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
