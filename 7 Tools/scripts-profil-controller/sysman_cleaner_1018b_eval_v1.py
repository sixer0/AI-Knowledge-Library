#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Daftar lengkap tagihan ORPHAN-TAG ronde 18-10 + konteks penilaian per kartu (read-only)."""
import os, sqlite3, time, pathlib, re, collections

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
DB = HOME / 'kanban.db'
now = int(time.time())
con = sqlite3.connect(str(DB))
con.row_factory = sqlite3.Row

# tagihan yang mendarat <=3 jam terakhir
CUT = now - 3 * 3600
tags = list(con.execute(
    "SELECT task_id, body, created_at FROM task_comments "
    "WHERE body LIKE '%ORPHAN-TAG%' AND created_at>? ORDER BY created_at", (CUT,)))
print(f"TAGIHAN_RONDE_INI={len(tags)}")
ids = [t['task_id'] for t in tags]
kinds = {}
for t in tags:
    m = re.search(r'\[ORPHAN-TAG v1\] ([A-Z0-9\->]+):', t['body'])
    kinds[t['task_id']] = m.group(1) if m else '?'

by_kind = collections.Counter(kinds.values())
print("PER_KELAS:", dict(by_kind))

print("\n=== PENILAIAN PER KARTU ===")
for tid in ids:
    t = con.execute("SELECT id,assignee,status,title,tenant,created_at,completed_at,"
                    "last_heartbeat_at,current_run_id FROM tasks WHERE id=?", (tid,)).fetchone()
    if not t:
        print(f"\n{tid}: TIDAK ADA DI tasks")
        continue
    le = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()['m'] or 0
    # komentar non-tagihan terakhir
    lastc = con.execute(
        "SELECT author, substr(body,1,90) b, created_at FROM task_comments WHERE task_id=? "
        "AND body NOT LIKE '%ORPHAN-TAG%' ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    ncorr = con.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%SYSMAN-CLEANER%'",
                        (tid,)).fetchone()['c']
    dig = con.execute("SELECT substr(body,1,60) b FROM task_comments WHERE task_id=? AND body LIKE '%Digantikan t_%' "
                      "ORDER BY created_at DESC LIMIT 1", (tid,)).fetchone()
    partner_status = ''
    if dig:
        m = re.search(r'Digantikan (t_[0-9a-f]{8})', dig['b'])
        if m:
            p = con.execute("SELECT status FROM tasks WHERE id=?", (m.group(1),)).fetchone()
            partner_status = f"pasangan={m.group(1)}:{p['status'] if p else 'HILANG'}"
    # parents & status ortu
    par = list(con.execute(
        "SELECT tl.parent_id, p.status FROM task_links tl JOIN tasks p ON p.id=tl.parent_id "
        "WHERE tl.child_id=?", (tid,)))
    parstr = ",".join(f"{p['parent_id'][-6:]}:{p['status']}" for p in par) or '-'
    # anak & status anak
    ch = list(con.execute(
        "SELECT tl.child_id, c.status FROM task_links tl JOIN tasks c ON c.id=tl.child_id "
        "WHERE tl.parent_id=?", (tid,)))
    chstr = ",".join(f"{c['child_id'][-6:]}:{c['status']}" for c in ch) or '-'
    print(f"\n{kinds[tid]} {tid} st={t['status']} asn={t['assignee']} tenant={t['tenant']} "
          f"ev_age={(now-le)/3600:.1f}j koreksi_lama={ncorr} {partner_status}")
    print(f"  title: {(t['title'] or '')[:70]}")
    print(f"  ortu=[{parstr}] anak=[{chstr}]")
    if lastc:
        print(f"  komentar_terakhir[{lastc['author']}] {(now-lastc['created_at'])/3600:.1f}j: {lastc['b']}")
con.close()
