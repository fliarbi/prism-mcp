#!/usr/bin/env python3
"""articles — turning a ClickHouse `target_id` into an article a person can read.

The news corpus is split in two on purpose. ClickHouse holds the SIGNAL — one
row per article with its sentiment, priority, tags, categories, geography and
full text — and answers "which articles, how many, when". The article RECORD
(url, title, publisher, published date) lives in MongoDB, sharded across 31
nodes by a consistent hash of the id.

So resolving articles is a three-hop walk, and it is the same walk the Prism
frontend does:

    target_id -> consistent hash -> node
    node.inferences_analysis2.main -> which partition holds it
    node.news_chunks2.<partition>  -> the record

Two details that are easy to get wrong and produce an empty feed rather than an
error: the partition name defaults to `from_2020_to_now` when the routing
document is missing, and the TITLE is not a column — it is inside a JSON blob
of scraped meta tags, under og:title or twitter:title. An article whose page
carried neither has no title, and this returns the first line of its text
instead of dropping the article.
"""
from __future__ import annotations

import json
import re
import sys
import threading

MONGO_COMMON = "/mnt/nfs1/news/common"
DEFAULT_PARTITION = "from_2020_to_now"
_LOCK = threading.Lock()
_CLIENTS: dict = {}
_ROUTER = None


def _router():
    """`get_node_for_id` + `mongo_map_raw` from the cluster's own routing module,
    imported rather than copied: the ring is 31 nodes and a stale copy of the
    map silently reads the wrong shard, which returns nothing rather than
    failing."""
    global _ROUTER
    if _ROUTER is None:
        if MONGO_COMMON not in sys.path:
            sys.path.insert(0, MONGO_COMMON)
        from main import get_node_for_id, mongo_map_raw
        _ROUTER = (get_node_for_id, mongo_map_raw)
    return _ROUTER


def _client(node_id: int):
    with _LOCK:
        if node_id not in _CLIENTS:
            import pymongo
            _, mp = _router()
            _CLIENTS[node_id] = pymongo.MongoClient(
                f"mongodb://{mp[node_id]}", serverSelectionTimeoutMS=4000,
                socketTimeoutMS=15000, connectTimeoutMS=4000)
        return _CLIENTS[node_id]


_PROJECTION = {"url": 1, "website": 1, "json_data.text": 1,
               "json_data.meta_data": 1, "var.published_date": 1}


def _title_of(doc: dict) -> tuple:
    """(title, first_line). Titles live in a JSON string of scraped meta tags."""
    jd = doc.get("json_data") or {}
    text = (jd.get("text") or "").strip()
    first = text.split("\n")[0][:300] if text else ""
    raw = jd.get("meta_data")
    if raw:
        try:
            md = json.loads(raw) if isinstance(raw, str) else raw
            t = ((md.get("og") or {}).get("title")
                 or (md.get("twitter") or {}).get("title")
                 or md.get("title"))
            if t:
                return str(t).strip()[:300], first
        except Exception:
            pass
    return "", first


def _iso(v):
    """Any date-ish value -> an ISO string, or None. Never an object."""
    if v is None or isinstance(v, str):
        return v or None
    try:
        return v.isoformat(sep=" ", timespec="seconds")
    except Exception:
        return str(v)


def _publisher(doc: dict) -> str:
    """The publishing host, normalised.

    `www.` is stripped because the same outlet is stored both ways and a
    concentration number that reports thewest.com.au twice, at half its real
    share each time, is worse than no concentration number."""
    raw = (doc.get("website") or "").strip() or (doc.get("url") or "")
    host = re.sub(r"^https?://", "", raw).split("/")[0].strip().lower()
    return re.sub(r"^www\d?\.", "", host)


