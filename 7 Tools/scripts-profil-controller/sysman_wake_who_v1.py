# -*- coding: utf-8 -*-
"""Siapa yang menutup RG19 + komentar terakhir (read-only)."""
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
    return f"{(now - float(v))/60:.1f}m"

print("-- events RG19 terbaru --")
for e in con.execute("SELECT kind,created_at,payload FROM task_events WHERE task_id='t_40ba3fee' ORDER BY rowid DESC LIMIT 6"):
    pay = (str(e["payload"])[:120] if "payload" in e.keys() else "")
    print(f"{e['kind']} {age(e['created_at'])} {pay}")

print("-- komentar RG19 terbaru (3) --")
for c in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id='t_40ba3fee' ORDER BY rowid DESC LIMIT 3"):
    print(f"[{c['author']}] {age(c['created_at'])}: {c['body'][:200]}".replace("\n", " "))

print("-- events RG20 terbaru: promosi oleh siapa --")
for e in con.execute("SELECT kind,created_at,payload FROM task_events WHERE task_id='t_6b458b6f' ORDER BY rowid DESC LIMIT 4"):
    pay = (str(e["payload"])[:120] if "payload" in e.keys() else "")
    print(f"{e['kind']} {age(e['created_at'])} {pay}")
con.close()
