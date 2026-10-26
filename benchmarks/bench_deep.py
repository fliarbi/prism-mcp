"""Benchmark, deep tiers: a policy maker's briefing and a researcher's deep dive, as HTML reports.

The casual tier (bench.py) hands both models the same captured tool results. Here the Prism setups
are connected LIVE to the Prism MCP and choose their own calls; plain setups get the same prompt and no
tools. Every run is timed (wall clock, time to first output, each tool call's duration) and its tool
responses are saved in full, so the ground pass can trace the report's numbers, charts, map and forecast.

    python3 benchmarks/bench_deep.py --stage run|ground|judge|render|pdf|all [--tiers policy,research]

Rubric and prompts: benchmarks/rubric/benchmark_deep_rubric.json (designed by Fable 5.1).
Writes benchmarks/results/deep/<tier>/.
"""
import argparse
import json
import os
import random
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from html import escape
from html.parser import HTMLParser

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "showcase"))
sys.path.insert(0, ROOT)
import bench as v2  # noqa: E402
import compare  # noqa: E402

DEEP_P = os.path.join(HERE, "rubric", "benchmark_deep_rubric.json")
DEEP = json.load(open(DEEP_P)) if os.path.exists(DEEP_P) else {}
OUT = os.environ.get("BENCH_DEEP_OUT") or os.path.join(ROOT, "benchmarks", "results", "deep")
TODAY = v2.TODAY
SEED = 20261023
PY = "/usr/bin/python3"
MCP = {"mcpServers": {"prism": {"type": "stdio", "command": PY, "args": [f"{ROOT}/prism_mcp.py"]}}}
SETUPS = v2.SETUPS
SCRATCH = compare.SCRATCH

CONTRACT = """=== DELIVERABLE CONTRACT (identical for every respondent) ===
Return ONE self-contained HTML document inside a single ```html fenced block, and nothing outside it.
- Charts: Vega-Lite 5 loaded from cdn.jsdelivr.net exactly as
  <script src="https://cdn.jsdelivr.net/npm/vega@5.30.0"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-lite@5.21.0"></script>
  <script src="https://cdn.jsdelivr.net/npm/vega-embed@6.26.0"></script>
  and rendered with vegaEmbed('#<chart id>', spec) into an element whose id equals the chart's manifest id,
  with the data inline in each spec ("data": {"values": [...]}); the only file a spec may load is the map file below.
- Maps: country-level choropleths using the GeoJSON served next to the report at the relative URL
  "world_india_official.geojson" (Vega-Lite data {"url": "world_india_official.geojson", "format": {"type": "json",
  "property": "features"}}; each feature has properties.iso3, properties.name and properties.id = ISO numeric;
  India is drawn with the official Survey of India outline). Join your values with a lookup transform on
  "properties.iso3". Do not use any other map file. In the manifest, map points are [country name or ISO alpha-3, value].
- Every number shown on the page carries a source tag: [c1] [c2] ... (a call you made, declared in the
  manifest), [r1] [r2] ... (an entry in References) or (est.) (an estimate from memory). A chart, map, table or
  forecast whose values have no source and are not labelled estimate is scored as invented.
- The page MUST contain <script type="application/json" id="report-manifest"> holding JSON with keys:
  "verdict": {"answer": "...", "decision": "...", "confidence": "high|medium|low - reason", "what_would_change": "..."},
  "charts": [ {"id", "kind": "line|bars|hbar|share|map|forecast", "title", "unit",
               "window": {"from": "YYYY-MM-DD", "to": "YYYY-MM-DD"}, "x": {"field": "period|year|label|country", "type": "temporal|ordinal|geo"},
               "series": [{"name", "source": "call:<feature>#<n> | ref:rN | estimate", "points": [[x, value], ...]}],
               "forecast": {"method": "...", "source": "call:<feature>#<n> | estimate", "horizon": "...",
                            "points": [[x, central, lower, upper], ...]}   (kind=forecast only),
               "caption", "supports": "the sentence on the page this chart backs, verbatim"} ],
  "exports": [ {"name": "file.csv", "source", "window": "from..to", "unit", "coverage": "full|partial|unknown", "csv": "header\\nrow..."} ],
  "calls": [ {"id": "c1", "feature", "args", "used_for"} ... , {"id": "f1", "question", "feature", "args"} ... ],
  "references": [ {"id": "r1", "title", "venue", "year", "doi_or_url"} ]
  Every chart drawn on the page appears in the manifest with the same values; the visible page and the
  manifest must agree. "calls" may be [] if you ran no data queries. Follow-up entries (f1..) give a next
  question and the query that would answer it: a tool feature and args if you have a tool, else the query in words.
"""
ARTICLE = """- RESEARCHER TIER: the page also contains <article id="research-article"> with the sections Abstract,
  Introduction, Data and methods, Results, Discussion, Limitations, References (each as an <h2>)."""


# ---------------------------------------------------------------- live runs with timing

def _stream(cmd, prompt, timeout, on_event):
    """Run a CLI, feed the prompt, timestamp every stdout JSON line as it arrives."""
    t0 = time.time()
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                         cwd=SCRATCH, bufsize=1)
    err = []
    threading.Thread(target=lambda: err.extend(p.stderr), daemon=True).start()
    p.stdin.write(prompt)
    p.stdin.close()
    killer = threading.Timer(timeout, p.kill)
    killer.start()
    try:
        for line in p.stdout:
            try:
                ev = json.loads(line)
            except Exception:
                continue
            on_event(ev, round(time.time() - t0, 2))
        p.wait()
    finally:
        killer.cancel()
    return round(time.time() - t0, 1), "".join(err)[-1500:], p.returncode


def run_claude(prompt, live):
    os.makedirs(SCRATCH, exist_ok=True)
    cmd = ["claude", "-p", "--model", v2.RESP_MODEL, "--no-session-persistence", "--setting-sources", "",
           "--system-prompt", f"You are Claude, an AI assistant made by Anthropic. Today's date is {TODAY}.",
           "--output-format", "stream-json", "--verbose", "--strict-mcp-config"]
    cmd += (["--mcp-config", json.dumps(MCP), "--allowedTools", "mcp__prism", "--tools", ""] if live
            else ["--mcp-config", '{"mcpServers":{}}', "--tools", ""])
    st = {"calls": [], "pending": {}, "first_output": None, "text": "", "usage": None}

    def on(ev, t):
        if ev.get("type") == "assistant":
            for c in ev["message"].get("content", []):
                if c.get("type") == "text" and c.get("text", "").strip() and st["first_output"] is None:
                    st["first_output"] = t
                if c.get("type") == "tool_use":
                    rec = {"tool": c["name"].replace("mcp__prism__", ""), "args": c.get("input"), "start": t}
                    st["pending"][c["id"]] = rec
                    st["calls"].append(rec)
        elif ev.get("type") == "user":
            for c in ev["message"].get("content", []):
                if isinstance(c, dict) and c.get("type") == "tool_result" and c.get("tool_use_id") in st["pending"]:
                    body = c.get("content")
                    if isinstance(body, list):
                        body = "".join(x.get("text", "") for x in body if isinstance(x, dict))
                    r = st["pending"].pop(c["tool_use_id"])
                    r.update(end=t, seconds=round(t - r["start"], 2), result=body, error=bool(c.get("is_error")))
        elif ev.get("type") == "result":
            st["text"] = ev.get("result", "") or ""
            st["usage"] = ev.get("usage")
    wall, err, rc = _stream(cmd, prompt, 3600, on)
    return _finish(st, wall, err, rc, v2.RESP_MODEL if v2.RESP_MODEL.startswith("claude") else f"claude-{v2.RESP_MODEL}")


