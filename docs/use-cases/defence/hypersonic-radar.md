# Hypersonic weapons research

[Defence & geopolitics](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Research momentum on a strategic technology.  
> **Why it is hard.** Much of it is in engineering venues, not defence journals.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [hypersonic-radar.json](../../examples/hypersonic-radar.json).

**The question:**

> What is new in hypersonic missile research?

## What Prism returned

### Direction of travel

| Series | Window | First → last | Peak | Late third vs early third | Direction |
| --- | --- | --- | --- | ---: | --- |
| Research papers (typed corpus) | 2017 – 2025 | 5,269 → 6,048 | 6,251 (2024) | 1.15× | flat |
| News articles | 2019-01-01 – 2026-05-01 | 0 → 19 | 87 (2025-03-01) | 3.27× | rising |

**Framing shift since 2021:** cautionary share 6.4% before vs 6% since (-0.4 points): *framing is broadly unchanged*.

### New work since 2021

*the most-cited typed papers published since the start year whose title carries one of the subject's own phrases*

| Year | Paper | Venue | Orientation | Cited by |
| ---: | --- | --- | --- | ---: |
| 2021 | [Finite-Time Fuzzy Adaptive Constrained Tracking Control for Hypersonic Flight Vehicles With Singularity-Free Switching](https://doi.org/10.1109/tmech.2021.3090509) | IEEE/ASME Transactions on Mechatronics | breakthrough | 105 |
| 2021 | [Air–Carbon Ablation Model for Hypersonic Flight from Molecular-Beam Data](https://doi.org/10.2514/1.j060516) | AIAA Journal | breakthrough | 67 |
| 2022 | [Finite-Time Deterministic Learning Command Filtered Control for Hypersonic Flight Vehicle](https://doi.org/10.1109/taes.2022.3160687) | IEEE Transactions on Aerospace and Electronic Systems | promising | 64 |
| 2021 | [Predefined-Time Asymptotic Tracking Control for Hypersonic Flight Vehicles With Input Quantization and Faults](https://doi.org/10.1109/taes.2021.3068442) | IEEE Transactions on Aerospace and Electronic Systems | breakthrough | 53 |
| 2023 | [Robust Self-Learning Fault-Tolerant Control for Hypersonic Flight Vehicle Based on ADHDP](https://doi.org/10.1109/tsmc.2023.3264552) | IEEE Transactions on Systems Man and Cybernetics Systems | breakthrough | 40 |
| 2022 | [Robust Adaptive Control of Hypersonic Flight Vehicle With Aero-Servo-Elastic Effect](https://doi.org/10.1109/taes.2022.3210153) | IEEE Transactions on Aerospace and Electronic Systems | promising | 40 |
| 2023 | [Safe Reinforcement Learning-Based Robust Approximate Optimal Control for Hypersonic Flight Vehicles](https://doi.org/10.1109/tvt.2023.3264243) | IEEE Transactions on Vehicular Technology | breakthrough | 32 |
| 2021 | [Intelligent Control of Flexible Hypersonic Flight Dynamics With Input Dead Zone Using Singular Perturbation Decompositio](https://doi.org/10.1109/tnnls.2021.3131578) | IEEE Transactions on Neural Networks and Learning Systems | promising | 32 |
| 2021 | [Adaptive dynamic programing design for the neural control of hypersonic flight vehicles](https://doi.org/10.1016/j.jfranklin.2021.08.014) | Journal of the Franklin Institute | promising | 32 |
| 2021 | [Realization of trajectory precise tracking for hypersonic flight vehicles with prescribed performances](https://doi.org/10.1016/j.ast.2021.106554) | Aerospace Science and Technology | breakthrough | 27 |

![Most-cited new work](../img/hypersonic-radar-new-work.svg)

### What the research covers and the news does not

| Research topic | Papers | News articles |
| --- | ---: | ---: |
| Ultrasonics and Acoustic Wave Propagation | 48,743 | 0 |
| Geophysical Methods and Applications | 6,784 | 0 |
| Acoustic Wave Resonator Technologies | 3,600 | 0 |
| Thermography and Photoacoustic Techniques | 3,596 | 0 |
| Acoustic Wave Phenomena Research | 2,667 | 0 |
| Microwave Imaging and Scattering Analysis | 2,551 | 0 |
| Photoacoustic and Ultrasonic Imaging | 2,261 | 0 |
| Flow Measurement and Analysis | 2,242 | 0 |

![Under-covered topics](../img/hypersonic-radar-under-covered.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/hypersonic-radar-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 1.0 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.0 | 3.5 | 1.0 | 0.0 |
| Visualisation from counted data | 4.0 | 4.0 | 1.0 | 0.5 |
| Exploration and drill-down | 4.0 | 2.0 | 1.0 | 1.0 |
| Data export with provenance | 3.0 | 3.5 | 1.0 | 0.5 |
| Reproducibility | 5.0 | 4.5 | 1.0 | 1.0 |
| Traceable references | 3.5 | 1.0 | 1.0 | 0.0 |
| Accuracy against the corpus | 4.5 | 4.0 | 2.5 | 3.5 |
| Calibration and limits | 4.0 | 4.0 | 3.0 | 3.0 |
| Decision-grade verdict | 4.0 | 4.0 | 3.0 | 2.5 |
| Facet coverage | 5.0 | 4.0 | 1.0 | 1.5 |
| **Score /100** | **76.4** | 72.1 | 31.6 | 26.6 |

**Claude Opus judge:** B and C both grounded their answers in the radar call, but B covered every facet. It contrasted research output (flat, 1.15x) with news attention (3.27x) using correct arithmetic, flagged the off-topic under-covered rows, and gave resolvable references with honest limits. C was accurate but charted only research and broke its DOIs and CSV formatting. A and D answered from memory; D's estimated publication doubling contradicts the measured flat trend.

**GPT judge:** D is strongest for a decision-maker: it connects the research themes to a traced publication trend and contrasts that with rising news attention, while warning that neither establishes capability. C has stronger full-series and export machinery, but its failed DOI checks materially weaken the paper-level evidence.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/hypersonic-radar/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/hypersonic-radar.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is new in hypersonic missile research?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.radar" \
  -H 'content-type: application/json' \
  -d '{"topic": "hypersonic", "since_year": 2021}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_radar']["fn"](**{'topic': 'hypersonic', 'since_year': 2021})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
