#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Read-only census papan untuk ronde tagihan orphan-cleaner 18-10 (sysman cron).

Cetak: sensus status, umur event terakhir papan (MAX), kandidat per kelas alat,
riwayat komentar tagihan/koreksi per kartu, heartbeat running, pasangan 'Digantikan'.
TIDAK menulis apa pun ke papan.
"""
import json, os, sqlite3, time, pathlib, collections

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
REG = pathlib.Path(r'C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')
DB = HOME / 'kanban.db'

live = set(json.loads(REG.read_text(encoding='utf-8'))['hidup'])
now = int(time.time())
con = sqlite3.connect(str(DB))
con.row_factory = sqlite3.Row

print(f"DB={DB} now={now} live_registry={len(live)}")

# --- sanity: papan hidup
r = con.execute("SELECT MAX(created_at) mx, COUNT(*) n FROM task_events").fetchone()
print(f"EVENTS total={r['n']} newest_age_min={(now - r['mx'])/60:.1f}")
for t in ('tasks', 'task_comments', 'task_runs'):
    try:
        print(f"  {t}: {con.execute(f'SELECT COUNT(*) c FROM {t}').fetchone()['c']} rows")
    except Exception as e:
        print(f"  {t}: ERR {e}")

print("\n=== SENSUS STATUS ===")
for row in con.execute("SELECT status, COUNT(*) n FROM tasks GROUP BY status ORDER BY n DESC"):
    print(f"  {row['status']:12s} {row['n']}")

OPEN = ('blocked', 'review', 'todo', 'running')
print("\n=== KANDIDAT TAGIHAN (predikat alat v1) ===")
rows = list(con.execute(
    "SELECT id,assignee,status,title,tenant,last_heartbeat_at,current_run_id,"
    "max_runtime_seconds,consecutive_failures,created_at FROM tasks "
    "WHERE status IN (?,?,?,?) ORDER BY status, created_at", OPEN))
cands = []
for t in rows:
    tid = t['id']
    le = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()['m'] or 0
    idle_h = (now - le) / 3600
    kind = None
    if t['status'] == 'running' and idle_h >= 2:
        kind = 'RUNNING-TANPA-HEARTBEAT'
    elif t['status'] in ('blocked', 'review', 'todo') and idle_h >= 24:
        kind = 'DIBIARKAN->=24JAM'
    elif t['assignee'] and t['assignee'].startswith('gsp-') and t['assignee'] not in live:
        kind = 'ASSIGNEE-DI-LUAR-REGISTRI'
    if not kind:
        continue
    recent = con.execute(
        "SELECT COUNT(*) c FROM task_events WHERE task_id=? AND kind='commented' AND created_at>?",
        (tid, now - 72000)).fetchone()['c']
    # riwayat komentar tagihan & koreksi
    hist = list(con.execute(
        "SELECT author, substr(body,1,60) b, created_at FROM task_comments WHERE task_id=? "
        "AND (body LIKE '%ORPHAN-TAG%' OR body LIKE '%SYSMAN-CLEANER%') ORDER BY created_at", (tid,)))
    tags = [h['created_at'] for h in hist if 'ORPHAN-TAG' in h['b']]
    corr = [h['created_at'] for h in hist if 'SYSMAN-CLEANER' in h['b']]
    # pasangan Digantikan
    dig = list(con.execute(
        "SELECT body FROM task_comments WHERE task_id=? AND body LIKE '%Digantikan%'", (tid,)))
    cands.append(dict(id=tid, kind=kind, status=t['status'], assignee=t['assignee'],
                      tenant=t['tenant'], title=(t['title'] or '')[:60], idle_h=idle_h,
                      spam_skip=bool(recent), n_tag=len(tags), last_tag=max(tags) if tags else 0,
                      n_corr=len(corr), last_corr=max(corr) if corr else 0,
                      dig=[d['body'][:80] for d in dig]))

for c in sorted(cands, key=lambda x: (x['kind'], -x['idle_h'])):
    print(f"\n[{c['kind']}] {c['id']} st={c['status']} asn={c['assignee']} tenant={c['tenant']} "
          f"idle={c['idle_h']:.0f}j skip_spam={c['spam_skip']} tag={c['n_tag']}"
          f"(last {(now-c['last_tag'])/3600:.0f}j lalu) koreksi={c['n_corr']}"
          f"(last {(now-c['last_corr'])/3600:.0f}j lalu)")
    print(f"    title: {c['title']}")
    for d in c['dig']:
        print(f"    dig: {d}")

print("\n=== RINGKASAN KANDIDAT ===")
cnt = collections.Counter((c['kind'], c['spam_skip']) for c in cands)
for (k, s), n in sorted(cnt.items()):
    print(f"  {k:28s} skip_spam={s} -> {n}")
print(f"  TOTAL kandidat={len(cands)} akan-ditagih={sum(1 for c in cands if not c['spam_skip'])}")

print("\n=== KARTU RUNNING (heartbeat) ===")
for t in rows:
    if t['status'] != 'running':
        continue
    le = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (t['id'],)).fetchone()['m'] or 0
    hb = t['last_heartbeat_at'] or 0
    try:
        hbn = float(hb)
        if hbn < 1e11:
            hbn *= 1000 if hbn > 1e10 else 1
    except Exception:
        hbn = 0
    laps = list(con.execute(
        "SELECT author, substr(body,1,40) b, created_at FROM task_comments WHERE task_id=? "
        "AND body LIKE '%LAPOR%' ORDER BY created_at DESC LIMIT 3", (t['id'],)))
    acks = con.execute(
        "SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'", (t['id'],)).fetchone()['c']
    print(f"  {t['id']} asn={t['assignee']} tenant={t['tenant']} ev_age={(now-le)/3600:.1f}j "
          f"hb={hb} run={t['current_run_id']} cap={t['max_runtime_seconds']} lap={len(laps)} ack={acks}")
    for l in laps:
        print(f"     lap[{l['author']}] {(now-l['created_at'])/3600:.1f}j: {l['b']}")
con.close()
