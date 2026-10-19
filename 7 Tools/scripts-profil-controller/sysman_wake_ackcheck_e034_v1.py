# Cek ACK per simpul ber-LAPOR-SELESAI + status akhir simpul orang tua
import sqlite3, time, os
DB = os.path.join(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
now = time.time()
for i in ["t_4bb6e4ef","t_20c6706f","t_7bee8b1e","t_bcb209e6"]:
    r = con.execute("SELECT id,status,completed_at,last_heartbeat_at FROM tasks WHERE id=?", (i,)).fetchone()
    cs = con.execute("SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at", (i,)).fetchall()
    lapor = [c for c in cs if "LAPOR-SELESAI" in (c["body"] or "")]
    ack = [c for c in cs if "RANTAI-ACK" in (c["body"] or "")]
    park = [c for c in cs if (c["body"] or "").startswith("PARKED")]
    print(i, "| status:", r["status"],
          "| hb_min:", round((now-r["last_heartbeat_at"])/60,1) if r["last_heartbeat_at"] else None,
          "| LAPOR:", len(lapor), "terakhir", round((now-lapor[-1]["created_at"])/60,1) if lapor else None,
          "| ACK:", len(ack), [a["author"] for a in ack],
          "| PARKED:", len(park))
con.close()
