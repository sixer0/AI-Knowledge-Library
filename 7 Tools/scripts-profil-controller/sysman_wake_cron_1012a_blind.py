# Sapuan blind akhir 12-10: LAPOR 6 jam terakhir lintas status/tenant vs ACK, lalu re-scan kanonis
import sqlite3, time, subprocess, sys

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB); cur = con.cursor()

print("== LAPOR dalam 6 jam terakhir (lintas status & tenant) ==")
rows = cur.execute("""
  SELECT c.task_id, t.status, t.tenant, c.author, c.created_at, substr(t.title,1,60)
  FROM task_comments c JOIN tasks t ON t.id=c.task_id
  WHERE c.created_at >= ? AND upper(c.body) LIKE '%LAPOR%'
  ORDER BY c.created_at DESC
""", (now - 6*3600,)).fetchall()
if not rows:
    print("  (kosong - tidak ada laporan pekerja 6 jam terakhir)")
for tid, st, tenant, author, ts, title in rows:
    coms = cur.execute("SELECT author, body FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)).fetchall()
    lap_authors = {a for a,b in coms if "LAPOR" in b.upper()}
    acks = [a for a,b in coms if "RANTAI-ACK" in b.upper()]
    ack_lain = [a for a in acks if a not in lap_authors]
    mark = sum(1 for a,b in coms if "RANTAI-WAKE" in b.upper())
    flag = "NYATA?" if (not ack_lain and st in ("done","blocked","parked")) else "ok"
    print(f"  {tid} status={st} tenant={tenant!r} lap_author={sorted(lap_authors)} ack_lain={len(ack_lain)} marker={mark} vonis_awal={flag} | {title}")

print("== kartu berstatus bukan done/archived (terbuka) ==")
open_rows = cur.execute("SELECT id,status,tenant,title FROM tasks WHERE status NOT IN ('done','archived') ORDER BY status").fetchall()
for tid, st, tenant, title in open_rows:
    print(f"  {tid} {st} tenant={tenant!r} | {title[:60]}")
con.close()

print("== RE-SCAN KANONIS (CLI) ==")
r = subprocess.run([
    "C:/Users/TRIAL/AppData/Local/hermes/bin/uv","run","--python","3.11","--no-project",
    "python","C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py"],
    capture_output=True, text=True)
print("rc=", r.returncode, "stdout_len=", len(r.stdout.strip()))
print(r.stdout.strip() or "(kosong)")
