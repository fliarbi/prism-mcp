#!/bin/bash
# Wait until the index answers three strict reads in a row (three minutes apart), then run the given command.
cd "$(dirname "$0")/.."
set -a; [ -f .env ] && . ./.env; set +a   # index host and login (untracked; see .env.example)
ok_read() { curl -s -m 30 -u "${PRISM_CH_USER:-default}:${PRISM_CH_PASSWORD:-}" "${PRISM_CH_HOST:-http://localhost:8123}/" --data "SELECT count() FROM marketai.marketai_distributed WHERE datetime >= '2026-05-01' SETTINGS skip_unavailable_shards=0" | grep -qE '^[0-9]+$'; }
streak=0
until [ "$streak" -ge 3 ]; do
  if ok_read; then streak=$((streak+1)); else streak=0; fi
  [ "$streak" -ge 3 ] || sleep 180
done
echo "STABLE $(date)"
eval "$@"
echo "RETRY_DONE $(date)"
