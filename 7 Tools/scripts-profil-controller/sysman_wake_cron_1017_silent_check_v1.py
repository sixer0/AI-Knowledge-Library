# -*- coding: utf-8 -*-
# Ronde senyap 17-10: rekonsiliasi stdout kosong pemindai kanonis.
# (1) panggil scan() kanonis via importlib, tangkap NILAI KEMBALIAN (bukan stdout).
# (2) umur event terakhir papan (MAX, bukan MIN).
# (3) sensus kartu blocked: last_ev umur, ada komentar controller setelahnya,
#     marker RANTAI-WAKE, token koreksi [SYSMAN-CLEANER / Digantikan.
# (4) blind-spot rute-4b: event terminal completed/blocked <=6 jam tanpa syarat tenant.
import sqlite3, os, sys, time, importlib.util

HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
now = int(time.time())

spec = importlib.util.spec_from_file_location(
    "mws", os.path.join(HOME, "scripts", "gsp_mission_wake_scan.py"))
mws = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mws)
findings = mws.scan(DB, now, mws.DEFAULT_AUTHORS.split(","))
print("scan() temuan =", len(findings), findings if findings else "")

con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")

for tbl, col in (("task_events", "created_at"), ("task_comments", "created_at")):
    mx = con.execute("SELECT MAX(%s) m FROM %s" % (col, tbl)).fetchone()["m"]
    print("MAX %s.%s age_min = %.1f" % (tbl, col, (now - mx) / 60.0))

print("-- sensus blocked --")
ids = [r["id"] for r in con.execute(
    "SELECT id FROM tasks WHERE status='blocked' ORDER BY id")]
n_triased = n_marker = n_cleaner = n_bare = 0
bare = []
for tid in ids:
    last_ev = con.execute(
        "SELECT COALESCE(MAX(created_at),0) m FROM task_events WHERE task_id=?",
        (tid,)).fetchone()["m"]
    ctrl = con.execute(
        "SELECT 1 FROM task_comments c WHERE c.task_id=? AND c.author IN "
        "('default','sysmanager-cleaner','mission-wake') AND c.created_at>=? LIMIT 1",
        (tid, last_ev)).fetchone()
    mark = con.execute(
        "SELECT 1 FROM task_comments c WHERE c.task_id=? AND c.body LIKE '%RANTAI-WAKE %' "
        "AND c.created_at>=? LIMIT 1", (tid, last_ev)).fetchone()
    cleaner = con.execute(
        "SELECT 1 FROM task_comments c WHERE c.task_id=? AND "
        "(c.body LIKE '%[SYSMAN-CLEANER%' OR c.body LIKE '%Digantikan t_%') LIMIT 1",
        (tid,)).fetchone()
    if ctrl: n_triased += 1
    if mark: n_marker += 1
    if cleaner: n_cleaner += 1
    if not (ctrl or mark):
        n_bare += 1
        title = con.execute("SELECT title FROM tasks WHERE id=?", (tid,)).fetchone()["title"]
        bare.append((tid, title[:60], int((now-last_ev)/60)))
print("blocked total=%d ber-komentar-controller-setelah-event=%d ber-marker=%d ber-koreksi-cleaner/digantikan=%d TANPA-dua-duanya=%d"
      % (len(ids), n_triased, n_marker, n_cleaner, n_bare))
for b in bare:
    print("  BARE:", b)

print("-- blind spot rute-4b: event terminal <=6j (tanpa syarat tenant) --")
rows = con.execute(
    "SELECT e.task_id id, MAX(e.created_at) ts, t.status st, t.tenant ten "
    "FROM task_events e JOIN tasks t ON t.id=e.task_id "
    "WHERE e.kind IN ('completed','blocked') AND e.created_at >= ? "
    "GROUP BY e.task_id", (now - 6*3600,)).fetchall()
print("kandidat terminal 6j =", len(rows))
for r in rows:
    acks = [a["author"] for a in con.execute(
        "SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",
        (r["id"],)).fetchall()]
    lap = con.execute(
        "SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%' "
        "ORDER BY id DESC LIMIT 1", (r["id"],)).fetchone()
    lap_a = lap["author"] if lap else ""
    other_ack = any((a or "") != (lap_a or "~") for a in acks)
    print("  ", r["id"], r["st"], "tenant=", (r["ten"] or "-"),
          "ack_n=", len(acks), "ack_lain=", other_ack,
          "umur_mnt=", int((now-r["ts"])/60))
con.close()
