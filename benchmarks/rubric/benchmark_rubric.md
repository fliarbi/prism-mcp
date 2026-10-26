# Prism MCP benchmark v2: scoring rubric

Draft 2.0, 2026-10-23. Machine-readable twin: [`benchmark_v2_rubric.json`](benchmark_v2_rubric.json). Nothing here has been run; this is the design.

## 1. What v1 measured, and why that was the wrong thing

v1 (`showcase/compare.py`) sent 113 questions to four setups (Claude alone, ChatGPT alone, Claude + Prism, ChatGPT + Prism), capped every answer at 280 words of plain text, and had a blind Opus judge score five writing criteria out of 5: specificity, verifiability, currency, calibration, accuracy. The judge was told not to penalise omissions. Averages out of 25: Claude + Prism 21.7, ChatGPT + Prism 19.7, Claude alone 18.8, ChatGPT alone 15.1.

Reading the saved answers (`docs/comparisons/*.json`) shows what that measured:

- **Memory answers scored high on specificity by quoting unmeasured numbers.** Claude alone on NVIDIA: "plausibly tens of thousands of articles a month" (the corpus says 6k–15.5k); on CRISPR: "the health literature index hits roughly 3,000–4,000 in 2017, 7,000–9,000 in 2020"; on EV batteries: a full table of Wh/kg ranges with "Nature Energy and Joule review literature" as the source. The judge could not check any of it, so it mostly passed as "plausible".
- **Omissions were free.** ChatGPT alone on NVIDIA declined to answer and still scored 12; a Prism answer that skipped tone or geography lost nothing.
- **The measured artefacts were never in the contest.** The monthly series, the comparison chart, the CSV with a provenance sidecar (`docs/exports/`) were built by `build_pages.py` afterwards; the judge saw prose.
- **Currency punished honesty.** The corpus ends 2026-05/06 and today is 2026-10-22; a Prism answer that said so lost currency points, a memory answer that guessed at 2026 did not.

So v1 could not score the things a plain model cannot honestly produce: a measured trend, a measured comparison, a chart whose points exist, a table a reader can export, a next layer to click into, a verdict bounded by a window. v2 scores those, keeps the two v1 criteria that still earn a place (accuracy, calibration reframed as limits), and charges omissions through a facet check.

## 2. Design rules

1. **Score the deliverable, not the prose.** All four setups produce the same thing: a markdown report with typed fenced blocks (chart specs, CSV tables, a call list) that a script parses and one renderer turns into an identical HTML dashboard. Presentation is therefore unscored.
2. **Script first, judge lower-only.** Everything that can be checked against the recorded tool responses or the corpus is checked by a script before any model reads the deliverable. The judge may lower a script score with a stated reason, never raise it. Accuracy, verdict support and facet reading remain judge calls.
3. **Invented is zero; honest-unmeasured is one.** A chart series, CSV table or verdict number with no resolvable source and no `estimate` label is invented: it scores 0 on that parameter and caps the whole scenario at 40 (invention gate). An honest `estimate` label earns exactly 1 on measured parameters and no accuracy penalty. A bare model that refuses to fabricate therefore finishes above one that does.
4. **N/A is decided by the pattern, not by the setup.** If the scenario's pattern has a time axis, `trend` applies to all four setups; a setup that omits it scores 0. N/A parameters drop out of numerator and denominator.
5. **Prism cannot score by dumping.** Charts count only when they support a sentence in the prose and the judge marks them relevant (max 4); tables count only when the prose names them (max 5); a breakdown counts only if its values trace; the tool catalogue is not drill-down; caveats in a footer are not limits; a dump trips a gate that caps verdict and facets.
6. **Bare models can ground on public figures, with a cap.** A series or number sourced to a real published figure the judge confirms counts as grounded, but script-scored parameters cap at 3 for citation-sourced grounding because the benchmark cannot replay it. The cap is stated in every anchor it affects.

## 3. Parameters

Eleven parameters in three families, weights summing to 100. Each is scored 0–5 against the anchors; weighted score = 100 × Σ(wᵢ·sᵢ) / (5 × Σ wᵢ) over applicable parameters.

