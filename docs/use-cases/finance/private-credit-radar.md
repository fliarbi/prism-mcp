# Private credit research radar

[Finance & markets](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A radar for an emerging asset class.  
> **Why it is hard.** Small literature: the honest answer reports how thin it is.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [private-credit-radar.json](../../examples/private-credit-radar.json).

**The question:**

> What is new in research on private credit markets since 2022?

## What Prism returned

### Direction of travel

| Series | Window | First → last | Peak | Late third vs early third | Direction |
| --- | --- | --- | --- | ---: | --- |
| Research papers (typed corpus) | 2017 – 2025 | 10 → 28 | 28 (2025) | 2.25× | rising |
| News articles | 2019-01-01 – 2026-05-01 | 8 → 569 | 980 (2026-03-01) | 10.79× | rising |

**Framing shift since 2022:** cautionary share 41.9% before vs 40% since (-1.9 points): *framing is broadly unchanged*.

### New work since 2022

*the most-cited typed papers published since the start year whose title carries one of the subject's own phrases*

| Year | Paper | Venue | Orientation | Cited by |
| ---: | --- | --- | --- | ---: |
| 2023 | [Less Bank Regulation, More Non-Bank Lending](https://doi.org/10.17016/feds.2023.026) | Finance and Economics Discussion Series | critical | 8 |
| 2024 | [Private Credit: Characteristics and Risks](https://doi.org/10.17016/2380-7172.3462) | FEDS Notes | descriptive | 8 |
| 2022 | [Government Domestic Borrowing and Private Credit in Nigeria: Testing the Lazy Bank Hypothesis](https://doi.org/10.7176/jesd/13-7-07) |  | cautionary | 8 |
| 2024 | [Private Credit Growth and Monetary Policy Transmission](https://doi.org/10.17016/2380-7172.3565) | FEDS Notes | descriptive | 5 |
| 2025 | [Promoting Sustainable Banking: The Role of Private Credit in Reducing CO2 Emissions in Indonesia](https://doi.org/10.32479/ijeep.18036) | International Journal of Energy Economics and Policy | critical | 5 |
| 2023 | [The Impact of Macroprudential and Monetary Policies Instruments on the Private Credit Growth in the Arab Banking Sector](https://doi.org/10.32479/ijefi.14783) | International Journal of Economics and Financial Issues | cautionary | 4 |
| 2024 | [Probability causal inference of interest rate fluctuations: Evidence from private credit in emerging markets](https://doi.org/10.1016/j.techfore.2023.123163) | Technological Forecasting and Social Change | descriptive | 3 |
| 2022 | [Credible risk: private credit bureaus and the work of loan officers in West Africa](https://doi.org/10.1017/s0001972022000353) | Africa | promising | 3 |
| 2024 | [Private credit: a renaissance in corporate finance](https://doi.org/10.1080/14735970.2024.2351230) | Journal of Corporate Law Studies | comparative | 3 |
| 2022 | [Does growth of nonperforming loan ratio have a temporal impact on private credit growth in Bangladesh economy?](https://doi.org/10.1108/ajeb-03-2022-0030) | Asian Journal of Economics and Banking | promising | 3 |

![Most-cited new work](../img/private-credit-radar-new-work.svg)

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/private-credit-radar-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 3.5 | 1.0 | 1.0 |
| Measured comparison | 2.5 | 3.5 | 1.0 | 1.0 |
| Visualisation from counted data | 2.5 | 3.5 | 1.0 | 1.0 |
| Exploration and drill-down | 3.0 | 2.0 | 1.0 | 1.0 |
| Data export with provenance | 4.0 | 2.5 | 1.0 | 1.0 |
| Reproducibility | 4.0 | 4.5 | 1.0 | 0.0 |
| Traceable references | 3.5 | 3.0 | 1.0 | 1.0 |
| Accuracy against the corpus | 4.0 | 4.5 | 2.5 | 1.5 |
| Calibration and limits | 4.0 | 3.0 | 3.5 | 3.5 |
| Decision-grade verdict | 3.0 | 4.0 | 3.0 | 3.5 |
| Facet coverage | 5.0 | 4.0 | 1.0 | 1.5 |
| **Score /100** | **71.5** | 71.3 | 32.4 | 29.4 |

**Claude Opus judge:** B and D both grounded their answers in the radar call. Only B noticed that half of the 'private credit' papers concern bank credit to the private sector rather than private credit markets, which shows how thin the real literature is. B also quantified the gap between research and news. D was faithful to the data but had a shallower trend and only one chart. A and C answered from memory: C was honestly labelled but answered with AUM rather than research measures, and A cited unresolvable identifiers.

**GPT judge:** A is the strongest decision aid: it treats the literature as a selected, thin map, quantifies the framing shift, and clearly bounds what the data can establish. B adds useful comparisons and exports, but mislabels an unspecified trend unit and overstates a cross-window research/news comparison; C and D are candid about memory limits but provide little grounded measurement.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/private-credit-radar/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/private-credit-radar.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is new in research on private credit markets since 2022?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.radar" \
  -H 'content-type: application/json' \
  -d '{"topic": "private credit", "since_year": 2022}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['research_radar']["fn"](**{'topic': 'private credit', 'since_year': 2022})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
