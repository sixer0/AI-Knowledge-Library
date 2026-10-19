#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe akhir ronde 14-10 C: badai konkurensi + loop hidup/mati + isi checkpoint."""
import os
import sqlite3
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"),
                  "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())
TEN = "VIBE-BIBLE-1013"

print("=== 1. ADA RUN HIDUP SEKARANG? ===")
live = list(con.execute(
    "SELECT r.id,r.task_id,r.status,r.outcome,r.worker_pid,r.claim_lock,r.claim_expires,"
    "r.last_heartbeat_at FROM task_runs r JOIN tasks t ON t.id=r.task_id WHERE t.tenant=? "
    "AND r.status NOT IN ('completed','timed_out','failed','crashed','gave_up','blocked')", (TEN,)))
print("run non-terminal tenant:", len(live))
for r in live:
    print("  ", dict(r))
any_live = list(con.execute(
    "SELECT COUNT(*) n FROM task_runs WHERE status='running'").fetchone())
print("run status=running seluruh papan:", any_live[0])

print("\n=== 2. PETA WAKTU RUN (badai konkurensi) ===")
runs = list(con.execute(
    "SELECT r.task_id,r.started_at,r.ended_at,r.max_runtime_seconds,r.outcome "
    "FROM task_runs r JOIN tasks t ON t.id=r.task_id WHERE t.tenant=? "
    "AND r.outcome IN ('timed_out','blocked') ORDER BY r.started_at", (TEN,)))
buckets = {}
for r in runs:
    key = int(((r["started_at"] or 0) // 600) * 600)
    buckets.setdefault(key, 0)
    buckets[key] += 1
for k in sorted(buckets):
    print("  start-window %s : %d run" % (time.strftime("%H:%M", time.localtime(k)), buckets[k]))
el = [((r["ended_at"] or r["started_at"]) - r["started_at"]) / 60.0 for r in runs if r["started_at"]]
print("jumlah run gagal:", len(runs), "| durasi menit min/max/rata:",
      round(min(el), 1), round(max(el), 1), round(sum(el) / len(el), 1))
print("total jam kerja terbakar:", round(sum(el) / 60.0, 1))

print("\n=== 3. ISI KOMENTAR PEKERJA (representatif) ===")
for tid in ("t_674377e1", "t_4d7a1691", "t_0df60358", "t_d3cc135a", "t_2543fb8f"):
    print("\n--- %s ---" % tid)
    for c in con.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? "
                         "ORDER BY id", (tid,)):
        print("  [%s] %s" % (c["author"], (c["body"] or "").replace("\r", " ")[:700]))
        print()
