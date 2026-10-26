# RBI repo rate coverage

[Finance & markets](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Central-bank decision tracking for India.  
> **Why it is hard.** An acronym-heavy term; the resolver must route it as a topic, not a place.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [rbi-repo-rate.json](../../examples/rbi-repo-rate.json).

**The question:**

> What has the news said about RBI repo rate decisions over the last two years?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “repo rate”, Jun 2024 – May 2026 | 7,127 |
| Critical coverage (priority 7–9) | 5,203 (73%) |
| Peak month | Jun 2025 (849 articles) |
| Last third of the window vs first third | 1.33× (rising) |
| Negative · positive | 33.5% · 52.1% |
| Tone vs all news (negative-to-positive ratio) | 0.64 vs 0.58 baseline: *about as negative as ordinary news coverage* |
| What Prism thinks “repo rate” is | topic |

![Monthly coverage of repo rate](../img/rbi-repo-rate-trend.svg)

![Tone of repo rate coverage](../img/rbi-repo-rate-tone.svg)

![Countries in repo rate coverage](../img/rbi-repo-rate-geo.svg)

![Themes in repo rate coverage](../img/rbi-repo-rate-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “repo rate” coverage (they also name the companies, people and places it is written about with): rbi (6,137), reserve bank of india (4,183), inflation (3,237), the reserve bank of india (3,061), interest rates (1,693), economic growth (1,561), banking (1,027), financial policy (733), emi (664), sbi (664), hdfc bank (519), q3 (330)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| monetary policy committee (united kingdom) | barbie hsu | india |
| mpc | boman irani | united states |
| sdf | nirmala sitharaman | china |
| fd | roger bootle | iran |
| bank of baroda | greg lindberg | united kingdom |
| sbi | sanjeev arora | japan |

**Top publishers in a 200-article sample:** businessnewsthisweek.com (7.5%), economictimes.indiatimes.com (5%), bhaskar.com (3.5%), newkerala.com (3.5%), indiatoday.in (3%), prabhatkhabar.com (2.5%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-05-26 | [RBI MPC 2026: Check Out Key Details Here](https://m.dailyhunt.in/news/india/english/newsx+english-epaper-newsxen/rbi+mpc+2026+check+out+key+details+here-newsid-n713678062) | m.dailyhunt.in | 8 | slight_pos |
| 2026-02-06 | [Repo Rate Stays At 5.25% After RBI MPC Meet, Yet Smart Borrowers May Still Unlock Big Home Loan EMI Savings](https://www.freepressjournal.in/business/repo-rate-stays-at-525-after-rbi-mpc-meet-yet-smart-borrowers-may-still-unlock-big-home-loan-emi-savings) | freepressjournal.in | 8 | slight_neg |
| 2026-02-06 | [RBI holds repo rate steady at 5.25% in February 2026 MPC meeting](http://zeenews.india.com/economy/rbi-holds-repo-rate-steady-at-5-25-in-february-2026-mpc-meeting-3014187.html) | zeenews.india.com | 8 | slight_pos |
| 2026-02-06 | [RBI holds repo rate steady at 5.25% in February 2026 MPC meeting](https://zeenews.india.com/economy/rbi-holds-repo-rate-steady-at-5-25-in-february-2026-mpc-meeting-3014187.html) | zeenews.india.com | 8 | slight_pos |
| 2026-02-06 | [RBI keeps repo rate unchanged at 5.25% - Business Upturn](https://www.businessupturn.com/finance/economy/rbi-keeps-repo-rate-unchanged-at-5-25/) | businessupturn.com | 8 | slight_pos |
| 2026-02-06 | [RBI LIVE: Repo rate unchanged – Proposes exempting NBFCs under Rs 1,000 cr from registration, draft norms for cyber frau](https://www.financialexpress.com/business/news/rbi-mpc-meeting-february-2026-live-updates-sanjay-malhotra-repo-rate-rupee-tariff/4132719/) | financialexpress.com | 8 | slight_pos |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 295 | 228 | 73 | 153 |
| Jul 2024 | 54 | 43 | 28 | 20 |
| Aug 2024 | 283 | 212 | 66 | 150 |
| Sep 2024 | 90 | 68 | 47 | 32 |
| Oct 2024 | 300 | 230 | 73 | 137 |
| Nov 2024 | 67 | 56 | 37 | 24 |
| Dec 2024 | 376 | 277 | 86 | 206 |
| Jan 2025 | 81 | 57 | 37 | 33 |
| Feb 2025 | 769 | 606 | 336 | 357 |
| Mar 2025 | 148 | 112 | 74 | 64 |
| Apr 2025 | 772 | 573 | 310 | 369 |
| May 2025 | 123 | 67 | 37 | 77 |
| Jun 2025 | 849 | 561 | 302 | 483 |
| Jul 2025 | 225 | 130 | 77 | 121 |
| Aug 2025 | 499 | 343 | 162 | 273 |
| Sep 2025 | 146 | 99 | 47 | 58 |
| Oct 2025 | 270 | 192 | 56 | 181 |
| Nov 2025 | 113 | 86 | 55 | 37 |
| Dec 2025 | 530 | 407 | 176 | 300 |
| Jan 2026 | 117 | 90 | 48 | 62 |
| Feb 2026 | 409 | 295 | 68 | 256 |
| Mar 2026 | 85 | 59 | 36 | 38 |
| Apr 2026 | 449 | 350 | 121 | 248 |
| May 2026 | 77 | 62 | 32 | 36 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/rbi-repo-rate-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 3.5 | 4.0 | 1.0 | 1.0 |
| Measured comparison | 4.0 | 4.0 | 2.0 | 2.0 |
| Visualisation from counted data | 2.5 | 3.0 | 1.0 | 1.0 |
| Exploration and drill-down | 3.5 | 3.0 | 1.5 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 1.0 |
| Reproducibility | 5.0 | 4.5 | 1.0 | 0.0 |
| Traceable references | 1.0 | 2.0 | 0.5 | 0.5 |
| Accuracy against the corpus | 4.5 | 4.5 | 3.5 | 3.0 |
| Calibration and limits | 4.5 | 4.5 | 3.0 | 3.0 |
| Decision-grade verdict | 4.0 | 3.5 | 3.0 | 0.0 |
| Facet coverage | 5.0 | 4.0 | 1.5 | 1.5 |
| **Score /100** | **74.5** | 73.8 | 35.9 | 24.4 |

**Claude Opus judge:** C and B both grounded every figure in the recorded overview, but C read the data more critically. It rejected the misleading CAGR, separated 'critical' from polarity, and flagged the entity and place collisions and the non-RBI contamination. It also stated plainly that RBI decisions after May 2026 are unseen. A and D answered honestly from memory but could not measure coverage at all.

**GPT judge:** A is the strongest decision aid: it separates mention-based coverage from RBI decisions, gives a traceable volume and tone read, and places the key data limits beside the findings. B covers more facets, but its chart treats the censored final month as an ordinary low point and its export labels coverage as full, making its trend reading less dependable.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/rbi-repo-rate/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/rbi-repo-rate.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What has the news said about RBI repo rate decisions over the last two years?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "repo rate", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'repo rate', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
