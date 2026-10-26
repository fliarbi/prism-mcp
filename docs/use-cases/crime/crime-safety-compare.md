# Fraud vs theft vs violence in the news

[Crime & public safety](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Which crime type dominates attention.  
> **Why it is hard.** Violent crime dominates criticality even when fraud dominates volume.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · 2024-06-01 to 2026-06-01 (exclusive) · all listed tables passed strict index partition reads and historical row floors. Saved responses: [crime-safety-compare.json](../../examples/crime-safety-compare.json).

**The question:**

> Compare coverage of fraud, robbery and murder over the last two years.

## What Prism returned

| Term | Articles | Share | Critical | Growth (late vs early) | Negative-to-positive | vs all news |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **fraud** | 351,112 | 36.9% | 287,954 | 1.2× (flat) | 5.02 | 8.66× |
| **robbery** | 57,044 | 6% | 42,991 | 1.18× (flat) | 21.46 | 37.0× |
| **murder** | 543,019 | 57.1% | 475,613 | 0.96× (flat) | 12.47 | 21.5× |

![Comparison over time](../img/crime-safety-compare-compare.svg)

![Total coverage](../img/crime-safety-compare-share.svg)

> more coverage is attention, not importance, and a term that is also a common word will over-count — check each term's own volume against its sources panel

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/crime-safety-compare-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 2.5 | 1.0 | 0.0 | 0.0 |
| Measured comparison | 4.5 | 4.0 | 0.0 | 0.0 |
| Visualisation from counted data | 2.5 | 0.0 | 0.0 | 0.5 |
| Exploration and drill-down | 1.5 | 1.0 | 0.5 | 0.5 |
| Data export with provenance | 3.0 | 3.0 | 0.0 | 0.5 |
| Reproducibility | 3.0 | 3.0 | 0.0 | 1.0 |
| Accuracy against the corpus | 2.0 | 3.0 | 3.0 | 3.0 |
| Calibration and limits | 3.0 | 3.5 | 3.5 | 3.0 |
| Decision-grade verdict | 3.0 | 3.0 | 2.5 | 2.5 |
| Facet coverage | 4.0 | 3.0 | 0.5 | 0.5 |
| **Score /100** | **56.5** | 48.5 | 21.8 | 25.5 |

**Claude Opus judge:** A was the only deliverable to address the question's crux: murder dominates on both volume and critical share (87.6% vs 82.0% for fraud and 75.4% for robbery). It also caught the non-deduplicated combined total and placed the 5-month currency gap next to the numbers. However, its hand-computed 12-month sums are wrong. C traced the same data and exported the full monthly series, but its chart is broken and it ignored criticality. B and D were honest refusals that give a decision-maker nothing measured.

**GPT judge:** D is the most decision-useful because it compares all three topics on the same measured scale, exposes criticality alongside volume, and supplies the monthly series and provenance. Its trend arithmetic and coverage interpretation need correction; C is more cautious about limits but does not quantify trend adequately and leaves key comparison facets unresolved.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/crime-safety-compare/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/crime-safety-compare.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Compare coverage of fraud, robbery and murder over the last two years.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.compare" \
  -H 'content-type: application/json' \
  -d '{"terms": ["fraud", "robbery", "murder"], "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_terms']["fn"](**{'terms': ['fraud', 'robbery', 'murder'], 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
