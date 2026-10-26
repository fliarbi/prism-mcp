# Tariffs and stock markets

[Finance & markets](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** How tariff policy fed market fear in the news.  
> **Why it is hard.** 2025 tariff announcements created sharp spikes; the comparison must show the timing.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · 2024-06-01 to 2026-06-01 (exclusive) · all listed tables passed strict index partition reads and historical row floors. Saved responses: [tariffs-markets.json](../../examples/tariffs-markets.json).

**The question:**

> Compare news coverage of tariffs vs trade war vs stock market crash.

## What Prism returned

| Term | Articles | Share | Critical | Growth (late vs early) | Negative-to-positive | vs all news |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **tariffs** | 479,208 | 88.4% | 365,884 | 2.18× (rising) | 2.9 | 5.0× |
| **trade war** | 61,081 | 11.3% | 48,061 | 1.35× (rising) | 4.59 | 7.91× |
| **stock market crash** | 1,648 | 0.3% | 1,154 | 0.92× (flat) | 4.23 | 7.29× |

![Comparison over time](../img/tariffs-markets-compare.svg)

![Total coverage](../img/tariffs-markets-share.svg)

> more coverage is attention, not importance, and a term that is also a common word will over-count — check each term's own volume against its sources panel

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/tariffs-markets-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 1.5 | 0.0 |
| Visualisation from counted data | 2.5 | 4.5 | 1.0 | 0.0 |
| Exploration and drill-down | 3.5 | 1.0 | 1.5 | 1.0 |
| Data export with provenance | 3.0 | 0.0 | 1.0 | 0.0 |
| Reproducibility | 4.5 | 3.0 | 0.0 | 1.0 |
| Accuracy against the corpus | 3.5 | 3.0 | 3.0 | 4.0 |
| Calibration and limits | 4.0 | 3.0 | 4.0 | 3.0 |
| Decision-grade verdict | 4.0 | 3.5 | 3.0 | 1.5 |
| Facet coverage | 4.5 | 4.0 | 1.0 | 0.5 |
| **Score /100** | **75.7** | 62.1 | 34.6 | 24.3 |

**Claude Opus judge:** B and C both traced the measured April 2025 spike: 93,515 tariffs, 19,452 trade war and 329 stock market crash articles. B quantified the rise and decay, defined its baseline and placed the specific limits next to the numbers. C plotted the full series but zero-filled tone columns and misplaced the censoring caveat onto May 2026. A and D answered from memory or not at all: honest, but they give a decision-maker nothing measured.

**GPT judge:** C is the most decision-ready: it quantifies the shared April 2025 spike, ranks the three terms on a common window, and provides reproducible calls and useful caveats. Its selected-month chart/export and unresolved trend-label tension keep the timing evidence from being fully audit-ready; A has the complete chart but its export contradicts the recorded tone counts.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/tariffs-markets/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/tariffs-markets.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Compare news coverage of tariffs vs trade war vs stock market crash.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.compare" \
  -H 'content-type: application/json' \
  -d '{"terms": ["tariffs", "trade war", "stock market crash"], "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_terms']["fn"](**{'terms': ['tariffs', 'trade war', 'stock market crash'], 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
