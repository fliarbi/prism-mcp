// Feed saved LIVE response payloads through the actual WordPress renderers.
const fs = require('node:fs');
const vm = require('node:vm');
const path = require('node:path');
const dir = process.argv[2];
if (!dir) throw new Error('Usage: node tests/check_topic_responses.js RESULT_DIRECTORY [OUTPUT_FILE]');
const source = fs.readFileSync('wordpress/wp-content/plugins/prism-research/assets/admin.js', 'utf8');
const sandbox = {document:{addEventListener(){}},window:{},wp:{},Map,Promise};
vm.runInNewContext(source.replace(/\}\)\(\);\s*$/, 'globalThis.renderers = R;})();'), sandbox);
const rows = fs.readFileSync(path.join(dir,'responses.jsonl'),'utf8').trim().split('\n').filter(Boolean).map(JSON.parse);
const render = sandbox.renderers;
const methods = {'research.evidence':'docs','research.counter_evidence':'docs',
                 'research.statistics':'stats','research.citations':'citations',
                 'research.audit':'audit','compose.sections':'sections','compose.continue':'cont'};
const checked=[];
for (const row of rows) {
  const r=row.response;
  if (!r || typeof r.ok !== 'boolean') continue;
  const method=r.ok ? methods[row.feature] : 'error';
  if (!method) continue;
  const item={case_id:row.case_id,feature:row.feature,stage:row.stage,method,issues:[],warnings:[]};
  try {
    const html=method==='error' ? render.error(r) : render[method](r.data,row.args.topic || row.args.claim || 'Test');
    if (html.includes('[object Object]')) item.issues.push('object serialized as visible text');
    if (html.includes('undefined')) item.issues.push('undefined in rendered HTML');
    if (!html || !html.trim()) item.issues.push('empty renderer output');
    // Escaped HTML inside data-insert attributes is intentional. Inspect only
    // text outside real tags/attributes, where escaped markup is visible.
    const visibleText=html.replace(/<[^>]*>/g,'');
    if (/&lt;(?:sub|sup|strong|span|div|a|p|em)\b/i.test(visibleText)) {
      item.warnings.push('Source HTML is escaped into visible markup; normalize text or use a reviewed rich-content renderer');
      item.citation_style=r.data && r.data.style;
    }
    item.html_chars=html.length;
  } catch (e) { item.issues.push(e.message); }
  checked.push(item);
}
const report={responses:rows.length,rendered:checked.length,
              failures:checked.filter(x=>x.issues.length),
              warnings:checked.filter(x=>x.warnings.length),checked};
const output=process.argv[3] || path.join(dir,'wordpress-render-checks.json');
fs.writeFileSync(output,JSON.stringify(report,null,2),{flag:'wx'});
console.log(JSON.stringify({responses:report.responses,rendered:report.rendered,failures:report.failures,warnings:report.warnings},null,2));
process.exitCode=report.failures.length ? 1 : 0;
