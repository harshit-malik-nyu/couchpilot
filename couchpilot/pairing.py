"""Short-lived single-use handoff for the local server. No account or tracking."""
import secrets
import threading
import time
from .core import SEGMENTS

class Pairings:
    def __init__(self,clock=time.monotonic):self.clock=clock;self.items={};self.lock=threading.Lock()
    def create(self,segment_id):
        if segment_id not in SEGMENTS:raise ValueError('Unknown segment')
        with self.lock:
            self.items={k:v for k,v in self.items.items() if v['expires']>self.clock()}
            if len(self.items)>=100:raise ValueError('Handoff capacity reached')
            code=secrets.token_urlsafe(24);owner=secrets.token_urlsafe(24)
            self.items[code]={'owner':owner,'segment_id':segment_id,'expires':self.clock()+120}
            return {'code':code,'owner':owner,'ttl_seconds':120}
    def consume(self,code):
        with self.lock:
            item=self.items.pop(code,None)
            if not item or item['expires']<=self.clock():raise ValueError('Handoff expired or already used')
            return dict(SEGMENTS[item['segment_id']])
    def revoke(self,code,owner):
        with self.lock:
            item=self.items.get(code)
            if not item or not secrets.compare_digest(item['owner'],owner):raise ValueError('Unknown handoff')
            del self.items[code]
