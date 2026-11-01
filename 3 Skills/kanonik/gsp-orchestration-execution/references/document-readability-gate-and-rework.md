# Gerbang Keterbacaan Dokumen + Pola Rework (preseden misi terkait / PROMANUAL-V2-1006, 04-06 Okt 2026)

Vonis user atas buku 686 hal edisi 1: "hard to understand, choice of words bad, no charts, knowledge not embedded" -> triase T1 (cacat penyampaian) + T4 (evolusi kebutuhan). Akar proses BUKAN pekerja: fase tulis mengukur kekayaan isi tapi TIDAK punya meteran keterbacaan di gerbang rilis. Pelajaran turun-temurun: untuk SETIAP misi dokumen panjang, keterbacaan dan visual adalah GERBANG TERUKUR, bukan harapan.

## 1. G-CECER - gerbang keterbacaan terukur (naikkan jadi syarat rilis, bukan aspirasi)
Meter deterministik (contoh hidup: `docs/2026-10-06-prompt-manual-v2/toolkit/cecer_meter.py`) per berkas:
- M1 rata-rata kata/kalimat: target <=18, keras <=20, kalimat tunggal maks 25 kecuali blok verbatim ber-tanda. Definisi kalimat/pemisah dinyatakan eksplisit di alat.
- M2 definisi-first-muncul >=95% (daftar istilah input; istilah = cetak tebal + kurung dalam 1 kalimat pada kemunculan pertama).
- M3 rasio figur >=1 per <=4 halaman (estimasi baris saat tulis; HALAMAN NYATA dihitung ulang dari PDF saat rakit).
- M4 penambat per seksi 100%; M5 blok anatomi ajar lengkap (mis. 7 blok: konsep-inti<=3 kalimat, analogi berlabel, figur pembawa, mekanisme, contoh+contoh-gagal, latihan 'kalau X diubah maka Y', penambat); M6 noise=0 (kalimat meta, hedge kosong, redundansi frasa).
- GERBANG RED-GREEN untuk meter itu sendiri SEBELUM dipakai menghakimi: alat harus mereproduksi angka kegagalan yang diketahui (dari laporan gerbang lama) DAN menangkap pelanggaran tananam. Alat tanpa bukti kalibrasi = bukan gerbang.
- Uji tandingan Pembaca-Butir: agen reviewer netral TANPA konteks tulis menjawab soal pemahaman per bab yang disusun dari REGISTER (kunci), target >=90%. Penulis-bukan-verifikator berlaku di sini.

## 2. Spesimen dulu, produksi kemudian (pattern anti-penolakan massal)
Sebelum gelombang rework/penulisan massal: 1 bab dirework penuh + dirender ke format final + divonis INDEPENDEN (keterbacaan + kontrak-desain butir-per-butir + konten-kekal + pembaca-butir). Vonis PASS melepas produksi; FAIL -> tambal GAYA/SISTEM dulu. Vonis spesimen memisahkan dengan tegas "naskah lulus semua uji" vs "lapis render/builder gagal" - kegagalan mesin render tidak boleh membatalkan produksi naskah yang sudah lulus (jalur paralel: naskah lanjut, render ditambal terpisah lalu re-vonis lapis render saja).

## 3. Konten-kekal saat rework penyampaian (anti-drift fakta)
- Register beku HANYA dibaca; klaim baru kartu fix ditulis ke ADDENDUM (`research/FIX/*/addendum-KL.md`), satu kartu REFREEZE menggabungkan append-only + sha16 baru + REFREEZE-LOG (LAMA->BARU, backup .pre-refreeze.bak, diff nol-suntingan-lama). Larangan sunting register beku langsung = risiko tabrakan tulis dengan kartu lain yang membacanya serentak.
- Angka/nama/URL/tanggal di naskah hanya placeholder terikat register; emitter memancarkan Register.json dari register beku; audit bind dua arah (stray=0 dengan allow-list tercatat); cakupan-balik: himpunan ID dikutip v2 == v1 (tidak ada ID hilang atau ID tambahan tanpa sumber); kesetaraan nilai numeral lintas format (EN->ID) diverifikasi parser.
- Parafrase dijaga dua-kanal: reviewer netral menguji "apakah paragraf baru membuat klaim yang tidak dibuat baris register-nya?" - satu 'ya' = FAIL butir.
- Putusan kanal naturalisasi milik USER bila ambang menabrak karakter genre (prosa teknis dewasa vs plafon kanal kitab yang dikalibrasi buku remaja): ajukan via dua-kanal dengan angka; putusan dicatat di Decision Log. Pengecualian verbatim (emoji objek ukur, keluaran mesin) = putusan controller tercatat, BUKAN hapus-buta.

