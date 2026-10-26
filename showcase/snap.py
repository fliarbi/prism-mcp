"""Visual QA: screenshot SVG charts in light and dark mode with headless Chrome.

    python3 showcase/snap.py OUT_PREFIX a.svg b.svg ...   -> OUT_PREFIX-light.png, OUT_PREFIX-dark.png
"""
import os
import subprocess
import sys
import tempfile

CHROME = os.path.expanduser("~/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome")
out, files = sys.argv[1], sys.argv[2:]
for mode, bg in (("light", "#ffffff"), ("dark", "#0d1117")):
    html = f"<html><body style='margin:0;padding:10px;background:{bg}'>" + "".join(
        f"<img style='display:block;margin-bottom:10px' src='file://{os.path.abspath(f)}'>" for f in files) + "</body></html>"
    h = tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, dir=os.path.dirname(os.path.abspath(out)))
    h.write(html); h.close()
    flags = ["--blink-settings=preferredColorScheme=0" if mode == "dark" else "--blink-settings=preferredColorScheme=1"]
    subprocess.run([CHROME, "--headless=new", "--no-sandbox", "--hide-scrollbars", *flags,
                    f"--screenshot={out}-{mode}.png", f"--window-size=800,{min(16000, 360 * len(files) + 40)}",
                    "file://" + h.name], capture_output=True, timeout=60)
    os.remove(h.name)
