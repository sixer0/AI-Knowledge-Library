# Read-only targeted comment/event probe for specific card ids (cron mission-wake eval).
# Pattern per skill gsp-system-manager-ops: DB = kanban.db at hermes ROOT, not boards/gsp/.
import sqlite3, time, sys, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
ids = ["t_f4de0f1f", "t_52521c3b"]

con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
cur = con.cursor()
now = time.time()

for tid in ids:
    print("=" * 70)
    row = cur.execute(
        "SELECT id,title,status,assignee,last_heartbeat_at,completed_at,current_run_id FROM tasks WHERE id=?",
        (tid,),
    ).fetchone()
    if not row:
        print(tid, "NOT FOUND")
        continue
    print(f"[{row[0]}] status={row[2]} assignee={row[3]} hb_age_min={(now-(row[4] or 0))/60:.1f} completed_at={row[5]}")
    print("title:", row[1][:110])
    print("-- last 8 comments --")
    for c in cur.execute(
        "SELECT author,substr(body,1,300),created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 8",
        (tid,),
    ):
        print(f"  age={(now-c[2])/60:.1f}m by {c[0]}: {c[1].replace(chr(10),' | ')[:280]}")
    print("-- last 6 events --")
    try:
        for e in cur.execute(
            "SELECT kind,detail,created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 6",
            (tid,),
        ):
            print(f"  age={(now-e[2])/60:.1f}m kind={e[0]} detail={str(e[1])[:120]}")
    except sqlite3.OperationalError as ex:
        print("  events query err:", ex)
con.close()
