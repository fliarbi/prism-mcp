"""Finish disease and topic reports after a build: regenerate any write-up keys that came back empty (a writer call can
time out), then re-render each page, its chart images and its GitHub README from the saved data. No MCP calls.

    python3 showcase/repair_reports.py [--kind diseases|topics|all]
"""
import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, HERE)
import disease_intel as di  # noqa: E402
import topic_intel as ti  # noqa: E402
from intel_reports import theme_years  # noqa: E402

METHOD_KEYS = [m[0] for m in di.METHODS] + ["workflow"]


def repair_disease(slug):
    d = os.path.join(di.OUT, slug)
    if not os.path.exists(os.path.join(d, "writeup.json")):
        return
    w = json.load(open(os.path.join(d, "writeup.json")))
    data = json.load(open(os.path.join(d, "data.json")))
    missing = [k for k in ("summary", "policy", "doctor", "scientist") + tuple(METHOD_KEYS) if not w["text"].get(k)]
    if missing:
        F, text = di.write(slug, data)
        for k, v in text.items():
            if not w["text"].get(k):
                w["text"][k] = v
        w["facts"] = F
        json.dump(w, open(os.path.join(d, "writeup.json"), "w"), ensure_ascii=False, indent=1, default=str)
    di.build(slug, write_only=True)
    print(f"disease {slug}: refilled {missing}", flush=True)


def repair_topic(slug):
    d = os.path.join(ti.OUT, slug)
    wp = os.path.join(d, "writeup.json")
    if not os.path.exists(wp) or json.load(open(wp)).get("v") != 2:
        return
    w = json.load(open(wp))
    data = json.load(open(os.path.join(d, "data.json")))
    missing = [k for k in ("summary", "themes_time", "aud0", "aud1", "aud2") + tuple(METHOD_KEYS) if not w["text"].get(k)]
    if missing:
        TY, keep = theme_years(data)
        F, text = ti.write(slug, data, TY)
        for k, v in text.items():
            if not w["text"].get(k):
                w["text"][k] = v
        json.dump(w, open(wp, "w"), ensure_ascii=False, indent=1, default=str)
    ti.build(slug, write_only=True)
    print(f"topic {slug}: refilled {missing}", flush=True)


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--kind", default="all")
    a = ap.parse_args()
    if a.kind in ("all", "diseases"):
        for s in di.DISEASES:
            repair_disease(s)
        di.index()
        di.home()
    if a.kind in ("all", "topics"):
        for s in ti.TOPICS:
            repair_topic(s)
        ti.tp.index()
    print("REPAIR_DONE", flush=True)
