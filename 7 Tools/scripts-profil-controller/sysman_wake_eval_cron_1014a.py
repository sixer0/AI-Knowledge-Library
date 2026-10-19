# Read-only schema probe for kanban DB (mission-wake eval round 14-10 cron)
import sqlite3, json

DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

tables = [r[0] for r in cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")]
out = {"tables": tables}
for t in tables:
    cols = [r[1] for r in cur.execute(f"PRAGMA table_info({t})")]
    out[t] = cols
print(json.dumps(out, indent=1))
