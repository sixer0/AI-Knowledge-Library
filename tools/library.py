#!/usr/bin/env python3
"""Resolver rujukan pustaka, tanpa jaringan dan tanpa menjalankan skrip koleksi."""
from pathlib import Path
from collections import Counter
from urllib.parse import unquote, urlsplit
import argparse
import csv
import hashlib
import json
import re
import sys


def normalize(value):
    value = re.sub(r'/+', '/', unquote(value).replace('\\', '/'))
    return value.rstrip('/') if value != '/' else value


def anchors(text):
    result, used, fence = set(), Counter(), None
    for line in text.splitlines():
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            char = marker[1][0]
            fence = char if fence is None else None if char == fence else fence
            continue
        if fence:
            continue
        match = re.match(r'^#{1,6}\s+(.+?)(?:\s+#+)?$', line)
        if match:
            title = re.sub(r'<[^>]+>', '', match[1]).lower().strip()
            slug = ''.join(c for c in title if c.isalnum() or c in ' _-').replace(' ', '-')
            number = used[slug]; used[slug] += 1
            result.add(slug + (f'-{number}' if number else ''))
        result.update(re.findall(r'(?:id|name)=["\x27]([^"\x27]+)', line))
    return result


def markdown_links(text):
    lines, fence = [], None
    for line in text.splitlines():
        marker = re.match(r'^\s*(`{3,}|~{3,})', line)
        if marker:
            char = marker[1][0]
            fence = char if fence is None else None if char == fence else fence
        elif not fence:
            lines.append(line)
    return re.findall(r'!?\[[^\]\n]*\]\((<[^>\n]+>|[^)\n]+)\)', '\n'.join(lines))


