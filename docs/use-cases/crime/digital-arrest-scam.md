# Digital arrest scams in India

[Crime & public safety](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** An emerging fraud pattern, tracked from first appearance.  
> **Why it is hard.** A 2024+ phrase that most models have never seen in training.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [digital-arrest-scam.json](../../examples/digital-arrest-scam.json).

**The question:**

> What is being reported about 'digital arrest' scams in India?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “digital arrest”, Jun 2024 – May 2026 | 5,394 |
| Critical coverage (priority 7–9) | 4,727 (87.6%) |
| Peak month | Dec 2024 (474 articles) |
| Last third of the window vs first third | 1.17× (flat) |
| Negative · positive | 91.4% · 8.4% |
| Tone vs all news (negative-to-positive ratio) | 10.88 vs 0.58 baseline: *markedly more negative than ordinary news coverage* |
| What Prism thinks “digital arrest” is | topic |

![Monthly coverage of digital arrest](../img/digital-arrest-scam-trend.svg)

![Tone of digital arrest coverage](../img/digital-arrest-scam-tone.svg)

![Countries in digital arrest coverage](../img/digital-arrest-scam-geo.svg)

![Themes in digital arrest coverage](../img/digital-arrest-scam-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “digital arrest” coverage (they also name the companies, people and places it is written about with): cybercrime (1,893), cbi (1,591), fraud (1,400), cyber crime (1,257), whatsapp (1,092), sim (641), aadhaar (615), scam (445), the central bureau of investigation (390), scams (317), delhi police (298), money laundering (290)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| telecom regulatory authority of india | surya kant | india |
| central bureau of investigation | immanuel kant | cambodia |
| sim | tushar mehta | united states |
| canara bank | g. parameshwara | cameroon |
| theprint | narendra modi | china |
| apk | vallabhbhai patel | myanmar |

**Top publishers in a 220-article sample:** livehindustan.com (13.2%), newsmobile.in (7.3%), etvbharat.com (5.5%), abplive.com (5.5%), indianexpress.com (5%), amarujala.com (3.6%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-03-30 | [Digital arrest scam: 63-year-old Mumbai teacher loses over Rs 32 lakh](https://www.mid-day.com/mumbai/mumbai-crime-news/article/digital-arrest-scam-63-year-old-mumbai-teacher-loses-over-rs-32-lakh-23623364) | mid-day.com | 9 | very_neg |
| 2026-05-01 | [Her phone rang as she was being cremated, revealed UP woman's digital arrest trail](https://www.indiatoday.in/india/story/up-bijnor-digital-arrest-uttar-pradesh-woman-suicide-harassment-phone-rang-cremation-case-cybercrime-fraud-news-2904155-2026-05-01) | indiatoday.in | 8 | extreme_neg |
| 2026-04-28 | [Digital Arrest Has No Legal Standing, Senior Citizens Must Stay Alert - Outlook Money](https://outlookmoney.com/retirement/digital-arrest-has-no-legal-standing-senior-citizens-must-stay-alert) | outlookmoney.com | 8 | very_neg |
| 2026-04-28 | [Digital Arrest Has No Legal Standing, Senior Citizens Must Stay Alert - Outlook Money](https://www.outlookmoney.com/retirement/digital-arrest-has-no-legal-standing-senior-citizens-must-stay-alert) | outlookmoney.com | 8 | very_neg |
| 2026-04-18 | [CBI busts 'digital arrest' scam in Andhra, Telangana](https://thebetterandhra.com/news/cbi-digital-arrest-scam-andhra-telangana/) | thebetterandhra.com | 8 | very_neg |
| 2026-05-15 | [Meet Abhay, your new shield against âdigital arrestâ \| Delhi News - The Times of India](https://timesofindia.indiatimes.com/city/delhi/meet-abhay-your-new-shield-against-digital-arrest/articleshow/131125102.cms) | timesofindia.indiatimes.com | 8 | very_neg |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 37 | 31 | 36 | 1 |
| Jul 2024 | 54 | 46 | 53 | 1 |
| Aug 2024 | 108 | 89 | 103 | 5 |
| Sep 2024 | 105 | 86 | 101 | 4 |
| Oct 2024 | 417 | 360 | 364 | 53 |
| Nov 2024 | 415 | 351 | 372 | 41 |
| Dec 2024 | 474 | 371 | 416 | 56 |
| Jan 2025 | 256 | 211 | 236 | 16 |
| Feb 2025 | 161 | 130 | 146 | 15 |
| Mar 2025 | 173 | 147 | 164 | 9 |
| Apr 2025 | 161 | 140 | 142 | 19 |
| May 2025 | 106 | 91 | 104 | 1 |
| Jun 2025 | 110 | 96 | 106 | 4 |
| Jul 2025 | 218 | 176 | 208 | 8 |
| Aug 2025 | 171 | 140 | 149 | 22 |
| Sep 2025 | 236 | 217 | 228 | 8 |
| Oct 2025 | 241 | 225 | 216 | 23 |
| Nov 2025 | 289 | 269 | 272 | 16 |
| Dec 2025 | 294 | 276 | 270 | 22 |
| Jan 2026 | 267 | 252 | 248 | 19 |
| Feb 2026 | 289 | 268 | 256 | 33 |
| Mar 2026 | 228 | 215 | 205 | 23 |
| Apr 2026 | 419 | 393 | 382 | 31 |
| May 2026 | 165 | 147 | 143 | 22 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/digital-arrest-scam-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 4.0 | 4.5 | 1.0 | 0.0 |
| Measured comparison | 4.0 | 4.5 | 1.5 | 0.0 |
| Visualisation from counted data | 3.0 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 2.5 | 3.5 | 1.5 | 1.0 |
| Data export with provenance | 2.5 | 4.5 | 1.0 | 0.0 |
| Reproducibility | 3.5 | 4.5 | 1.0 | 1.0 |
| Traceable references | 1.0 | 0.5 | 0.5 | 0.5 |
| Accuracy against the corpus | 3.5 | 3.5 | 2.0 | 3.0 |
| Calibration and limits | 2.5 | 4.5 | 3.0 | 3.0 |
| Decision-grade verdict | 3.0 | 3.5 | 2.0 | 2.5 |
| Facet coverage | 4.0 | 4.0 | 1.0 | 1.0 |
| **Score /100** | 61.5 | **74.8** | 28.6 | 23.8 |

**Claude Opus judge:** C and B both grounded their work in the same traced corpus call. C went further: it decomposed critical against total coverage, surfaced dated headlines with URLs, and flagged entity-label artefacts. B gave cleaner exports but misread the censoring and omitted headlines. A and D had no measured data; A declined honestly, while D offered memory estimates about a different quantity.

**GPT judge:** A is the strongest decision aid: it answers the question with a traced, correctly qualified coverage trend, tone comparison, useful breakdowns, and reproducible exports. C offers broad coverage of facets but misreads the overall direction and censoring, while B and D either rely on estimates or cannot measure the requested reporting pattern.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/digital-arrest-scam/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/digital-arrest-scam.pdf)

## Live MCP session

Here each model was given only the question and a live connection to the Prism MCP server, and chose its own calls.

**Claude** (claude-sonnet, 182.1 s) called 3 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `prism_overview` | `{}` | see payload · 78 chars |
| 2 | `prism_overview` | `{"term": "digital arrest scam"}` | ok · 39,825 chars |
| 3 | `critical_news` | `{"term": "digital arrest scam", "limit": 6}` | ok · 5,371 chars |

<details><summary>Claude's answer</summary>

**Direct answer:** Indian news treats "digital arrest" scams as a persistent, escalating cybercrime problem. Coverage is almost entirely negative, and the government response has moved from police cases to telecom and platform controls.

**What the data shows** (Prism news corpus, Jun 2024–May 2026, mention match)
- **Volume:** 686 articles, of which 653 (95%) are flagged critical. The first one appeared in July 2024.
- **Trend:** Monthly counts rose from 3 in Jul 2024 to 33 in Oct 2024. They peaked at 75 in Apr 2026. The late third of the window had 1.75× the articles of the early third.
- **Tone:** 94.3% of articles are negative and 5.6% positive. That is roughly 29× more negative than the corpus baseline.
- **Geography:** 67% of articles with a place label are placed in India. Cambodia (30), Myanmar (13) and Laos (7) also appear, which suggests coverage of offshore scam compounds. Place labels are noisy, and the Cameroon count (29) is probably a labelling artefact.
- **Themes:** The articles cluster under cybercrime law and digital forensics, and under public-safety technology. The most frequent organisation labels are TRAI, CBI and MeitY.
- **Typical stories (Feb–May 2026):**
  - Fake police, ED or NIA officers extort victims, many of them elderly. Cases include ₹4.11 crore from an 85-year-old in Thrissur, ₹1.6 crore from a 77-year-old woman in Pune, and ₹60 lakh from a Mumbai widow.
  - Delhi Police busted a network tied to 190+ complaints and suspected proceeds above ₹100 crore (mid-day, Feb 2026).
  - Policy actions reported:
    - The government ordered WhatsApp to block device IDs used in these scams (India Today, 21 Mar 2026).
    - The government told the Supreme Court that fraudulent SIMs can be blocked within 2–3 hours and that WhatsApp banned 9,400 accounts (Navbharat Times, 29 Apr 2026).
- **Outlets:** Coverage is spread across many publishers. The top outlet, Hindustan Times, has about 10% of the sample.

**Interpretation (mine)**
- The April 2026 spike seems to follow the Supreme Court and regulatory activity rather than a verified rise in cases. The corpus counts articles, not victims or losses.
- The stories point to a shift toward targeting the elderly, larger sums and physical cash collection.

**Caveats**
- The data ends 31 May 2026, and the newest months are thinly labelled, so I can't speak to June–October 2026.
- Entity labels are machine-assigned. For example, "Surya Kant" and "Immanuel Kant" appear as people, so I would not rely on them.
- I found no official national loss statistics in these results.

</details>

**ChatGPT** (gpt-6-luna, 179.8 s) called 3 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `critical_news` | `{"term": "digital arrest", "match": "central", "days": 365, "limit": 8}` | ok · 15,900 chars |
| 2 | `news_trends` | `{"term": "digital arrest", "country": "India", "granularity": "quarterly", "since": "2024-01-01"}` | ok · 7,787 chars |
| 3 | `recent_news` | `{"term": "digital arrest scams India", "limit": 10, "since": "2025-01-01"}` | see payload · 1,843 chars |

<details><summary>ChatGPT's answer</summary>

**Indian reporting depicts “digital arrest” as coercive impersonation fraud:** scammers pose as police or federal investigators, accuse targets of links to crimes, keep them on video calls, and pressure them to transfer money. Reports describe large losses among older victims, investigations and arrests, and at least one case involving prolonged intimidation.

**What Prism’s data shows:** Its India-filtered news series counted **2,990 matching articles from January 2024 through May 2026**; **2,693 were scored “critical”** (priority 7+). Coverage peaked at **706 articles in October–December 2024**, then reached **440 in January–March 2026**. Prism’s latest quarter, April–June 2026, is partial and censored at June 1, so it should not be compared as a full quarter. In the latest-year feed, reports included a **₹32.69 lakh** loss by a Mumbai retiree (Mid-Day, March 30, 2026) and a CBI operation with **three arrests** in Andhra Pradesh and Telangana (The Better Andhra, April 18, 2026). [Mid-Day](https://www.mid-day.com/mumbai/mumbai-crime-news/article/digital-arrest-scam-63-year-old-mumbai-teacher-loses-over-rs-32-lakh-23623364) · [The Better Andhra](https://thebetterandhra.com/news/cbi-digital-arrest-scam-andhra-telangana/)

**Interpretation:** The sustained, largely negative coverage and recurring reports of substantial losses suggest a persistent public-safety concern. But article counts measure media attention, not the number of scams or victims; Prism’s news results alone cannot establish the fraud’s true prevalence or whether incidents are increasing.

</details>

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is being reported about 'digital arrest' scams in India?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "digital arrest", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'digital arrest', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
