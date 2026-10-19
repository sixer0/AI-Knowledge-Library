#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-scan kanonis + rekonsiliasi ronde cron 12-10 (read-only)."""
import importlib.util
import os
import sqlite3
import time

SCRIPTS = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location(
    "wake_scan", os.path.join(SCRIPTS, "gsp_mission_wake_scan.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

db = mod.DEFAULT_DB
now = int(time.time())
authors = mod.DEFAULT_AUTHORS.split(",")
findings = mod.scan(db, now, authors)
print("RESCAN findings =", len(findings))
for f in findings:
    print("WAKE", *f)

con = sqlite3.connect("file:" + db.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

print("-- status census --")
for r in con.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status"):
    print(r["status"], "=", r["n"])

print("-- kartu terbuka (blocked/review/todo): umur event terakhir + komentar controller --")
ph = ",".join("?" * len(authors))
for r in con.execute(
        "SELECT t.id, t.status, t.title, t.tenant, "
        "COALESCE((SELECT MAX(e.created_at) FROM task_events e WHERE e.task_id=t.id), t.created_at) last_ev "
        "FROM tasks t WHERE t.status IN ('blocked','review','todo') ORDER BY last_ev"):
    age = int((now - r["last_ev"]) // 60)
    ctrl = con.execute(
        "SELECT MAX(c.created_at) mx, c.author FROM task_comments c "
        "WHERE c.task_id=? AND c.author IN (%s) GROUP BY c.author" % ph,
        [r["id"]] + authors).fetchone()
    ctrl_after = ""
    if ctrl and ctrl["mx"] and ctrl["mx"] >= r["last_ev"]:
        ctrl_after = "ctrl_comment_after=%s" % ctrl["author"]
    excl = con.execute(
        "SELECT 1 FROM task_comments WHERE task_id=? AND body LIKE '%PROF-MERGE-1010%' LIMIT 1",
        (r["id"],)).fetchone()
    print("%s [%s] age=%dm tenant=%s %s %s | %s" % (
        r["id"], r["status"], age, r["tenant"] or "-", ctrl_after,
        "PM1010" if excl else "", (r["title"] or "")[:48]))

print("-- terminal events <=6h tanpa syarat tenant (blind rute-4b) --")
cand = con.execute(
    "SELECT e.task_id id, MAX(e.created_at) ts, t.status, t.tenant "
    "FROM task_events e JOIN tasks t ON t.id=e.task_id "
    "WHERE e.kind IN ('completed','blocked') AND t.status IN ('done','review','blocked') "
    "AND e.created_at >= ? GROUP BY e.task_id HAVING ts >= ?",
    (now - 6 * 3600, mod.DONE_UNACKED_CUTOFF)).fetchall()
print("kandidat terminal <=6h:", len(cand))
for r in cand:
    lap = con.execute(
        "SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%' "
        "ORDER BY id DESC LIMIT 1", (r["id"],)).fetchone()
    acks = con.execute(
        "SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",
        (r["id"],)).fetchall()
    lap_a = (lap[0] if lap else "") or "~"
    other = any((a[0] or "") != lap_a for a in acks)
    marker = con.execute(
        "SELECT 1 FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%' LIMIT 1",
        (r["id"],)).fetchone()
    tenant_ok = bool(r["tenant"])
    print("%s status=%s tenant=%s lap=%s ack_lain=%s marker=%s tenant_gate=%s" % (
        r["id"], r["status"], r["tenant"] or "-", lap_a, other,
        bool(marker), tenant_ok))
con.close()
