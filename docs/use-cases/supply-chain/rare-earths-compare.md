# Rare earths vs lithium vs cobalt

[Supply chain & trade](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Critical-minerals attention for a procurement team.  
> **Why it is hard.** China's 2025 rare-earth export controls spike one series.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · 2024-06-01 to 2026-06-01 (exclusive) · all listed tables passed strict index partition reads and historical row floors. Saved responses: [rare-earths-compare.json](../../examples/rare-earths-compare.json).

**The question:**

> Compare news coverage of rare earths, lithium and cobalt.

## What Prism returned

| Term | Articles | Share | Critical | Growth (late vs early) | Negative-to-positive | vs all news |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **rare earth** | 21,173 | 24.6% | 15,483 | 4.07× (rising) | 0.57 | 0.98× |
| **lithium** | 52,522 | 61% | 35,622 | 0.91× (flat) | 0.21 | 0.36× |
| **cobalt** | 12,341 | 14.3% | 7,589 | 0.99× (flat) | 0.2 | 0.34× |

![Comparison over time](../img/rare-earths-compare-compare.svg)

![Total coverage](../img/rare-earths-compare-share.svg)

> more coverage is attention, not importance, and a term that is also a common word will over-count — check each term's own volume against its sources panel

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/rare-earths-compare-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 3.5 | 3.0 | 0.5 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 1.0 | 0.0 |
| Visualisation from counted data | 3.0 | 3.5 | 0.0 | 0.0 |
| Exploration and drill-down | 3.5 | 2.0 | 1.0 | 1.0 |
| Data export with provenance | 2.0 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.0 | 0.0 | 1.0 |
| Accuracy against the corpus | 1.5 | 2.5 | 3.5 | 3.5 |
| Calibration and limits | 3.5 | 3.5 | 4.0 | 2.5 |
| Decision-grade verdict | 3.5 | 3.0 | 3.0 | 1.5 |
| Facet coverage | 3.5 | 3.0 | 1.0 | 0.5 |
| **Score /100** | 63.9 | **65.8** | 31.1 | 22.2 |

**Claude Opus judge:** D and A both grounded their answers in the same traced call, but D read the series more closely. It named peaks and computed critical shares, caught that combined_articles is an undeduplicated sum, and placed the window and overlap limits where they change the reading. Each data-backed deliverable has a factual slip. D misstates lithium's peak month, and A wrongly says lithium leads in every month. B and C honestly declined to measure, so a decision-maker gets nothing actionable from them.

**GPT judge:** C gives the strongest decision-ready comparison: its complete traced chart and exports show lithium’s volume lead and rare earths’ spikes, with useful limits. B quantifies the trend and offers deeper follow-up, but its unsupported interpretation of the combined count and overlap weakens trust; C also has a direction error in its trend prose.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/rare-earths-compare/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/rare-earths-compare.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Compare news coverage of rare earths, lithium and cobalt.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.compare" \
  -H 'content-type: application/json' \
  -d '{"terms": ["rare earth", "lithium", "cobalt"], "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_terms']["fn"](**{'terms': ['rare earth', 'lithium', 'cobalt'], 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
