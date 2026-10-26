# Mindfulness research framing

[Academic research & literature review](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Framing trend for a meta-research paper.  
> **Why it is hard.** Replication critiques after 2017 should show.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [mindfulness-stance.json](../../examples/mindfulness-stance.json).

**The question:**

> Is research on mindfulness becoming more critical over time?

## What Prism returned

**20,812 papers** matched (phrases: mindfulness, mindful awareness, mindfulness-based interventions, mindful practice, mindfulness training, mindfulness meditation).

![Framing by year](../img/mindfulness-stance-stance.svg)

![Papers by orientation](../img/mindfulness-stance-orientation.svg)

| Year | Papers | Positive | Contested |
| ---: | ---: | ---: | ---: |
| 2017 | 2,743 | 31% | 9.7% |
| 2018 | 3,023 | 31.4% | 10.4% |
| 2019 | 3,595 | 24.1% | 10.2% |
| 2020 | 4,111 | 31.1% | 8.6% |
| 2021 | 4,627 | 26.1% | 9.7% |
| 2022 | 4,866 | 33.5% | 9.1% |
| 2023 | 5,643 | 26% | 8.3% |
| 2024 | 5,799 | 34.9% | 7.9% |
| 2025 | 6,990 | 29.1% | 8.7% |

### Most recent promising studies (23,174 matched)

| Year | Paper | Venue | Contribution |
| ---: | --- | --- | --- |
| 2025 | [Mindfulness-based interventions for caregivers and family members of individuals in palliative care](https://doi.org/10.11606/issn.2176-7262.rmrp.2025.225207) | Medicina (Ribeirão Preto) | review |
| 2025 | [Effects of yoga practice on perceived stress levels and mindfulness during the COVID-19 pandemic: pilot study with colle](https://doi.org/10.11606/issn.2176-7262.rmrp.2025.220695) | Medicina (Ribeirão Preto) | empirical |
| 2025 | Unraveling the impact of loneliness on brain and emotion: exploring pathways for meaningful interventions | The International Islamic University Malaysia Repository (The International Islamic University Malaysia) | review |
| 2025 | Mindful Parenting as an Educational Construction for Children in Single-Parent FamiliesafterDivorce | Research Repository Universitas Islam Negeri Maulana Malik Ibrahim (University of Southampton) | methodological |
| 2025 | [The effects of a breathing meditation program on job satisfaction and mindfulness in early childhood teachers](https://doi.org/10.12972/mpca.2025.35.2) | Journal of Meditation based Psychological Counseling | empirical |
| 2025 | [Structural Relationships among Mindfulness, Achievement Emotions, and Academic Performance in Nursing Students: Mediatin](https://doi.org/10.5392/ijoc.2025.21.4.150) | International Journal of Contents | empirical |
| 2025 | [A Text Mining Analysis of Domestic Research Trends on Mindfulness-Based Parenting Stress](https://doi.org/10.58601/kjre.2025.12.30.09) |  | empirical |
| 2025 | [Self-Control and Digital Well-Being Among University Students: A Mediation Analysis of Online Mindfulness within a Self-](https://doi.org/10.24036/02025144148-0-86) | Konselor | empirical |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/mindfulness-stance-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 5.0 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.0 | 4.5 | 1.5 | 0.0 |
| Visualisation from counted data | 4.5 | 3.0 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 3.5 | 1.5 | 1.0 |
| Data export with provenance | 3.0 | 3.5 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.0 | 0.0 | 1.0 |
| Traceable references | 3.5 | 0.5 | 2.5 | 0.5 |
| Accuracy against the corpus | 3.0 | 3.5 | 2.0 | 4.0 |
| Calibration and limits | 4.0 | 4.0 | 3.0 | 2.5 |
| Decision-grade verdict | 4.0 | 4.0 | 2.5 | 2.5 |
| Facet coverage | 4.0 | 3.5 | 1.0 | 0.5 |
| **Score /100** | **78.2** | 69.8 | 30.6 | 24.8 |

**Claude Opus judge:** C decomposed the measured series: critical share fell from 1.2% to 0.6% while total volume grew about 2.5x, and contested share fell from 10.1% to 8.3%. It also tied paper IDs and specific limits to its 'not more critical' answer. B reached the same reading but did not use the yearly totals it had. D's memory-based 'probably yes' contradicts the record, and A gave no answer.

**GPT judge:** C gives the strongest decision-grade account: it traces the annual series, compares framing shares and orientation growth, and lays out relevant limits. Its denominator mix-up and unsupported coverage claims keep it below a clean expert-ready result; B is more cautious but leaves the supported framing comparison out of its chart and export.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/mindfulness-stance/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/mindfulness-stance.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Is research on mindfulness becoming more critical over time?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.stance_trends" \
  -H 'content-type: application/json' \
  -d '{"term": "mindfulness"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['stance_trends']["fn"](**{'term': 'mindfulness'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `stance_trends` (52.4 s) → `browse_research` (98.3 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
