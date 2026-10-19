#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""optwf_gate_inspect2.py — cek bentuk event gerbang + kolom AgentRequest di PG."""
import sqlite3

db = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect('file:' + db.replace('\\', '/') + '?mode=ro', uri=True)
for r in con.execute("SELECT id, task_id, run_id, payload, created_at FROM task_events WHERE kind='review_requested' ORDER BY id DESC LIMIT 2"):
    print('REVIEW SAMPLE:', r)
for r in con.execute("SELECT id, task_id, payload FROM task_events WHERE kind='changes_requested' ORDER BY id DESC LIMIT 1"):
    print('CHANGES_REQ SAMPLE:', r)
con.close()

import urllib.parse, os
envp = r"C:/Users/TRIAL/gsp-datacenter/.env"
url = None
for line in open(envp, encoding='utf-8', errors='ignore'):
    if line.startswith('DATABASE_URL='):
        url = line.split('=', 1)[1].strip().strip('"')
u = urllib.parse.urlparse(url)
from pg8000 import dbapi
pg = dbapi.connect(user=urllib.parse.unquote(u.username),
                   password=urllib.parse.unquote(u.password or ""),
                   host=u.hostname, port=u.port or 5432,
                   database=os.path.basename(u.path))
cur = pg.cursor()
cur.execute("""SELECT column_name, data_type, column_default FROM information_schema.columns
               WHERE table_name='AgentRequest' ORDER BY ordinal_position""")
for r in cur.fetchall():
    print('PG COL:', r)
cur.execute('SELECT COUNT(*) FROM "AgentRequest"')
print('AR count:', cur.fetchone())
cur.execute("SELECT id, title, status, origin, \\\"hermesTaskId\\\" FROM \"AgentRequest\" WHERE status='awaiting_approval' ORDER BY \\\"createdAt\\\" DESC LIMIT 3")
for r in cur.fetchall():
    print('AR AWAITING:', str(r)[:160])
pg.close()
