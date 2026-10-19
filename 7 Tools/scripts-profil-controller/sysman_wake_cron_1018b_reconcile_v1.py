# Rekonsiliasi 1018b: kenapa 4 kandidat done-unacked alat longgar TIDAK naik ke scan() kanonis
import sqlite3, time, importlib.util, os

SCRIPTS = r"C:/Users/TRIAL/AppData/Local/hermes/scripts"
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())

spec = importlib.util.spec_from_file_location("mws", os.path.join(SCRIPTS, "gsp_mission_wake_scan.py"))
mws = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mws)
for nm in ("DONE_UNACKED_MIN", "STALLED_MIN", "RUN_WINDOW_H", "FASE_STALL_MIN"):
    if hasattr(mws, nm):
        print(f"AMBANG {nm} =", getattr(mws, nm))
# cari konstanta cutoff rute-4b apa adanya
for nm in dir(mws):
    v = getattr(mws, nm)
    if isinstance(v, int) and 1700000000 < v < 2000000000:
        print(f"KONSTANTA_EPOCH {nm} = {v}")

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
ids = ["t_8358d01c", "t_d663f001", "t_63b993df", "t_491531fd"]
for tid in ids:
    r = con.cursor().execute(
        "SELECT id, status, tenant, completed_at, created_at FROM tasks WHERE id LIKE ?",
        (tid + "%",)).fetchone()
    if not r:
        print(tid, "TIDAK-DITEMUKAN")
        continue
    age_done_min = (now - r["completed_at"]) / 60.0 if r["completed_at"] else None
    print(f"{r['id'][:12]} status={r['status']} tenant={r['tenant']!r} "
          f"completed_age_min={round(age_done_min,1) if age_done_min is not None else 'None'}")

# status todo lintas waktu (cek definisi: mungkin ada yang berubah sejak alat longgar membaca)
c = con.cursor().execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status").fetchall()
print("CENSUS_STATUS:", {row["status"]: row["n"] for row in c})
con.close()
