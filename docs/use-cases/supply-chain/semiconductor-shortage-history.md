# Chip shortage research trend

[Supply chain & trade](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Measured series with a forward range.  
> **Why it is hard.** 2021 shortage spike: a naive trend line overshoots.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [semiconductor-shortage-history.json](../../examples/semiconductor-shortage-history.json).

**The question:**

> How did research on semiconductor supply chains grow and what range follows?

## What Prism returned

![History and scenarios](../img/semiconductor-shortage-history-history.svg)

| Year | Records | Kind |
| ---: | ---: | --- |
| 2017 | 10 | observed |
| 2018 | 10 | observed |
| 2019 | 15 | observed |
| 2020 | 5 | observed |
| 2021 | 14 | observed |
| 2022 | 16 | observed |
| 2023 | 25 | observed |
| 2024 | 37 | observed |
| 2025 | 52 | observed |
| 2026 | 57.2 (range 46.1–68.4) | scenario |
| 2027 | 62.5 (range 40.2–84.8) | scenario |
| 2028 | 67.8 (range 34.3–101.2) | scenario |

**Backtest:** expanding-window, one-step ahead; mean absolute error {"no_change": 9.5, "linear_drift": 7.360714285714287}. The selected baseline is the one that forecast past years best, not the one that looks most exciting.

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
SELECT publication_year, count() FROM Prism research index PREWHERE publication_year BETWEEN 2017 AND 2025 WHERE (multiSearchAnyCaseInsensitive(title, ['semiconductor supply chain'])) GROUP BY publication_year ORDER BY publication_year
```
</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/semiconductor-shortage-history-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 1.5 | 0.0 |
| Visualisation from counted data | 4.0 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 2.0 | 1.5 | 0.5 |
| Data export with provenance | 4.5 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 4.0 | 0.0 | 0.5 |
| Accuracy against the corpus | 4.0 | 4.0 | 3.0 | 4.0 |
| Calibration and limits | 4.0 | 3.0 | 3.0 | 2.5 |
| Decision-grade verdict | 4.0 | 3.0 | 2.0 | 2.0 |
| Facet coverage | 4.5 | 4.0 | 1.0 | 1.0 |
| **Score /100** | **86.0** | 70.5 | 30.2 | 23.4 |

**Claude Opus judge:** B and A both traced the same 10→52 series and the scenario output. B went further: it gave an exact CAGR and year-on-year growth, an early-vs-late split, and a quantified baseline-vs-drift backtest showing that every fold under-predicted. Its verdict carried a usable 2026 range and a falsifiable trigger. C refused outright, and D offered only labelled memory estimates whose shape conflicts with the record.

**GPT judge:** A is the strongest decision deliverable: it connects the traced annual rise to conditional scenario bounds, provides reproducible exports, and names useful follow-up questions. D is a concise, largely accurate account but leaves out scenario values and several decision-relevant facets; B is careful but does not answer the measured question, while C's explicitly labelled estimates are not decision-grade evidence.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/semiconductor-shortage-history/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/semiconductor-shortage-history.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How did research on semiconductor supply chains grow and what range follows?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/analysis.history" \
  -H 'content-type: application/json' \
  -d '{"subject_phrases": ["semiconductor supply chain"], "outcome_phrases": null, "query_seconds": 30}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['historical_analysis']["fn"](**{'subject_phrases': ['semiconductor supply chain'], 'outcome_phrases': None, 'query_seconds': 30})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `historical_analysis` (1.2 s) → `trend_scenarios` (0.0 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
