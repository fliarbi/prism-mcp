# Does metformin lower cancer risk?

[Medical & clinical evidence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A clinician-grade answer: the meta-analyses, the contrary trials, and the size of the effect.  
> **Why it is hard.** Observational meta-analyses say yes; randomised trials are weaker. A good answer has to separate the two tiers.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [metformin-cancer-risk.json](../../examples/metformin-cancer-risk.json).

**The question:**

> Does metformin reduce cancer risk in people with type 2 diabetes? How strong is the evidence and what disagrees?

## What Prism returned

### How much evidence exists

| Corpus | Records on both sides of the claim | Window |
| --- | ---: | --- |
| Typed research papers | 334 | 2017-2025 |
| Papers with abstracts | 196 | 1990-2025 |
| the health literature index records | 135 | 1990-2025 |
| News articles | 51 | 2019-01-01..2026-06-01 |
| Patents | 0 | 2005-2024 |
| arXiv preprints | 0 | 2005-2025 |

![Evidence volume by corpus](../img/metformin-cancer-risk-volumes.svg)

![Framing of the literature](../img/metformin-cancer-risk-sides.svg)

*orientation is a label on the paper's own framing, not a verdict on the claim; this corpus starts in 2017* Contested share: **32.3%**.

### The strongest evidence, read

Prism read 3 sources: **2 support, 1 contradict, 0 qualify** (tier-weighted {"supports": 12, "contradicts": 6, "qualifies": 0}). Each quote is copied from the abstract and verified against it; 2 candidate quotes failed that check and were dropped.

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2012 | [Cancer Risk in Diabetic Patients Treated with Metformin: A Systematic Review and Meta-analysis](https://doi.org/10.1371/journal.pone.0033411)<br><sub>PLoS ONE</sub> | meta_analysis | supports | the risks of cancer among metformin users were significantly lower than those among non-metformin users: the pooled RRs (95% confidence interval) were 0.66 (0.49-0.88) for cancer mortality, 0.67 (0.53-0.85) for all-cancer incidence, 0.68 (0.53-0.88) for colore… |
| 2024 | [Association of metformin use and cancer incidence: a systematic review and meta-analysis](https://doi.org/10.1093/jnci/djae021)<br><sub>JNCI Journal of the National Cancer Institute</sub> | meta_analysis | unrelated | Reduced risk for overall cancer was observed in case-control studies (RR = 0.55, 95% confidence interval [CI] = 0.30 to 0.80) and prospective cohort studies (RR = 0.65, 95% CI = 0.37 to 0.93). |
| 2020 | [The effect of metformin on lung cancer risk and survival in patients with type 2 diabetes mellitus: A meta-analysis.](https://doi.org/10.1111/jcpt.13167)<br><sub>Journal of clinical pharmacy and therapeutics</sub> | meta_analysis | supports | Metformin treatment was associated with decreased lung cancer incidence (HR 0.78; 95% CI 0.70-0.86) and increased lung cancer survival (HR 0.65; 95% CI 0.55-0.77). |
| 2023 | [Breast cancer risk for women with diabetes and the impact of metformin: A meta-analysis.](https://doi.org/10.1002/cam4.5545)<br><sub>Cancer medicine</sub> | meta_analysis | contradicts | No statistically significant reduction of BC risk was observed among metformin users. |
| 2024 | [Associations of metformin therapy treatment with endometrial cancer risk and prognosis: A systematic review and meta-ana](https://doi.org/10.1016/j.ygyno.2024.01.007)<br><sub>Gynecologic oncology</sub> | meta_analysis | unrelated | the use of metformin was associated with a significantly higher incidence of EC (HR = 1.17, 95% CI 1.09-1.26, P < 0.0001). |
| 2021 | [The effect of metformin on esophageal cancer risk in patients with type 2 diabetes mellitus: a systematic review and met](https://doi.org/10.1007/s12094-020-02415-6)<br><sub>Clinical & translational oncology : official publication of the Federation of Spanish Oncology Societies and of the National Cancer Institute of Mexico</sub> | meta_analysis | unrelated | metformin could not reduce esophageal cancer risk in type 2 diabetes mellitus patients (HR 0.88, 95% CI 0.60-1.28, P > 0.05). |
| 2019 | [Metformin use and prostate cancer risk: A meta-analysis of cohort studies.](https://doi.org/10.1097/MD.0000000000014955)<br><sub>Medicine</sub> | meta_analysis | unrelated | metformin use was not significantly associated with the risk of prostate cancer (RR 0.97, 95% CI 0.80-1.16, P = .711). |
| 2015 | [Metformin Use Is Associated With Better Survival of Breast Cancer Patients With Diabetes: A Meta-Analysis](https://doi.org/10.1634/theoncologist.2015-0096)<br><sub>The Oncologist</sub> | meta_analysis | unrelated | Metformin was associated with better overall survival times and cancer‑specific survival times. |

![Study designs](../img/metformin-cancer-risk-tiers.svg)

### What disagrees

Prism's counter-evidence pass found no source that directly contradicts the claim among those it read (tally {"supports": 3, "contradicts": 0, "qualifies": 0, "unrelated": 5, "unread": 0}).

> The documents read support the claim; this selected sample does not establish scientific consensus.

### Numbers you can quote

| Figure | Measures | Population | Source |
| --- | --- | --- | --- |
| **0.90 (95% confidence interval, 0.73-1.10)** | hazard ratio for cancer incidence | participants in Diabetes Prevention Program | [Randomized Study of Metformin and Intensive Lifestyle Intervention on Cancer Incidence over 21 Years of Follow-up in the](https://doi.org/10.1158/1940-6207.CAPR-23-0461) 2025 |
| **approximately 10% to 40%** | decrease in overall cancer incidence | individuals with diabetes | [Randomized Study of Metformin and Intensive Lifestyle Intervention on Cancer Incidence over 21 Years of Follow-up in the](https://doi.org/10.1158/1940-6207.CAPR-23-0461) 2025 |
| **RR = 0.55, 95% confidence interval [CI] = 0.30 to 0.80** | relative risk for overall cancer | case-control studies | [Association of metformin use and cancer incidence: a systematic review and meta-analysis](https://doi.org/10.1093/jnci/djae021) 2024 |
| **RR = 0.65, 95% CI = 0.37 to 0.93** | relative risk for overall cancer | prospective cohort studies | [Association of metformin use and cancer incidence: a systematic review and meta-analysis](https://doi.org/10.1093/jnci/djae021) 2024 |
| **RR = 0.79, 95% CI = 0.73 to 0.85** | relative risk for gastrointestinal cancer | metformin use studies | [Association of metformin use and cancer incidence: a systematic review and meta-analysis](https://doi.org/10.1093/jnci/djae021) 2024 |
| **RR = 0.88, 95% CI = 0.78 to 0.99** | relative risk for urologic cancer | metformin use studies | [Association of metformin use and cancer incidence: a systematic review and meta-analysis](https://doi.org/10.1093/jnci/djae021) 2024 |

![Research output per year](../img/metformin-cancer-risk-research-series.svg)

**Extracted disease-factor claims** (4 claims; extracted claims, not papers — one paper can produce several, and the same finding restated in ten papers counts ten times): association/na (clinical) ×2, protective/decreases (unspecified) ×1, protective/decreases (review_meta) ×1

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/metformin-cancer-risk-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 3.5 | 3.5 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.0 | 2.0 | 1.0 |
| Visualisation from counted data | 3.5 | 3.5 | 1.0 | 0.5 |
| Exploration and drill-down | 2.5 | 2.5 | 1.5 | 0.5 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 1.0 |
| Reproducibility | 4.0 | 4.0 | 1.0 | 1.0 |
| Traceable references | 4.0 | 4.0 | 1.0 | 1.0 |
| Accuracy against the corpus | 3.5 | 4.0 | 3.5 | 2.5 |
| Calibration and limits | 3.5 | 4.0 | 3.5 | 3.0 |
| Decision-grade verdict | 3.5 | 4.0 | 4.0 | 3.5 |
| Facet coverage | 4.0 | 3.5 | 1.0 | 1.0 |
| **Score /100** | 71.8 | **73.7** | 39.3 | 29.1 |

**Claude Opus judge:** B and C both separated the observational tier (RR about 0.55–0.67) from the randomized DPP null (HR 0.90, 0.73–1.10) with traced numbers and resolving DOIs. B went further: it surfaced the site-level contradictions (breast, endometrial, esophageal, prostate) and noted that the tool's tally hides them as 'unrelated'. A and D gave expert-sounding memory answers. D also carried an unresolvable DOI and a pseudo-numeric chart.

**GPT judge:** B best separates the observational association from the weaker randomized evidence, flags the DPP population mismatch, and gives a usable decision with traceable estimates. D is broader and supplies more site-specific counterexamples, but its claim that no established-T2D randomized trial was found exceeds what the record establishes, and its censoring account is inconsistent.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/metformin-cancer-risk/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/metformin-cancer-risk.pdf)

## Live MCP session

Here each model was given only the question and a live connection to the Prism MCP server, and chose its own calls.

**Claude** (claude-sonnet, 511.8 s) called 2 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `find_evidence` | `{"claim": "Metformin reduces cancer risk in people with type 2 diabetes", "limit": 12}` | ok · 23,053 chars |
| 2 | `find_counter_evidence` | `{"claim": "Metformin reduces cancer risk in people with type 2 diabetes"}` | ok · 5,000 chars |

<details><summary>Claude's answer</summary>

**Direct answer:** Probably a modest reduction in some cancers, but the evidence is observational and mixed by cancer site. It doesn't establish that metformin causes the reduction. The evidence I retrieved does not include trials of cancer prevention in diabetics.

**What the data shows** (Prism, typed corpus 2017–2025, 338 papers on this exact claim)
- Framing is mostly favourable. By orientation label, 99 papers are promising and 66 cautionary. By side, 106 support, 84 qualify and 21 contradict (31.1% contested). These labels describe how papers frame their findings. They are not verdicts.
- The strongest supporting source is a 2024 JNCI meta-analysis (O'Connor et al.). It found a lower overall cancer risk in case-control studies (RR 0.55, 95% CI 0.30–0.80) and in prospective cohorts (RR 0.65, 0.37–0.93). Those intervals are wide.
- Lung cancer meta-analyses are consistently protective:
  - Zhang 2014: RR 0.71 (0.55–0.95)
  - Yao 2019: RR 0.89 (0.83–0.96)
  - Xiao 2020: HR 0.78 (0.70–0.86)
  
  I did not read these abstracts myself. The tool's quote check failed on them, so treat the figures as the tool's extraction.

**What disagrees** (site-specific meta-analyses)
- Prostate: OR 0.94 (0.79–1.11), 2025; RR 0.97 (0.80–1.16), 2019. Neither is significant.
- Breast: no significant reduction (2023).
- Esophageal, in type 2 diabetes: HR 0.88 (0.60–1.28), 2021. Not significant.
- Endometrial: OR 1.05 (0.82–1.35), 2018, and HR 1.17 (1.09–1.26), 2024. The 2024 result points toward higher incidence.
- A 22-trial meta-analysis of people who already had cancer (2022) found no effect on cancer mortality. That is a different question from prevention.

**Interpretation (mine)**
- The pooled "overall cancer" benefit is likely inflated by the usual biases in observational drug studies, such as immortal-time bias and comparison with non-users who are sicker. The pattern of lung benefit but null or adverse results elsewhere fits that. I haven't tested this here.
- The tool's tally was thin: only 1 of 16 documents was read as directly supporting, and 8 were judged unrelated to the claim as worded. Treat the evidence as moderate at best.
- The wording I'd defend is "associated with lower risk of some cancers, notably lung, in observational data, with no proven causal effect."

</details>

**ChatGPT** (gpt-6-luna, 536.7 s) called 3 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `find_evidence` | `{"claim": "Metformin reduces cancer incidence or cancer mortality in people with type 2 diabetes compared with other glucose-lowering therapies or no metformin"` | ok · 52,869 chars |
| 2 | `research_plan` | `{"question": "Does metformin reduce cancer risk in people with type 2 diabetes? Need evidence strength and disagreement.", "subject_phrases": ["metformin", "typ` | ok · 3,453 chars |
| 3 | `research_packet` | `{"claim": "Does metformin reduce cancer risk in people with type 2 diabetes?", "subject_phrases": ["metformin", "type 2 diabetes"], "outcome_phrases": ["cancer ` | ok · 21,340 chars |

<details><summary>ChatGPT's answer</summary>

**Probably not established.** Metformin is associated with lower cancer incidence in some studies of people with type 2 diabetes, but the evidence does not show reliably that the drug itself prevents cancer.

**What the data shows:** A 2023 systematic-review/meta-analysis abstract reported **31% lower overall cancer incidence** among metformin users (summary RR 0.69; 95% CI 0.52–0.90). Prism’s 2020–2025 paper sample also included contrary findings: a study found **no association** between metformin use and lung cancer risk, while a small Algerian study reported higher risk among users (OR 4.61; 95% CI 1.48–14.37). These studies differ in cancer type and design; the pooled estimate does not specify a common follow-up window. [2023 meta-analysis abstract](https://doi.org/10.1158/1940-6207.c.6544806) · [lung cancer study](https://doi.org/10.1158/1940-6207.c.6544617) · [Algerian study](https://doi.org/10.32113/wcrj_20229_2394)

**My interpretation:** The apparent benefit is suggestive, but not strong causal evidence. Much of this literature is observational, so differences in health, diabetes severity, treatment choice and time exposed to medication can distort comparisons. The contrary studies reinforce that findings vary by cancer and population. I would not treat metformin as a proven cancer-prevention drug; the strongest conclusion is that a preventive effect remains uncertain.

</details>

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Does metformin reduce cancer risk in people with type 2 diabetes? How strong is the evidence and what disagrees?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.evidence" \
  -H 'content-type: application/json' \
  -d '{"claim": "Metformin reduces cancer risk in diabetic patients", "limit": 10}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['find_evidence']["fn"](**{'claim': 'Metformin reduces cancer risk in diabetic patients', 'limit': 10})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `find_evidence` (69.4 s) → `find_counter_evidence` (8.6 s) → `find_statistics` (8.2 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
