# What is trending in business news

[Finance & markets](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A corpus-wide trend scan, not a single-topic query.  
> **Why it is hard.** Trending must run on curated subcategories; raw tags surface boilerplate.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [fintech-trending.json](../../examples/fintech-trending.json).

**The question:**

> What topics are rising fastest in business and finance news right now?

## What Prism returned

Last 60 days against the 60 days before, category *business*.

| Rising topic | Articles now | Window before | Growth |
| --- | ---: | ---: | ---: |
| entertainment and companion robotics | 15,401 | 324 | 47.53× |
| domestic service robotics for household tasks | 15,550 | 466 | 33.37× |
| travel-related infectious disease risks | 1,315 | 14 | 93.93× |
| human-robot interaction and collaborative robotics | 3,869 | 237 | 16.32× |
| green chemistry and eco-friendly alternatives | 2,680 | 144 | 18.61× |
| digitalization and automation in chemical processes | 2,750 | 212 | 12.97× |
| sustainable chemical production techniques | 2,769 | 234 | 11.83× |
| bio-based chemical product development | 2,795 | 246 | 11.36× |
| r&d in advanced chemical formulations | 2,925 | 288 | 10.16× |
| waterborne infectious agents | 411 | 19 | 21.63× |
| agrochemicals development and distribution | 2,924 | 443 | 6.6× |
| stock price fluctuations and market reactions | 35,209 | 18,559 | 1.9× |
| investment & funding | 27,863 | 15,318 | 1.82× |
| quarterly and annual financial results | 38,298 | 28,462 | 1.35× |
| corporate earnings reports and financial performance | 38,151 | 28,582 | 1.33× |

![Rising topics](../img/fintech-trending-rising.svg)

**Biggest topics in the window:** new product launches and innovations (44,403), strategic partnerships and collaborations (43,601), quarterly and annual financial results (38,298), corporate earnings reports and financial performance (38,151), stock price fluctuations and market reactions (35,209), technology adoption and digital transformation (32,635), company expansions and new market entries (29,311), executive leadership changes and appointments (28,675)

![Biggest topics](../img/fintech-trending-biggest.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/fintech-trending-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 3.5 | 0.0 | 0.0 |
| Measured comparison | 4.5 | 4.0 | 0.5 | 0.0 |
| Visualisation from counted data | 4.5 | 4.0 | 0.0 | 0.0 |
| Exploration and drill-down | 1.0 | 4.0 | 1.0 | 1.0 |
| Data export with provenance | 4.0 | 3.5 | 1.0 | 0.0 |
| Reproducibility | 4.5 | 4.5 | 0.0 | 0.5 |
| Accuracy against the corpus | 4.0 | 4.5 | 3.5 | 4.0 |
| Calibration and limits | 3.0 | 3.0 | 3.0 | 3.0 |
| Decision-grade verdict | 4.5 | 4.5 | 2.5 | 2.5 |
| Facet coverage | 4.5 | 4.0 | 1.0 | 0.5 |
| **Score /100** | 79.9 | **80.2** | 26.2 | 25.7 |

**Claude Opus judge:** C and D both used the same measured run and flagged its 144-day staleness. D separated the fragile small-base risers (robotics, chemicals, disease labels) from the finance core (stock moves 1.9x, funding 1.82x), using exact deltas, an overlap caveat and a chart that supports its verdict. C stopped at noting that the category fit was questionable. A and B honestly declined to measure, so they offer a decision-maker nothing beyond a prompt to go get data.

**GPT judge:** A is the strongest decision aid: it answers with traced growth, exposes the surprising category mismatch, and recommends treating the stale results as leads rather than current signals. B is richer in comparisons, but its unsupported investor-relations figures and incorrect summary of biggest-topic growth weaken trust; C and D are candid about lacking measurements but cannot answer the question.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/fintech-trending/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/fintech-trending.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What topics are rising fastest in business and finance news right now?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.trending" \
  -H 'content-type: application/json' \
  -d '{"days": 60, "category": "business", "limit": 15}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['trending_topics']["fn"](**{'days': 60, 'category': 'business', 'limit': 15})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
