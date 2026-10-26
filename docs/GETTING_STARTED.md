# Getting started

[Prism MCP](../README.md) · [Use cases](use-cases/README.md) · [API index](https://radar-api.fliarbi.com/prism/v1)

## 1. Check the server

```bash
systemctl --user status prism-mcp          # the unit in deploy/prism-mcp.service
curl -s http://127.0.0.1:8790/livez        # {"ok": true, "service": "prism", "features": 63}
curl -s http://127.0.0.1:8790/healthz      # strict index partition reads + row floors for all 8 corpora
curl -s http://127.0.0.1:8790/v1/system.freshness | jq .data   # where the news window ends and why
```

Install or restore the unit:

```bash
cp deploy/prism-mcp.service ~/.config/systemd/user/
systemctl --user daemon-reload && systemctl --user enable --now prism-mcp
```

`/healthz` returns `ok: false` when any corpus is short of its row floor. `/readyz` also probes every
article-store node: when a node is down, headlines from that node come back as `unresolved` and are
counted, never dropped silently.

## 2. Connect a client

| Client | How |
| --- | --- |
| Claude Code | `claude mcp add prism -- /usr/bin/python3 prism_mcp.py` |
| Claude Desktop / Cursor / VS Code | `mcpServers.prism` = `{"command": "/usr/bin/python3", "args": ["prism_mcp.py"]}` |
| Codex CLI | `[mcp_servers.prism]` with `command`, `args`, `tool_timeout_sec = 600`, `default_tools_approval_mode = "approve"` |
| ChatGPT connector, remote agents | streamable HTTP at `http://<host>:8790/mcp` |
| n8n, Zapier, custom GPT actions | import `http://<host>:8790/v1/openapi.json` |
| Python | `import prism_mcp; prism_mcp.REGISTRY["news_trends"]["fn"](term="...")` |

Long tools (evidence reading, briefs, audits, tables) can take 30 s to several minutes cold, and return in
under a second from the 12-hour cache. Give MCP clients a tool timeout of at least 300 s.

Some clients stop waiting before a slow call returns. In the showcase's live sessions the Codex CLI
(ChatGPT) ended its turn while `search_research` was still running under heavy cluster load. For those
clients use the asynchronous pair: `system.request` (`submit_request`, returns a `request_id` at once)
and `system.request_status` (poll it, passing `next_cursor` as `after`), which streams plain-language
progress and then the final envelope.

## 3. First five calls

```bash
P=http://127.0.0.1:8790/v1
curl -s "$P/system.status"                                   | jq '.data.corpora | map_values(.rows)'
curl -s -X POST $P/news.overview -H 'content-type: application/json' -d '{"term":"ozempic"}'   | jq '.data.profile'
curl -s -X POST $P/news.compare  -H 'content-type: application/json' -d '{"terms":["tesla","byd"]}' | jq '.data.rows[] | {term,articles,growth}'
curl -s -X POST $P/research.evidence -H 'content-type: application/json' -d '{"claim":"Exercise reduces depression symptoms"}' | jq '.data.tally'
curl -s -X POST $P/research.stance_trends -H 'content-type: application/json' -d '{"term":"mindfulness"}' | jq '.data.points[] | {year,positive_pct,contested_pct}'
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
            "coverage": { "partial": false, "note": "all listed tables passed strict index partition reads and historical row floors" },
            "seconds": 100.9 }
}
```

`ok: false` is a normal answer. `error.kind` is one of `no_data`, `not_resolvable`, `bad_request`,
`upstream` or `internal` (HTTP 404, 404, 400, 502 and 500), and `error.reason` says what to change.
