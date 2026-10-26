# Does glyphosate cause cancer?

[Agriculture & food security](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Both sides of a litigated scientific question.  
> **Why it is hard.** IARC classification vs regulators: the literature is polarised.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [glyphosate-cancer.json](../../examples/glyphosate-cancer.json).

**The question:**

> Does glyphosate exposure cause cancer? What does the evidence say and what disagrees?

## What Prism returned

### How much evidence exists

| Corpus | Records on both sides of the claim | Window |
| --- | ---: | --- |
| Typed research papers | 27,109 | 2017-2025 |
| Papers with abstracts | 366 | 1990-2025 |
| the health literature index records | 3,886 | 1990-2025 |
| News articles | 158 | 2019-01-01..2026-06-01 |
| Patents | 23 | 2005-2024 |
| arXiv preprints | 1 | 2005-2025 |

![Evidence volume by corpus](../img/glyphosate-cancer-volumes.svg)

![Framing of the literature](../img/glyphosate-cancer-sides.svg)

*orientation is a label on the paper's own framing, not a verdict on the claim; this corpus starts in 2017* Contested share: **23%**.

### The strongest evidence, read

> few titles carry both sides of this claim, so the documents read were chosen by the subject in the title and the outcome in the abstract.

Prism read 1 sources: **0 support, 1 contradict, 0 qualify** (tier-weighted {"supports": 0, "contradicts": 6, "qualifies": 0}). Each quote is copied from the abstract and verified against it; 0 candidate quotes failed that check and were dropped.

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2016 | [Systematic review and meta-analysis of glyphosate exposure and risk of lymphohematopoietic cancers](https://doi.org/10.1080/03601234.2016.1142748)<br><sub>Journal of Environmental Science and Health Part B</sub> | meta_analysis | contradicts | Thus, a causal relationship has not been established between glyphosate exposure and risk of any type of LHC. |
| 2024 | [Overview of human health effects related to glyphosate exposure](https://doi.org/10.3389/ftox.2024.1474792)<br><sub>Frontiers in Toxicology</sub> | review | unrelated | In 2015, the IARC (International Agency for Research on Cancer) classified glyphosate and its derivatives in Group 2A, as probable human carcinogens. |
| 2021 | [Pleiotropic Outcomes of Glyphosate Exposure: From Organ Damage to Effects on Inflammation, Cancer, Reproduction and Deve](https://doi.org/10.3390/ijms222212606)<br><sub>International Journal of Molecular Sciences</sub> | review | unrelated | has been found to induce the generation of reactive oxygen species (ROS) and several cytotoxic and genotoxic effects in vitro and in animal models |
| 2025 | [[Research progress on population load and hepatotoxicity of glyphosate].](https://doi.org/10.3760/cma.j.cn121094-20240422-00174)<br><sub>Zhonghua lao dong wei sheng zhi ye bing za zhi = Zhonghua laodong weisheng zhiyebing zazhi = Chinese journal of industrial hygiene and occupational diseases</sub> | review | unrelated | is associated with the occurrence and development of different types of cancer |
| 2025 | [Re-Evaluating the Use of Glyphosate-based Herbicides: Implications on Fertility.](https://doi.org/10.1007/s43032-025-01834-6)<br><sub>Reproductive sciences (Thousand Oaks, Calif.)</sub> | review | unrelated | recent studies on exposure have suggested association with cancer, metabolic disorders, endocrine disruption and infertility |
| 2022 | [Effects of glyphosate on zebrafish: a systematic review and meta-analysis.](https://doi.org/10.1007/s10646-022-02581-z)<br><sub>Ecotoxicology (London, England)</sub> | meta_analysis | unrelated | We concluded that glyphosate causes damage in the embryonic, larval and adult stages of this species. |
| 2021 | [Is glyphosate toxic to bees? A meta-analytical review.](https://doi.org/10.1016/j.scitotenv.2021.145397)<br><sub>The Science of the total environment</sub> | meta_analysis | unrelated | Therefore, GLY can be considered toxic to bees. |
| 2005 | [Comparison of broiler performance when fed diets containing corn grain with insect-protected (corn rootworm and European](https://doi.org/10.1093/ps/84.12.1893)<br><sub>Poultry science</sub> | trial | unrelated | No differences among diets were observed (P > 0.05) in performance (final live weights, feed intake, feed conversion, and adjusted feed conversion), carcass yield... |

![Study designs](../img/glyphosate-cancer-tiers.svg)

### What disagrees

Prism's counter-evidence pass found no source that directly contradicts the claim among those it read (tally {"supports": 0, "contradicts": 0, "qualifies": 0, "unrelated": 8, "unread": 0}).

> No verified document verdict supports a wording recommendation for this claim.

### Numbers you can quote

| Figure | Measures | Population | Source |
| --- | --- | --- | --- |
| **meta-RR = 1.3, 95% confidence interval (CI) = 1.0-1.6** | association between any versus no use of glyphosate and risk of NHL | based on six studies | [Systematic review and meta-analysis of glyphosate exposure and risk of lymphohematopoietic cancers](https://doi.org/10.1080/03601234.2016.1142748) 2016 |
| **meta-RR = 1.1, 95% CI = 0.7-1.6** | association between any versus no use of glyphosate and risk of HL | two studies | [Systematic review and meta-analysis of glyphosate exposure and risk of lymphohematopoietic cancers](https://doi.org/10.1080/03601234.2016.1142748) 2016 |

![Research output per year](../img/glyphosate-cancer-research-series.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/glyphosate-cancer-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 3.0 | 0.5 | 0.5 |
| Measured comparison | 4.5 | 4.0 | 2.0 | 2.0 |
| Visualisation from counted data | 4.0 | 3.0 | 1.0 | 1.0 |
| Exploration and drill-down | 3.0 | 1.0 | 1.0 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 1.0 |
| Reproducibility | 4.5 | 4.5 | 0.0 | 1.0 |
| Traceable references | 1.0 | 4.0 | 2.5 | 1.0 |
| Accuracy against the corpus | 3.0 | 3.0 | 2.0 | 2.5 |
| Calibration and limits | 4.0 | 3.5 | 3.0 | 3.0 |
| Decision-grade verdict | 4.0 | 4.0 | 3.5 | 3.5 |
| Facet coverage | 4.5 | 3.5 | 1.5 | 2.0 |
| **Score /100** | **72.3** | 67.6 | 32.6 | 34.4 |

**Claude Opus judge:** B and C both grounded their numbers in the recorded calls. B read the research series correctly as flat, added the news trend and all four cancer-specific RRs, and gave a confidence level justified by the 6-paper intersection; C misread the series direction and dropped news. The memory-only deliverables A and D gave reasonable narrative answers but carried unverifiable or wrong specifics, and A had a fabricated IARC DOI.

**GPT judge:** A is strongest for a decision-maker because it combines the most complete traced evidence, quantified comparisons, and explicit limits, while directly answering the causation question. Its unsupported export window, censored endpoint handling, and one unresolvable DOI keep the deliverable short of fully reliable.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/glyphosate-cancer/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/glyphosate-cancer.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Does glyphosate exposure cause cancer? What does the evidence say and what disagrees?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.evidence" \
  -H 'content-type: application/json' \
  -d '{"claim": "Glyphosate exposure causes cancer", "limit": 10}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['find_evidence']["fn"](**{'claim': 'Glyphosate exposure causes cancer', 'limit': 10})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `find_evidence` (166.8 s) → `find_counter_evidence` (23.4 s) → `find_statistics` (17.6 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
