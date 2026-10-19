#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bobot turunan transitif kartu verifikasi G4 + status terkini (read-only)."""
import os, sqlite3, time
DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
cols = [r[1] for r in con.execute("PRAGMA table_info(task_links)")]
print("task_links cols:", cols)
par_col = "parent_task_id" if "parent_task_id" in cols else ("parent" if "parent" in cols else cols[0])
ch_col = "child_task_id" if "child_task_id" in cols else ("child" if "child" in cols else cols[1])

def descendants(root):
    seen, stack = set(), [root]
    while stack:
        cur = stack.pop()
        for r in con.execute("SELECT child_id AS c FROM task_links WHERE parent_id=?", (cur,)):
            if r["c"] not in seen:
                seen.add(r["c"]); stack.append(r["c"])
    return seen

for tid in ["t_555599e8", "t_6145749f"]:
    t = con.execute("SELECT status,title FROM tasks WHERE id=?", (tid,)).fetchone()
    ds = descendants(tid)
    dst = {d: con.execute("SELECT status FROM tasks WHERE id=?", (d,)).fetchone()["status"] for d in ds}
    hb = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=? AND kind='heartbeat'", (tid,)).fetchone()["m"]
    ev = con.execute("SELECT kind,MAX(created_at) m FROM task_events WHERE task_id=? GROUP BY kind ORDER BY m DESC", (tid,)).fetchall()
    cs = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=?", (tid,)).fetchone()["n"]
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["n"]
    print(tid, "|", t["status"], "| heartbeat_age_min=", (now - hb) // 60 if hb else None,
          "| comments=%d ack=%d" % (cs, ack), "| descendants=%d" % len(ds), dst or "")
    print("   last events:", [(e["kind"], (now - e["m"]) // 60) for e in ev[:4]])
con.close()
