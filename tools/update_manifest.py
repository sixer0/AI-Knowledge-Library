#!/usr/bin/env python3
"""Satu-satunya penulis MANIFEST.csv repositori penuh; tanpa --write hanya melapor."""
from pathlib import Path
import argparse
import csv
import hashlib
import importlib.util
import io
import json
import os
import sys
import tempfile

# Mengimpor resolver tidak boleh menyisakan __pycache__ pada clone.
sys.dont_write_bytecode = True

HEADER = ['relative_path', 'bytes', 'sha256']
SIDECAR_SUFFIXES = ('-shm', '-wal', '-journal')
SQLITE_HEADER = b'SQLite format 3\x00'


def load_library(root):
    specification = importlib.util.spec_from_file_location('library', Path(__file__).with_name('library.py'))
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module.Library(root)


def render(rows):
    """UTF-8 tanpa BOM, `\\n`, urut byte UTF-8, kutip minimal: identik byte dengan MANIFEST.csv."""
    stream = io.StringIO(newline='')
    writer = csv.writer(stream, lineterminator='\n')
    writer.writerow(HEADER)
    for name in sorted(rows, key=lambda value: value.encode('utf-8')):
        writer.writerow([name, *rows[name]])
    return stream.getvalue().encode('utf-8')


def measure(library):
    rows = {}
    for name in library.manifest_expected():
        file = library.root / name
        if file.is_file():
            data = file.read_bytes()
            rows[name] = (str(len(data)), hashlib.sha256(data).hexdigest())
    return rows


def manifest_bytes(root):
    """Isi manifest yang seharusnya untuk pohon `root`, memakai resolver di samping berkas ini."""
    return render(measure(load_library(root)))


def read_rows(data):
    reader = csv.DictReader(io.StringIO(data.decode('utf-8'), newline=''))
    return {row['relative_path']: (row['bytes'], row['sha256']) for row in reader}


def sqlite_sidecars(library, names):
    """Berkas sisi hanya bila pasangannya benar basis data SQLite; basis data itu tidak dibuka lewat SQLite."""
    found = []
    for name in sorted(names):
        for suffix in SIDECAR_SUFFIXES:
            pair = library.root / name[:-len(suffix)]
            if name.endswith(suffix) and pair.is_file():
                with pair.open('rb') as stream:
                    if stream.read(len(SQLITE_HEADER)) == SQLITE_HEADER:
                        found.append({'reason': 'sqlite_sidecar', 'file': name})
    return found


def inspect(library):
    path = library.inside(library.root / library.config['manifest'])
    current = path.read_bytes()
    old, new = read_rows(current), measure(library)
    rejected = [f for f in library.scope_failures() if f['reason'] in {'manifest_scope_empty', 'manifest_root_missing'}]
    if render(old) != current:
        # Tanpa ini, menulis ulang mengubah baris yang tidak tercantum pada daftar.
        rejected.append({'reason': 'manifest_not_canonical', 'file': library.config['manifest']})
    rejected += sqlite_sidecars(library, new)
    report = {'added': sorted(new.keys() - old.keys()), 'removed': sorted(old.keys() - new.keys()),
              'changed': sorted(name for name in new.keys() & old.keys() if new[name] != old[name]),
              'rejected': rejected, 'entries': len(new), 'written': False}
    return report, path, current, render(new)


def approved_paths(path):
    with Path(path).open(encoding='utf-8', newline='') as stream:
        return {row['relative_path'] for row in csv.DictReader(stream)}


def replace_file(path, data):
    """Berkas sementara di folder yang sama, lalu os.replace: tidak ada manifest setengah jadi."""
    descriptor, temporary = tempfile.mkstemp(prefix='.' + path.name + '.', dir=path.parent)
    try:
        with os.fdopen(descriptor, 'wb') as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        os.chmod(temporary, path.stat().st_mode & 0o777)
        os.replace(temporary, path)
    except BaseException:
        Path(temporary).unlink(missing_ok=True)
        raise


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Tulis bila semua selisih tercantum pada --approved')
    parser.add_argument('--approved', help='CSV dengan kolom relative_path')
    args = parser.parse_args(argv)
    if args.write and not args.approved:
        parser.error('--write memerlukan --approved')
    try:
        library = load_library(None)
        report, path, current, data = inspect(library)
        if args.write:
            allowed = approved_paths(args.approved)
            difference = report['added'] + report['changed'] + report['removed']
            report['unapproved'] = sorted(set(difference) - allowed)
            if report['rejected'] or report['unapproved']:
                print(json.dumps(report, ensure_ascii=False, indent=2))
                return 1
            if data != current:
                replace_file(path, data)
                report['written'] = True
    except (OSError, ValueError, KeyError, csv.Error) as error:
        print(json.dumps({'status': 'invalid', 'reason': str(error)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 1 if report['rejected'] else 0


if __name__ == '__main__':
    sys.exit(main())