## 4. Kelas cacat formulasi: kartu builder-berat > plafon bridge (SISTEMIK, preseden 12+ instance)
Kartu berformat "N bab + M figur + render" mati identik di 1800 dtk (timeout->retry->gave_up) BERULANG KALI lintas papan: RWA..RWE, SPEC4, RAKIT. Ini cacat FORMULASI cakupan kartu, bukan pekerja. Aturan turun-temurun:
- Estimasi kartu produksi wajib memperhitungkan plafond run 1800 dtk; bentuk kartu besar jadi RANTAI per-lapisan/per-bab (L1 kerangka, L2/L3/L4 badan, L5 bind-final+PDF+lint) dengan checkpoint append per bagian.
- Setelah kemati-serentak: UKUR DISK dulu (naskah/aset yang lahir SELAMAT dan besar), baru unblock + komentar RESUME berisi daftar aset beku (larangan rebuild) + sisa kerja terkurangi + kewajiban partial-handoff ber-pin sebelum plafon (anti 'mati bisu'). JANGAN lepas kartu pecah baru sementara run resume masih hidup (tabrakan kerja ganda, preseden 03-09).
- Watchdog boleh mengelola kap: antrean kartu ber-status blocked-transient ('slot terbuka = unblock otomatis') agar tidak ada waktu mati menunggu controller.

## 5. Kartu vonis dengan VERDICT FAIL ditutup complete, bukan dibiar menggantung
Kartu gerbang (verifier/reviewer) yang memvonis FAIL TELAH menjalankan fungsinya: tutup `complete` dengan result "gerbang dijalankan penuh; VERDICT FAIL terdokumentasi" + rujukan laporan temuan, lalu remedi lewat kartu fix terpisah (maks 2 retry). Penahan promosi ditegakkan lewat EDGE DAG (hilir ber-parent kartu vonis/remedi), bukan lewat status blocked permanen.

## 6. Pitfall mekanik yang terbukti di sesi ini
- Modul builder kartu yang membuat kartu di LEVEL-MODUL (tanpa guard `if __name__ == "__main__"`) akan MENJALANKAN create ulang saat di-import giliran lain -> gelombang duplikat. Aturan: panggil `lad_card.py` langsung per kartu, atau guard keras; tabrakan terjadi = set lebih dulu kanonik, duplikat (ready, nol run) komentar jejak + archive.
- Status papan dibaca dari `show --json` level `["task"]["status"]`; parser yang salah level menghasilkan '?' yang loop penutup salah vonis 'SETTLED'. Perlakukan '?' sebagai TIDAK-TERKENAL (lanjut), bukan terminal.
- `curl/python -o` dll: path git-bash tidak diterjemahkan untuk program native - selalu C:/... (sudah di pitfalls utama; tetap hidup).
- Payload inline besar (heredoc multi-ribu char) bisa kena hardline parser terminal: tulis skrip ke berkas Temp lalu jalankan; `$_` PowerShell tertelan konversi MSYS - tulis .ps1 ke berkas.
- Glue antar-alat antar-kartu adalah pekerjaan controller yang sah dan murah: format input alat beda (terms JSON vs TXT), pin usang (berkas sumber dimutakhirkan sesi lain semalam) - ukur ulang pin pada giliran pakai, pancangkan konversi, steering ke kartu berjalan via komentar (jangan kartu baru).

## 7. Peta rujukan
- Preseden artefak: `docs/2026-10-04-prompt-manual/` (v1, vonis user) dan `docs/2026-10-06-prompt-manual-v2/` (rework: blueprint §6 anatomi cerna, §7 peta visual, §8 konten-kekal; toolkit/ cecer_meter + datum_buku; verification/vonis-spesimen*.md).
- Otoritas bentuk dokumen DATUM: skill fleet `datum-house-style` + guideline `docs/2026-10-03-datum-guideline/` (lihat juga memory #standar-datum; berkas kanonis lama hilang - known-defect fleet).
- Lapis satelit: [`saturation-gate-sweep-lanes.md`](saturation-gate-sweep-lanes.md) (vonis jenuh per lajur riset buku), [`knowledge-baseline-architecture.md`](knowledge-baseline-architecture.md) (anatomi dokumen), [`design-contract-drift.md`](design-contract-drift.md) (dump sumber -> KONTRAK-DESAIN -> re-vonis artefak).
