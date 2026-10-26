#!/usr/bin/env python3
"""vocab — resolve a term against the corpus's OWN label vocabularies first.

This replaces guessing. Until now a term became a query by having a model
propose phrases and then auditing them against titles — and the audit could
only reject, never discover. "Herniated disc surgery" passed the audit with 3
titles while the corpus held 1,692 papers filed under `Diskectomy` and
`Intervertebral Disc Displacement`, because the model never proposed those
words and nothing asked the corpus what it calls the thing.

So: every distinct label in every label column the corpora carry — news
subcategories, categories and tags; OpenAlex topics; Prism's keywords; MeSH
headings — is embedded ONCE into a local index. A term is embedded with the
same model and matched by cosine against all of it in milliseconds. What comes
back is not a list of words but a list of (label, column, corpus, usage): the
label the corpus actually uses, WHICH COLUMN to filter on, and how many rows
carry it. That tuple is the whole point — it is what turns a phrase into a
predicate without a guess in the chain.

The index is a numpy matrix on disk, rebuilt by `build()` (minutes; run after
a corpus refresh). Query time is a single matrix product.

WHAT THE COLUMN TELLS YOU
  news_subcats      marketai.subcats        curated, 59% of articles
  news_categories   marketai.categories     coarse, 99%
  news_tags         marketai.tags           raw publisher tags, 100%, noisy
  oa_topics         research.oa_topics      OpenAlex curated, best research lane
  prism_keywords    research.prism_keywords Prism's T5 keywords, specific
  mesh              pubmed.mesh_terms       indexer-assigned; the best health lane
"""
from __future__ import annotations

import json
import os
import sys
import time

import numpy as np

from . import ch

VOCAB_DIR = os.environ.get("PRISM_VOCAB_DIR", os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "cache", "vocab"))
os.makedirs(VOCAB_DIR, exist_ok=True)
ENCODE_URL = os.environ.get("PRISM_ENCODE_URL", "http://127.0.0.1:5003/encode/")
DIM = 384

# name -> (table_key, array expression, where, usage floor)
VOCABS = {
    "news_subcats": ("news", "arrayMap(x -> x.1, subcats)", "datetime >= '2024-01-01'", 50),
    "news_categories": ("news", "arrayMap(x -> x.1, categories)", "datetime >= '2024-01-01'", 50),
    "news_tags": ("news", "tags", "datetime >= '2025-01-01'", 300),
    "oa_topics": ("research_typed", "oa_topics", "publication_year >= 2017", 200),
    "prism_keywords": ("research_typed", "prism_keywords", "publication_year >= 2020", 300),
    "mesh": ("pubmed", "mesh_terms", "pub_year >= 2015", 200),
}
COLUMN = {"news_subcats": "subcats", "news_categories": "categories", "news_tags": "tags",
          "oa_topics": "oa_topics", "prism_keywords": "prism_keywords", "mesh": "mesh_terms"}

# MeSH check tags and demographic headings that are on every paper and mean
# nothing about the subject. They would otherwise match everything weakly.
_MESH_NOISE = {"humans", "male", "female", "adult", "middle aged", "aged", "young adult",
               "adolescent", "child", "animals", "mice", "rats", "retrospective studies",
               "prospective studies", "treatment outcome", "follow-up studies",
               "cohort studies", "risk factors", "time factors", "aged, 80 and over",
               "united states", "china", "incidence", "prevalence", "child, preschool",
               "infant", "surveys and questionnaires", "cross-sectional studies"}

_LOG = lambda m: print(f"[prism.vocab] {m}", file=sys.stderr, flush=True)
_CACHE: dict = {}


def embed(texts: list, batch: int = 256) -> np.ndarray:
    """bge/MiniLM vectors from the encode API, normalised, (n, 384)."""
    import urllib.request
    out = []
    for i in range(0, len(texts), batch):
        chunk = texts[i:i + batch]
        req = urllib.request.Request(
            ENCODE_URL, data=json.dumps({"text": chunk, "key": "embeddings"}).encode(),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=120) as r:
            d = json.loads(r.read())
        out.extend(d.get("embedding") or d.get("embeddings"))
    a = np.asarray(out, dtype=np.float32)
    n = np.linalg.norm(a, axis=1, keepdims=True)
    return a / np.where(n == 0, 1, n)


