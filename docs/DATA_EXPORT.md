# Data export

[Prism MCP](../README.md) · [Research analysis](RESEARCH_ANALYSIS.md) · [Use cases](use-cases/README.md)

Every Prism feature returns one envelope:

```json
{"ok": true, "feature": "news.compare", "subject": {...}, "data": {...},
 "window": {"from": "2024-06-01", "to": "2026-06-01", "to_is_exclusive": true, "censored_at": "2026-06-01"},
 "meta": {"coverage": {"partial": false, "note": "all data was available for this answer"}}}
```

The tables sit inside `data`, and the window and coverage you need to cite the numbers sit beside them. Keep the
window with the numbers when you save them: a spreadsheet should still say what it is and when it was counted.

## Sample exports

Real exports are in [`exports/`](exports/): one CSV per table, plus a `provenance.json` with the feature, the
arguments, the window and the coverage. For example:

`exports/tesla-vs-byd/compare_terms/summary.csv`
```csv
term,articles,share_pct,critical,direction,growth,tone_ratio,vs_baseline
tesla,215756,81.8,137701,flat,0.89,0.83,1.43
byd,47974,18.2,26323,rising,1.42,0.39,0.67
```

`exports/metformin-cancer-risk/find_statistics/figures.csv` (first row)
```csv
value,measures,population,...,source.title,source.year,source.tier,source.url
"0.90 (95% confidence interval, 0.73-1.10)",hazard ratio for cancer incidence,participants in Diabetes Prevention Program,...,"Randomized Study of Metformin and Intensive Lifestyle Intervention on Cancer Incidence over 21 Years...",2025,trial,https://doi.org/10.1158/1940-6207.CAPR-23-0461
```

| Feature | Tables in the response |
| --- | --- |
| `news.overview` | monthly, tone, places, subcategories, organizations, people, publishers, critical_articles |
| `news.compare` | summary (one row per term), monthly (term × month) |
| `news.trends`, `news.sentiment`, `news.geography`, `news.sources` | the series or ranking |
| `news.recent`, `news.critical` | articles: date, headline, publisher, URL, priority, tone |
| `research.evidence` | documents: year, title, venue, tier, stance, verbatim quote, DOI |
| `research.counter_evidence` | against, for |
| `research.statistics` | figures, research_per_year, news_per_month |
| `research.browse`, `research.stance_trends` | papers; by_year |
| `research.table` | one row per input row: value, measures, papers, top source |
| `research.citations` | citations in APA, Vancouver, BibTeX and more |
| `analysis.history`, `analysis.scenarios` | series; scenarios with sensitivity bounds |

## Straight from the API with `jq`

```bash
curl -s -X POST "https://radar-api.fliarbi.com/prism/v1/news.trends" -H "Authorization: Bearer rdr_…" \
  -H 'content-type: application/json' -d '{"term":"gold price","since":"2024-06-01"}' \
  | jq -r '.data.points[] | [.period,.articles,.critical,.negative,.positive] | @csv' > gold.csv
```

Check `meta.coverage.partial` before you save anything. When some data is unavailable, counts come back
*smaller*, not as an error, and `partial` is `true`.

## From an assistant

Ask in plain language and let the assistant call the tools and write the file:

> *"Using Prism, compare news coverage of Netflix, Disney+ and Prime Video since June 2024 and save the
> monthly series as a CSV with a note on the window."*

An assistant that can write files saves the CSV itself. In a chat client, ask for the table in the reply and paste it
into a sheet.
