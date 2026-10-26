# Vaccine hesitancy research trend

[Public health & epidemiology](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A measured multi-year series with a forward range.  
> **Why it is hard.** Post-COVID research spike; a naive extrapolation overstates the trend.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [vaccine-hesitancy-trend.json](../../examples/vaccine-hesitancy-trend.json).

**The question:**

> How has research on vaccine hesitancy grown, and what range does it project for the next three years?

## What Prism returned

![History and scenarios](../img/vaccine-hesitancy-trend-history.svg)

| Year | Records | Kind |
| ---: | ---: | --- |
| 2017 | 70 | observed |
| 2018 | 84 | observed |
| 2019 | 137 | observed |
| 2020 | 254 | observed |
| 2021 | 1,235 | observed |
| 2022 | 1,458 | observed |
| 2023 | 1,168 | observed |
| 2024 | 897 | observed |
| 2025 | 776 | observed |
| 2026 | 776 (range 486–1,066) | scenario |
| 2027 | 776 (range 196–1,356) | scenario |
| 2028 | 776 (range 0–1,646) | scenario |

**Backtest:** expanding-window, one-step ahead; mean absolute error {"no_change": 226.25, "linear_drift": 332.24821428571425}. The selected baseline is the one that forecast past years best, not the one that looks most exciting.

**Limitations Prism attaches:**
- Record counts, not deduplicated studies, adoption, sentiment, or causal effects.
- Not normalized for changing corpus size or enrichment coverage.
- Year bounds are ingestion-safe defaults, not proof of complete coverage.
- Extrapolates the declared count series, not real-world future events.
- Sensitivity ranges use worst one-step backtest error times horizon; NOT confidence intervals.
- Model selection uses these same folds; no independent validation or multi-step calibration.
- Structural breaks, seasonality, policy shifts and changing data coverage are not modeled.

<details><summary>The exact query behind the series</summary>

```sql
SELECT publication_year, count() FROM Prism research index PREWHERE publication_year BETWEEN 2017 AND 2025 WHERE (multiSearchAnyCaseInsensitive(title, ['vaccine hesitancy'])) GROUP BY publication_year ORDER BY publication_year
```
</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/vaccine-hesitancy-trend-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.0 | 4.0 | 1.5 | 0.0 |
| Visualisation from counted data | 4.0 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 3.5 | 2.5 | 1.0 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.0 | 0.0 | 1.0 |
| Accuracy against the corpus | 3.5 | 3.5 | 2.0 | 4.0 |
| Calibration and limits | 4.0 | 3.0 | 3.5 | 3.0 |
| Decision-grade verdict | 3.5 | 3.5 | 1.5 | 2.0 |
| Facet coverage | 4.0 | 3.5 | 1.0 | 0.5 |
| **Score /100** | **76.0** | 69.9 | 26.4 | 25.7 |

**Claude Opus judge:** B and D both reproduced the measured rise to the 2022 peak and the decline to 776, along with the flat no-change projection and its widening bounds. B went further: it charted the central scenario, exported the scenario rows, and used a pre-pandemic baseline. It also explained why naive linear extrapolation fails (worse MAE, and no-change over-predicting a falling series), which is exactly the trap this question sets. A honestly declined to answer, while C offered memory estimates on a different scale with an internally inconsistent range.

**GPT judge:** D is the strongest decision aid: it traces the full observed series, gives the three-year central path and sensitivity bounds, compares periods on one scale, and states the limits and follow-up calls. C is careful and largely accurate but omits the forecast bounds from its chart and lacks a second export; D loses ground by overstating coverage and framing a mature plateau as a stronger conclusion than the series alone warrants.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/vaccine-hesitancy-trend/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/vaccine-hesitancy-trend.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How has research on vaccine hesitancy grown, and what range does it project for the next three years?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/analysis.history" \
  -H 'content-type: application/json' \
  -d '{"subject_phrases": ["vaccine hesitancy"], "outcome_phrases": null}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['historical_analysis']["fn"](**{'subject_phrases': ['vaccine hesitancy'], 'outcome_phrases': None})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `historical_analysis` (14.8 s) → `trend_scenarios` (0.0 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
