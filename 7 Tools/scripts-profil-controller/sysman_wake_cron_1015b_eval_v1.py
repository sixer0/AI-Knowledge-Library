# Read-only eval: 2 running cards (heartbeat, LAPOR/ACK, tenant) + why canonical
# scan skipped recent done-unacked candidates (marker presence per card).
import sqlite3, time, os
DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

RUNNING = ["t_ecd85ac8", "t_841f18dc"]
DONE_CANDS = ["t_febbc27c","t_a79d5897","t_18720708","t_ee1517ea","t_5318f783","t_5adc3df2",
              "t_b02ed4db","t_937692a6","t_3f4d4d81","t_b4d6303d","t_02f42f42","t_847af2bf",
              "t_d86dcc82","t_46a35ff9"]

print("== RUNNING cards ==")
for tid in RUNNING:
    r = con.execute("SELECT id,title,status,tenant,assignee,last_heartbeat_at,current_run_id,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    if not r:
        print(f"[{tid}] NOT FOUND"); continue
    hb = r["last_heartbeat_at"]
    hb_age = (now - hb)/60.0 if hb else None
    print(f"[{tid}] {r['title'][:60]} | status={r['status']} tenant={r['tenant']} assignee={r['assignee']} hb_age_min={hb_age if hb_age is None else round(hb_age,1)}")
    ev = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 5", (tid,)).fetchall()
    for e in ev:
        print(f"   ev {e['kind']} age={(now-e['created_at'])/60:.1f}m")
    cs = con.execute("SELECT author, substr(body,1,90) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 6", (tid,)).fetchall()
    for c in cs:
        print(f"   c {c['author']} {(now-c['created_at'])/60:.1f}m: {c['b']}")

print("\n== DONE candidates: marker + ack + tenant ==")
for tid in DONE_CANDS:
    r = con.execute("SELECT id,status,tenant,completed_at FROM tasks WHERE id=?", (tid,)).fetchone()
    if not r:
        print(f"[{tid}] NOT FOUND"); continue
    mk = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (tid,)).fetchone()["n"]
    mk_last = con.execute("SELECT MAX(created_at) t FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (tid,)).fetchone()["t"]
    lap = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%'", (tid,)).fetchone()["n"]
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["n"]
    comp_age = (now - r["completed_at"])/60.0 if r["completed_at"] else None
    print(f"[{tid}] status={r['status']} tenant={r['tenant']} done_age={comp_age and round(comp_age,1)}m LAPOR={lap} ACK={ack} markers={mk} marker_age={mk_last and round((now-mk_last)/60.0,1)}m")
con.close()