| Family | Parameter | Weight | Script-checkable | Applies to |
| --- | --- | ---: | --- | --- |
| A. Measured content (42) | Measured trend | 10 | yes | pulse, compare, stance, brief, evidence, radar, history, trending |
| | Measured comparison | 7 | yes | + claims, geo, table; not audit, citations, improve, library |
| | Visualisation from counted data | 10 | yes | all but citations, improve |
| | Exploration and drill-down | 7 | yes | all but citations, improve |
| | Data export with provenance | 8 | yes | all but improve |
| B. Trust (40) | Reproducibility | 12 | yes | all |
| | Traceable references | 8 | yes (corpus lookups) | research patterns + pulse, table, audit; not compare, geo, trending, history |
| | Accuracy against the corpus | 12 | judge, seeded by script | all |
| | Calibration and limits | 8 | presence yes, placement judge | all |
| C. Decision value (18) | Decision-grade verdict | 12 | structure/consistency yes, support judge | all |
| | Facet coverage | 6 | yes via grounding map | all |

The anchor pattern for the measured family is the same everywhere: 0 absent or invented; 1 honestly unmeasured; 2 partly grounded or grounded without provenance; 3 grounded with provenance but incomplete for the question; 4 grounded, complete, provenance full; 5 read correctly for the decision (consistent, bounded, decomposed).

### 3.1 Measured trend (10)

*Definition.* A time series of the quantity asked about, over a stated window, with the change quantified (growth factor, CAGR, delta, peak with date) and the direction read correctly.

*Why.* Decisions turn on direction and rate, not level. "Coverage is high" is not actionable; "rose 1.83× between the first and last third of Jun 2024–May 2026, peak 15,514 in Feb 2026" is. Memory can only assert direction.

*Anchors.* 0 no series, or invented, or window/unit that contradicts the source · 1 direction asserted with no series, or series labelled estimate · 2 cited-unverified series, or traced series without window/granularity · 3 traced series with window but change unquantified, censoring caveat dropped, or only first/last given when points existed · 4 traced, window + censoring, change quantified exactly, decisive points named with dates · 5 plus direction-consistency passes everywhere, recomputations exact, series decomposed where the data allows (critical vs total, orientation split, central vs bounds).

*Verification.* Parse `prism-chart` blocks with a temporal x and CSVs keyed by period/year; resolve `source` to the recorded response; match points to `data.points`, `data.rows[i].points`, `data.series`, `data.scenarios`; grounded share; window equality; recompute growth (late third / early third), peak, CAGR; direction words in Trend and Verdict vs the sign of the change and the tool's own `trend`/`direction`; no point at or after `censored_at` plotted as a full period. For citation-sourced series the judge states whether the source is real; where the definition is replicable (a yearly title-phrase count) the harness can run `analysis.history` for an order-of-magnitude band.

*Anti-gaming.* Unsourced series = 0, not 1. Pasting the points array is not a trend (anchors 3–5 need the change read). A censored month plotted as a collapse caps at 2. Duplicate charts of one quantity count once.

### 3.2 Measured comparison (7)

*Definition.* A contrast on one scale and one window: vs a baseline (corpus tone, previous window), between comparators (term A vs B, claim A vs B, research lane vs news lane) or between periods (early vs late, observed vs scenario), with ratio or delta stated and the tool's caveat carried.

*Why.* "Which is bigger, which is growing, by how much, since when" is the shape of most intelligence questions. Aviation news is negative by default; a tone level without the baseline misleads. A ratio across windows or lanes is a wrong answer dressed as a number (`global_comparison` says "three different questions; do not add them together").

*Anchors.* 0 none, untraced, or lanes/windows combined as one scale · 1 qualitative only · 2 memory figures, or mixed lanes stated but unresolved · 3 traced on one scale with ratio stated but an arithmetic slip or an undefined baseline (`tone_ratio`, `lift`, `critical` used undefined) · 4 ratios recompute exactly, baseline defined, caveat carried (overlap, placed_pct) · 5 plus the contrast is the question's contrast (attention vs sales; studied vs reported) with what the data can and cannot test about it.

*Verification.* Recompute share = articles / combined_articles, growth, `framing_shift.delta_pct_points`, `vs_baseline`, tier-weighted supports vs contradicts, `growth_x` = articles / previous, scenario central vs last observed; flag arithmetic across values whose `what`/`lane`/`unit`/`window` differ; require the tool's `how`/`what`/`reading` definition for any field name used.

