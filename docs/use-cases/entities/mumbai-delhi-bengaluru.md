# Mumbai vs Delhi vs Bengaluru

[Companies, people & places](README.md) · [All use cases](../README.md) · [How the benchmark works](../../../benchmarks/README.md) · [Prism MCP](../../../README.md)

> **Intelligence requirement.** Three cities on one scale, with growth and tone.  
> **Why it is hard.** Delhi carries national-government news; the comparison has to say so.  
> **Data.** Captured 2026-10-23 from the live Prism MCP server · 2024-06-01 to 2026-06-01 (exclusive) · all listed tables passed strict index partition reads and historical row floors. Saved responses: [mumbai-delhi-bengaluru.json](../../examples/mumbai-delhi-bengaluru.json).

**The question:**

> How does news attention compare across Mumbai, Delhi and Bengaluru, and how does tone differ?

## What Prism returned

| Term | Articles | Share | Critical | Growth (late vs early) | Negative-to-positive | vs all news |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| **mumbai** | 708,512 | 32.2% | 329,321 | 1.24× (flat) | 0.5 | 0.86× |
| **delhi** | 1,176,901 | 53.6% | 727,715 | 1.08× (flat) | 0.8 | 1.38× |
| **bengaluru** | 312,082 | 14.2% | 177,054 | 1.22× (flat) | 0.5 | 0.86× |

![Comparison over time](../img/mumbai-delhi-bengaluru-compare.svg)

![Total coverage](../img/mumbai-delhi-bengaluru-share.svg)

> more coverage is attention, not importance, and a term that is also a common word will over-count — check each term's own volume against its sources panel

## Beyond the news trend

This page also shows: **Drill into a section**. Each section below is one Prism call; the call is printed under it so you can run it on any other company, person, place or phrase.

### Drill-down: delhi → air pollution

**8,939** articles about delhi also mention air pollution: **0.76%** of its coverage; last third of the window vs first: **0.97×**. Tone: 2.83 negative per positive in the section vs 0.8 for delhi overall (the section is covered more negatively than the entity as a whole).

![air pollution share of delhi coverage](../img/mumbai-delhi-bengaluru-x0-drill.svg)

**Inside the section, the top tags are:** delhi (7,795), air pollution (6,952), air quality (3,080), new delhi (3,059), india (2,799), aqi (2,410), delhi-ncr (1,882), ncr (1,762), air quality index (1,715), climate change (1,689)

| Day | Outlets that day | What was reported |
| --- | ---: | --- |
| 2024-11-18 | 225 | delhi is grappling with one of its worst air pollution crises in recent years, with air quality levels plunging to “severe” and beyond. the air quality index (aqi) in the city reac |
| 2024-11-19 | 205 | baku (azerbaijan), nov 18 (pti) delhi's hazardous air quality was a key focus at cop29, as experts warned about the health risks of air pollution and called for immediate global ac |
| 2025-12-15 | 105 | new delhi (ap) — dense toxic smog blanketed india’s national capital monday, pushing air pollution levels to their worst levels in weeks, disrupting travel and causing authorities |
| 2024-11-22 | 98 | congress leader and lok sabha leader of opposition rahul gandhi on friday raised concern over air pollution in the northern part of india, and termed it a “national emergency,” as |
| 2024-10-23 | 90 | as the air quality index (aqi) in the capital city continues to deteriorate, several parts of the national capital have witnessed smog in the last few days. a thick layer of smog e |
| 2025-12-17 | 90 | as delhi environment minister manjinder singh sirsa “apologised” to the people of the capital and blamed the air pollution crisis on the previous aam aadmi party (aap) government, |

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
{"term": "delhi", "scope": "air pollution"}
```

**REST**

```bash
curl -s -X POST "$PRISM_URL/v1/news.drill" -H "Authorization: Bearer $FLIAR_API_KEY" \
  -H 'content-type: application/json' -d '{"term": "delhi", "scope": "air pollution"}' | jq '.data'
```

**Python**

```python
import prism_mcp
r = prism_mcp.REGISTRY["news_drill"]["fn"](term="delhi", scope="air pollution")
print(r["data"], r["window"])
```

**CLI**

```bash
prism call news.drill term='delhi' scope='air pollution'
```

</details>

### Drill-down: mumbai → air pollution

**1,181** articles about mumbai also mention air pollution: **0.17%** of its coverage; last third of the window vs first: **0.89×**. Tone: 2.15 negative per positive in the section vs 0.5 for mumbai overall (the section is covered more negatively than the entity as a whole).

![air pollution share of mumbai coverage](../img/mumbai-delhi-bengaluru-x1-drill.svg)

**Inside the section, the top tags are:** mumbai (1,149), air pollution (937), india (642), delhi (564), air quality (462), aqi (421), bengaluru (328), air quality index (219), bmc (207), climate change (202)

| Day | Outlets that day | What was reported |
| --- | ---: | --- |
| 2024-07-04 | 30 | over seven percent of all deaths (approximately 33,000 each year) in 10 cities in india annually can be attributed to air pollution levels that are below india&#39;s national clean |
| 2024-11-19 | 22 | delhi's air quality stayed in the 'severe plus' category for the second consecutive day on tuesday, with thick smog reducing visibility and pushing air pollution levels to alarming |
| 2025-11-28 | 19 | in the latest assessment of air quality index (aqi) across some major cities, it has been revealed that mumbai’s overall average aqi has not reached a ‘safe’ category in the past t |
| 2025-11-27 | 15 | the bombay high court on thursday remarked that officials cannot attribute mumbai's air pollution to ash clouds from the volcanic eruption in ethiopia, noting that the city's air q |
| 2025-12-03 | 13 | new delhi: amid growing concerns over air pollution in the national capital, dmk rajya sabha mp p wilson on wednesday termed it a "gas chamber", urging the government to reconsider |
| 2024-11-25 | 12 | as urban india battles soaring air pollution, zerodha co-founder nithin kamath has sparked a radical debate: link property prices to air and water quality.advertisement“maybe a pro |

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
{"term": "mumbai", "scope": "air pollution"}
```

