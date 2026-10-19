# -*- coding: utf-8 -*-
"""Ronde 15-10b cron: struktur orang tua 33 todo WAKE + nasib kartu rebuild + aktivitas 3 jam terakhir."""
import sqlite3, time
from collections import Counter

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("=== A. pasangan orang tua per kartu todo WAKE (siapa blocked vs done) ===")
rows = con.cursor().execute("""SELECT t.id, t.title FROM tasks t WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='todo'""").fetchall()
pat = Counter()
for r in rows:
    ps = con.cursor().execute("""SELECT p.id,p.status,p.title FROM task_links l JOIN tasks p ON p.id=l.parent_id WHERE l.child_id=?""", (r["id"],)).fetchall()
    stat = tuple(sorted(p["status"] for p in ps))
    pat[(stat, len(ps))] += 1
    if r["id"] == "t_002af121":
        for p in ps:
            print("  contoh t_002af121 <- %s [%s] %s" % (p["id"], p["status"], p["title"][:60]))
print("pola (status ortu, jumlah):", dict(pat))

print("\n=== B. kartu rebuild pengganti: status ===")
repl = [x.split()[1].rstrip('().') for x in [] ]
ids = con.cursor().execute("""SELECT result FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'""").fetchall()
import re
targets = set()
for a in ids:
    m = re.search(r'Digantikan (t_[0-9a-f]+)', a["result"] or "")
    if m: targets.add(m.group(1))
st = Counter(); run = []
for tid in sorted(targets):
    t = con.cursor().execute("SELECT id,status,title FROM tasks WHERE id LIKE ?", (tid+"%",)).fetchone()
    if not t: st["(hilang)"] += 1; continue
    st[t["status"]] += 1
    if t["status"] == "running": run.append((t["id"], t["title"][:50]))
print("rebuild n=%s status=%s" % (len(targets), dict(st)))
for x in run: print("  RUNNING:", x)

print("\n=== C. semua kartu tenant yang bukan (blocked-superseded/todo-wake/done): running? ===")
q = con.cursor().execute("""SELECT id,status,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status NOT IN ('todo','blocked','done')""").fetchall()
for a in q: print("%s | %s | %s" % (a["id"], a["status"], a["title"][:60]))
print("(kosong = tidak ada status lain)")

print("\n=== D. timeline event tenant 3 jam terakhir (kind x umur) ===")
q = con.cursor().execute("""SELECT e.kind, e.created_at, e.task_id FROM task_events e JOIN tasks t ON t.id=e.task_id
 WHERE t.tenant='VIBE-BIBLE-1013' AND e.created_at > ? ORDER BY e.created_at DESC LIMIT 25""", (now-3*3600,)).fetchall()
for a in q:
    print("%.0fm | %-12s | %s" % ((now-a["created_at"])/60.0, a["kind"], a["task_id"]))
c2 = Counter(a["kind"] for a in q)
print("ringkas 3 jam:", dict(c2))

print("\n=== E. kartu timed_out terbaru (31m): status kini + elapsed ===")
q = con.cursor().execute("""SELECT DISTINCT e.task_id FROM task_events e JOIN tasks t ON t.id=e.task_id
 WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind='timed_out' AND e.created_at > ?""", (now-2*3600,)).fetchall()
for a in q:
    t = con.cursor().execute("SELECT id,status,title FROM tasks WHERE id=?", (a["task_id"],)).fetchone()
    ev = con.cursor().execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (a["task_id"],)).fetchone()["mx"]
    print("%s | %s | ev=%.0fm | %s" % (t["id"], t["status"], (now-(ev or 0))/60.0, (t["title"] or "")[:55]))
