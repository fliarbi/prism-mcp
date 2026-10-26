# Minimum wage and jobs

[Policy & regulation](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Both poles of the classic labour-economics debate.  
> **Why it is hard.** The literature is genuinely split; tier-weighting is the whole answer.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below. Saved responses: [minimum-wage-employment.json](../../examples/minimum-wage-employment.json).

**The question:**

> Do minimum wage increases reduce employment? Compare with the claim that they raise wages without job loss.

## What Prism returned

| | Claim | Papers on both sides | Read: supports / contradicts / qualifies / unrelated | Contested | Strongest source |
| --- | --- | ---: | --- | ---: | --- |
| A | Minimum wage increases reduce employment | 238 | 0 / 1 / 0 / 0 | 33.6% | The effect of minimum wage increases on wages, hours worked and job loss (2018, preprint, contradicts) |
| B | Minimum wage increases raise earnings without job losses | 32,032 | 0 / 0 / 0 / 9 | 39.1% | [Are the Effects of Minimum Wage Increases Always Small? New Evidence from a Case Study of New York State](https://doi.org/10.1177/001979391206500207) (2012, article, unrelated) |

![Claim A framing](../img/minimum-wage-employment-claim-a.svg)

![Claim B framing](../img/minimum-wage-employment-claim-b.svg)

> **Prism's comparison:** the second claim has more evidence behind it

*A larger pool is not stronger evidence: the counts say how much research frames each claim, the read documents say what the strongest sources found.*

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/minimum-wage-employment-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured comparison | 5.0 | 4.5 | 2.0 | 1.0 |
| Visualisation from counted data | 0.0 | 0.0 | 0.0 | 0.0 |
| Exploration and drill-down | 3.0 | 1.0 | 1.0 | 1.5 |
| Data export with provenance | 4.5 | 4.5 | 1.0 | 0.0 |
| Reproducibility | 3.0 | 4.5 | 1.0 | 1.0 |
| Traceable references | 1.5 | 2.0 | 1.0 | 1.0 |
| Accuracy against the corpus | 4.5 | 3.0 | 2.0 | 2.5 |
| Calibration and limits | 5.0 | 4.5 | 4.0 | 3.0 |
| Decision-grade verdict | 4.5 | 4.0 | 0.0 | 3.5 |
| Facet coverage | 4.0 | 4.5 | 2.0 | 2.0 |
| **Score /100** | **69.3** | 64.8 | 26.0 | 32.3 |

**Claude Opus judge:** A was the only deliverable that used the measured record to read its own instrument. It normalised the stance mixes, showed that claim B's 32,032 count is a matching artifact (99.4% of its subject set), and turned that into the decision rule 'do not cite the count as proof', with every derived number recomputing exactly. B traced cleanly but stopped at the headline ratio and misread tier fields. C and D answered from memory, C with a likely fabricated DOI and a misquote, and D with an untagged threshold in its verdict.

**GPT judge:** C is strongest for a decision-maker because its comparisons, exports, and numerical claims are reproducible and it clearly separates corpus volume from causal evidence. Its missing chart, weak document references, and unexecuted follow-ups limit the deliverable, but D’s apparent breadth is weakened by an unsupported chart window and untraced numbers.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/minimum-wage-employment/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/minimum-wage-employment.pdf)

## Live MCP session

Here each model was given only the question and a live connection to the Prism MCP server, and chose its own calls.

**Claude** (claude-sonnet, 692.3 s) called 2 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `find_evidence` | `{"claim": "Minimum wage increases reduce employment", "limit": 10}` | ok · 7,209 chars |
| 2 | `compare_claims` | `{"claim_a": "Minimum wage increases reduce employment", "claim_b": "Minimum wage increases raise wages without job loss"}` | ok · 1,735 chars |

<details><summary>Claude's answer</summary>

**Direct answer:** Prism's evidence doesn't show that minimum wage increases reduce employment in general. Moderate increases most often show small or no job losses. The evidence is thin, though, and it doesn't settle the question.

**What the data shows**
- The only paper Prism read in full for the "reduces employment" claim contradicts it. It is Bishop (2018), a non-peer-reviewed preprint on Australian award wages. He reports "no evidence that these small, incremental increases… have an adverse effect on hours worked or the job destruction rate."
- Prism's typed-paper corpus (2017–2025) has 1,158 papers on both minimum wage increases and job loss. By their own framing, 222 support the claim, 389 qualify it, 57 contradict it and 490 are neutral. 38.5% are contested.
- For "raises wages without job loss", 32,221 papers cover both sides. 6,789 support the claim, 10,300 qualify it, 2,286 contradict it and 12,846 are neutral. 39.1% are contested.
- Prism's tool judged the second claim to have more evidence behind it. Its strongest source is Are the Effects of Minimum Wage Increases Always Small? (2012), a case study of New York State, which it tagged as contradicting the claim.
- Prism read only 1 paper for the first claim and 10 for the second, and none came back as "supports."

**Interpretation (mine, not measured)**
- The better-supported conclusion is that the average effect of moderate increases on employment is small. Effects likely depend on how large the increase is relative to local wages and on the labor market.
- Neither claim is clean. "No job loss" is too strong, and "reduces employment" is too strong for modest increases.
- The 2017–2025 corpus is mostly framing labels, not effect sizes. The two claims also matched very different pools of papers, with different breadth of subject and outcome terms. Prism's own caveat is that more evidence doesn't mean more true.

**Gaps:** I found no extracted elasticities, no meta-analysis and no the health literature index designs. Before publishing, check the leading US studies and meta-analyses directly.

</details>

**ChatGPT** (gpt-6-luna, 292.9 s) called 3 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `find_statistics` | `{"claim": "Effects of minimum wage increases on wages and employment, including evidence for no job loss", "include_context": true, "include_trend": false, "lim` | ok · 13,607 chars |
| 2 | `compare_claims` | `{"claim_a": "Minimum wage increases reduce employment", "claim_b": "Minimum wage increases raise wages without job loss", "read": true}` | ok · 3,916 chars |
| 3 | `find_statistics` | `{"claim": "minimum wage increases raise earnings or wages for low-wage workers", "include_context": true, "limit": 8}` | see payload · 13,715 chars |

<details><summary>ChatGPT's answer</summary>

**Direct answer:** Minimum wage increases reliably raise pay for affected workers, but “without job loss” is too categorical. Employment effects are often small or hard to detect on average, yet some studies find losses for particular groups or measures.

**What the data shows:** Prism’s research statistics include a 2022 study estimating that a 10% increase in the binding minimum wage reduced vacancies 2.4% immediately and potentially 4.5% one year later; vacancies are a hiring measure, not a count of jobs lost. A 2024 study found a 10% increase associated with one fewer weekly work hour for minimum wage workers. By contrast, a study using U.S. Current Population Survey data from 2004 and 2006 estimated a 20.2–21.8% employment reduction among less-skilled, less-educated workers after New York’s increase, with the largest effects for ages 16–24. That is a specific subgroup and setting, not a general estimate. ([Prism-linked 2022 study](https://doi.org/10.26509/frbc-wp-201930r), [2024 study](https://doi.org/10.1111/ecca.12555), [New York study](https://doi.org/10.1177/001979391206500207))

**Interpretation:** The evidence supports neither “always cuts jobs” nor “never costs jobs.” Outcomes vary by the size of the increase, local conditions, and who is studied; employers may also adjust through hours or vacancies rather than layoffs. The figures above establish employment-side effects, but Prism’s retrieved statistics did not provide a comparable wage-gain estimate, so they cannot quantify the “raises wages” part of the claim.

</details>

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Do minimum wage increases reduce employment? Compare with the claim that they raise wages without job loss.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.compare" \
  -H 'content-type: application/json' \
  -d '{"claim_a": "Minimum wage increases reduce employment", "claim_b": "Minimum wage increases raise earnings without job losses"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_claims']["fn"](**{'claim_a': 'Minimum wage increases reduce employment', 'claim_b': 'Minimum wage increases raise earnings without job losses'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
