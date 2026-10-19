#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ronde 17-10 pagi: rekonsiliasi stdout kosong vs 44 kartu blocked.
Read-only. Menjalankan scan() kanonis via importlib (mENGAMBIL nilai kembali,
bukan redirect_stdout - preseden 15-10) lalu sensus komentar terakhir per blocked."""
import importlib.util
import os
import sqlite3
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
DB = os.path.join(os.path.dirname(HERE), "kanban.db")

spec = importlib.util.spec_from_file_location(
    "wake_scan", os.path.join(HERE, "gsp_mission_wake_scan.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

now = int(time.time())
authors = mod.DEFAULT_AUTHORS.split(",")
findings = mod.scan(DB, now, authors)
print("SCAN findings =", len(findings))
for f in findings:
    print("  ", tuple(f))

con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

print("\n-- census status (open) --")
for r in con.execute("SELECT status, COUNT(*) n FROM tasks WHERE status NOT IN "
                     "('done','archived') GROUP BY status ORDER BY n DESC"):
    print("  %s = %d" % (r["status"], r["n"]))

print("\n-- umur event terakhir papan (MAX) --")
mx = con.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
mc = con.execute("SELECT MAX(created_at) FROM task_comments").fetchone()[0]
print("  events  age_min = %.1f" % ((now - mx) / 60.0))
print("  comments age_min = %.1f" % ((now - mc) / 60.0))

print("\n-- blocked: komentar terakhir per kartu (id | tenant | created_by | umur_ev_mnt | rem?) --")
ids = [r["id"] for r in con.execute(
    "SELECT id FROM tasks WHERE status='blocked' ORDER BY id")]
no_rem = []
for tid in ids:
    c = con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=?"
                    " ORDER BY id DESC LIMIT 1", (tid,)).fetchone()
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?",
                     (tid,)).fetchone()["m"]
    t = con.execute("SELECT tenant, created_by, title FROM tasks WHERE id=?",
                    (tid,)).fetchone()
    body = (c["body"] if c else "") or ""
    age = (now - (ev or 0)) / 60.0
    rem = ("SYSMAN-CLEANER" in body) or ("RANTAI-WAKE" in body) or ("RANTAI-ACK" in body) \
        or ("Digantikan" in body) or ("ANCHOR-KONTRAK" in body)
    tag = "REM" if rem else "NO-REM"
    if not rem:
        no_rem.append(tid)
    print("  %s | %s | %s | %7.0f | %s | %s" % (
        tid, (t["tenant"] or "-")[:16], (t["created_by"] or "-")[:18], age, tag,
        (body.replace("\n", " ")[:70] if body else "<KOMENTAR NOL>")))

print("\nNO-REM count =", len(no_rem), no_rem)

# blind spot: running dengan LAPOR tanpa ACK (mustahil bila nol running, tetap diukur)
print("\n-- blind spot running --")
rows = list(con.execute("SELECT id, tenant, last_heartbeat_at FROM tasks WHERE status='running'"))
print("  running =", len(rows))
for r in rows:
    lap = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'",
                      (r["id"],)).fetchone()["n"]
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",
                      (r["id"],)).fetchone()["n"]
    hb = ((now - r["last_heartbeat_at"]) / 60.0) if r["last_heartbeat_at"] else -1
    print("   %s lap=%d ack=%d hb_age_min=%.1f" % (r["id"], lap, ack, hb))

# kandidat done-unacked longgar (jendela 6h, tanpa gerbang tenant) sebagai sapuan tambahan
print("\n-- sapuan longgar terminal <=6h (rekonsilasi, bukan vonis) --")
cut = now - 6 * 3600
for r in con.execute("SELECT e.task_id id, MAX(e.created_at) ts FROM task_events e "
                     "JOIN tasks t ON t.id=e.task_id "
                     "WHERE e.kind IN ('completed','blocked') AND t.status IN ('done','review','blocked') "
                     "AND e.created_at>=? GROUP BY e.task_id HAVING ts>=?", (cut, cut)):
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",
                      (r["id"],)).fetchone()["n"]
    mk = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'",
                     (r["id"],)).fetchone()["n"]
    t = con.execute("SELECT tenant, status FROM tasks WHERE id=?", (r["id"],)).fetchone()
    print("   %s status=%s tenant=%s ack=%d marker=%d age_min=%.0f" % (
        r["id"], t["status"], (t["tenant"] or "-"), ack, mk, (now - r["ts"]) / 60.0))
con.close()
