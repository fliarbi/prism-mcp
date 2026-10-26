# Vitamin D and depression

[Medical & clinical evidence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Separate the trials from the association studies and state the mix of findings.  
> **Why it is hard.** Hundreds of association papers drown a handful of RCTs; counting them equally gives the wrong answer.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [vitamin-d-depression.json](../../examples/vitamin-d-depression.json).

**The question:**

> Is vitamin D supplementation effective for depression?

## What Prism returned

### How much evidence exists

| Corpus | Records on both sides of the claim | Window |
| --- | ---: | --- |
| Typed research papers | 50,757 | 2017-2025 |
| Papers with abstracts | 4,027 | 1990-2025 |
| the health literature index records | 65,359 | 1990-2025 |
| News articles | 2,040 | 2019-01-01..2026-06-01 |
| Patents | 0 | 2005-2024 |
| arXiv preprints | 1 | 2005-2025 |

![Evidence volume by corpus](../img/vitamin-d-depression-volumes.svg)

![Framing of the literature](../img/vitamin-d-depression-sides.svg)

*orientation is a label on the paper's own framing, not a verdict on the claim; this corpus starts in 2017* Contested share: **21.8%**.

### The strongest evidence, read

> few titles carry both sides of this claim, so the documents read were chosen by the subject in the title and the outcome in the abstract.

Prism read 3 sources: **2 support, 1 contradict, 0 qualify** (tier-weighted {"supports": 7, "contradicts": 4, "qualifies": 0}). Each quote is copied from the abstract and verified against it; 0 candidate quotes failed that check and were dropped.

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2018 | [Efficacy of vitamin D supplementation in major depression](https://doi.org/10.4103/jpgm.jpgm_571_17)<br><sub>Journal of Postgraduate Medicine</sub> | review | supports | Pooled mean effect size for vitamin D supplementation on depressive symptom ratings in major depression was 0.58 (95% confidence interval, 0.45–0.72). |
| 2008 | [Effects of vitamin D supplementation on symptoms of depression in overweight and obese subjects: randomized double blind](https://doi.org/10.1111/j.1365-2796.2008.02008.x)<br><sub>Journal of Internal Medicine</sub> | article | supports | In the two groups given vitamin D, but not in the placebo group, there was a significant improvement in BDI scores after 1 year. |
| 2012 | [Depressed adolescents in a case‐series were low in vitamin D and depression was ameliorated by vitamin D supplementation](https://doi.org/10.1111/j.1651-2227.2012.02655.x)<br><sub>Acta Paediatrica</sub> | article | unrelated | There was a significant amelioration of depression according to the MFQ-S (p < 0.05). |
| 2025 | [The effect of vitamin D supplementation on mental and functional health outcomes in African Americans with type 2 diabet](https://doi.org/10.1016/j.jsbmb.2025.106698)<br><sub>The Journal of steroid biochemistry and molecular biology</sub> | trial | unrelated | Vitamin D3 4000 IU/day in AAs with T2DM did not produce significant difference in mental and functional health scores compared to 600 IU/day. |
| 2013 | [Efficacy of Vitamin D Supplementation in Depression in Adults: A Systematic Review](https://doi.org/10.1210/jc.2013-3450)<br><sub>The Journal of Clinical Endocrinology & Metabolism</sub> | review | contradicts | Results of the classical meta-analysis showed no significant effect of Vit D supplementation on postintervention depression scores (standardized mean difference = -0.14, 95% confidence interval = -0.41 to 0.13, P = .32; odds ratio = 0.93, 95% confidence interv… |
| 2012 | [Vitamin D Supplementation and Depression in the Women's Health Initiative Calcium and Vitamin D Trial](https://doi.org/10.1093/aje/kwr482)<br><sub>American Journal of Epidemiology</sub> | article | unrelated | The findings do not support a relation between supplementation with 400 IU/day of vitamin D(3) along with calcium and depression in older women. |
| 2025 | [Vitamin D for Painful Diabetic Neuropathy: A Systematic Review and Meta-Analysis of Randomised Controlled Trials.](https://doi.org/10.1002/edm2.70118)<br><sub>Endocrinology, diabetes & metabolism</sub> | meta_analysis | unrelated | The primary outcome was pain intensity measured with validated tools. |
| 2025 | [Risk of suicide, suicide attempt, and suicidal ideation among people with vitamin D deficiency: a systematic review and ](https://doi.org/10.1186/s12888-025-06613-w)<br><sub>BMC psychiatry</sub> | meta_analysis | unrelated | Meta-analysis included observational studies that assessed the association between SBs and vitamin D blood serum level and/or vitamin D deficiency. |

![Study designs](../img/vitamin-d-depression-tiers.svg)

### What disagrees

Prism's counter-evidence pass found no source that directly contradicts the claim among those it read (tally {"supports": 0, "contradicts": 0, "qualifies": 0, "unrelated": 6, "unread": 2}).

> No verified document verdict supports a wording recommendation for this claim.

### Numbers you can quote

| Figure | Measures | Population | Source |
| --- | --- | --- | --- |
| **0.58 (95% confidence interval, 0.45–0.72)** | pooled mean effect size for depressive symptom ratings | major depression | [Efficacy of vitamin D supplementation in major depression](https://doi.org/10.4103/jpgm.jpgm_571_17) 2018 |
| **-0.14, 95% confidence interval = -0.41 to 0.13** | standardized mean difference for postintervention depression scores |  | [Efficacy of Vitamin D Supplementation in Depression in Adults: A Systematic Review](https://doi.org/10.1210/jc.2013-3450) 2013 |
| **0.93, 95% confidence interval = 0.54 to 1.59** | odds ratio for postintervention depression scores |  | [Efficacy of Vitamin D Supplementation in Depression in Adults: A Systematic Review](https://doi.org/10.1210/jc.2013-3450) 2013 |

![Research output per year](../img/vitamin-d-depression-research-series.svg)

**Extracted disease-factor claims** (1 claims; extracted claims, not papers — one paper can produce several, and the same finding restated in ten papers counts ten times): treatment/decreases (unspecified) ×1

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/vitamin-d-depression-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.0 | 4.0 | 1.5 | 1.5 |
| Visualisation from counted data | 4.0 | 4.0 | 1.0 | 1.0 |
| Exploration and drill-down | 1.0 | 2.0 | 1.0 | 1.0 |
| Data export with provenance | 0.0 | 3.0 | 1.0 | 0.5 |
| Reproducibility | 4.0 | 4.5 | 0.0 | 1.0 |
| Traceable references | 4.5 | 4.5 | 1.0 | 0.5 |
| Accuracy against the corpus | 4.0 | 4.5 | 2.0 | 1.5 |
| Calibration and limits | 4.5 | 4.5 | 3.0 | 3.0 |
| Decision-grade verdict | 3.5 | 4.5 | 0.0 | 3.0 |
| Facet coverage | 4.5 | 3.5 | 1.0 | 1.0 |
| **Score /100** | 71.4 | **80.2** | 21.5 | 26.3 |

**Claude Opus judge:** D and A both grounded their answer in the recorded calls, with verbatim quotes and resolving DOIs. D went further: it surfaced the 16-paper subject/outcome intersection, the news trend, the source-fit failures and per-corpus gaps to today, which justified a low-confidence 'not established' verdict. B and C reached clinically sensible conclusions from memory, but could not be traced; C also attached mismatched or unresolvable identifiers to its key references.

**GPT judge:** A best supports a treatment decision: it gives a cautious answer, distinguishes broad vitamin D publication volume from depression-specific evidence, and presents the conflicting review findings with traceable sources. B covers more corpus facets, but its unsupported news detail and treatment of source-fit failures as contradictions reduce confidence; C and D rely on unverified specifics.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/vitamin-d-depression/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/vitamin-d-depression.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Is vitamin D supplementation effective for depression?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.evidence" \
  -H 'content-type: application/json' \
  -d '{"claim": "Vitamin D supplementation reduces depression symptoms", "limit": 10}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['find_evidence']["fn"](**{'claim': 'Vitamin D supplementation reduces depression symptoms', 'limit': 10})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `find_evidence` (76.6 s) → `find_counter_evidence` (17.2 s) → `find_statistics` (9.5 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
