# -*- coding: utf-8 -*-
"""Ronde 15-10b cron lanjutan: blokade 33 orang-tua, jejak timeout/gave_up, ACK done,
   pembanding ronde-ronde sebelumnya (apakah ini baris baru atau tagihan berulang)."""
import sqlite3, time

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

IDS = [r["id"] for r in con.cursor().execute(
    "SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo' ORDER BY id")]
parents = []
for i in IDS:
    for p in con.cursor().execute("SELECT parent_id FROM task_links WHERE child_id=?", (i,)):
        pr = con.cursor().execute("SELECT id,status,title,assignee FROM tasks WHERE id=?", (p["parent_id"],)).fetchone()
        if pr and pr["status"] not in ("done",):
            parents.append(pr)

print("=== A. orang-tua yang memblokir (n=%s) ===" % len(parents))
for pr in parents[:40]:
    ev = con.cursor().execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (pr["id"],)).fetchone()["mx"]
    lastc = con.cursor().execute("SELECT author, substr(body,1,150) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (pr["id"],)).fetchone()
    print("%s | %-8s | %s | ev=%.0fm | %s" % (pr["id"], pr["status"], pr["assignee"], (now - (ev or 0)) / 60.0, (pr["title"] or "")[:50]))
    if lastc:
        print("     com[%s]: %s" % (lastc["author"], lastc["b"].replace("\n", " ")))

print("\n=== B. sensus kind event pada kartu blocked VBCB ===")
from collections import Counter
c = Counter()
for r in con.cursor().execute("SELECT e.kind k FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked'"):
    c[r["k"]] += 1
print(dict(c))
print("\n   contoh payload gave_up/timed_out:")
for r in con.cursor().execute("""SELECT e.task_id, e.kind, e.created_at, substr(COALESCE(e.payload,''),1,200) p
    FROM task_events e JOIN tasks t ON t.id=e.task_id
    WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind IN ('gave_up','timed_out') ORDER BY e.created_at DESC LIMIT 6"""):
    print("  %s | %s | %.0fm | %s" % (r["task_id"], r["kind"], (now - r["created_at"]) / 60.0, r["p"].replace("\n", " ")))

print("\n=== C. komentar penanda ronde sysman terdahulu di tenant ini ===")
for r in con.cursor().execute("""SELECT t.id, c.author, substr(c.body,1,90) b, c.created_at FROM task_comments c
    JOIN tasks t ON t.id=c.task_id WHERE t.tenant='VIBE-BIBLE-1013'
    AND (c.body LIKE '%RANTAI-WAKE%' OR c.body LIKE '%RANTAI-ACK%') ORDER BY c.created_at DESC LIMIT 25"""):
    print("  %s | %s | %.0fm | %s" % (r["id"], r["author"], (now - r["created_at"]) / 60.0, r["b"].replace("\n", " ")))
n_wake = con.cursor().execute("""SELECT COUNT(DISTINCT task_id) n FROM task_comments c JOIN tasks t ON t.id=c.task_id
    WHERE t.tenant='VIBE-BIBLE-1013' AND c.body LIKE '%RANTAI-WAKE%'""").fetchone()["n"]
print("  kartu VBCB ber-marker RANTAI-WAKE:", n_wake)

print("\n=== D. done VBCB tanpa ACK (serah-terima senyap) ===")
q = con.cursor().execute("""SELECT t.id, t.completed_at,
      (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-ACK%') ack,
      (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%LAPOR%SELESAI%') lap
    FROM tasks t WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='done'""").fetchall()
noack = [r for r in q if r["ack"] == 0]
print("done=%s tanpa-ACK=%s" % (len(q), len(noack)))
for r in noack[:12]:
    print("   %s lap=%s selesai %.0fm lalu" % (r["id"], r["lap"], (now - (r["completed_at"] or now)) / 60.0))

print("\n=== E. status run terakhir per kartu blocked (retry_status) ===")
try:
    cols = [d[1] for d in con.cursor().execute("PRAGMA table_info(task_runs)")]
    print("kolom task_runs:", cols)
    for r in con.cursor().execute("""SELECT t.id, r.status, r.outcome, r.created_at FROM task_runs r
        JOIN tasks t ON t.id=r.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='blocked'
        ORDER BY r.created_at DESC LIMIT 8"""):
        print("  %s | %s | %s | %.0fm" % (r["id"], r["status"], r["outcome"], (now - r["created_at"]) / 60.0))
except Exception as e:
    print("task_runs gagal:", e)
