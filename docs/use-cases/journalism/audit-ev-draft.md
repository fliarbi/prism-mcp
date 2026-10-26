# Audit an EV explainer

[Journalism & fact-checking](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Claim-by-claim evidence status for a tech explainer.  
> **Why it is hard.** Lifecycle-emissions claims need research, not news.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [audit-ev-draft.json](../../examples/audit-ev-draft.json).

**The question:**

> Fact-check this electric-vehicle explainer.
> 
> Electric vehicles produce fewer lifetime emissions than petrol cars even on coal-heavy grids. EV batteries lose most of their capacity within five years. Battery fires are more common in electric vehicles than in petrol cars.

## What Prism returned

**3 claims detected**, 2 checkable by research. Evidence coverage 50%: *share of the RESEARCH-CHECKABLE claims with a literature behind them, weighted by how directly it speaks to the claim. Claims only a record could settle are excluded rather than counted as failures. It is not a truth score: it says a body of work exists, not that the work agrees*

| # | Claim | Status | Papers on both sides | Searched as | What could be wrong |
| ---: | --- | --- | ---: | --- | --- |
| 1 | Electric vehicles produce fewer lifetime emissions than petrol cars even on coal-heavy grids. | **claim_covered** | 8,695 | electric vehicles, petrol cars + lifetime emissions | definition of "lifetime emissions" may vary across studies |
| 2 | EV batteries lose most of their capacity within five years. | **no_literature** | 0 | ev batteries | "most" is vague and depends on measurement methods |
| 3 | Battery fires are more common in electric vehicles than in petrol cars. | **not_research** | – | battery fires, electric vehicles | underreporting of fire incidents may bias the comparison |

![Claim status](../img/audit-ev-draft-status.svg)

<details><summary>What each status means</summary>

- **not_research**: only a record — a filing, a register or a news report — could settle this. Prism's research corpus has no opinion, and that is not the same as the claim being wrong
- **no_literature**: no paper title matches this claim's own wording. The field may still cover it under different words — run research.evidence on the claim to find out
- **thin_literature**: a handful of paper titles match this wording — too few to rest an assertion on without reading them
- **literature_exists**: research exists on this subject — which is not the same as research agreeing with the claim; research.evidence reads it
- **claim_covered**: papers cover BOTH sides of the claim, so the literature speaks to it directly
- **unchecked**: the corpus lane failed for this claim
</details>

### Deep reads of the weakest claims

**EV batteries lose most of their capacity within five years.**: 0 support, 0 contradict, 0 qualify

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/audit-ev-draft-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Visualisation from counted data | 0.0 | 0.0 | 0.0 | 0.0 |
| Exploration and drill-down | 4.5 | 1.0 | 1.5 | 1.0 |
| Data export with provenance | 2.5 | 4.5 | 1.0 | 1.0 |
| Reproducibility | 4.0 | 4.5 | 1.0 | 0.0 |
| Traceable references | 4.5 | 1.0 | 1.0 | 1.5 |
| Accuracy against the corpus | 4.0 | 3.5 | 2.5 | 3.0 |
| Calibration and limits | 4.5 | 3.0 | 3.5 | 4.0 |
| Decision-grade verdict | 3.0 | 3.5 | 2.5 | 3.5 |
| Facet coverage | 4.5 | 4.0 | 1.5 | 2.0 |
| **Score /100** | **68.1** | 57.1 | 32.7 | 35.9 |

**Claude Opus judge:** B best combined traced audit facts with honest, clearly labelled background judgment on whether each claim is true. It also caught the record's internal inconsistencies, and it carried resolvable DOIs with verbatim quotes. A was fully traced but never told the reader whether the claims were true. C and D answered from memory: C was useful but leaned on a weak fire statistic, and D presented unverifiable quotes and hedged where the literature is clear.

**GPT judge:** D is strongest for a decision-maker because its measured figures are reproducible, its references resolve, and it exposes important inconsistencies and limits in the audit. Its recommendation still needs care: the audit’s claim_covered status means literature addresses both sides of the emissions claim, not that the claim is supported.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/audit-ev-draft/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/audit-ev-draft.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Fact-check this electric-vehicle explainer.

Electric vehicles produce fewer lifetime emissions than petrol cars even on coal-heavy grids. EV batteries lose most of their capacity within five years. Battery fires are more common in electric vehicles than in petrol cars.
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.audit" \
  -H 'content-type: application/json' \
  -d '{"text": "Electric vehicles produce fewer lifetime emissions than petrol cars even on coal-heavy grids. EV batteries lose most of their capacity within five years. Battery fires are more common in electric vehicles than in petrol cars.", "deep": 3}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_audit']["fn"](**{'text': 'Electric vehicles produce fewer lifetime emissions than petrol cars even on coal-heavy grids. EV batteries lose most of their capacity within five years. Battery fires are more common in electric vehicles than in petrol cars.', 'deep': 3})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
