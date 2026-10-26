# Chips race in the news

[Technology & AI](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Geopolitics of chips, measured as attention.  
> **Why it is hard.** Export-control coverage spikes on US announcements.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · 2024-06-01 to 2026-06-01 (exclusive) · all listed tables passed strict index partition reads and historical row floors. Saved responses: [semiconductors-compare.json](../../examples/semiconductors-compare.json).

**The question:**

> Compare news coverage of semiconductors, TSMC and chip export controls.

## What Prism returned

| Term | Articles | Share | Critical | Growth (late vs early) | Negative-to-positive | vs all news |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **semiconductor** | 128,051 | 74.4% | 72,469 | 1.54× (rising) | 0.18 | 0.31× |
| **tsmc** | 36,563 | 21.3% | 25,235 | 1.32× (rising) | 0.39 | 0.67× |
| **export controls** | 7,399 | 4.3% | 6,403 | 2.9× (rising) | 2.45 | 4.22× |

![Comparison over time](../img/semiconductors-compare-compare.svg)

![Total coverage](../img/semiconductors-compare-share.svg)

> more coverage is attention, not importance, and a term that is also a common word will over-count — check each term's own volume against its sources panel

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/semiconductors-compare-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.0 | 1.0 | 0.0 |
| Visualisation from counted data | 3.0 | 3.0 | 1.0 | 0.0 |
| Exploration and drill-down | 3.0 | 2.0 | 1.0 | 1.0 |
| Data export with provenance | 3.0 | 4.5 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 3.5 | 0.0 | 1.0 |
| Accuracy against the corpus | 3.5 | 3.5 | 3.0 | 3.5 |
| Calibration and limits | 4.5 | 3.0 | 3.0 | 3.0 |
| Decision-grade verdict | 3.5 | 3.5 | 3.0 | 2.5 |
| Facet coverage | 4.5 | 4.0 | 1.5 | 0.5 |
| **Score /100** | **74.2** | 70.0 | 32.0 | 25.7 |

**Claude Opus judge:** B and C both reported traced figures from the same news.compare call. C went further: it decomposed critical share by term, named the peaks and the October 2025 export-control spike (1,773 vs 195 the month before), and flagged undefined fields and the generic-term over-count. B instead gave cleaner, complete exports. A gave an estimated term ordering that contradicts the measured data, and D gave no answer at all.

**GPT judge:** A is the strongest decision aid: it provides the complete traced monthly series, comparable totals, and caveats, while avoiding D’s unsupported reading of critical coverage as negative tone. D covers more facets and offers stronger limits, but its sparse chart and partial monthly export weaken auditability, and its verdict overstates what the tone and generic export-controls match can show.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/semiconductors-compare/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/semiconductors-compare.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Compare news coverage of semiconductors, TSMC and chip export controls.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.compare" \
  -H 'content-type: application/json' \
  -d '{"terms": ["semiconductor", "tsmc", "export controls"], "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_terms']["fn"](**{'terms': ['semiconductor', 'tsmc', 'export controls'], 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
