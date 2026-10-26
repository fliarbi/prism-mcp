# ISRO: media intelligence

[Companies, people & places](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A public agency as an entity: launches, missions and the people around them.  
> **Why it is hard.** Mission spikes (Chandrayaan, Gaganyaan) dominate; tone is unusually positive.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [isro-pulse.json](../../examples/isro-pulse.json).

**The question:**

> What is the world saying about ISRO: coverage volume, tone, themes, people and places?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “isro”, Jun 2024 – May 2026 | 18,871 |
| Critical coverage (priority 7–9) | 14,505 (76.9%) |
| Peak month | Jan 2025 (1,533 articles) |
| Last third of the window vs first third | 0.65× (falling) |
| Negative · positive | 16.8% · 81.8% |
| Tone vs all news (negative-to-positive ratio) | 0.21 vs 0.58 baseline: *markedly more positive than ordinary news coverage* |
| What Prism thinks “isro” is | topic |

![Monthly coverage of isro](../img/isro-pulse-trend.svg)

![Tone of isro coverage](../img/isro-pulse-tone.svg)

![Countries in isro coverage](../img/isro-pulse-geo.svg)

![Themes in isro coverage](../img/isro-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “isro” coverage (they also name the companies, people and places it is written about with): india (13,593), earth (4,674), nasa (3,658), space exploration (3,135), bengaluru (2,273), moon (1,996), space (1,052), mars (929), nta (884), srinagar (788), up (779), astronomy (768)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| axiom space | virender sehwag | india |
| iit bombay | ravi shastri | united states |
| space technology | kapila | china |
| defence research and development organisation | dharmendra | united kingdom |
| esa | ekta kapoor | russia |
| european space agency | sunil gavaskar | pakistan |

**Top publishers in a 212-article sample:** livehindustan.com (9%), indiatoday.in (4.7%), newkerala.com (4.2%), thehindu.com (3.8%), indianexpress.com (3.3%), timesofindia.indiatimes.com (3.3%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-05-16 | [Ex-ISRO Scientist Startup Soars: A Rs 1,500 Cr Vision - NewsDIO](https://newsdio.com/ex-isro-scientist-startup-soars-a-rs-1500-cr-vision/) | newsdio.com | 8 | extreme_pos |
| 2026-02-26 | [Isro NVS-02 failure: Broken electrical circuit likely prevented orbit injection, says committee](https://indianexpress.com/article/india/isro-nvs-02-failure-broken-electrical-circuit-says-committee-10553127/) | indianexpress.com | 8 | slight_neg |
| 2026-04-30 | [Joint India-US venture NISAR shows Mexico City sinking at alarming pace - Social News XYZ](https://www.socialnews.xyz/2026/04/29/joint-india-us-venture-nisar-shows-mexico-city-sinking-at-alarming-pace/) | socialnews.xyz | 8 | very_neg |
| 2026-05-09 | [Skyroot Aerospace Soars to $1.1 Billion Unicorn Status as India's First Space-Tech Giant Gears Up for Launch](https://beamstart.com/news/indian-spacetech-startup-skyroot-hits-177829034128) | beamstart.com | 8 | very_pos |
| 2026-04-10 | [ISRO Successfully Conducts Second Integrated Air Drop Test for Gaganyaan Mission - Online Media Cafe](https://onlinemediacafe.com/news/isro-successfully-conducts-second-integrated-air-drop-test-for-gaganyaan-mission/) | onlinemediacafe.com | 8 | very_pos |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 803 | 661 | 318 | 472 |
| Jul 2024 | 594 | 475 | 170 | 410 |
| Aug 2024 | 1,068 | 818 | 150 | 903 |
| Sep 2024 | 488 | 372 | 37 | 442 |
| Oct 2024 | 523 | 411 | 65 | 450 |
| Nov 2024 | 720 | 592 | 77 | 635 |
| Dec 2024 | 1,086 | 911 | 68 | 1,000 |
| Jan 2025 | 1,533 | 1,216 | 156 | 1,356 |
| Feb 2025 | 884 | 590 | 242 | 626 |
| Mar 2025 | 981 | 616 | 327 | 649 |
| Apr 2025 | 738 | 492 | 214 | 516 |
| May 2025 | 639 | 492 | 123 | 506 |
| Jun 2025 | 1,039 | 800 | 175 | 840 |
| Jul 2025 | 1,148 | 809 | 90 | 1,044 |
| Aug 2025 | 1,428 | 1,085 | 187 | 1,209 |
| Sep 2025 | 739 | 574 | 94 | 631 |
| Oct 2025 | 470 | 349 | 32 | 432 |
| Nov 2025 | 763 | 602 | 35 | 723 |
| Dec 2025 | 623 | 518 | 56 | 562 |
| Jan 2026 | 711 | 572 | 132 | 568 |
| Feb 2026 | 492 | 411 | 108 | 380 |
| Mar 2026 | 337 | 254 | 59 | 273 |
| Apr 2026 | 508 | 389 | 60 | 437 |
| May 2026 | 556 | 496 | 192 | 356 |

</details>

## Beyond the news trend

This page also shows: **Areas of activity and company events** · **Drill into a section** · **Month-by-month ultra research**. Each section below is one Prism call; the call is printed under it so you can run it on any other company, person, place or phrase.

### Areas of activity: isro

![Areas of activity for isro](../img/isro-pulse-x0-areas.svg)

| Area of activity | Articles | Lift over all news |
| --- | ---: | ---: |
| Business & Industrial › Aerospace & Defense › Space Technology | 10,757 | 169.6× |
| Science › Astronomy | 7,083 | 117.8× |
| Internet & Telecom › Service Providers › Cable & Satellite Providers | 776 | 47.1× |
| Internet & Telecom › Communications Equipment | 236 | 73.8× |
| Business & Industrial › Aerospace & Defense | 2,939 | 18.6× |
| Jobs & Education › Education › Standardized & Admissions Tests | 1,013 | 9.0× |
| Computers & Electronics › Consumer Electronics › GPS & Navigation | 158 | 20.3× |
| Science › Engineering & Technology | 369 | 13.1× |
| Jobs & Education › Education › Colleges & Universities | 1,699 | 5.8× |
| Law & Government › Military › Air Force | 377 | 11.4× |

**Activity topics inside those areas:** space station infrastructure, microgravity experimentation in biology, orbital mechanics and celestial motion calculations, space suit technology evolution, earth observation satellite applications, satellite communication technologies, space habitat design and engineering, space launch infrastructure development

<details><summary><b>How to run this:</b> <code>news.activities</code> (MCP tool <code>news_activities</code>)</summary>

The function is `activities(term, domain, since, until, limit)` in [`prism/deep.py`](../../../prism/deep.py), registered as the `news.activities` feature in [`prism_mcp.py`](../../../prism_mcp.py): the industry taxonomy each article is classified under (generic news classes removed), the curated subcategories inside it, the top tags, and, with a web domain, the company's news events by type.

**MCP** (Claude, ChatGPT, Cursor, any MCP client): call the tool `news_activities` with

```json
{"term": "isro"}
```

**REST**

```bash
curl -s -X POST "$PRISM_URL/v1/news.activities" -H "Authorization: Bearer $FLIAR_API_KEY" \
  -H 'content-type: application/json' -d '{"term": "isro"}' | jq '.data'
```

**Python**

```python
import prism_mcp
r = prism_mcp.REGISTRY["news_activities"]["fn"](term="isro")
print(r["data"], r["window"])
```

**CLI**

```bash
prism call news.activities term='isro'
```

</details>

### Drill-down: isro → gaganyaan

**2,288** articles about isro also mention gaganyaan: **12.12%** of its coverage; last third of the window vs first: **0.78×**. Tone: 0.04 negative per positive in the section vs 0.21 for isro overall (the section is covered more positively than the entity as a whole).

![gaganyaan share of isro coverage](../img/isro-pulse-x1-drill.svg)

**Inside the section, the top tags are:** isro (2,202), gaganyaan (2,099), india (2,032), earth (989), the indian space research organisation (842), space exploration (784), nasa (748), the international space station (748), shubhanshu shukla (696), indian space research organisation (618)

| Day | Outlets that day | What was reported |
| --- | ---: | --- |
| 2026-04-10 | 49 | sriharikota (andhra pradesh), apr 10 (bnp): the indian space research organisation (isro) has successfully completed the second integrated air drop test (iadt-02) for the upcoming |
| 2025-08-24 | 40 | india is all set to create a pool of astronauts to take part in the future human flight mission. the pool would not be restricted to only air force personnel and would also include |
| 2025-01-16 | 39 | bengaluru, jan 16: in a major boost to india’s ambitious future space missions, isro on thursday successfully performed the docking of satellites as part of the space docking exper |
| 2025-08-23 | 38 | national space day 2025: pm modi urges scientists to prepare for deep space exploration pm modi addressed the nation on national space day. pm also challenged the private sector to |
| 2025-01-31 | 38 | new delhi, jan 31 (pti) the day is not far when an indian citizen will travel to space aboard the indigenously developed gaganyaan spacecraft, president droupadi murmu said on frid |
| 2025-07-15 | 32 | #watch \| axiom-4 mission \| lucknow, up: group captain shubhanshu shukla’s family rejoices and celebrates as he and the entire crew return to the earth after an 18-day stay aboard t |

<details open><summary><b>How to run this:</b> <code>news.drill</code> (MCP tool <code>news_drill</code>)</summary>

The function is `drill(term, scope, since, until, limit)` in [`prism/deep.py`](../../../prism/deep.py), registered as the `news.drill` feature in [`prism_mcp.py`](../../../prism_mcp.py): an article is in the section when it mentions the entity and every scope phrase; the section's monthly volume is divided by the entity's own, its tone compared with the entity's, and its busiest days listed.

The scoping itself is this function: the entity's own match, narrowed by every scope phrase, so the section is always a subset of the entity's coverage:

```python
def _pred(term: str, scope_terms: list) -> str:
    p = news.term_predicate(term, "mention")
    for s in scope_terms:
        p = f"({p} AND {news.term_predicate(s, 'mention')})"
    return p
```

**MCP** (Claude, ChatGPT, Cursor, any MCP client): call the tool `news_drill` with

```json
{"term": "isro", "scope": "gaganyaan"}
```

**REST**

```bash
curl -s -X POST "$PRISM_URL/v1/news.drill" -H "Authorization: Bearer $FLIAR_API_KEY" \
  -H 'content-type: application/json' -d '{"term": "isro", "scope": "gaganyaan"}' | jq '.data'
```

**Python**

```python
import prism_mcp
r = prism_mcp.REGISTRY["news_drill"]["fn"](term="isro", scope="gaganyaan")
print(r["data"], r["window"])
```

**CLI**

```bash
prism call news.drill term='isro' scope='gaganyaan'
```

</details>

### Month by month: Prism reads isro

Prism took the days most outlets reported the subject, one month at a time, read the stories' openings, and wrote what happened and why it mattered; every point cites the stories it rests on.

> **The arc.** India’s space narrative kicked off in June 2025 with its first commercial astronaut flying to the ISS, establishing a new human‑spaceflight foothold. Over the summer, ISRO cemented international collaboration by launching the joint US‑India NISAR satellite and confirmed the first Gaganyaan test flight for December, while also rolling out indigenous technologies such as the Vikram microprocessor. The latter half of 2025 saw a shift toward commercial and industrial integration, highlighted by the transfer of PSLV development to Indian industry, a heavy‑lift LVM3‑M6 launch of the world’s heaviest satellite from Indian soil, and a $145 million public‑private Earth‑observation partnership. Entering 2026, ISRO expanded its multi‑payload capabilities with PSLV‑C62, outlined an ambitious human‑spaceflight roadmap, and advanced lunar and orbital docking projects, even as it grappled with NavIC functionality issues and a security controversy. The program now balances crewed missions, lunar exploration, defense satellites, and growing commercial launch services, positioning India as a rising contender in the global space race.

- **Turning point, 2025-06:** India’s first commercial astronaut launched on Axiom‑4, marking the nation’s entry into crewed spaceflight on a private vehicle.
- **Turning point, 2025-08:** ISRO confirmed the first Gaganyaan test flight for December, moving the human spaceflight program from planning to execution.
- **Turning point, 2025-11:** The agency transferred 50% of PSLV development to Indian industry and inaugurated the Infinity Campus, signaling a major shift toward public‑private manufacturing.
- **Turning point, 2025-12:** LVM3‑M6 delivered the heaviest satellite from Indian soil and launched a $145 million public‑private Earth‑observation partnership, showcasing ISRO’s expanding commercial launch capability.

| Month | Articles | Signal | What happened |
| --- | ---: | --- | --- |
| 2025-06 | 1,039 | new | **India’s first commercial astronaut flies to the ISS on Axiom‑4 after multiple delays** The Axiom‑4 mission, carrying Indian astronaut Group Captain Shubhanshu Shukla, was scheduled for early June but was postponed several times before finally launching in late June. The mission launched successfully and Shukla made his first call from orbit, describing the experience as “indescribable” and greeting viewers with a “namaskar” from space. |
| 2025-07 | 1,148 | turning point | **India celebrated its first astronaut’s safe return while gearing up for its first joint US‑India Earth observation launch** India’s first astronaut, Group Captain Shubhanshu Shukla, completed an 18‑day stint on the International Space Station and splashed down safely on July 15, ending the AX‑4 mission. Space Minister Jitendra Singh hailed Shukla’s return as a moment of pride and glory for India and the world. ISRO scheduled the launch of the NISAR Earth‑observation satellite, the first mission jointly developed with N |
| 2025-08 | 1,428 | escalating | **ISRO advanced its human spaceflight program, secured a new earth‑observation constellation contract, prepared a major communications launch, and highlighted space heritage on National Space Day.** ISRO confirmed the first Gaganyaan test flight for December 2025, with over 80% of critical tests already completed. India’s space regulator awarded a zero‑bid to a Pixxel Space‑led consortium to build a 12‑satellite earth‑observation constellation, a first‑of‑its‑kind development. ISRO scheduled the launch of its fifth LVM3‑M5 communications satellite for 2 November, continuing its steady satelli |
| 2025-09 | 739 | escalating | **ISRO drives indigenous tech and new industry partnership in September 2025** India unveiled a fully indigenous 32‑bit microprocessor, ‘Vikram’, developed by and for ISRO, marking a milestone in domestic space‑grade computing hardware. Schneider Electric partnered with ISRO to deploy advanced automation technology for India’s launch vehicle and satellite missions, strengthening operational efficiency and reliability. |
| 2025-10 | 470 | escalating | **ISRO nears its first crewed flight and readies a new communications satellite amid a broader push for indigenous aerospace and semiconductor capabilities.** ISRO announced that about 90% of the development work on the Gaganyaan crewed mission has been completed, indicating the program is on track for an upcoming human spaceflight. The agency scheduled the launch of the CMS-03 multi‑band communications satellite on 2 November, using its LVM3 launch vehicle, to provide coverage across the Indian subcontinent. Adani Defence and Aerospace signed a major a |
| 2025-11 | 763 | escalating | **India's space sector accelerates with industry partnership, new launch campus, and massive R&D funding** ISRO announced it will transfer 50% of PSLV development to Indian industry, with a HAL‑L&T consortium already building the first PSLV rocket slated for launch by early 2026. The Infinity Campus, a 200,000‑sq‑ft facility inaugurated by Prime Minister Modi, will support design, testing and monthly production of orbital rockets, debuting Skyroot’s Vikram‑I launch vehicle. In a national broadcast, Mod |
| 2025-12 | 623 | escalating | **ISRO’s LVM3‑M6 launch on Dec 24 delivered the heaviest satellite from Indian soil, cementing its commercial launch capability and heralding a new era of public‑private space initiatives.** ISRO confirmed and executed the LVM3‑M6 mission on Dec 24, 2025, using the heavy‑lift LVM3 (Bahubali) from the second launch pad at Satish Dhawan Space Centre, marking the launch of the heaviest satellite ever deployed from Indian soil. The mission carried the U.S. commercial satellite “Bluebird Block‑2” (also called “Bluebird‑6”) under a contract with NewSpace India Limited, highlighting ISRO’s e |
| 2026-01 | 711 | escalating | **ISRO kicked off 2026 with the PSLV‑C62 launch, unveiling an advanced Earth‑observation satellite and multiple co‑passenger payloads while outlining a human‑spaceflight roadmap.** ISRO launched PSLV‑C62 on Jan 12, deploying the EOS‑N1 advanced Earth‑observation satellite and 15 co‑passenger satellites, including eight from foreign partners. The launch marked the start of India’s 2026 space calendar, showcasing ISRO’s capability to conduct multi‑payload missions and reaffirming its role in global satellite deployment. Former ISRO director Josyula A. Kamalakar outlined an amb |
| 2026-02 | 492 | steady | **ISRO pushes forward with Chandrayaan‑4 and Gaganyaan plans while a former employee is arrested for alleged murder** The agency identified a south‑polar lunar landing site and received government approval for the Chandrayaan‑4 sample‑return mission, which is now slated for at least two years out. Astronauts selected for the Gaganyaan crew are applying lessons from prior Russian and U.S. training programs as India prepares for its maiden human spaceflight scheduled for 2027. A former ISRO employee, Nagesh Ishwar  |
| 2026-03 | 337 | escalating | **ISRO pushes forward with defense satellite plans, orbital docking tests, and new commercial ties despite NavIC setbacks** India’s navigation satellite system (NavIC) was reported as not fully functional, raising concerns that the country may be unable to use it for security and strategic purposes. ISRO and the Ministry of Defence are developing a plan to launch specialised satellites dedicated to protecting India’s assets in orbit. The agency is preparing two advanced orbital docking experiments, Spadex‑2 and Spadex‑ |
| 2026-04 | 508 | steady | **ISRO advances crewed mission tests and data access while facing internal security controversy** The agency completed its second integrated air‑drop test (IADT‑02) for the Gaganyaan human spaceflight programme, marking another key milestone toward crewed launch capability. The agency opened a call for proposals to use data from its Aditya‑L1 solar mission, expanding scientific research opportunities, even as a former scientist’s allegations of a spy network and missile‑technology leaks sparke |
| 2026-05 | 556 | steady | **May 2026: India’s security, education, and diplomatic moves set the backdrop for ISRO’s steady month** India carried out Operation Sindoor, a high‑precision cross‑border counter‑terrorism strike that marks a shift in its security doctrine, potentially influencing ISRO’s dual‑use technology priorities. The cancellation of the NEET‑UG 2026 exam and a parliamentary committee’s endorsement of pen‑and‑paper testing sparked debate over India’s education system, highlighting challenges in nurturing scient |

**What to watch:** Progress of the Gaganyaan crewed launch scheduled for 2027; Approval and timeline of Chandrayaan‑4 sample‑return mission; Outcomes of the Spadex‑2 and Spadex‑3 orbital docking experiments; Resolution of NavIC functionality issues and related defense satellite deployments

<details><summary><b>How to run this:</b> <code>analysis.timeline</code> (MCP tool <code>deep_timeline</code>)</summary>

The function is `timeline(term, scope, months, until, per_month)` in [`prism/deep.py`](../../../prism/deep.py), registered as the `analysis.timeline` feature in [`prism_mcp.py`](../../../prism_mcp.py): for each month, the days most outlets reported the subject are read from their openings and summarised with citations; then the arc across the months.

**MCP** (Claude, ChatGPT, Cursor, any MCP client): call the tool `deep_timeline` with

```json
{"term": "isro", "months": 12}
```

**REST**

```bash
curl -s -X POST "$PRISM_URL/v1/analysis.timeline" -H "Authorization: Bearer $FLIAR_API_KEY" \
  -H 'content-type: application/json' -d '{"term": "isro", "months": 12}' | jq '.data'
```

**Python**

```python
import prism_mcp
r = prism_mcp.REGISTRY["deep_timeline"]["fn"](term="isro", months=12)
print(r["data"], r["window"])
```

**CLI**

```bash
prism call analysis.timeline term='isro' months='12'
```

</details>

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is the world saying about ISRO: coverage volume, tone, themes, people and places?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "isro", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'isro', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `prism_overview` (99.8 s) → `news_activities` (14.5 s) → `news_drill` (12.0 s) → `deep_timeline` (7.4 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
