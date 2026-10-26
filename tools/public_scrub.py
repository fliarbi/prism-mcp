"""Scrub the saved responses and documents in this repo for publication: the same public naming the public API applies
(prism/envelope.py: Prism research index ids and DOIs instead of the upstream index, no table, host, store or model
names), private-network addresses, local paths, and the keys that carry internals (traces, SQL, cache keys, hosts).

Applies to JSON, Markdown, HTML, text, CSV and SVG files under docs/ and benchmarks/ and to README.md. Code is never
touched. Idempotent; run it before publishing a rebuild.

    python3 tools/public_scrub.py [--check]     # --check: report what would change, write nothing
"""
import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
from prism.envelope import public, public_text, _PUBLIC_EXTRA  # noqa: E402

DIRS = ("docs", "benchmarks")
FILES = ("README.md",)
EXT = (".json", ".md", ".html", ".txt", ".csv", ".svg")
DROP = {"trace", "cache_key", "sql", "table", "host", "hosts", "nodes", "node", "local_path"}

_LOCAL = [
    (re.compile(r"\b[Aa] shard\b"), "an index partition"),
    (re.compile(r"openalex:(W\d+)", re.I), r"prism:\1"),
    (re.compile(r"openalex", re.I), "Prism research index"),
    (re.compile(r"/home/[a-z0-9_-]+/prism-mcp/"), ""),
    (re.compile(r"/home/[a-z0-9_-]+/prism-mcp\b"), "."),
    (re.compile(r"/home/[a-z0-9_-]+/"), "~/"),
    (re.compile(r"\b(?:192\.168|10\.\d{1,3}|172\.(?:1[6-9]|2\d|3[01])|100\.(?:6[4-9]|[7-9]\d|1[01]\d|12[0-7]))\.\d{1,3}\.\d{1,3}(?::\d+)?\b"),
     "an index node"),
    (re.compile(r"\b[a-z0-9_]+_distributed\b"), "the index"),
    (re.compile(r"\b(?:user|password)=[^&\s\"']+"), ""),
]
# _PUBLIC_EXTRA's "/home/..." rule would turn a path into prose; the _LOCAL rules above handle paths first
_EXTRA = [(p, r) for p, r in _PUBLIC_EXTRA if p.pattern != r"/home/\S+"]


def text(s):
    s = public_text(s)
    for pat, rep in _LOCAL + _EXTRA:
        s = pat.sub(rep, s)
    return s


def walk(o):
    if isinstance(o, str):
        return text(o)
    if isinstance(o, dict):
        return {text(k) if isinstance(k, str) else k: walk(v) for k, v in o.items() if k not in DROP}
    if isinstance(o, list):
        return [walk(v) for v in o]
    return o


def scrub_file(path, check=False):
    raw = open(path, encoding="utf-8", errors="surrogateescape").read()
    if path.endswith(".json"):
        try:
            obj = json.loads(raw)
        except ValueError:
            obj = None
        if obj is not None:
            out = walk(public(obj))
            same = out == obj
            new = json.dumps(out, ensure_ascii=False, indent=1, default=str) + "\n"
        else:
            new = text(raw)
            same = new == raw
    else:
        new = text(raw)
        same = new == raw
    if same:
        return False
    if not check:
        open(path, "w", encoding="utf-8", errors="surrogateescape").write(new)
    return True


def files():
    for d in DIRS:
        for base, _, names in os.walk(os.path.join(ROOT, d)):
            for n in names:
                if n.endswith(EXT):
                    yield os.path.join(base, n)
    for f in FILES:
        yield os.path.join(ROOT, f)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    changed = [p for p in files() if scrub_file(p, a.check)]
    print(f"{'would change' if a.check else 'changed'} {len(changed)} files")
    for p in changed[:15]:
        print("  " + os.path.relpath(p, ROOT))
