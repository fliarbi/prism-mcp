#!/bin/bash
# Publish the interactive topic and disease pages to fliarbi.com (owner-run; private folder with a random name).
set -e
cd "$(dirname "$0")/.."
set -a; [ -f .env ] && . ./.env; set +a
H=${PRISM_PUBLISH_HOST:?set PRISM_PUBLISH_HOST (ssh target) in .env}
R=/var/www/html/fliar_site/fliar/demo/docs/prism-dashboards-3bb43e4c
for kind in topics diseases investors; do
  for d in docs/$kind/*/page; do
    slug=$(basename "$(dirname "$d")")
    ssh "$H" "mkdir -p $R/$kind/$slug && chmod 755 $R/$kind $R/$kind/$slug"
    rsync -a --chmod=F644 "$d"/ "$H":$R/$kind/$slug/
  done
done
echo published
