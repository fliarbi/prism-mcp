# Floods vs heatwaves vs wildfires

[Environment & disasters](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Hazard attention for a disaster-risk team.  
> **Why it is hard.** Seasonality: each hazard peaks in a different month.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · 2024-06-01 to 2026-06-01 (exclusive) · all listed tables passed strict index partition reads and historical row floors. Saved responses: [floods-vs-heatwaves.json](../../examples/floods-vs-heatwaves.json).

**The question:**

> Compare news coverage of floods, heatwaves and wildfires.

## What Prism returned

| Term | Articles | Share | Critical | Growth (late vs early) | Negative-to-positive | vs all news |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **floods** | 58,416 | 38.8% | 49,486 | 0.63× (falling) | 3.47 | 5.98× |
| **heatwave** | 22,552 | 15% | 14,217 | 1.09× (flat) | 2.29 | 3.95× |
| **wildfire** | 69,544 | 46.2% | 55,473 | 0.5× (falling) | 2.88 | 4.97× |

![Comparison over time](../img/floods-vs-heatwaves-compare.svg)

![Total coverage](../img/floods-vs-heatwaves-share.svg)

> more coverage is attention, not importance, and a term that is also a common word will over-count — check each term's own volume against its sources panel

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/floods-vs-heatwaves-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 3.5 | 3.0 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.0 | 1.0 | 0.0 |
| Visualisation from counted data | 4.0 | 2.5 | 1.0 | 0.5 |
| Exploration and drill-down | 3.0 | 1.0 | 1.0 | 1.0 |
| Data export with provenance | 4.5 | 1.5 | 1.0 | 0.0 |
| Reproducibility | 3.5 | 4.0 | 0.0 | 1.0 |
| Accuracy against the corpus | 3.5 | 2.5 | 2.0 | 4.0 |
| Calibration and limits | 4.0 | 3.5 | 3.5 | 3.0 |
| Decision-grade verdict | 3.5 | 3.0 | 2.0 | 2.5 |
| Facet coverage | 4.0 | 3.5 | 1.0 | 0.5 |
| **Score /100** | **75.1** | 57.6 | 27.0 | 28.0 |

**Claude Opus judge:** C was the only deliverable to read the data rather than restate it. It showed that wildfire's lead depends on the single January 2025 spike, recomputed a year-on-year split that disagrees with the tool's growth labels, and handled censoring correctly. B was traced and clean on its totals, but it misread the censoring and did not engage with seasonality or the spike. A and D honestly declined to measure, which leaves a decision-maker with nothing to act on.

**GPT judge:** A is the most decision-ready because it combines traced seasonal data, quantified same-window comparisons, complete exports and explicit caveats, though its trend reconciliation and unsupported coverage figures need correction. D is strong on the measured totals and limits but has inconsistent May handling; B is honest but offers no measurements, while C adds unsupported estimates.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/floods-vs-heatwaves/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/floods-vs-heatwaves.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Compare news coverage of floods, heatwaves and wildfires.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.compare" \
  -H 'content-type: application/json' \
  -d '{"terms": ["floods", "heatwave", "wildfire"], "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_terms']["fn"](**{'terms': ['floods', 'heatwave', 'wildfire'], 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
