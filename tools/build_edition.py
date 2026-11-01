#!/usr/bin/env python3
"""Pembangun edisi umum: pohon turunan dari daftar izin, dibaca dari blob commit, ditulis ke luar clone.

Stdout hanya JSON berisi jumlah dan `path_sha256`. Path, baris, dan grup ditulis ke N-49.
Teks cocokan dan isi pola tidak pernah keluar dari proses.
"""
from pathlib import Path
from urllib.parse import quote, unquote
import argparse
import csv
import fnmatch
import hashlib
import importlib.util
import io
import json
import os
import posixpath
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata
import zipfile

# Memuat resolver tidak boleh menyisakan __pycache__ pada pohon edisi atau clone.
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]

ALLOWLIST = 'edisi-umum/DAFTAR-IZIN.json'
STAMP = 'edisi-umum/STEMPEL.txt'
FRONT_TEMPLATE = 'edisi-umum/HALAMAN-DEPAN.md.tmpl'
HARNESS_TEMPLATE = 'edisi-umum/HARNESS-EDISI.md.tmpl'
PATTERNS = 'work/edisi-umum/POLA-PINDAI.txt'
REPORT = 'work/edisi-umum/LAPORAN-BUILD.json'
POLICY = 'KEBIJAKAN-SENSITIVITAS.md'
POINTER = 'TEMPLAT-PENUNJUK.md'
ACCESS_GUIDE = 'PANDUAN-AKSES.md'
RESOLVER = 'tools/library.py'
SKILL_CATALOG = '3 Skills/KATALOG.jsonl'
SKILL_COPIES = ('3 Skills/kanonik', '3 Skills/registry-fleet')
SALVAGE = '_salvage-profil-merge-1010'
WIKI = '4 Knowledge Bank/wiki-information-library/'
ROLES = '2 Roles/peran-fleet/'
HOLDER_SUFFIX = '.pohon-lama'
OUTPUT_NAME = 'ai-knowledge-library-edisi-umum'

STAMP_ID = 'library-edition-stamp:v1'
ALLOWLIST_SCHEMA_VERSION = 1
EDITION_SCHEMA_VERSION = 1
LIBRARY_SCHEMA_VERSION = 1
CATALOG_SCHEMA_VERSION = 1
EDITION_ID = 'edisi-umum'
INSTRUCTION_AUTHORITY_NONE = 'none'
CATALOG_MAX_CHARS = 25000 * 2
CATALOG_DESCRIPTION_MAX_CHARS = 120
INDEX_MAX_CHARS = 100000
DERIVED_MIN_CHARS = 5
# Label keluarga skill pada `perkara` wiki, bukan nama perkara: bila ikut, folder skill keluarga itu tertolak semua.
# Hanya nilai `perkara` yang dikecualikan; stem berkas wiki bernama sama tetap masuk pembanding.
DERIVED_FAMILY_LABEL = 'gsp-orchestration'
OOXML_MEMBER_MAX_BYTES = 64 * 1024 * 1024
CONTROL_BLOB_MAX_BYTES = 16 * 1024 * 1024

GROUPS = ('GOV_DEF', 'CLASS_MARK', 'COMMERCIAL', 'PERSONAL', 'CLIENT_DOC', 'HOST', 'CREDENTIAL', 'RULE_TEXT')
CONTROL_GROUPS = ('GOV_DEF', 'RULE_TEXT')
UNREVIEWABLE = {'GOV_DEF', 'RULE_TEXT'}
DERIVED_NAME = 'DERIVED_NAME'
BASES = {'template-default', 'documentation-example', 'public-regulator', 'fixture', 'generic-word'}
TOP_KEYS = {'schema_version', 'id', 'approval', 'publish_access_docs', 'admitted_extensions', 'drop_globs',
            'harness_template_source_sha256', 'entries', 'skills', 'scan_reviews', 'rule_text_exempt_sha256'}
PLACEHOLDERS = {'SOURCE_COMMIT', 'FILE_COUNT', 'COLLECTION_ROWS'}

SCRIPT_SUFFIXES = {'.py', '.sh', '.js', '.cjs', '.mjs', '.ts', '.ps1', '.bat', '.patch'}
DENIED_SUFFIXES = {'.zip', '.tar', '.gz', '.tgz', '.bz2', '.xz', '.7z', '.rar', '.db', '.sqlite', '.sqlite3'}
SIDECAR_SUFFIXES = ('-wal', '-shm', '-journal')
SQLITE_HEADER = b'SQLite format 3\x00'
OOXML_SUFFIXES = {'.docx', '.xlsx'}
DENIED_ROOTS = {'docs', 'work', 'graft', 'tests', 'edisi-umum'}
RESERVED_ROOTS = {'ekas', 'roles', 'skills', 'fleet', 'gsp-hermes', 'c:', '$localappdata', '%localappdata%', '~'}
AUTOLOAD_NAMES = {'agents.md', 'claude.md', 'gemini.md'}
BUILT_ROOT_FILES = {'README.md', 'HARNESS.md', 'library.json', 'MANIFEST.csv', '.gitignore', '.gitattributes'}
COPIED_REQUIRED = ('AGENTS.md', 'CLAUDE.md', POLICY, RESOLVER)
SOURCE_REQUIRED = ('HARNESS.md', 'library.json')
BOM = b'\xef\xbb\xbf'
GITIGNORE = b'.DS_Store\n__pycache__/\n*.pyc\n/graft/\n/.graft/\n'
GITATTRIBUTES = b'* -text\n'
VIOLATION_ORDER = ('harness_autoload_path', 'denied_path', 'reserved_root_name', 'denied_type')


class Blocked(Exception):
    """Berhenti dengan satu `reason`. `details` hanya menuju N-49, `extra` boleh ke stdout (jumlah saja)."""

    def __init__(self, reason, details=(), **extra):
        super().__init__(reason)
        self.reason, self.details, self.extra = reason, list(details), extra


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def path_sha256(path):
    return sha256(path.encode('utf-8', 'surrogateescape'))


def sort_key(path):
    return path.encode('utf-8', 'surrogateescape')


def json_bytes(value):
    return (json.dumps(value, ensure_ascii=False, indent=2) + '\n').encode('utf-8')


