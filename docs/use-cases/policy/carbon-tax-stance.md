# Carbon tax research framing

[Policy & regulation](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Stance trend of a flagship climate policy.  
> **Why it is hard.** Distributional critiques grew after 2018; the trend shows it.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [carbon-tax-stance.json](../../examples/carbon-tax-stance.json).

**The question:**

> Is research on carbon taxes becoming more favourable or more critical?

## What Prism returned

**2,775 papers** matched (phrases: carbon tax, carbon pricing, greenhouse gas tax, emissions tax).

![Framing by year](../img/carbon-tax-stance-stance.svg)

![Papers by orientation](../img/carbon-tax-stance-orientation.svg)

| Year | Papers | Positive | Contested |
| ---: | ---: | ---: | ---: |
| 2017 | 340 | 12.6% | 25% |
| 2018 | 403 | 15.6% | 20.8% |
| 2019 | 418 | 18.9% | 21.1% |
| 2020 | 480 | 18.3% | 26.7% |
| 2021 | 530 | 19.2% | 24.9% |
| 2022 | 645 | 17.1% | 21.4% |
| 2023 | 844 | 16.7% | 21.8% |
| 2024 | 745 | 19.6% | 22.1% |
| 2025 | 1,125 | 24.4% | 16.9% |

### Most recent promising studies (1,632 matched)

| Year | Paper | Venue | Contribution |
| ---: | --- | --- | --- |
| 2025 | [Neutrosophic Profit-based Multi-objective Fixed-charge Emission and Budget Constrained Solid Transportation Problem with](https://doi.org/10.17485/ijst/v18i48.1622) | Indian Journal of Science and Technology | methodological |
| 2025 | [SUSTAINABLE FINANCE AND THE TRANSITION TO A LOW-CARBON ECONOMY](https://doi.org/10.57233/gujoba.v4i2.05) | GUSAU Journal of Business Administration | empirical |
| 2025 | [A Dynamic Marginal Abatement Cost Framework for Manufacturing Systems: Optimising Emissions Reductions under real-world ](https://doi.org/10.64820/aepjmm.11.18.23.122025) | Journal of Mechanics and Materials | methodological |
| 2025 | [Can Carbon Emissions Trading Policies Enhance Urban Economic Resilience? Evidence from China](https://doi.org/10.1080/1540496x.2025.2610709) | Emerging Markets Finance and Trade | empirical |
| 2025 | [DO GREEN TAXES DELIVER ENVIRONMENTAL DIVIDENDS? PANEL EVIDENCE ON CARBON EFFICIENCY AND SUSTAINABILITY](https://doi.org/10.5281/zenodo.18636490) | Zenodo (CERN European Organization for Nuclear Research) | empirical |
| 2025 | [Effect of Environmental Taxation on Carbon Emissions of World’s Top Cabon Tax Revenue Countries](https://doi.org/10.35219/eai15840409545) | Annals of Dunarea de Jos University of Galati Fascicle I Economics and Applied Informatics | empirical |
| 2025 | [ROLE OF FISCAL POLICY IN THE CONTEXT OF GREEN ECONOMIC GROWTH AND CLIMATE CHANGE](https://doi.org/10.52174/2579-2989_2025.4-5) | Amberd Bulletin | empirical |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/carbon-tax-stance-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 1.5 | 0.5 |
| Visualisation from counted data | 4.5 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 4.0 | 2.0 | 2.0 |
| Data export with provenance | 3.0 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 4.0 | 1.0 | 1.0 |
| Traceable references | 3.0 | 3.0 | 1.0 | 0.5 |
| Accuracy against the corpus | 3.5 | 4.0 | 3.0 | 3.0 |
| Calibration and limits | 4.0 | 4.0 | 3.0 | 3.0 |
| Decision-grade verdict | 4.0 | 4.0 | 2.5 | 2.5 |
| Facet coverage | 4.0 | 4.0 | 1.0 | 0.5 |
| **Score /100** | **80.7** | 78.1 | 33.7 | 25.3 |

**Claude Opus judge:** B and D both grounded their answers in the 2017-2025 stance series and both recompute correctly. B charted the right quantity (positive vs contested shares), flagged that the shift is concentrated in 2025, and caught false phrase matches. D plotted raw counts in a growing corpus. A and C were honest about having no measurement but gave a decision-maker nothing traceable. C's guessed series also mis-levels the critical share, and none of the four tested the distributional-critique claim directly.

**GPT judge:** B best supports a decision because it compares traced positive and contested shares over time, quantifies the shift, and acknowledges the stable broader framing summary. A is careful and well sourced but its chart emphasizes counts; C and D do not provide a measured trend.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/carbon-tax-stance/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/carbon-tax-stance.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Is research on carbon taxes becoming more favourable or more critical?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.stance_trends" \
  -H 'content-type: application/json' \
  -d '{"term": "carbon tax"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['stance_trends']["fn"](**{'term': 'carbon tax'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `stance_trends` (33.1 s) → `browse_research` (57.9 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
