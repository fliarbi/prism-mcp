# Prism benchmark: scoring rubric

[Benchmark results](../README.md)

The benchmark puts the same question to four setups: Claude alone, ChatGPT alone, Claude + Prism and ChatGPT + Prism.
Each one must produce the same deliverable, a decision-grade report, and every report is scored on the eleven
parameters below. This page explains what each parameter rewards and why.

## 1. What is scored, and why

An earlier, simpler comparison capped answers at a few hundred words of prose and scored writing qualities such as
specificity. It rewarded memory answers for quoting precise but unmeasured numbers, let omissions go unpunished, and
never looked at the measured artefacts (series, charts, exports) at all. This rubric scores those artefacts instead:
a measured trend, a measured comparison, a chart whose points exist, a table a reader can export, a next layer to click
into, and a verdict bounded by a window.

## 2. Rules

1. **Score the deliverable, not the prose.** All four setups produce the same structured report (charts, tables, a list
   of the calls it rests on), rendered through one shared template, so presentation is not scored.
2. **Checks first, judges may only lower.** Everything that can be checked mechanically (numbers traced to the recorded
   results, charts and tables traced, DOIs resolved, follow-up calls run) is checked before a judge reads the report.
   Two blind AI judges then score, and may lower a checked score with a stated reason but never raise it.
3. **Invented is zero; honest-unmeasured is one.** A chart series, table or verdict number with no source and no
   `estimate` label is invented: it scores 0 on that parameter and caps the whole scenario at 40. An honest `estimate`
   label earns exactly 1 on measured parameters and no accuracy penalty, so a model that declines to fabricate finishes
   above one that does.
4. **Not-applicable is decided by the question type, not by the setup.** If the question has a time axis, the trend
   parameter applies to all four setups, and a setup that omits it scores 0. Parameters that do not apply drop out.
5. **No credit for dumping.** Charts count only when they support a sentence in the prose (at most four); tables count
   only when the prose names them (at most five); a tool list is not drill-down; caveats in a footer are not limits.
6. **Public figures count, with a cap.** A number sourced to a real published figure that the judges confirm counts as
   grounded, but mechanically scored parameters cap at 3 for such sources because the benchmark cannot replay them.

## 3. Parameters

Eleven parameters in three families, weights summing to 100. Each is scored 0–5. A scenario's score is the weighted
mean of its applicable parameters, scaled to 100.

| Family | Parameter | Weight | Applies to |
| --- | --- | ---: | --- |
| A. Measured content (42) | Measured trend | 10 | questions with a time axis |
| | Measured comparison | 7 | questions with a contrast |
| | Visualisation from counted data | 10 | all but citation and rewrite questions |
| | Exploration and drill-down | 7 | all but citation and rewrite questions |
| | Data export with provenance | 8 | all but rewrite questions |
| B. Trust (40) | Reproducibility | 12 | all |
| | Traceable references | 8 | research questions, plus pulse, table and audit |
| | Accuracy against the data | 12 | all |
| | Calibration and limits | 8 | all |
| C. Decision value (18) | Decision-grade verdict | 12 | all |
| | Facet coverage | 6 | all |

The measured family shares one scale: 0 absent or invented; 1 honestly unmeasured; 2 partly grounded, or grounded
without provenance; 3 grounded with provenance but incomplete for the question; 4 grounded, complete, full provenance;
5 read correctly for the decision (consistent, bounded, broken down).

### 3.1 Measured trend (10)

A time series of the quantity asked about, over a stated window, with the change quantified (growth, delta, peak with
date) and the direction read correctly. Decisions turn on direction and rate, not level; memory can only assert a
direction.

*Scores.* 0 no series, an invented one, or a window that contradicts the source · 1 direction asserted with no series,
or a series labelled estimate · 2 an unverified cited series, or a traced series without window · 3 traced with window
but the change not quantified, or the incomplete newest period not flagged · 4 traced, windowed, change quantified,
decisive points dated · 5 plus direction consistent everywhere and the series broken down where the data allows.

