"""Ask Claude and ChatGPT each scenario's question, with and without Prism, then judge.

Four answers per scenario:
    claude_bare     Claude (claude -p, Sonnet), no tools, no web, no memory
    chatgpt_bare    ChatGPT (codex exec, GPT-6, ChatGPT account), told not to run commands
    claude_prism    Claude given the Prism tool results for the scenario
    chatgpt_prism   ChatGPT given the same Prism tool results

The tool results are the captured responses in docs/examples/<slug>.json, compacted
the same way for both models (digest()). `--live-mcp` instead connects each CLI to
the Prism MCP server and lets the model choose its own calls; that is what the
flagship pages show.

A blind judge (Claude Opus) scores the four answers on five criteria. The judge is
given the Prism record as reference data and told to penalise only contradictions
with it, not omissions. Where the Prism answers do not beat the bare ones, the
judge says why, and that lands in docs/ENGINEERING_FLAGS.md.

    python3 showcase/compare.py [--only a,b] [--workers 3] [--stage answers|judge|all]
"""
import argparse
import json
import os
import random
import re
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "showcase"))
from scenarios import BY_SLUG, SCENARIOS  # noqa: E402

EX = os.path.join(ROOT, "docs", "examples")
CMP = os.path.join(ROOT, "docs", "comparisons")
SCRATCH = os.environ.get("PRISM_SHOWCASE_SCRATCH", "/tmp/prism-showcase-empty")
TODAY = "2026-10-22"
PY = "/usr/bin/python3"

CLAUDE_MODEL = "sonnet"
JUDGE_MODEL = "opus"
CHATGPT_MODEL = "gpt-6-luna"

DROP = {"coverage", "sql", "how", "type_evidence", "fill_rates", "provenance", "checked_at",
        "expires_in_seconds", "strict_shard_read", "completeness", "queue_seconds", "execution_seconds",
        "target_id", "partition", "institutions", "claimed_quote", "tier_rank", "match_mode_note"}


def compact(o, depth=0, list_cap=8):
    if isinstance(o, dict):
        out = {}
        for k, v in o.items():
            if k in DROP or v in (None, "", [], {}):
                continue
            cap = 30 if k in ("points", "series") else list_cap
            out[k] = compact(v, depth + 1, cap)
        return out
    if isinstance(o, list):
        return [compact(x, depth + 1, list_cap) for x in o[:list_cap]]
    if isinstance(o, str):
        return o if len(o) <= 360 else o[:360] + "…"
    if isinstance(o, float):
        return round(o, 3)
    return o


def slim_overview(data: dict) -> dict:
    """news.overview carries eight panels (~32k chars compacted). Cutting it at a
    character budget dropped geography, sources and headlines, so the models
    never saw them. Keep every panel; drop only fields another panel repeats."""
    if not isinstance(data, dict) or "trends" not in data:
        return data
    keep = lambda rows, cols, n: [{c: r.get(c) for c in cols if r.get(c) is not None} for r in (rows or [])[:n]]
    tr, se, th, en = (data.get(k) or {} for k in ("trends", "sentiment", "themes", "entities"))
    return {
        "profile": {k: (data.get("profile") or {}).get(k) for k in ("term", "type", "articles", "critical_articles", "first_seen", "last_seen")},
        "monthly": keep(tr.get("points"), ("period", "articles", "critical", "negative", "positive"), 30),
        "trend": tr.get("trend"), "critical_trend": tr.get("critical_trend"),
        "tone": {k: se.get(k) for k in ("totals", "corpus_baseline_ratio", "vs_baseline", "reading")},
        "categories": keep((th.get("categories") or {}).get("rows"), ("label", "share_pct", "lift"), 8),
        "subcategories": keep((th.get("subcategories") or {}).get("rows"), ("label", "articles", "lift"), 10),
        "organizations": keep((en.get("organizations") or {}).get("rows"), ("label", "articles", "share_pct"), 8),
        "people": keep((en.get("people") or {}).get("rows"), ("label", "articles", "share_pct"), 8),
        "places": keep((en.get("places") or {}).get("rows"), ("label", "articles"), 6),
        "geography": {**{k: (data.get("geography") or {}).get(k) for k in ("placed_pct", "caveat")},
                      "rows": keep((data.get("geography") or {}).get("rows"), ("label", "articles", "share_pct", "lift"), 12)},
        "publishers": {**{k: (data.get("sources") or {}).get(k) for k in ("sampled_articles", "concentration")},
                       "rows": keep((data.get("sources") or {}).get("publishers"), ("publisher", "share_pct"), 10)},
        "critical_headlines": [{**{c: a.get(c) for c in ("published", "title", "publisher", "priority", "tone", "url")},
                                "excerpt": (a.get("excerpt") or "")[:180]}
                               for a in ((data.get("critical") or {}).get("articles") or [])[:8]],
        "recent_headlines": [{c: a.get(c) for c in ("published", "title", "publisher")}
                             for a in ((data.get("recent") or {}).get("articles") or [])[:5]],
    }


