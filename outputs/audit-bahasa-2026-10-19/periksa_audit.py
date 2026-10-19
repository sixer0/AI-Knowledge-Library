#!/usr/bin/env python3
"""Periksa keutuhan audit bahasa terhadap commit awal; tidak menjalankan skrip pustaka.

Pemakaian: python3 outputs/audit-bahasa-2026-10-19/periksa_audit.py
Opsi --output <path> menyimpan hasil JSON. Memerlukan Git dan riwayat commit awal.
"""
from pathlib import Path
from collections import Counter
from urllib.parse import unquote, urlsplit
import argparse
import csv
import hashlib
import io
import json
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
BASE = '8785880'
FOLDERS = ['1 Workflow', '2 Roles', '3 Skills', '4 Knowledge Bank',
           '5 Integration', '6 Database', '7 Tools']
NUMBERS = re.compile(r'(?<![\w])\d[\d.,:/-]*')


def git_bytes(path):
    return subprocess.run(['git', 'show', f'{BASE}:{path}'], cwd=ROOT,
                          check=True, capture_output=True).stdout


def digest(data):
    return hashlib.sha256(data).hexdigest()


def numeric_values(text):
    # Penanda daftar dapat berubah bentuk (1) menjadi 1.; nilainya bukan data faktual.
    text = re.sub(r'^\s*\d+[.)]\s+', '', text, flags=re.M)
    text = re.sub(r'(?<!\w)\(\d+\)\s+', '', text)
    return Counter(m.rstrip('.:/-') for m in NUMBERS.findall(text))


def regions(text):
    front = re.match(r'\A---\r?\n.*?\r?\n---(?:\r?\n|$)', text, re.S)
    marker = None
    block = []
    blocks = []
    prose = []
    for line in text.splitlines(keepends=True):
        m = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            block.append(line)
            if m and m[1][0] == marker:
                blocks.append(''.join(block)); block = []; marker = None
        elif m:
            marker = m[1][0]; block = [line]
        else:
            prose.append(line)
    if block:
        blocks.append(''.join(block))
    rest = ''.join(prose)
    return {
        'metadata': front[0] if front else '',
        'blok_kode': blocks,
        'kode_sebaris': Counter(re.findall(r'`+[^`\n]*`+', rest)),
        'url': Counter(re.findall(r'https?://[^\s<>\]\)"`]+', text)),
        'angka': numeric_values(text),
        'himpunan_literal': Counter(re.findall(r'\{[^{}\r\n]*\}', text)),
        'perintah_prompt': re.findall(r'^\s*(?:python(?:3)?\b|node\b|--[\w-]+(?=\s|=|$)).*', text, re.M),
    }


def heading_ids(text):
    found = set()
    used = Counter()
    for title in re.findall(r'^#{1,6}\s+(.+)', text, re.M):
        title = re.sub(r'<[^>]+>', '', title)
        title = title.lower().strip()
        slug = ''.join(c for c in title if c.isalnum() or c in ' _-').replace(' ', '-')
        n = used[slug]; used[slug] += 1
        found.add(slug + (f'-{n}' if n else ''))
    found.update(re.findall(r'(?:id|name)=["\x27]([^"\x27]+)', text))
    return found


def links(text):
    # Audit tautan Markdown eksplisit; rujukan path dalam kode sebaris bukan hyperlink.
    return re.findall(r'!?\[[^\]\n]*\]\(([^)\n]+)\)', text)


