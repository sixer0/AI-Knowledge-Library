# -*- coding: utf-8 -*-
"""Rollout 03-09-2026: persempit cakupan blok GATE NATURALISASI di SOUL.md fleet.

Kartu    : t_ed3489c6 (GATE-NAT-SCOPE)
Kontrak  : docs/2026-09-03-gate-nat-scope/contract.md
Kebijakan: user 03-09 - gerbang HANYA untuk keluaran yang diserahkan ke user;
           artefak markdown antar-agen & jejak orkestrasi dikecualikan.

Idempoten: file yang sudah memuat marker 'cakupan dipersempit 03-09-2026' dilewati.
Aman EOL: blok ditulis dengan EOL yang sama dengan target. Backup berstempel.
Marker watchdog (BLOCK_START '## GATE NATURALISASI' dan baris penutup D-TA-10)
dipertahankan agar check_gate_naturalisasi.py C-1 tetap hijau.
"""
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HOME = Path(r"C:\Users\TRIAL\AppData\Local\hermes")
TARGETS = sorted(HOME.glob("profiles/*/SOUL.md")) + [HOME / "SOUL.md"]

NEW_BLOCK = """## GATE NATURALISASI (WAJIB, kebijakan 02-09-2026; cakupan dipersempit 03-09-2026)
Gerbang naturalisasi HANYA berlaku pada keluaran yang benar-benar diserahkan ke user. Artefak internal yang dikonsumsi antar agen AI (jejak orkestrasi) dikecualikan agar proses orkestrasi tidak melambat:
1. **Cakupan** (user 03-09): TUNDUK gerbang = jawaban/chat ke user, dokumen/deck/etalase final, notifikasi untuk user. DIKECUALIKAN (tanpa cek-gerbang) = berkas antar-agen dan jejak orkestrasi: contract doc `docs/`, kartu/komentar kanban, `identification/*` (RT/SPEC/blueprint), checkpoint, laporan fase internal, log, `metadata` mesin. Naturalisasi tetap konten-kekal: angka, fakta, satuan, sitasi, dan struktur data tidak boleh berubah. A1/A2 (em dash, middle dot) tetap nol pada SEMUA keluaran yang dibaca user.
2. **Urutan wajib** (hanya kanal TUNDUK): draft (konten faktual selesai) -> naturalisasi -> cek-gerbang -> serahkan. FAIL dikembalikan ke langkah naturalisasi, bukan diloloskan.
3. **Register default formal per kanal** (D-TA-05): chat kerja = formal-effisien (tanpa emoji, tanpa basa-basi servil); dokumen/deck/etalase = formal institusional; notifikasi = formal-netral. Ringkasan handoff antar-agen dan komentar kanban dikecualikan sejak 03-09 (sebelumnya tunduk gerbang via D-TA-07); `metadata` mesin tetap dikecualikan.
4. **Override hanya atas permintaan tersurat user**, scoped ke kanal dan misi yang disebut, umur sampai dicabut atau misi selesai lalu auto-revert ke formal, dan wajib dicatat di Decision Log kontrak misi. Override tidak pernah mengampuni A1/A2 (em dash dan middle dot tetap nol di semua register).
5. **Rujukan**: skill `gsp-output-naturalization` (registry fleet `$LOCALAPPDATA/hermes/skills/gsp/gsp-output-naturalization/`) + scanner deterministik `scripts/scan_ai_footprint.py` di dalamnya. Jejak cek = laporan scanner atau centang-manual berformat; tanpa jejak, tahap dianggap tidak dijalankan. Berlaku pada kanal TUNDUK.
6. **Batas klaim** (D-TA-10): dilarang klaim `fleet-wide 0`; gerbang bersifat prosedural-terverifikasi, bukan hard-gate transport.
"""

OLD_START = "## GATE NATURALISASI"
OLD_END = "gerbang bersifat prosedural-terverifikasi, bukan hard-gate transport."
MARKER = "cakupan dipersempit 03-09-2026"


def process(p: Path, dry: bool) -> str:
    raw = p.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    if MARKER in text:
        return "SKIP (sudah baru)"
    i = text.find(OLD_START)
    if i < 0:
        return "SKIP (tidak ada blok)"
    j = text.find(OLD_END, i)
    if j < 0:
        return "FAIL (marker akhir tak ditemukan)"
    end = j + len(OLD_END)
    if end < len(text) and text[end] == "\n":
        end += 1
    eol = "\r\n" if "\r\n" in text[i:end] else "\n"
    block = NEW_BLOCK.replace("\n", eol) if eol == "\r\n" else NEW_BLOCK
    new_text = text[:i] + block + text[end:]
    if dry:
        return "DRY (%d b -> %d b)" % (len(raw), len(new_text.encode("utf-8")))
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = p.with_name(p.name + f".bak-gatescope-{stamp}")
    bak.write_bytes(raw)
    p.write_bytes(new_text.encode("utf-8"))
    return "PATCHED (backup %s)" % bak.name


def main():
    dry = "--dry-run" in sys.argv
    patched = skipped = failed = 0
    for p in TARGETS:
        if not p.exists():
            continue
        r = process(p, dry)
        tag = r.split(" ")[0]
        if tag == "PATCHED":
            patched += 1
        elif tag == "FAIL":
            failed += 1
        else:
            skipped += 1
        print("%-9s %s" % (tag, str(p).replace(str(HOME), "~")))
    print("TOTAL target=%d patched=%d skip=%d fail=%d dry=%s" % (patched + skipped + failed, patched, skipped, failed, dry))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
