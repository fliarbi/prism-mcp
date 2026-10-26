# Microplastics in the news

[Environment & disasters](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** An environmental-risk media read.  
> **Why it is hard.** Human-tissue studies (brain, placenta) drove 2024-2025 spikes.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [microplastics-pulse.json](../../examples/microplastics-pulse.json).

**The question:**

> What does the news say about microplastics, and how has coverage moved?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “microplastics”, Jun 2024 – May 2026 | 12,920 |
| Critical coverage (priority 7–9) | 11,179 (86.5%) |
| Peak month | Mar 2025 (1,547 articles) |
| Last third of the window vs first third | 1.27× (rising) |
| Negative · positive | 45.3% · 52.3% |
| Tone vs all news (negative-to-positive ratio) | 0.87 vs 0.58 baseline: *markedly more negative than ordinary news coverage* |
| What Prism thinks “microplastics” is | topic |

![Monthly coverage of microplastics](../img/microplastics-pulse-trend.svg)

![Tone of microplastics coverage](../img/microplastics-pulse-tone.svg)

![Countries in microplastics coverage](../img/microplastics-pulse-geo.svg)

![Themes in microplastics coverage](../img/microplastics-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “microplastics” coverage (they also name the companies, people and places it is written about with): sustainability (3,124), environmental impact (2,477), research (1,505), environment (1,357), pet (923), pp (690), ps (640), water quality (619), food safety (535), ecosystems (370), biodiversity (287), environmental policy (284)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| university of new mexico | maha jodi | united states |
| american chemistry council | lee zeldin | united kingdom |
| technical support | carl linnaeus | france |
| united nations environment programme | robert f. kennedy jr. | canada |
| world wide fund for nature | robert f. kennedy | china |
| material science | orlando bloom | india |

**Top publishers in a 219-article sample:** yahoo.com (10.5%), pubmed.ncbi.nlm.nih.gov (6.4%), infobae.com (2.7%), psychologytoday.com (2.3%), beveragedaily.com (1.8%), phys.org (1.8%)

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 377 | 296 | 148 | 206 |
| Jul 2024 | 317 | 272 | 145 | 163 |
| Aug 2024 | 388 | 327 | 212 | 166 |
| Sep 2024 | 452 | 386 | 207 | 232 |
| Oct 2024 | 392 | 338 | 172 | 200 |
| Nov 2024 | 458 | 404 | 203 | 242 |
| Dec 2024 | 625 | 565 | 264 | 342 |
| Jan 2025 | 515 | 457 | 231 | 266 |
| Feb 2025 | 546 | 480 | 286 | 241 |
| Mar 2025 | 1,547 | 1,384 | 606 | 925 |
| Apr 2025 | 461 | 380 | 228 | 224 |
| May 2025 | 427 | 345 | 195 | 214 |
| Jun 2025 | 435 | 348 | 206 | 209 |
| Jul 2025 | 490 | 406 | 242 | 227 |
| Aug 2025 | 481 | 391 | 252 | 219 |
| Sep 2025 | 540 | 480 | 210 | 313 |
| Oct 2025 | 509 | 446 | 222 | 273 |
| Nov 2025 | 428 | 377 | 181 | 238 |
| Dec 2025 | 472 | 408 | 192 | 263 |
| Jan 2026 | 720 | 637 | 319 | 385 |
| Feb 2026 | 576 | 524 | 249 | 317 |
| Mar 2026 | 517 | 439 | 225 | 275 |
| Apr 2026 | 853 | 741 | 397 | 441 |
| May 2026 | 394 | 348 | 237 | 152 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/microplastics-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.5 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 1.0 | 0.0 |
| Visualisation from counted data | 4.0 | 3.0 | 1.0 | 0.0 |
| Exploration and drill-down | 2.5 | 2.5 | 1.5 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.5 | 4.5 | 1.0 | 1.0 |
| Traceable references | 2.0 | 0.5 | 3.0 | 0.5 |
| Accuracy against the corpus | 3.5 | 4.0 | 3.5 | 3.5 |
| Calibration and limits | 3.5 | 3.0 | 3.5 | 3.0 |
| Decision-grade verdict | 3.5 | 4.0 | 3.0 | 2.5 |
| Facet coverage | 4.5 | 4.5 | 1.0 | 0.5 |
| **Score /100** | **73.4** | 70.6 | 38.7 | 24.4 |

**Claude Opus judge:** B and C both traced the full monthly series, the 2025-03 peak and the 1.5x negativity versus baseline. C went further with the critical-versus-total decomposition, news items with URLs, and caught anomalies such as noisy entity labels and the undefined 'critical' flag, though it mis-stated what the March outlier inflates. A was an honest memory answer with real DOIs but measured nothing, and D was an honest blank.

**GPT judge:** C and D provide the only fully traced movement series and baseline tone comparison, so they support a decision about how coverage moved rather than offering a memory-based narrative. D is the stronger decision brief because it defines the tone baseline, explains the data limits, and treats the empty critical-headline result as contrary evidence; its main weakness is calling the final month complete.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/microplastics-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/microplastics-pulse.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What does the news say about microplastics, and how has coverage moved?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "microplastics", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'microplastics', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
