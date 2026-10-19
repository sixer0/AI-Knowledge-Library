# -*- coding: utf-8 -*-
"""Ronde 15-10d cron: simpul blocked VBCB (alasan+checkpoint+umur), rekonsiliasi done-unacked longgar."""
import sqlite3, time
from collections import Counter

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

# A) simpul blocked VBCB: alasan + umur event + checkpoint
print("=== A. SIMPUL blocked VBCB ===")
ages = []
reasons = Counter()
cp = 0
for r in con.cursor().execute("SELECT id,title,result FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='blocked'"):
    ev = con.cursor().execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["mx"]
    ages.append((now-(ev or 0))/60.0)
    key = ((r["result"] or "")[:80]).replace("\n", " ")
    if not key:
        c = con.cursor().execute("SELECT substr(body,1,80) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (r["id"],)).fetchone()
        key = (c["b"] if c else "(tanpa alasan)").replace("\n", " ")
    reasons[key] += 1
    n_cp = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%CHECKPOINT%'", (r["id"],)).fetchone()["n"]
    if n_cp: cp += 1
print("blocked n=%s umur_ev min=%.0f max=%.0f mnt | kartu ber-CHECKPOINT=%s" % (len(ages), min(ages), max(ages), cp))
for k, n in reasons.most_common(6):
    print("  %2dx | %s" % (n, k))

# B) gave_up per kartu penulis (konfirmasi beku permanen)
gu = con.cursor().execute("SELECT COUNT(DISTINCT e.task_id) n FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind='gave_up'").fetchone()["n"]
to = con.cursor().execute("SELECT COUNT(DISTINCT e.task_id) n FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND e.kind='timed_out'").fetchone()["n"]
runn = con.cursor().execute("SELECT COUNT(*) n FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='running'").fetchone()["n"]
print("\n=== B. kartu VBCB ber-event timed_out=%s gave_up=%s | running=%s" % (to, gu, runn))

# C) komentar CHECKPOINT terbaru (isi rem yang ditawarkan worker)
print("\n=== C. contoh komentar CHECKPOINT (terbaru) ===")
for c in con.cursor().execute("""SELECT t.id, c.author, c.created_at, substr(c.body,1,220) b FROM task_comments c
 JOIN tasks t ON t.id=c.task_id WHERE t.tenant='VIBE-BIBLE-1013' AND c.body LIKE '%CHECKPOINT%'
 ORDER BY c.created_at DESC LIMIT 2"""):
    print("  [%s] %.0fm | %s\n    %s" % (c["author"], (now-c["created_at"])/60, c["id"], (c["b"] or "").replace("\n", " ")[:200]))

# D) rekonsiliasi done-unacked longgar: kenapa tidak jadi baris WAKE (window 6 jam?)
print("\n=== D. rekonsiliasi kandidat done tanpa ACK (cek umur selesai vs jendela) ===")
import importlib.util
spec = importlib.util.spec_from_file_location("wake_scan", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
src = open("C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py", encoding="utf-8").read()
import re
m = re.findall(r"(RUN_WINDOW_H|DONE_UNACKED_MIN|CUTOFF\w*)\s*=\s*[0-9]+", src)
print("ambang dari sumber:", m)
for tid in ("t_9bff1001", "t_817b0c60", "t_b8f35c42", "t_1caad711"):
    t = con.cursor().execute("SELECT id,status,tenant,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    lap = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (tid,)).fetchone()["n"]
    hrs = (now - (t["completed_at"] or 0))/3600.0
    print("  %s | %s | selesai %.1f jam lalu | LAPOR=%s" % (tid, t["status"], hrs, lap))

# E) tenant lain dengan kartu terbuka (anti-lewat): sensus status non-VBCB
print("\n=== E. kartu TERBUKA lintas tenant selain VBCB ===")
for r in con.cursor().execute("""SELECT COALESCE(NULLIF(tenant,''),'(null)') ten, status, COUNT(*) n FROM tasks
 WHERE status IN ('running','blocked','todo') AND tenant <> 'VIBE-BIBLE-1013'
 GROUP BY ten, status ORDER BY n DESC LIMIT 25"""):
    print("  %-24s %-8s %s" % (r["ten"], r["status"], r["n"]))
