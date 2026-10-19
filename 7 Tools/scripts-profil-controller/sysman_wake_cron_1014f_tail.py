#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cek akhir: nasib t_bb725705 (ronde lalu) + dua simpul DATUM1014 ber-LAPOR tanpa ACK."""
import os, sqlite3, time
DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
NOW = int(time.time())
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

for tid in ["t_bb725705", "t_2b10bac7", "t_8439633f"]:
    t = con.execute("SELECT id,title,status,tenant,created_by,assignee FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print("%s NOT-IN-DB" % tid); continue
    hb = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    print("\n#### %s | st=%s | tenant=%s | by=%s | asg=%s | hbAge=%dm" % (
        tid, t["status"], t["tenant"], t["created_by"], t["assignee"], int((NOW-hb)/60) if hb else -1))
    print("  TITLE: %s" % (t["title"] or ""))
    for c in con.execute("SELECT author, substr(replace(body,char(10),' '),1,120) b, created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 4", (tid,)):
        print("   [%s|%dm] %s" % (c["author"], int((NOW-c["created_at"])/60), c["b"]))

# apakah dua simpul DATUM sudah done sekarang?
for tid in ["t_2b10bac7", "t_8439633f"]:
    rs = con.execute("SELECT outcome, MAX(COALESCE(ended_at,started_at)) mx FROM task_runs WHERE task_id=? GROUP BY outcome", (tid,)).fetchall()
    print("\nRUNS %s: %s" % (tid, [(r["outcome"], int((NOW-r["mx"])/60)) for r in rs]))
con.close()
