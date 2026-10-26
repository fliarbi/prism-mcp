# Inflation vs recession in the news

[Finance & markets](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Which macro fear dominated, and when the narrative turned.  
> **Why it is hard.** Overlapping terms; the comparison must be on one scale and one window.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · 2024-06-01 to 2026-06-01 (exclusive) · all listed tables passed strict index partition reads and historical row floors. Saved responses: [inflation-vs-recession.json](../../examples/inflation-vs-recession.json).

**The question:**

> Compare news coverage of inflation, recession and interest rates over the last two years.

## What Prism returned

| Term | Articles | Share | Critical | Growth (late vs early) | Negative-to-positive | vs all news |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **inflation** | 456,860 | 65.8% | 304,187 | 1.09× (flat) | 1.81 | 3.12× |
| **recession** | 50,279 | 7.2% | 32,021 | 0.55× (falling) | 2.27 | 3.91× |
| **interest rates** | 186,782 | 26.9% | 115,455 | 0.79× (falling) | 1.28 | 2.21× |

![Comparison over time](../img/inflation-vs-recession-compare.svg)

![Total coverage](../img/inflation-vs-recession-share.svg)

> more coverage is attention, not importance, and a term that is also a common word will over-count — check each term's own volume against its sources panel

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/inflation-vs-recession-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 2.5 | 1.0 | 0.5 |
| Measured comparison | 5.0 | 4.0 | 1.5 | 0.5 |
| Visualisation from counted data | 4.0 | 2.5 | 1.0 | 0.5 |
| Exploration and drill-down | 2.0 | 2.0 | 1.5 | 1.0 |
| Data export with provenance | 5.0 | 4.0 | 1.0 | 0.5 |
| Reproducibility | 5.0 | 4.0 | 0.0 | 1.0 |
| Accuracy against the corpus | 4.0 | 1.5 | 2.5 | 4.0 |
| Calibration and limits | 4.5 | 2.5 | 3.5 | 3.5 |
| Decision-grade verdict | 3.5 | 3.0 | 2.0 | 3.0 |
| Facet coverage | 4.0 | 3.5 | 2.0 | 1.5 |
| **Score /100** | **82.4** | 58.0 | 31.1 | 34.2 |

**Claude Opus judge:** C was the only deliverable that read the measured record correctly end to end. Its ratios and peaks recompute exactly, it understood that combined counts are not unique articles, it applied censoring to the right month and it flagged data anomalies. A used the same data but misread the censored month and claimed rising trends against the tool's own direction labels. B offered memory-based estimates that contradicted the data, and D declined to answer.

**GPT judge:** B is the strongest decision aid: it provides a traced, same-window comparison, monthly series, quantified contrasts, and usable exports. Its unsupported coverage check and overconfident recession interpretation lower confidence; C is less reliable because it misreads the censored month, while A and D do not deliver measured comparisons.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/inflation-vs-recession/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/inflation-vs-recession.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Compare news coverage of inflation, recession and interest rates over the last two years.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.compare" \
  -H 'content-type: application/json' \
  -d '{"terms": ["inflation", "recession", "interest rates"], "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_terms']["fn"](**{'terms': ['inflation', 'recession', 'interest rates'], 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
