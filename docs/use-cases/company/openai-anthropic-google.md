# OpenAI vs Anthropic vs Google DeepMind

[Company & competitive intelligence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** AI-lab competitive landscape by coverage.  
> **Why it is hard.** OpenAI dominates volume; share and growth tell a different story.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · 2024-06-01 to 2026-06-01 (exclusive) · all listed tables passed strict index partition reads and historical row floors. Saved responses: [openai-anthropic-google.json](../../examples/openai-anthropic-google.json).

**The question:**

> Compare news attention on OpenAI, Anthropic and Google DeepMind.

## What Prism returned

| Term | Articles | Share | Critical | Growth (late vs early) | Negative-to-positive | vs all news |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **openai** | 255,044 | 75.8% | 190,992 | 2.06× (rising) | 0.39 | 0.67× |
| **anthropic** | 70,192 | 20.9% | 51,731 | 5.68× (rising) | 0.45 | 0.78× |
| **deepmind** | 11,047 | 3.3% | 8,688 | 1.4× (rising) | 0.18 | 0.31× |

![Comparison over time](../img/openai-anthropic-google-compare.svg)

![Total coverage](../img/openai-anthropic-google-share.svg)

> more coverage is attention, not importance, and a term that is also a common word will over-count — check each term's own volume against its sources panel

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/openai-anthropic-google-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 3.5 | 3.5 | 1.0 | 0.5 |
| Measured comparison | 4.5 | 4.5 | 1.0 | 0.5 |
| Visualisation from counted data | 3.0 | 3.5 | 0.5 | 0.5 |
| Exploration and drill-down | 3.0 | 3.0 | 1.0 | 1.0 |
| Data export with provenance | 3.0 | 4.0 | 1.0 | 1.0 |
| Reproducibility | 4.0 | 4.0 | 0.0 | 1.0 |
| Accuracy against the corpus | 3.0 | 3.0 | 3.0 | 3.0 |
| Calibration and limits | 3.5 | 4.0 | 2.5 | 2.5 |
| Decision-grade verdict | 4.0 | 4.0 | 2.0 | 2.0 |
| Facet coverage | 4.0 | 3.5 | 1.0 | 0.5 |
| **Score /100** | 70.8 | **73.8** | 26.7 | 26.8 |

**Claude Opus judge:** C answered the hard part: OpenAI has the most volume, but Anthropic's gap to OpenAI narrowed from about 7.9:1 to 1.9:1. The ratios recompute exactly, the censoring is read correctly, and the anomalies are flagged. A had cleaner full-series exports and exact share arithmetic, but it misread May as censored and framed its decision around volume alone. B and D were honest but unmeasured.

**GPT judge:** D is the strongest decision aid: it compares all three terms on a shared scale, shows the monthly pattern, and carries the ingest caveat into its reading. A covers more caveats and follow-up questions, but its sampled trend export and unsupported coverage claim weaken trust; D still needs item-level evidence and a clearer reconciliation of May's partial status.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/openai-anthropic-google/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/openai-anthropic-google.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Compare news attention on OpenAI, Anthropic and Google DeepMind.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.compare" \
  -H 'content-type: application/json' \
  -d '{"terms": ["openai", "anthropic", "deepmind"], "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_terms']["fn"](**{'terms': ['openai', 'anthropic', 'deepmind'], 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
