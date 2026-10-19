#!/usr/bin/env python3
"""Ronde senyap 17-10b: saksi kesegaran scheduler + gateway + sensus blocked."""
import os, sqlite3, time, glob

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
DB = HOME + "/kanban.db"
now = time.time()

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

print("== umur event terbaru per tabel ==")
for tbl, col in (("task_events","created_at"),("task_comments","created_at"),("tasks","created_at"),("tasks","completed_at")):
    try:
        r = cur.execute(f"SELECT MAX({col}) m FROM {tbl}").fetchone()
        m = r["m"]
        print(f"  {tbl}.{col}: age_min = {round((now-(m or now))/60,1)}")
    except Exception as e:
        print(f"  {tbl}.{col}: ERR {e}")

print("-- sensus status --")
for r in cur.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(f"  {r['status']} = {r['n']}")

open_running = [dict(r) for r in cur.execute(
    "SELECT id,title,status FROM tasks WHERE status IN ('running','todo','in_progress')")]
print(f"-- kartu running/todo = {len(open_running)} --")
for r in open_running[:20]:
    print("   ", r["id"], r["status"], (r["title"] or "")[:60])

print("== sensus blocked: koreksi terakhir ==")
ids = [r["id"] for r in cur.execute("SELECT id FROM tasks WHERE status='blocked'")]
cleaned, uncleaned = 0, []
for tid in ids:
    row = cur.execute("SELECT id,status,title,tenant,created_at FROM tasks WHERE id=?", (tid,)).fetchone()
    cs = cur.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (tid,)).fetchall()
    last = cs[0]["body"] if cs else ""
    hit = ("[SYSMAN-CLEANER" in last) or ("RANTAI-WAKE" in last) or ("Digantikan" in last)
    # juga cek apakah ada koreksi SYSMAN-CLEANER kapan pun
    ever = cur.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%[SYSMAN-CLEANER%'", (tid,)).fetchone()["n"]
    if hit or ever:
        cleaned += 1
    else:
        uncleaned.append((tid, (row["title"] or "")[:70], round((now-(row["created_at"] or now))/60/60,1), last[:90].replace("\n"," ")))
print(f"  blocked total={len(ids)} sudah-berkoreksi={cleaned} TANPA-koreksi={len(uncleaned)}")
for u in uncleaned:
    print("   *", u[0], "|", u[1], "| umur_jam=", u[2], "| last:", u[3])

print("== saksi (a): mtime cron output ==")
for prof in ("gsp-system-manager","default"):
    base = f"{HOME}/profiles/{prof}/cron/output"
    if not os.path.isdir(base):
        print(f"  {prof}: TIDAK ADA"); continue
    dirs = sorted(glob.glob(base+"/*"), key=lambda p: os.path.getmtime(p))[-4:]
    for d in dirs:
        fs = sorted(glob.glob(d+"/*"), key=lambda p: os.path.getmtime(p))
        newest = fs[-1] if fs else None
        age = round((now-os.path.getmtime(newest))/60,1) if newest else None
        print(f"  {prof}/{os.path.basename(d)}: newest age_min={age}")

print("== saksi (b): heartbeat gateway ==")
hb_dirs = [(f"{HOME}/profiles", True), (HOME, False)]
seen = {}
for base, is_prof in hb_dirs:
    if not is_prof:
        p = f"{base}/state/gateway.heartbeat"
        if os.path.exists(p):
            seen["default"] = os.path.getmtime(p)
        continue
    for d in sorted(glob.glob(base+"/gsp-*")) + sorted(glob.glob(base+"/default")):
        p = d + "/state/gateway.heartbeat"
        if os.path.exists(p):
            seen[os.path.basename(d)] = os.path.getmtime(p)
fresh = [(k, round((now-v)/60,1)) for k,v in seen.items() if (now-v) < 300]
stale = sorted([(k, round((now-v)/60/60,1)) for k,v in seen.items() if (now-v) >= 300], key=lambda x:-x[1])
print(f"  fresh(<5m) = {len(fresh)} -> {sorted(k for k,_ in fresh)}")
print(f"  stale(>=5m, jam) = {len(stale)} -> {stale[:12]}")
con.close()
