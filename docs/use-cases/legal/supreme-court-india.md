# Supreme Court of India coverage

[Legal & compliance](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A judiciary media read for a legal team.  
> **Why it is hard.** 'Supreme Court' is ambiguous across countries; geography disambiguates.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [supreme-court-india.json](../../examples/supreme-court-india.json).

**The question:**

> What themes dominate coverage of India's Supreme Court?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “supreme court of india”, Jun 2024 – May 2026 | 7,646 |
| Critical coverage (priority 7–9) | 6,797 (88.9%) |
| Peak month | Feb 2026 (868 articles) |
| Last third of the window vs first third | 1.6× (rising) |
| Negative · positive | 65.3% · 30.7% |
| Tone vs all news (negative-to-positive ratio) | 2.13 vs 0.58 baseline: *markedly more negative than ordinary news coverage* |
| What Prism thinks “supreme court of india” is | topic |

![Monthly coverage of supreme court of india](../img/supreme-court-india-trend.svg)

![Tone of supreme court of india coverage](../img/supreme-court-india-tone.svg)

![Countries in supreme court of india coverage](../img/supreme-court-india-geo.svg)

![Themes in supreme court of india coverage](../img/supreme-court-india-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “supreme court of india” coverage (they also name the companies, people and places it is written about with): india (5,270), the supreme court (4,203), supreme court (2,565), court (2,187), sc (1,029), the supreme court’s (862), cji (834), surya kant (791), the high court (770), bench (674), delhi high court (358), the supreme court's (263)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| ita | surya kant | india |
| public image ltd | immanuel kant | united states |
| internal revenue service | kapil sibal | cameroon |
| paralympic | vikram nath | united kingdom |
| national council of educational research and training | tushar mehta | canada |
| federal energy regulatory commission | b. v. nagarathna | austria |

**Top publishers in a 233-article sample:** legalbites.in (6%), m.dailyhunt.in (5.2%), thehindu.com (4.7%), taxguru.in (4.3%), english.mathrubhumi.com (4.3%), outlookindia.com (3%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-04-09 | [Gurugram Child Sexual Assault: Max Hospital doctor denies changing medical opinion](https://medicaldialogues.in/news/health/doctors/gurugram-child-sexual-assault-max-hospital-doctor-denies-changing-medical-opinion-168316) | medicaldialogues.in | 9 | extreme_neg |
| 2026-02-10 | [Supreme Court rejects Kuldeep Singh Sengar’s bail plea in custodial death case](https://thenewsmill.com/2026/02/supreme-court-rejects-kuldeep-singh-sengars-bail-plea-in-custodial-death-case/) | thenewsmill.com | 9 | extreme_neg |
| 2026-05-15 | [Rethinking Abortion Law: A Rights-Based Approach For Rape Survivors](https://www.livelaw.in/articles/supreme-court-of-india-abortion-law-gestational-limits-for-rape-survivors-analysis-534134) | livelaw.in | 8 | slight_neg |
| 2026-05-10 | [सुप्रीम कोर्ट में उठी ‘महिला खतना’ पर रोक की मांग, आखिर क्यों दुनिया भर में विवादित है FGM?](https://www.abplive.com/gk/demand-to-ban-female-circumcision-reaches-supreme-court-why-fgm-remains-one-of-the-world-s-most-controversial-practices-3127817) | abplive.com | 8 | very_neg |
| 2026-04-15 | [SC concludes Sterling Biotech case after Rs 9,800 crore recovery](https://www.financialexpress.com/business/news/sc-closes-sterling-biotech-case-after-rs-9800-crore-recovery/4208239/) | financialexpress.com | 8 | slight_neg |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 159 | 134 | 96 | 54 |
| Jul 2024 | 269 | 246 | 162 | 100 |
| Aug 2024 | 404 | 343 | 230 | 158 |
| Sep 2024 | 338 | 305 | 247 | 73 |
| Oct 2024 | 239 | 202 | 131 | 99 |
| Nov 2024 | 253 | 230 | 154 | 94 |
| Dec 2024 | 235 | 209 | 163 | 58 |
| Jan 2025 | 238 | 200 | 140 | 87 |
| Feb 2025 | 345 | 273 | 174 | 138 |
| Mar 2025 | 200 | 150 | 141 | 54 |
| Apr 2025 | 317 | 286 | 229 | 78 |
| May 2025 | 312 | 273 | 184 | 110 |
| Jun 2025 | 150 | 131 | 95 | 46 |
| Jul 2025 | 216 | 167 | 163 | 39 |
| Aug 2025 | 290 | 267 | 196 | 87 |
| Sep 2025 | 260 | 246 | 182 | 70 |
| Oct 2025 | 242 | 224 | 172 | 58 |
| Nov 2025 | 207 | 188 | 127 | 74 |
| Dec 2025 | 222 | 198 | 126 | 86 |
| Jan 2026 | 281 | 254 | 191 | 77 |
| Feb 2026 | 868 | 813 | 529 | 314 |
| Mar 2026 | 472 | 428 | 343 | 113 |
| Apr 2026 | 644 | 592 | 481 | 138 |
| May 2026 | 485 | 438 | 326 | 137 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/supreme-court-india-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 4.0 | 0.5 | 0.0 |
| Measured comparison | 4.5 | 3.5 | 0.5 | 0.0 |
| Visualisation from counted data | 3.5 | 3.5 | 0.5 | 0.0 |
| Exploration and drill-down | 4.0 | 2.5 | 1.5 | 1.0 |
| Data export with provenance | 3.0 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 5.0 | 1.0 | 0.5 |
| Traceable references | 1.0 | 1.0 | 0.5 | 0.5 |
| Accuracy against the corpus | 4.0 | 3.5 | 3.5 | 4.0 |
| Calibration and limits | 4.0 | 4.0 | 3.0 | 2.5 |
| Decision-grade verdict | 4.5 | 4.0 | 3.0 | 2.0 |
| Facet coverage | 4.5 | 4.0 | 1.5 | 1.5 |
| **Score /100** | **77.5** | 72.6 | 31.8 | 23.6 |

**Claude Opus judge:** B and D both traced every number to the overview call. B went further: it read the data critically, flagging the Immanuel Kant, Cameroon and IRS label artefacts, explaining what the 'critical' flag actually marks, and linking headline URLs. A gave honest but unmeasured memory themes, and C declined to answer, so neither supports a decision.

**GPT judge:** D is the strongest decision aid: it gives a traced answer about dominant themes, a quantified trend, and specific limits on the news data. Its main correction is that the sentiment baseline is cached over 30 days, not measured across the full reporting window; A has richer drill-down but makes unsupported or conflicting claims about censoring and theme coverage.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/supreme-court-india/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/supreme-court-india.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What themes dominate coverage of India's Supreme Court?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "supreme court of india", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'supreme court of india', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
