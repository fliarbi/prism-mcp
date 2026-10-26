# Measles resurgence coverage

[Public health & epidemiology](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Outbreak monitoring: volume, geography, critical stories.  
> **Why it is hard.** The 2025 US and Canadian outbreaks dominate; a global picture needs the geography split.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [measles-outbreak-pulse.json](../../examples/measles-outbreak-pulse.json).

**The question:**

> How much measles outbreak coverage has there been, where, and how has it trended?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “measles”, Jun 2024 – May 2026 | 22,178 |
| Critical coverage (priority 7–9) | 19,359 (87.3%) |
| Peak month | Mar 2025 (2,531 articles) |
| Last third of the window vs first third | 3.36× (rising) |
| Negative · positive | 79.5% · 18.5% |
| Tone vs all news (negative-to-positive ratio) | 4.3 vs 0.58 baseline: *markedly more negative than ordinary news coverage* |
| What Prism thinks “measles” is | topic |

![Monthly coverage of measles](../img/measles-outbreak-pulse-trend.svg)

![Tone of measles coverage](../img/measles-outbreak-pulse-tone.svg)

![Countries in measles coverage](../img/measles-outbreak-pulse-geo.svg)

![Themes in measles coverage](../img/measles-outbreak-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “measles” coverage (they also name the companies, people and places it is written about with): public health (6,628), cdc (6,513), vaccine (4,179), robert f. kennedy jr. (4,050), kennedy (3,761), the centers for disease control and prevention (3,504), vaccines (3,349), new mexico (3,319), hhs (1,808), health and human services (1,653), the u.s. centers for disease control and prevention (1,411), infectious disease (1,165)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| cult of the dead cow | robert f. kennedy jr. | united states |
| centers for disease control and prevention | robert f. kennedy | canada |
| pan american health organization | the who | united kingdom |
| uk health security agency | jay bhattacharya | mexico |
| the who | tedros adhanom ghebreyesus | georgia |
| american academy of pediatrics | ron wyden | australia |

**Top publishers in a 209-article sample:** dhakatribune.com (22.5%), yahoo.com (11%), tbsnews.net (6.7%), uniindia.com (2.9%), time.news (2.4%), wgal.com (2.4%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-05-27 | [Bangladesh Faces Devastating Measles Outbreak](https://time.news/bangladesh-faces-devastating-measles-outbreak/) | time.news | 9 | very_neg |
| 2026-05-16 | [Measles outbreak: Death toll reaches 453 as 2 more children die in 24hrs](https://www.tbsnews.net/bangladesh/health/measles-outbreak-death-toll-reaches-453-2-more-children-die-24hrs-1440641) | tbsnews.net | 9 | very_neg |
| 2026-05-11 | [Two kids die of measles in Dherki \| 24 News HD](https://www.24newshd.tv/11-May-2026/two-kids-die-measles-dherki) | 24newshd.tv | 9 | very_neg |
| 2026-04-24 | [Child Found Drunk At School \| MD Chef Wins Big \| Peeping Tom On Loose: MD News](https://patch.com/maryland/belair/child-found-drunk-school-toddler-drowns-peeping-tom-loose-md-top-news) | patch.com | 9 | extreme_neg |
| 2026-04-23 | [Deadly meningitis spreads as Sudanese refugees pack Chad camps, MSF says](https://www.yahoo.com/news/articles/deadly-meningitis-spreads-sudanese-refugees-154314042.html) | yahoo.com | 9 | extreme_neg |
| 2026-04-20 | [3-Year-Old Drowns \| 1st Measles Case Of 2026 \| New Mac And Cheese Shop: MD Weekend](https://patch.com/maryland/across-md/3-year-old-drowns-1st-measles-case-2026-new-mac-cheese-shop-md-weekend) | patch.com | 9 | very_neg |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 200 | 171 | 122 | 74 |
| Jul 2024 | 275 | 238 | 177 | 92 |
| Aug 2024 | 285 | 225 | 156 | 121 |
| Sep 2024 | 300 | 244 | 203 | 90 |
| Oct 2024 | 210 | 152 | 121 | 82 |
| Nov 2024 | 359 | 298 | 231 | 116 |
| Dec 2024 | 315 | 273 | 234 | 76 |
| Jan 2025 | 555 | 453 | 366 | 174 |
| Feb 2025 | 1,264 | 1,143 | 1,111 | 145 |
| Mar 2025 | 2,531 | 2,297 | 2,181 | 326 |
| Apr 2025 | 2,380 | 2,126 | 2,032 | 321 |
| May 2025 | 1,325 | 1,082 | 1,056 | 246 |
| Jun 2025 | 689 | 567 | 534 | 144 |
| Jul 2025 | 1,041 | 793 | 861 | 173 |
| Aug 2025 | 998 | 850 | 811 | 179 |
| Sep 2025 | 1,050 | 956 | 708 | 333 |
| Oct 2025 | 744 | 693 | 564 | 177 |
| Nov 2025 | 577 | 506 | 464 | 105 |
| Dec 2025 | 588 | 506 | 476 | 106 |
| Jan 2026 | 827 | 754 | 632 | 180 |
| Feb 2026 | 2,069 | 1,833 | 1,693 | 257 |
| Mar 2026 | 1,047 | 894 | 776 | 141 |
| Apr 2026 | 1,635 | 1,489 | 1,338 | 279 |
| May 2026 | 914 | 816 | 751 | 153 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/measles-outbreak-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 4.5 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 1.5 | 0.0 |
| Visualisation from counted data | 3.5 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 3.5 | 3.0 | 1.0 | 2.0 |
| Data export with provenance | 4.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 5.0 | 1.0 | 1.0 |
| Traceable references | 1.0 | 0.5 | 1.5 | 0.5 |
| Accuracy against the corpus | 3.0 | 4.5 | 3.5 | 3.0 |
| Calibration and limits | 2.5 | 4.5 | 3.0 | 2.5 |
| Decision-grade verdict | 4.0 | 4.0 | 3.0 | 2.5 |
| Facet coverage | 5.0 | 4.5 | 1.0 | 0.0 |
| **Score /100** | 73.0 | **77.1** | 35.5 | 23.2 |

**Claude Opus judge:** D and B both reproduce the measured series exactly, but D also splits the geography, flags the entity and place anomalies, and shows the enrichment lag that under-counts the 2026 Bangladesh surge. D also reaches item-level headlines with URLs, which B never does. A and C measure nothing about coverage; C substitutes memory case counts, which a decision-maker could misread as a coverage series.

**GPT judge:** C is the strongest decision-grade answer: its traced trend, comparisons, and limits stay aligned with the record, though it lacks a geography export and external references. D covers more facets, but its false claim that the latest month is complete undermines its trend reading and confidence.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/measles-outbreak-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/measles-outbreak-pulse.pdf)

## Live MCP session

Here each model was given only the question and a live connection to the Prism MCP server, and chose its own calls.

**Claude** (claude-sonnet, 197.7 s) called 1 Prism tool:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `prism_overview` | `{"term": "measles outbreak"}` | ok · 44,911 chars |

<details><summary>Claude's answer</summary>

**Measles outbreak coverage: about 3,978 news articles from June 2024 to May 2026. It is concentrated in the US and peaked in March 2025.** Coverage is rising overall, but it comes in bursts. The source is Prism's news corpus, matching articles that mention "measles outbreak". The window ends 1 June 2026 because later data is thin.

**What the data shows**
- **Trend:**
  - Volume was low through 2024, at 8–29 articles a month.
  - It jumped to 388 in February 2025 and peaked at 675 in March 2025 (609 in April).
  - It fell to 61 in June 2025.
  - It then recovered in waves: 224 in August 2025, 350 in February 2026 and 370 in April 2026.
  - The last third of the window had 1,453 articles against 173 in the first third, about 8.4 times as many.
- **Geography:** This covers the 73% of articles that were placed in a country.
  - US 2,587 (46%), Canada 470 (8.4%), Mexico 376 (6.7%) and "Georgia" 291 (5.2%).
  - UK 281 (5%), Australia 120, Samoa 96, New Zealand 87 and Bangladesh 68 (1.2%).
  - Mexico and Samoa are over-represented relative to normal news. The "Georgia" count may be the US state or the country, so I'd treat it with caution.
  - Place labels are only reliable through April 2026, so recent months are under-placed.
- **Tone:** 91.4% of articles are negative and 8.2% positive. That is about 19 times more negative than the corpus baseline, and 3,743 of the 3,978 articles (94%) were flagged critical.
- **Themes and actors:** Vaccine hesitancy, immunization and herd immunity dominate. Robert F. Kennedy Jr. appears in about 1,075 articles with people labels, and the CDC and WHO are the leading organisations.
- **Recent coverage:** April–May 2026 articles cover Bangladesh (reports of over 100 child deaths), South Carolina's outbreak ending, London and Madhya Pradesh in India.

**Interpretation**
- The 2025 peak is consistent with a US-centred news cycle, and the high Kennedy and CDC share points to policy and politics driving it.
- The 2026 rise looks more international, with Bangladesh in the recent feed.
- The negativity is largely built in, because outbreak stories are inherently bad news. The tone figure says little about editorial stance.

**Caveats**
- Article counts measure attention, not case numbers.
- The publisher sample was only 75 articles and the entity labels are machine-assigned, so one organisation label ("cult of the dead cow") is clearly spurious.
- Nothing after May 2026 is covered.

</details>

**ChatGPT** (gpt-6-luna, 202.9 s) called 5 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `resolve_term` | `{"term": "measles"}` | ok · 3,645 chars |
| 2 | `freshness_status` | `{}` | ok · 1,709 chars |
| 3 | `news_geography` | `{"term": "measles", "level": "country", "limit": 10}` | ok · 5,727 chars |
| 4 | `news_trends` | `{"term": "measles", "granularity": "month"}` | see payload · 671 chars |
| 5 | `news_trends` | `{"term": "measles", "granularity": "monthly", "since": "2024-05-01", "until": "2026-06-01"}` | ok · 13,055 chars |

<details><summary>ChatGPT's answer</summary>

Prism recorded **22,586 measles news articles from May 2024 through May 2026**. Monthly coverage rose overall but fluctuated sharply, peaking at **2,531 articles in March 2025**; May 2026 had **914**. The corpus’s early-to-late period comparison shows the final third had **3.57×** the coverage of the first third. *(Prism news.trends; monthly, mention-matched articles.)*

**Where:** Of **21,672** matched articles with geography results, **13,753 (63.5%)** were assigned a country. The United States led with **11,280 (44.0% of placed articles)**, followed by Canada (**1,701; 6.6%**), the UK (**1,581; 6.2%**) and Mexico (**1,052; 4.1%**). These are places the articles were *about*, not publisher locations. *(Prism news.geography; May 2024–May 2026.)*

**What the data shows:** Coverage was highest in early 2025, fell afterward, then rose again in early 2026—**2,069** articles in February and **1,635** in April—before easing to 914 in May. The series’ annualized growth measure is **49.7%** across the window; it does not mean coverage increased steadily month by month.

**Interpretation:** Attention was concentrated on the United States, with smaller but notable coverage about Canada, the UK and Mexico. The overall upward comparison reflects a volatile two-year period with major spikes, rather than a smooth climb. Prism censors the series at **June 1, 2026** because newer news ingestion is incomplete; it reports full corpus index partition coverage, but that is not proof every article has been ingested.

</details>

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How much measles outbreak coverage has there been, where, and how has it trended?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "measles", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'measles', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
