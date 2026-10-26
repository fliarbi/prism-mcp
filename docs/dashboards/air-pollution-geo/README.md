# Air pollution: geo-intelligence dashboard

**Use case:** GEO intelligence · **Built by:** claude-opus-5-5 connected live to the Prism MCP · **Time:** 7.0 min, 19 Prism calls

**[Open the live dashboard](https://fliarbi.com/demo/docs/prism-dashboards-3bb43e4c/air-pollution-geo/)** · source: [dashboard.html](dashboard.html) (serve it next to the two map files)

![Dashboard, first screen](screenshot.jpg)

## The brief

One prompt, given verbatim:

```text
Build a geo-intelligence dashboard on AIR POLLUTION for an environmental policy team in India, using the
Prism tools. They want to see, on one screen and then below it, where the issue is being reported, where it is
studied, how India compares with the world, and which places and stories are driving it.

Panels:
1. Header KPI tiles: total coverage, India's share of placed coverage and its lift, how much coverage could be
   placed at all, and the research volume. Each tile states its window.
2. World map: the country each article is about, coloured by lift over the all-news baseline, with a ranked table
   (articles, share, lift).
3. India state map: coverage and lift by state. The state level returns places outside India too; show only
   Indian states on the map and list what you excluded.
4. City leaderboard: the Indian cities and the NCR cluster, with lift.
5. Trend: monthly coverage for India against the rest of the world, with the incomplete newest month handled.
6. Studied vs reported vs patented: the separate geography lanes for research and patents next to news, never
   added together, with India and three comparators.
7. The critical stories: date, publisher, headline and link.
8. Data quality: placement share, windows and censoring, and any artefacts you caught (labels that are not
   places, acronym collisions), so a reader trusts the map for the right reasons.
```

Plus the build rules every dashboard gets (Vega-Lite, the official-outline map files, a source line under every panel, CSV downloads, and a `check_report` pass before answering). Full prompt: `session.json`.

## How the assistant built it

The model chose these Prism tools itself, in this order:

| # | Tool | Arguments | Seconds |
|---:|---|---|---:|
| 1 | `corpus_status` | `{}` | 0.25 |
| 2 | `freshness_status` | `{}` | 0.01 |
| 3 | `resolve_term` | `{"term": "air pollution"}` | 1.88 |
| 4 | `article_store_status` | `{}` | 6.0 |
| 5 | `news_geography` | `{"term": "air pollution", "level": "country", "limit": 25}` | 3.59 |
| 6 | `news_geography` | `{"term": "air pollution", "level": "state", "limit": 40}` | 6.43 |
| 7 | `news_geography` | `{"term": "air pollution", "level": "city", "limit": 40}` | 9.51 |
| 8 | `news_trends` | `{"term": "air pollution", "granularity": "monthly"}` | 2.0 |
| 9 | `news_trends` | `{"term": "air pollution", "granularity": "monthly", "country": "india"}` | 4.47 |
| 10 | `global_comparison` | `{"claim": "air pollution", "country": "india"}` | 23.43 |
| 11 | `browse_research` | `{"term": "air pollution", "limit": 5}` | 19.91 |
| 12 | `critical_news` | `{"term": "air pollution", "days": 365, "limit": 12}` | 32.92 |
| 13 | `historical_analysis` | `{"subject_phrases": ["air pollution"], "first_year": 2017, "last_year": 2025}` | 33.71 |
| 14 | `check_report` | `{"html": "<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"w…` | 1.06 |
| 15 | `check_report` | `{"html": "<!DOCTYPE html><html><head><script type=\"application/json\" id=\"report-manifest\">{\"charts\":[]}<…` | 0.44 |
| 16 | `check_report` | `{"html": "<!DOCTYPE html><html><head><script type=\"application/json\" id=\"report-manifest\">{\"charts\":[]}<…` | 0.35 |
| 17 | `list_features` | `{}` | 0.03 |
| 18 | `check_report` | `{"html": "<!DOCTYPE html><html><head><script type=\"application/json\" id=\"report-manifest\">{\"charts\":[]}<…` | 0.51 |
| 19 | `check_report` | `{"html": "<!DOCTYPE html>\n<html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"w…` | 0.89 |

## Checks on the finished page

- Charts rendered in headless Chrome: **5**, zero-width: 0, console errors: 0
- Prism `check_report`: ready, nothing to fix
- India appears with its official outline (J&K including PoK, Gilgit-Baltistan and Aksai Chin; Ladakh is drawn inside J&K in the state file).

## The whole page

![Dashboard, full page](screenshot_full.jpg)

