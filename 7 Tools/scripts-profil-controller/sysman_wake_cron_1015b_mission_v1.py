#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ronde 15-10 pagi (sysman): vonis tingkat-misi VIBE-BIBLE-1013 + sapuan buta-tutup kartu lain.
Read-only."""
import os
import sqlite3
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())
TEN = "VIBE-BIBLE-1013"

print("== 1. KARTU BLOCKED (orang tua) tenan %s: alasan + umur event ==" % TEN)
rows = con.execute("SELECT id, title, substr(COALESCE(body,''),1,200) AS b, created_at FROM tasks WHERE tenant=? AND status='blocked' ORDER BY id", (TEN,)).fetchall()
ages = []
for r in rows:
    le = con.execute("SELECT MAX(created_at) AS ts FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["ts"] or r["created_at"]
    ages.append((now - le) // 60)
    note = ""
    nb = con.execute("SELECT body FROM task_comments WHERE task_id=? ORDER BY id DESC LIMIT 1", (r["id"],)).fetchone()
    if nb:
        note = nb["body"].replace("\n", " ")[:130]
    print("%s ev=%dmin | %s | cmt: %s" % (r["id"], (now - le) // 60, r["title"][:60], note))
if ages:
    print("RENTANG UMUR EVENT blocked: min=%d max=%d mnt (n=%d)" % (min(ages), max(ages), len(ages)))

print("\n== 2. EVENT gave_up/timed_out sepanjang masa (tenan ini) ==")
rows = con.execute("SELECT e.task_id, e.kind, e.created_at, t.status FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? AND e.kind IN ('gave_up','timed_out') ORDER BY e.created_at DESC LIMIT 80", (TEN,)).fetchall()
from collections import Counter
cnt = Counter(r["kind"] for r in rows)
print("counts:", dict(cnt), "| total_baris_ditampilkan:", len(rows))
newest = rows[0]["created_at"] if rows else None
if newest:
    print("gagal_terbaru_umur=%d mnt" % ((now - newest) // 60))

print("\n== 3. SENSUS ACK kartu done tenan (serah-terima senyap) ==")
done = con.execute("SELECT id, title, completed_at FROM tasks WHERE tenant=? AND status='done' ORDER BY completed_at DESC", (TEN,)).fetchall()
noack = []
for r in done:
    n = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["n"]
    mk = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()["n"]
    if n == 0:
        noack.append((r["id"], r["title"][:50], (now - (r["completed_at"] or 0)) // 60, mk))
print("done=%d tanpa_ACK=%d" % (len(done), len(noack)))
for tid, ti, age, mk in noack:
    print("  %s ack=0 marker=%d umur_done=%dmnt | %s" % (tid, mk, age, ti))

print("\n== 4. Komentar CHECKPOINT / rem pada kartu blocked (cari opsi controller) ==")
rows = con.execute("SELECT DISTINCT c.task_id, c.author, substr(c.body,1,220) AS b, c.created_at FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE t.tenant=? AND (c.body LIKE '%CHECKPOINT%' OR c.body LIKE '%lanjut-checkpoint%' OR c.body LIKE '%cap%' OR c.body LIKE '%watcher%') ORDER BY c.created_at DESC LIMIT 12", (TEN,)).fetchall()
for r in rows:
    print("[%s @%dmnt] %s: %s" % (r["task_id"], (now - r["created_at"]) // 60, r["author"], r["b"].replace("\n", " ")))
if not rows:
    print("(kosong)")

print("\n== 5. SENSUS status seluruh papan (non-tenan ini) ==")
rows = con.execute("SELECT status, COUNT(*) AS n FROM tasks WHERE status NOT IN ('done','archived') AND (tenant IS NULL OR tenant != ?) GROUP BY status", (TEN,)).fetchall()
print({r["status"]: r["n"] for r in rows})
rows = con.execute("SELECT id, status, tenant, created_by, title FROM tasks WHERE status NOT IN ('done','archived') AND (tenant IS NULL OR tenant != ?) ORDER BY status LIMIT 20", (TEN,)).fetchall()
for r in rows:
    le = con.execute("SELECT MAX(created_at) AS ts FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["ts"]
    lap = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()["n"]
    ack = con.execute("SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["n"]
    print("  %s [%s] tenant=%s ev=%dmnt LAPOR=%d ACK=%d | %s" % (r["id"], r["status"], r["tenant"], (now - le) // 60 if le else -1, lap, ack, r["title"][:70]))

print("\n== 6. Riwayat ronde sysman sebelumnya (marker RANTAI-WAKE di tenan ini) ==")
rows = con.execute("SELECT c.task_id, c.author, c.created_at, substr(c.body,1,80) AS b FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE t.tenant=? AND c.body LIKE '%RANTAI-WAKE%' ORDER BY c.created_at DESC LIMIT 10", (TEN,)).fetchall()
for r in rows:
    print("%s [%s @%dmnt] %s" % (r["task_id"], r["author"], (now - r["created_at"]) // 60, r["b"].replace("\n", " ")))
if not rows:
    print("(tidak ada marker di tenan ini)")

print("\n== 7. Komentar controller/default terbaru lintas papan (cek apakah misi sudah ternilai) ==")
rows = con.execute("SELECT c.task_id, t.tenant, c.author, substr(c.body,1,150) AS b, c.created_at FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE c.author IN ('default','mission-wake','sysmanager-cleaner','gsp-master','gsp-master01') AND c.created_at >= ? ORDER BY c.created_at DESC LIMIT 15", (now - 24 * 3600,)).fetchall()
for r in rows:
    print("[%s %s @%dmnt] %s: %s" % (r["task_id"], r["tenant"], (now - r["created_at"]) // 60, r["author"], r["b"].replace("\n", " ")))
con.close()
