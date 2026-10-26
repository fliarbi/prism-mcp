"""report_check — render an HTML report the way its reader will, and say what is broken.

A model that writes a long, data-heavy HTML report makes page mistakes a reader sees at once and a model
never does: a chart sized to a container that has no width yet (it draws at 0 px), one stray brace that
stops every chart on the page, a manifest that lists a chart the page never draws. This renders the page in
headless Chrome, measures every Vega view, collects console errors, and compares the page with its
manifest, so the author can fix the page before handing it over.
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import tempfile

CHROME = os.environ.get("PRISM_CHROME", os.path.expanduser(
    "~/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome"))
_ASSETS = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "showcase", "assets")
MAPS = [os.path.join(_ASSETS, "world_india_official.geojson"), os.path.join(_ASSETS, "india_states_official.geojson")]


def _manifest(html):
    m = re.search(r'<script[^>]*id=["\'](?:report|prism)-manifest["\'][^>]*>(.*?)</script>', html, re.S | re.I)
    if not m:
        return None, "no <script type=\"application/json\" id=\"report-manifest\"> found"
    try:
        return json.loads(m.group(1)), ""
    except Exception as e:
        return None, f"the manifest is not valid JSON ({e})"


def check(html: str) -> dict:
    html = html.strip()
    m = re.search(r"```html\s*\n(.*?)```", html, re.S | re.I)
    if m:
        html = m.group(1)
    issues, fixes = [], []
    man, merr = _manifest(html)
    if merr:
        issues.append(merr)
        fixes.append("add the manifest script block with verdict, charts, exports, calls and references")
    d = tempfile.mkdtemp(prefix="prism_report_")
    try:
        page = os.path.join(d, "report.html")
        open(page, "w").write(html)
        for f in MAPS:
            if os.path.exists(f):
                shutil.copy(f, os.path.join(d, os.path.basename(f)))
        r = subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--hide-scrollbars", "--virtual-time-budget=25000",
                            "--allow-file-access-from-files", "--window-size=1280,2400", "--enable-logging=stderr",
                            "--v=0", "--dump-dom", "file://" + page], capture_output=True, text=True, timeout=150)
        dom = r.stdout
    finally:
        shutil.rmtree(d, ignore_errors=True)
    errors = [re.sub(r"^.*?CONSOLE:\d+\]\s*", "", l)[:240] for l in r.stderr.splitlines()
              if "CONSOLE" in l and re.search(r"error|uncaught", l, re.I)]
    for e in errors[:6]:
        issues.append(f"console error: {e}")
    if errors:
        fixes.append("a script error stops every chart after it; fix the reported line (unbalanced braces and "
                     "trailing commas are the usual cause) and keep each vegaEmbed call independent")
    views = []
    for vm in re.finditer(r'<(canvas|svg)[^>]*class="[^"]*\bmarks\b[^"]*"[^>]*>', dom):
        tag = vm.group(0)
        w = re.search(r'width="([\d.]+)"', tag)
        views.append(float(w.group(1)) if w else None)
    zero = sum(1 for w in views if w is not None and w < 10)
    if zero:
        issues.append(f"{zero} of {len(views)} charts render at zero width")
        fixes.append('give every spec a pixel width ("width": 640) instead of "container", or give the chart\'s '
                     "element an explicit CSS width; a container that is not laid out yet has no width")
    charts = (man or {}).get("charts") or []
    missing = []
    for c in charts:
        cid = c.get("id")
        if cid and not re.search(rf'id=["\']{re.escape(str(cid))}["\']', dom):
            missing.append(cid)
    if missing:
        issues.append(f"manifest charts with no element on the page: {missing[:8]}")
        fixes.append("draw each manifest chart with vegaEmbed('#<chart id>', spec) into an element with that id")
    if charts and len(views) < len(charts):
        issues.append(f"the manifest lists {len(charts)} charts but {len(views)} rendered")
    maps = [c for c in charts if c.get("kind") == "map"]
    if maps and "world_india_official.geojson" not in html and "india_states_official.geojson" not in html:
        issues.append("a map is listed but the page does not load world_india_official.geojson")
        fixes.append("load maps from the relative URL world_india_official.geojson (India drawn with its official outline)")
    vis = re.sub(r"<script.*?</script>|<style.*?</style>|<svg.*?</svg>|<[^>]+>", " ", dom, flags=re.S)
    nums = [x for x in re.finditer(r"(?<![\w.#/-])\d[\d,]*(?:\.\d+)?%?", vis) if not re.fullmatch(r"(19|20)\d\d", x.group(0))]
    untagged = sum(1 for x in nums if not re.search(r"[\[(](c|r)\d+[\])]|\(est", vis[x.end():x.end() + 260]))
    out = {"renders": bool(dom.strip()), "charts_in_manifest": len(charts), "charts_rendered": len(views) - zero,
           "zero_width_charts": zero, "console_errors": errors[:6], "manifest_ok": not merr,
           "numbers_on_page": len(nums), "numbers_without_a_nearby_source_tag": untagged,
           "issues": issues, "fixes": list(dict.fromkeys(fixes)), "ready": not issues}
    return out
