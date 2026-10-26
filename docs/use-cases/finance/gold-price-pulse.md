# Gold price narrative

[Finance & markets](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Market-narrative intelligence for a commodities desk.  
> **Why it is hard.** Gold hit records through 2025-2026; tone and criticality move differently from volume.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [gold-price-pulse.json](../../examples/gold-price-pulse.json).

**The question:**

> What is the news narrative around gold prices: volume, tone, and the critical stories?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “gold price”, Jun 2024 – May 2026 | 32,804 |
| Critical coverage (priority 7–9) | 7,788 (23.7%) |
| Peak month | Oct 2025 (2,193 articles) |
| Last third of the window vs first third | 1.78× (rising) |
| Negative · positive | 33.6% · 65.4% |
| Tone vs all news (negative-to-positive ratio) | 0.51 vs 0.58 baseline: *about as negative as ordinary news coverage* |
| What Prism thinks “gold price” is | topic |

![Monthly coverage of gold price](../img/gold-price-pulse-trend.svg)

![Tone of gold price coverage](../img/gold-price-pulse-tone.svg)

![Countries in gold price coverage](../img/gold-price-pulse-geo.svg)

![Themes in gold price coverage](../img/gold-price-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “gold price” coverage (they also name the companies, people and places it is written about with): gold (14,609), federal reserve (7,863), fed (6,702), silver (5,921), interest rates (4,357), us dollar (4,114), the federal reserve (3,087), usd (2,843), global market (2,819), global markets (2,439), gmt (2,044), jerome powell (1,974)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| mcx | jerome powell | united states |
| comex | christopher waller | india |
| federal reserve | lisa d. cook | china |
| multi commodity exchange | austan goolsbee | united kingdom |
| theprint | kevin hassett | iran |
| hdfc securities | peter schiff | russia |

**Top publishers in a 219-article sample:** fortune.com (12.3%), indianews.in (10.5%), bitcoinethereumnews.com (9.6%), mettisglobal.news (5.9%), livehindustan.com (5%), boerse-express.com (5%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-04-07 | [20-day EMA acts as key barrier ahead of Trump’s deadline to Iran](https://bitcoinethereumnews.com/finance/20-day-ema-acts-as-key-barrier-ahead-of-trumps-deadline-to-iran/) | bitcoinethereumnews.com | 8 | none |
| 2026-02-22 | [High-Grade Near-Surface Graphite Intersected at Millennium](https://investingnews.com/high-grade-near-surface-graphite-intersected-at-millennium/) | investingnews.com | 8 | slight_neg |
| 2026-03-26 | [Kiyosaki sieht Goldpreis bei 35.000 US-Dollar](https://wallstreet-online.de/nachricht/20662026-rallye-silber-bitcoin-kiyosaki-gold-35-000-us-dollar-groesstem-crash-geschichte) | wallstreet-online.de | 8 | very_neg |
| 2026-04-13 | [Gold Buyers Hold Back as US-Iran Deadlock and Hawkish Fed Outlook Strengthen Dollar](https://www.bizzbuzz.news/wealth/gold/gold-price-xauusd-us-iran-tensions-analysis-1388867) | bizzbuzz.news | 8 | slight_neg |
| 2026-04-09 | [Gold nears $4,800 as softer Dollar and yields lift demand](https://bitcoinethereumnews.com/finance/gold-nears-4800-as-softer-dollar-and-yields-lift-demand/) | bitcoinethereumnews.com | 8 | slight_neg |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 521 | 115 | 162 | 353 |
| Jul 2024 | 790 | 188 | 226 | 554 |
| Aug 2024 | 906 | 175 | 285 | 612 |
| Sep 2024 | 1,060 | 208 | 252 | 791 |
| Oct 2024 | 1,281 | 250 | 349 | 922 |
| Nov 2024 | 1,121 | 291 | 460 | 651 |
| Dec 2024 | 1,058 | 213 | 318 | 719 |
| Jan 2025 | 1,182 | 237 | 245 | 927 |
| Feb 2025 | 1,271 | 370 | 368 | 883 |
| Mar 2025 | 1,419 | 414 | 388 | 1,018 |
| Apr 2025 | 2,099 | 663 | 631 | 1,460 |
| May 2025 | 1,235 | 369 | 546 | 683 |
| Jun 2025 | 999 | 238 | 417 | 578 |
| Jul 2025 | 969 | 214 | 304 | 657 |
| Aug 2025 | 1,189 | 257 | 355 | 815 |
| Sep 2025 | 1,573 | 368 | 328 | 1,232 |
| Oct 2025 | 2,193 | 544 | 666 | 1,492 |
| Nov 2025 | 1,175 | 310 | 402 | 754 |
| Dec 2025 | 1,170 | 214 | 287 | 877 |
| Jan 2026 | 1,682 | 432 | 537 | 1,131 |
| Feb 2026 | 1,946 | 408 | 725 | 1,204 |
| Mar 2026 | 2,089 | 472 | 1,094 | 980 |
| Apr 2026 | 2,165 | 471 | 913 | 1,223 |
| May 2026 | 1,711 | 367 | 764 | 928 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/gold-price-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 1.0 | 0.0 |
| Visualisation from counted data | 2.5 | 3.0 | 1.0 | 0.0 |
| Exploration and drill-down | 2.5 | 3.5 | 2.0 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.0 | 1.0 | 1.0 |
| Traceable references | 1.0 | 1.0 | 0.5 | 0.0 |
| Accuracy against the corpus | 3.0 | 4.0 | 3.5 | 4.0 |
| Calibration and limits | 4.5 | 4.0 | 3.0 | 3.0 |
| Decision-grade verdict | 3.0 | 3.5 | 2.0 | 3.0 |
| Facet coverage | 4.5 | 3.5 | 1.0 | 1.5 |
| **Score /100** | 66.8 | **69.8** | 32.2 | 27.2 |

**Claude Opus judge:** D gave a decision-maker the full picture: volume decomposed into critical and tone, the spring-2026 negative turn against baseline, dated critical headlines with URLs, and limits placed where they bite. It has one denominator misreading on geography. A was accurate and tidy, but it charted only volume and missed the tone reversal its own data contained. B and C honestly declined to measure, so they offer scoping, not evidence.

**GPT judge:** B best supports a decision-maker with a traced monthly volume series, a correctly defined tone comparison, and a bounded account of themes and sampled headlines. D covers more facets and charts tone, but its chart window is misleading and its verdict leans on an unsupported price-correction claim; neither deliverable provides fully resolving references for the critical stories.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/gold-price-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/gold-price-pulse.pdf)

## Live MCP session

Here each model was given only the question and a live connection to the Prism MCP server, and chose its own calls.

**Claude** (claude-sonnet, 238.0 s) called 2 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `prism_overview` | `{"term": "gold prices"}` | see payload · – chars |
| 2 | `freshness_status` | `{}` | ok · 735 chars |

<details><summary>Claude's answer</summary>

**Gold-price coverage has roughly doubled and turned more negative since early 2026. Even so, it reads about as negative as ordinary news.**

Window: Jun 2024 to May 2026. News ingest thins after May 2026, so I cut the series there. Today is 22 Oct 2026, so nothing from June–October is included. Source: Prism news corpus, 31,072 articles that mention "gold prices".

**What the data shows**
- **Volume:** Monthly articles rose from 459 (Jun 2024) to a peak of 2,124 (Feb 2026), then 1,755 in May 2026. The latest third of the window had 1.96× the articles of the earliest third. The April 2025 spike (1,915) and the October 2025 spike (2,092) stand out.
- **Tone:** Across the window, 65.5% of articles are positive and 33.6% negative. The negative-to-positive ratio is 0.51, against a corpus baseline of 0.58, so tone is about baseline. March 2026 is the exception: negative articles (1,109) outnumbered positive ones (864), a ratio of 1.28. April and May 2026 stayed elevated at 0.78 and 0.87.
- **Critical share:** 8,753 articles (28%) are flagged critical. The monthly share peaked at 34.7% in Feb 2025 and was 32.5% in Feb 2026. The lowest was 20.2% in Dec 2025.
- **Critical stories (May 2026, priority 8):**
  - Kerala price swings of ₹10,200 on 13 May, then drops of ₹1,640 per pavan on 15 May and a further drop on 18 May, framed around duty-hike protests and smuggling.
  - Delhi gold rebounding ₹800 to ₹1.63 lakh per 10 g on 19 May, as US–Iran talks eased inflation fears.
- **Themes:** The coverage clusters around the Federal Reserve (27% of entity-labelled articles) and Jerome Powell, with Donald Trump named in 42% of articles that name a person. Other recurring themes are the US dollar, interest rates, and trade wars and geopolitics. The leading places are the US (25%) and India (17%), and India's lift is 2.5×.
- **Price levels quoted in coverage:** Gold passed $4,700/oz in early May 2026 and fell below $4,500 late in the month.
- **Concentration:** Coverage is spread across many outlets. In a sample of 217 articles, the top publisher had 10.6%.

**My interpretation**
The rise looks driven by record prices, Fed uncertainty and geopolitics. The March 2026 negative turn probably reflects volatility and sell-offs, not a collapse in interest. This is an inference. I didn't check what happened to prices that month.

**Caveats**
Geography and entity labels are thin for May 2026, and the overview only returned four critical headlines.

</details>

**ChatGPT** (gpt-6-luna, 106.0 s) called 3 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `news_trends` | `{"term": "gold prices", "granularity": "monthly", "since": "2025-10-01"}` | ok · 7,067 chars |
| 2 | `news_sentiment` | `{"term": "gold prices", "granularity": "monthly", "since": "2025-10-01"}` | ok · 5,089 chars |
| 3 | `critical_news` | `{"term": "gold prices", "days": 180, "limit": 12}` | ok · 15,934 chars |

<details><summary>ChatGPT's answer</summary>

Gold coverage was **heavy, broadly positive, then turned sharply more negative in March 2026**. Prism’s indexed data run from **October 2025 through May 2026**; its news window is censored at June 1, so it does not describe coverage since then.

**What the data shows — Prism news corpus:** 13,965 articles across those eight complete months, with monthly volume peaking at **2,124 in February 2026**. **3,935 (28%)** were in Prism’s critical priority bands. Overall, **60.3%** were scored positive and **38.7%** negative; the negative-to-positive ratio was **0.64**, versus a **0.58** corpus baseline. March was the clear reversal: **1,109 negative vs. 864 positive** (ratio **1.28**). Coverage remained substantial in April and May, but sentiment stayed net positive. Prism reports full index partition coverage; this is a corpus count, not a census of all news.  

**Critical stories — retrieved examples:** Coverage tied gold to rate expectations and inflation, including a *LiveMint* story on traders awaiting the Fed decision, and an *Economic Times* report linking gold’s fall to oil-driven inflation worries as US–Iran talks faltered. India-focused stories tracked sharp retail price swings in Kerala and a May rebound as US–Iran tensions eased ([LiveMint](https://www.livemint.com/market/stock-market-news/gold-rates-today-mcx-gold-price-remains-steady-ahead-of-us-federal-reserve-policy-decision-11765377590708.html), [Economic Times](https://economictimes.indiatimes.com/markets/commodities/news/gold-falls-on-oil-driven-inflation-worries-as-usiran-peace-talks-falter/articleshow/131001554.cms), [Daily Excelsior](https://www.dailyexcelsior.com/gold-rebounds-rs-800-to-rs-1-63-lakh-10g-as-easing-us-iran-tensions-spur-buying/)).

**Interpretation:** The narrative is not uniformly “safe-haven bullish”: reporting tracks gold’s sensitivity to rates, inflation and geopolitical risk, with local price moves adding volatility. The tone figures describe article labels, not market positioning or investor sentiment.

</details>

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is the news narrative around gold prices: volume, tone, and the critical stories?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "gold price", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'gold price', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
