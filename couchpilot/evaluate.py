"""Authored acceptance benchmark. Never claims independent held-out validation."""
import argparse
import hashlib
import json
import math
import platform
import statistics
import time
import urllib.request
from .core import ROOT,LocalModel,run,rules

def grade(case,result):
    actions=result.get('actions',[])
    correct=result['status']==case['status'] and sorted(a['tool'] for a in actions)==sorted(case['tools']) and all(a['segment_id']==case['segment'] for a in actions)
    return {'correct':correct,'wrong_seek':any(a['tool']=='seek' and (case['segment']!=a['segment_id'] or 'seek' not in case['tools']) for a in actions)}

def evaluate(model_name=None,output='evaluation/baseline.json'):
    cases=json.loads((ROOT/'evaluation/cases.json').read_text());results=[]
    report={'scope':'12 authored development acceptance cases, one run each. Text input only. No real viewer, ASR, device or generalization claim.',
            'mode':'local-model' if model_name else 'rules-baseline','model':model_name,'python':platform.python_version(),'platform':platform.platform(),
            'hashes':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['couchpilot/core.py','evaluation/cases.json','data/lesson.json']},'results':results}
    if model_name:
        op=urllib.request.build_opener(urllib.request.ProxyHandler({}))
        for name in ('tags','version'):
            with op.open('http://127.0.0.1:11434/api/'+name,timeout=10) as r:report['ollama_'+name]=json.load(r)
    path=ROOT/output;path.parent.mkdir(parents=True,exist_ok=True)
    for case in cases:
        start=time.perf_counter();result=run(case['query'],LocalModel(model_name),case['current']) if model_name else rules(case['query'],case['current'])
        row={'id':case['id'],'query':case['query'],'current':case['current'],'result':result,'seconds':round(time.perf_counter()-start,4),**grade(case,result)}
        results.append(row);path.write_text(json.dumps(report,indent=2)+'\n');print(case['id'],row['correct'],row['seconds'],flush=True)
    times=sorted(r['seconds'] for r in results)
    report['summary']={'correct':sum(r['correct'] for r in results),'total':len(results),'wrong_seek':sum(r['wrong_seek'] for r in results),
                       'median_seconds':statistics.median(times),'p95_seconds':times[math.ceil(.95*len(times))-1],
                       'errors':sum(r['result']['status']=='error' for r in results)}
    path.write_text(json.dumps(report,indent=2)+'\n');return report
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--model');p.add_argument('--output',default='evaluation/baseline.json');a=p.parse_args();print(json.dumps(evaluate(a.model,a.output)['summary']))
