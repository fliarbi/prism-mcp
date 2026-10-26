# How intermittent-fasting research is framed

[Medical & clinical evidence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Year-by-year framing of the literature, plus the most promising recent studies.  
> **Why it is hard.** Framing is a property of thousands of abstracts, not something a model can recall.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [intermittent-fasting-stance.json](../../examples/intermittent-fasting-stance.json).

**The question:**

> How has research on intermittent fasting shifted in tone over the past years? Is it getting more promising or more cautious?

## What Prism returned

**1,549 papers** matched (phrases: intermittent fasting, time-restricted feeding, alternate day fasting, periodic fasting, fasting protocols).

![Framing by year](../img/intermittent-fasting-stance-stance.svg)

![Papers by orientation](../img/intermittent-fasting-stance-orientation.svg)

| Year | Papers | Positive | Contested |
| ---: | ---: | ---: | ---: |
| 2017 | 91 | 19.8% | 18.7% |
| 2018 | 123 | 31.7% | 14.6% |
| 2019 | 237 | 18.1% | 6.3% |
| 2020 | 302 | 20.2% | 14.9% |
| 2021 | 358 | 25.7% | 11.5% |
| 2022 | 422 | 26.1% | 7.1% |
| 2023 | 443 | 32.5% | 11.7% |
| 2024 | 481 | 31.2% | 7.5% |
| 2025 | 611 | 30.9% | 8.7% |

### Most recent promising studies (1,545 matched)

| Year | Paper | Venue | Contribution |
| ---: | --- | --- | --- |
| 2025 | Reactivity of Isolated Arteries After 5-Week-Lasting Period of Intermittent Fasting Followed by the Return to Ad Libitum | the health literature index | empirical |
| 2025 | [The Relationship Between the Level of Understanding of Intermittent Fasting and Self-Motivation Behavior Toward the Risk](https://doi.org/10.64141/pmhs.v2i2.51) | Papua Medicine and Health Science | empirical |
| 2025 | [Intermittent Fasting and Probiotics for Gut Microbiota Modulation in Type 2 Diabetes Mellitus: A Narrative Review](https://doi.org/10.3390/nu18010119) | Nutrients | review |
| 2025 | Medical Reflection: The Urgency of Fasting Therapy | Research Repository Universitas Islam Negeri Maulana Malik Ibrahim (University of Southampton) | review |
| 2025 | [Protective effects of intermittent fasting and chamomile extract against margarine-induced oxidative stress in mouse tis](https://doi.org/10.1080/13813455.2025.2610470) | Archives of Physiology and Biochemistry | empirical |
| 2025 | [Pre-exposure to time-restricted feeding reduces tissue CD4+ T cells with a limited effect on Mycobacterium tuberculosis ](https://doi.org/10.17632/ypnpckfx6z.1) | Mendeley Data | empirical |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/intermittent-fasting-stance-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 5.0 | 4.0 | 1.0 | 1.0 |
| Measured comparison | 5.0 | 4.0 | 1.5 | 1.0 |
| Visualisation from counted data | 4.0 | 3.0 | 1.0 | 0.5 |
| Exploration and drill-down | 4.0 | 3.5 | 2.0 | 1.5 |
| Data export with provenance | 3.0 | 4.0 | 1.0 | 1.0 |
| Reproducibility | 5.0 | 4.0 | 1.0 | 1.0 |
| Traceable references | 3.0 | 3.0 | 3.0 | 1.0 |
| Accuracy against the corpus | 4.5 | 4.0 | 1.5 | 1.0 |
| Calibration and limits | 4.5 | 4.0 | 3.0 | 2.5 |
| Decision-grade verdict | 4.5 | 4.0 | 2.0 | 2.0 |
| Facet coverage | 4.0 | 3.0 | 1.5 | 1.5 |
| **Score /100** | **85.8** | 74.5 | 32.7 | 25.1 |

**Claude Opus judge:** C answered the tone question with the right measure: yearly positive vs contested shares, exact deltas, and early/late ratios. It also flagged the tool's own facet inconsistency, giving a decision-maker a traced 'more promising in volume, broadly stable in balance' answer. B reached the same verdict with traced data but charted counts rather than shares. A and D answered from memory with a 'more cautious' narrative that the measured corpus does not support, and D additionally fabricated and misdated references.

**GPT judge:** A best supports a decision: it traces the full annual series, separates rising counts from the largely stable contested share, and states what the framing labels can and cannot establish. C is also well sourced, but its count-only chart and single-year ratio do less to answer whether the balance of tone shifted.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/intermittent-fasting-stance/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/intermittent-fasting-stance.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How has research on intermittent fasting shifted in tone over the past years? Is it getting more promising or more cautious?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.stance_trends" \
  -H 'content-type: application/json' \
  -d '{"term": "intermittent fasting"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['stance_trends']["fn"](**{'term': 'intermittent fasting'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `stance_trends` (22.8 s) → `browse_research` (18.9 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
