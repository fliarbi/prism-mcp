# Drug trafficking geography

[Crime & public safety](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** The research-vs-news geography of an organised-crime topic.  
> **Why it is hard.** Place resolution has acronym collisions; the caveat matters.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below. Saved responses: [drug-trafficking-geo.json](../../examples/drug-trafficking-geo.json).

**The question:**

> Where is drug trafficking studied and where is it reported?

## What Prism returned

Four different questions, kept apart because they measure different things: where the **authors** are, where the **journal** is published, where the **news** is about, and where the **patent applicants** are.

![Where the research is done](../img/drug-trafficking-geo-research-authorship.svg)

![Where it is published](../img/drug-trafficking-geo-research-publication.svg)

![News by country](../img/drug-trafficking-geo-news-geo.svg)

| Rank | Where the research is done | Where it is published | Where it is reported |
| ---: | --- | --- | --- |
| 1 | United Kingdom (1) | England (2) | United States (20,133) |
| 2 | United States (1) | Germany (1) | Mexico (5,996) |
| 3 |  | United States (1) | Venezuela (5,267) |
| 4 |  |  | India (4,200) |
| 5 |  |  | Canada (3,094) |
| 6 |  |  | Colombia (3,045) |
| 7 |  |  | China (2,848) |
| 8 |  |  | United Kingdom (2,364) |
| 9 |  |  | France (2,088) |
| 10 |  |  | Brazil (1,646) |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/drug-trafficking-geo-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured comparison | 3.0 | 3.0 | 0.5 | 0.5 |
| Visualisation from counted data | 3.0 | 0.0 | 0.0 | 0.0 |
| Exploration and drill-down | 3.5 | 2.5 | 1.5 | 1.5 |
| Data export with provenance | 3.0 | 4.5 | 1.0 | 0.0 |
| Reproducibility | 4.5 | 4.5 | 1.0 | 0.5 |
| Accuracy against the corpus | 4.5 | 4.0 | 3.5 | 3.5 |
| Calibration and limits | 4.0 | 3.0 | 3.0 | 2.5 |
| Decision-grade verdict | 3.5 | 3.0 | 2.5 | 2.5 |
| Facet coverage | 4.5 | 4.0 | 1.0 | 0.5 |
| **Score /100** | **75.2** | 63.5 | 33.2 | 28.0 |

**Claude Opus judge:** D was the only deliverable that grounded both lanes, charted the traced news shares, and read the evidence honestly. It concluded that a 2-paper research sample cannot support a studied-vs-reported verdict, and it named what would close the gap. C traced its numbers well but compared news to news instead of answering the studied-vs-reported question, and it lacked a chart. A and B were honest but unmeasured, with A at least offering a labelled hypothesis.

**GPT judge:** B is the strongest decision aid: it traces both research and news geography, explains why their counts cannot be directly compared, and carries the key coverage and timing caveats. Its main weakness is that the chart covers only news and the headline comparison does not establish a measured research-versus-reporting gap; C has stronger exports, but its comparison also stops short of that core contrast.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/drug-trafficking-geo/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/drug-trafficking-geo.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Where is drug trafficking studied and where is it reported?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.geography" \
  -H 'content-type: application/json' \
  -d '{"claim": "Drug trafficking"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['global_comparison']["fn"](**{'claim': 'Drug trafficking'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `global_comparison` (42.0 s) → `news_geography` (32.1 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
