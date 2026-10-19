# Round 6: fresh run-state of t_4edfcf3a + exact stalled breakdown counts.
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row

def d(sql, args=()):
    cur = con.cursor()
    cur.execute(sql, args)
    return cur.fetchall()

print("RUNS t_4edfcf3a:")
for r in d("SELECT id, outcome, started_at, ended_at, max_runtime_seconds FROM task_runs WHERE task_id='t_4edfcf3a' ORDER BY started_at"):
    en = f"ended {round((now-r['ended_at'])/60)}m ago" if r["ended_at"] else "LIVE"
    print(f"  run#{r['id']} outcome={r['outcome']} started {round((now-r['started_at'])/60)}m ago, {en}")

t = d("SELECT status FROM tasks WHERE id='t_4edfcf3a'")[0]["status"]
print("card status now:", t)

# stalled 34 breakdown: how many have >=1 running parent vs all-parents-blocked
ids = ["t_edb280b5","t_5831a79d","t_e04bca14","t_a48e52d1","t_99418ea0","t_cb601d70","t_a4b6791b","t_153594d4","t_7391c81b","t_46ff8be6","t_34bf2edc","t_002af121","t_77a9bcd3","t_1c98456a","t_95b5b6cb","t_9ebc8fbc","t_799a1879","t_3782b61a","t_9e457da5","t_a064e4cc","t_d4fca8b3","t_23f7da05","t_1168e59f","t_9bf75422","t_60ed37fa","t_0311d1e4","t_efb6071f","t_2e0e92d4","t_14e7030f","t_a37d190b","t_0bf0854c","t_397be920","t_f9ac1ff2","t_c8784acc"]
run_par = 0; blk_par = 0
for tid in ids:
    ps = d("SELECT p.status FROM task_links l JOIN tasks p ON p.id=l.parent_id WHERE l.child_id=?", (tid,))
    if any(p["status"] == "running" for p in ps):
        run_par += 1
    else:
        blk_par += 1
print(f"stalled-todo total={len(ids)} with-running-parent={run_par} all-parents-blocked={blk_par}")
