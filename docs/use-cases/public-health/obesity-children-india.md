# Childhood obesity in India

[Public health & epidemiology](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A geo-scoped brief: what is studied about India specifically.  
> **Why it is hard.** A geo scope must be a scope (papers about India), not a keyword (papers mentioning India).  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [obesity-children-india.json](../../examples/obesity-children-india.json).

**The question:**

> Give me a research brief on childhood obesity in India.

## What Prism returned

| Corpus | Records | Window |
| --- | ---: | --- |
| research | 1,382 | 2017-2025 |
| readable papers | 48 | 1990-2025 |
| pubmed | 5,149 | 1990-2025 |
| news | 112 | 2019-01-01..2026-06-01 |
| patents | 0 | 2005-2024 |
| arxiv | 0 | 2005-2025 |

### What is established

| Year | Review or guideline | Tier | Cited by |
| ---: | --- | --- | ---: |
| 2015 | [Habitual Sleep Duration and Risk of Childhood Obesity: Systematic Review and Dose-response Meta-analysis of Prospective ](https://doi.org/10.1038/srep16160) | meta_analysis | 174 |
| 2025 | [Parent-focused behavioural interventions for the prevention of early childhood obesity (TOPCHILD): a systematic review a](https://doi.org/10.1016/S0140-6736(25)01144-4) | meta_analysis | 0 |
| 2025 | [Comparative Efficacy of Glucagon-Like Peptide 1 Receptor Agonists for Cardiovascular Outcomes in Asian Versus White Popu](https://doi.org/10.2337/dc24-1533) | meta_analysis | 0 |
| 2025 | [Precision nutrition-based interventions for the management of obesity in children and adolescents up to the age of 19 ye](https://doi.org/10.1002/14651858.CD015877) | meta_analysis | 0 |
| 2005 | [Childhood Obesity](https://doi.org/10.1210/jc.2004-1389) | review | 416 |
| 2013 | [A Systematic Review of Health Videogames on Childhood Obesity Prevention and Intervention](https://doi.org/10.1089/g4h.2013.0025) | review | 137 |

![Contested share](../img/obesity-children-india-contested.svg)

### Key numbers

| Figure | Measures | Source |
| --- | --- | --- |
| **-0·01** | mean difference in BMI Z score | [Parent-focused behavioural interventions for the prevention of early childhood obesity (TOPCHILD): a systematic review a](https://doi.org/10.1016/S0140-6736(25)01144-4) |
| **-0·08 to 0·05** | 95% CI for mean difference in BMI Z score | [Parent-focused behavioural interventions for the prevention of early childhood obesity (TOPCHILD): a systematic review a](https://doi.org/10.1016/S0140-6736(25)01144-4) |
| **50%** | percentage of participants who were boys | [Parent-focused behavioural interventions for the prevention of early childhood obesity (TOPCHILD): a systematic review a](https://doi.org/10.1016/S0140-6736(25)01144-4) |
| **48%** | percentage of participants who were girls | [Parent-focused behavioural interventions for the prevention of early childhood obesity (TOPCHILD): a systematic review a](https://doi.org/10.1016/S0140-6736(25)01144-4) |
| **2%** | percentage of participants with unknown sex | [Parent-focused behavioural interventions for the prevention of early childhood obesity (TOPCHILD): a systematic review a](https://doi.org/10.1016/S0140-6736(25)01144-4) |
| **38%** | proportion of completed eligible trials assessing primary outcome (BMI Z score) | [Parent-focused behavioural interventions for the prevention of early childhood obesity (TOPCHILD): a systematic review a](https://doi.org/10.1016/S0140-6736(25)01144-4) |

<details><summary>geography</summary>

```json
{
 "available": true,
 "research_authorship": {
  "what": "country of the first author's affiliation (the health literature index) — where the research is done, as far as an affiliation says",
  "rows": [
   {
    "country": "United States",
    "papers": 57019
   },
   {
    "country": "China",
    "papers": 18217
   },
   {
    "country": "United Kingdom",
    "papers": 11026
   },
   {
    "country": "Italy",
    "papers": 8038
   },
   {
    "country": "Australia",
    "papers": 7638
   },
   {
    "country": "Spain",
    "papers": 7608
   },
   {
    "country": "Brazil",
    "papers": 7280
   },
   {
    "country": "Germany",
    "papers": 6364
   },
   {
    "country": "Canada",
    "papers": 6276
   },
   {
    "country": "Japan",
    "papers": 5997
   },
   {
    "country": "France",
    "papers": 5725
   },
   {
    "country": "South Korea",
    "papers": 5612
   }
  ]
 },
 "news_coverage": {
  "what": "country an article is about",
  "rows": [
   {
    "country": "united states",
    "articles": 591
   },
   {
    "country": "united kingdom",
    "articles": 161
   },
   {
    "country": "india",
    "articles": 81
   },
   {
    "country": "australia",
    "articles": 26
   },
   {
    "country": "china",
    "articles": 23
   },
   {
    "country": "barbados",
    "articles": 22
   },
   {
    "country": "new zealand",
    "articles": 17
   },
   {
    "country": "spain",
    "articles": 16
   },
   {
    "country": "canada",
    "articles": 15
   },
   {
    "country": "ireland",
    "articles": 12
   },
   {
    "country": "brazil",
    "articles": 11
   },
   {
    "country": "sweden",
    "articles": 9
   }
  ]
 },
 "research_publication": {
  "what": "country of the publishing journal (the health literature index) — not where the study was done",
  "rows": [
   {
    "country": "United States",
    "papers": 108802
   },
   {
    "country": "England",
    "papers": 62362
   },
   {
    "country": "Switzerland",
    "papers": 16045
   },
   {
    "country": "Netherlands",
    "papers": 12412
   },
   {
    "country": "Germany",
    "papers": 11979
   },
   {
    "country": "China",
    "papers": 2930
   },
   {
    "country": "Spain",
    "papers": 2861
   },
   {
    "country": "France",
    "papers": 2859
   },
   {
    "country": "Japan",
    "papers": 2810
   },
   {
    "country": "Ireland",
    "papers": 2545
   },
   {
    "country": "Brazil",
    "papers": 2450
   },
   {
    "country": "Italy",
    "papers": 2358
   }
  ]
 },
 "patent_origin": {
  "what": "assignee country
```
</details>

![News coverage](../img/obesity-children-india-news.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/obesity-children-india-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 3.0 | 1.0 | 2.0 |
| Measured comparison | 4.0 | 3.5 | 1.0 | 2.0 |
| Visualisation from counted data | 3.5 | 3.0 | 1.0 | 1.0 |
| Exploration and drill-down | 2.0 | 1.0 | 1.0 | 1.0 |
| Data export with provenance | 3.0 | 3.5 | 1.0 | 1.0 |
| Reproducibility | 4.5 | 4.5 | 0.0 | 0.0 |
| Traceable references | 4.5 | 4.0 | 1.0 | 2.5 |
| Accuracy against the corpus | 4.0 | 3.5 | 2.5 | 3.5 |
| Calibration and limits | 4.0 | 4.0 | 3.0 | 3.0 |
| Decision-grade verdict | 4.0 | 3.5 | 0.0 | 3.5 |
| Facet coverage | 4.5 | 4.0 | 1.0 | 2.0 |
| **Score /100** | **77.2** | 69.1 | 22.0 | 39.8 |

**Claude Opus judge:** A traced every number. It quantified both the research and news trends and flagged that the 'India' query returned global evidence, including its conflicting institution and research-row signals. Its decision is honest: get national survey data before sizing the problem. B was similarly traced but thinner, and it misread the censoring. C and D gave plausible prevalence figures from memory that a decision-maker cannot verify; C also has questionable specifics.

**GPT judge:** B is the strongest decision brief because its core counts, monthly series, comparisons, and citations are traceable, and it clearly says the corpus cannot establish Indian child prevalence. C is careful and reproducible but omits the available quantified news trend and has no successful follow-up calls; neither brief resolves the underlying need for representative India-specific prevalence data.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/obesity-children-india/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/obesity-children-india.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Give me a research brief on childhood obesity in India.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.brief" \
  -H 'content-type: application/json' \
  -d '{"topic": "childhood obesity", "geo": "india"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_brief']["fn"](**{'topic': 'childhood obesity', 'geo': 'india'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `research_brief` (166.0 s) → `news_trends` (2.0 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