def _labels(name: str) -> list:
    tbl, expr, where, floor = VOCABS[name]
    rows = ch.chq_rows(
        f"SELECT l, count() c FROM (SELECT arrayJoin({expr}) AS l FROM "
        f"{ch.TABLE[tbl]} WHERE {where} AND notEmpty({expr})) GROUP BY l "
        f"HAVING c >= {floor} ORDER BY c DESC", timeout=290)
    out = [(r[0], int(r[1])) for r in rows if r[0] and r[0].strip()]
    if name == "mesh":
        out = [(l, c) for l, c in out if l.lower() not in _MESH_NOISE]
    return out


def build(names=None) -> dict:
    """Embed every vocabulary once. Minutes, not hours; run after a refresh."""
    names = names or list(VOCABS)
    report = {}
    for name in names:
        t0 = time.time()
        labels = _labels(name)
        if not labels:
            report[name] = {"labels": 0, "error": "no labels returned"}
            continue
        texts = [l for l, _ in labels]
        vecs = embed(texts)
        np.save(os.path.join(VOCAB_DIR, f"{name}.npy"), vecs)
        with open(os.path.join(VOCAB_DIR, f"{name}.json"), "w") as f:
            json.dump({"labels": texts, "usage": [c for _, c in labels],
                       "built": time.time(), "column": COLUMN[name],
                       "corpus": VOCABS[name][0]}, f)
        _CACHE.pop(name, None)
        report[name] = {"labels": len(texts), "seconds": round(time.time() - t0, 1)}
        _LOG(f"{name}: {len(texts):,} labels in {report[name]['seconds']}s")
    return report


def _load(name: str):
    if name in _CACHE:
        return _CACHE[name]
    npy, meta = (os.path.join(VOCAB_DIR, f"{name}.npy"),
                 os.path.join(VOCAB_DIR, f"{name}.json"))
    if not (os.path.exists(npy) and os.path.exists(meta)):
        return None
    with open(meta) as f:
        m = json.load(f)
    _CACHE[name] = (np.load(npy), m)
    return _CACHE[name]


def status() -> dict:
    out = {}
    for name in VOCABS:
        got = _load(name)
        out[name] = ({"built": True, "labels": len(got[1]["labels"]),
                      "column": got[1]["column"], "corpus": got[1]["corpus"],
                      "age_hours": round((time.time() - got[1]["built"]) / 3600, 1)}
                     if got else {"built": False})
    return out


def resolve(term: str, k: int = 8, min_sim: float = 0.45,
            vocabs=None) -> dict:
    """term -> the labels the corpora actually use for it, with their columns.

    Returns, per vocabulary, the top-k labels above `min_sim` cosine, each with
    the column to filter and how many rows carry it. Cosine on MiniLM between
    a phrase and a curated label is well separated: 0.6+ is the same concept,
    0.45-0.6 a close neighbour, below 0.45 noise."""
    term = (term or "").strip()
    if not term:
        return {"available": False, "reason": "empty term"}
    names = [n for n in (vocabs or list(VOCABS)) if n in VOCABS]
    q = embed([term])[0]
    out, missing = {}, []
    for name in names:
        got = _load(name)
        if not got:
            missing.append(name)
            continue
        vecs, meta = got
        sims = vecs @ q
        idx = np.argpartition(-sims, min(k * 3, len(sims) - 1))[:k * 3]
        idx = idx[np.argsort(-sims[idx])]
        rows = [{"label": meta["labels"][i], "similarity": round(float(sims[i]), 3),
                 "usage": meta["usage"][i]}
                for i in idx if sims[i] >= min_sim][:k]
        out[name] = {"column": meta["column"], "corpus": meta["corpus"],
                     "matches": rows}
    best = sorted(((n, m) for n, v in out.items() for m in v["matches"]),
                  key=lambda x: -x[1]["similarity"])[:6]
    return {"available": any(v["matches"] for v in out.values()), "term": term,
            "vocabularies": out, "missing": missing,
            "best_overall": [{"vocabulary": n, **m} for n, m in best],
            "how": ("the term is embedded and matched by cosine against every "
                    "distinct label in each corpus's own label columns; each "
                    "match names the column to filter on")}


def terms_for(term: str, name: str, k: int = 4, min_sim: float = 0.5) -> list:
    """Just the label strings for one vocabulary — what a predicate builder wants."""
    r = resolve(term, k=k, min_sim=min_sim, vocabs=[name])
    return [m["label"] for m in (r.get("vocabularies", {}).get(name) or {}).get("matches", [])]
