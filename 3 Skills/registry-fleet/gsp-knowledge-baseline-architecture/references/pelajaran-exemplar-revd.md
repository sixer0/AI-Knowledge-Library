# PELAJARAN-EXEMPLAR-REVD — Diff artefak misi IMS-WMS-DRP-0908 vs sumber pelajaran
Ditulis: 09-09-2026 | Status: jejak internal (rujukan perbaikan permanen)
Sumber pelajaran: Dasar_Pengetahuan_Project_IMS_WMS_Arsenal_Batu_Poron____-GSP-KT-IX-2026_RevC.pdf (133 hal) & RevD.pdf (135 hal) — jawaban AI pesaing atas tugas yang sama, dipakai user sebagai alat ukur.

## 1. Vonis ringkas
Keluhan user "tidak tersusun dengan baik dan profesional" TERBUKTI benar dan terlokalisasi:
- Akurasi data saya bukan masalah (gerbang angka 0 cacat). Masalahnya ARSITEKTUR DOKUMEN dan CARA MENYAJIKAN KEDALAMAN.
- Dokumen saya = "apa kata tiap dokumen sumber" (organisasi per-sumber, dump mentah per-baris 4.700 baris ke dalam dokumen).
- Dokumen RevD = "bagaimana sistem ini akan dibangun" (organisasi per-sistem; data mentah jadi masukan satu rantai hitung beku; dokumen memuat MODEL + REGISTER + KEPUTUSAN, berkas kerja mentah cukup disertakan sebagai lampiran kerja).

## 2. Anatomi arsitektur RevD (hasil pembacaan halaman-per-halaman)
1. HALAMAN MUKA penuh identitas: klasifikasi + nomor salinan (01 dari 03), alamat divisi, judul + subjudul + 1 paragraf lingkup, nomor dokumen + revisi + tanggal, PENYUSUN/KUSTODIAN (ENG-01)/DITUJUKAN KEPADA/HALAMAN, dasar lingkup, status verifikasi, NIB + ID terbitan.
2. LEMBAR KENDALI: tabel riwayat revisi REV|TANGGAL|APA YANG BERUBAH|MENGAPA|DAMPAK. Disiplin append-only: "Tidak satu pun nilai lama berubah; penambahan bersifat menambah, bukan mengoreksi." Keputusan Direktur tercatat dengan dampaknya (populasi 121 disahkan; gudang berperangkat 98->113; seluruh turunan bergeser naik).
3. CARA MEMBACA dengan routing pembaca: pembaca cepat (Ringkasan+Bab1+4B+16), penyusun daftar kuantitas (4A,4B,6-14,A,I,N), pemeriksa angka (2,4,B,C).
4. REL BUKTI: kolom kanan 32 mm berisi tanda asal angka per paragraf (glif DATUM: TERUKUR■, DITURUNKAN◈, PEMASOK◇, ASUMSI△) + rujukan sumber. Kolom kosong = keadaan benar.
5. RINGKASAN R.1-R.6: sepuluh angka lingkup (tabel), delapan angka teknis + dasar singkat, keadaan dokumen sumber (N temuan, N uji lulus), tiga penahan + cara membuka, pembeda rancangan, keputusan yang tertahan + akibat ditunda.
6. BAB 2 METODE + GERBANG BEKU MODEL: tiga syarat pembekuan; sebaran tanda asal dihitung dan ditampilkan (569 besaran: 219 TERUKUR, 329 DITURUNKAN, 1 PEMASOK, 20 ASUMSI); tingkat artefak TERBIT vs SERAH didefinisikan eksplisit.
7. BAB 3 RANTAI TURUNAN: pohon turunan (satu akar populasi -> profil -> kamera/port -> aliran -> bandwidth/storage/telemetri); contoh penelusuran 6 kuantitas sampai masukan terukur; akibat selisih satu gudang dihitung eksplisit (634 vs 628 port, dampak ke switch dan unit); MATRIKS DAMPAK 10 masukan x daftar lengkap besaran yang wajib dihitung ulang; cara menjalankan perubahan.
8. BAB 4 SILSILAH DOKUMEN: daftar D-01..D-10 + kedudukan (Masukan / BASELINE berlaku / Turunan / Lingkup berbeda tidak dipakai / Konteks); penetapan SATU dasar lingkup dengan tiga alasan yang dapat diperiksa; TABEL ANGKA DITARIK DARI PEREDARAN (besaran | nilai lama | nilai berlaku | alasan).
9. BAB 4-A/4-B: data dasar asesmen pemberi kerja apa adanya + bab kalibrasinya (profil perangkat lengkap per tipe bangunan, tiga keputusan direktur).
10. BAB 5-15 per SUBSISTEM: arsitektur tujuh lapis, sembilan zona jaringan, profil perangkat, proses gudang + kaidah dua orang, jaringan (port/switch/PoE/bandwidth/pekerjaan sipil), armada kamera + audit register + celah + peremajaan, deteksi-alarm-eskalasi, server AI + anggaran VRAM, otoritas AI (28 aksi, tiga tingkat, 7 tertutup permanen), pertahanan berlapis + pemakaian ulang aset, penyimpanan-telemetri-retensi, keselamatan amunisi (zona HERO, batas pemancar).
11. BAB 16-19: anggaran + ENAM GERBANG PENGUNCIAN + tiga pertanyaan wajib; risiko dengan biaya terukur; peta jalan lima tahap; PERTANYAAN PEMERIKSA DAN JAWABANNYA (Q&A antisipatif per kelas pertanyaan).
12. LAMPIRAN A REGISTER KUANTITAS BEKU (grup A-N, alfabetis; nama|nilai|satuan|tanda|dasar). LAMPIRAN B UJI DUA RUTE (164 uji; nilai rute1 vs rute2 side-by-side; putusan COCOK). LAMPIRAN C TEMUAN AUDIT T-01..T-42 (kelas KRITIS/MAYOR, pernyataan, Dampak, Tindakan; termasuk kesalahan dokumen GSP sendiri — dilaporkan, bukan disembunyikan). LAMPIRAN D asumsi + akibat bila salah. LAMPIRAN E sumber + cara menelusuri satu angka + BERKAS KERJA YANG MENYERTAI. LAMPIRAN F kamus. LAMPIRAN G batas pengetahuan + bantahan + tiga hal yang tidak dilakukan. LAMPIRAN H-N modul kanonik, daftar kuantitas indikatif 12 kelompok, matriks ketertelusuran kebutuhan->kuantitas, rekonsiliasi lingkup antardokumen, rancangan uji terima, catatan interogasi, master data materiil.
13. PENUTUP LEMBAR VERIFIKASI AKHIR: tabel PEMERIKSAAN|CARA|HASIL (rantai berjalan penuh, 164 uji, jalan ulang byte-identik, pengikatan angka 569, aritmetika blok derivasi, geometri gambar A4, interogasi 13 berkas, rekonsiliasi lembar) + "YANG TIDAK DIPERIKSA OLEH ALAT" (4 hal milik manusia) + SIDIK JARI MODEL (sha256 terpotong 16 digit; dokumen turunan mengutip sidik jari yang sama).
14. Nomor dokumen jujur: "[?]/GSP/KT/IX/2026" + catatan bahwa menebak nomor merusak keunikan register; diisi pada rekonsiliasi. Isi tidak bergantung nomor.

