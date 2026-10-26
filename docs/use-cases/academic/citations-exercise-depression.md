# Vancouver citations for exercise and depression

[Academic research & literature review](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Citation-ready references for a manuscript.  
> **Why it is hard.** Meta-analyses outrank single trials; the ranking shows why.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [citations-exercise-depression.json](../../examples/citations-exercise-depression.json).

**The question:**

> Give me Vancouver-style citations showing exercise reduces depression, ranked by evidence weight.

## What Prism returned

### VANCOUVER citations, rendered from stored metadata

1. Zhao X, Oh S, Zhang Z, Wang C. Move your body, stay away from depression: a systematic review and meta-analysis of exercise-based prevention of depression in middle-aged and older adults. Frontiers in public health. 2025. https://doi.org/10.3389/fpubh.2025.1554195 <sub>[meta_analysis, very_high]</sub>

Inline markers: `[1]`

### Source ladder

| Rank | Source | Tier | Why this tier carries the weight it does |
| ---: | --- | --- | --- |
| 1 | [Effects of physical activity on depressive symptoms during breast cancer survivorship: a meta-analysis of randomised con](https://doi.org/10.1136/esmoopen-2017-000271) (2017) | meta_analysis | pools multiple studies and reports a combined estimate |
| 2 | [Does aerobic exercise reduce postpartum depressive symptoms? a systematic review and meta-analysis](https://doi.org/10.3399/bjgp17x692525) (2017) | meta_analysis | pools multiple studies and reports a combined estimate |
| 3 | [The association between accelerometer-measured physical activity and symptoms of depression and anxiety in children and ](https://doi.org/10.1186/s12887-025-06420-y) (2025) | meta_analysis | pools multiple studies and reports a combined estimate |
| 4 | [Effect of exercise on mental health and alcohol consumption in individuals with alcohol use disorder: a systematic revie](https://doi.org/10.1136/bmjopen-2025-102622) (2025) | meta_analysis | pools multiple studies and reports a combined estimate |
| 5 | [Effects of exercise on psychological distress in patients with COPD: A systematic review and meta-analysis of randomised](https://doi.org/10.1097/MD.0000000000044026) (2025) | meta_analysis | pools multiple studies and reports a combined estimate |
| 6 | [Impact of aerobic exercise on cardiovascular and mental health in postmenopausal women: a systematic review and meta-ana](https://doi.org/10.1097/GME.0000000000002552) (2025) | meta_analysis | pools multiple studies and reports a combined estimate |
| 7 | [Effects of Exercise on Depression and Anxiety in Lung Cancer Survivors: A Systematic Review and Meta-Analysis of Randomi](https://doi.org/10.3390/curroncol32060304) (2025) | meta_analysis | pools multiple studies and reports a combined estimate |
| 8 | [Move your body, stay away from depression: a systematic review and meta-analysis of exercise-based prevention of depress](https://doi.org/10.3389/fpubh.2025.1554195) (2025) | meta_analysis | pools multiple studies and reports a combined estimate |

![Source tiers](../img/citations-exercise-depression-ladder.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/citations-exercise-depression-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Data export with provenance | 3.5 | 3.0 | 1.0 | 1.0 |
| Reproducibility | 4.0 | 2.0 | 0.0 | 1.0 |
| Traceable references | 3.5 | 3.0 | 3.5 | 3.5 |
| Accuracy against the corpus | 3.5 | 3.5 | 1.5 | 3.5 |
| Calibration and limits | 4.0 | 3.0 | 2.5 | 3.0 |
| Decision-grade verdict | 3.5 | 3.5 | 3.0 | 4.0 |
| Facet coverage | 3.5 | 3.0 | 1.0 | 1.5 |
| **Score /100** | **73.0** | 60.0 | 35.2 | 51.8 |

**Claude Opus judge:** C was the only deliverable that grounded every element in the recorded calls. It exported a traced, provenance-complete CSV and read the tool honestly: only 1 of 8 Vancouver entries came back, and the evidence tier was flat across all eight sources. It also bounded its decision to what the data measured. A and B gave clinically sensible memory answers built on landmark reviews, but they are unverifiable, and B's effect sizes contain errors. D was grounded but drew too narrow a verdict from its own evidence and reshuffled the ranking.

**GPT judge:** C best preserves the distinction between the one directly returned prevention citation, whose stance qualifies, and the population-specific records that do not establish a universal treatment effect. B gives a useful, plausible memory-based answer with a practical decision, while A overstates what its retrieved records support and D relies on unverified numeric specifics.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/citations-exercise-depression/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/citations-exercise-depression.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Give me Vancouver-style citations showing exercise reduces depression, ranked by evidence weight.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.citations" \
  -H 'content-type: application/json' \
  -d '{"claim": "Exercise reduces depression symptoms", "style": "vancouver", "limit": 8}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['get_citations']["fn"](**{'claim': 'Exercise reduces depression symptoms', 'style': 'vancouver', 'limit': 8})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `get_citations` (297.6 s) → `rank_sources` (17.5 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
