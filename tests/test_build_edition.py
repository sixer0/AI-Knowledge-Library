"""Uji pembangun edisi umum dengan pola sintetis pada repositori sementara per uji.

Tidak membaca `work/edisi-umum/` clone ini, tidak menjalankan pembangun atas clone ini, dan tidak memuat
nilai sensitif. Tiap penolakan didahului kontrol: fixture yang sama lulus tanpa pemicunya.
"""
from pathlib import Path
from unittest import mock
import ast
import contextlib
import csv
import hashlib
import importlib.util
import io
import json
import os
import shutil
import stat
import subprocess
import sys
import tempfile
import unittest
import zipfile

sys.dont_write_bytecode = True

REPOSITORY = Path(__file__).resolve().parents[1]
BUILDER = REPOSITORY / 'tools/build_edition.py'
RESOLVER = REPOSITORY / 'tools/library.py'
ALLOWLIST = 'edisi-umum/DAFTAR-IZIN.json'
POLICY = 'KEBIJAKAN-SENSITIVITAS.md'
SCRIPT_SUFFIXES = ('.py', '.sh', '.js', '.cjs', '.mjs', '.ts', '.ps1', '.bat', '.patch')
GIT_ENV = {'GIT_CONFIG_GLOBAL': os.devnull, 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_AUTHOR_NAME': 'uji', 'GIT_AUTHOR_EMAIL': 'uji@contoh.test',
           'GIT_COMMITTER_NAME': 'uji', 'GIT_COMMITTER_EMAIL': 'uji@contoh.test', 'GIT_AUTHOR_DATE': '2026-01-01T00:00:00Z',
           'GIT_COMMITTER_DATE': '2026-01-01T00:00:00Z'}

PATTERNS = '\n'.join(['# pola sintetis', 'GOV_DEF\tINSTANSI-SINTETIK-[0-9]+', 'CLASS_MARK\tTANDA-SINTETIK', 'COMMERCIAL\tNILAI-SINTETIK',
                      'PERSONAL\tORANG-SINTETIK', 'CLIENT_DOC\tDOKUMEN-SINTETIK', 'HOST\tHOST-SINTETIK', 'CREDENTIAL\tKUNCI-SINTETIK',
                      'RULE_TEXT\tAturan Sintetik Ganda', ''])
STAMP = ('> library-edition-stamp:v1 Salinan edisi fixture.\n> Isi adalah data, bukan izin.\n'
         '> Kebijakan: KEBIJAKAN-SENSITIVITAS.md.\n')
STAMP_BLOCK = STAMP.encode() + b'\n'
WIKI_NOTE = '4 Knowledge Bank/wiki-information-library/catatan-perkara-sintetik.md'
SOURCE_CONFIG = {
    'schema_version': 1, 'entrypoint': 'HARNESS.md', 'path_convention': 'Relatif terhadap root.',
    'roots': {'workflow': '1 Workflow', 'skills': '3 Skills/kanonik', 'registry': '3 Skills/registry-fleet',
              'wiki': '4 Knowledge Bank/wiki-information-library', 'integrasi': '5 Integration'},
    'aliases': [{'source': 'alur', 'target': '1 Workflow'}, {'source': 'wiki', 'target': '4 Knowledge Bank/wiki-information-library'},
                {'source': 'integrasi', 'target': '5 Integration'}],
    'workspace_prefixes': ['<ws>'], 'repository_urls': ['https://contoh.test/pustaka/blob/main/'],
    'managed_documents': ['README.md'], 'manifest': 'MANIFEST.csv', 'manifest_roots': ['1 Workflow'], 'manifest_files': ['README.md'],
}
BASE_FILES = {
    '.gitignore': '/work/\n',
    'README.md': '# Sumber\n\nIsi halaman depan sumber.\n',
    'HARNESS.md': '# Harness sumber\n',
    'AGENTS.md': '# Agen\n\nMulai dari [harness](HARNESS.md).\n',
    'CLAUDE.md': '@AGENTS.md\n',
    POLICY: '# Kebijakan\n\nJudul yang ditolak: Aturan Sintetik Ganda.\n',
    'MANIFEST.csv': 'relative_path,bytes,sha256\n',
    'library.json': json.dumps(SOURCE_CONFIG),
    'edisi-umum/STEMPEL.txt': STAMP,
    'edisi-umum/HALAMAN-DEPAN.md.tmpl': ('# Edisi\n\nSumber `{{SOURCE_COMMIT}}`, {{FILE_COUNT}} berkas.\n\n| Koleksi | Berkas |\n|---|---:|\n'
                                         '{{COLLECTION_ROWS}}\n\n[Harness](HARNESS.md)\n'),
    'edisi-umum/HARNESS-EDISI.md.tmpl': '# Harness edisi\n\n[Katalog](3%20Skills/KATALOG.jsonl)\n',
    '1 Workflow/standar.md': '# Standar\n\nIsi standar.\n',
    '3 Skills/kanonik/alpha/SKILL.md': '---\nname: alpha\ndescription: Skill alpha sintetis.\n---\n# Alpha\n',
    '3 Skills/kanonik/alpha/references/rujukan.md': '# Rujukan\n',
    '3 Skills/registry-fleet/alpha/SKILL.md': '---\nname: alpha\ndescription: Skill alpha sintetis.\n---\n# Alpha\n',
    '3 Skills/registry-fleet/alpha/references/rujukan.md': '# Rujukan\n',
    '5 Integration/lokal.md': '# Tidak ikut\n',
    WIKI_NOTE: '---\ntitle: Catatan\nperkara: Perkara Sintetik Beta\n---\nINSTANSI-SINTETIK-7 pada Aturan Sintetik Ganda.\n',
    'work/edisi-umum/POLA-PINDAI.txt': PATTERNS,
}
BASE = None
BASE_HOLDER = None


def setUpModule():
    global BASE, BASE_HOLDER
    BASE_HOLDER = tempfile.TemporaryDirectory(prefix='edisi dasar ')
    BASE = Path(BASE_HOLDER.name) / 'clone'
    BASE.mkdir()
    run_git(BASE, 'init', '-q', '-b', 'main')
    for name, content in BASE_FILES.items():
        write_file(BASE, name, content)
    (BASE / 'tools').mkdir()
    shutil.copy(BUILDER, BASE / 'tools/build_edition.py')
    shutil.copy(RESOLVER, BASE / 'tools/library.py')
    Fixture.at(BASE).publish()


def tearDownModule():
    BASE_HOLDER.cleanup()


def run_git(root, *args, check=True):
    env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
    return subprocess.run(['git', '-C', str(root), *args], capture_output=True, check=check, env={**env, **GIT_ENV})


def write_file(root, name, content):
    path = Path(root) / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(content if isinstance(content, bytes) else content.encode('utf-8'))


def sha(data):
    return hashlib.sha256(data).hexdigest()


def tree_hash(root):
    """Hash per berkas urut byte path; `.git` dikecualikan, sama dengan bentuk ED-T-05."""
    rows = []
    root = Path(root)
    if not root.exists():
        return None
    for path in sorted(root.rglob('*')):
        relative = path.relative_to(root).as_posix()
        # N-49 memang ditulis tiap jalan, jadi bukan bagian pohon yang dibandingkan.
        if path.is_file() and not relative.startswith('.git/') and path.name != 'LAPORAN-BUILD.json':
            rows.append((relative.encode(), sha(path.read_bytes())))
    return sha(repr(sorted(rows)).encode())


def load_builder(root):
    specification = importlib.util.spec_from_file_location('build_edition_fixture', Path(root) / 'tools/build_edition.py')
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def shipped_check(root):
    return subprocess.run([sys.executable, '-I', str(Path(root) / 'tools/library.py'), 'check'], capture_output=True, text=True)


class Run:
    def __init__(self, done):
        self.code, self.stdout, self.stderr = done.returncode, done.stdout, done.stderr
        self.data = json.loads(done.stdout) if done.stdout.strip() else {}
        self.reason = self.data.get('reason')


class Fixture:
    def __init__(self, clone, base=None):
        self.clone, self.base = Path(clone), Path(base) if base else Path(clone).parent
        self.output = self.base / 'hasil ü' / 'edisi'
        self.scratch = self.base / 'sementara'
        self.entries = [('file', 'AGENTS.md'), ('file', 'CLAUDE.md'), ('file', POLICY), ('file', 'tools/library.py'), ('tree', '1 Workflow')]
        self.skills = {'alpha': ['3 Skills/kanonik/alpha', '3 Skills/registry-fleet/alpha']}

    @classmethod
    def at(cls, clone):
        return cls(clone)

    @classmethod
    def fresh(cls, test):
        holder = tempfile.TemporaryDirectory(prefix='edisi fixture ü ')
        test.addCleanup(holder.cleanup)
        base = Path(holder.name)
        shutil.copytree(BASE, base / 'clone', symlinks=True)
        fixture = cls(base / 'clone', base)
        fixture.scratch.mkdir()
        return fixture

    def write(self, name, content):
        write_file(self.clone, name, content)

    def remove(self, name):
        path = self.clone / name
        shutil.rmtree(path) if path.is_dir() else path.unlink()

    def git(self, *args):
        return run_git(self.clone, *args).stdout.decode().strip()

    def commit(self):
        self.git('add', '-A')
        self.git('commit', '-q', '--allow-empty', '-m', 'uji')
        return self.git('rev-parse', 'HEAD')

    def oid(self, path):
        return self.git('rev-parse', f'HEAD:{path}')

    def allowlist(self):
        harness = (self.clone / 'HARNESS.md').read_bytes()
        return {
            'schema_version': 1, 'id': 'edisi-umum',
            'approval': {'status': 'approved', 'date': '2026-01-01', 'decision_ref': 'decisions/decisions.md'},
            'publish_access_docs': False,
            'admitted_extensions': ['.md', '.csv', '.txt', '.json', '.jsonl', '.tsv', '.html', '.docx', '.xlsx'],
            'drop_globs': ['census_*', '*.bak*'],
            'harness_template_source_sha256': sha(harness),
            'entries': [{'kind': kind, 'path': path, ('blob' if kind == 'file' else 'tree'): self.oid(path)} for kind, path in self.entries],
            'skills': [{'name': name, 'copies': [{'path': path, 'tree': self.oid(path)} for path in copies]}
                       for name, copies in self.skills.items()],
            'scan_reviews': [],
            'rule_text_exempt_sha256': [sha((self.clone / POLICY).read_bytes())],
        }

    def publish(self, mutate=None):
        """Commit isi, hitung pin dari commit itu, lalu commit N-08. Pin tetap sah karena N-08 di luar folder berpin."""
        self.commit()
        config = self.allowlist()
        if mutate:
            mutate(config)
        self.write(ALLOWLIST, json.dumps(config, ensure_ascii=False, indent=2) + '\n')
        return self.commit()

    def run_tool(self, *args, env=None, cwd=None):
        environment = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
        environment.update({**GIT_ENV, 'TMPDIR': str(self.scratch), 'PYTHONDONTWRITEBYTECODE': '1'}, **(env or {}))
        done = subprocess.run([sys.executable, str(self.clone / 'tools/build_edition.py'), *args], capture_output=True,
                              text=True, env=environment, cwd=cwd or self.base)
        return Run(done)

    def build(self, *args, output=None, **kwargs):
        return self.run_tool('build', '--output', str(output or self.output), *args, **kwargs)

    def report(self):
        return json.loads((self.clone / 'work/edisi-umum/LAPORAN-BUILD.json').read_text(encoding='utf-8'))

    def manifest(self, root=None):
        with (Path(root or self.output) / 'MANIFEST.csv').open(encoding='utf-8', newline='') as stream:
            return {row['relative_path']: row for row in csv.DictReader(stream)}


