# -*- coding: utf-8 -*-
"""Ronde wake 18-10b: sanity papan hidup + rekonsiliasi scan() saat stdout kosong.
Read-only. Peta kolom teruji: task_comments (bukan comments), task_events.created_at,
tasks tanpa updated_at, task_links(parent_id, child_id), MAX bukan MIN utk umur event."""
import os, sys, time, sqlite3, importlib.util

HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
SCAN = os.path.join(HOME, "scripts", "gsp_mission_wake_scan.py")

now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

print("== SENSUS STATUS ==")
for r in con.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(f"  {r['status']:12s} {r['n']}")

ev = con.execute("SELECT MAX(created_at) m, COUNT(*) n FROM task_events").fetchone()
age_min = (now - ev["m"]) / 60.0 if ev["m"] else -1
print(f"== EVENT TERAKHIR: umur {age_min:.1f} menit; total events={ev['n']}")
cm = con.execute("SELECT MAX(created_at) m, COUNT(*) n FROM task_comments").fetchone()
print(f"== KOMENTAR TERAKHIR: umur {(now-cm['m'])/60.0:.1f} menit; total comments={cm['n']}")
tk = con.execute("SELECT COUNT(*) n FROM tasks").fetchone()["n"]
print(f"== TOTAL TASKS: {tk}")

print("== KARTU RUNNING (blind-spot rute-4b) ==")
run = con.execute("SELECT id, title, tenant, last_heartbeat_at, current_run_id FROM tasks WHERE status='running'").fetchall()
if not run:
    print("  (nol kartu running)")
for r in run:
    hb = r["last_heartbeat_at"]
    hb_age = (now - hb) / 60.0 if hb else -1
    laps = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()["n"]
    acks = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["n"]
    print(f"  {r['id']} | {r['title'][:50]} | tenant={r['tenant']} | hb={hb_age:.0f}mnt | LAPOR={laps} ACK={acks}")

print("== KARTU TODO TERBUKA (turunan potensial) ==")
todo = con.execute("SELECT COUNT(*) n FROM tasks WHERE status='todo'").fetchone()["n"]
print(f"  todo={todo}")

print("== NON-DONE RINGKAS PER TENANT (top 10) ==")
for r in con.execute("""SELECT tenant, COUNT(*) n FROM tasks
                        WHERE status NOT IN ('done','archived') AND tenant IS NOT NULL AND tenant != ''
                        GROUP BY tenant ORDER BY n DESC LIMIT 10"""):
    print(f"  {r['tenant']:30s} {r['n']}")

print("== REKONSILIASI scan() KANONIS ==")
spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
authors = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
if isinstance(authors, str):
    authors = authors.split(",")
rows = mod.scan(DB, now, authors)
print(f"  scan() -> {len(rows)} temuan")
for row in rows:
    print(f"  ROW: {tuple(row)}")
con.close()
