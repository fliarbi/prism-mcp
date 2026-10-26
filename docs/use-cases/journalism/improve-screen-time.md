# Fix a screen-time claim

[Journalism & fact-checking](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A defensible rewrite and the strongest source.  
> **Why it is hard.** Association is not causation; the rewrite must downgrade the verb.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below. Saved responses: [improve-screen-time.json](../../examples/improve-screen-time.json).

**The question:**

> Rewrite: 'Screen time causes ADHD in children.'

## What Prism returned

**Original:** “Screen time causes ADHD in children”  
**Prism's verdict:** **overstated**: The claim asserts causation, but evidence only shows association and mixed findings; no direct causal evidence is provided.

| Better-supported rewrite | Why |
| --- | --- |
| “Screen time is associated with ADHD in children” | Reflects the observed association without implying causation. |
| “Screen time has been linked to ADHD symptoms in children” | Indicates a connection while acknowledging that the evidence is not definitive for causation. |
| “Evidence suggests screen time may be related to ADHD in children” | Conveys the tentative nature of the relationship given mixed and qualifying evidence. |

Based on 11 documents read (0 support, 0 contradict, 0 qualify, 10 unrelated). Lane: *only 0 papers cover both sides of this claim, so the evidence below is about media consumption, screen time exposure alone and does not establish the connection the claim asserts*.

> **No evidence card:** 11 documents were read and none speaks to this claim as written. Prism does not promote an unrelated paper to 'strongest evidence'.

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/improve-screen-time-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Reproducibility | 2.5 | 2.5 | 1.0 | 0.0 |
| Traceable references | 1.0 | 1.0 | 1.0 | 1.0 |
| Accuracy against the corpus | 3.0 | 3.5 | 3.5 | 1.5 |
| Calibration and limits | 4.5 | 4.0 | 4.0 | 2.5 |
| Decision-grade verdict | 4.0 | 3.5 | 4.0 | 3.0 |
| Facet coverage | 4.0 | 3.0 | 1.0 | 1.0 |
| **Score /100** | **62.8** | 59.3 | 51.0 | 30.3 |

**Claude Opus judge:** All four correctly downgrade 'causes' to an associational verb. B best tied its rewrite, the corpus mix and the subject-lane caveat to the recorded call, and gave a calibrated low confidence. B and C both lose points for quoting text from a c2 call that actually returned null. D's polished citations rest on an unresolvable DOI, and A is an honest memory answer with one factual slip.

**GPT judge:** B is the most decision-ready: it gives a clear noncausal rewrite and accurately reports the assessment, lane caveat, corpus classifications, and missing evidence card. C covers more implied facets, but misattributes the 11-document tally to the empty evidence-card call; A is candid but largely memory-based, while D relies on an unresolved DOI.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/improve-screen-time/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/improve-screen-time.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Rewrite: 'Screen time causes ADHD in children.'
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.improve" \
  -H 'content-type: application/json' \
  -d '{"claim": "Screen time causes ADHD in children"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['improve_claim']["fn"](**{'claim': 'Screen time causes ADHD in children'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `improve_claim` (48.4 s) → `evidence_card` (0.0 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
