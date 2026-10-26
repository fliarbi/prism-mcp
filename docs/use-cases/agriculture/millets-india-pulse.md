# Millets in Indian news

[Agriculture & food security](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A food-policy and market narrative.  
> **Why it is hard.** International Year of Millets 2023 created a spike; what remains after?  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [millets-india-pulse.json](../../examples/millets-india-pulse.json).

**The question:**

> What is the news saying about millets in India?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “millets”, Jun 2024 – May 2026 | 1,589 |
| Critical coverage (priority 7–9) | 651 (41%) |
| Peak month | Sep 2024 (134 articles) |
| Last third of the window vs first third | 0.55× (falling) |
| Negative · positive | 8.3% · 91.3% |
| Tone vs all news (negative-to-positive ratio) | 0.09 vs 0.58 baseline: *markedly more positive than ordinary news coverage* |
| What Prism thinks “millets” is | topic |

![Monthly coverage of millets](../img/millets-india-pulse-trend.svg)

![Tone of millets coverage](../img/millets-india-pulse-tone.svg)

![Countries in millets coverage](../img/millets-india-pulse-geo.svg)

![Themes in millets coverage](../img/millets-india-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “millets” coverage (they also name the companies, people and places it is written about with): agriculture (414), nutrition (299), food (262), food industry (169), food security (117), farming (96), diet (67), farmers (63), msp (58), breakfast (49), snacks (38), rice (37)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| marico | shivraj singh chouhan | india |
| theprint | tony abbott | united states |
| tata consumer products | narendra modi | united kingdom |
| fci | bhupendrabhai patel | cameroon |
| united nations general assembly | mohan charan majhi | china |
| debenhams | vallabhbhai patel | canada |

**Top publishers in a 200-article sample:** livehindustan.com (14.5%), amarujala.com (4%), pubmed.ncbi.nlm.nih.gov (3.5%), etvbharat.com (3%), timesofindia.indiatimes.com (3%), indianexpress.com (3%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-04-12 | [Advisory To States On Crop Bonus Policy To Encourage Greater Crop Diversification: FinMin](https://www.etvbharat.com/en/business/advisory-to-states-on-crop-bonus-policy-to-encourage-greater-crop-diversification-says-finmin-enn26041204597) | etvbharat.com | 8 | slight_pos |
| 2026-04-12 | [Advisory to states on crop bonus policy to encourage greater crop diversification: FinMin](https://economictimes.indiatimes.com/news/economy/agriculture/advisory-to-states-on-crop-bonus-policy-to-encourage-greater-crop-diversification-finmin/articleshow/130210891.cms) | economictimes.indiatimes.com | 8 | slight_pos |
| 2026-04-12 | [Centre Refutes TN CM's Claim on Crop Bonus Policy](https://www.newkerala.com/news/a/only-advisory-centre-refutes-tamil-nadu-cms-claim-557.htm) | newkerala.com | 8 | slight_pos |
| 2026-02-01 | [Revisiting minor millets as an underutilised super food for enduring global food security.](https://pubmed.ncbi.nlm.nih.gov/41704875/) | pubmed.ncbi.nlm.nih.gov | 8 | slight_neg |
| 2026-04-15 | [PM Appeals to People to Take 9 Pledges on Health, Conservation of Nature, Service, Others](https://www.deccanchronicle.com/nation/politics/pm-appeals-to-people-to-take-nine-pledges-on-health-conservation-of-nature-service-others-1950594) | deccanchronicle.com | 8 | very_pos |
| 2026-04-13 | [FM Sitharaman slams Stalin over 'false narratives' on paddy bonus; bats for pulses, oilseeds for self-reliance- Moneycon](https://www.moneycontrol.com/news/business/fm-sitharaman-slams-stalin-over-false-narratives-on-paddy-bonus-bats-for-pulses-oilseeds-for-self-reliance-13887438.html) | moneycontrol.com | 8 | slight_neg |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 61 | 33 | 7 | 54 |
| Jul 2024 | 77 | 36 | 8 | 68 |
| Aug 2024 | 97 | 39 | 4 | 93 |
| Sep 2024 | 134 | 56 | 10 | 123 |
| Oct 2024 | 110 | 41 | 15 | 95 |
| Nov 2024 | 97 | 42 | 9 | 86 |
| Dec 2024 | 91 | 38 | 11 | 80 |
| Jan 2025 | 71 | 23 | 2 | 69 |
| Feb 2025 | 80 | 29 | 2 | 78 |
| Mar 2025 | 70 | 33 | 3 | 66 |
| Apr 2025 | 52 | 20 | 4 | 48 |
| May 2025 | 32 | 12 | 2 | 30 |
| Jun 2025 | 37 | 13 | 2 | 35 |
| Jul 2025 | 47 | 15 | 6 | 41 |
| Aug 2025 | 45 | 24 | 5 | 40 |
| Sep 2025 | 79 | 25 | 2 | 76 |
| Oct 2025 | 42 | 17 | 1 | 41 |
| Nov 2025 | 40 | 18 | 3 | 37 |
| Dec 2025 | 47 | 14 | 5 | 42 |
| Jan 2026 | 55 | 14 | 3 | 52 |
| Feb 2026 | 62 | 21 | 10 | 52 |
| Mar 2026 | 55 | 29 | 4 | 51 |
| Apr 2026 | 70 | 41 | 6 | 64 |
| May 2026 | 38 | 18 | 8 | 30 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/millets-india-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 5.0 | 4.0 | 1.0 | 0.5 |
| Measured comparison | 4.5 | 4.5 | 1.5 | 0.5 |
| Visualisation from counted data | 4.5 | 3.5 | 1.0 | 0.5 |
| Exploration and drill-down | 1.0 | 4.0 | 2.0 | 1.0 |
| Data export with provenance | 3.0 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 4.5 | 1.0 | 1.0 |
| Traceable references | 1.0 | 1.0 | 1.5 | 0.5 |
| Accuracy against the corpus | 3.0 | 3.5 | 3.0 | 3.5 |
| Calibration and limits | 4.5 | 3.0 | 4.0 | 3.0 |
| Decision-grade verdict | 3.0 | 4.0 | 3.0 | 3.0 |
| Facet coverage | 4.0 | 4.0 | 1.0 | 0.5 |
| **Score /100** | 71.5 | **73.3** | 37.3 | 28.3 |

**Claude Opus judge:** C gave the decision-maker the most usable picture. It shows volume falling (CAGR -21.9%, late/early 0.55) with the critical share decomposed, tone set against a defined baseline, and limits placed next to the numbers, including the five unmeasured months. Its weak points are failing follow-ups and an unlinked headline layer. B is cleanly traced but thinner: one series, no critical or CAGR reading. A and D answered honestly from no data or memory and cannot support a decision.

**GPT judge:** C is the strongest decision brief: it gives a traceable trend, a grounded tone comparison, useful breakdowns, and a reproducible export while distinguishing news coverage from adoption or outcomes. B has fuller trend decomposition, but its unsupported causal account and failed follow-ups weaken its decision value; C’s main gaps are the missing trend CAGR and incomplete placement of data limits.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/millets-india-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/millets-india-pulse.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is the news saying about millets in India?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "millets", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'millets', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
