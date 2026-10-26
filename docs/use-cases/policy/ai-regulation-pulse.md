# AI regulation coverage

[Policy & regulation](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A policy-landscape read for a public-affairs team.  
> **Why it is hard.** EU AI Act, US executive orders and India's approach are covered very differently by country.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [ai-regulation-pulse.json](../../examples/ai-regulation-pulse.json).

**The question:**

> How is AI regulation being covered globally? Which countries, which themes, which critical stories?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “ai regulation”, Jun 2024 – May 2026 | 4,069 |
| Critical coverage (priority 7–9) | 3,638 (89.4%) |
| Peak month | May 2026 (256 articles) |
| Last third of the window vs first third | 1.46× (rising) |
| Negative · positive | 57.1% · 41% |
| Tone vs all news (negative-to-positive ratio) | 1.39 vs 0.58 baseline: *markedly more negative than ordinary news coverage* |
| What Prism thinks “ai regulation” is | topic |

![Monthly coverage of ai regulation](../img/ai-regulation-pulse-trend.svg)

![Tone of ai regulation coverage](../img/ai-regulation-pulse-tone.svg)

![Countries in ai regulation coverage](../img/ai-regulation-pulse-geo.svg)

![Themes in ai regulation coverage](../img/ai-regulation-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “ai regulation” coverage (they also name the companies, people and places it is written about with): white house (1,521), georgia (1,426), missouri (1,419), all newsletters (1,409), all newsletters ap quizzes test your news (1,409), i.q. (1,409), ufc (1,407), español china asia pacific latin america (1,396), newsletter (1,187), knicks (1,186), motorsport (1,166), yemen (411)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| andreessen horowitz | scott wiener | united states |
| national institute of standards and technology | marc andreessen | united kingdom |
| openai | marsha blackburn | china |
| european parliament | henna virkkunen | colombia |
| meta | michael kratsios | india |
| ofcom | gavin newsom | france |

**Top publishers in a 212-article sample:** cuatrecasas.com (4.7%), linkedin.com (4.7%), faz.net (4.2%), onetrust.com (4.2%), staffingindustry.com (3.8%), b4bschwaben.de (2.8%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-02-19 | [India AI Impact Summit 2026: OpenAI CEO Sam Altman calls for urgent AI regulations as superintelligence nears](https://www.digit.in/news/general/india-ai-impact-summit-2026-openai-ceo-sam-altman-calls-for-global-ai-watchdog-as-superintelligence-nears.html) | digit.in | 8 | slight_pos |
| 2026-04-02 | [AI Industry Mobilizes Funds for 2026 Midterms Amid Regulatory Scrutiny](https://www.theedadvocate.org/ai-industry-mobilizes-funds-for-2026-midterms-amid-regulatory-scrutiny/) | theedadvocate.org | 8 | fair_pos |
| 2026-02-19 | [UK AI Minister Calls for Stronger India Partnership on Technology](https://www.newkerala.com/news/a/we-lot-do-together-uk-ai-minister-kanishka-561.htm) | newkerala.com | 8 | very_pos |
| 2026-02-20 | [Evolution towards an AI‑Native Tax System: UAE’s 2026 AI Governance and Its Impact on Corporate Tax](https://www.linkedin.com/pulse/evolution-towards-ainative-tax-system-uaes-2026-ai-elisa-mar%C3%ADa-2sinf) | linkedin.com | 8 | slight_pos |
| 2026-02-20 | [India’s AI future can’t be built on copy paste regulation, says Google’s Sachin Kakkar - BusinessToday](https://www.businesstoday.in/technology/news/story/indias-ai-future-cant-be-built-on-copy-paste-regulation-says-googles-sachin-kakkar-517210-2026-02-20) | businesstoday.in | 8 | slight_pos |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 113 | 105 | 35 | 77 |
| Jul 2024 | 102 | 89 | 37 | 57 |
| Aug 2024 | 133 | 120 | 41 | 85 |
| Sep 2024 | 131 | 117 | 53 | 74 |
| Oct 2024 | 113 | 103 | 51 | 60 |
| Nov 2024 | 195 | 186 | 111 | 83 |
| Dec 2024 | 161 | 154 | 102 | 54 |
| Jan 2025 | 218 | 203 | 131 | 86 |
| Feb 2025 | 209 | 186 | 119 | 81 |
| Mar 2025 | 78 | 64 | 30 | 48 |
| Apr 2025 | 56 | 48 | 16 | 40 |
| May 2025 | 129 | 112 | 79 | 47 |
| Jun 2025 | 196 | 178 | 120 | 73 |
| Jul 2025 | 229 | 196 | 144 | 81 |
| Aug 2025 | 129 | 120 | 72 | 52 |
| Sep 2025 | 169 | 155 | 118 | 45 |
| Oct 2025 | 200 | 174 | 110 | 87 |
| Nov 2025 | 212 | 186 | 148 | 63 |
| Dec 2025 | 248 | 226 | 146 | 102 |
| Jan 2026 | 155 | 148 | 104 | 50 |
| Feb 2026 | 212 | 181 | 121 | 88 |
| Mar 2026 | 211 | 183 | 128 | 79 |
| Apr 2026 | 214 | 187 | 135 | 76 |
| May 2026 | 256 | 217 | 173 | 78 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/ai-regulation-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.5 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 0.5 | 0.5 |
| Visualisation from counted data | 4.0 | 3.5 | 0.5 | 0.0 |
| Exploration and drill-down | 3.5 | 2.5 | 1.5 | 1.0 |
| Data export with provenance | 3.0 | 4.0 | 0.5 | 0.5 |
| Reproducibility | 4.5 | 4.5 | 0.0 | 0.5 |
| Traceable references | 1.0 | 1.0 | 1.0 | 0.0 |
| Accuracy against the corpus | 4.5 | 3.5 | 3.0 | 3.5 |
| Calibration and limits | 4.0 | 3.0 | 3.5 | 2.5 |
| Decision-grade verdict | 4.0 | 3.5 | 2.5 | 2.0 |
| Facet coverage | 4.5 | 4.0 | 1.5 | 0.5 |
| **Score /100** | **77.6** | 70.0 | 28.8 | 21.9 |

**Claude Opus judge:** D and B both measured volume, tone and geography from the same traced call. D went further: it named the peak and trough, caught the Colombia and tag-panel artefacts, and placed its limits beside the numbers they bound. A and C could not measure coverage at all; C's memory map is honestly labelled but is not decision-grade. B is a solid second but slightly misreads the enrichment bound and gives a thinner drill-down.

**GPT judge:** A is the strongest decision aid: it combines a fully traced trend with tone, themes, geography, selected headlines, and unusually specific limits. B has cleaner complete exports, but answers less of the global country and story question; neither deliverable provides a verifiable linked reference set.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/ai-regulation-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/ai-regulation-pulse.pdf)

## Live MCP session

Here each model was given only the question and a live connection to the Prism MCP server, and chose its own calls.

**Claude** (claude-sonnet, 163.9 s) called 3 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `prism_overview` | `{}` | see payload · 78 chars |
| 2 | `prism_overview` | `{"term": "AI regulation"}` | ok · 40,090 chars |
| 3 | `freshness_status` | `{}` | ok · 735 chars |

<details><summary>Claude's answer</summary>

**Direct answer:** Coverage of AI regulation is rising, heavily negative, and centred on the US, UK and China. It is framed mainly as ethics and tech policy. The data stops at 31 May 2026. June onward is too thinly ingested to read.

**What the data shows** (Prism news corpus, 1 Jun 2024 – 31 May 2026, term "AI regulation", mention match)
- **Volume:** 4,069 articles. Monthly volume rose from 113 (Jun 2024) to 256 (May 2026, the peak). That is about 53% compound annual growth, and the late third of the window ran 1.46× the early third.
- **Tone:** 57.1% negative against 41.0% positive. The negative-to-positive ratio is 1.39, against a corpus baseline of 0.58, so about 2.4× more negative than ordinary news. 3,638 articles (89%) are flagged critical.
- **Countries:** Geography covers only 36.7% of articles (May 2024 – Apr 2026). Of those placed, the US has 28.4%, the UK 9.4%, China 9.0%, Colombia 4.8%, India 4.8%, France 3.9%, Canada 2.8% and Australia 2.5%. Colombia is over-indexed (lift 9.9) and Belgium's lift is 4.4. Place labels can mis-resolve, so treat those two cautiously.
- **Themes (lift-ranked):** Ethical considerations in AI development are 21.3% of articles that carry a subcategory label. Tech policy and government regulation is 13.7% and data-privacy regulation 6.4%. Top categories are business 22%, technology 20% and politics 20%.
- **Actors:** The most-linked organisations are OpenAI (326 articles), Meta (193) and the European Parliament (84). The most-mentioned people are Gavin Newsom (82) and Scott Wiener (34).
- **Critical stories (Feb–May 2026):**
  - Trump scrapped an AI executive order on 21 May, and Politico reported a split among White House staff.
  - The EU agreed in early May to weaken or delay AI Act high-risk obligations, with a deadline of December 2027.
  - Sam Altman called for urgent regulation and a global watchdog at the India AI Impact Summit (Feb 2026).
  - Industry money is flowing into the 2026 US midterms.

**Interpretation (mine)**
- The US federal retreat and the EU softening are probably what drives the rising negative tone, but I did not test that causally.
- The "critical" flag is very broad. At 89%, it separates little.
- The US and UK lead partly because the corpus favours English-language sources.

**Caveats:** Only about a third of the articles carry a place label. Publisher spread is wide: no outlet exceeds 4.7% of the sampled articles.

</details>

**ChatGPT** (gpt-6-luna, 311.0 s) called 12 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `news_geography` | `{"term": "AI regulation", "since": "2025-10-22", "until": "2026-05-31", "level": "country", "limit": 15}` | ok · 6,441 chars |
| 2 | `news_themes` | `{"term": "AI regulation", "since": "2025-10-22", "until": "2026-05-31", "limit": 15}` | ok · 17,232 chars |
| 3 | `news_entities` | `{"term": "AI regulation", "since": "2025-10-22", "until": "2026-05-31", "kind": "country", "limit": 15}` | ok · 13,821 chars |
| 4 | `prism_overview` | `{"term": "AI regulation", "since": "2025-10-22", "until": "2026-05-31", "granularity": "month"}` | ok · 71,245 chars |
| 5 | `critical_news` | `{"term": "AI regulation", "days": 365, "limit": 10}` | ok · 18,067 chars |
| 6 | `freshness_status` | `{}` | ok · 1,709 chars |
| 7 | `news_geography` | `{"term": "AI regulation", "since": "2025-10-22", "until": "2026-05-31", "level": "country", "limit": 12}` | ok · 5,993 chars |
| 8 | `news_themes` | `{"term": "AI regulation", "since": "2025-10-22", "until": "2026-05-31", "limit": 12}` | ok · 14,834 chars |
| 9 | `critical_news` | `{"term": "AI regulation", "days": 220, "limit": 8, "match": "central"}` | ok · 13,316 chars |
| 10 | `recent_news` | `{"term": "AI regulation", "since": "2025-10-22", "until": "2026-05-31", "country": "china", "limit": 5, "match": "central"}` | ok · 5,860 chars |
| 11 | `recent_news` | `{"term": "AI regulation", "since": "2025-10-22", "until": "2026-05-31", "country": "united kingdom", "limit": 5, "match": "central"}` | ok · 5,874 chars |
| 12 | `recent_news` | `{"term": "AI regulation", "since": "2025-10-22", "until": "2026-05-31", "country": "india", "limit": 5, "match": "central"}` | ok · 9,648 chars |

<details><summary>ChatGPT's answer</summary>

AI regulation coverage is led by the United States, with China and the UK the next most covered countries. The main frame is political and commercial: who sets the rules, and how those rules affect technology and business.

**What Prism’s data shows — 22 Oct 2025–31 May 2026:** It matched 1,591 articles to “AI regulation.” Country labels were available for 27.6% of 1,339 matched articles, so the country ranking is partial: United States 284, China 95, UK 86, India 51; Colombia and France 30 each. [Prism country coverage](https://prism)

Among labelled coverage, politics appeared in 1,045 articles, business in 1,077, technology in 850, and social issues in 654; categories overlap. [Prism themes](https://prism) Specific recurring themes included AI policy and government rules, ethics, and data privacy.

Critical stories in the window include the US debate over restricting states’ power to regulate AI ([December executive order coverage](https://www.yahoo.com/news/articles/trump-says-hell-sign-executive-143924071.html)), India’s AI Impact Summit and calls for global oversight ([summit coverage](https://www.digit.in/news/general/india-ai-impact-summit-2026-openai-ceo-sam-altman-calls-for-global-ai-watchdog-as-superintelligence-nears.html)), and reported plans for stricter Indian rules on deepfakes and cybersecurity ([India coverage](https://www.startuptalky.com/news/india-govt-considers-stricter-ai-governance/)).

**Interpretation:** The coverage suggests a two-track story: US federal–state conflict over regulatory authority, alongside broader debate about national rules, privacy, ethics, and coordination. The country labels cover only a subset, and Prism’s news ingest becomes sparse after May 2026; this is a bounded snapshot, not a full account through today.

</details>

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How is AI regulation being covered globally? Which countries, which themes, which critical stories?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "ai regulation", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'ai regulation', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
