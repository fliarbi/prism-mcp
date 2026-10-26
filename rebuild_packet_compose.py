#!/usr/bin/env python3
"""Verify editor reuse of an existing packet; generate but never publish."""
import argparse
import json
from pathlib import Path
import time
import httpx

parser = argparse.ArgumentParser()
parser.add_argument('--port', type=int, default=8791)
parser.add_argument('--case', type=Path, default=Path('out/rebuild-20260912/matrix50-final/41.json'))
parser.add_argument('--output', type=Path, default=Path('out/rebuild-20260912/packet-compose.json'))
args = parser.parse_args()
source = json.loads(args.case.read_text())
topic = source['args']['claim']; pid = source['first']['response']['data']['packet_id']
out = {'topic': topic, 'packet_id': pid, 'published': False}
with httpx.Client(base_url=f'http://127.0.0.1:{args.port}', timeout=120) as client:
    start = time.monotonic()
    out['sections'] = client.post('/v1/compose.sections', json={'topic': topic, 'packet_id': pid}).json()
    out['sections_seconds'] = time.monotonic()-start
    assert out['sections']['ok'], out
    start = time.monotonic()
    out['section'] = client.post('/v1/compose.section', json={
        'topic': topic, 'packet_id': pid, 'section': 'state_of_evidence'}).json()
    out['section_seconds'] = time.monotonic()-start
    out['scope_mismatch'] = client.post('/v1/compose.sections', json={'topic': 'A different subject.', 'packet_id': pid}).json()
    assert out['scope_mismatch']['ok'] is False
args.output.write_text(json.dumps(out, indent=2, ensure_ascii=False))
print(json.dumps({'sections_seconds': out['sections_seconds'], 'section_seconds': out['section_seconds'],
                  'section_ok': out['section']['ok'], 'grounded': (out['section'].get('data') or {}).get('grounded')}))
