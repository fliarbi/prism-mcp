"""After a server fix: re-capture what the fix touched, re-compare it, rebuild.

    python3 showcase/phase2.py [--since 2026-10-22T23:10]

Stale = a scenario whose tool plan goes through query.build (every research
pattern) and whose capture is older than the last fix (showcase/logs/
last_fix_time.txt). News patterns (pulse, compare, trending) and history do not
touch the changed code and are kept. For a stale scenario the memory-only answers
stay (they never saw Prism); only the Prism-backed answers and the judge are redone.
"""
import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "showcase"))
from scenarios import SCENARIOS  # noqa: E402

RESEARCH = {"evidence", "claims", "improve", "citations", "audit", "table", "geo", "brief", "library", "radar"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--since", default=open(os.path.join(ROOT, "showcase/logs/last_fix_time.txt")).read().strip())
    ap.add_argument("--workers", type=int, default=5)
    a = ap.parse_args()
    redo = []
    for s in SCENARIOS:
        path = os.path.join(ROOT, "docs/examples", f"{s['slug']}.json")
        if not os.path.exists(path):
            redo.append(s["slug"])
            continue
        if s["pattern"] in RESEARCH and json.load(open(path))["captured_at"][:16] < a.since:
            redo.append(s["slug"])
    print(f"re-capturing {len(redo)} scenarios captured before {a.since}", flush=True)
    for slug in redo:
        c = os.path.join(ROOT, "docs/comparisons", f"{slug}.json")
        if os.path.exists(c):
            d = json.load(open(c))
            for k in ("claude_prism", "chatgpt_prism", "judge"):
                d.pop(k, None)
            json.dump(d, open(c, "w"), indent=1, ensure_ascii=False)
    py = sys.executable
    if redo:
        subprocess.run([py, "showcase/capture.py", "--only", ",".join(redo), "--workers", str(a.workers)], cwd=ROOT)
    subprocess.run([py, "showcase/compare.py", "--workers", "3"], cwd=ROOT)
    subprocess.run([py, "showcase/build_pages.py"], cwd=ROOT)
    print("PHASE2_DONE", flush=True)


if __name__ == "__main__":
    main()
