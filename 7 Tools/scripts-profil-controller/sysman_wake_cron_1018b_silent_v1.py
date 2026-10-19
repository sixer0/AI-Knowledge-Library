# Ronde senyap 18-10b: replika scan() kanonis + penilaian 44 kartu blocked + cek t_841f18dc
import sqlite3, time, os, sys, importlib.util
from datetime import datetime

HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HOME, "kanban.db")
SCAN = os.path.join(HOME, "scripts", "gsp_mission_wake_scan.py")

now = int(time.time())

# 1) scan() kanonis — tangkap nilai kembali (list temuan), BUKAN stdout
spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
authors = None
try:
    authors = mod.DEFAULT_AUTHORS.split(",")
except Exception:
    authors = ["default", "sysmanager-cleaner", "mission-wake"]
findings = mod.scan(DB, now, authors)
print("SCAN findings =", len(findings))
for f in findings:
    print("  FINDING:", tuple(f))

# 2) sensus blocked + koreksi terakhir
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()
rows = cur.execute("""
  SELECT id, title, tenant, status, created_at, completed_at, assignee, created_by
  FROM tasks WHERE status='blocked' ORDER BY created_at DESC
""").fetchall()
print("BLOCKED total =", len(rows))
ids = [r["id"] for r in rows]
uncorrected = []
for r in rows:
    tid = r["id"]
    c2 = con.cursor()
    lastc = c2.execute(
        "SELECT author, body, created_at FROM task_comments WHERE task_id=? "
        "ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    laste = c2.execute(
        "SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    body = (lastc["body"] if lastc else "") or ""
    head = body[:80].replace("\n", " ")
    corrected = ("[SYSMAN-CLEANER" in body) or body.startswith("RANTAI-WAKE") or ("RANTAI-WAKE" in body[:40])
    ev_age = round((now - laste) / 60.0, 1) if laste else None
    flag = "OK" if corrected else "NILAI-LAIN"
    print(f"{tid} | {flag} | ev_age={ev_age}m | lastc({(lastc['author'] if lastc else '-')}) :: {head}")
    if not corrected:
        uncorrected.append((tid, r["title"], flag, ev_age))

print("UNCORRECTED count =", len(uncorrected))
for u in uncorrected:
    print("  UNC:", u[0], "|", (u[1] or "")[:60], "| last_event_age_min=", u[3])

# 3) cek khusus t_841f18dc (W7-GATECLOSE VBCB, butir SAH ronde 17-10)
r = con.execute("SELECT id,status,title,completed_at FROM tasks WHERE id LIKE 't_841f18dc%'").fetchone()
if r:
    print("W7GATE:", dict(r))
    c3 = con.cursor()
    evs = c3.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 5", (r["id"],)).fetchall()
    for e in evs:
        print("   ev:", e["kind"], round((now - e["created_at"]) / 60.0, 1), "min ago")
    cms = c3.execute("SELECT author, substr(body,1,70) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (r["id"],)).fetchall()
    for cm in cms:
        print("   cm:", cm["author"], "|", cm["b"].replace("\n", " "), "|", round((now - cm["created_at"]) / 60.0, 1), "min ago")

# 4) saksi kesegaran scheduler (mtime cron output)
import glob
for jobdir in glob.glob(os.path.join(HOME, "profiles/gsp-system-manager/cron/output/*")):
    files = glob.glob(os.path.join(jobdir, "*"))
    if files:
        newest = max(os.path.getmtime(f) for f in files)
        print("CRONJOB", os.path.basename(jobdir), "newest_age_min=", round((now - newest) / 60.0, 1))
con.close()
