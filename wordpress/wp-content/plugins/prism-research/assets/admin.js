/* Prism Research — admin + editor. Vanilla JS; talks only to this site's REST proxy. */
(function () {
  'use strict';
  const H = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const pending = new Map();
  const call = (feature, args = {}, timeout = 120) => {
    const key = JSON.stringify([feature, args, timeout]);
    if (pending.has(key)) return pending.get(key);
    const request = wp.apiFetch({ path: 'prism/v1/call', method: 'POST', data: { feature, args, timeout } }).finally(() => pending.delete(key));
    pending.set(key, request);
    return request;
  };
  const pause = (ms) => new Promise((resolve) => setTimeout(resolve, ms));
  const activeRequests = new Map();
  function runRequest(feature, args = {}, update = () => {}) {
    const key = JSON.stringify([feature, args]);
    if (activeRequests.has(key)) return activeRequests.get(key);
    const task = (async () => {
      const start = await call('system.request', { feature, args }, 30);
      const requestId = start && start.data && start.data.request_id;
      if (!start || !start.ok || !requestId) return start || {ok:false,error:{reason:'Could not start the request.'}};
      let cursor = 0, failures = 0, history = [];
      const deadline = Date.now() + 15 * 60 * 1000;
      update({ ...start.data, events: history });
      const interrupted = (reason) => ({ok:false,request_id:requestId,error:{kind:'request interrupted',reason:reason + ' Request ID: ' + requestId + '. No new request has been started.'}});
      while (Date.now() < deadline) {
        await pause(1200);
        const r = await call('system.request_status', {request_id:requestId, after:cursor}, 30)
          .catch(() => ({ok:false,error:{kind:'transport'}}));
        if (!r || !r.ok) {
          if (r && r.error && r.error.kind === 'no_data') return interrupted('This request is no longer available.');
          if (++failures >= 3) return interrupted('We lost the connection. Your work may still be running.');
          continue;
        }
        failures = 0;
        const d = r.data || {};
        const fresh = (d.events || []).filter((e) => e.sequence > cursor);
        history = history.concat(fresh).slice(-12);
        cursor = Math.max(cursor, Number(d.next_cursor) || 0);
        update({...d, events:history});
        if (d.status === 'done' || d.status === 'failed') {
          if (d.result && typeof d.result.ok === 'boolean') return d.result;
          return interrupted(d.message || 'We could not finish this request.');
        }
      }
      return interrupted('This is taking longer than expected. You can check the request again later.');
    })().finally(() => activeRequests.delete(key));
    activeRequests.set(key, task);
    return task;
  }
  async function awaitJob(start) {
    const jobId = start.data && start.data.job_id;
    if (!start.ok || !jobId) return start;
    const deadline = Date.now() + 10 * 60 * 1000;
    let failures = 0;
    while (Date.now() < deadline) {
      await pause(1500);
      const r = await call('system.job', { job_id: jobId }, 30).catch((e) => ({ ok: false, error: { kind: 'transport', reason: e.message } }));
      if (!r.ok) {
        if (r.error && r.error.kind === 'no_data') return r;
        if (++failures >= 3) return r;
        continue;
      }
      failures = 0;
      const d = r.data || {};
      if (d.status === 'failed') return { ok: false, error: { kind: 'job failed', reason: d.error || 'The section could not be written.' } };
      if (d.status === 'done') {
        const result = d.result || {};
        if ('ok' in result) return result;
        return { ok: result.available !== false, data: result, error: { kind: result.kind, reason: result.reason } };
      }
    }
    return { ok: false, error: { kind: 'timeout', reason: `Still running. Check job ${jobId} on the Jobs page before starting it again.` } };
  }

  /* ── editor bridge: selection, whole draft, insertion ── */
  const Editor = {
    isBlock() { return !!(window.wp && wp.data && wp.data.select('core/block-editor')); },
    selection() {
      const s = window.getSelection && window.getSelection().toString().trim();
      if (s) return s;
      if (this.isBlock()) { const b = wp.data.select('core/block-editor').getSelectedBlock(); if (b && b.attributes && b.attributes.content) return String(b.attributes.content).replace(/<[^>]+>/g, '').trim(); }
      return '';
    },
    draftText() {
      if (this.isBlock()) return (wp.data.select('core/editor').getEditedPostContent() || '').replace(/<!--[\s\S]*?-->/g, '').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
      if (window.tinymce && tinymce.activeEditor) return tinymce.activeEditor.getContent({ format: 'text' });
      const ta = document.getElementById('content'); return ta ? ta.value : '';
    },
    lastParagraph() { const t = this.draftText(); const parts = t.split(/\n+|(?<=\.)\s{2,}/).filter(Boolean); return parts.slice(-2).join(' ').slice(-1200) || t.slice(-1200); },
    title() { if (this.isBlock()) return wp.data.select('core/editor').getEditedPostAttribute('title') || ''; const t = document.getElementById('title'); return t ? t.value : ''; },
    insertHTML(html) {
      if (this.isBlock() && wp.blocks) {
        const blocks = wp.blocks.rawHandler({ HTML: html });
        wp.data.dispatch('core/block-editor').insertBlocks(blocks);
        return;
      }
      if (window.tinymce && tinymce.activeEditor && !tinymce.activeEditor.isHidden()) { tinymce.activeEditor.execCommand('mceInsertContent', false, html); return; }
      const ta = document.getElementById('content'); if (ta) ta.value += '\n' + html + '\n';
    },
  };

  /* ── renderers for each feature's envelope ── */
  const R = {
    progress(d) {
      return `<div class="prism-card" role="status" aria-live="polite"><p><span class="prism-spinner"></span>${H(d.message || 'Working on your request…')}</p>${d.heartbeat ? `<p><small>${H(d.heartbeat)}</small></p>` : ''}<ol>${(d.events || []).slice(-6).map((e) => `<li>${H(e.message)}</li>`).join('')}</ol><small>Request ${H(d.request_id)}${d.elapsed_seconds != null ? ' · ' + H(d.elapsed_seconds) + 's elapsed' : ''}</small></div>`;
    },
    docs(d, label) {
      let docs = d.documents || d.sources || [...(d.contradicting || []), ...(d.supporting || [])];
      const c = (d.tally && d.tally.counts) || null;
      const t = c ? `<p class="prism-mono">read ${d.tally.read ?? ''} · supports ${c.supports} · qualifies ${c.qualifies} · contradicts ${c.contradicts} · unrelated ${c.unrelated}</p>` : '';
      const onClaim = c ? (c.supports + c.qualifies + c.contradicts) : docs.length;
      let banner = '';
      if (c && onClaim === 0) {
        banner = `<div class="prism-card warn"><h3>Nothing speaks to this claim as phrased</h3><p>${docs.length} papers were retrieved and read, and none of them addresses it — that is the honest answer, not a failure. Compound or informal claims retrieve poorly. Try one concrete, checkable sentence: <em>“Columnar databases can scan a billion rows per second on NVMe storage.”</em></p></div>`;
        const inner = docs.map((x) => `<div class="prism-doc"><span class="prism-badge unrelated">unrelated</span><div>${x.url ? `<a href="${H(x.url)}" target="_blank" rel="noopener">${H(x.title)}</a>` : H(x.title)}<br><small>${H(x.venue || '')}, ${H(x.year || '')}</small></div><div></div></div>`).join('');
        return banner + `<div class="prism-card"><details><summary>What was retrieved and set aside (${docs.length})</summary>${inner}</details></div>`;
      }
      docs = docs.filter((x) => x.stance !== 'unrelated').concat(docs.filter((x) => x.stance === 'unrelated'));
      const rows = docs.map((x, i) => {
        const cite = `${H(x.venue || x.source || 'study')}, ${H(x.year || '')}`;
        const link = x.url ? `<a href="${H(x.url)}" target="_blank" rel="noopener">${H(x.title)}</a>` : H(x.title);
        const quote = x.quote && x.grounded !== false ? `<q>${H(x.quote)}</q>` : '';
        const ins = x.quote && x.grounded === true ? `<button type="button" class="button button-small" data-insert="${H(`<p>${H(x.quote)} (<a href="${H(x.url || '')}" rel="noopener">${cite}</a>)</p>`)}">Insert quote</button>` : '';
        return `<div class="prism-doc"><span class="prism-badge ${H(x.stance || x.tier || '')}">${H(x.stance || x.tier || '')}</span><div>${link}<br><small>${cite} · ${H(x.tier || '')}${x.cited_by ? ' · cited ' + H(x.cited_by) : ''}</small>${quote}</div><div>${ins}</div></div>`;
      }).join('');
      return `<div class="prism-card"><h3>${H(label)}</h3>${t}${rows || '<p>Nothing on this claim in the corpus.</p>'}</div>`;
    },
    stats(d) {
      const items = d.stats || d.statistics || d.figures || d.items || [];
      const rows = items.map((x) => {
        const src = typeof x.source === 'object' && x.source ? x.source : x;
        const sentence = x.sentence || x.what || x.context || '';
        const attribution = `${src.venue || src.title || 'source'}${src.year ? ', ' + src.year : ''}`;
        const html = `<p>${H(sentence)} (${src.url ? `<a href="${H(src.url)}" rel="noopener">${H(attribution)}</a>` : H(attribution)})</p>`;
        return `<tr><td><strong>${H(x.value ?? x.figure ?? '')}</strong></td><td>${H(sentence)}</td><td><small>${H(attribution)}</small></td><td><button type="button" class="button button-small" data-insert="${H(html)}">Insert</button></td></tr>`;
      }).join('');
      return `<div class="prism-card"><h3>Numbers with their sentence</h3>${rows ? `<table class="prism-table"><tbody>${rows}</tbody></table>` : '<p>No verified figures for this claim.</p>'}</div>`;
    },
    sections(d, topic) {
      const rows = (d.sections || []).map((s) => `<tr><td><strong>${H(s.title)}</strong><br><small>${H(s.brief || '')}</small></td><td>${H(s.strength || '')} ${s.strength_score != null ? '(' + H(s.strength_score) + ')' : ''}<br><small>${s.evidence_items != null ? H(s.evidence_items) + ' items' : ''}</small></td><td>${s.available === false ? '<small>not enough evidence</small>' : `<button type="button" class="button button-small" data-section="${H(s.key)}" data-topic="${H(topic)}" data-title="${H(s.title)}">Write &amp; insert</button>`}</td></tr>`).join('');
      const strength = typeof d.overall_strength === 'object' ? (d.overall_strength.label || d.overall_strength.score) : d.overall_strength;
      return `<div class="prism-card"><h3>Sections this topic can support</h3><p class="prism-mono">overall strength ${H(strength ?? '')} · contested ${d.contested_pct == null ? 'unknown' : H(d.contested_pct) + '%'}</p><table class="prism-table"><tbody>${rows}</tbody></table></div>`;
    },
    cont(d) {
      const option = (a) => {
        const t = typeof a === 'string' ? a : ((a || {}).text || (a || {}).paragraph || '');
        if (!t) return '';
        const grounded = a && typeof a === 'object' && a.grounded === true;
        return `<p>${H(t)}</p>${grounded ? `<button type="button" class="button button-small" data-insert="${H('<p>' + H(t) + '</p>')}">Insert</button>` : '<p class="prism-card warn">Grounding has not passed. Review the source before inserting.</p>'}`;
      };
      const main = option(d.next_paragraph) || '<p><em>No grounded continuation could be written.</em></p>';
      const alts = (d.alternatives || []).map((a) => `<div class="prism-doc"><span class="prism-badge">${H(a.label || 'alt')}</span><div>${option(a)}</div></div>`).join('');
      return `<div class="prism-card"><h3>Next paragraph</h3>${main}${alts}${d.writer_note ? `<p><small>${H(d.writer_note)}</small></p>` : ''}</div>`;
    },
    citations(d) {
      const entries = d.entries || [];
      const html = '<ol>' + entries.map((e) => `<li>${H(e.citation)}${e.url ? ` <a href="${H(e.url)}" rel="noopener">Source</a>` : ''}</li>`).join('') + '</ol>';
      return `<div class="prism-card"><h3>References (${H(d.style || 'APA')})</h3>${html}${entries.length ? `<button type="button" class="button" data-insert="${H(html)}">Insert references</button>` : '<p>No citations matched.</p>'}</div>`;
    },
    audit(d) {
      const claims = d.claims || (Array.isArray(d.claims_detected) ? d.claims_detected : []);
      const rows = claims.map((c) => `<tr><td>${H(c.claim)}</td><td><span class="prism-badge ${H(c.status || '')}">${H(c.status || c.checkable_by || '')}</span></td><td><small>${H(c.why || c.risk || c.note || c.reason || '')}</small></td></tr>`).join('');
      const by = d.by_status ? Object.entries(d.by_status).map(([k, v]) => `${H(k)} ${H(v)}`).join(' · ') : '';
      return `<div class="prism-card ${(d.by_status && (d.by_status.unsupported || d.by_status.contradicted || d.by_status.unchecked)) ? 'warn' : ''}"><h3>Audit of the draft</h3><p class="prism-mono">${by}</p>${rows ? `<table class="prism-table"><thead><tr><th>claim</th><th>status</th><th>note</th></tr></thead><tbody>${rows}</tbody></table>` : '<p>No checkable claims found.</p>'}</div>`;
    },
    trend(d, term) {
      const pts = d.points || [];
      const rows = pts.slice(-8).map((p) => `<tr><td>${H(String(p.period).slice(0, 7))}</td><td>${H(p.articles)}</td><td>${H(p.critical_pct)}%</td></tr>`).join('');
      return `<div class="prism-card"><h3>News mentioning “${H(term)}”</h3><table class="prism-table"><thead><tr><th>period</th><th>articles</th><th>critical</th></tr></thead><tbody>${rows}</tbody></table><button type="button" class="button button-small" data-insert="${H(`[prism_trend term="${term}"]`)}">Insert as shortcode</button></div>`;
    },
    chart(d, topic, card) {
      const url = d.url || (d.images && d.images.light && d.images.light.url);
      if (!url) return `<div class="prism-card warn"><p>No chart: this card holds nothing for “${H(topic)}”.</p></div>`;
      const html = d.embed_html || `<figure class="wp-block-image"><img src="${url}" alt="${H(topic)}"/></figure>`;
      return `<div class="prism-card"><h3>Chart</h3><img src="${H(url)}" style="max-width:100%"><p><button type="button" class="button button-small" data-insert="${H(html)}">Insert image</button> <button type="button" class="button button-small" data-insert="${H(`[prism_chart topic="${topic}" card="${card}"]`)}">Insert as shortcode</button></p></div>`;
    },
    error(r) { return `<div class="prism-card bad"><p><strong>${H((r.error && r.error.kind) || 'no result')}</strong> — ${H((r.error && r.error.reason) || r.reason || 'Prism returned nothing usable')}</p></div>`; },
  };

  /* ── the meta box ── */
  function initBox() {
    const box = document.getElementById('prism-box'); if (!box) return;
    const out = document.getElementById('prism-out'); const claim = document.getElementById('prism-claim');
    let busyTimer = null;
    const busy = (m) => {
      clearInterval(busyTimer);
      const t0 = Date.now();
      out.innerHTML = `<p><span class="prism-spinner"></span>${H(m)} <span class="prism-mono" id="prism-busy-s"></span></p><p class="prism-mono" style="color:#646970">Retrieval and writing time depend on the topic and backend availability. Matching recent results are reused.</p>`;
      busyTimer = setInterval(() => { const el = document.getElementById('prism-busy-s'); if (el) el.textContent = Math.round((Date.now() - t0) / 1000) + 's'; else clearInterval(busyTimer); }, 1000);
    };
    const done = (html) => { clearInterval(busyTimer); out.innerHTML = html; };
    const editorCall = (feature, args) => runRequest(feature, args, (d) => done(R.progress(d)));
    box.addEventListener('click', async (ev) => {
      const b = ev.target.closest('button'); if (!b) return;
      if (b.dataset.insert) { Editor.insertHTML(b.dataset.insert); b.textContent = 'Inserted'; b.disabled = true; return; }
      if (b.dataset.section) {
        if (box.dataset.busy === 'true') return;
        box.dataset.busy = 'true';
        b.disabled = true; b.textContent = 'Writing…';
        busy('Getting your sources ready…');
        const r = await editorCall('compose.section', { topic: b.dataset.topic, section: b.dataset.section, background: false }).catch((e) => ({ ok: false, error: { reason: e.message } }));
        box.dataset.busy = 'false';
        done('');
        const d = r.data || {};
        const paras = (d.paragraphs && d.paragraphs.length ? d.paragraphs : String(d.body || '').split(/\n\n+/)).filter((p) => p.trim());
        const html = paras.map((p) => `<p>${H(p)}</p>`).join('');
        if (r.ok && html && d.grounded === true) {
          Editor.insertHTML(`<h2>${H(d.heading || b.dataset.title)}</h2>` + html);
          b.textContent = 'Inserted';
          out.insertAdjacentHTML('afterbegin', '<p>The section has been inserted.</p>');
          if (d.bibliography && d.bibliography.entries) out.insertAdjacentHTML('afterbegin', R.citations(d.bibliography));
        } else {
          b.textContent = 'Failed — retry';
          b.disabled = false;
          out.insertAdjacentHTML('afterbegin', R.error(r.ok ? { error: { kind: d.grounded !== true ? 'grounding failed' : 'empty section', reason: d.note || d.reason || 'The section did not pass its insertion checks.' } } : r));
        }
        return;
      }
      const f = b.dataset.prism; if (!f) return;
      if (f === 'selection') { claim.value = Editor.selection() || claim.value; return; }
      const text = claim.value.trim() || Editor.title();
      if (box.dataset.busy === 'true') return;
      box.dataset.busy = 'true';
      b.disabled = true;
      try {
        if (f === 'research.audit') { busy('Auditing every claim in the draft…'); const r = await editorCall(f, { text: Editor.draftText() }); done(r.ok ? R.audit(r.data) : R.error(r)); return; }
        if (!text) { out.innerHTML = '<div class="prism-card warn"><p>Type a claim or select text first.</p></div>'; return; }
        if (f === 'research.evidence') { busy('Reading the research…'); const r = await editorCall(f, { claim: text, limit: 10 }); done(r.ok ? R.docs(r.data, 'Evidence') : R.error(r)); }
        else if (f === 'research.counter_evidence') { busy('Looking for what disagrees…'); const r = await editorCall(f, { claim: text }); done(r.ok ? R.docs(r.data, 'What disagrees, or qualifies') : R.error(r)); }
        else if (f === 'research.statistics') { busy('Finding figures with their sentences…'); const r = await editorCall(f, { claim: text, include_context: false, include_trend: false }); done(r.ok ? R.stats(r.data) : R.error(r)); }
        else if (f === 'research.citations') { busy('Finding source references…'); const r = await editorCall(f, { claim: text, style: 'apa', limit: 8 }); done(r.ok ? R.citations(r.data) : R.error(r)); }
        else if (f === 'compose.sections') { busy('Ranking sections by evidence…'); const r = await editorCall(f, { topic: text }); done(r.ok ? R.sections(r.data, text) : R.error(r)); }
        else if (f === 'compose.continue') { busy('Writing the next paragraph from the evidence…'); const r = await editorCall(f, { draft: Editor.lastParagraph() || text, topic: text }); done(r.ok ? R.cont(r.data) : R.error(r)); }
        else if (f === 'news.trends') { busy('Measuring the news…'); const r = await editorCall(f, { term: text, granularity: 'quarterly', since: '2024-01-01' }); done(r.ok ? R.trend(r.data, text) : R.error(r)); }
        else if (f === 'compose.chart') { const card = document.getElementById('prism-chart-card').value; busy('Drawing…'); const r = await call(f, { topic: text, card }, 300); done(r.ok ? R.chart(r.data, text, card) : R.error(r)); }
      } catch (e) { done(R.error({ error: { kind: 'request failed', reason: e.message } })); }
      finally { box.dataset.busy = 'false'; b.disabled = false; }
    });
  }
  function mdLite(md) { return md.split(/\n{2,}/).map((p) => p.startsWith('#') ? `<h3>${H(p.replace(/^#+\s*/, ''))}</h3>` : `<p>${H(p)}</p>`).join('\n'); }

  /* ── New article page: background job + progress + import ── */
  function initNewArticle() {
    const btn = document.getElementById('prism-start'); if (!btn) return;
    const prog = document.getElementById('prism-progress'), fill = document.getElementById('prism-bar-fill'), label = document.getElementById('prism-progress-label'), res = document.getElementById('prism-result');
    btn.addEventListener('click', async () => {
      const subject = document.getElementById('prism-subject').value.trim(); const k = parseInt(document.getElementById('prism-k').value || '12', 10);
      if (!subject) return;
      btn.disabled = true; prog.hidden = false; res.hidden = true; res.innerHTML = ''; fill.style.width = '2%'; label.textContent = 'starting…';
      const start = await call('compose.quick_story', { subject, k, background: true }, 60).catch((e) => ({ ok: false, error: { reason: e.message } }));
      const jobId = start.job_id || (start.data && start.data.job_id);
      if (!jobId) { res.hidden = false; res.innerHTML = R.error(start); btn.disabled = false; return; }
      const t0 = Date.now(); let stage = 0, failures = 0;
      const stages = ['resolving the subject', 'shortlisting papers', 'reading abstracts', 'finding the news', 'drawing charts', 'planning the story', 'drawing illustrations', 'writing', 'cold reader round 1', 'revising', 'cold reader round 2', 'finishing'];
      const tick = async () => {
        const j = await call('system.job', { job_id: jobId }, 30).catch(() => null);
        const secs = Math.round((Date.now() - t0) / 1000);
        if (!j || j.ok === false) {
          failures += 1;
          if (failures >= 3 || (j && j.error && j.error.kind === 'no_data')) {
            res.hidden = false; res.innerHTML = R.error(j || { error: { reason: `Cannot read job ${jobId}. Check the Jobs page before retrying.` } }); btn.disabled = false; return;
          }
        } else { failures = 0; }
        if (secs > 1800) { res.hidden = false; res.innerHTML = R.error({ error: { reason: `Job ${jobId} is still running. Check the Jobs page.` } }); btn.disabled = false; return; }
        const st = j && (j.status || (j.data && j.data.status));
        const pr = (j && j.progress) || (j && j.data && j.data.progress) || {};
        const pct = pr.pct != null ? pr.pct : Math.min(95, Math.round(100 * secs / 420));
        fill.style.width = pct + '%';
        stage = Math.min(stages.length - 1, Math.floor(secs / 35));
        label.textContent = `${st || 'running'} · ${pr.label || stages[stage]} · ${secs}s`;
        if (st === 'done') { const result = j.result || (j.data && j.data.result) || {}; return finish(result, subject); }
        if (st === 'failed' || st === 'error') { res.hidden = false; res.innerHTML = R.error({ error: { kind: 'job failed', reason: (j.data && j.data.error) || (j.error && j.error.reason) || 'see Prism logs' } }); btn.disabled = false; return; }
        setTimeout(tick, 5000);
      };
      setTimeout(tick, 4000);
    });
    async function finish(result, subject) {
      fill.style.width = '100%'; label.textContent = 'done — creating the draft…';
      const data = result.data || result;
      if (!data || data.available === false) { res.hidden = false; res.innerHTML = R.error({ error: { kind: 'not available', reason: (data && data.reason) || 'Prism could not build this piece' } }); btn.disabled = false; return; }
      const imp = await wp.apiFetch({ path: 'prism/v1/import', method: 'POST', data: { title: data.title, html: data.html, markdown: data.markdown, subject, images: data.images || [], checks: data.checks || {}, reader_rounds: data.reader_rounds || [], papers: data.papers || [], publishable: !!data.publishable } }).catch((e) => ({ ok: false, error: { reason: e.message } }));
      res.hidden = false;
      const rr = (data.reader_rounds || []).map((r) => `<tr><td>${r.round}</td><td>${r.understood ?? '—'}/10</td><td>${r.kept_reading ? 'yes' : 'no'}</td><td>${r.pass ? 'passed' : H(r.why || '')}</td><td>${r.delivered ? '✓' : ''}</td></tr>`).join('');
      const c = data.checks || {};
      const cut = (c.excised_unsupported || []).map((s) => `<li>${H(s)}</li>`).join('');
      res.innerHTML = `
        <div class="prism-card ${data.publishable ? 'good' : 'warn'}"><h3>${H(data.title || subject)}</h3>
          <p>${H(data.words)} words · ${(data.papers || []).filter((p) => p.used).length} of ${(data.papers || []).length} papers cited · ${(data.news || []).length} news records · ${(data.charts || []).length} charts · ${(data.images || []).length} illustrations · ${H(data.seconds)}s · written by ${H(data.written_by)} · read by ${H(data.read_by)}</p>
          ${imp.ok ? `<p><a class="button button-primary" href="${H(imp.edit_url)}">Open the draft in the editor</a> <a class="button" href="${H(imp.view_url)}" target="_blank">Preview</a> <span class="prism-mono">saved as ${H(imp.status)}</span></p>` : R.error(imp)}
        </div>
        <div class="prism-card"><h3>Cold reader rounds</h3><table class="prism-table"><thead><tr><th>read</th><th>understood</th><th>kept reading</th><th>verdict</th><th>delivered</th></tr></thead><tbody>${rr}</tbody></table></div>
        <div class="prism-card ${cut ? 'warn' : ''}"><h3>Checks</h3><p class="prism-mono">ungrounded figures: ${(c.ungrounded_numbers || []).length} · unsourced names: ${(c.unsourced_names || []).length} · links repaired: ${(c.links_repaired || []).length} · direction errors: ${(c.direction || []).length} · machine voice: ${(c.machine_voice || []).length}</p>${cut ? `<p>Sentences cut because no source supports them:</p><ul>${cut}</ul>` : ''}${data.coverage && data.coverage.note ? `<p><small>${H(data.coverage.note)}</small></p>` : ''}</div>`;
      btn.disabled = false;
    }
  }

  /* ── Jobs + Settings status ── */
  async function initJobs() {
    const el = document.getElementById('prism-jobs'); if (!el) return;
    const r = await call('system.jobs', { limit: 25 }, 30).catch((e) => ({ ok: false, error: { reason: e.message } }));
    const jobs = (r.data && (r.data.jobs || r.data)) || r.jobs || [];
    if (!Array.isArray(jobs) || !jobs.length) { el.innerHTML = r.ok === false ? R.error(r) : '<p>No jobs yet.</p>'; return; }
    el.innerHTML = `<table class="widefat striped prism-jobs"><thead><tr><th>job</th><th>kind</th><th>status</th><th>progress</th><th>age</th></tr></thead><tbody>${jobs.map((j) => `<tr><td class="prism-mono">${H(j.job_id || j.id)}</td><td>${H(j.kind)}</td><td>${H(j.status)}</td><td>${typeof j.progress === 'string' ? H(j.progress) : j.progress ? H(j.progress.done) + '/' + H(j.progress.total) : ''} ${H(j.label || '')}</td><td>${j.age_seconds == null ? H(j.updated || '') : H(j.age_seconds) + 's'}</td></tr>`).join('')}</tbody></table>`;
  }
  async function initStatus() {
    const el = document.getElementById('prism-status'); if (!el) return;
    const r = await call('system.status', {}, 30).catch((e) => ({ ok: false, error: { reason: e.message } }));
    if (!r.ok) { el.innerHTML = `<p class="prism-status-bad">Cannot reach Prism — ${H((r.error && r.error.reason) || '')}</p>`; return; }
    const d = r.data || {};
    el.innerHTML = `<p class="${d.partial ? 'prism-status-bad' : 'prism-status-ok'}">${d.partial ? 'Connected; data storage is degraded.' : 'Connected.'}</p><pre class="prism-mono">${H(JSON.stringify(d, null, 1).slice(0, 3000))}</pre>`;
  }

  /* WordPress 6.7+ keeps the block editor's meta-box pane collapsed; a research
     box nobody can see is no research box. Open it once, the first time. */
  function openMetaBoxPane() {
    if (!(window.wp && wp.data && document.getElementById('prism-box'))) return;
    try {
      const prefs = wp.data.select('core/preferences');
      if (prefs && prefs.get('core/edit-post', 'prismPaneOpened')) return;
      wp.data.dispatch('core/preferences').set('core/edit-post', 'metaBoxesMainIsOpen', true);
      wp.data.dispatch('core/preferences').set('core/edit-post', 'metaBoxesMainOpenHeight', 520);
      wp.data.dispatch('core/preferences').set('core/edit-post', 'prismPaneOpened', true);
    } catch (e) { /* classic editor: nothing to open */ }
  }
  document.addEventListener('DOMContentLoaded', () => { initBox(); initNewArticle(); initJobs(); initStatus(); setTimeout(openMetaBoxPane, 1200); });
})();
