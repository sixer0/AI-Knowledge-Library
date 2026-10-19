# -*- coding: utf-8 -*-
"""Distribusi waktu timed_out (pra/pasca merge 10-10), heartbeat kartu running, profil disk vs registry."""
import sqlite3, os, pathlib, json, time, datetime

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA',''))/'hermes'
WS = pathlib.Path(r'C:/Users/TRIAL/workspace/gsp-hermes/workspace')
con = sqlite3.connect(HOME/'kanban.db'); cur = con.cursor()
day = int(time.time())-86400

print("== A) timed_out per jam (24j terakhir) ==")
for r in cur.execute("SELECT profile,strftime('%d-%m %H',ended_at,'unixepoch','localtime'),COUNT(*) FROM task_runs WHERE outcome='timed_out' AND ended_at>? GROUP BY 1,2 ORDER BY 2", (day,)):
    print("  ", r)

print("== B) run terbaru 24j pada profil yang SUDAH DIARSIPKAN ==")
arch = pathlib.Path(r'C:/Users/TRIAL/gsp-archive/hermes-profiles-2026-10-10')
archived = set(p.name for p in arch.iterdir() if p.is_dir()) if arch.exists() else set()
print("   jumlah profil terarsipkan:", len(archived))
live = set(json.loads((WS/'fleet'/'PROFILE-REGISTRY.json').read_text(encoding='utf-8'))['hidup'])
rows = list(cur.execute("SELECT profile,COUNT(*),max(datetime(ended_at,'unixepoch','localtime')) FROM task_runs WHERE ended_at>? GROUP BY 1 ORDER BY 2 DESC", (day,)))
for prof, n, last in rows:
    tag = 'ARSIP' if prof in archived else ('LIVE' if prof in live else 'di-luar-registry')
    print(f"   {tag:16} {prof:26} n={n:3} last={last}")

print("== C) kartu running: heartbeat ==")
now = time.time()
for r in cur.execute("SELECT id,substr(title,1,50),assignee,last_heartbeat_at,current_run_id FROM tasks WHERE status='running'"):
    hb = r[3] or 0
    print(f"   {r[0]} hb_umur={(now-hb)/3600:.1f}h run={r[4]} {r[2]} | {r[1]}")

print("== D) run aktif saat ini (task_runs status running) ==")
try:
    for r in cur.execute("SELECT id,profile,datetime(started_at,'unixepoch','localtime') FROM task_runs WHERE status='running' ORDER BY started_at DESC LIMIT 15"):
        print("  ", r)
except Exception as e:
    print("   err:", e)
con.close()
