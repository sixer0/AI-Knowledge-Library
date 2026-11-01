# CER-001 — Cara Entitas Regional China (amandemen SPK-002, 04-09)

Dipakai untuk SEMUA akuisisi identifier entitas China / pameran di China. Dokumen penuh: `docs/2026-09-04-data-accuracy-standard/STANDAR-PROSEDUR-AKURASI-DATA-SPK-002.md` seksi 3b.

## Tangga akuisisi identifier (berjenjang, vonis berakun)
1. **R0 sumber resmi penyelenggara** — field situs di API direktori organiser (mis. API terdokumentasi penyelenggara: `POST <endpoint-detail>` body `{<id-perusahaan>, <id-pameran>}` -> field situs; endpoint yang tidak terdokumentasi tidak dicoba, catat `butuh otorisasi`). Otoritas identitas tertinggi: token-match TIDAK diperlukan, provenans "situs resmi dari API organiser".
2. **R1 registri CN** (aiqicha/qcc/tianyancha/qichamao) — HANYA jembatan nama hukum<->merek; tidak pernah jadi tautan terbit (halaman profil mereka = DIR-BLOCK).
3. **R2 pencarian MANDARIN** — kueri `"<nama_cn>" 官网` / `"<nama_cn>"` (bukan nama EN via search global). ddgs region cn efektif; Firecrawl sebagai pembanding.
4. **R3 ICP footer** — regex `(ICP备|备案号|京ICP|沪ICP|粤ICP|浙ICP...)` di body = penanda situs resmi CN terkuat.
5. **R4 CDX domain .cn + Wikipedia-ZH** — konfirmasi hidup dan disambiguasi merek (China Unicom <-> China United Network Communications).

## Larangan mutlak
- Nama kota/provinsi (shanghai/beijing/shenzhen/hangzhou/... ) sebagai BUKTI kepemilikan situs — semua perusahaan CN mengandung kota di namanya; ini akar insiden WAIC 04-09 (238/646 BENAR palsu: britannica/Wuhan, ehangzhou.gov.cn, chinahighlights/Shenzhen).
- Domain direktori/wisata/pemerintah-portal/berita/marketplace sebagai tautan terbit.
- Pencarian EN-global sebagai sumber identifier entitas CN.

## Aturan teknis
- **SATU modul aturan bukti** untuk semua lapis (gate/autofix/tangga/recheck/verifier): `cer_rules.py` pola kanonis — matcher ganda antar-lapis = buta-titik terwarisi (pelajaran D-T1-17/19). Uji regresi wajib (kasus pos+neg) setiap kali mengubah aturan.
- Bukti sah berjenjang: organiser-resmi > token-khas-di-label-host/prefik-label >=3 > title-token > merek-gabungan/akronim nama mentah (amgeneral, stengg, agl) > translisi Eropa (muenstermann, eberspaecher) > nama-CN-di-body > entitas-pemerintah+host-gov.
- Entitas pemerintah: kata geo ADALAH identitas (Region Ile-de-France -> iledefrance.fr sah); host gov = bukti.
- **Kegagalan fetch saat re-check BUKAN bukti salah** (D-T1-19f): hanya vonis tegas SALAH/DIR/GEO yang membatalkan; timeout tidak membatalkan temuan yang sudah berjejak.
- Nama hukum vs merek dagang hanya terjembatani Wikipedia/CDX -> whitelist dua arah ber-alasan, jangan edit senyap.

## Angka bukti penerapan (WAIC 04-09)
Tangga CER atas 369 antrean tanpa-situs: 251 FIXED (68%), jalur menang ddgs-kueri-Mandarin 231. Sumber R0 organiser menutup 482/1.019 langsung. Website terisi naik 641 -> 890/1.010 dengan tally verdict kekal.
