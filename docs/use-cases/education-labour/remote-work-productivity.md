# Does remote work hurt productivity?

[Education & labour](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Evidence for a workplace policy decision.  
> **Why it is hard.** Pandemic-era studies and RCTs disagree; both appear.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [remote-work-productivity.json](../../examples/remote-work-productivity.json).

**The question:**

> Does remote work reduce productivity? What does the evidence say?

## What Prism returned

### How much evidence exists

| Corpus | Records on both sides of the claim | Window |
| --- | ---: | --- |
| Typed research papers | 2,288 | 2017-2025 |
| Papers with abstracts | 325 | 1990-2025 |
| the health literature index records | 0 | 1990-2025 |
| News articles | 92 | 2019-01-01..2026-06-01 |
| Patents | 0 | 2005-2024 |
| arXiv preprints | 0 | 2005-2025 |

![Evidence volume by corpus](../img/remote-work-productivity-volumes.svg)

![Framing of the literature](../img/remote-work-productivity-sides.svg)

*orientation is a label on the paper's own framing, not a verdict on the claim; this corpus starts in 2017* Contested share: **18.1%**.

### The strongest evidence, read

Prism read 5 sources: **0 support, 5 contradict, 0 qualify** (tier-weighted {"supports": 0, "contradicts": 15, "qualifies": 0}). Each quote is copied from the abstract and verified against it; 0 candidate quotes failed that check and were dropped.

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2022 | [Exploring the remote work challenges in the era of COVID-19 pandemic: review and application model](https://doi.org/10.1108/bij-07-2021-0421)<br><sub>Benchmarking An International Journal</sub> | article | contradicts | Practitioners could use this framework to focus on the factors that can create a conducive environment to improve work efficiency in a remote workforce. |
| 2023 | [The impact of remote working on employee productivity during COVID-19 in the UAE: the moderating role of job level](https://doi.org/10.1108/jbsed-09-2022-0104)<br><sub>Journal of Business and Socio-economic Development</sub> | article | contradicts | The results indicate that direct variables such as workload, job satisfaction, work–life balance and social support have a significant positive impact on employee PR in the UAE. |
| 2025 | [The Impact of Remote Working on Productivity and Work-Life Balance of Millennial Employees in DKI Jakarta](https://doi.org/10.52300/jmso.v6i3.22787)<br><sub>Jurnal Manajemen Sains dan Organisasi</sub> | article | contradicts | The results of the study show that remote working has a significant and positive effect on employee productivity |
| 2025 | [The Impact of Remote Work on Employee Productivity and Well-being: A Comparative Study of Tech and Non- Tech Industries ](https://doi.org/10.59256/ijrtmr.20250506015)<br><sub>International Journal Of Recent Trends In Multidisciplinary Research</sub> | article | contradicts | while it enhances productivity in technology sectors through increased autonomy and flexibility |
| 2025 | [Transformasi Paradigma Kerja di Era Digital: Tinjauan Literatur Sistematis terhadap Efektivitas, Produktivitas, dan Kese](https://doi.org/10.55606/detector.v3i4.5368)<br><sub>Detector Jurnal Inovasi Riset Ilmu Kesehatan</sub> | article | contradicts | the study finds that productivity experienced a net increase of 13% to 22% |
| 2021 | [WORKPLACE ISOLATION IN THE GROWTH TREND OF REMOTE WORKING: A LITERATURE REVIEW](https://doi.org/10.47743/rebs-2021-1-0005)<br><sub>Review of Economic and Business Studies</sub> | review | unrelated | With the rising popularity of remote working, employees has been received many sbenefits, for example, benefits of travel expenses or job performance. |
| 2025 | [Navigating Leadership in Hybrid or Remote Workplaces: A Systematic Review of Employee Engagement Strategies](https://doi.org/10.1177/15344843251381386)<br><sub>Human Resource Development Review</sub> | review | unrelated | Our findings highlight that established leadership constructs, such as transformational and LMX, remain effective. |
| 2021 | [Working from home effectiveness during Covid-19: Evidence from university staff in Indonesia](https://doi.org/10.1016/j.apmrv.2021.05.002)<br><sub>Asia Pacific Management Review</sub> | article | unrelated | Only an individual's digital orientation was found to have significant impact on the individual's digital capability which in turn affected their d productivity during implementing work from home in this covid-19 pandemic. |

![Study designs](../img/remote-work-productivity-tiers.svg)

### What disagrees

| Year | Study | Tier | Reads as | Verbatim finding |
| ---: | --- | --- | --- | --- |
| 2022 | [Investigating the Impact of Remote Working on Employee Productivity and Work-life Balance: A Study on the Business Consu](https://doi.org/10.20469/ijbas.8.10002-2)<br><sub>International Journal of Business and Administrative Studies</sub> | article | contradicts | Analysis of the responses demonstrated that remote working has a strong positive relation to employees' productivity. |

> No document read directly supports the claim as written. 1 contradict it and 0 require qualifications; revise or withhold the claim.

![Research output per year](../img/remote-work-productivity-research-series.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/remote-work-productivity-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 4.0 | 1.0 | 1.0 |
| Measured comparison | 4.0 | 4.0 | 2.0 | 1.0 |
| Visualisation from counted data | 4.0 | 4.0 | 1.0 | 1.0 |
| Exploration and drill-down | 3.0 | 1.0 | 1.5 | 1.0 |
| Data export with provenance | 3.5 | 3.0 | 1.0 | 1.0 |
| Reproducibility | 4.5 | 4.5 | 1.0 | 1.0 |
| Traceable references | 4.0 | 4.5 | 1.5 | 1.0 |
| Accuracy against the corpus | 3.0 | 3.5 | 1.5 | 2.0 |
| Calibration and limits | 3.5 | 4.5 | 3.0 | 3.0 |
| Decision-grade verdict | 3.0 | 3.5 | 2.5 | 3.5 |
| Facet coverage | 4.0 | 3.5 | 1.5 | 1.5 |
| **Score /100** | 73.4 | **74.0** | 31.5 | 32.2 |

**Claude Opus judge:** A was the only deliverable that read its own data honestly. It surfaced that zero read papers supported the claim and flagged the rejected 13-22% statistic and the framing-label trap. It also gave a low-confidence verdict noting that RCTs were absent from the pull. C used the same data but misstated it as 'both sides' and had no working follow-ups. B and D carried the substantive RCT-vs-pandemic content from memory, but with misattributed venues and effect sizes.

**GPT judge:** A is the strongest decision-grade deliverable: it gives a cautious, actionable answer while tracing its corpus figures, chart, references and limitations. B is more comprehensive, but it turns unsupported study-design claims and a rejected effect-size quote into evidence; C and D offer useful context but rely on memory estimates rather than reproducible measurements.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/remote-work-productivity/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/remote-work-productivity.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
Does remote work reduce productivity? What does the evidence say?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.evidence" \
  -H 'content-type: application/json' \
  -d '{"claim": "Remote work reduces productivity", "limit": 10}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['find_evidence']["fn"](**{'claim': 'Remote work reduces productivity', 'limit': 10})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `find_evidence` (113.2 s) → `find_counter_evidence` (8.3 s) → `find_statistics` (30.3 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
