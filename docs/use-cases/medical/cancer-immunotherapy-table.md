# Immunotherapy evidence table

[Medical & clinical evidence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** One research question answered across many rows: a spreadsheet you can export.  
> **Why it is hard.** Each row needs its own source; a single answer pasted into ten rows is a fabrication.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below. Saved responses: [cancer-immunotherapy-table.json](../../examples/cancer-immunotherapy-table.json).

**The question:**

> Build me a table: for each cancer type, what does the research say about immunotherapy response rates?

## What Prism returned

Answered **4 of 6** rows. A blank value means the corpus does not state one; it is never filled in.

| Row | Value | Measures | Papers | Top source |
| --- | --- | --- | ---: | --- |
| **melanoma** | 32.4% | partial or complete response rate | 3 | [Early Readout on Overall Survival of Patients With Melanoma Treated With Immunotherapy Using a Novel Imaging Analysis.](https://doi.org/10.1001/jamaoncol.2021.6818) |
| **non-small cell lung cancer** | 0.80 [95% CI, 0.74 to 0.88] | objective response rate risk ratio | 3 | [Immune Checkpoint Inhibitors in Epidermal Growth Factor Receptor-Tyrosine Kinase Inhibitor-Resistant Chemotherapy-Naïve ](https://doi.org/10.1200/PO-24-00907) |
| **renal cell carcinoma** | – |  | 4 | [Age-Related Survival Disparities in Advanced Renal Carcinoma in the Immune Checkpoint Inhibitor Era using the SEER Datab](https://doi.org/10.1038/s41598-025-06297-y) |
| **bladder cancer** | 44.4% | overall response rate | 4 | [Randomized Phase 1 Trial of Pembrolizumab with Sequential Versus Concomitant Stereotactic Body Radiotherapy in Metastati](https://doi.org/10.1016/j.eururo.2019.01.009) |
| **colorectal cancer** | 55.6% | response rate per RECIST1.1 at month-2 | 5 | [Ethnic diversity in treatment response for colorectal cancer: proof of concept for radiomics-driven enrichment trials.](https://doi.org/10.1007/s00330-023-09862-z) |
| **breast cancer** | – |  | – |  |

![Papers per row](../img/cancer-immunotherapy-table-papers.svg)

**Export:** the same rows as CSV, straight from the response:

```csv
row,value,measures,papers,top_source_title,top_source_url
"melanoma","32.4%","partial or complete response rate","3","Early Readout on Overall Survival of Patients With Melanoma Treated With Immunotherapy Using a Novel Imaging Analysis.","https://doi.org/10.1001/jamaoncol.2021.6818"
"non-small cell lung cancer","0.80 [95% CI, 0.74 to 0.88]","objective response rate risk ratio","3","Immune Checkpoint Inhibitors in Epidermal Growth Factor Receptor-Tyrosine Kinase Inhibitor-Resistant Chemotherapy-Naïve Advanced Non-Small Cell Lung Cancer: A Meta-Analysis Based on Eight Randomized Trials.","https://doi.org/10.1200/PO-24-00907"
"renal cell carcinoma","","","4","Age-Related Survival Disparities in Advanced Renal Carcinoma in the Immune Checkpoint Inhibitor Era using the SEER Database and Meta-analysis.","https://doi.org/10.1038/s41598-025-06297-y"
"bladder cancer","44.4%","overall response rate","4","Randomized Phase 1 Trial of Pembrolizumab with Sequential Versus Concomitant Stereotactic Body Radiotherapy in Metastatic Urothelial Carcinoma.","https://doi.org/10.1016/j.eururo.2019.01.009"
"colorectal cancer","55.6%","response rate per RECIST1.1 at month-2","5","Ethnic diversity in treatment response for colorectal cancer: proof of concept for radiomics-driven enrichment trials.","https://doi.org/10.1007/s00330-023-09862-z"
"breast cancer","","","","",""
```

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/cancer-immunotherapy-table-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured comparison | 3.5 | 1.0 | 2.0 | 1.5 |
| Visualisation from counted data | 0.0 | 0.0 | 0.0 | 0.0 |
| Exploration and drill-down | 1.0 | 1.0 | 1.0 | 1.0 |
| Data export with provenance | 3.0 | 4.5 | 1.0 | 1.0 |
| Reproducibility | 4.0 | 3.0 | 1.0 | 1.0 |
| Traceable references | 4.0 | 4.0 | 1.0 | 1.0 |
| Accuracy against the corpus | 5.0 | 4.5 | 3.0 | 1.0 |
| Calibration and limits | 4.5 | 4.0 | 3.0 | 3.0 |
| Decision-grade verdict | 4.5 | 4.5 | 0.0 | 3.0 |
| Facet coverage | 4.0 | 4.0 | 1.0 | 1.0 |
| **Score /100** | **68.8** | 62.7 | 25.6 | 27.4 |

**Claude Opus judge:** B and D both stayed faithful to the single recorded table call, kept nulls as nulls, and refused to rank non-comparable figures. D went further by reading the rows critically: the colorectal figure is a radiomics subgroup, the melanoma figure is an imaging study, and the breast news item is off-topic. A and C answered from memory; A presented wrong trial figures and a bad DOI as sourced fact, while C at least labelled every value as an estimate.

**GPT judge:** B is the strongest decision aid: it identifies the four reported rows, distinguishes the NSCLC risk ratio from response proportions, and explains why the figures cannot support a cross-cancer ranking. A has the cleaner export and provenance hygiene, but B’s within-row arm comparison and more explicit interpretation of the colorectal evidence make its answer more useful while remaining consistent with the record.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/cancer-immunotherapy-table/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/cancer-immunotherapy-table.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Build me a table: for each cancer type, what does the research say about immunotherapy response rates?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.table" \
  -H 'content-type: application/json' \
  -d '{"rows": ["melanoma", "non-small cell lung cancer", "renal cell carcinoma", "bladder cancer", "colorectal cancer", "breast cancer"], "question": "immune checkpoint inhibitor response rate"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_table']["fn"](**{'rows': ['melanoma', 'non-small cell lung cancer', 'renal cell carcinoma', 'bladder cancer', 'colorectal cancer', 'breast cancer'], 'question': 'immune checkpoint inhibitor response rate'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
