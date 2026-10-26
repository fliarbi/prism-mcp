# PFAS and health

[Environment & disasters](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Effect sizes for an environmental-health regulator.  
> **Why it is hard.** Many outcomes; one mechanism per claim keeps retrieval on target.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [pfas-evidence.json](../../examples/pfas-evidence.json).

**The question:**

> Do PFAS 'forever chemicals' harm human health? Give numbers and sources.

## What Prism returned

### How much evidence exists

| Corpus | Records on both sides of the claim | Window |
| --- | ---: | --- |
| Typed research papers | 55 | 2017-2025 |
| Papers with abstracts | 4 | 1990-2025 |
| the health literature index records | 870 | 1990-2025 |
| News articles | 10 | 2019-01-01..2026-06-01 |
| Patents | 0 | 2005-2024 |
| arXiv preprints | 0 | 2005-2025 |

![Evidence volume by corpus](../img/pfas-evidence-volumes.svg)

![Framing of the literature](../img/pfas-evidence-sides.svg)

*orientation is a label on the paper's own framing, not a verdict on the claim; this corpus starts in 2017* Contested share: **23.6%**.

### The strongest evidence, read

Prism read 4 sources: **0 support, 1 contradict, 3 qualify** (tier-weighted {"supports": 0, "contradicts": 6, "qualifies": 9}). Each quote is copied from the abstract and verified against it; 0 candidate quotes failed that check and were dropped.

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2024 | [Exposure to per- and polyfluoroalkyl substances and breast cancer risk: a systematic review and meta-analysis of epidemi](https://doi.org/10.1093/aje/kwae010)<br><sub>American journal of epidemiology</sub> | meta_analysis | contradicts | the summary relative risks (RRs) estimated by random-effects meta-analyses did not support an association between PFAS and overall breast cancer risk (eg, a natural log (ln)-unit increase in serum/plasma concentrations [ng/mL] for perfluorooctanoate [PFOA] RR … |
| 2024 | [Serum metabolome associated with novel and legacy per- and polyfluoroalkyl substances exposure and thyroid cancer risk: ](https://doi.org/10.1016/j.envint.2024.109203)<br><sub>Environment International</sub> | article | qualifies | PFHxA and PFDoA exposure associated with increased TC risk, while PFHxS and PFOA associated with decreased TC risk in single compound models (all P < 0.05). |
| 2025 | [Integrating nontargeted metabolomics and machine learning to assess PFAS exposure associations with liver cancer risk](https://doi.org/10.1016/j.envint.2025.110014)<br><sub>Environment International</sub> | article | qualifies | Higher human serum levels of perfluorooctanoic acid (PFOA), perfluorononanoate, perfluorodecanoate, perfluorohexane sulfonate, perfluorooctanesulfonic acid, and 6:2 chlorinated polyfluoroether sulfonic acid were significantly correlated with the increased live… |
| 2025 | [Environmental PFAS exposure as an understudied social determinant of health for endometrial cancer disparities: A geospa](https://doi.org/10.1200/jco.2025.43.16_suppl.10564)<br><sub>Journal of Clinical Oncology</sub> | article | qualifies | Census tracts with higher proximity to PFAS show higher age-adjusted incidence and mortality odds for both Types I and II EC in NHW. |
| 2023 | [Effect of environmental exposures on cancer risk: Emerging role of non-coding RNA shuttled by extracellular vesicles.](https://doi.org/10.1016/j.envint.2023.108255)<br><sub>Environment international</sub> | review | unrelated | Environmental and lifestyle exposures have a huge impact on cancer risk; nevertheless, the biological mechanisms underlying this association remain poorly understood. |
| 2025 | [Fine particulate matter exposure and cancer risk: a systematic review and meta-analysis of prospective cohort studies.](https://doi.org/10.1515/reveh-2024-0171)<br><sub>Reviews on environmental health</sub> | meta_analysis | unread | – |
| 2025 | [The impact of cadmium exposure on breast cancer risk: Exploring dose-response relationships and mediating effects.](https://doi.org/10.1016/j.ecoenv.2025.118247)<br><sub>Ecotoxicology and environmental safety</sub> | meta_analysis | unread | – |
| 2000 | [Personal exposure to atmospheric polycyclic aromatic hydrocarbons in a general adult population and lung cancer risk ass](https://doi.org/10.1097/00043764-200002000-00004)<br><sub>Journal of occupational and environmental medicine</sub> | trial | unread | – |

![Study designs](../img/pfas-evidence-tiers.svg)

### What disagrees

Prism's counter-evidence pass found no source that directly contradicts the claim among those it read (tally {"supports": 0, "contradicts": 0, "qualifies": 0, "unrelated": 8, "unread": 0}).

> No verified document verdict supports a wording recommendation for this claim.

![Research output per year](../img/pfas-evidence-research-series.svg)

**Extracted disease-factor claims** (1 claims; extracted claims, not papers — one paper can produce several, and the same finding restated in ten papers counts ten times): association/increases (unspecified) ×1

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/pfas-evidence-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 4.5 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 2.0 | 2.0 |
| Visualisation from counted data | 3.5 | 4.0 | 1.0 | 0.0 |
| Exploration and drill-down | 4.5 | 1.0 | 1.5 | 1.0 |
| Data export with provenance | 3.0 | 4.5 | 1.0 | 1.0 |
| Reproducibility | 4.5 | 4.5 | 0.0 | 1.0 |
| Traceable references | 4.5 | 4.5 | 1.0 | 4.0 |
| Accuracy against the corpus | 4.0 | 4.0 | 3.5 | 3.5 |
| Calibration and limits | 4.5 | 3.0 | 3.5 | 4.0 |
| Decision-grade verdict | 4.0 | 3.5 | 4.0 | 4.0 |
| Facet coverage | 4.0 | 4.0 | 2.0 | 2.0 |
| **Score /100** | **81.6** | 77.5 | 38.1 | 41.4 |

**Claude Opus judge:** B and C both grounded their numbers in the same cancer-only Prism calls. B was the only one to read that evidence honestly: the top-tier meta-analysis contradicts the claim, the statistics and counter-evidence calls failed, and confidence is therefore low. B also paired this with executable outcome-specific follow-ups. C reached a 'Yes' verdict that outran its data and offered no working follow-ups. A and D gave plausible memory answers that a decision-maker cannot verify or regenerate.

**GPT judge:** C narrowly leads by combining traced evidence, useful document-level drill-down, and explicit limits on what the cancer-focused calls establish. D has stronger chart and export packaging, but its follow-up calls did not execute and its drill-down remains shallow.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/pfas-evidence/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/pfas-evidence.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Do PFAS 'forever chemicals' harm human health? Give numbers and sources.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.evidence" \
  -H 'content-type: application/json' \
  -d '{"claim": "PFAS exposure increases cancer risk", "limit": 10}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['find_evidence']["fn"](**{'claim': 'PFAS exposure increases cancer risk', 'limit': 10})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `find_evidence` (315.1 s) → `find_counter_evidence` (45.2 s) → `find_statistics` (2.2 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
