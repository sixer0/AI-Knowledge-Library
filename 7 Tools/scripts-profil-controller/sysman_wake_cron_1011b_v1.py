"""Read-only cek pendukung cron mission-wake 11-10 (sysman):
1) umur event terminal papan (task_events) — anti DB basi
2) sensus 7 kartu blocked: judul, tenant, umur, author+body komentar terakhir
   (cek apakah 'DITAHAN controller' = keputusan tercatat atau butir nyata)
3) kartu done 24 jam terakhir tanpa RANTAI-ACK lintas author (kandidat senyap-done)
"""
import sqlite3, time, os, json

DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
now = time.time()
con = sqlite3.connect(DB)
con.row_factory = sqlite3.Row
cur = con.cursor()

print("DB =", DB)

# 1) umur event terakhir per kind
print("\n-- umur event terminal (menit) --")
try:
    for r in cur.execute("""SELECT kind, MAX(created_at) mx, COUNT(*) n FROM task_events
                            WHERE created_at > ? GROUP BY kind ORDER BY mx DESC LIMIT 12""",
                         (now - 7*86400,)):
        print(f"{r['kind']:<22} n={r['n']:<5} last_age_min={(now - r['mx'])/60:.1f}")
except Exception as e:
    print("ERR events:", e)

# 2) blocked census
print("\n-- kartu blocked --")
for r in cur.execute("SELECT id,title,tenant,assignee,created_at,block_kind,block_recurrences,last_heartbeat_at FROM tasks WHERE status='blocked' ORDER BY created_at DESC"):
    age_d = (now - r["created_at"])/86400
    print(f"\n[{r['id']}] {r['title'][:80]} | tenant={r['tenant']} | assignee={r['assignee']} | umur={age_d:.1f}hari | kind={r['block_kind']}x{r['block_recurrences']}")
    cs = list(cur.execute("SELECT author,body,created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (r["id"],)))
    for c in cs:
        print(f"   c({(now-c['created_at'])/3600:.1f}h) [{c['author']}]: {c['body'][:160].replace(chr(10),' / ')}")
    if not cs:
        print("   (tanpa komentar)")

# 3) done-24jam tanpa ACK (rekonsilasi; vonis kanonis tetap scan())
print("\n-- done 24 jam terakhir: LAPOR vs RANTAI-ACK --")
rows = list(cur.execute("""SELECT id,title,tenant,completed_at FROM tasks
    WHERE status='done' AND completed_at > ? ORDER BY completed_at DESC""", (now - 86400,)))
print(f"jumlah done-24j = {len(rows)}")
for r in rows:
    cs = list(cur.execute("SELECT author,body FROM task_comments WHERE task_id=? ORDER BY created_at ASC", (r["id"],)))
    lapor = [c for c in cs if "LAPOR" in c["body"].upper()]
    ack = [c for c in cs if "RANTAI-ACK" in c["body"]]
    if lapor and not ack:
        print(f"  TANPA-ACK [{r['id']}] {r['title'][:70]} tenant={r['tenant']} lapor_authors={[c['author'] for c in lapor][:3]}")
print("selesai")
