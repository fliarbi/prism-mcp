"""Real work-stage notifications, scoped to one request and safe across threads."""
from contextlib import contextmanager
from contextvars import ContextVar
import functools

MESSAGES = {
    'queued': 'Your request is in line. We will start shortly.',
    'started': 'We have started working on your request.',
    'database': 'Checking the database for you.',
    'query': 'Understanding your topic and finding the right search terms.',
    'scope': 'Identifying the subject and the question you want answered.',
    'vocabulary': 'Looking up the words researchers use for this topic.',
    'matching': 'Checking that search terms refer to the same subject.',
    'corpus_totals': 'Counting matching records across the research collections.',
    'articles': 'Finding articles about your topic.',
    'reading': 'Reading articles for you and checking what they say.',
    'source_fit': 'Checking that each finding answers your exact question.',
    'themes': 'Ranking news themes for you.',
    'sentiment': 'Checking how the news describes this topic.',
    'trends': 'Checking how this topic has changed over time.',
    'numbers': 'Finding figures and checking them against their sources.',
    'claims': 'Finding the claims in your draft.',
    'sections': 'Ranking the sections your sources can support.',
    'writing': 'Writing from the sources we found for you.',
    'references': 'Putting your source references together.',
    'cached': 'Reusing the results we already checked for you.',
    'finishing': 'Putting your results together.',
    'done': 'Your results are ready.',
    'no_result': 'We finished checking, but did not find enough suitable material.',
    'failed': 'We could not finish this request. Please try again later.',
}
_SINK = ContextVar('prism_progress_sink', default=None)


def emit(stage):
    sink = _SINK.get()
    if sink is not None and stage in MESSAGES:
        # A notification failure must not corrupt the evidence result.
        try:
            sink(stage, MESSAGES[stage])
        except Exception:
            pass


@contextmanager
def track(sink):
    token = _SINK.set(sink)
    try:
        yield
    finally:
        _SINK.reset(token)


def stage(name):
    def decorate(fn):
        @functools.wraps(fn)
        def wrapped(*args, **kwargs):
            emit(name)
            return fn(*args, **kwargs)
        return wrapped
    return decorate
