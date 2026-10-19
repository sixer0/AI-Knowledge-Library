#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sysman cron 15-10c: vonis buta-tutup 4 kartu (read-only)."""
import os, sqlite3, time, pathlib

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
con = sqlite3.connect(HOME / 'kanban.db')
con.row_factory = sqlite3.Row
now = int(time.time())

for tid in ["t_c38a042f", "t_a3378d47", "t_bb725705", "t_6359bba5", "t_66b1a0b2"]:
    r = con.execute("SELECT id,title,status,assignee,tenant,block_kind,reason FROM tasks WHERE id=?", (tid,)).fetchone() if 'reason' in [x[1] for x in con.execute("PRAGMA table_info(tasks)")] else None
    r = con.execute("SELECT id,title,status,assignee,tenant,block_kind FROM tasks WHERE id=?", (tid,)).fetchone()
    print("=" * 90)
    print(f"CARD {tid} status={r['status']} assignee={r['assignee']} tenant={r['tenant']} block_kind={r['block_kind']}")
    print(f"TITLE: {(r['title'] or '')[:80]}")
    cs = list(con.execute("SELECT author, created_at, substr(replace(body, char(10),' '),1,160) b FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (tid,)))
    for c in reversed(cs):
        print(f"  [{time.strftime('%m-%d %H:%M', time.localtime(c['created_at']))}] {c['author']}: {c['b']}")
    evs = list(con.execute("SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 5", (tid,)))
    print("  EVENTS: " + ", ".join(f"{e['kind']}@{time.strftime('%m-%d %H:%M', time.localtime(e['created_at']))}" for e in evs))
