# GLP-1 drugs and muscle loss

[Medical & clinical evidence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Quantified evidence on lean-mass loss, with study design and population for each figure.  
> **Why it is hard.** A fast-moving 2023-2026 literature; model training data ends before most of it.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [glp1-weight-loss-muscle.json](../../examples/glp1-weight-loss-muscle.json).

**The question:**

> Do GLP-1 weight-loss drugs like semaglutide cause significant lean muscle loss?

## What Prism returned

### How much evidence exists

| Corpus | Records on both sides of the claim | Window |
| --- | ---: | --- |
| Typed research papers | 30 | 2017-2025 |
| Papers with abstracts | 0 | 1990-2025 |
| the health literature index records | 0 | 1990-2025 |
| News articles | 0 | 2019-01-01..2026-06-01 |
| Patents | 0 | 2005-2024 |
| arXiv preprints | 0 | 2005-2025 |

![Evidence volume by corpus](../img/glp1-weight-loss-muscle-volumes.svg)

![Framing of the literature](../img/glp1-weight-loss-muscle-sides.svg)

*orientation is a label on the paper's own framing, not a verdict on the claim; this corpus starts in 2017* Contested share: **36.7%**.

### The strongest evidence, read

Prism read 0 sources: **0 support, 0 contradict, 0 qualify** (tier-weighted {"supports": 0, "contradicts": 0, "qualifies": 0}). Each quote is copied from the abstract and verified against it; 1 candidate quotes failed that check and were dropped.

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2025 | [Nutrition support whilst on glucagon-like peptide-1 based therapy. Is it necessary?](https://doi.org/10.1097/mco.0000000000001130)<br><sub>Current Opinion in Clinical Nutrition & Metabolic Care</sub> | review | unrelated | Studies have shown that while GLP-1 RA are effective in reducing fat mass, up to 40% of the total weight loss can come from FFM. |
| 2025 | [Glucagon Like Peptide-1 Receptor Agonists for Sarcopenia and Muscle Wasting Disorders: A Systematic Review of Efficacy a](https://doi.org/10.14336/ad.2025.1165)<br><sub>Aging and Disease</sub> | review | unrelated | limited clinical studies showed body weight reduction accompanied by a decline in lean mass following GLP-1RA treatment. |
| 2024 | [Antibody blockade of activin type II receptors preserves skeletal muscle mass and enhances fat loss during GLP-1 recepto](https://doi.org/10.1016/j.molmet.2024.101880)<br><sub>Molecular Metabolism</sub> | article | unrelated | Daily treatment of obese mice with semaglutide potently decreased body weight; this included a significant decrease in both muscle and fat mass. |
| 2003 | [Long-term pharmacotherapy for obesity and overweight](https://doi.org/10.1002/14651858.cd004094.pub2)<br><sub>Cochrane Database of Systematic Reviews</sub> | review | unrelated | Studies evaluating the long-term efficacy of anti-obesity agents are limited to orlistat and sibutramine. |
| 2012 | [A systematic review and mixed treatment comparison of pharmacological interventions for the treatment of obesity](https://doi.org/10.1111/j.1467-789x.2011.00981.x)<br><sub>Obesity Reviews</sub> | review | unrelated | The active drugs were all effective at reducing weight and BMI. |
| 2014 | [Incretin Effect After Oral Amino Acid Ingestion in Humans](https://doi.org/10.1210/jc.2014-3865)<br><sub>The Journal of Clinical Endocrinology & Metabolism</sub> | article | unrelated | The objective of the study was to explore insulin secretion and incretin hormones after oral and iv amino acid administration at matched total amino acid concentrations in healthy subjects. |
| 2022 | [Effects of GLP-1 Infusion Upon Whole-body Glucose Uptake and Skeletal Muscle Perfusion During Fed-state in Older Men](https://doi.org/10.1210/clinem/dgac613)<br><sub>The Journal of Clinical Endocrinology & Metabolism</sub> | article | unrelated | We thus hypothesized exogenous GLP-1 infusions would enhance muscle perfusion and positively affect glucose metabolism during fed-state clamps in older people. |
| 2023 | [Dulaglutide Protects Mice against Diabetic Sarcopenia-Mediated Muscle Injury by Inhibiting Inflammation and Regulating t](https://doi.org/10.1155/2023/9926462)<br><sub>International Journal of Endocrinology</sub> | article | unrelated | Here, we aimed to determine whether the GLP-1 receptor agonist (GLP-1RA) dulaglutide (Dul) affects the progression of diabetic sarcopenia. |

![Study designs](../img/glp1-weight-loss-muscle-tiers.svg)

### What disagrees

Prism's counter-evidence pass found no source that directly contradicts the claim among those it read (tally {"supports": 0, "contradicts": 0, "qualifies": 0, "unrelated": 5, "unread": 1}).

> No verified document verdict supports a wording recommendation for this claim.

### Numbers you can quote

| Figure | Measures | Population | Source |
| --- | --- | --- | --- |
| **40%** | proportion of total weight loss from fat free mass |  | [Nutrition support whilst on glucagon-like peptide-1 based therapy. Is it necessary?](https://doi.org/10.1097/mco.0000000000001130) 2025 |
| **∼10 %** | increase in lean mass | obese mice | [Antibody blockade of activin type II receptors preserves skeletal muscle mass and enhances fat loss during GLP-1 recepto](https://doi.org/10.1016/j.molmet.2024.101880) 2024 |

![Research output per year](../img/glp1-weight-loss-muscle-research-series.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/glp1-weight-loss-muscle-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 3.5 | 3.5 | 1.0 | 0.0 |
| Measured comparison | 1.5 | 2.5 | 2.0 | 2.0 |
| Visualisation from counted data | 3.5 | 3.5 | 1.0 | 1.0 |
| Exploration and drill-down | 2.0 | 1.0 | 1.0 | 1.0 |
| Data export with provenance | 2.5 | 2.5 | 1.0 | 1.0 |
| Reproducibility | 4.0 | 4.0 | 1.0 | 0.0 |
| Traceable references | 4.0 | 4.0 | 2.5 | 1.0 |
| Accuracy against the corpus | 3.5 | 3.5 | 3.0 | 3.0 |
| Calibration and limits | 4.5 | 3.0 | 3.5 | 3.0 |
| Decision-grade verdict | 3.5 | 4.0 | 4.0 | 3.5 |
| Facet coverage | 4.0 | 3.5 | 1.5 | 1.5 |
| **Score /100** | **67.7** | 65.9 | 40.4 | 31.6 |

**Claude Opus judge:** D and B both grounded their answers in the recorded calls and reached the same calibrated conclusion: lean-mass loss is plausible at class level, but there is no human semaglutide effect size. D went further than B. It quantified the trend, exported the tally, and caught the corpus's own anomalies, including the mismatched subject headings term, the off-topic documents and the source-fit failures. A and C were honest memory syntheses; C gives the more expert-recognisable picture, but neither can be traced or reproduced.

**GPT judge:** B is the strongest decision aid: it answers directly, separates class-level human evidence from a mouse finding, and traces its annual series and citations. Its 2025 censoring treatment and incomplete exports and limits keep it short of a fully reproducible, decision-grade deliverable; C is similarly well sourced but weakens its answer with an ungrounded diet comparison.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/glp1-weight-loss-muscle/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/glp1-weight-loss-muscle.pdf)

## Live MCP session

Here each model was given only the question and a live connection to the Prism MCP server, and chose its own calls.

**Claude** (claude-sonnet, 694.7 s) called 2 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `find_evidence` | `{"claim": "GLP-1 receptor agonists like semaglutide cause significant lean muscle mass loss", "limit": 10}` | ok · 17,607 chars |
| 2 | `find_statistics` | `{"claim": "semaglutide weight loss lean mass proportion of total weight lost", "include_context": false, "include_trend": false}` | see payload · 306 chars |

<details><summary>Claude's answer</summary>

**Direct answer:** Yes, in part. GLP-1 drugs reduce lean mass in absolute terms, but whether that is "significant" or harmful is still debated. Most of the weight lost is fat.

**What the data shows** (Prism research corpus, papers from 2017–2025; 30 papers cover both GLP-1 and muscle)
- A 2025 review (Chrysavgis et al., *Int J Mol Sci*) says trials show GLP-1 therapies mainly reduce adipose tissue. They also produce absolute lean-mass reductions, "generally representing 20–30% of total weight loss."
- A 2025 meta-analysis (Anyiam et al., *Obesity Reviews*) reports a mean reduction in muscle-mass measures of −1.41 kg (95% CI −2.12 to −0.71) in people without diabetes. The Prism read suggests this was not significant in type 2 diabetes. I only have its snippet, and Prism could not verify the quote against the abstract.
- A 2025 systematic review on mitochondrial function (Old et al., *J Cachexia Sarcopenia Muscle*) states that up to 40% of weight lost may be lean mass. This is background framing, not a measured outcome.
- Scheen (2025) calls the human evidence mixed: some studies report excess loss of fat-free or skeletal muscle mass, and others argue for a protective effect.
- Across the 30 papers, 6 are labelled cautionary and 4 problem-identifying. About 37% are contested.

**Limits on the evidence**
- Prism read only 1 of the 8 top documents fully. The other quotes are ungrounded or unverified.
- The corpus gives no trial-level data for semaglutide specifically, no outcomes on strength or function, and no news coverage.
- "Lean mass" in these studies usually means DXA fat-free mass. That includes water and organ tissue, so it is not the same as muscle.

**Interpretation (mine, not Prism's)**
- A lean-mass share of 20–40% of total weight loss is similar to what diet-induced weight loss produces. So the loss looks proportional to the weight lost, not specific to the drug.
- It matters most for older adults and others at risk of sarcopenia. Whether it causes real functional decline is unproven in this evidence.
- The reasonable view is to expect some lean-mass loss, not to assume it is harmful. Protein intake and resistance training are sensible mitigations. Prism did not retrieve any evidence testing them.

</details>

**ChatGPT** (gpt-6-luna, 514.8 s) called 1 Prism tool:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `find_statistics` | `{"claim": "In adults with overweight or obesity, semaglutide causes significant loss of lean body mass or skeletal muscle during weight loss.", "include_context` | see payload · 13,689 chars |

<details><summary>ChatGPT's answer</summary>

**Yes—semaglutide can reduce lean mass during weight loss, but available data do not show that most weight lost is muscle.**

**What the data show:** In a DXA body-composition substudy of STEP 1, after **68 weeks** of semaglutide treatment, participants lost **9.7% of lean body mass** and **19.3% of fat mass** from baseline. Lean mass therefore fell, while fat mass fell more. The study was a substudy, and DXA lean mass is not a direct measure of skeletal muscle alone. [STEP 1 body-composition analysis](https://pubmed.ncbi.nlm.nih.gov/?term=Impact+of+semaglutide+on+body+composition+in+adults+with+overweight+or+obesity+in+the+STEP+1+study)

**Interpretation:** The loss is real and may matter, especially for people already at risk of low muscle or frailty. But “lean mass loss” should not be read as the same percentage of muscle lost: lean mass includes more than muscle, and the substudy does not establish how much muscle function changed. The result supports monitoring strength and nutrition during substantial weight loss; it does not by itself show that semaglutide causes clinically significant muscle impairment.

</details>

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Do GLP-1 weight-loss drugs like semaglutide cause significant lean muscle loss?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.evidence" \
  -H 'content-type: application/json' \
  -d '{"claim": "Semaglutide causes loss of lean muscle mass", "limit": 10}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['find_evidence']["fn"](**{'claim': 'Semaglutide causes loss of lean muscle mass', 'limit': 10})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `find_evidence` (90.4 s) → `find_counter_evidence` (4.0 s) → `find_statistics` (2.7 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