*Anti-gaming.* Two memory numbers cap at 2 even if both are real: one scale cannot be established. Restating `most_covered` or `framing_shift.reading` without the numbers caps at 3. Mixing lanes to inflate a number is 0.

### 3.3 Visualisation from counted data (10)

*Definition.* Chart specs whose every plotted value traces to a recorded source, with window, unit and source line, each supporting a specific sentence. A chart of invented numbers scores zero.

*Why.* A chart is how a trend reaches a meeting, and the easiest artefact to fake: a plausible curve with no numbers behind it will be believed.

*Anchors.* 0 no chart, or any series invented, or values contradict the named source · 1 estimate-labelled memory chart, or cited-unverified · 2 traced but no window/unit/source, wrong kind (pie of a time series), or orphan (no sentence uses it) · 3 fully traced and tied to a claim, but views the question asked for and the data supported are missing (only volume when tone was asked), or labels wrong · 4 a traced chart for each facet the question asks that the data supports, each with a reading caption · 5 plus comparison or decomposition rather than bare levels (critical share over volume; early vs late; central with bounds; both lanes side by side) and censored periods visibly marked.

*Verification.* Parse against the chart schema; resolve `source` and `path`; diff values after rounding; presence of window/unit/source; kind suitability; `supports` sentence found in the prose (≥0.8 token overlap); censoring check; judge marks relevance; **the parameter is the minimum over counted charts**, so one invented chart zeroes it.

*Anti-gaming.* Minimum, not mean. Max four counted charts, chosen by relevance. A chart of a panel the question did not ask about does not raise the score. For plain models the `estimate` label is the only honest route to a memory chart and earns exactly 1.

### 3.4 Exploration and drill-down (7)

*Definition.* The next layer under the headline numbers (total → breakdown → item with an identifier: volume → subcategories → headline with url; claim → documents → verbatim quote with DOI; country rows → articles), plus 3–8 follow-up questions each paired with an executable call (feature + args) that returns on-topic data when run.

*Why.* A dashboard is used by clicking into the number that surprised you. This is the "graph-like exploration" and "clickable" requirement made substantive: are the links real, and can the reader go one level deeper from here.

*Anchors.* 0 flat summary or invented breakdown · 1 generic "where to look next", or memory breakdown labelled · 2 one traced layer with no way further, or follow-ups that are the catalogue or fail/return empty · 3 one traced layer + ≥3 specific follow-ups that executed ok with on-topic data, or two traced layers · 4 two or more traced layers reaching an item with identifier, and executable follow-ups covering the question's open facets · 5 plus every breakdown item carries its identifier and at least one follow-up was executed by the setup itself and folded back with traced values.

*Verification.* Parse `prism-calls`; validate feature against `REGISTRY` and args against the function's `validate_call`; execute through the registry (12-hour cache makes it cheap); judge marks results on-topic; detect layers by matching table rows (label + value, title + DOI/url) to `data.themes.subcategories.rows`, `data.entities.*.rows`, `data.geography.rows`, `data.documents`, `data.critical.articles`, `data.claims`, `data.rows`; identifiers must appear in a recorded response or resolve in the corpus.

*Anti-gaming.* Catalogue listing caps at 2. Off-topic or failing calls do not count. Pasting all eight overview panels is one layer. Breakdown without identifiers caps at 4. Plain models can reach 3–5 only through citation-grounded layers; executable calls are impossible for them, which is the honest structural gap, not a rigged rule.

### 3.5 Data export with provenance (8)

*Definition.* The CSV tables the question needs (monthly series, per-term summary, documents with DOIs and quotes, per-row table with nulls kept, bibliography), rows tracing to a recorded response, with source call, window, unit, coverage flag and export date.

*Why.* The numbers leave the report for a sheet or a slide. A table that does not say what it is and when it was counted is a liability a month later; a memory table pasted into a sheet is a fabrication.

*Anchors.* 0 none, invented, or disagrees with the chart/prose for the same quantity · 1 estimate-labelled, or no window and no source · 2 traced but provenance incomplete, or a dump of every table with no prose reference · 3 full provenance but one table where two were needed, or never referenced from the prose · 4 every needed table, 100% traced, full provenance, referenced, tool field names or documented renames · 5 plus nulls kept as nulls with the tool's reason (never zeros), row identifiers included, and a `provenance` JSON block in the shape `tools/prism_export.py` writes.

