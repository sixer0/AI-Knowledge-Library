# Sweep: done-in-24h cards where a WORKER wrote LAPOR-SELESAI but NO RANTAI-ACK
# from another author exists, and no controller triage/damping comment covers it.
# lap detection excludes PARKED lines and controller 'atas LAPOR' quotes.
import sqlite3, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
con = sqlite3.connect(DB)
cur = con.cursor()
now = time.time()

dones = cur.execute(
    "SELECT id,title,tenant,completed_at,assignee FROM tasks "
    "WHERE status='done' AND completed_at >= ? ORDER BY completed_at",
    (now - 24*3600,),
).fetchall()

CONTROLLERISH = ("default", "gsp-master01", "gsp-master", "gsp-system-manager", "sysmanager-cleaner")

flagged = []
for tid, title, tenant, cat, assignee in dones:
    comments = cur.execute(
        "SELECT author, body, created_at FROM task_comments WHERE task_id=? ORDER BY created_at",
        (tid,)).fetchall()
    lap_workers = set()
    for a, b, ts in comments:
        if "LAPOR-SELESAI" in b and not b.lstrip().startswith("PARKED") and "atas LAPOR" not in b:
            if a not in CONTROLLERISH:
                lap_workers.add(a)
    ack_authors = set(a for a, b, ts in comments if "RANTAI-ACK" in b)
    ctrl_triage = any(("CATATAN CONTROLLER" in b or "redaman pemindai" in b or "VONIS CONTROLLER" in b or "TRIASE" in b)
                      for a, b, ts in comments)
    wake_marker = any("RANTAI-WAKE" in b for a, b, ts in comments)
    if lap_workers and not (ack_authors - lap_workers) :
        flagged.append((tid, title, tenant, assignee, sorted(lap_workers), sorted(ack_authors), ctrl_triage, wake_marker, (now-cat)/3600))

print(f"done_in_24h={len(dones)} worker-LAPOR-without-other-ACK={len(flagged)}")
for tid, title, tenant, assignee, lw, aa, triage, wm, age_h in flagged:
    print(f"{tid} tenant={tenant} assignee={assignee} lap={lw} ack={aa} ctrl_triage={triage} wake_marker={wm} done_age_h={age_h:.1f} | {title[:55]}")
con.close()