class Repository:
    """Akses baca blob commit. Variabel GIT_* diabaikan agar sumber tidak ditentukan lingkungan."""

    def __init__(self, root):
        self.root = root
        self.env = {key: value for key, value in os.environ.items() if not key.startswith('GIT_')}
        self.env['GIT_NO_REPLACE_OBJECTS'] = '1'
        self.batch = None

    def run(self, *args):
        return subprocess.run(['git', '-C', str(self.root), *args], capture_output=True, env=self.env)

    def commit(self, reference):
        done = self.run('rev-parse', '--verify', '--quiet', '--end-of-options', reference + '^{commit}')
        if done.returncode:
            raise Blocked('source_ref_invalid')
        return done.stdout.decode('ascii').strip()

    def listing(self, commit):
        done = self.run('ls-tree', '-r', '-t', '-l', '-z', '--full-tree', commit)
        if done.returncode:
            raise Blocked('source_ref_invalid')
        files, trees = {}, {}
        for record in done.stdout.split(b'\0'):
            if not record:
                continue
            meta, raw = record.split(b'\t', 1)
            mode, kind, oid, size = meta.split()
            path = raw.decode('utf-8', 'surrogateescape')
            if kind == b'tree':
                trees[path] = oid.decode('ascii')
            else:
                files[path] = (mode.decode('ascii'), oid.decode('ascii'), 0 if size == b'-' else int(size))
        return files, trees

    def blob(self, oid):
        if self.batch is None:
            self.batch = subprocess.Popen(['git', '-C', str(self.root), 'cat-file', '--batch'], env=self.env,
                                          stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        self.batch.stdin.write(oid.encode('ascii') + b'\n')
        self.batch.stdin.flush()
        header = self.batch.stdout.readline().split()
        if len(header) != 3:
            raise KeyError('objek tidak terbaca')
        data = self.batch.stdout.read(int(header[2]))
        self.batch.stdout.read(1)
        return data

    def tree_difference(self, old, new):
        """Jumlah ditambah, diubah, dihapus antara dua tree. None bila pin lama tidak dikenal repositori."""
        counts = {'added': 0, 'changed': 0, 'removed': 0}
        done = self.run('diff-tree', '-r', '--no-renames', '--name-status', '-z', old, new)
        if done.returncode:
            return {key: None for key in counts}
        names = {b'A': 'added', b'D': 'removed'}
        for status in done.stdout.split(b'\0')[::2]:
            if status:
                counts[names.get(status, 'changed')] += 1
        return counts

    def close(self):
        if self.batch is not None:
            self.batch.stdin.close()
            self.batch.stdout.close()
            self.batch.wait()
            self.batch = None


# Tahap 1: lokasi keluaran.

def inside(child, parent):
    """Menaiki leluhur `child` dan membandingkan identitas berkas: sistem berkas tak peka kapitalisasi tetap tertangkap."""
    current = Path(os.path.realpath(child))
    for candidate in (current, *current.parents):
        try:
            if os.path.samefile(candidate, parent):
                return True
        except OSError:
            continue
    return False


def old_edition_commit(output):
    """Pohon lama hanya diterima bila memang edisi; selain itu folder asing tidak disentuh."""
    try:
        config = json.loads((output / 'library.json').read_text(encoding='utf-8'))
        edition = config['edition']
        if edition['id'] != EDITION_ID:
            raise ValueError
    except (OSError, ValueError, KeyError, TypeError):
        raise Blocked('output_not_allowed') from None
    commit = edition.get('source_commit')
    return commit[:7] if isinstance(commit, str) and re.fullmatch(r'[0-9a-f]{7,64}', commit) else 'tanpa-commit'


def holder_path(output):
    return Path(os.path.realpath(output) + HOLDER_SUFFIX)


def check_output(output, root):
    if inside(output, root) or inside(root, output):
        raise Blocked('output_not_allowed')
    holder = holder_path(output)
    if inside(holder, root) or inside(root, holder):
        raise Blocked('output_not_allowed')
    if not os.path.lexists(output):
        return None
    if not output.is_dir():
        raise Blocked('output_not_allowed')
    if not any(output.iterdir()):
        return None
    short = old_edition_commit(output)
    if os.path.lexists(holder):
        if holder.is_symlink() or not holder.is_dir() or not os.access(holder, os.W_OK | os.X_OK):
            raise Blocked('output_not_allowed')
    elif not os.access(holder.parent, os.W_OK | os.X_OK):
        raise Blocked('output_not_allowed')
    return short


# Tahap 2: masukan dari blob commit.

def invalid(field):
    return Blocked('allowlist_invalid', [{'field': field}])


def is_hex(value, sizes=(64,)):
    return isinstance(value, str) and len(value) in sizes and re.fullmatch(r'[0-9a-f]+', value) is not None


def valid_relative(path):
    if not isinstance(path, str) or not path or path.startswith('/') or path.endswith('/') or re.search(r'[*?\[\]\\\x00-\x1f]', path):
        return False
    return not any(part in {'', '.', '..'} for part in path.split('/'))


def valid_include(items):
    """Daftar positif relatif terhadap salinan: urut byte, tanpa duplikat, tanpa surrogat, memuat `SKILL.md`."""
    if not isinstance(items, list) or 'SKILL.md' not in items or not all(valid_relative(item) for item in items):
        return False
    try:
        keys = [item.encode('utf-8') for item in items]
    except UnicodeEncodeError:
        return False
    return keys == sorted(set(keys))


def validate_allowlist(raw):
    """Skema tertutup: kunci tak dikenal ditolak, jadi kolom pengecualian tidak dapat ditambahkan.

    Satu-satunya kunci opsional pada salinan skill adalah `include`, daftar positif. Semua salinan satu
    skill sama-sama memakainya dengan daftar yang sama, atau sama-sama tanpa `include`.
    """
    try:
        config = json.loads(raw.decode('utf-8'))
    except ValueError:
        raise invalid('json') from None
    if not isinstance(config, dict):
        raise invalid('json')
    if set(config) - TOP_KEYS or (TOP_KEYS - {'approval'}) - set(config):
        raise invalid('keys')
    if config['schema_version'] != ALLOWLIST_SCHEMA_VERSION or config['id'] != EDITION_ID:
        raise invalid('version')
    if 'approval' in config:
        approval = config['approval']
        if not isinstance(approval, dict) or set(approval) != {'status', 'date', 'decision_ref'}:
            raise invalid('approval')
        if not all(isinstance(value, str) and value for value in approval.values()):
            raise invalid('approval')
    if not isinstance(config['publish_access_docs'], bool):
        raise invalid('publish_access_docs')
    extensions = config['admitted_extensions']
    if not isinstance(extensions, list) or not all(isinstance(item, str) and re.fullmatch(r'\.[a-z0-9]+', item) for item in extensions):
        raise invalid('admitted_extensions')
    if set(extensions) & (SCRIPT_SUFFIXES | DENIED_SUFFIXES):
        raise invalid('admitted_extensions')
    globs = config['drop_globs']
    if not isinstance(globs, list) or not all(isinstance(item, str) and item and '/' not in item for item in globs):
        raise invalid('drop_globs')
    if not is_hex(config['harness_template_source_sha256']):
        raise invalid('harness_template_source_sha256')
    if not isinstance(config['entries'], list) or not isinstance(config['skills'], list):
        raise invalid('entries')
    for entry in config['entries']:
        if not isinstance(entry, dict) or not valid_relative(entry.get('path')):
            raise invalid('entries')
        pin = {'file': 'blob', 'tree': 'tree'}.get(entry.get('kind'))
        if pin is None or set(entry) != {'kind', 'path', pin} or not is_hex(entry[pin], (40, 64)):
            raise invalid('entries')
    names = set()
    for skill in config['skills']:
        if not isinstance(skill, dict) or set(skill) != {'name', 'copies'} or not isinstance(skill['name'], str):
            raise invalid('skills')
        if not skill['name'] or skill['name'] in names or not isinstance(skill['copies'], list) or not skill['copies']:
            raise invalid('skills')
        names.add(skill['name'])
        for copy in skill['copies']:
            if not isinstance(copy, dict) or set(copy) - {'include'} != {'path', 'tree'} or not is_hex(copy['tree'], (40, 64)):
                raise invalid('skills')
            if not valid_relative(copy['path']) or not any(copy['path'].startswith(base + '/') for base in SKILL_COPIES):
                raise invalid('skills')
            if 'include' in copy and not valid_include(copy['include']):
                raise invalid('include')
            if copy.get('include') != skill['copies'][0].get('include'):
                raise invalid('include')
    for review in config['scan_reviews']:
        if not isinstance(review, dict) or set(review) != {'group', 'source_sha256', 'lines', 'basis'}:
            raise invalid('scan_reviews')
        if review['group'] not in (set(GROUPS) - UNREVIEWABLE) | {DERIVED_NAME}:
            raise invalid('scan_reviews')
        if not is_hex(review['source_sha256']) or review['basis'] not in BASES:
            raise invalid('scan_reviews')
        if not isinstance(review['lines'], int) or isinstance(review['lines'], bool) or review['lines'] < 1:
            raise invalid('scan_reviews')
    exempt = config['rule_text_exempt_sha256']
    if not isinstance(exempt, list) or not all(is_hex(item) for item in exempt):
        raise invalid('rule_text_exempt_sha256')
    return config


def validate_stamp(raw):
    try:
        lines = raw.decode('utf-8').replace('\r\n', '\n').rstrip('\n').split('\n')
    except UnicodeDecodeError:
        raise invalid('stamp') from None
    if not 1 <= len(lines) <= 3 or STAMP_ID not in lines[0]:
        raise invalid('stamp')
    for line in lines:
        if not line.startswith('> ') or re.search(r'\]\(|`{3}|~{3}|(?:id|name)=', line) or re.match(r'>\s*#', line):
            raise invalid('stamp')
    return [line.encode('utf-8') for line in lines]


def validate_template(raw):
    try:
        text = raw.decode('utf-8')
    except UnicodeDecodeError:
        raise invalid('template') from None
    if set(re.findall(r'\{\{([^{}]*)\}\}', text)) - PLACEHOLDERS:
        raise invalid('template')
    return text


# Tahap 3 dan 4: pola, gagal tertutup.

def load_patterns(root):
    try:
        lines = (root / PATTERNS).read_text(encoding='utf-8').splitlines()
    except (OSError, UnicodeDecodeError):
        raise Blocked('pattern_file_invalid') from None
    compiled = []
    for number, line in enumerate(lines, 1):
        if not line.strip() or line.startswith('#'):
            continue
        group, tab, expression = line.partition('\t')
        if not tab or group not in GROUPS or not expression:
            raise Blocked('pattern_file_invalid', [{'line': number}])
        try:
            compiled.append((group, re.compile(expression)))
        except re.error:
            raise Blocked('pattern_file_invalid', [{'line': number}]) from None
    missing = set(GROUPS) - {group for group, _ in compiled}
    if missing:
        raise Blocked('pattern_file_invalid', [{'group': group} for group in sorted(missing)])
    return compiled


def control_patterns(patterns, files, repository):
    """Grup kontrol harus cocok pada clone penuh; hasil nol berarti pola rusak, bukan koleksi bersih."""
    pending = {group for group in CONTROL_GROUPS}
    active = [(group, regex) for group, regex in patterns if group in pending]
    for path in sorted(files, key=sort_key):
        if not pending:
            return
        mode, oid, size = files[path]
        pending -= {group for group, regex in active if regex.search(path)}
        if mode in {'120000', '160000'} or size > CONTROL_BLOB_MAX_BYTES or not pending:
            continue
        text = repository.blob(oid).decode('utf-8', 'replace')
        pending -= {group for group, regex in active if group in pending and regex.search(text)}
    if pending:
        raise Blocked('pattern_control_failed', [{'group': group} for group in sorted(pending)])


# Pembacaan frontmatter: subset, tanpa YAML.

def frontmatter_lines(data):
    if data.startswith(BOM):
        data = data[len(BOM):]
    text = data.decode('utf-8').replace('\r\n', '\n').replace('\r', '\n')
    lines = text.split('\n')
    if not lines or lines[0].rstrip() != '---':
        return None
    for index, line in enumerate(lines[1:], 1):
        if line.rstrip() == '---':
            return lines[1:index]
    raise ValueError('frontmatter tidak tertutup')


def _quoted(first, lines, position):
    quote_mark = first[0]
    buffer, current = [], first[1:]
    while True:
        result, index = [], 0
        while index < len(current):
            char = current[index]
            if quote_mark == "'" and char == "'":
                if current[index + 1:index + 2] == "'":
                    result.append("'"); index += 2; continue
                buffer.append(''.join(result))
                return ' '.join(part.strip() for part in buffer), position
            if quote_mark == '"' and char == '\\':
                following = current[index + 1:index + 2]
                result.append({'n': '\n', 't': '\t'}.get(following, following)); index += 2; continue
            if quote_mark == '"' and char == '"':
                buffer.append(''.join(result))
                return ' '.join(part.strip() for part in buffer), position
            result.append(char); index += 1
        buffer.append(''.join(result))
        position += 1
        if position >= len(lines):
            raise ValueError('kutip tidak tertutup')
        current = lines[position]


def parse_frontmatter(data):
    """Kunci tingkat atas saja: polos, kutip, blok `>` dan `|`, polos multibaris, larik sebaris dan larik blok."""
    lines = frontmatter_lines(data)
    if lines is None:
        return {}
    values, position = {}, 0
    while position < len(lines):
        match = re.match(r'^([A-Za-z_][\w-]*):(?:[ \t]+(.*))?$', lines[position])
        position += 1
        if not match:
            continue
        key, value = match[1], (match[2] or '').strip()
        if re.fullmatch(r'[|>][+-]?\d?[+-]?', value):
            block = []
            while position < len(lines) and (not lines[position].strip() or lines[position][0] in ' \t'):
                block.append(lines[position].strip()); position += 1
            values[key] = ' '.join(part for part in block if part)
        elif value[:1] in {'"', "'"}:
            values[key], position = _quoted(value, lines, position - 1)
            position += 1
        elif value.startswith('['):
            if not value.endswith(']'):
                raise ValueError('larik tidak tertutup')
            values[key] = [item.strip().strip('"\'') for item in value[1:-1].split(',') if item.strip()]
        elif not value:
            items = []
            while position < len(lines) and re.match(r'^\s*- ', lines[position]):
                items.append(lines[position].split('- ', 1)[1].strip().strip('"\'')); position += 1
            if items:
                values[key] = items
            else:
                while position < len(lines) and lines[position][:1] in {' ', '\t'}:
                    position += 1
                values[key] = ''
        else:
            parts = [re.sub(r'\s+#.*$', '', value)]
            while position < len(lines) and lines[position][:1] in {' ', '\t'} and lines[position].strip():
                parts.append(lines[position].strip()); position += 1
            values[key] = ' '.join(parts)
    return values


def skill_name(data):
    try:
        name = parse_frontmatter(data).get('name')
    except (ValueError, UnicodeDecodeError):
        return None
    return name if isinstance(name, str) and name else None


# Tahap 5: pin, aturan name, larangan.

def path_violation(path):
    parts = path.split('/')
    if any(part.startswith('.') for part in parts):
        return 'harness_autoload_path'
    if any('\udc80' <= char <= '\udcff' for char in path):
        return 'denied_path'
    if parts[0].casefold() in DENIED_ROOTS or (parts[0] == 'tools' and path != RESOLVER):
        return 'denied_path'
    if path.startswith(ROLES) and parts[-1] == '_INDEX.md':
        return 'denied_path'
    if len(parts) > 1 and parts[-1].casefold() in AUTOLOAD_NAMES:
        return 'harness_autoload_path'
    if parts[0].casefold() in RESERVED_ROOTS:
        return 'reserved_root_name'
    lowered = parts[-1].casefold()
    if Path(lowered).suffix in DENIED_SUFFIXES or lowered.endswith(SIDECAR_SUFFIXES):
        return 'denied_type'
    return None


def raise_violations(found):
    for reason in VIOLATION_ORDER:
        if found.get(reason):
            raise Blocked(reason, [{'path': path} for path in sorted(found[reason], key=sort_key)])


def is_built_collection_file(path):
    parts = path.split('/')
    return (len(parts) == 2 and parts[1] == 'INDEKS.md') or path == SKILL_CATALOG


def covered(files, base):
    return [path for path in files if path.startswith(base + '/')]


def check_pins(config, files, trees, repository):
    mismatch = []
    for entry in config['entries']:
        path = entry['path']
        if entry['kind'] == 'file':
            current = files.get(path, (None, None, 0))[1]
            if current != entry['blob']:
                difference = {'added': 0, 'changed': 0, 'removed': 0}
                difference['changed' if current else 'removed'] = 1
                mismatch.append({'path': path, **difference})
        elif trees.get(path) != entry['tree']:
            mismatch.append({'path': path, **pin_difference(repository, entry['tree'], trees.get(path))})
    for skill in config['skills']:
        for copy in skill['copies']:
            if trees.get(copy['path']) != copy['tree']:
                mismatch.append({'path': copy['path'], **pin_difference(repository, copy['tree'], trees.get(copy['path']))})
    if mismatch:
        raise Blocked('allowlist_pin_mismatch', mismatch)


def pin_difference(repository, old, new):
    if new is None:
        return {'added': 0, 'changed': 0, 'removed': None}
    return repository.tree_difference(old, new)


def check_skills(config, files, repository):
    """Skill per `name` beserta semua salinannya; nama yang ditolak tidak dapat masuk lewat kembaran."""
    folders = {}
    for path in files:
        if posixpath.basename(path) == 'SKILL.md' and path.startswith('3 Skills/'):
            name = skill_name(repository.blob(files[path][1]))
            folders.setdefault(name, set()).add(posixpath.dirname(path))
    nested, mismatch = [], []
    owned = []
    for skill in config['skills']:
        listed = {copy['path'] for copy in skill['copies']}
        if listed != folders.get(skill['name'], set()):
            mismatch.append({'skill': skill['name'], 'listed': len(listed),
                             'found': len(folders.get(skill['name'], set()))})
        owned += [(copy['path'], skill['name']) for copy in skill['copies']]
    owned += [(entry['path'], None) for entry in config['entries'] if entry['kind'] == 'tree']
    for base, owner in owned:
        for path in covered(files, base):
            if posixpath.basename(path) == 'SKILL.md' and (owner is None or skill_name(repository.blob(files[path][1])) != owner):
                nested.append({'path': path})
    for entry in config['entries']:
        if entry['kind'] == 'file' and posixpath.basename(entry['path']) == 'SKILL.md':
            nested.append({'path': entry['path']})
    if nested:
        raise Blocked('skill_nested_unlisted', nested)
    if mismatch:
        raise Blocked('skill_copies_mismatch', mismatch)


def select_files(config, files, trees, repository):
    found = {}
    for entry in config['entries']:
        path = entry['path']
        if path in BUILT_ROOT_FILES or is_built_collection_file(path):
            raise invalid('entries')
        violation = path_violation(path)
        if violation:
            found.setdefault(violation, []).append(path)
    raise_violations(found)
    grouped = [entry['path'] for entry in config['entries'] if entry['path'] == '3 Skills' or entry['path'].startswith('3 Skills/')]
    if grouped:
        raise Blocked('skill_nested_unlisted', [{'path': path} for path in grouped])
    check_pins(config, files, trees, repository)
    check_skills(config, files, repository)
    candidates, listed = set(), set()
    for entry in config['entries']:
        candidates.update([entry['path']] if entry['kind'] == 'file' else covered(files, entry['path']))
    for skill in config['skills']:
        for copy in skill['copies']:
            if 'include' in copy:
                listed.update(f"{copy['path']}/{item}" for item in copy['include'])
            else:
                candidates.update(covered(files, copy['path']))
    missing = listed - files.keys()
    if missing:
        raise Blocked('skill_include_missing', [{'path': path} for path in sorted(missing, key=sort_key)])
    candidates |= listed
    extensions = set(config['admitted_extensions'])
    admitted, found, unused = {}, {}, []
    for path in sorted(candidates, key=sort_key):
        violation = path_violation(path)
        if violation:
            found.setdefault(violation, []).append(path)
            continue
        if files[path][0] in {'120000', '160000'}:
            found.setdefault('denied_type', []).append(path)
            continue
        if is_built_collection_file(path):
            continue
        name = posixpath.basename(path)
        if path != RESOLVER and (Path(name.casefold()).suffix not in extensions
                                 or any(fnmatch.fnmatchcase(name, pattern) for pattern in config['drop_globs'])):
            # Daftar positif tidak boleh gugur diam-diam.
            if path in listed:
                unused.append(path)
            continue
        admitted[path] = files[path][1]
    raise_violations(found)
    if unused:
        raise Blocked('skill_include_not_admitted', [{'path': path} for path in unused])
    return admitted


def check_required(config, files, admitted):
    missing = [path for path in COPIED_REQUIRED if path not in admitted]
    missing += [path for path in SOURCE_REQUIRED if path not in files]
    for path in (POINTER, ACCESS_GUIDE):
        if (path in admitted) != config['publish_access_docs']:
            missing.append(path)
    if missing:
        raise Blocked('required_file_missing', [{'path': path} for path in missing])


# Tahap 6 sampai 8: hasil.

def collision_key(path):
    return unicodedata.normalize('NFC', path).casefold()


def check_collisions(names):
    seen, clashes = {}, []
    for name in sorted(names, key=sort_key):
        key = collision_key(name)
        if key in seen:
            clashes.append({'path': name})
        seen[key] = name
    if clashes:
        raise Blocked('path_collision', clashes)


def stamp_block(stamp, eol):
    return eol.join(stamp) + eol + eol


def insert_stamp(path, data, stamp):
    """Stempel setelah penutup frontmatter pada byte; menghapus blok ini mengembalikan byte sumber."""
    if data.startswith(BOM):
        raise Blocked('frontmatter_bom', [{'path': path}])
    eol = b'\r\n' if b'\r\n' in data else b'\n'
    opening = re.match(rb'---[ \t\r]*\n', data)
    position = 0
    if opening:
        closing = re.compile(rb'^---[ \t\r]*\n', re.M).search(data, opening.end())
        if not closing:
            raise Blocked('frontmatter_unclosed', [{'path': path}])
        position = closing.end()
    return data[:position] + stamp_block(stamp, eol) + data[position:]


def normalize_description(value):
    text = re.sub(r'\s+', ' ', value).strip()
    if len(text) <= CATALOG_DESCRIPTION_MAX_CHARS:
        return text
    head = text[:CATALOG_DESCRIPTION_MAX_CHARS - 4]
    if ' ' in head:
        head = head[:head.rindex(' ')]
    return head.rstrip() + ' ...'


def comparable(data):
    data = data.replace(b'\r\n', b'\n').replace(b'\r', b'\n')
    for token in (b'../', b'registry-fleet/', b'kanonik/'):
        data = data.replace(token, b'')
    return data


def content_differs(folder, contents):
    """Bandingkan folder skill terpilih dengan folder kembarannya; satu salinan saja berarti tidak berbeda."""
    for base, other in (SKILL_COPIES, SKILL_COPIES[::-1]):
        if folder.startswith(base + '/'):
            twin = other + folder[len(base):]
            break
    else:
        return False

    def members(root):
        return {path[len(root) + 1:] for path in contents if path.startswith(root + '/')}
    mine, theirs = members(folder), members(twin)
    if not theirs:
        return False
    if any('.bak' not in posixpath.basename(name) for name in mine ^ theirs):
        return True
    return any(comparable(contents[f'{folder}/{name}']) != comparable(contents[f'{twin}/{name}']) for name in mine & theirs)


def catalog_rows(contents):
    groups = {}
    for path, data in contents.items():
        if posixpath.basename(path) != 'SKILL.md' or not any(path.startswith(base + '/') for base in SKILL_COPIES):
            continue
        if 'fixtures' in path.split('/'):
            continue
        try:
            values = parse_frontmatter(data)
        except (ValueError, UnicodeDecodeError):
            raise Blocked('catalog_schema', [{'path': path}]) from None
        name = values.get('name')
        if not isinstance(name, str) or not name:
            raise Blocked('catalog_schema', [{'path': path}])
        groups.setdefault(name, []).append((path, values))
    rows = []
    for name in sorted(groups):
        def rank(item):
            path = item[0]
            return (path.split('/', 2)[2].startswith(SALVAGE + '/'), len(path.split('/')),
                    not path.startswith(SKILL_COPIES[0] + '/'), path)
        path, values = min(groups[name], key=rank)
        description = values.get('description')
        if not isinstance(description, str) or not re.sub(r'\s+', '', description):
            raise Blocked('catalog_schema', [{'path': path}])
        rows.append({'name': name, 'description': normalize_description(description), 'path': path,
                     'content_diff': content_differs(posixpath.dirname(path), contents),
                     'instruction_authority': INSTRUCTION_AUTHORITY_NONE})
    return rows


def render_catalog(rows):
    lines = [{'catalog_schema_version': CATALOG_SCHEMA_VERSION, 'rows': len(rows)}, *rows]
    return ''.join(json.dumps(line, ensure_ascii=False, separators=(',', ':')) + '\n' for line in lines)


def validate_catalog(text, names):
    """Validasi N-05 saat build (RK-12); setelah build, MANIFEST.csv mengunci byte-nya."""
    if len(text) > CATALOG_MAX_CHARS:
        raise Blocked('catalog_oversize', [{'path': SKILL_CATALOG, 'chars': len(text)}])
    columns = ['name', 'description', 'path', 'content_diff', 'instruction_authority']
    schema = Blocked('catalog_schema', [{'path': SKILL_CATALOG}])
    if not text.endswith('\n'):
        raise schema
    try:
        head, *rows = [json.loads(line) for line in text[:-1].split('\n')]
    except ValueError:
        raise schema from None
    if not isinstance(head, dict) or list(head) != ['catalog_schema_version', 'rows']:
        raise schema
    if head['catalog_schema_version'] != CATALOG_SCHEMA_VERSION or head['rows'] != len(rows):
        raise schema
    previous = None
    for row in rows:
        if not isinstance(row, dict) or list(row) != columns:
            raise schema
        if not isinstance(row['name'], str) or not row['name'] or not isinstance(row['description'], str) or not row['description']:
            raise schema
        if not isinstance(row['content_diff'], bool) or row['instruction_authority'] != INSTRUCTION_AUTHORITY_NONE:
            raise schema
        if len(row['description']) > CATALOG_DESCRIPTION_MAX_CHARS:
            raise schema
        if not isinstance(row['path'], str) or row['path'] not in names or not any(row['path'].startswith(base + '/') for base in SKILL_COPIES):
            raise schema
        if 'fixtures' in row['path'].split('/') or (previous is not None and row['name'] <= previous):
            raise schema
        previous = row['name']


def table_cell(value):
    return value.replace('|', '\\|')


def render_index(collection, rows, stamp):
    """`rows`: (path relatif terhadap koleksi, byte). Tanpa tanggal dan deskripsi; tidak membaca INDEKS sumber."""
    lines = [f'# Indeks {collection}'.encode('utf-8'), b'',
             b'Daftar berkas koleksi ini pada edisi umum, dibuat dari pohon edisi.', b'',
             b'| Berkas | Byte |', b'|---|---:|']
    for name, size in sorted(rows, key=lambda item: sort_key(item[0])):
        lines.append(f'| [{table_cell(name)}]({quote(name, safe="/")}) | {size} |'.encode('utf-8'))
    return stamp_block(stamp, b'\n') + b'\n'.join(lines) + b'\n'


def check_index_size(path, data):
    chars = len(data.decode('utf-8'))
    if chars > INDEX_MAX_CHARS:
        raise Blocked('index_oversize', [{'path': path, 'chars': chars}])


def collection_of(path):
    return path.split('/')[0] if '/' in path else None


def build_library_config(source, config, names, commit, allowlist_hash, expected_missing, collections):
    def present(target):
        target = target.rstrip('/')
        return target in names or any(name.startswith(target + '/') for name in names)
    roots = {key: value for key, value in source.get('roots', {}).items() if present(value)}
    aliases = [alias for alias in source.get('aliases', []) if present(alias['target'])]
    access = [path for path in (POINTER, ACCESS_GUIDE) if config['publish_access_docs']]
    indexes = [f'{collection}/INDEKS.md' for collection in collections]
    root_files = sorted((name for name in names if '/' not in name and name not in BUILT_ROOT_FILES
                         and name not in {'AGENTS.md', 'CLAUDE.md', POLICY, POINTER, ACCESS_GUIDE}), key=sort_key)
    return {
        'schema_version': LIBRARY_SCHEMA_VERSION,
        'entrypoint': source.get('entrypoint', 'HARNESS.md'),
        'path_convention': source.get('path_convention', ''),
        'roots': roots,
        'aliases': aliases,
        'workspace_prefixes': source.get('workspace_prefixes', []),
        'repository_urls': [],
        'managed_documents': ['README.md', 'HARNESS.md', 'AGENTS.md', 'CLAUDE.md', POLICY, *indexes, *access],
        'manifest': source.get('manifest', 'MANIFEST.csv'),
        'manifest_roots': sorted({collection_of(name) for name in names if collection_of(name)}, key=sort_key),
        'manifest_files': ['README.md', 'HARNESS.md', 'AGENTS.md', 'CLAUDE.md', 'library.json', POLICY, *access, *root_files],
        'edition': {'schema_version': EDITION_SCHEMA_VERSION, 'id': EDITION_ID, 'source_commit': commit,
                    'allowlist_sha256': allowlist_hash, 'expected_missing': expected_missing},
    }


def render_manifest(rows):
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, lineterminator='\n')
    writer.writerow(['relative_path', 'bytes', 'sha256', 'source_sha256'])
    for name in sorted(rows, key=sort_key):
        writer.writerow([name, *rows[name]])
    return stream.getvalue().encode('utf-8')


