# Boeing crisis coverage

[Company & competitive intelligence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Reputation-risk monitoring for a stakeholder.  
> **Why it is hard.** Tone must be read against the corpus baseline; aviation news is negative by default.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [boeing-crisis.json](../../examples/boeing-crisis.json).

**The question:**

> What is the news saying about Boeing, and how negative is it compared with normal news?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “boeing”, Jun 2024 – May 2026 | 147,354 |
| Critical coverage (priority 7–9) | 95,946 (65.1%) |
| Peak month | Jun 2025 (9,181 articles) |
| Last third of the window vs first third | 0.95× (flat) |
| Negative · positive | 46.4% · 49.6% |
| Tone vs all news (negative-to-positive ratio) | 0.93 vs 0.58 baseline: *markedly more negative than ordinary news coverage* |
| What Prism thinks “boeing” is | organization |

![Monthly coverage of boeing](../img/boeing-crisis-trend.svg)

![Tone of boeing coverage](../img/boeing-crisis-tone.svg)

![Countries in boeing coverage](../img/boeing-crisis-geo.svg)

![Themes in boeing coverage](../img/boeing-crisis-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “boeing” coverage (they also name the companies, people and places it is written about with): boeing (145,377), airbus (28,404), max (17,705), nasa (15,877), air india (12,913), aircraft (11,978), faa (10,414), united airlines (8,249), aircraft safety (7,878), airline (7,179), american airlines (6,992), the federal aviation administration (6,805)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| boeing | campbell wilson | united states |
| airbus | john f. kennedy | united kingdom |
| alaska airlines | surya kant | india |
| air india | elon musk | china |
| federal aviation administration | joe biden | canada |
| national transportation safety board | thales of miletus | japan |

**Top publishers in a 227-article sample:** defensenews.com (1.8%), abc17news.com (1.8%), independent.co.uk (1.3%), straitstimes.com (1.3%), storyboard18.com (1.3%), zawya.com (1.3%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-02-05 | [UK regulator asks Air India why Boeing with fuel switch issue was cleared to fly](https://www.independent.co.uk/asia/india/uk-air-india-fuel-switches-boeing-dreamliner-b2914278.html) | independent.co.uk | 9 | very_neg |
| 2026-03-13 | [What Boeing's plea deal could mean for the aviation industry](https://www.pbssocal.org/shows/newshour/clip/boeing-s-troubles-1720211762) | pbssocal.org | 9 | very_neg |
| 2026-04-06 | [Air India Crash: Air India 171 crash: 4-second question that could change everything we think we know \| Mumbai News - T](https://timesofindia.indiatimes.com/city/mumbai/air-india-171-crash-4-second-question-that-could-change-everything-we-think-we-know/articleshow/130050205.cms) | timesofindia.indiatimes.com | 9 | very_neg |
| 2026-02-22 | [How A British Airways Flight To Jakarta Survived Volcanic Ash And Failure Of All Four Engines](https://www.ndtv.com/lifestyle/how-a-british-airways-flight-to-jakarta-survived-volcanic-ash-and-failure-of-all-four-engines-11112919) | ndtv.com | 9 | very_neg |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 6,292 | 4,530 | 3,294 | 2,717 |
| Jul 2024 | 5,836 | 3,833 | 2,725 | 2,871 |
| Aug 2024 | 5,674 | 3,925 | 2,680 | 2,772 |
| Sep 2024 | 6,053 | 4,177 | 2,918 | 2,888 |
| Oct 2024 | 5,965 | 3,965 | 3,000 | 2,752 |
| Nov 2024 | 4,953 | 2,946 | 2,052 | 2,572 |
| Dec 2024 | 5,899 | 4,080 | 3,125 | 2,505 |
| Jan 2025 | 6,540 | 4,187 | 3,017 | 3,176 |
| Feb 2025 | 6,070 | 3,592 | 2,341 | 3,344 |
| Mar 2025 | 7,693 | 5,168 | 3,546 | 3,725 |
| Apr 2025 | 5,847 | 3,743 | 2,907 | 2,646 |
| May 2025 | 6,641 | 4,112 | 3,232 | 3,093 |
| Jun 2025 | 9,181 | 7,309 | 6,653 | 2,295 |
| Jul 2025 | 7,371 | 4,912 | 4,401 | 2,815 |
| Aug 2025 | 6,274 | 3,978 | 2,493 | 3,408 |
| Sep 2025 | 5,999 | 3,682 | 2,424 | 3,210 |
| Oct 2025 | 4,686 | 2,797 | 1,728 | 2,871 |
| Nov 2025 | 5,033 | 3,115 | 1,807 | 3,090 |
| Dec 2025 | 4,314 | 2,652 | 1,567 | 2,648 |
| Jan 2026 | 4,581 | 2,653 | 1,497 | 2,945 |
| Feb 2026 | 6,033 | 3,497 | 2,145 | 3,599 |
| Mar 2026 | 5,907 | 3,665 | 2,576 | 3,099 |
| Apr 2026 | 6,651 | 3,569 | 2,112 | 4,326 |
| May 2026 | 7,861 | 5,859 | 3,964 | 3,666 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/boeing-crisis-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 5.0 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 1.0 | 0.0 |
| Visualisation from counted data | 4.0 | 3.0 | 1.0 | 0.0 |
| Exploration and drill-down | 2.5 | 2.0 | 1.0 | 0.0 |
| Data export with provenance | 4.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 4.0 | 0.0 | 1.0 |
| Traceable references | 1.5 | 0.5 | 0.0 | 0.0 |
| Accuracy against the corpus | 3.5 | 4.0 | 3.0 | 3.0 |
| Calibration and limits | 4.5 | 3.0 | 2.5 | 2.5 |
| Decision-grade verdict | 3.0 | 3.5 | 2.5 | 2.5 |
| Facet coverage | 5.0 | 4.0 | 1.5 | 1.5 |
| **Score /100** | **77.4** | 65.9 | 27.4 | 21.4 |

**Claude Opus judge:** B answers the question the way a decision-maker needs. It reads tone against the corpus baseline (0.93 vs 0.58, 1.6x) and charts the monthly ratio against that baseline, which shows the gap closing in late 2025 and reopening in May 2026. It also flags the corpus's own artefacts: name collisions, a re-dated archive item and incidental critical hits. C has the same headline numbers but charts and exports only volume and drills down less. A and D are honest but unmeasured.

**GPT judge:** D is the strongest decision aid: it directly answers the baseline comparison with a defined ratio and delta, then bounds the interpretation with window, matching, and sample caveats. C offers richer traced trend and facet detail, but its subcategory-fill error and overlong verdict weaken reliability; neither report supplies the needed tone comparison as a chart.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/boeing-crisis/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/boeing-crisis.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is the news saying about Boeing, and how negative is it compared with normal news?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "boeing", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'boeing', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
