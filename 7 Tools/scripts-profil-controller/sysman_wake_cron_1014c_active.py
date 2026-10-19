# -*- coding: utf-8 -*-
"""Ukur keadaan aktif VIBE-BIBLE-1013 + artefak (ronde 14-10 c)."""
import sqlite3, os, time, collections, glob
DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect("file:" + DB.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())

print("== sensus status task_runs tenant VIBE ==")
agg = collections.Counter()
for r in con.execute("SELECT ru.status,ru.outcome FROM task_runs ru JOIN tasks t ON t.id=ru.task_id WHERE t.tenant='VIBE-BIBLE-1013'"):
    agg[(r["status"], r["outcome"])] += 1
for k, v in agg.items():
    print("  ", k, v)

print("\n== RUN belum berakhir (ended_at NULL) ==")
rows = con.execute("""SELECT ru.task_id,ru.status,ru.profile,ru.started_at,ru.last_heartbeat_at
    FROM task_runs ru JOIN tasks t ON t.id=ru.task_id
    WHERE t.tenant='VIBE-BIBLE-1013' AND ru.ended_at IS NULL ORDER BY ru.started_at DESC""").fetchall()
print("open_runs=", len(rows))
for r in rows[:40]:
    print("  ", r["task_id"], r["status"], r["profile"], "started", int((now - r["started_at"]) / 60) if r["started_at"] else None,
          "m | hb", int((now - r["last_heartbeat_at"]) / 60) if r["last_heartbeat_at"] else None, "m")

print("\n== kartu tasks ber-current_run aktif ==")
rows = con.execute("""SELECT id,status,current_run_id,last_heartbeat_at,assignee FROM tasks
    WHERE tenant='VIBE-BIBLE-1013' AND current_run_id IS NOT NULL AND status NOT IN ('done','archived')""").fetchall()
for r in rows[:40]:
    hb = int((now - r["last_heartbeat_at"]) / 60) if r["last_heartbeat_at"] else None
    print("  ", r["id"], r["status"], r["assignee"], "run", r["current_run_id"], "hb", hb, "m")

print("\n== KARTU VBCB done/review ==")
for r in con.execute("SELECT id,title,status FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status NOT IN ('todo','blocked') ORDER BY status LIMIT 20"):
    print("  ", r["id"], r["status"], (r["title"] or "")[:60])

print("\n== ARTEFAK naskah VIBE ==")
hits = []
for root, dirs, files in os.walk("C:/Users/TRIAL/workspace/gsp-hermes/workspace"):
    dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "__pycache__")]
    up = root.upper()
    if "VIBE" in up or "BIBLE" in up:
        for f in files:
            hits.append(os.path.join(root, f))
print("files_in_vibe_dirs=", len(hits))
nonempty = [(p, os.path.getsize(p)) for p in hits if os.path.getsize(p) > 0]
print("nonempty=", len(nonempty))
for p, s in sorted(nonempty, key=lambda x: -x[1])[:15]:
    print("  ", s, p.replace("\\", "/"))

print("\n== SYNCNAS t_bb725705 ==")
for r in con.execute("SELECT author,substr(body,1,200) b,created_at FROM task_comments WHERE task_id='t_bb725705' ORDER BY id DESC LIMIT 5"):
    print("-", r["author"], int((now - r["created_at"]) / 60), "m |", r["b"].replace("\n", " | "))
r = con.execute("SELECT body,status,block_kind,assignee,created_by FROM tasks WHERE id='t_bb725705'").fetchone()
print("status:", r["status"], "| block_kind:", r["block_kind"], "| assignee:", r["assignee"], "| by:", r["created_by"])
print("body:", (r["body"] or "")[:400].replace("\n", " | "))
con.close()
