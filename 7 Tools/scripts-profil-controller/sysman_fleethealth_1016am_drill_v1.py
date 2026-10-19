#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Ronde pagi 16-10: drill-down cetakan gsp_fleet_health_report.py (read-only).

Ukur: (a) komposisi kartu blocked per tenant + reason, (b) run gagal 24j per kartu/misi,
(c) sensus ACK kartu done tenant utama, (d) kesegaran papan. Tidak menulis apa pun.
"""
import json, os, re, sqlite3, time, pathlib

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
DB = HOME / 'kanban.db'
now = int(time.time())
day = now - 86400

con = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
con.row_factory = sqlite3.Row
cur = con.cursor()

print('=== SANITY PAPAN HIDUP ===')
r = cur.execute("SELECT COUNT(*) n FROM tasks").fetchone()
print('tasks total :', r['n'])
r = cur.execute("SELECT MAX(created_at) m FROM task_events").fetchone()
print('event terakhir berumur (menit):', round((now - r['m']) / 60, 1) if r['m'] else 'NONE')

print()
print('=== KARTU BLOCKED: sensus per tenant ===')
rows = list(cur.execute("""
  SELECT COALESCE(NULLIF(tenant,''),'(null)') ten, COUNT(*) n
  FROM tasks WHERE status='blocked' GROUP BY 1 ORDER BY 2 DESC
""").fetchall())
for r in rows:
    print(f"{r['n']:4d}  {r['ten']}")

print()
print('=== KARTU BLOCKED: sensus reason (potong 90 char) ===')
rows = list(cur.execute("""
  SELECT substr(COALESCE(NULLIF(blocked_reason,''),'(tanpa reason)'),1,90) rea,
         COUNT(*) n, MIN(strftime('%s','now')-created_at)/60 min_age,
         MAX(strftime('%s','now')-created_at)/60 max_age
  FROM tasks WHERE status='blocked' GROUP BY 1 ORDER BY 2 DESC LIMIT 15
""").fetchall())
for r in rows:
    print(f"{r['n']:4d}  umur {int(r['min_age'])}..{int(r['max_age'])}m  {r['rea']}")

print()
print('=== KELAS parent-tersingkir: kartu blocked dgn pengganti done ===')
repl = re.compile(r'Digantikan\s+(t_[0-9a-f]{8})')
rows = list(cur.execute("SELECT id,title,body,status FROM tasks WHERE status='blocked'").fetchall())
tot = done_repl = alive_repl = norel = 0
for r in rows:
    blob = (r['body'] or '')
    m = repl.search(blob)
    if not m:
        # cek juga komentar
        c = con.cursor()
        cm = c.execute("SELECT body FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 5", (r['id'],)).fetchall()
        blob = ' '.join((x['body'] or '') for x in cm)
        m = repl.search(blob)
    if m:
        tot += 1
        st = cur.execute("SELECT status FROM tasks WHERE id=?", (m.group(1),)).fetchone()
        if st and st['status'] == 'done':
            done_repl += 1
        else:
            alive_repl += 1
    else:
        norel += 1
print(f'blocked total={len(rows)} | ber-pengganti={tot} (pengganti done={done_repl}, hidup={alive_repl}) | tanpa penanda ganti={norel}')

print()
print('=== RUN GAGAL 24 JAM: rinci per kartu ===')
rows = list(cur.execute("""
  SELECT r.outcome, t.id, t.status, substr(t.title,1,60) ttl, COALESCE(NULLIF(t.tenant,''),'(null)') ten,
         r.max_runtime_seconds cap, (r.ended_at-r.started_at) elapsed,
         datetime(r.ended_at,'unixepoch','localtime') ended
  FROM task_runs r JOIN tasks t ON t.id=r.task_id
  WHERE r.outcome IN ('timed_out','crashed','gave_up','blocked') AND r.ended_at>?
  ORDER BY r.ended_at DESC
""", (day,)).fetchall())
for r in rows:
    print(f"{r['outcome']:10s} {r['id']} {r['status']:8s} cap={r['cap']} el={r['elapsed']}s {r['ten']:22s} {r['ttl']}")

print()
print('=== TIMED_OUT: apakah loop masih jalan (retry_status) ===')
rows = list(cur.execute("""
  SELECT r.task_id, r.outcome, r.retry_status, datetime(r.ended_at,'unixepoch','localtime') ended,
         (SELECT COUNT(*) FROM task_runs x WHERE x.task_id=r.task_id) n_runs
  FROM task_runs r WHERE r.outcome IN ('timed_out','gave_up') AND r.ended_at>? ORDER BY r.ended_at DESC
""", (day,)).fetchall())
for r in rows:
    print(f"{r['task_id']} {r['outcome']:9s} retry={r['retry_status']} runs={r['n_runs']} ended={r['ended']}")

print()
print('=== SENSUS ACK kartu done tenant terbesar (serah-terima senyap?) ===')
top = rows and None
tops = list(cur.execute("""
  SELECT COALESCE(NULLIF(tenant,''),'(null)') ten, COUNT(*) n FROM tasks
  WHERE status='done' AND completed_at>? GROUP BY 1 ORDER BY 2 DESC LIMIT 6
""", (day,)).fetchall())
for t in tops:
    ids = [x['id'] for x in cur.execute(
        "SELECT id FROM tasks WHERE status='done' AND completed_at>? AND COALESCE(NULLIF(tenant,''),'(null)')=?",
        (day, t['ten'])).fetchall()]
    acked = 0
    for i in ids:
        c = con.cursor()
        if c.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (i,)).fetchone()['n']:
            acked += 1
    print(f"{t['ten']:24s} done-24j={len(ids):3d} ber-ACK={acked:3d} tanpa-ACK={len(ids)-acked:3d}")

print()
print('=== needs-review HQ: umur (via marker file dari alat utama tidak ada; lihat query node terpisah) ===')
