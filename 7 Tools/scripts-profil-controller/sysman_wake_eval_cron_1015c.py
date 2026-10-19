# sysman cron 15-10 ronde C: sapuan blind-spot global (running LAPOR tanpa ACK) + re-scan kanonis
import sqlite3, time, importlib.util, sys, io, contextlib

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

# A) semua kartu running lintas papan: umur heartbeat + LAPOR + ACK
run = con.execute("SELECT id,title,status,tenant,assignee,last_heartbeat_at,started_at FROM tasks WHERE status='running'").fetchall()
print(f"RUNNING global: {len(run)}")
for r in run:
    hb = r["last_heartbeat_at"]
    lap = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (r["id"],)).fetchone()["c"]
    ack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["c"]
    age_hb = f"{(now-hb)/60:.0f}m" if hb else "-"
    print(f"  {r['id']} tenant={r['tenant']} hb={age_hb} lap={lap} ack={ack} :: {(r['title'] or '')[:70]}")

# B) blocked non-VBCB dengan LAPOR tanpa ACK (rute-4b bisa menangkap blocked)
oth = con.execute("""SELECT t.id,t.title,t.tenant FROM tasks t WHERE t.status IN ('blocked','done')
 AND (t.tenant IS NULL OR t.tenant != 'VIBE-BIBLE-1013')
 AND EXISTS(SELECT 1 FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%LAPOR%SELESAI%')
 AND NOT EXISTS(SELECT 1 FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-ACK%')
 AND NOT EXISTS(SELECT 1 FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-WAKE done-unacked%')""").fetchall()
print(f"\nLAPOR-tanpa-ACK-tanpa-marker NON-VBCB: {len(oth)}")
for r in oth:
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["m"]
    print(f"  {r['id']} tenant={r['tenant']} umur_ev={(now-ev)/60:.0f}m :: {(r['title'] or '')[:70]}")

# C) re-scan kanonis via import modul scan()
spec = importlib.util.spec_from_file_location("wake_scan", "C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
sys.argv = ["gsp_mission_wake_scan.py"]
buf = io.StringIO()
try:
    spec.loader.exec_module(mod)
    with contextlib.redirect_stdout(buf):
        if hasattr(mod, "scan"):
            import inspect
            sig = list(inspect.signature(mod.scan).parameters)
            print(f"\nscan() params: {sig}")
            da = getattr(mod, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
            auth = da.split(",") if isinstance(da, str) else list(da)
            mod.scan("C:/Users/TRIAL/AppData/Local/hermes/kanban.db", int(time.time()), auth)
        else:
            print("modul tidak punya scan() — nama fungsi lain:", [n for n in dir(mod) if callable(getattr(mod,n)) and not n.startswith('_')][:10])
except SystemExit:
    pass
out = buf.getvalue().strip()
print("RE-SCAN OUTPUT:")
print(out if out else "(kosong)")
con.close()
