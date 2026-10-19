#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ronde cron 15-10b langkah-3: nilai kandidat blind-spot t_b9aac21a + cek exemption author."""
import os
import sqlite3
import time

LOCALAPPDATA = os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local")
DB = os.path.join(LOCALAPPDATA, "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())

tid = "t_b9aac21a"
t = con.execute("SELECT id,title,status,tenant,created_by,created_at,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
print("id=%s status=%s tenant=%r by=%s created=%s completed=%s" % (
    t["id"], t["status"], t["tenant"], t["created_by"],
    time.strftime("%d-%m %H:%M", time.localtime(t["created_at"])),
    time.strftime("%d-%m %H:%M", time.localtime(t["completed_at"])) if t["completed_at"] else "-"))
print("judul=%s" % t["title"])
print("\n-- komentar --")
for c in con.execute("SELECT author, created_at, substr(body,1,300) AS b FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)):
    print("[%s @%s] %s" % (c["author"], time.strftime("%d-%m %H:%M", time.localtime(c["created_at"])), c["b"].replace("\n", " | ")[:280]))
print("\n-- event --")
for e in con.execute("SELECT kind, author, created_at FROM task_events WHERE task_id=? ORDER BY created_at", (tid,)):
    print("%s by=%s @%s" % (e["kind"], e["author"], time.strftime("%d-%m %H:%M", time.localtime(e["created_at"]))))
print("\n-- link --")
for l in con.execute("SELECT parent_id, child_id FROM task_links WHERE parent_id=? OR child_id=?", (tid, tid)):
    print("parent=%s child=%s" % (l["parent_id"], l["child_id"]))