def run_codex(prompt, live):
    os.makedirs(SCRATCH, exist_ok=True)
    out = os.path.join(SCRATCH, f"deep_{os.getpid()}_{random.randint(0, 1 << 30)}.txt")
    cmd = ["codex", "exec", "--json", "--ignore-user-config", "-m", compare.CHATGPT_MODEL, "-c",
           "model_reasoning_effort=medium", "-s", "read-only", "--skip-git-repo-check", "--ephemeral", "-o", out]
    if live:
        cmd += ["-c", f'mcp_servers.prism.command="{PY}"', "-c", f'mcp_servers.prism.args=["{ROOT}/prism_mcp.py"]',
                "-c", "mcp_servers.prism.tool_timeout_sec=900", "-c", "mcp_servers.prism.startup_timeout_sec=90",
                "-c", 'mcp_servers.prism.default_tools_approval_mode="approve"']
    cmd.append("-")
    st = {"calls": [], "pending": {}, "first_output": None, "text": "", "usage": None}

    def on(ev, t):
        it = ev.get("item") or {}
        typ = ev.get("type")
        if typ == "item.started" and it.get("type") == "mcp_tool_call":
            rec = {"tool": it.get("tool"), "args": it.get("arguments"), "start": t}
            st["pending"][it.get("id")] = rec
            st["calls"].append(rec)
        elif typ == "item.completed" and it.get("type") == "mcp_tool_call":
            r = st["pending"].pop(it.get("id"), None)
            res = it.get("result") or {}
            body = "".join(x.get("text", "") for x in (res.get("content") or []) if isinstance(x, dict)) \
                if isinstance(res, dict) else json.dumps(res)
            if r is not None:
                r.update(end=t, seconds=round(t - r["start"], 2), result=body, error=bool(it.get("error")))
        elif typ == "item.completed" and it.get("type") == "agent_message" and st["first_output"] is None:
            st["first_output"] = t
        elif typ == "turn.completed":
            st["usage"] = ev.get("usage")
    wall, err, rc = _stream(cmd, prompt, 3600, on)
    st["text"] = open(out).read().strip() if os.path.exists(out) else ""
    if os.path.exists(out):
        os.remove(out)
    return _finish(st, wall, err, rc, compare.CHATGPT_MODEL)


def _finish(st, wall, err, rc, model):
    for r in st["pending"].values():  # the session ended while the call was still running
        r.update(returned=False)
    calls = st["calls"]
    tool_s = sum(c.get("seconds") or 0 for c in calls)
    timing = {"wall_seconds": wall, "first_output_seconds": st["first_output"], "tool_calls": len(calls),
              "tool_calls_returned": sum(1 for c in calls if "end" in c), "tool_seconds_sum": round(tool_s, 1),
              "slowest_call": max(calls, key=lambda c: c.get("seconds") or 0)["tool"] if calls else None,
              "usage": st["usage"]}
    if not st["text"]:
        raise RuntimeError(f"{model} rc={rc}: {err[-400:]}")
    return {"model": model, "text": st["text"], "timing": timing, "calls": calls}


def prompt_for(tier, topic, setup):
    t = DEEP["tiers"][tier]
    contract = CONTRACT + (ARTICLE if tier == "research" else "")
    p = t["prompt"].replace("{topic}", topic).replace("{today}", TODAY).replace("{contract}", contract)
    suf = DEEP["setup_suffixes"]["bare" if setup.endswith("_bare") else "prism_live"]
    return p + "\n\n" + suf + (" Do not run any commands or tools." if setup.endswith("_bare") else "")


def draw_topic():
    pool = DEEP["topic_pool"]["entries"]
    t = random.Random(SEED).choice(pool)
    return t, f"{t['label']} (central claim: {t['central_claim']})"


_lock = threading.Lock()


def run_tier(tier, topic, force=False):
    d = os.path.join(OUT, tier)
    os.makedirs(d, exist_ok=True)
    path = os.path.join(d, "runs.json")
    rec = json.load(open(path)) if os.path.exists(path) else {"tier": tier, "topic": topic}
    prompts = {k: prompt_for(tier, topic, k) for k in SETUPS}
    json.dump(prompts, open(os.path.join(d, "prompts.json"), "w"), ensure_ascii=False, indent=1)

    def go(k):
        live = k.endswith("_prism")
        fn = run_claude if k.startswith("claude") else run_codex
        for attempt in range(2):
            try:
                r = fn(prompts[k], live)
                if live and not r["calls"] and attempt == 0:
                    print(f"  {tier} {k}: no tool calls, retrying", flush=True)
                    continue
                r["no_tool_calls"] = live and not r["calls"]
                with _lock:
                    rec[k] = r
                    json.dump(rec, open(path, "w"), ensure_ascii=False, indent=1)
                tm = r["timing"]
                print(f"  {tier} {k}: {tm['wall_seconds']}s, {tm['tool_calls']} calls, {len(r['text'])} chars",
                      flush=True)
                return
            except Exception as e:
                print(f"  {tier} {k} error: {e}", flush=True)

    todo = [k for k in SETUPS if force or k not in rec]
    with ThreadPoolExecutor(4) as ex:
        list(ex.map(go, todo))
    return rec


# ---------------------------------------------------------------- parse the HTML deliverable

def extract_html(text):
    m = re.search(r"```html\s*\n(.*?)```", text, re.S | re.I)
    if m:
        return m.group(1)
    m = re.search(r"(<!doctype html.*</html>)", text, re.S | re.I)
    return m.group(1) if m else ""


def manifest_of(html):
    m = re.search(r'<script[^>]*id=["\'](?:report|prism)-manifest["\'][^>]*>(.*?)</script>', html, re.S | re.I)
    if not m:
        return None, "no manifest"
    try:
        return json.loads(m.group(1)), ""
    except Exception as e:
        return None, f"manifest is not valid JSON: {e}"


class _Text(HTMLParser):
    """Visible text with <h1>-<h3> turned into markdown headings, so the v2 section parser works."""
    SKIP = {"script", "style", "head", "title"}

    def __init__(self):
        super().__init__()
        self.out, self.skip, self.h = [], 0, None

    def handle_starttag(self, tag, attrs):
        if tag in self.SKIP:
            self.skip += 1
        elif tag in ("h1", "h2", "h3"):
            self.out.append("\n## ")
            self.h = tag
        elif tag in ("p", "li", "tr", "br", "div", "section", "article", "table"):
            self.out.append("\n" + ("- " if tag == "li" else ""))
        elif tag in ("td", "th"):
            self.out.append(" | ")

    def handle_endtag(self, tag):
        if tag in self.SKIP:
            self.skip = max(0, self.skip - 1)
        elif tag in ("h1", "h2", "h3"):
            self.out.append("\n")

    def handle_data(self, data):
        if not self.skip:
            self.out.append(re.sub(r"\s+", " ", data))


def visible_text(html):
    p = _Text()
    p.feed(html)
    return re.sub(r"\n\s*\n+", "\n\n", "".join(p.out)).strip()


def as_doc(html, man):
    """The page as the v2 ground pass reads a markdown deliverable: prose, then typed blocks from the manifest."""
    prose = visible_text(html)
    v = (man or {}).get("verdict") or {}
    head = (f"## Verdict\n- Answer: {v.get('answer', '')}\n- Decision: {v.get('decision', '')}\n"
            f"- Confidence: {v.get('confidence', '')}\n- What would change it: {v.get('what_would_change', '')}\n\n")
    blocks = []
    for ch in (man or {}).get("charts") or []:
        c = dict(ch)
        if c.get("kind") == "forecast" and not c.get("series") and (c.get("forecast") or {}).get("points"):
            c["series"] = [{"name": "central", "source": c["forecast"].get("source"),
                            "points": [[p[0], p[1]] for p in c["forecast"]["points"]]}]
        blocks.append("```prism-chart\n" + json.dumps(c, ensure_ascii=False) + "\n```")
    for e in (man or {}).get("exports") or []:
        info = " ".join(f"{k}={str(e.get(k, '')).replace(' ', '_')}" for k in ("name", "source", "window", "unit", "coverage") if e.get(k))
        blocks.append(f"```csv {info}\n{e.get('csv', '')}\n```")
    if (man or {}).get("calls"):
        blocks.append("```prism-calls\n" + json.dumps(man["calls"], ensure_ascii=False) + "\n```")
    refs = (man or {}).get("references") or []
    if refs and "## references" not in prose.lower():
        prose += "\n\n## References\n" + "\n".join(
            f"[{r.get('id')}] {r.get('title')}. {r.get('venue')}, {r.get('year')}. {r.get('doi_or_url')}" for r in refs)
    return head + canon_headings(prose) + "\n\n" + "\n\n".join(blocks)


