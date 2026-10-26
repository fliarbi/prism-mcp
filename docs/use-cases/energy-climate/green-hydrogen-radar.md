# Green hydrogen research radar

[Energy & climate](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Technology momentum for a transition fund.  
> **Why it is hard.** Electrolyser cost papers vs policy papers move differently.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [green-hydrogen-radar.json](../../examples/green-hydrogen-radar.json).

**The question:**

> What is new in green hydrogen research since 2022?

## What Prism returned

### Direction of travel

| Series | Window | First → last | Peak | Late third vs early third | Direction |
| --- | --- | --- | --- | ---: | --- |
| Research papers (typed corpus) | 2017 – 2025 | 1,857 → 5,227 | 6,236 (2024) | 2.46× | rising |
| News articles | 2019-01-01 – 2026-05-01 | 2 → 76 | 317 (2025-05-01) | 3.43× | rising |

**Framing shift since 2022:** cautionary share 6.5% before vs 10.1% since (+3.6 points): *framing is broadly unchanged*.

### New work since 2022

*the most-cited typed papers published since the start year whose title carries one of the subject's own phrases*

| Year | Paper | Venue | Orientation | Cited by |
| ---: | --- | --- | --- | ---: |
| 2022 | [An overview of water electrolysis technologies for green hydrogen production](https://doi.org/10.1016/j.egyr.2022.10.127) | Energy Reports | problem_identifying | 1,277 |
| 2022 | [Influence of renewable energy power fluctuations on water electrolysis for green hydrogen production](https://doi.org/10.1016/j.ijhydene.2022.11.018) | International Journal of Hydrogen Energy | problem_identifying | 449 |
| 2022 | [A Critical Review of Renewable Hydrogen Production Methods: Factors Affecting Their Scale-Up and Its Role in Future Ener](https://doi.org/10.3390/membranes12020173) | Membranes | problem_identifying | 345 |
| 2022 | [A high-performance capillary-fed electrolysis cell promises more cost-competitive renewable hydrogen](https://doi.org/10.1038/s41467-022-28953-x) | Nature Communications | breakthrough | 318 |
| 2024 | [Integration of renewable energy sources in tandem with electrolysis: A technology review for green hydrogen production](https://doi.org/10.1016/j.ijhydene.2024.06.342) | International Journal of Hydrogen Energy | promising | 265 |
| 2024 | [Alkaline Water Electrolysis for Green Hydrogen Production](https://doi.org/10.1021/acs.accounts.3c00709) | Accounts of Chemical Research | problem_identifying | 239 |
| 2022 | [Prospects and challenges for green hydrogen production and utilization in the Philippines](https://doi.org/10.1016/j.ijhydene.2022.04.101) | International Journal of Hydrogen Energy | problem_identifying | 158 |
| 2023 | [Economic, social, and regulatory challenges of green hydrogen production and utilization in the US: A review](https://doi.org/10.1016/j.ijhydene.2023.08.157) | International Journal of Hydrogen Energy | problem_identifying | 157 |
| 2023 | [Identifying a Universal Activity Descriptor and a Unifying Mechanism Concept on Perovskite Oxides for Green Hydrogen Pro](https://doi.org/10.1002/adma.202305074) | Advanced Materials | breakthrough | 156 |
| 2024 | [High Temperature Solid Oxide Electrolysis for Green Hydrogen Production](https://doi.org/10.1021/acs.chemrev.3c00795) | Chemical Reviews | problem_identifying | 140 |

![Most-cited new work](../img/green-hydrogen-radar-new-work.svg)

### What the research covers and the news does not

| Research topic | Papers | News articles |
| --- | ---: | ---: |
| Hydrogen Storage and Materials | 26,310 | 0 |
| Ammonia Synthesis and Nitrogen Reduction | 5,662 | 0 |
| Magnesium Alloys: Properties and Applications | 2,941 | 0 |
| Rare-earth and actinide compounds | 2,347 | 0 |
| Nuclear Materials and Properties | 1,480 | 0 |
| Boron and Carbon Nanomaterials Research | 1,368 | 0 |
| Aluminum Alloys Composites Properties | 1,273 | 0 |
| Fuel Cells and Related Materials | 1,213 | 0 |

![Under-covered topics](../img/green-hydrogen-radar-under-covered.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/green-hydrogen-radar-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 3.0 | 1.0 | 0.0 |
| Measured comparison | 2.0 | 3.5 | 1.5 | 0.0 |
| Visualisation from counted data | 4.0 | 3.0 | 1.0 | 0.0 |
| Exploration and drill-down | 3.0 | 1.5 | 1.0 | 1.0 |
| Data export with provenance | 2.5 | 2.5 | 1.0 | 1.0 |
| Reproducibility | 4.0 | 4.0 | 0.0 | 0.0 |
| Traceable references | 3.0 | 3.5 | 1.0 | 1.5 |
| Accuracy against the corpus | 2.5 | 3.0 | 2.5 | 2.5 |
| Calibration and limits | 3.5 | 4.0 | 2.5 | 3.0 |
| Decision-grade verdict | 3.0 | 3.5 | 2.5 | 2.0 |
| Facet coverage | 4.0 | 3.0 | 1.0 | 1.0 |
| **Score /100** | **66.0** | 63.8 | 27.9 | 22.2 |

**Claude Opus judge:** A turned the single radar call into a traced trend, framing and new-work picture. It quantified the change, placed limits next to the numbers and listed 10 resolvable DOIs, with only a minor counting slip. C used the same data more thinly and misread the tool's caveats. B and D were honest about having no measurements, and only D engaged the policy-versus-technology split the question raises.

**GPT judge:** A is the strongest decision aid: it gives a cautious, reproducible research-volume trend and useful new-work examples while distinguishing indexed attention from technical or commercial progress. B is broader, but its miscounted paper list and invalid cross-window growth comparison weaken its conclusions; C and D lack grounded measurements.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/green-hydrogen-radar/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/green-hydrogen-radar.pdf)

## Live MCP session

Here each model was given only the question and a live connection to the Prism MCP server, and chose its own calls.

**Claude** (claude-sonnet, 330.1 s) called 2 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `research_radar` | `{"topic": "green hydrogen", "since_year": 2022}` | ok · 4,982 chars |
| 2 | `stance_trends` | `{"term": "green hydrogen", "since": 2017}` | ok · 5,175 chars |

<details><summary>Claude's answer</summary>

**Direct answer:** Green hydrogen research has grown fast since 2022. Its framing is still mostly optimistic, but more of the work now flags problems. The new papers are mainly applied: techno-economic studies, system integration and certification governance.

**What the data shows** (Prism typed corpus, 2017–2025; 2026 is incomplete)

- **Volume:** The broad hydrogen-related research set (radar scope) went from 1,857 papers in 2017 to 5,227 in 2025. It peaked at 6,236 in 2024, and the compound annual growth rate was 13.8%.
- **Narrow "green hydrogen" titles and keywords:** Papers per year were 322 in 2022, 637 in 2023, 1,088 in 2024 and 1,297 in 2025. That is about 4× in three years, from a small base.
- **Framing:**
  - "Promising" papers were the largest share, at 555 of 1,297 in 2025.
  - "Breakthrough" papers rose from 23 in 2022 to 195 in 2025.
  - "Problem-identifying" and "cautionary" papers also rose, to 206 and 66 in 2025.
  - The contested share (cautionary, critical and problem-identifying) was 34% in 2022 and 22% in 2025. It averaged 15% in the early third of the window and 23.9% in the late third. The radar's wider hydrogen scope shows a cautionary share of 6.1% rising to 8.7%, which it reads as "broadly unchanged".
- **Examples of 2025 work:**
  - Tasmanian renewable-hydrogen certification governance.
  - Geothermal-integrated green hydrogen in Indonesia, a techno-economic analysis.
  - A solar-powered hydrogen and AC power system with digital control.
- **News:** Coverage was 76 articles in the latest month. It peaked at 317 in May 2025. Coverage across the whole period is up 3.4× from the early third to the late third. News ingest thins after May 2026, so recent months are undercounted.

**Interpretation (mine, not measured)**

- The growth looks like a shift from materials chemistry toward deployment questions: costs, grid integration, certification and regional feasibility.
- The cautionary and problem-identifying share has stayed high even as volume rose. I read that as the field becoming more realistic about economics and scale. I would not read it as the technology losing credibility.
- Orientation labels describe how a paper frames its own findings. They don't show whether the findings are true.
- The radar's two scopes disagree on how much the framing has changed. I would treat that shift as modest and sensitive to how the topic is defined.

**Limits:** These are counts of papers. They don't measure how much hydrogen was produced, what it cost, or what was deployed.

</details>

**ChatGPT** (gpt-6-luna, 377.0 s) called 1 Prism tool:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `research_radar` | `{"topic": "green hydrogen", "since_year": 2022}` | ok · 11,048 chars |

<details><summary>ChatGPT's answer</summary>

**Green hydrogen research is expanding and broadening—from production systems into certification and governance.**

**What Prism’s data shows:** The research series rose from 1,857 papers in 2017 to 5,227 in 2025, peaking at 6,236 in 2024 (2017–2025). Its recent-work list includes 2025 studies on renewable-hydrogen certification in Tasmania ([DOI](https://doi.org/10.1080/1523908x.2025.2608983)), geothermal integration and techno-economic analysis in Indonesia ([DOI](https://doi.org/10.47760/cognizance.2025.v05i12.026)), and an integrated solar system for hydrogen production ([DOI](https://doi.org/10.1016/j.sciaf.2025.e03160)). The share of papers labeled cautionary was 9.1% in the recent window versus 7.1% earlier, a 2 percentage-point increase; Prism characterizes the overall framing as broadly unchanged.

**My interpretation:** The field’s growth is bringing more attention to how hydrogen is certified, integrated with energy systems, and assessed economically—not just how it is produced. The cautionary uptick merits watching, but it does not by itself show that the technology’s prospects have worsened.

</details>

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is new in green hydrogen research since 2022?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.radar" \
  -H 'content-type: application/json' \
  -d '{"topic": "green hydrogen", "since_year": 2022}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_radar']["fn"](**{'topic': 'green hydrogen', 'since_year': 2022})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
