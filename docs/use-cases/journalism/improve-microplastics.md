# Fix an overstated claim

[Journalism & fact-checking](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A better-supported rewrite plus the evidence card behind it.  
> **Why it is hard.** The evidence is mostly animal and cell studies; the rewrite must say so.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below. Saved responses: [improve-microplastics.json](../../examples/improve-microplastics.json).

**The question:**

> Rewrite this sentence so it says what the evidence supports: 'Microplastics cause cancer in humans.'

## What Prism returned

**Original:** “Microplastics cause cancer in humans”  
**Prism's verdict:** **unsupported**: No evidence directly links microplastics to cancer in humans; all cited studies are unrelated.

| Better-supported rewrite | Why |
| --- | --- |
| “There is currently no evidence that microplastics cause cancer in humans.” | Reflects the lack of supporting or qualifying evidence in the provided material. |
| “Microplastics have not been shown to cause cancer in humans.” | Accurately conveys that the evidence does not support the claim. |
| “Evidence linking microplastics to cancer in humans is lacking.” | States the absence of relevant findings while matching the original sentence length. |

Based on 11 documents read (0 support, 0 contradict, 0 qualify, 10 unrelated). Lane: *only 6 papers cover both sides of this claim, so the evidence below is about microplastic particles, microplastic exposure alone and does not establish the connection the claim asserts*.

> **No evidence card:** 11 documents were read and none speaks to this claim as written. Prism does not promote an unrelated paper to 'strongest evidence'.

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/improve-microplastics-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Reproducibility | 3.0 | 2.0 | 1.0 | 1.0 |
| Traceable references | 1.0 | 1.0 | 1.5 | 0.5 |
| Accuracy against the corpus | 2.5 | 3.0 | 3.5 | 4.0 |
| Calibration and limits | 4.0 | 3.0 | 3.0 | 2.5 |
| Decision-grade verdict | 3.5 | 3.5 | 3.5 | 3.0 |
| Facet coverage | 4.0 | 3.5 | 2.0 | 1.5 |
| **Score /100** | **59.3** | 53.4 | 49.7 | 44.5 |

**Claude Opus judge:** Only A's rewrite says what the evidence actually is: plastic particles found in human tissue, plausible mechanisms in cell and animal studies, and no human causal evidence. That is the crux of the question. A also introduced no fabrications. D was the best grounded and read the subject-lane corpus mix correctly, but it invented contents for the failed evidence-card call and gave a rewrite that omits the animal and cell basis. C had the same fabrication problem. B was honest but thin.

**GPT judge:** D best equips a decision-maker with a cautious rewrite, a clear policy boundary, and the relevant distinction between broad topic counts and evidence directly testing human cancer causation. Its c2 document-count error and unsupported background account keep it below a clean result; A is the more internally consistent alternative but is less complete about the evidence facets.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/improve-microplastics/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/improve-microplastics.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Rewrite this sentence so it says what the evidence supports: 'Microplastics cause cancer in humans.'
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.improve" \
  -H 'content-type: application/json' \
  -d '{"claim": "Microplastics cause cancer in humans"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['improve_claim']["fn"](**{'claim': 'Microplastics cause cancer in humans'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `improve_claim` (59.1 s) → `evidence_card` (0.0 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
