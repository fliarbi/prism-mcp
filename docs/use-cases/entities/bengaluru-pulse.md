# Bengaluru as a news entity

[Companies, people & places](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** A city as an entity: tech, traffic, water, politics.  
> **Why it is hard.** Bangalore and Bengaluru are one place; tone moves with civic crises.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · research corpus windows below · all listed tables passed strict index partition reads and historical row floors. Saved responses: [bengaluru-pulse.json](../../examples/bengaluru-pulse.json).

**The question:**

> What is the world saying about Bengaluru: coverage volume, tone, themes, people and organisations?

## What Prism returned

### At a glance

| Measure | Value |
| --- | ---: |
| Articles that mention “bengaluru”, Jun 2024 – May 2026 | 312,082 |
| Critical coverage (priority 7–9) | 177,054 (56.7%) |
| Peak month | Apr 2026 (20,245 articles) |
| Last third of the window vs first third | 1.22× (flat) |
| Negative · positive | 32.7% · 65.5% |
| Tone vs all news (negative-to-positive ratio) | 0.5 vs 0.58 baseline: *somewhat more positive than ordinary news coverage* |
| What Prism thinks “bengaluru” is | place |

![Monthly coverage of bengaluru](../img/bengaluru-pulse-trend.svg)

![Tone of bengaluru coverage](../img/bengaluru-pulse-tone.svg)

![Countries in bengaluru coverage](../img/bengaluru-pulse-geo.svg)

![Themes in bengaluru coverage](../img/bengaluru-pulse-themes.svg)

**Top tags.** Every theme above is built from the articles' own tags; these are the most frequent tags on “bengaluru” coverage (they also name the companies, people and places it is written about with): bengaluru (285,885), mumbai (70,170), karnataka (52,412), hyderabad (35,404), pune (22,105), royal challengers bengaluru (19,568), theprint (14,957), rcb (13,861), royal challengers (13,155), siddaramaiah (12,740), bangalore (12,034), kannada (8,333)

### Who and what appears alongside it

| Organisations | People | Places |
| --- | --- | --- |
| theprint | siddaramaiah | india |
| swiggy | sivakumar | united states |
| zepto | g. parameshwara | united kingdom |
| zomato | virat kohli | china |
| air india express | tejasvi surya | australia |
| blinkit | smriti mandhana | japan |

**Top publishers in a 221-article sample:** hindustantimes.com (5.9%), livemint.com (5.4%), timesofindia.indiatimes.com (4.5%), newkerala.com (4.5%), timesnownews.com (4.1%), thehindu.com (4.1%)

### Critical headlines

| Date | Headline | Publisher | Priority | Tone |
| --- | --- | --- | ---: | --- |
| 2026-04-29 | [Bengaluru News: बेंगलुरु में भारी बारिश के बीच अस्पताल की दीवार गिरी, 3 बच्चों समेत 7 लोगों की मौत](https://navbharattimes.indiatimes.com/state/karnataka/bengaluru/bengaluru-heavy-rain-bowring-hospital-wall-collapse-7-dead-siddaramaiah-announces-compensation-of-5-lakh/articleshow/130611356.cms) | navbharattimes.indiatimes.com | 9 | extreme_neg |
| 2026-04-30 | [Bengaluru Rain Chaos After Heatwave IMD Warns Hailstorms Across Karnataka Regions](https://www.newsmobile.in/climate/bengaluru-rain-chaos-after-heatwave-imd-warns-hailstorms-across-karnataka-regions/) | newsmobile.in | 9 | very_neg |
| 2026-04-08 | [Bengaluru Shocker: 19-Year-Old BTech Student Dies by Suicide After Jumping From 9th Floor of Hostel Building \| 📰 Latest](https://www.latestly.com/india/news/bengaluru-shocker-19-year-old-btech-student-dies-by-suicide-after-jumping-from-9th-floor-of-hostel-building-7384471.html) | latestly.com | 9 | extreme_neg |
| 2026-05-02 | [GBA chief commissioner orders removal of dilapidated structures at risk of collapse](https://www.hindustantimes.com/cities/bengaluru-news/gba-chief-commissioner-orders-removal-of-dilapidated-structures-at-risk-of-collapse-101777715395951.html) | hindustantimes.com | 9 | very_neg |

<details><summary>Monthly series (table view of the charts)</summary>

| Month | Articles | Critical | Negative | Positive |
| --- | ---: | ---: | ---: | ---: |
| Jun 2024 | 9,393 | 5,528 | 3,338 | 5,909 |
| Jul 2024 | 11,057 | 7,013 | 4,027 | 6,909 |
| Aug 2024 | 11,358 | 7,079 | 3,831 | 7,374 |
| Sep 2024 | 11,757 | 7,185 | 4,064 | 7,511 |
| Oct 2024 | 14,809 | 8,534 | 5,140 | 9,366 |
| Nov 2024 | 11,548 | 6,617 | 3,498 | 7,912 |
| Dec 2024 | 11,898 | 6,845 | 3,930 | 7,832 |
| Jan 2025 | 13,046 | 7,567 | 4,309 | 8,512 |
| Feb 2025 | 12,491 | 7,222 | 3,481 | 8,777 |
| Mar 2025 | 14,373 | 7,763 | 4,877 | 9,186 |
| Apr 2025 | 13,503 | 6,922 | 4,605 | 8,593 |
| May 2025 | 12,161 | 6,248 | 4,240 | 7,539 |
| Jun 2025 | 11,284 | 6,577 | 3,853 | 7,188 |
| Jul 2025 | 11,852 | 6,472 | 4,119 | 7,550 |
| Aug 2025 | 13,088 | 7,539 | 4,417 | 8,421 |
| Sep 2025 | 13,156 | 7,760 | 4,054 | 8,917 |
| Oct 2025 | 11,688 | 7,171 | 4,017 | 7,484 |
| Nov 2025 | 12,076 | 7,088 | 3,696 | 8,164 |
| Dec 2025 | 12,887 | 7,652 | 4,337 | 8,360 |
| Jan 2026 | 11,165 | 6,458 | 3,609 | 7,379 |
| Feb 2026 | 14,520 | 8,404 | 4,069 | 10,294 |
| Mar 2026 | 16,161 | 8,223 | 5,138 | 10,550 |
| Apr 2026 | 20,245 | 9,955 | 6,027 | 13,686 |
| May 2026 | 16,566 | 9,232 | 5,362 | 10,724 |

</details>

## Beyond the news trend

This page also shows: **Areas of activity and company events** · **Drill into a section** · **City-level geography**. Each section below is one Prism call; the call is printed under it so you can run it on any other company, person, place or phrase.

### Areas of activity: bengaluru

![Areas of activity for bengaluru](../img/bengaluru-pulse-x0-areas.svg)

| Area of activity | Articles | Lift over all news |
| --- | ---: | ---: |
| Sports › Team Sports › Cricket | 40,699 | 11.0× |
| Autos & Vehicles › Motor Vehicles (By Type) › Scooters & Mopeds | 1,654 | 16.3× |
| Business & Industrial › Business Services › Shared Workspaces | 566 | 27.6× |
| Food & Drink › Food & Grocery Delivery › Restaurant Delivery Services | 1,043 | 15.5× |
| Business & Industrial › Business Finance › Venture Capital | 8,557 | 5.2× |
| Travel & Transportation › Transportation › Air Travel | 12,657 | 3.7× |
| Travel & Transportation › Transportation › Taxi & Ride Hail Services | 1,496 | 10.7× |
| Real Estate › Real Estate Listings › Commercial Properties | 4,034 | 6.2× |
| Business & Industrial › Aerospace & Defense › Aviation Industry | 8,752 | 4.0× |
| Real Estate › Property Development | 5,785 | 4.9× |

**Activity topics inside those areas:** cricket domestic leagues, cricket test matches, cricket fan culture and merchandise, cricket women's world cup, cricket women's leagues, cricket coaching methods, cricket sponsorship and branding, domestic flight services

<details><summary><b>How to run this:</b> <code>news.activities</code> (MCP tool <code>news_activities</code>)</summary>

The function is `activities(term, domain, since, until, limit)` in [`prism/deep.py`](../../../prism/deep.py), registered as the `news.activities` feature in [`prism_mcp.py`](../../../prism_mcp.py): the industry taxonomy each article is classified under (generic news classes removed), the curated subcategories inside it, the top tags, and, with a web domain, the company's news events by type.

**MCP** (Claude, ChatGPT, Cursor, any MCP client): call the tool `news_activities` with

```json
{"term": "bengaluru"}
```

**REST**

```bash
curl -s -X POST "$PRISM_URL/v1/news.activities" -H "Authorization: Bearer $FLIAR_API_KEY" \
  -H 'content-type: application/json' -d '{"term": "bengaluru"}' | jq '.data'
```

**Python**

```python
import prism_mcp
r = prism_mcp.REGISTRY["news_activities"]["fn"](term="bengaluru")
print(r["data"], r["window"])
```

**CLI**

```bash
prism call news.activities term='bengaluru'
```

</details>

### Drill-down: bengaluru → water

**2,927** articles about bengaluru also mention water: **0.94%** of its coverage; last third of the window vs first: **0.97×**. Tone: 1.0 negative per positive in the section vs 0.5 for bengaluru overall (the section is covered more negatively than the entity as a whole).

![water share of bengaluru coverage](../img/bengaluru-pulse-x1-drill.svg)

**Inside the section, the top tags are:** bengaluru (2,778), india (1,248), karnataka (856), sustainability (466), bwssb (443), water conservation (402), delhi (394), mumbai (385), chennai (302), water quality (302)

| Day | Outlets that day | What was reported |
| --- | ---: | --- |
| 2025-12-08 | 26 | bengaluru, december 8climate change is battering asia's water and power systems and putting millions in harm's way, forcing countries to pour billions into shoring up basic service |
| 2024-10-16 | 24 | heavy rains in chennai and other places in tamil nadu completely disrupted life. from colonies to roads, knee-deep water filled the place. road, train and air transport systems cam |
| 2025-05-20 | 23 | heavy rainfall continued to batter bengaluru on tuesday and disrupt normal life. people were seen walking through knee-deep water, and traffic jams were reported in several parts o |
| 2024-10-17 | 22 | incessant rainfall in bengaluru in the past few days has brought the bruhat bengaluru mahanagara palike (bbmp) to its knees, with several areas and roads flooded, causing inconveni |
| 2025-02-18 | 21 | in recent months, bengaluru faced a deficit of 300-500 million litres of water daily.in response to the ongoing water crisis, the bengaluru water board has announced stringent fine |
| 2024-10-15 | 21 | heavy rains in bengaluru: viral video shows manyata tech park flooded; early exit suggested for workersauthored by : kanishka singharia updated oct 15, 2024, 16:46 istbengaluru wea |

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
{"term": "bengaluru", "scope": "water"}
```

**REST**

```bash
curl -s -X POST "$PRISM_URL/v1/news.drill" -H "Authorization: Bearer $FLIAR_API_KEY" \
  -H 'content-type: application/json' -d '{"term": "bengaluru", "scope": "water"}' | jq '.data'
```

**Python**

```python
import prism_mcp
r = prism_mcp.REGISTRY["news_drill"]["fn"](term="bengaluru", scope="water")
print(r["data"], r["window"])
```

**CLI**

```bash
prism call news.drill term='bengaluru' scope='water'
```

</details>

### Drill-down: bengaluru → traffic

**5,729** articles about bengaluru also mention traffic: **1.84%** of its coverage; last third of the window vs first: **1.52×**. Tone: 1.14 negative per positive in the section vs 0.5 for bengaluru overall (the section is covered more negatively than the entity as a whole).

![traffic share of bengaluru coverage](../img/bengaluru-pulse-x2-drill.svg)

**Inside the section, the top tags are:** bengaluru (5,381), traffic (1,694), india (1,601), karnataka (1,195), mumbai (979), delhi (916), metro (753), transportation (687), technology (565), traffic congestion (527)

| Day | Outlets that day | What was reported |
| --- | ---: | --- |
| 2025-02-13 | 33 | in an effort to tackle bengaluru’s worsening traffic congestion, the karnataka government plans to invest ₹1 lakh crore, deputy chief minister d.k. shivakumar announced at the inve |
| 2025-05-19 | 32 | bengaluru heavy rains : life in bengaluru was thrown off gear on monday morning after torrential overnight rains left large parts of the city inundated. several key areas, includin |
| 2024-10-15 | 29 | amid severe rain in bengaluru, a dramatic car crash on the mysuru expressway left two young children injured after a head-on collision. the incident occurred on sunday evening, whe |
| 2024-10-16 | 27 | incessant rains had thrown normal life out of gear with waterlogging and traffic congestion in several parts of the city on tuesday.in the last 24 hours till 8.30 am on wednesday, |
| 2025-10-17 | 26 | a video of a bengaluru road. photo: unsplash the karnataka cabinet has approved the long-pending peripheral ring road project, now renamed the bengaluru business corridor, aimed at |
| 2025-10-16 | 24 | this article has been reviewed according to science x's editorial process and policies . editors have highlighted the following attributes while ensuring the content's credibility: |

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
{"term": "bengaluru", "scope": "traffic"}
```

**REST**

```bash
curl -s -X POST "$PRISM_URL/v1/news.drill" -H "Authorization: Bearer $FLIAR_API_KEY" \
  -H 'content-type: application/json' -d '{"term": "bengaluru", "scope": "traffic"}' | jq '.data'
```

**Python**

```python
import prism_mcp
r = prism_mcp.REGISTRY["news_drill"]["fn"](term="bengaluru", scope="traffic")
print(r["data"], r["window"])
```

**CLI**

```bash
prism call news.drill term='bengaluru' scope='traffic'
```

</details>

![City-level geography](../img/bengaluru-pulse-x3-geo.svg)

<details><summary><b>How to run this:</b> <code>news.geography</code> (MCP tool <code>news_geography</code>)</summary>

The function is `geography(term, level, since, until, limit)` in [`prism/news.py`](../../../prism/news.py), registered as the `news.geography` feature in [`prism_mcp.py`](../../../prism_mcp.py): the place each article is about, at country, state or city level, with lift over all news.

**MCP** (Claude, ChatGPT, Cursor, any MCP client): call the tool `news_geography` with

```json
{"term": "bengaluru", "level": "city"}
```

**REST**

```bash
curl -s -X POST "$PRISM_URL/v1/news.geography" -H "Authorization: Bearer $FLIAR_API_KEY" \
  -H 'content-type: application/json' -d '{"term": "bengaluru", "level": "city"}' | jq '.data'
```

**Python**

```python
import prism_mcp
r = prism_mcp.REGISTRY["news_geography"]["fn"](term="bengaluru", level="city")
print(r["data"], r["window"])
```

**CLI**

```bash
prism call news.geography term='bengaluru' level='city'
```

</details>

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
What is the world saying about Bengaluru: coverage volume, tone, themes, people and organisations?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.overview" \
  -H 'content-type: application/json' \
  -d '{"term": "bengaluru", "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['prism_overview']["fn"](**{'term': 'bengaluru', 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `prism_overview` (155.6 s) → `news_activities` (18.5 s) → `news_drill` (32.0 s) → `news_drill` (29.6 s) → `news_geography` (18.0 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
