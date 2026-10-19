# Full triage comments + blind-spot sweep (running cards w/ LAPOR-SELESAI & no ACK) - cron 14-10a
import sqlite3, time

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

print("### FULL COMMENTS t_6359bba5")
for r in cur.execute("SELECT author,created_at,body FROM task_comments WHERE task_id='t_6359bba5' ORDER BY created_at"):
    print(f"--- [{round((now-r['created_at'])/60)}m] {r['author']}:\n{r['body'][:1800]}\n")

print("### FULL COMMENTS t_bb725705 (last 2)")
rows = cur.execute("SELECT author,created_at,body FROM task_comments WHERE task_id='t_bb725705' ORDER BY created_at").fetchall()
for r in rows[-2:]:
    print(f"--- [{round((now-r['created_at'])/60)}m] {r['author']}:\n{r['body'][:1800]}\n")

print("### BLIND SPOT: running cards")
run = cur.execute("SELECT id,title,tenant,assignee,started_at FROM tasks WHERE status='running'").fetchall()
print("N_RUNNING:", len(run))
for c in run:
    lap = cur.execute("SELECT COUNT(*),MAX(created_at) FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR-SELESEI%')", (c['id'],)).fetchone()
    ack = cur.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (c['id'],)).fetchone()[0]
    hb = cur.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=? AND kind='heartbeat'", (c['id'],)).fetchone()[0]
    age_hb = round((now-hb)/60) if hb else None
    if lap[0] and ack == 0:
        print(f"!! {c['id']} [{c['tenant']}] {c['title'][:70]} LAPOR={lap[0]} ACK=0 hb_age={age_hb}m")
    else:
        print(f"   ok {c['id']} [{c['tenant']}] {c['title'][:60]} lap={lap[0]} ack={ack} hb={age_hb}m")

print("### BOARD SANITY")
tot = cur.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
ev_last = cur.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
cm_last = cur.execute("SELECT MAX(created_at) FROM task_comments").fetchone()[0]
print("tasks:", tot, "| last_event_min:", round((now-ev_last)/60), "| last_comment_min:", round((now-cm_last)/60))
con.close()
