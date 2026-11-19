"""Check completeness and provenance. Does not convert test coverage into product quality."""
import hashlib
import json
from pathlib import Path

root=Path(__file__).resolve().parents[1]
cases_path='evaluation/robustness-cases.json'
raw=(root/cases_path).read_bytes();cases=json.loads(raw)
design=json.loads((root/'evaluation/robustness-design.json').read_text())
assert design['cases_sha256']==hashlib.sha256(raw).hexdigest(),'Frozen case design changed'
assert len(cases)==design['count']==54
expected={c['id'] for c in cases}
for path in ('evaluation/baseline-v3.json','evaluation/model-v3.json','evaluation/model-v4.json','evaluation/model-v5.json'):
    report=json.loads((root/path).read_text())
    assert report['hashes'][cases_path]==design['cases_sha256'],path
    rows=report['results'];summary=report['summary']
    assert len(rows)==len(expected) and {r['id'] for r in rows}==expected,path
    assert summary['correct']==sum(r['correct'] for r in rows),path
    assert summary['wrong_seek']==sum(r['wrong_seek'] for r in rows),path
    assert summary['source_fidelity_failures']==sum(not r['source_fidelity'] for r in rows),path
    assert all(r['result'].get('model_calls',0)<=3 for r in rows),path
    print(path,summary['correct'],'/',summary['total'],'exact tasks;',summary['wrong_seek'],'wrong jump proposals')
latest=json.loads((root/'evaluation/model-v5.json').read_text())
for p,digest in latest['hashes'].items():assert hashlib.sha256((root/p).read_bytes()).hexdigest()==digest,p+' differs from measured source'
assert latest['summary']['wrong_seek']==0 and latest['summary']['source_fidelity_failures']==0
print('Report integrity and proposal safety checks pass. No production readiness claim.')
