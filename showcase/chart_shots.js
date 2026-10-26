// Screenshot chart elements of a tabbed report: node chart_shots.js page.html outdir "id:name,id:name"
const { chromium } = (() => { try { return require('playwright-core'); } catch (e) { return require(process.env.PLAYWRIGHT_CORE || require('os').homedir() + '/projects/prism_stocks/node_modules/playwright-core'); } })();
const path = require('path');
(async () => {
  const [page, out, spec] = process.argv.slice(2);
  const b = await chromium.launch({ executablePath: process.env.HOME + '/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome', args: ['--no-sandbox', '--allow-file-access-from-files'] });
  const p = await b.newPage({ viewport: { width: 1200, height: 1000 }, deviceScaleFactor: 1.5 });
  await p.goto('file://' + page, { waitUntil: 'networkidle' });
  await p.waitForTimeout(1500);
  const tabs = await p.$$('.tabs button');
  const want = Object.fromEntries(spec.split(',').map(x => x.split(':')));
  const done = new Set();
  for (const t of tabs) {
    await t.click(); await p.waitForTimeout(1200);
    for (const [id, name] of Object.entries(want)) {
      if (done.has(id)) continue;
      const el = await p.$('.panel.on #' + id);
      if (!el) continue;
      const box = await el.boundingBox();
      if (!box || box.width < 20) continue;
      await el.screenshot({ path: path.join(out, name + '.png') });
      done.add(id);
    }
  }
  console.log([...done].join(','));
  await b.close();
})();