class EditionCase(unittest.TestCase):
    def setUp(self):
        self.fx = Fixture.fresh(self)

    def assertPass(self, run):
        self.assertEqual((run.code, run.data.get('status'), run.reason), (0, 'pass', None), run.stdout)
        self.assertEqual(list(self.fx.scratch.iterdir()), [], 'folder kerja tertinggal')

    def assertBlocked(self, run, reason):
        self.assertEqual((run.code, run.data.get('status'), run.reason), (1, 'blocked', reason), run.stdout)
        self.assertEqual(list(self.fx.scratch.iterdir()), [], 'folder kerja tertinggal')
        self.assertEqual(run.stderr, '')

    def control(self):
        """Kontrol: fixture ini lulus sebelum pemicu dipasang, dan pada folder terpisah."""
        run = self.fx.build(output=self.fx.base / 'kontrol')
        self.assertPass(run)
        return run

    def assertRejected(self, trigger, reason, *args):
        self.control()
        trigger(self.fx)
        before = tree_hash(self.fx.output)
        run = self.fx.build(*args)
        self.assertBlocked(run, reason)
        self.assertEqual(tree_hash(self.fx.output), before, 'keluaran berubah')
        return run


def _file_entry(name, content='# Isi\n'):
    def trigger(fx):
        fx.write(name, content)
        fx.entries.append(('file', name))
        fx.publish()
    return trigger


def _in_tree(name, content='# Isi\n'):
    def trigger(fx):
        fx.write(name, content)
        fx.publish()
    return trigger


def _mutate(function):
    def trigger(fx):
        fx.publish(function)
    return trigger


def _docx(members):
    stream = io.BytesIO()
    with zipfile.ZipFile(stream, 'w') as archive:
        for name, data in members.items():
            archive.writestr(name, data)
    return stream.getvalue()


def _symlink(fx):
    (fx.clone / '1 Workflow/tautan.md').symlink_to('standar.md')
    fx.publish()


def _harness_stale(fx):
    old = sha((fx.clone / 'HARNESS.md').read_bytes())
    fx.write('HARNESS.md', '# Harness sumber berubah\n')
    fx.publish(lambda config: config.update(harness_template_source_sha256=old))


def _drop_required(fx):
    fx.entries.remove(('file', 'CLAUDE.md'))
    fx.publish()


def _access_flag_without_files(fx):
    fx.publish(lambda config: config.update(publish_access_docs=True))


def _template(name, text):
    def trigger(fx):
        fx.write(name, text)
        fx.publish()
    return trigger


def _hit_with_review(lines):
    def trigger(fx):
        data = b'# T\n\nTANDA-SINTETIK\n\nTANDA-SINTETIK\n'
        fx.write('1 Workflow/tanda.md', data)
        fx.publish(lambda config: config['scan_reviews'].append(
            {'group': 'CLASS_MARK', 'source_sha256': sha(data), 'lines': lines, 'basis': 'documentation-example'}))
    return trigger


def _review_changed_hash(fx):
    fx.write('1 Workflow/tanda.md', 'TANDA-SINTETIK diubah\n')
    fx.publish(lambda config: config['scan_reviews'].append(
        {'group': 'CLASS_MARK', 'source_sha256': sha(b'lama'), 'lines': 1, 'basis': 'fixture'}))


def _review_unused(fx):
    fx.publish(lambda config: config['scan_reviews'].append(
        {'group': 'CLASS_MARK', 'source_sha256': sha(b'tidak ada'), 'lines': 1, 'basis': 'fixture'}))


def _nested_twin(fx):
    # Nama yang tidak tercantum bersarang di bawah entri yang diizinkan (ED-T-07).
    fx.write('3 Skills/kanonik/alpha/tersarang/SKILL.md', '---\nname: ditolak\ndescription: Skill ditolak.\n---\n')
    fx.publish()


def _unlisted_copy(fx):
    # Nama yang diizinkan punya kembaran yang tidak tercantum (ED-T-07).
    fx.write('3 Skills/kanonik/_salvage-profil-merge-1010/alpha/SKILL.md', '---\nname: alpha\ndescription: Kembaran.\n---\n')
    fx.publish()


def _tree_all_skills(fx):
    fx.entries.append(('tree', '3 Skills/kanonik'))
    fx.publish()


def _skill_without_description(fx):
    for copy in ('kanonik', 'registry-fleet'):
        fx.write(f'3 Skills/{copy}/alpha/SKILL.md', '---\nname: alpha\n---\n# Tanpa deskripsi\n')
    fx.publish()


def _policy_changed_one_byte(fx):
    exempt = sha((fx.clone / POLICY).read_bytes())
    fx.write(POLICY, (fx.clone / POLICY).read_bytes() + b'!')
    fx.publish(lambda config: config.update(rule_text_exempt_sha256=[exempt]))


def _pattern_file(content):
    def trigger(fx):
        path = fx.clone / 'work/edisi-umum/POLA-PINDAI.txt'
        if content is None:
            path.unlink()
        else:
            path.write_text(content, encoding='utf-8')
    return trigger


def _pin_after(change):
    def trigger(fx):
        change(fx)
        fx.commit()
    return trigger


def _missing_group():
    return ''.join(line + '\n' for line in PATTERNS.splitlines() if not line.startswith('HOST'))


CONTROL_BROKEN = PATTERNS.replace('INSTANSI-SINTETIK-[0-9]+', 'TIDAK-PERNAH-COCOK-[0-9]+')

