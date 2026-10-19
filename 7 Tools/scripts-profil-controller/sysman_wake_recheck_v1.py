#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Re-check butiran blind-spot: status terkini, bobot turunan terbuka, ACK mendarat? (read-only)."""
import os, sqlite3, time

db = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
con = sqlite3.connect("file:" + db.replace("\\", "/") + "?mode=ro", uri=True)
con.row_factory = sqlite3.Row
con.execute("PRAGMA query_only = ON")
now = int(time.time())

for tid in ("t_40ba3fee", "t_b4a49859"):
    t = con.execute("SELECT id,status,title FROM tasks WHERE id=?", (tid,)).fetchone()
    print("=" * 60)
    print(tid, "|", t["status"], "|", t["title"][:70])
    lap = con.execute("SELECT created_at, author, body FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR-SELESAI%' ORDER BY created_at", (tid,)).fetchall()
    for c in lap:
        print("  LAPOR @%d mnt oleh %s :: %s" % (int((now - c["created_at"]) // 60), c["author"], c["body"][:400].replace("\n", " | ")))
    acks = con.execute("SELECT created_at, author, substr(body,1,80) b FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' ORDER BY created_at DESC LIMIT 3", (tid,)).fetchall()
    print("  ACKs:", [(int((now - a["created_at"]) // 60), a["author"]) for a in acks] or "(none)")
    lastev = con.execute("SELECT MAX(created_at) ts FROM task_events WHERE task_id=?", (tid,)).fetchone()["ts"]
    print("  last_event_age_min:", int((now - lastev) // 60))
    # transitif open descendants via task_links
    links = con.execute("SELECT * FROM task_links LIMIT 0").keys()
    print("  link_cols:", list(links))
    parents = con.execute("SELECT * FROM task_links WHERE child_id=? OR parent_id=? LIMIT 10", (tid, tid)).fetchall() if "child_id" in list(links) else []
    for p in parents:
        print("   link:", dict(p))
