# Apple tone vs the baseline

[Company & competitive intelligence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A tone benchmark for investor relations.  
> **Why it is hard.** Product launches create positive spikes; regulation creates negative ones.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [apple-sentiment.json](../../examples/apple-sentiment.json).

**The question:**

> Is coverage of Apple more positive or more negative than average news? How has it moved?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “apple inc”, Jun 2024 – May 2026 | 9,343 |
| Critical coverage (priority 7–9) | 4,752 (50.9%) |
| Peak month | Apr 2026 (697 articles) |
| Last third of the window vs first third | 1.47× (rising) |
| Negative · positive | 26% · 72.5% |
| Tone vs all news (negative-to-positive ratio) | 0.36 vs 0.58 baseline: *markedly more positive than ordinary news coverage* |
| What Prism thinks “apple inc” is | organization |

![Monthly coverage of apple inc](../img/apple-sentiment-trend.svg)

![Tone of apple inc coverage](../img/apple-sentiment-tone.svg)

![Countries in apple inc coverage](../img/apple-sentiment-geo.svg)

![Themes in apple inc coverage](../img/apple-sentiment-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “apple inc” coverage (they also name the companies, people and places it is written about with): apple (7,565), iphone (4,477), ipad (2,872), mac (2,830), apple watch (2,381), apple tv (1,377), tim cook (1,375), iphones (1,322), nvda (769), cook (682), wedbush (636), app store (597)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| apple inc. | ronald wayne | united states |
| foxconn | steve wozniak | china |
| siri | tim cook | india |
| tesla, inc. | steve jobs | united kingdom |
| loop capital | mark gurman | colombia |
| alphabet inc. | jim cramer | south korea |

**Top publishers in a 218-article sample:** defenseworld.net (39.9%), baseballnewssource.com (7.8%), watchlistnews.com (6.9%), thelincolnianonline.com (6%), thestar.com.my (5%), benzinga.com (4.6%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-03-17 | [Apple overshoots iPhone production target under PLI scheme by 80%](https://www.business-standard.com/companies/news/apple-overshoots-iphone-production-target-under-pli-scheme-by-80-126031700959_1.html) | business-standard.com | 8 | slight_neg |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 290 | 204 | 70 | 218 |
| Jul 2024 | 274 | 204 | 87 | 182 |
| Aug 2024 | 313 | 221 | 111 | 197 |
| Sep 2024 | 253 | 161 | 88 | 161 |
| Oct 2024 | 292 | 178 | 77 | 214 |
| Nov 2024 | 202 | 139 | 62 | 138 |
| Dec 2024 | 168 | 108 | 50 | 117 |
| Jan 2025 | 546 | 273 | 207 | 329 |
| Feb 2025 | 386 | 183 | 104 | 258 |
| Mar 2025 | 461 | 97 | 48 | 412 |
| Apr 2025 | 542 | 229 | 187 | 349 |
| May 2025 | 417 | 226 | 156 | 254 |
| Jun 2025 | 382 | 138 | 83 | 294 |
| Jul 2025 | 306 | 183 | 100 | 202 |
| Aug 2025 | 472 | 246 | 116 | 346 |
| Sep 2025 | 608 | 242 | 121 | 475 |
| Oct 2025 | 318 | 202 | 67 | 246 |
| Nov 2025 | 291 | 185 | 84 | 202 |
| Dec 2025 | 256 | 152 | 88 | 164 |
| Jan 2026 | 417 | 187 | 76 | 340 |
| Feb 2026 | 521 | 243 | 123 | 394 |
| Mar 2026 | 483 | 186 | 82 | 397 |
| Apr 2026 | 697 | 338 | 158 | 529 |
| May 2026 | 448 | 227 | 86 | 352 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/apple-sentiment-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 4.0 | 0.5 | 0.0 |
| Measured comparison | 4.0 | 4.0 | 1.0 | 0.0 |
| Visualisation from counted data | 4.0 | 3.5 | 0.5 | 0.0 |
| Exploration and drill-down | 2.5 | 2.0 | 1.5 | 1.0 |
| Data export with provenance | 4.5 | 3.0 | 0.5 | 0.0 |
| Reproducibility | 4.0 | 4.0 | 1.0 | 1.0 |
| Traceable references | 1.5 | 1.0 | 0.5 | 0.5 |
| Accuracy against the corpus | 3.5 | 4.0 | 4.0 | 4.0 |
| Calibration and limits | 4.5 | 4.0 | 4.0 | 2.5 |
| Decision-grade verdict | 4.0 | 4.5 | 3.0 | 2.5 |
| Facet coverage | 4.5 | 4.5 | 1.0 | 0.5 |
| **Score /100** | **74.9** | 71.6 | 33.9 | 24.8 |

**Claude Opus judge:** B and D both answer with traced numbers that Apple coverage is markedly more positive than the corpus baseline (0.36 vs 0.58). D goes further: - It separates the 'critical' flag from negative polarity. - It quantifies volume and critical trends. - It flags the Colombia anomaly and the label-fill lag. - It gives news items with URLs.  D has one averaging slip. A and C offer no measurement; C's honestly labelled memory guess happens to point the right way.

**GPT judge:** D is the strongest decision brief: it gives a measured comparison, a readable monthly movement, and a bounded verdict with relevant caveats. C provides richer exports and breakdowns, but its first-six-month tone average is miscalculated and its report adds more unsupported precision.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/apple-sentiment/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/apple-sentiment.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Is coverage of Apple more positive or more negative than average news? How has it moved?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "apple inc", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'apple inc', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
