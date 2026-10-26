# Precision agriculture research radar

[Agriculture & food security](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A technology radar for an agtech fund.  
> **Why it is hard.** Drones, AI and IoT sub-literatures move at different speeds.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [precision-farming-radar.json](../../examples/precision-farming-radar.json).

**The question:**

> What is new in precision agriculture research?

## What Prism returned

### Direction of travel

| Series | Window | First → last | Peak | Late third vs early third | Direction |
| --- | --- | --- | --- | ---: | --- |
| Research papers (typed corpus) | 2017 – 2025 | 3,250 → 24,885 | 24,885 (2025) | 4.35× | rising |
| News articles | 2019-01-01 – 2026-05-01 | 37 → 70 | 120 (2025-03-01) | 2.55× | rising |

**Framing shift since 2022:** cautionary share 10.3% before vs 8.3% since (-2.0 points): *framing is broadly unchanged*.

### New work since 2022

*the most-cited typed papers published since the start year whose title carries one of the subject's own phrases*

| Year | Paper | Venue | Orientation | Cited by |
| ---: | --- | --- | --- | ---: |
| 2023 | [The Path to Smart Farming: Innovations and Opportunities in Precision Agriculture](https://doi.org/10.3390/agriculture13081593) | Agriculture | descriptive | 645 |
| 2024 | [Application of Precision Agriculture Technologies for Sustainable Crop Production and Environmental Sustainability: A Sy](https://doi.org/10.1155/2024/2126734) | The Scientific World JOURNAL | promising | 254 |
| 2024 | [Smart Sensors and Smart Data for Precision Agriculture: A Review](https://doi.org/10.3390/s24082647) | Sensors | descriptive | 248 |
| 2022 | [A Comprehensive Survey of the Recent Studies with UAV for Precision Agriculture in Open Fields and Greenhouses](https://doi.org/10.3390/app12031047) | Applied Sciences | problem_identifying | 217 |
| 2024 | [Integrating artificial intelligence and Internet of Things (IoT) for enhanced crop monitoring and management in precisio](https://doi.org/10.1016/j.sintl.2024.100292) | Sensors International | promising | 214 |
| 2024 | [A systematic review of hyperspectral imaging in precision agriculture: Analysis of its current state and future prospect](https://doi.org/10.1016/j.compag.2024.109037) | Computers and Electronics in Agriculture | promising | 197 |
| 2025 | [Deep learning and computer vision in plant disease detection: a comprehensive review of techniques, models, and trends i](https://doi.org/10.1007/s10462-024-11100-x) | Artificial Intelligence Review | descriptive | 192 |
| 2023 | [Emerging Frontiers in Nanotechnology for Precision Agriculture: Advancements, Hurdles and Prospects](https://doi.org/10.3390/agrochemicals2020016) | Agrochemicals | descriptive | 174 |
| 2024 | [Drones in Precision Agriculture: A Comprehensive Review of Applications, Technologies, and Challenges](https://doi.org/10.3390/drones8110686) | Drones | promising | 168 |
| 2024 | [Enhancing precision agriculture: A comprehensive review of machine learning and AI vision applications in all-terrain ve](https://doi.org/10.1016/j.atech.2024.100483) | Smart Agricultural Technology | promising | 166 |

![Most-cited new work](../img/precision-farming-radar-new-work.svg)

### What the research covers and the news does not

| Research topic | Papers | News articles |
| --- | ---: | ---: |
| Smart Agriculture and AI | 90,008 | 0 |
| Spectroscopy and Chemometric Analyses | 15,152 | 0 |
| Leaf Properties and Growth Measurement | 6,834 | 0 |
| Greenhouse Technology and Climate Control | 5,317 | 0 |
| Plant Disease Management Techniques | 4,031 | 0 |
| Remote Sensing and LiDAR Applications | 3,775 | 0 |
| Date Palm Research Studies | 3,650 | 0 |
| IoT-based Smart Home Systems | 2,390 | 0 |

![Under-covered topics](../img/precision-farming-radar-under-covered.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/precision-farming-radar-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 3.0 | 1.0 | 0.0 |
| Measured comparison | 4.0 | 4.0 | 1.5 | 0.5 |
| Visualisation from counted data | 3.5 | 3.0 | 1.0 | 0.0 |
| Exploration and drill-down | 3.0 | 2.0 | 1.0 | 0.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.5 | 4.0 | 1.0 | 1.0 |
| Traceable references | 3.0 | 3.0 | 0.5 | 0.0 |
| Accuracy against the corpus | 2.5 | 3.0 | 2.5 | 3.5 |
| Calibration and limits | 4.0 | 4.0 | 3.5 | 3.0 |
| Decision-grade verdict | 3.5 | 3.0 | 3.0 | 3.0 |
| Facet coverage | 4.0 | 3.5 | 1.0 | 1.0 |
| **Score /100** | **70.8** | 64.6 | 32.3 | 24.7 |

**Claude Opus judge:** C and D both grounded their answers in the radar call. C used more of it: it quantified the research and news trends with ratios and the news peak, listed all ten DOI-linked works, and read the under-coverage zeros correctly. D omitted the news series and misread the direction of the framing shift in its verdict. A and B were honest memory-only answers with no measured support; B added labelled estimates that understate the recorded growth.

**GPT judge:** D offers the broadest decision-grade picture: it connects research and news trends, framing, recent papers, and taxonomy results while explaining what those counts cannot establish. Its numerical coverage and drill-down are stronger than B’s, though an orientation-count error and unsupported peak caveat weaken its accuracy; B is the cleaner, more restrained alternative.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/precision-farming-radar/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/precision-farming-radar.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is new in precision agriculture research?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.radar" \
  -H 'content-type: application/json' \
  -d '{"topic": "precision agriculture", "since_year": 2022}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_radar']["fn"](**{'topic': 'precision agriculture', 'since_year': 2022})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
