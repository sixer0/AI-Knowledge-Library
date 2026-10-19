#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""GSP Board Orphan Cleaner v1 (PROF-MERGE-1010). Harian, no_agent, diam-saat-sehat.

Tagih kartu tanpa tuan pada peta 3-worker:
  A) blocked/review/todo tanpa event >=24 jam -> komentar tagihan ke controller (satu tagihan/kartu/hari)
  B) running tanpa heartbeat >=2 jam -> klaim mati, tagih reclaim
  C) assignee di luar PROFILE-REGISTRY hidup -> kartu yatim era lama
Aksi hanya KOMENTAR (read-only terhadap status). stdout non-kosong = ada aksi.
"""
import json, os, sqlite3, subprocess, pathlib, time

HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
HERMES = str(HOME / 'hermes-agent' / 'venv' / 'Scripts' / 'hermes.exe')
REG = pathlib.Path(r'C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')

def main():
    live = set(json.loads(REG.read_text(encoding='utf-8'))['hidup'])
    con = sqlite3.connect(HOME / 'kanban.db'); cur = con.cursor()
    now = int(time.time())
    acts = []
    rows = list(cur.execute(
        "SELECT id,assignee,status,title FROM tasks WHERE status IN ('blocked','review','todo','running')"))
    for tid, a, s, title in rows:
        le = cur.execute("SELECT MAX(created_at) FROM task_events WHERE task_id=?", (tid,)).fetchone()[0] or 0
        idle_h = (now - le) / 3600
        kind = None
        if s == 'running' and idle_h >= 2:
            kind = 'RUNNING-TANPA-HEARTBEAT'
        elif s in ('blocked', 'review', 'todo') and idle_h >= 24:
            kind = 'DIBIARKAN->=24JAM'
        elif a and a.startswith('gsp-') and a not in live:
            kind = 'ASSIGNEE-DI-LUAR-REGISTRI'
        if not kind:
            continue
        # anti-spam: jangan tagih dua kali dalam 20 jam
        recent = cur.execute(
            "SELECT COUNT(*) FROM task_events WHERE task_id=? AND kind='commented' AND created_at>?",
            (tid, now - 72000)).fetchone()[0]
        if recent:
            continue
        msg = (f"[ORPHAN-TAG v1] {kind}: status={s} idle={idle_h:.0f}j assignee={a}. "
               "Tagihan ke controller: tutup dengan bukti, unblock, atau needs_input ke user "
               "(aturan gerbang punya pemilik + tenggat).")
        r = subprocess.run([HERMES, 'kanban', '--board', 'default', 'comment', tid, msg,
                            '--author', 'board-cleaner'], capture_output=True, text=True, timeout=60)
        if r.returncode == 0:
            acts.append(f"{kind} {tid} ({(title or '')[:36]})")
    if acts:
        print(f"BOARD-CLEANER AKSI {len(acts)}: " + "; ".join(acts[:12]))
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