CANON = [("what the data shows", r"what the data shows|measured picture|analytical report"),
         ("trend", r"trend|attention|rq1|over time"),
         ("comparison", r"against the world|compar|rq3|india vs|versus|selected countries|same lane"),
         ("geography", r"geograph|map"),
         ("evidence", r"evidence|rq2|risk factor"),
         ("drill-down", r"drill"),
         ("exports", r"export|data table|csv"),
         ("method and limits", r"method|limit"),
         ("references", r"^references?$")]


def canon_headings(prose):
    """map the tier's own section names onto the v2 section keys the ground pass reads"""
    def rep(m):
        h = m.group(1).strip().lower()
        for key, pat in CANON:
            if re.search(pat, h):
                return f"## {key}"
        return m.group(0)
    return re.sub(r"^## (.+)$", rep, prose, flags=re.M)


def replay_calls(calls):
    """Full envelopes for the calls a live session made: replay each through the registry (12h cache = same
    answer the session got); fall back to the session's own result text when replay fails."""
    import prism_mcp as m
    out, seen = [], {}
    for i, c in enumerate(calls, 1):
        tool = c["tool"].split("__")[-1].replace("prism.", "")
        entry = m.REGISTRY.get(tool)
        resp = None
        try:
            resp = json.loads(c.get("result") or "")
        except Exception:
            pass
        if entry and (not isinstance(resp, dict) or "data" not in resp):
            try:
                resp = entry["fn"](**(c.get("args") or {}))
            except Exception as e:
                resp = {"ok": False, "error": {"message": str(e)}}
        resp = resp if isinstance(resp, dict) else {"ok": False}
        feat = resp.get("feature") or (entry or {}).get("feature") or tool
        seen[feat] = seen.get(feat, 0) + 1
        out.append({"id": f"c{i}", "tool": tool, "feature": feat, "n": seen[feat], "args": c.get("args"),
                    "response": resp, "seconds": c.get("seconds"), "returned": "end" in c})
    return out


def render_check(html_path, png):
    """Render in headless Chrome: rendered Vega views, console errors, a full-page screenshot."""
    base = [v2.CHROME, "--headless=new", "--no-sandbox", "--hide-scrollbars", "--virtual-time-budget=25000",
            "--blink-settings=preferredColorScheme=1", "--enable-logging=stderr", "--v=0",
            "--allow-file-access-from-files"]
    r = subprocess.run(base + ["--dump-dom", "file://" + html_path], capture_output=True, text=True, timeout=180)
    dom = r.stdout
    tags = re.findall(r'<(?:canvas|svg)[^>]*class="[^"]*\bmarks\b[^"]*"[^>]*>', dom)
    widths = [float(w) for t in tags for w in re.findall(r'width="([\d.]+)"', t)[:1]]
    views = sum(1 for w in widths if w >= 10)  # a view drawn at zero width is not a rendered chart
    errors = [l for l in r.stderr.splitlines() if "CONSOLE" in l and re.search(r"error|uncaught", l, re.I)]
    h = 24000
    subprocess.run(base + [f"--screenshot={png}", f"--window-size=1200,{h}", "file://" + html_path],
                   capture_output=True, timeout=240)
    try:
        from PIL import Image, ImageChops
        im = Image.open(png).convert("RGB")
        box = ImageChops.difference(im, Image.new("RGB", im.size, im.getpixel((5, im.height - 5)))).getbbox()
        if box:
            im.crop((0, 0, im.width, min(im.height, box[3] + 30))).save(png)
    except Exception:
        pass
    return {"rendered_views": views, "zero_width_views": len(widths) - views, "console_errors": errors[:10], "dom_chars": len(dom)}


# ---------------------------------------------------------------- ground (script pass for the deep tiers)

PARAMS = {p["key"]: p for p in DEEP.get("parameters", [])}
V2_KEYS = ("trend", "comparison", "chart", "drilldown", "export", "repro", "refs", "accuracy", "limits", "verdict")
ALIAS = {"usa": "USA", "us": "USA", "united states": "USA", "united states of america": "USA", "uk": "GBR",
         "united kingdom": "GBR", "england": "GBR", "scotland": "GBR", "wales": "GBR", "northern ireland": "GBR",
         "russia": "RUS", "south korea": "KOR", "korea": "KOR", "iran": "IRN", "vietnam": "VNM", "czechia": "CZE",
         "turkey": "TUR", "turkiye": "TUR", "taiwan": "TWN", "tanzania": "TZA", "bolivia": "BOL", "venezuela": "VEN",
         "syria": "SYR", "laos": "LAO", "moldova": "MDA", "congo": "COG", "dr congo": "COD", "ivory coast": "CIV"}


def iso3(name):
    import pycountry
    n = str(name or "").strip()
    if re.fullmatch(r"[A-Z]{3}", n):
        return n
    k = re.sub(r"[^\w\s]", "", n.lower()).strip()
    if k in ALIAS:
        return ALIAS[k]
    try:
        return pycountry.countries.lookup(n).alpha_3
    except LookupError:
        try:
            return pycountry.countries.search_fuzzy(n)[0].alpha_3
        except Exception:
            return None


def paths(obj, path="", acc=None):
    acc = [] if acc is None else acc
    if isinstance(obj, dict):
        for k, v in obj.items():
            paths(v, f"{path}.{k}" if path else k, acc)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            paths(v, f"{path}[{i}]", acc)
    elif isinstance(obj, (int, float)) and not isinstance(obj, bool):
        acc.append((path, float(obj)))
    return acc


def corpus_of(feature, path):
    p = path.lower()
    if any(x in p for x in ("pubmed", "health", "disease", "clinical")):
        return "health"
    if "patent" in p:
        return "patents"
    if "news" in p:
        return "news"
    if "research" in p or "openalex" in p or "arxiv" in p:
        return "research"
    return {"news": "news", "research": "research"}.get(feature.split(".")[0], "research" if feature.startswith("analysis") else feature.split(".")[0])


def geo_index(calls):
    """country iso3 -> set of values from geography lanes in the recorded responses"""
    idx = {}
    for c in calls:
        if c["feature"] not in ("research.geography", "news.geography"):
            continue
        for row_path, val in paths(c["response"].get("data")):
            pass
        def walk(o):
            if isinstance(o, dict):
                lab = o.get("country") or o.get("label") or o.get("name")
                if isinstance(lab, str):
                    code = iso3(lab)
                    if code:
                        for k, v in o.items():
                            if isinstance(v, (int, float)) and not isinstance(v, bool):
                                idx.setdefault(code, set()).add(float(v))
                for v in o.values():
                    walk(v)
            elif isinstance(o, list):
                for v in o:
                    walk(v)
        walk(c["response"].get("data"))
    return idx


def close(v, vals):
    return any(abs(v - x) < 1e-9 or abs(round(x, 1) - v) < 1e-9 or (abs(v) >= 10 and abs(round(x) - v) < 1e-9)
               for x in vals)


