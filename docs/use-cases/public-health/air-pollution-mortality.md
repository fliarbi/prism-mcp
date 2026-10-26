# Air pollution and mortality

[Public health & epidemiology](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Effect sizes with sources, for a public-health briefing.  
> **Why it is hard.** The corpus files this under 'Air Quality and Health Impacts', not 'air pollution'; term discovery matters.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [air-pollution-mortality.json](../../examples/air-pollution-mortality.json).

**The question:**

> How strong is the evidence that PM2.5 air pollution increases mortality? Give numbers.

## What Prism returned

### How much evidence exists

| Corpus | Records on both sides of the claim | Window |
| --- | ---: | --- |
| Typed research papers | 115,772 | 2017-2025 |
| Papers with abstracts | 888 | 1990-2025 |
| the health literature index records | 811 | 1990-2025 |
| News articles | 934 | 2019-01-01..2026-06-01 |
| Patents | 20 | 2005-2024 |
| arXiv preprints | 1 | 2005-2025 |

![Evidence volume by corpus](../img/air-pollution-mortality-volumes.svg)

![Framing of the literature](../img/air-pollution-mortality-sides.svg)

*orientation is a label on the paper's own framing, not a verdict on the claim; this corpus starts in 2017* Contested share: **17.2%**.

### The strongest evidence, read

> few titles carry both sides of this claim, so the documents read were chosen by the subject in the title and the outcome in the abstract.

Prism read 2 sources: **2 support, 0 contradict, 0 qualify** (tier-weighted {"supports": 6, "contradicts": 0, "qualifies": 0}). Each quote is copied from the abstract and verified against it; 2 candidate quotes failed that check and were dropped.

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2017 | [Long-Term PM2.5 Exposure and Respiratory, Cancer, and Cardiovascular Mortality in Older US Adults](https://doi.org/10.1093/aje/kwx166)<br><sub>American Journal of Epidemiology</sub> | article | supports | We found significantly positive associations of 12-month moving average PM2.5 exposures (per 10-μg/m3 increase) with respiratory, chronic obstructive pulmonary disease, and pneumonia mortality, with risk ratios ranging from 1.10 to 1.24. |
| 2018 | [Ambient PM2.5 exposure and expected premature mortality to 2100 in India under climate change scenarios](https://doi.org/10.1038/s41467-017-02755-y)<br><sub>Nature Communications</sub> | article | supports | Premature mortality burden is expected to be 2.4-4 and 28.5-38.8% higher under RCP8.5 scenario relative to the RCP4.5 scenario in 2031-2040 and 2091-2100, respectively. |
| 2020 | [Global Estimates and Long-Term Trends of Fine Particulate Matter Concentrations (1998–2018)](https://doi.org/10.1021/acs.est.0c01764)<br><sub>Environmental Science & Technology</sub> | article | unrelated | Exposure to outdoor fine particulate matter (PM<sub>2.5</sub>) is a leading risk factor for mortality. |
| 2019 | [Transition in source contributions of PM2.5 exposure and associated premature mortality in China during 2005–2015](https://doi.org/10.1016/j.envint.2019.105111)<br><sub>Environment International</sub> | article | unrelated | From 2005 to 2015, the mortality due to PM<sub>2.5</sub> from ambient air pollution (AAP) decreases from 1.04 (95% confidence interval, 0.84-1.25) million to 0.87 (0.70-1.04) million. |
| 2019 | [Estimating mortality burden attributable to short-term PM2.5 exposure: A national observational study in China](https://doi.org/10.1016/j.envint.2019.01.073)<br><sub>Environment International</sub> | article | unread | – |
| 2020 | [The impact of long-term PM2.5 exposure on specific causes of death: exposure-response curves and effect modification amo](https://doi.org/10.1186/s12940-020-00575-0)<br><sub>Environmental Health</sub> | article | unread | – |

![Study designs](../img/air-pollution-mortality-tiers.svg)

### What disagrees

Prism's counter-evidence pass found no source that directly contradicts the claim among those it read (tally {"supports": 2, "contradicts": 0, "qualifies": 0, "unrelated": 2, "unread": 2}).

> The documents read support the claim; this selected sample does not establish scientific consensus.

### Numbers you can quote

| Figure | Measures | Population | Source |
| --- | --- | --- | --- |
| **5%** | increase in all-cause mortality per 10 μg/m3 increase in PM2.5 |  | [The impact of long-term PM2.5 exposure on specific causes of death: exposure-response curves and effect modification amo](https://doi.org/10.1186/s12940-020-00575-0) 2020 |
| **8.8%** | increase in cardiovascular disease deaths per 10 μg/m3 increase in PM2.5 |  | [The impact of long-term PM2.5 exposure on specific causes of death: exposure-response curves and effect modification amo](https://doi.org/10.1186/s12940-020-00575-0) 2020 |
| **5.6%** | increase in respiratory deaths per 10 μg/m3 increase in PM2.5 |  | [The impact of long-term PM2.5 exposure on specific causes of death: exposure-response curves and effect modification amo](https://doi.org/10.1186/s12940-020-00575-0) 2020 |
| **2.5%** | increase in cancer deaths per 10 μg/m3 increase in PM2.5 |  | [The impact of long-term PM2.5 exposure on specific causes of death: exposure-response curves and effect modification amo](https://doi.org/10.1186/s12940-020-00575-0) 2020 |
| **10% to 27%** | effects of PM2.5 on cardiovascular mortality higher than conventional estimates |  | [Understanding the Joint Impacts of Fine Particulate Matter Concentration and Composition on the Incidence and Mortality ](https://doi.org/10.1021/acs.est.9b06861) 2020 |
| **32,186 deaths** | deaths attributable to PM2.5 exposure (linear model estimate) |  | [Estimating mortality burden attributable to short-term PM2.5 exposure: A national observational study in China](https://doi.org/10.1016/j.envint.2019.01.073) 2019 |

![Research output per year](../img/air-pollution-mortality-research-series.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/air-pollution-mortality-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 3.5 | 1.0 | 0.5 |
| Measured comparison | 3.5 | 4.5 | 2.0 | 1.5 |
| Visualisation from counted data | 3.0 | 3.5 | 1.0 | 1.0 |
| Exploration and drill-down | 2.5 | 3.0 | 1.0 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 1.0 |
| Reproducibility | 3.5 | 4.5 | 1.0 | 0.0 |
| Traceable references | 3.0 | 4.5 | 1.5 | 1.0 |
| Accuracy against the corpus | 2.5 | 4.0 | 2.0 | 1.0 |
| Calibration and limits | 3.5 | 4.5 | 3.0 | 3.0 |
| Decision-grade verdict | 3.5 | 4.0 | 0.0 | 2.5 |
| Facet coverage | 4.0 | 4.5 | 1.0 | 1.0 |
| **Score /100** | 65.2 | **79.1** | 25.4 | 24.1 |

**Claude Opus judge:** C and D were both grounded in the recorded Prism responses and both flagged the 7-paper intersection limit. A and B relied on memory, and B's citations did not match its effect sizes. C edged D by covering more facets: the full trend with peak and CAGR, the news thirds, and a traced cause-specific effect chart. D was slightly cleaner on accuracy but charted and exported only research volume.

**GPT judge:** A best supports a decision: it pairs traceable mortality effect estimates with clear limits on what the selected corpus can establish, and it makes the policy implication conditional on observational evidence. B includes more material but introduces an unresolved, directionally inconsistent news trend and an unsupported study window; C and D rely on unverified memory estimates and conflicting reference details.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/air-pollution-mortality/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/air-pollution-mortality.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How strong is the evidence that PM2.5 air pollution increases mortality? Give numbers.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.evidence" \
  -H 'content-type: application/json' \
  -d '{"claim": "PM2.5 air pollution increases mortality", "limit": 10}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['find_evidence']["fn"](**{'claim': 'PM2.5 air pollution increases mortality', 'limit': 10})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `find_evidence` (126.2 s) → `find_counter_evidence` (30.4 s) → `find_statistics` (31.2 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
