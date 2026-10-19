#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifikasi pasca-tempel ronde 18-10: hitung koreksi hari ini per kelas + cek ulang predikat alat."""
import os, sqlite3, time, pathlib

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
con = sqlite3.connect(str(HOME / 'kanban.db'))
con.row_factory = sqlite3.Row
now = int(time.time())

n = con.execute("SELECT COUNT(DISTINCT task_id) c FROM task_comments WHERE body LIKE '%[SYSMAN-CLEANER 18-10]%'").fetchone()['c']
print(f"kartu_berkoreksi_18-10={n}")

# re-cek predikat alat: semua kartu tertagih kini punya komentar <=20j -> skip_spam harus True semua
tagged = [r['task_id'] for r in con.execute(
    "SELECT DISTINCT task_id FROM task_comments WHERE body LIKE '%ORPHAN-TAG%' AND created_at>?", (now - 3*3600,))]
open_ids = [r['id'] for r in con.execute("SELECT id FROM tasks WHERE id IN (%s) AND status NOT IN ('done','archived')"
                                          % ",".join("?" * len(tagged)), tagged)]
skip = 0
noskip = []
for tid in tagged:
    recent = con.execute("SELECT COUNT(*) c FROM task_events WHERE task_id=? AND kind='commented' AND created_at>?",
                         (tid, now - 72000)).fetchone()['c']
    if recent:
        skip += 1
    else:
        noskip.append(tid)
print(f"tertagih={len(tagged)} masih_terbuka={len(open_ids)} terlindung_jendela_20j={skip} tanpa_perlindungan={noskip}")

# t_841f18dc keadaan terakhir
t = con.execute("SELECT status FROM tasks WHERE id='t_841f18dc'").fetchone()
le = con.execute("SELECT MAX(created_at) m FROM task_events WHERE task_id='t_841f18dc'").fetchone()['m']
print(f"t_841f18dc status={t['status']} umur_event_terakhir_j={(now-le)/3600:.1f}")
con.close()
