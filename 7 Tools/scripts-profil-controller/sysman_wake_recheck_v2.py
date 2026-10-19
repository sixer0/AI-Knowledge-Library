#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-check butiran blind-spot v2: status terkini, komentar terbaru, link papan (read-only)."""
import os, sqlite3, time

db = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect("file:" + db.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())

cols = [r["name"] for r in con.execute("PRAGMA table_info(task_links)")]
print("task_links cols:", cols)

for tid in ("t_40ba3fee", "t_b4a49859"):
    t = con.execute("SELECT id,status,title FROM tasks WHERE id=?", (tid,)).fetchone()
    print("=" * 66)
    print(tid, "|", t["status"], "|", t["title"][:70])
    lastev = con.execute("SELECT MAX(created_at) ts FROM task_events WHERE task_id=?", (tid,)).fetchone()["ts"]
    print("  last_event_age_min:", int((now - lastev) // 60))
    runs = con.execute("SELECT outcome, started_at, ended_at FROM task_runs WHERE task_id=? ORDER BY started_at DESC LIMIT 3", (tid,)).fetchall()
    for r in runs:
        print("  run:", r["outcome"], "start_age_min=", int((now - r["started_at"]) // 60), "ended_age_min=", (int((now - r["ended_at"]) // 60) if r["ended_at"] else None))
    cs = con.execute("SELECT created_at, author, substr(body,1,160) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 6", (tid,)).fetchall()
    for c in cs:
        print("   cmt [%dm] %s :: %s" % (int((now - c["created_at"]) // 60), c["author"], c["b"].replace("\n", " | ")))
    try:
        ls = con.execute("SELECT * FROM task_links WHERE child=? OR parent=?", (tid, tid)).fetchall()
    except sqlite3.OperationalError:
        ls = con.execute("SELECT * FROM task_links WHERE child_id=? OR parent_id=?", (tid, tid)).fetchall()
    open_desc = []
    for l in ls:
        d = dict(l)
        other = d.get("parent") or d.get("parent_id")
        child = d.get("child") or d.get("child_id")
        role = "PARENT-of" if child == tid else "child-of"
        st = con.execute("SELECT status FROM tasks WHERE id=?", (other,)).fetchone()
        print("   link %s %s [%s]" % (role, other, st["status"] if st else "?"))
        if role == "parent-of" and st and st["status"] not in ("done", "archived"):
            open_desc.append(other)
    print("  OPEN descendants direct:", len(open_desc))
