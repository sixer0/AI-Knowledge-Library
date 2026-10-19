#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Verifikasi NAT-S13: blok GATE NATURALISASI utuh & identik di semua SOUL profil aktif.
Deterministik: tiap check mencetak CHECK n: PASS|FAIL + VERDICT akhir. Read-only."""
import hashlib
import sys
from pathlib import Path

P = Path("C:/Users/TRIAL/AppData/Local/hermes/profiles")
BAK = Path("C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-09-02-naturalisasi-output/backup_gate_nat_20260902_120656")
START = "## GATE NATURALISASI"
END = "gerbang bersifat prosedural-terverifikasi, bukan hard-gate transport."

souls = sorted(p for p in P.glob("*/SOUL.md") if p.is_file())
names = [s.parent.name for s in souls]
results = []

def check(n, name, ok, detail=""):
    results.append(ok)
    print(f"CHECK {n}: {'PASS' if ok else 'FAIL'} - {name}" + (f" | {detail}" if detail else ""))

texts = {s.parent.name: s.read_text(encoding="utf-8", errors="replace") for s in souls}

# C1: jumlah target = 55 (basis 53 + drift 2), semua ber-SOUL
check(1, "sensus SOUL.md tingkat atas", len(souls) == 55, f"{len(souls)} berkas")

# C2: blok utuh (marker awal + penutup) pada seluruh target
utuh = [n for n, t in texts.items() if START in t and END in t]
check(2, "blok GATE NATURALISASI utuh", len(utuh) == len(souls), f"{len(utuh)}/{len(souls)}")

# C3: tidak ada duplikasi blok
dup = [n for n, t in texts.items() if t.count(START) != 1]
check(3, "tidak ada blok ganda", not dup, f"pelanggar={dup}")

# C4: isi blok byte-identik lintas profil (sha256 ekstrak blok)
def block_of(t):
    i = t.index(START)
    j = t.index(END, i) + len(END)
    return t[i:j]
hashes = {}
for n, t in texts.items():
    h = hashlib.sha256(block_of(t).encode("utf-8")).hexdigest()
    hashes.setdefault(h, []).append(n)
check(4, "isi blok identik lintas profil", len(hashes) == 1,
      f"{len(hashes)} hash unik; sha256 blok={next(iter(hashes))}")

# C5: prefix pra-edit utuh (backup asal == potongan awal berkas sekarang)
bad_prefix = []
for n in names:
    b = BAK / f"{n}__SOUL.md"
    if not b.is_file():
        bad_prefix.append(n + " (backup hilang)")
        continue
    orig = b.read_bytes()
    cur = Path(P / n / "SOUL.md").read_bytes()
    if not cur.startswith(orig):
        bad_prefix.append(n)
check(5, "prefix byte-identik dengan backup pra-edit", not bad_prefix, f"pelanggar={bad_prefix}")

# C6: bebas karakter terlarang U+2014/U+00B7 di dalam blok yang dipasang
bad_ch = [n for n, t in texts.items() if chr(0x2014) in block_of(t) or chr(0x00B7) in block_of(t)]
check(6, "blok bebas U+2014/U+00B7", not bad_ch, f"pelanggar={bad_ch}")

# C7: lima butir wajib hadir di blok (rujukan isi minimal kartu)
must = ["draft", "naturalisasi", "cek-gerbang", "serahkan",
        "formal-effisien", "Decision Log", "auto-revert",
        "gsp-output-naturalization", "scan_ai_footprint.py",
        "metadata", "D-TA-07", "D-TA-10"]
b0 = block_of(next(iter(texts.values())))
missing = [m for m in must if m not in b0]
check(7, "butir wajib blok lengkap (urutan/register/override/rujukan/metadata)", not missing, f"hilang={missing}")

v = "PASS" if all(results) else "FAIL"
print(f"VERDICT: {v} ({sum(results)}/{len(results)} check)")
sys.exit(0 if v == "PASS" else 1)
