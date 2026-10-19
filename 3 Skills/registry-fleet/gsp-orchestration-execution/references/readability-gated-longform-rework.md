# Gerbang Keterbacaan Keluaran Panjang + Protokol Rework Konten-Kekal

Preseden: PROMANUAL-1004 (edisi 1, buku 686 hal) -> vonis user -> PROMANUAL-V2-1006 (rework edisi 2), Okt 2026.
Pemicu berlakunya: vonis user atas dokumen panjang yang dibaca manusia ("hard to understand", "choice of words and sentences are bad", "not explaining with charts/graphics/visualization", "eliminate the noise"). Prioritas user yang dinyatakan: pembaca mencerna SELURUH pesan; pengetahuan tertanam setelah baca.

## 1. Triase dulu, baru bergerak (protokol KLAIM-TRIAGE untuk vonis dokumen)
- T1 cacat penyampaian: kalimat padat / nol figur / noise - buktinya angka keterbacaan terukur, bukan perasaan.
- T4 evolusi kebutuhan: gaya/kanal/bentuk baru diminta (house style, visualisasi) - scope baru, bukan kesalahan siapa pun; edisi lama tetap artefak sah (arsip), tidak dicabut.
- Nyatakan AKAR PROSES dan tambal di gerbang, bukan hanya di naskah. Preseden: edisi 1 gagal karena KETERBACAAN tidak pernah menjadi syarat lulus; vonis "lulus" hanya sah dengan angka keterbacaan + uji cerna pembaca.

## 2. Meter keterbacaan WAJIB terkalibrasi sebelum dipakai menghakimi
Enam metrik per bab (contoh implementasi: cecer_meter.py, 594 baris, deterministik dua-run byte-identik):
- M1 rata-rata kata/kalimat: target <=18, keras <=20, kalimat tunggal maks 25 kecuali verbatim ber-tanda. Definisi pemisah kalimat (. ! ? di luar blok kode/tabel/URL) dinyatakan eksplisit di alat.
- M2 definisi-first-muncul >=95% (istilah didefinisikan inline saat kemunculan pertama; tabel glosarium sah via flag).
- M3 rasio figur >=1 per <=4 halaman badan (estimasi baris; halaman nyata dihitung saat rakit).
- M4 penambat per seksi 100% (blok ringkas sebelum heading setingkat berikutnya).
- M5 blok anatomi ajar lengkap. Tujuh blok terbukti untuk buku ajar: konsep-inti (<=3 kalimat, janji hasil) | analogi berlabel aside | figur pembawa klaim | mekanisme (satu gagasan satu kalimat) | contoh + contoh-gagal | latihan "kalau X diubah maka Y" + mini-eksperimen | penambat + jembatan.
- M6 noise = 0 (kalimat meta, hedge kosong, redundansi). Definisi noise: elemen penyampaian tanpa beban informasi. BUKAN noise: angka, atribusi, predikat keraguan, batasan klaim, tanggal, URL. Uji satu kalimat: "apakah menghapusnya membuat pembaca kehilangan informasi yang bisa salah?" Ya = fakta, tahan.

GERBANG RED-GREEN alat (wajib sebelum dipercaya): (a) reproduksi angka kegagalan dikenal dari korpus lama dalam toleransi parser; (b) tanam 3 pelanggaran (kalimat 40 kata, istilah tanpa definisi, seksi tanpa penambat) -> ketiganya tertangkap; (c) berkas contoh cerna -> PASS. Alat penghakim dikalibrasi dulu, baru menghakimi.
GLUE: jangan asumsikan format input alat tetangga - contoh nyata: berkas istilah dibaca sebagai TXT satu-istilah-per-baris (alias setelah '|'), sementara pekerja menyerahkan JSON; pancangkan konversinya + jadikan aturan kartu (serahkan DUA format).

## 3. Uji pembaca-butir (retensi, bukan rasa)
Agen reviewer NETRAL (tanpa konteks tulis) menjawab 5 pertanyaan pemahaman per bab yang disusun dari REGISTER (bukan dari teks), tanpa sumber luar; skor >=90% lulus. Anti-bocor: penanya tidak membaca draf; penulis bukan verifikator.

## 4. Rework konten-kekal (penyampaian berubah, fakta tidak bergeser)
- Pin sha16 register beku sumber; UKUR ULANG saat kartu dipakai - pin bisa basi bila berkas hulu dimutakhirkan (kejadian nyata: pin standar gaya usang karena revisi semalam; berkas kini identik arsip rev resmi).
- Angka/nama/URL/tanggal hanya placeholder ke register atau salinan verbatim; emitter memancarkan register edisi-2 dari edisi-1 (append-only, tidak diketik tangan).
- Audit dua arah saat rakit: himpunan KL v2 == v1 (nol hilang, nol hantu); stray angka = 0; kesetaraan nilai numeral lintas format (ribuan/persen rumah) diverifikasi parser, bukan mata.
- Perubahan nilai hanya lewat putusan controller tercatat + refreeze append-only (baris DICABUT ditandai, tidak dihapus) + log LAMA->BARU + backup + diff "hanya baris berizin berubah".

## 5. Specimen-first production gate (hindari penolakan massal)
1. Rework SATU bab sebagai spesimen penuh + figur nyata (PNG 300 dpi, grid bentuk final).
2. Render ke bentuk final; vonis independen menguji DUA LAPIS TERPISAH: lapis NASKAH (keterbacaan, konten-kekal, uji cerna) dan lapis RENDER/BUILDER (halaman muka, ukuran kertas assert twips, lembar kendali, kolofon, rel glif, lint).
3. Naskah PASS + render FAIL = tambal MESIN, JANGAN sentuh naskah; pin hash naskah agar remediasi tidak bisa memutasi isi; re-vonis hanya lapis render.
4. Baru lepas produksi massal paralel (kap 5 running/misi). Akselerasi user boleh produksi dini MENYUSUL spesimen yang sudah PASS meter teks - tiap kartu produksi membawa klausul risiko-revisi + laporan keputusan penyampaian agar revisi murah.
5. Lembar verifikasi akhir buku mencetak angka PER BAB (bukan rata-rata buku): M1-M6, skor uji cerna, predikat desain per butir, SALAH-TARGET=0, defect tampil-tautan=0, hasil scanner, sha16 register.

## 6. Aturan kanal naturalisasi untuk buku (putusan user "paling komprehensif")
Kanal TERKETAT berlaku; dicapai lewat SUNTINGAN KEPADATAN menyeluruh dengan aturan konten-kekal mutlak, BUKAN menurunkan ambang atau menukar kanal. Pengecualian verbatim terkendali: baris register yang memuat objek ukur (emoji pada uji tokenisasi) dan keluaran mesin wajib tetap verbatim - menambalnya = memalsukan rekaman ukur; yang dibetulkan adalah SENSOR (mode verbatim-mesin), bukan datanya.

## 7. Sumber desain & mesin kanonik yang hilang
Dump struktur sumber desain (berkas otoritas user + token skill) SEBELUM blueprint; KONTRAK-DESAIN per butir PERSIS/ADAPTASI-alasan/DIBUANG-putusan-user. Mesin kanonik hilang dari registry (mis. chart engine, renderer): pulihkan BENTUK+ATURAN dengan mekanisme pengganti terdokumentasi (matplotlib dikonfigurasi token; renderer SVG->PNG alternatif dibuktikan selftest) - predikat bentuk tetap PERSIS, penggantian mesin dicatat. Known-behavior fleet (glif tanpa wajah font) dicatat di lembar verifikasi; jangan tukar font.