def ground_deep(tier, setup, run, calls, d):
    html = extract_html(run["text"])
    man, merr = manifest_of(html)
    prism = setup.endswith("_prism")
    page = os.path.join(d, f"{setup}.html")
    open(page, "w").write(html or "<html><body><p>No HTML document was returned.</p></body></html>")
    geo = os.path.join(d, "world_india_official.geojson")
    if not os.path.exists(geo):
        import shutil
        shutil.copy(os.path.join(ROOT, "showcase", "assets", "world_india_official.geojson"), geo)
    charts = (man or {}).get("charts") or []
    plain = [c for c in charts if c.get("kind") not in ("map", "forecast")]
    base_man = dict(man or {}, charts=plain + [c for c in charts if c.get("kind") == "forecast" and False])
    doc = as_doc(html, base_man)
    g = v2.ground(None, setup, doc, calls, pattern="brief", applies=[k for k in V2_KEYS if k in DEEP["tiers"][tier]["weights"]])
    ceil, inv = g["ceiling"], g["invented"]
    text = visible_text(html)

    # map
    maps = [c for c in charts if c.get("kind") == "map"]
    gi = geo_index(calls) if prism else {}
    mres = []
    for mp in maps:
        pts = [p for se in mp.get("series") or [] for p in (se.get("points") or []) if isinstance(p, (list, tuple)) and len(p) > 1]
        srcs = {(se.get("source") or "").split("#")[0] for se in mp.get("series") or []}
        how = "call" if any(x.startswith("call:") for x in srcs) else "estimate" if any(x.startswith("estimate") for x in srcs) else "ref" if any(x.startswith("ref:") for x in srcs) else "none"
        ok = sum(1 for p in pts if isinstance(p[1], (int, float)) and close(float(p[1]), gi.get(iso3(p[0]) or "", set())))
        india = any(iso3(p[0]) == "IND" for p in pts)
        lane = bool(re.search(r"affiliation|first.author|journal|publish|about|reported|coverage|assignee|patent", json.dumps(mp).lower()))
        mres.append({"title": mp.get("title"), "points": len(pts), "how": how, "traced_share": ok / len(pts) if pts else 0, "india": india, "lane_stated": lane})
        if how == "none" and pts:
            inv.append(f"map '{mp.get('title')}' has no source")
    if not maps:
        ceil["map"] = 0
    else:
        best = 0
        for m in mres:
            if m["how"] == "none":
                sc = 0
            elif m["how"] != "call":
                sc = 1
            elif m["traced_share"] >= 0.999 and m["lane_stated"] and m["india"]:
                sc = 5
            elif m["traced_share"] >= 0.9:
                sc = 3 if m["lane_stated"] else 2
            else:
                sc = 1
            best = max(best, sc)
        ceil["map"] = 0 if any(m["how"] == "none" for m in mres) else best

    # forecast
    fcs = [c for c in charts if c.get("kind") == "forecast"]
    scen = set()
    for c in calls if prism else []:
        if c["feature"] in ("analysis.scenarios", "analysis.history"):
            scen |= v2.leaves(c["response"].get("data"), set())
    fres = []
    for f in fcs:
        fp = (f.get("forecast") or {}).get("points") or []
        src = (f.get("forecast") or {}).get("source") or ""
        nums = [float(x) for p in fp for x in p[1:4] if isinstance(x, (int, float))]
        share = sum(1 for x in nums if close(x, scen)) / len(nums) if nums and scen else 0
        bounds = all(len(p) >= 4 and p[2] is not None and p[3] is not None for p in fp) if fp else False
        method = bool((f.get("forecast") or {}).get("method"))
        fres.append({"title": f.get("title"), "source": src, "periods": len(fp), "traced_share": share, "bounds": bounds, "method": method})
        if fp and not src:
            inv.append(f"forecast '{f.get('title')}' has no source")
    if not fcs:
        ceil["forecast"] = 1 if re.search(r"\b(will|projected|forecast|by 20\d\d)\b", text, re.I) else 0
    else:
        def fsc(r):
            if not r["source"]:
                return 0
            if not r["source"].startswith("call:"):
                return 2 if r["method"] else 1
            if r["traced_share"] >= 0.9 and r["bounds"] and r["method"]:
                return 5 if re.search(r"backtest|MAE|no.change", text, re.I) else 3
            return 2
        ceil["forecast"] = max(fsc(r) for r in fres)

    # dimensions
    dims = set()
    for c in charts:
        hows = {(se.get("source") or "").split(":")[0] for se in c.get("series") or []} | (
            {((c.get("forecast") or {}).get("source") or "").split(":")[0]} if c.get("kind") == "forecast" else set())
        grounded = "call" in hows if prism else False
        if not grounded and prism:
            continue
        k = c.get("kind")
        t = (json.dumps(c).lower())
        if k == "map":
            dims.add("geography")
        elif k == "forecast":
            dims.add("forecast")
        elif (c.get("x") or {}).get("type") == "temporal" or (c.get("x") or {}).get("field") in ("period", "year"):
            dims.add("time")
        if k in ("share", "stacked") or re.search(r"orientation|stance|tier|supports|contradict|share of", t):
            dims.add("composition")
        if re.search(r"effect|odds|relative risk|hazard|\brr\b|\bor\b", t):
            dims.add("evidence magnitude")
        if re.search(r"pubmed|patent", t) and re.search(r"news|research", t):
            dims.add("source mix")
        if len(c.get("series") or []) >= 2 and (c.get("x") or {}).get("type") != "temporal" or re.search(r"india|china|united states|countr", t) and k != "map":
            dims.add("comparison")
    nd = len(dims)
    if not prism:
        ceil["dimensions"] = 1 if charts else 0
    else:
        ceil["dimensions"] = 5 if nd >= 5 else 4 if nd >= 4 else nd

    # cross-domain: corpora behind the traced numbers on the page
    corp_vals = {}
    for c in calls if prism else []:
        for pth, val in paths(c["response"].get("data")):
            corp_vals.setdefault(corpus_of(c["feature"], pth), set()).add(val)
    used, connecting = set(), 0
    for sent in re.split(r"(?<=[.!?])\s+", text):
        cs = set()
        for m in v2.NUM.finditer(sent):
            v = v2.num_val(m.group(0).rstrip(","))
            if v is None or v2.is_year(m.group(0)):
                continue
            for corp, vals in corp_vals.items():
                if close(v, vals):
                    cs.add(corp)
        used |= cs
        if len(cs) >= 2:
            connecting += 1
    if not prism:
        ceil["crossdomain"] = 1
    else:
        n = len(used)
        ceil["crossdomain"] = 5 if n >= 4 and connecting >= 2 else 4 if n >= 3 and connecting >= 2 else 3 if n >= 3 and connecting >= 1 else 2 if n >= 2 else n

    # integrity (render happens in stage_render; here: manifest and fence)
    ceil["integrity"] = 5 if (html and man) else 0

    extra = {"maps": mres, "forecasts": fres, "dimensions": sorted(dims), "corpora_traced": sorted(used),
             "connecting_sentences": connecting, "manifest_error": merr, "html_bytes": len(html or "")}

    # policy options
    if tier == "policy":
        m = re.search(r'<table[^>]*id=["\']policy-options["\'][^>]*>(.*?)</table>', html or "", re.S | re.I)
        po = {"present": bool(m)}
        if not m:  # the id on a wrapper instead of the table itself: accept the first table inside it, and say so
            w = re.search(r'id=["\']policy-options["\'][^>]*>(.*?)</(?:section|div)>', html or "", re.S | re.I)
            m = re.search(r"<table[^>]*>(.*?)</table>", w.group(1), re.S | re.I) if w else None
            po.update(present=bool(m), id_on_wrapper=bool(m))
        if m:
            rows = re.findall(r"<tr[^>]*>(.*?)</tr>", m.group(1), re.S | re.I)
            cells = [[re.sub(r"<[^>]+>", "", x).strip() for x in re.findall(r"<t[hd][^>]*>(.*?)</t[hd]>", r, re.S | re.I)] for r in rows]
            want = ["option", "who acts", "evidence", "cost / benefit", "trade-off", "indicator"]
            hdr = [h.lower().replace("cost/benefit", "cost / benefit") for h in (cells[0] if cells else [])]
            body = cells[1:]
            po.update(header_ok=[h[:14] for h in hdr] == [w[:14] for w in want], rows=len(body),
                      status_quo=any(re.search(r"status quo|no change", " ".join(r), re.I) for r in body),
                      who_specific=sum(1 for r in body if len(r) > 1 and re.search(r"ministr|department|board|commission|authorit|state|municipal|corporation|regulator|parliament|council|niti|fssai|icmr|cpcb|[A-Z]{3,}", r[1])),
                      evidence_tagged=sum(1 for r in body if len(r) > 2 and re.search(r"\[(c|r)\d+\]", r[2])),
                      cost_ok=sum(1 for r in body if len(r) > 3 and (re.search(r"\[(c|r)\d+\]|\(est|not measured", r[3], re.I) or not re.search(r"\d", r[3]))))
            untagged_cost = [r[3] for r in body if len(r) > 3 and re.search(r"\d", r[3]) and not re.search(r"\[(c|r)\d+\]|\(est|not measured", r[3], re.I)]
            if untagged_cost:
                inv.append("options-table cost figure without a source: " + untagged_cost[0][:80])
            ok3 = po["header_ok"] and po["rows"] >= 3 and po["status_quo"] and po["who_specific"] >= po["rows"] - 1 and po["evidence_tagged"] >= po["rows"] - 1
            rec = bool(re.search(r"recommend", text, re.I))
            ceil["actionability"] = (5 if ok3 and rec and re.search(r"do not know|don't know|unknown", text, re.I) else 4 if ok3 and rec else 3 if ok3 else 2)
        else:
            ceil["actionability"] = 1 if re.search(r"recommend|option", text, re.I) else 0
        extra["policy_options"] = po

    # research article
    if tier == "research":
        m = re.search(r'<article[^>]*id=["\']research-article["\'][^>]*>(.*?)</article>', html or "", re.S | re.I)
        ar = {"present": bool(m)}
        if m:
            heads = [re.sub(r"<[^>]+>", "", h).strip().lower() for h in re.findall(r"<h[23][^>]*>(.*?)</h[23]>", m.group(1), re.S | re.I)]
            want = ["abstract", "introduction", "data and methods", "results", "discussion", "limitations", "references"]
            pos = [next((i for i, h in enumerate(heads) if w in h), -1) for w in want]
            atext = visible_text(m.group(1))
            words = len(atext.split())
            parts = re.split(r"\n## ", "\n" + atext)
            abstract = next((p for p in parts if p.lower().startswith("abstract")), "")
            res = next((p for p in parts if p.lower().startswith("results")), "")
            rn = [x for x in v2.NUM.finditer(res) if not v2.is_year(x.group(0))]
            def para_tail(pos):
                end = res.find("\n", pos)
                return res[pos:end if end > 0 else len(res)]
            rtag = sum(1 for x in rn if re.search(r"[\[(](c|r)\d+[\])]|\(est", para_tail(x.end())))
            ar.update(sections_found=sum(1 for p_ in pos if p_ >= 0), in_order=all(a < b for a, b in zip([p_ for p_ in pos if p_ >= 0], [p_ for p_ in pos if p_ >= 0][1:])),
                      words=words, abstract_words=len(abstract.split()) - 1, results_numbers=len(rn), results_tagged=rtag)
            full = ar["sections_found"] == 7 and ar["in_order"]
            tagged = rtag / len(rn) if rn else 1
            if not full:
                ceil["article"] = 1
            elif words < 2000:
                ceil["article"] = 2
            elif prism:
                ceil["article"] = 5 if tagged >= 0.9 else 3 if tagged >= 0.6 else 2
            else:
                ceil["article"] = 3 if tagged >= 0.6 else 2
        else:
            ceil["article"] = 0
        extra["article"] = ar

    ceil = {k: v for k, v in ceil.items() if k in DEEP["tiers"][tier]["weights"]}
    g.update(ceiling=ceil, invented=inv, deep=extra)
    return g