*Verification.* Parse `csv` info-string attributes and body; resolve source; match rows by key column; cell-grounded share; provenance completeness; chart–csv–prose agreement on (period, value); null hygiene against `research.table` rows; prose must name the file; five tables counted.

*Anti-gaming.* Unlabelled memory table = invented = 0 + gate. All eight overview panels dumped with no reference = 2 regardless of size. Zero-filled nulls fail anchor 5 and are reported.

### 3.6 Reproducibility (12)

*Definition.* Every number in the prose traces to a recorded call (feature + args + window) or a named public source; derived numbers show or allow recomputation; the listed calls, replayed, reproduce the numbers within rounding. A third party could regenerate the deliverable.

*Why.* A number that cannot be regenerated cannot be defended in a review or an audit. v1's specificity rewarded precision regardless of origin; this rewards only numbers with an origin.

*Anchors.* 0 measured-looking numbers with no source, or replay materially differs with no window stated · 1 labelled memory/estimate, or generic sources ("the review literature") · 2 under 60% trace, or calls listed without args · 3 60–89% trace, calls with args, replay matches · 4 ≥90% trace, every call with args and window, replay exact within rounding, derived numbers recomputable · 5 plus 100% trace or are marked interpretation, and a regenerate recipe (`prism-calls` with every call used + capture date) rebuilds every chart and table.

*Verification.* Numeric extraction from prose with inline tags; a value index of every numeric leaf in every recorded response (path, window, feature) plus derived shares/ratios/growths; exact-after-rounding or formula match; near-misses (same path, different value) go to the accuracy judge; replay via `REGISTRY` and leaf-by-leaf diff; citation-sourced numbers classified by the judge (real-plausible / unverifiable / wrong) and capped at 3.

*Anti-gaming.* Precision is not evidence. Marking everything "interpretation" to dodge tracing costs facets and verdict. Numbers quoted out of their window (a 2017–2025 research count beside a 2024–2026 news count as one window) are mismatches.

### 3.7 Traceable references (8)

*Definition.* Papers, articles and headlines the deliverable relies on carry identifiers that resolve (DOI/Prism research index id in the research tables, url in the news table, or on the web), metadata that matches, the claim each supports, and verbatim quotes found in the source abstract.

*Why.* v1's verifiability made mechanical. Models invent DOIs and misdate trials (the judge caught "CAF-PD-type trials, 2020" for Postuma 2017); one dead DOI and the reader stops trusting the rest. For evidence, audit and citation questions the references *are* the product.

*Anchors.* 0 none where needed, or majority fabricated · 1 any fabricated identifier, or none resolvable · 2 ≥80% resolve but no year/venue/tier/quote/claim-tie · 3 ≥90% resolve, tied to claims, with tier; quotes absent or not found · 4 100% resolve, tied, every quote found verbatim, tier as the tool states · 5 plus ranked/tiered with reason, contrary sources equally traceable, news items with date + publisher + resolving url.

*Verification.* Extract DOIs, Prism research index ids, urls; look up offline in the index (research works by DOI/id, news by url), fall back to a cached rate-limited HEAD on doi.org; title fuzzy ≥0.85 and year ±1 against the corpus record; quotes as whitespace-normalised substrings of the abstract or the tool's `quote`; tiers equal the tool's `tier`; judge checks claim-tie.

*Anti-gaming.* One fabricated identifier caps at 1 however many others are real. Count does not help: the eight entries most directly tied to claims are scored. Copying the tool's citation block without tying it to claims caps at 2.

### 3.8 Accuracy against the corpus (12) — kept from v1

*Definition.* No contradiction with the reference record, no fabricated-looking specifics presented as measured, fields read by their definitions (critical ≠ negative; subject lane ≠ claim lane; share_pct with its denominator).

*Why.* A traced chart beside a wrong sentence is still a wrong report. Omissions are now charged, but under facets, not here.

*Anchors.* 0 multiple contradictions or fabrications · 1 one clear contradiction or one fabricated-looking specific · 2 no contradiction but field misreadings or claims beyond the data presented as measured · 3 none; minor imprecision ("roughly four times" for 4.5×) · 4 exact, definitions respected, interpretation labelled · 5 plus the reference's own anomalies caught (truncated monthly array vs trend summary, Colombia/Cameroon place collisions, off-topic rows, undefined `critical`) rather than repeated as findings.

