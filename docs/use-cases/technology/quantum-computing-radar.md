# Quantum computing research radar

[Technology & AI](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Momentum and framing shift for a deep-tech investor.  
> **Why it is hard.** Error-correction milestones in 2024-2025 shifted the framing.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [quantum-computing-radar.json](../../examples/quantum-computing-radar.json).

**The question:**

> What is new in quantum computing research since 2023?

## What Prism returned

### Direction of travel

| Series | Window | First → last | Peak | Late third vs early third | Direction |
| --- | --- | --- | --- | ---: | --- |
| Research papers (typed corpus) | 2017 – 2025 | 11,103 → 41,759 | 41,759 (2025) | 2.39× | rising |
| News articles | 2019-01-01 – 2026-05-01 | 74 → 899 | 1,246 (2026-04-01) | 6.59× | rising |

**Framing shift since 2023:** cautionary share 8.9% before vs 11% since (+2.1 points): *framing is broadly unchanged*.

### New work since 2023

*the most-cited typed papers published since the start year whose title carries one of the subject's own phrases*

| Year | Paper | Venue | Orientation | Cited by |
| ---: | --- | --- | --- | ---: |
| 2023 | [Evidence for the utility of quantum computing before fault tolerance](https://doi.org/10.1038/s41586-023-06096-3) | Nature | breakthrough | 956 |
| 2023 | [A Survey of Important Issues in Quantum Computing and Communications](https://doi.org/10.1109/comst.2023.3254481) | IEEE Communications Surveys & Tutorials | problem_identifying | 217 |
| 2023 | [Quantum Computing for Healthcare: A Review](https://doi.org/10.3390/fi15030094) | Future Internet | breakthrough | 195 |
| 2024 | [A versatile single-photon-based quantum computing platform](https://doi.org/10.1038/s41566-024-01403-4) | Nature Photonics | breakthrough | 190 |
| 2024 | [Quantum computing with Qiskit](https://doi.org/10.48550/arxiv.2405.08810) | arXiv (Cornell University) | descriptive | 170 |
| 2024 | [Quantum Computing for High-Energy Physics: State of the Art and Challenges](https://doi.org/10.1103/prxquantum.5.037001) | PRX Quantum | problem_identifying | 160 |
| 2024 | [Distributed quantum computing: A survey](https://doi.org/10.1016/j.comnet.2024.110672) | Computer Networks | problem_identifying | 156 |
| 2023 | [MQT Bench: Benchmarking Software and Design Automation Tools for Quantum Computing](https://doi.org/10.22331/q-2023-07-20-1062) | Quantum | breakthrough | 145 |
| 2025 | [A manufacturable platform for photonic quantum computing](https://doi.org/10.1038/s41586-025-08820-7) | Nature | breakthrough | 131 |
| 2023 | [Application-Oriented Performance Benchmarks for Quantum Computing](https://doi.org/10.1109/tqe.2023.3253761) | IEEE Transactions on Quantum Engineering | breakthrough | 127 |

![Most-cited new work](../img/quantum-computing-radar-new-work.svg)

### What the research covers and the news does not

| Research topic | Papers | News articles |
| --- | ---: | ---: |
| Quantum Computing Algorithms and Architecture | 93,160 | 0 |
| Quantum Information and Cryptography | 80,327 | 0 |
| Quantum Mechanics and Applications | 41,275 | 0 |
| Quantum and electron transport phenomena | 17,840 | 0 |
| Neural Networks and Reservoir Computing | 8,579 | 0 |
| Quantum optics and atomic interactions | 8,003 | 0 |
| Cold Atom Physics and Bose-Einstein Condensates | 7,301 | 0 |
| Mechanical and Optical Resonators | 6,596 | 0 |

![Under-covered topics](../img/quantum-computing-radar-under-covered.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/quantum-computing-radar-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 2.5 | 1.0 | 0.5 |
| Measured comparison | 3.0 | 3.5 | 2.0 | 0.0 |
| Visualisation from counted data | 3.0 | 2.5 | 1.0 | 1.0 |
| Exploration and drill-down | 2.0 | 2.0 | 1.5 | 1.0 |
| Data export with provenance | 2.5 | 3.0 | 1.0 | 0.5 |
| Reproducibility | 4.0 | 3.5 | 1.0 | 1.0 |
| Traceable references | 2.5 | 3.0 | 1.0 | 0.0 |
| Accuracy against the corpus | 4.5 | 2.0 | 3.0 | 0.5 |
| Calibration and limits | 4.0 | 4.0 | 3.5 | 3.0 |
| Decision-grade verdict | 4.0 | 3.5 | 3.5 | 2.5 |
| Facet coverage | 4.0 | 3.5 | 1.5 | 1.5 |
| **Score /100** | **70.2** | 59.5 | 37.5 | 21.4 |

**Claude Opus judge:** D read every radar field correctly, including CAGRs, peak, censoring and the under-covered artifact. It quantified the change exactly and was honest that error-correction milestones are outside what the call can show. B used the same data but misreported the growth ratio and mislabelled paper counts as an index. A gave the most expert-correct narrative on error correction, but entirely from memory. C's references were largely fabricated or mismatched.

**GPT judge:** B is the strongest decision aid: it traces the broad volume and framing indicators, states their limits, and gives a usable but bounded answer. A is close, but adds unsupported coverage metadata; C and D offer more concrete error-correction claims, yet their evidence is substantially less verifiable.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/quantum-computing-radar/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/quantum-computing-radar.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is new in quantum computing research since 2023?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.radar" \
  -H 'content-type: application/json' \
  -d '{"topic": "quantum computing", "since_year": 2023}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_radar']["fn"](**{'topic': 'quantum computing', 'since_year': 2023})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
