#!/usr/bin/env python3
"""Verify final evidence counts and hash immutable artifacts/source changes."""
import hashlib
import json
from pathlib import Path

root = Path(__file__).resolve().parent
dest = root/'out/rebuild-20260912'
results = [json.loads((dest/'matrix50-final'/f'{i:02d}.json').read_text()) for i in range(1, 51)]
assert all(r['first']['response']['ok'] and 'passages' in r and 'repeat' in r for r in results)
assert len({r['id'] for r in results}) == 50
transport = json.loads((dest/'transport-production-reuse.json').read_text())
assert transport['packet_sections']['ok']
assert transport['scope_mismatch']['error']['kind'] == 'bad_request'
assert 'Ran 85 tests' in (dest/'tests.log').read_text()
files = [root/'prism_mcp.py', root/'docs'/'engineering'/'AGENT_RESEARCH.md', *sorted((root/'prism').glob('*.py')),
         *sorted((root/'tests').glob('*.*')), *sorted(root.glob('rebuild_*.py')),
         root/'deploy_rebuild.py', root/'verify_rebuild.py',
         root/'wordpress/wp-content/plugins/prism-research/assets/admin.js',
         root/'wordpress/wp-content/plugins/prism-research/prism-research.php']
files += [p for p in dest.rglob('*') if p.is_file() and p.suffix in ('.json', '.md') and
          'before' not in p.parts and not any(x.endswith('-cache') for x in p.parts) and
          p.name != 'manifest.json']
records = [{'path': str(p.relative_to(root)), 'bytes': p.stat().st_size,
            'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in sorted(set(files))]
(dest/'manifest.json').write_text(json.dumps({'files': records, 'count': len(records),
                                          'final_matrix_cases': 50, 'tests': 85}, indent=2))
print(f'Verified 50 complete final cases, live packet reuse, 85 tests; hashed {len(records)} files.')
