# Does the death penalty deter crime?

[Legal & compliance](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Both sides of a long-running empirical debate.  
> **Why it is hard.** Econometric claims of deterrence are heavily contested.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [death-penalty-deterrence.json](../../examples/death-penalty-deterrence.json).

**The question:**

> Does the death penalty deter murder? What does the evidence say?

## What Prism returned

### How much evidence exists

| Corpus | Records on both sides of the claim | Window |
| --- | ---: | --- |
| Typed research papers | 334 | 2017-2025 |
| Papers with abstracts | 235 | 1990-2025 |
| the health literature index records | 0 | 1990-2025 |
| News articles | 8 | 2019-01-01..2026-06-01 |
| Patents | 0 | 2005-2024 |
| arXiv preprints | 0 | 2005-2025 |

![Evidence volume by corpus](../img/death-penalty-deterrence-volumes.svg)

![Framing of the literature](../img/death-penalty-deterrence-sides.svg)

*orientation is a label on the paper's own framing, not a verdict on the claim; this corpus starts in 2017* Contested share: **59%**.

### The strongest evidence, read

Prism read 1 sources: **0 support, 1 contradict, 0 qualify** (tier-weighted {"supports": 0, "contradicts": 3, "qualifies": 0}). Each quote is copied from the abstract and verified against it; 0 candidate quotes failed that check and were dropped.

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2013 | [Facts or Ideology: What Determines the Results of Econometric Estimates of the Deterrence Effect of Death Penalty? A Met](http://ux-tauri.unisg.ch/RePEc/usg/econwp/EWP-1303.pdf)<br><sub>RePEc: Research Papers in Economics</sub> | meta_analysis | unread | the literature on the deterrent effect of capital punishment is overall inconclusive |
| 2022 | [Estimating the effect of death penalty moratoriums on homicide rates using the synthetic control method](https://doi.org/10.1111/1745-9133.12601)<br><sub>Criminology & Public Policy</sub> | article | contradicts | no evidence of a deterrent effect attributable to death penalty statutes was found. |
| 2004 | [A TASTE FOR PUNISHMENT: Black and White Americans' Views on the Death Penalty and the War on Drugs](https://doi.org/10.1017/s1742058x04040081)<br><sub>Du Bois Review Social Science Research on Race</sub> | article | unrelated | Our results, first, confirm large Black-White differences in opinion with Blacks consistently less punitive than Whites. |
| 2008 | [The decline of the death penalty and the discovery of innocence](https://doi.org/10.5860/choice.45-7050)<br><sub>Choice Reviews Online</sub> | article | unrelated | Since 1996, death sentences in America have declined by more than 60 percent, reversing a generation-long trend toward greater acceptance of capital punishment. |
| 2003 | [Why Do White Americans Support the Death Penalty?](https://doi.org/10.1111/1468-2508.t01-2-00006)<br><sub>The Journal of Politics</sub> | article | unrelated | This article explores the roots of white support for capital punishment in the United States. |
| 2002 | [The Political Sociology of the Death Penalty: A Pooled Time-Series Analysis](https://doi.org/10.2307/3088936)<br><sub>American Sociological Review</sub> | article | unrelated | Despite the interest in the death penalty, no statistical studies have isolated the social and political forces that account for the legality of this punishment. |
| 2022 | [Racial Resentment and the Death Penalty](https://doi.org/10.1017/rep.2022.30)<br><sub>The Journal of Race Ethnicity and Politics</sub> | article | unrelated | We explore the annual number of death sentences imposed on black and white offenders within each US state from 1989 through 2017, with particular attention to the impact of aggregate levels of racial resentment. |
| 2021 | [Capital Punishment and the Legacies of Slavery and Lynching in the United States](https://doi.org/10.1177/00027162211016277)<br><sub>The Annals of the American Academy of Political and Social Science</sub> | article | unrelated | Capital punishment in the United States is racialized: those convicted of the murder of Whites are much more likely to receive the death penalty than those convicted for the murder of Blacks. |

![Study designs](../img/death-penalty-deterrence-tiers.svg)

### What disagrees

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2012 | [Deterrence and the Death Penalty](https://doi.org/10.17226/13363)<br><sub>National Academies Press eBooks</sub> | article | contradicts | research to date on the effect of capital punishment on homicide rates is not useful in determining whether the death penalty increases, decreases, or has no effect on these rates. |

> The documents read include both supporting and contradictory findings; explain their differences.

![Research output per year](../img/death-penalty-deterrence-research-series.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/death-penalty-deterrence-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 3.5 | 4.0 | 1.0 | 0.5 |
| Measured comparison | 3.0 | 4.0 | 2.0 | 0.5 |
| Visualisation from counted data | 3.0 | 4.0 | 1.0 | 1.0 |
| Exploration and drill-down | 3.0 | 4.5 | 1.5 | 2.5 |
| Data export with provenance | 3.0 | 4.0 | 1.0 | 1.0 |
| Reproducibility | 4.5 | 4.5 | 1.0 | 1.0 |
| Traceable references | 5.0 | 1.0 | 2.0 | 3.0 |
| Accuracy against the corpus | 3.0 | 3.5 | 2.0 | 4.0 |
| Calibration and limits | 4.5 | 4.0 | 3.5 | 3.0 |
| Decision-grade verdict | 4.0 | 4.5 | 0.0 | 3.5 |
| Facet coverage | 4.0 | 4.5 | 1.5 | 2.0 |
| **Score /100** | 73.8 | **77.7** | 28.3 | 41.2 |

**Claude Opus judge:** B and D both grounded their numbers in the database and reached the same calibrated answer: deterrence is unproven rather than disproven. B wins on fully resolvable, tiered references and on limits that change the reading, notably that the corpus starts in 2017 and so omits the classic deterrence literature. A was honest but empty. C filled gaps with memory figures and inconsistent citations, and put an untagged number in its verdict.

**GPT judge:** A is the strongest decision aid: it gives a clear, bounded answer and makes its retrieved evidence, comparison, and limitations reproducible. C offers the richest grounded detail, but its reading-status claim and incomplete trend coverage weaken trust; B is appropriately cautious but cannot measure the evidence, while D relies heavily on unverifiable estimates.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/death-penalty-deterrence/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/death-penalty-deterrence.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Does the death penalty deter murder? What does the evidence say?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.evidence" \
  -H 'content-type: application/json' \
  -d '{"claim": "The death penalty deters homicide", "limit": 10}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['find_evidence']["fn"](**{'claim': 'The death penalty deters homicide', 'limit': 10})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `find_evidence` (79.8 s) → `find_counter_evidence` (6.4 s) → `find_statistics` (3.6 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
