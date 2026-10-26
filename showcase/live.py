"""Flagship runs: Claude and ChatGPT connected to the Prism MCP server, choosing their own calls.

Unlike compare.py (which hands both models the same captured tool results), here each
model gets only the question and a live MCP connection, and the transcript records
which Prism tools it called, with what arguments, and how long each took.

    python3 showcase/live.py [--only a,b] [--workers 2]

Writes docs/comparisons/live/<slug>.json.
"""
import argparse
import json
import os
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "showcase"))
from scenarios import BY_SLUG  # noqa: E402
from compare import SCRATCH, TODAY, PY, CLAUDE_MODEL, CHATGPT_MODEL, save  # noqa: E402

OUT = os.path.join(ROOT, "docs", "live_sessions")

FLAGSHIPS = ["metformin-cancer-risk", "glp1-weight-loss-muscle", "measles-outbreak-pulse", "gold-price-pulse",
             "nvidia-pulse", "ai-regulation-pulse", "digital-arrest-scam", "drone-warfare-pulse",
             "green-hydrogen-radar", "gen-ai-education-stance", "red-sea-shipping", "audit-coffee-draft",
             "ev-battery-table", "minimum-wage-employment"]

PROMPT = ("Today is {today}. You are connected to Prism, a research and news intelligence MCP server. "
          "Use its tools to answer, choosing whichever tools fit.\n\nQuestion: {q}\n\n"
          "Answer as a senior analyst in at most 280 words, lead with the direct answer, give numbers with "
          "their time window and source, and separate what the data shows from your interpretation.")

MCP = {"mcpServers": {"prism": {"type": "stdio", "command": PY, "args": [f"{ROOT}/prism_mcp.py"]}}}


def claude_live(q):
    cmd = ["claude", "-p", "--model", CLAUDE_MODEL, "--no-session-persistence", "--setting-sources", "",
           "--system-prompt", f"You are Claude, an AI assistant made by Anthropic. Today's date is {TODAY}.",
           "--output-format", "stream-json", "--verbose", "--strict-mcp-config", "--mcp-config", json.dumps(MCP),
           "--allowedTools", "mcp__prism", "--tools", ""]
    t0 = time.time()
    r = subprocess.run(cmd, input=PROMPT.format(today=TODAY, q=q), capture_output=True, text=True,
                       timeout=2400, cwd=SCRATCH)
    calls, text, pending = [], "", {}
    for line in r.stdout.splitlines():
        try:
            ev = json.loads(line)
        except Exception:
            continue
        if ev.get("type") == "assistant":
            for c in ev["message"].get("content", []):
                if c.get("type") == "tool_use":
                    pending[c["id"]] = {"tool": c["name"].replace("mcp__prism__", ""), "args": c.get("input"),
                                        "t": time.time()}
                    calls.append(pending[c["id"]])
        elif ev.get("type") == "user":
            for c in ev["message"].get("content", []):
                if isinstance(c, dict) and c.get("type") == "tool_result" and c.get("tool_use_id") in pending:
                    body = c.get("content")
                    body = body if isinstance(body, str) else json.dumps(body)
                    pending[c["tool_use_id"]]["ok"] = '"ok":true' in body.replace(" ", "")[:200]
                    pending[c["tool_use_id"]]["chars"] = len(body)
        elif ev.get("type") == "result":
            text = ev.get("result", "")
    for c in calls:
        c.pop("t", None)
    if not text:
        raise RuntimeError(f"claude live failed: {r.stderr[-300:]}")
    return {"text": text.strip(), "seconds": round(time.time() - t0, 1), "model": f"claude-{CLAUDE_MODEL}",
            "tool_calls": calls}


