#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cek komentar terakhir 11 kartu done VBCB + marker RANTAI-WAKE (read-only)."""
import os, sqlite3, time
DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
NOW = int(time.time())
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
ids = ["t_87b1a40e","t_4330b479","t_5957156d","t_b378d64e","t_68f547bd","t_87aa2f1f","t_ff19af14","t_2de376b5","t_be215530","t_c6512519","t_009f2fdc"]
for tid in ids:
    t = con.execute("SELECT title,status,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    nmark = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (tid,)).fetchone()["c"]
    print("%s | doneAge=%dm | MARKER=%d | %s" % (tid, int((NOW-t["completed_at"])/60) if t["completed_at"] else -1, nmark, t["title"][:60]))
    for c in con.execute("SELECT author, substr(replace(body,char(10),' '),1,110) b, created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 2", (tid,)).fetchall():
        print("   [%s %dm] %s" % (c["author"], int((NOW-c["created_at"])/60), c["b"]))
con.close()