def load_resolver(tree):
    """Resolver yang dikirim, dari blob commit: keluaran tidak bergantung pada pohon kerja (TR-14)."""
    try:
        specification = importlib.util.spec_from_file_location('edition_library', tree / RESOLVER)
        module = importlib.util.module_from_spec(specification)
        specification.loader.exec_module(module)
        module.Library, module.markdown_links
        return module
    except Exception:
        raise Blocked('check_failed', [{'path': RESOLVER}]) from None


class SourcePath:
    """Path atas daftar pohon commit, agar `Library.resolve` menilai sumber tanpa menulis nama berkas ke disk."""

    def __init__(self, value, files, folders):
        self.value, self.files, self.folders = value, files, folders

    def _make(self, value):
        return SourcePath(value, self.files, self.folders)

    def __truediv__(self, other):
        other = str(other)
        return self._make(other if other.startswith('/') else posixpath.join(self.value, other))

    def __str__(self):
        return self.value

    def resolve(self):
        return self._make(posixpath.normpath(self.value))

    def relative_to(self, _root):
        if self.value.startswith('/') or self.value == '..' or self.value.startswith('../'):
            raise ValueError('di luar pohon')
        return self

    def as_posix(self):
        return self.value

    def exists(self):
        return self.value == '.' or self.value in self.files or self.value in self.folders

    def is_file(self):
        return self.value in self.files

    @property
    def parent(self):
        return self._make(posixpath.dirname(self.value) or '.')

    @property
    def suffix(self):
        return Path(self.value).suffix

    def read_text(self, encoding='utf-8'):
        # Ada-tidaknya target yang diminta; jangkar dinilai `check` pada pohon edisi.
        return ''


