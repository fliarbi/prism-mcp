# Oil vs renewables in the news

[Energy & climate](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Energy-mix attention over two years.  
> **Why it is hard.** Oil-price spikes drive volume; renewables carry positive tone.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · 2024-06-01 to 2026-06-01 (exclusive) · all listed tables passed strict index partition reads and historical row floors. Saved responses: [oil-vs-renewables.json](../../examples/oil-vs-renewables.json).

**The question:**

> Compare coverage of crude oil, renewable energy and natural gas.

## What Prism returned

| Term | Articles | Share | Critical | Growth (late vs early) | Negative-to-positive | vs all news |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **crude oil** | 70,737 | 13.7% | 48,625 | 2.92× (rising) | 2.24 | 3.86× |
| **renewable energy** | 361,780 | 70.2% | 260,319 | 1.06× (flat) | 0.19 | 0.33× |
| **natural gas** | 82,709 | 16.1% | 58,147 | 1.62× (rising) | 0.66 | 1.14× |

![Comparison over time](../img/oil-vs-renewables-compare.svg)

![Total coverage](../img/oil-vs-renewables-share.svg)

> more coverage is attention, not importance, and a term that is also a common word will over-count — check each term's own volume against its sources panel

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/oil-vs-renewables-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 3.5 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.0 | 1.0 | 0.0 |
| Visualisation from counted data | 4.0 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 3.0 | 2.0 | 1.0 | 0.5 |
| Data export with provenance | 4.0 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.0 | 1.0 | 0.5 |
| Accuracy against the corpus | 4.0 | 4.0 | 3.5 | 4.0 |
| Calibration and limits | 4.0 | 3.5 | 3.0 | 3.0 |
| Decision-grade verdict | 3.5 | 3.5 | 2.5 | 2.0 |
| Facet coverage | 4.0 | 3.5 | 0.5 | 0.5 |
| **Score /100** | **77.9** | 72.0 | 33.3 | 23.6 |

**Claude Opus judge:** C and D both rest on the same traced news.compare call. D read what the question turns on: the March 2026 oil and gas spike, the negative vs positive tone split, and the non-deduplicated combined total. C only reported endpoint changes and declined to interpret tone. A and B measured nothing, so they offer a decision-maker only a plan.

**GPT judge:** D is the strongest decision aid: it exposes the monthly oil and gas spike, compares all three terms on a shared window, and supplies usable exports with clear limits. C is more restrained about tone, but D better answers the scenario’s central risk that a price-driven spike can distort headline coverage; both leave the spike’s cause and unique-article overlap unresolved.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/oil-vs-renewables/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/oil-vs-renewables.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Compare coverage of crude oil, renewable energy and natural gas.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.compare" \
  -H 'content-type: application/json' \
  -d '{"terms": ["crude oil", "renewable energy", "natural gas"], "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_terms']["fn"](**{'terms': ['crude oil', 'renewable energy', 'natural gas'], 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
