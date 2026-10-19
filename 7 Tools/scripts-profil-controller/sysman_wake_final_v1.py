# -*- coding: utf-8 -*-
"""Cek akhir read-only: nasib RG19 + heartbeat running saat ini."""
import os
import sqlite3
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"),
                  "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = time.time()

def age(v):
    if v is None:
        return "?"
    ts = float(v)
    if ts > 1e12:
        ts /= 1000.0
    return f"{(now - ts)/60:.1f}m"

t = con.execute("SELECT id,status,completed_at FROM tasks WHERE id='t_40ba3fee'").fetchone()
acks = con.execute("SELECT author,created_at FROM task_comments WHERE task_id='t_40ba3fee' AND body LIKE '%RANTAI-ACK%' ORDER BY rowid").fetchall()
print(f"RG19 t_40ba3fee status={t['status']} done_age={age(t['completed_at'])} ACK={[(a['author'], age(a['created_at'])) for a in acks]}")

for r in con.execute("SELECT id,title,status,last_heartbeat_at,started_at,max_runtime_seconds FROM tasks WHERE status='running'"):
    print(f"running {r['id']} hb={age(r['last_heartbeat_at'])} started={age(r['started_at'])} maxrun={r['max_runtime_seconds']} | {r['title'][:50]}")

# RG20 komentar & LAPOR terakhir
for c in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id='t_6b458b6f' ORDER BY rowid DESC LIMIT 2"):
    print(f"RG20 c[{c['author']}] {age(c['created_at'])}: {c['body'][:120]}".replace("\n", " "))
con.close()
