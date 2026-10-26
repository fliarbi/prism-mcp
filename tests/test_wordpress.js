// Exercise the actual plugin renderers and async editor flow without WordPress writes.
const assert = require('node:assert/strict');
const fs = require('node:fs');
const vm = require('node:vm');
const src = fs.readFileSync('wordpress/wp-content/plugins/prism-research/assets/admin.js', 'utf8');
let handler, responses = [], inserted = [], requests = [];
const box = { dataset: {}, addEventListener: (_, fn) => { handler = fn; } };
const out = { innerHTML: '', insertAdjacentHTML: (_, html) => { out.innerHTML += html; } };
const elements = { 'prism-box': box, 'prism-out': out, 'prism-claim': { value: 'Test claim' } };
const sandbox = {
  console, Date, Map, Promise,
  setTimeout: (fn) => { fn(); return 1; }, clearTimeout: () => {},
  setInterval: () => 1, clearInterval: () => {},
  document: { addEventListener: () => {}, getElementById: (id) => elements[id] },
  window: {},
  wp: { apiFetch: async (req) => { requests.push(req); return responses.shift(); } },
};
vm.runInNewContext(src.replace(/\}\)\(\);\s*$/, 'globalThis.api = {R, call, runRequest, awaitJob, Editor, initBox};})();'), sandbox);
const { R, call, runRequest, awaitJob, Editor, initBox } = sandbox.api;
async function main() {
  const paragraph = 'The trial measured output.';
  const cont = R.cont({ next_paragraph: { text: paragraph, grounded: true }, alternatives: [{ text: 'Unsupported 90%.', grounded: false }] });
  assert(!cont.includes('[object Object]'));
  assert(cont.includes(paragraph));
  assert.equal((cont.match(/data-insert=/g) || []).length, 1);
  assert(!R.docs({documents:[{title:'Unchecked',quote:'made up',grounded:false}]},'Evidence').includes('data-insert='));
  assert(R.docs({contradicting:[{title:'Contrary study',stance:'contradicts'}], supporting:[]},'Counter').includes('Contrary study'));
  assert(R.stats({stats:[{value:'0',sentence:'No events were observed.',source:{venue:'Test journal',year:2024,url:'https://example.org/study'}}]}).includes('Test journal, 2024'));
  assert(!R.stats({stats:[{value:'0',sentence:'No events.',source:{venue:'Test'}}]}).includes('[object Object]'));
  assert(R.audit({claims_detected:1,claims:[{claim:'Claim shown',status:'unsupported'}]}).includes('Claim shown'));
  assert(R.sections({overall_strength:{score:60,band:'moderate'},sections:[]},'Topic').includes('60'));
  assert(R.citations({style:'apa',entries:[{citation:'Test citation',url:'https://example.org'}]}).includes('Insert references'));
  responses = [{ok:true,data:{}}]; requests = [];
  const [a,b] = await Promise.all([call('research.citations',{claim:'same'}),call('research.citations',{claim:'same'})]);
  assert.equal(requests.length,1); assert.equal(a,b);
  responses = [{ok:true,data:{status:'failed',error:'storage unavailable'}}];
  const failed = await awaitJob({ok:true,data:{job_id:'test'}});
  assert.equal(failed.error.reason,'storage unavailable');
  responses = [{ok:false,error:{kind:'no_data',reason:'expired'}}];
  assert.equal((await awaitJob({ok:true,data:{job_id:'gone'}})).error.reason,'expired');
  responses = Array(3).fill({ok:false,error:{kind:'transport',reason:'offline'}});
  assert.equal((await awaitJob({ok:true,data:{job_id:'offline'}})).error.reason,'offline');
  requests = []; const updates = [];
  const finalResult = {ok:true,data:{entries:[]}};
  responses = [{ok:true,data:{request_id:'req-1',message:'Queued'}},
    {ok:true,data:{status:'running',events:[{sequence:1,message:'Reading articles for you.'}],next_cursor:1}},
    {ok:true,data:{status:'done',events:[{sequence:2,message:'Ready'}],next_cursor:2,result:finalResult}}];
  const [first,second] = await Promise.all([runRequest('research.citations',{claim:'cursor'},d=>updates.push(d)),runRequest('research.citations',{claim:'cursor'})]);
  assert.equal(first,finalResult); assert.equal(second,first); assert.equal(requests.length,3);
  assert.equal(requests[2].data.args.after,1); assert.equal(updates.length,3);
  assert(!R.progress({message:'<script>x</script>',events:[],request_id:'<bad>'}).includes('<script>'));
  responses = [{ok:true,data:{request_id:'lost'}},...Array(3).fill({ok:false,error:{kind:'transport',reason:'offline'}})];
  requests = [];
  assert.equal((await runRequest('research.citations',{claim:'lost'})).ok,false);
  assert.equal(requests.filter(r=>r.data.feature==='system.request').length,1);
  responses = [{ok:true,data:{request_id:'fail'}},{ok:true,data:{status:'failed',result:{ok:false,error:{kind:'no_data',reason:'Nothing suitable'}}}}];
  assert.equal((await runRequest('research.citations',{claim:'fail'})).error.reason,'Nothing suitable');
  Editor.insertHTML = (html) => inserted.push(html);
  initBox();
  const section = {available:true,grounded:true,heading:'A heading',paragraphs:['First paragraph.','Second paragraph.'],bibliography:{style:'apa',entries:[{citation:'The source'}]}};
  responses = [{ok:true,data:{request_id:'section'}},{ok:true,data:{status:'done',result:{ok:true,data:section}}}];
  const button = {dataset:{section:'state_of_evidence',topic:'Topic',title:'Section'},disabled:false};
  await handler({target:{closest:()=>button}});
  assert.equal(inserted.length,1); assert(inserted[0].includes('<p>Second paragraph.</p>'));
  assert(out.innerHTML.includes('The source'));
  assert(requests.some(r=>r.data.feature==='system.request' && r.data.args.feature==='compose.section' && r.data.args.args.background===false));
  responses = [{ok:true,data:{request_id:'bad'}},{ok:true,data:{status:'done',result:{ok:true,data:{...section,grounded:false}}}}];
  await handler({target:{closest:()=>button}});
  assert.equal(inserted.length,1); assert(out.innerHTML.includes('grounding failed'));
  console.log('PASS: WordPress renderers, citations, grounding, request coalescing, job failures and section insertion');
}
main().catch((e)=>{console.error(e);process.exitCode=1;});
