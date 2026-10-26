# Quick commerce in India

[Consumer, brands & media](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A sector narrative for a retail strategist.  
> **Why it is hard.** Blinkit, Zepto and Instamart; dark-store regulation stories.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [quick-commerce-pulse.json](../../examples/quick-commerce-pulse.json).

**The question:**

> What is the news saying about quick commerce in India?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “quick commerce”, Jun 2024 – May 2026 | 8,153 |
| Critical coverage (priority 7–9) | 5,096 (62.5%) |
| Peak month | Jan 2025 (639 articles) |
| Last third of the window vs first third | 0.81× (flat) |
| Negative · positive | 17.1% · 82.5% |
| Tone vs all news (negative-to-positive ratio) | 0.21 vs 0.58 baseline: *markedly more positive than ordinary news coverage* |
| What Prism thinks “quick commerce” is | topic |

![Monthly coverage of quick commerce](../img/quick-commerce-pulse-trend.svg)

![Tone of quick commerce coverage](../img/quick-commerce-pulse-tone.svg)

![Countries in quick commerce coverage](../img/quick-commerce-pulse-geo.svg)

![Themes in quick commerce coverage](../img/quick-commerce-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “quick commerce” coverage (they also name the companies, people and places it is written about with): india (4,770), e-commerce (1,946), retail (1,631), bengaluru (1,624), mumbai (1,515), flipkart (1,385), ipo (1,168), yoy (540), gurugram (361), market share (339), online shopping (310), bangalore (265)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| zepto | motilal oswal financial services | india |
| blinkit | bonita ely | united states |
| zomato | aesop | china |
| swiggy | mansukh mandaviya | united kingdom |
| flipkart | piyush goyal | singapore |
| d2c | p. v. sindhu | japan |

**Top publishers in a 215-article sample:** financialexpress.com (5.1%), livemint.com (4.2%), linkedin.com (4.2%), livehindustan.com (3.3%), cnbctv18.com (3.3%), business-standard.com (3.3%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-03-09 | [Nitro Commerce Acquires Zodiac Labs AI - Entrepreneur News Network](https://entrepreneurnewsnetwork.com/2026/03/09/nitro-commerce-acquires-zodiac-labs-ai/) | entrepreneurnewsnetwork.com | 8 | very_pos |
| 2026-02-25 | [Quick Commerce to Reach $40B in India by 2030: McKinsey](https://www.newkerala.com/news/a/quick-commerce-growing-fastest-digital-commerce-segment-reach-177.htm) | newkerala.com | 8 | very_pos |
| 2026-05-06 | [AI in E-commerce: Enabling the next phase of growth and innovation - The Economic Times](https://economictimes.indiatimes.com/ai/ai-insights/ai-in-e-commerce-enabling-the-next-phase-of-growth-and-innovation/printarticle/130852107.cms) | economictimes.indiatimes.com | 8 | very_pos |
| 2026-04-14 | [Eternal: Can Blinkit Sustain Growth as 50% TAM Penetration Nears Maturity?](https://tradebrains.in/eternal-can-blinkit-sustain-growth-as-50-tam-penetration-nears-maturity/) | tradebrains.in | 8 | slight_pos |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 193 | 147 | 22 | 171 |
| Jul 2024 | 141 | 83 | 16 | 125 |
| Aug 2024 | 363 | 255 | 52 | 307 |
| Sep 2024 | 352 | 206 | 53 | 299 |
| Oct 2024 | 468 | 263 | 91 | 374 |
| Nov 2024 | 475 | 320 | 78 | 389 |
| Dec 2024 | 469 | 272 | 62 | 407 |
| Jan 2025 | 639 | 411 | 132 | 506 |
| Feb 2025 | 349 | 201 | 54 | 295 |
| Mar 2025 | 399 | 238 | 92 | 305 |
| Apr 2025 | 351 | 172 | 56 | 294 |
| May 2025 | 322 | 181 | 70 | 251 |
| Jun 2025 | 213 | 141 | 42 | 169 |
| Jul 2025 | 339 | 214 | 67 | 270 |
| Aug 2025 | 289 | 150 | 37 | 250 |
| Sep 2025 | 293 | 158 | 26 | 265 |
| Oct 2025 | 259 | 171 | 43 | 216 |
| Nov 2025 | 190 | 110 | 26 | 163 |
| Dec 2025 | 297 | 204 | 54 | 241 |
| Jan 2026 | 380 | 284 | 141 | 235 |
| Feb 2026 | 234 | 157 | 22 | 211 |
| Mar 2026 | 315 | 193 | 32 | 282 |
| Apr 2026 | 442 | 284 | 50 | 391 |
| May 2026 | 381 | 281 | 74 | 306 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/quick-commerce-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 3.5 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.0 | 2.0 | 0.5 |
| Visualisation from counted data | 3.0 | 3.0 | 1.0 | 0.0 |
| Exploration and drill-down | 3.5 | 2.0 | 1.0 | 2.0 |
| Data export with provenance | 3.0 | 4.5 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 5.0 | 1.0 | 1.0 |
| Traceable references | 1.0 | 1.0 | 0.5 | 0.5 |
| Accuracy against the corpus | 4.0 | 4.0 | 3.0 | 3.0 |
| Calibration and limits | 4.5 | 4.5 | 3.0 | 3.0 |
| Decision-grade verdict | 4.0 | 3.5 | 3.5 | 2.0 |
| Facet coverage | 3.5 | 3.0 | 1.0 | 0.0 |
| **Score /100** | **72.8** | 71.0 | 34.6 | 23.5 |

**Claude Opus judge:** A and B both answer from the traced overview with correct trend and tone-versus-baseline numbers. B goes further: it names dated critical headlines with URLs, decomposes critical versus negative, and catches entity and place anomalies. A has cleaner provenance and fewer slips. C and D are honest but measure nothing; C offers memory estimates and D declines entirely.

**GPT judge:** C best combines a quantified trend, tone comparison, grounded themes and entities, and a clear warning that “critical” is not the same as negative. D has cleaner exports and stronger reproducibility, but its trend reading is less complete and its follow-up drill-downs mostly did not execute; neither deliverable fully resolves dark-store regulation or the brand-versus-generic comparison.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/quick-commerce-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/quick-commerce-pulse.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is the news saying about quick commerce in India?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "quick commerce", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'quick commerce', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
