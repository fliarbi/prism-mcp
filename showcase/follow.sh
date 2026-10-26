#!/bin/bash
# Run compare.py on whatever has been captured, every 10 minutes, until capture.py exits; then once more.
cd "$(dirname "$0")/.."
while pgrep -f "showcase/capture.py --workers" >/dev/null; do
  python3 showcase/compare.py --workers 2 >> showcase/logs/compare.log 2>&1
  sleep 600
done
python3 showcase/compare.py --workers 3 >> showcase/logs/compare.log 2>&1
echo FOLLOW_DONE >> showcase/logs/compare.log
