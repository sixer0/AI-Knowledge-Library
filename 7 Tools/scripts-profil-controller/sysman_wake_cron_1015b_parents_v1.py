# sysman cron 15-10 ronde b (lanjutan): nilai 33 orang tua blocked VBCB — pola parent-tersingkir
import sqlite3, time, re

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row

def age(ts): return round((NOW-ts)/60.0) if ts else None

kids = [r["child_id"] for r in con.execute(
    "SELECT DISTINCT child_id FROM task_links WHERE child_id IN "
    "(SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo')").fetchall()]
parents = []
for k in kids:
    for r in con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (k,)).fetchall():
        p = con.execute("SELECT id,status,title FROM tasks WHERE id=?", (r["parent_id"],)).fetchone()
        if p and p["status"] == "blocked":
            parents.append((k, r["parent_id"]))

print("anak_todo=%s induk_blocked=%s" % (len(kids), len(parents)))
dig = 0; replaced_done = 0
sample_shown = 0
outcome_counts = {}
for kid, pid in parents:
    ev = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (pid,)).fetchone()
    cm = [dict(r) for r in con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (pid,))]
    d = None
    for c in cm:
        m = re.search(r"Digantikan\s+(t_[0-9a-f]{8})", c["body"] or "")
        if m: d = m.group(1)
    runs = [r["outcome"] for r in con.execute("SELECT outcome FROM task_runs WHERE task_id=?", (pid,)).fetchall()]
    for o in runs: outcome_counts[o] = outcome_counts.get(o, 0) + 1
    if d:
        dig += 1
        rep = con.execute("SELECT status FROM tasks WHERE id=?", (d,)).fetchone()
        if rep and rep["status"] == "done": replaced_done += 1
    if sample_shown < 3:
        sample_shown += 1
        print("\nSAMPLE induk %s status=blocked last_ev=%s age=%s runs=%s digantikan=%s" % (pid, ev["kind"] if ev else None, age(ev["created_at"]) if ev else None, runs, d))
        for c in cm[-3:]:
            print("   [%s @%smin] %s" % (c["author"], age(c["created_at"]), (c["body"] or "")[:180].replace("\n"," | ")))

print("\ninduk_dengan_marker_Digantikan=%s (pengganti done=%s)" % (dig, replaced_done))
print("outcome_runs_untuk_33_induk=%s" % outcome_counts)

# latar gave_up/timed_out seluruh tenant
rows = [dict(r) for r in con.execute(
    "SELECT ru.outcome o, COUNT(*) c FROM task_runs ru JOIN tasks t ON t.id=ru.task_id "
    "WHERE t.tenant='VIBE-BIBLE-1013' GROUP BY ru.outcome").fetchall()]
print("outcome_per_tenant=%s" % {r["o"]: r["c"] for r in rows})

# event tenant 24h terakhir (apakah masih ada aktivitas)
r = con.execute("SELECT MAX(e.created_at) m FROM task_events e JOIN tasks t ON t.id=e.task_id WHERE t.tenant='VIBE-BIBLE-1013'").fetchone()
print("tenant_last_event_age_min=%s" % age(r["m"]))

# kartu jangkar/blueprint tenant & status PARKED ekor tanpa ACK (konteks vonis tingkat-misi)
for r in con.execute("SELECT id,status,title,completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status NOT IN ('done','todo','blocked')").fetchall():
    print("nonstandard: %s %s %s" % (r["id"], r["status"], (r["title"] or "")[:60]))
