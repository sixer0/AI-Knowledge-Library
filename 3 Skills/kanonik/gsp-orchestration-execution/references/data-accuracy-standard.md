# Standar Prosedur Akurasi Data (SPK-002-GSP-IX-2026) - ringkasan operasional untuk orkestrator

Dokumen penuh: shared ws `docs/2026-09-04-data-accuracy-standard/STANDAR-PROSEDUR-AKURASI-DATA-SPK-002.md`. Rule terpasang di SOUL root+54 profil (skrip `gsp-hermes/scripts/install_data_accuracy_rule_20260904.py`, guard sisip-murni).

## Pemicu insiden
EXPO26-T1: kolom Website WAIC dipromosikan dengan 55% salah-target (China Telecom -> menu KFC Jepang; portal berita sama dipakai 7 perusahaan berbeda). Verifier+countersign PASS karena hanya menguji fidelity ke berkas sumber, bukan truth ke dunia. Sinyal sudah ada di flag hulu (FAIL name-not-found 538 baris) tapi tidak memblokir. User menemukan lebih dulu = kegagalan tata kelola.

## Tujuh prinsip (hafal)
1. Truth di atas fidelity - data warisan/hulu diuji ulang untuk field terbit.
2. Entity-match wajib untuk identifier eksternal (token nama di host/judul/OG/isi). Hasil pencarian tanpa gerbang = karantina.
3. Kosong lebih baik daripada salah.
4. Flag hulu memblokir promosi field.
5. Gerbang rilis = verifikasi deterministik 100% populasi field beban-rilis; sampling hanya monitoring/uji tandingan (seed tercatat, beda antar-putaran). Rilis hanya bila SALAH-TARGET=0.
6. Angka turunan: parser rekaman + uji semantik (preseden F-01 baris-fisik vs rekaman).
7. Temuan pasca-terbit: known-defect, traceroot tahap penyebab, tambal gerbang, remediasi populasi penuh, seed berbeda, revisi naik.

## Kewajiban kartu
- Kartu pengumpulan/konsolidasi yang menghasilkan field beban-rilis: cantumkan gerbang entity-match + larangan top-result mentah + kolom prov "hasil-pencarian-terverifikasi".
- Kartu penutup misi dengan data terbit: WAJIB tabel VERIFIKASI-AKURASI (field | populasi | metode | cakupan% | BENAR | SALAH-TARGET | MATI | KOSONG | keputusan | ts | seed). Tanpa tabel = kartu tidak bisa ditutup; verifier menolak.
- AC misi data wajib memuat minimal satu CHECK truth-hidup (fetch nyata + entity-match) per field beban-rilis, bukan hanya struktur/fidelity.
- Controller memegang gerbang P4; meloloskan rilis dengan salah-target>0 = pelanggaran dan wajib diumumkan dengan angka.

## Preseden pitfall terkait
- Fidelity-but-false: promoted.csv lama (E06) lolos depth audit karena audit menguji kutipan terhadap cache, bukan kepemilikan situs.
- summary_source boleh menunjuk halaman lepas: jangan samakan "sumber ringkasan" dengan "situs entitas".
- Flag weak/FAIL di hulu adalah sinyal mahal: hitung distribusinya sebelum memutuskan reuse pipeline lama.
