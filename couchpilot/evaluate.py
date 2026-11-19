"""Authored acceptance benchmark. Never claims independent held-out validation."""
import argparse
import hashlib
import json
import math
import platform
import statistics
import time
import urllib.request
from .core import ROOT,LocalModel,run,rules,SEGMENTS,selection_to_plan

def grade(case,result):
    actions=result.get('actions',[])
    fidelity=all(a.get('segment_id') in SEGMENTS and all(a.get(k)==SEGMENTS[a['segment_id']][k] for k in ('start','end','title','text')) for a in actions)
    correct=result['status']==case['status'] and sorted(a['tool'] for a in actions)==sorted(case['tools']) and all(a['segment_id']==case['segment'] for a in actions) and fidelity
    return {'correct':correct,'source_fidelity':fidelity,'wrong_seek':any(a['tool']=='seek' and (case['segment']!=a['segment_id'] or 'seek' not in case['tools']) for a in actions)}

def evaluate(model_name=None,output='evaluation/baseline-v3.json',cases_path='evaluation/robustness-cases.json'):
    cases=json.loads((ROOT/cases_path).read_text());results=[]
    if len({c['id'] for c in cases})!=len(cases):raise ValueError('Duplicate case IDs')
    report={'scope':f'{len(cases)} authored development acceptance cases, one run each. Visible during development, NOT independent held-out data. Text only; no viewer, ASR, device or generalization claim.',
            'cases_path':cases_path,'recorded_at_utc':time.strftime('%Y-%m-%dT%H:%M:%SZ',time.gmtime()),
            'mode':'local-model' if model_name else 'rules-baseline','model':model_name,'python':platform.python_version(),'platform':platform.platform(),
            'hashes':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['couchpilot/core.py','couchpilot/policy.py','couchpilot/evaluate.py',cases_path,'data/lesson.json']},'results':results}
    if model_name:
        op=urllib.request.build_opener(urllib.request.ProxyHandler({}))
        for name in ('tags','version'):
            with op.open('http://127.0.0.1:11434/api/'+name,timeout=10) as r:report['ollama_'+name]=json.load(r)
    path=ROOT/output;path.parent.mkdir(parents=True,exist_ok=True)
    for case in cases:
        start=time.perf_counter();result=run(case['query'],LocalModel(model_name),case['current']) if model_name else rules(case['query'],case['current'])
        row={'id':case['id'],'query':case['query'],'current':case['current'],'category':case.get('category','original-development'),'result':result,'seconds':round(time.perf_counter()-start,4),**grade(case,result)}
        results.append(row);path.write_text(json.dumps(report,indent=2)+'\n');print(case['id'],row['correct'],row['seconds'],flush=True)
    times=sorted(r['seconds'] for r in results)
    report['summary']={'correct':sum(r['correct'] for r in results),'total':len(results),'wrong_seek':sum(r['wrong_seek'] for r in results),
                       'median_seconds':statistics.median(times),'p95_seconds':times[math.ceil(.95*len(times))-1],
                       'errors':sum(r['result']['status']=='error' for r in results),
                       'source_fidelity_failures':sum(not r['source_fidelity'] for r in results),
                       'model_calls':sum(r['result'].get('model_calls',0) for r in results),
                       'tasks_with_model_calls':sum(r['result'].get('model_calls',0)>0 for r in results),
                       'policy_only_tasks':sum(r['result'].get('model_calls',0)==0 for r in results) if model_name else None,
                       'repair_tasks':sum(any(t['tool']=='repair_actions' for t in r['result'].get('trace',[])) for r in results),
                       'categories':{c:{'correct':sum(r['correct'] for r in results if r['category']==c),'total':sum(r['category']==c for r in results)} for c in sorted({r['category'] for r in results})}}
    path.write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--model');p.add_argument('--cases',default='evaluation/robustness-cases.json');p.add_argument('--output',default='evaluation/baseline-v3.json');a=p.parse_args();print(json.dumps(evaluate(a.model,a.output,a.cases)['summary']))