def folders_of(names):
    result = set()
    for name in names:
        parent = posixpath.dirname(name)
        while parent and parent not in result:
            result.add(parent)
            parent = posixpath.dirname(parent)
    return result


def source_view(module, source_config, files):
    view = object.__new__(module.Library)
    view.root = SourcePath('.', set(files), folders_of(files))
    view.config = {**source_config, 'repository_urls': []}
    return view


def count_expected_missing(module, source_config, files, documents, names):
    """N-36: tautan yang targetnya ada di sumber dan menurut daftar izin tidak ikut. Tidak membaca pohon hasil."""
    view = source_view(module, source_config, files)
    present = set(names) | folders_of(names) | {'.'}
    count = 0
    for document, data in documents.items():
        for reference in module.markdown_links(data.decode('utf-8')):
            result = view.resolve(reference, document)
            exists = result.get('status') == 'local' or result.get('reason') == 'anchor_not_found'
            if exists and result.get('relative_path') not in present:
                count += 1
    return count


def assemble(tree, config, stamp, front, harness, source_config, files, admitted, repository, commit, allowlist_hash):
    """Menulis pohon edisi. Salinan memakai byte blob; hanya `.md` mendapat stempel."""
    contents, sources, stamped = {}, {}, 0
    documents = {}
    for path in sorted(admitted, key=sort_key):
        data = repository.blob(admitted[path])
        if data.startswith(SQLITE_HEADER):
            raise Blocked('denied_type', [{'path': path}])
        sources[path] = sha256(data)
        if path.casefold().endswith('.md'):
            try:
                data.decode('utf-8')
            except UnicodeDecodeError:
                raise Blocked('binary_not_scannable', [{'path': path}]) from None
            documents[path] = data
            data = insert_stamp(path, data, stamp)
            stamped += 1
        contents[path] = data

    rows = catalog_rows(contents)
    catalog = render_catalog(rows)
    contents[SKILL_CATALOG] = catalog.encode('utf-8')

    collections = sorted({collection_of(name) for name in contents if collection_of(name)} - {'tools'}, key=sort_key)
    names = set(contents) | {'README.md', 'HARNESS.md', 'library.json', 'MANIFEST.csv', '.gitignore', '.gitattributes'}
    names |= {f'{collection}/INDEKS.md' for collection in collections}
    check_collisions(names)
    validate_catalog(catalog, names)

    for collection in collections:
        prefix = collection + '/'
        members = sorted(name for name in contents if name.startswith(prefix))
        if collection == '3 Skills':
            members = [name for name in members if posixpath.basename(name) == 'SKILL.md']
        index = render_index(collection, [(name[len(prefix):], len(contents[name])) for name in members], stamp)
        check_index_size(prefix + 'INDEKS.md', index)
        contents[prefix + 'INDEKS.md'] = index
        stamped += 1

    tally = {}
    for name in names:
        if collection_of(name):
            tally[collection_of(name)] = tally.get(collection_of(name), 0) + 1
    # Bentuk baris mengikuti kepala tabel `Koleksi | Berkas` pada N-47.
    table = ''.join(f'| [{table_cell(key)}]({quote(key)}/INDEKS.md) | {tally[key]} |\n' for key in collections)
    fills = {'SOURCE_COMMIT': commit, 'FILE_COUNT': str(len(names)), 'COLLECTION_ROWS': table.rstrip('\n')}

    def fill(text):
        return re.sub(r'\{\{([A-Z_]+)\}\}', lambda match: fills[match[1]], text).encode('utf-8')
    contents['README.md'] = insert_stamp('README.md', fill(front), stamp)
    contents['HARNESS.md'] = insert_stamp('HARNESS.md', fill(harness), stamp)
    stamped += 2
    contents['.gitignore'] = GITIGNORE
    contents['.gitattributes'] = GITATTRIBUTES

    for name, data in contents.items():
        write_file(tree, name, data)

    module = load_resolver(tree)
    expected = count_expected_missing(module, source_config, files, documents, names)
    library = build_library_config(source_config, config, names, commit, allowlist_hash, expected, collections)
    contents['library.json'] = json_bytes(library)
    write_file(tree, 'library.json', contents['library.json'])
    write_file(tree, 'MANIFEST.csv', b'relative_path,bytes,sha256,source_sha256\n')

    resolver = library_for_links(module, tree)
    broken = []
    for template in ('README.md', 'HARNESS.md'):
        for reference in module.markdown_links(contents[template].decode('utf-8')):
            if resolver.resolve(reference, template)['status'] not in {'local', 'external'}:
                broken.append({'path': template})
    if broken:
        raise Blocked('template_link_broken', broken)

    rows_manifest = {}
    for name, data in contents.items():
        if name in {'.gitignore', '.gitattributes'}:
            continue
        rows_manifest[name] = (str(len(data)), sha256(data), sources.get(name, ''))
    contents['MANIFEST.csv'] = render_manifest(rows_manifest)
    write_file(tree, 'MANIFEST.csv', contents['MANIFEST.csv'])
    return contents, sources, stamped, expected


