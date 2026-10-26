# Long COVID statistics

[Medical & clinical evidence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Verbatim figures with the sentence and source each came from.  
> **Why it is hard.** Prevalence figures range from 5% to 50% depending on definition; a figure without its population is useless.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [long-covid-statistics.json](../../examples/long-covid-statistics.json).

**The question:**

> What are the most cited statistics on long COVID prevalence, and where do they come from?

## What Prism returned

### How much evidence exists

| Corpus | Records on both sides of the claim | Window |
| --- | ---: | --- |
| Typed research papers | 396,354 | 2017-2025 |
| Papers with abstracts | 5,691 | 1990-2025 |
| the health literature index records | 322,360 | 1990-2025 |
| News articles | 17,339 | 2019-01-01..2026-06-01 |
| Patents | 76 | 2005-2024 |
| arXiv preprints | 14 | 2005-2025 |

![Evidence volume by corpus](../img/long-covid-statistics-volumes.svg)

![Framing of the literature](../img/long-covid-statistics-sides.svg)

*orientation is a label on the paper's own framing, not a verdict on the claim; this corpus starts in 2017* Contested share: **29%**.

### The strongest evidence, read

Prism read 1 sources: **1 support, 0 contradict, 0 qualify** (tier-weighted {"supports": 4, "contradicts": 0, "qualifies": 0}). Each quote is copied from the abstract and verified against it; 0 candidate quotes failed that check and were dropped.

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2021 | [Long covid—mechanisms, risk factors, and management](https://doi.org/10.1136/bmj.n1648)<br><sub>BMJ</sub> | review | unrelated | Long covid can affect the whole spectrum of people with covid-19, from those with very mild acute disease to the most severe forms. |
| 2021 | [Long COVID or post-COVID-19 syndrome: putative pathophysiology, risk factors, and treatments](https://doi.org/10.1080/23744235.2021.1924397)<br><sub>Infectious Diseases</sub> | review | unrelated | Long COVID ... affects COVID-19 survivors at all levels of disease severity, even younger adults, children, and those not hospitalized. |
| 2021 | [Symptoms, complications and management of long COVID: a review](https://doi.org/10.1177/01410768211032850)<br><sub>Journal of the Royal Society of Medicine</sub> | review | supports | a significant proportion continue to experience symptoms and complications after their acute illness. |
| 2025 | [S100 Protein and Interleukin Biomarkers Among COVID-19 Subjects With and Without Pneumonia: A Systematic Review and Meta](https://doi.org/10.3389/bjbs.2025.15355)<br><sub>British journal of biomedical science</sub> | meta_analysis | unrelated | This meta-analysis underscores the potential of IL-6, IL-10, and S100 proteins as important biomarkers in evaluating COVID-19 severity, offering valuable insights to help clinical management. |
| 2025 | [Bioelectrical Impedance in Monitoring Hyperhydration and Muscle Wasting in Critically Ill Corona Virus Disease (COVID-19](https://pubmed.ncbi.nlm.nih.gov/41511101/)<br><sub>Physiological research</sub> | trial | unrelated | BIVA is a practical tool for monitoring hydration, but not muscle mass, in critically ill patients. |
| 2025 | [Clot twist - D-dimer analysis of healthy adults receiving heterologous or homologous booster COVID-19 vaccine after a si](https://doi.org/10.7196/SAMJ.2025.v115i8.3121)<br><sub>South African medical journal = Suid-Afrikaanse tydskrif vir geneeskunde</sub> | trial | unrelated | Elevated D-dimer levels in asymptomatic, low-risk adults were unexpectedly common and not associated with thromboembolism. |
| 2025 | [Effect of dynamic neuromuscular stabilization exercises on postural stability, pulmonary function, motor performance, an](https://doi.org/10.1016/j.jbmt.2025.09.029)<br><sub>Journal of bodywork and movement therapies</sub> | trial | unrelated | DNS exercises can be effectively integrated into physical exercise and rehabilitative programs to improve PS, PF, MP, and QoL in COVID-19 survivors with post‑COVID symptoms. |
| 2022 | [Pathophysiology and mechanism of long COVID: a comprehensive review](https://doi.org/10.1080/07853890.2022.2076901)<br><sub>Annals of Medicine</sub> | review | unrelated | the number of patients enduring persistent symptoms long after acute infection is a matter of concern. |

![Study designs](../img/long-covid-statistics-tiers.svg)

### What disagrees

Prism's counter-evidence pass found no source that directly contradicts the claim among those it read (tally {"supports": 0, "contradicts": 0, "qualifies": 0, "unrelated": 7, "unread": 1}).

> No verified document verdict supports a wording recommendation for this claim.

### Numbers you can quote

| Figure | Measures | Population | Source |
| --- | --- | --- | --- |
| **52.9%** | proportion of survivors with impaired lung function | COVID-19 survivors | [Subphenotypic classification of COVID-19 survivors and response to telerehabilitation: a latent class analysis.](https://doi.org/10.2340/jrm.v57.42726) 2025 |
| **47.1%** | proportion of survivors with better lung function | COVID-19 survivors | [Subphenotypic classification of COVID-19 survivors and response to telerehabilitation: a latent class analysis.](https://doi.org/10.2340/jrm.v57.42726) 2025 |

![Research output per year](../img/long-covid-statistics-research-series.svg)

**Extracted disease-factor claims** (2,495 claims; extracted claims, not papers — one paper can produce several, and the same finding restated in ten papers counts ten times): association/na (unspecified) ×1061, association/na (observational) ×283, risk_factor/increases (unspecified) ×222, risk_factor/increases (observational) ×127, association/na (clinical) ×120, association/na (review_meta) ×74

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/long-covid-statistics-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 2.5 | 3.0 | 1.0 | 0.0 |
| Measured comparison | 3.0 | 3.5 | 2.0 | 1.5 |
| Visualisation from counted data | 2.5 | 3.0 | 1.0 | 0.5 |
| Exploration and drill-down | 2.0 | 3.0 | 1.5 | 1.0 |
| Data export with provenance | 2.5 | 3.0 | 1.0 | 0.5 |
| Reproducibility | 4.0 | 4.0 | 1.0 | 1.0 |
| Traceable references | 4.0 | 4.0 | 2.5 | 1.0 |
| Accuracy against the corpus | 3.0 | 4.0 | 3.0 | 1.0 |
| Calibration and limits | 4.0 | 3.0 | 3.5 | 2.5 |
| Decision-grade verdict | 3.0 | 4.0 | 3.0 | 2.5 |
| Facet coverage | 3.0 | 2.5 | 1.5 | 1.5 |
| **Score /100** | 61.4 | **68.9** | 38.7 | 23.5 |

**Claude Opus judge:** A was the only deliverable that stayed fully traced and handled the censored period correctly. It told the decision-maker plainly that the retrieved statistics are not prevalence estimates and set out what to commission next. B had richer context, including the useful phrase audit, but plotted a censored year as a decline and included an untraced news figure. C and D answered from memory: D's figures were broadly right and honestly flagged, while C misattributed its headline sources.

**GPT judge:** D is the strongest decision aid because it clearly separates highly cited reviews and survivor lung-function percentages from actual long COVID prevalence, then recommends against using them as prevalence headlines. C reaches a similar caution, but spends more of the deliverable on broad corpus trends and stance counts that do not answer the prevalence question.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/long-covid-statistics/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/long-covid-statistics.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What are the most cited statistics on long COVID prevalence, and where do they come from?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.evidence" \
  -H 'content-type: application/json' \
  -d '{"claim": "Long COVID affects a significant share of people after infection", "limit": 10}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['find_evidence']["fn"](**{'claim': 'Long COVID affects a significant share of people after infection', 'limit': 10})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `find_evidence` (189.6 s) → `find_counter_evidence` (39.5 s) → `find_statistics` (43.1 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
