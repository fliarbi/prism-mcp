"""Short, shared reachability checks before expensive distributed reads.

Topology comes from ClickHouse, and a shard fails only when ALL its replicas
are unreachable. This is an early outage check, not a replacement for strict
queries or the corpus row floors. No failed result is cached as research data.
"""
import os
import re
import socket
import threading
import time
from concurrent.futures import ThreadPoolExecutor

_LOCK = threading.RLock()
_TOPOLOGY = ({}, {}, 0.0)
_PROBES = {}
_PROBE_LOCKS = {}
PROBE_SECONDS = 1.5
SUCCESS_TTL = 15.0
FAILURE_TTL = 3.0


def _topology():
    global _TOPOLOGY
    from . import ch
    with _LOCK:
        if time.monotonic() < _TOPOLOGY[2]:
            return _TOPOLOGY[:2]
        tables = ch._request("SELECT database,name,engine_full FROM system.tables "
                             "WHERE engine='Distributed' FORMAT TabSeparated", 5, True)
        nodes = ch._request("SELECT cluster,shard_num,host_address,port FROM system.clusters "
                            "FORMAT TabSeparated", 5, True)
        mapping, clusters = {}, {}
        for line in tables.splitlines():
            db, name, engine = [ch._unescape(x) for x in line.split('\t', 2)]
            match = re.match(r"Distributed\('([^']+)'", engine)
            if match:
                mapping[f'{db}.{name}'] = match[1]
        for line in nodes.splitlines():
            cluster, shard, host, port = [ch._unescape(x) for x in line.split('\t')]
            clusters.setdefault(cluster, {}).setdefault(shard, []).append((host, int(port)))
        _TOPOLOGY = (mapping, clusters, time.monotonic() + 300)
        return mapping, clusters


def _reachable(address):
    with _LOCK:
        lock = _PROBE_LOCKS.setdefault(address, threading.Lock())
    with lock:
        hit = _PROBES.get(address)
        if hit and time.monotonic() < hit[1]:
            return hit[0]
        try:
            with socket.create_connection(address, timeout=PROBE_SECONDS):
                pass
            ok = True
        except OSError:
            ok = False
        _PROBES[address] = (ok, time.monotonic() + (SUCCESS_TTL if ok else FAILURE_TTL))
        return ok


def require_tables(tables):
    from . import ch
    if os.environ.get("PRISM_ALLOW_PARTIAL") == "1":
        return  # operator switch (see ch.chq): answer from the shards that respond; coverage still says partial
    mapping, clusters = _topology()
    needed = {mapping[t] for t in tables if t in mapping}
    shards = [(cluster, shard, replicas) for cluster in needed
              for shard, replicas in clusters.get(cluster, {}).items()]
    addresses = sorted({a for _, _, replicas in shards for a in replicas})
    if not addresses:
        return
    with ThreadPoolExecutor(max_workers=min(16, len(addresses))) as pool:
        states = dict(zip(addresses, pool.map(_reachable, addresses)))
    failed = [(cluster, shard, replicas) for cluster, shard, replicas in shards
              if not any(states[a] for a in replicas)]
    if failed:
        hosts = sorted({f'{h}:{p}' for _, _, replicas in failed for h, p in replicas})
        raise ch.CHError('ClickHouse distributed storage unavailable: '
                         f'{len(failed)} shard(s) have no reachable replica: '
                         + ', '.join(hosts) + '. Retry after cluster connectivity recovers.')


def check_sql(sql):
    from . import ch
    tables = [table for table in ch.TABLE.values()
              if re.search(r'(?<![\w.])' + re.escape(table) + r'(?![\w])', sql)]
    if tables:
        require_tables(tables)
