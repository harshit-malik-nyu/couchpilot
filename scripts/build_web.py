"""Package recorded evidence and the original content; no model result is invented."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
r={'cases':json.loads((ROOT/'evaluation/cases.json').read_text())}
for key,path in [('baseline','baseline.json'),('model','model-run.json')]:
 p=ROOT/'evaluation'/path
 r[key]=json.loads(p.read_text()) if p.exists() else None
(ROOT/'web/evidence.js').write_text('window.EVIDENCE='+json.dumps(r,separators=(',',':')).replace('<','\\u003c')+';\n')
(ROOT/'web/lesson.js').write_text('window.LESSON='+json.dumps(json.loads((ROOT/'data/lesson.json').read_text()))+';\n')
print('Evidence packaged; model measured:',bool(r['model'] and r['model'].get('summary')))