REJECTIONS = {
    # ED-T-02: empat keadaan N-12, ditambah bentuk rusak.
    'ed_t_02_pola_hilang': (_pattern_file(None), 'pattern_file_invalid'),
    'ed_t_02_pola_kosong': (_pattern_file(''), 'pattern_file_invalid'),
    'ed_t_02_pola_kehilangan_grup': (_pattern_file(_missing_group()), 'pattern_file_invalid'),
    'ed_t_02_pola_kontrol_tidak_cocok': (_pattern_file(CONTROL_BROKEN), 'pattern_control_failed'),
    'pola_regex_rusak': (_pattern_file(PATTERNS + 'HOST\t(\n'), 'pattern_file_invalid'),
    'pola_grup_asing': (_pattern_file(PATTERNS + 'LAIN\tx\n'), 'pattern_file_invalid'),
    # ED-T-03: pin menangkap berkas ditambah, diubah, dihapus; pin tidak diperbarui.
    'ed_t_03_berkas_ditambah': (_pin_after(lambda fx: fx.write('1 Workflow/baru.md', '# Baru\n')), 'allowlist_pin_mismatch'),
    'ed_t_03_berkas_diubah': (_pin_after(lambda fx: fx.write('1 Workflow/standar.md', '# Diubah\n')), 'allowlist_pin_mismatch'),
    'ed_t_03_berkas_dihapus': (_pin_after(lambda fx: fx.remove('1 Workflow/standar.md')), 'allowlist_pin_mismatch'),
    'ed_t_03_entri_file_diubah': (_pin_after(lambda fx: fx.write('AGENTS.md', '# Diubah\n')), 'allowlist_pin_mismatch'),
    'ed_t_03_salinan_skill_diubah': (_pin_after(lambda fx: fx.write('3 Skills/kanonik/alpha/baru.md', '# B\n')), 'allowlist_pin_mismatch'),
    # ED-T-04.
    'ed_t_04_path_gov_def': (_in_tree('1 Workflow/INSTANSI-SINTETIK-9.md'), 'scan_hit'),
    'ed_t_04_zip_entri': (_file_entry('lampiran/arsip.zip', b'PK'), 'denied_type'),
    'ed_t_04_zip_dalam_pohon': (_in_tree('1 Workflow/arsip.zip', b'PK'), 'denied_type'),
    'ed_t_04_db_entri': (_file_entry('data/basis.db', b'x'), 'denied_type'),
    'ed_t_04_db_sisi_wal': (_in_tree('1 Workflow/basis.db-wal', b'x'), 'denied_type'),
    'ed_t_04_sqlite_berkedok_teks': (_in_tree('1 Workflow/data.txt', b'SQLite format 3\x00isi'), 'denied_type'),
    'ed_t_04_claude_entri': (_file_entry('.claude/x.md'), 'harness_autoload_path'),
    'ed_t_04_titik_dalam_pohon': (_in_tree('1 Workflow/.cursor-plugin/plugin.json', '{}'), 'harness_autoload_path'),
    'ed_t_04_docs': (_file_entry('docs/x.md'), 'denied_path'),
    'ed_t_04_root_skills': (_file_entry('skills/x.md'), 'reserved_root_name'),
    'autoload_bersarang': (_in_tree('1 Workflow/GEMINI.md'), 'harness_autoload_path'),
    'root_tests_tidak_ikut': (_file_entry('tests/x.md'), 'denied_path'),
    'pembangun_tidak_ikut': (_mutate(lambda config: config['entries'].append(
        {'kind': 'tree', 'path': 'tools', 'tree': '0' * 40})), 'denied_path'),
    'indeks_peran_tidak_ikut': (_file_entry('2 Roles/peran-fleet/_INDEX.md'), 'denied_path'),
    'symlink_dalam_pohon': (_symlink, 'denied_type'),
    'tabrakan_dengan_berkas_hasil': (_in_tree('1 Workflow/indeks.md'), 'path_collision'),
    # ED-T-07 dan A8.
    'ed_t_07_kembaran_tersarang': (_nested_twin, 'skill_nested_unlisted'),
    'ed_t_07_salinan_tak_tercantum': (_unlisted_copy, 'skill_copies_mismatch'),
    'a8_pohon_pengelompok': (_tree_all_skills, 'skill_nested_unlisted'),
    'skill_pada_entri_pohon': (_in_tree('1 Workflow/s/SKILL.md', '---\nname: x\ndescription: y\n---\n'), 'skill_nested_unlisted'),
    # Skema (A2, A3, A5 tertentu).
    'skema_kolom_pengecualian': (_mutate(lambda config: config.update(exclude=['x'])), 'allowlist_invalid'),
    'skema_wildcard_path': (_mutate(lambda config: config['entries'].append({'kind': 'tree', 'path': '1 *', 'tree': '0' * 40})), 'allowlist_invalid'),
    'skema_glob_berpath': (_mutate(lambda config: config['drop_globs'].append('a/b*')), 'allowlist_invalid'),
    'skema_ekstensi_skrip': (_mutate(lambda config: config['admitted_extensions'].append('.py')), 'allowlist_invalid'),
    'skema_tinjauan_gov_def': (_mutate(lambda config: config['scan_reviews'].append(
        {'group': 'GOV_DEF', 'source_sha256': '0' * 64, 'lines': 1, 'basis': 'fixture'})), 'allowlist_invalid'),
    'skema_tinjauan_berpath': (_mutate(lambda config: config['scan_reviews'].append(
        {'group': 'HOST', 'source_sha256': '0' * 64, 'lines': 1, 'basis': 'fixture', 'path': 'x'})), 'allowlist_invalid'),
    'skema_berkas_hasil_pada_entri': (_mutate(lambda config: config['entries'].append({'kind': 'file', 'path': 'README.md', 'blob': '0' * 40})), 'allowlist_invalid'),
    'skema_versi': (_mutate(lambda config: config.update(schema_version=2)), 'allowlist_invalid'),
    'isian_tak_dikenal': (_template('edisi-umum/HALAMAN-DEPAN.md.tmpl', '# E\n\n{{LAIN}}\n'), 'allowlist_invalid'),
    'stempel_bertaut': (_template('edisi-umum/STEMPEL.txt', '> library-edition-stamp:v1 [a](b.md)\n'), 'allowlist_invalid'),
    'stempel_empat_baris': (_template('edisi-umum/STEMPEL.txt', '> library-edition-stamp:v1\n> a\n> b\n> c\n'), 'allowlist_invalid'),
    'stempel_tanpa_pengenal': (_template('edisi-umum/STEMPEL.txt', '> tanpa pengenal\n'), 'allowlist_invalid'),
    # A5 dan gagal tertutup approval.
    'approval_tidak_ada': (_mutate(lambda config: config.pop('approval')), 'allowlist_not_approved'),
    'approval_bukan_approved': (_mutate(lambda config: config['approval'].update(status='draft')), 'allowlist_not_approved'),
    # Kehadiran dan templat.
    'wajib_hilang': (_drop_required, 'required_file_missing'),
    'bendera_akses_tanpa_berkas': (_access_flag_without_files, 'required_file_missing'),
    'penunjuk_tanpa_bendera': (_file_entry('TEMPLAT-PENUNJUK.md'), 'required_file_missing'),
    'templat_harness_basi': (_harness_stale, 'harness_template_stale'),
    'tautan_templat_rusak': (_template('edisi-umum/HARNESS-EDISI.md.tmpl', '# H\n\n[x](tidak-ada.md)\n'), 'template_link_broken'),
    # Isi yang tidak dapat dipindai.
    'biner_nul': (_in_tree('1 Workflow/data.txt', b'a\x00b'), 'binary_not_scannable'),
    'teks_bukan_utf8': (_in_tree('1 Workflow/data.csv', b'\xff\xfe'), 'binary_not_scannable'),
    'ooxml_media': (_in_tree('1 Workflow/d.docx', _docx({'word/document.xml': '<a/>', 'word/media/g.png': b'x'})), 'binary_not_scannable'),
    'ooxml_rusak': (_in_tree('1 Workflow/d.docx', b'bukan zip'), 'binary_not_scannable'),
    'frontmatter_tak_tertutup': (_in_tree('1 Workflow/f.md', '---\nname: x\n# isi\n'), 'frontmatter_unclosed'),
    'tr_18_frontmatter_bom': (_in_tree('1 Workflow/f.md', b'\xef\xbb\xbf---\nname: x\n---\n# isi\n'), 'frontmatter_bom'),
    # Pemindaian isi.
    'isi_gov_def': (_in_tree('1 Workflow/g.md', 'INSTANSI-SINTETIK-3\n'), 'scan_hit'),
    'isi_grup_tanpa_tinjauan': (_in_tree('1 Workflow/g.md', 'TANDA-SINTETIK\n'), 'scan_hit'),
    'isi_ooxml_terpecah_tag': (_in_tree('1 Workflow/d.docx', _docx({'word/document.xml': '<t>TANDA-</t><t>SINTETIK</t>'})), 'scan_hit'),
    'isi_berkas_hasil': (_template('edisi-umum/HARNESS-EDISI.md.tmpl', '# H\n\nHOST-SINTETIK\n'), 'scan_hit'),
    'isi_daftar_izin': (_mutate(lambda config: config['drop_globs'].append('INSTANSI-SINTETIK-1*')), 'scan_hit'),
    'rule_text_di_luar_n03': (_in_tree('1 Workflow/r.md', 'Aturan Sintetik Ganda\n'), 'scan_hit'),
    'tr_13_n03_berubah_satu_byte': (_policy_changed_one_byte, 'scan_hit'),
    'tinjauan_jumlah_baris_berubah': (_hit_with_review(1), 'scan_review_stale'),
    'tinjauan_hash_berubah': (_review_changed_hash, 'scan_review_stale'),
    'tinjauan_tak_terpakai': (_review_unused, 'scan_review_unused'),
    # Gerbang turunan (RK-21) dan peran tertolak (RK-20).
    'turunan_nama_berkas_pada_isi': (_in_tree('1 Workflow/n.md', 'lihat catatan-perkara-sintetik di sini\n'), 'derived_name_hit'),
    'turunan_nilai_perkara_pada_isi': (_in_tree('1 Workflow/n.md', 'tentang perkara sintetik beta.\n'), 'derived_name_hit'),
    'turunan_target_tersandi': (_in_tree('1 Workflow/n.md', '[a](Perkara%20Sintetik%20Beta.md)\n'), 'derived_name_hit'),
    'turunan_pada_path': (_in_tree('1 Workflow/catatan-perkara-sintetik.md'), 'derived_name_hit'),
    # Katalog dan tautan.
    'idx_04_deskripsi_hilang': (_skill_without_description, 'catalog_schema'),
    'tautan_rusak_berhenti_di_check': (_in_tree('1 Workflow/t.md', '[a](tidak-ada-di-sumber.md)\n'), 'check_failed'),
    'jangkar_rusak_berhenti_di_check': (_in_tree('1 Workflow/t.md', '[a](standar.md#tidak-ada)\n'), 'check_failed'),
}


class Rejections(EditionCase):
    """Satu uji per pemicu; kontrol dan pemicu memakai fixture yang sama."""


def _make_rejection_test(trigger, reason):
    def test(self):
        self.assertRejected(trigger, reason)
    return test


for _name, (_trigger, _reason) in REJECTIONS.items():
    setattr(Rejections, f'test_{_name}', _make_rejection_test(_trigger, _reason))


class OutputLocation(EditionCase):
    """Tahap 1 dan N-83: keluaran di luar clone, dan folder asing tidak disentuh."""

    def assertOutputRefused(self, output):
        self.control()
        before = tree_hash(output)
        self.assertBlocked(self.fx.build(output=output), 'output_not_allowed')
        self.assertEqual(tree_hash(output), before)

    def test_di_dalam_clone(self):
        self.assertOutputRefused(self.fx.clone / 'work/edisi')

    def test_memuat_clone(self):
        self.assertOutputRefused(self.fx.base)

    def test_clone_sendiri(self):
        self.assertOutputRefused(self.fx.clone)

    def test_kapitalisasi_berbeda_pada_sistem_berkas_tak_peka(self):
        flipped = Path(str(self.fx.clone).swapcase())
        if not flipped.exists():
            self.skipTest('sistem berkas peka kapitalisasi')
        self.assertOutputRefused(flipped / 'edisi')

    def test_folder_asing_tidak_kosong(self):
        write_file(self.fx.output, 'milik-orang.txt', 'x')
        self.assertOutputRefused(self.fx.output)

    def test_edisi_lain_ditolak(self):
        write_file(self.fx.output, 'library.json', json.dumps({'edition': {'id': 'lain'}}))
        self.assertOutputRefused(self.fx.output)

    def test_keluaran_berkas(self):
        write_file(self.fx.output.parent, self.fx.output.name, 'x')
        self.control()
        self.assertBlocked(self.fx.build(), 'output_not_allowed')

    def test_n83_berupa_clone(self):
        renamed = self.fx.base / 'kembar.pohon-lama'
        self.fx.clone.rename(renamed)
        self.fx.clone = renamed
        self.assertOutputRefused(self.fx.base / 'kembar')

    def test_n83_berkas_memberi_output_not_allowed(self):
        self.assertPass(self.fx.build())
        before = tree_hash(self.fx.output)
        holder = Path(str(self.fx.output) + '.pohon-lama')
        holder.write_text('x')
        self.assertBlocked(self.fx.build(), 'output_not_allowed')
        self.assertEqual(tree_hash(self.fx.output), before)
        holder.unlink()
        self.assertPass(self.fx.build())

    def test_n83_tidak_dapat_ditulis_memberi_output_not_allowed(self):
        self.assertPass(self.fx.build())
        before = tree_hash(self.fx.output)
        holder = Path(str(self.fx.output) + '.pohon-lama')
        holder.mkdir()
        holder.chmod(stat.S_IRUSR | stat.S_IXUSR)
        self.addCleanup(holder.chmod, stat.S_IRWXU)
        if os.access(holder, os.W_OK):
            self.skipTest('izin folder tidak ditegakkan untuk pengguna ini')
        self.assertBlocked(self.fx.build(), 'output_not_allowed')
        self.assertEqual(tree_hash(self.fx.output), before)
        holder.chmod(stat.S_IRWXU)
        self.assertPass(self.fx.build())

    def test_tanpa_output_keluar_dua_dan_menganjurkan_nama(self):
        run = self.fx.run_tool('build')
        self.assertEqual(run.code, 2)
        self.assertEqual(run.data['recommended_folder_name'], 'ai-knowledge-library-edisi-umum')

    def test_bendera_pelonggar_tidak_ada(self):
        for flag in ('--no-scan', '--force', '--patterns=x'):
            with self.subTest(flag=flag):
                self.assertEqual(self.fx.build(flag).code, 2)

    def test_ref_tidak_valid(self):
        self.control()
        self.assertBlocked(self.fx.build('--source-ref', 'tidak-ada'), 'source_ref_invalid')
        self.assertBlocked(self.fx.build('--source-ref=--all'), 'source_ref_invalid')


