# Edtech in the news

[Education & labour](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Sector attention and one company's crisis.  
> **Why it is hard.** Byju's collapse dominates Indian edtech coverage in 2024.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · 2024-06-01 to 2026-06-01 (exclusive) · all listed tables passed strict index partition reads and historical row floors. Saved responses: [edtech-compare.json](../../examples/edtech-compare.json).

**The question:**

> Compare news coverage of edtech, online learning and Byju's.

## What Prism returned

| Term | Articles | Share | Critical | Growth (late vs early) | Negative-to-positive | vs all news |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **edtech** | 28,697 | 58.8% | 17,157 | 1.06× (flat) | 0.14 | 0.24× |
| **online learning** | 19,147 | 39.2% | 4,359 | 0.82× (flat) | 0.12 | 0.21× |
| **byju's** | 993 | 2% | 896 | 0.24× (falling) | 3.87 | 6.67× |

![Comparison over time](../img/edtech-compare-compare.svg)

![Total coverage](../img/edtech-compare-share.svg)

> more coverage is attention, not importance, and a term that is also a common word will over-count — check each term's own volume against its sources panel

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/edtech-compare-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 3.5 | 1.0 | 0.0 |
| Measured comparison | 5.0 | 4.5 | 1.0 | 0.0 |
| Visualisation from counted data | 3.5 | 4.0 | 1.0 | 0.0 |
| Exploration and drill-down | 2.0 | 2.0 | 1.0 | 1.0 |
| Data export with provenance | 4.0 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.5 | 0.0 | 1.0 |
| Accuracy against the corpus | 3.5 | 3.5 | 3.5 | 4.0 |
| Calibration and limits | 3.0 | 2.5 | 4.0 | 4.0 |
| Decision-grade verdict | 3.5 | 3.5 | 3.0 | 2.0 |
| Facet coverage | 4.5 | 4.5 | 1.0 | 0.5 |
| **Score /100** | **74.8** | 73.4 | 34.3 | 27.4 |

**Claude Opus judge:** B alone turns the single news.compare call into a decision-ready answer. Its first-12 vs last-12 changes, ratios and critical-share contrasts all recompute exactly, and it shows Byju's is about 2% of volume but 90% critical, which undercuts the 'Byju's dominates' premise for this window. B also catches the summed (not deduplicated) combined total and the critical-vs-negative distinction. C used the same data but misread censoring and drew a misleading direction from endpoint months, while A and D offered only memory or nothing measurable.

**GPT judge:** B is strongest for a decision-maker: it gives a reproducible, same-window comparison, a complete monthly chart and export, and keeps attention counts distinct from importance and public opinion. D adds useful trend detail, but its unsupported coverage figures and contradiction about edtech being mostly non-critical weaken trust in its conclusion.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/edtech-compare/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/edtech-compare.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Compare news coverage of edtech, online learning and Byju's.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.compare" \
  -H 'content-type: application/json' \
  -d '{"terms": ["edtech", "online learning", "byju's"], "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_terms']["fn"](**{'terms': ['edtech', 'online learning', "byju's"], 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
