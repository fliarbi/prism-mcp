# Ultra-processed food and health

[Consumer, brands & media](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Effect sizes for a food-policy brief.  
> **Why it is hard.** A large 2019+ cohort literature with umbrella reviews in 2024.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [ultra-processed-food.json](../../examples/ultra-processed-food.json).

**The question:**

> How strong is the evidence that ultra-processed food increases mortality?

## What Prism returned

### How much evidence exists

| Corpus | Records on both sides of the claim | Window |
| --- | ---: | --- |
| Typed research papers | 587 | 2017-2025 |
| Papers with abstracts | 1 | 1990-2025 |
| the health literature index records | 20 | 1990-2025 |
| News articles | 1 | 2019-01-01..2026-06-01 |
| Patents | 0 | 2005-2024 |
| arXiv preprints | 0 | 2005-2025 |

![Evidence volume by corpus](../img/ultra-processed-food-volumes.svg)

![Framing of the literature](../img/ultra-processed-food-sides.svg)

*orientation is a label on the paper's own framing, not a verdict on the claim; this corpus starts in 2017* Contested share: **18.9%**.

### The strongest evidence, read

Prism read 1 sources: **1 support, 0 contradict, 0 qualify** (tier-weighted {"supports": 6, "contradicts": 0, "qualifies": 0}). Each quote is copied from the abstract and verified against it; 3 candidate quotes failed that check and were dropped.

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2023 | [Dose-response meta-analysis of ultra-processed food with the risk of cardiovascular events and all-cause mortality: evid](https://doi.org/10.1039/d2fo02628g)<br><sub>Food & function</sub> | meta_analysis | supports | the pooled effect size for the highest versus lowest category of UPF consumption showed ... all-cause mortality (RR = 1.21, 95% CI, 1.15-1.27) |
| 2023 | [[Changes in the microbiota due to ultra-processed foods: obesity, cancer and premature death].](https://pubmed.ncbi.nlm.nih.gov/37094197/)<br><sub>Medicina</sub> | review | unrelated | Multiple long cohort studies have shown a relationship between their consumption and ... all-cause mortality. |
| 2025 | [Ultra-processed foods and risk of all-cause mortality: an updated systematic review and dose-response meta-analysis of p](https://doi.org/10.1186/s13643-025-02800-8)<br><sub>Systematic reviews</sub> | meta_analysis | unread | – |
| 2021 | [Ultra-Processed Food Consumption and Adult Mortality Risk: A Systematic Review and Dose-Response Meta-Analysis of 207,29](https://doi.org/10.3390/nu14010174)<br><sub>Nutrients</sub> | meta_analysis | unread | – |
| 2021 | [Ultra-processed food consumption modifies the association of Nutri-Score with all-cause mortality](https://doi.org/10.1093/eurpub/ckab164.448)<br><sub>European Journal of Public Health</sub> | article | unread | – |

![Study designs](../img/ultra-processed-food-tiers.svg)

### What disagrees

Prism's counter-evidence pass found no source that directly contradicts the claim among those it read (tally {"supports": 2, "contradicts": 0, "qualifies": 0, "unrelated": 2, "unread": 1}).

> The documents read support the claim; this selected sample does not establish scientific consensus.

### Numbers you can quote

| Figure | Measures | Population | Source |
| --- | --- | --- | --- |
| **HR = 1.15, 95% CI 1.09-1.22** | hazard ratio for all-cause mortality |  | [Ultra-processed foods and risk of all-cause mortality: an updated systematic review and dose-response meta-analysis of p](https://doi.org/10.1186/s13643-025-02800-8) 2025 |
| **HR = 1.10, 95% CI 1.04-1.16** | hazard ratio per 10% increment in UPF consumption |  | [Ultra-processed foods and risk of all-cause mortality: an updated systematic review and dose-response meta-analysis of p](https://doi.org/10.1186/s13643-025-02800-8) 2025 |
| **1,148,387 participants (173,107 deaths)** | total participants and deaths | participants | [Ultra-processed foods and risk of all-cause mortality: an updated systematic review and dose-response meta-analysis of p](https://doi.org/10.1186/s13643-025-02800-8) 2025 |
| **RR = 1.21, 95% CI, 1.15-1.27** | risk ratio for all-cause mortality |  | [Dose-response meta-analysis of ultra-processed food with the risk of cardiovascular events and all-cause mortality: evid](https://doi.org/10.1039/d2fo02628g) 2023 |
| **RR = 1.02, 95% CI, 1.01-1.03** | risk ratio per additional daily serving for all-cause mortality |  | [Dose-response meta-analysis of ultra-processed food with the risk of cardiovascular events and all-cause mortality: evid](https://doi.org/10.1039/d2fo02628g) 2023 |
| **HR = 1.21; 95% CI: 1.13, 1.30** | hazard ratio for all-cause mortality |  | [Ultra-Processed Food Consumption and Adult Mortality Risk: A Systematic Review and Dose-Response Meta-Analysis of 207,29](https://doi.org/10.3390/nu14010174) 2021 |

![Research output per year](../img/ultra-processed-food-research-series.svg)

**Extracted disease-factor claims** (9 claims; extracted claims, not papers — one paper can produce several, and the same finding restated in ten papers counts ten times): risk_factor/increases (observational) ×3, risk_factor/increases (unspecified) ×2, risk_factor/increases (review_meta) ×2, association/increases (observational) ×1, association/na (review_meta) ×1

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/ultra-processed-food-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.5 | 1.0 | 0.0 |
| Measured comparison | 4.0 | 3.5 | 2.0 | 1.5 |
| Visualisation from counted data | 4.5 | 3.5 | 1.0 | 1.0 |
| Exploration and drill-down | 1.0 | 1.0 | 1.0 | 1.0 |
| Data export with provenance | 4.5 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 4.5 | 4.5 | 0.0 | 1.0 |
| Traceable references | 3.5 | 4.0 | 1.0 | 1.0 |
| Accuracy against the corpus | 3.0 | 4.0 | 3.5 | 2.0 |
| Calibration and limits | 4.0 | 4.0 | 4.0 | 2.5 |
| Decision-grade verdict | 4.0 | 4.0 | 3.0 | 3.0 |
| Facet coverage | 4.5 | 4.5 | 1.5 | 1.5 |
| **Score /100** | **77.2** | 76.9 | 35.2 | 27.3 |

**Claude Opus judge:** C and D both ground the answer in the three recorded meta-analyses (HR/RR 1.15–1.21, with I² 83% in the newest) and reach the same calibrated answer: a consistent association that is not proven causal. C goes further, with two charts, two exports and a fuller tally and limits picture, but it slips in untraced Bonaccio subgroup figures; D is narrower but cleaner. A and B rely on memory: B is honestly labelled and largely correct, while A contains garbled and misattributed figures.

**GPT judge:** B gives the clearest decision-grade account: it grounds the pooled mortality estimates, distinguishes association from causation, and supplies a reproducible trend and useful export. D is more complete on charts and facets, but its unverified quote and unsupported Bonaccio estimate weaken its factual reliability.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/ultra-processed-food/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/ultra-processed-food.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How strong is the evidence that ultra-processed food increases mortality?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.evidence" \
  -H 'content-type: application/json' \
  -d '{"claim": "Ultra-processed food consumption increases mortality", "limit": 10}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['find_evidence']["fn"](**{'claim': 'Ultra-processed food consumption increases mortality', 'limit': 10})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `find_evidence` (185.4 s) → `find_counter_evidence` (20.1 s) → `find_statistics` (3.2 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
