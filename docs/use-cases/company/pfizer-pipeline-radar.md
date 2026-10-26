# mRNA beyond COVID

[Company & competitive intelligence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Pipeline intelligence for a pharma competitor.  
> **Why it is hard.** The COVID papers swamp the non-COVID ones; the radar must show the newest work.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [pfizer-pipeline-radar.json](../../examples/pfizer-pipeline-radar.json).

**The question:**

> What is new in mRNA vaccine research beyond COVID?

## What Prism returned

### Direction of travel

| Series | Window | First → last | Peak | Late third vs early third | Direction |
| --- | --- | --- | --- | ---: | --- |
| Research papers (typed corpus) | 2017 – 2025 | 4,245 → 17,102 | 17,102 (2025) | 2.95× | rising |
| News articles | 2019-01-01 – 2026-05-01 | 2 → 42 | 783 (2025-09-01) | 3.37× | rising |

**Framing shift since 2023:** cautionary share 12.6% before vs 10.8% since (-1.8 points): *framing is broadly unchanged*.

### New work since 2023

*the most-cited typed papers published since the start year whose title carries one of the subject's own phrases*

| Year | Paper | Venue | Orientation | Cited by |
| ---: | --- | --- | --- | ---: |
| 2023 | [A Comprehensive Review of mRNA Vaccines](https://doi.org/10.3390/ijms24032700) | International Journal of Molecular Sciences | descriptive | 379 |
| 2023 | [Immunogenicity of lipid nanoparticles and its impact on the efficacy of mRNA vaccines and therapeutics](https://doi.org/10.1038/s12276-023-01086-x) | Experimental & Molecular Medicine | descriptive | 331 |
| 2023 | [Circulating Spike Protein Detected in Post–COVID-19 mRNA Vaccine Myocarditis](https://doi.org/10.1161/circulationaha.122.061025) | Circulation | promising | 222 |
| 2023 | [mRNA vaccines in disease prevention and treatment](https://doi.org/10.1038/s41392-023-01579-1) | Signal Transduction and Targeted Therapy | descriptive | 202 |
| 2024 | [XBB.1.5 monovalent mRNA vaccine booster elicits robust neutralizing antibodies against XBB subvariants and JN.1](https://doi.org/10.1016/j.chom.2024.01.014) | Cell Host & Microbe | promising | 166 |
| 2023 | [Recent Advancement in mRNA Vaccine Development and Applications](https://doi.org/10.3390/pharmaceutics15071972) | Pharmaceutics | comparative | 143 |
| 2023 | [Research Advances on the Stability of mRNA Vaccines](https://doi.org/10.3390/v15030668) | Viruses | problem_identifying | 139 |
| 2023 | [Adverse events following COVID‐19 mRNA vaccines: A systematic review of cardiovascular complication, thrombosis, and thr](https://doi.org/10.1002/iid3.807) | Immunity Inflammation and Disease | descriptive | 134 |
| 2023 | [Recent Advances in the Lipid Nanoparticle-Mediated Delivery of mRNA Vaccines](https://doi.org/10.3390/vaccines11030658) | Vaccines | problem_identifying | 122 |
| 2023 | [mRNA vaccine in cancer therapy: Current advance and future outlook](https://doi.org/10.1002/ctm2.1384) | Clinical and Translational Medicine | promising | 120 |

![Most-cited new work](../img/pfizer-pipeline-radar-new-work.svg)

### What the research covers and the news does not

| Research topic | Papers | News articles |
| --- | ---: | ---: |
| vaccines and immunoinformatics approaches | 55,853 | 0 |
| SARS-CoV-2 and COVID-19 Research | 18,072 | 0 |
| Immunotherapy and Immune Responses | 15,130 | 0 |
| Monoclonal and Polyclonal Antibodies Research | 9,087 | 0 |
| T-cell and B-cell Immunology | 5,259 | 0 |
| Animal Virus Infections Studies | 3,987 | 0 |
| Influenza Virus Research Studies | 3,950 | 0 |
| RNA Interference and Gene Delivery | 3,931 | 0 |

![Under-covered topics](../img/pfizer-pipeline-radar-under-covered.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/pfizer-pipeline-radar-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 3.0 | 1.0 | 0.5 |
| Measured comparison | 3.5 | 4.0 | 1.5 | 2.0 |
| Visualisation from counted data | 3.5 | 3.5 | 1.0 | 0.5 |
| Exploration and drill-down | 3.5 | 2.0 | 1.5 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.5 |
| Reproducibility | 5.0 | 4.0 | 1.0 | 0.0 |
| Traceable references | 3.5 | 3.5 | 1.0 | 0.0 |
| Accuracy against the corpus | 4.0 | 4.0 | 3.0 | 1.5 |
| Calibration and limits | 4.0 | 4.0 | 3.0 | 3.5 |
| Decision-grade verdict | 4.0 | 3.0 | 3.5 | 3.0 |
| Facet coverage | 4.5 | 3.5 | 1.5 | 1.5 |
| **Score /100** | **78.2** | 68.8 | 36.0 | 25.2 |

**Claude Opus judge:** A and B both grounded their numbers in the radar call. A went further: it used the full thirds and news trend, recomputed exactly, and said plainly that the data cannot isolate non-COVID work, giving low confidence and naming the calls that would close the gap. B dropped the news series and overstated its confidence. C offered useful but unmeasured clinical context, honestly labelled. D attached fabricated DOIs to a confident narrative, which disqualifies it for decision use.

**GPT judge:** D is strongest for a decision-maker: it traces the broad research and news trends, names concrete papers and themes, and clearly warns that COVID-heavy data cannot answer non-COVID momentum. Its mixed-lane growth comparison and endpoint-only chart need care; C is more disciplined about the limits of the evidence but gives a thinner trend and drilldown.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/pfizer-pipeline-radar/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/pfizer-pipeline-radar.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is new in mRNA vaccine research beyond COVID?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.radar" \
  -H 'content-type: application/json' \
  -d '{"topic": "mrna vaccine", "since_year": 2023}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_radar']["fn"](**{'topic': 'mrna vaccine', 'since_year': 2023})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
