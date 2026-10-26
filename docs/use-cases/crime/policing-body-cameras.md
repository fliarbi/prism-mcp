# Do body cameras reduce police use of force?

[Crime & public safety](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Trial evidence for a policing intervention.  
> **Why it is hard.** Early RCTs said yes; the large replication said no effect. Both must appear.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [policing-body-cameras.json](../../examples/policing-body-cameras.json).

**The question:**

> Does police body-worn camera use reduce use of force and complaints?

## What Prism returned

### How much evidence exists

| Corpus | Records on both sides of the claim | Window |
| --- | ---: | --- |
| Typed research papers | 26,397 | 2017-2025 |
| Papers with abstracts | 47 | 1990-2025 |
| the health literature index records | 0 | 1990-2025 |
| News articles | 0 | 2019-01-01..2026-06-01 |
| Patents | 0 | 2005-2024 |
| arXiv preprints | 0 | 2005-2025 |

![Evidence volume by corpus](../img/policing-body-cameras-volumes.svg)

![Framing of the literature](../img/policing-body-cameras-sides.svg)

*orientation is a label on the paper's own framing, not a verdict on the claim; this corpus starts in 2017* Contested share: **46.3%**.

### The strongest evidence, read

Prism read 1 sources: **0 support, 1 contradict, 0 qualify** (tier-weighted {"supports": 0, "contradicts": 3, "qualifies": 0}). Each quote is copied from the abstract and verified against it; 0 candidate quotes failed that check and were dropped.

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2019 | [A randomized control trial evaluating the effects of police body-worn cameras](https://doi.org/10.1073/pnas.1814773116)<br><sub>Proceedings of the National Academy of Sciences</sub> | article | contradicts | we show that BWCs have very small and statistically insignificant effects on police use of force |
| 2017 | [Community Perceptions of Police Body-Worn Cameras](https://doi.org/10.1177/0093854816688037)<br><sub>Criminal Justice and Behavior</sub> | article | unrelated | recent research suggests positive impacts of BWCs on reducing police use-of-force and citizen complaints |
| 2015 | [Police Body-Worn Cameras: Perceptions of Law Enforcement Leadership](https://doi.org/10.1007/s12103-015-9316-4)<br><sub>American Journal of Criminal Justice</sub> | article | unrelated | command staff believe BWCs will impact police officers’ decisions to use force in encounters with citizens and police will be more reluctant to use necessary force |
| 2018 | [Police Body-Worn Cameras: Effects on Officers’ Burnout and Perceived Organizational Support](https://doi.org/10.1177/1098611118783987)<br><sub>Police Quarterly</sub> | article | unrelated | We find BWCs increase police officer burnout, and this effect is statistically different from zero. |
| 2022 | [The Achilles Heel of Police Body-Worn Cameras: Understanding the Factors That Influence Variation in Body-Worn Camera Ac](https://doi.org/10.1080/07418825.2022.2071325)<br><sub>Justice Quarterly</sub> | article | unrelated | Our analysis suggests that a wide variety of individual, situational, organizational, and neighborhood factors are related to an officer’s decision to activate their camera |
| 2021 | [The Influence of Defendant Race/Ethnicity and Police Body-Worn Cameras on Traffic Case Processing](https://doi.org/10.1177/21533687211004696)<br><sub>Race and Justice</sub> | article | unrelated | BWCs did significantly reduce the likelihood of a guilty plea for Black and White defendants |
| 2022 | [Testing the Evidentiary Value of Police Body-Worn Cameras in Misdemeanor Court](https://doi.org/10.1177/00111287221120185)<br><sub>Crime & Delinquency</sub> | article | unrelated | BWCs did not affect case flow but did affect processing and outcomes for most cases. |
| 2025 | [Automation and artificial intelligence in police body-worn cameras: Experimental evidence of impact on perceptions of fa](https://doi.org/10.1016/j.jcrimjus.2025.102373)<br><sub>Journal of Criminal Justice</sub> | article | unrelated | Automatic BWC activation and artificial intelligence auditing of footage cause declines in perceived fairness of monitoring. |

![Study designs](../img/policing-body-cameras-tiers.svg)

### What disagrees

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2019 | [A randomized control trial evaluating the effects of police body-worn cameras](https://doi.org/10.1073/pnas.1814773116)<br><sub>Proceedings of the National Academy of Sciences</sub> | article | contradicts | we show that BWCs have very small and statistically insignificant effects on police use of force |

> No document read directly supports the claim as written. 1 contradict it and 0 require qualifications; revise or withhold the claim.

### Numbers you can quote

| Figure | Measures | Population | Source |
| --- | --- | --- | --- |
| **61% reduced** | overall assaults | participating police departments | [Paradoxical effects of self-awareness of being observed: testing the effect of police body-worn cameras on assaults and ](https://doi.org/10.1007/s11292-017-9311-5) 2017 |
| **37% higher odds of assault** | odds of assault | treatment shifts vs control conditions | [Paradoxical effects of self-awareness of being observed: testing the effect of police body-worn cameras on assaults and ](https://doi.org/10.1007/s11292-017-9311-5) 2017 |
| **OR = 2.565; 95% CI 1.792, 3.672** | odds ratio for backfiring treatment effect | low discretion sites | [Paradoxical effects of self-awareness of being observed: testing the effect of police body-worn cameras on assaults and ](https://doi.org/10.1007/s11292-017-9311-5) 2017 |
| **394 assaults per 1000 arrests** | assaults per 1000 arrests | treatment shifts | [Paradoxical effects of self-awareness of being observed: testing the effect of police body-worn cameras on assaults and ](https://doi.org/10.1007/s11292-017-9311-5) 2017 |
| **284 assaults per 1000 arrests** | assaults per 1000 arrests | control shifts | [Paradoxical effects of self-awareness of being observed: testing the effect of police body-worn cameras on assaults and ](https://doi.org/10.1007/s11292-017-9311-5) 2017 |

![Research output per year](../img/policing-body-cameras-research-series.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/policing-body-cameras-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.5 | 1.0 | 1.5 |
| Measured comparison | 4.5 | 4.5 | 2.0 | 1.0 |
| Visualisation from counted data | 4.0 | 4.0 | 1.0 | 1.0 |
| Exploration and drill-down | 4.0 | 2.5 | 1.5 | 1.5 |
| Data export with provenance | 2.5 | 3.0 | 1.0 | 1.0 |
| Reproducibility | 4.0 | 4.0 | 1.0 | 0.0 |
| Traceable references | 4.5 | 4.5 | 3.5 | 0.0 |
| Accuracy against the corpus | 4.5 | 3.5 | 2.0 | 1.0 |
| Calibration and limits | 5.0 | 4.0 | 4.0 | 3.0 |
| Decision-grade verdict | 4.0 | 4.0 | 3.0 | 3.0 |
| Facet coverage | 3.5 | 3.0 | 1.5 | 1.5 |
| **Score /100** | **82.3** | 76.4 | 38.7 | 26.3 |

**Claude Opus judge:** A and C both grounded every number in the recorded calls. A went further: it flagged that the 26,397-paper lane is a broad topic with only 52 BWC-titled papers, gave low confidence because just one trial was read, and placed limits next to the numbers. B and D were the only deliverables to present both the early-RCT and replication sides, but they did so from memory. B relied on a fabricated DOI, and D misstated the discretion finding against the record. A decision-maker can trust A's narrow but honest answer: no traceable evidence that BWCs reduce force, and complaints unmeasured.

**GPT judge:** B best supports a decision with a fully traced, censored research-volume series, a correctly bounded comparison, and the clearest distinction between force and assaults on officers. D is similarly careful and more concise, but gives less usable drilldown and facet coverage; B still overstates what the retrieved evidence establishes about complaints.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/policing-body-cameras/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/policing-body-cameras.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Does police body-worn camera use reduce use of force and complaints?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.evidence" \
  -H 'content-type: application/json' \
  -d '{"claim": "Police body-worn cameras reduce use of force", "limit": 10}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['find_evidence']["fn"](**{'claim': 'Police body-worn cameras reduce use of force', 'limit': 10})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `find_evidence` (85.1 s) → `find_counter_evidence` (13.4 s) → `find_statistics` (5.5 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
