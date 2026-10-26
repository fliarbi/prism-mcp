#!/usr/bin/env python3
"""Render the manually authored case notes beside reproducible measurements."""
import json
from pathlib import Path
p=Path('out/usecases-50-20260912')
s=json.loads((p/'summary.json').read_text());notes=json.loads((p/'case-notes.json').read_text());dataset=json.loads((p/'dataset.json').read_text())
assert set(notes)=={str(i) for i in range(1,51)}
cs={c['id']:c for c in s['cases']}
models={v:{r['id']:r for r in s['models']['baseline'][v]['runs']} for v in ['openai','anthropic']}
out=['# Fifty-case manual assessment','',
 'These are exploratory workflow assessments, not a certified accuracy score or independent human panel. Every Prism first response was inspected; comparison answers were reviewed at task-fit level, with detailed paired review of the ten augmented cases. Only selected external claims received primary-source verification. “Useful” does not certify every classification, citation, or source sentence. First/repeat timings are Prism handler seconds; model timings include CLI setup.','']
for case in dataset['cases']:
    i=case['id'];c=cs[i];verdict,prism,comparison=notes[str(i)]
    out += [f"## {i:02}. {case['name']} — {verdict}",'',f"Endpoint: `{case['feature']}`. Question: {case['question']}",'',f"Prism first/repeat: {c['first_seconds']:.2f}s / {c['repeat_seconds']:.4f}s. GPT CLI: {models['openai'][i]['seconds']:.2f}s. Claude CLI: {models['anthropic'][i]['seconds']:.2f}s.",'',f'Prism: {prism}','',f'Comparison: {comparison}','',f"Evidence: [Prism](prism/{i:02}.json), [GPT](baseline/{i:02}-openai.json), [Claude](baseline/{i:02}-anthropic.json).",'']
(p/'CASES.md').write_text('\n'.join(out))
print('Wrote 50 case assessments')
