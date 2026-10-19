# -*- coding: utf-8 -*-
"""Sensus kartu hidup: umur blocked per assignee + kelas blocker gsp-worker + event papan terbaru."""
import sqlite3, os, time, json, pathlib
HOME = pathlib.Path(os.environ.get('LOCALAPPDATA','')) / 'hermes'
con = sqlite3.connect(HOME / 'kanban.db')
con.row_factory = sqlite3.Row
now = int(time.time())

print('== sanity: umur event papan terakhir (menit) ==')
r = con.execute("SELECT MAX(created_at) m FROM task_events").fetchone()
print('last_event_min =', round((now - r['m'])/60, 1))

print('== kartu hidup total ==')
tot = con.execute("SELECT COUNT(*) n FROM tasks WHERE status IN ('todo','running','blocked','review')").fetchone()['n']
print('open_total =', tot)

print('== gsp-worker blocked: umur + block_kind + sampel reason awal ==')
rows = con.execute("""SELECT id, title, block_kind, created_at, completed_at FROM tasks
  WHERE assignee='gsp-worker' AND status='blocked' ORDER BY created_at""").fetchall()
ages = [round((now-r['created_at'])/86400,1) for r in rows]
kinds = {}
for r in rows: kinds[r['block_kind']] = kinds.get(r['block_kind'],0)+1
print('n =', len(rows), '| umur_hari min/max =', (min(ages),max(ages)) if ages else '-', '| kinds =', kinds)
for r in rows[:6]:
    c = con.execute("SELECT body, author, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1",(r['id'],)).fetchone()
    last = (c['body'] or '').replace('\n',' ')[:90] if c else '(tanpa komentar)'
    print(f"  {r['id']} d{round((now-r['created_at'])/86400,1)} [{r['block_kind']}] {r['title'][:48]} || last: {last}")

print('== apakah sudah dikoreksi alat cleaner (token SYSMAN-CLEANER / Digantikan) ==')
fixed = 0
for r in rows:
    c = con.execute("SELECT COUNT(*) n FROM task_comments WHERE task_id=? AND (body LIKE '%[SYSMAN-CLEANER%' OR body LIKE 'Digantikan%')",(r['id'],)).fetchone()['n']
    if c: fixed += 1
print('worker_blocked_with_correction =', fixed, '/', len(rows))

print('== assignee lain blocked: umur + komentar terakhir ==')
for r in con.execute("""SELECT id, assignee, title, created_at FROM tasks
    WHERE status='blocked' AND assignee != 'gsp-worker' AND assignee IS NOT NULL ORDER BY created_at""").fetchall():
    c = con.execute("SELECT body FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1",(r['id'],)).fetchone()
    last=(c['body'] or '').replace('\n',' ')[:70] if c else '(nol komentar)'
    print(f"  {r['assignee']} | {r['id']} d{round((now-r['created_at'])/86400,1)} {r['title'][:44]} || {last}")

print('== running saat ini ==')
for r in con.execute("SELECT id, assignee, title, last_heartbeat_at FROM tasks WHERE status='running'").fetchall():
    hb = round((now-(r['last_heartbeat_at'] or 0))/60,1) if r['last_heartbeat_at'] else None
    print(f"  {r['id']} {r['assignee']} hb_min={hb} {r['title'][:50]}")
