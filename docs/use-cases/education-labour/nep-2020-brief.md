# National Education Policy brief

[Education & labour](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A policy brief scoped to India.  
> **Why it is hard.** Small, recent literature; the brief must say how thin it is.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [nep-2020-brief.json](../../examples/nep-2020-brief.json).

**The question:**

> Give me a research brief on India's National Education Policy 2020.

## What Prism returned

| Corpus | Records | Window |
| --- | ---: | --- |
| research | 291 | 2017-2025 |
| readable papers | 62 | 1990-2025 |
| pubmed | 1 | 1990-2025 |
| news | 7,692 | 2019-01-01..2026-06-01 |
| patents | 0 | 2005-2024 |
| arxiv | 0 | 2005-2025 |

### What is established

| Year | Review or guideline | Tier | Cited by |
| ---: | --- | --- | ---: |
| 2023 | [Teacher Education Policy in India: A Comprehensive Review](https://doi.org/10.53573/rhimrj.2023.v10n12.001) | review | 0 |

![Contested share](../img/nep-2020-brief-contested.svg)

### Key numbers

| Figure | Measures | Source |
| --- | --- | --- |
| **more than 50%** | under-25 population proportion of India's total population | [Chemical Education and Research in India: Challenges, Perspectives, and Future Opportunities in Line with the National E](https://doi.org/10.1021/acs.jchemed.2c00454) |
| **∼25%** | under-25 population proportion of world population | [Chemical Education and Research in India: Challenges, Perspectives, and Future Opportunities in Line with the National E](https://doi.org/10.1021/acs.jchemed.2c00454) |
| **almost 20%** | PhDs in chemistry proportion of PhDs in science in India | [Chemical Education and Research in India: Challenges, Perspectives, and Future Opportunities in Line with the National E](https://doi.org/10.1021/acs.jchemed.2c00454) |
| **6%** | allocation of the education budget as percent of GDP | [NEW EDUCATION POLICY, 2020: QUALITATIVE (CONTENTS) ANALYSIS AND TWITTER MINING (SENTIMENT) ANALYSIS](https://doi.org/10.31620/jccc.12.20/02) |

<details><summary>geography</summary>

```json
{
 "available": true,
 "research_authorship": {
  "what": "country of the first author's affiliation (the health literature index) — where the research is done, as far as an affiliation says",
  "rows": [
   {
    "country": "United States",
    "papers": 18
   },
   {
    "country": "United Kingdom",
    "papers": 12
   },
   {
    "country": "China",
    "papers": 7
   },
   {
    "country": "South Africa",
    "papers": 3
   },
   {
    "country": "Denmark",
    "papers": 2
   },
   {
    "country": "Canada",
    "papers": 2
   },
   {
    "country": "Hungary",
    "papers": 2
   },
   {
    "country": "New York",
    "papers": 1
   },
   {
    "country": "India",
    "papers": 1
   },
   {
    "country": "Brazil",
    "papers": 1
   },
   {
    "country": "Thailand",
    "papers": 1
   },
   {
    "country": "South Korea",
    "papers": 1
   }
  ]
 },
 "news_coverage": {
  "what": "country an article is about",
  "rows": [
   {
    "country": "india",
    "articles": 7084
   },
   {
    "country": "united states",
    "articles": 2227
   },
   {
    "country": "united kingdom",
    "articles": 442
   },
   {
    "country": "cameroon",
    "articles": 204
   },
   {
    "country": "ghana",
    "articles": 122
   },
   {
    "country": "nigeria",
    "articles": 98
   },
   {
    "country": "australia",
    "articles": 61
   },
   {
    "country": "china",
    "articles": 52
   },
   {
    "country": "germany",
    "articles": 36
   },
   {
    "country": "canada",
    "articles": 32
   },
   {
    "country": "singapore",
    "articles": 28
   },
   {
    "country": "japan",
    "articles": 27
   }
  ]
 },
 "research_publication": {
  "what": "country of the publishing journal (the health literature index) — not where the study was done",
  "rows": [
   {
    "country": "United States",
    "papers": 38
   },
   {
    "country": "England",
    "papers": 29
   },
   {
    "country": "Switzerland",
    "papers": 9
   },
   {
    "country": "Netherlands",
    "papers": 6
   },
   {
    "country": "Brazil",
    "papers": 4
   },
   {
    "country": "South Africa",
    "papers": 2
   },
   {
    "country": "China",
    "papers": 1
   },
   {
    "country": "Belgium",
    "papers": 1
   },
   {
    "country": "Germany",
    "papers": 1
   },
   {
    "country": "Japan",
    "papers": 1
   },
   {
    "country": "Singapore",
    "papers": 1
   },
   {
    "country": "Canada",
    "papers": 1
   }
  ]
 },
 "patent_origin": {
  "what": "assignee country",
  "rows": [
   {
    "country": "IN",
    "patent
```
</details>

![News coverage](../img/nep-2020-brief-news.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/nep-2020-brief-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 3.0 | 4.0 | 2.0 | 1.0 |
| Visualisation from counted data | 4.0 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 2.0 | 1.0 | 1.5 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.5 | 0.0 | 1.0 |
| Traceable references | 3.5 | 4.0 | 1.5 | 2.0 |
| Accuracy against the corpus | 3.5 | 4.0 | 2.5 | 3.5 |
| Calibration and limits | 4.5 | 3.5 | 3.0 | 3.5 |
| Decision-grade verdict | 3.0 | 4.0 | 0.0 | 3.5 |
| Facet coverage | 4.0 | 3.5 | 1.0 | 1.5 |
| **Score /100** | 71.6 | **73.0** | 24.9 | 32.6 |

**Claude Opus judge:** A and B both ground their claims in the recorded data. B goes further: it reads the rising research trend and the critical-share decomposition, catches the Indiana and off-country anomalies, and states plainly that the evidence base is thin (one review, one the health literature index record). Against that, B wrongly compares news 'critical' with research 'contested' as if they were one scale, and misreads a demographic quote. A is cleaner but narrower and never says the literature is thin. C and D are honest about having no data, but they deliver policy content and memory estimates rather than a measured brief.

**GPT judge:** D is the strongest decision brief: its measured comparisons, repeatable calls, and concise recommendation are well bounded by what the corpus can show. C covers more facets and evidence layers, but has weaker drill-down execution and a less decisive verdict; neither establishes implementation or educational impact.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/nep-2020-brief/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/nep-2020-brief.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Give me a research brief on India's National Education Policy 2020.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.brief" \
  -H 'content-type: application/json' \
  -d '{"topic": "national education policy", "geo": "india"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_brief']["fn"](**{'topic': 'national education policy', 'geo': 'india'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `research_brief` (127.1 s) → `news_trends` (6.8 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
