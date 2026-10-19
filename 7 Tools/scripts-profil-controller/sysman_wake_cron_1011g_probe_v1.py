# Probe: for zero-ACK sample cards, check LAPOR-SELESAI presence, terminal event,
# prior RANTAI-WAKE markers, and canonical scan() verdict via importlib.
import sqlite3, time, importlib.util, sys, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
cur = con.cursor()
now = int(time.time())

SAMPLES = [
    # tenant=None [RO01-W] packs (no ACK at all)
    "t_10569fbe","t_11db1218","t_5b7a8dd5","t_c0f7e7c0","t_140e456c",
    "t_9bacb330","t_b23dbf7f","t_a4c8b843","t_478595eb","t_dbd77711",
    "t_9fbba251","t_8d3fe657","t_7ad776ea" if False else "t_7ad76fea","t_41fa6500",
    "t_ad2e8c0e","t_c08057c4",
    # other zero-ACK no-comment cards
    "t_ef405f62","t_aef19275","t_6e8a2e73","t_ac884544",
    # zero-ack but ACK by same author as LAPOR (self-handover check) - sample 3
    "t_d9b3f445","t_4a4395db","t_bcb209e6",
]

print("-- per-card probe --")
for tid in SAMPLES:
    row = cur.execute("SELECT title,status,tenant,completed_at,created_by,assignee FROM tasks WHERE id=?", (tid,)).fetchone()
    if not row:
        print(f"{tid} NOT FOUND"); continue
    title, status, tenant, cat, cb, assignee = row
    comments = cur.execute(
        "SELECT author, substr(body,1,60), created_at FROM task_comments WHERE task_id=? ORDER BY created_at",
        (tid,)).fetchall()
    lapor = [c for c in comments if "LAPOR-SELESAI" in c[1]]
    acks = [c for c in comments if "RANTAI-ACK" in c[1]]
    wake_markers = [c for c in comments if "RANTAI-WAKE" in c[1]]
    ev = cur.execute(
        "SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 3",
        (tid,)).fetchall()
    print(f"{tid} [{status}] tenant={tenant} by={cb} assignee={assignee} done_age_h={(now-cat)/3600:.1f}" if cat else f"{tid} [{status}]", "|", title[:45])
    print(f"   comments={len(comments)} lapor={len(lapor)} ack={len(acks)} wake_marker={len(wake_markers)} last_events={[(k, round((now-a)/60)) for k,a in ev]}")
    for a, b, ts in comments[-4:]:
        print(f"   cmt[{a}] {round((now-ts)/60)}m: {b}")

# canonical scan()
print("-- canonical scan() --")
spec = importlib.util.spec_from_file_location("wake_scan", r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_mission_wake_scan.py")
mod = importlib.util.module_from_spec(spec)
sys.argv = ["x"]
spec.loader.exec_module(mod)
authors = None
for nm in ("DEFAULT_AUTHORS","CONTROLLER_AUTHORS"):
    v = getattr(mod, nm, None)
    if v:
        authors = v.split(",") if isinstance(v, str) else list(v)
        break
res = mod.scan(DB, now, authors)
print("scan rows:", len(res))
for r in res[:20]:
    print(r)
con.close()
