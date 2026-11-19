"""Loopback-only local prototype API and static host; not a production web server."""
import argparse
import json
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlsplit
from .core import ROOT,LocalModel,run
from .pairing import Pairings
import threading

def make_server(port=8787,model='qwen2.5:3b'):
    pairings=Pairings();inference=threading.BoundedSemaphore(1)
    class Handler(SimpleHTTPRequestHandler):
        def __init__(self,*args,**kw):super().__init__(*args,directory=str(ROOT/'web'),**kw)
        def log_message(self,*args):pass # Do not log prompts, tokens or paths.
        def valid_origin(self):
            allowed={f'localhost:{self.server.server_port}',f'127.0.0.1:{self.server.server_port}'}
            return self.headers.get('Host') in allowed and (not self.headers.get('Origin') or urlsplit(self.headers['Origin']).netloc in allowed)
        def respond(self,status,obj):
            body=json.dumps(obj).encode();self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Cache-Control','no-store');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
        def do_GET(self):
            if not self.valid_origin():return self.respond(403,{'error':'Origin rejected'})
            if self.path=='/api/health':return self.respond(200,{'local':True,'model':model})
            if self.path.startswith('/api/'):return self.respond(404,{'error':'Not found'})
            super().do_GET()
        def do_POST(self):
            if not self.valid_origin():return self.respond(403,{'error':'Origin rejected'})
            try:
                n=int(self.headers.get('Content-Length','0'))
                if not 0<n<=4096 or self.headers.get('Content-Type','').split(';')[0]!='application/json':raise ValueError('JSON body required, maximum 4 KB')
                data=json.loads(self.rfile.read(n))
                if type(data) is not dict:raise ValueError('Object required')
                if self.path=='/api/agent':
                    if not inference.acquire(blocking=False):return self.respond(429,{'error':'Model busy; try again'})
                    try:result=run(data.get('query'),LocalModel(model),data.get('current','intro'))
                    finally:inference.release()
                elif self.path=='/api/handoff':result=pairings.create(data['segment_id'])
                elif self.path=='/api/consume':result=pairings.consume(data['code'])
                elif self.path=='/api/revoke':pairings.revoke(data['code'],data['owner']);result={'revoked':True}
                else:return self.respond(404,{'error':'Not found'})
                self.respond(200,result)
            except (ValueError,KeyError,TypeError) as e:self.respond(400,{'error':str(e)[:160]})
    return ThreadingHTTPServer(('127.0.0.1',port),Handler)

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8787);parser.add_argument('--model',default='qwen2.5:3b');a=parser.parse_args()
    print(f'CouchPilot http://127.0.0.1:{a.port} · local only',flush=True)
    make_server(a.port,a.model).serve_forever()