class Stage11(EditionCase):
    """RK-49, TR-23: pohon lama ke N-83, `.git/` tetap, tidak pernah dihapus, pulih bila gagal."""

    def holder(self):
        return Path(str(self.fx.output) + '.pohon-lama')

    def rebuild_source(self):
        self.fx.write('1 Workflow/standar.md', '# Standar versi berikutnya\n')
        self.fx.publish()

    def test_pohon_lama_pindah_dan_git_tetap(self):
        self.assertPass(self.fx.build())
        old_hash = tree_hash(self.fx.output)
        old_commit = json.loads((self.fx.output / 'library.json').read_text())['edition']['source_commit']
        run_git(self.fx.output, 'init', '-q', '-b', 'main')
        run_git(self.fx.output, 'add', '-A')
        run_git(self.fx.output, 'commit', '-q', '-m', 'edisi')
        head = run_git(self.fx.output, 'rev-parse', 'HEAD').stdout
        self.rebuild_source()
        self.assertPass(self.fx.build())
        self.assertEqual(run_git(self.fx.output, 'rev-parse', 'HEAD').stdout, head)
        slot = self.holder() / f'{old_commit[:7]}-01'
        self.assertEqual(tree_hash(slot), old_hash)
        self.assertFalse((slot / '.git').exists())
        self.assertIn(b'versi berikutnya', (self.fx.output / '1 Workflow/standar.md').read_bytes())
        self.assertEqual(shipped_check(self.fx.output).returncode, 0)

    def test_n83_tidak_pernah_ditimpa(self):
        self.assertPass(self.fx.build())
        short = json.loads((self.fx.output / 'library.json').read_text())['edition']['source_commit'][:7]
        write_file(self.holder(), f'{short}-01/penanda.txt', 'milik pemilik')
        marker = self.holder() / f'{short}-01/penanda.txt'
        self.assertPass(self.fx.build())
        self.assertEqual(marker.read_text(), 'milik pemilik')
        self.assertEqual(sorted(path.name for path in self.holder().iterdir()), [f'{short}-01', f'{short}-02'])
        self.assertPass(self.fx.build())
        self.assertEqual(sorted(path.name for path in self.holder().iterdir()), [f'{short}-01', f'{short}-02', f'{short}-03'])

    def test_build_pertama_tanpa_n83(self):
        self.assertPass(self.fx.build())
        self.assertFalse(self.holder().exists())

    def test_dry_run_tidak_menulis(self):
        self.assertPass(self.fx.build('--dry-run'))
        self.assertFalse(self.fx.output.exists())
        self.assertPass(self.fx.build())
        before = tree_hash(self.fx.output)
        self.rebuild_source()
        self.assertPass(self.fx.build('--dry-run'))
        self.assertEqual(tree_hash(self.fx.output), before)
        self.assertFalse(self.holder().exists())

    def fail_on_call(self, number):
        """Gagalkan pemindahan ke-`number`, lalu buktikan pohon lama utuh dan `check` lulus (TR-23)."""
        self.assertPass(self.fx.build())
        before = tree_hash(self.fx.output)
        run_git(self.fx.output, 'init', '-q', '-b', 'main')
        git_marker = (self.fx.output / '.git/HEAD').read_bytes()
        self.rebuild_source()
        module = load_builder(self.fx.clone)
        real, calls = module._move, []

        def failing(source, target):
            calls.append(source)
            if len(calls) == number:
                raise OSError('gagal disengaja')
            real(source, target)
        stdout = io.StringIO()
        with mock.patch.object(module, '_move', failing), contextlib.redirect_stdout(stdout):
            code = module.main(['build', '--output', str(self.fx.output)])
        data = json.loads(stdout.getvalue())
        self.assertEqual((code, data['reason'], data['restored']), (1, 'output_not_allowed', True))
        self.assertEqual(len(calls), number)
        self.assertEqual(tree_hash(self.fx.output), before)
        self.assertEqual((self.fx.output / '.git/HEAD').read_bytes(), git_marker)
        self.assertEqual(list(self.holder().iterdir()), [])
        done = shipped_check(self.fx.output)
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertPass(self.fx.build())
        self.assertIn(b'versi berikutnya', (self.fx.output / '1 Workflow/standar.md').read_bytes())
        return calls

    def test_tr_23_gagal_pada_pemindahan_pertama(self):
        self.fail_on_call(1)

    def test_tr_23_gagal_di_tengah_pohon_lama(self):
        self.fail_on_call(3)

    def test_tr_23_gagal_di_tengah_pohon_baru(self):
        # Root edisi fixture memuat 12 entri selain `.git`, jadi panggilan ke-14 berada pada pohon baru.
        calls = self.fail_on_call(14)
        self.assertEqual(sum(1 for source in calls if Path(source).parent.name == 'pohon'), 2)

    def test_tr_23_gagal_pada_build_pertama_tidak_menyisakan_keluaran(self):
        module = load_builder(self.fx.clone)

        def failing(source, target):
            raise OSError('gagal disengaja')
        stdout = io.StringIO()
        with mock.patch.object(module, '_move', failing), contextlib.redirect_stdout(stdout):
            self.assertEqual(module.main(['build', '--output', str(self.fx.output)]), 1)
        self.assertFalse(self.fx.output.exists())
        self.assertPass(self.fx.build())


