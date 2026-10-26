# ESG investing research framing

[Finance & markets](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** The stance trend of a contested investment thesis.  
> **Why it is hard.** Backlash against ESG is a 2022+ story; the framing shift is the signal.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [esg-investing-stance.json](../../examples/esg-investing-stance.json).

**The question:**

> Is academic research on ESG investing becoming more critical over time?

## What Prism returned

**782 papers** matched (phrases: esg investing, sustainable investment, responsible investing, socially responsible investing).

![Framing by year](../img/esg-investing-stance-stance.svg)

![Papers by orientation](../img/esg-investing-stance-orientation.svg)

| Year | Papers | Positive | Contested |
| ---: | ---: | ---: | ---: |
| 2017 | 63 | 12.7% | 19% |
| 2018 | 59 | 5.1% | 27.1% |
| 2019 | 96 | 22.9% | 27.1% |
| 2020 | 143 | 19.6% | 26.6% |
| 2021 | 145 | 6.2% | 8.3% |
| 2022 | 152 | 5.3% | 27% |
| 2023 | 173 | 25.4% | 12.1% |
| 2024 | 281 | 30.6% | 6.8% |
| 2025 | 342 | 26.3% | 24.9% |

### Most recent promising studies (335 matched)

| Year | Paper | Venue | Contribution |
| ---: | --- | --- | --- |
| 2025 | [Monitoring Potential of Sustainable Investment of a Cemetery Land under the Urban Expansion in Ibadan, Nigeria](https://doi.org/10.63745/joger.2025.12.30.019) | Journal of Geomatics and Environmental Research | empirical |
| 2025 | [Pls-Sem Approach To Examine The Perspectives Of Gen Z Pertaining To Sustainable Investment: A Study In Ncr, India](https://doi.org/10.5281/zenodo.18059257) | Zenodo (CERN European Organization for Nuclear Research) | empirical |
| 2025 | [Determinants of Sustainable Investment Intention: The Mediating Role of Environmental Awareness](https://doi.org/10.59075/qnfd0h63) | The critical review of social sciences studies | empirical |
| 2025 | [Behavioral interventions in ESG investing: the impact of visual nudging and reflective questioning in a neobroker-based ](http://hdl.handle.net/10362/202813) | Portuguese National Funding Agency for Science, Research and Technology (RCAAP Project by FCT) | empirical |
| 2025 | [The Relationship between Fintech and Sustainable Investment Performance](https://doi.org/10.5281/zenodo.17865755) | Zenodo (CERN European Organization for Nuclear Research) | empirical |
| 2025 | [Measuring the Impact of Socially Responsible Investments on Portfolio Performance Using the Shapley Value](http://hdl.handle.net/10362/201840) | Portuguese National Funding Agency for Science, Research and Technology (RCAAP Project by FCT) | methodological |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/esg-investing-stance-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 5.0 | 3.5 | 1.0 | 0.0 |
| Measured comparison | 5.0 | 4.5 | 1.5 | 0.5 |
| Visualisation from counted data | 4.5 | 4.0 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 3.5 | 2.0 | 1.5 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 4.0 | 1.0 | 1.0 |
| Traceable references | 2.5 | 1.5 | 1.5 | 0.5 |
| Accuracy against the corpus | 4.0 | 3.0 | 2.0 | 4.0 |
| Calibration and limits | 4.0 | 4.0 | 3.0 | 2.5 |
| Decision-grade verdict | 4.5 | 3.0 | 2.0 | 2.5 |
| Facet coverage | 4.5 | 3.5 | 1.0 | 0.5 |
| **Score /100** | **84.6** | 68.0 | 30.9 | 26.2 |

**Claude Opus judge:** C charted and read the per-year contested and positive shares. It quantified both the early-to-late decline and the 2025 rebound, and it flagged the corpus noise, giving a decision-maker a calibrated 'no, but watch 2025'. A reached the same answer from raw counts, wrongly claimed shares were unavailable, and missed the rebound. B guessed the opposite direction from memory, and D declined.

**GPT judge:** B is the most decision-ready: it gives a reproducible annual framing series, quantifies the early-to-late shift, and flags the 2025 rebound and corpus limits. Its key weakness is conflating the separate contested-share measure with critical orientations; D is more cautious but misses that critical shares can be calculated from its own data.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/esg-investing-stance/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/esg-investing-stance.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Is academic research on ESG investing becoming more critical over time?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.stance_trends" \
  -H 'content-type: application/json' \
  -d '{"term": "esg investing"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['stance_trends']["fn"](**{'term': 'esg investing'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `stance_trends` (172.8 s) → `browse_research` (81.2 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
