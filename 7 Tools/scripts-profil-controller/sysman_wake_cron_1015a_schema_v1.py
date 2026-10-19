# Read-only: schema + board sanity for mission-wake round 15-10 (cron sysman)
import sqlite3, time, json

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
cur = con.cursor()

for t in ("tasks", "task_events", "task_comments", "task_links"):
    cols = [r[1] for r in cur.execute(f"PRAGMA table_info({t})").fetchall()]
    n = cur.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
    print(f"SCHEMA {t} cols={cols} rows={n}")

# Board sanity: MAX not MIN (MIN = oldest ever, false alarm)
mx = cur.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
now = int(time.time())
print(f"SANITY last_event_age_min={round((now-mx)/60,1)} now={now} last_event={mx}")

# Status census overall
print("CENSUS status:", cur.execute("SELECT status, COUNT(*) FROM tasks GROUP BY status").fetchall())

# Distinct tenants among the 33 wake ids
ids = ["t_002af121","t_0311d1e4","t_0bf0854c","t_1168e59f","t_14e7030f","t_153594d4","t_1c98456a","t_23f7da05","t_2e0e92d4","t_34bf2edc","t_3782b61a","t_397be920","t_46ff8be6","t_5831a79d","t_60ed37fa","t_7391c81b","t_77a9bcd3","t_799a1879","t_95b5b6cb","t_99418ea0","t_9bf75422","t_9e457da5","t_9ebc8fbc","t_a064e4cc","t_a37d190b","t_a48e52d1","t_a4b6791b","t_c8784acc","t_cb601d70","t_d4fca8b3","t_e04bca14","t_efb6071f","t_f9ac1ff2"]
ph = ",".join("?"*len(ids))
rows = cur.execute(f"SELECT tenant, COUNT(*) FROM tasks WHERE id IN ({ph}) GROUP BY tenant", ids).fetchall()
print("WAKE tenants:", rows)
missing = [i for i in ids if i not in {r[0] for r in cur.execute(f"SELECT id FROM tasks WHERE id IN ({ph})", ids).fetchall()}]
print("WAKE ids not found in tasks:", missing)
con.close()
