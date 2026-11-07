# Examples

Worked examples of the analysis Prism is built for — each one real data, the exact calls that
produced it, charts generated from the responses, and a cross-angle synthesis. Each folder's
`README.md` renders on GitHub as the full report.

| Example | Subject | The cross-angle finding |
|---|---|---|
| [intermittent-fasting-glycemic-control](./intermittent-fasting-glycemic-control/) | nutrition / metabolism | **Belief ≠ evidence** — fasting is marketed for the two angles (weight vs. dieting, heart disease) the corpus *least* supports; its real strengths are the quiet metabolic ones (blood pressure, liver fat, glucose). |
| [semaglutide](./semaglutide/) | pharmacology | **Proven core, unsettled frontier** — rigorously proven where it was trialed (weight, cardiovascular events), but thin or unsettled on the off-label frontier (alcohol) and safety questions (muscle, thyroid). |
| [crispr-gene-editing](./crispr-gene-editing/) | genetics / biotech | **Positive ≠ proven** — a field that reads "breakthrough" everywhere, yet evidence depth spans two orders of magnitude: deep on funded therapies (cancer), most contested on safety (off-target), thin-to-absent on a crop promise and a tool-vs-tool comparison — and one claim the lane honestly couldn't measure. |
| [minimum-wage](./minimum-wage/) | economics / labour policy | **Volume of debate ≠ depth of evidence** — the claims shouted loudest (teen layoffs, shuttered small businesses) have the *least* both-sides research (2 and 0 papers, ~3,000 news mentions each); the effect the corpus actually pins down is prices. |
| [electric-vehicles](./electric-vehicles/) | climate / energy | **Solid core, conditional caveats** — EVs cut emissions (2,156 papers, 48:1 supporting) and every objection is real but *conditional*: on the grid mix, the mileage, the segment. The one place framing and read-evidence openly disagree (grid strain). |
| [east-uttar-pradesh](./east-uttar-pradesh/) | regional / development | **A place, not a claim** — profiles a region from the news problem-space and the disease-claim layer, and shows the honest boundary: three region-specific research lanes return 0, 0 and 4 papers, so Prism says "no data" instead of fabricating one. |
| [ultra-processed-foods](./ultra-processed-foods/) | nutrition / public health | **One direction, five outcomes** — UPF is consistently associated with higher risk across obesity, type 2 diabetes, heart disease, all-cause mortality and depression (pooled ratios 1.10–1.55), yet every lane is observational and certainty is often graded *very low*; the brief reports the association and flags the confounding and publication-bias caveats instead of asserting cause. |
| [social-media-adolescent-mental-health](./social-media-adolescent-mental-health/) | psychology / society | **The headline outruns the evidence** — the clearest signals are small (depression, r = .11) or specific (night-time sleep); self-esteem and loneliness are genuinely inconsistent; and the anxiety claim has just **4 both-sides papers** against 104,000 on the subject, so it is filed as not established. |

Most reports are one `research.evidence` (`find_evidence`) call per angle; the two fields that carry
the insight are `lane_counts.intersection` (is the evidence even there?) and `tally.counts` (which
way the read documents fall). Some go further — `stance_trends`, `news_trends`, `news_geography`,
`research_gaps` (CRISPR), `stance_trends` (ultra-processed foods) and `news_themes` + `disease_profile`
(east UP). The examples span health, nutrition, economics, climate, psychology and regional development
on purpose: the honesty model — lane, window, coverage, evidence-vs-interpretation, like-with-like units,
and the refusal to fabricate — is the same in every domain.

Each example folder also carries a self-contained `index.html` (the same report, styled for reading in
light or dark) and links its hosted copy at the top.
