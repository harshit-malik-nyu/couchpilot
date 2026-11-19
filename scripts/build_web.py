"""Package recorded evidence and the original content; no model result is invented."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
r={'suites':[]}
for sid,title,cases,baseline,model in [
 ('v5','Latest workflow · 54 authored tasks','robustness-cases.json','baseline-v3.json','model-v5.json'),
 ('v4','Constrained decoder · 54 tasks','robustness-cases.json','baseline-v3.json','model-v4.json'),
 ('v3','Prompt + critic only · 54 tasks','robustness-cases.json','baseline-v3.json','model-v3.json'),
 ('v2','Previous model · 12 development tasks','cases.json','baseline.json','model-run.json'),
 ('v1','Initial model · 12 development tasks','cases.json','baseline.json','model-v1.json')]:
 suite={'id':sid,'title':title,'cases':json.loads((ROOT/'evaluation'/cases).read_text())}
 for key,path in [('baseline',baseline),('model',model)]:
  p=ROOT/'evaluation'/path;suite[key]=json.loads(p.read_text()) if p.exists() else None
 r['suites'].append(suite)
(ROOT/'web/evidence.js').write_text('window.EVIDENCE='+json.dumps(r,separators=(',',':')).replace('<','\\u003c')+';\n')
(ROOT/'web/lesson.js').write_text('window.LESSON='+json.dumps(json.loads((ROOT/'data/lesson.json').read_text()))+';\n')
print('Evidence packaged:',[(s['id'],bool(s['model'] and s['model'].get('summary'))) for s in r['suites']])
