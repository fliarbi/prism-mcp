# Immigration policy coverage

[Policy & regulation](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** The framing of US immigration debate in numbers.  
> **Why it is hard.** Terms overlap heavily; overlap must be stated.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · 2024-06-01 to 2026-06-01 (exclusive) · all listed tables passed strict index partition reads and historical row floors. Saved responses: [immigration-us-trend.json](../../examples/immigration-us-trend.json).

**The question:**

> Compare coverage of immigration, deportation and border security.

## What Prism returned

| Term | Articles | Share | Critical | Growth (late vs early) | Negative-to-positive | vs all news |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **immigration** | 453,840 | 78% | 351,365 | 1.53× (rising) | 5.24 | 9.03× |
| **deportation** | 101,655 | 17.5% | 89,262 | 1.16× (flat) | 19.89 | 34.29× |
| **border security** | 26,116 | 4.5% | 20,969 | 0.61× (falling) | 3.16 | 5.45× |

![Comparison over time](../img/immigration-us-trend-compare.svg)

![Total coverage](../img/immigration-us-trend-share.svg)

> more coverage is attention, not importance, and a term that is also a common word will over-count — check each term's own volume against its sources panel

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/immigration-us-trend-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 3.0 | 3.0 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.0 | 1.5 | 0.0 |
| Visualisation from counted data | 3.0 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 3.5 | 1.0 | 1.0 | 1.0 |
| Data export with provenance | 3.5 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.0 | 1.0 | 1.0 |
| Accuracy against the corpus | 2.5 | 3.0 | 2.0 | 3.0 |
| Calibration and limits | 3.5 | 3.0 | 3.0 | 2.5 |
| Decision-grade verdict | 3.5 | 3.5 | 2.5 | 2.5 |
| Facet coverage | 4.0 | 3.5 | 1.0 | 0.0 |
| **Score /100** | **68.7** | 64.1 | 30.8 | 22.8 |

**Claude Opus judge:** A and D both grounded the term totals, shares and exact ratios in the call. A went further: it read critical share per term, named peaks with dates, quantified changes, read the censoring correctly and shipped two exports with executable follow-ups. D misread the censoring, treating May as a partial month, and offered no runnable drill-down. B and C honestly declined or estimated, but C's guessed shares contradict the measured ordering, so neither supports a decision.

**GPT judge:** C is the strongest decision aid: it gives a reproducible same-window ranking, complete chart series, and careful separation of critical orientation from sentiment. B adds useful drill-down and comparison detail, but its endpoint treatment conflicts with the source’s censoring caveat; C also has a censor-date mistake, while A and D lack grounded measurements.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/immigration-us-trend/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/immigration-us-trend.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Compare coverage of immigration, deportation and border security.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.compare" \
  -H 'content-type: application/json' \
  -d '{"terms": ["immigration", "deportation", "border security"], "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_terms']["fn"](**{'terms': ['immigration', 'deportation', 'border security'], 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
