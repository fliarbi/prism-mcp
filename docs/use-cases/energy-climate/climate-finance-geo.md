# Climate finance geography

[Energy & climate](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Research vs news geography of a negotiation topic.  
> **Why it is hard.** Global South coverage vs Global North research.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below. Saved responses: [climate-finance-geo.json](../../examples/climate-finance-geo.json).

**The question:**

> Where is climate finance studied and where is it in the news?

## What Prism returned

Four different questions, kept apart because they measure different things: where the **authors** are, where the **journal** is published, where the **news** is about, and where the **patent applicants** are.

![News by country](../img/climate-finance-geo-news-geo.svg)

| Rank | Where it is reported |
| ---: | --- |
| 1 | United States (1,772) |
| 2 | Azerbaijan (1,550) |
| 3 | India (1,194) |
| 4 | Brazil (981) |
| 5 | China (941) |
| 6 | United Kingdom (721) |
| 7 | France (582) |
| 8 | United Arab Emirates (469) |
| 9 | Germany (459) |
| 10 | Nigeria (305) |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/climate-finance-geo-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured comparison | 4.0 | 4.5 | 0.5 | 0.5 |
| Visualisation from counted data | 4.5 | 0.0 | 0.0 | 0.0 |
| Exploration and drill-down | 3.5 | 3.5 | 1.0 | 1.0 |
| Data export with provenance | 3.0 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 4.5 | 4.5 | 1.0 | 1.0 |
| Accuracy against the corpus | 3.5 | 4.0 | 2.0 | 3.5 |
| Calibration and limits | 4.0 | 4.5 | 2.0 | 3.0 |
| Decision-grade verdict | 4.0 | 4.0 | 2.0 | 2.0 |
| Facet coverage | 4.0 | 4.0 | 1.0 | 1.0 |
| **Score /100** | **78.4** | 72.7 | 24.5 | 28.9 |

**Claude Opus judge:** B and D both grounded the news geography correctly and recognised the empty research lanes, so they did not invent a studied-vs-reported gap. D is the stronger of the two: it adds a traced chart, catches the small news block inside c1, and gives a properly bounded low-confidence verdict. A answered from memory and misdefined placed_pct, while C was honest but empty.

**GPT judge:** A best supports a decision-maker: it quantifies the news geography, states the empty research result, and keeps the two lanes from being mistaken for a measured mismatch. C is more visually complete, but its unsupported CSV rows and interpretation of lift weaken trust; neither deliverable can establish where climate finance is studied from these records.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/climate-finance-geo/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/climate-finance-geo.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Where is climate finance studied and where is it in the news?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.geography" \
  -H 'content-type: application/json' \
  -d '{"claim": "Climate finance"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['global_comparison']["fn"](**{'claim': 'Climate finance'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `global_comparison` (96.6 s) → `news_geography` (14.7 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
