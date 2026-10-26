# Data protection law geography

[Policy & regulation](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** The geography of a regulatory field.  
> **Why it is hard.** GDPR dominates research; DPDP Act dominates Indian news.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below. Saved responses: [data-protection-geo.json](../../examples/data-protection-geo.json).

**The question:**

> Where is data protection law studied and reported most?

## What Prism returned

Four different questions, kept apart because they measure different things: where the **authors** are, where the **journal** is published, where the **news** is about, and where the **patent applicants** are.

![Where the research is done](../img/data-protection-geo-research-authorship.svg)

![Where it is published](../img/data-protection-geo-research-publication.svg)

![Who patents it](../img/data-protection-geo-patent-origin.svg)

![News by country](../img/data-protection-geo-news-geo.svg)

| Rank | Where the research is done | Where it is published | Who patents it | Where it is reported |
| ---: | --- | --- | --- | --- |
| 1 | United States (24) | England (49) | Us (10) | United States (30,974) |
| 2 | United Kingdom (19) | United States (49) | Kr (6) | United Kingdom (11,412) |
| 3 | Netherlands (10) | Netherlands (12) |  (4) | India (6,832) |
| 4 | Germany (9) | Germany (11) | De (4) | China (5,822) |
| 5 | Belgium (7) | Canada (11) |  | Colombia (3,136) |
| 6 | Ireland (5) | Ireland (6) |  | France (2,883) |
| 7 | Italy (5) | Spain (4) |  | Australia (2,831) |
| 8 | Spain (5) | Switzerland (3) |  | Germany (2,605) |
| 9 | Portugal (4) | China (2) |  | Brazil (2,403) |
| 10 | Poland (4) | Belgium (2) |  | Indonesia (2,286) |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/data-protection-geo-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured comparison | 2.0 | 4.0 | 0.5 | 0.0 |
| Visualisation from counted data | 0.0 | 0.0 | 0.0 | 0.0 |
| Exploration and drill-down | 3.5 | 2.0 | 1.0 | 0.5 |
| Data export with provenance | 3.5 | 3.5 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.0 | 0.0 | 1.0 |
| Accuracy against the corpus | 2.5 | 4.0 | 3.0 | 4.0 |
| Calibration and limits | 3.5 | 4.0 | 3.0 | 3.0 |
| Decision-grade verdict | 2.5 | 3.5 | 2.5 | 2.0 |
| Facet coverage | 4.0 | 4.0 | 1.0 | 0.5 |
| **Score /100** | 55.2 | **64.4** | 27.9 | 27.9 |

**Claude Opus judge:** A and B both ground every number in the two calls and keep the lanes separate. B makes the sharper studied-vs-reported contrast but carries a false coverage=full label, an untraced row-floor figure and a placeholder chart window. A is narrower but clean, so it is the safer decision document. C and D honestly decline to measure, but D also misreads placed_pct and wrongly declares the patent lane empty.

**GPT judge:** C is the strongest decision aid: it gives traceable research and news leaders, distinguishes author affiliation from journal location and article subject, and puts placement coverage and timing limits near the numbers. D offers richer drill-downs and exports, but its headline 86.7% comparison and chart combine incompatible news and research slices, so they cannot support a reliable decision.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/data-protection-geo/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/data-protection-geo.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Where is data protection law studied and reported most?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.geography" \
  -H 'content-type: application/json' \
  -d '{"claim": "Data protection regulation"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['global_comparison']["fn"](**{'claim': 'Data protection regulation'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `global_comparison` (85.8 s) → `news_geography` (37.3 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
