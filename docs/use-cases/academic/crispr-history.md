# CRISPR research trend

[Academic research & literature review](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Bibliometric series and a forward range.  
> **Why it is hard.** A maturing field: growth is slowing; the range must reflect it.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [crispr-history.json](../../examples/crispr-history.json).

**The question:**

> How has CRISPR research volume grown, and what range should we expect next?

## What Prism returned

![History and scenarios](../img/crispr-history-history.svg)

| Year | Records | Kind |
| ---: | ---: | --- |
| 2017 | 3,072 | observed |
| 2018 | 3,781 | observed |
| 2019 | 4,694 | observed |
| 2020 | 5,101 | observed |
| 2021 | 5,289 | observed |
| 2022 | 5,710 | observed |
| 2023 | 6,314 | observed |
| 2024 | 6,742 | observed |
| 2025 | 7,633 | observed |
| 2026 | 8,203.1 (range 7,836.4–8,569.8) | scenario |
| 2027 | 8,773.2 (range 8,039.8–9,506.7) | scenario |
| 2028 | 9,343.4 (range 8,243.2–10,443.5) | scenario |

**Backtest:** expanding-window, one-step ahead; mean absolute error {"no_change": 586.0, "linear_drift": 172.1744047619045}. The selected baseline is the one that forecast past years best, not the one that looks most exciting.

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
SELECT publication_year, count() FROM Prism research index PREWHERE publication_year BETWEEN 2017 AND 2025 WHERE (multiSearchAnyCaseInsensitive(title, ['crispr'])) GROUP BY publication_year ORDER BY publication_year
```
</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/crispr-history-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 3.5 | 1.0 | 0.0 |
| Measured comparison | 4.0 | 3.5 | 1.5 | 0.0 |
| Visualisation from counted data | 4.5 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 2.0 | 2.0 | 1.0 | 1.0 |
| Data export with provenance | 4.5 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 3.0 | 1.0 | 1.0 |
| Accuracy against the corpus | 4.0 | 3.5 | 2.0 | 3.5 |
| Calibration and limits | 4.5 | 4.0 | 3.0 | 3.0 |
| Decision-grade verdict | 4.0 | 3.5 | 2.5 | 1.5 |
| Facet coverage | 4.0 | 3.0 | 1.0 | 0.5 |
| **Score /100** | **80.9** | 67.5 | 30.8 | 23.0 |

**Claude Opus judge:** A turned the traced series into a decision. It reads the slowdown year by year, gives exact CAGR and backtest deltas, charts central and bounds, and sets a falsifiable 2026 trigger. B traced the same data but never addressed the slowing growth that makes this question hard, and charted only the history. C declined to answer, and D offered internally inconsistent memory estimates on a different scale.

**GPT judge:** D is the strongest decision aid: it combines the traced historical series, quantified growth, backtest comparison, and conditional 2026–2028 range with useful limits. B is careful and reproducible but leaves the scenario comparison and mature-field slowdown less developed; D’s main weakness is overstating coverage and underplaying the 2025 rebound.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/crispr-history/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/crispr-history.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How has CRISPR research volume grown, and what range should we expect next?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/analysis.history" \
  -H 'content-type: application/json' \
  -d '{"subject_phrases": ["crispr"], "outcome_phrases": null, "query_seconds": 30}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['historical_analysis']["fn"](**{'subject_phrases': ['crispr'], 'outcome_phrases': None, 'query_seconds': 30})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `historical_analysis` (1.2 s) → `trend_scenarios` (0.0 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
