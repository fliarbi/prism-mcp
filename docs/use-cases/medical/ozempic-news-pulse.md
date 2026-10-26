# Ozempic in the news

[Medical & clinical evidence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A media-intelligence pulse on a blockbuster drug.  
> **Why it is hard.** Brand, generic and class names (Ozempic, semaglutide, GLP-1) are covered differently.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [ozempic-news-pulse.json](../../examples/ozempic-news-pulse.json).

**The question:**

> What is the news saying about Ozempic: volume, tone, themes and the critical stories?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “ozempic”, Jun 2024 – May 2026 | 22,214 |
| Critical coverage (priority 7–9) | 15,062 (67.8%) |
| Peak month | Mar 2026 (1,470 articles) |
| Last third of the window vs first third | 1.23× (flat) |
| Negative · positive | 37.9% · 61.8% |
| Tone vs all news (negative-to-positive ratio) | 0.61 vs 0.58 baseline: *about as negative as ordinary news coverage* |
| What Prism thinks “ozempic” is | topic |

![Monthly coverage of ozempic](../img/ozempic-news-pulse-trend.svg)

![Tone of ozempic coverage](../img/ozempic-news-pulse-tone.svg)

![Countries in ozempic coverage](../img/ozempic-news-pulse-geo.svg)

![Themes in ozempic coverage](../img/ozempic-news-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “ozempic” coverage (they also name the companies, people and places it is written about with): glp-1 (10,484), health (7,343), healthcare (6,519), obesity (4,937), fda (4,006), pharmaceuticals (2,502), medicare (1,970), medical research (1,842), medicaid (1,154), the food and drug administration (977), diet (831), the u.s. food and drug administration (794)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| novo nordisk | eli lilly | united states |
| new party (brazil) | lizzo | united kingdom |
| hims & hers health | kathy bates | canada |
| lilly | kelly clarkson | india |
| side effects | ned lamont | china |
| glp | whoopi goldberg | denmark |

**Top publishers in a 197-article sample:** yahoo.com (10.2%), archynewsy.com (2.5%), exame.com (2.5%), ibtimes.co.uk (2.5%), uniladtech.com (2.5%), bbc.co.uk (1.5%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-04-19 | [The global weight loss revolution: How drugs are redefining obesity](https://www.theweek.in/columns/dr-preetha-peddy/2026/04/11/the-global-weight-loss-revolution-how-drugs-are-redefining-obesity.html) | theweek.in | 8 | slight_neg |
| 2026-03-11 | [Experts Warn: 1 in 10,000 Wegovy Users Face 5X Higher Risk Leading to Serious Eye Complications](https://www.ibtimes.co.uk/experts-warn-1-10000-wegovy-users-face-5x-higher-risk-leading-serious-eye-complications-1784867) | ibtimes.co.uk | 8 | slight_neg |
| 2026-03-09 | [Abnehmen: Vitamin-D-Mangel wegen Ozempic & Co. – Dr. Riedl warnt vor Risiko](https://www.braunschweiger-zeitung.de/ratgeber-wissen/article411257613/abnehmen-ozempic-vitamin-d-omega-3-dr-riedl-warnt-vor-erhoehtem-sterberisiko.html) | braunschweiger-zeitung.de | 8 | very_neg |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 769 | 530 | 333 | 433 |
| Jul 2024 | 823 | 623 | 260 | 558 |
| Aug 2024 | 548 | 375 | 217 | 327 |
| Sep 2024 | 735 | 535 | 311 | 418 |
| Oct 2024 | 845 | 573 | 355 | 486 |
| Nov 2024 | 807 | 599 | 384 | 416 |
| Dec 2024 | 857 | 566 | 356 | 497 |
| Jan 2025 | 1,300 | 911 | 502 | 794 |
| Feb 2025 | 888 | 652 | 406 | 479 |
| Mar 2025 | 871 | 520 | 317 | 546 |
| Apr 2025 | 1,106 | 683 | 354 | 746 |
| May 2025 | 811 | 547 | 345 | 465 |
| Jun 2025 | 806 | 558 | 253 | 546 |
| Jul 2025 | 844 | 472 | 279 | 561 |
| Aug 2025 | 1,049 | 711 | 394 | 649 |
| Sep 2025 | 938 | 688 | 358 | 575 |
| Oct 2025 | 774 | 524 | 274 | 497 |
| Nov 2025 | 999 | 713 | 392 | 598 |
| Dec 2025 | 962 | 613 | 284 | 671 |
| Jan 2026 | 822 | 491 | 294 | 525 |
| Feb 2026 | 1,162 | 806 | 408 | 749 |
| Mar 2026 | 1,470 | 1,059 | 649 | 812 |
| Apr 2026 | 1,074 | 692 | 354 | 715 |
| May 2026 | 954 | 621 | 316 | 636 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/ozempic-news-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 5.0 | 4.5 | 1.0 | 0.5 |
| Measured comparison | 4.5 | 4.5 | 0.5 | 0.5 |
| Visualisation from counted data | 4.0 | 3.5 | 0.5 | 0.5 |
| Exploration and drill-down | 2.5 | 3.0 | 1.0 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.5 | 4.0 | 1.0 | 0.0 |
| Traceable references | 1.0 | 1.0 | 0.5 | 0.5 |
| Accuracy against the corpus | 4.5 | 4.0 | 3.5 | 4.0 |
| Calibration and limits | 4.5 | 3.0 | 3.5 | 4.0 |
| Decision-grade verdict | 5.0 | 4.0 | 2.5 | 2.5 |
| Facet coverage | 4.5 | 4.5 | 2.0 | 1.5 |
| **Score /100** | **80.4** | 71.9 | 32.3 | 28.7 |

**Claude Opus judge:** A and B both drew on the same overview data and reported matching volume, tone and theme figures. B went further: it decomposed the trend into critical and polarity series and exported them. It also quantified monthly tone extremes against the baseline and caught the mislabelled 'eli lilly' entity, making it the more decision-ready of the two. C and D honestly declined to measure; D added labelled memory themes, but neither gives a decision-maker usable numbers.

**GPT judge:** A gives the most decision-ready answer: it combines a fully traced, decomposed trend with tone, themes, limits, and a clear recommendation, while distinguishing critical flags from negative sentiment. D is similarly strong on measurement but omits a tone chart, has less complete export and follow-up coverage, and misstates how the censored month is handled.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/ozempic-news-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/ozempic-news-pulse.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is the news saying about Ozempic: volume, tone, themes and the critical stories?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "ozempic", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'ozempic', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