def library_for_links(module, tree):
    try:
        return module.Library(tree)
    except Exception:
        raise Blocked('check_failed', [{'path': 'library.json'}]) from None


def write_file(tree, name, data):
    path = tree / name
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)
    os.chmod(path, 0o644)


# Tahap 9: pemindaian hasil akhir.

def scan_texts(path, data):
    """Teks yang dipindai satu berkas. Yang tidak dapat dibaca penuh menghentikan build, bukan dilewati."""
    if Path(path.casefold()).suffix in OOXML_SUFFIXES:
        texts = []
        try:
            with zipfile.ZipFile(io.BytesIO(data)) as archive:
                for member in archive.infolist():
                    if member.is_dir():
                        continue
                    if not member.filename.endswith(('.xml', '.rels')) or member.file_size > OOXML_MEMBER_MAX_BYTES:
                        raise Blocked('binary_not_scannable', [{'path': path}])
                    raw = archive.read(member)
                    if b'\x00' in raw:
                        raise Blocked('binary_not_scannable', [{'path': path}])
                    text = raw.decode('utf-8', 'replace')
                    # Word memecah teks antarlari, jadi frasa utuh hanya terlihat setelah tag dibuang.
                    texts += [text, re.sub(r'<[^>]+>', '', text)]
        except (zipfile.BadZipFile, OSError, RuntimeError, NotImplementedError):
            raise Blocked('binary_not_scannable', [{'path': path}]) from None
        return texts
    if b'\x00' in data:
        raise Blocked('binary_not_scannable', [{'path': path}])
    try:
        return [data.decode('utf-8')]
    except UnicodeDecodeError:
        raise Blocked('binary_not_scannable', [{'path': path}]) from None


