#!/usr/bin/env python3
"""Kurasi vault oleh gsp-librarian: tandai objek sensitif -> menunggu_persetujuan
+ catatan_keputusan (alasan + rekonsiliasi angka). TIDAK mengubah isi/klaim body.
Hanya frontmatter status & catatan_keputusan (jejak keputusan librarian)."""
import re
from pathlib import Path

VAULT = Path(r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/vault")

# id -> catatan_keputusan (spesifik; umum ditambah otomatis per perkara)
SPECIFIC = {
    "adint-universum-vendor": "Rekonsiliasi 772 vs 1.417 vs 859: 772=vendor unik dianalisis (12h_master_document Bab 1; saturasi >95% vs universe 850-950), 1.417=total_vendors LIBRARY_INDEX, 859=rows 01_master_vendor_list.xlsx (enrichment). Tiga angka beda konteks, sah di sumbernya; JANGAN dicampur.",
    "adint-rekomendasi-strategis": "Rekonsiliasi biaya: USD9,8-37,2jt terverifikasi di ch8 8.1; USD14,2-52,8jt (most likely 18-28jt) terverifikasi di ADINT_Executive_Briefing 2.5. Dua angka beda sumber, keduanya sah; tidak diklaim kanonik tanpa keputusan manajemen.",
    "deliverable-final": "Inkonsistensi 161/62 (report.md v1.0) vs 1.360/337 (china_defence_expo_report_v2.md v2.1 rebuild) terverifikasi di kedua sumber; v2.1 lebih representatif namun perlu verifikasi ulang terhadap 12 file korpus regional sebelum diklaim kanonik.",
    "arsenal-dosir-keputusan": "Dua nilai RAB terverifikasi: Rp 24.945.404.550 (proposal GSP/IDSBT-PRP/2026-01 + design system master + RAB xlsx v2) vs Rp 24.750.028.288 (JSON 033/GSP/KT/VIII/2026 Rev B, konsisten internal). Dua iterasi RAB; angka final MENUNGGU verifikasi manusia/owner dokumen.",
    "arsenal-tahap-4-proyek": "Nilai RAB JSON Rev B (Rp 24.750.028.288) berbeda dari proposal GSP/IDSBT-PRP/2026-01 (Rp 24.945.404.550) — dua iterasi; lihat objek arsenal-dosir-keputusan.",
    "arsenal-tahap-4-konfigurasi-70-kamera": "Nilai RAB Rev B (Rp 24.750.028.288) terverifikasi dari JSON meta+slide 13 (43 mata pembayaran, 10 kelompok); berbeda dari nilai proposal — dua iterasi; lihat objek arsenal-dosir-keputusan.",
    "forensic-nfl-2026-vendor-database": "Rekonsiliasi 298 vs 203: 298=hasil pattern-match analyze_forensic.py (analysis_summary.txt 'Total manufacturers found: 298'), 203=entri ter-enumerasi vendor_master_database.json.vendors_by_region (32+142+14+3+0+12). Dua angka beda konteks, sah; JANGAN dicampur. 585 entri vendors_by_region.json = nama produk/vendor campur, bukan hitung unik.",
    "china-expo-vendor-master-594": "Verifikasi ulang: sheet Vendor Master Expo_China_Vendor_Batch_01_20_CIDEX.xlsx = 593 record data (Security China 563 + CIDEX 30; 578 year 2024, 11 year 2023, 4 year 2022), bukan 594 — selisih 1 baris vs klaim objek; catatan koreksi minor.",
    "kemhan-bin-arsitektur-design-system": "Artefak campuran dua proyek (ARSENAL IDS TNI AL vs TICC BIN) terverifikasi di sumber; JANGAN disamakan; cross-link antar perkara disarankan saat konsumsi.",
    "arsenal-ids-design-system-master": "Angka agregat (Rp 24.945.404.550, 6.546,18 m, 69 ruas, sebaran 25/17/16/12) terverifikasi di design_system_master_ids_bt.md (baris 859, 1092); konvensi RH-10 membolehkan agregat verbatim tanpa koordinat.",
    "labinsen-tni-al-penawaran-2026": "Angka IDR 21.250.000.000 (16.750.000.000 + 4.500.000.000) terverifikasi di PDF penawaran (Total Harga + Terbilang); nomor 09/SPH/HSP/IV/2026 terverifikasi.",
    "forensic-nfl-2026-boq-epistemik": "CAPEX mid USD 21.659.434 = perhitungan mandiri (harga_mid x qty), bukan klaim dokumen — status sintesis sesuai objek; USD 1.474.400 / 6,8% adalah klaim dokumen (Kajian lembar kendali).",
}

PERKARA_REASON = {
    "adint-vendor-research": "Riset intelijen vendor ADINT untuk Board of Directors PT GSP (classification CONFIDENTIAL — Internal Use Only); sensitif, wajib persetujuan user sebelum promote.",
    "gsp-outputs-history": "Objek memuat referensi/lokasi & materi workstream klien pertahanan/intelijen (ADINT, RANSUS, Arsenal, enforcement) serta sistem flag RAHASIA; sensitif, wajib persetujuan user sebelum promote.",
    "kemhan-bin": "Dosir pengadaan klien BIN/KEMHAN (klasifikasi INTERNAL s.d. RAHASIA); sensitif + data pengadaan/klien menuntut verifikasi manusia (verification-by) sebelum terbit.",
    "china-defence-expo": "Riset intelijen vendor & produk pertahanan China (OSINT flags, sanksi BIS/CMCL/OFAC) untuk procurement planning GSP; sensitif, wajib persetujuan user sebelum promote.",
    "arsenal-ids-barat-timur": "Dosir pengadaan TNI AL — ARSENAL IDS Barat & Timur (klasifikasi RAHASIA — SALINAN 01 DARI 04 · TIDAK UNTUK DIEDARKAN); sensitif + angka RAB menuntut verifikasi manusia sebelum terbit.",
    "arsenal-tahap-4": "Dosir pengadaan TNI AL — konfigurasi 70 kamera (klasifikasi RAHASIA); sensitif + angka RAB menuntut verifikasi manusia sebelum terbit.",
    "catatan_keputusan": "Catatan keputusan kurasi dosir ARSENAL (RAHASIA); sensitif + verifikasi manusia untuk nilai RAB final.",
    "ransus-pengamanan-informasi": "Dosir proposal pengadaan klien BIN (klasifikasi RAHASIA, salinan 01/05); sensitif + verifikasi manusia untuk klaim vendor/spesifikasi sebelum terbit.",
    "riset-sistem-ai-gsp": "Riset internal berklasifikasi RAHASIA/strategis memuat rahasia strategi komersial GSP-KAM (moat, arsitektur, ekonomi internal); sensitif (rahasia strategi komersial), wajib persetujuan user sebelum promote.",
    "forensic-nfl-2026": "Dokumen intelijen pengadaan pra-keputusan (classification INTERNAL — PRE-DECISIONAL); sensitif + angka BOQ/CAPEX menuntut verifikasi manusia sebelum terbit.",
    "labinsen-tni-al": "Dosir penawaran klien TNI AL — Labinsen (harga, spesifikasi peralatan uji energetik); sensitif + harga menuntut verifikasi manusia sebelum terbit.",
    "china-expo-toni": "Data vendor pertahanan China (CIDEX 2024, Security China) untuk riset GSP; sensitif, wajib persetujuan user sebelum promote.",
}

def parse(raw):
    m = re.match(r"^---\n(.*?)\n---\n?(.*)$", raw, re.S)
    if not m:
        return {}, raw
    fm = {}
    for line in m.group(1).splitlines():
        if ":" in line:
            k, v = line.split(":", 1)
            fm[k.strip()] = v.strip()
    return fm, m.group(2)

def rebuild(fm, body):
    lines = ["---"]
    for k, v in fm.items():
        lines.append(f"{k}: {v}")
    lines.append("---")
    return "\n".join(lines) + "\n\n" + body.strip() + "\n"

count = 0
for f in sorted(VAULT.rglob("*.md")):
    perkara = f.relative_to(VAULT).as_posix().split("/")[0]
    if perkara not in PERKARA_REASON:
        continue
    raw = f.read_text("utf-8")
    fm, body = parse(raw)
    if fm.get("sensitif", "").strip('"') != "ya":
        continue
    oid = fm.get("id", "?")
    fm["status"] = "menunggu_persetujuan"
    notes = ["SENSITIF: " + PERKARA_REASON[perkara]]
    if oid in SPECIFIC:
        notes.append("REKONSILIASI/VERIFIKASI: " + SPECIFIC[oid])
    # gabung jadi satu baris YAML (tanpa newline)
    fm["catatan_keputusan"] = ' '.join(notes)
    f.write_text(rebuild(fm, body), "utf-8")
    count += 1
    print(f"  {perkara}/{f.name}: {oid} -> menunggu_persetujuan")

print(f"\nTotal objek sensitif ditandai: {count}")