def digest(slug: str, budget: int = 20000) -> str:
    d = json.load(open(os.path.join(EX, f"{slug}.json")))
    parts = []
    per = budget // max(1, len(d["calls"]))
    for c in d["calls"]:
        r = dict(c["response"] or {})
        if c["tool"] == "prism_overview":
            r["data"] = slim_overview(r.get("data") or {})
        body = {"ok": r.get("ok"), "data": r.get("data"), "error": r.get("error"),
                "window": r.get("window"), "meta_note": (r.get("meta") or {}).get("lane_note")}
        txt = json.dumps(compact(body), ensure_ascii=False, separators=(",", ":"))
        if len(txt) > per:
            txt = json.dumps(compact(body, list_cap=4), ensure_ascii=False, separators=(",", ":"))[:per] + "…(truncated)"
        parts.append(f"### tool {c['tool']}  args={json.dumps(c['args'], ensure_ascii=False)}\n{txt}")
    return "\n\n".join(parts)


ANSWER_RULES = ("Answer as a senior analyst in at most 280 words. Lead with the direct answer, then the "
                "evidence. Give specific numbers, dates and named sources wherever you can, and say plainly "
                "where you are uncertain or where your knowledge may be out of date.")


def prompt_bare(s):
    return (f"Today is {TODAY}.\n\nQuestion: {s['question']}\n\n{ANSWER_RULES}\n"
            "Answer from your own knowledge only. Do not run any commands or tools and do not browse.")


def prompt_prism(s):
    return (f"Today is {TODAY}.\n\nQuestion: {s['question']}\n\n"
            "You called tools on the Prism MCP server (a research and news intelligence layer over 255M news "
            "articles, 401M research works, 41M PubMed records, 108M patents and 55M disease-factor claims). "
            "Their results are below. Every count and quote in them comes from the corpus, not a model. "
            "Use them as your primary evidence, keep their time window and caveats, and separate what the "
            "data shows from your own interpretation. You may add background knowledge, labelled as such.\n\n"
            f"{ANSWER_RULES} Do not run any commands.\n\n=== PRISM TOOL RESULTS ===\n{digest(s['slug'])}")


def run_claude(prompt, model=CLAUDE_MODEL, mcp=None, timeout=900):
    os.makedirs(SCRATCH, exist_ok=True)
    cmd = ["claude", "-p", "--model", model, "--no-session-persistence", "--setting-sources", "",
           "--system-prompt", f"You are Claude, an AI assistant made by Anthropic. Today's date is {TODAY}.",
           "--output-format", "json"]
    if mcp:
        cmd += ["--strict-mcp-config", "--mcp-config", json.dumps(mcp), "--allowedTools", "mcp__prism",
                "--tools", ""]
    else:
        cmd += ["--strict-mcp-config", "--mcp-config", '{"mcpServers":{}}', "--tools", ""]
    t0 = time.time()
    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout, cwd=SCRATCH)
    try:
        j = json.loads(r.stdout)
        text = j.get("result", "")
    except Exception:
        text = ""
    if not text:
        raise RuntimeError(f"claude failed rc={r.returncode}: {r.stdout[-300:]} {r.stderr[-300:]}")
    return {"text": text.strip(), "seconds": round(time.time() - t0, 1), "model": f"claude-{model}"}


def run_chatgpt(prompt, mcp=False, timeout=1200):
    os.makedirs(SCRATCH, exist_ok=True)
    out = os.path.join(SCRATCH, f"cx_{os.getpid()}_{random.randint(0, 1 << 30)}.txt")
    cmd = ["codex", "exec", "--ignore-user-config", "-m", CHATGPT_MODEL, "-c", "model_reasoning_effort=medium",
           "-s", "read-only", "--skip-git-repo-check", "--ephemeral", "-o", out]
    if mcp:
        cmd += ["-c", f'mcp_servers.prism.command="{PY}"',
                "-c", f'mcp_servers.prism.args=["{ROOT}/prism_mcp.py"]',
                "-c", "mcp_servers.prism.tool_timeout_sec=600",
                "-c", "mcp_servers.prism.startup_timeout_sec=60",
                "-c", 'mcp_servers.prism.default_tools_approval_mode="approve"']
    cmd.append("-")
    t0 = time.time()
    r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout, cwd=SCRATCH)
    text = open(out).read().strip() if os.path.exists(out) else ""
    if os.path.exists(out):
        os.remove(out)
    if not text:
        raise RuntimeError(f"codex failed rc={r.returncode}: {r.stderr[-400:]}")
    tools = re.findall(r"tool (prism\.\w+)", r.stderr) if mcp else []
    return {"text": text, "seconds": round(time.time() - t0, 1), "model": CHATGPT_MODEL, "tool_calls": tools}