def token_form(name):
    return unicodedata.normalize('NFC', name).casefold()


def token_regex(names):
    names = {token_form(name) for name in names}
    if not names:
        return None
    alternatives = '|'.join(re.escape(name) for name in sorted(names, key=lambda item: (-len(item), item)))
    return re.compile(r'(?<![^\W_])(?:' + alternatives + r')(?![^\W_])')


def collect_derived_names(files, repository):
    """Pembanding dihitung dari blob wiki pada commit, hanya di memori (RK-21).

    Frontmatter yang gagal diurai menghentikan build: nama di dalamnya tidak terbaca, jadi
    gerbang tidak dapat membuktikan nama itu absen dari edisi. Path hanya menuju N-49.
    """
    names, invalid_sources = set(), []
    for path in files:
        if not path.startswith(WIKI) or not path.endswith('.md'):
            continue
        try:
            value = parse_frontmatter(repository.blob(files[path][1])).get('perkara')
        except (ValueError, UnicodeDecodeError):
            invalid_sources.append(path)
            continue
        values = value if isinstance(value, list) else [value]
        values = [item.strip() for item in values if isinstance(item, str) and item.strip()]
        if values:
            names.update(item for item in values if token_form(item) != DERIVED_FAMILY_LABEL)
            names.add(Path(posixpath.basename(path)).stem)
    if invalid_sources:
        raise Blocked('derived_source_invalid', [{'path': path} for path in sorted(invalid_sources, key=sort_key)])
    return token_regex(name for name in names if len(name) >= DERIVED_MIN_CHARS)


