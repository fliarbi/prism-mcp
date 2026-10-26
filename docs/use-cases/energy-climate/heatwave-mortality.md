# Heatwaves and mortality

[Energy & climate](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Effect sizes for a climate-adaptation plan.  
> **Why it is hard.** Effect sizes vary hugely by city; population must travel with each number.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [heatwave-mortality.json](../../examples/heatwave-mortality.json).

**The question:**

> How strong is the evidence that heatwaves increase mortality? Give numbers.

## What Prism returned

### How much evidence exists

| Corpus | Records on both sides of the claim | Window |
| --- | ---: | --- |
| Typed research papers | 3,133 | 2017-2025 |
| Papers with abstracts | 128 | 1990-2025 |
| the health literature index records | 4,435 | 1990-2025 |
| News articles | 17 | 2019-01-01..2026-06-01 |
| Patents | 0 | 2005-2024 |
| arXiv preprints | 0 | 2005-2025 |

![Evidence volume by corpus](../img/heatwave-mortality-volumes.svg)

![Framing of the literature](../img/heatwave-mortality-sides.svg)

*orientation is a label on the paper's own framing, not a verdict on the claim; this corpus starts in 2017* Contested share: **27.4%**.

### The strongest evidence, read

Prism read 3 sources: **3 support, 0 contradict, 0 qualify** (tier-weighted {"supports": 10, "contradicts": 0, "qualifies": 0}). Each quote is copied from the abstract and verified against it; 0 candidate quotes failed that check and were dropped.

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2023 | [Public Health Preparedness for Extreme Heat Events](https://doi.org/10.1146/annurev-publhealth-071421-025508)<br><sub>Annual Review of Public Health</sub> | review | unrelated | climate change is driving an increasing proportion of heat-related mortality |
| 2022 | [Extreme heat events, high ambient temperatures and human morbidity and mortality in Africa: A systematic review](https://doi.org/10.17159/sajs.2022/12047)<br><sub>South African Journal of Science</sub> | review | supports | Eleven studies showed that high ambient temperatures and heat waves are linked with increased mortality rates in Africa |
| 2014 | [Exploring 167 years of vulnerability: An examination of extreme heat events in Australia 1844–2010](https://doi.org/10.1016/j.envsci.2014.05.003)<br><sub>Environmental Science & Policy</sub> | article | supports | From 1844 to 2010, extreme heat events have been responsible for at least 5332 fatalities in Australia |
| 2022 | [Climate Change and Extreme Heat Events: How Health Systems Should Prepare](https://doi.org/10.1056/cat.21.0454)<br><sub>NEJM Catalyst</sub> | article | supports | EHEs cause excess morbidity and mortality directly from heat illness, aggravation of comorbid conditions, and exacerbation of the damaging health effects of social factors as well as indirectly from corollary events such as wildfires and air pollution. |
| 2025 | [Quantifying the contributions of climate change and adaptation to mortality from unprecedented extreme heat events](https://doi.org/10.1073/pnas.2503577122)<br><sub>Proceedings of the National Academy of Sciences</sub> | article | unread | we attribute 6,079 deaths in August 2003 to climate change. |
| 2025 | [Sustainable cooling strategies for workers in the ready-made garment factory industry in Bangladesh under simulated extr](https://doi.org/10.1016/j.lanplh.2025.101317)<br><sub>The Lancet. Planetary health</sub> | trial | unrelated | Sustainable cooling interventions can reduce physiological heat strain under peak heat stress conditions in a typical non-airconditioned Bangladeshi ready-made garment factory. |
| 2024 | [Indoor overheating: A review of vulnerabilities, causes, and strategies to prevent adverse human health outcomes during ](https://doi.org/10.1080/23328940.2024.2361223)<br><sub>Temperature</sub> | review | unrelated | The likelihood of exposure to overheated indoor environments is increasing |
| 2019 | [Associations between Green Building Design Strategies and Community Health Resilience to Extreme Heat Events: A Systemat](https://doi.org/10.3390/ijerph16040663)<br><sub>International Journal of Environmental Research and Public Health</sub> | review | unrelated | Public health co-benefits included reducing the risk of vulnerability to heat stress and reducing heat-related morbidity and mortality |

![Study designs](../img/heatwave-mortality-tiers.svg)

### What disagrees

Prism's counter-evidence pass found no source that directly contradicts the claim among those it read (tally {"supports": 0, "contradicts": 0, "qualifies": 0, "unrelated": 7, "unread": 1}).

> No verified document verdict supports a wording recommendation for this claim.

### Numbers you can quote

| Figure | Measures | Population | Source |
| --- | --- | --- | --- |
| **6,079 deaths** | deaths attributed to climate change in August 2003 |  | [Quantifying the contributions of climate change and adaptation to mortality from unprecedented extreme heat events](https://doi.org/10.1073/pnas.2503577122) 2025 |
| **55%** | underprediction of excess deaths by standard heat-mortality exposure-response functions |  | [Quantifying the contributions of climate change and adaptation to mortality from unprecedented extreme heat events](https://doi.org/10.1073/pnas.2503577122) 2025 |

![Research output per year](../img/heatwave-mortality-research-series.svg)

**Extracted disease-factor claims** (2 claims; extracted claims, not papers — one paper can produce several, and the same finding restated in ten papers counts ten times): association/increases (review_meta) ×1, association/increases (review_meta) ×1

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/heatwave-mortality-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 3.5 | 3.0 | 2.0 | 0.5 |
| Visualisation from counted data | 3.5 | 3.0 | 1.0 | 0.0 |
| Exploration and drill-down | 3.0 | 1.0 | 1.5 | 0.5 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.5 | 1.0 | 1.0 |
| Traceable references | 4.0 | 1.0 | 1.0 | 1.0 |
| Accuracy against the corpus | 4.0 | 3.0 | 3.0 | 3.5 |
| Calibration and limits | 4.5 | 4.5 | 3.0 | 3.0 |
| Decision-grade verdict | 4.0 | 4.0 | 3.5 | 2.5 |
| Facet coverage | 3.5 | 3.5 | 1.0 | 1.0 |
| **Score /100** | **76.5** | 65.0 | 36.1 | 25.8 |

**Claude Opus judge:** B and A both grounded their answers in the retrieved record and said plainly that no pooled, population-specific effect size was available. B pulled ahead with correct call tags, the tool's own trend metrics, all references resolving, and a careful reading of the source-fit failures. D gave the decision-relevant magnitudes a reader wants, but from memory with several misattributions. C answered without any numbers, which fails a question that explicitly asked for them.

**GPT judge:** B is the strongest decision aid because it separates corpus activity from mortality evidence, reports the available numeric findings with their limits, and avoids claiming a pooled risk estimate when no population denominator was retrieved. D offers a useful annual chart, but its misattributed statistics and malformed DOI weaken its evidence trail; neither deliverable supplies the population-linked effect size the question most needs.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/heatwave-mortality/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/heatwave-mortality.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How strong is the evidence that heatwaves increase mortality? Give numbers.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.evidence" \
  -H 'content-type: application/json' \
  -d '{"claim": "Heatwaves increase mortality", "limit": 10}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['find_evidence']["fn"](**{'claim': 'Heatwaves increase mortality', 'limit': 10})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `find_evidence` (134.3 s) → `find_counter_evidence` (15.2 s) → `find_statistics` (9.5 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
