# -*- coding: utf-8 -*-
"""Replikakan kondisi rute-4b read-only utk kartu done tanpa ACK: kenapa
pemindai tidak menemukannya (tenant kosong / assignee controller / jendela waktu)."""
import os
import sqlite3
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"),
                  "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = time.time()

ids = ["t_ef0a078e", "t_6e8a2e73", "t_aef19275", "t_dc05872f"]
for tid in ids:
    t = con.execute("SELECT id,status,tenant,assignee,created_by,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=? AND kind IN ('completed','blocked')", (tid,)).fetchone()["m"]
    print(f"{tid} status={t['status']} tenant={t['tenant']!r} assignee={t['assignee']!r} created_by={t['created_by']!r} ev_completed_age={(now - ev)/60:.1f}m" if ev else f"{tid} NO terminal event")
    # komentar terakhir
    for c in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY rowid DESC LIMIT 3", (tid,)):
        print(f"   c[{c['author']}] {(now - float(c['created_at']))/60:.1f}m: {c['body'][:100]}".replace("\n", " "))

# siapa saja author controller yang dikecualikan skrip? baca dari sumber
import re
src = open(r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py", encoding="utf-8").read()
m = re.search(r"controller_authors\s*=\s*(\[[^\]]*\]|[^#\n]+)", src)
print("controller_authors def:", m.group(0) if m else "NOT FOUND")
m2 = re.search(r"DONE_UNACKED_WINDOW\s*=\s*[^#\n]+", src)
print(m2.group(0) if m2 else "window NOT FOUND")
m3 = re.search(r"DONE_UNACKED_CUTOFF\s*=\s*[^#\n]+", src)
print(m3.group(0) if m3 else "cutoff NOT FOUND")
con.close()