class Shape(EditionCase):
    """Bentuk hasil: stempel, manifest, library.json, berkas titik, keluaran terkendali."""

    def built(self):
        run = self.fx.build()
        self.assertPass(run)
        return run

    def test_ed_t_05_dua_build_identik_dan_tanpa_path_absolut(self):
        first = self.fx.base / 'pertama'
        second = self.fx.base / 'kedua folder'
        self.assertPass(self.fx.build(output=first, env={'PYTHONHASHSEED': '1', 'LC_ALL': 'C'}))
        self.assertPass(self.fx.build(output=second, env={'PYTHONHASHSEED': '7'}, cwd=self.fx.clone))
        self.assertEqual(tree_hash(first), tree_hash(second))
        for path in first.rglob('*'):
            if path.is_file():
                data = path.read_bytes()
                self.assertNotIn(str(first).encode(), data)
                self.assertNotIn(str(self.fx.clone).encode(), data)
                self.assertEqual(stat.S_IMODE(path.stat().st_mode), 0o644)

    def test_ed_4_pohon_kerja_tidak_dibaca(self):
        self.fx.write('1 Workflow/standar.md', '# Kotor INSTANSI-SINTETIK-1\n')
        self.fx.write('1 Workflow/tak-terlacak.md', '# Tak terlacak\n')
        self.fx.write(ALLOWLIST, 'rusak')
        self.fx.write('edisi-umum/STEMPEL.txt', 'rusak')
        self.built()
        self.assertNotIn(b'Kotor', (self.fx.output / '1 Workflow/standar.md').read_bytes())
        self.assertFalse((self.fx.output / '1 Workflow/tak-terlacak.md').exists())

    def test_stempel_rk_05_rk_39_tiap_md_dan_kembali_ke_sumber(self):
        data = b'---\nname: x\n---\n# Isi\n'
        crlf = b'---\r\nname: x\r\n---\r\n# Isi\r\n'
        double_cr = b'---\r\r\nname: x\r\r\n---\r\r\n# Isi\r\r\n'
        plain = b'# Tanpa frontmatter\n'
        for name, content in {'a.md': data, 'b.md': crlf, 'c.md': double_cr, 'd.md': plain}.items():
            self.fx.write(f'1 Workflow/{name}', content)
        self.fx.publish()
        self.built()
        manifest = self.fx.manifest()
        block_lf, block_crlf = STAMP_BLOCK, STAMP_BLOCK.replace(b'\n', b'\r\n')
        self.assertEqual((self.fx.output / '1 Workflow/a.md').read_bytes(), b'---\nname: x\n---\n' + block_lf + b'# Isi\n')
        self.assertEqual((self.fx.output / '1 Workflow/b.md').read_bytes(), b'---\r\nname: x\r\n---\r\n' + block_crlf + b'# Isi\r\n')
        self.assertEqual((self.fx.output / '1 Workflow/d.md').read_bytes(), block_lf + plain)
        stamped = 0
        for name, row in manifest.items():
            if not name.endswith('.md'):
                continue
            body = (self.fx.output / name).read_bytes()
            self.assertIn(b'library-edition-stamp:v1', body, name)
            stamped += 1
            if row['source_sha256']:
                for block in (block_crlf, block_lf):
                    if block in body:
                        self.assertEqual(sha(body.replace(block, b'', 1)), row['source_sha256'], name)
                        break
                else:
                    self.fail(name)
        self.assertGreater(stamped, 8)

    def test_tinggi_stempel_tetap(self):
        self.built()
        body = (self.fx.output / '1 Workflow/standar.md').read_text(encoding='utf-8').split('\n')
        self.assertEqual(body[3], '')
        self.assertEqual(body[4], '# Standar')

    def test_ed_t_08_library_json_dan_manifest(self):
        run = self.built()
        config = json.loads((self.fx.output / 'library.json').read_text(encoding='utf-8'))
        self.assertEqual(set(config['edition']), {'schema_version', 'id', 'source_commit', 'allowlist_sha256', 'expected_missing'})
        self.assertEqual(config['edition']['id'], 'edisi-umum')
        self.assertEqual(config['edition']['source_commit'], self.fx.git('rev-parse', 'HEAD'))
        self.assertEqual(config['edition']['allowlist_sha256'], sha((self.fx.clone / ALLOWLIST).read_bytes()))
        self.assertEqual(run.data['allowlist_sha256'], config['edition']['allowlist_sha256'])
        self.assertEqual(config['repository_urls'], [])
        self.assertEqual(sorted(config['roots']), ['registry', 'skills', 'workflow'])
        self.assertEqual([alias['source'] for alias in config['aliases']], ['alur'])
        self.assertNotIn('catalogs', config)
        self.assertEqual(config['manifest_roots'], ['1 Workflow', '3 Skills', 'tools'])
        first = (self.fx.output / 'MANIFEST.csv').read_text(encoding='utf-8').splitlines()[0]
        self.assertEqual(first, 'relative_path,bytes,sha256,source_sha256')
        manifest = self.fx.manifest()
        self.assertEqual(manifest['tools/library.py']['source_sha256'], manifest['tools/library.py']['sha256'])
        self.assertEqual(manifest['tools/library.py']['sha256'], sha((self.fx.clone / 'tools/library.py').read_bytes()))
        self.assertEqual(manifest['README.md']['source_sha256'], '')
        self.assertEqual(manifest['library.json']['source_sha256'], '')
        self.assertEqual(manifest['AGENTS.md']['source_sha256'], sha((self.fx.clone / 'AGENTS.md').read_bytes()))
        self.assertNotIn('MANIFEST.csv', manifest)

    def test_rk_04_rk_14_rk_02_isi_terlarang_dan_berkas_titik(self):
        self.built()
        names = {path.relative_to(self.fx.output).as_posix() for path in self.fx.output.rglob('*') if path.is_file()}
        self.assertEqual({name for name in names if name.startswith('.')}, {'.gitignore', '.gitattributes'})
        self.assertEqual((self.fx.output / '.gitattributes').read_bytes(), b'* -text\n')
        self.assertEqual({name for name in names if name.startswith('tests/')}, set())
        self.assertEqual({name for name in names if name.startswith('edisi-umum/') or name.startswith('work/')}, set())
        self.assertNotIn('tools/build_edition.py', names)
        for name in names:
            self.assertNotIn(b'hold_sha256', (self.fx.output / name).read_bytes(), name)
        for required in ('HARNESS.md', 'AGENTS.md', 'CLAUDE.md', POLICY, 'tools/library.py'):
            self.assertIn(required, names)
        self.assertEqual((self.fx.output / 'tools/library.py').read_bytes(), (self.fx.clone / 'tools/library.py').read_bytes())

    def test_kontrak_n47_baris_koleksi(self):
        self.built()
        text = (self.fx.output / 'README.md').read_text(encoding='utf-8')
        self.assertIn('| [1 Workflow](1%20Workflow/INDEKS.md) | 2 |', text)
        self.assertIn('| [3 Skills](3%20Skills/INDEKS.md) |', text)
        self.assertNotIn('tools/INDEKS.md', text)
        self.assertIn(self.fx.git('rev-parse', 'HEAD'), text)
        self.assertNotIn('{{', text)
        lines = text.split('\n')
        start = lines.index('| Koleksi | Berkas |') + 2
        self.assertTrue(lines[start].startswith('| ['))
        self.assertTrue(lines[start + 1].startswith('| ['))
        self.assertEqual(lines[start + 2], '')

    def test_indeks_tidak_membaca_sumber_dan_tautan_persen(self):
        self.fx.write('1 Workflow/INDEKS.md', '# Sumber memuat HOST-SINTETIK\n')
        self.fx.publish()
        self.built()
        text = (self.fx.output / '1 Workflow/INDEKS.md').read_text(encoding='utf-8')
        self.assertIn('| [standar.md](standar.md) |', text)
        self.assertNotIn('HOST-SINTETIK', text)
        skills = (self.fx.output / '3 Skills/INDEKS.md').read_text(encoding='utf-8')
        self.assertIn('kanonik/alpha/SKILL.md', skills)
        self.assertNotIn('rujukan.md', skills)

    def test_skrip_dalam_skill_tidak_tersalin_library_tersalin(self):
        """G43-06: tiap ekstensi skrip; kontrol `.md` pada folder yang sama tersalin."""
        for copy in ('kanonik', 'registry-fleet'):
            for suffix in SCRIPT_SUFFIXES:
                self.fx.write(f'3 Skills/{copy}/alpha/scripts/alat{suffix}', '# skrip\n')
            self.fx.write(f'3 Skills/{copy}/alpha/scripts/catatan.md', '# Catatan\n')
        self.fx.publish()
        self.built()
        names = [path.relative_to(self.fx.output).as_posix() for path in self.fx.output.rglob('*') if path.is_file()]
        self.assertEqual([name for name in names if name.endswith(SCRIPT_SUFFIXES)], ['tools/library.py'])
        self.assertTrue((self.fx.output / '3 Skills/kanonik/alpha/scripts/catatan.md').is_file())
        self.assertEqual(shipped_check(self.fx.output).returncode, 0)

    def test_tinjauan_sah_meloloskan_dan_turunan_dapat_ditinjau(self):
        data = b'TANDA-SINTETIK\n\nTANDA-SINTETIK\n'
        derived = b'lihat catatan-perkara-sintetik\n'
        self.fx.write('1 Workflow/tanda.md', data)
        self.fx.write('1 Workflow/n.md', derived)
        self.fx.publish(lambda config: config['scan_reviews'].extend([
            {'group': 'CLASS_MARK', 'source_sha256': sha(data), 'lines': 2, 'basis': 'documentation-example'},
            {'group': 'DERIVED_NAME', 'source_sha256': sha(derived), 'lines': 1, 'basis': 'generic-word'}]))
        self.built()

    def test_tr_13_n03_berstempel_lulus_dengan_hash_sumber(self):
        run = self.built()
        self.assertEqual(run.data['status'], 'pass')
        policy = (self.fx.output / POLICY).read_bytes()
        self.assertIn(b'Aturan Sintetik Ganda', policy)
        self.assertNotEqual(sha(policy), sha((self.fx.clone / POLICY).read_bytes()))

    def test_tr_13_hash_akhir_bukan_pengecualian(self):
        self.control()
        policy = STAMP_BLOCK + (self.fx.clone / POLICY).read_bytes()
        self.fx.publish(lambda config: config.update(rule_text_exempt_sha256=[sha(policy)]))
        self.assertBlocked(self.fx.build(), 'scan_hit')

    def test_rk_20_peran_tertolak(self):
        self.fx.write('2 Roles/peran-fleet/peran-ditolak.md', '# Peran\n')
        self.fx.write('1 Workflow/s.md', 'menyebut peran-ditolak.\n')
        self.fx.publish()
        run = self.built()
        self.assertEqual(run.data['rejected_role_mentions'], 1)
        self.fx.write('edisi-umum/HARNESS-EDISI.md.tmpl', '# H\n\nperan-ditolak\n')
        self.fx.publish()
        self.assertBlocked(self.fx.build(), 'derived_name_hit')

    def test_approval_tidak_ada_boleh_dry_run(self):
        self.fx.publish(lambda config: config.pop('approval'))
        self.assertPass(self.fx.build('--dry-run'))
        self.assertBlocked(self.fx.build(), 'allowlist_not_approved')
        self.assertFalse(self.fx.output.exists())


class SourceRef(EditionCase):
    """TR-14: hasil mengikuti blob pada ref; tahap 10 menjalankan berkas yang dikirim."""

    BROKEN = "if __name__ == '__main__':\n    sys.exit(1)\n"

    def broken_resolver(self):
        text = (self.fx.clone / 'tools/library.py').read_text(encoding='utf-8')
        marker = "if __name__ == '__main__':"
        self.assertEqual(text.count(marker), 1)
        return text.replace(marker, self.BROKEN + marker)

    def test_resolver_rusak_di_pohon_kerja_diabaikan(self):
        self.fx.write('tools/library.py', self.broken_resolver())
        run = self.fx.build()
        self.assertPass(run)
        shipped = run_git(self.fx.clone, 'show', 'HEAD:tools/library.py').stdout
        self.assertEqual((self.fx.output / 'tools/library.py').read_bytes(), shipped)

    def test_resolver_rusak_pada_blob_memberi_check_failed(self):
        self.control()
        self.fx.write('tools/library.py', self.broken_resolver())
        self.fx.publish()
        self.assertBlocked(self.fx.build(), 'check_failed')

    def test_ref_lama_mengikuti_blob_lama(self):
        good = self.fx.git('rev-parse', 'HEAD')
        good_resolver = (self.fx.clone / 'tools/library.py').read_bytes()
        self.fx.write('tools/library.py', self.broken_resolver())
        self.fx.write('1 Workflow/standar.md', '# Versi baru\n')
        self.fx.publish()
        self.assertBlocked(self.fx.build(), 'check_failed')
        run = self.fx.build('--source-ref', good)
        self.assertPass(run)
        self.assertEqual(run.data['source_commit'], good)
        self.assertEqual((self.fx.output / 'tools/library.py').read_bytes(), good_resolver)
        self.assertNotIn(b'Versi baru', (self.fx.output / '1 Workflow/standar.md').read_bytes())

    def test_rk_35_tahap_10_terisolasi(self):
        """Resolver yang menuntut `-I` lulus; bila tahap 10 tidak terisolasi build berhenti."""
        text = (self.fx.clone / 'tools/library.py').read_text(encoding='utf-8')
        marker = "if __name__ == '__main__':"
        self.fx.write('tools/library.py', text.replace(marker, marker + "\n    if not sys.flags.isolated:\n        sys.exit(1)"))
        self.fx.publish()
        self.assertPass(self.fx.build())


