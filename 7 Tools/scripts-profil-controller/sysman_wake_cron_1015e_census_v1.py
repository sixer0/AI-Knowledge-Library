# -*- coding: utf-8 -*-
"""Ronde 15-10e cron: cakupan bab VBCB, census ACK done VBCB+tenant lain, marker existing."""
import sqlite3, time, re
from collections import defaultdict

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

# 1) cakupan bab: penulis M4 done per bab 1..37
rows = con.cursor().execute("SELECT id,title,status FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND (title LIKE '%Penulis bab%' OR title LIKE '%M4%')").fetchall()
bych = defaultdict(list)
for r in rows:
    m = re.search(r"bab (\d+)", r["title"] or "")
    if m: bych[int(m.group(1))].append(r["status"])
missing = [b for b in range(1, 38) if "done" not in bych.get(b, [])]
print("bab tanpa penulis done:", missing or "TIDAK ADA (37/37 tercover)")

# 2) census ACK kartu done VBCB
dn = con.cursor().execute("SELECT id,title,completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'").fetchall()
ack0 = 0; mk0 = 0
for r in dn:
    ack = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["n"]
    if ack == 0:
        ack0 += 1
        mk = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()["n"]
        if mk: mk0 += 1
print("VBCB done=%s | ack=0: %s | dari itu sudah ber-marker sysman: %s" % (len(dn), ack0, mk0))

# 3) census done-14hari ack=0 per tenant lintas fleet + marker
print("\ndone-14h ack=0 per tenant:")
tot = 0
per = {}
for r in con.cursor().execute("SELECT id, COALESCE(NULLIF(tenant,''),'(null)') ten FROM tasks WHERE status='done' AND completed_at > ?", (now-14*86400,)):
    ack = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["n"]
    if ack == 0:
        tot += 1
        mk = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (r["id"],)).fetchone()["n"]
        per.setdefault(r["ten"], [0, 0])
        per[r["ten"]][0] += 1
        if mk: per[r["ten"]][1] += 1
for k in sorted(per, key=lambda x: -per[x][0]):
    print("  %-20s ack0=%s marker=%s" % (k, per[k][0], per[k][1]))
print("TOTAL done-14h tanpa ACK:", tot)

# 4) umur komentar terakhir papan (bukan hanya event) + running global
cmx = con.cursor().execute("SELECT MAX(created_at) mx FROM task_comments").fetchone()["mx"]
emx = con.cursor().execute("SELECT MAX(created_at) mx FROM task_events").fetchone()["mx"]
run = con.cursor().execute("SELECT COUNT(*) n FROM tasks WHERE status='running'").fetchone()["n"]
print("\nkomentar terakhir %.0f mnt | event terakhir %.0f mnt | running global=%s" % ((now-cmx)/60, (now-emx)/60, run))

# 5) cek apakah 33 kartu wake ini pernah dilaporkan ronde lalu (marker stalled dilarang; cek jejak komentar sysman)
n_sysman = con.cursor().execute("SELECT COUNT(DISTINCT task_id) n FROM task_comments WHERE author IN ('sysmanager-cleaner','mission-wake','default') AND body LIKE '%RANTAI-WAKE%' AND created_at > ?", (now-24*3600,)).fetchone()["n"]
print("kartu dgn marker RANTAI-WAKE 24 jam terakhir:", n_sysman)
