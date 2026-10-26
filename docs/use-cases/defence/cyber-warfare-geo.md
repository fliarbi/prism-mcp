# Cyber warfare geography

[Defence & geopolitics](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Country-level view of a domain of conflict.  
> **Why it is hard.** Attribution is political; the geography of coverage is itself a signal.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below. Saved responses: [cyber-warfare-geo.json](../../examples/cyber-warfare-geo.json).

**The question:**

> Where is cyber warfare studied and reported?

## What Prism returned

Four different questions, kept apart because they measure different things: where the **authors** are, where the **journal** is published, where the **news** is about, and where the **patent applicants** are.

![Where the research is done](../img/cyber-warfare-geo-research-authorship.svg)

![Where it is published](../img/cyber-warfare-geo-research-publication.svg)

![Who patents it](../img/cyber-warfare-geo-patent-origin.svg)

![News by country](../img/cyber-warfare-geo-news-geo.svg)

| Rank | Where the research is done | Where it is published | Who patents it | Where it is reported |
| ---: | --- | --- | --- | --- |
| 1 | Norway (1) | Switzerland (2) | Kr (5) | United States (523) |
| 2 | China (1) | England (2) | Us (2) | Russia (233) |
| 3 | Italy (1) | United States (1) |  | China (216) |
| 4 |  |  |  | Iran (180) |
| 5 |  |  |  | India (158) |
| 6 |  |  |  | Ukraine (146) |
| 7 |  |  |  | United Kingdom (144) |
| 8 |  |  |  | Israel (138) |
| 9 |  |  |  | Australia (71) |
| 10 |  |  |  | France (63) |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/cyber-warfare-geo-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured comparison | 4.0 | 2.5 | 0.5 | 0.0 |
| Visualisation from counted data | 3.0 | 0.0 | 0.0 | 0.0 |
| Exploration and drill-down | 3.0 | 4.0 | 1.0 | 1.5 |
| Data export with provenance | 4.0 | 3.5 | 1.0 | 1.0 |
| Reproducibility | 4.0 | 4.0 | 1.0 | 1.0 |
| Accuracy against the corpus | 3.5 | 3.5 | 2.5 | 3.0 |
| Calibration and limits | 4.5 | 4.0 | 3.0 | 2.5 |
| Decision-grade verdict | 3.0 | 3.5 | 2.5 | 2.0 |
| Facet coverage | 4.0 | 4.5 | 1.0 | 0.5 |
| **Score /100** | **72.4** | 64.5 | 29.4 | 27.7 |

**Claude Opus judge:** B and D used the same two calls. B read them critically: it noted that news rows overlap (2131 mentions vs 748 placed), flagged the conflict between the two news pulls and the undefined lift and share_pct baselines, and concluded that 'where it is studied' cannot be answered from 3 the health literature index papers. D presented the same sparse research rows as an answer at medium confidence and had no chart. A and C were honest about having no data, but C's memory map is the only one a decision-maker could act on qualitatively.

**GPT judge:** B best equips a decision-maker to distinguish where research authorship, journals, patents, and news attention are recorded, and it carries the clearest traceable drill-down and provenance. D offers a stronger same-window news comparison, but its unsupported overlap inference and lift interpretation weaken accuracy, while neither deliverable can establish a direct geographic ratio between studied and reported activity.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/cyber-warfare-geo/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/cyber-warfare-geo.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Where is cyber warfare studied and reported?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.geography" \
  -H 'content-type: application/json' \
  -d '{"claim": "Cyber warfare"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['global_comparison']["fn"](**{'claim': 'Cyber warfare'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `global_comparison` (71.9 s) → `news_geography` (14.3 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
