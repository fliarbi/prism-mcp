# Humanoid robot research trend

[Technology & AI](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A measured series and a forward range.  
> **Why it is hard.** Media hype vs research output; the series is the reality check.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [humanoid-robots-history.json](../../examples/humanoid-robots-history.json).

**The question:**

> How has research on humanoid robots grown, and what range should we expect for the next three years?

## What Prism returned

![History and scenarios](../img/humanoid-robots-history-history.svg)

| Year | Records | Kind |
| ---: | ---: | --- |
| 2017 | 474 | observed |
| 2018 | 554 | observed |
| 2019 | 535 | observed |
| 2020 | 437 | observed |
| 2021 | 447 | observed |
| 2022 | 446 | observed |
| 2023 | 441 | observed |
| 2024 | 589 | observed |
| 2025 | 821 | observed |
| 2026 | 864.4 (range 648.8–1,079.9) | scenario |
| 2027 | 907.8 (range 476.6–1,338.9) | scenario |
| 2028 | 951.1 (range 304.4–1,597.8) | scenario |

**Backtest:** expanding-window, one-step ahead; mean absolute error {"no_change": 96.5, "linear_drift": 93.85535714285714}. The selected baseline is the one that forecast past years best, not the one that looks most exciting.

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
SELECT publication_year, count() FROM Prism research index PREWHERE publication_year BETWEEN 2017 AND 2025 WHERE (multiSearchAnyCaseInsensitive(title, ['humanoid robot'])) GROUP BY publication_year ORDER BY publication_year
```
</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/humanoid-robots-history-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.0 | 1.0 | 1.0 |
| Measured comparison | 4.0 | 4.0 | 1.5 | 0.5 |
| Visualisation from counted data | 4.0 | 4.0 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 2.5 | 1.0 | 1.0 |
| Data export with provenance | 3.0 | 4.5 | 1.0 | 0.0 |
| Reproducibility | 3.0 | 4.0 | 0.0 | 1.0 |
| Accuracy against the corpus | 3.0 | 2.5 | 4.0 | 4.0 |
| Calibration and limits | 4.0 | 4.5 | 3.0 | 4.0 |
| Decision-grade verdict | 0.0 | 3.0 | 0.0 | 2.5 |
| Facet coverage | 4.0 | 4.0 | 1.0 | 0.5 |
| **Score /100** | 40 | **72.9** | 26.8 | 31.6 |

**Claude Opus judge:** B and C both used the measured title-match series (474→821, flat 2020-23, sharp 2024-25 rise) and the scenario range (central 864/908/951, bounds 304–1,598 by 2028). B recomputed every ratio, delta and fold error correctly and read the marginal backtest advantage, though its untagged verdict range zeroes its verdict score. C misreported the 2024→2025 jump as 73% instead of 39%. A offered labelled guesses on a different scale, and D declined to answer, so neither gives a decision-maker a usable range.

**GPT judge:** A is the strongest decision aid: it gives a reproducible historical series and a clearly bounded three-year scenario, while acknowledging the forecast’s weak validation. D offers deeper follow-up work, but its untagged verdict figures and unsupported full-coverage label weaken trust; B is careful but cannot quantify the answer, and C relies on estimates.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/humanoid-robots-history/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/humanoid-robots-history.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How has research on humanoid robots grown, and what range should we expect for the next three years?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/analysis.history" \
  -H 'content-type: application/json' \
  -d '{"subject_phrases": ["humanoid robot"], "outcome_phrases": null}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['historical_analysis']["fn"](**{'subject_phrases': ['humanoid robot'], 'outcome_phrases': None})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `historical_analysis` (18.5 s) → `trend_scenarios` (0.0 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
