# Ronde 17-10b: kenapa 10 done-noack lolos rute-4b + sensus tenant DKAB/V27
import importlib.util, sqlite3, time, os

HERMES = r"C:/Users/TRIAL/AppData/Local/hermes"
DB = os.path.join(HERMES, "kanban.db")
SCAN = os.path.join(HERMES, "scripts", "gsp_mission_wake_scan.py")
spec = importlib.util.spec_from_file_location("wake_scan", SCAN)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
now = time.time()

ids = ["t_6f9b7b1e","t_4352ee5a","t_c789eed1","t_9c02c6ed","t_0ae80997","t_bdfea029","t_c02f6244","t_e749792d","t_a8fdb9f6","t_ce103d8a"]
print("-- detail 10 kandidat --")
for tid in ids:
    t = con.execute("SELECT id,title,status,tenant,created_by,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    age_h = (now - t["completed_at"]) / 3600.0
    laps = con.execute("SELECT author, created_at, substr(body,1,40) b FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%' ORDER BY created_at", (tid,)).fetchall()
    acks = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["c"]
    print(f"{tid} tenant={t['tenant']!r} creator={t['created_by']} done_age_h={age_h:.1f} LAPOR={len(laps)} ACK={acks}")

# baca sumber rute-4b utk predikat persis
import inspect
src = inspect.getsource(mod)
i = src.find("4b")
print("\n-- cuplikan sumber rute-4b (sekitar token '4b') --")
print(src[max(0,i-1500):i+2500])
con.close()
