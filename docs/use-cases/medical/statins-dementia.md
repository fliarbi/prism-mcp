# Statins and dementia risk

[Medical & clinical evidence](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Both directions of the claim, weighted by tier.  
> **Why it is hard.** The literature points both ways; the useful output is the tier-weighted balance, not a yes/no.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below. Saved responses: [statins-dementia.json](../../examples/statins-dementia.json).

**The question:**

> Do statins protect against dementia, or increase cognitive risk?

## What Prism returned

| | Claim | Papers on both sides | Read: supports / contradicts / qualifies / unrelated | Contested | Strongest source |
| --- | --- | ---: | --- | ---: | --- |
| A | Statins reduce dementia risk | – | 0 / 0 / 0 / 11 | 21.6% | [Dementia risk estimates associated with measures of depression: a systematic review and meta-analysis](https://doi.org/10.1136/bmjopen-2015-008853) (2015, meta_analysis, unrelated) |
| B | Statins impair cognitive function | 17 | 0 / 2 / 0 / 10 | 20.8% | [Statin use and risk of dementia or Alzheimer’s disease: a systematic review and meta-analysis of observational studies](https://doi.org/10.1093/eurjpc/zwab208) (2021, meta_analysis, contradicts) |

![Claim A framing](../img/statins-dementia-claim-a.svg)

![Claim B framing](../img/statins-dementia-claim-b.svg)

> **Prism's comparison:** the first claim has more evidence behind it

*A larger pool is not stronger evidence: the counts say how much research frames each claim, the read documents say what the strongest sources found.*

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/statins-dementia-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured comparison | 5.0 | 4.5 | 2.0 | 1.0 |
| Visualisation from counted data | 3.5 | 0.0 | 0.0 | 0.0 |
| Exploration and drill-down | 2.0 | 1.0 | 1.0 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 3.0 | 0.0 | 1.0 |
| Traceable references | 4.5 | 1.0 | 1.0 | 0.0 |
| Accuracy against the corpus | 4.5 | 2.5 | 3.5 | 2.5 |
| Calibration and limits | 4.0 | 3.0 | 3.5 | 3.0 |
| Decision-grade verdict | 4.0 | 4.0 | 3.0 | 3.5 |
| Facet coverage | 4.0 | 4.0 | 1.0 | 1.5 |
| **Score /100** | **77.8** | 51.7 | 33.1 | 29.1 |

**Claude Opus judge:** D traced nearly every number to the single comparison call and computed exact ratios. It also flagged the record's own anomaly: the off-topic depression paper returned as claim A's strongest source. C traced the same tallies but misread that field and mixed memory effect sizes into the measured layer. A and B gave reasonable clinical verdicts from memory but no measured balance, and A's citations contain fabricated venue and DOI details.

**GPT judge:** B is strongest because it turns the recorded comparison into a reproducible, correctly caveated contrast and clearly distinguishes corpus volume from clinical truth. Its chart and exports are useful, though the database has no explicit window and the clinical evidence remains unresolved; the other deliverables either rely on unverified specifics or omit the measured comparison.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/statins-dementia/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/statins-dementia.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Do statins protect against dementia, or increase cognitive risk?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.compare" \
  -H 'content-type: application/json' \
  -d '{"claim_a": "Statins reduce dementia risk", "claim_b": "Statins impair cognitive function"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_claims']["fn"](**{'claim_a': 'Statins reduce dementia risk', 'claim_b': 'Statins impair cognitive function'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
