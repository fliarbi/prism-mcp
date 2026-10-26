# Bitcoin ETF coverage

[Finance & markets](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Product-level narrative tracking for a crypto analyst.  
> **Why it is hard.** Coverage is concentrated in a few publishers; the source concentration is part of the answer.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [crypto-etf-pulse.json](../../examples/crypto-etf-pulse.json).

**The question:**

> How has news coverage of Bitcoin ETFs evolved, and what is the tone?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “bitcoin etf”, Jun 2024 – May 2026 | 12,577 |
| Critical coverage (priority 7–9) | 8,745 (69.5%) |
| Peak month | Apr 2026 (978 articles) |
| Last third of the window vs first third | 0.91× (flat) |
| Negative · positive | 23.3% · 76% |
| Tone vs all news (negative-to-positive ratio) | 0.31 vs 0.58 baseline: *markedly more positive than ordinary news coverage* |
| What Prism thinks “bitcoin etf” is | topic |

![Monthly coverage of bitcoin etf](../img/crypto-etf-pulse-trend.svg)

![Tone of bitcoin etf coverage](../img/crypto-etf-pulse-tone.svg)

![Countries in bitcoin etf coverage](../img/crypto-etf-pulse-geo.svg)

![Themes in bitcoin etf coverage](../img/crypto-etf-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “bitcoin etf” coverage (they also name the companies, people and places it is written about with): bitcoin (11,416), etf (7,852), blackrock (5,775), btc (5,775), cryptocurrency (5,237), ethereum (4,205), fidelity (2,727), eth (2,399), solana (2,168), blockchain (2,084), digital assets (1,498), xrp (1,492)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| sosovalue | larry fink | united states |
| bitwise | satoshi nakamoto | ireland |
| escape the fate | michael j. saylor | china |
| vaneck | robert kiyosaki | united kingdom |
| grayscale | peter schiff | canada |
| blackrock | cathie wood | australia |

**Top publishers in a 207-article sample:** openpr.com (19.8%), bitcoinethereumnews.com (15%), crypto-economy.com (4.3%), coincu.com (4.3%), panewslab.com (3.4%), crypto.news (2.9%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-04-18 | [BlackRock IBIT Leads $664M ETF Inflows with $284M Daily Surge](https://bitcoinethereumnews.com/tech/blackrock-ibit-leads-664m-etf-inflows-with-284m-daily-surge/) | bitcoinethereumnews.com | 8 | very_pos |
| 2026-03-29 | [Bitcoin ETF Outflows Hit 225M as BTC Breaks Key Support](https://bitcoinethereumnews.com/bitcoin/bitcoin-etf-outflows-hit-225m-as-btc-breaks-key-support/) | bitcoinethereumnews.com | 8 | slight_neg |
| 2026-05-19 | [Breaking: Trump's Truth Social Withdraws Bitcoin ETF Filing Amid $648M Outflow](https://coingape.com/trump-truth-social-withdraws-bitcoin-etf-filing-amid-648m-outflow/) | coingape.com | 8 | very_neg |
| 2026-04-10 | [Tron Price Prediction: TRX and ADA Fade as Pepeto Pushes Toward 100x Potential](https://www.openpr.com/news/4465033/tron-price-prediction-trx-and-ada-fade-as-pepeto-pushes-toward) | openpr.com | 8 | fair_pos |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 489 | 330 | 107 | 379 |
| Jul 2024 | 392 | 248 | 56 | 334 |
| Aug 2024 | 642 | 405 | 129 | 507 |
| Sep 2024 | 671 | 440 | 163 | 504 |
| Oct 2024 | 756 | 527 | 125 | 626 |
| Nov 2024 | 761 | 573 | 89 | 662 |
| Dec 2024 | 640 | 481 | 113 | 524 |
| Jan 2025 | 536 | 382 | 76 | 460 |
| Feb 2025 | 510 | 351 | 134 | 375 |
| Mar 2025 | 315 | 184 | 65 | 246 |
| Apr 2025 | 420 | 317 | 75 | 345 |
| May 2025 | 525 | 388 | 90 | 429 |
| Jun 2025 | 479 | 304 | 77 | 402 |
| Jul 2025 | 373 | 249 | 54 | 315 |
| Aug 2025 | 243 | 169 | 50 | 186 |
| Sep 2025 | 384 | 241 | 89 | 289 |
| Oct 2025 | 432 | 316 | 128 | 297 |
| Nov 2025 | 588 | 470 | 232 | 351 |
| Dec 2025 | 359 | 243 | 119 | 235 |
| Jan 2026 | 326 | 218 | 107 | 216 |
| Feb 2026 | 544 | 401 | 271 | 271 |
| Mar 2026 | 560 | 403 | 167 | 391 |
| Apr 2026 | 978 | 684 | 198 | 777 |
| May 2026 | 654 | 421 | 216 | 437 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/crypto-etf-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 4.5 | 1.0 | 0.0 |
| Measured comparison | 5.0 | 4.5 | 1.0 | 0.0 |
| Visualisation from counted data | 4.5 | 3.5 | 1.0 | 0.5 |
| Exploration and drill-down | 3.5 | 2.0 | 1.5 | 1.5 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.5 | 3.5 | 0.0 | 1.0 |
| Traceable references | 1.0 | 0.5 | 0.0 | 1.5 |
| Accuracy against the corpus | 3.5 | 2.5 | 3.0 | 4.0 |
| Calibration and limits | 3.0 | 3.0 | 3.5 | 4.0 |
| Decision-grade verdict | 3.5 | 4.0 | 2.5 | 2.5 |
| Facet coverage | 5.0 | 4.0 | 1.0 | 1.0 |
| **Score /100** | **73.7** | 64.3 | 29.1 | 31.1 |

**Claude Opus judge:** C and A both traced a flat two-year volume series and a tone ratio well below the corpus baseline. Only C charted tone, showing the souring after Sept 2025, and only C named the concentrated publishers, gave dated headlines and flagged label anomalies. A misread February 2026 as net-negative and had no headline layer. B and D honestly declined to measure anything, which leaves a decision-maker without the volume, tone or concentration answer.

**GPT judge:** D is the strongest decision aid because it combines traced volume and tone series, a defined baseline comparison, source concentration, headline examples, and explicit limits. Its incorrect peak caption and a few unsupported coverage or match-mode claims need correction; C is cleaner in its trend interpretation but omits a tone chart and offers less usable drill-down.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/crypto-etf-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/crypto-etf-pulse.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How has news coverage of Bitcoin ETFs evolved, and what is the tone?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "bitcoin etf", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'bitcoin etf', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