def resolve(target_ids, signals: dict | None = None) -> list:
    """target_ids -> article records, batched per node.

    `signals` optionally maps id -> whatever ClickHouse already knows about that
    article (date, priority, tone, tags), which is merged into the record so a
    caller gets one object per article instead of having to join two lists.

    Missing ids are skipped rather than returned as blanks: an article whose
    Mongo record has been rotated away is not a failure of the query, and a feed
    with holes in it is harder to render than a shorter feed."""
    ids = [str(t) for t in (target_ids or []) if t]
    if not ids:
        return []
    try:
        from bson import ObjectId
        get_node, _ = _router()
    except Exception as e:
        return [{"target_id": t, "error": f"router unavailable: {type(e).__name__}: {e}"}
                for t in ids[:1]]

    by_node: dict = {}
    for t in ids:
        try:
            oid = ObjectId(t)
        except Exception:
            continue
        by_node.setdefault(int(get_node(str(oid))), []).append(oid)

    out = []
    for node_id, oids in by_node.items():
        try:
            cli = _client(node_id)
            parts: dict = {}
            for inf in cli.inferences_analysis2.main.find(
                    {"_id": {"$in": oids}}, {"collection_name": 1}):
                parts.setdefault(inf.get("collection_name") or DEFAULT_PARTITION,
                                 []).append(inf["_id"])
            found = {i for v in parts.values() for i in v}
            missing = [o for o in oids if o not in found]
            if missing:
                parts.setdefault(DEFAULT_PARTITION, []).extend(missing)
            for part, want in parts.items():
                for doc in cli.news_chunks2[part].find({"_id": {"$in": want}},
                                                       _PROJECTION):
                    tid = str(doc["_id"])
                    title, first = _title_of(doc)
                    # `published_date` comes back as a BSON datetime. Left as
                    # an object it serialises fine through the MCP layer and
                    # raises "Object of type datetime is not JSON serializable"
                    # over REST — the same payload working on one transport and
                    # failing on the other. Normalise here, once.
                    rec = {"target_id": tid, "url": doc.get("url"),
                           "title": title or None,
                           "excerpt": first or None,
                           "publisher": _publisher(doc),
                           "published": _iso((doc.get("var") or {}).get("published_date")),
                           "partition": part}
                    if signals and tid in signals:
                        rec.update(signals[tid])
                    out.append(rec)
        except Exception as e:
            out.append({"node": node_id, "error": f"{type(e).__name__}: {e}",
                        "requested": len(oids)})
    order = {t: i for i, t in enumerate(ids)}
    out.sort(key=lambda r: order.get(r.get("target_id", ""), 10**6))
    return out


def health(all_nodes: bool = False) -> dict:
    """Can the article store be reached at all, and how many nodes are in the ring."""
    try:
        get_node, mp = _router()
        if all_nodes:
            from concurrent.futures import ThreadPoolExecutor
            def probe(node):
                try:
                    _client(node).admin.command('ping')
                    return {'node': node, 'available': True}
                except Exception as e:
                    return {'node': node, 'available': False, 'error': str(e)}
            with ThreadPoolExecutor(max_workers=min(16, max(1, len(mp)))) as pool:
                nodes = list(pool.map(probe, mp))
            return {'available': all(n['available'] for n in nodes),
                    'ring_nodes': len(mp), 'probed_nodes': len(nodes), 'nodes': nodes}
        node = int(get_node("65f1c2a4b1e2c3d4e5f60718"))
        cli = _client(node)
        cli.admin.command("ping")
        return {"available": True, "ring_nodes": len(mp), "probed_node": node,
                "address": mp[node]}
    except Exception as e:
        return {"available": False, "reason": f"{type(e).__name__}: {e}"}


