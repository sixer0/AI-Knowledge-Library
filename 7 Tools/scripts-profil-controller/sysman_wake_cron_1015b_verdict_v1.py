# -*- coding: utf-8 -*-
"""Ronde 15-10b cron: vonis simpul - kartu rebuild pengganti, kartu blocked tunggal,
   census ACK vs marker pada done, dan keadaan run aktif tenant."""
import sqlite3, time

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

REPL = ["t_ad5d8e6f","t_c2180f14","t_0f3e37eb","t_7707a0cd","t_7124c228","t_6a370834",
        "t_ed8b0b54","t_ccfca3b8","t_b2b82e31","t_0ba22121","t_80a9fb43","t_de73c01d",
        "t_b10a1e32","t_ca284fa4","t_99bb85a4","t_ed9976be","t_0ac8927f","t_19930381",
        "t_6aa0384c","t_fa568361","t_7f36de9e","t_5291d587","t_a148a692","t_a66ce30a",
        "t_deb670d0","t_0913266d","t_aa98df31","t_896447e4","t_b7d31583","t_de326482",
        "t_eb458a5e","t_5715d1fc","t_0918b6d2"]

print("=== A. status 33 kartu rebuild pengganti ===")
from collections import Counter
st = Counter()
for i in REPL:
    r = con.cursor().execute("SELECT id,status,title,assignee,completed_at FROM tasks WHERE id=?", (i,)).fetchone()
    if not r:
        print(i, "HILANG"); continue
    st[r["status"]] += 1
print(dict(st))
# contoh isi komentar terakhir 3 kartu
for i in REPL[:3]:
    lastc = con.cursor().execute("SELECT author, substr(body,1,220) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 2", (i,)).fetchall()
    print("--", i)
    for c in lastc:
        print("   [%s] %.0fm: %s" % (c["author"], (now - c["created_at"]) / 60.0, c["b"].replace("\n", " ")))

print("\n=== B. kartu blocked tunggal VBCB ===")
for r in con.cursor().execute("SELECT id,status,title,assignee,result FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'"):
    ev = con.cursor().execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["mx"]
    print("%s | %s | %s | ev=%.0fm | %s" % (r["id"], r["status"], r["assignee"], (now-(ev or 0))/60.0, (r["title"] or "")[:60]))
    print("   result:", (r["result"] or "")[:200].replace("\n", " "))
    for c in con.cursor().execute("SELECT author, substr(body,1,200) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (r["id"],)):
        print("   com[%s] %.0fm: %s" % (c["author"], (now - c["created_at"]) / 60.0, c["b"].replace("\n", " ")))

print("\n=== C. done VBCB: ACK vs marker RANTAI-WAKE ===")
q = con.cursor().execute("""SELECT t.id,
   (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-ACK%') ack,
   (SELECT COUNT(*) FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-WAKE%') mk
   FROM tasks t WHERE t.tenant='VIBE-BIBLE-1013' AND t.status='done'""").fetchall()
print("done=%s | ber-marker=%s | tanpa-marker=%s" % (len(q), sum(1 for r in q if r["mk"]), sum(1 for r in q if not r["mk"])))
print("tanpa-marker:", [r["id"] for r in q if not r["mk"]])

print("\n=== D. run aktif (running/claimed) di seluruh papan + tenant VBCB ===")
for r in con.cursor().execute("""SELECT r.task_id, r.profile, r.status, r.outcome, r.started_at, r.last_heartbeat_at,
      substr(COALESCE(r.error,''),1,80) e FROM task_runs r WHERE r.status NOT IN ('completed','failed','timed_out','gave_up','cancelled')
      ORDER BY r.started_at DESC LIMIT 12"""):
    print("  %s | %s | %s | hb=%.0fm | %s" % (r["task_id"], r["profile"], r["status"], (now-(r["last_heartbeat_at"] or 0))/60.0, r["e"]))
vb = con.cursor().execute("""SELECT COUNT(*) n FROM task_runs r JOIN tasks t ON t.id=r.task_id
   WHERE t.tenant='VIBE-BIBLE-1013' AND r.status NOT IN ('completed','failed','timed_out','gave_up','cancelled')""").fetchone()["n"]
print("run non-terminal VBCB:", vb)

print("\n=== E. anak todo: siapa saja + apakah semua punya orang-tua blocked ===")
n_all = con.cursor().execute("SELECT COUNT(*) n FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo'").fetchone()["n"]
n_blocked_parent = 0
for r in con.cursor().execute("SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo'"):
    ps = con.cursor().execute("""SELECT t2.status s FROM task_links l JOIN tasks t2 ON t2.id=l.parent_id WHERE l.child_id=?""", (r["id"],)).fetchall()
    if any(p["s"] == "blocked" for p in ps):
        n_blocked_parent += 1
print("todo=%s yg punya orang-tua blocked=%s" % (n_all, n_blocked_parent))
