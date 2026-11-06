# Eastern Uttar Pradesh: a regional problem-space brief

> A deliberately different kind of example. The others adjudicate a *claim*; this one profiles a
> *place* — eastern UP (Purvanchal) — and in doing so exercises a different half of Prism: the news
> problem-space analytics and the extracted disease-claim layer, not title-matched research. It also
> shows the honest boundary: where the academic corpus **can't** resolve a sub-national region, Prism
> says so and routes around it. Every count is measured from the data; every quoted factor is
> extracted and verified.

**Subject:** eastern Uttar Pradesh (Purvanchal) · **Retrieved:** 2026-11-06 · **Tools:**
`news_themes`, `news_trends`, `disease_profile`, `find_evidence`

---

## What the news corpus says the region is *about*

Ask the news corpus what makes eastern UP distinctive — not what it mentions, but what it covers far
more than the rest of India — and one answer dominates: **extreme weather.** Climate coverage runs
**58×** the national baseline, weather **20×**, disaster **17×**. The concrete sub-themes are rainfall,
monsoon updates, and thunderstorm/lightning alerts; the anchor place-tag is **Gorakhpur** (497× lift),
and the story spills across the porous border into **Bihar** and **Jharkhand**.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/news-distinctiveness-dark.png">
  <img alt="Horizontal bars of news categories by lift over the all-India baseline for eastern UP. Climate 58x, weather 20x, disaster 17x (hazard cluster, highlighted) tower over infrastructure development 17x, religion 8x, tourism 5x, science 5x, infrastructure 4x, culture 4x, agriculture 4x." src="./assets/news-distinctiveness-light.png" width="100%">
</picture>

Across 2024–2026 the region draws **1,101** articles, roughly balanced in sentiment (241 positive /
188 negative in 2025) — a working regional news stream, not a national triumph or scandal.

---

## The signature crisis: encephalitis

The one health emergency the corpus ties tightly to this belt is **acute encephalitis syndrome** —
the disease behind the Gorakhpur and Muzaffarpur child-death tragedies. `disease_profile` returns
**1,523 extracted claims**, and their time-path carries the region's worst year on its face: a spike
to **692 claims in 2019**, the north-India outbreak surge.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/encephalitis-trend-dark.png">
  <img alt="Line chart of acute-encephalitis extracted claims per year, 2015 to 2025, with a sharp spike to 692 claims in 2019 (the outbreak surge) marked in red, otherwise ranging 19 to 141." src="./assets/encephalitis-trend-light.png" width="100%">
</picture>

What makes the extraction layer worth having is *what the claims name as causes.* They split cleanly
into two families — and the second is the striking one. Alongside the expected environmental drivers
(malnutrition, monsoon, water-logging, heavy rainfall), the corpus repeatedly names a **governance**
cause: *"inaction of the state machinery,"* *"poor governance,"* *"lack of medical facilities in
government hospitals,"* the *"poorest of the poor section."*

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/encephalitis-factors-dark.png">
  <img alt="Horizontal bars of factors the corpus ties to the encephalitis crisis, coloured by family. Environmental: malnutrition 8, malnourished children 4, monsoon season 3, children under 15 3, water-logging 2, heavy rainfall 2. Governance/poverty: inaction of the state machinery 3, poor governance 2, lack of govt medical facilities 2, 'poorest of the poor' 2." src="./assets/encephalitis-factors-light.png" width="100%">
</picture>

In this corpus the encephalitis crisis is framed as much a **governance failure** as a pathogen — the
top associations are *Bihar*, *Muzaffarpur* and a *"rising number of deaths."* (Honest caveat: only
**3%** of these claims come from high-tier studies; most are news-derived, so read them as *what is
being said about the crisis*, not as trial evidence.)

---

## What the research corpus could *not* tell us — and why that's the point

Here is the boundary, stated plainly. When the same region is put to the academic research tool as a
*claim*, the lanes **collapse**:

| Claim put to `find_evidence` | Both-sides papers | What Prism did |
|---|--:|---|
| encephalitis causes high child mortality **in eastern UP** | **0** | returned `no_data` (`ok:false`) — the disease has 197 titles, but the region-specific intersection is empty |
| river flooding damages agriculture **in eastern UP** | **0** | fell to the subject lane; the 5 papers are about Sikkim, the Sundarbans, J&K — not east UP |
| lack of employment drives out-migration **from eastern UP** | **4** | thin subject lane; *"employment in eastern uttar pradesh"* appears in **0** titles |

This is not a failure to hide — it's the finding. **The academic title index does not resolve
sub-national Indian regions.** A language model with a search box would have written a confident
paragraph about Purvanchal's flood-hit farms anyway. Prism instead said *"no data"*, named the lane it
fell back to, and the region's real intelligence surfaced where it actually lives: in the **news
problem-space** (1,101 articles, weather-dominated) and the **extracted disease-claim layer** (1,523
encephalitis claims). Knowing which corpus can answer a question — and admitting when none can — is
the product.

---

## The cross-angle insights

1. **A place is a news question, not a title-search question.** For eastern UP the distinctive signal
   — monsoon, flooding, lightning, encephalitis — is dense in the news and disease-claim corpora and
   near-absent from title-matched research. The right tool depends on the subject's *shape*, and Prism
   exposes enough to pick it.
2. **The extraction layer surfaces causes a search can't.** "Inaction of the state machinery" and
   "poor governance" sitting beside "monsoon" and "malnutrition" is a framing you only get by
   extracting factor-claims at scale — and it reframes encephalitis as a governance story.
3. **Refusal is a feature.** Three region-specific research lanes returned 0, 0 and 4 papers, and the
   report says so. The honesty model that reads "inconclusive" on a thin health claim reads "no data"
   on a region the corpus can't index — same discipline, applied to a place.
4. **Different subject, same contract.** Lane, window, coverage, evidence-vs-framing, and the refusal
   to fabricate carry over from the health and economics examples unchanged. Only the corpora that
   answered changed.

---

## Reproduce it

```bash
# what the region is distinctively about, and how much coverage
curl -s .../prism/v1/news.themes  -H "$AUTH" -d '{"term":"eastern Uttar Pradesh"}'
curl -s .../prism/v1/news.trends  -H "$AUTH" -d '{"term":"eastern Uttar Pradesh","granularity":"yearly"}'

# the signature crisis — causes, risk factors, time-series
curl -s .../prism/v1/research.disease -H "$AUTH" -d '{"disease":"acute encephalitis syndrome"}' \
  | jq '{claims, risk_factors: .data.risk_factors, series: .data.series}'

# the honest boundary — a region-specific claim the research corpus can't carry
curl -s .../prism/v1/research.evidence -H "$AUTH" \
  -d '{"claim":"acute encephalitis syndrome causes high child mortality in eastern Uttar Pradesh"}' \
  | jq '{ok, both_sides: .data.lane_counts.intersection, reason: .error.reason}'
```

Over MCP these are `news_themes`, `news_trends`, `disease_profile`, and `find_evidence`. The last one
returns `ok:false` with a reason here — that is the intended behaviour, not an error to route around.
Full payload in [`data.json`](./data.json).
