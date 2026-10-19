# -*- coding: utf-8 -*-
"""Ronde 15-10 cron: re-scan kanonis + blindspot lintas tenant + cakupan M4 VBCB."""
import sqlite3, time, importlib.util, sys

now = int(time.time())
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"

# 1) re-scan kanonis via import modul pemindai
spec = importlib.util.spec_from_file_location("wake_scan", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
fn = getattr(mod, "scan", None)
if fn:
    DEFAULT = getattr(mod, "DEFAULT_AUTHORS", "default")
    authors = DEFAULT.split(",") if isinstance(DEFAULT, str) else list(DEFAULT)
    print("RE-SCAN kanonis (authors=%s):" % authors)
    try:
        rows = fn(DB, int(now), authors)
        if not rows:
            print("  (kosong)")
        for r in rows:
            print("  ", r)
    except Exception as e:
        print("  ERROR scan():", e)
else:
    print("modul tanpa scan() — attributes:", [a for a in dir(mod) if not a.startswith("_")][:20])

# 2) blind spot: kartu running di SEMUA tenant, LAPOR vs ACK, umur heartbeat
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
print("\n=== BLINDSPOT running (semua tenant) ===")
run = con.cursor().execute("SELECT id,tenant,title,assignee,last_heartbeat_at FROM tasks WHERE status='running'").fetchall()
print("jumlah running:", len(run))
for r in run:
    hb = (now - (r["last_heartbeat_at"] or 0)) / 60.0
    lap = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (r["id"],)).fetchone()["n"]
    ack = con.cursor().execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["n"]
    ev = con.cursor().execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["mx"]
    print("  %s | tenant=%s | hb=%.0fm ev=%.0fm lap=%s ack=%s | %s" % (r["id"], r["tenant"] or "(null)", hb, (now - (ev or 0)) / 60, lap, ack, r["title"][:52]))

# 3) cakupan M4 VBCB: bab mana yang belum punya penulis done
print("\n=== CAKUPAN VBCB per bab (penulis EN) ===")
rows = con.cursor().execute("SELECT id,title,status FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND title LIKE '%Penulis bab%'").fetchall()
import re
from collections import defaultdict
bych = defaultdict(list)
for r in rows:
    m = re.search(r"bab (\d+)", r["title"])
    if m:
        bych[int(m.group(1))].append((r["status"], r["title"][:14]))
missing = []
for b in range(1, 38):
    lst = bych.get(b, [])
    st = set(s for s, _ in lst)
    ok = ("done" in st)
    if not ok:
        missing.append((b, sorted(st)))
print("bab 1..37: belum ada penulis done =", missing if missing else "TIDAK ADA (semua tercover)")
