# GDPR enforcement research

[Legal & compliance](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Regulatory-research radar for a compliance officer.  
> **Why it is hard.** Legal scholarship is slow; the radar shows how little is new.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [gdpr-fines-radar.json](../../examples/gdpr-fines-radar.json).

**The question:**

> What is new in research on GDPR enforcement and fines?

## What Prism returned

### Direction of travel

| Series | Window | First → last | Peak | Late third vs early third | Direction |
| --- | --- | --- | --- | ---: | --- |

### New work since 2022

*the most-cited typed papers published since the start year whose title carries one of the subject's own phrases*

| Year | Paper | Venue | Orientation | Cited by |
| ---: | --- | --- | --- | ---: |
| 2022 | [DPL: A Language for GDPR Enforcement](https://doi.org/10.1109/csf54842.2022.9919687) |  | breakthrough | 13 |
| 2022 | [Collective Damages for GDPR Breaches: A Feasible solution for the GDPR Enforcement Deficit?](https://doi.org/10.21552/edpl/2022/4/8) | European Data Protection Law Review | problem_identifying | 3 |
| 2023 | [GDPRxiv: Establishing the State of the Art in GDPR Enforcement](https://doi.org/10.56553/popets-2023-0121) | Proceedings on Privacy Enhancing Technologies | breakthrough | 2 |
| 2022 | [New limitations on GDPR enforcement? Advocate General’s Opinion in UI v Österreichische Post](https://doi.org/10.21428/9885764c.071a3da6) |  | critical | 1 |
| 2023 | [rgpdOS: GDPR Enforcement By The Operating System](https://doi.org/10.1109/dsn-s58398.2023.00032) |  | breakthrough | 1 |
| 2025 | [GDPR Enforcement Beyond EU-Borders — The Dutch Data Protection Authority’s Fine on Clearview AI and the Future of AI Reg](https://doi.org/10.9785/cri-2025-260103) | Computer Law Review International | problem_identifying | 0 |
| 2024 | [The Future of GDPR Enforcement](https://doi.org/10.59704/8c530ef633b462d7) |  | problem_identifying | 0 |
| 2024 | [It’s Not What You Say, It’s How You Say It: Investigating GDPR Enforcement Variation in the EU](https://doi.org/10.5465/amproc.2024.17252abstract) | Academy of Management Proceedings | critical | 0 |
| 2023 | [DPA powers toward effective and transparent GDPR enforcement: the case of Croatia](https://doi.org/10.24818/tbj/2023/13/2.03) | Juridical Tribune | problem_identifying | 0 |
| 2022 | [GDPR enforcement will improve slowly in the EU](https://doi.org/10.1108/oxan-db274294) | Emerald expert briefings | problem_identifying | 0 |

![Most-cited new work](../img/gdpr-fines-radar-new-work.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/gdpr-fines-radar-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 3.5 | 3.0 | 1.0 | 0.0 |
| Measured comparison | 3.0 | 3.5 | 2.0 | 0.0 |
| Visualisation from counted data | 3.0 | 3.0 | 1.0 | 0.0 |
| Exploration and drill-down | 2.0 | 2.0 | 1.5 | 1.5 |
| Data export with provenance | 0.0 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 3.0 | 4.0 | 1.0 | 1.0 |
| Traceable references | 3.0 | 3.0 | 1.0 | 0.5 |
| Accuracy against the corpus | 3.0 | 4.0 | 3.0 | 3.5 |
| Calibration and limits | 4.0 | 3.5 | 3.5 | 3.0 |
| Decision-grade verdict | 4.0 | 3.5 | 2.0 | 2.0 |
| Facet coverage | 4.0 | 4.0 | 1.5 | 1.0 |
| **Score /100** | 60.0 | **68.9** | 33.9 | 24.5 |

**Claude Opus judge:** A and B both grounded their answers in the same 10-paper radar list and correctly declined to read it as a field trend. B's fully traced, provenance-tagged export gave it the edge. A had stronger placed limits, but it carried untraced coverage figures and an export that contradicts its prose. C and D answered from memory: C honestly said almost nothing, and D substituted estimated fine totals for the research question that was asked.

**GPT judge:** D is the strongest decision aid: it answers what the recent selected papers cover, quantifies a carefully bounded comparison, and preserves the distinction between a radar shortlist and field-wide trends. A is also careful but has weaker reproducibility and export, while B and C lack traced evidence; C’s estimated fine series is especially easy to mistake for a measured trend.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/gdpr-fines-radar/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/gdpr-fines-radar.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is new in research on GDPR enforcement and fines?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.radar" \
  -H 'content-type: application/json' \
  -d '{"topic": "gdpr enforcement", "since_year": 2022}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_radar']["fn"](**{'topic': 'gdpr enforcement', 'since_year': 2022})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
