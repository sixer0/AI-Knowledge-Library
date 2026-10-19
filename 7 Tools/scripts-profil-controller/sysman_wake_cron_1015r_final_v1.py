# Ronde cron 15-10r akhir: penulis ACK per kartu + cek ulang S6 + t_841f18dc + scan() ulang
import sqlite3, time, os, importlib.util, io, contextlib

WS = os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local") + "/hermes"
DB = WS + "/kanban.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
now = int(time.time())

def ack_authors(cid):
    return [(a["author"], round((now - a["created_at"]) / 60)) for a in
            con.execute("SELECT author, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY created_at", (cid,))]

def lap_authors(cid):
    return [a["author"] for a in con.execute("SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (cid,))]

print("== DECK-HTMLPDF-1015: author LAPOR vs ACK ==")
for cid in ("t_c5da3e33","t_4004a170","t_f6bae2e2","t_2da2d99f","t_4905bc7f"):
    print(f"  {cid} lap={set(lap_authors(cid))} ack={ack_authors(cid)}")

print("== DKA W1/W2a ACK ==")
for cid in ("t_384f1e6e","t_1740784b"):
    print(f"  {cid} lap={set(lap_authors(cid))} ack={ack_authors(cid)}")

print("== WEBLOC ES15 t_6fd3f361 ==")
c = con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id='t_6fd3f361' ORDER BY created_at").fetchall()
for x in c:
    print(f"  [{int((now-x['created_at'])/60)}m] {x['author']}: {x['body'][:200]}")

print("== t_841f18dc (VBCB W7 gate-close) ==")
r = con.execute("SELECT id,title,status,tenant,assignee,reason FROM tasks WHERE id='t_841f18dc'").fetchone()
print(f"  status={r['status']} tenant={r['tenant']} assignee={r['assignee']} reason={str(r['reason'])[:160]}")
for x in con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id='t_841f18dc' ORDER BY created_at DESC LIMIT 3"):
    print(f"  [{int((now-x['created_at'])/60)}m] {x['author']}: {x['body'][:200]}")

print("== S6 t_26d8e0dc terkini ==")
r = con.execute("SELECT status, last_heartbeat_at, completed_at FROM tasks WHERE id='t_26d8e0dc'").fetchone()
lap = con.execute("SELECT MAX(created_at) m FROM task_comments WHERE task_id='t_26d8e0dc' AND body LIKE '%LAPOR-SELESAI%'").fetchone()["m"]
ackn = len(list(con.execute("SELECT author,created_at FROM task_comments WHERE task_id='t_26d8e0dc' AND body LIKE '%RANTAI-ACK%' AND created_at>=?", (lap,))))
print("  status=%s hb_age=%.1fm lap_age=%.1fm ack_after_lap=%d" % (r["status"], (now-int(r["last_heartbeat_at"]))/60, (now-lap)/60, ackn))

# scan() kanonis ulang
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
