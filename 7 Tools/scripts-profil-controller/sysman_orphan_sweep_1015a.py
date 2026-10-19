#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sysman cron 15-10: read-only assessment papan orphan (pola gsp_board_orphan_cleaner.py)."""
import json, os, sqlite3, time, pathlib

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
REG = pathlib.Path(r'C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')

live = set(json.loads(REG.read_text(encoding='utf-8'))['hidup'])
con = sqlite3.connect(HOME / 'kanban.db')
con.row_factory = sqlite3.Row
now = int(time.time())

# sanity: board alive?
maxev = con.execute("SELECT MAX(created_at) FROM task_events").fetchone()[0]
ntasks = con.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
ncom = con.execute("SELECT COUNT(*) FROM task_comments").fetchone()[0]
print(f"SANITY max_event_age_min={(now-maxev)/60:.1f} tasks={ntasks} comments={ncom}")

print("COLS:", [r[1] for r in con.execute("PRAGMA table_info(tasks)")])

rows = list(con.execute(
    "SELECT id,assignee,status,title,tenant,created_at,completed_at FROM tasks "
    "WHERE status IN ('blocked','review','todo','running')"))
print(f"OPEN_CARDS={len(rows)}")

def kind_of(s, idle_h, a):
    if s == 'running' and idle_h >= 2:
        return 'RUNNING-TANPA-HEARTBEAT'
    if s in ('blocked','review','todo') and idle_h >= 24:
        return 'DIBIARKAN->=24JAM'
    if a and a.startswith('gsp-') and a not in live:
        return 'ASSIGNEE-DI-LUAR-REGISTRI'
    return None

cands = []
for r in rows:
    tid = r['id']
    cur2 = con.cursor()
    le = cur2.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (tid,)).fetchone()[0] or 0
    idle_h = (now - le) / 3600
    k = kind_of(r['status'], idle_h, r['assignee'])
    if not k:
        continue
    # recent cleaner/tag comments
    n_tag = cur2.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%ORPHAN-TAG%'", (tid,)).fetchone()[0]
    last_tag = cur2.execute("SELECT MAX(created_at) FROM task_comments WHERE task_id=? AND body LIKE '%ORPHAN-TAG%'", (tid,)).fetchone()[0]
    n_sys = cur2.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND (body LIKE '%sysmanager-cleaner%' OR author='sysmanager-cleaner')", (tid,)).fetchone()[0]
    n_lapor = cur2.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%LAPOR%SELESAI%'", (tid,)).fetchone()[0]
    n_acks = cur2.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (tid,)).fetchone()[0]
    parents = [x[0] for x in cur2.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,))]
    pstat = []
    for p in parents:
        pr = cur2.execute("SELECT status FROM tasks WHERE id=?", (p,)).fetchone()
        pstat.append(pr['status'] if pr else '?')
    nchild_open = cur2.execute(
        "SELECT COUNT(*) FROM task_links tl JOIN tasks t ON t.id=tl.parent_id WHERE tl.child_id=? AND t.status NOT IN ('done','cancelled')",
        (tid,)).fetchone()[0]
    # last 3 comments summary
    lastc = list(cur2.execute("SELECT author, substr(replace(body, char(10),' '),1,90) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 3", (tid,)))
    # last events kinds
    evs = [x[0] for x in cur2.execute("SELECT kind FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 4", (tid,))]
    cands.append(dict(id=tid, kind=k, status=r['status'], assignee=r['assignee'],
                      title=(r['title'] or '')[:60], tenant=r['tenant'], idle_h=round(idle_h,1),
                      n_tag=n_tag, last_tag_h=(round((now-last_tag)/3600,1) if last_tag else None),
                      n_sys=n_sys, n_lapor=n_lapor, n_ack=n_acks,
                      parents=pstat, open_children=nchild_open,
                      last_events=evs, last_comments=[(c['author'], c['b'], round((now-c['created_at'])/3600,1)) for c in lastc]))

print(f"CANDIDATES={len(cands)}")
for c in sorted(cands, key=lambda x: -x['idle_h']):
    print(json.dumps(c, ensure_ascii=False))
