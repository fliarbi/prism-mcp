# Cybercrime coverage

[Crime & public safety](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A threat-landscape media read.  
> **Why it is hard.** Ransomware, fraud and data breaches split the coverage; themes separate them.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [cybercrime-pulse.json](../../examples/cybercrime-pulse.json).

**The question:**

> How much cybercrime coverage is there, where, and what are the critical stories?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “cybercrime”, Jun 2024 – May 2026 | 76,508 |
| Critical coverage (priority 7–9) | 64,468 (84.3%) |
| Peak month | Apr 2026 (4,931 articles) |
| Last third of the window vs first third | 1.17× (flat) |
| Negative · positive | 77% · 22.1% |
| Tone vs all news (negative-to-positive ratio) | 3.48 vs 0.58 baseline: *markedly more negative than ordinary news coverage* |
| What Prism thinks “cybercrime” is | topic |

![Monthly coverage of cybercrime](../img/cybercrime-pulse-trend.svg)

![Tone of cybercrime coverage](../img/cybercrime-pulse-tone.svg)

![Countries in cybercrime coverage](../img/cybercrime-pulse-geo.svg)

![Themes in cybercrime coverage](../img/cybercrime-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “cybercrime” coverage (they also name the companies, people and places it is written about with): cybercrime (73,371), cybersecurity (37,756), fraud (10,838), ransomware (4,360), data breach (4,191), scams (3,630), cyber crime (3,558), data security (3,554), sim (3,006), scam (2,424), financial security (2,279), cambodia (1,640)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| united nations office on drugs and crime | pavel durov | united states |
| europol | naseeruddin shah | india |
| sim | ishmael | united kingdom |
| lazarus group | changpeng zhao | china |
| theprint | g. parameshwara | nigeria |
| bec | elon musk | france |

**Top publishers in a 211-article sample:** livehindustan.com (6.6%), m.dailyhunt.in (6.2%), newindianexpress.com (3.3%), thehindu.com (3.3%), gulfnews.com (2.8%), dailytrust.com (2.8%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-04-28 | [Alleged China-Linked Hacker Extradited To U.S. By Italy](https://stratnewsglobal.com/china/alleged-china-linked-hacker-extradited-to-u-s-by-italy/) | stratnewsglobal.com | 9 | very_neg |
| 2026-04-15 | [Notice of Data Breach](http://www.prnewswire.com/news-releases/notice-of-data-breach-302743794.html) | prnewswire.com | 9 | very_neg |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 2,135 | 1,780 | 1,596 | 511 |
| Jul 2024 | 3,165 | 2,739 | 2,538 | 601 |
| Aug 2024 | 2,844 | 2,414 | 2,251 | 574 |
| Sep 2024 | 3,116 | 2,619 | 2,394 | 688 |
| Oct 2024 | 3,270 | 2,772 | 2,429 | 808 |
| Nov 2024 | 2,920 | 2,443 | 2,232 | 651 |
| Dec 2024 | 3,359 | 2,788 | 2,513 | 806 |
| Jan 2025 | 3,578 | 2,875 | 2,546 | 975 |
| Feb 2025 | 3,353 | 2,825 | 2,506 | 812 |
| Mar 2025 | 3,602 | 2,971 | 2,563 | 989 |
| Apr 2025 | 2,846 | 2,378 | 2,170 | 653 |
| May 2025 | 2,903 | 2,448 | 2,311 | 550 |
| Jun 2025 | 2,263 | 1,843 | 1,748 | 491 |
| Jul 2025 | 2,942 | 2,215 | 2,420 | 494 |
| Aug 2025 | 2,786 | 2,283 | 2,182 | 574 |
| Sep 2025 | 2,774 | 2,411 | 2,151 | 597 |
| Oct 2025 | 3,220 | 2,790 | 2,369 | 819 |
| Nov 2025 | 3,138 | 2,795 | 2,464 | 639 |
| Dec 2025 | 3,011 | 2,621 | 2,316 | 665 |
| Jan 2026 | 2,675 | 2,274 | 2,058 | 585 |
| Feb 2026 | 4,381 | 3,668 | 3,457 | 888 |
| Mar 2026 | 3,591 | 3,049 | 2,835 | 729 |
| Apr 2026 | 4,931 | 4,260 | 3,775 | 1,089 |
| May 2026 | 3,705 | 3,207 | 2,974 | 699 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/cybercrime-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 1.0 | 0.0 |
| Visualisation from counted data | 3.5 | 3.0 | 1.0 | 0.0 |
| Exploration and drill-down | 2.5 | 2.5 | 1.5 | 1.5 |
| Data export with provenance | 3.0 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 4.5 | 4.5 | 1.0 | 0.5 |
| Traceable references | 0.5 | 0.5 | 1.0 | 0.0 |
| Accuracy against the corpus | 4.0 | 3.5 | 2.5 | 3.0 |
| Calibration and limits | 2.5 | 4.0 | 3.0 | 3.0 |
| Decision-grade verdict | 3.5 | 3.0 | 1.5 | 2.0 |
| Facet coverage | 4.5 | 4.0 | 1.0 | 0.0 |
| **Score /100** | **69.6** | 68.6 | 28.7 | 20.1 |

**Claude Opus judge:** C and B both measured the same window, but C went further for a decision-maker. It split the coverage into fraud, ransomware and data-breach themes, decomposed critical and tone counts by month, and flagged anomalies in the data (non-organisation entity labels, the CAGR vs flat-label conflict, the high-lift Cambodia row). It also named the actual critical story threads. A and D lacked data: A gave honest memory estimates about losses rather than coverage, and D gave a well-formed refusal.

**GPT judge:** C is the strongest decision aid: it ties its monthly series, geography, tone, and sample caveats to a replayable source and exports the key tables. B is more expansive and offers more story examples, but its unsupported Cambodia geography row and inconsistent trend reading reduce trust; neither deliverable fully resolves the critical-story facet.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/cybercrime-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/cybercrime-pulse.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How much cybercrime coverage is there, where, and what are the critical stories?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "cybercrime", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'cybercrime', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
