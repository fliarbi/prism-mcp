# Military AI research framing

[Defence & geopolitics](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** The ethical-framing trend in a sensitive field.  
> **Why it is hard.** Autonomy debates produce a large critical literature.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [military-ai-stance.json](../../examples/military-ai-stance.json).

**The question:**

> Is research on military artificial intelligence becoming more cautionary?

## What Prism returned

**328 papers** matched (phrases: autonomous weapons, autonomous weapon systems, lethal autonomous weapons, killer robots).

![Framing by year](../img/military-ai-stance-stance.svg)

![Papers by orientation](../img/military-ai-stance-orientation.svg)

| Year | Papers | Positive | Contested |
| ---: | ---: | ---: | ---: |
| 2017 | 40 | 0% | 60% |
| 2018 | 47 | 2.1% | 31.9% |
| 2019 | 66 | 9.1% | 19.7% |
| 2020 | 90 | 2.2% | 28.9% |
| 2021 | 73 | 4.1% | 21.9% |
| 2022 | 114 | 2.6% | 26.3% |
| 2023 | 100 | 1% | 38% |
| 2024 | 85 | 12.9% | 30.6% |
| 2025 | 138 | 6.5% | 29% |

### Most recent promising studies (26 matched)

| Year | Paper | Venue | Contribution |
| ---: | --- | --- | --- |
| 2025 | [Penerapan Prinsip Pembedaan dan Proposionalitas dalam Hukum Humaniter Internasional terhadap Penggunaan Senjata Otonom (](https://doi.org/10.71417/jchi.v1i2.77) | Jurnal Cendekia Hukum Indonesia | methodological |
| 2025 | [ARTIFICIAL INTELLIGENCE AND AUTONOMOUS WEAPONS SYSTEMS: A NEW ERA OF MILITARY OPERATIONS](https://doi.org/10.37701/dndivsovt.24.2025.01) | Наукові праці Державного науково-дослідного інституту випробувань і сертифікації озброєння та військової техніки | position |
| 2025 | [Hybrid Humanoid Robot; An Investigation into the Ethics of Using Robotics and Lethal Autonomous Weapons Systems for Mili](https://doi.org/10.18130/6frv-jf57) | Libra | methodological |
| 2025 | [ASSESSINGMILITARY NECESSITY OF AUTONOMOUS WEAPONSSYSTEMS(AWS) IN ARMED CONFLICTS: A CASE STUDY OF IRAN-ISRAEL](https://doi.org/10.54690/margallapapers.28.2.279) | Margalla Papers | empirical |
| 2025 | [LEGAL REGULATION OF THE USE OF AUTONOMOUS WEAPON SYSTEMS IN LAW ENFORCEMENT: CHALLENGES AND PROSPECTS](https://doi.org/10.32782/2709-9261-2025-2-14-19) | Ukrainian polyceistics theory legislation practice | review |
| 2025 | [METHODOLOGY OF INTERNET ASSESSMENT OF THE ATTITUDE OF THE UKRAINIAN POPULATION TO AUTONOMOUS WEAPONS IN THE CONTEXT OF R](https://doi.org/10.30525/978-9934-26-562-4-21) |  | methodological |
| 2024 | [Good Practices in the Legal Review of Autonomous Weapon Systems](https://doi.org/10.5281/zenodo.16778142) | Zenodo (CERN European Organization for Nuclear Research) | methodological |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/military-ai-stance-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.0 | 4.5 | 1.0 | 0.0 |
| Visualisation from counted data | 3.5 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 3.5 | 2.0 | 1.0 |
| Data export with provenance | 1.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 3.5 | 1.0 | 1.0 |
| Traceable references | 3.5 | 3.0 | 1.0 | 0.0 |
| Accuracy against the corpus | 3.5 | 3.5 | 3.0 | 1.0 |
| Calibration and limits | 4.5 | 4.0 | 3.0 | 3.0 |
| Decision-grade verdict | 4.0 | 4.0 | 2.5 | 2.5 |
| Facet coverage | 4.5 | 3.5 | 1.0 | 1.0 |
| **Score /100** | **73.6** | 72.8 | 33.0 | 18.2 |

**Claude Opus judge:** D was the only deliverable to turn counts into shares on a common denominator. Doing so showed that rising cautionary counts mostly track corpus growth, which directly answers the question. D also caught the data's own anomalies (the 328 vs 753 mismatch and unlabelled early rows). C traced its numbers well but stopped at raw counts and wrongly claimed shares were unavailable. A was honest about using memory, but B offered no answer and likely invalid references.

**GPT judge:** A is the strongest decision aid: it separates rising critical and cautionary counts from the nearly unchanged contested framing and states what the evidence can support. B adds useful comparisons and drill-down, but its count interpretation and mismatched share presentation weaken confidence; both database-backed answers miss the 328-versus-753 internal anomaly.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/military-ai-stance/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/military-ai-stance.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Is research on military artificial intelligence becoming more cautionary?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.stance_trends" \
  -H 'content-type: application/json' \
  -d '{"term": "autonomous weapons"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['stance_trends']["fn"](**{'term': 'autonomous weapons'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `stance_trends` (74.4 s) → `browse_research` (77.0 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
