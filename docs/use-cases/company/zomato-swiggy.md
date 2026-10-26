# Zomato vs Swiggy

[Company & competitive intelligence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Indian quick-commerce rivalry by attention.  
> **Why it is hard.** Zomato renamed its parent to Eternal in 2025; a model may not know.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · 2024-06-01 to 2026-06-01 (exclusive) · all listed tables passed strict index partition reads and historical row floors. Saved responses: [zomato-swiggy.json](../../examples/zomato-swiggy.json).

**The question:**

> Compare Zomato and Swiggy in the news.

## What Prism returned

| Term | Articles | Share | Critical | Growth (late vs early) | Negative-to-positive | vs all news |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **zomato** | 22,619 | 50.9% | 12,538 | 0.51× (falling) | 0.33 | 0.57× |
| **swiggy** | 21,854 | 49.1% | 12,286 | 0.65× (falling) | 0.27 | 0.47× |

![Comparison over time](../img/zomato-swiggy-compare.svg)

![Total coverage](../img/zomato-swiggy-share.svg)

> more coverage is attention, not importance, and a term that is also a common word will over-count — check each term's own volume against its sources panel

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/zomato-swiggy-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 3.0 | 0.5 | 0.0 |
| Measured comparison | 4.5 | 4.0 | 0.5 | 0.5 |
| Visualisation from counted data | 4.5 | 3.0 | 0.0 | 0.0 |
| Exploration and drill-down | 2.0 | 2.0 | 1.0 | 1.0 |
| Data export with provenance | 4.5 | 2.5 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.0 | 0.0 | 0.5 |
| Accuracy against the corpus | 3.0 | 2.0 | 2.0 | 3.0 |
| Calibration and limits | 3.5 | 2.5 | 3.0 | 3.0 |
| Decision-grade verdict | 3.5 | 3.0 | 2.0 | 2.5 |
| Facet coverage | 4.0 | 3.0 | 1.0 | 0.5 |
| **Score /100** | **76.0** | 58.3 | 22.1 | 23.8 |

**Claude Opus judge:** A read the full traced series correctly. It named the peaks, computed exact declines and lead changes, decomposed tone, and flagged the Eternal rename and the overlap. C used the same data but compared only endpoints and misread the censoring, treating May 2026 as incomplete. B and D measured nothing; B also misdescribed combined_articles.

**GPT judge:** A is the most decision-ready: it gives the strongest traced volume and tone comparison, useful charts, and complete exports, though its recent-lead count and coverage claim need correction. D is close on the core comparison, but its false claim that May 2026 is censored materially distorts the trend and exports. B is careful but offers no measured comparison; C adds unsupported memory claims.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/zomato-swiggy/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/zomato-swiggy.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Compare Zomato and Swiggy in the news.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.compare" \
  -H 'content-type: application/json' \
  -d '{"terms": ["zomato", "swiggy"], "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_terms']["fn"](**{'terms': ['zomato', 'swiggy'], 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
