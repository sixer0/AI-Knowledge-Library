# sysman cron 15-10 ronde D: rekonsiliasi kontradiksi blindspot vs hitungan langsung
import sqlite3, time
DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
now = int(time.time())
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row
ids = ["t_153594d4","t_34bf2edc","t_46ff8be6","t_5831a79d","t_7391c81b","t_a48e52d1","t_a4b6791b","t_99418ea0","t_cb601d70","t_e04bca14","t_6359bba5"]
for tid in ids:
    t = con.execute("SELECT id,status,title,tenant,body FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t: print(f"{tid} TIDAK ADA"); continue
    ncom = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=?", (tid,)).fetchone()["c"]
    lap_c = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%'", (tid,)).fetchone()["c"]
    ack_c = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()["c"]
    mk_c  = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-WAKE done-unacked%'", (tid,)).fetchone()["c"]
    lap_body = 1 if "LAPOR" in (t["body"] or "") else 0
    ev = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
    print(f"{tid} status={t['status']} tenant={t['tenant']} com={ncom} lap_kom={lap_c} ack={ack_c} mark={mk_c} lap_di_body={lap_body} umur_ev={(now-ev)/60:.0f}m :: {(t['title'] or '')[:60]}")
# running global ulang
run = con.execute("SELECT COUNT(*) c FROM tasks WHERE status='running'").fetchone()["c"]
print("TOTAL RUNNING:", run)
con.close()
