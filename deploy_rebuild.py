#!/usr/bin/env python3
"""Explicit graceful replacement of the known standalone HTTP process only."""
import argparse
import json
import os
from pathlib import Path
import signal
import subprocess
import sys
import time
import httpx

ROOT = Path(__file__).resolve().parent
DEST = ROOT/'out/rebuild-20260912'


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--pid', type=int, required=True)
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    command = Path(f'/proc/{args.pid}/cmdline').read_bytes().split(b'\0')
    assert str(ROOT/'prism_mcp.py').encode() in command and b'8790' in command, 'Unexpected process; refusing replacement.'
    env = dict(os.environ)
    for item in Path(f'/proc/{args.pid}/environ').read_bytes().split(b'\0'):
        if item.startswith(b'PRISM_') and b'=' in item:
            key, value = item.decode().split('=', 1); env[key] = value
    with httpx.Client(timeout=10) as client:
        jobs = client.get('http://127.0.0.1:8790/v1/system.jobs?limit=100').json()
        active = [x for x in jobs['data']['jobs'] if x['status'] in ('queued', 'running')]
        assert not active, 'Active jobs exist; retry when idle.'
    if not args.apply:
        print('Verified standalone process and no active jobs. Use --apply for graceful replacement.')
        return
    os.kill(args.pid, signal.SIGTERM)
    for _ in range(100):
        try:
            stat = Path(f'/proc/{args.pid}/stat').read_text().rsplit(')', 1)[1].split()[0]
            if stat == 'Z':
                break
        except FileNotFoundError:
            break
        time.sleep(.2)
    else:
        raise RuntimeError('Old process did not stop gracefully; no forced termination performed.')
    with (DEST/'production.log').open('ab') as log:
        new = subprocess.Popen([sys.executable, str(ROOT/'prism_mcp.py'), '--http', '--port', '8790'],
                               cwd=ROOT, env=env, stdout=log, stderr=log, start_new_session=True)
    result = {'previous_pid': args.pid, 'new_pid': new.pid, 'port': 8790, 'ready': False}
    for _ in range(50):
        try:
            response = httpx.get('http://127.0.0.1:8790/livez', timeout=2)
            if response.is_success and response.json().get('features', 0) >= 63:
                result['ready'] = True; result['health'] = response.json(); break
        except httpx.HTTPError:
            pass
        time.sleep(.2)
    (DEST/'deployment.json').write_text(json.dumps(result, indent=2))
    print(json.dumps(result))
    assert result['ready'], 'Replacement did not become live; inspect production.log and saved source backup.'


if __name__ == '__main__':
    main()
