# Rising topics in tech news

[Technology & AI](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A tech-trend scan for a product strategist.  
> **Why it is hard.** Trending ranks by growth against the previous window, not by size.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [cybersecurity-trending.json](../../examples/cybersecurity-trending.json).

**The question:**

> What technology topics are rising fastest in the news?

## What Prism returned

Last 60 days against the 60 days before, category *technology*.

| Rising topic | Articles now | Window before | Growth |
| --- | ---: | ---: | ---: |
| unesco world heritage historical sites | 2,631 | 10 | 263.1× |
| landscape photography styles | 1,032 | 14 | 73.71× |
| entertainment and companion robotics | 15,870 | 1,020 | 15.56× |
| domestic service robotics for household tasks | 16,021 | 1,128 | 14.2× |
| dslr cameras and accessories | 3,913 | 224 | 17.47× |
| mirrorless camera systems | 5,426 | 556 | 9.76× |
| aerial photography innovations | 485 | 15 | 32.33× |
| human-robot interaction and collaborative robotics | 4,052 | 465 | 8.71× |
| green chemistry and eco-friendly alternatives | 2,760 | 275 | 10.04× |
| digitalization and automation in chemical processes | 2,821 | 336 | 8.4× |
| sustainable chemical production techniques | 2,850 | 373 | 7.64× |
| bio-based chemical product development | 2,881 | 406 | 7.1× |
| r&d in advanced chemical formulations | 2,970 | 441 | 6.73× |
| telemedicine prescription practices | 336 | 17 | 19.76× |
| agrochemicals development and distribution | 2,924 | 454 | 6.44× |

![Rising topics](../img/cybersecurity-trending-rising.svg)

**Biggest topics in the window:** cryptocurrency impact on forex markets (41,554), new product launches and innovations (33,903), strategic partnerships and collaborations (30,320), technology adoption and digital transformation (27,176), domestic service robotics for household tasks (16,021), entertainment and companion robotics (15,870), company expansions and new market entries (15,779), artificial intelligence advancements (13,914)

![Biggest topics](../img/cybersecurity-trending-biggest.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/cybersecurity-trending-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 1.0 | 0.0 | 0.0 |
| Measured comparison | 4.5 | 4.0 | 0.5 | 0.0 |
| Visualisation from counted data | 4.0 | 3.5 | 0.0 | 0.0 |
| Exploration and drill-down | 1.0 | 1.5 | 1.0 | 1.0 |
| Data export with provenance | 3.0 | 2.5 | 1.0 | 0.0 |
| Reproducibility | 4.5 | 3.0 | 0.0 | 0.5 |
| Accuracy against the corpus | 3.5 | 4.0 | 2.5 | 4.0 |
| Calibration and limits | 4.5 | 3.0 | 3.0 | 3.5 |
| Decision-grade verdict | 4.0 | 4.0 | 2.5 | 2.5 |
| Facet coverage | 4.0 | 4.0 | 1.0 | 0.5 |
| **Score /100** | **75.3** | 61.6 | 23.6 | 26.5 |

**Claude Opus judge:** B and D both read the one recorded call and filtered out off-topic labels. Only B set robotics' 14-16x rise against flat AI (1.01x) and the other big topics, and it tied every limit (144-day staleness, top-15 censoring, loose category tagging) to the numbers with a reproducible export. D was correct but narrower and had a coverage-flag inconsistency. A and C measured nothing: A offered labelled memory guesses, and C gave a bare refusal.

**GPT judge:** C gives the most careful decision-ready reading of the available two-window record: it separates the fastest visible technology-related labels from the off-topic growth leaders, quantifies the comparison, and bounds the stale, loosely categorized feed. B is more expansive and has stronger traced comparison material, but unsupported topic counts and a contradicted coverage claim make it less dependable; neither deliverable achieves usable drill-down.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/cybersecurity-trending/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/cybersecurity-trending.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What technology topics are rising fastest in the news?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.trending" \
  -H 'content-type: application/json' \
  -d '{"days": 60, "category": "technology", "limit": 15}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['trending_topics']["fn"](**{'days': 60, 'category': 'technology', 'limit': 15})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
