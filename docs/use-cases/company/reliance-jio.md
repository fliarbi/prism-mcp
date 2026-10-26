# Reliance Jio coverage

[Company & competitive intelligence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** An Indian conglomerate profile: themes, people, places.  
> **Why it is hard.** Jio IPO speculation and telecom tariffs both drive coverage.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [reliance-jio.json](../../examples/reliance-jio.json).

**The question:**

> What themes and people dominate news coverage of Reliance Jio?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “reliance jio”, Jun 2024 – May 2026 | 12,858 |
| Critical coverage (priority 7–9) | 7,969 (62%) |
| Peak month | Mar 2025 (890 articles) |
| Last third of the window vs first third | 0.66× (falling) |
| Negative · positive | 18.3% · 79.9% |
| Tone vs all news (negative-to-positive ratio) | 0.23 vs 0.58 baseline: *markedly more positive than ordinary news coverage* |
| What Prism thinks “reliance jio” is | topic |

![Monthly coverage of reliance jio](../img/reliance-jio-trend.svg)

![Tone of reliance jio coverage](../img/reliance-jio-tone.svg)

![Countries in reliance jio coverage](../img/reliance-jio-geo.svg)

![Themes in reliance jio coverage](../img/reliance-jio-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “reliance jio” coverage (they also name the companies, people and places it is written about with): india (8,479), telecom (3,552), telecommunications (1,558), mobile technology (1,306), dot (1,255), starlink (1,168), tariffs (905), gb (846), sms (731), ott (665), sim (645), verizon (423)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| jio | jyotiraditya scindia | india |
| airtel | mukesh ambani | united states |
| telecom regulatory authority of india | elon musk | china |
| 5g | nita ambani | south korea |
| reliance industries | anil ambani | finland |
| ericsson | motilal oswal financial services | united kingdom |

**Top publishers in a 220-article sample:** telecomtalk.info (20.5%), digit.in (8.2%), livehindustan.com (5.5%), prabhatkhabar.com (5.5%), financialexpress.com (3.2%), economictimes.indiatimes.com (3.2%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-03-31 | [Pan-India monthly 5G data traffic surges 70% on-year in 2025: Nokia MBiT 2026 report](https://telecom.economictimes.indiatimes.com/news/telecom-equipment/5g-data-traffic-in-india-soars-70-year-on-year-to-129-exabytes-in-2025/129920678) | telecom.economictimes.indiatimes.com | 8 | fair_pos |
| 2026-02-23 | [Views of Mukesh Ambani: “India must become a world leader in AI” -](https://tele.net.in/views-of-mukesh-ambani-india-must-become-a-world-leader-in-ai/) | tele.net.in | 8 | very_pos |
| 2026-02-20 | [India’s top telco tackles AI with $110b and proven playbook](https://www.theregister.com/2026/02/20/jio_ai_plans_india_summit/) | theregister.com | 8 | slight_pos |
| 2026-05-31 | [Affordable 6g: Reliance Jio and Google Partner to Launch](https://technosports.co.in/jio-google-affordable-6g-partnership/) | technosports.co.in | 8 | very_pos |
| 2026-05-30 | [Jio Platforms has Filed 6817 Patents](https://telecomtalk.info/jio-platforms-has-filed-6817-patents/1008016/) | telecomtalk.info | 8 | very_pos |
| 2026-05-17 | [Reliance Jio IPO: How much-awaited IPO likely to impact Reliance share price? \| Stock Market News](https://www.livemint.com/market/stock-market-news/reliance-jio-ipo-how-much-awaited-ipo-likely-to-impact-reliance-share-price-11779005719985.html) | livemint.com | 8 | slight_neg |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 605 | 387 | 98 | 495 |
| Jul 2024 | 720 | 362 | 154 | 555 |
| Aug 2024 | 612 | 317 | 106 | 499 |
| Sep 2024 | 530 | 305 | 102 | 427 |
| Oct 2024 | 791 | 518 | 169 | 613 |
| Nov 2024 | 536 | 329 | 141 | 391 |
| Dec 2024 | 497 | 276 | 130 | 363 |
| Jan 2025 | 680 | 361 | 125 | 548 |
| Feb 2025 | 611 | 393 | 85 | 519 |
| Mar 2025 | 890 | 654 | 134 | 746 |
| Apr 2025 | 554 | 349 | 114 | 417 |
| May 2025 | 444 | 280 | 124 | 312 |
| Jun 2025 | 444 | 308 | 82 | 361 |
| Jul 2025 | 443 | 259 | 57 | 385 |
| Aug 2025 | 842 | 472 | 155 | 680 |
| Sep 2025 | 361 | 233 | 55 | 304 |
| Oct 2025 | 386 | 251 | 44 | 341 |
| Nov 2025 | 394 | 263 | 57 | 335 |
| Dec 2025 | 529 | 391 | 82 | 350 |
| Jan 2026 | 333 | 243 | 58 | 272 |
| Feb 2026 | 335 | 232 | 45 | 289 |
| Mar 2026 | 368 | 225 | 65 | 299 |
| Apr 2026 | 557 | 320 | 99 | 447 |
| May 2026 | 396 | 241 | 71 | 322 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/reliance-jio-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.0 | 0.5 | 0.5 |
| Measured comparison | 4.0 | 4.0 | 0.5 | 0.0 |
| Visualisation from counted data | 3.5 | 3.0 | 0.0 | 0.5 |
| Exploration and drill-down | 3.5 | 2.0 | 1.5 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.5 |
| Reproducibility | 4.5 | 3.5 | 1.0 | 1.0 |
| Traceable references | 1.0 | 1.0 | 0.0 | 0.0 |
| Accuracy against the corpus | 4.5 | 3.5 | 3.5 | 3.5 |
| Calibration and limits | 4.5 | 3.0 | 3.0 | 3.5 |
| Decision-grade verdict | 4.0 | 3.5 | 2.5 | 3.0 |
| Facet coverage | 4.5 | 3.5 | 1.0 | 1.0 |
| **Score /100** | **76.7** | 63.0 | 28.2 | 29.0 |

**Claude Opus judge:** D answered the question with traced counts for themes, people and organisations. It separated the 'critical' flag from negative tone, caught pipeline anomalies, and placed every limit next to its number. B had the same data but was thinner: it omitted Musk among people and left the IPO-vs-tariff tension unquantified. A and C were honest memory-only responses with no measured content.

**GPT judge:** B is the strongest decision aid: it answers which themes and people dominate with traced counts, trend and caveats, and it addresses several implied contrasts. Its missing theme and people exports, incomplete drill-down linkage, and inconsistent end-date wording keep it short of a fully reproducible, decision-grade package.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/reliance-jio/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/reliance-jio.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What themes and people dominate news coverage of Reliance Jio?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "reliance jio", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'reliance jio', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
