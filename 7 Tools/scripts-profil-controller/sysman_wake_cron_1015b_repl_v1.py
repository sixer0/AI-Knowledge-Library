# -*- coding: utf-8 -*-
"""Ronde 15-10b: nasib kartu pengganti M4 rebuild (ekstrak dari komentar, bukan result)."""
import sqlite3, time, re
from collections import Counter

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

targets = set()
for a in con.cursor().execute("""SELECT c.body FROM task_comments c JOIN tasks t ON t.id=c.task_id
 WHERE t.tenant='VIBE-BIBLE-1013' AND c.body LIKE '%Digantikan t_%'""").fetchall():
    m = re.search(r'Digantikan (t_[0-9a-f]+)', a["body"])
    if m: targets.add(m.group(1))
st = Counter(); detail = []
for tid in sorted(targets):
    t = con.cursor().execute("SELECT id,status,title FROM tasks WHERE id LIKE ?", (tid+"%",)).fetchone()
    if not t: st["(hilang)"] += 1; continue
    st[t["status"]] += 1
    ev = con.cursor().execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (t["id"],)).fetchone()["mx"]
    detail.append((t["status"], t["id"], (now-(ev or 0))/60.0, (t["title"] or "")[:48]))
print("pengganti M4 rebuild n=%s status=%s" % (len(targets), dict(st)))
for s in sorted(detail):
    print("%-8s %s ev=%.0fm %s" % s)

print("\n=== kartu M4 rebuild yang masih todo/blocked (belum dirilis?) ===")
for s, tid, age, title in detail:
    if s != "done":
        c = con.cursor().execute("SELECT author, substr(body,1,100) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 2", (tid,)).fetchall()
        for x in c:
            print("  %s | %.0fm | %s: %s" % (tid, (now-x["created_at"])/60.0, x["author"], x["b"].replace("\n"," ")))
