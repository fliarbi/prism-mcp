# Climate impact on crop yields

[Agriculture & food security](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A per-crop evidence table, export-ready.  
> **Why it is hard.** Each crop has a separate literature; one number cannot serve all rows.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below. Saved responses: [crop-yields-climate-table.json](../../examples/crop-yields-climate-table.json).

**The question:**

> For each crop, what does research say about climate change impact on yield?

## What Prism returned

Answered **5 of 5** rows. A blank value means the corpus does not state one; it is never filled in.

| Row | Value | Measures | Papers | Top source |
| --- | --- | --- | ---: | --- |
| **wheat** | 57.32% | grain yield decrease | 8 | [How Does the Environment Affect Wheat Yield and Protein Content Response to Drought? A Meta-Analysis](https://doi.org/10.3389/fpls.2022.896985) |
| **rice** | 11% | grain yield increase | 8 | [Co-incorporation of manure and inorganic fertilizer improves leaf physiological traits, rice production and soil functio](https://doi.org/10.1038/s41598-021-89246-9) |
| **maize** | 22 ± 13% | percentage change in maize yield | 8 | [Global irrigation contribution to wheat and maize yield](https://doi.org/10.1038/s41467-021-21498-5) |
| **soybean** | 16% | soybean yield decrease per °C warming | 8 | [Impacts of recent climate change on Wisconsin corn and soybean yield trends](https://doi.org/10.1088/1748-9326/3/3/034003) |
| **millet** | 24% | percentage of yields obtained on former kraal fields | 6 | [Efficacy of Nutrient Management Options for Finger Millet Production on Degraded Smallholder Farms in Eastern Uganda](https://doi.org/10.3389/fsufs.2021.674926) |

![Papers per row](../img/crop-yields-climate-table-papers.svg)

**Export:** the same rows as CSV, straight from the response:

```csv
row,value,measures,papers,top_source_title,top_source_url
"wheat","57.32%","grain yield decrease","8","How Does the Environment Affect Wheat Yield and Protein Content Response to Drought? A Meta-Analysis","https://doi.org/10.3389/fpls.2022.896985"
"rice","11%","grain yield increase","8","Co-incorporation of manure and inorganic fertilizer improves leaf physiological traits, rice production and soil functionality in a paddy field","https://doi.org/10.1038/s41598-021-89246-9"
"maize","22 ± 13%","percentage change in maize yield","8","Global irrigation contribution to wheat and maize yield","https://doi.org/10.1038/s41467-021-21498-5"
"soybean","16%","soybean yield decrease per °C warming","8","Impacts of recent climate change on Wisconsin corn and soybean yield trends","https://doi.org/10.1088/1748-9326/3/3/034003"
"millet","24%","percentage of yields obtained on former kraal fields","6","Efficacy of Nutrient Management Options for Finger Millet Production on Degraded Smallholder Farms in Eastern Uganda","https://doi.org/10.3389/fsufs.2021.674926"
```

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/crop-yields-climate-table-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured comparison | 4.5 | 1.0 | 2.0 | 0.5 |
| Visualisation from counted data | 0.0 | 0.0 | 1.0 | 0.0 |
| Exploration and drill-down | 1.0 | 1.0 | 1.0 | 1.0 |
| Data export with provenance | 0.0 | 4.0 | 1.0 | 1.0 |
| Reproducibility | 5.0 | 3.0 | 1.0 | 0.0 |
| Traceable references | 4.5 | 4.5 | 4.0 | 3.0 |
| Accuracy against the corpus | 5.0 | 5.0 | 2.5 | 3.0 |
| Calibration and limits | 5.0 | 3.0 | 3.0 | 3.0 |
| Decision-grade verdict | 4.5 | 4.5 | 3.0 | 2.0 |
| Facet coverage | 4.5 | 4.5 | 2.0 | 1.0 |
| **Score /100** | **70.1** | 62.9 | 41.1 | 29.4 |

**Claude Opus judge:** B and C both saw that the database's five crop values mostly measure fertilizer, irrigation and soil effects, not climate impact. B went further: it kept the one valid like-for-like warming contrast (soybean vs corn per °C), quoted every source verbatim and placed its limits next to the numbers. A gave the most useful substantive answer from real, correctly recalled literature, but none of it is measured or reproducible. D gave neither data nor a usable answer, and it carried a garbled reference title.

**GPT judge:** B best equips a decision-maker to distinguish the one returned warming result from drought, irrigation, fertilizer, and soil-management figures, while stating that the crops cannot be ranked from these mixed measures. D is the strongest traceable row export and reaches the same cautious decision, but B adds the more useful explicit comparison and fuller limits.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/crop-yields-climate-table/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/crop-yields-climate-table.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
For each crop, what does research say about climate change impact on yield?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.table" \
  -H 'content-type: application/json' \
  -d '{"rows": ["wheat", "rice", "maize", "soybean", "millet"], "question": "climate change impact on crop yield percent"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_table']["fn"](**{'rows': ['wheat', 'rice', 'maize', 'soybean', 'millet'], 'question': 'climate change impact on crop yield percent'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