def stage_ground(tiers, draw):
    for tier in tiers:
        d = os.path.join(OUT, tier)
        runs = json.load(open(os.path.join(d, "runs.json")))
        rec = {}
        allcalls = {}
        for k in SETUPS:
            if k not in runs:
                continue
            calls = replay_calls(runs[k]["calls"]) if k.endswith("_prism") else []
            allcalls[k] = calls
            rec[k] = ground_deep(tier, k, runs[k], calls, d)
            print(f"  ground {tier} {k}: {rec[k]['ceiling']} inv={len(rec[k]['invented'])}", flush=True)
        json.dump(rec, open(os.path.join(d, "ground.json"), "w"), ensure_ascii=False, indent=1, default=str)
        json.dump({k: [{"id": c["id"], "feature": c["feature"], "args": c["args"], "seconds": c["seconds"],
                        "response": c["response"]} for c in v] for k, v in allcalls.items()},
                  open(os.path.join(d, "calls_full.json"), "w"), ensure_ascii=False, default=str)


def integrity_ceiling(g, rc, n_charts):
    if not g["deep"]["html_bytes"] or g["deep"]["manifest_error"]:
        return 0
    views, errs = rc["rendered_views"], len(rc["console_errors"])
    if n_charts and views < n_charts / 2:
        return 1
    if not n_charts or errs > 2:
        return 2
    if views < n_charts or errs:
        return 3
    return 5 if g["deep"]["html_bytes"] < 4_000_000 else 4


_old_stage_ground = stage_ground


def stage_ground(tiers, draw):
    _old_stage_ground(tiers, draw)
    for tier in tiers:
        d = os.path.join(OUT, tier)
        gp = os.path.join(d, "ground.json")
        gr = json.load(open(gp))
        runs = json.load(open(os.path.join(d, "runs.json")))
        for k, g in gr.items():
            man, _ = manifest_of(extract_html(runs[k]["text"]))
            n = len((man or {}).get("charts") or [])
            rc = render_check(os.path.join(d, f"{k}.html"), os.path.join(d, f"{k}_full.png"))
            g["render"] = dict(rc, manifest_charts=n)
            if "integrity" in g["ceiling"]:
                g["ceiling"]["integrity"] = integrity_ceiling(g, rc, n)
            print(f"  render {tier} {k}: {rc['rendered_views']}/{n} views, {len(rc['console_errors'])} console errors", flush=True)
        json.dump(gr, open(gp, "w"), ensure_ascii=False, indent=1, default=str)


# ---------------------------------------------------------------- judges

JUDGE = """You are one of two blind judges in a public benchmark of decision-grade intelligence deliverables.
Today is {today}. {n} respondents received the same brief; some had a live research-and-news database, some
answered from memory; do not guess which. Labels {labels} are in random order.

THE BRIEF (as given to every respondent; the deliverable format section is omitted here):
{brief}

THE RUBRIC (score every parameter 0-5 using these anchors exactly):
{rubric}

SCRIPT PASS. A script parsed each HTML deliverable, traced numbers, charts, maps, forecasts and CSV cells against
the recorded database responses, executed follow-up queries, looked up DOIs in a 401M-work corpus, and rendered
the page in headless Chrome. It gives each script-checkable parameter a CEILING: you may score BELOW a ceiling
with a reason, never above it.
{ground}

REFERENCE RECORD (the database responses the database-backed respondents received, union of both; a memory-only
respondent is not penalised for lacking it, only for contradicting it or inventing specifics):
{reference}

{answers}

Return ONLY JSON:
{{"scores": {{"A": {{"<param>": n, ...}}, "B": {{...}}, "C": {{...}}, "D": {{...}}}},
 "reasons": {{"A": {{"<param>": "short reason"}}, ...}},
 "errors": {{"A": ["contradictions or fabricated specifics"], ...}},
 "best": "A|B|C|D",
 "verdict": "two or three sentences: what separated the deliverables for this reader"}}"""


