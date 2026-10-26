# Coral bleaching research radar

[Environment & disasters](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A radar after the 2023-2024 global bleaching event.  
> **Why it is hard.** The fourth global bleaching event is post-training for many models.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [coral-bleaching-radar.json](../../examples/coral-bleaching-radar.json).

**The question:**

> What has changed in coral bleaching research recently?

## What Prism returned

### Direction of travel

| Series | Window | First → last | Peak | Late third vs early third | Direction |
| --- | --- | --- | --- | ---: | --- |
| Research papers (typed corpus) | 2017 – 2025 | 5,265 → 9,014 | 9,014 (2025) | 1.36× | rising |
| News articles | 2019-01-01 – 2026-05-01 | 4 → 0 | 15 (2024-04-01) | 1.58× | rising |

**Framing shift since 2022:** cautionary share 19.2% before vs 18.6% since (-0.6 points): *framing is broadly unchanged*.

### New work since 2022

*the most-cited typed papers published since the start year whose title carries one of the subject's own phrases*

| Year | Paper | Venue | Orientation | Cited by |
| ---: | --- | --- | --- | ---: |
| 2024 | [2023 Record marine heat waves: coral reef bleaching HotSpot maps reveal global sea surface temperature extremes, coral m](https://doi.org/10.1093/oxfclm/kgae005) | Oxford Open Climate Change | descriptive | 40 |
| 2022 | [Coral Reef Bleaching under Climate Change: Prediction Modeling and Machine Learning](https://doi.org/10.3390/su14106161) | Sustainability | promising | 24 |
| 2023 | [Imagining reef futures after mass coral bleaching events](https://doi.org/10.1016/j.envsci.2023.103625) | Environmental Science & Policy | problem_identifying | 11 |
| 2024 | [Assisted evolution of algal symbionts to enhance coral reef bleaching tolerance: A success story](https://doi.org/10.1111/gcb.17150) | Global Change Biology | problem_identifying | 3 |
| 2024 | [Detection of Coral Reef Bleaching by Multitemporal Sentinel-2 Data Using the PU-Bagging Algorithm: A Feasibility Study a](https://doi.org/10.3390/rs16132473) | Remote Sensing | breakthrough | 3 |
| 2022 | [Coral reef bleaching monitoring based on multitime Landsat-8 remote sensing image series](https://doaj.org/article/fbe4aa94a0d04770af7bd2f117526e9e) | SHILAP Revista de lepidopterología | promising | 2 |
| 2022 | [Symbiodinium IN CORAL REEFS AND ITS ADAPTATION RESPONSES TOWARD CORAL BLEACHING EVENTS: A REVIEW](https://doi.org/10.55230/mabjournal.v51i3.2162) | Malaysian Applied Biology | problem_identifying | 2 |
| 2024 | [Extreme temperatures in 2023 generate mass coral reef bleaching in the western Caribbean, Seaflower Biosphere Reserve](https://doi.org/10.5343/bms.2024.0003) | Bulletin of Marine Science | descriptive | 2 |
| 2024 | [Global Warming Threats to Coral Bleaching Events and Their Impacts on Coastal Ecosystem Sustainability](https://doi.org/10.1051/bioconf/202413402009) | BIO Web of Conferences | problem_identifying | 1 |
| 2023 | [Coral resistance in coral bleaching events in Lombok waters, Indonesia](https://doi.org/10.1088/1755-1315/1163/1/012005) | IOP Conference Series Earth and Environmental Science | descriptive | 1 |

![Most-cited new work](../img/coral-bleaching-radar-new-work.svg)

### What the research covers and the news does not

| Research topic | Papers | News articles |
| --- | ---: | ---: |
| Coral and Marine Ecosystems Studies | 61,984 | 0 |
| Marine and coastal plant biology | 11,575 | 0 |
| Marine Biology and Ecology Research | 7,334 | 0 |
| Coastal and Marine Management | 6,799 | 0 |
| Marine Sponges and Natural Products | 5,303 | 0 |
| Ichthyology and Marine Biology | 5,035 | 0 |
| Marine Bivalve and Aquaculture Studies | 4,188 | 0 |
| Marine animal studies overview | 4,052 | 0 |

![Under-covered topics](../img/coral-bleaching-radar-under-covered.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/coral-bleaching-radar-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 3.0 | 4.0 | 2.0 | 0.5 |
| Visualisation from counted data | 3.5 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 3.0 | 2.0 | 1.5 | 1.0 |
| Data export with provenance | 2.5 | 2.5 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 2.5 | 1.0 | 1.0 |
| Traceable references | 3.0 | 3.5 | 2.0 | 0.0 |
| Accuracy against the corpus | 3.5 | 3.5 | 2.5 | 1.5 |
| Calibration and limits | 4.0 | 4.0 | 3.5 | 3.0 |
| Decision-grade verdict | 3.5 | 4.0 | 3.0 | 2.5 |
| Facet coverage | 4.0 | 4.0 | 1.0 | 1.0 |
| **Score /100** | **69.8** | 68.2 | 36.1 | 20.1 |

**Claude Opus judge:** C and D both grounded their answers in the radar call and read its traps correctly, notably the taxonomy-label zeros. C went further: it exposed the new-work layer with DOIs, compared research and news on early-vs-late thirds, and flagged the incomplete final news month, so it gives a decision-maker the most usable picture. A gave honest, labelled memory about the 4th global event but nothing measured. B fabricated three DOIs.

**GPT judge:** D is strongest for a decision-maker: its core research-volume and framing figures trace to the reference record, and it provides a useful set of recent papers with identifiers. Its main weakness is the claim that news grew faster than research, which compares different windows and lanes; C is more careful about that limitation but has weaker traceability and export coverage.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/coral-bleaching-radar/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/coral-bleaching-radar.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What has changed in coral bleaching research recently?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.radar" \
  -H 'content-type: application/json' \
  -d '{"topic": "coral bleaching", "since_year": 2022}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_radar']["fn"](**{'topic': 'coral bleaching', 'since_year': 2022})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
