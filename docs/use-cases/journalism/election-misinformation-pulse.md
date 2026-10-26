# Election misinformation coverage

[Journalism & fact-checking](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A newsroom's beat monitor.  
> **Why it is hard.** 2024 was a global election year; coverage is spread across dozens of countries.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [election-misinformation-pulse.json](../../examples/election-misinformation-pulse.json).

**The question:**

> How much coverage has election misinformation received, and where?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “election misinformation”, Jun 2024 – May 2026 | 236 |
| Critical coverage (priority 7–9) | 208 (88.1%) |
| Peak month | Oct 2024 (51 articles) |
| Last third of the window vs first third | 0.11× (falling) |
| Negative · positive | 92.8% · 6.8% |
| Tone vs all news (negative-to-positive ratio) | 13.69 vs 0.58 baseline: *markedly more negative than ordinary news coverage* |
| What Prism thinks “election misinformation” is | topic |

![Monthly coverage of election misinformation](../img/election-misinformation-pulse-trend.svg)

![Tone of election misinformation coverage](../img/election-misinformation-pulse-tone.svg)

![Countries in election misinformation coverage](../img/election-misinformation-pulse-geo.svg)

![Themes in election misinformation coverage](../img/election-misinformation-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “election misinformation” coverage (they also name the companies, people and places it is written about with): misinformation (108), joe biden (93), elon musk (88), twitter (86), biden (59), kamala harris (49), alphabet (46), mark zuckerberg (39), first amendment (36), grok (34), x (27), voting (23)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| meta | hunter biden | united states |
| the postal service | sundar pichai | colombia |
| republican national committee | kamala harris | georgia |
| facebook | joe biden | india |
| federal election commission | elon musk | russia |
| republican party (united states) | mark zuckerberg | united kingdom |

**Top publishers in a 16-article sample:** winnipegfreepress.com (12.5%), newtelegraphng.com (6.2%), theconversation.com (6.2%), arstechnica.com (6.2%), euronews.com (6.2%), gantnews.com (6.2%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-04-15 | [Ekiti Poll: EU Moves To Tackle Election Misinformation](https://newtelegraphng.com/ekiti-poll-eu-moves-to-tackle-election-misinformation/) | newtelegraphng.com | 7 | very_pos |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 4 | 4 | 4 | 0 |
| Jul 2024 | 12 | 12 | 12 | 0 |
| Aug 2024 | 44 | 41 | 41 | 3 |
| Sep 2024 | 18 | 15 | 17 | 1 |
| Oct 2024 | 51 | 38 | 46 | 4 |
| Nov 2024 | 18 | 15 | 15 | 3 |
| Dec 2024 | 2 | 2 | 1 | 1 |
| Jan 2025 | 3 | 2 | 3 | 0 |
| Feb 2025 | 2 | 0 | 2 | 0 |
| Mar 2025 | 1 | 1 | 1 | 0 |
| Apr 2025 | 1 | 1 | 0 | 1 |
| May 2025 | 0 | 0 | 0 | 0 |
| Jun 2025 | 3 | 3 | 3 | 0 |
| Jul 2025 | 10 | 10 | 9 | 1 |
| Aug 2025 | 6 | 3 | 6 | 0 |
| Sep 2025 | 44 | 44 | 44 | 0 |
| Oct 2025 | 7 | 7 | 6 | 1 |
| Nov 2025 | 3 | 3 | 3 | 0 |
| Dec 2025 | 3 | 3 | 3 | 0 |
| Jan 2026 | 0 | 0 | 0 | 0 |
| Feb 2026 | 0 | 0 | 0 | 0 |
| Mar 2026 | 1 | 1 | 1 | 0 |
| Apr 2026 | 2 | 2 | 1 | 1 |
| May 2026 | 1 | 1 | 1 | 0 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/election-misinformation-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 3.5 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 1.0 | 0.0 |
| Visualisation from counted data | 3.0 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 3.0 | 1.0 | 2.0 | 1.0 |
| Data export with provenance | 2.5 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.5 | 0.0 | 1.0 |
| Traceable references | 1.0 | 1.0 | 0.5 | 0.5 |
| Accuracy against the corpus | 3.0 | 3.5 | 3.5 | 4.0 |
| Calibration and limits | 2.5 | 4.5 | 4.0 | 3.0 |
| Decision-grade verdict | 3.0 | 3.5 | 2.5 | 2.0 |
| Facet coverage | 4.0 | 4.0 | 1.5 | 0.5 |
| **Score /100** | 62.9 | **69.3** | 33.2 | 24.4 |

**Claude Opus judge:** A and B both traced the same Prism call. A also reported where coverage sits (US 52%, Colombia 14%) inside its verdict, quantified both spikes including Sept 2025, and flagged label anomalies such as the Georgia collision and theme noise. B dropped the 2025 spike and misread the censored month. C and D honestly declined to measure, so they offer a decision-maker nothing beyond a list of calls to run.

**GPT judge:** A is the strongest decision aid: it traces volume, trend, geography and tone to a replayable source, quantifies the fall and baseline contrast, and places the key coverage limits near the findings. C provides broader detail but misstates the window and labels a censored export complete; B is candid but offers no measurements, while D is explicitly a scoping estimate.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/election-misinformation-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/election-misinformation-pulse.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How much coverage has election misinformation received, and where?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "election misinformation", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'election misinformation', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
