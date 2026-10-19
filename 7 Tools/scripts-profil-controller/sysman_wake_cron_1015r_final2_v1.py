# Ronde cron 15-10r: t_841f18dc + S6 ulang + scan() final
import sqlite3, time, os, importlib.util, io, contextlib

WS = os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local") + "/hermes"
DB = WS + "/kanban.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
now = int(time.time())

print("== t_841f18dc (VBCB W7 gate-close) ==")
r = con.execute("SELECT id,title,status,tenant,assignee,block_kind FROM tasks WHERE id='t_841f18dc'").fetchone()
print("  status=%s tenant=%s assignee=%s block_kind=%s" % (r["status"], r["tenant"], r["assignee"], r["block_kind"]))
for x in con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id='t_841f18dc' ORDER BY created_at DESC LIMIT 3"):
    print("  [%dm] %s: %s" % (int((now-x["created_at"])/60), x["author"], x["body"][:220]))

print("== S6 t_26d8e0dc terkini ==")
r = con.execute("SELECT status, last_heartbeat_at FROM tasks WHERE id='t_26d8e0dc'").fetchone()
lap = con.execute("SELECT MAX(created_at) m FROM task_comments WHERE task_id='t_26d8e0dc' AND body LIKE '%LAPOR-SELESAI%'").fetchone()["m"]
ackn = len(list(con.execute("SELECT author FROM task_comments WHERE task_id='t_26d8e0dc' AND body LIKE '%RANTAI-ACK%' AND created_at>=?", (lap,))))
print("  status=%s hb_age=%.1fm lap_age=%.1fm ack_after_lap=%d" % (r["status"], (now-int(r["last_heartbeat_at"]))/60, (now-lap)/60, ackn))

spec = importlib.util.spec_from_file_location("wake_scan", WS + "/scripts/gsp_mission_wake_scan.py")
m = importlib.util.module_from_spec(spec)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    spec.loader.exec_module(m)
da = getattr(m, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
auth = da.split(",") if isinstance(da, str) else list(da)
res = m.scan(DB, int(time.time()), auth)
print("FINAL_SCAN_ROWS =", len(res) if res else 0)
for r in (res or []):
    print("  SCAN:", tuple(r))
con.close()
