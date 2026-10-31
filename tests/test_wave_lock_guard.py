"""Uji gerbang LOCK pra-gelombang dengan blueprint sintetis; tidak membaca data pustaka."""
from pathlib import Path
import ast
import json
import subprocess
import sys
import tempfile
import unittest

GUARD = Path(__file__).resolve().parents[1] / '7 Tools/scripts-profil-controller/gsp_wave_lock_guard.py'
COLUMNS = ['Step', 'Task Description', 'Agent_to_Invoke', 'Expected Output', 'Depends On',
           'Verification', 'Phase', 'WAJIB_BACA']
ALLOWED_IMPORTS = {'argparse', 'json', 're', 'sys'}
WRITER_METHODS = {'write', 'writelines', 'write_text', 'write_bytes', 'dump'}
DYNAMIC_CALLS = {'__import__', 'exec', 'eval'}


def blueprint(last_header, *last_cells):
    """Tabel breakdown sintetis: satu baris per sel kolom terakhir, tiap baris fase berbeda."""
    header = COLUMNS + [last_header]
    lines = ['# Blueprint sintetis', '', '| ' + ' | '.join(header) + ' |', '|' + '---|' * len(header)]
    for step, cell in enumerate(last_cells, 1):
        lines.append(f'| {step} | tugas {step} | gsp-worker | hasil {step} | - | ada | F{step} | a.md#b | {cell} |')
    return '\n'.join(lines) + '\n'


def id_table(*rows):
    """Tabel dengan kolom pertama ditentukan sendiri, untuk ID ganda dan ID kosong."""
    lines = ['| Step | Tugas | LOCK |', '|---|---|---|']
    lines += [f'| {card_id} | tugas | {lock} |' for card_id, lock in rows]
    return '\n'.join(lines) + '\n'


def guard_violations(source):
    """Bentuk di luar klaim RK-33: impor selain daftar, pemuatan dinamis, open tulis, dan pemanggilan penulis."""
    found = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            found += [f'import {alias.name}' for alias in node.names if alias.name.split('.')[0] not in ALLOWED_IMPORTS]
        elif isinstance(node, ast.ImportFrom):
            if (node.module or '').split('.')[0] not in ALLOWED_IMPORTS or node.level:
                found.append(f'from {node.module} import')
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            if node.func.id in DYNAMIC_CALLS:
                found.append(f'{node.func.id}()')
            elif node.func.id == 'open':
                modes = node.args[1:2] + [item.value for item in node.keywords if item.arg in ('mode', None)]
                if not all(isinstance(m, ast.Constant) and set(str(m.value)) <= set('rbt') for m in modes):
                    found.append('open tulis')
        elif isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):
            if node.func.attr in WRITER_METHODS and ast.unparse(node.func.value) not in ('sys.stdout', 'sys.stderr'):
                found.append(f'.{node.func.attr}()')
    return found


