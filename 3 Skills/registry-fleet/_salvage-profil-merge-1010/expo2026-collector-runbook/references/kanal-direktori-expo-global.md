# Referensi: kanal direktori expo global utk lajur sapuan (LB pola, AIE26SAT-1013 r1, 13-10-2026)

## EventEye (eventseye.com) = kanal primer yang HIDUP dan statis
- Kalender bulanan: `https://www.eventseye.com/fairs/d1_trade-shows_<bulan>_<hal>.html`
  - halaman `_0` = tahun berjalan (judul "Trade Show Calendar - January 2026"); `_1+` = tahun BERIKUTNYA (terbukti judul January/October 2027). Panen jendela 2026 = `_0` saja.
  - Baris fair: regex `href="(f-[^"]+\.html)"><b>(nama)</b><i>(deskripsi)</i>`; 50/halaman.
- Halaman tema: `t1_trade-shows_<slug>.html` + paginasi `_1.._N` (404 = ekor paginasi). Tema relevan tiga-ring: ict-information-communications-technologies, industrial-data-computing, quality-security, sciences-for-engineers-r-d, electronics-electrotechnics, industrial-fairs, office-equipment-service, equipment-service-for-commerce-and-industry. Zona: `zt1_trade-shows_<benua>_ict-...html`.
- Endpoint pencarian `/cgi-bin/tsearch.pl?SEARCH=` = MATI (200 shell 'Résultats' 5 KB, 0 fair-link). sitemap.xml & robots.txt = 404 (tidak ada robots -> tanpa batasan).
- Encoding halaman = cp1252 (bukan UTF-8!): decoder WAJIB fallback cp1252 atau Zürich/São Paulo rusak.
- Field detail f-*.html: `<h1>`, tanggal di `<td>` ("Oct. 06 - 08, 2026" / "Sept. 22, 2026"), kota+negara `cy1_...>City (Country)</a>`, venue `pl1_...title="...">`, cycle ("once a year"/"every 2 years"), URL RESMI ACARA = anchor `title="Go to X website"` (urutan atribut bebas: href bisa sebelum/sesudah title - regex dua arah!), url penyelenggara = `class="ev-web" href="..." title="Org - ..."`.
- Footer detail: "(Last update: Oct. 21st 2025)" -> direktori basi <=12 bln -> vonis PARTIAL+resweep, bukan jenuh.

## PITFALL parser tanggal direktori (cacat nyata r1, ketahuan oleh cek Gate-B)
Rentang lintas bulan "Nov. 30 - Dec. 02, 2026" dan "Jan. 27 - 29": regex harus menangkap BULAN kedua eksplisit; bulan-selesai < bulan-mulai => tahun selesai +1. Tanpa ini banyak baris selesai<mulai (invarian Gate-B #6 FAIL massal).

## Kanal MATI/TERBLOKIR dari host ini (akun 13-10-2026; jangan buang iterasi, langsung jalur cadangan)
- 10times.com: 403 urllib SEMUA path + Edge dump-dom = "Just a moment..." (Cloudflare). Jalur sah: CDX web.archive.org (retry setelah jeda - percobaan pertama kena 503/timeout; retry 200, snapshot topic AI Feb-2026 ada) ATAU agregator PROV. archive.ph/newest = 404 utk halaman topik.
- tradeshowwatch.com: DNS mati www+apex (ERR:URLError dua varian).
- auma.com: navigasi riil = /en_001/company/trade-fairs (SPA; render Edge 186 KB berisi event AUMA sendiri + kontak worldwide, TIDAK ada indeks expo global per-acara) -> AUMA hanya pembanding makro S3, bukan sumber baris. Path lama auma-de.com mati; semua tebakan /en/worldwide-exhibitions/ dkk 404.
- Kamar dagang: ahk.de/en/events + gtai.de/en/invest/events hidup (200) tapi isi seminar bilateral bukan direktori expo; amchamchina.org 403, britishchamber.co.uk 403, accshk.org ERR, amcham-shanghai.org shell 2 KB.

## DDGS multi-bahasa (kelas 4) hidup penuh
`uv run --quiet --with ddgs python <skrip>` 12/12 kueri sukses (EN/FR/DE/ZH/ES/IT/JP), 7-9 hit/kueri. Flagship bernama hasil kueri (WAIC, Ai Everything, Web Summit, RAISE, CES, IFA, HumanX) JANGAN dipanen lajur direktori -> LEMPAR.csv ke LC (kontrak §C-LC anchor penyelenggara).

## Pola rantai deterministik hemat iterasi
Simpan SEMUA fetch mentah ke raw/LB dengan nama prefix (idxA_/idxD_/det_/url_/chamber_/cdx_), lalu skrip akhir (classify->entity-match->build->Gate-B check) jalan ULANG dari cache tanpa re-fetch (cek `os.path.exists` + ukuran minimum). Healing cacat parser = patch + jalankan ulang skrip akhir, murah iterasi. Berkas append-only lintas lajur (LAMPIRAN-KANDIDAT.csv, LEMPAR.csv): JANGAN pernah overwrite bila sudah ada; skip kunci yang sudah ada saat append.

## Angka dasar r1 (pembanding r2)
Indeks 60 halaman (56x200, 4x404 ekor) -> 2.164 fair unik -> 245 kandidat ring -> 169 window-2026 -> delta 168 (+1 lempar-CER LD). EM: PASS 119 (R0), AGG 32, DEAD 12, FAIL 6 (identifier KOSONG, UNVERIFIED). Ring 68/83/17. Negara top USA 27 China 14 India 11.
