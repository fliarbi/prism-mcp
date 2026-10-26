# Tesla vs BYD

[Company & competitive intelligence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Competitive attention share and tone, one scale.  
> **Why it is hard.** BYD overtook Tesla in EV sales in 2024-2025; does attention follow sales?  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · 2024-06-01 to 2026-06-01 (exclusive) · all listed tables passed strict index partition reads and historical row floors. Saved responses: [tesla-vs-byd.json](../../examples/tesla-vs-byd.json).

**The question:**

> Compare news coverage of Tesla and BYD over the last two years.

## What Prism returned

| Term | Articles | Share | Critical | Growth (late vs early) | Negative-to-positive | vs all news |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **tesla** | 215,756 | 81.8% | 137,701 | 0.89× (flat) | 0.83 | 1.43× |
| **byd** | 47,974 | 18.2% | 26,323 | 1.42× (rising) | 0.39 | 0.67× |

![Comparison over time](../img/tesla-vs-byd-compare.svg)

![Total coverage](../img/tesla-vs-byd-share.svg)

> more coverage is attention, not importance, and a term that is also a common word will over-count — check each term's own volume against its sources panel

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/tesla-vs-byd-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.0 | 0.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 1.0 | 0.5 |
| Visualisation from counted data | 4.0 | 4.0 | 0.0 | 0.0 |
| Exploration and drill-down | 2.0 | 2.0 | 1.0 | 1.0 |
| Data export with provenance | 4.5 | 4.5 | 0.0 | 0.0 |
| Reproducibility | 4.0 | 4.0 | 0.0 | 1.0 |
| Accuracy against the corpus | 3.5 | 4.0 | 3.5 | 3.5 |
| Calibration and limits | 4.0 | 4.0 | 3.5 | 3.0 |
| Decision-grade verdict | 0.0 | 4.0 | 2.5 | 2.0 |
| Facet coverage | 4.5 | 4.0 | 1.5 | 1.0 |
| **Score /100** | 40 | **78.6** | 26.7 | 25.8 |

**Claude Opus judge:** A and B both traced the full monthly series and exports correctly, and neither tested whether attention follows sales. A gave the richer reading (peaks, critical shares, the 2025-10 BYD anomaly) but placed an untagged, slightly wrong day count in its verdict, which voids it. B is exact throughout, and its verdict is supported and bounded. C and D were honest refusals with no measured content.

**GPT judge:** C is the strongest decision deliverable: it compares Tesla and BYD on the same traced monthly scale, quantifies their relative attention and growth, and bounds its conclusion by the corpus and window. B has similarly rich evidence and exports, but its invented verdict number fails the script gate; both reports still need executed follow-ups to explain the observed spikes.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/tesla-vs-byd/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/tesla-vs-byd.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Compare news coverage of Tesla and BYD over the last two years.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.compare" \
  -H 'content-type: application/json' \
  -d '{"terms": ["tesla", "byd"], "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_terms']["fn"](**{'terms': ['tesla', 'byd'], 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
