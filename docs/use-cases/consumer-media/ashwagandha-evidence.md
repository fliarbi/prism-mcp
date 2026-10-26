# Does ashwagandha reduce stress?

[Consumer, brands & media](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Supplement-claim checking for a consumer-health brand.  
> **Why it is hard.** Small, industry-funded trials; tiering exposes it.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [ashwagandha-evidence.json](../../examples/ashwagandha-evidence.json).

**The question:**

> Does ashwagandha reduce stress and anxiety? What is the quality of evidence?

## What Prism returned

### How much evidence exists

| Corpus | Records on both sides of the claim | Window |
| --- | ---: | --- |
| Typed research papers | 11,603 | 2017-2025 |
| Papers with abstracts | 64 | 1990-2025 |
| the health literature index records | 147,894 | 1990-2025 |
| News articles | 25 | 2019-01-01..2026-06-01 |
| Patents | 15 | 2005-2024 |
| arXiv preprints | 0 | 2005-2025 |

![Evidence volume by corpus](../img/ashwagandha-evidence-volumes.svg)

![Framing of the literature](../img/ashwagandha-evidence-sides.svg)

*orientation is a label on the paper's own framing, not a verdict on the claim; this corpus starts in 2017* Contested share: **7.3%**.

### The strongest evidence, read

> few titles carry both sides of this claim, so the documents read were chosen by the subject in the title and the outcome in the abstract.

Prism read 3 sources: **3 support, 0 contradict, 0 qualify** (tier-weighted {"supports": 12, "contradicts": 0, "qualifies": 0}). Each quote is copied from the abstract and verified against it; 1 candidate quotes failed that check and were dropped.

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2025 | [Efficacy and safety of Ashwagandha (Withania somnifera) root extract on stress and weight management in adults: a prospe](https://doi.org/10.25122/jml-2025-0147)<br><sub>Journal of medicine and life</sub> | trial | supports | Compared with PL, ARE showed significant improvements (P < 0.05) in PSS, SF-12, SSS, and FCQ-T scores. |
| 2022 | [Does Ashwagandha supplementation have a beneficial effect on the management of anxiety and stress? A systematic review a](https://doi.org/10.1002/ptr.7598)<br><sub>Phytotherapy Research</sub> | review | supports | We found that Ashwagandha supplementation significantly reduced ... stress level (SMD: −1.75; 95% CI: −2.29, −1.22; p = .005; I 2 = 83.1%) compared to the placebo. |
| 2008 | A Standardized Withania Somnifera Extract Significantly Reduces Stress-Related Parameters in Chronically Stressed Humans<br><sub></sub> | article | supports | Between Days 0 and 60, the WSE 125 mg QD group decreased significantly more than placebo for mean mHAM‑A score, serum cortisol, serum C‑reactive protein, pulse rate and blood pressure, and increased significantly for mean serum DHEAS and hemoglobin. |
| 2024 | [Effects of Withania somnifera Extract in Chronically Stressed Adults: A Randomized Controlled Trial](https://doi.org/10.3390/nu16091293)<br><sub>Nutrients</sub> | article | unread | We have shown that aqueous WS extract (roots and leaves) safely reduces mild to moderate chronic stress at doses of 125 mg, 250 mg, and 500 mg/day for 8 weeks. |
| 2022 | [Withania somnifera Extracts Promote Resilience against Age-Related and Stress-Induced Behavioral Phenotypes in Drosophil](https://doi.org/10.3390/nu14193923)<br><sub>Nutrients</sub> | article | unrelated | Both extracts provided resilience against stress-induced behavioral changes. |
| 2025 | [Behavioral and biochemical observations on the neuroprotective impact of Withania somnifera extract in a rat model of Pa](https://doi.org/10.51470/jez.2026.29.1.771)<br><sub>JOURNAL OF EXPERIMENTAL ZOOLOGY INDIA</sub> | article | unrelated | The current study’s findings indicate that withania somnifera extract markedly safeguards neurons in a Parkinson’s disease rat model, mostly through the attenuation of inflammation and free radicals. |
| 2025 | [Polyphenol-Rich Sorghum Bicolor Extract Enhances Strength Recovery After Eccentric Exercise.](https://doi.org/10.1519/JSC.0000000000005144)<br><sub>Journal of strength and conditioning research</sub> | trial | unread | – |
| 2025 | [Scalp condition improvement with botanical extracts possessing chemical and physical antioxidant activity.](https://doi.org/10.1111/ics.13031)<br><sub>International journal of cosmetic science</sub> | trial | unread | – |

![Study designs](../img/ashwagandha-evidence-tiers.svg)

### What disagrees

Prism's counter-evidence pass found no source that directly contradicts the claim among those it read (tally {"supports": 1, "contradicts": 0, "qualifies": 0, "unrelated": 7, "unread": 0}).

> The documents read support the claim; this selected sample does not establish scientific consensus.

### Numbers you can quote

| Figure | Measures | Population | Source |
| --- | --- | --- | --- |
| **27–30%** | cortisol reduction |  | [Effects of Ashwagandha Supplementation on Strength, Endurance, and Post-Exercise Recovery: A Review](https://doi.org/10.12775/qs.2025.48.66886) 2025 |

![Research output per year](../img/ashwagandha-evidence-research-series.svg)

**Extracted disease-factor claims** (1 claims; extracted claims, not papers — one paper can produce several, and the same finding restated in ten papers counts ten times): treatment/decreases (unspecified) ×1

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/ashwagandha-evidence-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 3.5 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 3.5 | 1.5 | 1.0 |
| Visualisation from counted data | 4.0 | 4.0 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 2.5 | 1.5 | 1.0 |
| Data export with provenance | 2.5 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 3.0 | 1.0 | 1.0 |
| Traceable references | 1.0 | 4.0 | 1.0 | 0.0 |
| Accuracy against the corpus | 4.0 | 4.0 | 2.5 | 3.0 |
| Calibration and limits | 4.0 | 4.0 | 3.0 | 2.5 |
| Decision-grade verdict | 4.0 | 4.0 | 0.0 | 3.5 |
| Facet coverage | 4.5 | 4.5 | 1.0 | 2.0 |
| **Score /100** | **75.1** | 74.4 | 25.8 | 27.2 |

**Claude Opus judge:** B and D both grounded the answer in the recorded evidence: the meta-analysis SMD −1.75 with I² 83.1%, an RCT and a zero-contradiction tally. Both stated that the corpus intersection is empty. B went further by catching the off-topic Morinda cluster and quantifying the trends and contrasts, while D had cleaner references and exports. A was honest memory with no measurement, and C was undermined by a fabricated DOI and by presenting calls as run when none were.

**GPT judge:** B is the strongest decision deliverable: it combines reproducible research and news trends, quantified contrasts, and a direct conclusion bounded by the empty claim-intersection lane and a selected read sample. C is close and has cleaner paper citations and exports, but its incomplete regenerate calls and omitted trend decomposition weaken auditability; both leave the funding and bias question unresolved in the supplied evidence.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/ashwagandha-evidence/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/ashwagandha-evidence.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Does ashwagandha reduce stress and anxiety? What is the quality of evidence?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.evidence" \
  -H 'content-type: application/json' \
  -d '{"claim": "Ashwagandha reduces stress", "limit": 10}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['find_evidence']["fn"](**{'claim': 'Ashwagandha reduces stress', 'limit': 10})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `find_evidence` (311.9 s) → `find_counter_evidence` (27.3 s) → `find_statistics` (27.7 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
