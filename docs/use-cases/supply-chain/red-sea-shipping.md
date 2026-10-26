# Red Sea shipping disruption

[Supply chain & trade](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A chokepoint monitor for a logistics team.  
> **Why it is hard.** Houthi attacks since late 2023; coverage geography spans Asia and Europe.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [red-sea-shipping.json](../../examples/red-sea-shipping.json).

**The question:**

> What is the coverage of Red Sea shipping disruption: tone, places, critical stories?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “red sea shipping”, Jun 2024 – May 2026 | 455 |
| Critical coverage (priority 7–9) | 430 (94.5%) |
| Peak month | Mar 2025 (126 articles) |
| Last third of the window vs first third | 1.21× (flat) |
| Negative · positive | 78.9% · 20.2% |
| Tone vs all news (negative-to-positive ratio) | 3.9 vs 0.58 baseline: *markedly more negative than ordinary news coverage* |
| What Prism thinks “red sea shipping” is | topic |

![Monthly coverage of red sea shipping](../img/red-sea-shipping-trend.svg)

![Tone of red sea shipping coverage](../img/red-sea-shipping-tone.svg)

![Countries in red sea shipping coverage](../img/red-sea-shipping-geo.svg)

![Themes in red sea shipping coverage](../img/red-sea-shipping-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “red sea shipping” coverage (they also name the companies, people and places it is written about with): red sea (450), the red sea (289), yemen (286), israel (284), gaza (192), hamas (147), hezbollah (77), shipping (45), supreme (42), syria (42), nuclear program (39), east coast (34)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| maersk | bashar al-assad | united states |
| hapag-lloyd | michael waltz | yemen |
| east coast | sergey lavrov | israel |
| cma cgm | hassan nasrallah | iran |
| west coast | abdel fattah el-sisi | palestine |
| theprint | lloyd austin | lebanon |

**Top publishers in a 12-article sample:** thenationalnews.com (16.7%), mathrubhumi.com (8.3%), theloadstar.com (8.3%), straitstimes.com (8.3%), theprint.in (8.3%), hindustantimes.com (8.3%)

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 15 | 14 | 8 | 7 |
| Jul 2024 | 23 | 22 | 19 | 4 |
| Aug 2024 | 8 | 8 | 4 | 4 |
| Sep 2024 | 15 | 12 | 10 | 5 |
| Oct 2024 | 12 | 11 | 10 | 2 |
| Nov 2024 | 7 | 6 | 3 | 4 |
| Dec 2024 | 11 | 10 | 9 | 1 |
| Jan 2025 | 19 | 18 | 17 | 2 |
| Feb 2025 | 8 | 7 | 6 | 2 |
| Mar 2025 | 126 | 124 | 120 | 3 |
| Apr 2025 | 23 | 22 | 19 | 4 |
| May 2025 | 23 | 21 | 18 | 5 |
| Jun 2025 | 6 | 6 | 4 | 2 |
| Jul 2025 | 15 | 10 | 13 | 2 |
| Aug 2025 | 10 | 9 | 9 | 1 |
| Sep 2025 | 1 | 1 | 1 | 0 |
| Oct 2025 | 4 | 4 | 4 | 0 |
| Nov 2025 | 2 | 1 | 2 | 0 |
| Dec 2025 | 2 | 2 | 2 | 0 |
| Jan 2026 | 7 | 6 | 6 | 1 |
| Feb 2026 | 45 | 45 | 14 | 31 |
| Mar 2026 | 51 | 49 | 45 | 6 |
| Apr 2026 | 8 | 8 | 7 | 1 |
| May 2026 | 14 | 14 | 9 | 5 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/red-sea-shipping-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.5 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 0.5 | 0.0 |
| Visualisation from counted data | 4.0 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 2.5 | 1.0 | 1.5 | 1.0 |
| Data export with provenance | 2.5 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 5.0 | 1.0 | 1.0 |
| Traceable references | 1.0 | 1.0 | 0.5 | 0.5 |
| Accuracy against the corpus | 3.5 | 3.5 | 3.0 | 4.0 |
| Calibration and limits | 4.0 | 4.0 | 3.0 | 2.5 |
| Decision-grade verdict | 3.5 | 3.0 | 2.0 | 2.5 |
| Facet coverage | 4.0 | 4.0 | 1.0 | 0.5 |
| **Score /100** | **72.4** | 70.5 | 29.6 | 24.8 |

**Claude Opus judge:** A and D both traced every number to the Prism overview and stated window, censoring and the gap to today. A gave the decision-maker more: two critical headlines with URLs, the February 2026 positive-tone anomaly, the second volume bump, and a sharper framing decision. D had the cleaner full export. B and C honestly declined to measure, so they offer only framing for a decision.

**GPT judge:** D is the strongest decision aid: it supplies a reproducible monthly series, a correctly computed tone comparison, useful place and theme context, and specific limits around matching, enrichment, and sampling. B covers more facets and adds subthemes, but its critical-headline claims overreach the bounded empty result; neither database-backed report establishes a reliable ranking of the critical stories.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/red-sea-shipping/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/red-sea-shipping.pdf)

## Live MCP session

Here each model was given only the question and a live connection to the Prism MCP server, and chose its own calls.

**Claude** (claude-sonnet, 257.6 s) called 3 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `prism_overview` | `{"term": "Red Sea shipping disruption"}` | ok · 26,037 chars |
| 2 | `critical_news` | `{}` | see payload · 77 chars |
| 3 | `critical_news` | `{"term": "Red Sea", "days": 400, "limit": 8}` | see payload · 1,721 chars |

<details><summary>Claude's answer</summary>

**Direct answer:** Prism has very little coverage under this exact phrase. It found 14 articles between June 2024 and May 2026, and Prism flags anything under 25 articles as too thin to report on. What there is leans negative. I could not retrieve any headlines.

**What the data shows** (window 2024-06 to 2026-05, news corpus):
- **Volume:** 14 articles in total, spread across only 6 months. July 2024 was the peak with 4. March 2026 had 1 and May 2026 had 3. Prism labels the direction "falling" (late third 4 articles against early third 6), but with counts this small that label is weak.
- **Tone:** 9 of 14 articles were negative (64%) and 5 were positive (36%). That is a negative-to-positive ratio of 1.8 against a corpus baseline of 0.58, so about 3.1 times more negative than ordinary news.
- **Criticality:** 12 of the 14 articles (86%) were flagged critical. Mean priority was 6–7.5 in the months with coverage.
- **Places** (only 5 of 11 matched articles were placed, so treat as indicative):
  - China 4 articles.
  - United States, Vietnam, Australia, Iran and Singapore 2 each.
  - UAE, Indonesia, Malaysia, Israel and Thailand 1 each.
- **Themes and entities:**
  - Themes were trade, supply chain, maritime freight, oil and insurance.
  - The organisation most often named was Maersk, in 2 articles, and Louise Rasmussen was the only person named.
  - AD Ports Group, Xeneta and Temu also appeared.
  - Entity labels are machine-assigned and unverified.
- **Critical stories:** The recent-news and critical-news feeds returned nothing for this phrase. A broader "Red Sea" search over 2025-04 to 2026-05 also returned no articles after relevance and duplicate filtering. I therefore cannot name specific critical stories.

**Interpretation (mine, not measured):**
- The corpus appears to hold almost no articles about this topic under these tags. That probably reflects how the topic is labelled or tagged, not the real volume of coverage.
- Red Sea disruption is likely folded into broader freight, tariff and supply-chain stories. That would fit the "tariffs", "exports" and "FY26" tags.
- Because the sample is so small, the negative tone and the "falling" trend are suggestive only.
- Place labels, including Iran and Israel, may reflect incidental mentions, not the location of the disruption.
- News labelling also lags after about April 2026, so the latest months are the least reliable.

**Suggested next step:** Re-run with narrower terms such as "Houthi", "Suez Canal", "Maersk rerouting" or "container freight rates" to get a reportable sample.

</details>

**ChatGPT** (gpt-6-luna, 349.6 s) called 9 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `prism_overview` | `{"term": "Red Sea shipping disruption", "since": "2026-07-22", "until": "2026-10-22", "granularity": "week"}` | see payload · 757 chars |
| 2 | `resolve_term` | `{"term": "Red Sea shipping"}` | ok · 3,617 chars |
| 3 | `news_sentiment` | `{"term": "Red Sea shipping", "since": "2024-06-01", "until": "2026-06-01", "granularity": "month"}` | see payload · 683 chars |
| 4 | `prism_overview` | `{"term": "Red Sea shipping", "since": "2024-06-01", "until": "2026-06-01", "granularity": "month"}` | ok · 55,992 chars |
| 5 | `news_geography` | `{"term": "Red Sea shipping", "since": "2024-06-01", "until": "2026-06-01", "granularity": "month", "level": "country", "limit": 10}` | ok · 5,697 chars |
| 6 | `critical_news` | `{"term": "Red Sea shipping", "days": 730, "limit": 10}` | ok · 11,587 chars |
| 7 | `news_geography` | `{"term": "Red Sea shipping", "since": "2024-06-01", "until": "2026-06-01", "level": "country", "limit": 10}` | ok · 5,727 chars |
| 8 | `news_sentiment` | `{"term": "Red Sea shipping", "since": "2024-06-01", "until": "2026-06-01", "granularity": "monthly"}` | ok · 7,919 chars |
| 9 | `critical_news` | `{"term": "Red Sea shipping", "days": 730, "limit": 10}` | ok · 11,593 chars |

<details><summary>ChatGPT's answer</summary>

**Prism’s Red Sea shipping coverage is strongly negative, centered on Yemen and the wider regional conflict, with top-priority stories focused on US strikes and Houthi attacks.** The figures below use Prism’s news corpus for **1 June 2024–31 May 2026**; it censors coverage after May because newer news ingest is incomplete.

**What the data shows.** Prism resolved **455 articles** for “Red Sea shipping.” Among them, **359 were negative (78.9%)**, **92 positive (20.2%)**, and **4 neutral**. Negative coverage outnumbered positive coverage **3.9 to 1**; Prism’s same-window general-news baseline was **0.58 to 1**. The strongest monthly skew was March 2025: **120 negative vs. 3 positive**.

Geography is available for **339 of 441 matched articles (76.9%)**. Labels overlap: the most frequent were **United States (282)**, **Yemen (256)**, **Israel (233)** and **Iran (211)**. These are places articles were *about*, not where outlets are based.

Prism returned **4 of 10 requested critical-story records**; six were unavailable in its article store. The retrieved top-priority stories include DW’s [report on Trump’s strikes against the Houthis](https://www.dw.com/es/trump-ordena-ataque-decisivo-y-contundente-contra-los-hut%C3%ADes/a-71933637) (15 March 2025), *The Deccan Chronicle*’s [report on US strikes in Yemen](https://www.deccanchronicle.com/world/middle-east/us-strikes-in-yemen-kill-20-as-trump-vows-to-end-houthi-attacks-1867132) and *Hindustan Times’* [report on further US action](https://www.hindustantimes.com/world-news/us-news/us-vows-unrelenting-campaign-to-halt-huthi-ship-attacks-101742142128233.html) (both 16 March 2025).

**Interpretation.** Coverage frames shipping disruption chiefly through military escalation and regional geopolitics, rather than as a standalone logistics story. The March 2025 tone spike aligns with the retrieved strike coverage; it does not establish that those events alone caused the spike.

</details>

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is the coverage of Red Sea shipping disruption: tone, places, critical stories?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "red sea shipping", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'red sea shipping', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
