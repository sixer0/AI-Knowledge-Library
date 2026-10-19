"""Ronde wake 16-10: census kartu done terbaru per tenant + kenapa rute-4b diam."""
import os, sqlite3, time

DB = os.path.join(os.environ["LOCALAPPDATA"], "hermes", "kanban.db")
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
now = int(time.time())
cutoff = now - 24 * 3600

rows = list(con.execute(
    "SELECT id,tenant,status,completed_at,title FROM tasks "
    "WHERE status='done' AND completed_at>=? ORDER BY completed_at DESC", (cutoff,)))
print(f"done 24 jam terakhir: {len(rows)} kartu")

by_tenant = {}
for r in rows:
    t = r["tenant"] or "(NULL)"
    by_tenant.setdefault(t, []).append(r)

for t, cards in sorted(by_tenant.items(), key=lambda kv: -max(c["completed_at"] for c in kv[1])):
    newest = max(c["completed_at"] for c in cards)
    print(f"\n== tenant {t} | {len(cards)} kartu | done terakhir {(now-newest)/60:.0f} mnt lalu ==")
    for c in cards[:12]:
        lap = con.execute(
            "SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR SELESAI%' OR body LIKE '%STATUS: complete%')",
            (c["id"],)).fetchone()["n"]
        ack = con.execute(
            "SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",
            (c["id"],)).fetchone()["n"]
        mk = con.execute(
            "SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE%'",
            (c["id"],)).fetchone()["n"]
        age = (now - c["completed_at"]) / 60
        print(f"  {c['id']} age={age:6.1f}m lap={lap} ack={ack} marker={mk} | {c['title'][:60]}")

# open cards fleet-wide
open_cards = list(con.execute("SELECT id,status,title FROM tasks WHERE status NOT IN ('done','archived') AND status IS NOT NULL"))
print(f"\nkartu non-done/non-archived: {len(open_cards)}")
con.close()
