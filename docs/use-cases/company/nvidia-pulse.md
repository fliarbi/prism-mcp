# NVIDIA media intelligence

[Company & competitive intelligence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A full company media profile for an equity analyst.  
> **Why it is hard.** Entity names are canonical ('nvidia corporation'); matching must be by entity, not word.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [nvidia-pulse.json](../../examples/nvidia-pulse.json).

**The question:**

> What is the world saying about NVIDIA: coverage volume, tone, themes, related companies and places?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “nvidia”, Jun 2024 – May 2026 | 232,502 |
| Critical coverage (priority 7–9) | 164,123 (70.6%) |
| Peak month | Feb 2026 (15,514 articles) |
| Last third of the window vs first third | 1.83× (rising) |
| Negative · positive | 25.8% · 73.5% |
| Tone vs all news (negative-to-positive ratio) | 0.35 vs 0.58 baseline: *markedly more positive than ordinary news coverage* |
| What Prism thinks “nvidia” is | organization |

![Monthly coverage of nvidia](../img/nvidia-pulse-trend.svg)

![Tone of nvidia coverage](../img/nvidia-pulse-tone.svg)

![Countries in nvidia coverage](../img/nvidia-pulse-geo.svg)

![Themes in nvidia coverage](../img/nvidia-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “nvidia” coverage (they also name the companies, people and places it is written about with): nvidia (218,510), microsoft (53,530), gpu (40,531), jensen huang (33,259), amd (31,984), intel (30,076), nvda (25,349), alphabet (18,339), oracle (14,389), huang (13,678), tsmc (13,201), broadcom (8,745)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| nvidia | jensen huang | united states |
| supermicro | lip-bu tan | china |
| softbank group | vera rubin | colombia |
| intel | jim cramer | united kingdom |
| the motley fool | sam altman | japan |
| tsmc | chris malachowsky | india |

**Top publishers in a 222-article sample:** fool.com (13.5%), xda-developers.com (5.9%), fortune.com (3.6%), theverge.com (3.6%), theglobeandmail.com (3.6%), panewslab.com (2.7%)

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 7,439 | 5,155 | 1,357 | 6,028 |
| Jul 2024 | 5,643 | 3,695 | 1,399 | 4,219 |
| Aug 2024 | 6,577 | 4,472 | 2,110 | 4,417 |
| Sep 2024 | 5,950 | 4,183 | 1,632 | 4,278 |
| Oct 2024 | 6,405 | 4,603 | 1,175 | 5,190 |
| Nov 2024 | 6,717 | 4,533 | 1,523 | 5,140 |
| Dec 2024 | 5,796 | 3,891 | 1,528 | 4,223 |
| Jan 2025 | 12,580 | 8,232 | 3,934 | 8,553 |
| Feb 2025 | 8,130 | 5,364 | 2,506 | 5,560 |
| Mar 2025 | 9,582 | 6,549 | 2,744 | 6,791 |
| Apr 2025 | 9,400 | 6,700 | 3,812 | 5,512 |
| May 2025 | 7,873 | 5,423 | 1,982 | 5,841 |
| Jun 2025 | 5,563 | 3,498 | 885 | 4,652 |
| Jul 2025 | 7,941 | 5,101 | 1,849 | 6,047 |
| Aug 2025 | 10,733 | 7,696 | 3,576 | 7,057 |
| Sep 2025 | 11,887 | 8,467 | 2,583 | 9,200 |
| Oct 2025 | 11,287 | 9,042 | 2,288 | 8,954 |
| Nov 2025 | 14,365 | 10,869 | 4,364 | 9,911 |
| Dec 2025 | 11,429 | 8,082 | 3,006 | 8,181 |
| Jan 2026 | 11,194 | 7,492 | 2,358 | 8,762 |
| Feb 2026 | 15,514 | 10,940 | 3,579 | 11,840 |
| Mar 2026 | 13,745 | 10,119 | 3,021 | 10,617 |
| Apr 2026 | 11,815 | 8,573 | 2,504 | 9,235 |
| May 2026 | 14,937 | 11,444 | 4,136 | 10,593 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/nvidia-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.5 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 0.5 | 0.0 |
| Visualisation from counted data | 4.0 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 2.5 | 3.5 | 1.0 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 3.5 | 0.0 | 1.0 |
| Traceable references | 1.0 | 1.0 | 0.5 | 0.5 |
| Accuracy against the corpus | 4.0 | 4.0 | 3.0 | 3.0 |
| Calibration and limits | 3.0 | 3.0 | 2.5 | 3.5 |
| Decision-grade verdict | 4.0 | 3.5 | 2.5 | 2.0 |
| Facet coverage | 5.0 | 4.5 | 1.0 | 1.5 |
| **Score /100** | **75.2** | 70.2 | 26.9 | 24.0 |

**Claude Opus judge:** A and D both delivered measured answers from the same overview call. D went further: it decomposed volume into critical and total, distinguished critical from negative, flagged the Colombia place-resolution artefact, and exported both the monthly and the country tables. B and C honestly declined to measure, but that left a decision-maker with no usable figures. C's market-cap proxy does not measure coverage.

**GPT judge:** D gives the strongest decision-ready account: it traces both total and critical volume, compares tone against a defined baseline, and distinguishes critical flags from negative polarity while covering themes, entities and places. C is close, but D provides a fuller traced trend decomposition and export; its main weaknesses are the claim of completeness and limited successful drill-downs.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/nvidia-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/nvidia-pulse.pdf)

## Live MCP session

Here each model was given only the question and a live connection to the Prism MCP server, and chose its own calls.

**Claude** (claude-sonnet, 226.4 s) called 1 Prism tool:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `prism_overview` | `{"term": "NVIDIA"}` | ok · 33,065 chars |

<details><summary>Claude's answer</summary>

**NVIDIA coverage is large, still growing, and more positive than ordinary news. It centres on AI chips, the US and China, and the other big AI firms.** The window is June 2024 to May 2026, from Prism's news corpus. Prism's cutoff is 1 June 2026, so nothing after that is included.

**What the data shows**
- **Volume:** 232,502 articles mention NVIDIA. Monthly volume rose from 7,439 in June 2024 to 14,937 in May 2026, and the peak was 15,514 in February 2026. The late third of the window had 1.83 times the early third, which is about 44% annualised growth.
- **Tone:** Of the articles with a sentiment label, 73.5% are positive and 25.8% are negative. The negative-to-positive ratio is 0.35, against a corpus baseline of 0.58, so NVIDIA coverage is markedly more positive than typical news. The ratio peaked at 0.69 in April 2025.
- **Criticality:** 164,123 articles (about 71%) are in the high-priority "critical" band, which Prism says holds geopolitics, disasters and regulation. That share rose to 80.1% in October 2025 and 76.6% in May 2026. Priority is not the same as negative tone.
- **Themes (by lift over the corpus norm):**
  - GPUs, semiconductor industry updates, AI hardware acceleration and earnings.
  - Gaming and cloud computing.
  - Stock and market coverage.
- **Related companies:**
  - Intel, Microsoft, OpenAI, TSMC, SoftBank, Broadcom, SK Hynix and Supermicro.
  - AMD, Alphabet and Oracle also appear in the tags.
- **People:** Jensen Huang appears in about 18% of the entity-labelled articles. Sam Altman, Lip-Bu Tan and Satya Nadella also show up.
- **Places:** Only 51.6% of articles could be placed. Among those, the US has 30.9%, China 12.1%, then Colombia, the UK, Japan, India, South Korea and Taiwan.
- **Sources:** A sample of 222 articles came from 107 outlets. The top outlet, Motley Fool, had 13.5%, so no single newsroom dominates.

**Interpretation (mine, not measured)**
- The coverage reads as NVIDIA being treated as the bellwether of the AI buildout. Stock stories, the OpenAI and Microsoft ties, and US–China chip tensions fit that. I haven't checked individual articles to confirm it.
- The rising critical share suggests more geopolitical and market-risk framing, not hostile tone, since sentiment stayed positive.
- Colombia's 5.3% share (lift 10.9) is odd. It may be a place-resolution artefact, which Prism warns about, so I'd distrust it.

**Caveats**
- Entity and place labels are machine-assigned.
- Labelling lags for May 2026, with fill rates of about 4%. The entity and place panels therefore use data through April.
- Only one recent article was returned, and Prism's critical-news panel came back empty.

</details>

**ChatGPT** (gpt-6-luna, 137.8 s) called 6 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `news_trends` | `{"term": "NVIDIA", "since": "2026-04-01", "until": "2026-05-31", "limit": 8}` | ok · 4,115 chars |
| 2 | `news_sentiment` | `{"term": "NVIDIA", "since": "2026-04-01", "until": "2026-05-31", "limit": 8}` | ok · 3,963 chars |
| 3 | `news_themes` | `{"term": "NVIDIA", "since": "2026-04-01", "until": "2026-05-31", "limit": 8}` | ok · 11,731 chars |
| 4 | `news_geography` | `{"term": "NVIDIA", "since": "2026-04-01", "until": "2026-05-31", "limit": 8}` | ok · 5,411 chars |
| 5 | `news_entities` | `{"term": "NVIDIA", "since": "2026-04-01", "until": "2026-05-31", "limit": 8}` | ok · 10,293 chars |
| 6 | `news_themes` | `{"term": "NVIDIA", "since": "2026-04-01", "until": "2026-05-31", "limit": 6}` | ok · 10,213 chars |

<details><summary>ChatGPT's answer</summary>

**Direct answer:** NVIDIA drew heavy, predominantly positive coverage, centered on AI, GPUs, semiconductors and financial performance. Coverage connected it to major chipmakers, cloud companies and several countries.

**What Prism’s data shows**

- **Volume and tone — April 1–May 31, 2026:** 26,507 articles; 19,826 were marked critical. Sentiment classified 19,652 as positive (74.2%) and 6,572 as negative (24.8%). The negative-to-positive ratio was 0.33, versus a 0.62 news-corpus baseline. May’s volume is flagged partial, so the two-month total is not a clean comparison. *(Prism `news.trends`, `news.sentiment`; NVIDIA mentions.)*
- **Themes — same window:** technology appeared in 21,145 articles, business in 20,091, and finance in 11,374. Among subcategories, AI advancements appeared in 2,643, semiconductor-industry updates in 1,686, and GPU coverage in 542. Labels can overlap. *(Prism `news.themes`.)*
- **Related entities and places — April 2026:** company labels included Microsoft (1,860 articles), Intel (1,206), TSMC (541), Broadcom (482) and CoreWeave (238). The most-mentioned countries were the United States (3,900), China (974), Colombia (826) and Iran (811). Entity labels are automated; places mean the country an article is about, not where it was published. *(Prism `news.entities`, `news.geography`; enrichment through May 1.)*

**Interpretation**

Coverage reads as commercially upbeat and tightly tied to the AI infrastructure cycle, while the high “critical” share signals editorial priority, not necessarily negative sentiment. Geography and entity results lagged the article feed, so they describe April rather than the full two-month volume. Prism’s news window is censored at June 1 because later ingestion is incomplete.

</details>

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is the world saying about NVIDIA: coverage volume, tone, themes, related companies and places?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "nvidia", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'nvidia', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