def chatgpt_live(q):
    out = os.path.join(SCRATCH, f"live_{os.getpid()}_{int(time.time()*1000)}.txt")
    cmd = ["codex", "exec", "--json", "--ignore-user-config", "-m", CHATGPT_MODEL, "-c", "model_reasoning_effort=medium",
           "-s", "read-only", "--skip-git-repo-check", "--ephemeral",
           "-c", f'mcp_servers.prism.command="{PY}"', "-c", f'mcp_servers.prism.args=["{ROOT}/prism_mcp.py"]',
           "-c", "mcp_servers.prism.tool_timeout_sec=900", "-c", "mcp_servers.prism.startup_timeout_sec=90",
           "-c", 'mcp_servers.prism.default_tools_approval_mode="approve"', "-o", out, "-"]
    t0 = time.time()
    r = subprocess.run(cmd, input=PROMPT.format(today=TODAY, q=q), capture_output=True, text=True,
                       timeout=2400, cwd=SCRATCH)
    calls, started = [], {}
    for line in r.stdout.splitlines():
        try:
            ev = json.loads(line)
        except Exception:
            continue
        it = ev.get("item") or {}
        if ev.get("type") == "item.started" and it.get("type") == "mcp_tool_call":
            started[it.get("id")] = {"tool": it.get("tool"), "args": it.get("arguments")}
        if ev.get("type") == "item.completed" and it.get("type") == "mcp_tool_call":
            started.pop(it.get("id"), None)
            res = it.get("result") or {}
            body = json.dumps(res)
            calls.append({"tool": it.get("tool"), "args": it.get("arguments"),
                          "ok": bool(res) and not it.get("error") and '\\"ok\\": true' in body[:400],
                          "chars": len(body)})
    # Codex can end its turn while a slow MCP call is still running; record
    # those calls as unreturned rather than pretending none were made.
    calls += [{**c, "ok": False, "returned": False} for c in started.values()]
    text = open(out).read().strip() if os.path.exists(out) else ""
    if os.path.exists(out):
        os.remove(out)
    if not text:
        raise RuntimeError(f"codex live failed: {r.stderr[-300:]}")
    return {"text": text, "seconds": round(time.time() - t0, 1), "model": CHATGPT_MODEL, "tool_calls": calls}


def run(slug, force=False):
    path = os.path.join(OUT, f"{slug}.json")
    rec = json.load(open(path)) if os.path.exists(path) else {"slug": slug}
    q = BY_SLUG[slug]["question"]
    with ThreadPoolExecutor(2) as ex:
        fs = {}
        if force or "claude_live" not in rec:
            fs["claude_live"] = ex.submit(claude_live, q)
        if force or "chatgpt_live" not in rec:
            fs["chatgpt_live"] = ex.submit(chatgpt_live, q)
        for k, f in fs.items():
            try:
                rec[k] = f.result()
            except Exception as e:
                print(f"  {slug} {k}: {e}", flush=True)
    # A session with zero tool calls usually means the MCP server did not start
    # in time under load, and the model answered from memory. That is not a
    # live MCP demonstration: retry once, then label it rather than show it as one.
    for k, fn in (("claude_live", claude_live), ("chatgpt_live", chatgpt_live)):
        if k in rec and not rec[k].get("tool_calls"):
            try:
                again = fn(q)
                rec[k] = again if again.get("tool_calls") else {**rec[k], "no_tool_calls": True}
            except Exception as e:
                print(f"  {slug} {k} retry: {e}", flush=True)
                rec[k]["no_tool_calls"] = True
    os.makedirs(OUT, exist_ok=True)
    save(path, rec)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    os.makedirs(SCRATCH, exist_ok=True)
    slugs = [x for x in a.only.split(",") if x] or FLAGSHIPS

    def go(s):
        t0 = time.time()
        r = run(s, a.force)
        print(f"ok {s} {time.time()-t0:.0f}s claude={len((r.get('claude_live') or {}).get('tool_calls', []))} "
              f"chatgpt={len((r.get('chatgpt_live') or {}).get('tool_calls', []))}", flush=True)

    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(go, slugs))


if __name__ == "__main__":
    main()
