#!/usr/bin/env python3
"""
migrate_legacy.py — helper orkestrasi migrasi legacy workspace agentic → IL GSP.

Tahap:
  1. inventaris: walk pohon file download, tulis manifest.json (relpath, size, ext, folder)
  2. klasifikasi: tandai tiap file 'penting' vs 'operasional' (heuristik nama/path/ukuran)
  3. ringkasan per folder untuk panduan kurasi librarian
Dipakai oleh Brahma (orkestrator) sebagai dasar rekonsiliasi 'tidak ada info tertinggal'.
"""
import argparse, json, sys
from collections import Counter
from pathlib import Path

# ekstensi yang dianggap 'konten pengetahuan' (perlu kurasi)
KNOWLEDGE_EXT = {".md", ".markdown", ".txt", ".pdf", ".docx", ".doc", ".csv",
                 ".json", ".html", ".htm", ".pptx", ".xlsx", ".yaml", ".yml",
                 ".rst", ".tex", ".epub", ".mobi", ".odt"}

# pola nama yang menandakan artefak proses/operasional (bukan pengetahuan akhir)
PROCESS_PATTERNS = [
    "draft", "tmp", "temp", "wip", "scratch", "backup", "old", "copy",
    "checkpoint", "progres", "progress", "log", "cache", ".git",
]

def classify(rel: str) -> str:
    """Kembalikan 'penting' | 'operasional' | 'sumber' berdasarkan path."""
    low = rel.lower()
    name = Path(low).name
    ext = Path(low).suffix
    if any(p in low for p in PROCESS_PATTERNS):
        return "operasional"
    if ext in KNOWLEDGE_EXT and len(name) > 3:
        return "penting"
    if ext in KNOWLEDGE_EXT:
        return "penting"
    return "sumber"  # media/binari/arsip — disimpan utuh, bukan objek pengetahuan

def inventaris(root: Path, out_json: Path):
    files = []
    for p in sorted(root.rglob("*")):
        if not p.is_file():
            continue
        rel = p.relative_to(root).as_posix()
        files.append({
            "rel": rel,
            "size": p.stat().st_size,
            "ext": p.suffix.lower() or "(none)",
            "folder": rel.rsplit("/", 1)[0] if "/" in rel else "(root)",
            "kelas": classify(rel),
        })
    out_json.write_text(json.dumps(files, indent=2), "utf-8")
    return files

def report(files):
    total = len(files)
    total_size = sum(f["size"] for f in files)
    by_class = Counter(f["kelas"] for f in files)
    by_ext = Counter(f["ext"] for f in files)
    by_folder = Counter(f["folder"] for f in files)
    print(f"TOTAL FILE: {total}")
    print(f"TOTAL SIZE: {total_size/1e6:.2f} MB")
    print(f"KELAS: {dict(by_class)}")
    print(f"EXT (top10): {by_ext.most_common(10)}")
    print("\nPER FOLDER:")
    for folder, n in by_folder.most_common():
        sz = sum(f["size"] for f in files if f["folder"] == folder)
        print(f"  {folder}: {n} file, {sz/1e6:.2f} MB")
    penting = [f for f in files if f["kelas"] == "penting"]
    print(f"\nFILE PENTING ({len(penting)}):")
    for f in penting:
        print(f"  [{f['folder']}] {f['rel']} ({f['size']}B)")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="root pohon file yang di-download")
    ap.add_argument("--out", default="manifest.json")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args()
    root = Path(a.root)
    if not root.exists():
        print(f"error: root tidak ada: {root}", file=sys.stderr)
        return 2
    files = inventaris(root, Path(a.out))
    print(f"manifest ditulis: {Path(a.out).resolve()} ({len(files)} file)")
    if a.report:
        report(files)
    return 0

if __name__ == "__main__":
    sys.exit(main())
