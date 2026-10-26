# Alzheimer's drug research radar

[Medical & clinical evidence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** New work, momentum and framing shift since 2022.  
> **Why it is hard.** Lecanemab and donanemab approvals moved the field in 2023-2025, after most models' training data.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [alzheimers-drugs-radar.json](../../examples/alzheimers-drugs-radar.json).

**The question:**

> What has changed recently in Alzheimer's disease drug research?

## What Prism returned

### Direction of travel

| Series | Window | First → last | Peak | Late third vs early third | Direction |
| --- | --- | --- | --- | ---: | --- |
| Research papers (typed corpus) | 2017 – 2025 | 6,039 → 14,178 | 14,178 (2025) | 1.8× | rising |
| News articles | 2019-01-01 – 2026-05-01 | 3 → 3 | 629 (2026-04-01) | 19.05× | rising |

**Framing shift since 2022:** cautionary share 10.1% before vs 12.1% since (+2.0 points): *framing is broadly unchanged*.

### New work since 2022

*the most-cited typed papers published since the start year whose title carries one of the subject's own phrases*

| Year | Paper | Venue | Orientation | Cited by |
| ---: | --- | --- | --- | ---: |
| 2022 | [Intranasal Delivery of BACE1 siRNA and Rapamycin by Dual Targets Modified Nanoparticles for Alzheimer's Disease Therapy](https://doi.org/10.1002/smll.202203182) | Small | breakthrough | 124 |
| 2022 | [Celastrol enhances transcription factor EB (TFEB)-mediated autophagy and mitigates Tau pathology: Implications for Alzhe](https://doi.org/10.1016/j.apsb.2022.01.017) | Acta Pharmaceutica Sinica B | breakthrough | 99 |
| 2023 | [Caffeic acid loaded into engineered lipid nanoparticles for Alzheimer's disease therapy](https://doi.org/10.1016/j.colsurfb.2023.113270) | Colloids and Surfaces B Biointerfaces | promising | 60 |
| 2022 | [Transferrin-functionalized liposomes loaded with vitamin VB12 for Alzheimer's disease therapy](https://doi.org/10.1016/j.ijpharm.2022.122167) | International Journal of Pharmaceutics | promising | 56 |
| 2024 | [Insulin Delivery to the Brain via the Nasal Route: Unraveling the Potential for Alzheimer's Disease Therapy](https://doi.org/10.1007/s13346-024-01558-1) | Drug Delivery and Translational Research | cautionary | 42 |
| 2025 | [Nose-to-brain delivery of targeted lipid nanoparticles as two-pronged β-amyloid nanoscavenger for Alzheimer's disease th](https://doi.org/10.1016/j.apsb.2025.02.035) | Acta Pharmaceutica Sinica B | breakthrough | 23 |
| 2022 | [Investigating binding mechanism of thymoquinone to human transferrin, targeting Alzheimer's disease therapy](https://doi.org/10.1002/jcb.30299) | Journal of Cellular Biochemistry | breakthrough | 23 |
| 2024 | [Systemic Administration of Neurotransmitter‐Derived Lipidoids‐PROTACs‐DNA Nanocomplex Promotes Tau Clearance and Cogniti](https://doi.org/10.1002/adhm.202400149) | Advanced Healthcare Materials | breakthrough | 22 |
| 2022 | [Aptamer conjugated polydopamine-coated gold nanoparticles as a dual-action nanoplatform targeting β-amyloid peptide for ](https://doi.org/10.1039/d2tb01499h) | Journal of Materials Chemistry B | breakthrough | 20 |
| 2023 | [Computational Prediction of 3,5-Diaryl-1H-Pyrazole and spiropyrazolines derivatives as potential acetylcholinesterase in](https://doi.org/10.1080/07391102.2023.2252116) | Journal of Biomolecular Structure and Dynamics | promising | 17 |

![Most-cited new work](../img/alzheimers-drugs-radar-new-work.svg)

### What the research covers and the news does not

| Research topic | Papers | News articles |
| --- | ---: | ---: |
| Alzheimer's disease research and treatments | 80,857 | 0 |
| Dementia and Cognitive Impairment Research | 19,108 | 0 |
| Neuroinflammation and Neurodegeneration Mechanisms | 10,745 | 0 |
| Cholinesterase and Neurodegenerative Diseases | 7,606 | 0 |
| Parkinson's Disease Mechanisms and Treatments | 6,514 | 0 |
| Neuroscience and Neuropharmacology Research | 5,354 | 0 |
| Neurological Disease Mechanisms and Treatments | 4,769 | 0 |
| Tryptophan and brain disorders | 4,244 | 0 |

![Under-covered topics](../img/alzheimers-drugs-radar-under-covered.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/alzheimers-drugs-radar-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 3.5 | 1.5 | 0.0 |
| Measured comparison | 2.5 | 4.0 | 2.0 | 2.0 |
| Visualisation from counted data | 3.5 | 3.5 | 1.0 | 1.0 |
| Exploration and drill-down | 2.5 | 2.0 | 1.5 | 1.0 |
| Data export with provenance | 2.5 | 3.0 | 1.0 | 1.0 |
| Reproducibility | 4.5 | 4.5 | 0.0 | 0.0 |
| Traceable references | 3.0 | 3.0 | 3.0 | 4.0 |
| Accuracy against the corpus | 3.0 | 4.5 | 3.0 | 3.0 |
| Calibration and limits | 4.0 | 4.5 | 3.0 | 3.5 |
| Decision-grade verdict | 4.0 | 3.5 | 4.0 | 3.5 |
| Facet coverage | 4.5 | 4.0 | 1.5 | 1.5 |
| **Score /100** | 70.2 | **74.0** | 39.7 | 37.2 |

**Claude Opus judge:** A and D are the only grounded deliverables and score nearly level. D covers more facets, but it miscounts the orientation labels and mislabels the framing windows. A is cleaner but answers weakly. B gives the most domain-useful account of the lecanemab/donanemab shift, but it is from memory and cannot be reproduced.

**GPT judge:** B is the strongest decision deliverable: it traces and qualifies the research trend, covers framing and news, and supplies reproducible calls, while being candid about the limits of selected title matches. C covers more facets, but its cross-lane growth comparison and news-rise wording weaken its reading; neither database-backed response directly answers the clinical and regulatory changes highlighted by the question.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/alzheimers-drugs-radar/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/alzheimers-drugs-radar.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What has changed recently in Alzheimer's disease drug research?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.radar" \
  -H 'content-type: application/json' \
  -d '{"topic": "alzheimer disease treatment", "since_year": 2022}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_radar']["fn"](**{'topic': 'alzheimer disease treatment', 'since_year': 2022})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
