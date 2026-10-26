# Generative AI in education

[Technology & AI](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** The framing trend of a fast-moving literature.  
> **Why it is hard.** A 2023+ literature: almost entirely after most training cut-offs.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [gen-ai-education-stance.json](../../examples/gen-ai-education-stance.json).

**The question:**

> How is research on generative AI in education framed: promising or cautionary? How has it moved?

## What Prism returned

**2,118 papers** matched (phrases: generative ai, deep generative models, synthetic data generation, neural text generation, ai content creation).

![Framing by year](../img/gen-ai-education-stance-stance.svg)

![Papers by orientation](../img/gen-ai-education-stance-orientation.svg)

| Year | Papers | Positive | Contested |
| ---: | ---: | ---: | ---: |
| 2020 | 1 | 100% | 0% |
| 2022 | 4 | 25% | 75% |
| 2023 | 143 | 37.1% | 53.1% |
| 2024 | 577 | 39.9% | 47.5% |
| 2025 | 1,393 | 44% | 43.6% |

### Most recent promising studies (716 matched)

| Year | Paper | Venue | Contribution |
| ---: | --- | --- | --- |
| 2025 | [An Analysis of Creativity Changes in a University General Education Course Integrating Generative AI–Based Collaborative](https://doi.org/10.51636/jotd.2025.12.21.3.211) |  | methodological |
| 2025 | [From Instrumental Rationality to Value Symbiosis: Logical Rationale and Practical Mechanism of Generative AI Empowering ](https://doi.org/10.54097/tsyk3b62) | International Journal of Finance and Investment | theoretical |
| 2025 | [Exploring the Structural Relations Influencing K-12 Teachers’ Acceptance of Generative AI in Education: An Application o](https://doi.org/10.31216/bdl.2025.15.4.1) | Institute of Brain-based Education Korea National University of Education | empirical |
| 2025 | [Generative AI Literacy and Students’ Academic Performance: The Mediating Role of Student Engagement in Higher Education](https://doi.org/10.3126/pragya.v14i2.90772) | Patan Pragya | empirical |
| 2025 | [The Importance of Summarizing and Exploring Educational Directions Following the Emergence of Generative AI Chatbots](https://doi.org/10.37736/kjlr.2025.12.16.6.06) |  | empirical |
| 2025 | [Integrating Generative AI into Narrative-Based Educational Games for Moral Development: A Conceptual Approach](https://doi.org/10.26913/ava22505) | Avant | methodological |
| 2025 | [Academic Cheating with Generative AI in Higher Education: An Extended Model of the Theory of Planned Behavior with Motiv](https://doi.org/10.22146/jpsi.107932) | Jurnal Psikologi | methodological |
| 2025 | [GENERATIVE AI FOR MULTICULTURAL MUSIC EDUCATION](https://doi.org/10.29121/shodhkosh.v6.i5s.2025.6910) | ShodhKosh Journal of Visual and Performing Arts | methodological |

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/gen-ai-education-stance-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 5.0 | 3.5 | 1.0 | 0.0 |
| Measured comparison | 5.0 | 4.5 | 2.0 | 0.5 |
| Visualisation from counted data | 4.5 | 4.0 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 4.0 | 1.5 | 1.5 |
| Data export with provenance | 3.0 | 4.0 | 1.0 | 0.0 |
| Reproducibility | 5.0 | 5.0 | 0.0 | 1.0 |
| Traceable references | 3.0 | 3.0 | 3.5 | 0.0 |
| Accuracy against the corpus | 3.5 | 3.0 | 2.5 | 1.5 |
| Calibration and limits | 4.5 | 4.5 | 3.5 | 3.0 |
| Decision-grade verdict | 3.0 | 3.0 | 3.0 | 2.5 |
| Facet coverage | 5.0 | 4.0 | 1.5 | 1.5 |
| **Score /100** | **82.0** | 76.5 | 36.7 | 21.4 |

**Claude Opus judge:** D was the only deliverable to read the measured series correctly. Over the usable 2023–2025 years, the positive share rose and the contested share fell, which converges to a balanced field. D flagged the tool's 'more cautious' reading as an artefact of a one-paper baseline, and it also noted the off-topic phrase contamination. A was equally well traced but repeated that artefact in its verdict, against its own chart. B gave honest memory estimates that point the wrong way. C answered nothing and had misattributed DOIs.

**GPT judge:** A is the strongest decision aid: it traces the movement, compares orientations on defined scales, and keeps thin years and corpus limits visible. B offers a richer decomposition, but incorrectly calls the 2025 window incomplete and overreads a keyword facet; C and D cannot establish a measured trend.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/gen-ai-education-stance/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/gen-ai-education-stance.pdf)

## Live MCP session

Here each model was given only the question and a live connection to the Prism MCP server, and chose its own calls.

**Claude** (claude-sonnet, 169.2 s) called 2 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `stance_trends` | `{"term": "generative AI in education"}` | ok · 4,023 chars |
| 2 | `browse_research` | `{"term": "generative AI in education", "limit": 3}` | ok · 6,354 chars |

<details><summary>Claude's answer</summary>

**Direct answer:** The research is mostly promising, but a large cautionary share has built up alongside it, so it is mixed rather than one-sided. The balance shifted from enthusiasm toward a "promising plus problem-flagging" mix in 2024. It then partly rebalanced in 2025.

**What the data shows** (Prism typed research corpus, papers with "generative AI" in the title and an education scope, 2017–2025; the stance_trends call counts 1,339 papers and the browse call counts 2,118, because the two use different matching):
- Across the stance_trends set, promising papers are 616 of 1,339 (46%). Cautionary papers are 321 (24%), problem-identifying 185 (14%), critical 42 (3%), descriptive 142, and breakthrough 24.
- The browse facet shows a similar picture, with 33.8% promising, 23.5% problem-identifying and 19.3% cautionary. It puts "positive" at 42.4% and "contested" at 45.4%.
- Volume grew from 143 papers in 2023 to 577 in 2024 and 1,393 in 2025. Years before 2023 have fewer than 20 papers, so their shares are noise.
- The promising share was 27% in 2023 (39 of 143), 29% in 2024 (167 of 577) and 29% in 2025 (410 of 1,393).
- The contested share (cautionary, critical and problem-identifying papers) was 7% in 2023 and 42% in 2024. It fell to 21% in 2025. Problem-identifying papers peaked at 138 in 2024 and dropped to 44 in 2025.
- Descriptive papers rose to 131 in 2025 from 9 in 2024.
- The tool's own "framing shift" reading, which compares only the early and late thirds of the window, says recent work is 21 points more cautious. That comparison is built on the thin 2020 and 2022 years, so I would not rely on it.

**Interpretation (mine, not the data's):**
- Optimism was the default in 2023 and critical framing arrived in 2024, as classroom evidence and concerns about integrity, over-reliance and equity accumulated.
- In 2025 the field seems to have moved toward descriptive and empirical work, with cautionary framing continuing in absolute terms.
- Orientation labels describe how a paper frames its own finding, not whether the finding is true. 2025 may also be incomplete because of ingest lag.

</details>

**ChatGPT** (gpt-6-luna, 97.8 s) called 1 Prism tool:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `stance_trends` | `{"term": "generative AI in education", "since": 2017, "until": 2025}` | ok · 9,568 chars |

<details><summary>ChatGPT's answer</summary>

**The research is mixed, but the balance has shifted toward caution.** Promising papers remain numerous; cautionary and problem identifying work has grown alongside them.

**What the data shows —** Prism’s typed research corpus records **2,118 papers from 2017–2025** on generative AI in education. In **2025**, it classified **44.0%** as positive (promising or breakthrough) and **43.6%** as contested (cautionary, critical, or problem identifying). Counts grew sharply: **143 papers in 2023, 577 in 2024, and 1,393 in 2025**. Early years are too sparse for reliable shares: 2020 had one paper and 2022 had four. *(Source: Prism stance trends; coverage marked complete.)*

**My interpretation —** This is not a clean move from optimism to pessimism. The literature expanded rapidly, and both hopeful and skeptical framings grew; by 2025, positive and contested framings were nearly even. The data classifies how papers frame their findings, not whether their claims are correct.

</details>

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How is research on generative AI in education framed: promising or cautionary? How has it moved?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/research.stance_trends" \
  -H 'content-type: application/json' \
  -d '{"term": "generative ai in education"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['stance_trends']["fn"](**{'term': 'generative ai in education'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `stance_trends` (5.7 s) → `browse_research` (27.8 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