**REST**

```bash
curl -s -X POST "$PRISM_URL/v1/news.drill" -H "Authorization: Bearer $FLIAR_API_KEY" \
  -H 'content-type: application/json' -d '{"term": "mumbai", "scope": "air pollution"}' | jq '.data'
```

**Python**

```python
import prism_mcp
r = prism_mcp.REGISTRY["news_drill"]["fn"](term="mumbai", scope="air pollution")
print(r["data"], r["window"])
```

**CLI**

```bash
prism call news.drill term='mumbai' scope='air pollution'
```

</details>

### Drill-down: bengaluru → air pollution

**526** articles about bengaluru also mention air pollution: **0.17%** of its coverage; last third of the window vs first: **0.53×**. Tone: 2.46 negative per positive in the section vs 0.5 for bengaluru overall (the section is covered more negatively than the entity as a whole).

![air pollution share of bengaluru coverage](../img/mumbai-delhi-bengaluru-x2-drill.svg)

**Inside the section, the top tags are:** bengaluru (501), air pollution (439), india (413), mumbai (330), delhi (308), air quality (222), aqi (220), lucknow (134), chennai (131), health (128)

| Day | Outlets that day | What was reported |
| --- | ---: | --- |
| 2024-07-04 | 29 | more than seven percent of all deaths in 10 of india's biggest cities are linked to air pollution, a large study said thursday, leading researchers to call for action to save tens |
| 2025-03-11 | 29 | a new report reveals that 83% of global cities fail to meet who air pollution guidelines, with india, is among the worst-affected nations.bengaluru: most of the world is breathing |
| 2025-12-16 | 16 | by rajesh roy and sibi arasunew delhi (ap) — dense toxic smog blanketed india’s capital on monday, pushing air pollution levels to their worst levels in weeks, disrupting travel an |
| 2024-11-25 | 12 | as urban india battles soaring air pollution, zerodha co-founder nithin kamath has sparked a radical debate: link property prices to air and water quality.advertisement“maybe a pro |
| 2024-07-08 | 8 | a new study published in the lancet planetary health finds that even levels of air pollution below current indian air quality standards lead to increased daily mortality rates in i |
| 2024-11-19 | 8 | delhi's air quality stayed in the 'severe plus' category for the second consecutive day on tuesday, with thick smog reducing visibility and pushing air pollution levels to alarming |

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
{"term": "bengaluru", "scope": "air pollution"}
```

**REST**

```bash
curl -s -X POST "$PRISM_URL/v1/news.drill" -H "Authorization: Bearer $FLIAR_API_KEY" \
  -H 'content-type: application/json' -d '{"term": "bengaluru", "scope": "air pollution"}' | jq '.data'
```

**Python**

```python
import prism_mcp
r = prism_mcp.REGISTRY["news_drill"]["fn"](term="bengaluru", scope="air pollution")
print(r["data"], r["window"])
```

**CLI**

```bash
prism call news.drill term='bengaluru' scope='air pollution'
```

</details>

## Run it yourself

**In Claude, ChatGPT, Cursor or any MCP client**, with the Prism server connected:

```text
How does news attention compare across Mumbai, Delhi and Bengaluru, and how does tone differ?
```

**Over REST** (same function, same envelope):

```bash
curl -s -X POST "$PRISM_URL/v1/news.compare" \
  -H 'content-type: application/json' \
  -d '{"terms": ["mumbai", "delhi", "bengaluru"], "since": "2024-06-01"}' | jq '.data'
```

**From Python**, in-process:

```python
import prism_mcp
r = prism_mcp.REGISTRY['compare_terms']["fn"](**{'terms': ['mumbai', 'delhi', 'bengaluru'], 'since': '2024-06-01'})
print(r["ok"], r["window"], r["meta"]["coverage"]["note"])
```

Tool calls this page is built from: `compare_terms` (51.6 s) → `news_drill` (38.6 s) → `news_drill` (34.3 s) → `news_drill` (34.5 s)

## Take it further

- **Export:** every response is JSON in one envelope (`ok`, `data`, `window`, `meta`), so `jq`, pandas or a spreadsheet import reads it directly. See [Data export](../../DATA_EXPORT.md).
- **Research workflow:** chain this with `research.brief`, `research.citations` and `research.audit` to go from a question to a sourced draft. See [Research analysis](../../RESEARCH_ANALYSIS.md).