def run():
    raw_manifest = git_bytes('MANIFEST.csv')
    before = {r['relative_path']: r for r in csv.DictReader(io.StringIO(raw_manifest.decode()))}
    before['MANIFEST.csv'] = {'relative_path': 'MANIFEST.csv',
                              'bytes': len(raw_manifest), 'sha256': digest(raw_manifest)}
    current = {}
    fingerprints = {}
    old_text = {}
    changed = []
    failures = []
    checks = Counter()
    for path, row in before.items():
        file = ROOT / path
        if not file.is_file():
            failures.append({'berkas': path, 'cek': 'berkas asli hilang'}); continue
        data = file.read_bytes()
        fingerprints[path] = (len(data), digest(data))
        if file.suffix == '.md':
            current[path] = data.decode('utf-8')
        if digest(data) == row['sha256']:
            checks['berkas_identik'] += 1
            continue
        changed.append(path)
        if path in {'README.md', 'MANIFEST.csv'} or file.name == 'INDEKS.md':
            if file.suffix == '.md':
                old_text[path] = git_bytes(path).decode('utf-8')
            continue
        prompt = path.startswith('7 Tools/scripts-repo-gsp-hermes/prompts/') and file.suffix == '.txt'
        if file.suffix != '.md' and not prompt:
            failures.append({'berkas': path, 'cek': 'kode, data, atau aset berubah'}); continue
        if any(s in path.lower() for s in ['fixtures', '/corpus-merah-hijau/', '/03_source-vault/', '/08_evidence/']):
            failures.append({'berkas': path, 'cek': 'korpus uji atau bukti sumber berubah'})
        old = git_bytes(path).decode('utf-8'); old_text[path] = old
        a, b = regions(old), regions(data.decode('utf-8'))
        for name in a:
            if a[name] != b[name]:
                failures.append({'berkas': path, 'cek': name})
        checks['dokumen_dibandingkan'] += 1

    rows = list(csv.DictReader((ROOT / 'MANIFEST.csv').open(newline='')))
    if len(rows) != len(before) - 1 or len({r['relative_path'] for r in rows}) != len(rows):
        failures.append({'cek': 'jumlah atau keunikan entri manifest'})
    if {r['relative_path'] for r in rows} != set(before) - {'MANIFEST.csv'}:
        failures.append({'cek': 'cakupan manifest berubah'})
    for row in rows:
        data = (ROOT / row['relative_path']).read_bytes()
        if int(row['bytes']) != len(data) or row['sha256'] != digest(data):
            failures.append({'berkas': row['relative_path'], 'cek': 'ukuran atau SHA-256 manifest'})
    checks['entri_manifest'] = len(rows)

    scope_file = ROOT / 'outputs/audit-bahasa-2026-10-19/cakupan-audit.csv'
    scope = list(csv.DictReader(scope_file.open(newline='')))
    if len(scope) != len(before) or {r['berkas'] for r in scope} != set(before):
        failures.append({'cek': 'cakupan CSV audit'})
    for row in scope:
        path = row['berkas']
        if path not in before or path not in fingerprints:
            continue
        if row['sha256_awal'] != before[path]['sha256'] or row['sha256_akhir'] != fingerprints[path][1]:
            failures.append({'berkas': path, 'cek': 'hash pada CSV cakupan audit'})
    checks['baris_cakupan_audit'] = len(scope)
    for folder in FOLDERS:
        slug = folder.split()[0]
        csv_path = ROOT / f'outputs/audit-bahasa-2026-10-19/{slug}-perubahan.csv'
        detail = list(csv.DictReader(csv_path.open(newline='')))
        expected = {p for p in changed if p.startswith(folder + '/')}
        if len(detail) != len(expected) or {r['berkas'] for r in detail} != expected:
            failures.append({'berkas': str(csv_path.relative_to(ROOT)), 'cek': 'daftar perubahan folder'})
        for row in detail:
            path = row['berkas']
            if path not in before or path not in fingerprints:
                continue
            size, sha = fingerprints[path]
            if (int(row['byte_awal']) != int(before[path]['bytes']) or
                    row['sha256_awal'] != before[path]['sha256'] or
                    int(row['byte_sesudah']) != size or row['sha256_sesudah'] != sha):
                failures.append({'berkas': path, 'cek': 'ukuran atau hash pada rincian folder'})
        checks['baris_rincian_folder'] += len(detail)

    for folder in FOLDERS:
        index = current[folder + '/INDEKS.md']
        listed = re.findall(r'^\| `([^`]+)` \|', index, re.M)
        expected = {p for p in before if p.startswith(folder + '/') and p != folder + '/INDEKS.md'}
        if set(listed) != expected or len(listed) != len(set(listed)):
            failures.append({'berkas': folder + '/INDEKS.md', 'cek': 'cakupan indeks'})
        for p in listed:
            if not (ROOT / p).is_file():
                failures.append({'berkas': p, 'cek': 'path indeks hilang'})
        checks['path_indeks'] += len(listed)

    prefix_a, prefix_b = '3 Skills/kanonik/', '3 Skills/registry-fleet/'
    a = {p[len(prefix_a):]: r for p, r in before.items() if p.startswith(prefix_a)}
    b = {p[len(prefix_b):]: r for p, r in before.items() if p.startswith(prefix_b)}
    for key in a.keys() & b.keys():
        if a[key]['sha256'] == b[key]['sha256']:
            if (ROOT / prefix_a / key).read_bytes() != (ROOT / prefix_b / key).read_bytes():
                failures.append({'berkas': key, 'cek': 'pasangan skill yang semula identik berbeda'})
            checks['pasangan_skill_identik'] += 1
        else:
            checks['pasangan_skill_berbeda_sejak_awal'] += 1

    def baseline_text(path):
        return old_text.get(path, current.get(path, ''))

    def valid_link(owner, target, baseline=False):
        target = target.strip().strip('<>')
        if ' "' in target:
            target = target.split(' "', 1)[0]
        parts = urlsplit(target)
        if parts.scheme or parts.netloc:
            return None
        target_path = unquote(parts.path)
        file = (ROOT / owner).parent / target_path if target_path else ROOT / owner
        file = file.resolve()
        try:
            rel = str(file.relative_to(ROOT))
        except ValueError:
            return None
        exists = rel in before or any(p.startswith(rel + '/') for p in before) if baseline else file.exists()
        if not exists:
            return False
        if parts.fragment and file.suffix == '.md':
            text = baseline_text(rel) if baseline else current.get(rel, file.read_text())
            return unquote(parts.fragment) in heading_ids(text)
        return True

    existing_broken = 0
    regressions = []
    for path, text in current.items():
        old = baseline_text(path)
        old_links = set(links(old))
        for target in old_links:
            was = valid_link(path, target, baseline=True)
            now = valid_link(path, target)
            if was is False:
                existing_broken += 1
            if was is True and now is False:
                regressions.append({'berkas': path, 'tautan': target})
        for target in set(links(text)) - old_links:
            if valid_link(path, target) is False:
                regressions.append({'berkas': path, 'tautan': target})
    for path in sorted((ROOT / 'outputs/audit-bahasa-2026-10-19').glob('*.md')):
        for target in links(path.read_text()):
            if valid_link(str(path.relative_to(ROOT)), target) is False:
                regressions.append({'berkas': str(path.relative_to(ROOT)), 'tautan': target})
    if regressions:
        failures.extend({'cek': 'regresi tautan lokal', **r} for r in regressions)
    checks['tautan_lokal_bermasalah_sejak_awal'] = existing_broken
    checks['regresi_tautan_lokal'] = len(regressions)

    whitespace = subprocess.run(['git', '-c', 'core.whitespace=cr-at-eol', 'diff', BASE, '--check'],
                                cwd=ROOT, capture_output=True, text=True)
    if whitespace.returncode:
        failures.append({'cek': 'git diff --check', 'rincian': whitespace.stdout})
    counts = {f: {'asli': sum(p.startswith(f + '/') for p in before),
                  'diubah': sum(p.startswith(f + '/') for p in changed)} for f in FOLDERS}
    return {'tanggal': '2026-10-19', 'baseline': BASE,
            'status': 'LULUS' if not failures else 'GAGAL',
            'berkas_asli': len(before), 'berkas_asli_diubah': len(changed),
            'folder': counts, 'cek': dict(checks), 'kegagalan': failures,
            'tidak_dijalankan': ['uji layanan dan skrip operasional', 'pemeriksaan fakta eksternal',
                                 'pembacaan editorial manual setiap kalimat', 'audit keamanan']}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    result = run()
    text = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        args.output.write_text(text)
    print(text, end='')
    sys.exit(0 if result['status'] == 'LULUS' else 1)
