# -*- coding: utf-8 -*-
"""Rollout 03-09-2026: blok MANDAT VERIFIKASI di SOUL 6 akun verifier/reviewer (VERIF-SHORT-B).

Kartu    : t_907b7543 | Kontrak: docs/2026-09-03-verif-short/ (D-06)
Idempoten: marker 'MANDAT VERIFIKASI' sudah ada -> skip. Backup berstempel, EOL-safe.
"""
import sys
from datetime import datetime
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

HOME = Path(r"C:\Users\TRIAL\AppData\Local\hermes\profiles")
TARGETS = ["gsp-verifier", "gsp-test-expert", "gsp-security-review",
           "gsp-senior-code-reviewer", "gsp-document-reviewer", "gsp-pm-verifier"]

MARKER = "## MANDAT VERIFIKASI"
BLOCK = """## MANDAT VERIFIKASI (VERIF-SHORT-B, kebijakan user 03-09-2026)
Kamu adalah jalur pemulihan utama sistem: pekerja hanya boleh healing maks 1 loop, sehingga mutu akhir bertumpu pada verdict-mu. Aturan mengikat:
1. **Verdict contract**: hasil verifikasi WAJIB berupa daftar `CHECK n: PASS|FAIL|NEEDS_REVIEW - nama | angka/bukti` + satu baris `VERDICT: PASS|FAIL|NEEDS_REVIEW` yang KONSISTEN dengan baris CHECK (FAIL di baris CHECK mana pun membatalkan VERDICT: PASS). Bukti dari baca-file/eksekusi ulang saat itu, bukan dari summary pekerja.
2. **Penulis bukan verifikator**: kamu dilarang memverifikasi artefak yang kamu tulis sendiri; bila kartu ternyata meminta itu, kembalikan ke controller (`blocked`, alasan `self_verification_conflict`).
3. **FAIL adalah masukan, bukan musuhan**: FAIL ditulis dengan akar + lokasi + reprouksi agar controller bisa menyusun kartu fix presisi (maks 2 retry per tugas). Jangan menambal artefak orang lain dalam kartu verifier-mu; verdict murni.
4. **PASS tanpa bukti segar dilarang** (Iron Law): setiap klaim lulus menyebut perintah yang dijalankan + outputnya. NEEDS_REVIEW untuk keputusan manusia, bukan tempat membuang ketidakjujuran.
5. **Skala penuh sesuai peran**: tester menjalankan suite penuh/red-green; reviewer menelaah requirement baris-per-baris; security memakai gate-nya. Short check pekerja BUKAN alasan memangkas verifikasi-mu.
"""


def process(p: Path, dry: bool) -> str:
    raw = p.read_bytes()
    text = raw.decode("utf-8", errors="replace")
    if MARKER in text:
        return "SKIP (sudah ada)"
    eol = "\r\n" if "\r\n" in text else "\n"
    block = BLOCK.replace("\n", eol)
    ins = ("\n" if not text.endswith(("\n", "\r")) else "") + block
    if dry:
        return "DRY (+%d b)" % len(ins.encode("utf-8"))
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    bak = p.with_name(p.name + f".bak-mandateverif-{stamp}")
    bak.write_bytes(raw)
    p.write_bytes((text + ins).encode("utf-8"))
    return "PATCHED"


def main():
    dry = "--dry-run" in sys.argv
    ok = skip = fail = 0
    for name in TARGETS:
        p = HOME / name / "SOUL.md"
        if not p.exists():
            print("MISSING %s" % p)
            fail += 1
            continue
        r = process(p, dry)
        tag = r.split(" ")[0]
        if tag == "PATCHED":
            ok += 1
        elif tag == "SKIP":
            skip += 1
        print("%-8s %s" % (tag, name))
    print("TOTAL=%d patched=%d skip=%d fail=%d dry=%s" % (len(TARGETS), ok, skip, fail, dry))
    sys.exit(1 if fail else 0)


if __name__ == "__main__":
    main()
