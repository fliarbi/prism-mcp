# Gut microbiome and depression literature

[Academic research & literature review](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A literature map for a systematic review.  
> **Why it is hard.** Mouse studies and human cohorts share a vocabulary; stance labels separate the framings.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [microbiome-depression-stance.json](../../examples/microbiome-depression-stance.json).

**The question:**

> How is research on the gut microbiome and depression framed, and which recent studies are most promising?

## What Prism returned

**14 papers** matched (phrases: gut microbiome and depression, gut-brain axis in depression).

![Framing by year](../img/microbiome-depression-stance-stance.svg)

![Papers by orientation](../img/microbiome-depression-stance-orientation.svg)

| Year | Papers | Positive | Contested |
| ---: | ---: | ---: | ---: |
| 2018 | 2 | 100% | 0% |
| 2020 | 4 | 25% | 0% |
| 2021 | 1 | 0% | 0% |
| 2022 | 1 | 0% | 100% |
| 2023 | 4 | 25% | 0% |
| 2024 | 3 | 33.3% | 33.3% |
| 2025 | 2 | 50% | 0% |

### Most recent promising studies (6 matched)

| Year | Paper | Venue | Contribution |
| ---: | --- | --- | --- |
| 2025 | [The microbiota-gut-brain axis in depression: unraveling the relationships and therapeutic opportunities](https://doi.org/10.3389/fimmu.2025.1644160) | Frontiers in Immunology | review |
| 2024 | [The Impact of Antidepressants on Gut Microbiome and Depression Management](https://doi.org/10.36877/pmmb.a0000446) | Progress In Microbes & Molecular Biology | review |
| 2023 | [Bioengineered Wheat Arabinoxylan: Fostering Next-Generation Prebiotics Targeting Gut Microbiome and Depression Inversely](https://doi.org/10.20381/ruor-29036) | uO Research (University of Ottawa) | empirical |
| 2020 | [Gut Microbiome and Depression: How Microbes Affect the Way We Think](https://doi.org/10.7759/cureus.9966) | Cureus | review |
| 2018 | [Gut microbiome and depression: what we know and what we need to know](https://doi.org/10.1515/revneuro-2017-0072) | Reviews in the Neurosciences | theoretical |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/microbiome-depression-stance-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 5.0 | 4.5 | 1.0 | 0.0 |
| Measured comparison | 4.0 | 4.0 | 1.0 | 0.5 |
| Visualisation from counted data | 4.0 | 4.0 | 1.0 | 0.0 |
| Exploration and drill-down | 2.5 | 2.5 | 1.5 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 3.0 | 1.0 | 1.0 |
| Traceable references | 4.0 | 3.5 | 3.0 | 4.0 |
| Accuracy against the corpus | 4.0 | 4.0 | 3.0 | 4.0 |
| Calibration and limits | 4.5 | 4.0 | 3.0 | 3.0 |
| Decision-grade verdict | 4.0 | 3.5 | 3.0 | 3.5 |
| Facet coverage | 4.0 | 4.0 | 1.0 | 1.5 |
| **Score /100** | **81.5** | 72.9 | 36.7 | 35.5 |

**Claude Opus judge:** A and D both grounded their framing analysis in the recorded calls. A was more careful: it caught the anomaly where counts did not sum to totals, placed its limits next to the numbers, kept nulls as nulls, and calibrated confidence as low. D overstated confidence on a 14-paper base. B and C, answering from memory, correctly separated mouse transfer studies from human cohorts but could not measure framing or trends; C was the most honest about this, and B offered labelled estimates.

**GPT judge:** B gives the clearest decision-grade account: it traces the framing series, quantifies the cautious shift, and links the small, review-heavy corpus to practical limits. D is close, but its chart turns absent years into zeros and its export/reproduction details are weaker; A and C rely mainly on memory or estimates.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/microbiome-depression-stance/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/microbiome-depression-stance.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How is research on the gut microbiome and depression framed, and which recent studies are most promising?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.stance_trends" \
  -H 'content-type: application/json' \
  -d '{"term": "gut microbiome depression"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['stance_trends']["fn"](**{'term': 'gut microbiome depression'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `stance_trends` (43.9 s) → `browse_research` (61.1 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
