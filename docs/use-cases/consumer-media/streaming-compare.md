# Netflix vs Disney+ vs Prime Video

[Consumer, brands & media](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Media-brand attention share.  
> **Why it is hard.** Netflix dominates; growth tells the challenger story.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · 2024-06-01 to 2026-06-01 (exclusive) · all listed tables passed strict index partition reads and historical row floors. Saved responses: [streaming-compare.json](../../examples/streaming-compare.json).

**The question:**

> Compare news coverage of Netflix, Disney+ and Amazon Prime Video.

## What Prism returned

| Term | Articles | Share | Critical | Growth (late vs early) | Negative-to-positive | vs all news |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **netflix** | 533,727 | 72.4% | 96,986 | 1.44× (rising) | 0.27 | 0.47× |
| **disney+** | 103,301 | 14% | 13,007 | 1.32× (rising) | 0.18 | 0.31× |
| **prime video** | 99,892 | 13.6% | 9,370 | 1.52× (rising) | 0.14 | 0.24× |

![Comparison over time](../img/streaming-compare-compare.svg)

![Total coverage](../img/streaming-compare-share.svg)

> more coverage is attention, not importance, and a term that is also a common word will over-count — check each term's own volume against its sources panel

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/streaming-compare-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 3.0 | 3.5 | 0.0 | 0.0 |
| Measured comparison | 5.0 | 4.5 | 1.0 | 0.0 |
| Visualisation from counted data | 3.0 | 2.0 | 0.0 | 0.0 |
| Exploration and drill-down | 2.0 | 1.0 | 1.0 | 1.0 |
| Data export with provenance | 3.5 | 3.5 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.0 | 1.0 | 1.0 |
| Accuracy against the corpus | 2.5 | 3.0 | 3.0 | 3.0 |
| Calibration and limits | 3.0 | 3.5 | 3.0 | 2.5 |
| Decision-grade verdict | 3.0 | 3.5 | 2.5 | 2.5 |
| Facet coverage | 3.5 | 3.5 | 1.0 | 0.5 |
| **Score /100** | 64.3 | **64.5** | 28.3 | 23.5 |

**Claude Opus judge:** A gives the decision-maker the full traced monthly series for all three services. It also computes the share shift that actually tells the challenger story: Prime Video gains about 2.8 points while Netflix slips 3.4. It adds a critical-share contrast, with only a minor critical-peak slip. D's numbers trace, but it reduces the trend to two endpoints and misreads the censoring rule. B and C measured nothing, and B's estimate index points the wrong way on Disney+ vs Prime.

**GPT judge:** A is the most decision-ready: it quantifies the attention gap and challenger growth, preserves key caveats, and supplies a traced monthly export. C has richer charts and tables, but its treatment of censored May 2026 as a real collapse undermines its trend and verdict; B and D appropriately acknowledge that they cannot measure the comparison.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/streaming-compare/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/streaming-compare.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Compare news coverage of Netflix, Disney+ and Amazon Prime Video.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.compare" \
  -H 'content-type: application/json' \
  -d '{"terms": ["netflix", "disney+", "prime video"], "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_terms']["fn"](**{'terms': ['netflix', 'disney+', 'prime video'], 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
