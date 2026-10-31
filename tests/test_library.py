"""Uji perilaku resolver dan relokasi; tidak mengimpor skrip operasional pustaka."""
from pathlib import Path
import ast
import importlib.util
import json
import csv
import hashlib
import os
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'tools/library.py'
SPEC = importlib.util.spec_from_file_location('library', MODULE)
MODULE_API = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE_API)
REPOSITORY = MODULE.parents[1]
UPDATER = REPOSITORY / 'tools/update_manifest.py'


class ResolutionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='library clone ü ')
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        for name, content in {
            'HARNESS.md': '[lokal](folder/rujukan%20lokal.md#judul-utama)',
            'README.md': '# Root\n',
            'folder/rujukan lokal.md': '# Judul Utama\n# Judul Utama\n',
            'folder/nested/source.md': '# Sumber\n',
            'skills/one/SKILL.md': '# Skill\n',
            'tools/library.py': MODULE.read_text(),
        }.items():
            path = self.root / name; path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content)
        config = {'schema_version': 1, 'roots': {'docs': 'folder'},
                  'aliases': [{'source': 'ekas', 'target': 'folder'},
                              {'source': 'C:/Users/TRIAL/skills', 'target': 'skills'},
                              {'source': '$LOCALAPPDATA/hermes/skills/gsp', 'target': 'skills'}],
                  'workspace_prefixes': ['<ws>'],
                  'repository_urls': ['https://github.com/owner/library/blob/main/'],
                  'managed_documents': ['HARNESS.md'], 'manifest': 'MANIFEST.csv',
                  'manifest_files': ['README.md']}
        (self.root / 'library.json').write_text(json.dumps(config))
        self.library = MODULE_API.Library(self.root)

    def make_manifest(self):
        data = (self.root / 'README.md').read_bytes()
        with (self.root / 'MANIFEST.csv').open('w', newline='') as stream:
            writer = csv.writer(stream)
            writer.writerow(['relative_path', 'bytes', 'sha256'])
            writer.writerow(['README.md', len(data), hashlib.sha256(data).hexdigest()])

    def test_check_detects_missing_manifest_entry_and_changed_data(self):
        self.make_manifest()
        self.assertEqual(self.library.check()['status'], 'pass')
        (self.root / 'README.md').write_text('diubah')
        self.assertIn('manifest_mismatch', [f.get('reason') for f in self.library.check()['failures']])
        (self.root / 'MANIFEST.csv').write_text('relative_path,bytes,sha256\n')
        self.assertIn('manifest_coverage', [f.get('reason') for f in self.library.check()['failures']])

    def test_check_detects_missing_local_link(self):
        self.make_manifest()
        (self.root / 'HARNESS.md').write_text('[hilang](missing.md)')
        self.assertEqual(self.library.check()['status'], 'fail')
        (self.root / 'HARNESS.md').write_text('# Panduan\n')
        (self.root / 'README.md').write_text('[hilang](missing.md)')
        self.make_manifest()
        self.assertEqual(self.library.check()['status'], 'fail')

    def test_percent_encoding_fragment_and_document_relative_path(self):
        value = self.library.resolve('../rujukan%20lokal.md#judul-utama', 'folder/nested/source.md')
        self.assertEqual(value['status'], 'local')
        self.assertEqual(value['relative_path'], 'folder/rujukan lokal.md')
        self.assertEqual(value['fragment'], 'judul-utama')

    def test_no_root_basename_fallback_when_source_is_given(self):
        result = self.library.resolve('README.md', 'folder/nested/source.md')
        self.assertEqual(result['status'], 'missing')

    def test_windows_and_environment_alias(self):
        for reference in [r'C:\Users\TRIAL\skills\one\SKILL.md',
                          '$LOCALAPPDATA/hermes/skills/gsp/one/SKILL.md']:
            self.assertEqual(self.library.resolve(reference)['relative_path'], 'skills/one/SKILL.md')

    def test_workspace_prefix_and_alias(self):
        result = self.library.resolve('<ws>/ekas/rujukan lokal.md')
        self.assertEqual(result['status'], 'local')

    def test_public_url_and_local_service_are_not_rewritten(self):
        for url in ['https://example.org/source.pdf', 'http://localhost:9011/api/tasks']:
            self.assertEqual(self.library.resolve(url), {'status': 'external', 'reference': url, 'url': url})

    def test_main_url_becomes_local_but_commit_url_stays_historical(self):
        result = self.library.resolve('https://github.com/owner/library/blob/main/folder/rujukan%20lokal.md#judul-utama')
        self.assertEqual(result['status'], 'local')
        value = self.library.resolve('https://github.com/owner/library/commit/abcdef')
        self.assertEqual(value['status'], 'external')

    def test_missing_source_is_not_replaced_with_similar_name(self):
        result = self.library.resolve('docs/absent.md')
        self.assertEqual(result['status'], 'missing')
        self.assertNotIn('absolute_path', result)

    def test_missing_anchor_and_duplicate_heading(self):
        self.assertEqual(self.library.resolve('ekas/rujukan lokal.md#absent')['reason'], 'anchor_not_found')
        self.assertEqual(self.library.resolve('ekas/rujukan lokal.md#judul-utama-1')['status'], 'local')

    def test_explicit_table_anchor_preserves_identifier_case(self):
        file = self.root / 'folder/rujukan lokal.md'
        file.write_text(file.read_text() + '\n| <a id="NUM-001"></a>NUM-001 | kemampuan |\n')
        self.assertEqual(self.library.resolve('ekas/rujukan lokal.md#NUM-001')['status'], 'local')
        self.assertEqual(self.library.resolve('ekas/rujukan lokal.md#num-001')['reason'], 'anchor_not_found')

    def test_traversal_absolute_and_encoded_escape_are_rejected(self):
        for reference in ['../outside', 'ekas/../../../outside', '%2e%2e/outside', '/', 'file:///etc/passwd']:
            with self.subTest(reference=reference):
                self.assertEqual(self.library.resolve(reference)['status'], 'invalid')

    def test_symlink_outside_clone_is_rejected(self):
        with tempfile.TemporaryDirectory() as outside:
            (self.root / 'escape').symlink_to(outside, target_is_directory=True)
            self.assertEqual(self.library.resolve('escape')['status'], 'invalid')

    def test_ambiguous_alias_is_not_silently_chosen(self):
        self.library.config['aliases'].append({'source': 'ekas', 'target': 'skills'})
        self.assertEqual(self.library.resolve('ekas/one/SKILL.md')['status'], 'ambiguous')

    def test_cli_after_relocation_from_unrelated_cwd(self):
        with tempfile.TemporaryDirectory(prefix='pindah clone ') as destination:
            relocated = Path(destination) / 'pustaka dengan spasi'
            shutil.copytree(self.root, relocated)
            result = subprocess.run([sys.executable, str(relocated / 'tools/library.py'),
                                     'resolve', 'ekas/rujukan lokal.md', '--json'],
                                    cwd=destination, text=True, capture_output=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            data = json.loads(result.stdout)
            self.assertEqual(data['absolute_path'], str((relocated / 'folder/rujukan lokal.md').resolve()))

    def test_markdown_examples_in_fences_are_not_navigation(self):
        links = MODULE_API.markdown_links('```md\n[x](missing.md)\n```\n`[x](not-a-link.md)`\n[y](ok.md)')
        self.assertEqual(links, ['ok.md'])


class GateFixture(unittest.TestCase):
    """Fixture yang sama dengan ResolutionTests, tanpa mengulang 16 uji di sana."""
    setUp = ResolutionTests.setUp
    make_manifest = ResolutionTests.make_manifest

    def failures(self):
        self.make_manifest()
        return self.library.check()['failures']

    def reasons(self):
        return [failure.get('reason') for failure in self.failures()]

    def shadows(self):
        return [f for f in self.failures() if f.get('reason') == 'alias_shadow']


class AliasShadowTests(GateFixture):
    """UP-13 menurut RK-34: gagal, lewat daftar folder, tanpa cabang lewati."""

    def test_alias_shadow_local_file_on_alias_prefix(self):
        (self.root / 'ekas').mkdir()
        (self.root / 'ekas/sama.md').write_text('# Asing\n')
        self.assertEqual([f['alias'] for f in self.shadows()], ['ekas'])
        self.assertEqual(self.library.check()['status'], 'fail')

    def test_alias_shadow_empty_folder_with_alias_name(self):
        (self.root / 'ekas').mkdir()
        self.assertEqual([f['alias'] for f in self.shadows()], ['ekas'])

    def test_alias_shadow_other_aliases_skills_and_roles(self):
        self.library.config['aliases'] += [{'source': 'skills', 'target': 'folder'},
                                           {'source': 'roles', 'target': 'folder'}]
        (self.root / 'roles').mkdir()
        self.assertEqual(sorted(f['alias'] for f in self.shadows()), ['roles', 'skills'])

    def test_alias_shadow_case_variant_skills_without_skip(self):
        (self.root / 'skills').rename(self.root / 'Skills')
        self.library.config['aliases'] = [{'source': 'skills', 'target': 'folder'}]
        self.assertEqual(os.listdir(self.root).count('Skills'), 1)
        self.assertEqual([f['found'] for f in self.shadows()], ['Skills'])

    def test_alias_shadow_nested_alias_reports_disk_case(self):
        self.library.config['aliases'].append({'source': 'docs/standards', 'target': 'folder'})
        (self.root / 'Docs/Standards').mkdir(parents=True)
        self.assertEqual([f['found'] for f in self.shadows()], ['Docs/Standards'])

    def test_alias_shadow_literal_environment_folder(self):
        (self.root / '$LOCALAPPDATA/hermes/skills/gsp').mkdir(parents=True)
        self.assertEqual([f['alias'] for f in self.shadows()], ['$LOCALAPPDATA/hermes/skills/gsp'])

    def test_alias_shadow_compares_nfc_and_nfd(self):
        self.library.config['aliases'].append({'source': unicodedata.normalize('NFC', 'résumé'), 'target': 'folder'})
        (self.root / unicodedata.normalize('NFD', 'résumé')).mkdir()
        self.assertEqual(len(self.shadows()), 1)

    def test_no_alias_shadow_for_docs_without_alias_path(self):
        self.library.config['aliases'].append({'source': 'docs/standards', 'target': 'folder'})
        (self.root / 'docs').mkdir()
        self.assertEqual(self.shadows(), [])

    def test_no_alias_shadow_for_absent_non_relative_aliases(self):
        self.assertEqual(self.shadows(), [])
        self.assertEqual(self.library.check()['status'], 'pass')


class CheckScopeTests(GateFixture):
    """Kode N-59 selain entrypoint_oversize: `check` sendiri harus dapat gagal (RK-29)."""

    def test_check_manifest_scope_empty(self):
        self.library.config['manifest_files'] = []
        self.library.config['manifest_roots'] = []
        self.assertIn('manifest_scope_empty', self.reasons())
        del self.library.config['manifest_files'], self.library.config['manifest_roots']
        self.assertIn('manifest_scope_empty', self.reasons())
        self.assertEqual(self.library.check()['status'], 'fail')

    def test_check_manifest_root_missing(self):
        self.library.config['manifest_roots'] = ['hilang']
        self.assertIn('manifest_root_missing', self.reasons())

    def test_check_root_file_unlisted(self):
        (self.root / 'TAK-TERDAFTAR.md').write_text('[rusak](hilang.md)\n')
        unlisted = [f for f in self.failures() if f.get('reason') == 'root_file_unlisted']
        self.assertEqual([f['file'] for f in unlisted], ['TAK-TERDAFTAR.md'])

    def test_check_expected_missing_mismatch_two_directions(self):
        (self.root / 'HARNESS.md').write_text('[a](tidak-ikut-1.md)\n[b](tidak-ikut-2.md)\n')
        for expected in (1, 3):
            self.library.config['edition'] = {'expected_missing': expected}
            mismatch = [f for f in self.failures() if f.get('reason') == 'expected_missing_mismatch']
            self.assertEqual([(f['expected'], f['found']) for f in mismatch], [(expected, 2)])
        self.library.config['edition'] = {}
        self.assertIn('expected_missing_mismatch', self.reasons())
        self.library.config['edition'] = {'expected_missing': 2}
        self.make_manifest()
        self.assertEqual(self.library.check()['failures'], [])

    def test_edition_block_keeps_other_missing_reasons_failing(self):
        (self.root / 'HARNESS.md').write_text('[a](folder/rujukan%20lokal.md#absen)\n')
        self.library.config['edition'] = {'expected_missing': 0}
        self.assertIn('anchor_not_found', self.reasons())

    def test_full_clone_without_edition_block_still_fails_on_missing(self):
        (self.root / 'HARNESS.md').write_text('[a](tidak-ikut.md)\n')
        self.assertIn('not_in_clone', self.reasons())

    def test_dot_files_in_root_are_not_unlisted(self):
        (self.root / '.gitattributes').write_text('* -text\n')
        self.make_manifest()
        self.assertEqual(self.library.check()['status'], 'pass')

    def test_check_leaves_fixture_tree_unchanged(self):
        self.make_manifest()
        def snapshot():
            return {path: path.read_bytes() for path in self.root.rglob('*') if path.is_file()}
        before = snapshot()
        self.library.check()
        self.assertEqual(snapshot(), before)


class EntrypointLimitTests(GateFixture):
    """G43-07, RK-42. C-16: `wc -l` harus kurang dari 200, jadi 199 batas terakhir yang sah. C-18: paling banyak 32768."""

    def write_entrypoint(self, data):
        (self.root / 'HARNESS.md').write_bytes(data)
        self.library.config['entrypoint'] = 'HARNESS.md'

    def test_entrypoint_lines_at_limit_c16_passes(self):
        self.write_entrypoint(b'baris\n' * 199)
        self.make_manifest()
        self.assertEqual(self.library.check()['status'], 'pass')

    def test_entrypoint_lines_one_above_c16_fails(self):
        self.write_entrypoint(b'baris\n' * 200)
        self.assertIn('entrypoint_oversize', self.reasons())

    def test_entrypoint_bytes_at_limit_c18_passes(self):
        self.write_entrypoint(b'x' * 32768)
        self.make_manifest()
        self.assertEqual(self.library.check()['status'], 'pass')

    def test_entrypoint_bytes_one_above_c18_fails(self):
        self.write_entrypoint(b'x' * 32769)
        self.assertIn('entrypoint_oversize', self.reasons())


def resolver_violations(source):
    """Uji AST 07d:60: tanpa pemanggilan penulis, `open` hanya baca, impor pustaka standar."""
    found = []
    for node in ast.walk(ast.parse(source)):
        if isinstance(node, ast.Import):
            modules = [alias.name for alias in node.names]
        elif isinstance(node, ast.ImportFrom):
            modules = [node.module or '']
        else:
            modules = []
        found += [f'import:{m}' for m in modules if m.split('.')[0] not in sys.stdlib_module_names]
        if not isinstance(node, ast.Call):
            continue
        func = node.func
        name = func.attr if isinstance(func, ast.Attribute) else getattr(func, 'id', '')
        if name in {'write_text', 'write_bytes', 'mkdir', 'unlink'}:
            found.append('call:' + name)
        if name == 'replace' and isinstance(func, ast.Attribute) and getattr(func.value, 'id', '') == 'os':
            found.append('call:os.replace')
        if name == 'open':
            # open(path, mode) lawan Path.open(mode): letak argumen mode berbeda.
            modes = node.args[0:1] if isinstance(func, ast.Attribute) else node.args[1:2]
            modes += [k.value for k in node.keywords if k.arg == 'mode']
            for mode in modes:
                if not (isinstance(mode, ast.Constant) and isinstance(mode.value, str)
                        and not set(mode.value) & set('wax+')):
                    found.append('call:open-mode')
    return found


class ResolverStaticTests(unittest.TestCase):
    def test_resolver_has_no_writer_and_only_standard_imports(self):
        self.assertEqual(resolver_violations(MODULE.read_text(encoding='utf-8')), [])

    def test_static_check_can_fail(self):
        for source, expected in {'import requests': 'import:requests',
                                 'from yaml import load': 'import:yaml',
                                 'p.write_text("x")': 'call:write_text',
                                 'p.write_bytes(b"x")': 'call:write_bytes',
                                 'p.mkdir()': 'call:mkdir',
                                 'p.unlink()': 'call:unlink',
                                 'os.replace(a, b)': 'call:os.replace',
                                 'open(p, "w")': 'call:open-mode',
                                 'open(p, mode="a")': 'call:open-mode',
                                 'p.open("r+")': 'call:open-mode',
                                 'os.open(p, flags)': 'call:open-mode'}.items():
            with self.subTest(source=source):
                self.assertEqual(resolver_violations(source), [expected])
        self.assertEqual(resolver_violations('open(p)\np.open(encoding="utf-8")\n"a".replace("a", "b")'), [])


class LineEndingTests(GateFixture):
    """Uji 07d:61, RK-14: clone autocrlf gagal tanpa N-16 dan lulus dengan N-16."""

    def git(self, *args, cwd=None):
        environment = {**os.environ, 'GIT_CONFIG_NOSYSTEM': '1', 'GIT_CONFIG_GLOBAL': os.devnull}
        command = ['git', '-c', 'user.name=uji', '-c', 'user.email=uji@example.invalid',
                   '-c', 'core.hooksPath=' + os.devnull, *args]
        return subprocess.run(command, cwd=cwd, env=environment, text=True, capture_output=True, check=True).stdout

    def clone_and_check(self, destination):
        self.git('clone', '-q', '-c', 'core.autocrlf=true', str(self.root), str(destination))
        environment = {**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}
        result = subprocess.run([sys.executable, str(destination / 'tools/library.py'), 'check'],
                                text=True, capture_output=True, env=environment)
        return result, json.loads(result.stdout)

    def test_autocrlf_clone_fails_without_attribute_and_passes_with_it(self):
        attribute = REPOSITORY / '.gitattributes'
        self.assertTrue(attribute.is_file(), 'N-16 belum ada')
        self.assertEqual(attribute.read_bytes(), b'* -text\n')
        self.make_manifest()
        self.git('init', '-q', cwd=self.root)
        self.git('add', '--', 'HARNESS.md', 'MANIFEST.csv', 'README.md', 'folder', 'library.json', 'skills', 'tools',
                 cwd=self.root)
        self.git('commit', '-q', '-m', 'tanpa atribut', cwd=self.root)
        with tempfile.TemporaryDirectory(prefix='autocrlf ') as clones:
            result, data = self.clone_and_check(Path(clones) / 'tanpa')
            self.assertEqual(result.returncode, 1)
            self.assertEqual([f['reason'] for f in data['failures']], ['manifest_mismatch'])
            shutil.copy(attribute, self.root / '.gitattributes')
            self.git('add', '--', '.gitattributes', cwd=self.root)
            self.git('commit', '-q', '-m', 'dengan atribut', cwd=self.root)
            result, data = self.clone_and_check(Path(clones) / 'dengan')
            self.assertEqual((result.returncode, data['failures']), (0, []))
            self.assertEqual(self.git('status', '--short', cwd=Path(clones) / 'dengan'), '')


class ManifestWriterTests(GateFixture):
    """N-17: uji 07d:59 butir a, b, c dan UP-14 sasaran N-17."""

    def setUp(self):
        GateFixture.setUp(self)
        self.assertTrue(UPDATER.is_file(), 'tools/update_manifest.py belum ada')
        shutil.copy(UPDATER, self.root / 'tools/update_manifest.py')
        self.manifest = self.root / 'MANIFEST.csv'
        self.approved = Path(self.temp.name + ' disetujui.csv')
        self.addCleanup(self.approved.unlink, missing_ok=True)

    def configure(self, **changes):
        path = self.root / 'library.json'
        path.write_text(json.dumps({**json.loads(path.read_text()), **changes}))

    def row(self, name):
        data = (self.root / name).read_bytes()
        cell = f'"{name}"' if ',' in name else name
        return f'{cell},{len(data)},{hashlib.sha256(data).hexdigest()}\n'.encode('utf-8')

    def canonical(self, *names):
        """Manifest yang disusun tangan: `\\n`, urut byte UTF-8, kutip minimal."""
        rows = sorted(names, key=lambda name: name.encode('utf-8'))
        self.manifest.write_bytes(b'relative_path,bytes,sha256\n' + b''.join(self.row(name) for name in rows))
        return self.manifest.read_bytes()

    def run_writer(self, *args):
        result = subprocess.run([sys.executable, str(self.root / 'tools/update_manifest.py'), *args], text=True,
                                capture_output=True, env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'}, cwd=tempfile.gettempdir())
        return result.returncode, json.loads(result.stdout) if result.stdout else {}

    def write_with(self, *paths):
        with self.approved.open('w', encoding='utf-8', newline='') as stream:
            writer = csv.writer(stream, lineterminator='\n')
            writer.writerow(['relative_path', 'change_type', 'approval_ref'])
            writer.writerows([path, 'ubah', 'uji'] for path in paths)
        return self.run_writer('--write', '--approved', str(self.approved))

    def sidecar_fixture(self):
        (self.root / 'data').mkdir()
        (self.root / 'data/x.db').write_bytes(b'SQLite format 3\x00' + b'\x00' * 84)
        (self.root / 'data/x.db-shm').write_bytes(b'')
        (self.root / 'data/x.db-wal').write_bytes(b'')
        self.configure(manifest_roots=['data'])
        self.canonical('README.md')

    def test_writer_output_is_byte_identical_to_canonical_manifest(self):
        names = ['README.md', 'Z.md', 'a,b.md', 'a.md', 'ü.md']
        for name in names[1:]:
            (self.root / name).write_text('# Isi\n')
        self.configure(manifest_files=names)
        before = self.canonical(*names)
        self.assertLess(before.index(b'Z.md'), before.index(b'"a,b.md"'))
        self.assertNotIn(b'\r', before)
        code, report = self.run_writer()
        self.assertEqual((code, report['added'], report['changed'], report['removed']), (0, [], [], []))
        specification = importlib.util.spec_from_file_location('update_manifest_uji', UPDATER)
        writer = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(writer)
        self.assertEqual(writer.manifest_bytes(self.root), before)
        self.assertEqual(self.write_with()[0], 0)
        self.assertEqual(self.manifest.read_bytes(), before)

    def test_writer_rejects_change_outside_approved_list_without_writing(self):
        before = self.canonical('README.md')
        (self.root / 'README.md').write_text('diubah')
        code, report = self.write_with('berkas-lain.md')
        self.assertEqual((code, report['unapproved'], report['written']), (1, ['README.md'], False))
        self.assertEqual(self.manifest.read_bytes(), before)

    def test_writer_changes_only_listed_rows(self):
        names = ['README.md', 'lain.md', 'baru.md']
        (self.root / 'lain.md').write_text('# Tetap\n')
        self.configure(manifest_files=names[:2])
        self.canonical(*names[:2])
        untouched = self.row('lain.md')
        (self.root / 'README.md').write_text('diubah')
        (self.root / 'baru.md').write_text('# Baru\n')
        self.configure(manifest_files=names)
        listing = set(os.listdir(self.root))
        code, report = self.write_with('README.md', 'baru.md')
        self.assertEqual((code, report['added'], report['changed'], report['removed']),
                         (0, ['baru.md'], ['README.md'], []))
        lines = self.manifest.read_bytes().splitlines(keepends=True)
        self.assertEqual(lines, [b'relative_path,bytes,sha256\n', self.row('README.md'), self.row('baru.md'), untouched])
        self.assertEqual(set(os.listdir(self.root)), listing)

    def test_writer_report_mode_never_writes(self):
        before = self.canonical('README.md')
        (self.root / 'README.md').write_text('diubah')
        code, report = self.run_writer()
        self.assertEqual((code, report['changed'], report['written']), (0, ['README.md'], False))
        self.assertEqual(self.manifest.read_bytes(), before)

    def test_writer_requires_approved_list_to_write(self):
        before = self.canonical('README.md')
        (self.root / 'README.md').write_text('diubah')
        self.assertEqual(self.run_writer('--write')[0], 2)
        self.assertEqual(self.manifest.read_bytes(), before)

    def test_writer_refuses_empty_scope_and_non_canonical_manifest(self):
        before = self.canonical('README.md')
        self.configure(manifest_files=[])
        code, report = self.write_with('README.md')
        self.assertEqual((code, report['rejected']), (1, [{'reason': 'manifest_scope_empty'}]))
        self.assertEqual(self.manifest.read_bytes(), before)
        self.configure(manifest_files=['README.md'])
        crlf = before.replace(b'\n', b'\r\n')
        self.manifest.write_bytes(crlf)
        code, report = self.write_with('README.md')
        self.assertEqual((code, [r['reason'] for r in report['rejected']]), (1, ['manifest_not_canonical']))
        self.assertEqual(self.manifest.read_bytes(), crlf)

    def test_sqlite_sidecar_rejected_by_writer(self):
        self.sidecar_fixture()
        before = self.manifest.read_bytes()
        expected = [{'reason': 'sqlite_sidecar', 'file': 'data/x.db-shm'},
                    {'reason': 'sqlite_sidecar', 'file': 'data/x.db-wal'}]
        code, report = self.run_writer()
        self.assertEqual((code, report['rejected']), (1, expected))
        code, report = self.write_with('README.md', 'data/x.db', 'data/x.db-shm', 'data/x.db-wal')
        self.assertEqual((code, report['rejected'], report['written']), (1, expected, False))
        self.assertEqual(self.manifest.read_bytes(), before)

    def test_ordinary_names_are_not_sqlite_sidecars(self):
        (self.root / 'data').mkdir()
        for name, content in {'catatan-wal.md': b'# Catatan\n', 'y-wal': b'', 'bukan.db': b'teks', 'bukan.db-wal': b''}.items():
            (self.root / 'data' / name).write_bytes(content)
        self.configure(manifest_roots=['data'])
        self.canonical('README.md')
        code, report = self.run_writer()
        self.assertEqual((code, report['rejected']), (0, []))
        self.assertEqual(len(report['added']), 4)

    def test_sidecar_outside_manifest_scope_is_not_reported(self):
        # N-17 hanya menilai cakupan manifest; berkas di luar cakupan tidak pernah masuk manifest.
        (self.root / 'luar').mkdir()
        (self.root / 'luar/x.db').write_bytes(b'SQLite format 3\x00')
        (self.root / 'luar/x.db-shm').write_bytes(b'')
        self.canonical('README.md')
        code, report = self.run_writer()
        self.assertEqual((code, report['rejected'], report['added']), (0, [], []))

    def test_sidecar_in_manifest_root_still_gives_manifest_coverage(self):
        self.sidecar_fixture()
        self.library = MODULE_API.Library(self.root)
        coverage = [f for f in self.library.check()['failures'] if f.get('reason') == 'manifest_coverage']
        self.assertEqual(coverage[0]['missing'], ['data/x.db', 'data/x.db-shm', 'data/x.db-wal'])


if __name__ == '__main__':
    unittest.main()
