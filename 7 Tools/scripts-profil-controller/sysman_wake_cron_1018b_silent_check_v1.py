# Ronde senyap 18-10b: rekonsiliasi scan() kanonis + census todo + saksi scheduler hidup
import importlib.util, sqlite3, time, os, glob, sys

SCRIPTS = r"C:/Users/TRIAL/AppData/Local/hermes/scripts"
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"

# 1) scan() kanonis — tangkap nilai kembali (bukan stdout)
spec = importlib.util.spec_from_file_location("mws", os.path.join(SCRIPTS, "gsp_mission_wake_scan.py"))
mws = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mws)
authors = mws.DEFAULT_AUTHORS.split(",") if isinstance(mws.DEFAULT_AUTHORS, str) else list(mws.DEFAULT_AUTHORS)
findings = mws.scan(DB, int(time.time()), authors)
print("SCAN_FINDINGS =", len(findings))
for f in findings:
    print("  FIND:", tuple(f))

now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

# 2) census todo: id, judul, umur event terakhir, orang tua + statusnya
cur = con.cursor()
rows = cur.execute("SELECT id, title, status, tenant, created_at FROM tasks WHERE status='todo' ORDER BY created_at DESC").fetchall()
print("TODO_COUNT =", len(rows))
for r in rows:
    c2 = con.cursor()
    ev = c2.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    age = round((now - ev) / 60.0, 1) if ev else None
    par = con.cursor().execute(
        "SELECT p.id, p.status FROM task_links l JOIN tasks p ON p.id=l.parent_id WHERE l.child_id=?",
        (r["id"],)).fetchall()
    pars = "; ".join(f"{p['id'][:8]}:{p['status']}" for p in par) or "TIDAK-BERORANG-TUA"
    print(f"  TODO {r['id'][:12]} age_ev={age}m parents=[{pars}] | {r['title'][:52]}")

# 3) saksi scheduler hidup: mtime berkas cron output sysman terbaru
out = r"C:/Users/TRIAL/AppData/Local/hermes/profiles/gsp-system-manager/cron/output"
files = []
for d in glob.glob(os.path.join(out, "*")):
    for f in glob.glob(os.path.join(d, "*")):
        try:
            files.append((os.path.getmtime(f), f))
        except OSError:
            pass
files.sort(reverse=True)
print("SCHEDULER_WITNESS (cron output terbaru):")
for mt, f in files[:4]:
    print(f"  age_min={round((time.time()-mt)/60.0,1)} :: {os.path.basename(os.path.dirname(f))}/{os.path.basename(f)}")

# 4) umur event papan terakhir (MAX, bukan MIN)
ev = con.cursor().execute("SELECT MAX(created_at) m FROM task_events").fetchone()["m"]
cm = con.cursor().execute("SELECT MAX(created_at) m FROM task_comments").fetchone()["m"]
print("LAST_EVENT_age_min =", round((now - ev) / 60.0, 1))
print("LAST_COMMENT_age_min =", round((now - cm) / 60.0, 1))
con.close()
