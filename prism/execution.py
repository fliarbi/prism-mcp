"""Bounded blocking work shared by MCP and REST, off the event loop."""
import os
import time
import anyio

_DATA_LIMIT = anyio.CapacityLimiter(int(os.environ.get('PRISM_REQUEST_WORKERS', '8')))
_HEALTH_LIMIT = anyio.CapacityLimiter(2)
_CONTROL_LIMIT = anyio.CapacityLimiter(2)
_CONTROL_NAMES = {'job_status', 'list_jobs', 'list_features', 'client_surface',
                  'submit_request', 'request_status'}


async def run(fn, *args, health=False, **kwargs):
    queued = time.monotonic()
    def invoke():
        started = time.monotonic()
        result = fn(*args, **kwargs)
        if isinstance(result, dict) and 'feature' in result and 'ok' in result:
            result = {**result, 'meta': {**(result.get('meta') or {}),
                      'queue_seconds': round(started - queued, 4),
                      'execution_seconds': round(time.monotonic() - started, 4)}}
        return result
    limiter = (_HEALTH_LIMIT if health else _CONTROL_LIMIT
               if getattr(fn, '__name__', '') in _CONTROL_NAMES else _DATA_LIMIT)
    return await anyio.to_thread.run_sync(
        invoke, limiter=limiter)
