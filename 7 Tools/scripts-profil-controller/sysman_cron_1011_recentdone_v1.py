import sqlite3, os, time
db = os.path.join(os.environ.get("LOCALAPPDATA","C:/Users/TRIAL/AppData/Local"),"hermes","kanban.db")
con = sqlite3.connect(db); con.row_factory = sqlite3.Row
now = time.time()
# rute-4b buta-tutup: kartu done/blocked ber-tenant kosong dgn LAPOR-SELESAI tanpa ACK, selesai 24 jam terakhir
rows = con.execute("""SELECT id,title,status,tenant,assignee,created_by,completed_at FROM tasks
 WHERE status IN ('done','blocked') AND completed_at >= ? ORDER BY completed_at DESC""", (now-86400,)).fetchall()
print("recent_terminal_24h =", len(rows))
for r in rows:
    cid=r["id"]
    cmts = con.execute("SELECT author,body FROM task_comments WHERE task_id=? ORDER BY created_at",(cid,)).fetchall()
    lapor=[c for c in cmts if "LAPOR-SELESAI" in c["body"].upper() or "LAPOR SELESAI" in c["body"].upper()]
    ack=[c for c in cmts if "RANTAI-ACK" in c["body"].upper()]
    if lapor and not ack:
        print(f"SUSPECT {cid} | {r['title'][:60]} | tenant='{r['tenant']}' | status={r['status']} | LAPOR={len(lapor)} ACK={len(ack)}")
print("SWEEP_DONE suspects_above_only")