def token_lines(regex, text):
    """Nomor baris cocokan, termasuk target tautan yang tersandi persen."""
    if regex is None:
        return set()
    lines = set()
    for number, line in enumerate(text.split('\n'), 1):
        folded = unicodedata.normalize('NFC', line).casefold()
        if regex.search(folded) or ('%' in folded and regex.search(unquote(folded))):
            lines.add(number)
    return lines


def pattern_lines(patterns, text):
    found = {}
    for group, regex in patterns:
        for match in regex.finditer(text):
            found.setdefault(group, set()).add(text.count('\n', 0, match.start()) + 1)
    return found


def scan_edition(contents, sources, config, patterns, derived, rejected_roles, entry_documents, allowlist_raw):
    hard, derived_hard, unreviewed, stale, used = [], [], [], [], set()
    reviews = {(item['group'], item['source_sha256']): item for item in config['scan_reviews']}
    exempt = set(config['rule_text_exempt_sha256'])
    role_mentions = 0

    def add_hit(path, group, lines, source):
        count = len(lines)
        rows = [{'path': path, 'line': line, 'group': group} for line in sorted(lines)]
        bucket = derived_hard if group == DERIVED_NAME else hard
        if not source or group in UNREVIEWABLE:
            bucket.extend(rows)
            return
        review = reviews.get((group, source))
        if review is None:
            unreviewed.extend(rows)
        elif review['lines'] != count:
            stale.append({'path': path, 'group': group, 'lines': count})
        else:
            used.add((group, source))

    for path in sorted(contents, key=sort_key):
        data, source = contents[path], sources.get(path, '')
        hard += [{'path': path, 'line': 0, 'group': group} for group, regex in patterns if regex.search(path)]
        if derived and derived.search(unicodedata.normalize('NFC', path).casefold()):
            derived_hard.append({'path': path, 'line': 0, 'group': DERIVED_NAME})
        found, names = {}, set()
        for offset, text in enumerate(scan_texts(path, data)):
            for group, lines in pattern_lines(patterns, text).items():
                found.setdefault(group, set()).update((offset, line) for line in lines)
            names.update((offset, line) for line in token_lines(derived, text))
            roles = token_lines(rejected_roles, text)
            if roles and path in entry_documents:
                derived_hard += [{'path': path, 'line': line, 'group': DERIVED_NAME} for line in sorted(roles)]
            elif roles:
                role_mentions += 1
        for group, lines in found.items():
            if group == 'RULE_TEXT' and path == POLICY and source in exempt:
                continue
            add_hit(path, group, {line for _, line in lines}, source)
        if names:
            add_hit(path, DERIVED_NAME, {line for _, line in names}, source)

    allowlist_text = allowlist_raw.decode('utf-8')
    for group, lines in pattern_lines(patterns, allowlist_text).items():
        hard += [{'path': ALLOWLIST, 'line': line, 'group': group} for line in sorted(lines)]
    derived_hard += [{'path': ALLOWLIST, 'line': line, 'group': DERIVED_NAME} for line in sorted(token_lines(derived, allowlist_text))]

    orphans = [key for key in reviews if key not in used and not any(
        item['group'] == key[0] and sources.get(item['path']) == key[1] for item in stale)]
    if hard:
        raise Blocked('scan_hit', hard)
    if derived_hard:
        raise Blocked('derived_name_hit', derived_hard)
    # Hash yang berubah terlihat sebagai cocokan tanpa tinjauan bersama entri yatim pada grup yang sama.
    orphan_groups = {group for group, _ in orphans}
    moved = [row for row in unreviewed if row['group'] in orphan_groups]
    if stale or moved:
        raise Blocked('scan_review_stale', stale + moved)
    if unreviewed:
        reason = 'derived_name_hit' if all(row['group'] == DERIVED_NAME for row in unreviewed) else 'scan_hit'
        raise Blocked(reason, unreviewed)
    if orphans:
        raise Blocked('scan_review_unused', [{'group': group} for group, _ in orphans])
    return role_mentions


# Tahap 10 dan 11.

def run_check(tree):
    """Berkas yang dikirim dijalankan terisolasi; kegagalannya menuju N-49, bukan stdout."""
    done = subprocess.run([sys.executable, '-I', str(tree / RESOLVER), 'check'], cwd=str(tree.parent),
                          capture_output=True)
    if done.returncode == 0:
        return
    try:
        failures = json.loads(done.stdout.decode('utf-8'))['failures']
    except (ValueError, KeyError, TypeError):
        failures = []
    details = []
    for failure in failures:
        path = failure.get('document') or failure.get('file') or failure.get('relative_path')
        details.append({**({'path': path} if path else {}),
                        **{key: failure[key] for key in ('reason', 'expected', 'found', 'status') if key in failure}})
    raise Blocked('check_failed', details or [{'exit': done.returncode}])


def _move(source, target):
    shutil.move(str(source), str(target))


def reserve_holder(output, short):
    holder = holder_path(output)
    try:
        holder.mkdir(parents=True, exist_ok=True)
        number = 1
        while True:
            candidate = holder / f'{short}-{number:02d}'
            try:
                candidate.mkdir()
                return candidate
            except FileExistsError:
                number += 1
    except OSError:
        raise Blocked('output_not_allowed', [{'stage': 11}]) from None


def publish(tree, output, short):
    """RK-49: pohon lama pindah ke N-83, `.git/` tetap, build tidak pernah menghapus pohon lama."""
    created = not os.path.lexists(output)
    if created:
        try:
            output.mkdir(parents=True)
        except OSError:
            raise Blocked('output_not_allowed', [{'stage': 11}]) from None
    old = sorted(name for name in os.listdir(output) if name != '.git')
    slot = reserve_holder(output, short) if old else None
    moved_old, moved_new = [], []
    try:
        for name in old:
            _move(output / name, slot / name)
            moved_old.append(name)
        for name in sorted(os.listdir(tree)):
            _move(tree / name, output / name)
            moved_new.append(name)
    except BaseException as error:
        restored = roll_back(tree, output, slot, moved_old, moved_new, len(moved_old) == len(old), created)
        if isinstance(error, OSError):
            raise Blocked('output_not_allowed', [{'stage': 11, 'restored': restored}], restored=restored) from None
        raise
    return bool(old)


def roll_back(tree, output, slot, moved_old, moved_new, old_cleared, created):
    """Yang baru kembali ke folder kerja, yang lama kembali dari N-83. Pohon lama tidak pernah dihapus."""
    restored = True
    for name in moved_new:
        try:
            shutil.move(str(output / name), str(tree / name))
        except OSError:
            restored = False
    if old_cleared:
        # Sisa salinan lintas sistem berkas milik proses ini; pohon lama sudah aman di N-83.
        for name in os.listdir(tree):
            partial = output / name
            try:
                if os.path.lexists(partial):
                    shutil.rmtree(partial) if partial.is_dir() and not partial.is_symlink() else partial.unlink()
            except OSError:
                restored = False
    for name in moved_old:
        try:
            shutil.move(str(slot / name), str(output / name))
        except OSError:
            restored = False
    if slot is not None:
        try:
            slot.rmdir()
        except OSError:
            restored = False
    if created:
        try:
            output.rmdir()
        except OSError:
            pass
    return restored


def set_folder_modes(tree):
    for current, folders, _ in os.walk(tree):
        for folder in folders:
            os.chmod(Path(current) / folder, 0o755)


