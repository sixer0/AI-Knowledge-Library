# Census tenant WEBLOC-PD-1015 (status per kartu + ACK terakhir) + re-scan kanonis akhir ronde.
import sqlite3, time, os, importlib.util, io, contextlib
DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
print("== tenant WEBLOC-PD-1015 ==")
rows = con.execute("SELECT id,title,status,completed_at FROM tasks WHERE tenant=? ORDER BY created_at", ("WEBLOC-PD-1015",)).fetchall()
for r in rows:
    ack = con.execute("SELECT COUNT(*) n, MAX(created_at) t FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()
    lap = con.execute("SELECT MAX(created_at) t FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()["t"]
    print(f"[{r['id']}] {r['status']:8} ack={ack['n']} ack_age={(now-ack['t'])/60:.0f}m lap_age={(now-lap)/60:.0f}m | {r['title'][:55]}")
con.close()

spec = importlib.util.spec_from_file_location("wake_scan", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
res = mod.scan(DB, now, ["default","sysmanager-cleaner","mission-wake"])
print("\n== FINAL RE-SCAN scan() ==")
print("temuan:", res if res else "KOSONG (0 baris)")
