# NATO vs Russia vs Ukraine attention

[Defence & geopolitics](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** The attention balance of the war over time.  
> **Why it is hard.** Russia and Ukraine co-occur in most articles; overlap is the caveat.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · 2024-06-01 to 2026-06-01 (exclusive) · all listed tables passed strict index partition reads and historical row floors. Saved responses: [nato-russia-ukraine.json](../../examples/nato-russia-ukraine.json).

**The question:**

> Compare news coverage of NATO, Russia and Ukraine over two years.

## What Prism returned

| Term | Articles | Share | Critical | Growth (late vs early) | Negative-to-positive | vs all news |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **nato** | 253,305 | 10.8% | 210,459 | 1.26× (rising) | 4.03 | 6.95× |
| **russia** | 1,215,343 | 51.7% | 927,721 | 1.03× (flat) | 2.66 | 4.59× |
| **ukraine** | 879,966 | 37.5% | 704,809 | 0.87× (flat) | 3.47 | 5.98× |

![Comparison over time](../img/nato-russia-ukraine-compare.svg)

![Total coverage](../img/nato-russia-ukraine-share.svg)

> more coverage is attention, not importance, and a term that is also a common word will over-count — check each term's own volume against its sources panel

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/nato-russia-ukraine-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 3.5 | 2.5 | 0.5 | 0.0 |
| Measured comparison | 3.5 | 3.5 | 1.0 | 0.0 |
| Visualisation from counted data | 3.5 | 3.0 | 0.0 | 0.0 |
| Exploration and drill-down | 3.0 | 2.0 | 1.0 | 1.0 |
| Data export with provenance | 4.0 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 3.0 | 1.0 | 1.0 |
| Accuracy against the corpus | 3.0 | 3.0 | 3.5 | 3.5 |
| Calibration and limits | 3.5 | 2.5 | 3.5 | 3.0 |
| Decision-grade verdict | 3.5 | 3.5 | 3.0 | 3.0 |
| Facet coverage | 4.0 | 3.5 | 1.0 | 0.5 |
| **Score /100** | **70.8** | 61.0 | 32.8 | 27.0 |

**Claude Opus judge:** D was the only deliverable to turn the data into a decision-grade comparison. It gives exact half-on-half changes, ratios and peaks. It caught that combined_articles is a plain sum, so overlap is unresolved. It also flagged the mismatch between Ukraine's 'flat' label and its -15.9% decline. It has one wrong trough. B traced the same data but read it shallowly and misplaced the censoring. A and C honestly declined and gave a decision-maker nothing usable.

**GPT judge:** D is the most decision-ready: it gives a supported ranking and comparable ratios while clearly treating overlap and tone interpretation as limits. C has richer analysis and drill-down, but its speculative tone-ratio reading and treatment of the overlapping combined count weaken confidence; A and B are honest scoping notes rather than measured comparisons.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/nato-russia-ukraine/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/nato-russia-ukraine.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Compare news coverage of NATO, Russia and Ukraine over two years.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.compare" \
  -H 'content-type: application/json' \
  -d '{"terms": ["nato", "russia", "ukraine"], "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_terms']["fn"](**{'terms': ['nato', 'russia', 'ukraine'], 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
