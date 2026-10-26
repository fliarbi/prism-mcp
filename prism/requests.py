"""Bounded asynchronous editor requests backed by durable jobs and progress."""
import inspect
import typing
from pydantic import TypeAdapter, ValidationError
from . import jobs, progress

ALLOWED = frozenset({
    'research.evidence', 'research.counter_evidence', 'research.statistics',
    'research.audit', 'research.citations', 'research.evidence_card', 'research.browse',
    'compose.sections', 'compose.section', 'compose.continue', 'compose.titles',
    'news.trends', 'news.recent', 'news.critical', 'news.overview', 'news.resolve',
    'news.themes', 'news.sentiment',
    'research.missing', 'research.radar', 'research.source_ranking', 'research.gaps',
    'news.compare', 'news.entities', 'news.geography', 'news.sources',
    'research.plan', 'research.packet', 'research.packet_read',
    'analysis.history', 'analysis.scenarios',
})
_REGISTRY = {}


def configure(registry):
    _REGISTRY.clear()
    _REGISTRY.update({s['feature']:s['fn'] for s in registry.values()})


def submit_request(feature, args):
    if feature not in ALLOWED or feature not in _REGISTRY:
        return {'available':False, 'kind':'bad_request', 'reason':'This feature does not support editor requests.'}
    if not isinstance(args, dict):
        return {'available':False, 'kind':'bad_request', 'reason':'args must be a JSON object.'}
    fn = _REGISTRY[feature]
    try:
        bound = inspect.signature(fn).bind(**args)
        hints = typing.get_type_hints(fn)
        validated = {k:TypeAdapter(hints[k]).validate_python(v) if k in hints else v
                     for k,v in bound.arguments.items()}
    except (ValueError, TypeError, ValidationError) as e:
        return {'available':False, 'kind':'bad_request', 'reason':str(e)}
    # Never create a job that merely spawns a second job.
    if feature == 'compose.section':
        validated['background'] = False
    out = jobs.start('request:'+feature, fn, validated, progress_events=True)
    if out.get('available') is False:
        return out
    rid = out['job_id']
    return {'available':True, 'request_id':rid, 'status':'queued',
            'requested_feature':feature, 'message':progress.MESSAGES['queued'],
            'poll':f'/v1/system.request_status?request_id={rid}', 'poll_after_ms':1000}


def request_status(request_id, after=0):
    if not isinstance(after, int) or after < 0:
        return {'available':False, 'kind':'bad_request', 'reason':'after must be a non-negative integer.'}
    state = jobs.status(request_id)
    if not state.get('available'):
        return state
    if not state.get('kind', '').startswith('request:'):
        return {'available':False, 'kind':'bad_request', 'reason':'Use system.job for this job ID.'}
    history = jobs.events(request_id, after)
    status = state['status']
    result = state.get('result')
    # A heartbeat describes elapsed waiting; it does not invent completed work.
    waiting = status in ('queued', 'running')
    heartbeat = (f"Still working on your request ({int(state['seconds'])} seconds elapsed). "
                 "The latest step is shown below; no result has been confirmed yet.") if waiting else None
    if status == 'done':
        history['message'] = progress.MESSAGES['done']
    elif status == 'failed':
        error = result.get('error') if isinstance(result, dict) else None
        kind = error.get('kind') if isinstance(error, dict) else None
        history['message'] = progress.MESSAGES['no_result' if kind in ('no_data', 'not_resolvable') else 'failed']
    return {'available':True, 'request_id':request_id, 'status':status,
            'requested_feature':state['kind'][8:], 'elapsed_seconds':state['seconds'],
            'poll_after_ms':1000 if status in ('queued','running') else None,
            'heartbeat': heartbeat,
            **history, **({'result':result} if result is not None else {})}