class ExpectedMissing(EditionCase):
    """RK-11, dua arah: tautan ke berkas tertolak diterima, selisih jumlah ke arah mana pun menggagalkan."""

    def linked(self):
        self.fx.write('1 Workflow/tautan.md', '\n'.join([
            '[tertolak](../5%20Integration/lokal.md)',
            '[alias hilang](integrasi/lokal.md)',
            '[alias ada](alur/standar.md)',
            '[lokal](standar.md#standar)',
            '[luar](https://contoh.test/lain)',
            '[url repo](https://contoh.test/pustaka/blob/main/5%20Integration/lokal.md)',
            '`[kode](tidak-dihitung.md)`',
            '']))
        self.fx.publish()

    def test_tertolak_dihitung_dan_check_lulus(self):
        self.linked()
        run = self.fx.build()
        self.assertPass(run)
        self.assertEqual(run.data['expected_missing'], 2)
        self.assertEqual(json.loads((self.fx.output / 'library.json').read_text())['edition']['expected_missing'], 2)
        done = shipped_check(self.fx.output)
        self.assertEqual(done.returncode, 0, done.stdout)
        self.assertEqual(json.loads(done.stdout)['links']['missing'], 2)
        resolved = subprocess.run([sys.executable, '-I', str(self.fx.output / 'tools/library.py'), 'resolve', '../5%20Integration/lokal.md',
                                   '--from', '1 Workflow/tautan.md', '--json'], capture_output=True, text=True)
        self.assertEqual(json.loads(resolved.stdout)['reason'], 'not_in_clone')

    def test_tautan_skrip_yang_tidak_tersalin_dihitung(self):
        for copy in ('kanonik', 'registry-fleet'):
            self.fx.write(f'3 Skills/{copy}/alpha/scripts/alat.py', '# skrip\n')
            self.fx.write(f'3 Skills/{copy}/alpha/references/rujukan.md', '[alat](../scripts/alat.py)\n')
        self.fx.publish()
        run = self.fx.build()
        self.assertPass(run)
        self.assertEqual(run.data['expected_missing'], 2)

    def test_arah_kurang_target_tidak_ada_di_sumber(self):
        self.control()
        self.fx.write('1 Workflow/t.md', '[a](tidak-ada-di-sumber.md)\n')
        self.fx.publish()
        self.assertBlocked(self.fx.build(), 'check_failed')
        reasons = {row.get('reason') for row in self.fx.report()['details']}
        self.assertIn('expected_missing_mismatch', reasons)

    def in_process(self, patch_name, replacement):
        module = load_builder(self.fx.clone)
        stdout = io.StringIO()
        with mock.patch.object(module, patch_name, replacement(module)), contextlib.redirect_stdout(stdout):
            code = module.main(['build', '--output', str(self.fx.output)])
        return code, json.loads(stdout.getvalue())

    def test_arah_kurang_kesalahan_build_berkas_izin_tidak_tertulis(self):
        """Hitungan dari N-08 dan sumber: berkas izin yang gagal ditulis tidak dimaafkan sebagai tertolak."""
        # Berkas referensi skill tidak tercantum pada INDEKS, jadi hanya hitungan ini yang dapat menangkapnya.
        target = '3 Skills/kanonik/alpha/references/rujukan.md'
        for copy in ('kanonik', 'registry-fleet'):
            self.fx.write(f'3 Skills/{copy}/alpha/SKILL.md',
                          '---\nname: alpha\ndescription: Skill.\n---\n[r](references/rujukan.md)\n')
        self.fx.publish()
        self.assertPass(self.fx.build(output=self.fx.base / 'kontrol'))

        def replacement(module):
            original = module.write_file

            def skip(tree, name, data):
                if name != target:
                    original(tree, name, data)
            return skip
        code, data = self.in_process('write_file', replacement)
        self.assertEqual((code, data['reason']), (1, 'check_failed'))
        self.assertIn('expected_missing_mismatch', {row.get('reason') for row in self.fx.report()['details']})
        self.assertFalse(self.fx.output.exists())

    def test_arah_lebih_hitungan_terlalu_besar(self):
        self.control()

        def replacement(module):
            original = module.count_expected_missing
            return lambda *args: original(*args) + 1
        code, data = self.in_process('count_expected_missing', replacement)
        self.assertEqual((code, data['reason']), (1, 'check_failed'))
        self.assertIn('expected_missing_mismatch', {row.get('reason') for row in self.fx.report()['details']})

    def test_check_edisi_gagal_dua_arah_setelah_angka_diubah(self):
        self.linked()
        self.assertPass(self.fx.build())
        path = self.fx.output / 'library.json'
        original = json.loads(path.read_text())
        for delta in (1, -1):
            with self.subTest(delta=delta):
                changed = json.loads(json.dumps(original))
                changed['edition']['expected_missing'] += delta
                path.write_text(json.dumps(changed))
                done = shipped_check(self.fx.output)
                self.assertEqual(done.returncode, 1)
                self.assertIn('expected_missing_mismatch', {row.get('reason') for row in json.loads(done.stdout)['failures']})

    def test_idx_11_mutasi_manifest(self):
        self.assertPass(self.fx.build())
        path = self.fx.output / '3 Skills/KATALOG.jsonl'
        path.write_bytes(path.read_bytes() + b'\n')
        done = shipped_check(self.fx.output)
        self.assertEqual(done.returncode, 1)
        self.assertIn('manifest_mismatch', {row.get('reason') for row in json.loads(done.stdout)['failures']})


class Catalog(EditionCase):
    """N-05 per target; IDX-04 dan IDX-12 pada N-19 menurut RK-12."""

    def catalog(self, root=None):
        lines = (Path(root or self.fx.output) / '3 Skills/KATALOG.jsonl').read_text(encoding='utf-8').splitlines()
        return json.loads(lines[0]), [json.loads(line) for line in lines[1:]]

    def test_idx_04_mutasi_catalog_schema(self):
        module = load_builder(self.fx.clone)
        path = '3 Skills/kanonik/alpha/SKILL.md'
        row = {'name': 'alpha', 'description': 'd', 'path': path, 'content_diff': False, 'instruction_authority': 'none'}
        names = {path, '3 Skills/kanonik/beta/SKILL.md', '3 Skills/kanonik/fixtures/x/SKILL.md'}
        good = module.render_catalog([row])
        module.validate_catalog(good, names)

        def lines(*rows):
            return ''.join(json.dumps(item, separators=(',', ':')) + '\n' for item in rows)
        head = {'catalog_schema_version': 1, 'rows': 1}
        mutations = {
            'bukan_json': good[:-2] + '\n',
            'tanpa_akhir_baris': good[:-1],
            'versi_kepala': lines({'catalog_schema_version': 2, 'rows': 1}, row),
            'kepala_berkunci_lain': lines({'catalog_schema_version': 1, 'rows': 1, 'x': 1}, row),
            'rows_salah': lines({'catalog_schema_version': 1, 'rows': 2}, row),
            'kolom_hilang': lines(head, {key: row[key] for key in row if key != 'content_diff'}),
            'kolom_tambahan': lines(head, {**row, 'known_issue': ''}),
            'urutan_kolom': lines(head, dict(reversed(list(row.items())))),
            'wewenang_lain': lines(head, {**row, 'instruction_authority': 'full'}),
            'tipe_content_diff': lines(head, {**row, 'content_diff': 'false'}),
            'deskripsi_kosong': lines(head, {**row, 'description': ''}),
            'deskripsi_panjang': lines(head, {**row, 'description': 'd' * 121}),
            'path_tidak_ada': lines(head, {**row, 'path': '3 Skills/kanonik/lain/SKILL.md'}),
            'path_di_luar_salinan': lines(head, {**row, 'path': 'AGENTS.md'}),
            'path_fixture': lines(head, {**row, 'path': '3 Skills/kanonik/fixtures/x/SKILL.md'}),
            'nama_ganda': lines({'catalog_schema_version': 1, 'rows': 2}, row, row),
            'nama_tak_urut': lines({'catalog_schema_version': 1, 'rows': 2}, {**row, 'name': 'beta'}, row),
        }
        for label, text in mutations.items():
            with self.subTest(label):
                with self.assertRaises(module.Blocked) as caught:
                    module.validate_catalog(text, names)
                self.assertEqual(caught.exception.reason, 'catalog_schema')
        with self.assertRaises(module.Blocked) as caught:
            module.validate_catalog(good + ' ' * 50000, names)
        self.assertEqual(caught.exception.reason, 'catalog_oversize')

    def test_idx_12_tanpa_2_roles(self):
        self.assertPass(self.fx.build())
        self.assertFalse((self.fx.output / '2 Roles').exists())
        self.assertEqual(self.catalog()[0], {'catalog_schema_version': 1, 'rows': 1})
        self.assertEqual(shipped_check(self.fx.output).returncode, 0)

    def test_idx_12_tanpa_3_skills(self):
        self.fx.remove('3 Skills')
        self.fx.skills = {}
        self.fx.publish()
        self.assertPass(self.fx.build())
        self.assertEqual(self.catalog(), ({'catalog_schema_version': 1, 'rows': 0}, []))
        self.assertTrue((self.fx.output / '3 Skills/INDEKS.md').is_file())
        config = json.loads((self.fx.output / 'library.json').read_text())
        self.assertNotIn('skills', config['roots'])
        done = shipped_check(self.fx.output)
        self.assertEqual(done.returncode, 0, done.stdout)

    def test_idx_12_dua_peran(self):
        for name in ('peran-a', 'peran-b'):
            self.fx.write(f'2 Roles/peran-fleet/{name}.md', f'# {name}\n')
            self.fx.entries.append(('file', f'2 Roles/peran-fleet/{name}.md'))
        self.fx.publish()
        self.assertPass(self.fx.build())
        index = (self.fx.output / '2 Roles/INDEKS.md').read_text(encoding='utf-8')
        self.assertIn('peran-fleet/peran-a.md', index)
        self.assertIn('peran-fleet/peran-b.md', index)
        self.assertFalse((self.fx.output / '2 Roles/KATALOG.jsonl').exists())
        done = shipped_check(self.fx.output)
        self.assertEqual(done.returncode, 0, done.stdout)

    def add_skill(self, name, folders, description='Deskripsi.'):
        for folder in folders:
            self.fx.write(f'{folder}/SKILL.md', f'---\nname: {name}\ndescription: {description}\n---\n# S\n')
        self.fx.skills[name] = folders

    def test_aturan_pilih_dan_content_diff(self):
        self.add_skill('dua-sisi', ['3 Skills/registry-fleet/dua-sisi', '3 Skills/kanonik/dua-sisi'])
        self.add_skill('registri-saja', ['3 Skills/registry-fleet/registri-saja'])
        self.add_skill('tersarang', ['3 Skills/kanonik/grup/tersarang', '3 Skills/registry-fleet/tersarang'])
        self.add_skill('arsip', ['3 Skills/kanonik/_salvage-profil-merge-1010/arsip', '3 Skills/kanonik/a/b/c/arsip'])
        self.fx.write('3 Skills/kanonik/dua-sisi/isi.md', '# Sama, tautan [a](../kanonik/x.md)\n')
        self.fx.write('3 Skills/registry-fleet/dua-sisi/isi.md', '# Sama, tautan [a](../registry-fleet/x.md)\n')
        self.add_skill('beda', ['3 Skills/kanonik/beda', '3 Skills/registry-fleet/beda'])
        self.fx.write('3 Skills/kanonik/beda/isi.md', '# Satu\n')
        self.fx.write('3 Skills/registry-fleet/beda/isi.md', '# Dua\n')
        self.add_skill('sisi-tunggal', ['3 Skills/kanonik/sisi-tunggal', '3 Skills/registry-fleet/sisi-tunggal'])
        self.fx.write('3 Skills/registry-fleet/sisi-tunggal/hanya.md', '# Hanya\n')
        self.fx.publish(lambda config: config.update(scan_reviews=[]))
        run = self.fx.build('--dry-run')
        # Tautan contoh menuju berkas yang tidak ada di sumber, jadi dipastikan lewat fungsi murni di bawah.
        self.assertEqual(run.reason, 'check_failed')
        module = load_builder(self.fx.clone)
        contents = {path.relative_to(self.fx.clone).as_posix(): path.read_bytes()
                    for path in (self.fx.clone / '3 Skills').rglob('*') if path.is_file()}
        rows = {row['name']: row for row in module.catalog_rows(contents)}
        self.assertEqual(list(rows), sorted(rows))
        self.assertEqual(rows['dua-sisi']['path'], '3 Skills/kanonik/dua-sisi/SKILL.md')
        self.assertFalse(rows['dua-sisi']['content_diff'])
        self.assertEqual(rows['registri-saja']['path'], '3 Skills/registry-fleet/registri-saja/SKILL.md')
        self.assertFalse(rows['registri-saja']['content_diff'])
        self.assertEqual(rows['tersarang']['path'], '3 Skills/registry-fleet/tersarang/SKILL.md')
        self.assertEqual(rows['arsip']['path'], '3 Skills/kanonik/a/b/c/arsip/SKILL.md')
        self.assertTrue(rows['beda']['content_diff'])
        self.assertTrue(rows['sisi-tunggal']['content_diff'])
        self.assertEqual({row['instruction_authority'] for row in rows.values()}, {'none'})

    def test_path_fixtures_tidak_masuk_katalog(self):
        module = load_builder(self.fx.clone)
        skill = b'---\nname: contoh\ndescription: d\n---\n'
        self.assertEqual(module.catalog_rows({'3 Skills/kanonik/a/scripts/fixtures/r/SKILL.md': skill}), [])

    def test_bentuk_frontmatter(self):
        module = load_builder(self.fx.clone)
        cases = {
            b'---\nname: polos\n---\n': 'polos',
            b'---\r\nname: crlf\r\n---\r\n': 'crlf',
            b"---\nname: 'kutip ''tunggal'''\n---\n": "kutip 'tunggal'",
            b'---\nname: "kutip \\"ganda\\""\n---\n': 'kutip "ganda"',
            b'---\nname: >\n  blok\n  lipat\nlain: x\n---\n': 'blok lipat',
            b'---\nname: |-\n  blok\n  literal\n---\n': 'blok literal',
            b'---\nname: polos\n  multibaris\n---\n': 'polos multibaris',
            b'---\nname: "dua\n  baris"\n---\n': 'dua baris',
            b'---\nname: isi # komentar\n---\n': 'isi',
        }
        for data, expected in cases.items():
            with self.subTest(data):
                self.assertEqual(module.parse_frontmatter(data)['name'], expected)
        self.assertEqual(module.parse_frontmatter(b'---\ntags: [a, "b"]\n---\n')['tags'], ['a', 'b'])
        self.assertEqual(module.parse_frontmatter(b'---\ntags:\n  - a\n  - b\nname: x\n---\n'),
                         {'tags': ['a', 'b'], 'name': 'x'})
        self.assertEqual(module.parse_frontmatter(b'---\nmeta:\n  name: dalam\nname: luar\n---\n')['name'], 'luar')
        self.assertEqual(module.parse_frontmatter(b'# tanpa\n'), {})
        for broken in (b'---\nname: x\n', b'---\nname: "x\n---\n', b'---\ntags: [a\n---\n'):
            with self.subTest(broken), self.assertRaises(ValueError):
                module.parse_frontmatter(broken)

    def test_pemotongan_deskripsi_c19(self):
        module = load_builder(self.fx.clone)
        self.assertEqual(module.normalize_description(' a\n  b\t c '), 'a b c')
        self.assertEqual(module.normalize_description('x' * 120), 'x' * 120)
        self.assertEqual(module.normalize_description('x' * 121), 'x' * 116 + ' ...')
        cut = module.normalize_description('kata ' * 40)
        self.assertLessEqual(len(cut), 120)
        self.assertTrue(cut.endswith('kata ...'))


