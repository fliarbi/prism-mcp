"""Benchmark over every showcase scenario: Claude Sonnet and ChatGPT, each alone and with Prism.

Per scenario: four deliverables (captured Prism calls for the Prism setups), the script ground pass, two blind
judges (Claude Opus, GPT), first-screen captures and a per-scenario PDF with before/after screens and the
parameter table. Resumable: every stage is skipped when its output exists.

    python3 benchmarks/bench_full.py [--workers 3] [--only a,b] [--summary]

Writes benchmarks/results/full/<slug>/ and, with --summary, the aggregate pages.
"""
import argparse
import json
import os
import sys
import time
import traceback
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
FULL = os.path.join(ROOT, "benchmarks", "results", "full")
os.environ["BENCH_OUT"] = FULL
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "showcase"))
import bench as v2  # noqa: E402
from scenarios import SCENARIOS  # noqa: E402

KEYS = list(v2.SETUPS)


def done(slug, name):
    return os.path.exists(os.path.join(FULL, slug, name))


def lean(slug):
    """keep what GitHub needs (JSON, first-screen JPEGs); the full-page captures live inside the PDF"""
    from PIL import Image
    d = os.path.join(FULL, slug)
    for k in KEYS:
        png = os.path.join(d, f"{k}_first.png")
        if os.path.exists(png):
            im = Image.open(png).convert("RGB")
            im = im.crop((0, 0, im.width, min(im.height, int(im.width * 1.45))))
            im = im.resize((720, int(im.height * 720 / im.width)))
            im.save(os.path.join(d, f"{k}_first.jpg"), quality=62, optimize=True)
            os.remove(png)
    for f in os.listdir(d):
        if f.endswith("_full.png") or "_full_s" in f or f.endswith(".html"):
            os.remove(os.path.join(d, f))


def one(slug):
    t0 = time.time()
    try:
        d = os.path.join(FULL, slug)
        os.makedirs(d, exist_ok=True)
        ans = v2.answers(slug)
        if any(k not in ans for k in KEYS):
            print(f"FAIL {slug}: missing answers {[k for k in KEYS if k not in ans]}", flush=True)
            return
        if not done(slug, "ground.json"):
            calls = v2.calls_of(slug)
            gr = {k: v2.ground(slug, k, ans[k]["text"], calls) for k in KEYS}
            json.dump(gr, open(os.path.join(d, "ground.json"), "w"), ensure_ascii=False, indent=1, default=str)
        for w in ("opus", "gpt"):
            if not done(slug, f"judge_{w}.json"):
                v2.judge(slug, w)
        r = v2.results(slug)
        if not done(slug, "report.pdf"):
            v2.screens(slug)
            v2.pdf([slug], "One of the 113 showcase scenarios; every scenario was run.", out=os.path.join(d, "report.pdf"))
            lean(slug)
        print(f"DONE {slug} {time.time()-t0:.0f}s " + " ".join(f"{k}={r['setups'][k]['strict']}" for k in KEYS), flush=True)
    except Exception as e:
        print(f"FAIL {slug}: {type(e).__name__}: {e}\n{traceback.format_exc()[-600:]}", flush=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--only", default="")
    a = ap.parse_args()
    slugs = a.only.split(",") if a.only else [s["slug"] for s in SCENARIOS]
    print(f"{len(slugs)} scenarios, {a.workers} at a time", flush=True)
    with ThreadPoolExecutor(a.workers) as ex:
        list(ex.map(one, slugs))
    print("FULL_DONE", flush=True)


if __name__ == "__main__":
    main()
