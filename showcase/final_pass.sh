#!/bin/bash
# Wait for phase2, then re-capture the audit/improve scenarios fixed after it started, re-compare, rebuild.
cd "$(dirname "$0")/.."
until grep -q PHASE2_DONE showcase/logs/phase2.log; do sleep 20; done
S=audit-coffee-draft,audit-ev-draft,improve-microplastics,improve-screen-time
python3 - <<'PY'
import json
for s in "audit-coffee-draft,audit-ev-draft,improve-microplastics,improve-screen-time".split(","):
    p=f"docs/comparisons/{s}.json"; d=json.load(open(p))
    for k in ("claude_prism","chatgpt_prism","judge"): d.pop(k,None)
    json.dump(d,open(p,"w"),indent=1,ensure_ascii=False)
PY
python3 showcase/capture.py --only $S --workers 4
python3 showcase/compare.py --only $S --workers 4
python3 showcase/build_pages.py
systemctl --user restart prism-mcp
echo FINAL_DONE
