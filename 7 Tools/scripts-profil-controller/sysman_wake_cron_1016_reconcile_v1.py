# Reconciliation ronde cron 16-10: kandidat longgar detail_v2 vs gerbang rute-4b kanonis
import sqlite3, time, os
DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
now = int(time.time())
IDS = ["t_ba9f0bf6","t_8998b559","t_8da71c9f","t_fb910478","t_887201e5","t_2da2d99f","t_26d8e0dc","t_841f18dc","t_e941b2ba"]
cc = con.cursor()
for tid in IDS:
    r = cc.execute("SELECT id,title,status,tenant,completed_at,created_by,assignee FROM tasks WHERE id=?", (tid,)).fetchone()
    if not r:
        print(tid, "NOT-FOUND"); continue
    comments = cc.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)).fetchall()
    lapor = [c for c in comments if "LAPOR-SELESAI" in c["body"] or "LAPOR SELESAI" in c["body"]]
    acks = [c for c in comments if "RANTAI-ACK" in c["body"]]
    markers = [c for c in comments if "RANTAI-WAKE" in c["body"]]
    lap_ts = lapor[-1]["created_at"] if lapor else 0
    lap_author = lapor[-1]["author"] if lapor else ""
    ack_lain_after = [c for c in acks if c["author"] != lap_author and c["created_at"] >= lap_ts] if lapor else []
    done_age_min = round((now - (r["completed_at"] or now))/60,1) if r["completed_at"] else None
    print(f"{tid} | {r['title'][:48]} | status={r['status']} tenant={r['tenant']!r} by={r['created_by']} assignee={r['assignee']}")
    print(f"   done_age={done_age_min}m lapor={len(lapor)}(author={lap_author},ts={lap_ts}) ack_total={len(acks)} ack_lain_after_lapor={len(ack_lain_after)} markers={[ (m['body'][:40], round((now-m['created_at'])/60)) for m in markers ]}")
# sensus tenant DKA dan SYNCNAS: kartu terbuka vs done tanpa ACK
for pat in ("DKA%","SYNCNAS%"):
    rows = cc.execute("SELECT id,status,title FROM tasks WHERE tenant LIKE ? ORDER BY created_at", (pat,)).fetchall()
    open_rows = [x for x in rows if x["status"] not in ("done","archived")]
    print(f"-- tenant {pat}: total={len(rows)} terbuka={len(open_rows)}")
    for x in open_rows[:10]:
        print("   OPEN:", x["id"], x["status"], x["title"][:60])
print("MAX event age:", round((now - cc.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0])/60,1), "min")
