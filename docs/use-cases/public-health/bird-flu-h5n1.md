# H5N1 bird flu coverage

[Public health & epidemiology](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** An early-warning read of a zoonotic threat.  
> **Why it is hard.** Coverage spikes are driven by single events; the critical-share trend matters more than raw volume.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [bird-flu-h5n1.json](../../examples/bird-flu-h5n1.json).

**The question:**

> What does the news say about H5N1 bird flu in dairy cattle and humans? Is coverage rising?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “bird flu”, Jun 2024 – May 2026 | 13,044 |
| Critical coverage (priority 7–9) | 10,753 (82.4%) |
| Peak month | Feb 2025 (2,127 articles) |
| Last third of the window vs first third | 0.32× (falling) |
| Negative · positive | 88.5% · 10.9% |
| Tone vs all news (negative-to-positive ratio) | 8.09 vs 0.58 baseline: *markedly more negative than ordinary news coverage* |
| What Prism thinks “bird flu” is | topic |

![Monthly coverage of bird flu](../img/bird-flu-h5n1-trend.svg)

![Tone of bird flu coverage](../img/bird-flu-h5n1-tone.svg)

![Countries in bird flu coverage](../img/bird-flu-h5n1-geo.svg)

![Themes in bird flu coverage](../img/bird-flu-h5n1-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “bird flu” coverage (they also name the companies, people and places it is written about with): cdc (3,495), usda (2,349), public health (2,084), the centers for disease control and prevention (1,970), bird (1,762), infection (1,725), pandemic (997), vaccine (929), the u.s. centers for disease control and prevention (839), vaccines (660), infectious disease (557), easter (540)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| cult of the dead cow | brooke rollins | united states |
| united states department of agriculture | aceyalone | canada |
| centers for disease control and prevention | the who | united kingdom |
| animal health | robert f. kennedy jr. | india |
| foundation for ancient research and mormon studies | sanjay gupta | china |
| moderna | kevin hassett | australia |

**Top publishers in a 216-article sample:** yahoo.com (16.7%), livehindustan.com (6%), indianexpress.com (2.8%), time.news (2.8%), timesofindia.indiatimes.com (2.3%), myrepublica.nagariknetwork.com (1.9%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-02-25 | [Pa. Governor Josh Shapiro discusses bird flu outbreak](https://www.yahoo.com/news/articles/pa-governor-josh-shapiro-discusses-000011565.html) | yahoo.com | 9 | very_neg |
| 2026-03-12 | [Scientists concerned about transmission of bird flu to cows](https://www.pbssocal.org/shows/newshour/clip/bird-flu-1715810471) | pbssocal.org | 9 | very_neg |
| 2026-03-11 | [Officials continue to warn about bird flu outbreak in Pennsylvania](https://www.yahoo.com/news/articles/officials-continue-warn-bird-flu-234809145.html) | yahoo.com | 9 | very_neg |
| 2026-05-20 | [Dead polar bear tests positive for bird flu in first case of its kind in Europe](https://www.dailystar.co.uk/news/latest-news/dead-polar-bear-tests-positive-37183267) | dailystar.co.uk | 8 | fair_neg |
| 2026-05-19 | [Norway reports Europe’s first case of bird flu in a polar bear](https://www.straitstimes.com/world/europe/norway-reports-europes-first-case-of-bird-flu-in-a-polar-bear) | straitstimes.com | 8 | slight_neg |
| 2026-05-19 | [Norway reports Europe’s first case of bird flu in a polar bear](https://www.scmp.com/news/world/europe/article/3354146/norway-reports-europes-first-case-bird-flu-polar-bear) | scmp.com | 8 | slight_neg |
| 2026-05-13 | [Bird flu outbreak that killed dozens of Bay Area elephant seals declared over](https://www.yahoo.com/news/articles/bird-flu-outbreak-killed-dozens-202741302.html) | yahoo.com | 8 | very_neg |
| 2026-05-13 | [Birds in 2 more poultry farms test positive for Avian Flu \| India News - The Times of India](https://timesofindia.indiatimes.com/india/birds-in-2-more-poultry-farms-test-positive-for-avian-flu/articleshow/131073693.cms) | timesofindia.indiatimes.com | 8 | slight_neg |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 748 | 642 | 650 | 97 |
| Jul 2024 | 598 | 515 | 471 | 123 |
| Aug 2024 | 229 | 195 | 189 | 39 |
| Sep 2024 | 282 | 232 | 244 | 35 |
| Oct 2024 | 431 | 404 | 401 | 29 |
| Nov 2024 | 614 | 518 | 586 | 28 |
| Dec 2024 | 1,387 | 1,228 | 1,299 | 85 |
| Jan 2025 | 1,560 | 1,333 | 1,443 | 112 |
| Feb 2025 | 2,127 | 1,707 | 1,920 | 188 |
| Mar 2025 | 1,070 | 823 | 906 | 161 |
| Apr 2025 | 559 | 426 | 480 | 77 |
| May 2025 | 554 | 442 | 441 | 96 |
| Jun 2025 | 178 | 143 | 148 | 30 |
| Jul 2025 | 341 | 230 | 310 | 29 |
| Aug 2025 | 305 | 236 | 256 | 43 |
| Sep 2025 | 166 | 141 | 145 | 20 |
| Oct 2025 | 263 | 179 | 239 | 19 |
| Nov 2025 | 459 | 386 | 420 | 37 |
| Dec 2025 | 206 | 166 | 176 | 29 |
| Jan 2026 | 166 | 144 | 144 | 22 |
| Feb 2026 | 316 | 262 | 280 | 33 |
| Mar 2026 | 225 | 184 | 182 | 42 |
| Apr 2026 | 173 | 140 | 136 | 37 |
| May 2026 | 87 | 77 | 72 | 15 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/bird-flu-h5n1-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 3.5 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.0 | 1.0 | 0.0 |
| Visualisation from counted data | 3.0 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 2.0 | 1.0 | 1.0 |
| Data export with provenance | 2.5 | 3.5 | 1.0 | 0.0 |
| Reproducibility | 4.5 | 4.0 | 1.0 | 0.5 |
| Traceable references | 1.0 | 0.5 | 0.5 | 0.5 |
| Accuracy against the corpus | 4.0 | 2.5 | 3.5 | 3.5 |
| Calibration and limits | 4.0 | 3.5 | 3.5 | 2.5 |
| Decision-grade verdict | 4.0 | 4.0 | 3.0 | 2.0 |
| Facet coverage | 4.0 | 3.0 | 1.0 | 0.5 |
| **Score /100** | **73.7** | 63.2 | 34.0 | 21.2 |

**Claude Opus judge:** A and B both read the measured series correctly: bird-flu coverage peaked in Feb 2025 and is falling. A went further. It quantified the critical-share trend, gave dated headlines with urls, caught entity mislabels, and honestly flagged that dairy and human coverage was not isolated. B was cleaner on the full series but thinner on drill-down and slightly misread censoring. C refused, and D offered labelled memory about the outbreak rather than coverage.

**GPT judge:** B is the strongest decision aid: it quantifies the broad bird-flu attention decline, decomposes total and critical volume, and supplies useful breakdowns and reproducible calls. Its main flaw is a material inconsistency about the censored May endpoint; C is more cautious but also mislabels that endpoint and omits the critical-share decomposition, while neither can establish cattle- or human-specific coverage from the broad query.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/bird-flu-h5n1/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/bird-flu-h5n1.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What does the news say about H5N1 bird flu in dairy cattle and humans? Is coverage rising?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "bird flu", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'bird flu', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
