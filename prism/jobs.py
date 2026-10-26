"""Persistent jobs: detect dead owners, explicitly retry, preserve expired results.

Jobs can publish before a process stops, so interrupted work is never replayed
automatically. OS file locks bound execution across processes on this host.
"""
from __future__ import annotations
import fcntl
import json
import os
from pathlib import Path
import socket
import sqlite3
import threading
import time
import traceback
import uuid
from . import cache
from . import progress as notifications

DB_PATH = os.path.join(cache.CACHE_DIR, 'prism_jobs.db')
KEEP_SECONDS = int(os.environ.get('PRISM_JOB_TTL', '86400'))
MAX_RUNNING = int(os.environ.get('PRISM_JOB_WORKERS', '3'))
MAX_QUEUED = int(os.environ.get('PRISM_JOB_QUEUE', '100'))
_LOCK = threading.RLock()
_CONN = None
_HANDLERS = {}


def _identity(pid=None):
    pid = pid or os.getpid()
    start = Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()[19]
    boot = Path('/proc/sys/kernel/random/boot_id').read_text().strip()
    return f'{socket.gethostname()}:{boot}:{pid}:{start}'


def _owner_alive(owner):
    if not owner:
        return None
    host, boot, pid, start = owner.split(':')
    if host != socket.gethostname():
        return None
    try:
        if Path(f'/proc/{pid}/stat').read_text().rsplit(')', 1)[1].split()[0] == 'Z':
            return False
        return _identity(int(pid)) == owner
    except (OSError, ValueError):
        return False


def _conn():
    global _CONN
    if _CONN is None:
        c = sqlite3.connect(DB_PATH, check_same_thread=False, timeout=15)
        c.execute('PRAGMA journal_mode=WAL')
        c.execute('''CREATE TABLE IF NOT EXISTS jobs (
            id TEXT PRIMARY KEY, kind TEXT, status TEXT, args TEXT,
            result TEXT, error TEXT, done INTEGER, total INTEGER, label TEXT,
            created REAL, updated REAL)''')
        for name, decl in [('owner', 'TEXT'), ('archived', 'INTEGER DEFAULT 0')]:
            if name not in {r[1] for r in c.execute('PRAGMA table_info(jobs)')}:
                try:
                    c.execute(f'ALTER TABLE jobs ADD COLUMN {name} {decl}')
                except sqlite3.OperationalError:
                    if name not in {r[1] for r in c.execute('PRAGMA table_info(jobs)')}:
                        raise
        c.execute('''CREATE TABLE IF NOT EXISTS job_events (
            job_id TEXT, seq INTEGER, stage TEXT, message TEXT, created REAL,
            PRIMARY KEY(job_id, seq))''')
        c.commit()
        _CONN = c
    return _CONN


def _write(job_id, **fields):
    fields['updated'] = time.time()
    with _LOCK:
        c = _conn()
        c.execute(f"UPDATE jobs SET {', '.join(k+'=?' for k in fields)} WHERE id=?",
                  (*fields.values(), job_id))
        c.commit()


def register(kind, fn, supports_progress=False):
    _HANDLERS[kind] = (fn, supports_progress)


def reconcile():
    with _LOCK:
        c = _conn()
        rows = c.execute("SELECT id,owner FROM jobs WHERE status IN ('queued','running')").fetchall()
        for jid, owner in rows:
            if _owner_alive(owner) is False:
                _write(jid, status='failed', error='interrupted: owner process exited; '
                       'inspect existing artifacts before explicitly retrying')


def reap():
    """Expire terminal jobs from the API while retaining their stored results."""
    with _LOCK:
        c = _conn()
        cur = c.execute("UPDATE jobs SET archived=1 WHERE archived=0 AND "
                        "status IN ('done','failed') AND updated < ?",
                        (time.time() - KEEP_SECONDS,))
        c.commit()
        return cur.rowcount


def _slot():
    while True:
        for i in range(MAX_RUNNING):
            f = open(os.path.join(cache.CACHE_DIR, f'prism-job-slot-{i}.lock'), 'a')
            try:
                fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
                return f
            except BlockingIOError:
                f.close()
        time.sleep(.25)


