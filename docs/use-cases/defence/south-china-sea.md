# South China Sea tensions

[Defence & geopolitics](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A maritime flashpoint monitor.  
> **Why it is hard.** Philippine, Vietnamese and Chinese framing differ; geography splits it.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [south-china-sea.json](../../examples/south-china-sea.json).

**The question:**

> What is the coverage of the South China Sea: places, tone and the critical stories?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “south china sea”, Jun 2024 – May 2026 | 18,820 |
| Critical coverage (priority 7–9) | 16,337 (86.8%) |
| Peak month | Jun 2024 (1,366 articles) |
| Last third of the window vs first third | 0.6× (falling) |
| Negative · positive | 66% · 31.3% |
| Tone vs all news (negative-to-positive ratio) | 2.11 vs 0.58 baseline: *markedly more negative than ordinary news coverage* |
| What Prism thinks “south china sea” is | topic |

![Monthly coverage of south china sea](../img/south-china-sea-trend.svg)

![Tone of south china sea coverage](../img/south-china-sea-tone.svg)

![Countries in south china sea coverage](../img/south-china-sea-geo.svg)

![Themes in south china sea coverage](../img/south-china-sea-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “south china sea” coverage (they also name the companies, people and places it is written about with): china (15,095), philippines (10,886), beijing (9,612), manila (6,192), taiwan (5,496), vietnam (5,356), malaysia (4,289), asean (2,380), the indo-pacific (1,836), indo-pacific (1,699), marcos (1,698), peking (1,038)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| indo-pacific | lloyd austin | china |
| armed forces of the philippines | ferdinand marcos | united states |
| theprint | bongbong marcos | philippines |
| pagasa | xi jinping | taiwan |
| united states indo-pacific command | lai ching-te | vietnam |
| marcos | richard marles | japan |

**Top publishers in a 202-article sample:** thestar.com.my (5%), ibtimes.sg (4.5%), yahoo.com (4%), bairdmaritime.com (4%), philstar.com (3.5%), chinadaily.com.cn (3.5%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-03-10 | [Missing Malaysia Airlines flight MH370 - Latest news updates, theories, pictures, video and more - Mirror Online](https://www.mirror.co.uk/all-about/missing-malaysian-airlines-flight) | mirror.co.uk | 9 | very_neg |
| 2026-03-10 | [Missing Malaysia Airlines flight MH370 - Latest news updates, theories, pictures, video and more - Mirror Online](http://www.mirror.co.uk/all-about/missing%20malaysian%20airlines%20flight) | mirror.co.uk | 9 | very_neg |
| 2026-03-11 | [Former Vice Foreign Minister of Thailand: South China Sea Should Be a Sea of Peace](https://en.antaranews.com/news/407987/former-vice-foreign-minister-of-thailand-south-china-sea-should-be-a-sea-of-peace) | en.antaranews.com | 9 | very_neg |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 1,366 | 1,212 | 1,031 | 312 |
| Jul 2024 | 1,197 | 1,066 | 820 | 336 |
| Aug 2024 | 1,178 | 1,073 | 836 | 311 |
| Sep 2024 | 1,085 | 964 | 761 | 295 |
| Oct 2024 | 808 | 699 | 541 | 246 |
| Nov 2024 | 904 | 803 | 597 | 291 |
| Dec 2024 | 1,020 | 920 | 770 | 219 |
| Jan 2025 | 878 | 691 | 506 | 351 |
| Feb 2025 | 717 | 648 | 482 | 217 |
| Mar 2025 | 735 | 640 | 449 | 246 |
| Apr 2025 | 848 | 747 | 551 | 265 |
| May 2025 | 526 | 439 | 333 | 181 |
| Jun 2025 | 357 | 293 | 219 | 122 |
| Jul 2025 | 573 | 442 | 329 | 235 |
| Aug 2025 | 824 | 724 | 538 | 262 |
| Sep 2025 | 783 | 695 | 560 | 213 |
| Oct 2025 | 686 | 618 | 458 | 219 |
| Nov 2025 | 578 | 535 | 400 | 164 |
| Dec 2025 | 363 | 317 | 236 | 123 |
| Jan 2026 | 604 | 523 | 395 | 174 |
| Feb 2026 | 712 | 443 | 319 | 375 |
| Mar 2026 | 498 | 443 | 320 | 160 |
| Apr 2026 | 781 | 679 | 463 | 277 |
| May 2026 | 799 | 723 | 496 | 287 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/south-china-sea-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 4.0 | 0.5 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 0.5 | 0.5 |
| Visualisation from counted data | 4.0 | 4.0 | 0.5 | 0.0 |
| Exploration and drill-down | 2.5 | 3.0 | 1.5 | 1.0 |
| Data export with provenance | 3.0 | 4.5 | 0.5 | 0.0 |
| Reproducibility | 5.0 | 5.0 | 0.0 | 1.0 |
| Traceable references | 1.5 | 1.0 | 0.5 | 0.5 |
| Accuracy against the corpus | 3.5 | 4.5 | 4.0 | 4.0 |
| Calibration and limits | 3.0 | 3.0 | 3.0 | 3.0 |
| Decision-grade verdict | 2.5 | 4.0 | 2.5 | 2.0 |
| Facet coverage | 4.5 | 4.5 | 2.0 | 1.5 |
| **Score /100** | 69.6 | **77.9** | 29.2 | 26.3 |

**Claude Opus judge:** A and C both grounded every number in the recorded overview. A went further: it named the peak and trough, flagged the Feb-2026 positive-tone anomaly, attached URLs to the critical headlines, and caught the feed's false positives and label duplications. C is clean but thinner on the critical stories. B and D honestly declined to measure, which leaves a decision-maker with nothing usable beyond a plan of calls.

**GPT judge:** A is the strongest decision aid: it combines a traced trend, tone comparison, topical and geographic breakdowns, and explicit limits while keeping critical labels distinct from editorial importance. B is broader and includes headline URLs, but its geography denominator, enrichment bound, and tone-trend reading contain material errors; C and D provide no measured answer.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/south-china-sea/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/south-china-sea.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is the coverage of the South China Sea: places, tone and the critical stories?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "south china sea", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'south china sea', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
