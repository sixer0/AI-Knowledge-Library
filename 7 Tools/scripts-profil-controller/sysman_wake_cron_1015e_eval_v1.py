# Ronde wake 15-10-e: evaluasi 33 baris stalled seragam (~483 mnt) dari DB read-only.
import sqlite3, time, json

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
IDS = """t_002af121 t_0311d1e4 t_0bf0854c t_1168e59f t_14e7030f t_153594d4 t_1c98456a
t_23f7da05 t_2e0e92d4 t_34bf2edc t_3782b61a t_397be920 t_46ff8be6 t_5831a79d t_60ed37fa
t_7391c81b t_77a9bcd3 t_799a1879 t_95b5b6cb t_99418ea0 t_9bf75422 t_9e457da5 t_9ebc8fbc
t_a064e4cc t_a37d190b t_a48e52d1 t_a4b6791b t_c8784acc t_cb601d70 t_d4fca8b3 t_e04bca14
t_efb6071f t_f9ac1ff2""".split()

con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

now = int(time.time())

# sanity papan hidup: MAX event age
r = cur.execute("SELECT MAX(created_at) m, COUNT(*) n FROM task_events").fetchone()
print("SANITY events: max_age_min=%.1f total=%d" % ((now - r["m"]) / 60.0, r["n"]))
r = cur.execute("SELECT COUNT(*) n FROM tasks").fetchone()
print("SANITY tasks:", r["n"])

# schema guard
cols = [x["name"] for x in cur.execute("PRAGMA table_info(tasks)")]
print("TASK_COLS:", ",".join(cols))

def kids(pid):
    c2 = con.cursor()
    return [x["child_id"] for x in c2.execute("SELECT child_id FROM task_links WHERE parent_id=?", (pid,))]

def parents(cid):
    c2 = con.cursor()
    return [x["parent_id"] for x in c2.execute("SELECT parent_id FROM task_links WHERE child_id=?", (cid,))]

tenants = {}
for tid in IDS:
    t = cur.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print("MISSING", tid)
        continue
    c2 = con.cursor()
    ev = c2.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (tid,)).fetchall()
    c3 = con.cursor()
    ncom = c3.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=?", (tid,)).fetchone()["n"]
    c4 = con.cursor()
    laps = c4.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (tid,)).fetchone()["n"]
    c5 = con.cursor()
    acks = c5.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["n"]
    c6 = con.cursor()
    mark = c6.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'", (tid,)).fetchone()["n"]
    c7 = con.cursor()
    lastcom = c7.execute("SELECT author, substr(body,1,120) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    ps = parents(tid)
    pstat = []
    if ps:
        c8 = con.cursor()
        for p in ps:
            pr = c8.execute("SELECT status FROM tasks WHERE id=?", (p,)).fetchone()
            pstat.append((p, pr["status"] if pr else "?"))
    ks = kids(tid)
    n_open = 0
    if ks:
        c9 = con.cursor()
        for k in ks:
            kr = c9.execute("SELECT status FROM tasks WHERE id=?", (k,)).fetchone()
            if kr and kr["status"] in ("todo", "blocked", "running"):
                n_open += 1
    tenants[t["tenant"] or "(null)"] = tenants.get(t["tenant"] or "(null)", 0) + 1
    print(json.dumps({
        "id": tid, "status": t["status"], "tenant": t["tenant"],
        "title": (t["title"] or "")[:80],
        "last_ev": [(e["kind"], round((now - e["created_at"]) / 60.0)) for e in ev],
        "comments": ncom, "lapor": laps, "ack": acks, "marker": mark,
        "parents": pstat, "kids_open": n_open,
        "last_com": (lastcom["author"], round((now - lastcom["created_at"]) / 60.0), lastcom["b"]) if lastcom else None,
    }, ensure_ascii=False))

print("TENANTS_IN_WAKE:", json.dumps(tenants, ensure_ascii=False))
