#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Blindspot sweep: kartu running tenant KORPUS-LANJUTAN-1011 — umur heartbeat + LAPOR vs ACK."""
import os, sqlite3, time
DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
rows = con.execute("SELECT id,title,assignee,started_at FROM tasks WHERE tenant='KORPUS-LANJUTAN-1011' AND status='running'").fetchall()
for r in rows:
    hb = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=? AND kind='heartbeat'", (r["id"],)).fetchone()["m"]
    runs = con.execute("SELECT id,status,outcome,started_at,ended_at FROM task_runs WHERE task_id=? ORDER BY started_at DESC LIMIT 2", (r["id"],)).fetchall()
    cs = con.execute("SELECT author,created_at,body FROM task_comments WHERE task_id=? ORDER BY created_at", (r["id"],)).fetchall()
    lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "") or "LAPOR-SELESAI" in (c["body"] or "").upper()]
    ack = [c for c in cs if "RANTAI-ACK" in (c["body"] or "")]
    print(r["id"], "|", (r["title"] or "")[:70])
    print("   started_age_min=%s heartbeat_age_min=%s comments=%d lapor=%d ack=%d" % (
        (now - r["started_at"]) // 60 if r["started_at"] else None,
        (now - hb) // 60 if hb else None, len(cs), len(lapor), len(ack)))
    for ru in runs:
        print("   run", ru["id"], ru["status"], ru["outcome"], "age_min=", (now - (ru["ended_at"] or ru["started_at"])) // 60)
    for c in cs[-3:]:
        print("   cmt", c["author"], "age_min=%d" % ((now - c["created_at"]) // 60), "|", (c["body"] or "").replace("\n", " / ")[:160])
con.close()
