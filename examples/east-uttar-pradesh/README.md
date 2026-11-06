# Eastern Uttar Pradesh: a multi-vertical regional brief

> A region read two ways. First as a **chain** — leading with the signal that dominates eastern UP
> (Purvanchal), **climate**, and following it downstream through weather, disaster and the health
> crisis it causes. Then **widened** across the other verticals the same corpus surfaces: crime,
> agriculture, migration and economy, religion and tourism — each looked into with its own data, and
> the whole thing closed on a mood that tracks the hazard calendar. Every count is measured from the
> data; every quoted factor is extracted and verified; publisher and company names are withheld, and
> *IMD* = India Meteorological Department (the public body in the weather alerts).

**Subject:** eastern Uttar Pradesh (Purvanchal) · **Retrieved:** 2026-11-06 · **Tools:**
`news_themes`, `news_trends`, `news_sentiment`, `critical_news`, `disease_profile`, `find_evidence`

---

## The flow, in one picture

The spine of the brief is this causal chain — the climate signal is the upstream cause of the
region's worst health outcome, and the corpus connects the two by name.

```mermaid
flowchart LR
  A["Monsoon and heavy rainfall<br/>climate signal · 58× lift"] --> B["Flooding and water-logging<br/>disaster · 17× lift"]
  F["Water released from Nepal<br/>into the Ghaghra and Rapti"] --> B
  B --> C["Encephalitis risk factors<br/>monsoon · water-logging · malnutrition"]
  C --> D["Child mortality<br/>2019 surge: 692 claims"]
  E["Weak health system<br/>'inaction of the state machinery'"] --> D
```

## The vertical landscape

Before following the chain, the lay of the land. Rank the region's **highest-priority** stories by
subject and the verticals fall out: weather dominates, but **health, governance, crime and
agriculture** are all live beats. Two of them — crime and health — barely register as *news
categories* yet surface sharply at the *event* level; that gap is itself a finding, and the sections
below treat each on its own terms.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/vertical-landscape-dark.png">
  <img alt="Horizontal bars of east-UP high-priority stories by vertical, out of the top 20: weather/climate/disaster 8, health 4, governance/politics 3, crime/law-and-order 2, accident/social 1, education/tech 1, agriculture/infrastructure 1." src="./assets/vertical-landscape-light.png" width="100%">
</picture>

---

## 1 · Climate — the defining signal

Ask the corpus what makes eastern UP *distinctive* and three hazard categories tower over everything:
**climate 58×** the national baseline, **weather 20×**, **disaster 17×**. No other theme is close. For
this region the climate is not a section of the news — it *is* the news.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/news-distinctiveness-dark.png">
  <img alt="Horizontal bars of news categories by lift over the all-India baseline for eastern UP: climate 58x, weather 20x, disaster 17x tower over infrastructure development 17x, religion 8x, tourism 5x, science 5x, infrastructure 4x, culture 4x, agriculture 4x." src="./assets/news-distinctiveness-light.png" width="100%">
</picture>

Break that signal into sub-themes and it resolves into a **water** story first: rainfall &
precipitation **14.1%** of labelled weather items, monsoon updates **6.3%** — a fifth of weather
coverage — with forecasting and lightning alerts filling the rest, heat a distant last.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/hazard-composition-dark.png">
  <img alt="Horizontal bars of east-UP weather sub-themes by share: rainfall 14.1% and monsoon 6.3% (water), forecast updates 13.3% and regional patterns 10.4% (forecasting), lightning alerts 9.9% (storm), daily temperature 3.3% (heat)." src="./assets/hazard-composition-light.png" width="100%">
</picture>

> **Common issues, measured:** monsoon rainfall and flooding (20% of weather coverage), thunderstorm
> & lightning (~10%), heat (~3%). Anchor place-tag: **Gorakhpur** (497× lift).

---

## 2 · Weather — the hazard calendar

One level down the signal is **operational** — the region runs on forecasts and warnings (IMD tag
98× lift) — and the warnings **rotate**, so there is no off-season. The dated, verified high-priority
alerts assemble into a calendar:

