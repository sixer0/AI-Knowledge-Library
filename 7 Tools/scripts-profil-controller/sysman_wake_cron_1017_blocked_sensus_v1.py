#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sensus kartu blocked: koreksi terakhir per kartu (ronde 17-10, read-only)."""
import os
import sqlite3
import time

HOME = os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local")
DB = os.path.join(HOME, "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())

ids = [r["id"] for r in con.execute("SELECT id FROM tasks WHERE status='blocked' ORDER BY id")]
print("BLOCKED=%d" % len(ids))
untouched = []
for tid in ids:
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    cm = con.execute(
        "SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 1",
        (tid,)).fetchone()
    body = (cm["body"] if cm else "") or ""
    covered = any(tok in body for tok in ("[SYSMAN-CLEANER", "RANTAI-WAKE", "RANTAI-ACK", "Digantikan", "PROF-MERGE-1010"))
    ctrl_after = bool(cm and cm["author"] in ("default", "sysmanager-cleaner", "mission-wake") and ev and cm["created_at"] >= ev)
    if not (covered or ctrl_after):
        untouched.append((tid, body[:70].replace("\n", " | "), cm["author"] if cm else "-"))
print("COVERED=%d UNTOUCHED=%d" % (len(ids) - len(untouched), len(untouched)))
for u in untouched:
    print("  UNTOUCHED %s [%s] %s" % u)
con.close()