*Verification.* Judge, seeded with the script's near-miss list and lane/field flags, the full reference record (every panel, no truncation) and the same contradiction/fabrication listing as v1. A script-detected mismatch counts as a contradiction unless explained.

*Anti-gaming.* An empty or refusing deliverable scores 3 here (no contradictions) and 0 on the measured family, which is the right trade. Verbatim copying caps at 4. Hedging does not remove a contradiction.

### 3.9 Calibration and limits (8) — v1 calibration + currency, sharpened

*Definition.* The specific limits that apply, stated where the numbers are used: window with end and censoring, the gap to today, lane, coverage flag, enrichment lag, match mode, thin evidence; measured separated from interpreted; "the corpus does not state one" where so.

*Why.* The three ways this cluster has produced confident wrong answers (lane, coverage, window) are all limits. A series ending 2026-05-31 cannot answer "right now" on 2026-10-22, and the reader must be told next to the number, not in a footer.

*Anchors.* 0 memory as measurement, counts as real-world quantities, or no limits · 1 generic hedges · 2 uncertainty without the specific limits · 3 window and what the counts are, measured vs interpreted, but one material limit missed · 4 every applicable limit beside its number; honest "no data" where so · 5 plus the limits change the reading and the deliverable says what would close the gap.

*Verification.* Window strings must equal recorded windows; Method must state the newest data date and the gap to TODAY; `meta.coverage.partial` must be echoed when true and not claimed when false; lane named when `lane_note`/`query.lane` exists; censoring mentioned where a censored series is used; where a response says `available:false`, `answered:0`, `value:null` or `tally.read:0` no number may be supplied in its place; judge scores placement and whether the limits alter the verdict's bounds.

*Anti-gaming.* A closing disclaimer paragraph is anchor 2. More hedging does not reach 4; an honest, specific "I cannot measure this" earns 3. Repeating every caveat field verbatim is a footer and caps at 3.

### 3.10 Decision-grade verdict (12)

*Definition.* A direct answer, the decision it supports, confidence with reason, what would change it; consistent with every chart and table in the same deliverable; naming the strongest contrary evidence it contains; bounded by the data's limits.

*Why.* This is what the reader came for. v1 rewarded "lead with the direct answer" as style; v2 checks that the answer rests on the deliverable's own numbers and does not contradict them.

*Anchors.* 0 none, or contradicts its own data, or rests on invented numbers · 1 restates the question, "it depends", or a dump · 2 direct but unsupported, or no confidence and no conditions · 3 supported by traced numbers with confidence, but decision or "what would change it" missing, or a contrary finding in its own evidence ignored · 4 all four lines, consistent, strongest contrary item named · 5 plus bounded by window/lane/coverage, measured vs interpreted separated inside the verdict, expert would sign without edits.

*Verification.* Verdict section first with the four labelled lines (missing → cap 3); direction words vs computed direction; verdict numbers must trace (any unsourced unlabelled number → 0); judge for support, contrary acknowledgement, bounds, expert sign-off.

*Anti-gaming.* Over 150 words caps at 3. Restating headline counts is anchor 1. Plain models can score 4 on questions memory suffices for; 5 on measured questions needs the window. Prism-backed verdicts that ignore the tool's own contradicting documents or empty rows cap at 3.

### 3.11 Facet coverage (6)

