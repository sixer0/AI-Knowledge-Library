#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Rollout 02-09-2026 (NAT-S15): kewajiban naturalisasi di blok GATE ENFORCEMENT
profil roster controller.

Kartu    : t_0c860641 (NAT-S15) | Induk: t_7f2125a9 (NAT-S13), t_bdfde921 (NAT-SM)
Blueprint: docs/2026-09-02-naturalisasi-output/identification/02_structured.md langkah 15
Kontrak  : docs/2026-09-02-naturalisasi-output/contract.md (D-04, D-TA-02, D-TA-10)
Pola     : rollout_gate_naturalisasi_20260902.py (idempoten, byte-safe EOL, backup berstempel)

Keputusan mengikat:
  D-04     kebijakan naturalisasi berlaku untuk SEMUA keluaran ke user termasuk
           jawaban orkestrator sendiri - butir baru menyebut ini eksplisit.
  D-TA-02  basis = keadaan disk saat eksekusi; nama roster yang tidak ada di disk
           TIDAK diklaim sukses (khususnya `default`, TA-K2); profil nyata yang
           muncul di roster setelah kartu ditulis (drift) ikut dipasang dan
           dilaporkan satu baris.
  D-TA-10  tanpa klaim fleet-wide abstrak; klaim mengikuti bukti grep/sha256 run ini.