def answers(slug, force=False):
    s = BY_SLUG[slug]
    path = os.path.join(CMP, f"{slug}.json")
    rec = json.load(open(path)) if os.path.exists(path) else {"slug": slug}
    jobs = {"claude_bare": lambda: run_claude(prompt_bare(s)),
            "chatgpt_bare": lambda: run_chatgpt(prompt_bare(s)),
            "claude_prism": lambda: run_claude(prompt_prism(s)),
            "chatgpt_prism": lambda: run_chatgpt(prompt_prism(s))}
    todo = {k: f for k, f in jobs.items() if force or k not in rec}
    with ThreadPoolExecutor(4) as ex:
        futs = {k: ex.submit(f) for k, f in todo.items()}
        for k, fu in futs.items():
            try:
                rec[k] = fu.result()
            except Exception as e:
                print(f"  {slug} {k} failed: {e}", flush=True)
    rec.pop("judge", None) if todo else None
    save(path, rec)
    return rec


JUDGE = """You are judging four answers to the same research question, for a public benchmark.
Today is {today}. The answers are labelled A-D in random order. Some had access to a research database
and some answered from memory; do not guess which is which.

QUESTION: {question}
WHY IT IS HARD: {special}

REFERENCE RECORD (query results from the research and news database, for checking facts; an answer is NOT
penalised for omitting things in it, only for contradicting it or for stating specific facts that look
fabricated or out of date):
{reference}

{answers}

Score each answer 1-5 on:
- specificity: concrete numbers, dates, named sources rather than generalities
- verifiability: could a reader check the claims (named studies, DOIs, URLs, publishers, counts with windows)?
- currency: does it reflect what is known as of {today}, and say when its knowledge may be stale?
- calibration: does it state uncertainty, disagreement and limits honestly?
- accuracy: no contradictions with the reference, no fabricated-looking specifics (5 = none)

Then: name the best answer, list any specific fabricated or wrong claims per answer (short), and say in one
or two sentences whether the database-backed evidence in the reference materially improves on what a model
knows from memory for THIS question. If the reference record is thin, off-topic, empty or misleading, say
exactly how (this is used to fix the database tools).

Return ONLY JSON:
{{"scores": {{"A": {{"specificity":n,"verifiability":n,"currency":n,"calibration":n,"accuracy":n}}, "B": {{...}}, "C": {{...}}, "D": {{...}}}},
 "best": "A|B|C|D", "errors": {{"A": [..], "B": [..], "C": [..], "D": [..]}},
 "reference_quality": "strong|adequate|thin|off_topic|empty",
 "reference_problem": "what is wrong with the reference record, or empty string",
 "verdict": "one or two sentences"}}"""


def judge(slug, force=False):
    s = BY_SLUG[slug]
    path = os.path.join(CMP, f"{slug}.json")
    rec = json.load(open(path))
    keys = ["claude_bare", "chatgpt_bare", "claude_prism", "chatgpt_prism"]
    if any(k not in rec for k in keys) or ("judge" in rec and not force):
        return rec
    order = keys[:]
    random.Random(slug).shuffle(order)
    labels = dict(zip("ABCD", order))
    ans = "\n\n".join(f"=== ANSWER {l} ===\n{rec[k]['text']}" for l, k in labels.items())
    p = JUDGE.format(today=TODAY, question=s["question"], special=s["special"],
                     reference=digest(slug, budget=12000), answers=ans)
    for attempt in range(3):
        try:
            out = run_claude(p, model=JUDGE_MODEL, timeout=900)["text"]
            j = json.loads(re.search(r"\{.*\}", out, re.S).group(0))
            break
        except Exception as e:
            print(f"  judge retry {slug}: {e}", flush=True)
            j = None
    if not j:
        return rec
    by_cond = {labels[l]: v for l, v in j["scores"].items() if l in labels}
    rec["judge"] = {"model": f"claude-{JUDGE_MODEL}", "labels": labels, "raw": j,
                    "scores": by_cond,
                    "totals": {k: sum(v.values()) for k, v in by_cond.items()},
                    "best": labels.get(j.get("best"), j.get("best")),
                    "errors": {labels[l]: v for l, v in (j.get("errors") or {}).items() if l in labels},
                    "reference_quality": j.get("reference_quality"),
                    "reference_problem": j.get("reference_problem"),
                    "verdict": j.get("verdict")}
    save(path, rec)
    return rec


def save(path, rec):
    os.makedirs(CMP, exist_ok=True)
    tmp = path + ".part"
    with open(tmp, "w") as f:
        json.dump(rec, f, ensure_ascii=False, indent=1)
    os.replace(tmp, path)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--stage", default="all")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    slugs = [x for x in a.only.split(",") if x] or [s["slug"] for s in SCENARIOS]
    slugs = [x for x in slugs if os.path.exists(os.path.join(EX, f"{x}.json"))]
    print(f"{len(slugs)} scenarios, stage={a.stage}", flush=True)

    def go(slug):
        t0 = time.time()
        try:
            if a.stage in ("answers", "all"):
                answers(slug, a.force)
            if a.stage in ("judge", "all"):
                r = judge(slug, a.force)
                t = (r.get("judge") or {}).get("totals")
                print(f"ok {slug} {time.time()-t0:.0f}s {t}", flush=True)
        except Exception as e:
            print(f"ERR {slug}: {e}", flush=True)

    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(go, slugs))


if __name__ == "__main__":
    main()