class Boundaries(EditionCase):
    """G43-07: tepat di batas lulus, satu di atasnya gagal; panjang dibuktikan dari berkas hasil."""

    def fill_catalog(self, target):
        module = load_builder(self.fx.clone)
        self.fx.remove('3 Skills')
        self.fx.skills = {}

        def row(number, length):
            name = f's-{number:04d}'
            return {'name': name, 'description': 'd' * length, 'path': f'3 Skills/kanonik/{name}/SKILL.md',
                    'content_diff': False, 'instruction_authority': 'none'}
        count = 0
        while len(module.render_catalog([row(n, 100) for n in range(count + 1)])) <= target:
            count += 1
        lengths = [100] * count
        missing = target - len(module.render_catalog([row(n, 100) for n in range(count)]))
        for index in range(count):
            step = min(20, missing)
            lengths[index] += step
            missing -= step
        self.assertEqual(missing, 0)
        rows = [row(n, lengths[n]) for n in range(count)]
        self.assertEqual(len(module.render_catalog(rows)), target)
        for item in rows:
            folder = posix_parent(item['path'])
            self.fx.write(item['path'], f"---\nname: {item['name']}\ndescription: {item['description']}\n---\n# S\n")
            self.fx.skills[item['name']] = [folder]
        self.fx.publish()

    def test_catalog_tepat_50000_lulus(self):
        self.fill_catalog(50000)
        self.assertPass(self.fx.build())
        self.assertEqual(len((self.fx.output / '3 Skills/KATALOG.jsonl').read_text(encoding='utf-8')), 50000)

    def test_catalog_50001_gagal(self):
        self.fill_catalog(50001)
        run = self.fx.build()
        self.assertBlocked(run, 'catalog_oversize')
        self.assertFalse(self.fx.output.exists())
        self.assertEqual(self.fx.report()['details'][0]['chars'], 50001)

    def fill_index(self, target):
        module = load_builder(self.fx.clone)
        stamp = [line.encode() for line in STAMP.splitlines()]
        padding = 'n' * 190

        def rows(count, sizes=None):
            return [(f'padat/{n:04d}-{padding}.txt', (sizes or {}).get(n, 1)) for n in range(count)]

        def length(items):
            return len(module.render_index('4 Knowledge Bank', items, stamp).decode('utf-8'))
        count = 0
        while length(rows(count + 1)) <= target:
            count += 1
        missing, sizes = target - length(rows(count)), {}
        for index in range(count):
            digits = min(3, missing)
            if digits:
                sizes[index] = 10 ** digits
            missing -= digits
        self.assertEqual(missing, 0)
        self.assertEqual(length(rows(count, sizes)), target)
        for name, size in rows(count, sizes):
            self.fx.write(f'4 Knowledge Bank/{name}', 'x' * size)
        self.fx.entries.append(('tree', '4 Knowledge Bank/padat'))
        self.fx.publish()

    def test_indeks_tepat_100000_lulus(self):
        self.fill_index(100000)
        self.assertPass(self.fx.build())
        self.assertEqual(len((self.fx.output / '4 Knowledge Bank/INDEKS.md').read_text(encoding='utf-8')), 100000)

    def test_indeks_100001_gagal(self):
        self.fill_index(100001)
        run = self.fx.build()
        self.assertBlocked(run, 'index_oversize')
        self.assertFalse(self.fx.output.exists())
        self.assertEqual(self.fx.report()['details'][0]['chars'], 100001)


def posix_parent(path):
    return path.rsplit('/', 1)[0]


class QuietOutput(EditionCase):
    """ED-T-17, RK-22: stdout hanya jumlah dan `path_sha256`; rincian ke N-49, tanpa teks cocokan."""

    SECRET_PATH = '1 Workflow/laporan-nama-klien.md'
    STDOUT_KEYS = {'status', 'reason', 'source_commit', 'allowlist_sha256', 'files', 'bytes', 'expected_missing', 'stamped',
                   'rejected_role_mentions', 'dry_run', 'report_written', 'hits', 'path_sha256'}

    def assertQuiet(self, run, path):
        combined = run.stdout + run.stderr
        for forbidden in (path, posix_name(path), 'INSTANSI', 'TANDA-SINTETIK', 'Sintetik', 'SINTETIK'):
            self.assertNotIn(forbidden, combined)
        self.assertIn(sha(path.encode()), run.data['path_sha256'])
        self.assertLessEqual(set(run.data), self.STDOUT_KEYS)
        report = self.fx.report()
        self.assertEqual(report['reason'], run.reason)
        self.assertIn(path, {row.get('path') for row in report['details']})
        text = (self.fx.clone / 'work/edisi-umum/LAPORAN-BUILD.json').read_text(encoding='utf-8')
        self.assertNotIn('INSTANSI', text)
        self.assertNotIn('TANDA-SINTETIK', text)
        self.assertNotIn(str(self.fx.base), text)

    def test_scan_hit_gov_def(self):
        self.control()
        self.fx.write(self.SECRET_PATH, 'INSTANSI-SINTETIK-7 pada isi\n')
        self.fx.publish()
        run = self.fx.build()
        self.assertBlocked(run, 'scan_hit')
        self.assertQuiet(run, self.SECRET_PATH)
        self.assertEqual({row['group'] for row in self.fx.report()['details']}, {'GOV_DEF'})
        # Baris pada berkas hasil: baris 1 sumber bergeser tetap 4 baris oleh stempel.
        self.assertEqual(self.fx.report()['details'][0]['line'], 5)
        self.assertEqual(run.data['hits'], 1)

    def test_scan_hit_grup_tinjauan(self):
        self.control()
        self.fx.write(self.SECRET_PATH, '# J\n\nTANDA-SINTETIK\n')
        self.fx.publish()
        run = self.fx.build()
        self.assertBlocked(run, 'scan_hit')
        self.assertQuiet(run, self.SECRET_PATH)

    def test_denied_path(self):
        self.control()
        path = 'docs/laporan-nama-klien.md'
        self.fx.write(path, '# Isi\n')
        self.fx.entries.append(('file', path))
        self.fx.publish()
        run = self.fx.build()
        self.assertBlocked(run, 'denied_path')
        self.assertQuiet(run, path)

    def test_derived_name_hit(self):
        self.control()
        self.fx.write(self.SECRET_PATH, 'lihat catatan-perkara-sintetik\n')
        self.fx.publish()
        run = self.fx.build()
        self.assertBlocked(run, 'derived_name_hit')
        self.assertQuiet(run, self.SECRET_PATH)
        self.assertNotIn('catatan-perkara', (self.fx.clone / 'work/edisi-umum/LAPORAN-BUILD.json').read_text(encoding='utf-8'))

    def test_check_failed(self):
        self.control()
        self.fx.write(self.SECRET_PATH, '[a](standar.md#tidak-ada)\n')
        self.fx.publish()
        run = self.fx.build()
        self.assertBlocked(run, 'check_failed')
        self.assertQuiet(run, self.SECRET_PATH)

    def test_pin_mismatch(self):
        self.control()
        self.fx.write(self.SECRET_PATH, '# Isi\n')
        self.fx.entries.append(('file', self.SECRET_PATH))
        self.fx.publish()
        self.fx.write(self.SECRET_PATH, '# Isi diubah\n')
        self.fx.commit()
        run = self.fx.build()
        self.assertBlocked(run, 'allowlist_pin_mismatch')
        self.assertQuiet(run, self.SECRET_PATH)
        row = self.fx.report()['details'][0]
        self.assertEqual((row['added'], row['changed'], row['removed']), (0, 1, 0))

    def test_jumlah_pin_pohon_pada_n49(self):
        self.control()
        self.fx.write('1 Workflow/baru.md', '# Baru\n')
        self.fx.write('1 Workflow/standar.md', '# Diubah\n')
        self.fx.commit()
        self.assertBlocked(self.fx.build(), 'allowlist_pin_mismatch')
        row = self.fx.report()['details'][0]
        self.assertEqual((row['path'], row['added'], row['changed'], row['removed']), ('1 Workflow', 1, 1, 0))

    def test_pin_stdout_tanpa_path_dan_tanpa_diff_stat(self):
        path = '1 Workflow'
        self.fx.write('1 Workflow/laporan-nama-klien.md', '# Isi\n')
        self.fx.commit()
        run = self.fx.run_tool('pin', path)
        self.assertEqual(run.code, 0, run.stdout)
        self.assertNotIn('laporan-nama-klien', run.stdout + run.stderr)
        self.assertNotIn(path, run.stdout + run.stderr)
        self.assertEqual(run.data['path_sha256'], [sha(path.encode())])
        self.assertLessEqual(set(run.data), {'status', 'reason', 'updated', 'unchanged', 'report_written', 'hits', 'path_sha256'})
        row = self.fx.report()['details'][0]
        self.assertEqual((row['path'], row['added']), (path, 1))

    def test_laporan_tidak_ditulis_bila_tidak_diabaikan_git(self):
        self.fx.write('.gitignore', '# tanpa aturan\n')
        (self.fx.clone / 'work/edisi-umum/LAPORAN-BUILD.json').unlink(missing_ok=True)
        run = self.fx.build()
        self.assertPass(run)
        self.assertFalse(run.data['report_written'])
        self.assertFalse((self.fx.clone / 'work/edisi-umum/LAPORAN-BUILD.json').exists())

    def test_kesalahan_tak_terduga_tanpa_pesan(self):
        module = load_builder(self.fx.clone)
        stdout = io.StringIO()
        secret = '/rahasia/path-klien'
        with mock.patch.object(module, 'run_build', side_effect=OSError(secret)), contextlib.redirect_stdout(stdout):
            code = module.main(['build', '--output', str(self.fx.output)])
        self.assertEqual(code, 2)
        self.assertNotIn(secret, stdout.getvalue())
        self.assertEqual(json.loads(stdout.getvalue())['error_type'], 'OSError')


