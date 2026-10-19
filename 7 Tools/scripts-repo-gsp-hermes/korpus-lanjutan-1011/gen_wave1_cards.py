#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gen_wave1_cards.py - buat kartu G1+G1* (langkah 1-8) dari baris tabel 02_structured.md.
Deterministik: baris kartu = salinan kolom blueprint; tanpa interpretasi ulang. Stdlib+subprocess."""
import io, re, subprocess, os, sys, json

WS = 'C:/Users/TRIAL/workspace/gsp-hermes/workspace'
BP = WS + '/docs/2026-10-11-korpus-lanjutan-1011/identification/02_structured.md'
LAD = 'C:/Users/TRIAL/AppData/Local/hermes/skills/gsp/gsp-limit-aware-delegation/scripts/lad_card.py'
PARENT = 't_ef405f62'
TENANT = 'KORPUS-LANJUTAN-1011'
ENV = dict(os.environ); ENV.pop('HERMES_DELEGATED_CHILD_CONTEXT', None)
EST = {'1': 20, '2': 15, '3': 30, '4': 12, '5': 35, '6': 25, '7': 45, '8': 45}

def split_row(ln):
    ln = ln.strip().strip('|')
    tmp = ln.replace('\\|', '\x00')
    return [c.strip().replace('\x00', '|') for c in tmp.split('|')]

rows = {}
for ln in io.open(BP, encoding='utf-8').read().splitlines():
    m = re.match(r'^\|\s*(\d+)\s*\|', ln.strip())
    if m and int(m.group(1)) <= 8:
        rows[m.group(1)] = split_row(ln)

assert len(rows) == 8, f'baris 1-8 harus 8, dapat {len(rows)}'
out = []
for n in sorted(rows, key=int):
    r = rows[n]
    step, desc, agent, exp, deps, verif, phase, wajib, peranlock = r[:9]
    peran = re.search(r'peran\s*=\s*(\S+\.md)', peranlock)
    lock = re.search(r'LOCK\s*=\s*(.+)$', peranlock)
    body = (f"KELAS: BERAT (dari 01 sha16 a3260e6b4d3be01c; baris langkah {n} di 02_structured.md adalah otoritas kerjamu)\n"
            f"BERKAS PERAN: {WS}/roles/{peran.group(1) if peran else 'gsp-worker.md'}\n"
            f"TUGAS (verbatim 02): {desc}\n"
            f"EXPECTED OUTPUT: {exp}\n"
            f"VERIFIKASI (short check, maks 3 langkah): {verif}\n"
            f"WAJIB-BACA: {wajib}\n"
            f"LOCK (hanya berkas ini yang boleh kamu tulis): {lock.group(1) if lock else '(lihat 02)'}\n"
            f"BATAS: catatan koreksi TERTANGGAL bukan sunting senyap; jangan sentuh berkas di luar LOCK; "
            f"temuan di luar lingkup = komentar ISU-LINTAS-OWNER, jangan ditambal. "
            f"SAT-1010 bila disebut: pakai peta-lokus JSON, DILARANG baca penuh berkas besar ke konteks.\n"
            f"SELESAI: komentar LAPOR-SELESAI + wait-ack (C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_deleg_watch.py) lalu complete hanya jika ACKED/PARKED.\n"
            f"[jejak: blueprint 02 baris {n}, phase {phase}]")
    title = desc.split(':')[0] + f" (langkah {n}/{phase}): " + desc.split(':', 1)[1].strip()[:70]
    p = subprocess.run([sys.executable, LAD, '--title', title[:110], '--assignee', agent,
                        '--est', str(EST[n]), '--shape', 'satu', '--parents', PARENT,
                        '--tenant', TENANT, '--body', body],
                       capture_output=True, text=True, env=ENV)
    line = [l for l in (p.stdout + p.stderr).splitlines() if l.startswith('Created')]
    print(n, agent, EST[n], '->', line[0] if line else ('ERR ' + (p.stderr or p.stdout)[:120]))
    if line:
        out.append({'step': n, 'card': line[0].split()[1], 'assignee': agent})
io.open(WS + '/docs/2026-10-11-korpus-lanjutan-1011/work/waves/cards_wave1.json', 'w', encoding='utf-8').write(json.dumps(out, indent=1))
print('total dibuat =', len(out))
