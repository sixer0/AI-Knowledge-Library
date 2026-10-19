# Cron mission-wake sysman: konfirmasi liveness papan saat stdout kosong
# (umur event terbaru lintas task_events/comments + census kartu terbuka + blocked note)
import sqlite3, os, time, json

DB = os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", "kanban.db")
if not os.path.exists(DB):
    alt = os.path.expanduser("~/AppData/Local/hermes/kanban.db")
    DB = alt
con = sqlite3.connect(DB)
cur = con.cursor()
now = time.time()

def age(minute=True):
    return lambda t: round((now - t) / 60.0, 1)

for tbl, col in (("task_events", "created_at"), ("task_comments", "created_at"), ("tasks", "created_at")):
    try:
        row = cur.execute(f"SELECT MAX({col}) FROM {tbl}").fetchone()[0]
        print(f"{tbl}: max={row} age_min={age()(row) if row else 'NONE'}")
    except Exception as e:
        print(f"{tbl}: ERR {e}")

print("-- open statuses --")
for st, n in cur.execute("SELECT status, COUNT(*) FROM tasks WHERE status NOT IN ('done','archived') GROUP BY status"):
    print(f"{st} = {n}")

print("-- blocked cards --")
for tid, title, upd in cur.execute(
    "SELECT id, title, created_at FROM tasks WHERE status='blocked' ORDER BY created_at DESC"
):
    last_ev = cur.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (tid,)).fetchone()[0]
    last_note = cur.execute(
        "SELECT substr(replace(body, char(10), ' '),1,110), author, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1",
        (tid,),
    ).fetchone()
    print(f"{tid} | {title[:60]} | ev_age_min={age()(last_ev) if last_ev else '-'} | last: {age()(last_note[2]) if last_note else '-'}m by {last_note[1] if last_note else '-'} :: {(last_note[0] if last_note else '(no comment)')[:100]}")

# running cards (blind spot): harus kosong saat papan diam
run = cur.execute("SELECT id, title FROM tasks WHERE status IN ('running','in_progress')").fetchall()
print(f"-- running/in_progress = {len(run)} --")
for tid, title in run:
    print(f"RUN {tid} {title[:60]}")
con.close()
