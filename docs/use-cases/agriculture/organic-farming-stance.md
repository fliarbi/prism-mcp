# Organic farming research framing

[Agriculture & food security](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Stance trend for a sustainability review.  
> **Why it is hard.** Yield-gap critiques vs environmental-benefit findings.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [organic-farming-stance.json](../../examples/organic-farming-stance.json).

**The question:**

> Is research on organic farming becoming more favourable?

## What Prism returned

**19,729 papers** matched (phrases: organic farming, organic agriculture, sustainable agriculture, organic crop production, organic farming systems).

![Framing by year](../img/organic-farming-stance-stance.svg)

![Papers by orientation](../img/organic-farming-stance-orientation.svg)

| Year | Papers | Positive | Contested |
| ---: | ---: | ---: | ---: |
| 2017 | 2,001 | 7.7% | 12.7% |
| 2018 | 2,439 | 8.1% | 12.7% |
| 2019 | 2,400 | 18.8% | 13.2% |
| 2020 | 3,089 | 9.8% | 26.6% |
| 2021 | 3,717 | 23.4% | 24.5% |
| 2022 | 3,842 | 23.7% | 25.1% |
| 2023 | 4,991 | 12.9% | 24.6% |
| 2024 | 6,540 | 16.1% | 17.6% |
| 2025 | 10,245 | 18.8% | 19.2% |

### Most recent promising studies (13,767 matched)

| Year | Paper | Venue | Contribution |
| ---: | --- | --- | --- |
| 2025 | [The Role of Ethnoecological Knowledge, Climate Adaptation Strategies, and Farmer Innovation in Achieving Sustainable Agr](https://doi.org/10.58812/wsnt.v3i04.2473) | West Science Nature and Technology | empirical |
| 2025 | [Kajian Kelayakan Usahatani Kopi Organik dan Anorganik berdasarkan Aspek Finansial di Desa Kayumas Kabupaten Situbondo, I](https://doi.org/10.37149/jimdp.v10i6.2376) | Jurnal Ilmiah Membangun Desa dan Pertanian | empirical |
| 2025 | [Pertanian Organik Sebagai Upaya Peningkatan Perekonomian Masyarakat di Lembang Basokan](https://doi.org/10.62951/svargapena.v2i4.185) | Svarga Pena Jurnal Pengabdian Kepada Masyarakat | empirical |
| 2025 | [Fruit and Vegetable Wastes: Review of Nutritional Composition, Antimicrobial Potential, and Sustainable Applications in ](https://doi.org/10.23917/pharmacon.v22i2.13799) | Pharmacon Jurnal Farmasi Indonesia | review |
| 2025 | [Plant Growth Promoting Bacteria: Promising Avenues for Sustainable Agriculture and Climate Change Resilience](https://doi.org/10.5281/zenodo.18411208) | Zenodo (CERN European Organization for Nuclear Research) | review |
| 2025 | [Climate Resilience Crop Varieties and Adoptation Strategies](https://doi.org/10.5281/zenodo.18411370) | Zenodo (CERN European Organization for Nuclear Research) | position |
| 2025 | [Application of pH and TDS Sensors to the Growth of Red Lettuce (Lactuca sativa var. crispa) in a Hydroponic System](https://doi.org/10.29303/jbt.v25i4b.10859) | JURNAL BIOLOGI TROPIS | empirical |
| 2025 | [CRICKET POWDER (ACHETA DOMESTICUS): A VERSATILE AND SUSTAINABLE PROTEIN SOURCE IN FOOD APPLICATIONS](https://doi.org/10.11118/actaun.2025.021) | Acta Universitatis Agriculturae et Silviculturae Mendelianae Brunensis | review |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/organic-farming-stance-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.5 | 1.0 | 0.0 |
| Measured comparison | 5.0 | 4.0 | 2.0 | 0.0 |
| Visualisation from counted data | 4.5 | 4.0 | 1.0 | 0.0 |
| Exploration and drill-down | 3.0 | 3.0 | 2.0 | 1.0 |
| Data export with provenance | 3.0 | 3.5 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 4.0 | 1.0 | 0.5 |
| Traceable references | 3.0 | 2.5 | 3.0 | 0.0 |
| Accuracy against the corpus | 4.0 | 4.0 | 4.0 | 3.0 |
| Calibration and limits | 4.0 | 4.0 | 3.5 | 3.0 |
| Decision-grade verdict | 3.0 | 3.5 | 3.0 | 1.5 |
| Facet coverage | 4.0 | 3.5 | 1.5 | 0.5 |
| **Score /100** | **78.8** | 74.6 | 42.6 | 18.8 |

**Claude Opus judge:** A was the only deliverable that compared positive and contested framing shares on one scale. It showed that both rose and that the gap nearly closed, and it flagged that the 'sustainable agriculture' phrase and off-topic rows contaminate the corpus. C used the same data but leaned on raw counts that mostly reflect volume growth. B offered accurate memory-based yield-gap context with real DOIs but no measurement, and D offered nothing.

**GPT judge:** C is the strongest decision aid: it shows the traced annual framing series, compares positive and contested patterns, and warns that framing is not evidence quality. D offers a more polished comparison but misstates the phrase matching; A and B appropriately limit claims but cannot measure the trend.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/organic-farming-stance/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/organic-farming-stance.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Is research on organic farming becoming more favourable?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.stance_trends" \
  -H 'content-type: application/json' \
  -d '{"term": "organic farming"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['stance_trends']["fn"](**{'term': 'organic farming'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `stance_trends` (52.0 s) → `browse_research` (127.9 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
