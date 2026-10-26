#!/bin/bash
# After final_pass.sh: re-capture the scenarios that hit an LLM fallback or a history timeout, re-compare, rebuild.
cd "$(dirname "$0")/.."
until grep -q FINAL_DONE showcase/logs/final.log; do sleep 20; done
S=metformin-cancer-risk,glp1-weight-loss-muscle,vitamin-d-depression,crispr-history,semiconductor-shortage-history
python3 - <<'PY'
import json
for s in "metformin-cancer-risk,glp1-weight-loss-muscle,vitamin-d-depression,crispr-history,semiconductor-shortage-history".split(","):
    p=f"docs/comparisons/{s}.json"; d=json.load(open(p))
    for k in ("claude_prism","chatgpt_prism","judge"): d.pop(k,None)
    json.dump(d,open(p,"w"),indent=1,ensure_ascii=False)
PY
python3 showcase/capture.py --only $S --workers 5
python3 showcase/compare.py --only $S --workers 5
python3 showcase/build_pages.py
systemctl --user restart prism-mcp
echo FINAL2_DONE