def rubric_text(tier):
    w = DEEP["tiers"][tier]["weights"]
    out = []
    for k, wt in w.items():
        p = PARAMS.get(k) or v2.PARAMS.get(k)
        anc = p.get("scale_anchors") or {}
        anc = "; ".join(f"{s}={anc[s]}" for s in sorted(anc))
        out.append(f"- {k} (weight {wt}): {p.get('definition', '')}\n  anchors: {anc}\n  anti-gaming: {p.get('anti_gaming', '')}")
    return "\n".join(out)


def reference(tier):
    full = json.load(open(os.path.join(OUT, tier, "calls_full.json")))
    parts = []
    for k, calls in full.items():
        for c in calls:
            body = {"data": compare.compact(c["response"].get("data"), list_cap=10) if c["response"].get("data") else None,
                    "window": c["response"].get("window"), "error": c["response"].get("error")}
            parts.append(f"--- {k} {c['id']} {c['feature']} args={json.dumps(c['args'], ensure_ascii=False)}\n"
                         + json.dumps(body, ensure_ascii=False, separators=(",", ":"), default=str)[:7000])
    return "\n".join(parts)[:120000]


def deliverable_view(text):
    html = extract_html(text)
    man, err = manifest_of(html)
    vis = visible_text(html) if html else text
    mj = json.dumps(man, ensure_ascii=False)[:30000] if man else f"(manifest missing: {err})"
    return f"VISIBLE TEXT:\n{vis[:60000]}\n\nMANIFEST:\n{mj}"


def judge(tier, which, draw):
    d = os.path.join(OUT, tier)
    runs = json.load(open(os.path.join(d, "runs.json")))
    gr = json.load(open(os.path.join(d, "ground.json")))
    keys = [k for k in SETUPS if k in runs]
    order = keys[:]
    random.Random(f"{tier}-{which}").shuffle(order)
    labels = dict(zip("ABCD", order))
    gtxt = "\n".join(
        f"{l}: ceilings={json.dumps(gr[k]['ceiling'])}; numbers {gr[k]['numbers']['traced']}/{gr[k]['numbers']['total']} traced, "
        f"{gr[k]['numbers']['untagged_untraced']} untagged; DOIs {gr[k]['dois']['found_in_corpus']}/{gr[k]['dois']['cited']} found; "
        f"follow-ups ok {gr[k]['followups_ok']}/{len(gr[k]['followups'])}; render {gr[k].get('render', {}).get('rendered_views')}/"
        f"{gr[k].get('render', {}).get('manifest_charts')} views, {len(gr[k].get('render', {}).get('console_errors', []))} console errors; "
        f"deep={json.dumps({x: gr[k]['deep'][x] for x in ('maps', 'forecasts', 'dimensions', 'corpora_traced', 'connecting_sentences', 'policy_options', 'article') if x in gr[k]['deep']}, default=str)[:1500]}; "
        f"invented: {gr[k]['invented'][:4]}" for l, k in labels.items())
    brief = DEEP["tiers"][tier]["prompt"].replace("{topic}", draw["label"]).replace("{today}", TODAY).replace("{contract}", "(HTML contract omitted)")
    atxt = "\n\n".join(f"=== DELIVERABLE {l} ===\n{deliverable_view(runs[k]['text'])}" for l, k in labels.items())
    p = JUDGE.format(today=TODAY, n=len(labels), labels=", ".join(labels), brief=brief, rubric=rubric_text(tier), ground=gtxt, reference=reference(tier), answers=atxt)
    j = None
    for attempt in range(3):
        try:
            out = (compare.run_claude(p, model="opus", timeout=2400)["text"] if which == "opus"
                   else compare.run_chatgpt(p, timeout=2400)["text"])
            j = json.loads(re.search(r"\{.*\}", out, re.S).group(0))
            break
        except Exception as e:
            print(f"  judge {which} {tier} retry: {e}", flush=True)
    if not j:
        raise RuntimeError(f"judge {which} failed for {tier}")
    res = {"labels": labels, "raw": j, "scores": {}, "clamped": {}}
    for l, k in labels.items():
        sc = {}
        for prm in DEEP["tiers"][tier]["weights"]:
            v = j["scores"].get(l, {}).get(prm)
            cap = gr[k]["ceiling"].get(prm, 5)
            v = cap if v is None else min(int(round(float(v))), 5)
            if v > cap:
                res["clamped"].setdefault(k, []).append(f"{prm} {v}->{cap}")
                v = cap
            sc[prm] = v
        res["scores"][k] = sc
    json.dump(res, open(os.path.join(d, f"judge_{which}.json"), "w"), ensure_ascii=False, indent=1)
    return res


def weighted(tier, sc, invented, render_fail):
    w = DEEP["tiers"][tier]["weights"]
    v = sum(w[k] * sc[k] for k in w if k in sc) / 5 * 100 / sum(w.values())
    cap = 100
    if invented:
        cap = 40
    if render_fail:
        cap = min(cap, 25)
    return round(min(v, cap), 1), round(v, 1)


def stage_judge(tiers, draw):
    for tier in tiers:
        with ThreadPoolExecutor(2) as ex:
            list(ex.map(lambda w: judge(tier, w, draw), ("opus", "gpt")))
        d = os.path.join(OUT, tier)
        gr = json.load(open(os.path.join(d, "ground.json")))
        runs = json.load(open(os.path.join(d, "runs.json")))
        js = {w: json.load(open(os.path.join(d, f"judge_{w}.json"))) for w in ("opus", "gpt")}
        out = {}
        for k in gr:
            per = {p: round(sum(j["scores"][k][p] for j in js.values()) / 2, 1) for p in DEEP["tiers"][tier]["weights"]}
            rf = gr[k]["ceiling"].get("integrity", 5) == 0
            strict, plain = weighted(tier, per, bool(gr[k]["invented"]), rf)
            out[k] = {"params": per, "strict": strict, "plain": plain, "invented": bool(gr[k]["invented"]),
                      "by_judge": {w: weighted(tier, j["scores"][k], bool(gr[k]["invented"]), rf)[0] for w, j in js.items()},
                      "timing": runs[k]["timing"]}
        diffs = [abs(js["opus"]["scores"][k][p] - js["gpt"]["scores"][k][p]) for k in gr for p in DEEP["tiers"][tier]["weights"]]
        res = {"tier": tier, "setups": out, "judge_mad": round(sum(diffs) / len(diffs), 2),
               "verdicts": {w: j["raw"].get("verdict") for w, j in js.items()},
               "errors": {w: {j["labels"][l]: v for l, v in (j["raw"].get("errors") or {}).items() if l in j["labels"]} for w, j in js.items()}}
        json.dump(res, open(os.path.join(d, "results.json"), "w"), ensure_ascii=False, indent=1)
        print(f"  results {tier}: " + ", ".join(f"{k} {v['strict']}" for k, v in out.items()), flush=True)


# ---------------------------------------------------------------- screens and pdf

def stage_render(tiers, draw):
    from PIL import Image
    for tier in tiers:
        d = os.path.join(OUT, tier)
        for k in SETUPS:
            full = os.path.join(d, f"{k}_full.png")
            if not os.path.exists(full):
                render_check(os.path.join(d, f"{k}.html"), full)
            im = Image.open(full)
            im.crop((0, 0, im.width, min(im.height, 2400))).save(os.path.join(d, f"{k}_first.png"))


def _fmt_s(x):
    if x is None:
        return "—"
    return f"{x/60:.1f} min" if x >= 120 else f"{x:.0f} s"