A half-counted newest month plotted as a collapse caps the trend at 2.

### 3.2 Measured comparison (7)

A contrast on one scale and one window: against a baseline, between comparators, or between periods, with the ratio or
delta stated and the caveats carried. A ratio across different windows or different kinds of data is a wrong answer
dressed as a number.

*Scores.* 0 none, untraced, or different windows combined as one scale · 1 qualitative only · 2 remembered figures, or
mixed scales stated but unresolved · 3 traced on one scale but with an arithmetic slip or an undefined baseline · 4 ratios
recompute exactly, baseline defined, caveats carried · 5 plus the contrast is the one the question asked, with what the
data can and cannot test about it.

### 3.3 Visualisation from counted data (10)

Charts whose every plotted value traces to a recorded source, with window, unit and source line, each supporting a
specific sentence. A chart of invented numbers scores zero, and the parameter is the minimum over the counted charts,
so one invented chart zeroes it.

*Scores.* 0 no chart, or any invented series · 1 an estimate-labelled chart · 2 traced but without window, unit or
source, or not used by the prose · 3 traced and tied to a claim, but views the question asked for are missing · 4 a
traced chart for each facet the data supports, each with a reading · 5 plus comparisons or breakdowns rather than bare
levels, and incomplete periods visibly marked.

### 3.4 Exploration and drill-down (7)

The next layer under the headline numbers (total → breakdown → an item with an identifier, such as a headline with its
link or a quote with its DOI), plus follow-up questions each paired with a call that returns on-topic data when run.

*Scores.* 0 flat summary or invented breakdown · 1 generic "where to look next" · 2 one traced layer and no way
further · 3 one traced layer and at least three follow-ups that ran with on-topic results, or two traced layers · 4 two
or more traced layers reaching identified items, and follow-ups covering the open facets · 5 plus every item carries
its identifier and at least one follow-up was run and folded back in.

### 3.5 Data export with provenance (8)

The tables the question needs, with rows that trace to a recorded result and a provenance note: source call, window,
unit, coverage and export date. A table that does not say what it is and when it was counted is a liability a month
later.

*Scores.* 0 none, invented, or disagreeing with the chart or prose · 1 estimate-labelled, or no window and no source ·
2 traced but provenance incomplete, or a dump with no prose reference · 3 full provenance but a needed table missing ·
4 every needed table, fully traced, with provenance, referenced in the prose · 5 plus missing values kept as blanks with
their reason (never zeros) and row identifiers included.

### 3.6 Reproducibility (12)

Every number in the prose traces to a recorded call (feature, arguments and window) or a named public source; derived
numbers can be recomputed; replaying the listed calls reproduces the numbers within rounding.

*Scores.* 0 measured-looking numbers with no source · 1 labelled memory, or generic sources · 2 under 60% traced · 3
60–89% traced, calls listed with arguments · 4 at least 90% traced, replay exact, derived numbers recomputable · 5 plus
every number traced or marked as interpretation, and a call list that rebuilds every chart and table.

### 3.7 Traceable references (8)

Papers, articles and headlines the report relies on carry identifiers that resolve (DOI or link), metadata that
matches, the claim each supports, and quotes found verbatim in the source. One fabricated identifier caps this
parameter at 1, however many others are real.

*Scores.* 0 none where needed, or mostly fabricated · 1 any fabricated identifier · 2 at least 80% resolve but not tied
to claims · 3 at least 90% resolve, tied to claims · 4 all resolve, every quote found verbatim · 5 plus ranked with
reasons, contrary sources equally traceable, news items with date, publisher and link.

### 3.8 Accuracy against the data (12)

No contradiction with the recorded results, no fabricated-looking specifics presented as measured, and fields read by
their meaning (critical is not the same as negative; a count about a subject is not a count about a claim).

*Scores.* 0 several contradictions or fabrications · 1 one · 2 no contradiction but misread fields or claims beyond the
data · 3 none, minor imprecision · 4 exact, interpretation labelled · 5 plus anomalies in the results themselves caught
rather than repeated as findings.

