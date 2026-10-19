# Sensus ulang done VBCB x ACK x marker (kursor terpisah; pitfall 14-10b).
import sqlite3, time
DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
now = int(time.time())
m = lambda s: round((now - s)/60.0, 1) if s else None
ids = [(r["id"], r["title"], r["completed_at"]) for r in con.cursor().execute(
    "SELECT id,title,completed_at FROM tasks WHERE tenant LIKE 'VIBE-BIBLE-1013%' AND status='done'")]
print("total done:", len(ids))
ack0m0 = []; ack0m1 = []; ackn = []
for tid, title, comp in ids:
    ac = con.cursor().execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["c"]
    mk = con.cursor().execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()["c"]
    (ackn if ac else (ack0m1 if mk else ack0m0)).append((tid, (title or "")[:52], m(comp), mk))
print(f"ber-ACK={len(ackn)} tanpa-ACK+marker={len(ack0m1)} tanpa-ACK+tanpa-marker={len(ack0m0)}")
print("\n-- TANPA ACK + TANPA MARKER (kandidat done-unacked) --")
for x in ack0m0: print("  ", x)
print("\n-- TANPA ACK + BERMARKER --")
for x in ack0m1: print("  ", x)
print("\n-- BER-ACK (contoh 8) --")
for x in ackn[:8]: print("  ", x)
