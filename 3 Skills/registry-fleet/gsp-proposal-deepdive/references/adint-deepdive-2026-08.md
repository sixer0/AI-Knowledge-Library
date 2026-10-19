# Studi kasus: pendalaman proposal ADINT 150 hal (2026-08-24)

Detail nyata yang menjadi dasar skill `gsp-proposal-deepdive`.

## Dokumen & ekstraksi
- Sumber: `GSP_Technical_Report_ADINT.pdf` — 150 hal, GSP-TR-ADINT-2026,
  Advertising Intelligence (de-anonimisasi via ekosistem iklan programatik RTB)
  untuk Kementerian Pertahanan RI.
- `read_file` gagal: "PDF has no extractable text (TextBased, 150 pages): OCR
  is required". **KELIRU** — pymupdf mengekstrak 426.885 karakter, 0 halaman
  kosong. Seluruh pendalaman dikerjakan dari lapisan teks; OCR vision tidak
  pernah dibutuhkan (meski skill OCR GSP sebelumnya sempat dipakai pada
  dokumen ini dan menghasilkan halusinasi — lihat gsp-document-vision-ocr).
- Output: `raw/adint_proposal_full.md` (8.234 baris, 453 KB) dengan penanda
  `<!-- ===== PAGE N ===== -->`.

## Struktur kerja yang terbukti
```
adint-deepdive/
  00_decomposition.md        # peta bab/lampiran + 13 asumsi kunci + rencana
  vendor_lists.md            # 141+ vendor per 6 kategori (nama, origin, produk, website)
  raw/                       # bahan mentah subagen (extract_*, wiki_*, search_*.json)
  research/01_*.md           # verifikasi 13 asumsi (subagen 1)
  dossier/01_*.md            # ADINT + broker (46 vendor) (subagen 2)
  dossier/02_*.md            # identity + ad-tech (33 vendor) (subagen 3)
  dossier/03_*.md            # OSINT + crypto (62 vendor) (subagen 4)
  landscape/                 # catatan orkestrator: market sizing, status website, katalog tambahan
  report/                    # bab-bab laporan + master GSP-TR-ADINT-DEEP-2026.md
  scripts/rakit_laporan.py   # penggabung bagian-bagian + output subagen
```

## Orkestrasi (4 subagen paralel)
1. Verifikasi 13 asumsi teknis inti (RTB sensor grid, OpenRTB 2.6/AdCOM, eids
   atype=3, Privacy Sandbox mati Okt 2025, Starlink D2C, VPN de-anon, Fellegi–
   Sunter, crypto forensics, angka vendor, klaim demo).
2. Dossier ADINT/bid-stream (13) + location brokers (33).
3. Dossier identity graphs (14) + ad-tech supply chain (19).
4. Dossier OSINT/fusion (46) + crypto-intel (16).

Tiap subagen: output path unik, format per vendor baku (identitas/produk/
website/risiko/relevansi Indonesia), label [VENDOR] untuk klaim pemasaran.

## Temuan koreksi penting (dimasukkan ke laporan)
- **Privacy Sandbox mati** (17 Okt 2025) → ADINT persistent (Engadget/Google).
- **Starlink D2C** FCC grant Nov 2024 → IMSI/MSISDN nyata + lawful intercept
  (TechCrunch/Bloomberg).
- **TargetTeam/Stargetz** dikonfirmasi Cyprus Inform (Mei 2026): ~1 juta
  terminal Starlink, VPNz, mantan karyawan Rayzone & Cognyte.
- **Tornado Cash sanksi DICABUT** 21 Mar 2025 (The Block) — proposal hanya
  menyebut sanksi 2022.
- **IMX (Indonesia Mobile Exchange)** — imx.co.id kini blog "Bisnis & Digital
  Marketing", bukan exchange aktif; koreksi asumsi arsitektur sovereign.
- **NSO Group diakuisisi investor AS** (Okt 2025, TechCrunch).
- **Indodax 44,68%** market share Okt 2025 (Kompas) — cocok klaim >40%.
- **Android Indonesia 82,78%** (StatCounter mobile+tablet) — cocok ~83%.
- **Citizen Lab Webloc** (500M devices) + ATF batalkan kontrak Webloc (AP).
- Angka vendor deck vs live site: Beosin 5B→~2B, 220M→~22M; Coinfirm akuisisi
  21 Mei 2024; Merkle Science investor (Kraken Ventures/DCG/Fenbushi).

## Pitfalls yang benar-benar terjadi
- **web_search guardrail**: mencapai batas ~50 panggilan per turn
  (loop_web_search_cap) setelah banyak pencarian paralel + retry; ganti strategi
  (web_extract untuk URL yang sudah dikenal, serahkan ke subagen).
- **Subagen hang di browser_exec**: timeout 420s; dua kali steer tidak memotong
  tool call yang berjalan — steering baru berlaku setelah call selesai.
- **Subagen menulis bahan di raw/ tapi file final belum ada** sampai akhir —
  verifikasi file output sebelum klaim selesai.
- Backend pencarian (searxng lokal) kadang mengembalikan noise (Zhihu, kamus) —
  perlu query presisi + web_extract langsung pada domain target.
