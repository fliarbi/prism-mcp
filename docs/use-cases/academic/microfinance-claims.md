# Microfinance: empowerment or debt trap?

[Academic research & literature review](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Two competing claims measured the same way.  
> **Why it is hard.** The 2015 RCT wave turned the consensus; both sides persist.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below. Saved responses: [microfinance-claims.json](../../examples/microfinance-claims.json).

**The question:**

> Does microfinance empower women, or does it create debt traps? Compare the evidence.

## What Prism returned

| | Claim | Papers on both sides | Read: supports / contradicts / qualifies / unrelated | Contested | Strongest source |
| --- | --- | ---: | --- | ---: | --- |
| A | Microfinance empowers women | 376 | 1 / 0 / 0 / 9 | 44.9% | Role of Microfinance Institutions in Women Empowerment: A Case Study of Akhuwat, Pakistan (2015, article, supports) |
| B | Microfinance causes over-indebtedness | – | 0 / 0 / 0 / 12 | 35% | [Adoption of agricultural technology in the developing world: A meta-analysis of the empirical literature](https://doi.org/10.1016/j.worlddev.2021.105599) (2021, meta_analysis, unrelated) |

![Claim A framing](../img/microfinance-claims-claim-a.svg)

![Claim B framing](../img/microfinance-claims-claim-b.svg)

> **Prism's comparison:** the first claim has more evidence behind it

*A larger pool is not stronger evidence: the counts say how much research frames each claim, the read documents say what the strongest sources found.*

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/microfinance-claims-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured comparison | 4.0 | 4.5 | 1.5 | 1.0 |
| Visualisation from counted data | 0.0 | 0.0 | 0.0 | 0.0 |
| Exploration and drill-down | 2.0 | 1.0 | 1.5 | 1.0 |
| Data export with provenance | 4.5 | 4.5 | 1.0 | 0.0 |
| Reproducibility | 3.0 | 4.5 | 0.0 | 1.0 |
| Traceable references | 2.5 | 2.5 | 1.5 | 3.5 |
| Accuracy against the corpus | 2.0 | 4.0 | 2.0 | 2.5 |
| Calibration and limits | 4.0 | 4.0 | 3.0 | 4.0 |
| Decision-grade verdict | 3.0 | 3.5 | 0.0 | 3.5 |
| Facet coverage | 3.5 | 3.5 | 1.0 | 1.5 |
| **Score /100** | 54.9 | **64.8** | 21.1 | 37.1 |

**Claude Opus judge:** C was the only deliverable that kept every number traced and on the correct lane. It flagged the off-topic strongest source and the undefined contested share, and it gave a clean, provenance-backed export. D did more comparative arithmetic but mixed the intersection and subject lanes in its headline reading. The memory-only answers (A, B) could not measure anything, and B misreported a key RCT.

**GPT judge:** B is the strongest decision aid: it preserves the recorded corpus counts and provenance, calculates the limited same-scale comparison, and clearly explains why those counts cannot decide borrower outcomes. D offers richer calculations and a chart, but mixes incompatible lanes and adds unverified memory claims; A is careful but largely unmeasured, while C overstates unverified specifics.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/microfinance-claims/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/microfinance-claims.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Does microfinance empower women, or does it create debt traps? Compare the evidence.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.compare" \
  -H 'content-type: application/json' \
  -d '{"claim_a": "Microfinance empowers women", "claim_b": "Microfinance causes over-indebtedness"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_claims']["fn"](**{'claim_a': 'Microfinance empowers women', 'claim_b': 'Microfinance causes over-indebtedness'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
