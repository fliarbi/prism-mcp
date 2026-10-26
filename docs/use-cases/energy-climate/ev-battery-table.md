# EV battery chemistries table

[Energy & climate](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A spreadsheet of one question across chemistries, export-ready.  
> **Why it is hard.** Each row must carry its own figure and source; null means the corpus does not state one.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below. Saved responses: [ev-battery-table.json](../../examples/ev-battery-table.json).

**The question:**

> For each battery chemistry, what does research say about energy density?

## What Prism returned

Answered **0 of 5** rows. A blank value means the corpus does not state one; it is never filled in.

| Row | Value | Measures | Papers | Top source |
| --- | --- | --- | ---: | --- |
| **lithium iron phosphate** | – |  | – |  |
| **nickel manganese cobalt** | – |  | 3 | [Synthesis and Manipulation of Single-Crystalline Lithium Nickel Manganese Cobalt Oxide Cathodes: A Review of Growth Mech](https://doi.org/10.3389/fchem.2020.00747) |
| **sodium-ion** | – |  | 1 | [Advances in Sodium-Ion Battery Technology: Enhancing Energy Density for Future Applications](https://doi.org/10.54097/62wswy20) |
| **solid-state** | – |  | 0 | [Critical Design Parameters for All-Solid-State Batteries to Achieve 350 Wh/Kg Specific Energy at C/3](https://doi.org/10.1149/ma2025-023590mtgabs) |
| **lithium-sulfur** | – |  | 5 | [Cathode porosity is a missing key parameter to optimize lithium-sulfur battery energy density](https://doi.org/10.1038/s41467-019-12542-6) |

![Papers per row](../img/ev-battery-table-papers.svg)

**Export:** the same rows as CSV, straight from the response:

```csv
row,value,measures,papers,top_source_title,top_source_url
"lithium iron phosphate","","","","",""
"nickel manganese cobalt","","","3","Synthesis and Manipulation of Single-Crystalline Lithium Nickel Manganese Cobalt Oxide Cathodes: A Review of Growth Mechanism","https://doi.org/10.3389/fchem.2020.00747"
"sodium-ion","","","1","Advances in Sodium-Ion Battery Technology: Enhancing Energy Density for Future Applications","https://doi.org/10.54097/62wswy20"
"solid-state","","","0","Critical Design Parameters for All-Solid-State Batteries to Achieve 350 Wh/Kg Specific Energy at C/3","https://doi.org/10.1149/ma2025-023590mtgabs"
"lithium-sulfur","","","5","Cathode porosity is a missing key parameter to optimize lithium-sulfur battery energy density","https://doi.org/10.1038/s41467-019-12542-6"
```

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/ev-battery-table-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured comparison | 1.5 | 0.0 | 1.0 | 1.0 |
| Visualisation from counted data | 0.0 | 0.0 | 1.0 | 0.0 |
| Exploration and drill-down | 1.0 | 1.0 | 1.0 | 1.0 |
| Data export with provenance | 1.0 | 4.5 | 1.0 | 0.0 |
| Reproducibility | 2.0 | 2.0 | 1.0 | 1.0 |
| Traceable references | 3.5 | 3.5 | 0.5 | 0.5 |
| Accuracy against the corpus | 4.0 | 4.0 | 2.5 | 2.5 |
| Calibration and limits | 4.5 | 4.5 | 3.0 | 3.0 |
| Decision-grade verdict | 3.5 | 4.0 | 3.0 | 3.0 |
| Facet coverage | 4.0 | 4.0 | 1.0 | 1.0 |
| **Score /100** | 50.6 | **55.8** | 32.0 | 28.0 |

**Claude Opus judge:** A and B both report the corpus honestly: 0 of 5 rows have a stated energy-density figure. B goes further for a decision-maker. It catches the solid-state 0-papers anomaly and the off-topic LFP news row, quantifies the 146-day staleness, and keeps clearly labelled memory ranges apart from corpus results. C and D answer only from memory with no traceable sources; C also has midpoint slips and a fabricated chart window.

**GPT judge:** A is the strongest decision aid because it preserves nulls row by row, traces them to the supplied corpus response, and explains why those nulls cannot support a ranking. C covers the same rows but weakens its answer with unverified estimates and treats a title target as a relevant figure; B and D are candid about memory estimates but do not deliver grounded findings for the requested rows.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/ev-battery-table/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/ev-battery-table.pdf)

## Live MCP session

Here each model was given only the question and a live connection to the Prism MCP server, and chose its own calls.

**Claude** (claude-sonnet, 1330.9 s) called 5 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `find_statistics` | `{"claim": "lithium-ion battery energy density Wh/kg", "limit": 6, "include_trend": false}` | see payload · 6,741 chars |
| 2 | `find_statistics` | `{"claim": "solid-state lithium metal battery energy density Wh/kg", "limit": 6, "include_trend": false}` | ok · 1,868 chars |
| 3 | `find_statistics` | `{"claim": "sodium-ion battery energy density Wh/kg", "limit": 6, "include_trend": false}` | see payload · 6,575 chars |
| 4 | `find_statistics` | `{"claim": "lithium-sulfur battery energy density Wh/kg", "limit": 6, "include_trend": false}` | see payload · 330 chars |
| 5 | `find_statistics` | `{"claim": "lithium iron phosphate LFP battery energy density Wh/kg", "limit": 6, "include_trend": false}` | see payload · 6,245 chars |

<details><summary>Claude's answer</summary>

**Short answer:** Prism could not give a per-chemistry comparison of energy density. Across five searches, only one verified energy-density figure came back. I won't fill the gaps from memory and present them as findings.

**What the data shows**
- **Lithium-metal, anode-free:** an NCM811/E-Cu pouch cell reached 420 Wh/kg. This is from Advanced Energy Materials (2021), a single paper. It was measured with limited electrolyte (2 g/Ah), and capacity retention was 84%. The paper is in the 2017–2025 typed corpus. Its source is https://doi.org/10.1002/aenm.202003709.
- **Li-ion (Ni-rich), sodium-ion, LFP:** the retrieved abstracts reported capacity (mAh/g), cycling retention or recycling results. None reported energy density in Wh/kg, so Prism's extractor rejected them. One example is a Ni-rich cathode at 226.9 mAh/g (ACS Energy Letters, 2025). Another is a sodium-ion hard-carbon anode at 361 mAh/g (2018).
- **Lithium-sulfur:** the search returned nothing usable. Prism could not resolve a search phrase for it.

**Coverage, as paper counts for 2017–2025**
- Solid-state/lithium-metal: about 327,000 typed papers.
- Li-ion and LFP: each about 327,000 typed papers. These counts match the solid-state figure almost exactly, so they probably reflect a broad battery cluster, not chemistry-specific volume.
- Sodium-ion: about 180,000 typed papers.

**Interpretation (mine, not measured)**
- The literature is large, but the abstracts mostly report materials-level metrics, not cell-level Wh/kg. Cell-level figures are what a chemistry comparison needs.
- The 420 Wh/kg result is a lab pouch cell under favourable conditions. Don't treat it as a typical or commercial value.
- A credible comparison needs cell-level values from review papers or datasheets, with the same basis for each chemistry: cell versus pack, gravimetric versus volumetric. Prism's abstract-level retrieval doesn't supply that.

**Suggested next step:** run `research_packet` or `find_evidence` per chemistry, restricted to review papers. Alternatively, provide specific reviews to read.

</details>

**ChatGPT** (gpt-6-luna, 194.9 s) called 2 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `search_research` | `{"query_text": "battery chemistry energy density gravimetric volumetric lithium ion LFP NMC sodium ion solid state", "limit": 10, "want_recent": true}` | ok · 4,472 chars |
| 2 | `research_brief` | `{"topic": "battery chemistry energy density comparison LFP NMC sodium-ion solid-state lithium-sulfur"}` | ok · 27,368 chars |

<details><summary>ChatGPT's answer</summary>

**Direct answer:** Prism’s research does not provide a comparable set of energy-density figures across battery chemistries. Its retrieved evidence supports a specific 2025 sodium-ion result; it does not establish a ranking across chemistries.

**What the data shows:** A 2025 *Journal of the American Chemical Society* paper reports **385 Wh/L volumetric energy density** for a nano-Bi/hard-carbon composite anode in a sodium-ion battery. That is a specific research result, not a chemistry-wide benchmark. Prism’s broader review of battery energy-density research covers **2017–2025**, but returned no verified key-number comparisons for LFP, NMC, solid-state, or lithium-sulfur chemistries. [Lu et al., 2025](https://doi.org/10.1021/jacs.5c03507); [Prism research brief, 2017–2025](https://doi.org/10.1016/j.egyr.2023.08.069)

**My interpretation:** The evidence here is insufficient to say how much denser one chemistry is than another. The sodium-ion figure is an electrode-level study result, so it should not be treated as a like-for-like cell or pack comparison.

</details>

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
For each battery chemistry, what does research say about energy density?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.table" \
  -H 'content-type: application/json' \
  -d '{"rows": ["lithium iron phosphate", "nickel manganese cobalt", "sodium-ion", "solid-state", "lithium-sulfur"], "question": "battery energy density Wh/kg"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_table']["fn"](**{'rows': ['lithium iron phosphate', 'nickel manganese cobalt', 'sodium-ion', 'solid-state', 'lithium-sulfur'], 'question': 'battery energy density Wh/kg'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
