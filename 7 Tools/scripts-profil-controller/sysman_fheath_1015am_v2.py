# -*- coding: utf-8 -*-
"""Sysman cron 15-10 ronde2: (a) done-24j tanpa ACK per tenant, (b) kartu blocked non-VIBE
(judul+reason+umur event terakhir), (c) HQ needs-review."""
import sqlite3, os, time, pathlib, subprocess, json

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
con = sqlite3.connect(f'file:{HOME/"kanban.db"}?mode=ro', uri=True)
cur = con.cursor()
now = int(time.time()); DAY = now - 86400

print('[A] done 24j tanpa RANTAI-ACK per tenant:')
cur.execute("""
SELECT COALESCE(t.tenant,'(null)'), COUNT(*)
FROM tasks t WHERE t.status='done' AND t.completed_at>=?
AND NOT EXISTS (SELECT 1 FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-ACK%')
GROUP BY 1 ORDER BY 2 DESC""", (DAY,))
for r in cur.fetchall():
    print('  ', r)

print('\n[B] kartu blocked non-VIBE (id, tenant, assignee, judul, reason, umur-ev-mnt):')
cur.execute("""
SELECT t.id, COALESCE(t.tenant,'(null)'), t.assignee, substr(t.title,1,55),
       substr(COALESCE((SELECT body FROM task_events e2 WHERE e2.task_id=t.id AND e2.kind='blocked'
                        ORDER BY e2.created_at DESC LIMIT 1), t.status, ''),1,90)
FROM tasks t WHERE t.status='blocked' AND COALESCE(t.tenant,'') != 'VIBE-BIBLE-1013'""")
for tid, tn, ag, ti, rs in cur.fetchall():
    cur2 = con.cursor()
    cur2.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (tid,))
    mx = cur2.fetchone()[0]
    age = int((now - mx) / 60) if mx else -1
    print(f'   {tid} | {tn} | {ag} | {ti} | ev {age}mnt | {rs!r}')
con.close()

# [C] HQ needs-review via node pg
DC = r'C:/Users/TRIAL/gsp-datacenter'
js = pathlib.Path(DC) / 'tmp_sysman_nr_1015.cjs'
js.write_text("""const{Client}=require('pg');
const u=require('fs').readFileSync('.env','utf8').match(/DATABASE_URL="([^"]+)"/)[1];
const c=new Client({connectionString:u});
c.connect().then(()=>c.query("SELECT id,left(\\\\"prompt\\\\",70) p,status,\\"createdAt\\",\\\\"updatedAt\\" FROM \\\\"AgentRequest\\\\" WHERE status='needs-review' ORDER BY \\"updatedAt\\" DESC"))
 .then(r=>{console.log(JSON.stringify(r.rows));return c.end()})
 .catch(e=>{console.log('ERR '+e.message);return c.end()});
""", encoding='utf-8')
r = subprocess.run(['node', str(js)], cwd=DC, capture_output=True, text=True, timeout=45)
print('\n[C] HQ needs-review:')
out = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else '(kosong)'
try:
    for row in json.loads(out):
        print('  ', {k: (str(v)[:70]) for k, v in row.items()})
except Exception:
    print('   raw:', out[:300], '| stderr:', r.stderr[:200])
