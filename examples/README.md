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

Most reports are one `research.evidence` (`find_evidence`) call per angle; the two fields that carry
the insight are `lane_counts.intersection` (is the evidence even there?) and `tally.counts` (which
way the read documents fall). Some go further — `stance_trends`, `news_trends`, `news_geography`,
`research_gaps` (CRISPR) and `news_themes` + `disease_profile` (east UP). The examples span health,
economics, climate and regional development on purpose: the honesty model — lane, window, coverage,
evidence-vs-interpretation, like-with-like units, and the refusal to fabricate — is the same in every
domain.
