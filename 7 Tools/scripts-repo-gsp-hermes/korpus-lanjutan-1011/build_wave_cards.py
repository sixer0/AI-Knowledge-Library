#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""build_wave_cards.py - ekstrak tabel 9 kolom 02_structured.md -> JSON kartu per gelombang
untuk gsp_wave_lock_guard.py --cards (kolom terakhir bernama PERAN+LOCK, parser --blueprint
menuntut header persis 'LOCK' - catatan TA S2 butir 7). Deterministik, stdlib-only."""
import io, json, re, sys, os

SRC = sys.argv[1] if len(sys.argv) > 1 else 'identification/02_structured.md'
OUTD = sys.argv[2] if len(sys.argv) > 2 else 'work/waves'

def split_row(line):
    line = line.strip()
    if line.startswith('|'): line = line[1:]
    if line.endswith('|'): line = line[:-1]
    # lindungi pipe ter-escape
    tmp = line.replace('\\|', '\x00')
    cells = [c.strip().replace('\x00', '|') for c in tmp.split('|')]
    return cells

rows = []
for ln in io.open(SRC, encoding='utf-8').read().splitlines():
    if re.match(r'^\|\s*\d+\s*\|', ln.strip()):
        rows.append(split_row(ln))

cards = []
for r in rows:
    while len(r) < 9: r.append('')
    step, desc, agent, exp, deps, verif, phase, wajib, peranlock = r[:9]
    m = re.search(r'LOCK\s*=\s*(.+)$', peranlock)
    lockcell = m.group(1) if m else ''
    locks = []
    for part in re.split(r';|\|', lockcell):
        part = part.strip().strip('`')
        if not part or part in ('-', '--', 'n/a', 'N/A', 'NONE'): continue
        # dua notasi hanya-baca: sufiks kanonis guard ('x RO'/'x (RO)') dan prefiks TA ('RO=x'/'(RO)=x')
        ro = bool(re.search(r'\(RO\)|\bRO$', part)) or bool(re.match(r'^\(?RO\)?=\s*', part, re.I))
        tgt = re.sub(r'^\(?(RO|ro)\)?=\s*', '', part)
        tgt = re.sub(r'\s*\(?RO\)?\s*$', '', tgt).strip()
        locks.append({'target': tgt, 'ro': ro})
    cards.append({'id': step, 'title': desc[:60], 'agent': agent, 'phase': phase,
                  'deps': [d.strip() for d in re.split(r'[;,\s]+', deps) if d.strip() and d.strip() != '—'],
                  'locks': locks})

os.makedirs(OUTD, exist_ok=True)
waves = {}
for c in cards:
    waves.setdefault(c['phase'], []).append(c)
idx = {}
for ph in sorted(waves):
    safe = re.sub(r'[^A-Za-z0-9_-]', 'X', ph)
    guard_cards = [{'id': f"s{c['id']}", 'title': c['title'],
                    'locks': [l['target'] for l in c['locks'] if not l['ro']],
                    'readonly': all(l['ro'] for l in c['locks']) and len(c['locks']) > 0}
                   for c in waves[ph]]
    p = os.path.join(OUTD, f'wave-{safe}.json')
    io.open(p, 'w', encoding='utf-8', newline='\n').write(json.dumps(guard_cards, indent=1, ensure_ascii=False))
    idx[ph] = {'n': len(waves[ph]), 'file': p}
io.open(os.path.join(OUTD, 'index.json'), 'w', encoding='utf-8', newline='\n').write(
    json.dumps(idx, indent=1, ensure_ascii=False))
print('kartu total =', len(cards))
for ph in sorted(idx): print(f"  {ph}: {idx[ph]['n']} kartu -> {idx[ph]['file']}")
# peringatan: kartu tanpa lock non-RO dan tanpa RO (mungkin sel kosong)
for c in cards:
    if not c['locks']:
        print('WARN kartu tanpa LOCK terparse:', c['id'], c['title'][:40])
