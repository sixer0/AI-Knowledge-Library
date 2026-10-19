# Ronde cron 15-10r: rekonsiliasi — scan() kanonis + census tenant DKA/DECK/WEBLOC + detail kandidat
import sqlite3, time, os, importlib.util, io, contextlib, json

WS = os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local") + "/hermes"
DB = WS + "/kanban.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
now = int(time.time())

# 1) scan() kanonis
spec = importlib.util.spec_from_file_location("wake_scan", WS + "/scripts/gsp_mission_wake_scan.py")
m = importlib.util.module_from_spec(spec)
buf = io.StringIO()
with contextlib.redirect_stdout(buf):
    spec.loader.exec_module(m)
fn = getattr(m, "scan", None)
if fn:
    try:
        da = getattr(m, "DEFAULT_AUTHORS", "default,sysmanager-cleaner,mission-wake")
        auth = da.split(",") if isinstance(da, str) else list(da)
        res = fn(DB, int(time.time()), auth)
        print("CANONICAL_SCAN_ROWS =", len(res) if res else 0)
        for r in (res or []):
            print("  SCAN:", tuple(r))
    except Exception as e:
        print("SCAN_ERR:", e)
else:
    print("no scan(); module stdout during exec:", buf.getvalue()[:200])

# 2) sensus per tenant untuk kartu done tanpa ACK lain-author
def tenant_of(tid):
    r = con.execute("SELECT tenant FROM tasks WHERE id=?", (tid,)).fetchone()
    return r["tenant"] if r else None

ids = ["t_8998b559","t_8da71c9f","t_fb910478","t_e941b2ba","t_887201e5","t_1740784b","t_384f1e6e","t_6fd3f361","t_96332f33","t_2d9cf424","t_2da2d99f"]
tenants = set()
for i in ids:
    tn = tenant_of(i)
    if tn: tenants.add(tn)
print("TENANTS_SEEN:", sorted(tenants))

for tn in sorted(tenants):
    rows = con.execute("SELECT id,title,status,completed_at FROM tasks WHERE tenant=? ORDER BY created_at", (tn,)).fetchall()
    open_c = [r for r in rows if r["status"] not in ("done","archived")]
    print(f"\n== TENANT {tn}: total={len(rows)} open={len(open_c)} ==")
    for r in rows:
        cid = r["id"]
        lap = con.execute("SELECT author, MAX(created_at) m FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (cid,)).fetchone()
        acks = con.execute("SELECT author, created_at FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY created_at", (cid,)).fetchall()
        mk = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (cid,)).fetchone()["c"]
        ack_other = sum(1 for a in acks if lap and a["author"] != lap["author"])
        age = f"{(now - r['completed_at'])/60:.0f}m" if r["completed_at"] else "-"
        print(f"  {cid} {r['status']:8s} done_age={age:>6s} lap={lap['author'] if lap and lap['m'] else 'NONE':22s} ack={len(acks)} ack_other={ack_other} wake_markers={mk} | {r['title'][:44]}")

# 3) status terkini t_26d8e0dc (ACK sudah mendarat?)
r = con.execute("SELECT status, last_heartbeat_at FROM tasks WHERE id='t_26d8e0dc'").fetchone()
lap = con.execute("SELECT MAX(created_at) m FROM task_comments WHERE task_id='t_26d8e0dc' AND body LIKE '%LAPOR-SELESAI%'").fetchone()["m"]
ack = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id='t_26d8e0dc' AND body LIKE '%RANTAI-ACK%' AND created_at>=?", (lap or 0,)).fetchone()["c"]
hb_age = (now - int(r["last_heartbeat_at"]))/60 if r["last_heartbeat_at"] else None
print(f"\nS6_NOW status={r['status']} hb_age_min={hb_age:.1f} ack_after_lap={ack}")
con.close()
