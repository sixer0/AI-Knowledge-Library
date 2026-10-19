#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ronde 14-10c lanjutan: kenapa loop retry mati, ACK kartu done, komentar pasca-event."""
import os, sqlite3, time, json

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

print("=== F. EVENT TERAKHIR 1 KARTU PENULIS (t_2543fb8f) — kenapa berhenti ===")
for r in con.execute("SELECT kind, created_at, substr(COALESCE(payload,''),1,220) p FROM task_events WHERE task_id='t_2543fb8f' ORDER BY id DESC LIMIT 12"):
    print("  [%dmn] %s | %s" % (int((now - r["created_at"]) // 60), r["kind"], (r["p"] or "").replace("\n", " ")[:200]))

print("\n=== G. RUN TERAKHIR t_2543fb8f — metadata/error penuh ===")
for r in con.execute("SELECT id,status,outcome,started_at,ended_at,error,substr(metadata,1,400) md,summary FROM task_runs WHERE task_id='t_2543fb8f' ORDER BY id DESC LIMIT 3"):
    print("  run#%s %s/%s mulai=%dmn lalu ended=%dmn lalu" % (r["id"], r["status"], r["outcome"], int((now - r["started_at"]) // 60), int((now - (r["ended_at"] or now)) // 60)))
    print("    error=%s" % (r["error"] or "")[:200])
    print("    meta=%s" % (r["md"] or "").replace("\n", " ")[:380])
    print("    summary=%s" % (r["summary"] or "")[:200])

print("\n=== H. KOMENTAR TERBARU PER AUTHOR di tenant (siapa bicara terakhir) ===")
for r in con.execute("SELECT c.author, MAX(c.created_at) mx, COUNT(*) c2 FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE t.tenant='VIBE-BIBLE-1013' GROUP BY c.author ORDER BY mx DESC"):
    print("  %-18s terakhir %4dmn lalu, %d komentar" % (r["author"], int((now - r["mx"]) // 60), r["c2"]))

print("\n=== I. 11 KARTU DONE: ACK & LAPOR ===")
for r in con.execute("SELECT id, title, completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done' ORDER BY completed_at DESC"):
    ack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    lap = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()["c"]
    mk = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (r["id"],)).fetchone()["c"]
    print("  %s | %s | done %4dmn lalu | LAPOR=%d ACK=%d MARKER=%d" % (r["id"], (r["title"] or "")[:44], int((now - r["completed_at"]) // 60), lap, ack, mk))

print("\n=== J. APAKAH ADA RUN BARU SETELAH timed_out terakhir per kartu (retry hidup?) ===")
q = """SELECT ru.task_id tid, MAX(ru.id) last_run, MAX(COALESCE(ru.ended_at,ru.started_at)) last_ts
FROM task_runs ru JOIN tasks t ON t.id=ru.task_id
WHERE t.tenant='VIBE-BIBLE-1013' GROUP BY ru.task_id"""
n_new = 0
for r in con.execute(q):
    st = con.execute("SELECT status FROM tasks WHERE id=?", (r["tid"],)).fetchone()["status"]
    age = int((now - r["last_ts"]) // 60)
    if st == "blocked" and age < 100:
        n_new += 1
print("kartu blocked dgn run <100mn lalu: %d (0 = loop mati total)" % n_new)

print("\n=== K. CEK CHECKPOINT/CHECKPOINT-RESUME: berapa kartu menawarkan rem ===")
for r in con.execute("SELECT c.task_id tid, substr(c.body,1,300) b FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked' AND (c.body LIKE '%CHECKPOINT%' OR c.body LIKE '%checkpoint%') ORDER BY c.id DESC LIMIT 4"):
    print("  %s: %s" % (r["tid"], r["b"].replace("\n", " ")[:280]))

print("\n=== L. TUGAS AKHIR DARI 1 RUN TIMED_OUT (apakah PARKED/lanjut-checkpoint ditawarkan) ===")
r = con.execute("SELECT body FROM task_comments c JOIN tasks t ON t.id=c.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND c.body LIKE '%CHECKPOINT-RESUME%' ORDER BY c.id DESC LIMIT 1").fetchone()
if r: print(r["body"][:1200])
