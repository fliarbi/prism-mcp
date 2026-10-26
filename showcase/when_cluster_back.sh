#!/bin/bash
# Wait for the ClickHouse cluster to answer a strict read, then finish the live parts of the showcase.
cd "$(dirname "$0")/.."
set -a; [ -f .env ] && . ./.env; set +a   # index host and login (untracked; see .env.example)
ok_read() { curl -s -m 30 -u "${PRISM_CH_USER:-default}:${PRISM_CH_PASSWORD:-}" "${PRISM_CH_HOST:-http://localhost:8123}/" --data "SELECT count() FROM marketai.marketai_distributed WHERE datetime >= '2026-05-01' SETTINGS skip_unavailable_shards=0" | grep -qE '^[0-9]+$'; }
# a flapping host passes one check and drops again: require three passes, three minutes apart
streak=0
until [ "$streak" -ge 3 ]; do
  if ok_read; then streak=$((streak+1)); else streak=0; fi
  [ "$streak" -ge 3 ] || sleep 180
done
echo "CLUSTER_BACK $(date)"
python3 showcase/topic_pages.py --only cybercrime --workers 1
echo "TRIAL_DONE $(date)"
python3 showcase/capture_extras.py --workers 3
python3 showcase/disease_pages.py
python3 showcase/entity_gifs.py
python3 showcase/topic_pages.py --workers 3
(cd showcase && python3 build_pages.py)
echo "WHEN_BACK_DONE $(date)"