def stage_pdf(tiers, draw):
    order = [k for k in ["claude_bare", "claude_prism", "chatgpt_bare", "chatgpt_prism"] if k in SETUPS]
    css = v2.PAGE_CSS + """
@page{size:A4;margin:13mm}.wrap{max-width:none;padding:0}.pb{page-break-before:always}
h1{font-size:28px;margin:0 0 6px}.lead{font-size:14px;color:var(--ink2);max-width:760px}
.kpis{display:grid;grid-template-columns:repeat(4,1fr);gap:10px;margin:14px 0}.kpi{background:var(--card);border-radius:8px;padding:10px}
.kpi .n{font-size:26px;font-weight:700}.kpi .l{font-size:11.5px;color:var(--ink2)}
.pair{display:grid;grid-template-columns:1fr 1fr;gap:10px}.pair img{width:100%;border:1px solid var(--line)}
.pair .h{font-weight:700;font-size:13px;margin-bottom:4px}.full img{width:100%;border:1px solid var(--line);display:block}
.small{font-size:11.5px;color:var(--ink2)} td.num{text-align:right;font-variant-numeric:tabular-nums}.hi{font-weight:700}
"""
    cas = [] if os.environ.get("BENCH_DEEP_ONLY") else json.load(open(os.path.join(v2.OUT, "pilot.json")))["slugs"]
    CR = {s: json.load(open(os.path.join(v2.OUT, s, "results.json"))) for s in cas}
    CA = {s: json.load(open(os.path.join(v2.OUT, s, "answers.json"))) for s in cas}
    DR = {t: json.load(open(os.path.join(OUT, t, "results.json"))) for t in tiers}
    DG = {t: json.load(open(os.path.join(OUT, t, "ground.json"))) for t in tiers}
    tier_name = {"policy": "Policy maker", "research": "Researcher"}

    def tool_secs(slug):
        ex = json.load(open(os.path.join(v2.EX, f"{slug}.json")))
        return sum(c.get("seconds") or 0 for c in ex["calls"])

    h = [f"<h1>{escape(os.environ.get('BENCH_TITLE') or 'Prism benchmark v2: casual users, policy makers, researchers')}</h1>"
         + (f"<div class='lead'>{escape(os.environ['BENCH_LEAD'])}</div>" if os.environ.get("BENCH_LEAD") else "") +
         ("" if os.environ.get("BENCH_LEAD") else
         f"<div class='lead'>Plain Claude and ChatGPT against the same models with Prism, on three kinds of reader. "
         f"Casual tier: two random everyday questions answered as a full report. Deep tiers: a NITI Aayog decision "
         f"briefing and a researcher's deep dive with a full article, both as interactive HTML reports with maps, "
         f"multi-dimension charts, forecasts and cross-domain analysis, on one randomly drawn topic: "
         f"<b>{escape(draw['label'])}</b>. Scoring rubric designed by Fable 5.1; script checks first, then two blind "
         f"judges (Claude Opus, GPT) who may only lower the script's ceilings. Run {TODAY}.</div>")]
    rows = []
    for s in cas:
        rows.append((f"Casual · {s}", {k: CR[s]["setups"][k]["strict"] for k in order}))
    for t in tiers:
        rows.append((f"{tier_name[t]} · deep dive", {k: DR[t]["setups"][k]["strict"] for k in order if k in DR[t]["setups"]}))
    avg = {k: round(sum(r[1].get(k, 0) for r in rows) / len(rows), 1) for k in order}
    h.append("<div class='kpis' style='grid-template-columns:repeat(%d,1fr)'>" % len(order) + "".join(f"<div class='kpi'><div class='n'>{avg[k]}</div><div class='l'>{v2.SETUPS[k]}"
                                           f"<br>mean /100 over {len(rows)} tasks</div></div>" for k in order) + "</div>")
    h.append("<table><tr><th>Task</th>" + "".join(f"<th>{v2.SETUPS[k]}</th>" for k in order) + "</tr>" + "".join(
        f"<tr><td>{escape(n)}</td>" + "".join(f"<td class='num{' hi' if r.get(k) == max(r.values()) else ''}'>{r.get(k, '—')}</td>" for k in order) + "</tr>"
        for n, r in rows) + "</table>")
    h.append("<div class='small'>Weighted 0-100 score, mean of the two judges; invention gate caps a task at 40, a page that does not render at 25.</div>")

    # timing
    h.append("<h2>Timing</h2><table><tr><th>Task</th><th>Setup</th><th>Wall clock</th><th>First output</th>"
             "<th>Tool calls</th><th>Tool time</th><th>Output size</th></tr>")
    for s in cas:
        for k in order:
            a = CA[s][k]
            tc = tool_secs(s) if k.endswith("_prism") else None
            h.append(f"<tr><td>Casual · {s}</td><td>{v2.SETUPS[k]}</td><td class='num'>{_fmt_s(a['seconds'] + (tc or 0))}</td><td class='num'>—</td>"
                     f"<td class='num'>{len(json.load(open(os.path.join(v2.EX, s + '.json')))['calls']) if tc is not None else 0}</td>"
                     f"<td class='num'>{_fmt_s(tc) if tc is not None else '—'}</td><td class='num'>{len(a['text'])//1000} k chars</td></tr>")
    for t in tiers:
        runs = json.load(open(os.path.join(OUT, t, "runs.json")))
        for k in order:
            if k not in runs:
                continue
            tm = runs[k]["timing"]
            h.append(f"<tr><td>{tier_name[t]}</td><td>{v2.SETUPS[k]}</td><td class='num'>{_fmt_s(tm['wall_seconds'])}</td>"
                     f"<td class='num'>{_fmt_s(tm['first_output_seconds'])}</td><td class='num'>{tm['tool_calls']}"
                     f"{'' if tm['tool_calls'] == tm['tool_calls_returned'] else ' (' + str(tm['tool_calls'] - tm['tool_calls_returned']) + ' unreturned)'}</td>"
                     f"<td class='num'>{_fmt_s(tm['tool_seconds_sum']) if tm['tool_calls'] else '—'}</td><td class='num'>{len(runs[k]['text'])//1000} k chars</td></tr>")
    h.append("</table><div class='small'>Casual tier: Prism setups received pre-captured tool results, so their wall clock = answer time + "
             "the original capture time of those calls. Deep tiers: Prism setups called the live MCP themselves; wall clock covers the whole "
             "session. Tool time is summed per call and can exceed wall clock when calls run in parallel. Timing is reported, not scored.</div>")

    # deep tiers
    for t in tiers:
        r, g = DR[t], DG[t]
        h.append(f"<div class='pb'></div><h1 style='font-size:24px'>{tier_name[t]} deep dive</h1>"
                 f"<div class='lead'><b>Topic:</b> {escape(draw['label'])}<br><b>Persona:</b> "
                 + escape(DEEP['tiers'][t]['prompt'].split('WHO I AM AND WHAT I NEED')[1].split('.')[0].strip()) + ".</div>")
        h.append("<table><tr><th>Parameter (0-5)</th>" + "".join(f"<th>{v2.SETUPS[k]}</th>" for k in order) + "</tr>")
        for p_, w in DEEP["tiers"][t]["weights"].items():
            vals = [r["setups"][k]["params"].get(p_, 0) for k in order]
            name = (PARAMS.get(p_) or v2.PARAMS.get(p_) or {}).get("name", p_)
            h.append(f"<tr><td>{escape(name)} <span class='small'>w{w}</span></td>" + "".join(
                f"<td class='num{' hi' if v == max(vals) else ''}'>{v}</td>" for v in vals) + "</tr>")
        h.append("<tr><td><b>Weighted /100</b></td>" + "".join(f"<td class='num hi'>{r['setups'][k]['strict']}{' ⚠' if r['setups'][k]['invented'] else ''}</td>" for k in order) + "</tr></table>")
        h.append("<h2>Script findings</h2><table><tr><th></th>" + "".join(f"<th>{v2.SETUPS[k]}</th>" for k in order) + "</tr>")
        fr = [("Numbers traced to the corpus", lambda x: f"{x['numbers']['traced']}/{x['numbers']['total']}"),
              ("Charts rendered / in manifest", lambda x: f"{x.get('render', {}).get('rendered_views')}/{x.get('render', {}).get('manifest_charts')}"),
              ("Console errors", lambda x: str(len(x.get("render", {}).get("console_errors", [])))),
              ("Maps (traced share)", lambda x: ", ".join(f"{m['traced_share']:.0%}" if m["how"] == "call" else m["how"] for m in x["deep"]["maps"]) or "none"),
              ("Forecasts (traced share)", lambda x: ", ".join(f"{f_['traced_share']:.0%}" if f_["source"].startswith("call:") else (f_["source"] or "unsourced") for f_ in x["deep"]["forecasts"]) or "none"),
              ("Chart dimensions (traced)", lambda x: str(len(x["deep"]["dimensions"]))),
              ("Corpora behind traced numbers", lambda x: ", ".join(x["deep"]["corpora_traced"]) or "none"),
              ("Cross-corpus sentences", lambda x: str(x["deep"]["connecting_sentences"])),
              ("DOIs found in 401M-work corpus", lambda x: f"{x['dois']['found_in_corpus']}/{x['dois']['cited']}"),
              ("Follow-up queries that ran", lambda x: f"{x['followups_ok']}/{len(x['followups'])}"),
              ("Invention gate", lambda x: "TRIPPED" if x["invented"] else "clear")]
        if t == "policy":
            fr.insert(8, ("Policy options table", lambda x: (lambda po: f"{po.get('rows', 0)} rows, header {'ok' if po.get('header_ok') else 'wrong'}" if po.get("present") else "missing")(x["deep"].get("policy_options", {}))))
        if t == "research":
            fr.insert(8, ("Research article", lambda x: (lambda ar: f"{ar.get('sections_found')}/7 sections, {ar.get('words')} words" if ar.get("present") else "missing")(x["deep"].get("article", {}))))
        for n, fn in fr:
            h.append(f"<tr><td>{n}</td>" + "".join(f"<td class='num'>{escape(fn(g[k]))}</td>" for k in order if k in g) + "</tr>")
        h.append("</table>")
        for w, v in r["verdicts"].items():
            h.append(f"<p><b>{'Claude Opus' if w == 'opus' else 'GPT'} judge:</b> {escape(v or '')}</p>")
        errs = {k: sorted(set(sum((r["errors"].get(w, {}).get(k) or [] for w in r["errors"]), [])))[:4] for k in order}
        h.append("<h2>Errors the judges found</h2><table>" + "".join(
            f"<tr><td style='width:140px'><b>{v2.SETUPS[k]}</b></td><td class='small'>{'<br>'.join(escape(str(e)) for e in errs[k]) or '—'}</td></tr>" for k in order) + "</table>")
        d = os.path.join(OUT, t)
        for m, mk in ((v2.RESP_LABEL, "claude"), ("ChatGPT", "chatgpt")):
            if mk + "_bare" not in SETUPS:
                continue
            h.append(f"<div class='pb'></div><h2>Before / after: {m} — {tier_name[t]} report, first screen</h2><div class='pair'>"
                     f"<div><div class='h'>BEFORE · {m} alone · {r['setups'][mk + '_bare']['strict']}/100</div><img src='file://{d}/{mk}_bare_first.png'></div>"
                     f"<div><div class='h'>AFTER · {m} + Prism · {r['setups'][mk + '_prism']['strict']}/100</div><img src='file://{d}/{mk}_prism_first.png'></div></div>")

    # casual tier summary pages reuse the pilot's pages
    for s in cas:
        r = CR[s]
        h.append(f"<div class='pb'></div><h1 style='font-size:22px'>Casual · {escape(v2.BY_SLUG[s]['question'])}</h1>")
        ps = list(r["setups"]["claude_bare"]["params"])
        h.append("<table><tr><th>Parameter (0-5)</th>" + "".join(f"<th>{v2.SETUPS[k]}</th>" for k in order) + "</tr>" + "".join(
            f"<tr><td>{v2.PARAMS[p_]['name']}</td>" + "".join(f"<td class='num'>{r['setups'][k]['params'][p_]}</td>" for k in order) + "</tr>" for p_ in ps)
            + "<tr><td><b>Weighted /100</b></td>" + "".join(f"<td class='num hi'>{r['setups'][k]['strict']}</td>" for k in order) + "</tr></table>")
        sd = os.path.join(v2.OUT, s)
        for m, mk in (("Claude", "claude"), ("ChatGPT", "chatgpt")):
            h.append(f"<h2>Before / after: {m}</h2><div class='pair'><div><div class='h'>BEFORE · {m} alone · {r['setups'][mk + '_bare']['strict']}/100</div>"
                     f"<img src='file://{sd}/{mk}_bare_first.png'></div><div><div class='h'>AFTER · {m} + Prism · {r['setups'][mk + '_prism']['strict']}/100</div>"
                     f"<img src='file://{sd}/{mk}_prism_first.png'></div></div><div class='pb'></div>")

    h.append("<h1 style='font-size:22px'>Appendix: the deep-tier HTML reports in full</h1><div class='lead'>Each report as it rendered in headless "
             "Chrome. The live HTML files are published next to this PDF.</div>")
    for t in tiers:
        for k in order:
            h.append(f"<div class='pb'></div><h2>{tier_name[t]} · {v2.SETUPS[k]} · {DR[t]['setups'][k]['strict']}/100</h2>")
            for sl in v2.slices(os.path.join(OUT, t, f"{k}_full.png"), h=1500):
                h.append(f"<div class='full'><img src='file://{sl}'></div>")
    html = (f"<!doctype html><html><head><meta charset='utf-8'><title>Prism benchmark v2</title><style>{css}</style></head>"
            f"<body><div class='wrap'>{''.join(h)}</div></body></html>")
    base = OUT if os.environ.get("BENCH_DEEP_ONLY") else v2.OUT
    hp = os.path.join(base, "prism_benchmark_v2_full.html")
    open(hp, "w").write(html)
    pp = os.path.join(base, "prism_benchmark_v2_full.pdf")
    subprocess.run([v2.CHROME, "--headless=new", "--no-sandbox", "--no-pdf-header-footer", "--allow-file-access-from-files",
                    f"--print-to-pdf={pp}", "file://" + hp], capture_output=True, timeout=600)
    print("pdf:", pp, flush=True)