| When | Hazard | Verbatim from the corpus |
|---|---|---|
| **December** | Dense fog | *"dense fog"*, *"zero visibility or below 50 metres"* across **13 districts** of the Terai belt and eastern UP |
| **Apr–Jun** | Heat + lightning | an IMD orange alert pairing a **47°C** heatwave with *"thunderstorms, lightning"*; an earlier report records a *"death toll from the heatwave in eastern Uttar Pradesh, Bihar"* |
| **Jul–Sep** | Monsoon flood | *"many major rivers across the state … flow above the danger mark"* — the **Ganga** *"above danger mark … Allahabad, Varanasi flooded"* |
| **Oct** | Cyclone tail | a late cyclone *"broke a 20-year record"*, dropping the max temperature to **22.7°C** with 24 mm rain |

The extraction tool discarded two further flood factors *"because no source named"* — the discipline
that lets the rest be quoted at all.

---

## 3 · Disaster — the flood mechanism

When rain and monsoon tip over they register as **disaster** (17× baseline), and the corpus names the
*mechanism*: east-UP flooding is a **two-source** problem — the monsoon from above and water from
across the border — *"late monsoon rain, along with water released from Nepal into our rivers, have
been causing flooding of fields."* The rivers that drown Purvanchal (the **Ghaghra** and **Rapti**)
rise in Nepal, so an upstream release lands as a flooded paddy downstream. The recorded impact is
exactly that — *"flooding of fields"* (crop loss) and **water-logging** that lingers into the
encephalitis season of Section 4. The flood belt is a region, not a state line: co-occurring tags are
**Bihar** (110×) and **Jharkhand** (151×).

> **⟡ Research-scope deep-dive — the floods are not from more rain** *(33 papers · 39 s build)*. Point
> the research-scope engine at flood *drivers* and the obvious explanation fails: mean rainfall across
> the belt has been **falling**, not rising — annual and monsoon rainfall declined across Bihar over
> 1901–2002 (**−2.17 / −2.13 mm·yr⁻¹**), with significant negative trends across the Kosi, Gandak and
> Sone sub-basins. The water comes from **concentration and saturation**, not totals: the monsoon months
> carry **84%** of the year's rain, late-September 2019 ran **176% above average** with soil moisture
> **19% above**, and rising monsoon groundwater (a ~2 m head swing) tops up the rivers. One monsoon left
> **7,019 km²** of the plain submerged. The driver is *timing and extremes*, not the annual sum.
> *(10 studies, 2017–2024; DOIs in [`data.json`](./data.json).)*

---

## 4 · Health — bigger than encephalitis

The dominant health emergency is **acute encephalitis syndrome** — **1,523 extracted claims**,
spiking to **692 in 2019**.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/encephalitis-trend-dark.png">
  <img alt="Line chart of acute-encephalitis extracted claims per year 2015-2025, spiking to 692 in 2019." src="./assets/encephalitis-trend-light.png" width="100%">
</picture>

Its causes split into two families — and the first *is Section 1*: **monsoon, water-logging, heavy
rainfall, malnutrition**. The second is the amplifier: *"inaction of the state machinery,"* *"poor
governance,"* *"lack of medical facilities."* So encephalitis here is a **monsoon disease multiplied
by poverty and a weak health system.**

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/encephalitis-factors-dark.png">
  <img alt="Horizontal bars of factors tied to the encephalitis crisis by family. Environmental: malnutrition 8, malnourished children 4, monsoon 3, children under 15 3, water-logging 2, heavy rainfall 2. Governance: inaction of the state machinery 3, poor governance 2, lack of govt medical facilities 2, 'poorest of the poor' 2." src="./assets/encephalitis-factors-light.png" width="100%">
</picture>

But the high-priority feed shows health is **wider** than encephalitis, and the measurements are
grim-to-hopeful: a verbatim *"399 deaths this year"* from brain fever reported by the Gorakhpur
government medical college; a *"rare incidence"* of cerebral **malaria** (mixed *Plasmodium*); drug-
resistant **tuberculosis** work at a Gorakhpur tertiary hospital; and, on the other side, a new
**32-bed ICU** *"ready… to relieve severe patients from Eastern Uttar Pradesh, Bihar and Nepal."* One
Gorakhpur hospital is the referral point for three jurisdictions — the health geography mirrors the
flood geography.

