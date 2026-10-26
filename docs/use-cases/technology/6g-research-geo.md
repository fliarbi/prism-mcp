# 6G research geography

[Technology & AI](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Country-level technology leadership.  
> **Why it is hard.** Patents publish ~18 months late; recent years are censored, not falling.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below. Saved responses: [6g-research-geo.json](../../examples/6g-research-geo.json).

**The question:**

> Which countries lead 6G research and patents?

## What Prism returned

Four different questions, kept apart because they measure different things: where the **authors** are, where the **journal** is published, where the **news** is about, and where the **patent applicants** are.

![Where the research is done](../img/6g-research-geo-research-authorship.svg)

![Where it is published](../img/6g-research-geo-research-publication.svg)

![News by country](../img/6g-research-geo-news-geo.svg)

| Rank | Where the research is done | Where it is published | Where it is reported |
| ---: | --- | --- | --- |
| 1 | Egypt (1) | England (2) | United States (1,395) |
| 2 | Iran (1) |  | India (1,058) |
| 3 |  |  | Finland (569) |
| 4 |  |  | China (437) |
| 5 |  |  | South Korea (319) |
| 6 |  |  | Japan (309) |
| 7 |  |  | United Kingdom (302) |
| 8 |  |  | Spain (279) |
| 9 |  |  | Germany (175) |
| 10 |  |  | France (167) |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/6g-research-geo-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured comparison | 4.0 | 4.0 | 2.0 | 0.0 |
| Visualisation from counted data | 3.0 | 0.0 | 0.0 | 0.0 |
| Exploration and drill-down | 3.0 | 3.0 | 1.0 | 0.5 |
| Data export with provenance | 3.5 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.0 | 1.0 | 1.0 |
| Accuracy against the corpus | 4.0 | 4.5 | 3.5 | 4.0 |
| Calibration and limits | 3.5 | 4.0 | 2.5 | 3.0 |
| Decision-grade verdict | 4.0 | 4.0 | 3.0 | 3.0 |
| Facet coverage | 4.5 | 4.0 | 1.0 | 2.0 |
| **Score /100** | **74.6** | 68.0 | 35.4 | 33.0 |

**Claude Opus judge:** C and A both read the database correctly: the research and patent lanes are empty or near-empty, and news shows only attention. C went further with recomputable ratios, a traced chart, both research and news exports, and it caught the Central African Republic place-resolution artifact. B and D answered from memory and were honest about it, but they give a decision-maker nothing measured, and B's patent shares are unverifiable.

**GPT judge:** C is the strongest decision aid: it separates the thin research evidence, empty patent-origin result and partial news geography, and its reported values trace cleanly. D adds a useful chart and broader exports, but its chart covers only news and it makes a stronger-than-supported claim about the Central African Republic row.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/6g-research-geo/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/6g-research-geo.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Which countries lead 6G research and patents?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.geography" \
  -H 'content-type: application/json' \
  -d '{"claim": "6G wireless networks"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['global_comparison']["fn"](**{'claim': '6G wireless networks'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `global_comparison` (57.1 s) → `news_geography` (22.7 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
