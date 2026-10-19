# -*- coding: utf-8 -*-
"""Baca komentar lengkap kartu kandidat butir nyata (read-only)."""
import os
import sqlite3
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"),
                  "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = time.time()

for tid in ("t_40ba3fee", "t_c38a042f"):
    t = con.execute("SELECT id,title,status,body,assignee,tenant FROM tasks WHERE id=?", (tid,)).fetchone()
    print("=" * 70)
    print(f"[{t['id']}] {t['status']} assignee={t['assignee']} tenant={t['tenant']}")
    print("TITLE:", t["title"])
    print("BODY(500):", (t["body"] or "")[:500].replace("\r", ""))
    print("-- comments terbaru (6) --")
    for c in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY rowid DESC LIMIT 6", (tid,)):
        print(f"--- [{c['author']}] {(now - float(c['created_at']))/60:.0f}m ---")
        print(c["body"][:900].replace("\r", ""))
con.close()
