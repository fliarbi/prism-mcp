# Nearshoring research radar

[Supply chain & trade](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A strategy radar for manufacturing.  
> **Why it is hard.** Post-2020 literature; framing moved from cost to resilience.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [nearshoring-radar.json](../../examples/nearshoring-radar.json).

**The question:**

> What is new in research on supply chain reshoring and nearshoring?

## What Prism returned

### Direction of travel

| Series | Window | First → last | Peak | Late third vs early third | Direction |
| --- | --- | --- | --- | ---: | --- |
| Research papers (typed corpus) | 2017 – 2025 | 9,608 → 29,387 | 29,387 (2025) | 2.26× | rising |
| News articles | 2019-01-01 – 2026-05-01 | 0 → 0 | 10 (2026-01-01) | 3.1× | rising |

**Framing shift since 2021:** cautionary share 29.1% before vs 29.8% since (+0.7 points): *framing is broadly unchanged*.

### New work since 2021

*the most-cited typed papers published since the start year whose title carries one of the subject's own phrases*

| Year | Paper | Venue | Orientation | Cited by |
| ---: | --- | --- | --- | ---: |
| 2024 | [SME supply chain resilience in disruptive times: the effects of supply chain robustness, access to government assistance](https://doi.org/10.1108/bpmj-02-2024-0073) | Business Process Management Journal | promising | 21 |
| 2021 | [The impact of information security initiatives on supply chain robustness and performance: an empirical study](https://doi.org/10.1108/ics-07-2020-0128) | Information and Computer Security | promising | 17 |
| 2021 | [Leverage risks for supply chain robustness against corruption](https://doi.org/10.1108/imds-10-2020-0587) | Industrial Management & Data Systems | promising | 9 |
| 2025 | [How do talent and technology factors affect supply chain robustness and resilience? Evidence from Chinese manufacturers](https://doi.org/10.1108/imds-07-2024-0676) | Industrial Management & Data Systems | promising | 7 |
| 2021 | [Improving Supply Chain Robustness &amp; Resilience? Lessons from a case study in the automotive industry during the firs](https://hal.science/hal-03306223) | HAL (Le Centre pour la Communication Scientifique Directe) | promising | 2 |
| 2025 | [Enhancing Liquefied Natural Gas supply chain robustness through digital twin-driven machine learning models: A special c](https://doi.org/10.1016/j.jgsce.2025.205714) | Gas Science and Engineering | breakthrough | 2 |
| 2022 | [Increasing Supply Chain Robustness During Allocation in a Just-in-Time Supply Set-Up](https://doi.org/10.1109/wsc57314.2022.10015477) | 2022 Winter Simulation Conference (WSC) | promising | 1 |
| 2022 | [The Effect of Cloud-Based Supply Chain Integration and Information Security Initiatives on Supply Chain Robustness and P](https://doi.org/10.21776/ub.apmba.2022.010.03.11) | Asia Pacific Management and Business Application | promising | 1 |
| 2024 | [Evaluating the Impact of Technological Adaptation in Third-Party Logistics on Farming Household Sustainability: The Medi](https://doi.org/10.31357/jbri.v10i1.7553) | Journal of business research and insights. | promising | 1 |
| 2025 | [Resilience in the Age of Disruption: How Digitalisation Enhances Supply Chain Robustness](https://doi.org/10.21863/jscms/2025.14.3.001) | Journal of Supply Chain Management Systems | promising | 0 |

![Most-cited new work](../img/nearshoring-radar-new-work.svg)

### What the research covers and the news does not

| Research topic | Papers | News articles |
| --- | ---: | ---: |
| Quality and Supply Management | 19,571 | 0 |
| Recycling and Waste Management Techniques | 9,051 | 0 |
| Sustainable Industrial Ecology | 8,180 | 0 |
| Consumer Market Behavior and Pricing | 4,190 | 0 |
| Outsourcing and Supply Chain Management | 4,026 | 0 |
| Supply Chain Resilience and Risk Management | 56,251 | 2 |
| Environmental Sustainability in Business | 27,477 | 6 |
| Innovation and Socioeconomic Development | 4,958 | 2 |

![Under-covered topics](../img/nearshoring-radar-under-covered.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/nearshoring-radar-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 3.5 | 1.0 | 0.0 |
| Measured comparison | 4.0 | 3.5 | 2.0 | 0.5 |
| Visualisation from counted data | 3.5 | 4.0 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 2.0 | 2.0 | 1.5 |
| Data export with provenance | 4.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.0 | 0.0 | 0.0 |
| Traceable references | 4.0 | 3.5 | 1.0 | 1.0 |
| Accuracy against the corpus | 4.5 | 4.0 | 2.5 | 1.0 |
| Calibration and limits | 4.0 | 3.5 | 3.0 | 3.0 |
| Decision-grade verdict | 4.0 | 4.0 | 2.5 | 3.0 |
| Facet coverage | 3.5 | 3.0 | 1.0 | 1.5 |
| **Score /100** | **79.6** | 71.1 | 30.8 | 20.6 |

**Claude Opus judge:** C was the only deliverable that traced nearly every number, recomputed its derived ratios correctly and carried the tool's caveats next to the figures. It also caught that the proxy search returned 'robustness' papers rather than reshoring work, so it did not present them as findings. B was honest but thinner, leaving out the news trend and the under-covered panel. A was a candid memory estimate, and D's references show fabricated-looking metadata.

**GPT judge:** B is the clearest decision brief: it answers that the supplied evidence measures broad resilience research, not reshoring or nearshoring, and gives a bounded sourcing recommendation. A has richer traced breakdowns and exports, but its trend and coverage claims carry material caveat problems; C and D rely on memory or provide no measurable research trend.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/nearshoring-radar/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/nearshoring-radar.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is new in research on supply chain reshoring and nearshoring?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.radar" \
  -H 'content-type: application/json' \
  -d '{"topic": "supply chain resilience", "since_year": 2021}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_radar']["fn"](**{'topic': 'supply chain resilience', 'since_year': 2021})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
