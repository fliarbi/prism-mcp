# Do interest rates drive house prices?

[Finance & markets](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Effect sizes from economics literature.  
> **Why it is hard.** Economics papers, not medical: tiering has to fall back from RCT logic to study type.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [housing-prices-evidence.json](../../examples/housing-prices-evidence.json).

**The question:**

> How strong is the evidence that rising interest rates lower house prices?

## What Prism returned

### How much evidence exists

| Corpus | Records on both sides of the claim | Window |
| --- | ---: | --- |
| Typed research papers | 64 | 2017-2025 |
| Papers with abstracts | 59 | 1990-2025 |
| the health literature index records | 1 | 1990-2025 |
| News articles | 22,397 | 2019-01-01..2026-06-01 |
| Patents | 0 | 2005-2024 |
| arXiv preprints | 1 | 2005-2025 |

![Evidence volume by corpus](../img/housing-prices-evidence-volumes.svg)

![Framing of the literature](../img/housing-prices-evidence-sides.svg)

*orientation is a label on the paper's own framing, not a verdict on the claim; this corpus starts in 2017* Contested share: **50%**.

### The strongest evidence, read

> few titles carry both sides of this claim, so the documents read were chosen by the subject in the title and the outcome in the abstract.

Prism read 1 sources: **1 support, 0 contradict, 0 qualify** (tier-weighted {"supports": 3, "contradicts": 0, "qualifies": 0}). Each quote is copied from the abstract and verified against it; 0 candidate quotes failed that check and were dropped.

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2021 | [The effect of rising interest rates on Swedish condominium prices.](http://hdl.handle.net/2077/67637)<br><sub>Gothenburg University Publications Electronic Archive (Gothenburg University)</sub> | article | supports | The inverse relationship between interest rates and condominium prices are in line with general economic theory that describes the relationship between capital goods and real interest rates. |
| 2024 | [Book Value Risk Management of Banks: Limited Hedging, HTM Accounting, and Rising Interest Rates](https://doi.org/10.3386/w32293)<br><sub>National Bureau of Economic Research</sub> | article | unrelated | In the face of rising interest rates in 2022, banks mitigated interest rate exposure of the accounting value of their assets but left the vast majority of their long-duration assets exposed to interest rate risk. |
| 2014 | [Rising Interest Rates](https://digitalcommons.butler.edu/jmdallchapters/89)<br><sub>Digital Commons @ Butler University (Butler University)</sub> | article | unrelated | Interest rates have remained at historically low levels since 2008; however, with the recovering economy and the prospect of the Fed reducing its intervention, it is likely that interest rates will rise. |
| 2023 | [The effect of high inflation and rising interest rates on real estate values and valuation approach](https://doi.org/10.69554/hcdt7364)<br><sub>Journal of building survey, appraisal & valuation</sub> | article | unrelated | This paper looks at how rising inflation and interest rates affect values and also how valuers need to develop new skills and understanding in valuing real estate assets in increasingly interconnected global financial markets. |
| 2022 | [Rising interest rates reduce inflation: an empirical study for the Republic of North Macedonia](https://doi.org/10.20544/horizons.a.30.1.22.p10)<br><sub>HORIZONS A</sub> | article | unrelated | An increase in interest rates reduces inflation. |
| 2019 | Effects of US Interest Rate Hikes and Global Risk on Daily Capital Flows in Emerging Market Countries<br><sub>RePEc: Research Papers in Economics</sub> | preprint | unrelated | The interest rate hikes in the United States and higher global risk aversion have increased capital outflows from emerging market countries in recent years. |

![Study designs](../img/housing-prices-evidence-tiers.svg)

### What disagrees

Prism's counter-evidence pass found no source that directly contradicts the claim among those it read (tally {"supports": 1, "contradicts": 0, "qualifies": 0, "unrelated": 6, "unread": 0}).

> The documents read support the claim; this selected sample does not establish scientific consensus.

![Research output per year](../img/housing-prices-evidence-research-series.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/housing-prices-evidence-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 3.5 | 1.0 | 0.0 |
| Measured comparison | 3.0 | 3.5 | 2.0 | 0.5 |
| Visualisation from counted data | 3.5 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 2.5 | 1.0 | 1.0 | 1.0 |
| Data export with provenance | 2.5 | 3.5 | 1.0 | 1.0 |
| Reproducibility | 3.0 | 3.0 | 1.0 | 1.0 |
| Traceable references | 4.5 | 2.0 | 1.0 | 3.5 |
| Accuracy against the corpus | 2.5 | 4.0 | 3.5 | 3.5 |
| Calibration and limits | 4.0 | 4.0 | 3.5 | 3.0 |
| Decision-grade verdict | 4.0 | 4.0 | 3.0 | 3.5 |
| Facet coverage | 4.5 | 4.0 | 1.5 | 1.5 |
| **Score /100** | **68.5** | 66.7 | 36.8 | 35.1 |

**Claude Opus judge:** B and D both read the database honestly: thin evidence, only 9 papers in the intersection lane, one supporting Swedish paper and no measured effect size. Both give low-confidence verdicts bounded by those limits. D had richer references and caught the c1/c2 anomaly, but its derived news comparison is materially miscalculated. B's cleaner exports and arithmetic edge it ahead. A and C answer from memory: A gives labelled estimates with no identifiers, and C cites real DOIs but has no measured content.

**GPT judge:** C is the most useful for a decision-maker: it surfaces the crucial mismatch between the broad subject corpus and the small joint-claim intersection, gives a traced trend, and makes a suitably cautious recommendation. A is also careful and has stronger export coverage, but its missing follow-up execution and censored-endpoint handling weaken reproducibility; B and D rely on memory or provide no measured evidence.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/housing-prices-evidence/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/housing-prices-evidence.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How strong is the evidence that rising interest rates lower house prices?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.evidence" \
  -H 'content-type: application/json' \
  -d '{"claim": "Rising interest rates reduce house prices", "limit": 10}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['find_evidence']["fn"](**{'claim': 'Rising interest rates reduce house prices', 'limit': 10})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `find_evidence` (94.5 s) → `find_counter_evidence` (2.3 s) → `find_statistics` (7.9 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
