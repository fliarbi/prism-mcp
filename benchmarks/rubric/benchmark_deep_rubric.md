# Prism MCP benchmark v2: deep tiers (POLICY and RESEARCH)

Draft 2.1, 2026-10-23. Machine-readable twin: [`benchmark_v2_deep_rubric.json`](benchmark_v2_deep_rubric.json). The prompts live only in the JSON (`tiers.*.prompt`); do not edit them here. Nothing has been run.

## 1. What the deep tiers add and why the casual tier stays

The two-scenario pilot (Claude 34.3 / 73.1, ChatGPT 24.8 / 68.0) asked v2's questions: a verdict, a trend, a comparison, charts, exports, references. It never asked for a map, a forecast, charts across dimensions, an HTML report, a cross-corpus argument, or an article. It is now the CASUAL tier and is not re-run.

The deep tiers ask one randomly drawn cross-domain topic in two voices:

- **POLICY**: a NITI Aayog adviser briefing a Group of Secretaries, India first, world as comparator, options table, who acts, cost of being wrong.
- **RESEARCH**: an evidence-synthesis researcher with five fixed research questions, a deep analytical report and a full seven-section article.

Both run on the owner's fixed contract (one HTML page, Vega-Lite 5, world-110m maps, a `prism-manifest` JSON block). Prism setups are LIVE on the MCP and choose their calls; plain setups get the same prompt and no tools.

## 2. Parameters per tier

Sixteen parameters each, weights to 100. Script ceilings first, two blind judges lower-only, as v2.

| Family | Parameter | Policy | Research | Status | Script |
| --- | --- | ---: | ---: | --- | --- |
| A measured | trend | 5 | 5 | kept, 10→ | yes |
| | comparison | 5 | 4 | kept, 7→ | yes |
| | chart (min over counted, excl. map/forecast) | 5 | 6 | kept, 10→, cap 4→10 | yes |
| | **dimensions** (multi-dimension coverage) | 6 | 5 | new | yes |
| | **map** (geo traced to data) | 7 | 5 | new | yes |
| | **forecast** | 7 | 5 | new | yes |
| | drilldown | 4 | 4 | kept, 7→ | yes |
| | export | 5 | 5 | kept, 8→ | yes |
| B trust | repro | 10 | 10 | kept, 12→ | yes |
| | refs (8 / 15 counted) | 5 | 9 | kept, 8→ | yes |
| | accuracy | 8 | 8 | kept, 12→ | judge, seeded |
| | limits | 6 | 6 | kept, 8→ | presence yes |
| | **integrity** (HTML renders, manifest = page) | 6 | 5 | new | yes |
| C value | verdict | 6 | 4 | kept, 12→ | structure yes |
| | **crossdomain** | 7 | 8 | new | yes + judge |
| | **actionability** | 8 | — | new, policy only | yes + judge |
| | **article** | — | 11 | new, research only | yes + judge |
| — | timing | 0 | 0 | report-only | metadata |

Family totals: policy A 44 / B 35 / C 21; research A 39 / B 38 / C 23.

**Dropped: facets.** Its job was to charge omissions. In the deep tiers every new component scores 0 when absent (no map, no forecast, one dimension, one corpus, no options table, no article), so a facet score would charge the same omission twice.

**Reweighted down: trend, chart, verdict, repro.** They stay the spine of trust, but the deep tiers have eight measured components instead of five, and the decision content moves into actionability (policy) and the article (research). Repro stays the single heaviest parameter in both tiers because every new component is scored by tracing.

### 2.1 The new parameters in one paragraph each

**Map.** Kind `map`, `points [[country, value]]`, at least five countries, traced to `research.geography` (four lanes: first-author affiliation, journal country, country an article is about, patent assignee; "three different questions; do not add them together") or `news.geography` (`label/articles/share_pct/lift`, `placed_pct`, `censored_at`). The lane must be named in the tool's words beside the map; empty lanes stated, not drawn; India present or reported absent. Anchor 5 catches the data's own artefacts: `England` rows (not a world-110m country), acronym place collisions (`central african republic` with lift 22 on a tech topic). Country names are normalised before matching (lowercase, pycountry, explicit aliases), so the respondent's name-to-ISO join is an integrity matter, not a map matter.

