#!/usr/bin/env python3
"""Isolated staging launch and reproducible read-only workflow probes."""
import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parent
DEST = ROOT / 'out/rebuild-20260912'


def environment(pid, cache_label='staging-cache'):
    env = dict(os.environ)
    for item in Path(f'/proc/{pid}/environ').read_bytes().split(b'\0'):
        if item.startswith(b'PRISM_') and b'=' in item:
            k, v = item.decode().split('=', 1)
            env[k] = v
    env['PRISM_CACHE_DIR'] = str(DEST / cache_label)
    return env


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--launch', action='store_true')
    p.add_argument('--source-pid', type=int)
    p.add_argument('--port', type=int, default=8791)
    p.add_argument('--cache-label', default='staging-cache')
    args = p.parse_args()
    if args.source_pid is None:
        deployed = DEST/'deployment.json'
        args.source_pid = json.loads(deployed.read_text())['new_pid'] if deployed.exists() else 3073370
    DEST.mkdir(exist_ok=True, parents=True)
    if args.launch:
        with (DEST/'staging.log').open('ab') as log:
            proc = subprocess.Popen([sys.executable, str(ROOT/'prism_mcp.py'), '--http', '--port', str(args.port)],
                                    cwd=ROOT, env=environment(args.source_pid, args.cache_label), stdout=log, stderr=log,
                                    start_new_session=True)
        (DEST/'staging-pid.json').write_text(json.dumps({'pid': proc.pid, 'port': args.port}))
        print('staging_pid', proc.pid)
        return
    import httpx
    cases = [
        ('heat', 'research.packet', {'claim': 'Occupational heat reduces worker productivity.',
          'subject_phrases': ['heat stress', 'occupational heat'], 'outcome_phrases': ['productivity'], 'limit': 6}),
        ('battery', 'research.packet', {'claim': 'Sodium ion batteries are an alternative for energy storage.',
          'subject_phrases': ['sodium-ion batteries', 'sodium ion batteries'], 'limit': 6}),
        ('biochar', 'research.packet', {'claim': 'Biochar improves soil water retention.',
          'subject_phrases': ['biochar'], 'outcome_phrases': ['water retention', 'water holding'], 'limit': 6}),
        ('fasting', 'research.packet', {'claim': 'Intermittent fasting improves weight loss compared with continuous calorie restriction.',
          'subject_phrases': ['intermittent fasting'], 'outcome_phrases': ['weight', 'calorie restriction'], 'limit': 6}),
        ('history', 'analysis.history', {'subject_phrases': ['sodium-ion batteries', 'sodium ion batteries']}),
        ('arithmetic', 'research.statistics', {'claim': 'In this supplied dataset, revenue was 100 in 2023 and 120 in 2024. Calculate the percentage increase using only these two values.', 'include_context': False, 'include_trend': False}),
    ]
    with httpx.Client(base_url=f'http://127.0.0.1:{args.port}', timeout=180) as client:
        for name, feature, body in cases:
            result = {'name': name, 'feature': feature, 'args': body}
            for label in ('first', 'repeat'):
                start = time.monotonic()
                try:
                    response = client.post('/v1/'+feature, json=body)
                    data = response.json()
                    result[label] = {'seconds': time.monotonic()-start, 'http': response.status_code, 'response': data}
                except Exception as exc:
                    result[label] = {'seconds': time.monotonic()-start, 'error': str(exc)}
                (DEST/(name+'.json')).write_text(json.dumps(result, indent=2, ensure_ascii=False))
                print(name, label, round(result[label]['seconds'], 3), result[label].get('response', {}).get('ok'), flush=True)
            payload = result['first'].get('response', {}).get('data') or {}
            if payload.get('packet_id'):
                page = client.post('/v1/research.packet_read', json={'packet_id': payload['packet_id'], 'limit': 8}).json()
                (DEST/(name+'-sources.json')).write_text(json.dumps(page, indent=2, ensure_ascii=False))
            if payload.get('history_id'):
                scenarios = client.post('/v1/analysis.scenarios', json={'history_id': payload['history_id']}).json()
                (DEST/'history-scenarios.json').write_text(json.dumps(scenarios, indent=2))


if __name__ == '__main__':
    main()
