#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifier deterministik NAT-S15 (kartu t_0c860641): butir naturalisasi di blok
GATE ENFORCEMENT profil roster controller. Read-only - tidak menulis apa pun
kecuali laporan di folder kontrak.

Keluaran: baris `CHECK n: PASS|FAIL|NEEDS_REVIEW - nama` + satu baris `VERDICT:`.
"""
import hashlib
import json
import re
import sys
from pathlib import Path

LOCALAPPDATA = Path("C:/Users/TRIAL/AppData/Local")
PROFILES = LOCALAPPDATA / "hermes" / "profiles"
WS = Path("C:/Users/TRIAL/workspace/gsp-hermes/workspace")
DOCSDIR = WS / "docs" / "2026-09-02-naturalisasi-output"
ROSTER_F = WS / "docs" / "2026-08-31-enforcement-fleet" / "controller-roster.json"
REPORT = DOCSDIR / "verify-gate-nat-controller-s15.md"

CARD_NAMES = [
    "agentriset", "firmanhidayat", "gsp-budi", "gsp-crawler-orchestrator",
    "gsp-creative", "gsp-firman-custom", "gsp-pm-planner", "gsp-skill-manager",
    "gsp-system-manager", "gspuser01", "novriandy", "user01",
]
GE_HEADING = "## GATE ENFORCEMENT"
GN_START = "## GATE NATURALISASI"
GN_END = "gerbang bersifat prosedural-terverifikasi, bukan hard-gate transport."
MARKER = "**Gerbang naturalisasi keluaran"
RUN1_BACKUP = DOCSDIR / "backup_gate_nat_ctrl_20260902_121349"

results = []


def emit(n, status, name, msg=""):
    results.append((n, status, name, msg))
    print(f"CHECK {n}: {status} - {name}" + (f" | {msg}" if msg else ""))


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def main():
    roster = json.loads(ROSTER_F.read_text(encoding="utf-8"))["controllers"]
    real = [n for n in roster if (PROFILES / n / "SOUL.md").is_file()]
    texts = {n: (PROFILES / n / "SOUL.md").read_bytes().decode("utf-8") for n in real}

    # CHECK 1: `default` roster TIDAK ada di disk dan tidak dihitung sukses
    default_absent = not (PROFILES / "default").is_dir()
    emit(1, "PASS" if default_absent else "FAIL", "profil `default` tidak ada di disk",
         "profiles/default tidak ditemukan; tidak masuk hitungan sukses"
         if default_absent else "profil default ternyata ADA - koreksi needed")

    # CHECK 2: 12 nama kartu nyata dan ber-SOUL.md
    missing = [n for n in CARD_NAMES if n not in real]
    emit(2, "PASS" if not missing else "FAIL", "12 nama kartu ada di disk",
         f"nyata={len(real)} dari roster {len(roster)}; hilang={missing}")

    # CHECK 3: marker butir ada tepat satu kali di 12 nama kartu
    bad = {n: texts[n].count(MARKER) for n in CARD_NAMES if n in texts and texts[n].count(MARKER) != 1}
    emit(3, "PASS" if not bad else "FAIL", "grep marker 'Gerbang naturalisasi keluaran' == 1 per profil kartu",
         f"pelanggar={bad}" if bad else f"{len([n for n in CARD_NAMES if n in texts])}/12 tercentang")

    # CHECK 4: butir berada DI DALAM blok GATE ENFORCEMENT (sebelum heading berikutnya)
    outside = []
    for n in CARD_NAMES:
        t = texts.get(n)
        if t is None:
            outside.append((n, "tanpa SOUL"))
            continue
        i_ge = t.find(GE_HEADING)
        nxt = t.find("\n## ", i_ge + len(GE_HEADING)) if i_ge >= 0 else -1
        i_end = nxt + 1 if nxt >= 0 else len(t)
        i_m = t.find(MARKER)
        if not (0 <= i_ge < i_m < i_end):
            outside.append((n, f"GE@{i_ge} marker@{i_m} akhir_blok@{i_end}"))
    emit(4, "PASS" if not outside else "FAIL", "butir di dalam blok GATE ENFORCEMENT",
         f"luar_blok={outside}" if outside else "semua marker antara heading GE dan heading berikutnya")

    # CHECK 5: penomoran lanjut tanpa duplikat (nomor baru = max sebelumnya + 1)
    badnum = []
    for n in CARD_NAMES:
        t = texts.get(n)
        if t is None:
            continue
        i_ge = t.find(GE_HEADING)
        nxt = t.find("\n## ", i_ge + len(GE_HEADING))
        ge_text = t[i_ge:(nxt + 1 if nxt >= 0 else len(t))]
        nums = [int(m) for m in re.findall(r"(?m)^(\d+)\.", ge_text)]
        if len(nums) != len(set(nums)) or nums != list(range(1, len(nums) + 1)):
            badnum.append((n, nums))
    emit(5, "PASS" if not badnum else "FAIL", "penomoran butir GE berurutan tanpa duplikat",
         f"pelanggar={badnum}" if badnum else "nomor 1..N utuh di semua target")

    # CHECK 6: konten di luar sisipan byte-identik dengan backup run-1 (prefix kekal)
    drift = []
    if not RUN1_BACKUP.is_dir():
        emit(6, "FAIL", "backup run-1 ada", f"tidak ditemukan: {RUN1_BACKUP}")
    else:
        for n in CARD_NAMES:
            bak = RUN1_BACKUP / f"{n}__SOUL.md"
            t = texts.get(n)
            if t is None or not bak.is_file():
                drift.append((n, "berkas hilang"))
                continue
            # buang persis satu baris sisipan berikut EOL-nya -> harus sama byte dgn backup
            pat = re.compile(r"(?m)^\d+\.[^\n]*\*\*Gerbang naturalisasi keluaran[^\n]*\r?\n")
            stripped = pat.sub("", t, count=1)
            if sha256_bytes(stripped.encode("utf-8")) != sha256_bytes(bak.read_bytes()):
                drift.append((n, "sha256 beda setelah buang sisipan"))
        emit(6, "PASS" if not drift else "FAIL", "sisa berkas byte-identik dengan backup run-1",
             f"pelanggar={drift}" if drift else "buang-baris-sisipan -> sha256 == backup, 12/12")

    # CHECK 7: blok GATE NATURALISASI (NAT-S13) tetap utuh dan tunggal di target
    bad_gn = []
    for n in CARD_NAMES:
        t = texts.get(n)
        if t is None or GN_START not in t or GN_END not in t or t.count(GN_START) != 1:
            bad_gn.append(n)
    emit(7, "PASS" if not bad_gn else "FAIL", "blok GATE NATURALISASI utuh pasca-edit",
         f"pelanggar={bad_gn}" if bad_gn else "12/12 masih memuat blok NAT-S13 tunggal")

    # CHECK 8: bebas karakter terlarang pada baris sisipan
    badch = []
    for n in CARD_NAMES:
        t = texts.get(n)
        if t is None:
            continue
        for line in t.splitlines():
            if MARKER in line and (chr(0x2014) in line or chr(0x00B7) in line):
                badch.append(n)
                break
    emit(8, "PASS" if not badch else "FAIL", "baris sisipan bebas U+2014/U+00B7",
         f"pelanggar={badch}" if badch else "0 match")

    fails = [r for r in results if r[1] == "FAIL"]
    reviews = [r for r in results if r[1] == "NEEDS_REVIEW"]
    verdict = "PASS" if not fails and not reviews else ("NEEDS_REVIEW" if not fails else "FAIL")
    print(f"VERDICT: {verdict} ({len(results) - len(fails) - len(reviews)}/{len(results)} check)")

    REPORT.write_text("\n".join([
        "# Verifikasi NAT-S15 - butir naturalisasi di blok GE roster controller",
        "",
        f"Roster: {len(roster)} nama; nyata di disk: {len(real)}; `default` tidak ada di disk "
        "(dicatat eksplisit, bukan klaim sukses).",
        "Drift vs kartu: gsp-master, gsp-master01 (masuk roster setelah kartu ditulis, ikut dipasang, dilaporkan).",
        "",
        "```",
        *[f"CHECK {n}: {s} - {name}{' | ' + msg if msg else ''}" for n, s, name, msg in results],
        f"VERDICT: {verdict}",
        "```",
        "",
    ]), encoding="utf-8")
    print(f"Laporan: {REPORT}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
