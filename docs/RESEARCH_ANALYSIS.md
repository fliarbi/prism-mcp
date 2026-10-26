# Research analysis with Prism

[Prism MCP](../README.md) · [Use cases](use-cases/README.md) · [Data export](DATA_EXPORT.md) · [Benchmark](../benchmarks/README.md)

Prism is built for the parts of research that a language model does worst on its own: counting a
literature, finding the paper that disagrees, quoting a figure exactly, and knowing what was published
after its training cut-off. This guide walks through six workflows. Each step shows the tool, the call
and real output captured from the live corpora (the full responses are in [`examples/`](examples/)).

Every number below comes from a saved response, not from this text.

## 1. Evidence synthesis: is the claim supported, and how strongly?

**Question:** does metformin reduce cancer risk in people with type 2 diabetes?

```text
research.evidence          claim="Metformin reduces cancer risk in diabetic patients"
research.counter_evidence  claim=...      # looks for dissent on purpose
research.statistics        claim=...      # verbatim figures with their population
```

What comes back ([full page](use-cases/medical/metformin-cancer-risk.md)):

| Measurement | Value |
| --- | --- |
| Typed papers on both sides of the claim, 2017–2025 | 334 |
| Framing of those papers | 98 supporting · 88 qualifying · 20 contradicting · 128 neutral (32.3% contested) |
| Strongest supporting source | JNCI 2024 meta-analysis: RR 0.55 (case-control), RR 0.65 (prospective cohorts) |
| Strongest randomised result | Diabetes Prevention Program, 21-year follow-up (2025): HR 0.90, 95% CI 0.73–1.10 |

The useful output is the **split**: observational meta-analyses report 30–45% lower risk, while the only
long randomised follow-up is null. Prism gives the writer both, each with a quote checked against its
abstract and a study-design tier (meta-analysis > RCT > cohort > case report).

**Pattern:** evidence → counter-evidence → statistics, then `research.citations` for the reference list.

## 2. Literature mapping: how is a field framing its findings over time?

Every paper in the 105.6M-record typed corpus carries an **orientation** label (breakthrough,
promising, descriptive, comparative, cautionary, problem-identifying, critical). Counting those labels by
year shows whether a field is getting more optimistic or more cautious, without a model reading a
single abstract.

```text
research.stance_trends  term="intermittent fasting"
research.browse         term="intermittent fasting" orientation="promising" sort="recent"
```

| Year | 2017 | 2019 | 2021 | 2023 | 2025 |
| --- | ---: | ---: | ---: | ---: | ---: |
| Positive framing | 19.8% | 18.1% | 25.7% | 32.5% | 30.9% |
| Contested framing | 18.7% | 6.3% | 11.5% | 11.7% | 8.7% |

Intermittent-fasting research is getting more positive over time and is rarely contested. That is a
finding about the literature, not about fasting, and the page says so
([full page](use-cases/medical/intermittent-fasting-stance.md)).

**Pattern for a systematic review:** `stance_trends` to size and shape the field → `browse` with
`orientation` and `contribution` filters to pull the empirical papers on each side → `research.table`
to extract one variable across them → `research.library_gaps` to check the reading list for missing topics.

## 3. Research history and forward scenarios

```text
analysis.history    subject_phrases=["vaccine hesitancy"]
analysis.scenarios  history_id=<from the call above>  horizon=3
```

The history call returns a yearly count **and the exact SQL that produced it**. The scenarios call
backtests two baselines (no change, linear drift) one step ahead on the series itself and keeps the one
that would have forecast the past better:

| | 2021 | 2022 | 2023 | 2024 | 2025 | 2026 (scenario) | 2028 (scenario) |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| Vaccine-hesitancy papers | 1,235 | 1,458 | 1,168 | 897 | 776 | 776 (486–1,066) | 776 (0–1,646) |

Backtest mean absolute error: no-change 226, linear drift 332, so no-change wins. A naive trend line
through the post-COVID spike would have projected growth. Prism's honest answer is "about flat, with a
wide range" ([full page](use-cases/public-health/vaccine-hesitancy-trend.md)).

## 4. Media analysis next to research

Most questions need both corpora: what the research says, and how the world is talking about it.
`research.brief` returns volumes for six corpora in one call (typed research, readable papers, the health literature index,
news, patents, arXiv). `news.overview` returns eight panels for a term: profile, monthly trend, tone
against the all-news baseline, themes ranked by lift, organisations, people, places and the critical
headlines.

[Ozempic in the news](use-cases/medical/ozempic-news-pulse.md): 22,214 articles from June 2024 to May
2026, peaking at 1,470 in March 2026, 61.8% positive. Its tone is 1.05× the all-news baseline, about as
negative as ordinary coverage. The organisation most named alongside it is Eli Lilly (20.7% of
entity-labelled articles).

## 5. Fact-checking and improving a draft

```text
research.audit    text=<the whole draft>     # every checkable claim, its status and best source
research.improve  claim=<one sentence>       # a rewrite that says what the evidence supports
research.citations claim=... style=apa|vancouver|harvard|mla|chicago|bibtex|inline|numbered|footnote
```

The audit separates claims that are supported, overstated, contradicted or unsupported. It runs on
sentences a writer actually wrote ([audit of a coffee article](use-cases/journalism/audit-coffee-draft.md)).
`improve` keeps the writer's sentence and changes only what the evidence requires, for example
"causes" to "is associated with" when the sources are observational.

## 6. One question across many rows: the spreadsheet case

```text
research.table  rows=["lithium iron phosphate","nickel manganese cobalt","sodium-ion","solid-state","lithium-sulfur"]
                question="battery energy density Wh/kg"
```

Each row is answered on its own, with its own top source and paper count. A row the corpus does not
answer comes back **blank, never filled in**. The [page](use-cases/energy-climate/ev-battery-table.md)
shows the result as CSV ready to paste into a sheet. See [Data export](DATA_EXPORT.md) for Excel output.

## Choosing the right tool

| You want | Use | Not |
| --- | --- | --- |
| whether a claim holds | `research.evidence` + `counter_evidence` | `search_research` (returns papers, not verdicts) |
| the shape of a field | `research.stance_trends` | reading 20 abstracts and guessing |
| a number to quote | `research.statistics` | a figure from memory |
| what is new | `research.radar` (since a year) | `search` sorted by date |
| attention and tone | `news.overview`, `news.compare` | counting search results |
| a defensible forecast | `analysis.history` → `analysis.scenarios` | a trend line through a spike |
| sources for a bibliography | `research.citations`, `research.source_ranking` | model-written references |

## Limits to plan around

* Research counts are **records**, not deduplicated studies; a finding restated in ten papers counts ten times.
* Orientation is a label on a paper's **own framing**, not a verdict on the claim.
* The typed corpus starts in **2017**; reading and history go back to 1900.
* News stops at **1 June 2026** by default (ingest lag); patents run about 18 months behind.
* A claim with several outcomes should be split, one mechanism per claim: retrieval resolves each claim to
  two poles, and a three-outcome claim resolves to the broadest one.
