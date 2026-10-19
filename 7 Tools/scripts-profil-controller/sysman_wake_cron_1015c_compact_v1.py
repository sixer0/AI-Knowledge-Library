#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ronde 15-10 pagi (sysman) ronde-2: ringkas, tanpa body panjang."""
import os
import sqlite3
import time
from collections import Counter

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())
TEN = "VIBE-BIBLE-1013"

print("== A. gave_up/timed_out sepanjang masa (tenan) ==")
rows = con.execute("SELECT e.kind, COUNT(*) AS n FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? AND e.kind IN ('gave_up','timed_out','crashed') GROUP BY e.kind", (TEN,)).fetchall()
print(dict((r["kind"], r["n"]) for r in rows))
lastev = con.execute("SELECT MAX(e.created_at) AS ts FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=?", (TEN,)).fetchone()["ts"]
print("event_terakhir_tenan_umur=%d mnt" % ((now - lastev) // 60))

print("\n== B. Kartu blocked: umur event + author komentar terakhir ==")
rows = con.execute("SELECT id, title FROM tasks WHERE tenant=? AND status='blocked' ORDER BY created_at", (TEN,)).fetchall()
ages = []
for r in rows:
    le = con.execute("SELECT MAX(created_at) AS ts FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["ts"]
    ages.append((now - le) // 60)
    nb = con.execute("SELECT author FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 1", (r["id"],)).fetchone()
    print("%s ev=%4dmnt lastcmt=%s | %s" % (r["id"], (now - le) // 60, nb["author"] if nb else "-", r["title"][:55]))
print("RENTANG: min=%d max=%d mnt n=%d" % (min(ages), max(ages), len(ages)))

print("\n== C. done tanpa ACK (serah-terima senyap) ==")
done = con.execute("SELECT id, title, completed_at FROM tasks WHERE tenant=? AND status='done'", (TEN,)).fetchall()
noack = []
for r in done:
    n = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["n"]
    mk = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()["n"]
    if n == 0:
        noack.append((r["id"], (now - (r["completed_at"] or 0)) // 60, mk, r["title"]))
print("done=%d tanpa_ACK=%d" % (len(done), len(noack)))
for tid, age, mk, ti in sorted(noack, key=lambda x: -x[1]):
    print("  %s ack=0 marker=%d umur_done=%dmnt | %s" % (tid, mk, age, ti[:55]))

print("\n== D. Token rem pada komentar blocked (CHECKPOINT/cap/konkurensi/watcher) ==")
rows = con.execute("SELECT c.task_id, c.author, c.created_at, CASE WHEN c.body LIKE '%CHECKPOINT%' THEN 'CHECKPOINT' ELSE '' END || CASE WHEN c.body LIKE '%cap%' THEN ' CAP' ELSE '' END || CASE WHEN c.body LIKE '%konkuren%' OR c.body LIKE '%concurren%' THEN ' KONKURENSI' ELSE '' END || CASE WHEN c.body LIKE '%watcher%' THEN ' WATCHER' ELSE '' END AS tokens FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE t.tenant=? AND status_dummy='x' LIMIT 0", (TEN,)).fetchall() if False else []
rows = con.execute(
    "SELECT c.task_id AS tid, c.author AS a, c.created_at AS ts, "
    "(c.body LIKE '%CHECKPOINT%') AS ck, (c.body LIKE '%watcher%') AS wa, "
    "(c.body LIKE '%konkuren%' OR c.body LIKE '%concurren%') AS ko, (c.body LIKE '%max_runtime%' OR c.body LIKE '%naikkan cap%' OR c.body LIKE '%kurangi konkurensi%') AS rem "
    "FROM task_comments c JOIN tasks t ON t.id=c.task_id "
    "WHERE t.tenant=? AND (c.body LIKE '%CHECKPOINT%' OR c.body LIKE '%watcher%' OR c.body LIKE '%konkuren%' OR c.body LIKE '%concurren%' OR c.body LIKE '%max_runtime%') "
    "ORDER BY c.created_at DESC LIMIT 12", (TEN,)).fetchall()
for r in rows:
    print("%s [%s @%dmnt] ck=%d watcher=%d konk=%d rem=%d" % (r["tid"], r["a"], (now - r["ts"]) // 60, r["ck"], r["wa"], r["ko"], r["rem"]))
if not rows:
    print("(kosong)")

print("\n== E. Papan non-tenan VBCB (status terbuka) ==")
rows = con.execute("SELECT id, status, tenant, created_by, title FROM tasks WHERE status NOT IN ('done','archived') AND (tenant IS NULL OR tenant != ?) ORDER BY status, created_at DESC", (TEN,)).fetchall()
print("jumlah_terbuka_non-VBCB=%d" % len(rows))
for r in rows:
    le = con.execute("SELECT MAX(created_at) AS ts FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["ts"]
    lap = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()["n"]
    ack = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["n"]
    print("  %s [%s] tenant=%s by=%s ev=%dmnt LAPOR=%d ACK=%d | %s" % (r["id"], r["status"], r["tenant"], r["created_by"], (now - le) // 60 if le else -1, lap, ack, r["title"][:60]))

print("\n== F. Marker RANTAI-WAKE di tenan VBCB ==")
rows = con.execute("SELECT c.task_id AS tid, c.author AS a, c.created_at AS ts FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE t.tenant=? AND c.body LIKE '%RANTAI-WAKE%' ORDER BY c.created_at DESC LIMIT 10", (TEN,)).fetchall()
for r in rows:
    print("%s [%s @%dmnt]" % (r["tid"], r["a"], (now - r["ts"]) // 60))
if not rows:
    print("(tidak ada)")

print("\n== G. Komentar author controller 24 jam terakhir lintas papan ==")
rows = con.execute("SELECT c.task_id AS tid, t.tenant AS ten, c.author AS a, c.created_at AS ts, substr(replace(c.body, char(10), ' '),1,110) AS b FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE c.author IN ('default','mission-wake','sysmanager-cleaner','gsp-master','gsp-master01') AND c.created_at >= ? ORDER BY c.created_at DESC LIMIT 12", (now - 24 * 3600,)).fetchall()
for r in rows:
    print("[%s %s @%dmnt] %s: %s" % (r["tid"], r["ten"], (now - r["ts"]) // 60, r["a"], r["b"]))
if not rows:
    print("(tidak ada)")
con.close()
