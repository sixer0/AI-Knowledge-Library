# -*- coding: utf-8 -*-
"""Ronde sysman 16-10: nilai kartu terbuka (blocked/todo/review/running) vs ambang tagihan."""
import os, sqlite3, time, json, pathlib

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
REG = pathlib.Path('C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')
live = set(json.loads(REG.read_text(encoding='utf-8'))['hidup'])

con = sqlite3.connect(str(HOME / 'kanban.db'))
con.row_factory = sqlite3.Row

now = int(time.time())
rows = list(con.execute(
    "SELECT id,title,assignee,status,tenant,created_at,started_at,reason_placeholder FROM "
    "(SELECT id,title,assignee,status,tenant,created_at,started_at,NULL AS reason_placeholder "
    "FROM tasks WHERE status IN ('blocked','review','todo','running'))"))
print(f"KARTU TERBUKA: {len(rows)}")

tc = con.cursor()
out = []
for r in rows:
    tid = r['id']
    le = tc.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id=?", (tid,)).fetchone()['m'] or 0
    idle_h = (now - le) / 3600.0
    last_kind = tc.execute(
        "SELECT kind, created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1",
        (tid,)).fetchone()
    ncom = tc.execute("SELECT COUNT(*) c FROM task_comments WHERE task_id=?", (tid,)).fetchone()['c']
    lastcom = tc.execute(
        "SELECT author, substr(body,1,160) b, created_at FROM task_comments WHERE task_id=? ORDER BY created_at DESC LIMIT 1",
        (tid,)).fetchone()
    # komentar pembersih/tagihan sebelumnya
    tagih = tc.execute(
        "SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND (body LIKE '%ORPHAN-TAG%' OR author='board-cleaner' OR author='sysmanager-cleaner')",
        (tid,)).fetchone()['c']
    # needs_input / menunggu user?
    wait_user = tc.execute(
        "SELECT COUNT(*) c FROM task_comments WHERE task_id=? AND (body LIKE '%needs_input%' OR body LIKE '%keputusan user%' OR body LIKE '%MENUNGGU USER%' OR body LIKE '%HIL%')",
        (tid,)).fetchone()['c']
    lk = tc.execute("SELECT COUNT(*) c FROM task_links WHERE child_id=?", (tid,)).fetchone()['c']
    par = [p['parent_id'] for p in tc.execute("SELECT parent_id FROM task_links WHERE child_id=?", (tid,))]
    parstat = []
    for p in par:
        pr = tc.execute("SELECT id,status FROM tasks WHERE id=?", (p,)).fetchone()
        if pr:
            parstat.append(f"{pr['id'][:10]}:{pr['status']}")
    out.append(dict(id=tid, title=(r['title'] or '')[:70], assignee=r['assignee'], status=r['status'],
                    tenant=r['tenant'], idle_h=round(idle_h, 1),
                    last_ev=f"{last_kind['kind']}@{int((now-last_kind['created_at'])/60)}m" if last_kind else '-',
                    comments=ncom, tagihan_lama=tagih, wait_user=wait_user,
                    parents=parstat,
                    lastcom=f"{lastcom['author']}@{int((now-lastcom['created_at'])/3600)}j: {lastcom['b']}" if lastcom else ''))

out.sort(key=lambda d: -d['idle_h'])
for d in out:
    offreg = 'OFFREG' if (d['assignee'] and str(d['assignee']).startswith('gsp-') and d['assignee'] not in live) else ''
    print(f"\n{d['id']} [{d['status']}] idle={d['idle_h']}j asg={d['assignee']} {offreg} tenant={d['tenant']}")
    print(f"  judul: {d['title']}")
    print(f"  ev={d['last_ev']} com={d['comments']} tagihan_lama={d['tagihan_lama']} wait_user={d['wait_user']} parents={d['parents']}")
    if d['lastcom']:
        print(f"  kom_terakhir: {d['lastcom']}")

print("\n=== RINGKASAN KELAS ===")
c24 = [d for d in out if d['status'] in ('blocked', 'review', 'todo') and d['idle_h'] >= 24]
crun = [d for d in out if d['status'] == 'running' and d['idle_h'] >= 2]
coff = [d for d in out if d['assignee'] and str(d['assignee']).startswith('gsp-') and d['assignee'] not in live]
print(f"DIBIARKAN>=24JAM: {len(c24)} -> {[d['id'] for d in c24]}")
print(f"RUNNING-TANPA-HB>=2J: {len(crun)} -> {[d['id'] for d in crun]}")
print(f"ASSIGNEE-DI-LUAR-REGISTRI: {len(coff)} -> {[(d['id'], d['assignee']) for d in coff]}")
