"""Prism research layer — the engine behind the Prism MCP server."""
import os as _os


def _load_env_file():
    """Deployment settings (index host and login, chart publish host, …) live in an untracked .env at the repo root,
    or in the file PRISM_ENV_FILE names. Lines are KEY=VALUE; variables already set in the environment win."""
    path = _os.environ.get("PRISM_ENV_FILE") or _os.path.join(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))), ".env")
    try:
        with open(path) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, v = line.split("=", 1)
                    _os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
    except OSError:
        pass


_load_env_file()