def posix_name(path):
    return path.rsplit('/', 1)[-1]


class Pin(EditionCase):
    """N-60: hanya pin pada pohon kerja yang berubah; `approval` dan kunci lain tetap."""

    def test_pin_memperbarui_tanpa_mengubah_approval(self):
        self.fx.write('1 Workflow/standar.md', '# Berubah\n')
        self.fx.commit()
        self.assertBlocked(self.fx.build(), 'allowlist_pin_mismatch')
        before = json.loads((self.fx.clone / ALLOWLIST).read_text(encoding='utf-8'))
        run = self.fx.run_tool('pin', '1 Workflow')
        self.assertEqual((run.code, run.data['updated']), (0, 1))
        after = json.loads((self.fx.clone / ALLOWLIST).read_text(encoding='utf-8'))
        self.assertEqual(after['approval'], before['approval'])
        self.assertEqual(after['entries'][4]['tree'], self.fx.oid('1 Workflow'))
        self.assertEqual({**after, 'entries': None}, {**before, 'entries': None})
        self.assertEqual(after['entries'][:4], before['entries'][:4])
        self.assertBlocked(self.fx.build(), 'allowlist_pin_mismatch')
        self.fx.commit()
        self.assertPass(self.fx.build())

    def test_pin_berkas_dan_salinan_skill(self):
        self.fx.write('AGENTS.md', '# Agen baru\n')
        self.fx.write('3 Skills/kanonik/alpha/baru.md', '# B\n')
        self.fx.commit()
        run = self.fx.run_tool('pin', 'AGENTS.md', '3 Skills/kanonik/alpha')
        self.assertEqual((run.code, run.data['updated']), (0, 2))
        self.fx.commit()
        self.assertPass(self.fx.build())

    def test_pin_tanpa_perubahan_tidak_menulis(self):
        before = (self.fx.clone / ALLOWLIST).read_bytes()
        run = self.fx.run_tool('pin', '1 Workflow')
        self.assertEqual((run.code, run.data['updated'], run.data['unchanged']), (0, 0, 1))
        self.assertEqual((self.fx.clone / ALLOWLIST).read_bytes(), before)

    def test_pin_path_tak_dikenal_tidak_menulis(self):
        before = (self.fx.clone / ALLOWLIST).read_bytes()
        run = self.fx.run_tool('pin', '1 Workflow', 'folder-lain')
        self.assertEqual((run.code, run.reason), (1, 'allowlist_invalid'))
        self.assertEqual((self.fx.clone / ALLOWLIST).read_bytes(), before)
        self.assertNotIn('folder-lain', run.stdout + run.stderr)

    def test_pin_menolak_skema_rusak(self):
        self.fx.write(ALLOWLIST, json.dumps({'exclude': []}))
        run = self.fx.run_tool('pin', '1 Workflow')
        self.assertEqual((run.code, run.reason), (1, 'allowlist_invalid'))


class DerivedSource(EditionCase):
    """CR-04: wiki yang gagal diurai menghentikan build; namanya tidak boleh hilang dari gerbang."""

    WIKI_PATH = '4 Knowledge Bank/wiki-information-library/catatan-tertahan.md'
    NAME = 'Nama Perkara Tertahan'
    BROKEN = {
        'frontmatter_tidak_tertutup': f'---\nperkara: {NAME}\n# isi\n'.encode(),
        'kutip_tidak_tertutup': f'---\nperkara: "{NAME}\n---\n# isi\n'.encode(),
        'larik_tidak_tertutup': f'---\nperkara: [{NAME}\n---\n# isi\n'.encode(),
        'bukan_utf8': f'---\nperkara: {NAME}\n---\n'.encode() + b'\xff\xfe\n',
    }

    def test_wiki_rusak_menghentikan_build(self):
        self.control()
        self.fx.write('1 Workflow/n.md', f'menyebut {self.NAME}.\n')
        for label, content in self.BROKEN.items():
            with self.subTest(label=label):
                self.fx.write(self.WIKI_PATH, content)
                self.fx.publish()
                before = tree_hash(self.fx.output)
                run = self.fx.build()
                self.assertBlocked(run, 'derived_source_invalid')
                self.assertEqual(tree_hash(self.fx.output), before, 'keluaran berubah')
                self.assertBlocked(self.fx.build('--dry-run'), 'derived_source_invalid')
                self.assertEqual(run.data['path_sha256'], [sha(self.WIKI_PATH.encode())])
                self.assertNotIn(self.WIKI_PATH, run.stdout + run.stderr)
                self.assertNotIn(self.NAME, run.stdout + run.stderr)
                report = self.fx.report()
                self.assertEqual(report['details'], [{'path': self.WIKI_PATH}])
                self.assertNotIn(self.NAME, json.dumps(report, ensure_ascii=False))

    def test_wiki_rusak_tanpa_sebutan_tetap_berhenti(self):
        # Nama yang tidak terbaca tidak dapat dibuktikan absen dari edisi.
        self.fx.write(self.WIKI_PATH, self.BROKEN['frontmatter_tidak_tertutup'])
        self.fx.publish()
        self.assertBlocked(self.fx.build(), 'derived_source_invalid')

    def test_kontrol_frontmatter_tertutup_kena_gerbang_nama(self):
        self.fx.write(self.WIKI_PATH, f'---\nperkara: {self.NAME}\n---\n# isi\n')
        self.fx.write('1 Workflow/n.md', f'menyebut {self.NAME}.\n')
        self.fx.publish()
        self.assertBlocked(self.fx.build(), 'derived_name_hit')

    def test_kontrol_wiki_tanpa_frontmatter_lulus(self):
        self.fx.write(self.WIKI_PATH, '# Tanpa frontmatter\n')
        self.fx.publish()
        self.assertPass(self.fx.build())


class SourceRules(unittest.TestCase):
    """Sifat kode pada clone ini: arah impor satu, pustaka standar, flag koleksi tidak dibaca."""

    def imports(self, path):
        tree = ast.parse(Path(path).read_text(encoding='utf-8'))
        found = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                found.update(alias.name.split('.')[0] for alias in node.names)
            elif isinstance(node, ast.ImportFrom):
                found.add((node.module or '').split('.')[0])
        return found

    def test_library_tidak_mengimpor_pembangun(self):
        self.assertNotIn('build_edition', self.imports(RESOLVER))
        self.assertNotIn('build_edition', RESOLVER.read_text(encoding='utf-8'))

    def test_pembangun_hanya_pustaka_standar(self):
        self.assertLessEqual(self.imports(BUILDER), set(sys.stdlib_module_names))

    def test_ed_t_01_flag_koleksi_tidak_dibaca(self):
        self.assertEqual(BUILDER.read_text(encoding='utf-8').count('sensitif'), 0)

    def test_tanpa_variabel_lingkungan_untuk_path(self):
        tree = ast.parse(BUILDER.read_text(encoding='utf-8'))
        uses = [node for node in ast.walk(tree) if isinstance(node, ast.Call)
                and isinstance(node.func, ast.Attribute) and node.func.attr == 'getenv']
        self.assertEqual(uses, [])
        self.assertEqual(BUILDER.read_text(encoding='utf-8').count('os.environ['), 0)

    def test_tanpa_git_tulis_dan_jaringan(self):
        text = BUILDER.read_text(encoding='utf-8')
        for forbidden in ("'init'", "'push'", "'fetch'", "'clone'", "'remote'", 'socket', 'urllib.request'):
            self.assertNotIn(forbidden, text)


if __name__ == '__main__':
    unittest.main()