*Definition.* Share of the facets the question asks and the pattern implies that are answered with grounded values or a grounded "no data" (the tool's own `available:false`/null with reason). This is where omissions, excused in v1, are charged.

*Why.* "Volume, tone, themes and the critical stories" is four deliverables. A fine trend chart that skips tone answered a different question.

*Anchors.* 0 under a quarter grounded · 1 mostly memory · 2 half · 3 three quarters · 4 all, or grounded "no data" · 5 plus the implied facets from `scenarios.py` `special` (brand vs generic vs class names; term overlap; seasonality; studied-vs-reported mismatch).

*Verification.* Per-pattern facet checklists (in the JSON) mapped to response paths; a facet is satisfied when a grounded number or row traced to that path appears, or the tool's own empty result is stated; judge confirms a reading sentence exists and marks the implied facet.

*Anti-gaming.* Pasting every panel satisfies the path check but not the reading check. Facets are fixed per pattern; a setup cannot narrow the question. An invented facet value is uncovered and trips the invention gate.

## 4. Rejected or removed

| Parameter | Verdict | Reason |
| --- | --- | --- |
| Specificity (v1) | removed | Rewards precise numbers regardless of origin; memory answers scored 4.4 by quoting unmeasured figures. Replaced by reproducibility. |
| Verifiability (v1) | replaced | Right idea, judged by impression. Now two mechanical parameters: reproducibility (numbers trace and replay) and traceable references (identifiers resolve in the corpus, quotes found). |
| Currency (v1) | merged into limits | Unverifiable without ground truth after the window; conflated corpus freshness with answer quality and punished honest window statements. Now: state the data end and the gap to today, and what it means. |
| Calibration (v1) | kept, sharpened | Became "calibration and limits": specific limits beside the numbers, not generic hedges. |
| Accuracy (v1) | kept, sharpened | Seeded with the script's mismatch list; anchor 5 for catching the reference's own anomalies. |
| Writing quality, length, structure | rejected | Formatting. The spec fixes structure; the renderer equalises looks. |
| Dashboard aesthetics / interactivity | rejected | Text-only CLIs; interactivity comes from the shared renderer identically. The substance (real links, executable drill-down) is scored under drill-down and references. |
| Tool efficiency, latency, cost | rejected (reported) | Not value to the reader; would punish long tools and reward abstention. Reported as metadata. |
| "Uses Prism tools correctly" | rejected | Measures the product, not the deliverable; unfair to bare setups; call choice is already in the engineering flags. |
| Forecast accuracy | rejected | The future is unavailable. History scenarios are scored on method disclosure (traced series, bounds, backtest MAE) under trend and limits. |
| Novelty / insight | rejected | Judge taste; rewards confident narrative, which is the failure mode v2 exists to stop. |
| Citation count / source breadth | rejected | Count gaming; invented DOIs would raise it. Replaced by resolvable share over at most eight tied entries. |
| Chart count | rejected | Gaming; the chart parameter is the minimum over at most four relevant charts. |
| Word-count compliance | removed | The 280-word rule was the problem. A 1,800-word prose cap remains as a parse gate, not a score. |
| Sentiment/tone correctness (standalone) | redundant | Tone is a facet, a baseline comparison, and a field-misreading accuracy anchor. |
| "Presentable clickable dashboard" (draft item) | split | Presentable = formatting (rejected); clickable = drill-down anchor 5 and references. |
| "Graph-like exploration" (draft item) | merged | Into drill-down (layers reaching items with identifiers, executable follow-ups) to avoid double-counting. |

Of the seven draft parameters, six are kept with sharper definitions (trend, historical comparison → measured comparison, visualisation, exploration/drill-down, export with provenance, reproducibility, decision-grade verdict); four were added (traceable references, accuracy, calibration and limits, facet coverage).

## 5. Fairness: same request, same rights, and where Prism should lose

**Same deliverable request.** All four setups receive the identical spec (section 6), the same 1,800-word prose cap, and the same right to include charts and tables. The bare prompt says so explicitly: charts and tables from memory are allowed, each series sourced as a named published figure (`ref:rN`) or `estimate`. A memory chart labelled estimate earns 1, not 0; an unlabelled one is invented.

**Citation-sourced grounding.** Bare models can earn up to 3 on script-scored parameters with real public figures the judge confirms (Tesla's 1,789,226 deliveries in 2024 is a real number a reader can check). The cap exists because the benchmark cannot replay them; it is stated in every anchor it affects.

**Judge controls.** Blind A–D shuffle as v1; every deliverable rendered through one template; script scores computed first and only lowerable; the judge is given the script's mismatch list rather than asked to spot numbers; a second judge (GPT via `codex exec`) scores the pilot and per-parameter agreement is reported. v1's caveat stands: the judge is a Claude model and Claude wrote two of the four deliverables.

**Where Prism is expected not to win** (from the v1 record, not hope):

- *Old, well-known evidence literatures* — minimum-wage-employment, death-penalty-deterrence, glyphosate-cancer, ubi-evidence, policing-body-cameras, remote-work-productivity, housing-prices-evidence. v1 retrieval was thin or off-topic; bare Claude names the landmark studies. If its DOIs resolve, bare Claude can take references, accuracy and verdict; Prism keeps trend, export and drill-down. Weighted totals will be close.
- *Radars where "new" means milestones* — alzheimers-drugs-radar, quantum-computing-radar, coral-bleaching-radar, pfizer-pipeline-radar. `new_work` is citation-ranked and misses 2024–2026 milestones; a mid-2026-cutoff model may win verdict and facets.
- *Tables the corpus cannot fill* — ev-battery-table, crop-yields-climate-table, cancer-immunotherapy-table. Prism answers 0 of 5 honestly (full limits, zero export and chart); the bare model's estimate-labelled table earns 1 on export and likely wins verdict. The bare model may win the scenario, which is the correct result for a corpus gap and should be reported as one.
- *Improve, citations, library* — v1 Prism output was one citation, garbled metadata, off-field classics. Bare models write better rewrites and know canonical citations, but invented DOIs cost them under references.
- *"Right now" and post-May-2026 events* — fintech-trending, cybersecurity-trending, antitrust-big-tech, copyright-ai-pulse. The corpus ends 2026-05/06; a later-cutoff bare model may give the better verdict.
- *ChatGPT + Prism in live mode on slow tools* — research.table, research.compare, cold research.evidence: codex ends its turn before the call returns; expect it below Claude alone until the request/poll path is automatic.
- *Audits* — bare Claude knew the BMJ 2017 umbrella review where Prism's deep reads were off-topic; expect a split (Prism: drill-down, export; bare: verdict, accuracy).

The capability matrix (section 7) exists so these losses are visible as "quality when produced" rather than hidden in an average.

## 6. Deliverable format

One markdown document as plain text, emitted by `claude -p` or `codex exec`, parsed by a script. Sections in this order; required ones marked; the pattern-conditional ones are listed in the JSON.

```
# <title>

## Verdict                       (required, first, ≤150 words)
- Answer: ...
- Decision: ...
- Confidence: high|medium|low - <reason>
- What would change it: ...

## What the data shows           (required; every number tagged [cN], [rN] or (est.))
## Trend                         (patterns with a time axis; ≥1 prism-chart with temporal x)
## Comparison                    (patterns with a contrast)
## Geography                     (geo; optional for pulse, brief)
## Evidence                      (research patterns; year, venue, tier, [rN], claim supported, quote)
## Drill-down                    (breakdown layers with identifiers + a prism-calls block)
## Exports                       (csv blocks with provenance + a provenance block)
## Method and limits             (required)
## References                    (required; [rN] Title. Venue, year. doi/url)
```

Typed blocks:

- ```` ```prism-chart ```` — JSON: `id, kind (line|bars|hbar|stacked|share|range), title, unit, window{from,to,to_is_exclusive,censored_at?}, x{field,type}, series[{name, source, path?, points[[x,y],…]}], bounds?, caption, supports, vega_lite?`. `source` is `call:<feature>#<n>`, `ref:rN` or `estimate`. Values are verified from `series`; `vega_lite` is optional decoration.
- ```` ```csv name=monthly.csv source=call:news.compare#1 window=2024-06-01..2026-06-01 unit=articles coverage=full ```` — RFC 4180 body with header; nulls as empty cells.
- ```` ```provenance ```` — JSON `{exported_at, calls:[{feature,args,window,coverage}]}`, the shape `tools/prism_export.py` writes.
- ```` ```prism-calls ```` — JSON list; entries with `used_for` declare the calls the report rests on (`c1…`), entries with `question` are follow-ups (`f1…`) the harness will execute. In Prism setups the harness reconciles `cN` against the calls it actually recorded; self-reported calls that were not made are ignored and flagged.

Counted limits: 4 charts, 5 tables, 8 references, 8 follow-up calls; extras are ignored, not penalised, unless invented.

Prompts: one common preamble for all four (reader is a decision-maker; every number tagged; unsourced unlabelled charts/tables score as invented; say what the data cannot answer). Bare: own knowledge only, memory charts allowed with `ref`/`estimate`. Prism-captured: the recorded calls with ids, full responses (no digest truncation; v1's cut monthly arrays made the models look wrong about the reference). Prism-live: MCP connection, harness records every call in full.

Modes: **captured** (all 113, Prism setups get `docs/examples/<slug>.json` with call ids; controls retrieval, cheap) and **live** (Prism setups choose calls; needed for drill-down and reproducibility anchor 5; pilot and flagships).

Rendering: one `render_v2.py` template turns every deliverable into an HTML page (charts via `svgchart.py` or Vega-Lite, tables, resolving links). The judge reads the rendered text; the script reads the parsed blocks.

## 7. Weighting and reporting

- **Per scenario, per setup:** eleven scores (0–5 or N/A), family sub-scores, weighted score (strict with gates; plain without), gate flags, metadata (seconds, calls, tokens).
- **Gates:** invention gate (any invented chart/table/verdict number → cap 40, `invented=true`); dump gate (no verdict fields and >60% of non-fenced lines are table rows → verdict ≤2, facets ≤3). Both variants reported; strict is the headline.
- **Per parameter:** mean per setup, produce rate (share of applicable scenarios with score ≥2), quality when produced (mean over those), N/A count.
- **Capability matrix:** setups × parameters, cell `produce% · quality` (e.g. `73% · 4.1`), with honest abstentions (score 1, estimate-labelled) reported separately from invented (0). This is the "can produce at all" vs "quality when produced" view: a setup that charts rarely but truthfully is distinguishable from one that charts always and invents.
- **Per category (17) and per pattern (15):** mean weighted per setup, best setup, gain of best-Prism over best-alone. Patterns are the natural unit because the N/A rules follow them.
- **Head-to-head, same model:** claude_prism vs claude_bare and chatgpt_prism vs chatgpt_bare, wins/ties/losses and mean delta per parameter. This controls for model strength and is the headline Prism effect; best-vs-best (v1's 86 of 113) is kept beside it.
- **Invention rate** per setup as a headline safety number.
- **Judge agreement** on the pilot: second judge, per-parameter weighted kappa and mean absolute difference, disagreements over 2 points listed.
- **Engineering flags v2:** every scenario where a Prism-backed setup scores below the same model alone, with the parameters lost and the script's diagnosis (empty rows, off-topic documents, truncated series, failed replay), in the style of `docs/ENGINEERING_FLAGS.md`.
- Outputs: `docs/comparisons_v2/<slug>.json`, `docs/COMPARISON_V2.md`, a "Deliverables" section on each use-case page linking the four rendered dashboards. v1 files untouched.

## 8. Pilot scenarios

Eight slugs chosen to hit every block type and every place the rubric could be ambiguous:

| Slug | Pattern | What it stresses |
| --- | --- | --- |
| `tesla-vs-byd` | compare | two monthly series on one scale; share/growth recomputation; monthly + summary exports; the attention-vs-sales contrast the data cannot test; bare models hold real 2024 delivery figures (citation-sourced cap) |
| `nvidia-pulse` | pulse | eight facets; layers themes → subcategories → headline; truncated monthly array vs trend summary and the Colombia artefact (accuracy 5); window end vs today |
| `crispr-history` | history | yearly series with scenario bounds (range chart); backtest MAE disclosure; bare models' plausible memory series; forecast not scored on correctness |
| `ev-battery-table` | table | corpus answers 0 of 5; honest nulls vs invented ranges; the case Prism should lose on total while winning limits; live record exists |
| `audit-coffee-draft` | audit | claim-level drill-down; references that must resolve; off-topic deep reads; bare Claude's strong recall; live record exists |
| `dengue-geography` | geo | four lanes that must not be added; studied-vs-reported mismatch as the comparison; placed_pct; trend N/A |
| `metformin-cancer-risk` | evidence | supporting vs contradicting with tier weights; verbatim quote check; DOI resolution; research/news series; live record exists |
| `gen-ai-education-stance` | stance | yearly orientation shares (stacked chart); framing shift as the comparison; post-2023 literature where memory is thin; live record exists |

Reserves: `fintech-trending` (stale window; Prism should lose on verdict) and `minimum-wage-employment` (claims; asymmetric matching; ChatGPT live timeouts).

Run the pilot in both modes, fix parser and anchor ambiguities, freeze the rubric version, then run all 113.

## 9. What to build next (not in this change)

`showcase/compare_v2.py` (prompts, modes, full-response capture, call ids), `showcase/ground_v2.py` (parser, value index, matching, replay through `REGISTRY`, DOI/url corpus lookups, direction checks, facet map), `showcase/render_v2.py` (one HTML template), `showcase/judge_v2.py` (blind, seeded with the ground report, lower-only), `showcase/report_v2.py` (aggregates and `COMPARISON_V2.md`). The 12-hour Prism cache makes replay and follow-up execution nearly free on the same day; record cache hits so replay diffs are attributable.
