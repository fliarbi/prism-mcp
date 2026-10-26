# AI agents in the news

[Technology & AI](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Hype-cycle read on an emerging category.  
> **Why it is hard.** A 2024-2025 term: model knowledge is thin, the corpus is not.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [ai-agents-pulse.json](../../examples/ai-agents-pulse.json).

**The question:**

> How much news coverage is there of AI agents, and how fast is it growing?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “ai agents”, Jun 2024 – May 2026 | 45,512 |
| Critical coverage (priority 7–9) | 32,257 (70.9%) |
| Peak month | Apr 2026 (4,883 articles) |
| Last third of the window vs first third | 4.46× (rising) |
| Negative · positive | 6.2% · 93.7% |
| Tone vs all news (negative-to-positive ratio) | 0.07 vs 0.58 baseline: *markedly more positive than ordinary news coverage* |
| What Prism thinks “ai agents” is | topic |

![Monthly coverage of ai agents](../img/ai-agents-pulse-trend.svg)

![Tone of ai agents coverage](../img/ai-agents-pulse-tone.svg)

![Countries in ai agents coverage](../img/ai-agents-pulse-geo.svg)

![Themes in ai agents coverage](../img/ai-agents-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “ai agents” coverage (they also name the companies, people and places it is written about with): ai (44,359), ai agents (19,969), agentic ai (6,345), automation (6,334), api (5,577), mcp (4,110), software development (3,988), llm (3,289), salesforce (2,846), crm (2,579), servicenow (1,833), generative ai (1,481)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| salesforce | marc benioff | united states |
| mcp | george clooney | united kingdom |
| gartner | jensen huang | india |
| api | satya nadella | netherlands |
| servicenow | sam roberts (singer-songwriter) | colombia |
| databricks | marc andreessen | china |

**Top publishers in a 230-article sample:** servicenow.com (2.2%), token.security (1.7%), it-boltwise.de (1.7%), aithority.com (1.7%), itbrief.com.au (1.7%), techzine.eu (1.3%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-05-27 | [ClickUp cuts 22% of staff, replaces them with 3,000 AI agents - Outsource Accelerator](https://news.outsourceaccelerator.com/clickup-cuts-staff-replaces-ai/) | news.outsourceaccelerator.com | 8 | very_pos |
| 2026-05-26 | [Apple's AI strategy challenge might be solved by the iPhone's 'agentic AI moat'](https://sg.finance.yahoo.com/news/apples-ai-strategy-challenge-might-be-solved-by-the-iphones-agentic-ai-moat-160442351.html) | sg.finance.yahoo.com | 8 | slight_pos |
| 2026-05-15 | [Venture Capital Funding: Samaya AI, Autonomize AI, Scamnetic - InfotechLead](https://infotechlead.com/tech/venture-capital-funding-samaya-ai-autonomize-ai-scamnetic-95847) | infotechlead.com | 8 | very_pos |
| 2026-05-12 | [OpenAI & PwC currently stuck in a "Marriage Of Necessity?'](https://thefinancestory.com/openai-partners-with-pwc-to-build-ai-agents-for-cfos) | thefinancestory.com | 8 | slight_pos |
| 2026-05-08 | [Cloudflare Lays Off 1,100 Employees Amid Major AI Restructuring](https://www.analyticsinsight.net/news/cloudflare-lays-off-1100-employees-amid-major-ai-restructuring) | analyticsinsight.net | 8 | slight_pos |
| 2026-05-06 | [AWS and OpenAI expand partnership with new AI tools](https://www.traveldailymedia.com/aws-and-openai-expand-partnership-with-new-ai-tools/) | traveldailymedia.com | 8 | very_pos |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 199 | 157 | 4 | 195 |
| Jul 2024 | 271 | 221 | 7 | 263 |
| Aug 2024 | 233 | 165 | 5 | 228 |
| Sep 2024 | 470 | 334 | 13 | 456 |
| Oct 2024 | 1,043 | 465 | 19 | 1,022 |
| Nov 2024 | 730 | 539 | 8 | 721 |
| Dec 2024 | 931 | 665 | 28 | 902 |
| Jan 2025 | 1,825 | 1,257 | 55 | 1,769 |
| Feb 2025 | 1,483 | 1,089 | 55 | 1,428 |
| Mar 2025 | 1,856 | 1,344 | 62 | 1,790 |
| Apr 2025 | 1,699 | 1,203 | 63 | 1,628 |
| May 2025 | 1,901 | 1,317 | 65 | 1,835 |
| Jun 2025 | 1,717 | 1,197 | 100 | 1,614 |
| Jul 2025 | 1,777 | 1,208 | 68 | 1,704 |
| Aug 2025 | 1,651 | 1,116 | 81 | 1,567 |
| Sep 2025 | 2,286 | 1,603 | 111 | 2,168 |
| Oct 2025 | 2,238 | 1,622 | 102 | 2,132 |
| Nov 2025 | 2,177 | 1,426 | 135 | 2,038 |
| Dec 2025 | 2,028 | 1,490 | 147 | 1,875 |
| Jan 2026 | 1,963 | 1,397 | 187 | 1,773 |
| Feb 2026 | 3,640 | 2,608 | 311 | 3,320 |
| Mar 2026 | 4,632 | 3,427 | 363 | 4,255 |
| Apr 2026 | 4,883 | 3,509 | 456 | 4,420 |
| May 2026 | 3,879 | 2,898 | 359 | 3,513 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/ai-agents-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 5.0 | 4.5 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 0.0 | 0.0 |
| Visualisation from counted data | 4.5 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 1.0 | 1.5 | 1.5 |
| Data export with provenance | 3.0 | 4.5 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 5.0 | 1.0 | 1.0 |
| Traceable references | 1.0 | 0.5 | 0.5 | 0.5 |
| Accuracy against the corpus | 4.0 | 4.0 | 3.5 | 4.0 |
| Calibration and limits | 4.5 | 4.0 | 3.5 | 2.5 |
| Decision-grade verdict | 3.0 | 4.0 | 3.5 | 2.5 |
| Facet coverage | 5.0 | 4.5 | 1.0 | 0.5 |
| **Score /100** | **79.3** | 74.7 | 34.5 | 25.5 |

**Claude Opus judge:** A and B both report the measured 45,512 articles and the 4.46× late-vs-early growth. A goes further: it decomposes tone and the critical flag, explains why 'critical' is not negativity, and gives URL-level headlines. Its limits are placed next to the numbers they bound. C and D answered from memory or declined, so they give a decision-maker nothing measurable about volume or growth.

**GPT judge:** B gives the strongest decision-grade answer: a reproducible monthly series, quantified growth, tone comparison, and useful breakdowns with explicit data limits. C is close and has cleaner export provenance, but offers less actionable drill-down; B’s small date and confidence overstatements keep it from a fully clean verdict.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/ai-agents-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/ai-agents-pulse.pdf)

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How much news coverage is there of AI agents, and how fast is it growing?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "ai agents", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'ai agents', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
