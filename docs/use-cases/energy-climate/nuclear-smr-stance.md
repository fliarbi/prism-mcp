# Small modular reactor framing

[Energy & climate](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Framing trend for a nuclear policy team.  
> **Why it is hard.** SMR cost overruns (NuScale 2023) should show as a cautionary turn.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [nuclear-smr-stance.json](../../examples/nuclear-smr-stance.json).

**The question:**

> Is research on small modular reactors getting more promising or more cautious?

## What Prism returned

**434 papers** matched (phrases: small modular reactor, small modular nuclear reactor, advanced modular reactor).

![Framing by year](../img/nuclear-smr-stance-stance.svg)

![Papers by orientation](../img/nuclear-smr-stance-orientation.svg)

| Year | Papers | Positive | Contested |
| ---: | ---: | ---: | ---: |
| 2017 | 23 | 47.8% | 8.7% |
| 2018 | 56 | 41.1% | 16.1% |
| 2019 | 52 | 13.5% | 21.2% |
| 2020 | 60 | 30% | 20% |
| 2021 | 55 | 16.4% | 3.6% |
| 2022 | 77 | 11.7% | 11.7% |
| 2023 | 134 | 31.3% | 12.7% |
| 2024 | 173 | 14.5% | 15.6% |
| 2025 | 198 | 42.4% | 6.1% |

### Most recent promising studies (332 matched)

| Year | Paper | Venue | Contribution |
| ---: | --- | --- | --- |
| 2025 | [Optimization of Solid Oxide Electrolysis Cell for Hydrogen Production Powered by Small Modular Reactors using Artificial](https://doi.org/10.1109/mepcon66918.2026.11360149) |  | methodological |
| 2025 | [Thermal coupling between a small modular nuclear reactor and a high-temperature steam electrolysis process: energy perfo](https://doi.org/10.1016/j.seta.2025.104780) | Sustainable Energy Technologies and Assessments | empirical |
| 2025 | [Model Predictive Control of a Small Modular Reactor with Partial Steam Diversion to Thermal Energy Storage with RELAP5-3](https://doi.org/10.1080/00295639.2025.2537501) | Nuclear Science and Engineering | methodological |
| 2025 | [Simulation of Thermohydrodynamic Processes during an SBO Accident with the Externally Cooled Vessel of a VVER-I Integral](https://doi.org/10.1134/s0040601525700600) | Thermal Engineering | empirical |
| 2025 | [Eco-friendly BaO-enriched zinc-calcium-erbium-borate glasses as dual radiation barriers for small modular reactors](https://doi.org/10.1016/j.chphi.2025.100981) | Chemical Physics Impact | empirical |
| 2025 | [Techno-Economic Assessment of Data Center Load Demand Powered by Small Modular Reactors and Distributed Energy Resources](https://doi.org/10.1115/imece2025-166968) |  | empirical |
| 2025 | [Corrosion and Anodic Oxidation of Alloy 690 in Simulated Primary Coolant of a Small Modular Reactor Studied by In Situ E](https://doi.org/10.3390/met15111242) | Metals | empirical |
| 2025 | [Research on linear load-following optimal control of a small modular reactor based on marginal entropy model predictive ](https://doi.org/10.1049/icp.2025.3564) | IET conference proceedings. | methodological |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/nuclear-smr-stance-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 3.5 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 3.0 | 1.5 | 0.0 |
| Visualisation from counted data | 4.5 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 3.0 | 1.5 | 1.0 |
| Data export with provenance | 3.0 | 0.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 3.0 | 1.0 | 1.0 |
| Traceable references | 3.0 | 2.0 | 1.0 | 0.5 |
| Accuracy against the corpus | 3.0 | 4.0 | 2.0 | 4.0 |
| Calibration and limits | 3.5 | 3.0 | 3.0 | 3.0 |
| Decision-grade verdict | 3.5 | 4.0 | 2.5 | 2.0 |
| Facet coverage | 4.0 | 3.5 | 1.0 | 0.5 |
| **Score /100** | **75.1** | 61.0 | 30.6 | 24.4 |

**Claude Opus judge:** B gave a fully traced orientation series split into positive and contested shares, an exact 2017-vs-2025 comparison, placed limits, and a caught count anomaly; its verdict honestly separates the 2025 rebound from a flat-to-slightly-negative net change. C was accurate but reported counts only and had untraced computed export columns. A declined to answer and D relied on memory about NuScale costs rather than measuring the research trend.

**GPT judge:** B best distinguishes rising research volume from the direction of orientation shares, gives a cautious decision with confidence and conditions, and preserves the key limits. A has richer charts and breakdowns but misreads the browse result’s filtered count and overstates the favorable endpoint; C is transparent but cannot answer the measured facets, while D’s cost-caution narrative remains memory-based.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/nuclear-smr-stance/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/nuclear-smr-stance.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Is research on small modular reactors getting more promising or more cautious?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.stance_trends" \
  -H 'content-type: application/json' \
  -d '{"term": "small modular reactor"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['stance_trends']["fn"](**{'term': 'small modular reactor'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `stance_trends` (44.8 s) → `browse_research` (78.9 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
