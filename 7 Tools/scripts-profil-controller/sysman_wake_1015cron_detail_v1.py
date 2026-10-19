# -*- coding: utf-8 -*-
"""Ronde 15-10 cron: alasan blocked 33 kartu + bukti ACK=0 done VBCB + status bab 6."""
import sqlite3, time
from collections import Counter

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("=== A. alasan blocked 33 kartu (kolom result / komentar BLOCKED terakhir) ===")
reasons = Counter()
for r in con.cursor().execute("SELECT id,title,result FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'"):
    c = con.cursor().execute("SELECT author, substr(body,1,110) b FROM task_comments WHERE task_id=? AND body LIKE '%BLOCKED%' ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
    key = None
    if r["result"]:
        key = (r["result"] or "")[:90].replace("\n", " ")
    if not key and c:
        key = "[%s] %s" % (c["author"], c["b"].replace("\n", " "))
    reasons[key or "(tanpa alasan)"] += 1
for k, n in reasons.most_common():
    print("%2dx | %s" % (n, k))

print("\n=== B. cek ulang ACK=0 pada kartu done VBCB (query longgar) ===")
q = con.cursor().execute("""SELECT COUNT(*) n FROM task_comments c JOIN tasks t ON t.id=c.task_id
 WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='done' AND c.body LIKE '%ACK%'""").fetchone()["n"]
print("komentar ber-token 'ACK' pada done VBCB:", q)
q2 = con.cursor().execute("""SELECT author, COUNT(*) n FROM task_comments c JOIN tasks t ON t.id=c.task_id
 WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='done' GROUP BY author""").fetchall()
print("author komentar pada done VBCB:", {a["author"]: a["n"] for a in q2})

print("\n=== C. nasib bab 6 (satu-satunya tanpa penulis EN done) ===")
for r in con.cursor().execute("SELECT id,status,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND title LIKE '%bab 6%'"):
    ev = con.cursor().execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["mx"]
    print("  %s | %s | ev=%.0fm | %s" % (r["id"], r["status"], (now - (ev or 0)) / 60, r["title"][:60]))

print("\n=== D. umur event terakhir per kartu blocked (sebar flat?) ===")
ages = []
for r in con.cursor().execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'"):
    ev = con.cursor().execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["mx"]
    ages.append((now - (ev or 0)) / 60.0)
print("blocked n=%s umur_ev min=%.0f max=%.0f mnt" % (len(ages), min(ages), max(ages)))
