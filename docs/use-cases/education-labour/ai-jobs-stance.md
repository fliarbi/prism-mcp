# AI and jobs research framing

[Education & labour](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Stance trend for a workforce strategy.  
> **Why it is hard.** Generative AI shifted the framing from automation to augmentation.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [ai-jobs-stance.json](../../examples/ai-jobs-stance.json).

**The question:**

> Is research on AI and automation-driven job displacement becoming more pessimistic?

## What Prism returned

**95 papers** matched (phrases: job displacement, workforce attrition).

![Framing by year](../img/ai-jobs-stance-stance.svg)

![Papers by orientation](../img/ai-jobs-stance-orientation.svg)

| Year | Papers | Positive | Contested |
| ---: | ---: | ---: | ---: |
| 2017 | 17 | 5.9% | 23.5% |
| 2018 | 13 | 0% | 23.1% |
| 2019 | 13 | 23.1% | 30.8% |
| 2020 | 9 | 11.1% | 22.2% |
| 2021 | 14 | 14.3% | 21.4% |
| 2022 | 7 | 0% | 57.1% |
| 2023 | 26 | 3.8% | 11.5% |
| 2024 | 35 | 14.3% | 20% |
| 2025 | 42 | 19% | 23.8% |

### Most recent promising studies (27 matched)

| Year | Paper | Venue | Contribution |
| ---: | --- | --- | --- |
| 2025 | [THE ROLE OF UNIONS IN ADDRESSING AI-INDUCED JOB DISPLACEMENT: A REVIEW STUDY](https://doi.org/10.35631/ijlgc.1041042) | International Journal of Law Government and Communication | review |
| 2025 | [Explainable Hybrid AI Model for Employee Retention and Workforce Attrition Prediction](https://doi.org/10.4018/979-8-3373-2215-5.ch015) |  | empirical |
| 2025 | [AI-ASSISTED INTERPRETING: VALUABLE TOOL OR JOB DISPLACEMENT?](https://doi.org/10.14293/p2199-8442.1.sop-.pgjtpv.v1) |  | review |
| 2025 | [Design and Evaluation of a Machine Learning Framework for Anticipating Workforce Attrition Trends](https://doi.org/10.38124/ijisrt/25may172) |  | methodological |
| 2025 | [AI Adoption Impact on Human Productivity and Job Displacement Simulation using System Dynamics Approach in R](https://doi.org/10.1109/rmkmate64874.2025.11042685) |  | empirical |
| 2025 | [Artificial Intelligence, Job Displacement, and Gender-Specific Training Pathways: A Multi-Group Analysis](https://doi.org/10.63332/joph.v5i5.1572) | Journal of Posthumanism | empirical |
| 2025 | [The Role of AI in Transforming Labor Markets: Productivity Gains Versus Job Displacement](https://doi.org/10.62802/vk8h9g79) | Next generation. | empirical |
| 2025 | [Exploring Workforce Attrition in Early Childcare Sector Using Data Segmentation, Machine Learning and Artificial Neural ](https://doi.org/10.63227/652.299.101) |  | methodological |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/ai-jobs-stance-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.0 | 1.5 | 0.0 |
| Measured comparison | 3.5 | 4.0 | 2.0 | 0.0 |
| Visualisation from counted data | 4.0 | 3.0 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 2.0 | 1.5 | 0.5 |
| Data export with provenance | 3.0 | 2.5 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 4.0 | 0.0 | 0.5 |
| Traceable references | 3.5 | 3.0 | 3.0 | 0.0 |
| Accuracy against the corpus | 3.0 | 3.5 | 3.5 | 3.0 |
| Calibration and limits | 4.0 | 3.5 | 3.0 | 1.0 |
| Decision-grade verdict | 3.5 | 3.5 | 3.0 | 0.0 |
| Facet coverage | 4.5 | 3.5 | 1.5 | 0.5 |
| **Score /100** | **77.3** | 67.4 | 38.5 | 11.3 |

**Claude Opus judge:** D best answered the actual question with traced data. It decomposed orientation counts so the promising rise could be set against the pessimistic labels, recomputed every ratio exactly, and caught the off-topic HR-attrition rows and the count mismatch that bias the corpus. B reached the same answer from the same data but charted only the promising share and left the pessimism side thin. C gave an informed memory-based narrative that cannot be checked, and A declined to answer.

**GPT judge:** A is the most decision-ready: it answers the question from the traced framing data, distinguishes paper framing from displacement outcomes, and names the limits. C has stronger traceability and drill-down, but its unsupported definition of ‘contested’ and unresolved corpus-count mismatch weaken its conclusion; B is a transparent memory-based synthesis, while D provides no substantive answer.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/ai-jobs-stance/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/ai-jobs-stance.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Is research on AI and automation-driven job displacement becoming more pessimistic?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.stance_trends" \
  -H 'content-type: application/json' \
  -d '{"term": "job displacement"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['stance_trends']["fn"](**{'term': 'job displacement'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `stance_trends` (18.6 s) → `browse_research` (24.5 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
