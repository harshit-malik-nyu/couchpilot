import sqlite3
from pathlib import Path
root=Path(__file__).resolve().parents[1]
db=sqlite3.connect(':memory:');db.execute('CREATE TABLE events(event_id TEXT PRIMARY KEY,session_id TEXT,request_id INTEGER,event TEXT)')
for i,seq in enumerate([['request_started','proposal_ready','actions_applied'],['request_started','proposal_ready','actions_applied','seek_undone'],['request_started','request_cancelled'],['request_started','unsupported']]):
 for j,e in enumerate(seq):db.execute('INSERT INTO events VALUES(?,?,?,?)',(f'{i}-{j}','synthetic',i,e))
r=db.execute((root/'analytics/funnel.sql').read_text()).fetchone();assert r==(4,2,2,1,1),r;print('Synthetic SQL funnel reconciles:',r)
