# -*- coding: utf-8 -*-
"""Rekonsiliasi: kenapa kandidat done-unacked longgar tidak lolos rute-4b kanonis."""
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())

ids = ["t_96332f33", "t_2d9cf424", "t_5c4fddea", "t_e087f2ba"]
for tid in ids:
    t = con.execute("SELECT id,title,status,tenant,assignee,created_by,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    print("== %s | status=%s tenant=%r assignee=%r created_by=%r" % (tid, t["status"], t["tenant"], t["assignee"], t["created_by"]))
    evs = [dict(r) for r in con.execute("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 8", (tid,))]
    for e in evs:
        print("   ev %s @ %.1fm" % (e["kind"], (now - e["created_at"]) / 60.0))
    cms = [dict(r) for r in con.execute("SELECT author,substr(body,1,90) b,created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 8", (tid,))]
    for c in cms:
        print("   cm [%s] @ %.1fm :: %s" % (c["author"], (now - c["created_at"]) / 60.0, c["b"].replace("\n", " ")[:88]))
con.close()
