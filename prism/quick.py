#!/usr/bin/env python3
"""quick — a short story-article from the few most relevant papers, fast.

The backlinks method (`~/projects/backlinks/RECIPE.md`) reads ~300
abstracts per subject on the local GPU — eight minutes of reading — and then
a hand-written generator per article. It produces the eight live pieces, and
it is the right method for a 3,000-word piece with twenty citations.

This is the fast lane for a short piece, and it keeps only the two parts of
that method that matter for one: SHORTLIST the papers that are actually about
the subject, and CRAFT what they say into a story. Everything else is cut.

  resolve    the subject → the phrases the literature uses (vocabulary index,
             then one model call for the phrasings the index cannot see)
  fetch      a pool of ~100 abstract-bearing papers across the same lanes the
             long method uses (most-cited, recent, reviews, mid, PubMed trials)
  shortlist  the pool → ~12, by vector relevance to the subject. No model.
             This is the step the long method does not have — it reads
             everything and lets the read's `relevance` field sort it out.
             Here the sort happens first, so only a dozen abstracts are read.
  read       each shortlisted abstract on Cerebras, in parallel, against the
             SAME fixed template as `read_papers.py` (imported, not copied),
             with the same rule: a number the model writes that is not in the
             abstract verbatim is dropped. Off-subject reads are dropped.
             Every read is saved where the long method saves its reads
             (`data/reads/`, Mongo `prism_reads`) — a result that only lived
             in a call did not happen.
  hook       the recent dated news on the subject, for the opener
  plan       a story plan: title, hook, thread, 5-6 beats, the number to watch
  write      700-900 words in the house voice (RECIPE §6), citing sources by
             what they ARE — "a 2023 study in *Agriculture*" — with the
             publisher link, never a doi.org link
  gate       verbatim-number grounding · direction (a sentence saying
             "improved" about a read that says mixed) · machine voice ·
             a cold reader, up to two revisions

The three laws hold: the model never supplies a fact; absolute paths; save
what you analysed. A short article is not a lower standard, it is a smaller
one.
"""
from __future__ import annotations

import concurrent.futures as cf
import importlib.util
import json
import os
import re
import sys
import time

import numpy as np

from . import cache, charts, compose, llm, news, reader, vocab, writer

BACKLINKS_PIPE = os.environ.get("PRISM_BACKLINKS_PIPE", os.path.expanduser("~/pipeline/backlinks"))
BACKLINKS_DOCS = os.environ.get("PRISM_BACKLINKS_DOCS", os.path.expanduser("~/projects/backlinks"))
READS_DIR = f"{BACKLINKS_DOCS}/data/reads"
ARTICLES_DIR = f"{BACKLINKS_DOCS}/articles"
PACKS_DIR = f"{BACKLINKS_DOCS}/data"

READ_MODEL_LABEL = f"cerebras:{llm.MODEL}"
POOL_N = 120            # candidates fetched
SHORTLIST_K = 12        # abstracts actually read
MIN_SIM = 0.32          # below this a candidate is not about the subject
READ_WORKERS = 6
TARGET_WORDS = (650, 950)
MAX_REVISIONS = 2


def _log(m):
    print(f"[prism.quick] {m}", file=sys.stderr, flush=True)


# ── the long method's reading tools, imported not copied ────────────────────
def _read_papers():
    """`read_papers.py` from the backlinks pipeline: TEMPLATE, ground(), chq()."""
    spec = importlib.util.spec_from_file_location(
        "read_papers", f"{BACKLINKS_PIPE}/read_papers.py")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["read_papers"] = mod
    spec.loader.exec_module(mod)
    # A dead shard must read as a smaller pool, not as a dead pipeline. The
    # long method's URL has no skip flag, so with one index host unreachable
    # every one of its queries returned HTTP 500 and the fast lane resolved
    # zero phrases. The skip is added here, and `coverage()` reports which
    # shards answered so the payload can say the counts are floors.
    if "skip_unavailable_shards" not in mod.CH:
        mod.CH = mod.CH + "&skip_unavailable_shards=1"
    return mod


def coverage() -> dict:
    """Which shards of the research cluster answered just now."""
    try:
        rp = _read_papers()
        rows = rp.chq("SELECT host_name, errors_count FROM system.clusters WHERE cluster = 'my_cluster3'")
        down = [r["host_name"] for r in rows if int(r.get("errors_count") or 0) > 0]
        return {"shards": len(rows), "down": down, "complete": not down,
                "note": (f"{len(down)} of {len(rows)} shards unreachable — every count is a floor"
                         if down else "all shards answered")}
    except Exception as e:
        return {"shards": None, "down": None, "complete": None, "note": f"coverage unknown ({type(e).__name__})"}


def _resolve_doi(doi: str) -> str:
    """Publisher page for a DOI, through the backlinks resolver and its cache.
    A doi.org link fails the audit; if the resolver is unavailable the raw
    link is returned and the payload says so."""
    try:
        spec = importlib.util.spec_from_file_location("visuals", f"{BACKLINKS_PIPE}/visuals.py")
        v = importlib.util.module_from_spec(spec)
        sys.modules.setdefault("visuals", v)
        spec.loader.exec_module(v)
        return v.resolve_doi(doi)
    except Exception as e:
        _log(f"doi resolve failed for {doi}: {type(e).__name__}")
        return f"https://doi.org/{doi}"


# ── 1. resolve ───────────────────────────────────────────────────────────────
_PHRASE_SYS = (
 "A subject is being searched in the titles of scientific papers. Give the "
 "phrases the LITERATURE uses for it — not the subject's own words, theirs: "
 "the terms that appear in paper titles. Return JSON "
 '{"phrases": [str], "health": bool}. 6-10 phrases, each 2-4 words, no '
 "single words (a bare word pulls in unrelated papers). `health` is true if "
 "this is a medical or public-health subject.")


_PLACE = re.compile(r"\s+(?:in|across|for|of)\s+(india|indian|delhi|mumbai|bengaluru|bangalore|chennai|kolkata|hyderabad|"
                    r"pune|uttar pradesh|bihar|kerala|gujarat|maharashtra|karnataka|tamil nadu|europe|the eu|"
                    r"china|the us|the united states|america|africa|asia|the uk|britain|south asia)\s*$", re.I)


def resolve(subject: str, model: str | None = None) -> dict:
    """Search phrases for the subject, validated by title counts.

    The place is split off for the research lane: papers are titled "EV
    charging infrastructure", not "EV charging infrastructure in India" — the
    first run matched nothing and the pool was empty. The place stays on the
    subject for the news lane, where it is what the reader asked about."""
    m = _PLACE.search(subject)
    head = _PLACE.sub("", subject).strip() if m else subject
    place = m.group(1) if m else None
    r = vocab.resolve(head, k=6, min_sim=0.5, vocabs=["prism_keywords", "mesh", "oa_topics"])
    vocs = r.get("vocabularies", {})
    mesh = [x["label"] for x in (vocs.get("mesh") or {}).get("matches", []) if x["similarity"] >= 0.6]
    kw = [x["label"] for x in (vocs.get("prism_keywords") or {}).get("matches", [])
          if x["similarity"] >= 0.55 and 2 <= len(x["label"].split()) <= 4]
    # the phrasings the index cannot see — low effort, because the fast model
    # spends a medium budget on reasoning and returns nothing (seen live)
    got = llm.call_json(_PHRASE_SYS, f"SUBJECT: {head}", max_tokens=900, effort="low") or {}
    if not got.get("phrases"):
        alt = writer.compose(_PHRASE_SYS + " Return ONLY the JSON object.", f"SUBJECT: {head}",
                             max_tokens=600, model=model, effort="low")
        got = llm._parse(alt.get("text") or "") or {}
    model_phrases = [str(x).strip() for x in (got.get("phrases") or []) if 2 <= len(str(x).split()) <= 5]
    health = bool(got.get("health")) or bool(mesh)
    cands = []
    for x in [head] + kw + model_phrases:
        x = re.sub(r"\s+", " ", x.strip().lower())
        if len(x.split()) >= 2 and x not in cands:
            cands.append(x)
    rp = _read_papers()
    counts = {}
    for x in cands[:16]:
        try:
            n = rp.chq(f"SELECT count() AS n FROM openalex.works_distributed "
                       f"WHERE positionCaseInsensitive(title, {rp.sql_arr([x])[1:-1]}) > 0 "
                       f"AND publication_year BETWEEN 2005 AND 2025")[0]["n"]
        except Exception:
            n = 0
        counts[x] = int(n)
    phrases = [x for x in cands if 5 <= counts.get(x, 0) <= 400000]
    if not phrases:
        phrases = [x for x in cands if counts.get(x, 0) > 0] or [head.lower()]
    return {"subject": subject, "head": head, "place": place, "phrases": phrases[:10],
            "health": health, "mesh": mesh[:4], "phrase_counts": counts}