class WaveLockGuardTests(unittest.TestCase):
    def run_guard(self, flag, name, content):
        with tempfile.TemporaryDirectory(prefix='guard uji ') as folder:
            path = Path(folder) / name
            path.write_text(content, encoding='utf-8')
            done = subprocess.run([sys.executable, '-B', str(GUARD), flag, str(path)],
                                  capture_output=True, text=True, encoding='utf-8')
        return done.returncode, done.stdout

    def run_blueprint(self, content):
        return self.run_guard('--blueprint', '02.md', content)

    def test_compound_header_detects_collision(self):
        code, out = self.run_blueprint(blueprint(
            'PERAN+LOCK', 'peran=roles/a.md \\| LOCK=bersama.md', 'peran=roles/b.md \\| LOCK=bersama.md'))
        self.assertEqual(code, 1, out)
        self.assertIn('CHECK 1: FAIL', out)
        self.assertIn('1~2:bersama.md', out)

    def test_compound_header_partitioned_passes(self):
        code, out = self.run_blueprint(blueprint(
            'PERAN+LOCK', 'peran=roles/a.md \\| LOCK=a.md; b.md', 'peran=roles/b.md \\| LOCK=c.md'))
        self.assertEqual(code, 0, out)
        self.assertIn('CHECK 1: PASS', out)
        self.assertIn('3 target tulis', out)

    def test_compound_readonly_steps_do_not_collide(self):
        code, out = self.run_blueprint(blueprint(
            'PERAN+LOCK', 'peran=roles/a.md \\| LOCK=RO', 'peran=roles/b.md \\| LOCK=RO'))
        self.assertEqual(code, 0, out)
        self.assertIn('CHECK 1: PASS', out)

    def test_compound_cell_without_lock_value_fails(self):
        code, out = self.run_blueprint(blueprint('PERAN+LOCK', 'peran=roles/a.md'))
        self.assertEqual(code, 1, out)
        self.assertIn('CHECK 2: FAIL', out)

    def test_unescaped_pipe_is_still_read(self):
        code, out = self.run_blueprint(blueprint(
            'PERAN+LOCK', 'peran=roles/a.md | LOCK=bersama.md', 'peran=roles/b.md | LOCK=bersama.md'))
        self.assertEqual(code, 1, out)
        self.assertIn('1~2:bersama.md', out)

    def test_bare_lock_readonly_steps_do_not_collide(self):
        code, out = self.run_blueprint(blueprint('LOCK', 'RO', 'RO'))
        self.assertEqual(code, 0, out)
        self.assertIn('CHECK 1: PASS', out)

    def test_bare_lock_collision_still_fails(self):
        # Kedua baris berada pada fase berbeda: --blueprint menilai seluruh tabel sebagai satu gelombang.
        code, out = self.run_blueprint(blueprint('LOCK', 'bersama.md', 'bersama.md'))
        self.assertEqual(code, 1, out)
        self.assertIn('1~2:bersama.md', out)

    def test_blueprint_without_lock_table_fails(self):
        code, out = self.run_blueprint('# Tanpa tabel\n\nHanya prosa.\n')
        self.assertEqual(code, 1, out)
        self.assertIn('VERDICT: FAIL', out)
        self.assertNotIn('VERDICT: PASS', out)

    def test_empty_card_list_fails(self):
        code, out = self.run_guard('--cards', 'gelombang.json', '[]')
        self.assertEqual(code, 1, out)
        self.assertIn('VERDICT: FAIL', out)

    def test_cards_collision_still_fails(self):
        cards = [{'id': 'a', 'locks': ['bersama.md']}, {'id': 'b', 'locks': ['bersama.md']}]
        code, out = self.run_guard('--cards', 'gelombang.json', json.dumps(cards))
        self.assertEqual(code, 1, out)
        self.assertIn('a~b:bersama.md', out)

    # Tambahan PL-5 di luar prediksi 06f. Merah awalnya dicatat apa adanya.

    def test_backtick_target_equals_plain_target(self):
        # PB-17a kasus 1. Pada header LOCK sel harus berbanyak target: clean_cell sudah memangkas sel tunggal.
        cases = [('LOCK', '`a.md`; b.md', 'a.md; c.md'),
                 ('LOCK', 'x.md; `a.md`; b.md', 'y.md; a.md'),
                 ('PERAN+LOCK', 'peran=roles/a.md \\| LOCK=`a.md`', 'peran=roles/b.md \\| LOCK=a.md')]
        for header, first, second in cases:
            with self.subTest(header=header, first=first):
                code, out = self.run_blueprint(blueprint(header, first, second))
                self.assertEqual(code, 1, out)
                self.assertIn('1~2:a.md', out)

    def test_backtick_readonly_target_stays_readonly(self):
        # PB-17a kasus 2. Dua penulisan RO menjadi satu target a.md, terlihat pada CHECK 3.
        code, out = self.run_blueprint(blueprint('LOCK', '`a.md` RO; a.md RO', 'a.md'))
        self.assertEqual(code, 0, out)
        self.assertIn('CHECK 1: PASS', out)
        self.assertIn('1:a.md', out)
        code, out = self.run_blueprint(blueprint('LOCK', 'x.md; `a.md` RO', 'y.md; a.md RO'))
        self.assertEqual(code, 0, out)
        self.assertIn('2 target tulis', out)

    def test_backtick_only_part_is_not_a_target(self):
        # PB-17a kasus 3. Di tengah sel, agar tidak terjangkau clean_cell.
        for mark in ('`', '``', '```', '` `'):
            with self.subTest(mark=mark):
                code, out = self.run_blueprint(blueprint('LOCK', f'x.md; {mark}; k.md', f'y.md; {mark}; m.md'))
                self.assertEqual(code, 0, out)
                self.assertIn('4 target tulis', out)

    def test_write_claim_beats_readonly_with_backticks(self):
        # PB-17b: tanpa ini PB-17a mengubah vonis kartu ini dari FAIL menjadi PASS.
        code, out = self.run_blueprint(blueprint('LOCK', 'x; `a.md`; a.md RO', 'y; `a.md`; z'))
        self.assertEqual(code, 1, out)
        self.assertIn('1~2:a.md', out)

    def test_write_claim_beats_readonly_in_plain_form(self):
        # PB-17b, dua urutan: vonis tidak boleh bergantung pada kemunculan terakhir.
        for first in ('a.md; a.md RO', 'a.md RO; a.md'):
            with self.subTest(first=first):
                code, out = self.run_blueprint(blueprint('LOCK', first, 'a.md'))
                self.assertEqual(code, 1, out)
                self.assertIn('1~2:a.md', out)

    def test_all_readonly_occurrences_do_not_collide(self):
        # Kontrol PB-17b: klaim tulis tidak dikarang bila semua kemunculan RO.
        code, out = self.run_blueprint(blueprint('LOCK', 'a.md RO; a.md (RO)', 'a.md'))
        self.assertEqual(code, 0, out)
        self.assertIn('1 target tulis', out)

    def test_two_waves_same_file_through_blueprint_fails(self):
        # RK-32: --blueprint menilai seluruh tabel sebagai satu gelombang.
        code, out = self.run_blueprint(blueprint(
            'PERAN+LOCK', 'peran=roles/a.md \\| LOCK=bersama.md', 'peran=roles/b.md \\| LOCK=bersama.md'))
        self.assertEqual(code, 1, out)
        self.assertIn('bersama.md', out)

    def test_two_waves_same_file_through_cards_per_wave_passes(self):
        # RK-32: pasangannya sebagai kontrol ada pada test_cards_collision_still_fails.
        for card in ({'id': 'a', 'locks': ['bersama.md']}, {'id': 'b', 'locks': ['bersama.md']}):
            with self.subTest(card=card['id']):
                code, out = self.run_guard('--cards', 'gelombang.json', json.dumps([card]))
                self.assertEqual(code, 0, out)
                self.assertIn('CHECK 1: PASS', out)

    # CR-01: tumbukan dinilai per kartu, bukan per ID.

    def test_same_id_cards_collide(self):
        code, out = self.run_blueprint(id_table(('W1', 'a.md'), ('W1', 'a.md')))
        self.assertEqual(code, 1, out)
        self.assertIn('W1~W1:a.md', out)
        cards = [{'id': 'W1', 'locks': ['a.md']}, {'id': 'W1', 'locks': ['a.md']}]
        code, out = self.run_guard('--cards', 'gelombang.json', json.dumps(cards))
        self.assertEqual(code, 1, out)
        self.assertIn('W1~W1:a.md', out)

    def test_cards_without_id_collide(self):
        for cards in ([{'locks': ['a.md']}, {'locks': ['a.md']}],
                      [{'id': '', 'locks': ['a.md']}, {'id': None, 'locks': ['a.md']}]):
            with self.subTest(cards=cards):
                code, out = self.run_guard('--cards', 'gelombang.json', json.dumps(cards))
                self.assertEqual(code, 1, out)
                self.assertIn('?~?:a.md', out)

    def test_blueprint_rows_without_id_collide(self):
        # Sel pertama kosong bukan alasan melewati baris: kartunya tetap menulis.
        code, out = self.run_blueprint(id_table(('', 'a.md'), ('', 'a.md')))
        self.assertEqual(code, 1, out)
        self.assertIn('?~?:a.md', out)

    def test_three_same_id_cards_count_every_pair(self):
        code, out = self.run_blueprint(id_table(('W1', 'a.md'), ('W1', 'a.md'), ('W1', 'a.md')))
        self.assertEqual(code, 1, out)
        self.assertIn('3 pasangan', out)

    def test_different_ids_readonly_do_not_collide(self):
        # Kontrol CR-01: perbaikan tidak mengarang tumbukan pada kartu hanya-baca.
        code, out = self.run_blueprint(id_table(('W1', 'a.md RO'), ('W2', 'a.md RO')))
        self.assertEqual(code, 0, out)
        self.assertIn('CHECK 1: PASS', out)
        cards = [{'id': 'W1', 'locks': ['a.md'], 'readonly': True}, {'id': 'W2', 'locks': ['a.md'], 'readonly': True}]
        code, out = self.run_guard('--cards', 'gelombang.json', json.dumps(cards))
        self.assertEqual(code, 0, out)
        self.assertIn('CHECK 1: PASS', out)

    def test_same_id_without_shared_write_passes(self):
        # Kontrol CR-01: ID sama saja bukan tumbukan, dan satu kartu tidak bertumbukan dengan dirinya.
        for rows in ((('W1', 'a.md'), ('W1', 'b.md')), (('W1', 'a.md'), ('W1', 'a.md RO')), (('W1', 'a.md; a.md'),)):
            with self.subTest(rows=rows):
                code, out = self.run_blueprint(id_table(*rows))
                self.assertEqual(code, 0, out)
                self.assertIn('CHECK 1: PASS', out)

    def test_empty_row_is_not_a_card(self):
        # Kontrol CR-01: baris tanpa isi sama sekali tetap dilewati.
        code, out = self.run_blueprint(id_table(('W1', 'a.md'), ('', '')).replace('|  | tugas |  |', '|  |  |  |'))
        self.assertEqual(code, 0, out)
        self.assertIn('CHECK 2: PASS', out)

    def test_guard_has_no_subprocess_socket_or_writer(self):
        # RK-33: dasar pengecualian N-18 sebagai satu-satunya pemanggil skrip 7 Tools.
        self.assertEqual(guard_violations(GUARD.read_text(encoding='utf-8')), [])

    def test_guard_violations_detects_forbidden_forms(self):
        # Kontrol uji AST: sumber sintetis hanya diurai, tidak dijalankan.
        for source in ('import subprocess', 'import socket', 'from socket import socket', 'import os.path',
                       'from . import sys', '__import__("socket")', 'open(p, "w")', 'open(p, mode="a")',
                       'open(p, m)', 'open(p, "r+")', 'Path(p).write_text("x")', 'f.write("x")', 'json.dump(x, f)'):
            with self.subTest(source=source):
                self.assertTrue(guard_violations(source))
        for source in ('import argparse', 'open(p, "r", encoding="utf-8")', 'open(p)',
                       'sys.stdout.write("x")', 're.compile("x")', '"a".replace("a", "b")'):
            with self.subTest(source=source):
                self.assertEqual(guard_violations(source), [])


if __name__ == '__main__':
    unittest.main()
