# Where dengue is studied vs reported

[Public health & epidemiology](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** The gap between where a disease is studied and where it is reported.  
> **Why it is hard.** Research comes from the rich world; outbreaks happen elsewhere. The interesting signal is the mismatch.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below. Saved responses: [dengue-geography.json](../../examples/dengue-geography.json).

**The question:**

> Which countries research dengue most, and which ones does the news cover?

## What Prism returned

Four different questions, kept apart because they measure different things: where the **authors** are, where the **journal** is published, where the **news** is about, and where the **patent applicants** are.

![Where the research is done](../img/dengue-geography-research-authorship.svg)

![Where it is published](../img/dengue-geography-research-publication.svg)

![News by country](../img/dengue-geography-news-geo.svg)

| Rank | Where the research is done | Where it is published | Where it is reported |
| ---: | --- | --- | --- |
| 1 | United States (2,583) | United States (7,359) | India (3,010) |
| 2 | India (1,700) | England (4,706) | United States (1,614) |
| 3 | Brazil (1,689) | Netherlands (1,813) | Brazil (792) |
| 4 | China (1,061) | Switzerland (1,076) | Bangladesh (492) |
| 5 | Thailand (840) | Brazil (686) | United Kingdom (303) |
| 6 | Singapore (636) | India (635) | France (280) |
| 7 | Taiwan (542) | Germany (407) | Australia (232) |
| 8 | Malaysia (539) | Thailand (226) | Philippines (226) |
| 9 | France (495) | France (214) | China (209) |
| 10 | Australia (474) | China (204) | Mexico (194) |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/dengue-geography-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured comparison | 4.5 | 2.5 | 1.0 | 0.5 |
| Visualisation from counted data | 4.0 | 0.0 | 0.0 | 0.0 |
| Exploration and drill-down | 3.5 | 2.0 | 1.5 | 1.5 |
| Data export with provenance | 4.5 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.5 | 4.0 | 1.0 | 0.5 |
| Accuracy against the corpus | 4.0 | 3.5 | 2.5 | 4.0 |
| Calibration and limits | 4.0 | 3.5 | 3.0 | 2.5 |
| Decision-grade verdict | 3.0 | 3.0 | 2.0 | 2.5 |
| Facet coverage | 4.5 | 3.5 | 1.0 | 0.5 |
| **Score /100** | **80.2** | 56.2 | 29.6 | 29.5 |

**Claude Opus judge:** D and C both traced the same two calls, but only D turned them into the studied-versus-reported contrast the question asks for. D names the research-heavy, news-light countries and the reverse case, charts both lanes, and catches the share_pct denominator anomaly. C stayed with within-lane ratios, had no chart and slipped on the window gap. A and B made no measurements; A at least offered labelled hypotheses, while B offered nothing usable.

**GPT judge:** A is the strongest decision aid: it directly quantifies the research and news leaders, shows within-lane ratios, and exposes traceable country tables with detailed limits. D is careful and reproducible but leaves the central mismatch largely qualitative; B abstains accurately, while C substitutes unsupported estimates for measurements.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/dengue-geography/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/dengue-geography.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Which countries research dengue most, and which ones does the news cover?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.geography" \
  -H 'content-type: application/json' \
  -d '{"claim": "Dengue fever outbreaks"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['global_comparison']["fn"](**{'claim': 'Dengue fever outbreaks'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `global_comparison` (137.0 s) → `news_geography` (19.0 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
