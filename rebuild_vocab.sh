#!/bin/bash
# Re-embed every label vocabulary from the live corpora. Minutes. Run after a
# corpus refresh, or weekly — labels drift as new subcats/topics are assigned.
cd "$(dirname "$0")" || exit 1
/usr/bin/python3 -c "
import sys; sys.path.insert(0,'.')
from prism import vocab
import json; print(json.dumps(vocab.build(), indent=1))
" 2>&1 | grep -vE "HTTP Request|INFO" >> cache/vocab/rebuild.log
