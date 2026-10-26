#!/usr/bin/env python3
"""Live REST, async progress and actual MCP-wire verification, no publishing."""
import argparse
import asyncio
import json
from pathlib import Path
import time

import httpx
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client


async def main(port, destination):
    out = {}
    url = f'http://127.0.0.1:{port}'
    with httpx.Client(base_url=url, timeout=30) as client:
        start = time.monotonic()
        r = client.post('/v1/research.packet', headers={'Prefer': 'respond-async'}, json={
            'claim': 'Heat stress reduces worker productivity.',
            'subject_phrases': ['occupational heat', 'heat stress'],
            'outcome_phrases': ['productivity'], 'limit': 4})
        out['submit'] = {'http': r.status_code, 'seconds': time.monotonic()-start, 'response': r.json()}
        assert r.status_code == 202, out['submit']
        rid = r.json()['data']['request_id']; cursor = 0; out['polls'] = []
        for _ in range(90):
            start = time.monotonic()
            response = client.get('/v1/system.request_status', params={'request_id': rid, 'after': cursor}).json()
            out['polls'].append({'seconds': time.monotonic()-start, 'response': response})
            state = response['data']; cursor = state['next_cursor']
            if state['status'] in ('done', 'failed'):
                break
            await asyncio.sleep(1)
        assert state['status'] == 'done', state
        pid = state['result']['data']['packet_id']
        out['packet_read'] = client.post('/v1/research.packet_read', json={'packet_id': pid}).json()
        assert out['packet_read']['ok']
        start = time.monotonic()
        out['packet_sections'] = client.post('/v1/compose.sections', json={
            'topic': 'Heat stress reduces worker productivity.', 'packet_id': pid}).json()
        out['packet_sections_seconds'] = time.monotonic()-start
        assert out['packet_sections']['ok'], out['packet_sections']
        out['scope_mismatch'] = client.post('/v1/compose.sections', json={
            'topic': 'An entirely different subject.', 'packet_id': pid}).json()
        assert out['scope_mismatch']['error']['kind'] == 'bad_request'
        out['optional_null'] = client.post('/v1/research.plan', json={
            'question': 'Does exercise improve wellbeing?', 'outcome_phrases': None}).json()
        assert out['optional_null']['ok']
        rows = [{'year': 2018+i, 'value': 100+10*i} for i in range(8)]
        out['scenario_rest'] = client.post('/v1/analysis.scenarios', json={'observations': rows}).json()
        assert out['scenario_rest']['ok']
        out['catalog'] = client.get('/v1').json()
        out['openapi'] = client.get('/v1/openapi.json').json()
    async with streamablehttp_client(url+'/mcp', timeout=30, sse_read_timeout=60) as (read, write, _):
        async with ClientSession(read, write) as session:
            out['initialize'] = (await session.initialize()).model_dump(mode='json')
            listing = await session.list_tools()
            out['mcp_tools'] = [{'name': t.name, 'annotations': t.annotations.model_dump(mode='json') if t.annotations else None} for t in listing.tools]
            for name, args in [('research_plan', {'question': 'How has energy storage research changed?'}),
                               ('research_packet_read', {'packet_id': pid, 'limit': 1}),
                               ('trend_scenarios', {'observations': rows})]:
                result = await session.call_tool(name, args)
                out[name] = result.model_dump(mode='json')
                assert result.structuredContent['ok'], out[name]
    destination.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    print(json.dumps({'tools': len(out['mcp_tools']), 'ack_seconds': out['submit']['seconds'],
                      'polls': len(out['polls']), 'final_status': state['status'],
                      'packet_sections_seconds': out['packet_sections_seconds'],
                      'max_poll_seconds': max(x['seconds'] for x in out['polls'])}))


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', type=int, default=8791)
    parser.add_argument('--output', type=Path, default=Path('out/rebuild-20260912/transport-staging.json'))
    args = parser.parse_args()
    asyncio.run(main(args.port, args.output))
