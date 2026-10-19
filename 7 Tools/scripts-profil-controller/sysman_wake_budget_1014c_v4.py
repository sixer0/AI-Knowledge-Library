#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Probe penutup ronde 14-10 C: sisa budget retry + jalur artefak + kartu jangkar."""
import json
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

print("=== SISA BUDGET RETRY (kartu penulis blocked) ===")
rows = list(con.execute(
    "SELECT id,title,status,consecutive_failures,max_retries,claim_lock,claim_expires,"
    "worker_pid,current_run_id,last_failure_error,workspace_path,workspace_kind,session_id "
    "FROM tasks WHERE tenant=? AND status='blocked' ORDER BY id", (TEN,)))
print("blocked:", len(rows))
for r in rows[:6]:
    print("  %s | cf=%s maxR=%s lock=%s exp=%s pid=%s curRun=%s" % (
        r["id"], r["consecutive_failures"], r["max_retries"], r["claim_lock"],
        r["claim_expires"], r["worker_pid"], r["current_run_id"]))
print("  ... workspace_path sampel:", rows[0]["workspace_path"], "| kind:", rows[0]["workspace_kind"])
print("  distinct workspace_path:", set(r["workspace_path"] for r in rows))
print("  distinct max_retries:", set(r["max_retries"] for r in rows))
print("  distinct consecutive_failures:", set(r["consecutive_failures"] for r in rows))
lf = set((r["last_failure_error"] or "")[:90] for r in rows)
print("  last_failure_error unik:", lf)

print("\n=== RUN TERAKHIR per kartu blocked: outcome + kapan ===")
for r in rows[:4]:
    rr = con.execute("SELECT id,status,outcome,started_at,ended_at FROM task_runs "
                     "WHERE task_id=? ORDER BY id DESC LIMIT 1", (r["id"],)).fetchone()
    print("  %s run#%s status=%s outcome=%s endAge=%dm" % (
        r["id"], rr["id"], rr["status"], rr["outcome"],
        int((now - (rr["ended_at"] or rr["started_at"])) // 60)))

print("\n=== KARTU JANGKAR / BLUEPRINT TENANT (semua status) ===")
for r in con.execute("SELECT id,title,status,assignee,created_by FROM tasks WHERE tenant=? "
                     "AND title NOT LIKE '%[VBCB][W%' ORDER BY id", (TEN,)):
    print("  ", dict(r))
print("judul unik pola W*:", sorted(set(
    (r["title"] or "")[:24] for r in con.execute(
        "SELECT title FROM tasks WHERE tenant=?", (TEN,))))[:12])

print("\n=== KARTU DONE TENANT: ACK census (vonis senyap?) ===")
for r in con.execute("SELECT id,title,status FROM tasks WHERE tenant=? AND status='done' ORDER BY id", (TEN,)):
    n_ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",
                        (r["id"],)).fetchone()["n"]
    mk = con.execute("SELECT 1 FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%' LIMIT 1",
                     (r["id"],)).fetchone()
    print("  %s | ack=%d | wakeMarker=%d | %s" % (r["id"], n_ack, int(mk is not None), r["title"][:56]))

print("\n=== EVENT TERMINAL TERAKHIR papan (bukti papan hidup) ===")
for r in con.execute("SELECT e.task_id,e.kind,e.created_at,t.tenant FROM task_events e "
                     "LEFT JOIN tasks t ON t.id=e.task_id ORDER BY e.id DESC LIMIT 8"):
    print("  %s | %-12s | age=%dm | tenant=%s" % (r["task_id"], r["kind"],
          int((now - r["created_at"]) // 60), r["tenant"]))
