#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ronde 14-Oct: (F) sampel komentar kartu GSF done (apakah serah-terima tercatat tanpa
token RANTAI-ACK), (G) hasil 3 kartu terakhir AIE26SAT + artefak xlsx di disk,
(H) komentar terakhir t_bb725705 utuh + induk t_1caad711. Read-only."""
import os
import sqlite3
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())


def age(ts):
    return round((now - ts) / 60.0, 1)


print("### F. SAMPEL KOMENTAR KARTU GSF done (serah-terima tanpa token?)")
for tid in ("t_40cefa7e", "t_9a813cbb", "t_d371afd9"):
    print("  -- %s" % tid)
    for c in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (tid,)):
        print("     [%7.1f mnt] %-16s :: %s" % (age(c["created_at"]), c["author"], (c["body"] or "").replace("\n", " ")[:260]))

print("\n### G. HASIL AKHIR AIE26SAT (3 kartu terakhir)")
for tid in ("t_9bff1001", "t_db5bc59a", "t_fe512da4"):
    r = con.execute("SELECT id,status,result,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    print("  -- %s [%s] selesai %s mnt lalu" % (r["id"], r["status"], age(r["completed_at"]) if r["completed_at"] else "-"))
    print("     RESULT: %s" % (r["result"] or "").replace("\n", " ")[:500])

print("\n### H. t_bb725705 komentar terakhir utuh + induk t_1caad711")
for c in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id='t_bb725705' ORDER BY created_at DESC LIMIT 1"):
    print("  [%6.1f mnt] %s ::\n%s" % (age(c["created_at"]), c["author"], c["body"]))
p = con.execute("SELECT id,status,title,result,completed_at FROM tasks WHERE id='t_1caad711'").fetchone()
if p:
    print("  INDUK %s [%s] selesai %s mnt :: %s" % (p["id"], p["status"], age(p["completed_at"]) if p["completed_at"] else "-", (p["title"] or "")[:80]))
    print("     RESULT: %s" % (p["result"] or "").replace("\n", " ")[:400])
    for c in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id='t_1caad711' ORDER BY created_at DESC LIMIT 3"):
        print("     kom [%7.1f mnt] %-14s :: %s" % (age(c["created_at"]), c["author"], (c["body"] or "").replace("\n", " ")[:300]))

print("\n### I. 4 kartu todo (cek turunan-stalled positif-palsu)")
for r in con.execute("SELECT id,status,title,assignee,tenant FROM tasks WHERE status='todo' ORDER BY created_at"):
    pars = [x["parent_id"] for x in con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (r["id"],))]
    pstat = [(pid, con.execute("SELECT status FROM tasks WHERE id=?", (pid,)).fetchone()["status"]) for pid in pars]
    le = con.execute("SELECT MAX(created_at) AS m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    print("  %-12s %-8s ev=%-7s parents=%s %s" % (r["id"], r["status"], (str(age(le)) + "m") if le else "-", pstat, (r["title"] or "")[:60]))