# ═══════════════════════════ mastheads ═══════════════════════════════════════
# A domain is not a citation. "timesofindia.indiatimes.com (2025-09-30) report
# that…" is how a scraper writes; "The Times of India reported on 30 September
# 2025" is how a publication writes. The map covers the outlets that actually
# dominate this corpus; anything unmapped falls back to a tidied host, which is
# still better than the raw domain and never invents a name.
MASTHEADS = {
    "timesofindia.indiatimes.com": "The Times of India",
    "indiatimes.com": "The Times of India",
    "economictimes.indiatimes.com": "The Economic Times",
    "hindustantimes.com": "Hindustan Times",
    "indianexpress.com": "The Indian Express",
    "newindianexpress.com": "The New Indian Express",
    "thehindu.com": "The Hindu",
    "ndtv.com": "NDTV",
    "livemint.com": "Mint",
    "business-standard.com": "Business Standard",
    "moneycontrol.com": "Moneycontrol",
    "indiatoday.in": "India Today",
    "news18.com": "News18",
    "firstpost.com": "Firstpost",
    "theprint.in": "ThePrint",
    "thewire.in": "The Wire",
    "scroll.in": "Scroll.in",
    "deccanherald.com": "Deccan Herald",
    "deccanchronicle.com": "Deccan Chronicle",
    "telegraphindia.com": "The Telegraph",
    "tribuneindia.com": "The Tribune",
    "outlookindia.com": "Outlook",
    "indiatvnews.com": "India TV",
    "zeenews.india.com": "Zee News",
    "cnbctv18.com": "CNBC-TV18",
    "businesstoday.in": "Business Today",
    "financialexpress.com": "The Financial Express",
    "thenewsmill.com": "The News Mill",
    "newsdrum.in": "NewsDrum",
    "timesnownews.com": "Times Now",
    "english.mathrubhumi.com": "Mathrubhumi English",
    "mathrubhumi.com": "Mathrubhumi",
    "newkerala.com": "NewKerala",
    "apnlive.com": "APN Live",
    "krishijagran.com": "Krishi Jagran",
    "bbc.co.uk": "the BBC", "bbc.com": "the BBC",
    "reuters.com": "Reuters",
    "apnews.com": "the Associated Press",
    "theguardian.com": "The Guardian",
    "nytimes.com": "The New York Times",
    "washingtonpost.com": "The Washington Post",
    "straitstimes.com": "The Straits Times",
    "aljazeera.com": "Al Jazeera",
    "jamaicaobserver.com": "the Jamaica Observer",
    "pti.in": "the Press Trust of India",
    "ptinews.com": "the Press Trust of India",
    "aninews.in": "ANI",
}

# Wire services and national dailies carry more weight in a citation than an
# aggregator. Used to ORDER which outlet a story is attributed to when several
# ran it, never to hide the others.
AUTHORITY = {
    "reuters.com": 5, "apnews.com": 5, "bbc.co.uk": 5, "bbc.com": 5,
    "ptinews.com": 5, "aninews.in": 4, "theguardian.com": 4, "nytimes.com": 4,
    "thehindu.com": 5, "indianexpress.com": 5, "hindustantimes.com": 4,
    "timesofindia.indiatimes.com": 4, "business-standard.com": 4,
    "livemint.com": 4, "ndtv.com": 4, "theprint.in": 4, "scroll.in": 4,
    "economictimes.indiatimes.com": 4, "telegraphindia.com": 4,
    "deccanherald.com": 3, "tribuneindia.com": 3, "india today": 3,
    "indiatoday.in": 3, "news18.com": 3, "cnbctv18.com": 3, "firstpost.com": 3,
    "indiatvnews.com": 2, "timesnownews.com": 2, "zeenews.india.com": 2,
}


def masthead(host: str | None) -> str:
    """A publication name a reader would recognise, from a domain."""
    h = (host or "").strip().lower().lstrip(".")
    h = re.sub(r"^www\d?\.", "", h)
    if h in MASTHEADS:
        return MASTHEADS[h]
    for dom, name in MASTHEADS.items():
        if h.endswith("." + dom):
            return name
    # Unmapped: tidy the host rather than invent a masthead.
    core = h.split("/")[0]
    core = re.sub(r"\.(com|in|co\.uk|org|net|news|co|io)$", "", core)
    core = core.replace("english.", "").replace("www.", "")
    return core if core else (host or "an outlet")


def authority(host: str | None) -> int:
    h = re.sub(r"^www\d?\.", "", (host or "").strip().lower())
    return AUTHORITY.get(h, 1)
