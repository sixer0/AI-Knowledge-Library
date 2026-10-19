# -*- coding: utf-8 -*-
# Ronde 15-10b verifikasi akhir: zero-ACK done (tanpa syarat marker), status 3 simpul LAPOR/PARKED, ACK baru mendarat?
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row
def age(ts): return round((NOW-ts)/60.0) if ts else None

print("== DONE VBCB zero-ACK (abaikan marker) ==")
rows = con.execute("SELECT id, title, completed_at FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='done'").fetchall()
z = []
for r in rows:
    ack = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchone()["n"]
    if ack == 0: z.append((r["id"], (r["title"] or "")[:45], age(r["completed_at"])))
print("done=", len(rows), "zero_ack=", len(z))
for x in z[:40]: print("  ", x)

print("\n== 3 SIMPUL LAPOR/PARKED: status & ACK terkini ==")
for tid in ["t_ad5d8e6f","t_99bb85a4","t_b10a1e32"]:
    t = con.execute("SELECT status FROM tasks WHERE id=?", (tid,)).fetchone()
    ack = con.execute("SELECT author, created_at, substr(body,1,60) b FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    ev = con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    print(tid, "status=", t["status"], "| last_ev=", ev["kind"], age(ev["created_at"]), "m | ack=", (ack["author"], age(ack["created_at"])) if ack else None)

print("\n== ACK mendarat 30 mnt terakhir (semua kartu) ==")
rows = con.execute("""SELECT task_id, author, created_at, substr(body,1,50) b FROM task_comments
 WHERE body LIKE '%RANTAI-ACK%' AND created_at > ? ORDER BY created_at DESC""", (NOW-1800,)).fetchall()
print("count=", len(rows))
for r in rows[:15]: print("  ", r["task_id"], r["author"], age(r["created_at"]), "m")
