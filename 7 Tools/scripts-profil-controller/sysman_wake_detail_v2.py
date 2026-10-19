# -*- coding: utf-8 -*-
"""Detail read-only bagian 2: blocked, todo, done-24jam-tanpa-ACK."""
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

def last_activity(tid):
    r = con.execute("SELECT MAX(created_at) m FROM task_comments WHERE task_id=?", (tid,)).fetchone()["m"]
    if r is None:
        r = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    return age(r)

print("-- blocked (15) --")
for t in con.execute("SELECT id,title,block_kind,block_recurrences FROM tasks WHERE status='blocked'"):
    cc = con.execute("SELECT body,author,created_at FROM task_comments WHERE task_id=? ORDER BY rowid DESC LIMIT 1", (t["id"],)).fetchone()
    note = f"{cc['author']} {age(cc['created_at'])}: {cc['body'][:70]}".replace("\n", " ") if cc else "-"
    print(f"{t['id']} lastact={last_activity(t['id'])} kind={t['block_kind']} rec={t['block_recurrences']} | {t['title'][:44]} | {note}")

print("-- todo (5) --")
for t in con.execute("SELECT id,title FROM tasks WHERE status='todo'"):
    par = con.execute("SELECT p.id, p.status FROM task_links l JOIN tasks p ON p.id=l.parent_id WHERE l.child_id=?", (t["id"],)).fetchall()
    parents = ",".join(f"{p['id']}:{p['status']}" for p in par) or "-"
    print(f"{t['id']} lastact={last_activity(t['id'])} parents=[{parents}] {t['title'][:48]}")

print("-- done tanpa ACK (menit pertama setelah selesai, 24 jam terakhir) --")
cutoff = now - 24 * 3600
for t in con.execute("SELECT id,title,completed_at FROM tasks WHERE status='done' AND completed_at>? ORDER BY completed_at DESC LIMIT 15", (cutoff,)):
    rows = con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY rowid", (t["id"],)).fetchall()
    lapor_author = None
    for r in rows:
        if "LAPOR-SELESAI" in r["body"]:
            lapor_author = r["author"]
    acks = [r for r in rows if "RANTAI-ACK" in r["body"]]
    ack_others = [r for r in acks if r["author"] != lapor_author]
    wakes = [r for r in rows if "RANTAI-WAKE" in r["body"]]
    print(f"{t['id']} done_age={age(t['completed_at'])} ACKtotal={len(acks)} ACK_lain_author={len(ack_others)} WAKE={len(wakes)} | {t['title'][:46]}")
con.close()
