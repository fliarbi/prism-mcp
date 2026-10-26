# Deepfake fraud research radar

[Crime & public safety](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A radar on a fast-moving threat.  
> **Why it is hard.** Generative AI moved this field in 2023; recency is everything.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [deepfake-fraud-radar.json](../../examples/deepfake-fraud-radar.json).

**The question:**

> What has changed in research on deepfake detection and fraud since 2022?

## What Prism returned

### Direction of travel

| Series | Window | First → last | Peak | Late third vs early third | Direction |
| --- | --- | --- | --- | ---: | --- |
| Research papers (typed corpus) | 2017 – 2025 | 2,437 → 6,988 | 6,988 (2025) | 2.01× | rising |
| News articles | 2019-01-01 – 2026-05-01 | 0 → 0 | 5 (2025-03-01) | 7.5× | rising |

**Framing shift since 2022:** cautionary share 7.6% before vs 9.5% since (+1.9 points): *framing is broadly unchanged*.

### New work since 2022

*the most-cited typed papers published since the start year whose title carries one of the subject's own phrases*

| Year | Paper | Venue | Orientation | Cited by |
| ---: | --- | --- | --- | ---: |
| 2022 | [A Review of Modern Audio Deepfake Detection Methods: Challenges and Future Directions](https://doi.org/10.3390/a15050155) | Algorithms | breakthrough | 147 |
| 2023 | [DFFMD: A Deepfake Face Mask Dataset for Infectious Disease Era With Deepfake Detection Algorithms](https://doi.org/10.1109/access.2023.3246661) | IEEE Access | breakthrough | 63 |
| 2022 | [Comparative Analysis on Different DeepFake Detection Methods and Semi Supervised GAN Architecture for DeepFake Detection](https://doi.org/10.1109/i-smac55078.2022.9987265) | 2022 Sixth International Conference on I-SMAC (IoT in Social, Mobile, Analytics and Cloud) (I-SMAC) | comparative | 27 |
| 2022 | [A Comparative Study on Deepfake Detection Algorithms](https://doi.org/10.1109/icac3n56670.2022.10074593) |  | comparative | 5 |
| 2024 | [A Study on Deepfake Detection Methods](https://doi.org/10.1109/ihcsp63227.2024.10960252) |  | problem_identifying | 2 |
| 2023 | [Artifact Based Deepfake Detection Methods](https://doi.org/10.1109/ici60088.2023.10421629) |  | comparative | 2 |
| 2024 | [One Detector to Rule Them All? On the Robustness and Generalizability of Current State-of-the-Art Deepfake Detection Met](https://doi.org/10.2352/ei.2024.36.4.mwsf-332) | Electronic Imaging | critical | 2 |
| 2024 | [2D-Malafide: Adversarial Attacks Against Face Deepfake Detection Systems](https://doi.org/10.1109/biosig61931.2024.10786754) |  | breakthrough | 2 |
| 2024 | [A Survey of Deepfake Detection Methods: Innovations, Accuracy, and Future Directions](https://doi.org/10.55041/ijsrem37000) | INTERANTIONAL JOURNAL OF SCIENTIFIC RESEARCH IN ENGINEERING AND MANAGEMENT | promising | 1 |
| 2024 | [Comparative analysis of deepfake detection methods using machine learning and deep learning](https://doi.org/10.1109/iccpct61902.2024.10673002) |  | cautionary | 1 |

![Most-cited new work](../img/deepfake-fraud-radar-new-work.svg)

### What the research covers and the news does not

| Research topic | Papers | News articles |
| --- | ---: | ---: |
| Digital Media Forensic Detection | 40,023 | 0 |
| Advanced Steganography and Watermarking Techniques | 13,174 | 0 |
| Generative Adversarial Networks and Image Synthesis | 9,723 | 0 |
| Chaos-based Image/Signal Encryption | 6,541 | 0 |
| Anomaly Detection Techniques and Applications | 3,704 | 0 |
| Adversarial Robustness in Machine Learning | 3,351 | 0 |
| Face recognition and analysis | 2,296 | 0 |
| Advanced Malware Detection Techniques | 2,283 | 0 |

![Under-covered topics](../img/deepfake-fraud-radar-under-covered.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/deepfake-fraud-radar-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 3.5 | 1.0 | 1.0 |
| Measured comparison | 4.0 | 4.5 | 2.0 | 1.0 |
| Visualisation from counted data | 3.0 | 3.0 | 1.0 | 1.0 |
| Exploration and drill-down | 3.0 | 2.5 | 2.0 | 1.5 |
| Data export with provenance | 3.0 | 3.5 | 1.0 | 1.0 |
| Reproducibility | 5.0 | 4.0 | 0.0 | 1.0 |
| Traceable references | 3.5 | 3.5 | 3.0 | 2.5 |
| Accuracy against the corpus | 4.0 | 4.0 | 3.5 | 2.5 |
| Calibration and limits | 4.5 | 4.5 | 3.5 | 3.5 |
| Decision-grade verdict | 4.0 | 4.5 | 3.5 | 2.5 |
| Facet coverage | 4.0 | 3.5 | 1.5 | 1.5 |
| **Score /100** | **77.4** | 75.4 | 40.2 | 34.9 |

**Claude Opus judge:** C and A both grounded their numbers in the radar call. C exposed the full new-work and under-covered layers, named the peak and the censoring, and admitted that the fraud half was unmeasured, which made it the most decision-ready. D gave a knowledgeable memory synthesis with honest labels but nothing traceable. B rested on mis-cited references.

**GPT judge:** C is the strongest decision-grade answer: it accurately quantifies research growth, distinguishes framing from truth, and clearly bounds what the data cannot say about fraud. D is close and more complete on surfaced papers, but overstates comparability for framing windows whose dates are missing; neither response measures deepfake-specific fraud outcomes.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/deepfake-fraud-radar/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/deepfake-fraud-radar.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What has changed in research on deepfake detection and fraud since 2022?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.radar" \
  -H 'content-type: application/json' \
  -d '{"topic": "deepfake detection", "since_year": 2022}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_radar']["fn"](**{'topic': 'deepfake detection', 'since_year': 2022})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