# Keluaran.

def write_report(root, repository, report):
    """N-49 hanya ditulis pada lokasi yang diabaikan Git, sehingga rinciannya tidak dapat ikut commit."""
    if repository.run('check-ignore', '-q', '--no-index', REPORT).returncode:
        return False
    path = root / REPORT
    try:
        path.parent.mkdir(parents=True, exist_ok=True)
        descriptor, temporary = tempfile.mkstemp(prefix='.laporan.', dir=path.parent)
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(json_bytes(report))
        os.replace(temporary, path)
    except OSError:
        return False
    return True


def summarize(result, details):
    """Stdout hanya jumlah dan hash path (RK-22)."""
    hashes = sorted({path_sha256(row['path']) for row in details if row.get('path')})
    return {**result, 'hits': len(details), 'path_sha256': hashes}


def run_build(args, root):
    repository = Repository(root)
    temporary = None
    result = {'status': 'blocked', 'reason': None, 'source_commit': None, 'allowlist_sha256': None, 'files': 0,
              'bytes': 0, 'expected_missing': None, 'stamped': 0, 'rejected_role_mentions': 0, 'dry_run': args.dry_run}
    details = []
    try:
        output = Path(os.path.abspath(args.output))
        short = check_output(output, root)
        commit = repository.commit(args.source_ref)
        result['source_commit'] = commit
        files, trees = repository.listing(commit)
        inputs = {}
        for name in (ALLOWLIST, STAMP, FRONT_TEMPLATE, HARNESS_TEMPLATE):
            if name not in files:
                raise invalid('input')
            inputs[name] = repository.blob(files[name][1])
        result['allowlist_sha256'] = sha256(inputs[ALLOWLIST])
        config = validate_allowlist(inputs[ALLOWLIST])
        stamp = validate_stamp(inputs[STAMP])
        front = validate_template(inputs[FRONT_TEMPLATE])
        harness = validate_template(inputs[HARNESS_TEMPLATE])
        if config.get('approval', {}).get('status') != 'approved' and not args.dry_run:
            raise Blocked('allowlist_not_approved')

        patterns = load_patterns(root)
        control_patterns(patterns, files, repository)

        admitted = select_files(config, files, trees, repository)
        check_required(config, files, admitted)
        if sha256(repository.blob(files['HARNESS.md'][1])) != config['harness_template_source_sha256']:
            raise Blocked('harness_template_stale')
        try:
            source_config = json.loads(repository.blob(files['library.json'][1]).decode('utf-8'))
        except ValueError:
            raise Blocked('required_file_missing', [{'path': 'library.json'}]) from None

        temporary = Path(tempfile.mkdtemp(prefix='edisi-'))
        tree = temporary / 'pohon'
        tree.mkdir()
        contents, sources, stamped, expected = assemble(tree, config, stamp, front, harness, source_config, files,
                                                        admitted, repository, commit, result['allowlist_sha256'])
        result.update(expected_missing=expected, stamped=stamped)

        derived = collect_derived_names(files, repository)
        rejected = {Path(posixpath.basename(path)).stem for path in files
                    if path.startswith(ROLES) and path.endswith('.md') and '/' not in path[len(ROLES):]
                    and not posixpath.basename(path).startswith('_') and path not in admitted}
        entry_documents = {'README.md', 'HARNESS.md', POLICY, SKILL_CATALOG}
        entry_documents |= {name for name in contents if is_built_collection_file(name)}
        result['rejected_role_mentions'] = scan_edition(contents, sources, config, patterns, derived,
                                                        token_regex(rejected), entry_documents, inputs[ALLOWLIST])
        run_check(tree)

        result.update(files=len(contents), bytes=sum(len(data) for data in contents.values()))
        if not args.dry_run:
            set_folder_modes(tree)
            publish(tree, output, short or 'tanpa-commit')
        result.update(status='pass', reason=None)
    except Blocked as stop:
        result['reason'] = stop.reason
        result.update(stop.extra)
        details = stop.details
    finally:
        if temporary is not None:
            shutil.rmtree(temporary, ignore_errors=True)
    result['report_written'] = write_report(root, repository, {**result, 'command': 'build', 'details': details})
    repository.close()
    return summarize(result, details), 0 if result['status'] == 'pass' else 1


def run_pin(args, root):
    """Memperbarui pin pada pohon kerja dari HEAD. `approval` tidak disentuh, dan selisihnya hanya menuju N-49."""
    repository = Repository(root)
    details = []
    result = {'status': 'blocked', 'reason': None, 'updated': 0, 'unchanged': 0}
    try:
        path = root / ALLOWLIST
        try:
            original = path.read_bytes()
        except OSError:
            raise invalid('input') from None
        config = validate_allowlist(original)
        files, trees = repository.listing(repository.commit('HEAD'))
        targets = {entry['path']: (entry, 'blob' if entry['kind'] == 'file' else 'tree') for entry in config['entries']}
        targets.update({copy['path']: (copy, 'tree') for skill in config['skills'] for copy in skill['copies']})
        unknown = [name for name in args.paths if name not in targets]
        if unknown:
            raise Blocked('allowlist_invalid', [{'path': name} for name in unknown])
        for name in args.paths:
            holder, key = targets[name]
            current = files[name][1] if key == 'blob' and name in files else trees.get(name) if key == 'tree' else None
            if current is None:
                raise Blocked('allowlist_pin_mismatch', [{'path': name, 'added': 0, 'changed': 0, 'removed': None}])
            if holder[key] == current:
                result['unchanged'] += 1
                details.append({'path': name, 'added': 0, 'changed': 0, 'removed': 0})
                continue
            difference = repository.tree_difference(holder[key], current) if key == 'tree' else {'added': 0, 'changed': 1, 'removed': 0}
            details.append({'path': name, **difference})
            holder[key] = current
            result['updated'] += 1
        data = json_bytes(config)
        if data != original:
            descriptor, temporary = tempfile.mkstemp(prefix='.daftar.', dir=path.parent)
            try:
                with os.fdopen(descriptor, 'wb') as stream:
                    stream.write(data)
                os.chmod(temporary, 0o644)
                os.replace(temporary, path)
            except BaseException:
                Path(temporary).unlink(missing_ok=True)
                raise
        result['status'] = 'pass'
    except Blocked as stop:
        result['reason'] = stop.reason
        details = stop.details
    result['report_written'] = write_report(root, repository, {**result, 'command': 'pin', 'details': details})
    repository.close()
    return summarize(result, details), 0 if result['status'] == 'pass' else 1


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest='command', required=True)
    build = sub.add_parser('build', help='Bangun edisi dari blob commit')
    build.add_argument('--output')
    build.add_argument('--source-ref', default='HEAD')
    build.add_argument('--dry-run', action='store_true')
    pin = sub.add_parser('pin', help='Perbarui pin entri N-08 pada pohon kerja')
    pin.add_argument('paths', nargs='+')
    args = parser.parse_args(argv)
    if args.command == 'build' and not args.output:
        print(json.dumps({'status': 'invalid', 'reason': 'output_required', 'recommended_folder_name': OUTPUT_NAME,
                          'note': 'Folder di luar clone memerlukan izin tulis terpisah.'}, ensure_ascii=False))
        return 2
    try:
        summary, code = (run_build if args.command == 'build' else run_pin)(args, ROOT)
    except Exception as error:
        # Pesan kesalahan sistem dapat memuat path, jadi hanya jenisnya yang dicetak.
        print(json.dumps({'status': 'invalid', 'reason': 'internal_error', 'error_type': type(error).__name__}))
        return 2
    print(json.dumps(summary, ensure_ascii=False))
    return code


if __name__ == '__main__':
    sys.exit(main())
