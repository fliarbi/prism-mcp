# What is my AI-ethics reading list missing?

[Academic research & literature review](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Library-gap analysis for a thesis.  
> **Why it is hard.** Coverage gaps are measured against the corpus, not suggested from memory.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [library-gaps-ai-ethics.json](../../examples/library-gaps-ai-ethics.json).

**The question:**

> Here is my reading list on AI ethics. What important topics is it missing?
> 
> - Algorithmic bias in hiring
> - Fairness in machine learning
> - Explainable AI methods
> - Privacy-preserving machine learning

## What Prism returned

Prism resolved the list against **200** corpus records for 4 items.

| Theme the list covers | Records in the list's neighbourhood |
| --- | ---: |
| Privacy-Preserving Technologies in Data | 95 |
| Cryptography and Data Security | 44 |
| Explainable Artificial Intelligence (XAI) | 40 |
| Adversarial Robustness in Machine Learning | 36 |
| Ethics and Social Impacts of AI | 26 |
| Blockchain Technology Applications and Security | 24 |

![Themes covered](../img/library-gaps-ai-ethics-themes.svg)

### Highly cited work the list is missing

| Year | Paper | Cited by |
| ---: | --- | ---: |
| 2016 | [Rethinking the Inception Architecture for Computer Vision](https://doi.org/10.1109/cvpr.2016.308) | 30,936 |
| 2018 | [MobileNetV2: Inverted Residuals and Linear Bottlenecks](https://doi.org/10.1109/cvpr.2018.00474) | 24,528 |
| 2020 | [An Image is Worth 16x16 Words: Transformers for Image Recognition at Scale](https://doi.org/10.48550/arxiv.2010.11929) | 21,613 |
| 2017 | [Grad-CAM: Visual Explanations from Deep Networks via Gradient-Based Localization](https://doi.org/10.1109/iccv.2017.74) | 21,555 |
| 2018 | [CBAM: Convolutional Block Attention Module](https://doi.org/10.1007/978-3-030-01234-2_1) | 21,428 |
| 2023 | [Generative Adversarial Nets](https://doi.org/10.1007/978-3-658-40442-0_9) | 19,938 |
| 2017 | [Xception: Deep Learning with Depthwise Separable Convolutions](https://doi.org/10.1109/cvpr.2017.195) | 18,952 |
| 2015 | [Delving Deep into Rectifiers: Surpassing Human-Level Performance on ImageNet Classification](https://doi.org/10.1109/iccv.2015.123) | 18,777 |
| 2016 | ["Why Should I Trust You?"](https://doi.org/10.1145/2939672.2939778) | 15,223 |
| 2020 | [Generative adversarial networks](https://doi.org/10.1145/3422622) | 13,622 |

### Recent work the list is missing

| Year | Paper | Cited by |
| ---: | --- | ---: |
| 2024 | [On a Method to Measure Supervised Multiclass Model’s Interpretability: Application to Degradation Diagnosis (Short Paper](https://doi.org/10.4230/oasics.dx.2024.27) | 13,138 |
| 2025 | [On Assessing ML Model Robustness: A Methodological Framework (Academic Track)](https://doi.org/10.4230/oasics.saia.2024.1) | 4,499 |
| 2024 | [The effects of over-reliance on AI dialogue systems on students' cognitive abilities: a systematic review](https://doi.org/10.1186/s40561-024-00316-7) | 1,011 |
| 2024 | [Mixup: Beyond empirical risk minimization](https://doi.org/10.57702/dcy1c3gw) | 960 |
| 2024 | [Ethical and regulatory challenges of AI technologies in healthcare: A narrative review](https://doi.org/10.1016/j.heliyon.2024.e26297) | 811 |
| 2024 | [A survey on large language model (LLM) security and privacy: The Good, The Bad, and The Ugly](https://doi.org/10.1016/j.hcc.2024.100211) | 768 |
| 2024 | [Cyberfraud in the Nigerian Banking Sector: The Techniques and Preventive Measures](https://doi.org/10.38124/ijisrt/ijisrt24aug395) | 739 |
| 2025 | [Accurate predictions on small data with a tabular foundation model](https://doi.org/10.1038/s41586-024-08328-6) | 636 |
| 2024 | [Detecting hallucinations in large language models using semantic entropy](https://doi.org/10.1038/s41586-024-07421-0) | 626 |
| 2024 | [Practical guide to <scp>SHAP</scp> analysis: Explaining supervised machine learning model predictions in drug developmen](https://doi.org/10.1111/cts.70056) | 595 |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/library-gaps-ai-ethics-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Visualisation from counted data | 3.5 | 0.0 | 0.0 | 0.0 |
| Exploration and drill-down | 3.0 | 3.0 | 2.0 | 1.0 |
| Data export with provenance | 4.0 | 3.5 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.0 | 1.0 | 0.0 |
| Traceable references | 3.0 | 3.0 | 3.0 | 3.5 |
| Accuracy against the corpus | 3.0 | 3.0 | 4.0 | 4.0 |
| Calibration and limits | 3.5 | 4.5 | 3.0 | 4.0 |
| Decision-grade verdict | 3.5 | 3.5 | 4.0 | 4.0 |
| Facet coverage | 3.5 | 3.5 | 1.5 | 1.0 |
| **Score /100** | **69.2** | 61.7 | 45.1 | 40.7 |

**Claude Opus judge:** A was the only deliverable that used the gap scan correctly. It read the theme counts by their definition, filtered the off-topic computer-vision 'highly cited missing' rows, and flagged the citation anomalies. It then turned the ethics-relevant recent items into concrete additions with DOIs and separated them from memory-based gaps. C used the same data but misread covered themes as gaps. B and D gave sensible but unmeasured, memory-only topic lists.

**GPT judge:** C best supports a decision-maker by separating corpus-grounded themes and leads from the question of whether they are truly ethics-relevant, while preserving traceable exports and explicit limits. D is more elaborate, but its misreading of the theme counts and unsupported date make its comparisons less dependable; A and B are honest memory-based suggestions without corpus-grounded coverage.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/library-gaps-ai-ethics/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/library-gaps-ai-ethics.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Here is my reading list on AI ethics. What important topics is it missing?

- Algorithmic bias in hiring
- Fairness in machine learning
- Explainable AI methods
- Privacy-preserving machine learning
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.library_gaps" \
  -H 'content-type: application/json' \
  -d '{"items": ["Algorithmic bias in hiring", "Fairness in machine learning", "Explainable AI methods", "Privacy-preserving machine learning"], "subject": "ai ethics"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['library_gaps']["fn"](**{'items': ['Algorithmic bias in hiring', 'Fairness in machine learning', 'Explainable AI methods', 'Privacy-preserving machine learning'], 'subject': 'ai ethics'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