**Dimensions.** Seven dimensions: time, geography, comparison, composition, forecast, evidence magnitude, source mix. A dimension counts only when a chart on it scores ≥3 on its own integrity (chart, map or forecast). Classification is mechanical from kind, x type and source path; the judge may reassign or strike duplicates but cannot add. Five dimensions with forecast and composition is a 5. Ten charts of one series is one dimension.

**Forecast.** Kind `forecast`: observed + central + lower + upper per horizon period, method, baseline, backtest error, observed_through, gap to today, what the series measures. Traced to `analysis.scenarios` (`central`, `lower_sensitivity`, `upper_sensitivity`, `selected_baseline`, `backtest.mae.{no_change, linear_drift}`, `observed_through`, `probabilities: null`, `stale_for_present`) over `analysis.history`; or recomputable by the script from a traced observed series (linear drift, mean growth, no-change within 5%); or labelled estimate. Bounds read as probabilities when the tool says `probabilities: null` cap at 2. A forecast of a real-world quantity (deaths, AQI) needs a published source or the estimate label; a corpus forecast must not be sold as one. Forecast accuracy stays rejected (v2): the future is unavailable; method disclosure is what is scored.

**Cross-domain synthesis.** Every traced number is attributed to a corpus by its source path (`volumes.research`/`research_series` → research; `volumes.pubmed`/`health_evidence` → health; `volumes.news`/`news_series`/`news.*` → news; `volumes.patents`/`patent_origin` → patents). Score = distinct corpora with traced numbers, plus connecting sentences (≥2 traced numbers from different corpora, windows stated, no cross-lane arithmetic). A six-corpus volumes table is one layer and caps at 2. Anchor 5 needs a connection that changes the verdict or option.

**Integrity.** Headless Chrome with an init shim that (a) freezes `console.error/warn` and `window.onerror` into an array before page scripts run, (b) intercepts the assignment of `window.vegaEmbed` and wraps it to force `renderer: 'svg'` and store each view by element id, (c) logs every request and serves cached copies of the pinned CDN scripts and the topojson on interception. Then: every manifest chart id has a view whose inline data equals the manifest points; maps have a filled geoshape mark; zero console errors; verdict visible in the first screen; 1280 and 390 px without overflow; under 4 MB. A page with no charts caps at 2 here and scores 0 on chart, dimensions, map and forecast.

**Actionability (policy).** `table#policy-options` with the six columns in order, ≥2 options plus status quo. Script: who-acts lexicon (a ministry, board, state, municipal body, regulator, Parliament; "the government" fails), evidence tags that resolve, cost/benefit figures tagged or `(est.)` or "not measured" (an untagged number here is invented and trips the gate), indicator fuzzy-matched to an export name or chart title in the manifest, a recommended option, a counter-evidence sentence with a resolving tag, a "do not know" list with a query per gap (executed through `REGISTRY` for Prism setups). Judge: trade-offs real, recommendation follows from verdict and forecast.

**Article (research).** `article#research-article` with the seven headings in order, abstract 150–300 words, ≥2,000 words. Script: Data and methods must name every recorded feature (or data source) and every window string must equal a recorded window; analysis verbs (meta-analysis, regression, pooled) must correspond to something in the record or a recomputable step, else "claimed analysis not performed"; Results numbers traced; a "we find / our analysis shows" sentence with untraced unlabelled numbers is an invented finding (0 + gate); figure/table references map to manifest charts/exports; `[rN]` keys match the reference list and resolve. Judge: one argument chain, methods honesty, reviewer acceptability. An honest literature review that performs no new analysis and whose DOIs resolve caps at 3; that is the fair ceiling for a plain model, not a zero.

### 2.2 What changes in the kept parameters

