# -*- coding: utf-8 -*-
"""Ronde 15-10 cron: gali VBCB — alasan blocked+author komentar triase, census ACK done, simpul running."""
import sqlite3, time
from collections import Counter

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

TEN = "VIBE-BIBLE-1013"

print("=== A. KARTU BLOCKED VBCB: alasan + komentar terakhir ===")
rows = con.cursor().execute("SELECT id,title,status,completed_at,body,block_kind,block_recurrences FROM tasks WHERE tenant=? AND status='blocked'", (TEN,)).fetchall()
print("jumlah blocked:", len(rows))
auth_cmt = Counter()
for r in rows[:3]:
    print("\n", r["id"], "|", r["title"][:60])
    body = con.cursor().execute("SELECT body FROM tasks WHERE id=?", (r["id"],)).fetchone()
    # tasks may not have body col; try
print("contoh reason/body kolom tasks:", [c[1] for c in con.cursor().execute("PRAGMA table_info(tasks)").fetchall()])

# ambil kolom yang ada
cols = [c[1] for c in con.cursor().execute("PRAGMA table_info(tasks)").fetchall()]
bodycol = "body" if "body" in cols else ("description" if "description" in cols else None)
for r in rows[:4]:
    txt = r[bodycol] if bodycol else ""
    print("\n--- %s | %s\n    body[:220]=%s" % (r["id"], r["title"][:55], (txt or "")[:220].replace("\n", " / ")))
    q = con.cursor().execute("SELECT author, created_at, substr(body,1,160) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 2", (r["id"],)).fetchall()
    for c in q:
        auth_cmt[c["author"]] += 1
        print("    cmt[%s] %dm lalu: %s" % (c["author"], round((now - c["created_at"]) / 60), c["b"].replace("\n", " / ")))
print("author komentar teratas (sampel 4 kartu):", dict(auth_cmt))

print("\n=== B. CENSUS ACK KARTU DONE VBCB ===")
done = con.cursor().execute("SELECT id,title,completed_at FROM tasks WHERE tenant=? AND status='done'", (TEN,)).fetchall()
noack, acked, nolap = [], [], []
for d in done:
    lap = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (d["id"],)).fetchone()["n"]
    ack = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (d["id"],)).fetchone()["n"]
    mk = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (d["id"],)).fetchone()["n"]
    rec = (d["id"], d["title"][:48], lap, ack, mk)
    if ack == 0:
        noack.append(rec)
    else:
        acked.append(rec)
    if lap == 0:
        nolap.append(rec)
print("done=%s | ack=0: %s | ber-ACK: %s | tanpa-LAPOR: %s" % (len(done), len(noack), len(acked), len(nolap)))
for rec in noack[:15]:
    print("  NOACK", rec)

print("\n=== C. SIMPUL RUNNING t_deb670d0 ===")
q = con.cursor().execute("SELECT * FROM tasks WHERE id='t_deb670d0'").fetchone()
print("status=%s assignee=%s" % (q["status"], q["assignee"]))
for e in con.cursor().execute("SELECT kind, created_at FROM task_events WHERE task_id='t_deb670d0' ORDER BY created_at DESC LIMIT 8"):
    print("  ev %s %dm" % (e["kind"], round((now - e["created_at"]) / 60)))
for c in con.cursor().execute("SELECT author, created_at, substr(body,1,200) b FROM task_comments WHERE task_id='t_deb670d0' ORDER BY created_at DESC LIMIT 4"):
    print("  cmt[%s] %dm: %s" % (c["author"], round((now - c["created_at"]) / 60), c["b"].replace("\n", " / ")))

print("\n=== D. EVENT unblocked 24 JAM (watcher melepas?) ===")
n = con.cursor().execute("SELECT COUNT(*) n FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant=? AND e.kind='unblocked' AND e.created_at>?", (TEN, now - 86400)).fetchone()["n"]
print("unblocked 24 jam:", n)

print("\n=== E. FASE token pada kartu blocked (peredam fase-stalled) ===")
tot = 0
for r in rows:
    f = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%[FASE]%'", (r["id"],)).fetchone()["n"]
    if f:
        tot += 1
print("kartu blocked dgn komentar [FASE]:", tot, "dari", len(rows))

print("\n=== F. Umur promoted terakhir kartu blocked (fase-stalled tagih) ===")
ages = []
for r in rows:
    p = con.cursor().execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=? AND kind='promoted'", (r["id"],)).fetchone()["mx"]
    if p:
        ages.append((now - p) / 60.0)
if ages:
    print("promoted terakhir: min=%.0f max=%.0f menit (n=%s)" % (min(ages), max(ages), len(ages)))
