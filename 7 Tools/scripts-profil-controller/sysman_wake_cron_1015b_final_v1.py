# -*- coding: utf-8 -*-
"""Ronde 15-10b cron: kelengkapan penulis per bab vs verifikasi terbuka + vonis akhir."""
import sqlite3, time, re
from collections import Counter

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def bab(title):
    m = re.search(r'bab (\d+)', title or "", re.I)
    return int(m.group(1)) if m else None

print("=== A. penulis EN done per bab (M4/rebuild) ===")
writers_done = {}
for r in con.cursor().execute("SELECT id,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done' AND title LIKE '%Penulis%'").fetchall():
    b = bab(r["title"])
    if b: writers_done.setdefault(b, []).append(r["id"])
print("bab dengan penulis done:", sorted(writers_done), "| jumlah bab:", len(writers_done))

print("\n=== B. verifikasi todo per bab -> apakah penulis bab itu sudah done? ===")
verif = con.cursor().execute("SELECT id,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo' AND title LIKE '%Verifikasi%'").fetchall()
ok_ready = 0; not_ready = []
for r in verif:
    b = bab(r["title"])
    if b in writers_done: ok_ready += 1
    else: not_ready.append((r["id"], b))
print("verifikasi todo=%s | penulis bab-nya sudah done=%s | belum ada penulis done=%s %s" % (len(verif), ok_ready, len(not_ready), not_ready))

print("\n=== C. bab tanpa penulis done sama sekali ===")
all_bab = set()
for r in con.cursor().execute("SELECT title FROM tasks WHERE tenant='VIBE-BIBLE-1013'").fetchall():
    b = bab(r["title"])
    if b: all_bab.add(b)
missing = sorted(all_bab - set(writers_done))
print("semua bab yang disebut di tenant:", len(all_bab), "| tanpa penulis done:", missing)
for b in missing:
    for r in con.cursor().execute("SELECT id,status,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND title LIKE ?", ("%bab %d%%" % b,)).fetchall():
        ev = con.cursor().execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["mx"]
        print("   bab %s: %s [%s] ev=%.0fm %s" % (b, r["id"], r["status"], (now-(ev or 0))/60.0, r["title"][:52]))

print("\n=== D. kartu done terbaru: kapan gelombang selesai + LAPOR tanpa ACK terakhir ===")
q = con.cursor().execute("""SELECT t.id,t.title,t.completed_at FROM tasks t WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='done'
 ORDER BY t.completed_at DESC LIMIT 5""").fetchall()
for a in q:
    print("%s | %.0f mnt | %s" % (a["id"], (now-(a["completed_at"] or 0))/60.0, (a["title"] or "")[:55]))
