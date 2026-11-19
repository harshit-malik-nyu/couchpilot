import json
import threading
import unittest
import urllib.error
import urllib.request
from couchpilot.core import retrieve,validate_plan,run,rules,SEGMENTS
from couchpilot.pairing import Pairings
from couchpilot.server import make_server

class SequenceModel:
    def __init__(self,outputs):self.outputs=iter(outputs)
    def call(self,*args):return next(self.outputs)

class CoreTests(unittest.TestCase):
    def test_retrieval_known_topic(self):self.assertEqual(retrieve('support guardrail')[0]['id'],'guardrails')
    def test_retrieval_unknown(self):self.assertEqual(retrieve('sourdough oven temperature'),[])
    def test_unknown_citation_rejected(self):
        with self.assertRaises(ValueError):validate_plan({'status':'ready','actions':[{'tool':'seek','segment_id':'fake'}]},retrieve('support'))
    def test_unretrieved_source_rejected(self):
        with self.assertRaises(ValueError):validate_plan({'status':'ready','actions':[{'tool':'seek','segment_id':'intro'}]},retrieve('support'))
    def test_extra_action_fields_rejected(self):
        with self.assertRaises(ValueError):validate_plan({'status':'ready','actions':[{'tool':'seek','segment_id':'guardrails','url':'https://example.com'}]},retrieve('support'))
    def test_purchase_tool_rejected(self):
        with self.assertRaises(ValueError):validate_plan({'status':'ready','actions':[{'tool':'purchase','segment_id':'guardrails'}]},retrieve('support'))
    def test_empty_ready_rejected(self):
        with self.assertRaises(ValueError):validate_plan({'status':'ready','actions':[]},[])
    def test_duplicate_tool_rejected(self):
        a={'tool':'seek','segment_id':'guardrails'}
        with self.assertRaises(ValueError):validate_plan({'status':'ready','actions':[a,a]},retrieve('support'))
    def test_two_model_steps_and_source_resolution(self):
        model=SequenceModel([{'query':'support'},{'action':'seek','segment_id':'guardrails'}])
        result=run('go to support',model)
        self.assertEqual(result['status'],'ready');self.assertEqual(result['actions'][0]['start'],80)
        self.assertEqual(result['actions'][0]['text'],SEGMENTS['guardrails']['text'])
        self.assertEqual(len(result['trace']),3)
    def test_model_failure_never_becomes_rules(self):
        class Bad:
            def call(self,*args):raise OSError('unavailable')
        result=run('step 2',Bad());self.assertEqual(result['status'],'error');self.assertEqual(result['actions'],[])
    def test_prompt_bound(self):
        with self.assertRaises(ValueError):run('x'*501,None)
    def test_card_is_draft(self):self.assertEqual(rules('send second step to phone')['actions'][0]['tool'],'prepare_card')
    def test_no_jump_on_negation(self):self.assertNotIn('seek',[a['tool'] for a in rules('do not jump explain assignment')['actions']])
    def test_single_use_handoff(self):
        p=Pairings();c=p.create('assignment');self.assertEqual(p.consume(c['code'])['id'],'assignment')
        with self.assertRaises(ValueError):p.consume(c['code'])
    def test_handoff_expiry(self):
        clock=[0];p=Pairings(lambda:clock[0]);c=p.create('intro');clock[0]=120
        with self.assertRaises(ValueError):p.consume(c['code'])
    def test_handoff_owner_revoke(self):
        p=Pairings();c=p.create('intro')
        with self.assertRaises(ValueError):p.revoke(c['code'],'wrong')
        p.revoke(c['code'],c['owner'])
        with self.assertRaises(ValueError):p.consume(c['code'])
    def test_concurrent_consume_only_one_wins(self):
        p=Pairings();c=p.create('intro');result=[]
        def get():
            try:p.consume(c['code']);result.append('yes')
            except ValueError:result.append('no')
        ts=[threading.Thread(target=get) for _ in range(8)]
        for t in ts:t.start()
        for t in ts:t.join()
        self.assertEqual(result.count('yes'),1)

class HTTPTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=make_server(0);cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True);cls.thread.start();cls.url=f'http://127.0.0.1:{cls.server.server_port}'
        cls.op=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    @classmethod
    def tearDownClass(cls):cls.server.shutdown();cls.server.server_close();cls.thread.join()
    def post(self,path,data,headers=None):
        r=urllib.request.Request(self.url+path,data=json.dumps(data).encode(),headers={'Content-Type':'application/json',**(headers or {})})
        with self.op.open(r) as response:return json.load(response)
    def test_real_http_handoff(self):
        c=self.post('/api/handoff',{'segment_id':'assignment'});r=self.post('/api/consume',{'code':c['code']});self.assertEqual(r['start'],40)
    def test_cross_origin_rejected(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:self.post('/api/handoff',{'segment_id':'intro'},{'Origin':'https://evil.example'})
        self.assertEqual(ctx.exception.code,403)
    def test_rebinding_host_rejected(self):
        with self.assertRaises(urllib.error.HTTPError) as ctx:self.post('/api/handoff',{'segment_id':'intro'},{'Host':'evil.example'})
        self.assertEqual(ctx.exception.code,403)
