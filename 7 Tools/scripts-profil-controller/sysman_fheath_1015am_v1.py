# -*- coding: utf-8 -*-
"""Sysman cron 15-10 pagi: traceroot cetakan gsp_fleet_health_report.py (read-only).
Ukur: distribusi timed_out/blocked 24j per tenant+assignee, gave_up, umur event terakhir
per tenant panas, kartu jangkar, census ACK done gelombang panas."""
import sqlite3, os, time, json, pathlib

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
DB = HOME / 'kanban.db'
con = sqlite3.connect(f'file:{DB}?mode=ro', uri=True)
cur = con.cursor()
now = int(time.time())
DAY = now - 86400

print('== DB:', DB, '| now', time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(now)))

# 1) sensus kind event 24 jam
cur.execute("SELECT kind, COUNT(*) FROM task_events WHERE created_at>=? GROUP BY kind ORDER BY 2 DESC", (DAY,))
print('\n[1] EVENT KINDS 24J:')
for k, n in cur.fetchall():
    print(f'  {k}: {n}')

# 2) timed_out per tenant (join tasks)
cur.execute("""
SELECT COALESCE(t.tenant,'(null)'), COUNT(*)
FROM task_events e LEFT JOIN tasks t ON t.id=e.task_id
WHERE e.kind='timed_out' AND e.created_at>=?
GROUP BY 1 ORDER BY 2 DESC LIMIT 15""", (DAY,))
print('\n[2] timed_out 24J per tenant:')
for r in cur.fetchall():
    print('  ', r)

# 3) gave_up total + 24j
cur.execute("SELECT COUNT(*) FROM task_events WHERE kind='gave_up'")
gu_all = cur.fetchone()[0]
cur.execute("SELECT COUNT(*) FROM task_events WHERE kind='gave_up' AND created_at>=?", (DAY,))
gu_24 = cur.fetchone()[0]
print(f'\n[3] gave_up total={gu_all} | 24j={gu_24}')

# 4) event blocked 24j per tenant
cur.execute("""
SELECT COALESCE(t.tenant,'(null)'), COUNT(*)
FROM task_events e LEFT JOIN tasks t ON t.id=e.task_id
WHERE e.kind='blocked' AND e.created_at>=?
GROUP BY 1 ORDER BY 2 DESC LIMIT 10""", (DAY,))
print('\n[4] event blocked 24J per tenant:')
for r in cur.fetchall():
    print('  ', r)

# 5) kartu hidup per assignee: breakdown per tenant
cur.execute("""
SELECT COALESCE(t.tenant,'(null)'), t.assignee, t.status, COUNT(*)
FROM tasks t WHERE t.status IN ('todo','blocked','running','in_review','needs-review')
GROUP BY 1,2,3 ORDER BY 4 DESC LIMIT 25""",)
print('\n[5] kartu hidup tenant x assignee x status:')
for r in cur.fetchall():
    print('  ', r)

# 6) umur event terakhir per tenant panas (top timed_out + top blocked)
tenants = set()
cur.execute("SELECT COALESCE(t.tenant,'(null)'), COUNT(*) FROM task_events e LEFT JOIN tasks t ON t.id=e.task_id WHERE e.kind IN ('timed_out','gave_up') AND e.created_at>=? GROUP BY 1 ORDER BY 2 DESC LIMIT 5", (DAY,))
hot = [r[0] for r in cur.fetchall()]
print('\n[6] umur event terakhir per tenant panas:', hot)
for tn in hot:
    if tn == '(null)':
        continue
    cur.execute("""
SELECT MIN(e.created_at), MAX(e.created_at), COUNT(*),
       SUM(CASE WHEN t.status='running' THEN 1 ELSE 0 END)
FROM tasks t JOIN task_events e ON e.task_id=t.id
WHERE t.tenant=?""", (tn,))
    mn, mx, c, run = cur.fetchone()
    if mx:
        print(f'  {tn}: last-event {int((now-mx)/60)} mnt lalu | running-now={run}')

# 7) sensus ACK done 24j (serah-terima senyap?)
cur.execute("""
SELECT COUNT(DISTINCT t.id) FROM tasks t WHERE t.status='done' AND t.completed_at>=?""", (DAY,))
done24 = cur.fetchone()[0]
cur.execute("""
SELECT COUNT(*) FROM (
  SELECT t.id FROM tasks t WHERE t.status='done' AND t.completed_at>=?
  AND NOT EXISTS (SELECT 1 FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-ACK%')
)""", (DAY,))
done24_noack = cur.fetchone()[0]
print(f'\n[7] done 24j={done24} tanpa-ACK={done24_noack}')

# 8) papan sanity: MAX event age
cur.execute("SELECT MAX(created_at) FROM task_events")
mx = cur.fetchone()[0]
print(f'[8] sanity: event papan terakhir berumur {int((now-mx)/60)} mnt (MAX, bukan MIN)')
con.close()
