# Container freight rates

[Supply chain & trade](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Freight-market narrative for a shipper.  
> **Why it is hard.** Rates spiked in 2024 on Red Sea diversions.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [container-freight-pulse.json](../../examples/container-freight-pulse.json).

**The question:**

> What has the news said about container freight rates?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “freight rates”, Jun 2024 – May 2026 | 4,385 |
| Critical coverage (priority 7–9) | 2,996 (68.3%) |
| Peak month | Mar 2026 (614 articles) |
| Last third of the window vs first third | 2.09× (rising) |
| Negative · positive | 60.2% · 37.7% |
| Tone vs all news (negative-to-positive ratio) | 1.6 vs 0.58 baseline: *markedly more negative than ordinary news coverage* |
| What Prism thinks “freight rates” is | topic |

![Monthly coverage of freight rates](../img/container-freight-pulse-trend.svg)

![Tone of freight rates coverage](../img/container-freight-pulse-tone.svg)

![Countries in freight rates coverage](../img/container-freight-pulse-geo.svg)

![Themes in freight rates coverage](../img/container-freight-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “freight rates” coverage (they also name the companies, people and places it is written about with): supply chain (1,033), transportation (845), trade (608), red sea (558), the red sea (530), logistics (480), freight (462), shipping (421), global trade (378), shanghai (313), west coast (198), fuel costs (163)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| hapag-lloyd | gboyega oyetola | united states |
| maersk | lenny cooper | china |
| world trade organization | roger bootle | india |
| bimco | dave mccormick | iran |
| cma cgm | sivakumar | united kingdom |
| tac | jpmorgan chase | russia |

**Top publishers in a 200-article sample:** indiaseatradenews.com (10%), freshplaza.com (7%), magzter.com (5.5%), theloadstar.com (4%), it-boltwise.de (3%), maritimemag.com (2.5%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-05-04 | [India Resumes Wheat Exports After Four Years But High Prices Likely To Limit Demand \| ESM Magazine](https://www.esmmagazine.com/supply-chain/india-resumes-wheat-exports-after-four-years-but-high-prices-likely-to-limit-demand-311176) | esmmagazine.com | 8 | slight_pos |
| 2026-02-05 | [Maersk layoffs: Shipping giant to cut 1,000 jobs after revenue sinks — here's what we know \| Company Business News](https://www.livemint.com/companies/news/maersk-layoffs-shipping-giant-to-cut-1-000-jobs-after-revenue-sinks-heres-what-we-know/amp-11770282105107.html) | livemint.com | 8 | very_neg |
| 2026-05-13 | [Hapag-Lloyd reporta pérdidas en primer trimestre de 2026 por condiciones climáticas y bloqueo en Ormuz - PortalPortuario](https://portalportuario.cl/hapag-lloyd-reporta-perdidas-en-primer-trimestre-de-2026-por-condiciones-climaticas-y-bloqueo-en-ormuz/) | portalportuario.cl | 8 | very_neg |
| 2026-02-06 | [Maersk to cut 1,000 jobs as profits fall](https://www.hrkatha.com/news/layoff/maersk-to-cut-1000-jobs-as-profits-fall/) | hrkatha.com | 8 | very_neg |
| 2026-05-04 | [Low water on the Rhine River means lighter loads and higher costs](https://www.bairdmaritime.com/shipping/inland-shipping/low-water-on-the-rhine-river-means-lighter-loads-and-higher-costs) | bairdmaritime.com | 8 | slight_neg |
| 2026-04-14 | [India Faces Pressure to Act on Ocean Carrier Profiteering - India Seatrade News](https://indiaseatradenews.com/india-faces-pressure-to-act-on-ocean-carrier-profiteering/) | indiaseatradenews.com | 8 | slight_neg |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 124 | 91 | 81 | 38 |
| Jul 2024 | 183 | 127 | 103 | 79 |
| Aug 2024 | 166 | 116 | 94 | 71 |
| Sep 2024 | 139 | 67 | 62 | 68 |
| Oct 2024 | 139 | 99 | 83 | 54 |
| Nov 2024 | 116 | 81 | 54 | 58 |
| Dec 2024 | 79 | 61 | 55 | 23 |
| Jan 2025 | 134 | 89 | 93 | 40 |
| Feb 2025 | 249 | 183 | 133 | 115 |
| Mar 2025 | 198 | 159 | 156 | 42 |
| Apr 2025 | 139 | 86 | 75 | 63 |
| May 2025 | 99 | 65 | 47 | 51 |
| Jun 2025 | 108 | 69 | 75 | 28 |
| Jul 2025 | 75 | 36 | 47 | 24 |
| Aug 2025 | 93 | 60 | 40 | 52 |
| Sep 2025 | 88 | 60 | 50 | 37 |
| Oct 2025 | 139 | 93 | 95 | 42 |
| Nov 2025 | 169 | 125 | 104 | 61 |
| Dec 2025 | 117 | 69 | 46 | 57 |
| Jan 2026 | 157 | 88 | 68 | 84 |
| Feb 2026 | 259 | 181 | 154 | 104 |
| Mar 2026 | 614 | 472 | 402 | 200 |
| Apr 2026 | 393 | 250 | 280 | 110 |
| May 2026 | 408 | 269 | 242 | 151 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/container-freight-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 2.0 | 0.0 |
| Visualisation from counted data | 2.5 | 4.0 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 4.5 | 2.0 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 5.0 | 1.0 | 1.0 |
| Traceable references | 1.0 | 2.0 | 0.5 | 0.5 |
| Accuracy against the corpus | 3.0 | 4.0 | 3.0 | 4.0 |
| Calibration and limits | 4.0 | 4.5 | 3.0 | 3.0 |
| Decision-grade verdict | 2.5 | 4.0 | 2.5 | 2.5 |
| Facet coverage | 4.0 | 3.5 | 1.0 | 0.5 |
| **Score /100** | 68.7 | **79.2** | 33.6 | 25.6 |

**Claude Opus judge:** A and B both grounded their answers in the measured news corpus and were honest that 'freight rates' is broader than container rates. A went further, decomposing critical share, naming the tone extremes and exposing headline URLs inline. B's verdict was cleaner and better bounded, but its decomposition was thinner. C and D could not measure what the news said; D's labelled memory index path offers orientation but no news evidence.

**GPT judge:** A best supports a cautious decision: it traces the news-volume and tone findings, distinguishes them from container prices, and states what evidence is missing before acting. D has broader breakdowns, but its container framing and unsupported Drewry snapshot weaken the decision; B and C either offer no measured corpus answer or substitute recalled rate-index estimates.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/container-freight-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/container-freight-pulse.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What has the news said about container freight rates?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "freight rates", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'freight rates', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