> **⟡ Research-scope deep-dive — the cause is not what the name says** *(38 papers · 38 s build)*. Run
> the engine on the *etiology* of the syndrome and the headline reverses: the leading identified cause
> of acute encephalitis syndrome in eastern UP is **scrub typhus** (*Orientia tsutsugamushi*), a
> mite-borne rickettsial infection — **not** Japanese encephalitis. Among **2,529** hospitalised AES
> cases in eastern UP, **50%** were antibody-positive and **37%** DNA-positive for *O. tsutsugamushi*;
> Gorakhpur seroprevalence ran **70.8%** in the epidemic season. JE virus turned up in only **10.3%** of
> 407 Gorakhpur AES patients, dengue in **7.1%**. It matters clinically: scrub typhus is treatable with
> a cheap antibiotic (doxycycline) — a very different intervention from a JE vaccine.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/health-etiology-dark.png">
  <img alt="Horizontal bars of the share of tested AES/febrile patients positive by cause in eastern UP: scrub typhus 50%, Japanese encephalitis 10.3%, dengue 7.1%, leptospira 3%. Scrub typhus dominates." src="./assets/health-etiology-light.png" width="100%">
</picture>

*(12 studies, 2017–2022; DOIs in [`data.json`](./data.json).)*

---

## 5 · Crime and law-and-order

Here the honesty model earns its keep. As a **news category** crime barely registers — the literal
term runs to a handful of articles, because crime news is tagged by its specifics, not by the word
"crime." But at the **event** level the structural signal is sharp, and it is the one Purvanchal is
infamous for: the **Bihar-border illegal-arms pipeline.** A single seizure in the corpus: a man
arrested in **Chandauli** carrying *"five pistols… five magazines of 32 bore,"* running them from
**Munger** (Bihar's gun-making hub) toward **Bhadohi.** And the politics is violent — a sitting Lok
Sabha MP from the region reporting a *"threat to life… criminals in Eastern Uttar Pradesh are
planning to harm him."*

> **The read:** crime in east UP is a *trafficking-and-muscle* story, not a property-crime beat — and
> it under-registers in categorical coverage precisely because it lives in one-off seizures and
> threats. The vertical-landscape chart (2 of the top 20 stories) is the honest floor, not the ceiling.

---

## 6 · Agriculture and the rural economy

At the news level, agriculture here is water: the upside is irrigation — the **Saryu Canal** expansion
to cover *"14.04 lakh hectare"*, *"great relief to the farmers of Eastern Uttar Pradesh"* — and the
downside is Section 3's flood landing on the same fields (*"flooding of fields"*; a monsoon flood that
reached relatives *"by boat"*). But the headline stops at the water's edge. For the **science** of what
ails these soils, this section is built with a different engine — and that difference is the point.

Because the academic corpus does not index "eastern UP" (Section 10), the depth below comes from
Prism's **research-scope** flow run on the agro-ecological system the region belongs to — the **eastern
Indo-Gangetic rice-wheat plain**. One scope gathered **93 findings from 38 papers** *(~40 s build)*;
focusing it on soil, water and yield returns a read no news feed carries.

**Soil — conventional practice is draining it.** Under puddled, conventional tillage soil organic
carbon stays low or falls: conventional-till rice-wheat gained only **0.9 t C/ha**, and intensified
cropping without conservation depleted total organic carbon **17.56%** at 0–30 cm. Conservation
agriculture reverses it — zero-till with residue gained **3.0–4.7 t C/ha** (3–5× conventional), lifted
soil carbon **+20% / +40%** in the 0–15 and 15–30 cm layers, and non-puddled rice with residue raised
SOC **+79%** and nitrogen **+62%** — but only near the surface; below 0.15 m, tillage made no
difference.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/agriculture-soil-carbon-dark.png">
  <img alt="Horizontal bars of soil carbon gained over the trial (t C/ha) by farming practice in eastern Indo-Gangetic rice-wheat: conventional tillage 0.9, zero-till no residue 1.1, zero-till plus residue 3.0 and 4.7. Conservation farming rebuilds soil carbon 3-5x faster." src="./assets/agriculture-soil-carbon-light.png" width="100%">
</picture>

**Salinity & sodicity.** On sodic soils, gypsum and pressmud cut sodification and compaction and raised
total organic carbon **32–64%** with about **25% higher yield**; across the trials, rice-wheat yield
rose with soil carbon and fell with pH, exchangeable-sodium percentage and bulk density — the chemistry
of a tired soil, quantified.

