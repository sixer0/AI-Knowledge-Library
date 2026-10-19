# -*- coding: utf-8 -*-
"""Ronde 15-10b cron: siapa yang hidup 107 mnt lalu + blind spot running/LAPOR tanpa ACK."""
import sqlite3, time
from collections import Counter

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("=== A. event papan umur <=12h (siapa bergerak terakhir) ===")
cut = now - 12 * 3600
for r in con.cursor().execute("""SELECT e.task_id, e.kind, e.created_at, t.status, t.tenant, substr(t.title,1,50) ti
    FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE e.created_at>=?
    ORDER BY e.created_at DESC LIMIT 15""", (cut,)):
    print("  %4.0fm | %-10s | %-12s | %-8s | %s | %s" % ((now - r["created_at"]) / 60, r["kind"], r["task_id"], r["status"], r["tenant"] or "(null)", r["ti"]))

print("\n=== B. kartu running lintas SELURUH papan (blind spot) ===")
run = con.cursor().execute("SELECT id,status,title,tenant,assignee FROM tasks WHERE status='running'").fetchall()
print("  jumlah running:", len(run))
for r in run:
    ev = con.cursor().execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["mx"]
    lap = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR SELESAI%')", (r["id"],)).fetchone()["n"]
    ack = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["n"]
    print("  %s | %-14s | ev=%.0fm lap=%s ack=%s | %s | %s" % (r["id"], r["tenant"] or "(null)", (now - (ev or 0)) / 60, lap, ack, r["assignee"] or "-", (r["title"] or "")[:52]))

print("\n=== C. kartu blocked non-VBCB umur >2h (butuh tangan lain?) ===")
for r in con.cursor().execute("SELECT id,title,tenant FROM tasks WHERE status='blocked' AND tenant IS NOT NULL AND tenant!='VIBE-BIBLE-1013'"):
    ev = con.cursor().execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["mx"]
    age = (now - (ev or 0)) / 60
    if age > 120:
        print("  %s | %-18s | %6.0fm | %s" % (r["id"], r["tenant"], age, (r["title"] or "")[:56]))

print("\n=== D. sampel komentar 1 kartu blocked VBCB (isi triase/CHECKPOINT?) ===")
b = con.cursor().execute("SELECT id,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked' LIMIT 1").fetchone()
cs = con.cursor().execute("SELECT author, substr(body,1,160) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (b["id"],)).fetchall()
print("  kartu:", b["id"], b["title"])
for c in cs:
    print("   -", c["author"], ":", c["b"].replace("\n", " "))
if not cs:
    print("   (tanpa komentar)")

print("\n=== E. umur marker sysman pada done VBCB (min/max) ===")
ages = []
for r in con.cursor().execute("""SELECT c.created_at FROM task_comments c JOIN tasks t ON t.id=c.task_id
    WHERE t.tenant='VIBE-BIBLE-1013' AND c.body LIKE '%RANTAI-WAKE done-unacked%'"""):
    ages.append((now - r["created_at"]) / 60)
print("  marker n=%s umur min=%.0f max=%.0f mnt" % (len(ages), min(ages), max(ages)))

print("\n=== F. reason blocked VBCB (kolom result) ===")
rc = Counter()
for r in con.cursor().execute("SELECT COALESCE(substr(result,1,80),'(null)') x FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'"):
    rc[r["x"].replace("\n", " ")] += 1
for k, n in rc.most_common(6):
    print("  %2dx %s" % (n, k))