## 3. Diff butir-per-butir vs artefak saya
| # | Aspek | RevD (contoh) | Artefak saya | Vonis |
|---|---|---|---|---|
| 1 | Organisasi bab | Per subsistem/keputusan desain | BAB 3-11 per dokumen sumber; 12-21 campur | STRUKTUR SALAH |
| 2 | Angka naskah | Diikat dari register (nol angka diketik) | Diketang penulis, diverifikasi belakangan | PROSES LEMAH |
| 3 | Rantai turunan | Satu spine beku + pohon + matriks dampak perubahan | Register hasil hitung per-kartu; tidak ada matriks dampak | HILANG |
| 4 | Penetapan dasar | Bab silsilah + 3 alasan + angka ditarik | Register otoritas internal; tidak jadi bab depan | HILANG dari dokumen |
| 5 | Data mentah | Berkas kerja menyertai (E.3) | Dump 4.700 baris masuk dokumen | OVERLOAD (misbaca steering D-14) |
| 6 | Rel bukti per paragraf | Ada (32 mm, glif DATUM) | Glif hanya di register | HILANG |
| 7 | Uji dua rute side-by-side | 164 uji di Lampiran B | GATE-CALC internal (30 cek) | SEBAGIAN |
| 8 | Temuan audit dalam dokumen | T-01..T-42 + dampak + tindakan | REGISTER-KONTRADIKSI 71 butir tetap di folder internal | HILANG dari dokumen |
| 9 | Lembar verifikasi akhir + batas alat | Di halaman penutup | COUNTERSIGN.md di luar dokumen | HILANG dari dokumen |
| 10 | Sidik jari model beku | sha16 register, dikutip turunan | Hash berkas keluaran saja | HILANG |
| 11 | Routing pembaca | 3 jalur baca | Ada cara membaca, tanpa jalur per peran | SEBAGIAN |
| 12 | Riwayat revisi ber-dampak | Tabel REV|APA|MENGAPA|DAMPAK | Blok riwayat revisi minimal | SEBAGIAN |
| 13 | Q&A pemeriksa | Bab khusus | BAB 20 klarifikasi terbuka | SEBAGIAN |
| 14 | Gerbang penguncian | 6 gate + 3 pertanyaan wajib menahan | Gate penguncian ada (BAB 20) | ADA (perlu dipertajam) |
| 15 | Kejujuran placeholder | [?] + mekanisme rekonsiliasi | "USULAN 041..." | SETARA |
| 16 | Kelengkapan identitas muka | Salinan/kustodian/alamat/NIB | Blok identitas GSP-SDT | SEBAGIAN |
| 17 | Kerapatan | 135 hal penuh keputusan | 219 hal, sebagian besar dump | INEFISIEN |
| 18 | Kesegaran korpus | Baseline P-0003 Rev A 8-Sept + keputusan direktur | Korpus terakhir 29-Jul; tidak cek edisi lebih baru | AKAR MASALAH HULU |