**Water.** The Gangetic aquifer is not the single homogeneous body it is mapped as — recharge,
permeability, storage and chemistry vary sharply across it. In the UP study region the groundwater is
neutral-to-alkaline, CaMgHCO₃-type and rock-dominated, and **40% of samples exceed the 50 mg/l nitrate
limit** — unfit for direct use. Yet the agronomy also finds slack: shifting wheat **sowing dates** alone
could unlock **+69%** untapped wheat potential with no trade-off on rice, irrigation or profit.

> **⟡ Research-scope deep-dive — the water table is being irrigated away** *(37 papers · 38 s build)*.
> A second scope on groundwater finds the depletion is irrigation-driven: irrigation raised modelled
> evapotranspiration **12%** across the Ganges basin, net irrigation ran **~101 mm·yr⁻¹ (67 km³)** with
> **70%** drawn in the dry season, and **83%** of 300 surveyed eastern-UP farmers said they had
> *increased* irrigation. The basin-scale cost is real — modelled irrigation-driven depletion cut
> freshwater flow to the Bay of Bengal by up to **1,200 m³·s⁻¹**, and reduced irrigation availability
> mapped to wheat-yield losses of **−4% to −36%**. On quality it confirms the nitrate signal above —
> Varanasi borewells **80% over** the 50 mg/l limit. *(11 studies, 2018–2025; DOIs in [`data.json`](./data.json).)*

**Yield & the rural economy.** System rice-equivalent yield ran **15.72–16.39 t/ha** under conservation
scenarios against **10.30** at baseline; nutrient-expert fertiliser cut wheat global-warming potential
**12–20%** while **>80% of participating farmers raised both yield and income**. And the human floor
shows through: resource-poor farm households are the most exposed to simulated drought, cushioned only
where off-farm income exists.

> **Why this section is deep where Sections 1–5 were thinner:** it was built with Prism's research-scope
> flow — a question becomes a scope of extracted findings carrying a scope-id, then a model re-analyses
> that scope for one focus (soil, water, yield). The earlier sections used the news/claim tools, which
> match on titles and return little for a sub-region. Same corpus, different engine.
> *(Sources: eastern Indo-Gangetic rice-wheat field trials, 2017–2022; study DOIs in [`data.json`](./data.json).)*

---

## 7 · Migration and the economy

Downstream of a hazard-exposed, under-industrialised belt is Purvanchal's other defining fact:
**labour out-migration.** The research corpus can't even measure it (Section 10), but the policy
response is all over the feed — the state trying to *manufacture* reasons to stay: **land-ownership
certificates** distributed to tribal and resettled families, and a Gorakhpur **"Centre of Excellence"**
built with a major IT-services firm to teach *"emerging technology to the youth of Eastern Uttar
Pradesh."* Even the grid is contested terrain — power-department staff *"mobilised against
privatisation."* The economic question underneath every vertical is whether the belt can hold its
own people.

> **⟡ Research-scope deep-dive — even the research can't see it** *(10 papers · 33 s build)*. Point the
> engine at out-migration and it comes back **honestly near-empty**: of the findings it gathered, none
> directly measures what drives out-migration from eastern UP, the evidence is Bihar-proxy and
> observational, and there is **no data on migration flows, destinations within India, or Purvanchal
> specifically**. The one driver-like signal is that circular labour migration tracks *scarce local
> opportunity*. The region's defining economic fact is, in the formal literature, a near-blank — which
> is exactly why the news and the migration itself (Section 10) carry the story the papers do not.

---

## 8 · Religion, culture and tourism

The region's other identity is **sacred geography** — and it is a real slice of the coverage:
religion, culture and tourism together run ~**250 articles** (religion alone at **8× lift**). This is
the land of **Varanasi** (Kashi) and the **Gorakhnath** temple; the place-tags carry the *Ram temple*
and pilgrimage towns like **Shravasti**. It is the one vertical where the region's dominant news tone
is *positive* rather than hazard-negative — and, as Section 9 shows, it is what pulls the autumn mood
back above the line.

---

## 9 · The mood follows the hazard calendar

