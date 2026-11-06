# Getting started

[Prism MCP](../README.md) · [Use cases](use-cases/README.md) · [API index](https://radar-api.fliarbi.com/prism/v1)

## 1. Get a key and install

1. [Fliar dashboard](https://fliarbi.com/radar/dashboard?tab=radarapi) → **API keys** → create a key with **All data** access, and buy prepaid credits on the same page.
2. Install the `prism` command and save your key:

```bash
curl -fsSL https://radar-api.fliarbi.com/prism/install.sh | bash   # installs to ~/.local/bin, sets PRISM_URL
prism login                                                       # paste your rdr_ key (or export FLIAR_API_KEY)
curl -s https://radar-api.fliarbi.com/prism/livez                 # {"ok": true, ...}
```

## 2. Connect a client

| Client | How |
| --- | --- |
| Claude Code | `prism mcp claude`, or `claude mcp add --transport http prism "$PRISM_URL/mcp" --header "Authorization: Bearer $FLIAR_API_KEY"` |
| Claude Desktop / Cursor / VS Code | an HTTP MCP server at `$PRISM_URL/mcp` with the header `Authorization: Bearer $FLIAR_API_KEY` |
| Codex CLI | `prism mcp codex` prints it: `[mcp_servers.prism]` with `url = "https://radar-api.fliarbi.com/prism/mcp"`, `bearer_token_env_var = "FLIAR_API_KEY"`, `tool_timeout_sec = 600` |
| ChatGPT connector, remote agents | streamable HTTP at `$PRISM_URL/mcp` (bearer auth) |
| n8n, Zapier, custom GPT actions | import `$PRISM_URL/v1/openapi.json` (bearer auth) |
| Terminal | `prism entity "tata motors"`, `prism evidence "..."`, `prism call <feature> key=value` |

Long tools (evidence reading, briefs, audits, tables) can take 30 s to several minutes cold, and return in
under a second from the 12-hour cache. Give MCP clients a tool timeout of at least 300 s.

Some clients stop waiting before a slow call returns. In the showcase's live sessions the Codex CLI
(ChatGPT) ended its turn while `search_research` was still running under heavy load. For those
clients use the asynchronous pair: `system.request` (`submit_request`, returns a `request_id` at once)
and `system.request_status` (poll it, passing `next_cursor` as `after`), which streams plain-language
progress and then the final envelope.

## 3. First five calls

```bash
P=$PRISM_URL/v1; A="Authorization: Bearer $FLIAR_API_KEY"
curl -s -H "$A" "$P/system.status"                                   | jq '.data.corpora | map_values(.rows)'
curl -s -H "$A" -X POST $P/news.overview -H 'content-type: application/json' -d '{"term":"ozempic"}'   | jq '.data.profile'
curl -s -H "$A" -X POST $P/news.compare  -H 'content-type: application/json' -d '{"terms":["tesla","byd"]}' | jq '.data.rows[] | {term,articles,growth}'
curl -s -H "$A" -X POST $P/research.evidence -H 'content-type: application/json' -d '{"claim":"Exercise reduces depression symptoms"}' | jq '.data.tally'
curl -s -H "$A" -X POST $P/research.stance_trends -H 'content-type: application/json' -d '{"term":"mindfulness"}' | jq '.data.points[] | {year,positive_pct,contested_pct}'
```

## 4. Prompts that work well

* **One mechanism per claim.** "Coffee lowers blood pressure", not "coffee is good for your heart, skin and mood".
* **Short subjects for news.** `"ozempic"`, `"red sea shipping"`, `"ai regulation"`. The resolver matches entities and
  central mentions; a sentence matches less.
* **Name the window when it matters.** `since="2024-06-01"`. The default ends at 1 June 2026 because news ingest lags.
* **Ask for the dissent.** "...and what disagrees" makes the assistant call `research.counter_evidence`.
* **Ask for a file.** "...and save it as CSV" (see [Data export](DATA_EXPORT.md)).

## 5. Reading a response

```json
{
  "ok": true,
  "feature": "research.evidence",
  "data": { "volumes": {...}, "corpus_stance": {...}, "documents": [...], "tally": {...} },
  "window": { "corpora": { "research": "2017-2025", "news": "2019-01-01..2026-06-01" } },
  "meta": { "lane": "intersection", "lane_note": "334 papers cover both sides of the claim, out of 86,957 on the subject...",
            "coverage": { "partial": false, "note": "the whole index answered" },
            "seconds": 100.9 }
}
```

`ok: false` is a normal answer. `error.kind` is one of `no_data`, `not_resolvable`, `bad_request`,
`upstream` or `internal` (HTTP 404, 404, 400, 502 and 500), and `error.reason` says what to change.
