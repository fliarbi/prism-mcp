# Data export

[Prism MCP](../README.md) · [Research analysis](RESEARCH_ANALYSIS.md) · [Use cases](use-cases/README.md)

Every Prism feature returns one envelope:

```json
{"ok": true, "feature": "news.compare", "subject": {...}, "data": {...},
 "window": {"from": "2024-06-01", "to": "2026-06-01", "to_is_exclusive": true, "censored_at": "2026-06-01"},
 "meta": {"coverage": {"partial": false, "note": "all corpora fully available"}, "seconds": 46.7}}
```

The tables sit inside `data`, and the window and coverage you need to cite the numbers sit beside them.
There are three ways to get the data out.

## 1. `tools/prism_export.py`: any response to CSV, Excel, JSONL or BibTeX

It knows where the rows are in each feature, flattens them, and writes a **provenance sidecar**
(feature, arguments, window, coverage, export time) next to the data. A spreadsheet then still says
what it is and when it was counted.

```bash
# live call, one CSV per table
python3 tools/prism_export.py news.compare --arg terms='["tesla","byd"]' --arg since=2024-06-01 -o exports/tesla_byd/

# one Excel workbook, one sheet per table + a provenance sheet (needs openpyxl)
python3 tools/prism_export.py news.overview --arg term=ozempic -o exports/ozempic.xlsx

# evidence table with verbatim quotes, DOIs and study tiers
python3 tools/prism_export.py research.evidence --arg claim="Metformin reduces cancer risk in diabetic patients" -o exports/metformin.csv

# a bibliography
python3 tools/prism_export.py research.citations --arg claim="Exercise reduces depression symptoms" --arg style=bibtex -o refs.bib

# re-export a saved response or a whole showcase capture, no server needed
python3 tools/prism_export.py --from docs/examples/ozempic-news-pulse.json -o exports/ozempic/
```

Real exports made this way are in [`exports/`](exports/), for example:

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

| Feature | Tables exported |
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
| `research.citations` | citations (or `.bib`) |
| `analysis.history`, `analysis.scenarios` | series; scenarios with sensitivity bounds |

## 2. Straight from the API with `jq` or pandas

```bash
curl -s -X POST "$PRISM_URL/v1/news.trends" -H 'content-type: application/json' \
  -d '{"term":"gold price","since":"2024-06-01"}' \
  | jq -r '.data.points[] | [.period,.articles,.critical,.negative,.positive] | @csv' > gold.csv
```

```python
import pandas as pd, requests
env = requests.post(f"{URL}/v1/news.compare", json={"terms": ["inflation", "recession", "interest rates"]}).json()
assert env["ok"] and not env["meta"]["coverage"]["partial"], env.get("error") or env["meta"]["coverage"]
monthly = pd.DataFrame([{"term": r["term"], **p} for r in env["data"]["rows"] for p in r["points"]])
monthly.pivot(index="period", columns="term", values="articles").to_csv("macro_attention.csv")
```

Check `meta.coverage.partial` before you save anything. During an index partition outage counts come back
*smaller*, not as an error.

## 3. From an assistant

Ask in plain language and let the model call the tools and write the file:

> *"Using Prism, compare news coverage of Netflix, Disney+ and Prime Video since June 2024 and save the
> monthly series as a CSV with a note on the window."*

Claude Code and Codex can run `tools/prism_export.py` themselves. In a chat client, ask for the table in
the reply and paste it into a sheet.

## Bulk export

Loop over subjects with the same feature and keep the provenance per file:

```bash
for t in "solar power" "green hydrogen" "carbon capture" "nuclear power"; do
  python3 tools/prism_export.py news.overview --arg term="$t" --arg since=2024-06-01 -o "exports/energy/${t// /_}/"
done
```

Prism caches every response for 12 hours (`PRISM_CACHE_TTL`), so re-running an export is instant and
returns the same numbers. Set `PRISM_CACHE=0` to force a fresh count.
