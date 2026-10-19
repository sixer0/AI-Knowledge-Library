#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rekonsiliasi cron mission-wake 11-10 (ronde f): vonis kanonis scan() +
fakta predikat per kandidat WAKE=1 dari alat detail (read-only)."""
import importlib.util
import os
import sqlite3
import time

SCRIPTS = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"),
                       "hermes", "scripts")
DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"),
                  "hermes", "kanban.db")
AUTHORS = "default,sysmanager-cleaner,mission-wake".split(",")

spec = importlib.util.spec_from_file_location(
    "wake_scan", os.path.join(SCRIPTS, "gsp_mission_wake_scan.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

now = int(time.time())
print("now_epoch =", now, "| cutoff =", mod.DONE_UNACKED_CUTOFF,
      "| window_h =", mod.DONE_UNACKED_WINDOW / 3600)

# 1. Vonis kanonis
findings = mod.scan(DB, now, AUTHORS)
print("CANONICAL_SCAN_FINDINGS =", len(findings))
for f in findings:
    print("  WAKE", *f)

con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

# 2. Sensus status (sanity papan)
print("-- status census --")
for r in con.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print("  %s = %d" % (r["status"], r["n"]))

# 3. Kartu running (blind-spot check)
running = con.execute("SELECT id,title FROM tasks WHERE status='running'").fetchall()
print("running_cards =", len(running))
for r in running:
    print("  RUNNING", r["id"], r["title"][:60])

# 4. Fakta predikat per kandidat dari alat detail
CAND = ["t_090415ec", "t_f4de0f1f", "t_5d087ab1", "t_e034cb5e",
        "t_df6a4a8a", "t_a707d4a3"]
print("-- kandidat detail-WAKE=1: fakta predikat rute-4b --")
for tid in CAND:
    t = con.execute("SELECT id,status,tenant,assignee,title FROM tasks WHERE id=?",
                    (tid,)).fetchone()
    ev = con.execute(
        "SELECT kind, MAX(created_at) ts FROM task_events WHERE task_id=? "
        "AND kind IN ('completed','blocked') GROUP BY task_id", (tid,)).fetchone()
    lap = con.execute(
        "SELECT author, created_at FROM task_comments WHERE task_id=? AND "
        "body LIKE '%LAPOR-SELESAI%' ORDER BY id DESC LIMIT 1", (tid,)).fetchone()
    acks = con.execute(
        "SELECT author, created_at FROM task_comments WHERE task_id=? AND "
        "body LIKE '%RANTAI-ACK%' ORDER BY id", (tid,)).fetchall()
    marker = con.execute(
        "SELECT 1 FROM task_comments WHERE task_id=? AND "
        "body LIKE '%RANTAI-WAKE done-unacked%' LIMIT 1", (tid,)).fetchone()
    ts = ev["ts"] if ev else None
    age = int((now - ts) // 60) if ts else None
    in_window = (ts is not None and ts >= now - mod.DONE_UNACKED_WINDOW)
    in_cutoff = (ts is not None and ts >= mod.DONE_UNACKED_CUTOFF)
    print("  %s status=%s tenant=%r assignee=%r term=%s@%s age=%sm in6h=%s postcutoff=%s"
          % (tid, t["status"], t["tenant"], t["assignee"],
             ev["kind"] if ev else None, ts, age, in_window, in_cutoff))
    print("     lap_author=%s ack_authors=%s marker=%s | %s"
          % (lap["author"] if lap else None,
             [a["author"] for a in acks] or "NONE",
             bool(marker), (t["title"] or "")[:55]))
con.close()
