# Map todo verif -> blocked parent -> M4 replacement; verify 1:1 — sysman cron 15-10 read-only
import sqlite3, time, re
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
def age(ts): return "%.0fm" % ((now-ts)/60) if ts else "-"

todos = con.execute("SELECT id,title FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo' ORDER BY title").fetchall()
print(f"todo verif cards: {len(todos)}")
ok = 0; bad = []
for r in todos:
    parents = con.execute("""SELECT l.parent_id, t.status, t.title FROM task_links l JOIN tasks t ON t.id=l.parent_id WHERE l.child_id=?""", (r["id"],)).fetchall()
    blocked_p = [p for p in parents if p["status"] == "blocked"]
    repl = None
    for p in blocked_p:
        c = con.execute("SELECT body FROM task_comments WHERE task_id=? AND body LIKE '%Digantikan%' ORDER BY created_at DESC LIMIT 1", (p["parent_id"],)).fetchone()
        if c:
            m = re.search(r"Digantikan (t_[0-9a-f]+)", c["body"])
            if m: repl = m.group(1)
    if repl:
        rt = con.execute("SELECT status FROM tasks WHERE id=?", (repl,)).fetchone()
        rs = rt["status"] if rt else "?"
    else:
        rs = "NO-REPL"
    # chapter match check
    ch_todo = re.search(r"bab (\d+)", r["title"])
    ch_repl = con.execute("SELECT title FROM tasks WHERE id=?", (repl,)).fetchone() if repl else None
    ch_repl_t = re.search(r"bab (\d+)", ch_repl["title"]) if ch_repl and ch_repl["title"] else None
    match = ch_todo and ch_repl_t and ch_todo.group(1) == ch_repl_t.group(1)
    if repl and rs in ("done","running") and match:
        ok += 1
    else:
        bad.append((r["id"], [p['parent_id'] for p in blocked_p], repl, rs))
print(f"MAPPED ok (replacement exists, done/running, chapter matches): {ok}/{len(todos)}")
for b in bad: print("  ANOMALY:", b)

# special: t_a37d190b (bab 33) — replacement running?
t = con.execute("SELECT status, last_heartbeat_at, started_at, max_runtime_seconds FROM tasks WHERE id='t_deb670d0'").fetchone()
print(f"\nbab33 repl t_deb670d0: status={t['status']} run_started={age(t['started_at'])} cap={t['max_runtime_seconds']}s hb={age(t['last_heartbeat_at'])}")
# elapsed of current run vs cap
run = con.execute("SELECT started_at FROM task_runs WHERE task_id='t_deb670d0' ORDER BY started_at DESC LIMIT 1").fetchone()
print(f"current run elapsed={age(run['started_at'])} vs cap {int(t['max_runtime_seconds']/60)}m")
