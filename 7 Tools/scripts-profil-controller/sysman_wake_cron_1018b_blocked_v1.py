# Ronde cron 18-10b: nilai kartu blocked non-arsip + saksi kesegaran papan (MAX event)
import sqlite3, time, os

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

now = int(time.time())

# 1. sensus status terbuka
print("-- census status NOT IN (done,archived) --")
for r in cur.execute("SELECT status, COUNT(*) c FROM tasks WHERE status NOT IN ('done','archived') GROUP BY status ORDER BY c DESC"):
    print(f"{r['status']} = {r['c']}")

# 2. daftar kartu blocked + komentar terakhir
ids = [r["id"] for r in cur.execute("SELECT id FROM tasks WHERE status='blocked' ORDER BY id").fetchall()]
print(f"\n-- blocked cards: {len(ids)} --")
n_cleaner = 0
n_unmarked = 0
for tid in ids:
    row = cur.execute("SELECT id, title, tenant, created_by, created_at FROM tasks WHERE id=?", (tid,)).fetchone()
    c = con.cursor()
    last = c.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    allc = c.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND (body LIKE '%[SYSMAN-CLEANER%' OR body LIKE '%RANTAI-WAKE%')", (tid,)).fetchone()[0]
    lastprev = ((now - last["created_at"]) / 60.0) if last else -1
    tag = "MARKED" if allc > 0 else "UNMARKED"
    if allc > 0:
        n_cleaner += 1
    else:
        n_unmarked += 1
        print(f"UNMARKED {row['id']} | {(row['title'] or '')[:60]} | tenant={row['tenant']} | last_comment_age_min={lastprev:.0f} | last={(last['body'][:70].replace(chr(10),' ') if last else 'NONE')}")
print(f"\nblocked marked(cleaner/wake) = {n_cleaner}, unmarked = {n_unmarked}")

# 3. saksi kesegaran: MAX event & MAX komentar
for tbl, col in (("task_events", "created_at"), ("task_comments", "created_at")):
    mx = cur.execute(f"SELECT MAX({col}) FROM {tbl}").fetchone()[0]
    print(f"MAX {tbl}.{col} age_min = {(now - mx) / 60.0:.1f}")

# 4. kartu running dengan LAPOR tanpa ACK (blind spot rute-4b)
run = [r["id"] for r in cur.execute("SELECT id FROM tasks WHERE status='running'").fetchall()]
print(f"\n-- running cards = {len(run)} --")
for tid in run:
    c = con.cursor()
    lap = c.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESEI%'", (tid,)).fetchone()[0]
    ack = c.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()[0]
    hb = cur.execute("SELECT last_heartbeat_at FROM tasks WHERE id=?", (tid,)).fetchone()[0]
    print(f"{tid} lap={lap} ack={ack} hb_age_min={(now-hb)/60.0:.0f}" if hb else f"{tid} lap={lap} ack={ack} hb=NONE")
con.close()
