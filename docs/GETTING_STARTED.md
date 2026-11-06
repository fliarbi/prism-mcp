# Getting started

[Prism MCP](../README.md) · [Use cases](use-cases/README.md) · [Data export](DATA_EXPORT.md)

## 1. Get a key and the `prism` command

```bash
curl -fsSL https://radar-api.fliarbi.com/prism/install.sh | bash      # installs the `prism` command, no sudo
prism login                                                          # paste your rdr_ key
prism compare "narendra modi" "donald trump"
```

Create the key in the [Fliar dashboard](https://fliarbi.com/radar/dashboard?tab=radarapi) (**API keys**). One key works
on Prism, the [Radar API](https://github.com/fliarbi/radar-api-mcp) and the Prism News APIs, and one prepaid wallet
pays for all of them.

**Live.** Base URL `https://radar-api.fliarbi.com/prism` · MCP `https://radar-api.fliarbi.com/prism/mcp`

## 2. Connect an assistant

| Client | How |
| --- | --- |
| Claude Code | `claude mcp add --transport http prism https://radar-api.fliarbi.com/prism/mcp --header "Authorization: Bearer rdr_…"` |
| Claude Desktop, Cursor, VS Code, Codex | add an HTTP MCP server at `https://radar-api.fliarbi.com/prism/mcp` with the header `Authorization: Bearer rdr_…` |
| ChatGPT connectors, n8n, Zapier | point them at `https://radar-api.fliarbi.com/prism/mcp` (streamable HTTP) |

Deep tools (reading the evidence, briefs, audits, research tables) can take a few minutes on a new question. Let your
client wait for them. If your client stops waiting early, use the asynchronous pair: `submit_request` returns a
`request_id` at once, and `request_status` reports plain-language progress and then the finished answer.

## 3. First calls over REST

```bash
curl -s -X POST "https://radar-api.fliarbi.com/prism/v1/news.overview" -H "Authorization: Bearer rdr_…" \
  -H 'content-type: application/json' -d '{"term":"ozempic"}' | jq '.data.profile'
curl -s -X POST "https://radar-api.fliarbi.com/prism/v1/news.compare" -H "Authorization: Bearer rdr_…" \
  -H 'content-type: application/json' -d '{"terms":["tesla","byd"]}' | jq '.data.rows[] | {term,articles,growth}'
curl -s -X POST "https://radar-api.fliarbi.com/prism/v1/research.evidence" -H "Authorization: Bearer rdr_…" \
  -H 'content-type: application/json' -d '{"claim":"Exercise reduces depression symptoms"}' | jq '.data.tally'
curl -s -X POST "https://radar-api.fliarbi.com/prism/v1/research.stance_trends" -H "Authorization: Bearer rdr_…" \
  -H 'content-type: application/json' -d '{"term":"mindfulness"}' | jq '.data.points[] | {year,positive_pct,contested_pct}'
```

## 4. Questions that work well

* **One mechanism per claim.** "Coffee lowers blood pressure", not "coffee is good for your heart, skin and mood".
* **Short subjects for news.** `"ozempic"`, `"red sea shipping"`, `"ai regulation"`. Prism matches a subject as a named
  thing or as what an article is centrally about; a whole sentence matches less.
* **Name the window when it matters.** `since="2024-06-01"`. By default the news window ends at the latest complete
  period (currently 1 June 2026), so a series never ends in a half-counted month.
* **Ask for the dissent.** "...and what disagrees" makes the assistant call `find_counter_evidence`.
* **Ask for a file.** "...and save it as CSV" (see [Data export](DATA_EXPORT.md)).

## 5. Reading a response

```json
{
  "ok": true,
  "feature": "research.evidence",
  "data": { "volumes": {...}, "corpus_stance": {...}, "documents": [...], "tally": {...} },
  "window": { "corpora": { "research": "2017-2025", "news": "2019-01-01..2026-06-01" } },
  "meta": { "lane": "intersection", "lane_note": "334 papers cover both sides of the claim, out of 86,957 on the subject...",
            "coverage": { "partial": false, "note": "all data was available for this answer" } }
}
```

* `window` is the period every number was counted over. Cite it with the numbers.
* `meta.lane` says whether the numbers describe the claim (both sides of it) or only its subject.
* `meta.coverage.partial` is `true` when some data was unavailable; treat counts from such an answer as a lower bound.

`ok: false` is a normal answer. `error.kind` `no_data`, `not_resolvable` or `bad_request` (HTTP 404, 404 and 400) comes
with an `error.reason` that says what to change; a 5xx answer means try again later.