### 3.9 Calibration and limits (8)

The specific limits that apply, stated where the numbers are used: the window and where it ends, the gap to today,
whether counts describe the claim or only its subject, the coverage flag, delays in labels, how terms were matched, thin
evidence; what was measured separated from what was interpreted.

*Scores.* 0 memory presented as measurement, or no limits · 1 generic hedges · 2 uncertainty without the specific
limits · 3 window and what the counts are, but one material limit missed · 4 every applicable limit beside its number ·
5 plus the limits change the reading and the report says what would close the gap.

### 3.10 Decision-grade verdict (12)

A direct answer, the decision it supports, confidence with a reason, and what would change it; consistent with every
chart and table in the report; naming the strongest contrary evidence; bounded by the data's limits.

*Scores.* 0 none, self-contradicting, or resting on invented numbers · 1 restates the question · 2 direct but unsupported
· 3 supported, but the decision or "what would change it" missing · 4 all four lines, consistent, strongest contrary item
named · 5 plus bounded by window and coverage, measured and interpreted separated, an expert would sign it unedited.

### 3.11 Facet coverage (6)

The share of the facets the question asks for (for example volume, tone, themes and the critical stories) that are
answered with grounded values or an honest "no data". This is where omissions are charged.

*Scores.* 0 under a quarter grounded · 1 mostly memory · 2 half · 3 three quarters · 4 all, or grounded "no data" · 5
plus the implied facets (brand vs generic names, overlapping terms, seasonality, studied-vs-reported mismatch).

## 4. Fairness

**Same request, same rights.** All four setups receive the identical deliverable specification, the same prose limit
and the same right to include charts and tables. Setups without Prism are told explicitly that charts and tables from
memory are allowed, each series sourced to a named published figure or labelled `estimate`.

**Judges.** Reports are shuffled and anonymised (A–D), rendered through one template, and scored by two AI judges after
the mechanical checks. The judges are AI models and could share biases with the respondents, which is why the
mechanical checks set ceilings the judges cannot raise.

**Where Prism is expected not to win.** Old, well-known evidence literatures (where a model can name the landmark
studies from memory); radars where "new" means recent milestones; tables the data cannot fill (Prism answers honestly
with blanks, and a labelled estimate table can score higher on the verdict); citation and rewrite tasks; and events after
the end of the data window. The capability matrix makes these losses visible instead of hiding them in an average.

## 5. Deliverable format

One markdown report, sections in this order:

```
# <title>

## Verdict                       (required, first, at most 150 words)
- Answer: ...
- Decision: ...
- Confidence: high|medium|low - <reason>
- What would change it: ...

## What the data shows           (required; every number tagged [cN], [rN] or (est.))
## Trend                         (questions with a time axis; at least one chart with a time axis)
## Comparison                    (questions with a contrast)
## Geography                     (geography questions)
## Evidence                      (research questions; year, venue, tier, [rN], claim supported, quote)
## Drill-down                    (breakdown layers with identifiers, and follow-up calls)
## Exports                       (CSV tables with provenance)
## Method and limits             (required)
## References                    (required; [rN] Title. Venue, year. DOI or link)
```

Tags: `[cN]` points to a recorded Prism call, `[rN]` to a reference, `(est.)` marks an estimate. Counted limits: 4 charts,
5 tables, 8 references, 8 follow-up calls; extras are ignored, not penalised, unless invented.

## 6. Reporting

* **Per scenario and setup:** the eleven scores, the weighted score with caps (strict, the headline) and without, and
  whether the invention check failed.
* **Per parameter:** the mean, the share of scenarios where the setup produced something real (score 2 or more), and the
  mean quality when it did. A setup that charts rarely but truthfully is distinguishable from one that charts always and
  invents.
* **Per category and per question type:** the mean per setup and the best setup.
* **Same model, with and without Prism:** wins, ties and losses, and the mean gain. This controls for model strength and
  is the headline Prism effect.
* **Invention rate** per setup, and **judge agreement** (mean absolute difference per parameter).
