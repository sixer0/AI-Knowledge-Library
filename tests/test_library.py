"""Uji perilaku resolver dan relokasi; tidak mengimpor skrip operasional pustaka."""
from pathlib import Path
import importlib.util
import json
import csv
import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest

MODULE = Path(__file__).resolve().parents[1] / 'tools/library.py'
SPEC = importlib.util.spec_from_file_location('library', MODULE)
MODULE_API = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE_API)


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
        links = MODULE_API.markdown_links('```md\n[x](missing.md)\n```\n[y](ok.md)')
        self.assertEqual(links, ['ok.md'])


if __name__ == '__main__':
    unittest.main()
