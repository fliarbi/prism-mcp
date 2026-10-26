# India defence exports

[Defence & geopolitics](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** An industrial-policy read for a defence analyst.  
> **Why it is hard.** BrahMos deals and record export figures drive positive tone.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [india-defence-exports.json](../../examples/india-defence-exports.json).

**The question:**

> What is the news saying about India's defence exports?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “defence exports”, Jun 2024 – May 2026 | 551 |
| Critical coverage (priority 7–9) | 497 (90.2%) |
| Peak month | Apr 2026 (89 articles) |
| Last third of the window vs first third | 1.18× (flat) |
| Negative · positive | 14.9% · 84.6% |
| Tone vs all news (negative-to-positive ratio) | 0.18 vs 0.58 baseline: *markedly more positive than ordinary news coverage* |
| What Prism thinks “defence exports” is | topic |

![Monthly coverage of defence exports](../img/india-defence-exports-trend.svg)

![Tone of defence exports coverage](../img/india-defence-exports-tone.svg)

![Countries in defence exports coverage](../img/india-defence-exports-geo.svg)

![Themes in defence exports coverage](../img/india-defence-exports-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “defence exports” coverage (they also name the companies, people and places it is written about with): india (457), rajnath singh (181), defence (140), narendra modi (104), singh (100), exports (93), the ministry of defence (90), indian economy (87), armenia (60), army (50), military technology (35), operation sindoor (29)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| hindustan aeronautics limited | rajnath singh | india |
| bharat electronics | upendra dwivedi | united states |
| defence research and development organisation | anil chauhan | russia |
| theprint | sanjeev kumar | ukraine |
| indian navy | olaf scholz | china |
| indian air force | nirmala sitharaman | france |

**Top publishers in a 86-article sample:** economictimes.indiatimes.com (9.3%), livemint.com (5.8%), financialexpress.com (5.8%), newkerala.com (3.5%), thehindu.com (3.5%), outlookbusiness.com (2.3%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-05-06 | [India’s Defence Exports Jump 25-Fold Since FY17, But Import Dependence Persists – Outlook Business](https://www.outlookbusiness.com/economy-and-policy/indias-defence-exports-jump-25-fold-since-fy17-but-import-dependence-persists) | outlookbusiness.com | 8 | very_pos |
| 2026-04-03 | [India’s Defence Exports Hit Record Rs 38,424 Crore in 2025-26 \| SportsZ News](https://sportsz.news/news/indias-defence-exports-hit-record-rs-38424-crore-in-2025-26/) | sportsz.news | 8 | very_pos |
| 2026-04-02 | [India's defence exports rise 62 pc to hit record Rs 38,424 crore in FY26](https://www.dtnext.in/news/national/indias-defence-exports-rise-62-pc-to-hit-record-rs-38424-crore-in-fy26) | dtnext.in | 8 | very_pos |
| 2026-04-02 | [India’s Defence Exports Hit Record Rs 38,424 Crore In FY26: Rajnath Singh](https://www.newsmobile.in/nation/indias-defence-exports-hit-record-rs-38424-crore-in-fy26-rajnath-singh/) | newsmobile.in | 8 | very_pos |
| 2026-04-02 | [India’s Defence Exports hit record Rs 38,424 crore in FY26](https://organiser.org/2026/04/02/346788/bharat/indias-defence-exports-hit-record-rs-38424-crore-in-fy26-jump-62-66-per-cent-on-rising-global-demand/) | organiser.org | 8 | very_pos |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 30 | 28 | 2 | 27 |
| Jul 2024 | 28 | 26 | 1 | 27 |
| Aug 2024 | 17 | 13 | 2 | 15 |
| Sep 2024 | 22 | 20 | 13 | 8 |
| Oct 2024 | 28 | 26 | 9 | 19 |
| Nov 2024 | 17 | 14 | 0 | 17 |
| Dec 2024 | 28 | 28 | 4 | 24 |
| Jan 2025 | 6 | 6 | 0 | 6 |
| Feb 2025 | 19 | 15 | 0 | 18 |
| Mar 2025 | 17 | 17 | 0 | 17 |
| Apr 2025 | 43 | 42 | 3 | 40 |
| May 2025 | 22 | 16 | 2 | 20 |
| Jun 2025 | 25 | 21 | 4 | 21 |
| Jul 2025 | 17 | 11 | 4 | 13 |
| Aug 2025 | 23 | 22 | 2 | 21 |
| Sep 2025 | 2 | 1 | 0 | 2 |
| Oct 2025 | 15 | 13 | 0 | 15 |
| Nov 2025 | 20 | 16 | 4 | 16 |
| Dec 2025 | 16 | 15 | 8 | 8 |
| Jan 2026 | 15 | 15 | 4 | 11 |
| Feb 2026 | 19 | 16 | 5 | 14 |
| Mar 2026 | 11 | 10 | 2 | 9 |
| Apr 2026 | 89 | 85 | 13 | 76 |
| May 2026 | 22 | 21 | 0 | 22 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/india-defence-exports-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 3.5 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.0 | 4.0 | 1.0 | 0.0 |
| Visualisation from counted data | 4.0 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 2.0 | 1.0 | 0.5 |
| Data export with provenance | 3.0 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 4.5 | 0.0 | 1.0 |
| Traceable references | 2.0 | 1.5 | 1.0 | 0.5 |
| Accuracy against the corpus | 3.5 | 4.0 | 2.5 | 3.0 |
| Calibration and limits | 4.0 | 4.5 | 3.0 | 3.0 |
| Decision-grade verdict | 3.5 | 4.0 | 0.0 | 2.0 |
| Facet coverage | 4.5 | 4.0 | 1.0 | 0.5 |
| **Score /100** | **74.8** | 74.2 | 22.0 | 21.3 |

**Claude Opus judge:** A and D both grounded their answers in the same overview call, but A went further. It added the tone comparison chart, the substantive export claims (Rs 38,424 crore, 25-fold), a correct reading of 'critical', and executable follow-ups. B gave plausible official figures from memory and did not measure the news at all, and C declined to answer.

**GPT judge:** A is the strongest decision aid: it grounds the positive tone against a defined corpus baseline, shows that article volume is volatile and flat overall, and separates news claims from verified export performance. B has more breakdowns and charts, but unsupported export and story specifics, plus a misreported window, weaken its reliability; C and D do not provide measured news evidence.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/india-defence-exports/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/india-defence-exports.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is the news saying about India's defence exports?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "defence exports", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'defence exports', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