## 4. Traceroot (mengapa bisa terjadi)
1. Blueprint TA menyusun kerangka dari permintaan RT "basis pengetahuan komprehensif per-domain" -> lahir organisasi per-sumber. Tidak ada gerbang "arsitektur dokumen = cara keputusan diambil, bukan cara sumber dibaca".
2. Steering D-14 ("ekstraksi penuh per-baris") saya salah tempatkan: seharusnya masuk BERKAS KERJA yang menyertai, bukan badan dokumen. Gerbang V-12 (baris lampiran == baris sumber) mengunci kekeliruan ini justru sebagai "kesuksesan".
3. Tidak ada pemeriksaan KESEGARAN KORPUS sebelum membekukan angka: exemplar memakai P-0003 Rev A (8-Sept) + tiga keputusan direktur yang mengubah baseline (113/234/355); korpus saya berhenti di 29-Jul. Data saya benar untuk zamannya, tapi kalah mutakhir.
4. Gerbang verifikasi saya mengukur BENAR (angka, hash, naturalisasi, desain) tapi tidak mengukur SUSUN (arsitektur informasi, kerapatan keputusan, routing pembaca, rel bukti). Tidak ada V-GATE "pemeriksa bisa menelusuri satu angka mana pun dalam <=2 langkah lewat register beku bersidik jari".

## 5. Aturan permanen yang dipasang (terpasang di skill gsp-knowledge-baseline-architecture)
R-01 MODEL-DULU: semua besaran lahir dari SATU rantai hitung beku (spine); angka naskah DIIKAT dari register, dilarang diketik; sidik jari register (sha16) dicetak di penutup dan dikutip dokumen turunan.
R-02 ORGANISASI-PER-SISTEM: bab disusun per subsistem/keputusan; dokumen sumber masuk bab SILSILAH, bukan jadi bab isi.
R-03 SATU DASAR LINGKUP: bab depan menetapkan dokumen dasar + alasan yang dapat diperiksa + tabel angka ditarik dari peredaran (lama|berlaku|alasan).
R-04 DATA-MENTAH=BERKAS-KERJA: ekstraksi per-baris disimpan sebagai berkas kerja menyertai (indeksnya di lampiran E); badan dokumen memuat model+register+keputusan.
R-05 REL BUKTI: setiap paragraf berangka memuat tanda asal (TERUKUR/DITURUNKAN/PEMASOK/ASUMSI) + sebarannya dihitung dan ditampilkan.
R-06 UJI DALAM DOKUMEN: rekonsiliasi dua rute side-by-side + lembar verifikasi akhir + daftar "yang TIDAK diperiksa alat".
R-07 TEMUAN AUDIT TERBIT: temuan cacat dokumen sumber (termasuk dokumen sendiri) tampil utuh di lampiran dengan kelas+dampak+tindakan.
R-08 ROUTING PEMBACA + Q&A PEMERIKSA wajib ada.
R-09 REVISI APPEND-ONLY + LEMBAR KENDALI berdampak (REV|APA|MENGAPA|DAMPAK).
R-10 KESEGARAN KORPUS: sebelum beku, wajib tanya/cek adanya edisi lebih baru + keputusan governance terbaru; vonis kedaluwarsa = blok.
R-11 GERBANG SUSUN (V-SUSUN): sebelum serah, uji arsitektur: traceability <=2 langkah, kerapatan (halaman keputusan vs halaman dump), routing, rel bukti, fingerprint. FAIL = kembalikan ke arsitektur, bukan tambal gejala.

## 6. Konsekuensi untuk artefak saat ini
Dokumen 219 hal yang sudah terbit AKURAT tapi SUSUNNYA di bawah standar exemplar. Remediasi = terbitan Rev B dengan arsitektur R-01..R-11 (badan ~70-80 hal per-subsistem + register beku + uji dua rute + temuan audit + penutup verifikasi), dump mentah turun menjadi berkas kerja menyertai. Menunggu persetujuan user (misi baru, estimasi ~2-3 jam dengan pipeline yang sudah ada).
