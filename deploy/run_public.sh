#!/bin/bash
# Launches the public Prism deployment: one Fliar API key, metered in credits (prism/access.py).
set -euo pipefail
cd "$(dirname "$0")/.."
set -a; . deploy/public.env; set +a
exec /usr/bin/python3 prism_mcp.py --http --host "${PRISM_BIND:-127.0.0.1}" --port "${PRISM_PUBLIC_PORT:-8795}"