class Library:
    def __init__(self, root=None):
        self.root = Path(root or Path(__file__).resolve().parents[1]).resolve()
        self.config = json.loads((self.root / 'library.json').read_text(encoding='utf-8'))
        if self.config.get('schema_version') != 1:
            raise ValueError('schema_version library.json tidak didukung')
        targets = list(self.config.get('roots', {}).values())
        targets += [a['target'] for a in self.config.get('aliases', [])]
        targets += self.config.get('managed_documents', [])
        targets += self.config.get('manifest_roots', []) + self.config.get('manifest_files', [])
        targets += [self.config.get('manifest', 'MANIFEST.csv')]
        for target in targets:
            if Path(target).is_absolute() or re.match(r'^[A-Za-z]:', target) or '..' in Path(target).parts:
                raise ValueError('Target konfigurasi harus relatif terhadap clone: ' + target)
            self.inside(self.root / target)

    def inside(self, path):
        path = path.resolve()
        path.relative_to(self.root)
        return path

    def _local(self, path, fragment, reference):
        try:
            path = self.inside(path)
        except ValueError:
            return {'status': 'invalid', 'reference': reference, 'reason': 'outside_clone'}
        relative = path.relative_to(self.root).as_posix() or '.'
        result = {'status': 'local' if path.exists() else 'missing',
                  'reference': reference, 'relative_path': relative, 'fragment': fragment}
        if not path.exists():
            result['reason'] = 'not_in_clone'
        elif fragment and path.suffix.lower() == '.md' and fragment not in anchors(path.read_text(encoding='utf-8')):
            result.update(status='missing', reason='anchor_not_found')
        else:
            result['absolute_path'] = str(path)
        return result

    def resolve(self, reference, source=None):
        original = reference
        reference = reference.strip().strip('`')
        if reference.startswith('<') and reference.endswith('>') and reference not in {'<ws>', '<shared-ws>'}:
            reference = reference[1:-1]
        if not reference or '\x00' in reference or '\n' in reference or '\r' in reference:
            return {'status': 'invalid', 'reference': original, 'reason': 'empty_or_control_character'}
        # URL sumber tetap eksternal; hanya URL branch main milik repo ini dilokalkan.
        repo_url = False
        for prefix in self.config.get('repository_urls', []):
            if reference.startswith(prefix):
                parsed = urlsplit(reference)
                reference = reference[len(prefix):].split('?', 1)[0].split('#', 1)[0]
                if parsed.fragment:
                    reference += '#' + parsed.fragment
                repo_url = True
                break
        if not repo_url and re.match(r'^[A-Za-z][\w+.-]*:', reference) and not re.match(r'^[A-Za-z]:[/\\]', reference):
            if reference.startswith('file://'):
                parsed = urlsplit(reference)
                if parsed.netloc not in {'', 'localhost'}:
                    return {'status': 'invalid', 'reference': original, 'reason': 'remote_file_uri'}
                reference = unquote(parsed.path)
                if re.match(r'^/[A-Za-z]:/', reference):
                    reference = reference[1:]
                if parsed.fragment:
                    reference += '#' + parsed.fragment
            else:
                return {'status': 'external', 'reference': original, 'url': original}
        raw, _, fragment = reference.partition('#')
        path, fragment = normalize(raw), unquote(fragment)
        if repo_url:
            return self._local(self.root / path, fragment, original)
        # Root dan konteks ditentukan dari clone, bukan cwd proses.
        context = self.root
        if source:
            try:
                context_file = self.inside(self.root / source)
            except ValueError:
                return {'status': 'invalid', 'reference': original, 'reason': 'source_outside_clone'}
            if not context_file.is_file():
                return {'status': 'invalid', 'reference': original, 'reason': 'source_not_found'}
            context = context_file.parent
        local = self._local(context / (path or '.'), fragment, original)
        if not path and source:
            return self._local(context_file, fragment, original)
        if local['status'] in {'local', 'invalid'} and not re.match(r'^[A-Za-z]:/', path):
            return local
        if source and path.startswith(('./', '../')):
            return local
        # Prefix workspace sumber dibuang lebih dulu; alias berikutnya tetap eksplisit.
        for prefix in sorted(self.config.get('workspace_prefixes', []), key=len, reverse=True):
            prefix = normalize(prefix)
            if path == prefix or path.startswith(prefix + '/'):
                path = path[len(prefix):].lstrip('/')
                break
        matched = []
        for alias in self.config.get('aliases', []):
            prefix = normalize(alias['source'])
            sensitive = not re.match(r'^[A-Za-z]:/', prefix)
            a, b = (path, prefix) if sensitive else (path.casefold(), prefix.casefold())
            if a == b or a.startswith(b + '/'):
                matched.append((len(prefix), alias['target'] + path[len(prefix):]))
        if matched:
            length = max(n for n, _ in matched)
            targets = sorted({target for n, target in matched if n == length})
            if len(targets) > 1:
                return {'status': 'ambiguous', 'reference': original, 'candidates': targets}
            return self._local(self.root / targets[0], fragment, original)
        if re.match(r'^[A-Za-z]:/', path):
            return {'status': 'missing', 'reference': original, 'reason': 'unmapped_host_path'}
        root_names = {Path(value).parts[0] for value in self.config.get('roots', {}).values()}
        if source and path.split('/')[0] not in root_names:
            return local
        return self._local(self.root / (path or '.'), fragment, original)

    def check(self):
        failures, counts = [], Counter()
        for key, target in self.config.get('roots', {}).items():
            result = self._local(self.root / target, '', target)
            if result['status'] != 'local':
                failures.append({'root': key, **result})
        for alias in self.config.get('aliases', []):
            result = self._local(self.root / alias['target'], '', alias['source'])
            if result['status'] != 'local':
                failures.append({'alias': alias['source'], **result})
        for document in self.config['managed_documents']:
            file = self.inside(self.root / document)
            if not file.is_file():
                failures.append({'document': document, 'reason': 'managed_document_missing'}); continue
            for reference in markdown_links(file.read_text(encoding='utf-8')):
                result = self.resolve(reference, document)
                counts[result['status']] += 1
                if result['status'] not in {'local', 'external'}:
                    failures.append({'document': document, **result})
        manifest = self.inside(self.root / self.config['manifest'])
        with manifest.open(encoding='utf-8', newline='') as stream:
            rows = list(csv.DictReader(stream))
        seen = set()
        for row in rows:
            name = row['relative_path']
            if name in seen:
                failures.append({'file': name, 'reason': 'duplicate_manifest_entry'})
            seen.add(name)
            result = self._local(self.root / name, '', name)
            if result['status'] != 'local':
                failures.append(result); continue
            data = Path(result['absolute_path']).read_bytes()
            if len(data) != int(row['bytes']) or hashlib.sha256(data).hexdigest() != row['sha256']:
                failures.append({'file': name, 'reason': 'manifest_mismatch'})
        expected = set(self.config.get('manifest_files', []))
        for directory in self.config.get('manifest_roots', []):
            for path in self.inside(self.root / directory).rglob('*'):
                if path.is_file() and '__pycache__' not in path.parts and path.name != '.DS_Store' and path.suffix != '.pyc':
                    expected.add(path.relative_to(self.root).as_posix())
        if expected and expected != seen:
            failures.append({'reason': 'manifest_coverage', 'missing': sorted(expected - seen),
                             'unexpected': sorted(seen - expected)})
        return {'status': 'pass' if not failures else 'fail', 'links': dict(counts),
                'manifest_entries': len(rows), 'failures': failures}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    resolve = sub.add_parser('resolve', help='Temukan rujukan lokal atau klasifikasikan sumber yang tidak disertakan')
    resolve.add_argument('reference')
    resolve.add_argument('--from', dest='source', help='Path dokumen terhadap root clone')
    resolve.add_argument('--json', action='store_true')
    check = sub.add_parser('check', help='Periksa pintu masuk, indeks, alias, dan manifest')
    check.add_argument('--json', action='store_true')
    args = parser.parse_args()
    try:
        library = Library()
        result = library.resolve(args.reference, args.source) if args.command == 'resolve' else library.check()
    except (OSError, ValueError, KeyError) as error:
        print(json.dumps({'status': 'invalid', 'reason': str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2
    if args.json or args.command == 'check':
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(result.get('absolute_path') or result.get('url') or json.dumps(result, ensure_ascii=False))
    return 0 if result['status'] in {'local', 'external', 'pass'} else 1


if __name__ == '__main__':
    sys.exit(main())
