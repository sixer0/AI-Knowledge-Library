#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sapu buta-tutup rute-4b (cron sysman 11-10a): SEMUA kartu dengan event terminal
completed/blocked/parked <=6 jam terakhir, TANPA syarat tenant, plus kartu berstatus
review dan kartu running ber-LAPOR tanpa ACK. Read-only. Pola diturunkan dari
sysman_wake_cron_1110f_blind.py."""
import os
import sqlite3
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"),
                  "hermes", "kanban.db")
WINDOW = 6 * 3600
now = int(time.time())

con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

rows = con.execute(
    "SELECT t.id id, t.status st, t.tenant ten, t.assignee asg, t.title title, "
    "MAX(e.created_at) ts, e.kind kind FROM tasks t "
    "JOIN task_events e ON e.task_id=t.id AND e.kind IN ('completed','blocked','parked') "
    "WHERE e.created_at >= ? AND t.status IN ('done','review','blocked','parked') "
    "GROUP BY t.id ORDER BY ts DESC", (now - WINDOW,)).fetchall()
print("terminal_last_6h_any_tenant =", len(rows))
for r in rows:
    lap = con.execute("SELECT author FROM task_comments WHERE task_id=? AND "
                      "(body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR SELESAI%' OR body LIKE '%LAPOR-SELESAI%') "
                      "ORDER BY id DESC LIMIT 1",
                      (r["id"],)).fetchone()
    acks = [a["author"] for a in con.execute(
        "SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",
        (r["id"],)).fetchall()]
    marker = con.execute("SELECT 1 FROM task_comments WHERE task_id=? AND "
                         "body LIKE '%RANTAI-WAKE done-unacked%' LIMIT 1",
                         (r["id"],)).fetchone()
    lap_a = (lap["author"] if lap else None) or "~"
    other = [a for a in acks if a != lap_a]
    age = int((now - r["ts"]) // 60)
    flag = "SILENT" if not other else "acked"
    print("  %s %-8s age=%4dm tenant=%-24r lap=%-18s ack=%-30s marker=%-5s %s | %s"
          % (flag, r["st"], age, r["ten"], lap["author"] if lap else None,
             ",".join(acks) or "NONE", bool(marker), r["kind"],
             (r["title"] or "")[:48]))

print("-- status review --")
for r in con.execute("SELECT id,status,title FROM tasks WHERE status='review'"):
    print("  REVIEW", r["id"], (r["title"] or "")[:60])

print("-- running (blind spot ACK) --")
run = con.execute("SELECT id,tenant,title,last_heartbeat_at FROM tasks WHERE status='running'").fetchall()
print("  running_count =", len(run))
for r in run:
    lap = con.execute("SELECT author,created_at FROM task_comments WHERE task_id=? AND "
                      "body LIKE '%LAPOR%' ORDER BY id DESC LIMIT 1",
                      (r["id"],)).fetchone()
    acks = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND "
                       "body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    hb = r["last_heartbeat_at"]
    hb_age = int((now - hb) / 60) if hb else -1
    print("  %s tenant=%r hb_age=%dm lap=%s ack=%d | %s"
          % (r["id"], r["tenant"], hb_age,
             (lap["author"] + "@" + str(int((now - lap["created_at"]) // 60)) + "m") if lap else "NONE",
             acks, (r["title"] or "")[:52]))

print("-- event terbaru papan (sanity) --")
r = con.execute("SELECT MAX(created_at) m FROM task_events").fetchone()
print("  last_event_age_min =", int((now - r["m"]) // 60))
con.close()