def start(kind, fn, args, supports_progress=False, progress_events=False):
    register(kind, fn, supports_progress)
    reconcile()
    reap()
    jid, now = 'job_' + uuid.uuid4().hex[:16], time.time()
    with _LOCK:
        c = _conn()
        c.execute('BEGIN IMMEDIATE')
        try:
            count = c.execute("SELECT count(*) FROM jobs WHERE status IN ('queued','running')").fetchone()[0]
            if count >= MAX_QUEUED + MAX_RUNNING:
                c.rollback()
                return {'available': False, 'kind': 'upstream', 'reason': 'job queue is full'}
            c.execute('INSERT INTO jobs(id,kind,status,args,done,total,created,updated,owner) '
                      'VALUES (?,?,?,?,?,?,?,?,?)',
                      (jid, kind, 'queued', json.dumps(args, default=str), 0, 0, now, now, _identity()))
            c.commit()
        except Exception:
            c.rollback()
            raise

    def run():
        slot = None
        try:
            slot = _slot()
            _write(jid, status='running')
            kw = dict(args)
            if supports_progress:
                kw['progress'] = lambda d, t, label='': _write(jid, done=d, total=t, label=str(label)[:100])
            with notifications.track(
                    (lambda stage, message: append_event(jid, stage, message))
                    if progress_events else None):
                notifications.emit('started')
                out = fn(**kw)
                notifications.emit('finishing')
            failed = isinstance(out, dict) and (out.get('available') is False or out.get('ok') is False)
            reason = ((out.get('error') or {}).get('reason') if isinstance(out.get('error'), dict)
                      else out.get('error')) if isinstance(out, dict) else None
            _write(jid, status='failed' if failed else 'done', result=json.dumps(out, default=str),
                   error=(reason or out.get('reason') or 'job returned no usable result') if failed else None)
            if progress_events:
                error_kind = out.get('error', {}).get('kind') if isinstance(out, dict) and isinstance(out.get('error'), dict) else None
                stage = ('no_result' if failed and error_kind in ('no_data', 'not_resolvable')
                         else 'failed' if failed else 'done')
                append_event(jid, stage, notifications.MESSAGES[stage])
        except Exception as e:
            _write(jid, status='failed', error=f'{type(e).__name__}: {e}\n{traceback.format_exc()[-1200:]}')
            if progress_events:
                append_event(jid, 'failed', notifications.MESSAGES['failed'])
        finally:
            if slot:
                slot.close()

    if progress_events:
        append_event(jid, 'queued', notifications.MESSAGES['queued'])
    threading.Thread(target=run, daemon=True, name=jid).start()
    return {'job_id': jid, 'status': 'queued', 'kind': kind,
            'poll': f'/v1/system.job?job_id={jid}', 'note': 'poll until done or failed'}


def append_event(job_id, stage, message):
    """Bounded persistent history. Sequence numbers are local to each job."""
    with _LOCK:
        c = _conn()
        c.execute('BEGIN IMMEDIATE')
        try:
            previous = c.execute('SELECT seq,stage FROM job_events WHERE job_id=? '
                                 'ORDER BY seq DESC LIMIT 1', (job_id,)).fetchone()
            if previous and previous[1] == stage:
                c.commit()
                return
            seq = (previous[0] if previous else 0) + 1
            c.execute('INSERT INTO job_events VALUES (?,?,?,?,?)',
                      (job_id, seq, stage, message, time.time()))
            c.execute('DELETE FROM job_events WHERE job_id=? AND seq<=?', (job_id, seq-128))
            c.commit()
        except Exception:
            c.rollback()
            raise


def events(job_id, after=0):
    with _LOCK:
        c = _conn()
        rows = c.execute('SELECT seq,stage,message,created FROM job_events '
                         'WHERE job_id=? AND seq>? ORDER BY seq LIMIT 128', (job_id, after)).fetchall()
        first = c.execute('SELECT min(seq) FROM job_events WHERE job_id=?', (job_id,)).fetchone()[0]
        latest = c.execute('SELECT stage,message FROM job_events WHERE job_id=? '
                           'ORDER BY seq DESC LIMIT 1', (job_id,)).fetchone()
    return {'events': [{'sequence':r[0], 'stage':r[1], 'message':r[2], 'at':r[3]} for r in rows],
            'next_cursor':rows[-1][0] if rows else after,
            'buffer_truncated':bool(first and after < first-1),
            'message':latest[1] if latest else notifications.MESSAGES['queued']}


def status(job_id):
    reconcile()
    reap()
    with _LOCK:
        row = _conn().execute('SELECT id,kind,status,result,error,done,total,label,created,updated,archived,owner '
                              'FROM jobs WHERE id=?', (job_id,)).fetchone()
    if not row or row[10]:
        return {'available': False, 'kind': 'no_data',
                'reason': 'job expired (result retained in storage)' if row else 'no job with that id'}
    jid, kind, st, result, error, done, total, label, created, updated, _, owner = row
    done = total if st == 'done' and total else done or 0
    out = {'available': True, 'job_id': jid, 'kind': kind, 'status': st,
           'progress': {'done': done, 'total': total or 0, 'label': label,
                        'pct': round(100 * done / total) if total else None},
           'seconds': round((time.time() if st in ('queued', 'running') else updated) - created, 1),
           'retryable': st == 'failed' and kind in _HANDLERS}
    if result:
        out['result'] = json.loads(result)
    if error:
        out['error'] = error
    if st in ('queued', 'running') and not owner:
        out['recovery_note'] = 'legacy job owner unknown; not automatically replayed'
    return out


def retry(job_id):
    state = status(job_id)
    if not state.get('retryable'):
        return {'available': False, 'kind': 'bad_request', 'reason': 'job is not retryable'}
    with _LOCK:
        kind, args = _conn().execute('SELECT kind,args FROM jobs WHERE id=?', (job_id,)).fetchone()
    fn, progress = _HANDLERS[kind]
    return {**start(kind, fn, json.loads(args), progress, progress_events=kind.startswith('request:')), 'retry_of': job_id}


def recent(limit=20):
    reconcile()
    reap()
    with _LOCK:
        rows = _conn().execute('SELECT id,kind,status,done,total,created FROM jobs '
                              'WHERE archived=0 ORDER BY created DESC LIMIT ?', (max(1, min(limit, 100)),)).fetchall()
    return {'available': True, 'jobs': [
        {'job_id': r[0], 'kind': r[1], 'status': r[2],
         'progress': f"{r[4] if r[2] == 'done' else r[3]}/{r[4]}" if r[4] else None,
         'age_seconds': round(time.time() - r[5], 1)} for r in rows]}