- Numbers are extracted from the rendered page's `innerText` (minus scripts and the manifest) instead of markdown prose; the `[cN]/[rN]/(est.)` grammar is supplied by the prompts because the contract has none.
- Charts, exports, calls and references come from the manifest; CSV from `exports[].csv`.
- Live reconciliation: a declared `cN` whose feature+args the harness did not record is a ghost: ignored, flagged, and the numbers it claims to support become untraced. Replay through `REGISTRY` with cache hits recorded.
- Reference record for the accuracy judge is the union of both Prism setups' recorded responses, labelled, with the note that the plain setups never saw it.
- Limits adds: patent lag beside patent counts, `placed_pct` beside maps, `observed_through`/`stale_for_present` beside forecasts, lane beside every geography row.
- Counted limits: 10 charts, 6 exports, 8 (policy) / 15 (research) references, 8 follow-ups, options ≥3 rows.

### 2.3 Gates

Invention gate (cap 40) now also covers map points, forecast fields, options-table figures and article findings. Render gate: no html fence, page does not render, or manifest unparsable → integrity 0 and cap 25, with whatever the manifest or DOM still yields scored. Timeout gate: no deliverable within the wall budget → zeros, `timed_out=true`, included in the means. Dump gate kept.

## 3. The prompts

Two prompts in the JSON, verbatim for all four setups, placeholders `{topic}`, `{today}`, `{contract}`. `{topic}` is rendered as `<label> (central claim: <central_claim>)` from the drawn pool entry so the evidence questions are fixed per topic. The harness appends the v2-style setup suffix (bare: own knowledge only, memory charts allowed with `ref`/`estimate`; prism_live: connected to a research and news intelligence MCP, cite calls as `call:<feature>#<n>`). Neither prompt names Prism. Every scored item is an explicit numbered ask: verdict, tagged numbers, two-lane trend, India-vs-comparators on one scale, map with lane and caveat, five of seven dimensions, three-year forecast with method/bounds/backtest/staleness, four corpora connected, options table (policy) or five RQs and the seven-section article (research), drill-down with executable queries, three exports, limits beside numbers, resolvable references, and the counted limits.

## 4. Topic pool

Nine topics, each with a claim-shaped centre (so `research.evidence/counter_evidence/statistics/geography` answer it), news terms with Indian and global coverage, a patentable layer and a disease-factor direction. Drawn once with a recorded seed; the same topic serves both tiers.

| Slug | Central claim | Expected |
| --- | --- | --- |
| air-pollution | PM2.5 increases mortality | Prism strongest (115k typed papers, India-heavy news, filters/monitoring patents, dense factor claims) |
| extreme-heat | heatwaves increase all-cause mortality | strong on news/geo/forecast; evidence lane thinner (128 readable intersection papers) |
| antimicrobial-resistance | antibiotic overuse drives AMR | strong; smaller news lane makes attention-vs-evidence the interesting result |
| dengue-climate | warming expands dengue transmission | strong map/comparison: India 23.8% of news share with lift 3.6, USA leads authorship |
| sugar-obesity-diabetes | sugary drinks raise T2D risk | strong on health; the tax literature is well known, so bare Claude competes on refs/actionability |
| tobacco-vaping | adolescent vaping leads to smoking | strong; factor-direction tally is a clear win; gateway debate well known to bare models |
| microplastics-health | microplastic exposure harms health | **expected weak**: thin factor claims, short history → poor backtest; bare may tie on evidence |
| pfas-forever-chemicals | PFAS exposure raises cancer risk | **expected weak**: India absent from every lane (honest empty map scores low on comparison 5); intersection lane 55 papers; bare Claude recalls the C8 studies |
| teen-social-media | social media use increases adolescent depression | **expected weak**: patents and factor claims near-empty (crossdomain caps 3); contested literature bare Claude knows; a bare win on article/refs would be the correct result |

"Climate change" alone is too broad for the claim-shaped tools; it is carried by extreme-heat and dengue-climate. If the bare label is wanted, the JSON gives the claim to use.

