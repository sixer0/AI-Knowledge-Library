# -*- coding: utf-8 -*-
# Sapuan akhir: kartu terbuka non-VBCB + tenant SYNCNAS + re-scan CLI dicatat terpisah.
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
def age(ts): return round((NOW-ts)/60.0) if ts else None

print("== KARTU TERBUKA (todo/blocked/running) NON-VBCB ==")
rows = con.execute("""SELECT id, status, COALESCE(tenant,'(null)') tn, substr(title,1,58) title
 FROM tasks WHERE status IN ('todo','blocked','running') AND (tenant IS NULL OR tenant != 'VIBE-BIBLE-1013')
 ORDER BY tn, status""").fetchall()
print("n=", len(rows))
for r in rows:
    ev = con.execute("SELECT MAX(created_at) mx FROM task_events WHERE task_id=?", (r["id"],)).fetchone()["mx"]
    print(" ", r["id"], r["status"], "|", r["tn"], "|", r["title"], "| ev_last:", age(ev), "m")

print("\n== TENANT VBCB: komposisi 33 blocked = hanya orang-tua lama? ==")
rows = con.execute("""SELECT substr(title,1,20) pref, COUNT(*) n FROM tasks
 WHERE tenant='VIBE-BIBLE-1013' AND status='blocked' GROUP BY pref""").fetchall()
for r in rows: print(" ", r["pref"], r["n"])
