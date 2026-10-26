#!/bin/bash
# The live parts of the showcase, in order: topic pages, entity extras, disease tabs, GIFs, demonstration pages.
cd "$(dirname "$0")/.."
python3 showcase/topic_pages.py --workers 3
echo "TOPICS_STAGE_DONE $(date)"
python3 showcase/capture_extras.py --workers 3
python3 showcase/disease_pages.py
python3 showcase/entity_gifs.py
(cd showcase && python3 build_pages.py)
echo "ALL_LIVE_DONE $(date)"
