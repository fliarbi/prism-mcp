# GST in Indian news

[Policy & regulation](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Indian tax-policy media tracking.  
> **Why it is hard.** GST 2.0 rate rationalisation in 2025 changed the tone.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [gst-india-pulse.json](../../examples/gst-india-pulse.json).

**The question:**

> What has the news said about India's GST Council and GST rate changes over the last two years?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “gst council”, Jun 2024 – May 2026 | 5,535 |
| Critical coverage (priority 7–9) | 4,007 (72.4%) |
| Peak month | Sep 2025 (2,430 articles) |
| Last third of the window vs first third | 0.22× (falling) |
| Negative · positive | 27.8% · 64.7% |
| Tone vs all news (negative-to-positive ratio) | 0.43 vs 0.58 baseline: *somewhat more positive than ordinary news coverage* |
| What Prism thinks “gst council” is | topic |

![Monthly coverage of gst council](../img/gst-india-pulse-trend.svg)

![Tone of gst council coverage](../img/gst-india-pulse-tone.svg)

![Countries in gst council coverage](../img/gst-india-pulse-geo.svg)

![Themes in gst council coverage](../img/gst-india-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “gst council” coverage (they also name the companies, people and places it is written about with): gst (4,244), council (1,482), centre (1,114), taxation (905), tax reform (721), health insurance (578), bihar (563), tax policy (401), tax (281), states (252), customs (220), tata motors (202)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| gst | nirmala sitharaman | india |
| itc | nitin gadkari | cameroon |
| swiggy | harpal singh cheema | united states |
| finance commission | narendra modi | china |
| hindustan unilever | p. chidambaram | japan |
| ultratech cement | vinod kumar alva | united kingdom |

**Top publishers in a 215-article sample:** livemint.com (9.3%), navbharattimes.indiatimes.com (6.5%), jagran.com (5.6%), livehindustan.com (5.6%), zeebiz.com (4.7%), thehindubusinessline.com (3.7%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-05-04 | [Exclusive: Tamil Nadu, Kerala, West Bengal & Puducherry poll results set to rewire GST Council power dynamics - CNBC TV1](https://www.cnbctv18.com/india/exclusive-tamil-nadu-kerala-west-bengal-puducherry-poll-results-set-to-rewire-gst-council-power-dynamics-ws-l-19898476.htm) | cnbctv18.com | 8 | slight_pos |
| 2026-02-03 | [Next GST Council likely to focus on registration, audit, refunds beside others](https://www.thehindubusinessline.com/economy/next-gst-council-likely-to-focus-on-registration-audit-refunds-beside-others/article70588036.ece) | thehindubusinessline.com | 8 | slight_pos |
| 2026-05-04 | [With state elections over, GST Council to get a new look - BusinessToday](https://www.businesstoday.in/india/story/with-state-elections-over-gst-council-to-get-a-new-look-529703-2026-05-04) | businesstoday.in | 8 | none |
| 2026-05-27 | [International Road Federation seeks GST cut on helmets, ambulances, essential medical equipment](https://www.thehindubusinessline.com/news/international-road-federation-seeks-gst-cut-on-helmets-ambulances-essential-medical-equipment/article71028521.ece) | thehindubusinessline.com | 8 | very_pos |
| 2026-04-15 | [GST Council clears rules, states agree to July 1 rollout \| Autocar Professional](https://www.autocarpro.in/news-national/gst-council-clears-rules-agree-july-24882) | autocarpro.in | 8 | slight_pos |
| 2026-05-27 | [SC ruling on GST levy for online gaming firms may squeeze margins: Tax experts](https://m.dailyhunt.in/news/india/english/millennium+post-epaper-millpost/sc+ruling+on+gst+levy+for+online+gaming+firms+may+squeeze+margins+tax+experts-newsid-n713948680) | m.dailyhunt.in | 8 | slight_neg |
| 2026-04-21 | [Worker protests: How higher wages and the viability of industry can be the win-win India needs \| Mint](https://www.livemint.com/opinion/online-views/worker-protests-higher-wages-industry-win-win-india-noida-factory-uttar-pradesh-labour-codes-11776673140527.html) | livemint.com | 7 | slight_neg |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 327 | 269 | 77 | 189 |
| Jul 2024 | 117 | 93 | 36 | 70 |
| Aug 2024 | 135 | 101 | 44 | 67 |
| Sep 2024 | 411 | 315 | 117 | 259 |
| Oct 2024 | 81 | 67 | 22 | 57 |
| Nov 2024 | 96 | 74 | 13 | 65 |
| Dec 2024 | 606 | 374 | 185 | 372 |
| Jan 2025 | 59 | 45 | 24 | 34 |
| Feb 2025 | 83 | 66 | 21 | 59 |
| Mar 2025 | 44 | 33 | 12 | 28 |
| Apr 2025 | 18 | 12 | 5 | 9 |
| May 2025 | 61 | 30 | 11 | 39 |
| Jun 2025 | 58 | 47 | 23 | 27 |
| Jul 2025 | 87 | 58 | 28 | 45 |
| Aug 2025 | 523 | 393 | 151 | 330 |
| Sep 2025 | 2,430 | 1,695 | 599 | 1,714 |
| Oct 2025 | 80 | 69 | 25 | 55 |
| Nov 2025 | 46 | 33 | 20 | 25 |
| Dec 2025 | 99 | 94 | 48 | 44 |
| Jan 2026 | 41 | 36 | 24 | 15 |
| Feb 2026 | 36 | 32 | 14 | 20 |
| Mar 2026 | 20 | 17 | 10 | 10 |
| Apr 2026 | 36 | 23 | 8 | 26 |
| May 2026 | 41 | 31 | 20 | 20 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/gst-india-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 1.5 | 0.0 |
| Visualisation from counted data | 4.0 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 2.0 | 1.5 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 4.0 | 0.0 | 1.0 |
| Traceable references | 1.0 | 1.0 | 0.5 | 0.5 |
| Accuracy against the corpus | 4.5 | 4.0 | 2.5 | 3.0 |
| Calibration and limits | 4.5 | 4.0 | 3.5 | 3.0 |
| Decision-grade verdict | 4.0 | 3.5 | 3.0 | 2.0 |
| Facet coverage | 4.5 | 3.5 | 1.5 | 0.5 |
| **Score /100** | **80.3** | 68.7 | 31.2 | 22.0 |

**Claude Opus judge:** A and C both measured the coverage, but A went further. It traced every number, separated the critical flag from polarity, caught the Cameroon and 'GST' label artefacts, and gave linkable headlines and the late-window tone turn. B offered accurate but unmeasured recall of the GST 2.0 events, and D declined to answer.

**GPT judge:** A is the strongest decision aid: it traces the full monthly news series, quantifies attention and tone against a defined baseline, and gives unusually specific limits and follow-up paths. B is cleaner but leaves out available trend decomposition and tone charting; C offers unverified recollection, while D is candid but supplies almost no measured answer.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/gst-india-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/gst-india-pulse.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What has the news said about India's GST Council and GST rate changes over the last two years?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "gst council", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'gst council', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
