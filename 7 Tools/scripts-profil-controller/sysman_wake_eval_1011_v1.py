#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-only evaluasi baris WAKE mission-wake 11-10 (korpus lanjutan)."""
import os, sqlite3, sys, time, importlib.util

DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
IDS = ["t_090415ec", "t_a3378d47", "t_f4de0f1f"]
now = int(time.time())

con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

print("NOW", now)
for tid in IDS:
    t = con.execute("SELECT id,title,status,tenant,assignee,created_at,started_at,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    print("=" * 70)
    print("CARD", tid, "|", t["status"], "| tenant", t["tenant"], "| assignee", t["assignee"])
    print("  title:", (t["title"] or "")[:110])
    evs = con.execute("SELECT kind,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 6", (tid,)).fetchall()
    print("  events:", [(e["kind"], now - e["created_at"]) for e in evs])
    cs = con.execute("SELECT author,created_at,body FROM task_comments WHERE task_id=? ORDER BY created_at ASC", (tid,)).fetchall()
    print("  comments:", len(cs))
    for c in cs:
        b = (c["body"] or "").replace("\n", " / ")
        tag = ""
        if "RANTAI-ACK" in b: tag = "[ACK]"
        elif "RANTAI-WAKE" in b: tag = "[WAKE-MARKER]"
        elif "LAPOR-SELESAI" in b: tag = "[LAPOR-SELESAI]"
        elif "PARKED" in b: tag = "[PARKED]"
        print("   ", tag or "[other]", c["author"], "age_min=%d" % ((now - c["created_at"]) // 60), "|", b[:150])
    acks = [c for c in cs if "RANTAI-ACK" in (c["body"] or "")]
    wakes = [c for c in cs if "RANTAI-WAKE done-unacked" in (c["body"] or "")]
    print("  >> ACK count:", len(acks), "| WAKE marker count:", len(wakes))

print("=" * 70)
print("TENANT CENSUS KORPUS-LANJUTAN-1011")
rows = con.execute("SELECT id,status,title,completed_at FROM tasks WHERE tenant='KORPUS-LANJUTAN-1011' ORDER BY id").fetchall()
from collections import Counter
print("  total cards:", len(rows), dict(Counter(r["status"] for r in rows)))
for r in rows:
    nack = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()[0]
    mark = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()[0]
    print("   ", r["id"], r["status"], "ack=%d wake_mark=%d" % (nack, mark), "|", (r["title"] or "")[:60])

print("=" * 70)
print("BOARD SANITY")
for q, lbl in [("SELECT COUNT(*) FROM tasks", "tasks"), ("SELECT COUNT(*) FROM task_events", "events"),
               ("SELECT COUNT(*) FROM task_comments", "comments"),
               ("SELECT MAX(created_at) FROM task_events", "last_event_epoch")]:
    v = con.execute(q).fetchone()[0]
    print("  ", lbl, "=", v, ("(age_min=%d)" % ((now - v) // 60)) if lbl == "last_event_epoch" else "")
con.close()
