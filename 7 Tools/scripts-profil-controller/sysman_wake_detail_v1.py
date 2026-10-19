# -*- coding: utf-8 -*-
"""Detail read-only: heartbeat kartu running + turunan terbuka + catatan blocked."""
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
    try:
        ts = float(v)
    except (TypeError, ValueError):
        return str(v)
    if ts > 1e12:
        ts /= 1000.0
    return f"{(now - ts)/60:.1f}m"

print("-- running detail --")
for t in con.execute("SELECT id,title,last_heartbeat_at,started_at,max_runtime_seconds,current_run_id,claim_lock FROM tasks WHERE status='running'"):
    print(f"{t['id']} hb={age(t['last_heartbeat_at'])} started={age(t['started_at'])} maxrun={t['max_runtime_seconds']} lock={t['claim_lock']}")

print("-- turunan t_40ba3fee --")
for lk in con.execute("SELECT * FROM task_links WHERE parent_id='t_40ba3fee'"):
    cid = dict(lk)["child_id"]
    r = con.execute("SELECT id,status,title FROM tasks WHERE id=?", (cid,)).fetchone()
    print(f"child {r['id']} [{r['status']}] {r['title'][:60]}")

print("-- blocked (15) --")
for t in con.execute("SELECT id,title,status,result,block_kind,block_recurrences,updated_at FROM tasks WHERE status='blocked' ORDER BY updated_at DESC"):
    body_note = ""
    cc = con.execute("SELECT body FROM task_comments WHERE task_id=? ORDER BY rowid DESC LIMIT 1", (t["id"],)).fetchone()
    if cc:
        body_note = cc["body"][:80].replace("\n", " ")
    print(f"{t['id']} upd={age(t['updated_at'])} kind={t['block_kind']} rec={t['block_recurrences']} | {t['title'][:48]} | last: {body_note}")

print("-- todo (5) --")
for t in con.execute("SELECT id,title,updated_at FROM tasks WHERE status='todo' ORDER BY updated_at DESC"):
    par = con.execute("SELECT p.id, p.status FROM task_links l JOIN tasks p ON p.id=l.parent_id WHERE l.child_id=?", (t["id"],)).fetchall()
    parents = ",".join(f"{p['id']}:{p['status']}" for p in par) or "-"
    print(f"{t['id']} upd={age(t['updated_at'])} parents=[{parents}] {t['title'][:50]}")

print("-- done tanpa ACK dalam 24 jam terakhir (cek rute-4b manual) --")
cutoff = now - 24 * 3600
for t in con.execute("SELECT id,title,completed_at FROM tasks WHERE status='done' AND completed_at>? ORDER BY completed_at DESC LIMIT 12", (cutoff,)):
    nack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (t["id"],)).fetchone()["c"]
    nwake = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (t["id"],)).fetchone()["c"]
    print(f"{t['id']} done_age={age(t['completed_at'])} ACK={nack} WAKE={nwake} | {t['title'][:52]}")
con.close()
