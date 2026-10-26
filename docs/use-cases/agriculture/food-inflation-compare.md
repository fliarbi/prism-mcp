# Food prices in the news

[Agriculture & food security](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Commodity narrative tracking for an Indian policy desk.  
> **Why it is hard.** Onion price coverage is seasonal and India-specific.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · 2024-06-01 to 2026-06-01 (exclusive) · all listed tables passed strict index partition reads and historical row floors. Saved responses: [food-inflation-compare.json](../../examples/food-inflation-compare.json).

**The question:**

> Compare coverage of food inflation, onion prices and wheat prices.

## What Prism returned

| Term | Articles | Share | Critical | Growth (late vs early) | Negative-to-positive | vs all news |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **food inflation** | 7,145 | 88.9% | 5,367 | 0.68× (falling) | 2.27 | 3.91× |
| **onion prices** | 446 | 5.6% | 225 | 0.54× (falling) | 1.99 | 3.43× |
| **wheat prices** | 442 | 5.5% | 233 | 1.3× (rising) | 2.03 | 3.5× |

![Comparison over time](../img/food-inflation-compare-compare.svg)

![Total coverage](../img/food-inflation-compare-share.svg)

> more coverage is attention, not importance, and a term that is also a common word will over-count — check each term's own volume against its sources panel

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/food-inflation-compare-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 3.5 | 3.5 | 1.0 | 0.0 |
| Measured comparison | 4.0 | 4.0 | 1.0 | 0.0 |
| Visualisation from counted data | 2.0 | 4.0 | 1.0 | 0.0 |
| Exploration and drill-down | 3.0 | 2.0 | 2.0 | 1.0 |
| Data export with provenance | 2.5 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 3.5 | 4.5 | 0.0 | 1.0 |
| Accuracy against the corpus | 3.5 | 3.0 | 3.5 | 3.5 |
| Calibration and limits | 3.5 | 4.0 | 2.5 | 2.5 |
| Decision-grade verdict | 3.0 | 2.5 | 2.5 | 2.0 |
| Facet coverage | 4.5 | 3.5 | 1.0 | 1.0 |
| **Score /100** | 65.0 | **70.0** | 32.0 | 24.1 |

**Claude Opus judge:** B and D both grounded every number in the single news.compare call, and A and C produced no measurements. D read the data more carefully: it named the spike months and computed critical shares. It also caught that the tool's direction labels contradict the endpoints, whereas B's verdict misstated the direction of onion coverage. D's weaknesses are a selected-months chart that drops the wheat spike and a verdict that restates the direction labels it had just questioned.

**GPT judge:** A is the strongest decision aid: it compares all three terms on one traced window, gives a complete monthly series and reproducible ratios, and distinguishes media attention from price movement. B adds useful spike observations but has material window, coverage, and overlap errors; C and D are transparent about missing measurements but do not answer the comparison.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/food-inflation-compare/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/food-inflation-compare.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Compare coverage of food inflation, onion prices and wheat prices.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.compare" \
  -H 'content-type: application/json' \
  -d '{"terms": ["food inflation", "onion prices", "wheat prices"], "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_terms']["fn"](**{'terms': ['food inflation', 'onion prices', 'wheat prices'], 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