Perilaku:
  * Target = controller roster JSON yang punya profiles/<nama>/SOUL.md di disk,
    MINUS `default`. Prasyarat tiap target: blok GATE ENFORCEMENT ada dan blok
    GATE NATURALISASI hasil NAT-S13 utuh; target tanpa prasyarat -> GAGAL (tidak
    ditambal).
  * Butir baru (nomor = butir terakhir blok GE + 1) disisipkan sebagai baris
    terakhir blok GATE ENFORCEMENT, tepat sebelum heading berikutnya. Konten
    lain byte-kekal: verifikasi pasca-tulis membuang sisipan lalu bandingkan
    sha256 dengan backup pra-edit (harus identik).
  * Idempoten: marker '**Gerbang naturalisasi keluaran' sudah ada -> skip.
  * Backup pra-edit SEMUA target diverifikasi sha256 asal==backup + ukuran > 0
    SEBELUM edit pertama; satu gagal -> abort tanpa menyentuh apa pun.
    Backup DI LUAR kanban/workspaces/** (docs kontrak, folder bertimestamp).
  * --check : mode baca-saja, tidak menulis apa pun.

Bebas karakter terlarang: skrip ini tidak memuat U+2014 maupun U+00B7.
"""
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import time
from pathlib import Path

RUN_STAMP = time.strftime("%Y%m%d_%H%M%S")
LOCALAPPDATA = Path(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"))
HERMES_HOME = LOCALAPPDATA / "hermes"
PROFILES = HERMES_HOME / "profiles"
WS = Path("C:/Users/TRIAL/workspace/gsp-hermes/workspace")
DOCSDIR = WS / "docs" / "2026-09-02-naturalisasi-output"
BACKUPS = DOCSDIR / f"backup_gate_nat_ctrl_{RUN_STAMP}"

ROSTER_F = WS / "docs" / "2026-08-31-enforcement-fleet" / "controller-roster.json"
CARD_NAMES = [  # 12 nama nyata yang WAJIB terpasang menurut kartu NAT-S15
    "agentriset", "firmanhidayat", "gsp-budi", "gsp-crawler-orchestrator",
    "gsp-creative", "gsp-firman-custom", "gsp-pm-planner", "gsp-skill-manager",
    "gsp-system-manager", "gspuser01", "novriandy", "user01",
]
ABSENT_ALLOWED = {"default"}  # roster memuat nama ini; tidak ada di disk (TA-K2)

GE_HEADING = "## GATE ENFORCEMENT"
GN_START = "## GATE NATURALISASI"
GN_END = "gerbang bersifat prosedural-terverifikasi, bukan hard-gate transport."
MARKER = "**Gerbang naturalisasi keluaran"

ITEM_TEMPLATE = (
    "{n}. **Gerbang naturalisasi keluaran (kebijakan 02-09-2026)**: setiap keluaran "
    "yang dibaca manusia dari profil controller ini wajib lolos blok GATE NATURALISASI "
    "di bawah lebih dulu, termasuk jawaban orkestrator ke user (D-04); urutan wajib "
    "draft -> naturalisasi -> cek-gerbang -> serahkan dengan angka/fakta/sitasi tetap "
    "konten-kekal; rujukan skill `gsp-output-naturalization` + scanner deterministik "
    "`scripts/scan_ai_footprint.py`; jejak cek wajib dilaporkan bersama artefak."
)


def eol_for(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"


def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def sha256_file(p: Path) -> str:
    return sha256_bytes(p.read_bytes())


def ge_block_span(t: str):
    """(start, end) blok GATE ENFORCEMENT: dari heading sampai heading `## ` berikut."""
    s = t.find(GE_HEADING)
    if s < 0:
        return None
    nxt = t.find("\n## ", s + len(GE_HEADING))
    e = nxt + 1 if nxt >= 0 else len(t)
    return s, e


def ensure_item(soul: Path):
    """Sisipkan butir naturalisasi di akhir blok GE. Return dict hasil."""
    raw = soul.read_bytes()
    t = raw.decode("utf-8")
    if MARKER in t:
        return {"name": soul.parent.name, "status": "skip"}
    span = ge_block_span(t)
    if span is None:
        raise RuntimeError(f"{soul}: blok GATE ENFORCEMENT tidak ada - prasyarat belum terpenuhi")
    if not (GN_START in t and GN_END in t):
        raise RuntimeError(f"{soul}: blok GATE NATURALISASI (hasil NAT-S13) tidak utuh - prasyarat belum terpenuhi")
    gs, ge = span
    ge_text = t[gs:ge]
    nums = [int(m) for m in re.findall(r"(?m)^(\d+)\.", ge_text)]
    n = (max(nums) + 1) if nums else 1
    item = ITEM_TEMPLATE.format(n=n)
    e = eol_for(t)
    insert_pos = gs + len(ge_text.rstrip())  # akhir baris konten terakhir blok GE
    new_t = t[:insert_pos] + e + item + t[insert_pos:]
    soul.write_bytes(new_t.encode("utf-8"))
    return {"name": soul.parent.name, "status": "installed", "item": e + item}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true",
                    help="baca-saja: status target, tanpa menulis apa pun")
    args = ap.parse_args()

    # Self-check teks sisipan: bebas karakter terlarang
    for ch, name in ((chr(0x2014), "U+2014"), (chr(0x00B7), "U+00B7")):
        if ch in ITEM_TEMPLATE:
            print(f"ABORT: teks sisipan memuat karakter terlarang {name}")
            return 2

    if not ROSTER_F.is_file():
        print(f"ABORT: roster tidak ada: {ROSTER_F}")
        return 2
    roster = json.loads(ROSTER_F.read_text(encoding="utf-8"))["controllers"]

    targets, absent = [], []
    for name in roster:
        soul = PROFILES / name / "SOUL.md"
        if soul.is_file():
            targets.append((name, soul))
        else:
            absent.append(name)
    drift = sorted({n for n, _ in targets} - set(CARD_NAMES))
    missing_card = sorted(set(CARD_NAMES) - {n for n, _ in targets})
    print(f"Roster: {len(roster)} nama | target nyata di disk: {len(targets)} | "
          f"tidak ada di disk: {absent} | drift vs kartu: {drift} | "
          f"nama kartu hilang dari disk: {missing_card}")
    unexpected_absent = sorted(set(absent) - ABSENT_ALLOWED)
    if unexpected_absent or missing_card:
        print(f"ABORT: nama wajib tidak ada di disk {missing_card} atau nama tak terduga "
              f"hilang {unexpected_absent} - periksa sebelum tulis.")

    if args.check:
        ok = 0
        for name, soul in targets:
            t = read(soul)
            st = "PASANG" if MARKER in t else "BELUM"
            print(f"  {name:26} {st}")
            ok += MARKER in t
        print(f"[check] butir naturalisasi terpasang: {ok}/{len(targets)}")
        return 0 if ok == len(targets) else 1

    # ---- Backup pra-edit terverifikasi SEBELUM edit pertama ----
    BACKUPS.mkdir(parents=True, exist_ok=False)
    manifest = []
    for name, soul in targets:
        size = soul.stat().st_size
        if size <= 0:
            print(f"ABORT: {soul} berukuran 0 - tidak lanjut.")
            return 2
        dst = BACKUPS / f"{name}__SOUL.md"
        shutil.copy2(soul, dst)
        h_src, h_dst = sha256_file(soul), sha256_file(dst)
        if h_src != h_dst or dst.stat().st_size <= 0:
            print(f"ABORT: verifikasi backup gagal untuk {name} "
                  f"(asal={h_src[:16]} backup={h_dst[:16]}) - tidak ada edit dilakukan.")
            return 2
        manifest.append({"profile": name, "path": str(soul), "bytes": size, "sha256": h_src})
    (BACKUPS / "_manifest.json").write_text(
        "\n".join(json.dumps(m) for m in manifest), encoding="utf-8")
    print(f"Backup pra-edit: {len(manifest)} berkas -> {BACKUPS} "
          f"(sha256 asal==backup terverifikasi, semua > 0 byte)")

    # ---- Sisip butir ----
    installed, skipped, failed = [], [], []
    for name, soul in targets:
        try:
            res = ensure_item(soul)
        except RuntimeError as ex:
            failed.append((name, str(ex)))
            continue
        if res["status"] == "installed":
            installed.append(res)
        else:
            skipped.append(name)

    print(f"Hasil: {len(installed)} dipasang, {len(skipped)} sudah punya (skip), "
          f"{len(failed)} gagal")
    for name, err in failed:
        print(f"  GAGAL {name}: {err}")

    # ---- Verifikasi pasca-tulis: marker tunggal + konten lain byte-kekal ----
    ok = 0
    for res in installed:
        name = res["name"]
        soul = PROFILES / name / "SOUL.md"
        new_b = soul.read_bytes()
        t = new_b.decode("utf-8")
        stripped = t.replace(res["item"], "", 1)
        bak = (BACKUPS / f"{name}__SOUL.md").read_bytes()
        if t.count(MARKER) == 1 and sha256_bytes(stripped.encode("utf-8")) == sha256_bytes(bak):
            ok += 1
        else:
            print(f"  RUSAK {name}: marker ganda atau konten di luar sisipan berubah")
    print(f"Verifikasi pasca-tulis: {ok}/{len(installed)} sisipan terverifikasi "
          f"(marker tunggal, sisa berkas byte-identik dengan backup)")
    print(f"Bukti sha256 backup: {BACKUPS}/_manifest.json")
    return 0 if (ok == len(installed) and not failed) else 1


if __name__ == "__main__":
    sys.exit(main())