# ---------------------------------------------------------------- main (stages are appended below as they are built)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", default="all")
    ap.add_argument("--tiers", default="policy,research")
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    os.makedirs(OUT, exist_ok=True)
    dp = os.path.join(OUT, "draw.json")
    if os.environ.get("BENCH_TOPIC_LABEL") and not os.path.exists(dp):
        draw = {"label": os.environ["BENCH_TOPIC_LABEL"], "chosen": "by the owner"}
        json.dump(draw, open(dp, "w"), ensure_ascii=False, indent=1)
    if os.path.exists(dp):
        draw = json.load(open(dp))
    else:
        t, label = draw_topic()
        draw = {"seed": SEED, "topic": t, "label": label, "pool": [e["slug"] for e in DEEP["topic_pool"]["entries"]]}
        json.dump(draw, open(dp, "w"), ensure_ascii=False, indent=1)
    tiers = a.tiers.split(",")
    print("topic:", draw["label"], flush=True)
    st = a.stage
    if st in ("all", "run"):
        with ThreadPoolExecutor(len(tiers)) as ex:
            list(ex.map(lambda t: run_tier(t, draw["label"], a.force), tiers))
    for name in ("ground", "judge", "render", "pdf"):
        fn = globals().get(f"stage_{name}")
        if st in ("all", name) and fn:
            fn(tiers, draw)
    print("BENCH_DEEP_DONE", flush=True)


if __name__ == "__main__":
    main()
