# Pipeline Kanonis v1 - verifikasi-saat-crawl untuk pendalaman exhibitor (SPK-002 P4/3b)

Diturunkan dari post-mortem EXPO26-T1 (04-09): akar lambat = data diturunkan TANPA bukti, lalu diverifikasi ulang di hilir (gate 100% + autofix = dua lintasan fetch ganda). Prinsip: **fetch sekali, verifikasi sekali, bukti menempel pada baris selamanya**.

## Lintasan (satu pass, tanpa daur-ulang)
1. **ACQUIRE** -> `staging.csv` (entitas unik, GUID-key, denominator gate tercatat).
2. **STAGE-1 (validasi situs SAAT crawl)**: untuk tiap baris ber-url: fetch 1x + entity-match (host label / title / OG / dua-token-sekuensial; domain generik ditolak; akronim pendek via label-domain) + fallback pencarian ber-gateway (kandidat baru wajib lolos entity-match SEBELUM diterima). Tulis per baris: `website_final, verdict(BENAR/SALAH-TARGET/MATI/KOSONG), status, final_host, sinyal(json), ts`. Baris tanpa situs: jalur pencarian penuh di tahap ini, bukan triase terpisah. TIDAK ADA baris turun tanpa verdict.
3. **CLASSIFY / SCORE**: deterministik dari staging+verdict (flag hulu ikut terbawa).
4. **DRILL Tier A/B**: fetch 2-8 halaman, tulis `evidence/drill/<id>.json` + kolom `drill_done, evidence_sha`. Ringkasan memakai templat BEBAS-DINGBAT (larangan em-dash di templat, preseden D-T1-11).
5. **PROMOTE/LOOP re-entrant** sampai nihil promosi (parity finish_expo).
6. **TRANSFORM -> pd_rows.csv** (modul bersama satu-definisi; kolom Website = `website_final`; Catatan validasi memuat verdict+ts).
7. **BUILD workbook**: gerbang wajib di dalam builder: kekekalan vs basis, KENDALI terhitung, hyperlink-rusak=0, **tampil-tautan=0** (setiap URL punya hyperlink http + warna ALERT FF9B1C1C + underline), dingbat-hanya-verbatim, roundtrip CSV->sheet 0 beda.
8. **GATE AKURASI FINAL 100% cache-only**: baca bukti tahap 2 (tidak fetch ulang kecuali baris tanpa bukti); exit non-zero bila SALAH-TARGET>0. Sampling seed berbeda = uji tandingan, bukan gerbang.
9. **LAPORAN + LEDGER** klaim resolve; countersign independen (skrip sendiri, sha dibaca dari disk saat mulai).

## Kontrak kolom wajib stage-1 (tambah dari 23 kolom lama)
`website_final, verdict_site, http_status, final_host, match_sinyal, site_ts, site_evidence_sha`

## Perkiraan waktu (kalibrasi E11)
2.636 baris stage-1 dengan fetch-once: ±45 menit (ThreadPool 8-10). Hilir tanpa re-fetch: gate final <5 menit. Total misi pendalaman expo berikutnya: target < 6 jam end-to-end (vs ~14 jam T1 karena daur-ulang).

## Gerbang anti-kelaparan-laju
- Backend pencarian MATI SENYAP = defect (preseden firecrawl :3002 /v1 search mengembalikan [] untuk semua kueri). Wajib probe hidup + statistik tried/hit/err dicetak; hit=0 dengan tried>0 = alarm; tried=0 padahal ada baris tanpa-situs = GAGAL, bukan hasil.
- Vonis matcher buta non-latin/akronim/nama-dagang: whitelist controller ber-alasan + bukti dua arah, JANGAN edit senyap.
