# Universal basic income evidence

[Policy & regulation](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** The trial evidence for a contested policy.  
> **Why it is hard.** Pilots are small and local; the counter-evidence on labour supply must be shown.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [ubi-evidence.json](../../examples/ubi-evidence.json).

**The question:**

> Does universal basic income reduce poverty without reducing work? What does the evidence say?

## What Prism returned

### How much evidence exists

| Corpus | Records on both sides of the claim | Window |
| --- | ---: | --- |
| Typed research papers | 36,874 | 2017-2025 |
| Papers with abstracts | 355 | 1990-2025 |
| the health literature index records | 0 | 1990-2025 |
| News articles | 6 | 2019-01-01..2026-06-01 |
| Patents | 0 | 2005-2024 |
| arXiv preprints | 0 | 2005-2025 |

![Evidence volume by corpus](../img/ubi-evidence-volumes.svg)

![Framing of the literature](../img/ubi-evidence-sides.svg)

*orientation is a label on the paper's own framing, not a verdict on the claim; this corpus starts in 2017* Contested share: **41%**.

### The strongest evidence, read

Prism read 1 sources: **0 support, 0 contradict, 1 qualify** (tier-weighted {"supports": 0, "contradicts": 0, "qualifies": 3}). Each quote is copied from the abstract and verified against it; 1 candidate quotes failed that check and were dropped.

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2025 | [The potential of universal basic income schemes to buffer shocks](https://doi.org/10.1093/9780198909453.003.0011)<br><sub></sub> | article | qualifies | In normal times and in times of crisis, poverty reduction increases with the generosity of the UBI benefit amount in both countries. |
| 2013 | [Relative Effectiveness of Conditional and Unconditional Cash Transfers for Schooling Outcomes in Developing Countries: A](https://doi.org/10.4073/csr.2013.8)<br><sub>Campbell Systematic Reviews</sub> | review | unrelated | Both conditional and unconditional cash transfer programmes increase enrolment compared to no program. |
| 2022 | [Unconditional cash transfers for reducing poverty and vulnerabilities: effect on use of health services and health outco](https://doi.org/10.1002/14651858.cd011135.pub3)<br><sub>Cochrane Database of Systematic Reviews</sub> | review | unrelated | This body of evidence suggests that unconditional cash transfers (UCTs) may not impact a summary measure of health service use in children and adults in LMICs. |
| 2021 | [The mental health effects of a Universal Basic Income: A synthesis of the evidence from previous pilots](https://doi.org/10.1016/j.socscimed.2021.114374)<br><sub>Social Science & Medicine</sub> | review | unrelated | Amongst its advocates, one of the key arguments for a Universal Basic Income (UBI) is its potential to improve population mental health. |
| 2016 | [Conditional and Unconditional Cash Transfers to Improve Use of Contraception in Low and Middle Income Countries: A Syste](https://doi.org/10.1111/sifp.12004)<br><sub>Studies in Family Planning</sub> | review | unrelated | This systematic review synthesizes evidence on the impact of conditional and unconditional cash transfers (CCT and UCT) on contraception in low- and middle-income countries. |
| 2018 | [Universal Basic Incomes versus Targeted Transfers: Anti-Poverty Programs in Developing Countries](https://doi.org/10.1257/jep.32.4.201)<br><sub>The Journal of Economic Perspectives</sub> | article | unrelated | We examine how the targeting of transfer programs is conducted in these settings, and provide empirical evidence on the tradeoffs involved between universal basic income and targeted transfer schemes using data from Indonesia and Peru—two countries that run na… |
| 2019 | [Exploring Universal Basic Income: A Guide to Navigating Concepts, Evidence, and Practices](https://doi.org/10.1596/978-1-4648-1458-7)<br><sub>Washington, DC: World Bank eBooks</sub> | article | unrelated | The book’s content benefited enormously from discussions with Junaid Kamal Ahmad, Asad Alam, Nicholas Barr, Christian Bodewig, Maurizio Bussolo, Joe Chrisp, Aline Coudouel, Shantayanan Devarajan, Simeon Djankov, Louise Fox, Marcelo Giugale, Kathy Lindert, Luke… |
| 2021 | [Sustainable welfare: How do universal basic income and universal basic services compare?](https://doi.org/10.1016/j.ecolecon.2021.107152)<br><sub>Ecological Economics</sub> | article | unrelated | The paper argues that UBI and UBS are not so much conflicting but complementary approaches for supporting sustainable welfare. |

![Study designs](../img/ubi-evidence-tiers.svg)

### What disagrees

Prism's counter-evidence pass found no source that directly contradicts the claim among those it read (tally {"supports": 0, "contradicts": 0, "qualifies": 0, "unrelated": 8, "unread": 0}).

> No verified document verdict supports a wording recommendation for this claim.

### Numbers you can quote

| Figure | Measures | Population | Source |
| --- | --- | --- | --- |
| **‐0.17 standard deviations** | material hardship reduction (standard deviations) | families with less than $500 of earnings in the previous month, roughly the bottom 50 percent of monthly earnings for the study sample | [The COVID Cash Transfer Study: The Impacts of a One‐Time Unconditional Cash Transfer on the Well‐Being of Families Recei](https://doi.org/10.1002/pam.22464) 2023 |

![Research output per year](../img/ubi-evidence-research-series.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/ubi-evidence-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 3.0 | 1.0 | 0.0 |
| Measured comparison | 2.5 | 1.5 | 2.0 | 1.5 |
| Visualisation from counted data | 3.5 | 3.0 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 3.5 | 1.0 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 1.0 |
| Reproducibility | 4.0 | 3.0 | 0.0 | 1.0 |
| Traceable references | 3.5 | 4.0 | 2.0 | 3.0 |
| Accuracy against the corpus | 3.5 | 4.0 | 3.5 | 3.0 |
| Calibration and limits | 3.5 | 4.0 | 3.0 | 2.5 |
| Decision-grade verdict | 4.0 | 4.0 | 4.0 | 4.0 |
| Facet coverage | 3.5 | 3.5 | 1.5 | 1.5 |
| **Score /100** | **71.9** | 67.2 | 37.6 | 34.9 |

**Claude Opus judge:** A and C grounded every number in the recorded calls and were honest that the retrieved evidence measures poverty but not work. A went further: it quantified the trend, flagged the broad lane, said explicitly that the work half was never queried, and set low confidence to match. B and D gave the more substantively informative memory-based answers on labour supply, including the OpenResearch work reduction, but nothing they reported can be traced or regenerated.

**GPT judge:** A is the strongest decision aid: it separates a measured one-time hardship result from the unanswered work and ongoing-UBI questions, and its verdict is bounded by those gaps. C has richer corpus tracing, but its cross-lane research/news ratio and unsupported detail about an unread model paper weaken its decision value.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/ubi-evidence/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/ubi-evidence.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Does universal basic income reduce poverty without reducing work? What does the evidence say?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.evidence" \
  -H 'content-type: application/json' \
  -d '{"claim": "Universal basic income reduces poverty", "limit": 10}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['find_evidence']["fn"](**{'claim': 'Universal basic income reduces poverty', 'limit': 10})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `find_evidence` (90.7 s) → `find_counter_evidence` (33.3 s) → `find_statistics` (16.8 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
