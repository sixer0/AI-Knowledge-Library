#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-only: umur heartbeat + ACK terkini untuk simpul running ber-LAPOR."""
import os
import sqlite3
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
IDS = ["t_fda23cbb", "t_d7fa5da4", "t_98725c99"]

con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())
for tid in IDS:
    t = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    hb = t["last_heartbeat_at"]
    evs = con.execute("SELECT kind, MAX(created_at) ts FROM task_events WHERE task_id=? GROUP BY kind", (tid,)).fetchall()
    last_any = con.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (tid,)).fetchone()[0]
    cs = con.execute("SELECT author, created_at, body FROM task_comments WHERE task_id=? ORDER BY id", (tid,)).fetchall()
    lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "")]
    acks = [c for c in cs if "RANTAI-ACK" in (c["body"] or "")]
    print("%s status=%s hb_age=%ss last_ev_age=%dm runs=%s" % (
        tid, t["status"],
        (now - hb) if hb else -1,
        int((now - last_any) / 60) if last_any else -1,
        {e["kind"]: int((now - e["ts"]) / 60) for e in evs}))
    print("   LAPOR=%s ACK=%s n_cmt=%d" % (
        [(c["author"], int((now - c["created_at"]) / 60)) for c in lapor],
        [(c["author"], int((now - c["created_at"]) / 60)) for c in acks], len(cs)))
    runs = con.execute("SELECT id, outcome, started_at, ended_at FROM task_runs WHERE task_id=? ORDER BY id DESC LIMIT 2", (tid,)).fetchall()
    for r in runs:
        print("   run outcome=%s started_age=%dm ended=%s" % (
            r["outcome"], int((now - r["started_at"]) / 60) if r["started_at"] else -1, r["ended_at"]))
con.close()
