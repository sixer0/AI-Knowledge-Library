#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Amend RULE AKURASI DATA MUTLAK: tambah butir 10 (CER-001 + satu sumber aturan bukti).
import glob, io, os

OLD = "Rujukan penuh: shared ws docs/2026-09-04-data-accuracy-standard/STANDAR-PROSEDUR-AKURASI-DATA-SPK-002.md (SPK-002-GSP-IX-2026) + skill gsp-orchestration-execution references/data-accuracy-standard.md."
NEW = ("10. **Entitas China / pameran di China wajib CER-001** (amandemen 04-09): akuisisi identifier berjenjang "
       "R0 situs resmi dari API penyelenggara (otoritas identitas, token-match tidak diperlukan) > R1 registri CN "
       "(jembatan nama saja, bukan tautan terbit) > R2 pencarian MANDARIN '<nama_cn> 官网' > R3 bukti ICP footer > "
       "R4 CDX .cn + Wikipedia-ZH. DILARANG: nama kota/provinsi jadi bukti kepemilikan; domain direktori/wisata/"
       "portal-pemerintah/berita jadi tautan terbit; pencarian EN-global sebagai sumber identifier entitas CN. "
       "SATU modul aturan bukti utk semua lapis (gate/autofix/tangga/recheck) - matcher ganda = buta-titik terwarisi.\n"
       + OLD)

targets = [r"C:\Users\TRIAL\AppData\Local\hermes\SOUL.md"] + glob.glob(r"C:\Users\TRIAL\AppData\Local\hermes\profiles\*\SOUL.md")
added = skipped = failed = 0
for p in targets:
    try:
        t = io.open(p, encoding="utf-8").read()
        if "CER-001" in t:
            skipped += 1; continue
        if "RULE AKURASI DATA MUTLAK" not in t or OLD not in t:
            failed += 1; print("SKIP-TANPA-PATTERN:", p); continue
        io.open(p, "w", encoding="utf-8").write(t.replace(OLD, NEW, 1))
        added += 1
    except Exception as e:
        failed += 1; print("ERR:", p, str(e)[:60])
print(f"targets={len(targets)} added={added} skipped={skipped} failed={failed}")