## 5. Timing: reconsidered and kept report-only

Recorded per setup: wall clock, first output, first and last tool call, tool calls (failed, distinct features), tool-busy seconds (union of intervals, plus the plain sum), model seconds (wall minus busy), tokens (claude `result.usage`; codex `token_count`), cost (claude `total_cost_usd`; codex null), turns, deliverable bytes, timed_out. Per call: feature, args, start, seconds, server `meta.seconds`, cache hit, ok, chars, the FULL response. Derived: traced numbers per minute and per tool-second, traced charts per minute, tool seconds per traced number, writing share after the last call.

Not scored, for four reasons the JSON states: speed is mostly a CLI and cluster property (claude -p vs codex exec; cold vs warm the index; the 12-hour Prism cache makes whichever Prism setup runs second look faster, so a speed score would score run order); it rewards abstention, which is what the benchmark exposes; against the human comparator (days) every setup wins and the ranking among them is noise; the timeout is already a gate. Two gates: 3,600 s wall budget, 600 s per call. Run the two Prism setups concurrently or clear the cache between them, and report tool seconds split cached/uncached.

Reported as a tier ladder (casual / policy / research × setup: score, wall minutes, calls, tool-busy minutes, tokens, cost), a per-tier timing table, an efficiency table, and a per-call appendix whose slowest five feed the engineering flags. Casual tier: wall seconds from `answers.json` as they are; tool calls 0 (captured mode); a reconstructed "capture seconds" column from `docs/examples/<slug>.json` `meta.seconds`, labelled as outside the respondent's wall clock; the tier marked captured and never compared on speed with the live tiers. No re-run.

## 6. Contract: nothing makes fair scoring impossible; two things must be added, several should be

**Add or integrity anchors 4–5 become screenshot judgement:**
1. "Render each chart with `vegaEmbed('#<chart id>', spec)` and inline the data as `values`." Without this the harness cannot tie a rendered view to a manifest chart.
2. Pin exact library versions and the topojson URL; the harness intercepts those URLs and serves cached copies, logging a CDN failure as `cdn_fallback`, never as the respondent's console error.

**Fix if you can:**
- `id="prism-manifest"` and "prism-calls" put the brand in front of the plain models. Cosmetic (they have no tools and are told so), but `report-manifest` / `calls` removes the question; if kept, print it in the report.
- Allow ISO alpha-3 in map `points[][0]`; say the harness normalises names (`England` → GB, lowercase labels). A wrong name-to-id join is a grey map (integrity), not a map-parameter loss.
- Define the forecast object's fields (`observed, central, lower, upper, method, baseline?, backtest?, observed_through?`); without names the script cannot tell central from bounds.
- Accept `calls: []` and follow-ups with `question` + `query_in_words` and no `feature/args` for plain setups; only entries with feature+args execute (the v2 structural gap, stated).
- The options table and the article are DOM elements the prompts require; mirroring options in the manifest is optional.
- Cap exports at 2,000 rows and the page at 4 MB.
- Live mode has no single reference record; the judge gets the union of both Prism setups' responses, labelled.
- codex may end its turn before a 100-second `research.geography` returns; wall budget 3,600 s, per-call 600 s, and incomplete runs recorded as `timed_out` rather than scored as a truncated page.

## 7. Where Prism should lose, so the report can say so

- Topics in the expected-weak list: thin factor claims and short histories (microplastics), India absent (PFAS), no patent layer and a contested literature bare models know (teen social media). A bare win on article and refs there is the correct result for a corpus gap.
- Actionability on sugar tax and tobacco: the policy literature is canonical; bare Claude can reach 3–4 with resolving DOIs while Prism's gain is the indicator column and the executable "do not know" queries.
- ChatGPT + Prism live on slow tools until the request/poll path is automatic.
- Integrity: plain models write cleaner single-file HTML more often than tool-driven runs that paste large responses; expect the plain setups to win integrity on some runs. That is why integrity is 5–6 points, not 15.