Put 24 months of sentiment together and the region's mood is **seasonal**, in lockstep with the
hazards above it. The net negative:positive ratio peaks in **May–July** (heat, then monsoon flood) and
in the January cold snap; it falls well below the line in **October–November**, the festival and
harvest season. The overall tone is *"somewhat more negative than ordinary news coverage"* (1.16× the
corpus baseline) — a region whose news is driven by what the weather does to it.

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="./assets/sentiment-season-dark.png">
  <img alt="Bar chart of east-UP mean negative-to-positive news ratio by calendar month (2024-26). Bars above the 1.0 balance line (net negative) in Jan, May, Jun, Jul; well below (net positive) in Feb, Oct, Nov. Heat+monsoon months are net negative; festival/harvest months net positive." src="./assets/sentiment-season-light.png" width="100%">
</picture>

---

## 10 · The honest boundary — what the research corpus can't tell us

Everything above is built from the **news problem-space** and the **extracted disease-claim layer** —
because when the region is put to the *academic research* tool as a claim, the lanes collapse:

| Claim put to `find_evidence` | Both-sides papers | What Prism did |
|---|--:|---|
| encephalitis causes high child mortality **in eastern UP** | **0** | returned `no_data` (`ok:false`) |
| river flooding damages agriculture **in eastern UP** | **0** | fell to the subject lane; papers are Sikkim / Sundarbans / J&K |
| lack of employment drives out-migration **from eastern UP** | **4** | thin subject lane; *"employment in eastern uttar pradesh"* = 0 titles |

**The academic title index does not resolve sub-national Indian regions.** A search-box model would
have written a confident paragraph anyway. Prism said *"no data,"* named the fallback, and the
region's real intelligence surfaced where it lives. *(Reliability in real time: during this run the
data backend dropped in and out — `news_factors` failed outright at one point while coverage was
degraded. Degraded coverage returns floors, not totals, so any figure pulled during an outage is a
silent undercount. Every number in this brief is from a **full-coverage** read; the pulls that came
back degraded were deferred, not estimated.)*

---

## Why this is "intelligence," not a dashboard

A dashboard shows ten unrelated panels. This brief shows **one causal chain** — monsoon → flooding →
water-logging → encephalitis → child death, amplified by poverty and governance — and then widens to
the **verticals the same data surfaces**: a crime economy that lives in border arms-seizures, an
agriculture that rides the same rivers that flood it, a migration the research can't measure, a sacred
geography that lifts the autumn mood. Leading with the dominant signal, following it downstream, and
being explicit about which verticals the corpus quantifies (weather, health, sentiment) versus which
it only *witnesses* (crime, migration) is what turns a pile of counts into a brief you can act on.

---

## Reproduce it

```bash
# the vertical landscape + the mood, from the same regional query
curl -s .../prism/v1/news.critical  -H "$AUTH" -d '{"term":"eastern Uttar Pradesh","days":540,"limit":25}'
curl -s .../prism/v1/news.sentiment -H "$AUTH" -d '{"term":"eastern Uttar Pradesh"}'

# 1-2. what the region is distinctively about, and the composition of the signal
curl -s .../prism/v1/news.themes  -H "$AUTH" -d '{"term":"eastern Uttar Pradesh"}'

# 3. the flood mechanism (verbatim, verified)
curl -s .../prism/v1/news.factors -H "$AUTH" -d '{"topic":"flooding in eastern Uttar Pradesh"}'

# 4. the crisis downstream — causes, risk factors, the 2019 time-series
curl -s .../prism/v1/research.disease -H "$AUTH" -d '{"disease":"acute encephalitis syndrome"}'

# 10. the honest boundary — a region-specific claim the research corpus can't carry
curl -s .../prism/v1/research.evidence -H "$AUTH" \
  -d '{"claim":"acute encephalitis syndrome causes high child mortality in eastern Uttar Pradesh"}' \
  | jq '{ok, both_sides: .data.lane_counts.intersection, reason: .error.reason}'
```

Over MCP these are `news_themes`, `news_trends`, `news_sentiment`, `critical_news`, `news_factors`,
`disease_profile`, and `find_evidence`. Crime and migration are read at the event level (via
`critical_news`) because the corpus under-categorises them — stated plainly rather than overclaimed.
Full payload in [`data.json`](./data.json).
