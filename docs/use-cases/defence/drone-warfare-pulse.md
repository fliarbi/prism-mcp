# Drone warfare coverage

[Defence & geopolitics](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A defence-intelligence media read.  
> **Why it is hard.** Ukraine, the Middle East and South Asia each carry a distinct drone story.  
> **Data.** Captured 2026-10-22 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [drone-warfare-pulse.json](../../examples/drone-warfare-pulse.json).

**The question:**

> How is drone warfare covered in the news: volume, places, themes and critical stories?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “drone warfare”, Jun 2024 – May 2026 | 1,431 |
| Critical coverage (priority 7–9) | 1,258 (87.9%) |
| Peak month | Mar 2026 (200 articles) |
| Last third of the window vs first third | 3.49× (rising) |
| Negative · positive | 53.3% · 44.5% |
| Tone vs all news (negative-to-positive ratio) | 1.2 vs 0.58 baseline: *markedly more negative than ordinary news coverage* |
| What Prism thinks “drone warfare” is | topic |

![Monthly coverage of drone warfare](../img/drone-warfare-pulse-trend.svg)

![Tone of drone warfare coverage](../img/drone-warfare-pulse-tone.svg)

![Countries in drone warfare coverage](../img/drone-warfare-pulse-geo.svg)

![Themes in drone warfare coverage](../img/drone-warfare-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “drone warfare” coverage (they also name the companies, people and places it is written about with): ukraine (963), russia (782), ukrainian (390), drones (356), nato (278), moscow (274), kyiv (237), military technology (122), volodymyr zelenskyy (109), operation sindoor (73), the indian army (63), zelensky (54)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| armed forces of ukraine | volodymyr zelenskyy | ukraine |
| british army | mykhailo fedorov | united states |
| nato | vladimir putin | russia |
| indian army | andrey belousov | china |
| raytheon | thales of miletus | iran |
| defence research and development organisation | anil chauhan | india |

**Top publishers in a 217-article sample:** yahoo.com (9.2%), idrw.org (4.1%), bgr.com (2.8%), rnz.co.nz (2.8%), radionz.co.nz (2.8%), island.lk (2.3%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-05-18 | [Russia Downs Over 3,100 Ukrainian Drones in One Week Amid Escalating Attacks - EconoTimes](https://econotimes.com/Russia-Downs-Over-3100-Ukrainian-Drones-in-One-Week-Amid-Escalating-Attacks-1741910) | econotimes.com | 9 | very_neg |
| 2026-04-16 | [Ukraine says it is employing new integrated drone-infantry warfare system](https://www.thestar.com.my/news/world/2026/04/16/ukraine-says-it-is-employing-new-integrated-drone-infantry-warfare-system) | thestar.com.my | 8 | slight_neg |
| 2026-03-30 | [Zentrum russischer Drohnenindustrie angegriffen](https://www.moneycab.com/international/zentrum-russischer-drohnenindustrie-angegriffen/) | moneycab.com | 8 | very_neg |
| 2026-03-27 | [Drones haven't won the fight in Ukraine. That matters as the West learns new ways of war.](https://www.yahoo.com/news/articles/drones-havent-won-fight-ukraine-092001486.html) | yahoo.com | 8 | slight_neg |
| 2026-05-24 | [Ukraine mayor says NATO needs Kyiv’s battle-tested army](https://ca.news.yahoo.com/ukraine-mayor-says-nato-needs-173856627.html) | ca.news.yahoo.com | 8 | slight_neg |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 27 | 23 | 9 | 17 |
| Jul 2024 | 14 | 13 | 8 | 6 |
| Aug 2024 | 22 | 19 | 8 | 13 |
| Sep 2024 | 27 | 23 | 14 | 13 |
| Oct 2024 | 19 | 16 | 7 | 11 |
| Nov 2024 | 39 | 32 | 20 | 19 |
| Dec 2024 | 37 | 29 | 22 | 14 |
| Jan 2025 | 25 | 25 | 14 | 9 |
| Feb 2025 | 31 | 28 | 10 | 19 |
| Mar 2025 | 47 | 43 | 24 | 22 |
| Apr 2025 | 48 | 42 | 23 | 24 |
| May 2025 | 87 | 77 | 50 | 36 |
| Jun 2025 | 49 | 42 | 28 | 21 |
| Jul 2025 | 72 | 55 | 38 | 30 |
| Aug 2025 | 44 | 31 | 20 | 21 |
| Sep 2025 | 111 | 103 | 73 | 38 |
| Oct 2025 | 46 | 41 | 17 | 27 |
| Nov 2025 | 29 | 28 | 20 | 9 |
| Dec 2025 | 43 | 34 | 17 | 23 |
| Jan 2026 | 40 | 32 | 14 | 26 |
| Feb 2026 | 61 | 53 | 27 | 33 |
| Mar 2026 | 200 | 178 | 124 | 70 |
| Apr 2026 | 113 | 101 | 58 | 53 |
| May 2026 | 200 | 190 | 117 | 82 |

</details>

## Claude and ChatGPT, with and without Prism

Each model wrote the same decision-grade report (verdict, measured trend, comparison, charts, drill-down, exports, references), once from memory and once with this page's Prism results. A script traced every number, chart, CSV cell and DOI, then two blind judges (Claude Opus, GPT) scored under the script's ceilings. [How the benchmark works](../../../benchmarks/README.md)

![Benchmark scores](../img/drone-warfare-pulse-benchmark.svg)

| Parameter (0-5) | Claude + Prism | ChatGPT + Prism | Claude alone | ChatGPT alone |
| --- | ---: | ---: | ---: | ---: |
| Measured trend | 5.0 | 4.0 | 1.0 | 0.0 |
| Measured comparison | 4.5 | 4.5 | 0.0 | 0.0 |
| Visualisation from counted data | 3.5 | 3.5 | 1.0 | 0.0 |
| Exploration and drill-down | 4.0 | 3.0 | 1.0 | 1.0 |
| Data export with provenance | 3.0 | 3.0 | 1.0 | 0.0 |
| Reproducibility | 4.0 | 4.0 | 0.0 | 1.0 |
| Traceable references | 1.0 | 1.0 | 0.5 | 0.5 |
| Accuracy against the corpus | 3.0 | 3.5 | 3.0 | 3.0 |
| Calibration and limits | 2.5 | 3.5 | 3.0 | 4.0 |
| Decision-grade verdict | 3.5 | 3.5 | 2.5 | 2.0 |
| Facet coverage | 4.0 | 3.5 | 1.0 | 0.5 |
| **Score /100** | **69.3** | 68.1 | 27.0 | 23.6 |

**Claude Opus judge:** B and D both traced the real series, but B went further. It decomposed critical vs total, read lift to separate distinctive places (Ukraine, Russia) from background ones (US), and surfaced the India–Pakistan (Operation Sindoor) and Middle East strands the question hinges on, with dated headlines that carry urls. D was accurate in outline but generic, and it misread the censor as applying to May. A and C were honest that they had no data, so they offer a decision-maker nothing measured.

**GPT judge:** D is the strongest decision brief: it answers volume, tone and place coverage with traced figures, a reproducible monthly export, and concrete headline examples while bounding what those measures mean. C has richer breakdowns, but its reversed March/April peak values and unsupported geography detail weaken confidence; neither database-backed deliverable charts the requested tone comparison.

Before/after screens, script findings and raw outputs: [benchmark page](../../../benchmarks/results/full/drone-warfare-pulse/README.md) · [full report PDF](https://fliarbi.com/demo/docs/prism-benchmark-v2-4ed65c83/full/drone-warfare-pulse.pdf)

## Live MCP session

Here each model was given only the question and a live connection to the Prism MCP server, and chose its own calls.

**Claude** (claude-sonnet, 168.0 s) called 1 Prism tool:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `prism_overview` | `{"term": "drone warfare"}` | ok · 40,796 chars |

<details><summary>Claude's answer</summary>

**Drone warfare coverage is rising fast, is concentrated on Ukraine and Russia, and is overwhelmingly critical.** All figures come from Prism news, 1 Jun 2024 to 31 May 2026. Prism cuts off at June 2026 because later ingest is incomplete.

**What the data shows**
- **Volume:** 1,431 matching articles. Monthly counts rose from 27 (Jun 2024) to 200 (Mar 2026 and May 2026). The late third of the window had 3.5 times the volume of the early third. Spikes were Sep 2025 (111), Mar 2026 (200) and May 2026 (200).
- **Critical share:** 1,258 articles (88%) were flagged critical. Mean priority ran about 7 out of 9 in most months.
- **Tone:** 53% negative against 45% positive. That is about twice as negative as the corpus baseline, with a negative-to-positive ratio of 1.20 against 0.58.
- **Places** (the place each article is about, with 63% of articles placed):
  - Ukraine 546 articles (16%)
  - United States 492 (15%)
  - Russia 480 (14%)
  - China 159, Iran 147, India 136
  - Pakistan 88 and Poland 54, both with above-average lift
- **Themes:**
  - Defence and military categories dominate.
  - Subcategories led by drone applications in defence, UAV advances, and cyber and space warfare.
  - Top tags: Ukraine, Russia, NATO, Kyiv, Operation Sindoor (India–Pakistan).
- **Named entities:** Zelenskyy appears in 199 articles, Putin in 147, and NATO in 189. Defence firms such as Northrop Grumman and Anduril also appear.
- **Publishers:** coverage is spread out. In a sample of 217 articles, the top outlet, Yahoo, had 9%.
- **Critical stories:**
  - Russia said it downed 3,124 Ukrainian drones in a week (May 2026).
  - Ukraine announced a drone-infantry combat model (Apr 2026).
  - Ukrainian drones hit the Taganrog drone-industry centre (Mar 2026).
  - A US strike hit a drone facility in Syria (May 2026).
  - Analysts argued drones "haven't won the fight" in Ukraine (Mar 2026).

**Interpretation**
- The Ukraine war frames the topic. The "lessons for NATO" and Western procurement angle is growing.
- Two caveats on the critical share. Most war news is flagged critical, so the 88% is partly an effect of that. The sentiment labels are also noisy, since "positive" often marks military success.
- Place and entity labels are incomplete from May 2026 (about 4% filled), so the late-window geography is undercounted.

</details>

**ChatGPT** (gpt-6-luna, 272.0 s) called 6 Prism tools:

| # | Tool | Arguments | Result |
| ---: | --- | --- | --- |
| 1 | `news_trends` | `{"term": "drone warfare", "since": "2024-01-01", "until": "2026-04-30", "granularity": "quarterly"}` | ok · 7,763 chars |
| 2 | `news_geography` | `{"term": "drone warfare", "since": "2024-01-01", "until": "2026-04-30", "level": "country", "limit": 10}` | ok · 5,709 chars |
| 3 | `news_themes` | `{"term": "drone warfare", "since": "2024-01-01", "until": "2026-04-30", "limit": 10}` | ok · 13,133 chars |
| 4 | `critical_news` | `{"term": "drone warfare", "days": 180, "limit": 10}` | ok · 15,497 chars |
| 5 | `news_themes` | `{"term": "drone warfare", "since": "2024-01-01", "until": "2026-04-30", "limit": 10}` | ok · 13,163 chars |
| 6 | `news_geography` | `{"term": "drone warfare", "since": "2024-01-01", "until": "2026-04-30", "level": "country", "limit": 8}` | ok · 5,407 chars |

<details><summary>ChatGPT's answer</summary>

**Drone-warfare coverage rose sharply through the measured period, with Ukraine and Russia dominating the mapped geography and military technology framing the coverage.** These are Prism news-corpus measures, not a census of all reporting.

**What the data shows (1 Jan 2024–30 Apr 2026):** Prism counted **1,360 articles**, **1,187** of them in its high-priority “critical” band. Quarterly volume peaked at **301** in Jan–Mar 2026, versus **61** in Jan–Mar 2024; the last three full quarters had **2.9×** the volume of the first three. The April–June 2026 bucket is partial, so I exclude it from that comparison. Prism’s ingest window is censored at 1 June 2026.  
Of the 1,360 articles, **880 (64.7%)** were assigned a country: Ukraine (615), US (555), Russia (540), China (180), Iran (174). Country counts can overlap; they are places articles are *about*, not publication locations.  
Theme labels emphasize defense (952), politics (925), international relations (716), and military (640). Subcategory labels include defense drone applications (428) and UAV advances (364). [Prism news trends, geography and themes](https://prism)

**Critical stories in Prism’s feed:** Reuters reported Ukraine’s new integrated drone–infantry combat model (16 Apr 2026); a March feature argued drones have not won the Ukraine war and warned against Western overreliance; other high-priority coverage described attacks on Taganrog and Ukraine’s claimed record drone interceptions. [Reuters via The Star](https://www.thestar.com.my/news/world/2026/04/16/ukraine-says-it-is-employing-new-integrated-drone-infantry-warfare-system) · [Business Insider via Yahoo](https://www.yahoo.com/news/articles/drones-havent-won-fight-ukraine-092001486.html)

**Interpretation:** Coverage is increasingly tied to battlefield adaptation, air defense and military investment, with Ukraine–Russia as its center of gravity. Prism’s counts show attention and framing; they do not verify battlefield claims.

</details>

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How is drone warfare covered in the news: volume, places, themes and critical stories?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "drone warfare", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'drone warfare', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