# ── 2. fetch ─────────────────────────────────────────────────────────────────
def fetch(phrases: list, health: bool, n: int = POOL_N) -> list:
    rp = _read_papers()
    m = f"multiSearchAnyCaseInsensitive(title, {rp.sql_arr(phrases)})"
    per = max(n // 4, 15)
    lanes = [
        ("cited", "publication_year BETWEEN 2005 AND 2025", "cited_by_count DESC", per),
        ("recent", "publication_year BETWEEN 2022 AND 2025", "publication_date DESC, cited_by_count DESC", per),
        ("reviews", "publication_year BETWEEN 2010 AND 2025 AND (work_type = 'review' OR "
                    "positionCaseInsensitive(title, 'review') > 0 OR "
                    "positionCaseInsensitive(title, 'meta-analysis') > 0)", "cited_by_count DESC", per),
        ("mid", "publication_year BETWEEN 2015 AND 2021", "cited_by_count DESC", per),
    ]
    seen, docs = set(), []
    for lane, yr, order, lim in lanes:
        try:
            rows = rp.chq(
                f"SELECT openalex_id AS id, title, abstract, authors, publication_year AS year, "
                f"cited_by_count AS cites, doi, work_type AS type, venue_name AS venue "
                f"FROM openalex.works_distributed WHERE {m} AND length(abstract) > 300 "
                f"AND title != '' AND {yr} ORDER BY {order} LIMIT {lim}")
        except Exception as e:
            _log(f"lane {lane} failed: {e}")
            rows = []
        for r in rows:
            if r["id"] in seen:
                continue
            seen.add(r["id"]); r["lane"] = lane; docs.append(r)
    if health:
        for lane, pt in (("pubmed-trial", "Randomized Controlled Trial"),
                         ("pubmed-meta", "Meta-Analysis")):
            try:
                rows = rp.chq(
                    f"SELECT concat('pmid:', toString(pmid)) AS id, title, abstract, authors, "
                    f"pub_year AS year, 0 AS cites, doi, article_types AS type, journal AS venue "
                    f"FROM ncbi.pubmed_articles_distributed WHERE {m} AND length(abstract) > 300 "
                    f"AND has(article_types, '{pt}') AND pub_year BETWEEN 2015 AND 2026 "
                    f"ORDER BY pub_year DESC LIMIT {per // 2}")
            except Exception as e:
                _log(f"lane {lane} failed: {e}")
                rows = []
            for r in rows:
                if r["id"] in seen:
                    continue
                seen.add(r["id"]); r["lane"] = lane; docs.append(r)
    _log(f"pool {len(docs)} across lanes")
    return docs


# ── 3. shortlist ─────────────────────────────────────────────────────────────
def shortlist(subject: str, phrases: list, docs: list, k: int = SHORTLIST_K) -> list:
    """The k papers most about the subject, by vector similarity, with lane
    diversity so the piece is not twelve most-cited reviews.

    The subject is embedded together with its phrases; each paper as its
    title plus the opening of its abstract. Cosine on the same encoder the
    vocabulary index uses. A small citation bonus breaks ties toward work
    the field has read; it never outranks relevance."""
    if not docs:
        return []
    q = vocab.embed([subject + " ; " + " ; ".join(phrases)])[0]
    texts = [f"{d['title']}. {(d.get('abstract') or '')[:400]}" for d in docs]
    M = vocab.embed(texts)
    sims = M @ q
    for d, s in zip(docs, sims):
        c = float(d.get("cites") or 0)
        d["sim"] = float(s)
        d["score"] = float(s) + min(np.log1p(c) / 60.0, 0.08)
    live = [d for d in docs if d["sim"] >= MIN_SIM]
    live.sort(key=lambda d: -d["score"])
    # diversity: at least two recent, two review/meta, two PubMed designs
    want = {"recent": 2, "reviews": 2, "pubmed-trial": 1, "pubmed-meta": 1}
    chosen, ids = [], set()
    for lane, need in want.items():
        for d in [x for x in live if x["lane"] == lane][:need]:
            if d["id"] not in ids:
                chosen.append(d); ids.add(d["id"])
    for d in live:
        if len(chosen) >= k:
            break
        if d["id"] not in ids:
            chosen.append(d); ids.add(d["id"])
    chosen.sort(key=lambda d: -d["score"])
    _log(f"shortlist {len(chosen)} of {len(live)} live (pool {len(docs)}); "
         f"sim range {chosen[-1]['sim']:.2f}-{chosen[0]['sim']:.2f}" if chosen else "shortlist empty")
    return chosen[:k]


# ── 4. read on Cerebras ──────────────────────────────────────────────────────
def _read_one(rp, subject: str, d: dict) -> dict | None:
    prompt = rp.TEMPLATE.format(subject=subject, title=d["title"], year=d.get("year"),
                                abstract=(d.get("abstract") or "")[:3500])
    t0 = time.time()
    r = llm.call_json("You are reading one scientific abstract against a fixed template.",
                      prompt, max_tokens=900, effort="low")
    if not isinstance(r, dict):
        return None
    r = rp.ground(r, d.get("abstract") or "")
    r.update(id=d["id"], title=d["title"], year=d.get("year"), cites=d.get("cites"),
             doi=(d.get("doi") or "").replace("https://doi.org/", "") or None,
             venue=d.get("venue"), lane=d.get("lane"), sim=round(d.get("sim", 0), 3),
             model=READ_MODEL_LABEL, seconds=round(time.time() - t0, 1),
             template_version=rp.TEMPLATE_VERSION,
             read_at=time.strftime("%Y-%m-%dT%H:%M:%S"))
    return r


def read(subject: str, slug: str, docs: list) -> list:
    rp = _read_papers()
    reads = []
    with cf.ThreadPoolExecutor(max_workers=READ_WORKERS) as ex:
        futs = {ex.submit(_read_one, rp, subject, d): d for d in docs}
        for f in cf.as_completed(futs):
            try:
                r = f.result()
            except Exception as e:
                _log(f"read failed: {type(e).__name__}: {e}")
                r = None
            if r:
                reads.append(r)
    on = [r for r in reads if r.get("relevance") != "off_subject"]
    _log(f"read {len(reads)} · on-subject {len(on)} · "
         f"{sum(len(r.get('key_numbers') or []) for r in on)} verified figures")
    # save what was analysed — same files and store as the long method
    try:
        os.makedirs(READS_DIR, exist_ok=True)
        with open(f"{READS_DIR}/{slug}.reads.jsonl", "w") as fh:
            for r in reads:
                fh.write(json.dumps(dict(r, slug=slug, subject=subject),
                                    ensure_ascii=False, default=str) + "\n")
        json.dump({"slug": slug, "subject": subject, "n": len(docs), "read": len(reads),
                   "on_subject": len(on), "model": READ_MODEL_LABEL, "lane": "quick"},
                  open(f"{READS_DIR}/{slug}.meta.json", "w"), indent=1)
    except Exception as e:
        _log(f"could not write reads: {e}")
    try:
        db = rp.mongo()
        if db is not None:
            col = db.paper_reads
            by_id = {d["id"]: d for d in docs}
            for r in reads:
                d = by_id.get(r["id"], {})
                col.replace_one({"slug": slug, "id": r["id"], "template_version": rp.TEMPLATE_VERSION},
                                dict(r, slug=slug, subject=subject, authors=d.get("authors"),
                                     abstract=d.get("abstract")), upsert=True)
    except Exception as e:
        _log(f"mongo save skipped: {type(e).__name__}")
    return on


# ── 5. news hook ─────────────────────────────────────────────────────────────
_GENERIC_TAIL = {"infrastructure", "systems", "system", "technology", "technologies", "sector",
                 "industry", "market", "policy", "policies", "development", "management", "issues"}


def hook(subject: str, head: str | None = None, place: str | None = None) -> dict:
    """Recent dated news on the subject, for the opener.

    The feed matches the whole phrase, so "electric vehicle charging
    infrastructure in India" found nothing while "electric vehicle charging"
    with country=India found Delhi's record expansion and Tata Power's
    60,000 home chargers. The place becomes a country filter; the term is
    tried whole, then without its generic tail, then as its first three
    words, and the first form with at least three records wins."""
    head = head or subject
    words = head.lower().split()
    trimmed = [w for w in words if w not in _GENERIC_TAIL]
    tries = []
    for t in (head, " ".join(trimmed), " ".join(words[:3]), " ".join(trimmed[:2])):
        t = t.strip()
        if t and t not in tries and len(t.split()) >= 2:
            tries.append(t)
    # last resort: the one long content word ("groundwater") — two-word forms
    # of "groundwater depletion" found nothing in the feeds while the word did
    longest = max(trimmed, key=len) if trimmed else ""
    if len(longest) >= 8 and longest not in tries:
        tries.append(longest)
    out = {"term": head, "place": place, "records": [], "series": None, "tried": []}
    for t in tries:
        for country in ([place, None] if place else [None]):
            try:
                r = news.recent_news(t, limit=10, min_priority=6, country=country)
                recs = (r.get("articles") or []) if isinstance(r, dict) else []
            except Exception as e:
                _log(f"news hook failed ({t!r}, {country}): {type(e).__name__}: {e}"); recs = []
            out["tried"].append({"term": t, "country": country, "n": len(recs)})
            if len(recs) >= 3:
                out["term"] = t; out["country"] = country
                for a in recs[:6]:
                    pub = a.get("publisher") or a.get("source") or a.get("domain") or ""
                    date = str(a.get("date") or a.get("datetime") or "")[:10]
                    out["records"].append({
                        "publisher": pub, "date": date, "title": a.get("title"),
                        "url": a.get("url"), "lede": (a.get("lede") or a.get("text") or "")[:500],
                        "cite": f"[{pub}, {date}]({a.get('url')})" if a.get("url") else None})
                break
        if out["records"]:
            break
    try:
        t = news.trends(out["term"], granularity="quarterly", since="2023-01-01",
                        **({"country": out.get("country")} if out.get("country") else {}))
        pts = t.get("series") or t.get("points") or []
        if pts:
            out["series"] = [{"label": str(p.get("period") or p.get("label") or p.get("date"))[:7],
                              "value": int(p.get("articles") or p.get("count") or p.get("value") or 0)}
                             for p in pts][-10:]
    except Exception as e:
        _log(f"news series failed: {type(e).__name__}")
    return out


# ── 6. charts ────────────────────────────────────────────────────────────────
_DIR_LABEL = {"improved": "improved", "worsened": "worsened", "no_change": "no change",
              "mixed": "mixed", "not_applicable": "not measured"}
_DESIGN_LABEL = {"rct": "randomised trial", "meta_analysis": "meta-analysis",
                 "systematic_review": "systematic review", "cohort": "cohort",
                 "case_control": "case-control", "cross_sectional": "cross-sectional",
                 "modelling": "modelling", "lab_experiment": "lab experiment",
                 "qualitative": "qualitative", "narrative_review": "narrative review",
                 "guideline": "guideline", "other": "other"}


def make_charts(subject: str, reads: list, hk: dict, slug: str) -> list:
    out = []
    designs = {}
    for r in reads:
        k = _DESIGN_LABEL.get(r.get("study_design") or "other", "other")
        designs[k] = designs.get(k, 0) + 1
    if designs:
        pts = sorted(designs.items(), key=lambda x: -x[1])
        spec = {"kind": "bars", "title": "What kind of studies these are",
                "subtitle": f"The {len(reads)} papers read on {subject}, by study design.",
                "source": f"Fliar BI · Prism · {len(reads)} abstracts reviewed",
                "alt": "Bar chart of study designs: " + ", ".join(f"{k} {v}" for k, v in pts),
                "points": [{"label": k[:16], "value": v} for k, v in pts],
                "highlight": [k[:16] for k, _ in pts if k in ("randomised trial", "meta-analysis")]}
        try:
            out.append(_chart(spec, f"{slug}-designs"))
        except Exception as e:
            _log(f"chart failed: {e}")
    if hk.get("series") and len(hk["series"]) >= 4:
        s = hk["series"]
        spec = {"kind": "bars", "title": "How much news there is",
                "subtitle": f"Articles mentioning {hk.get('term')}, by quarter. The last quarter is partial.",
                "source": "Fliar BI · Prism news corpus · 2023 to the latest quarter",
                "alt": "Bar chart of news volume by quarter: " + ", ".join(f"{p['label']} {p['value']}" for p in s),
                "points": [{"label": p["label"], "value": p["value"]} for p in s],
                "highlight": [s[-1]["label"]]}
        try:
            out.append(_chart(spec, f"{slug}-news"))
        except Exception as e:
            _log(f"chart failed: {e}")
    return out


def _chart(spec: dict, slug: str) -> dict:
    pub = charts.publish(spec, slug=slug)
    if not pub.get('verified'):
        raise RuntimeError(pub.get('upload_error') or 'chart delivery not verified')
    light = pub["images"]["light"]["url"]
    return {"slug": pub["slug"], "title": spec["title"], "points": spec["points"],
            "alt": spec["alt"], "url": light,
            "dark": pub["images"].get("dark", {}).get("url"),
            "markdown": f"![{spec['title']}]({light})"}


# ── 6b. illustrations, drawn by Codex ───────────────────────────────────────
CODEX_BIN = os.environ.get("PRISM_CODEX_BIN", os.path.expanduser("~/.nvm/versions/node/v22.19.0/bin/codex"))
CODEX_IMAGE_MODEL = os.environ.get("PRISM_CODEX_IMAGE_MODEL", "gpt-5.6-terra")
CODEX_IMG_DIR = os.path.expanduser("~/.codex/generated_images")
def _house_style() -> str:
    """The exact prompt suffix the backlinks illustrations use, so the two
    families of images look like one hand."""
    try:
        spec = importlib.util.spec_from_file_location("visuals", f"{BACKLINKS_PIPE}/visuals.py")
        v = importlib.util.module_from_spec(spec); sys.modules.setdefault("visuals", v); spec.loader.exec_module(v)
        return v.HOUSE
    except Exception:
        return ("sketchbook drawing: loose black ink pen lines, visible pencil construction marks, "
                "light watercolor wash in two muted colours, one scene, no text, no logos")
STORY_IMG_LOCAL = os.path.join(BACKLINKS_DOCS, "data", "story_images")


def illustrate_codex(scene: str, slug: str, timeout: int = 300) -> dict | None:
    """One house-style illustration from the Codex CLI's image tool.

    The backlinks pieces draw theirs with FLUX on Together; this uses the
    ChatGPT account instead, which costs no API credit. Codex writes the file
    under ~/.codex/generated_images/<session>/ and cannot always copy it out
    of its sandbox, so the newest PNG written after the call started is taken
    as the result, copied beside the other story images and uploaded to the
    same fliarbi path the long pieces use."""
    import glob, shutil, subprocess, tempfile
    os.makedirs(STORY_IMG_LOCAL, exist_ok=True)
    t0 = time.time()
    prompt = (f"Use your image generation tool to create ONE image: {scene}. {_house_style()} "
              f"No real or identifiable people, no politicians, no faces of public figures, no brand "
              f"names. Landscape, 16:9. Do not write any file; just generate the image and reply 'done'.")
    prompt += " In your final reply, give the full path of the generated image file."
    src = None
    with tempfile.TemporaryDirectory(prefix="prism-codex-img-") as d:
        last = os.path.join(d, "last.txt")
        cmd = [CODEX_BIN, "exec", "-m", CODEX_IMAGE_MODEL, "-C", d, "-s", "read-only",
               "--ephemeral", "--skip-git-repo-check", "-c", "model_reasoning_effort=\"low\"",
               "-o", last, "-"]
        try:
            r = subprocess.run(cmd, input=prompt, capture_output=True, text=True, timeout=timeout)
        except subprocess.TimeoutExpired:
            _log("codex image: timeout"); return None
        blob = (open(last).read() if os.path.exists(last) else "") + (r.stdout or "") + (r.stderr or "")
        # Codex names the file it wrote; take that, not "the newest file" —
        # two parallel calls once both picked the same newest picture.
        for m in re.finditer(r"(/[^\s`'\"]+/generated_images/[^\s`'\"]+\.png)", blob):
            if os.path.exists(m.group(1)):
                src = m.group(1); break
    if not src:
        fresh = [f for f in glob.glob(f"{CODEX_IMG_DIR}/*/*.png") if os.path.getmtime(f) >= t0 - 2]
        if not fresh:
            _log("codex image: no file produced"); return None
        src = max(fresh, key=os.path.getmtime)
    import hashlib
    h = hashlib.sha1(open(src, "rb").read()).hexdigest()[:10]
    dst = f"{STORY_IMG_LOCAL}/{slug}-{h}.png"
    shutil.copy(src, dst)
    url = None
    try:
        spec = importlib.util.spec_from_file_location("visuals", f"{BACKLINKS_PIPE}/visuals.py")
        v = importlib.util.module_from_spec(spec); sys.modules.setdefault("visuals", v); spec.loader.exec_module(v)
        url = v._upload(dst, "story")
    except Exception as e:
        _log(f"codex image upload failed: {type(e).__name__}: {e}")
    return {"slug": slug, "scene": scene, "path": dst, "url": url,
            "markdown": f"![{scene[:80]}]({url})" if url else None,
            "model": CODEX_IMAGE_MODEL, "seconds": round(time.time() - t0, 1)}


PLACE_CUE = (" The scene is set in {place}: local architecture, local vehicles, local dress, the light "
             "and street furniture of {place} — unmistakably {place}, with no text or signage.")


def make_images(story: dict, slug: str, place: str | None = None) -> list:
    """The plan's `images` (hero + up to one more), drawn in parallel."""
    wants = [i for i in (story.get("images") or []) if i.get("scene")][:2]
    if not wants:
        # the planner omitted scenes: ask the writer for two, from the plan
        got = llm.call_json(
            "From this story plan, describe TWO concrete scenes an illustrator could draw — a place, "
            "an ordinary person doing a thing, an object — one for the opening and one for a later "
            "section. Never a named or real person, never a politician or official. "
            'Return JSON {"images": [{"where": "hero", "scene": str}, {"where": "<beat heading>", "scene": str}]}. '
            "No text or numbers in the scenes.",
            json.dumps({k: story.get(k) for k in ("title", "hook", "thread", "beats")}, ensure_ascii=False)[:6000],
            max_tokens=600, effort="low") or {}
        wants = [i for i in (got.get("images") or []) if isinstance(i, dict) and i.get("scene")][:2]
    if not wants:
        return []
    out = []
    # A scene with no place cue comes back as a European boulevard or a
    # suburban American lot — seen twice. The place goes into every scene.
    if place:
        for w in wants:
            w["scene"] = w["scene"].rstrip(".") + "." + PLACE_CUE.format(place=place)
    with cf.ThreadPoolExecutor(max_workers=1) as ex:      # sequential: see illustrate_codex
        futs = {ex.submit(illustrate_codex, w["scene"], f"{slug}-{w.get('where', 'hero')[:24]}".lower().replace(" ", "-")): w
                for w in wants}
        for f in cf.as_completed(futs):
            w = futs[f]
            try:
                r = f.result()
            except Exception as e:
                _log(f"image failed: {e}"); r = None
            if r and r.get("url"):
                r["where"] = w.get("where") or "hero"; out.append(r)
    return out


# ── 7. plan and write ────────────────────────────────────────────────────────
_HOUSE = (
 "HOUSE RULES — each one came from a rejected draft:\n"
 "1. Start with the news, dated and linked, in the first sentence. The person, "
 "the date, the thing that happened. Never 'In today's world'. If there is no "
 "news record, open with the single most surprising finding, as a scene.\n"
 "2. Plain language for non-professionals. Explain every term the first time "
 "it appears, in the same sentence: 'a meta-analysis — a study that gathers "
 "every earlier study on a question and weighs them together'.\n"
 "3. One number per sentence. Short sentences. One idea per paragraph. The "
 "writer's own thread ('here is the part that surprised me').\n"
 "4. Every study is described from ITS OWN read: what it did, on how many, what "
 "came out. Cite it by pasting its `cite` string EXACTLY as given — never a "
 "surname, never 'X and colleagues', never a made-up link. At most one "
 "citation per paragraph, only where a reader would want to check.\n"
 "5. Direction matters more than the number. If the read says mixed, "
 "no_change or worsened, the sentence says so. Never turn a mixed result into "
 "an improvement.\n"
 "6. Say what the evidence cannot show, once, in plain words: 'not one of "
 "these is a randomised trial', 'a correlation is not a cause'.\n"
 "7. No marketing voice, no machine voice. Never 'retrieved', 'corpus', 'the "
 "papers I found', 'the data shows', 'the evidence does not cover'. You are a "
 "person telling a friend what you learned.\n"
 "8. Headings are the story ('The click that costs you the viewer'), never a "
 "template ('Introduction', 'Findings').\n"
 "9. Absolutes ('not one', 'every', 'no study') only about the papers read, "
 "and only when the material shows it.\n"
 "10. End with 'The number to watch': one measured thing the reader can check "
 "next season.\n"
 "11. Write NO number that is not in the material — not rounded, not "
 "converted. Name NO person, company or place that is not in the material. No "
 "Dr/Prof, no he/she for a researcher.\n"
 "12. Charts: where the plan places one, put its markdown line on its own "
 "line exactly as given, introduce it with one plain sentence.\n"
 "13. Do NOT write a Sources section or a method line — they are added after.\n\n"
 "THE SHAPE OF A PARAGRAPH, shown once. Not this:\n"
 "  'A meta-analysis of 43 studies found a pooled mean of 56.98 particles per litre [cite].'\n"
 "But this:\n"
 "  'How much plastic is in a glass of tap water depends entirely on whose tap. Pool "
 "every measurement published so far — 43 studies, weighed together in a 2025 "
 "meta-analysis — and the average comes to 56.98 particles per litre [cite]. Average is "
 "the wrong word for it, though, because the studies disagree by a factor of a "
 "thousand, and the next section is about why.'\n"
 "The idea comes first, in the writer's voice; the study is the evidence for it; the "
 "paragraph hands the reader to the next one. A section is two to four such paragraphs.")

_PLAN_SYS = (
 "You are planning a SHORT piece (700-900 words) for a curious non-specialist "
 "from the material below: a few dated news records and a dozen papers, each "
 "read against a fixed checklist. You are not writing yet.\n\n"
 "Return JSON:\n{\n"
 ' "title": str,          // a sentence a person would say, not a category\n'
 ' "about": str,          // one plain sentence\n'
 ' "hook": str,           // the opener: which news record (by its cite) or which finding, and how it is told\n'
 ' "thread": str,         // the one question the piece carries from the hook to the end\n'
 ' "beats": [{"heading": str, "idea": str, "uses": [str], "chart": str|null, "raises": str}],\n'
 "                        // 5-6. `uses` = cite strings of the reads/news this beat draws on. `raises` = the question the next beat answers. The last beat is 'The number to watch'.\n"
 ' "cannot_show": str,    // the one honest limit of this set of papers, in plain words\n'
 ' "terms": [{"term": str, "plain": str}]\n'
 "}\n" + _HOUSE)

_WRITE_SYS = (
 "Write the piece the PLAN describes, from the MATERIAL, for a curious "
 "non-specialist reading on a phone. Begin with the plan's title as a markdown "
 "H1. Open with the hook. EVERY beat in the plan becomes a section under a "
 "'## ' heading in the plan's words — a piece without section headings is "
 "wrong. Inside a section, each paragraph carries ONE idea and uses a study "
 "as evidence for it; never open a paragraph with 'A study…', 'Another "
 "study…', 'A review…' — say the idea, then the evidence. "
 "the first sentence of each section answers the question the previous one "
 "raised. Say `cannot_show` once, where it belongs. Use `terms` the first "
 "time each appears. Length 700-900 words.\n\n" + _HOUSE)

_REVISE_SYS = (
 "A reader read your draft cold and reported what happened to them, and the "
 "checks found what is listed. Rewrite the whole piece so that reader would "
 "not have had those problems and the checks are clean. You may cut, reorder, "
 "re-explain and re-open. You may NOT add a number, a name or a source that "
 "is not in the MATERIAL. Keep the length. Return the whole piece.\n\n" + _HOUSE)


_ALIAS = {"uk": "United Kingdom Britain British", "u.k.": "United Kingdom",
          "usa": "United States America American", "us": "United States", "u.s.": "United States",
          "eu": "European Union Europe European", "uae": "United Arab Emirates",
          "prc": "China Chinese", "roc": "Taiwan"}


def _aliases(material: dict) -> str:
    """The long forms of abbreviations a read's `setting` may carry, so the
    name gate does not flag 'United Kingdom' against a source that says UK."""
    out = []
    for p in material.get("papers") or []:
        st = str(p.get("setting") or "").lower()
        for k, v in _ALIAS.items():
            if re.search(rf"\b{re.escape(k)}\b", st):
                out.append(v)
    return " ".join(out)


def _material(reads: list, hk: dict, chart_list: list) -> dict:
    papers = []
    for r in reads:
        papers.append({
            "cite": r["cite"], "title": r.get("title"), "venue": r.get("venue"), "year": r.get("year"),
            "design": _DESIGN_LABEL.get(r.get("study_design") or "other", "other"),
            "sample_n": r.get("sample_n"), "sample_unit": r.get("sample_unit"),
            "setting": r.get("setting"), "intervention": r.get("intervention"),
            "outcome_direction": r.get("outcome_direction"),
            "stance": r.get("stance"), "main_finding": r.get("main_finding"),
            "key_numbers": r.get("key_numbers") or [],
            "limitation": r.get("limitation"), "times_cited": r.get("cites")})
    return {"news": hk.get("records") or [], "papers": papers,
            "charts": [{"slug": c["slug"], "title": c["title"], "markdown": c["markdown"],
                        "points": c["points"]} for c in chart_list],
            "counts": {}}


def _counts(reads: list) -> dict:
    designs, dirs = {}, {}
    for r in reads:
        k = _DESIGN_LABEL.get(r.get("study_design") or "other", "other")
        designs[k] = designs.get(k, 0) + 1
        d = _DIR_LABEL.get(r.get("outcome_direction") or "not_applicable", "not measured")
        dirs[d] = dirs.get(d, 0) + 1
    return {"papers_read": len(reads), "designs": designs, "directions": dirs,
            "strong_designs": sum(v for k, v in designs.items()
                                  if k in ("randomised trial", "meta-analysis", "systematic review"))}


def plan(subject: str, material: dict, model: str | None = None) -> dict:
    got = writer.compose(_PLAN_SYS, f"SUBJECT: {subject}\n\nMATERIAL:\n"
                         f"{json.dumps(material, ensure_ascii=False)[:40000]}",
                         max_tokens=5000, model=model, effort="medium")
    p = llm._parse(got.get("text") or "") or {}
    p["planned_by"] = got.get("model")
    return p


_BEAT_SYS = (
 "You are writing ONE section of a short piece for a curious non-specialist. "
 "You are given the section's heading, the one idea it exists to deliver, "
 "the question the previous section left hanging (your FIRST sentence "
 "answers it), the question this section must leave for the next one (your "
 "LAST sentence raises it), and the two or three sources you may use.\n\n"
 "Write 2-3 paragraphs, 80-150 words in all. No heading — it is added. Each "
 "paragraph: the idea first, in your own voice, then the study as the "
 "evidence for it, then a sentence that moves the reader on. Answer the "
 "hanging question in your first sentence WITHOUT restating it; raise the "
 "next one at the end as a statement or a question, once, in fresh words — "
 "never copy the question text you were given. Never begin a "
 "paragraph or a sentence with 'A study', 'Another study', 'A review', 'The "
 "study', 'Research shows'. One number per sentence. Explain a technical "
 "term in the sentence that uses it. Cite a source by pasting its `cite` "
 "string exactly, at most once per paragraph. Use ONLY the sources given; "
 "write NO number and NO name that is not in them. If a source's "
 "outcome_direction is mixed, no_change or worsened, say so plainly. No "
 "'retrieved', 'corpus', 'the data', 'the material'. Return the prose only.")

_OPENER_SYS = (
 "You are writing the OPENING of a short piece for a curious non-specialist. "
 "Start with the news: the date, the publisher, what happened to whom — told "
 "in 2-3 short paragraphs the way a person tells it, from the record's own "
 "words, with the record's `cite` string pasted exactly once. Never 'In "
 "today's world'. If no news record is given, open on the single most "
 "surprising finding as a scene, citing its source once. Explain any "
 "technical term in the sentence that uses it. End by raising the question "
 "the rest of the piece answers (given as RAISES). 80-140 words. No "
 "heading. Return the prose only.")


def _beat_sources(beat: dict, material: dict) -> list:
    uses = set(beat.get("uses") or [])
    pool = material["papers"] + material["news"]
    picked = [x for x in pool if x.get("cite") in uses]
    if not picked:
        # the plan named nothing usable: give the beat the three strongest papers
        picked = sorted(material["papers"], key=lambda x: -(x.get("times_cited") or 0))[:3]
    return picked[:4]


def _one_beat(sysm: str, user: str, model: str | None) -> dict:
    """A beat, with one retry: the fast model's reasoning can consume the
    whole budget and return nothing, and a piece then ends on a bare
    heading. Low effort and a generous cap first; a bigger cap on retry."""
    for cap, eff in ((2500, "low"), (4000, "low")):
        try:
            got = writer.compose(sysm, user, max_tokens=cap, model=model, effort=eff)
        except Exception as e:
            _log(f"beat failed: {type(e).__name__}: {e}")
            got = {}
        if (got.get("text") or "").strip():
            return got
    return {"text": ""}


def _run_beats(jobs_: list, model: str | None) -> dict:
    out = {}
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        futs = {ex.submit(_one_beat, sysm, user, model): name for name, sysm, user in jobs_}
        for f in cf.as_completed(futs):
            out[futs[f]] = f.result()
    return out


def write(subject: str, story: dict, material: dict, model: str | None = None) -> dict:
    """The piece, one beat at a time, in parallel, then joined.

    A single call that hands a model twelve findings and a page of rules
    produces a list of the twelve findings — every fast model did, every
    time. A call that hands it one idea, one question to answer, one to
    raise, and three sources produces a paragraph. So the plan is executed
    beat by beat; the reader loop then judges the whole."""
    beats = [b for b in (story.get("beats") or []) if b.get("heading")]
    if not beats:
        got = writer.compose(_WRITE_SYS, f"SUBJECT: {subject}\n\nPLAN:\n{json.dumps(story, ensure_ascii=False)}"
                             f"\n\nMATERIAL:\n{json.dumps(material, ensure_ascii=False)[:40000]}",
                             max_tokens=9000, model=model, effort="medium")
        return got
    terms = story.get("terms") or []
    news = material.get("news") or []
    jobs_ = []
    # opener
    opener_src = news[:3] if news else sorted(material["papers"], key=lambda x: -(x.get("times_cited") or 0))[:2]
    jobs_.append(("opener", _OPENER_SYS,
                  f"SUBJECT: {subject}\nHOOK (from the plan): {story.get('hook')}\n"
                  f"RAISES: {story.get('thread') or beats[0].get('idea')}\n"
                  f"TERMS TO EXPLAIN HERE, each in the sentence that first uses it: {json.dumps(terms, ensure_ascii=False)}\n"
                  f"SOURCES:\n{json.dumps(opener_src, ensure_ascii=False)}"))
    prev_raises = story.get("thread") or ""
    for i, b in enumerate(beats):
        srcs = _beat_sources(b, material)
        chart = next((c for c in material.get("charts") or [] if c.get("slug") == b.get("chart")), None)
        user = (f"SUBJECT: {subject}\nHEADING: {b['heading']}\nTHE IDEA: {b.get('idea')}\n"
                f"ANSWER FIRST: {prev_raises}\nRAISE AT THE END: {b.get('raises') or 'nothing — this is the last section'}\n"
                f"TERMS ALREADY EXPLAINED IN THE OPENING (use them, do not explain them again): "
                f"{', '.join(t.get('term', '') for t in terms)}\n"
                + (f"CANNOT SHOW (say it here, once, plainly): {story.get('cannot_show')}\n" if i == len(beats) - 2 and story.get("cannot_show") else "")
                + (f"CHART (put this line on its own line after the paragraph that introduces it): {chart['markdown']}\n" if chart else "")
                + f"SOURCES:\n{json.dumps(srcs, ensure_ascii=False)}")
        jobs_.append((f"beat{i+1}", _BEAT_SYS, user))
        prev_raises = b.get("raises") or prev_raises
    out = _run_beats(jobs_, model)
    return _assemble(story, out, jobs_, subject)


def _assemble(story: dict, out: dict, jobs_: list, subject: str) -> dict:
    beats = [b for b in (story.get("beats") or []) if b.get("heading")]
    images = story.get("_images") or []
    hero = next((i for i in images if (i.get("where") or "hero") == "hero"), None)
    parts = [f"# {story.get('title') or subject}", ""]
    if hero:
        parts += [hero["markdown"], ""]
    parts.append((out.get("opener") or {}).get("text", "").strip())
    for i, b in enumerate(beats):
        parts += ["", f"## {b['heading']}", ""]
        img = next((x for x in images if x is not hero and (x.get("where") or "").lower() == b["heading"].lower()), None)
        if img:
            parts += [img["markdown"], ""]
        parts.append((out.get(f"beat{i+1}") or {}).get("text", "").strip())
    models = {v.get("model") for v in out.values() if v.get("model")}
    return {"text": "\n".join(parts), "model": ", ".join(sorted(m for m in models if m)),
            "beats": len(beats), "_jobs": jobs_, "_story": story}


def revise_beats(prev: dict, notes: str, model: str | None = None) -> dict:
    """Revise section by section, each with the reader's notes, instead of
    rewriting the whole piece. A whole-piece rewrite on the fast model lost
    the headings and the opener on two runs out of two; a section given its
    own brief and the notes keeps its shape."""
    jobs_ = prev.get("_jobs") or []
    story = prev.get("_story") or {}
    if not jobs_:
        return {"text": ""}
    fixed = []
    for name, sysm, user in jobs_:
        fixed.append((name, sysm + "\n\nA reader read the whole piece and left these notes; "
                      "fix whatever applies to THIS section and leave the rest as it was:\n" + notes[:3000],
                      user))
    out = _run_beats(fixed, model)
    return _assemble(story, out, jobs_, story.get("title") or "")


def revise(draft: str, notes: str, story: dict, material: dict, model: str | None = None) -> dict:
    return writer.compose(_REVISE_SYS, f"READER'S NOTES AND CHECKS:\n{notes}\n\nPLAN:\n"
                          f"{json.dumps(story, ensure_ascii=False)}\n\nYOUR DRAFT:\n{draft}\n\n"
                          f"MATERIAL:\n{json.dumps(material, ensure_ascii=False)[:40000]}",
                          max_tokens=9000, model=model, effort="medium")


# ── 8. gates ─────────────────────────────────────────────────────────────────
_IMPROVE = re.compile(r"\b(reduc|cut|improv|lower|decreas|fell|drop|shrank|halv|boost|rais\w* (?:accuracy|quality))\w*", re.I)
_WORSEN = re.compile(r"\b(rais|increas|worsen|rose|higher|elevat|no change|did not|not clearly|no significant|mixed)\w*", re.I)


def direction_check(text: str, reads: list) -> list:
    """Sentences that cite a read and say 'improved' when the read says otherwise."""
    bad = []
    by_cite = {r["cite"]: r for r in reads if r.get("cite")}
    for s in re.split(r"(?<=[.!?])\s+", text):
        for cite, r in by_cite.items():
            if cite in s:
                d = r.get("outcome_direction")
                if d in ("mixed", "no_change", "worsened") and _IMPROVE.search(s) and not _WORSEN.search(s):
                    bad.append({"sentence": s.strip()[:200], "read_says": d,
                                "cite": cite})
    return bad


_GLYPHS = re.compile(r"[【】〔〕「」¹²³⁴⁵⁶⁷⁸⁹⁰]")
_LIST_OPEN = re.compile(r"^(?:A|An|Another|One|The same|A further|A second|A third) "
                        r"(?:[\w‑-]+ ){0,4}?(?:study|review|analysis|trial|paper|survey|meta[‑-]analysis)\b", re.I | re.M)


def _scrub(text: str) -> str:
    """Glyphs the fast model emits around citations (【 】) and a citation
    glued to the word before it."""
    t = _GLYPHS.sub("", text or "")
    # the fast model's citation markup: [cite: "X"], [cite]X[/cite], (cite: X)
    t = re.sub(r"\[cite:\s*\"?(\[[^\]]+\]\([^)]+\)|[^\]\"]+)\"?\s*\]", r"\1", t)
    t = re.sub(r"\[cite\](.*?)\[/cite\]", r"\1", t, flags=re.S)
    t = re.sub(r"\(cite:\s*(.*?)\)", r"\1", t)
    t = re.sub(r"(\w)(\[[^\]]+\]\([^)]+\))", r"\1 \2", t)
    t = re.sub(r"(\w)(\([A-Z][^()]{3,60}, \d{4}\))", r"\1 \2", t)
    return t


def structure_check(text: str) -> list:
    """The house shape, checked mechanically: story headings, and paragraphs
    that do not open on 'A study… Another study… A review…' — the study-by-
    study list the reader rejected, which a model writes the moment it stops
    following the plan."""
    problems = []
    h2 = re.findall(r"^##\s+\S", text, re.M)
    if len(h2) < 3:
        problems.append(f"only {len(h2)} section headings — the plan's beats must be sections with story headings")
    paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip() and not p.strip().startswith(("#", "!", "*", "-"))]
    listy = [p[:80] for p in paras if _LIST_OPEN.match(p)]
    if paras and len(listy) >= max(3, len(paras) // 3):
        problems.append(f"{len(listy)} of {len(paras)} paragraphs open on 'A study / Another study / A review' — "
                        "that is a list of papers, not a story; each paragraph must carry an idea, and the study is evidence for it")
    return problems


_MDLINK = re.compile(r"\[([^\]]+)\]\((https?://[^)\s]+)\)")


def link_check(text: str, reads: list, hk: dict, chart_list: list) -> tuple:
    """Every link in the body must be a (label, url) pair the material gave.

    Caught live: a paper with no DOI was cited as
    "[(UWSpace, 2021)](https://link.springer.com/10.1007/s11783-021-1492-5)"
    — the model borrowed another paper's URL for it. The number gate cannot
    see a URL and the name gate cannot either, so a reader following that
    link lands on the wrong study with no warning. Here each link is matched
    to the source whose label it carries; a link whose URL belongs to a
    different source is re-pointed to the right one, and a link to a URL no
    source has is reduced to its label. Every repair is reported."""
    by_url, by_label = {}, {}
    for r in reads:
        if r.get("cite") and r.get("link"):
            m = _MDLINK.fullmatch(r["cite"])
            if m:
                by_url[m.group(2)] = r["cite"]; by_label[m.group(1).strip().lower()] = r["cite"]
        elif r.get("cite"):
            by_label[r["cite"].strip("() ").lower()] = r["cite"]
    for n in (hk.get("records") or []):
        if n.get("cite"):
            m = _MDLINK.fullmatch(n["cite"])
            if m:
                by_url[m.group(2)] = n["cite"]; by_label[m.group(1).strip().lower()] = n["cite"]
    chart_urls = {c["url"] for c in chart_list} | {c.get("dark") for c in chart_list if c.get("dark")}
    chart_urls |= {i.get("url") for i in (hk.get("_images") or []) if i.get("url")}
    fixes = []

    def fix(m):
        label, url = m.group(1).strip(), m.group(2)
        if url in chart_urls:
            return m.group(0)
        want = by_label.get(label.strip("() ").lower())
        if want and (url not in by_url or by_url[url] != want):
            fixes.append({"was": m.group(0)[:160], "now": want[:160],
                          "why": "URL belonged to a different source" if url in by_url else "URL not in the material"})
            return want
        if url in by_url:
            return m.group(0)
        fixes.append({"was": m.group(0)[:160], "now": label, "why": "URL not in the material"})
        return label
    out = _MDLINK.sub(fix, text)
    # A bare "[Discover Water, 2025]" with no URL is the model citing by label
    # and dropping the link. The label names a source; give it back its link.
    def bare(m):
        label = m.group(1).strip()
        want = by_label.get(label.strip("() ").lower())
        if want:
            fixes.append({"was": m.group(0)[:120], "now": want[:160], "why": "link dropped"})
            return want
        return m.group(0)
    out = re.sub(r"\[([^\]\n]{4,90})\](?!\()", bare, out)
    return out, fixes


_SCEPTIC_SYS = (
 "You are a hostile fact-checker. You are given a short piece and the ONLY "
 "material its writer was allowed to use: a few news records and a dozen "
 "papers, each summarised from its abstract with its verified figures. For "
 "each paragraph, find any sentence that asserts something the material does "
 "not say — a trend ('is worsening', 'is growing'), a generalisation ('most "
 "plants', 'many facilities'), a cause, a claim about a study that the study's "
 "summary does not make, a number not present, a named thing not present. "
 "Quote the sentence verbatim. Ignore the writer's own transitions and "
 "questions; ignore plain-language glosses of terms; ignore anything the "
 "material does support. Return JSON {\"unsupported\": [{\"sentence\": str, "
 "\"why\": str, \"severity\": \"high\"|\"low\"}]}. High = a factual claim a reader "
 "would take as evidence; low = a soft inference.")


def sceptic(text: str, material: dict) -> list:
    got = llm.call_json(_SCEPTIC_SYS, f"THE PIECE:\n{text}\n\nTHE MATERIAL:\n"
                        f"{json.dumps(material, ensure_ascii=False)[:30000]}",
                        max_tokens=2500, effort="low")
    items = (got or {}).get("unsupported") or []
    out = []
    for it in items:
        if not isinstance(it, dict) or not it.get("sentence"):
            continue
        sent = str(it["sentence"]).strip()
        if len(sent) < 20 or sent[:40] not in text:
            continue                       # it must quote the piece
        out.append({"sentence": sent[:220], "why": str(it.get("why") or "")[:160],
                    "severity": "high" if str(it.get("severity")).lower() == "high" else "low"})
    return out[:12]


def place_charts(text: str, chart_list: list) -> str:
    """If the writer placed no chart, put the first one after the second
    section's first paragraph and the second after the opener. A data piece
    with no chart is unfinished (RECIPE §6, rule 'charts are mandatory')."""
    if not chart_list or any(c["url"] in text for c in chart_list):
        return text
    parts = text.split("\n## ")
    if len(parts) < 3:
        return text + "\n\n" + chart_list[0]["markdown"] + "\n"
    c0 = chart_list[0]
    sec = parts[2].split("\n\n")
    sec.insert(2 if len(sec) > 2 else len(sec), c0["markdown"])
    parts[2] = "\n\n".join(sec)
    if len(chart_list) > 1:
        parts[0] = parts[0].rstrip() + "\n\n" + chart_list[1]["markdown"]
    return "\n## ".join(parts)


def _gate(text: str, srcs: list, reads: list, audience: str, hk: dict | None = None,
          chart_list: list | None = None, material: dict | None = None) -> dict:
    text = _scrub(text)
    text = place_charts(text, chart_list or [])
    text, link_fixes = link_check(text, reads, hk or {}, chart_list or [])
    ex = writer.excise_ungrounded(text, srcs)
    g = writer.ground(ex["text"], srcs)
    lk = reader.leaks(g["text"], require_sources=False)
    dirs = direction_check(g["text"], reads)
    shape = structure_check(g["text"])
    objections = sceptic(g["text"], material) if material else []
    high = [o for o in objections if o["severity"] == "high"]
    rep = reader.read(g["text"], audience=audience)
    v = reader.verdict(rep, lk, g)
    if dirs:
        v = {"pass": False, "why": (v["why"] + "; " if not v["pass"] else "")
             + f"{len(dirs)} sentences claim improvement where the study says otherwise"}
    if shape:
        v = {"pass": False, "why": (v["why"] + "; " if not v["pass"] else "") + "; ".join(shape)}
    if high:
        v = {"pass": False, "why": (v["why"] + "; " if not v["pass"] else "")
             + f"{len(high)} claims the material does not support"}
    wc = len(g["text"].split())
    if wc > TARGET_WORDS[1] * 1.3:
        v = {"pass": False, "why": v["why"] + f"; too long ({wc} words, keep under {TARGET_WORDS[1]})"}
    if wc < TARGET_WORDS[0] * 0.8:
        v = {"pass": False, "why": (v["why"] + "; " if not v["pass"] else "") + f"too short ({wc} words, write {TARGET_WORDS[0]}-{TARGET_WORDS[1]})"}
    notes = reader.feedback_text(rep, lk, g)
    for pr in shape:
        notes += f"\nSHAPE: {pr}"
    for o in objections:
        notes += (f"\nNOT IN THE MATERIAL ({o['severity']}): \"{o['sentence']}\" — {o['why']}. "
                  f"Cut it, or say only what a source says.")
    for lf in link_fixes:
        notes += (f"\nLINK REPAIRED: {lf['was']} → {lf['now']} ({lf['why']}). Cite by pasting the "
                  f"source's `cite` string exactly; never attach a URL to a source that has none.")
    if wc < TARGET_WORDS[0] * 0.8:
        notes += f"\nTOO SHORT: {wc} words — tell the story properly, {TARGET_WORDS[0]}-{TARGET_WORDS[1]} words."
    for d in dirs:
        notes += (f"\nDIRECTION WRONG: \"{d['sentence']}\" — the study's read says "
                  f"outcome = {d['read_says']}. Say what it found.")
    if wc > TARGET_WORDS[1] * 1.3:
        notes += f"\nTOO LONG: {wc} words. Cut to {TARGET_WORDS[1]} without losing the story."
    return {"text": g["text"], "grounded": g["grounded"], "excised": ex["removed"],
            "ungrounded_numbers": g["ungrounded_numbers"], "unsourced_names": g["unsourced_names"],
            "leaks": lk, "direction": dirs, "shape": shape, "links": link_fixes,
            "objections": objections, "reader": rep, "verdict": v, "notes": notes, "words": wc}


# ── 9. the method line and sources, written by code ─────────────────────────
def _method_line(subject: str, n_papers: int, has_news: bool) -> str:
    today = time.strftime("%d %B %Y").lstrip("0")
    news_bit = ("was used to find the news and the relevant studies" if has_news
                else "was used to find the relevant studies")
    return (f"*How this was put together. [Fliar Prism](https://fliarbi.com/prism/), a research "
            f"tool, {news_bit}; the {n_papers} papers' abstracts on {subject} were reviewed "
            f"against one fixed checklist on {today}, and every study above is described from "
            f"its own abstract. "
            + ("The news items are linked to their publishers. " if has_news else "")
            + "Charts are drawn from the same figures the text cites.*")


def _sources_block(text: str, reads: list, hk: dict) -> str:
    used = [r for r in reads if r.get("cite") and r["cite"] in text]
    lines = []
    for r in used:
        tail = f" [{r.get('venue') or 'link'}]({r['link']})" if r.get("link") else ""
        lines.append(f"- *{r['title']}* — {r.get('venue') or 'no venue recorded'}, "
                     f"{r.get('year')}.{tail}")
    for n in (hk.get("records") or []):
        if n.get("cite") and n["cite"] in text:
            lines.append(f"- {n['publisher']}, {n['date']} — [{n['title']}]({n['url']})")
    return "## Sources\n\n" + "\n".join(lines) if lines else ""


# ── markdown → HTML, for callers that publish (a CMS has no markdown) ───────
def to_html(md: str) -> str:
    import html as _h
    def inline(t):
        t = _h.escape(t)
        t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
        t = re.sub(r"(?<!\*)\*(?!\*)(.+?)(?<!\*)\*(?!\*)", r"<em>\1</em>", t)
        return re.sub(r"(?<!!)\[([^\]]+)\]\((https?://[^)]+)\)", r'<a href="\2" rel="noopener">\1</a>', t)
    out, para, in_list = [], [], False
    def flush():
        if para:
            out.append(f"<p>{inline(' '.join(para).strip())}</p>"); para.clear()
    def close_list():
        nonlocal in_list
        if in_list:
            out.append("</ul>"); in_list = False
    for line in (md or "").split("\n"):
        s_ = line.rstrip()
        m = re.match(r"^\s*!\[([^\]]*)\]\((https?://[^)]+)\)\s*$", s_)
        if m:
            flush(); close_list()
            out.append(f'<figure class="wp-block-image"><img src="{_h.escape(m.group(2))}" alt="{_h.escape(m.group(1))}" loading="lazy"/></figure>'); continue
        h = re.match(r"^(#{1,6})\s+(.*)$", s_)
        if h:
            flush(); close_list()
            if len(h.group(1)) == 1:
                continue
            lvl = min(len(h.group(1)), 4)
            out.append(f"<h{lvl}>{_h.escape(h.group(2))}</h{lvl}>"); continue
        if re.match(r"^\s*[-*]\s+", s_):
            flush()
            if not in_list:
                out.append("<ul>"); in_list = True
            out.append(f"<li>{inline(re.sub(r'^\s*[-*]\s+', '', s_))}</li>"); continue
        if not s_.strip():
            flush(); close_list()
        else:
            para.append(s_)
    flush(); close_list()
    return "\n".join(out)


# ── the whole thing ──────────────────────────────────────────────────────────
def story(subject: str, slug: str | None = None, k: int = SHORTLIST_K,
          model: str | None = None, save: bool = True, progress=None,
          images: bool = True) -> dict:
    t0 = time.time()
    slug = slug or ("quick-" + re.sub(r"[^a-z0-9]+", "-", subject.lower()).strip("-")[:50])
    steps = {}

    def tick(name, **kw):
        steps[name] = {"seconds": round(time.time() - t0, 1), **kw}
        if progress:
            progress(name)
        _log(f"{name} {steps[name]}")

    cov = coverage(); tick("coverage", **{k: v for k, v in cov.items() if k != "note"})
    res = resolve(subject, model=model); tick("resolve", phrases=res["phrases"], health=res["health"], place=res.get("place"))
    pool = fetch(res["phrases"], res["health"]); tick("fetch", pool=len(pool))
    if not pool:
        return {"available": False, "reason": "no abstract-bearing papers match this subject's phrases",
                "subject": subject, "resolve": res}
    short = shortlist(res["head"], res["phrases"], pool, k=k); tick("shortlist", k=len(short))
    if not short:
        return {"available": False, "reason": "nothing in the pool is about the subject "
                f"(best similarity under {MIN_SIM})", "subject": subject, "resolve": res}
    reads = read(res["head"], slug, short); tick("read", on_subject=len(reads))
    if len(reads) < 3:
        return {"available": False, "reason": f"only {len(reads)} on-subject papers after reading — "
                "too few for a piece that is honest about its evidence",
                "subject": subject, "resolve": res, "reads": reads}
    for r in reads:
        r["link"] = _resolve_doi(r["doi"]) if r.get("doi") else None
        r["cite"] = (f"[{(r.get('venue') or 'study')[:60]}, {r.get('year')}]({r['link']})"
                     if r.get("link") else f"({(r.get('venue') or 'a study')[:60]}, {r.get('year')})")
    hk = hook(subject, head=res["head"], place=res.get("place"))
    tick("hook", news=len(hk["records"]), term=hk.get("term"), series=bool(hk["series"]))
    chart_list = make_charts(subject, reads, hk, slug); tick("charts", n=len(chart_list))
    material = _material(reads, hk, chart_list)
    material["counts"] = _counts(reads)
    st = plan(subject, material, model=model); tick("plan", ok=bool(st.get("beats")))
    st["_images"] = make_images(st, slug, place=res.get("place")) if images else []
    tick("images", n=len(st["_images"]))
    got = write(subject, st, material, model=model); tick("write", model=got.get("model"))
    body = got.get("text") or ""
    if not body.strip():
        return {"available": False, "reason": "the writer returned nothing", "subject": subject}

    # The illustrations' URLs carry a hex hash; to the number gate that is a
    # string of figures no source holds, and it excised every image line as
    # an ungrounded sentence. The images are part of the material.
    material["images"] = [{"where": i.get("where"), "url": i.get("url"), "markdown": i.get("markdown")}
                          for i in (st.get("_images") or [])]
    srcs = [json.dumps(material, ensure_ascii=False, default=str), _aliases(material)]
    audience = "curious non-specialist — a founder, a journalist, a postgraduate"
    rounds, best = [], None
    for rnd in range(MAX_REVISIONS + 1):
        hk["_images"] = st.get("_images") or []
        g = _gate(body, srcs, reads, audience, hk=hk, chart_list=chart_list, material=material)
        rep = g["reader"]
        rounds.append({"round": rnd + 1, "pass": g["verdict"]["pass"], "why": g["verdict"]["why"],
                       "understood": rep.get("understood"), "kept_reading": rep.get("kept_reading"),
                       "about": rep.get("about"), "words": g["words"],
                       "machine_voice": g["leaks"]["process_count"],
                       "direction_errors": len(g["direction"]),
                       "ungrounded": g["ungrounded_numbers"], "fix_first": rep.get("fix_first"),
                       "machine": g["leaks"]["process"][:3], "shape": g.get("shape"),
                       "unsupported": g.get("objections"), "text": g["text"]})
        key = (1 if g["verdict"]["pass"] else 0, 0 if g["leaks"].get("truncated") else 1,
               1 if g["grounded"] else 0, -len(g["direction"]),
               -len([o for o in g.get("objections") or [] if o["severity"] == "high"]),
               1 if rep.get("kept_reading") else 0, int(rep.get("understood") or 0))
        if best is None or key > best[0]:
            best = (key, g, rnd + 1)
        tick(f"gate{rnd + 1}", **{"pass": g["verdict"]["pass"], "understood": rep.get("understood")})
        if g["verdict"]["pass"] or rnd == MAX_REVISIONS:
            break
        nxt = revise_beats(got, g["notes"], model=model) if got.get("_jobs") else \
              revise(g["text"], g["notes"], st, material, model=model)
        if not (nxt.get("text") or "").strip():
            break
        body = nxt["text"]
        got = {**got, **{k: v for k, v in nxt.items() if k in ("_jobs", "_story", "model")}}
    _, g, delivered = best
    for r in rounds:
        r["delivered"] = (r["round"] == delivered)

    text = g["text"].rstrip()
    # The loop ended with a claim the material does not support still in the
    # piece. The rule for an unsupported number is excision, not a flag; the
    # rule for an unsupported sentence is the same. Cut it, list it.
    cut = []
    for o in (g.get("objections") or []):
        if o.get("severity") != "high":
            continue
        sent = o["sentence"].strip()
        for cand in (sent, sent[:60]):
            i = text.find(cand)
            if i >= 0:
                end = text.find(". ", i)
                end = (end + 1) if end >= 0 else min(len(text), i + len(sent))
                text = (text[:i] + text[end:]).replace("  ", " ")
                cut.append(sent[:200]); break
    # Machine-voice sentences are commentary about the process by
    # construction ("These reads cannot tell us…"); cutting one loses no
    # fact. Same treatment.
    for sent in (g.get("leaks") or {}).get("process") or []:
        sent = sent.strip()
        i = text.find(sent[:50])
        if i >= 0:
            end = text.find(". ", i)
            end = (end + 1) if end >= 0 else min(len(text), i + len(sent) + 10)
            text = (text[:i] + text[end:]).replace("  ", " ")
            cut.append("[machine voice] " + sent[:160])
    if cut:
        text = re.sub(r"\n{3,}", "\n\n", text)
        g["objections"] = [o for o in g.get("objections") or [] if o.get("severity") != "high"]
        g["leaks"]["process"] = []
    text = re.sub(r"^[ \t]+(?=\S)", "", text, flags=re.M)      # a cut can leave a paragraph starting with a space
    g["excised_unsupported"] = cut
    text = re.sub(r"\n#{1,3}\s*Sources\b.*$", "", text, flags=re.S).rstrip()
    method = _method_line(subject, len(reads), bool(hk["records"]))
    sources = _sources_block(text, reads, hk)
    md = text + "\n\n" + method + ("\n\n" + sources if sources else "") + "\n"
    title_m = re.search(r"^#\s+(.+)$", md, re.M)
    out = {
        "available": True, "subject": subject, "slug": slug,
        "title": (title_m.group(1).strip() if title_m else st.get("title")),
        "markdown": md, "html": to_html(md), "words": len(text.split()),
        "publishable": (g["grounded"] and not g["direction"] and not g["leaks"]["process"]
                        and not g.get("shape")
                        and not [o for o in g.get("objections") or [] if o["severity"] == "high"]),
        "checks": {"excised_unsupported": g.get("excised_unsupported") or [], "excised": g["excised"], "ungrounded_numbers": g["ungrounded_numbers"],
                   "unsourced_names": g["unsourced_names"], "direction": g["direction"],
                   "machine_voice": g["leaks"]["process"], "truncated": g["leaks"].get("truncated"),
                   "shape": g.get("shape"), "links_repaired": g.get("links"),
                   "unsupported": g.get("objections")},
        "reader_rounds": rounds, "plan": st,
        "papers": [{"title": r["title"], "venue": r.get("venue"), "year": r.get("year"),
                    "doi": r.get("doi"), "link": r.get("link"), "design": r.get("study_design"),
                    "direction": r.get("outcome_direction"), "sim": r.get("sim"),
                    "used": bool(r.get("cite") and r["cite"] in text)} for r in reads],
        "news": hk["records"], "charts": chart_list, "images": st.get("_images") or [],
        "resolve": {k: v for k, v in res.items() if k != "phrase_counts"},
        "coverage": cov,
        "steps": steps, "seconds": round(time.time() - t0, 1),
        "written_by": got.get("model"), "read_by": READ_MODEL_LABEL,
    }
    if save:
        try:
            os.makedirs(ARTICLES_DIR, exist_ok=True); os.makedirs(PACKS_DIR, exist_ok=True)
            open(f"{ARTICLES_DIR}/{slug}.md", "w").write(md)
            pack = {"slug": slug, "subject": subject, "material": material,
                    "reads": reads, "news": hk, "charts": chart_list,
                    "derived": {"papers_read": len(reads), **_counts(reads)},
                    "plan": st, "reader_rounds": rounds, "built": time.strftime("%Y-%m-%dT%H:%M:%S")}
            json.dump(pack, open(f"{PACKS_DIR}/{slug}.json", "w"), indent=1,
                      ensure_ascii=False, default=str)
            out["files"] = {"article": f"{ARTICLES_DIR}/{slug}.md",
                            "pack": f"{PACKS_DIR}/{slug}.json",
                            "reads": f"{READS_DIR}/{slug}.reads.jsonl"}
        except Exception as e:
            out["files"] = {"error": f"{type(e).__name__}: {e}"}
    return out
