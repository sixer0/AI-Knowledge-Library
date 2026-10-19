# -*- coding: utf-8 -*-
"""Cek blind spot read-only: kartu running dengan LAPOR-SELESAI tanpa ACK,
plus umur heartbeat dan bobot turunan terbuka. sysman cron mission-wake."""
import os
import sqlite3
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"),
                  "hermes", "kanban.db")
uri = "file:" + DB.replace("\\", "/") + "?mode=ro"
con = sqlite3.connect(uri, uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = time.time()

cols = [r[1] for r in con.execute("PRAGMA table_info(tasks)")]
print("task_cols:", ",".join(cols))
ccols = [r[1] for r in con.execute("PRAGMA table_info(task_comments)")]
print("comment_cols:", ",".join(ccols))

def ts_of(row, names):
    for n in names:
        if n in row.keys() and row[n] is not None:
            try:
                v = float(row[n])
            except (TypeError, ValueError):
                continue
            return v / 1000.0 if v > 1e12 else v
    return None

running = con.execute("SELECT * FROM tasks WHERE status='running'").fetchall()
print(f"-- running = {len(running)} --")
for t in running:
    tid = t["id"]
    title = (t["title"] if "title" in t.keys() else "")[:70]
    upd = ts_of(t, ("updated_at", "created_at"))
    print(f"\n[{tid}] {title}")
    if upd:
        print(f"  updated_age_min = {(now - upd)/60:.1f}")
    # komentar terbaru
    rows = con.execute(
        "SELECT * FROM task_comments WHERE task_id=? ORDER BY rowid DESC LIMIT 8",
        (tid,)).fetchall()
    lapor = ack = 0
    for c in rows:
        body = ""
        for cn in ("body", "comment", "text", "content"):
            if cn in c.keys() and c[cn]:
                body = str(c[cn])
                break
        cts = ts_of(c, ("created_at", "ts"))
        age = f"{(now - cts)/60:.0f}m" if cts else "?"
        marker = ""
        if "LAPOR-SELESAI" in body or "LAPOR SELESAI" in body or "LAPOR-SELESEI" in body:
            marker = " <LAPOR>"
        if "RANTAI-ACK" in body:
            marker = " <ACK>"
        author = c["author"] if "author" in c.keys() else (c["author_profile"] if "author_profile" in c.keys() else "?")
        print(f"  comment {age} by {author}{marker}: {body[:90].replace(chr(10),' ')}")
    nlapor = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR SELESAI%')", (tid,)).fetchone()[0]
    nack = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()[0]
    print(f"  totals: LAPOR={nlapor} ACK={nack}")
    # turunan terbuka transitif (walk task_links, kedalaman 3)
    open_desc = 0
    seen = set()
    frontier = [tid]
    for _ in range(3):
        nxt = []
        for p in frontier:
            for lk in con.execute("SELECT * FROM task_links WHERE parent_id=?", (p,)):
                child_cols = dict(lk).keys()
                cid = lk["child_id"] if "child_id" in child_cols else None
                if not cid or cid in seen:
                    continue
                seen.add(cid)
                st = con.execute("SELECT status FROM tasks WHERE id=?", (cid,)).fetchone()
                if st and st["status"] in ("todo", "running", "blocked"):
                    open_desc += 1
                nxt.append(cid)
        frontier = nxt
    print(f"  open_descendants(<=3lvl) = {open_desc}")
con.close()
