---
id: fiber-optic-korpus-ekas-0923
type: catatan
title: Korpus FIBER-OPTIC EKAS - peta, rumus, ambang, dan batas pengetahuan (NWSKILL-0923)
status: active
sumber: "docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md (hulu: 10 path wajib + 20 berkas pendukung ekas/ dan artefak, terdaftar di Bagian 1 objek)"
halaman: "marker [R-n, sumber, hal] per butir di body: PDF 129 dan 145 (Hayes FOA - loss budget, kolom terburuk; offset halaman tidak tetap +3 s.d. +10 = known-defect K-4); PDF 17, 14, 20, 43 (IEC 61280-4-2:2014 - empat metode, RTM, ketidakpastian, ORL Annex E); PDF 98 dan 120 (Hayes Bab 8-9); cetak 37 / PDF 44 (JDSU - jangkar atribusi diperdebatkan K-3); cetak 65 dan 89 / PDF 72 dan 96 (JDSU Bab 3-4)"
tanggal_akses: 2026-09-24
kelas_bukti: sintesis
sensitif: tidak
perkara: nwskill-0923
tags: [fiber-optic, serat-optik, loss-budget, otdr, olts, konektor, splice-fusi, singlemode, multimode, iec-61280, ofstp, fotp, tia-568, redaman, db-per-km, cable-plant]
links: [ekas/05_DOMAIN-KNOWLEDGE/FIBER-OPTIC, docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, ekas/05_DOMAIN-KNOWLEDGE/NETWORKING, faktas/waktu-deteksi-hilangnya-sinyal-video-tabel7-bsen-62676-1-2]
defek-terkait: "known-defect D2-FIXx 2026-09-24: 26 blok anotasi CATATAN DEFECT di 16 berkas lapis pakai EKAS (manifest docs/2026-09-23-nws-knowledge-register/fixekas/manifest_d2_20260924_135542.json; verifikasi BOCOR=0). Butir beban-rilis utama: ~550 m MM tanpa sumber (K-1), 5,96 dB @1550 tidak reproducible (K-2), atribusi 0,02-0,05 dB/hari FOA vs JDSU (K-3), ketegangan OTDR R2 vs R3 (K-11). Warisan: faktas/waktu-deteksi-hilangnya-sinyal-video-tabel7-bsen-62676-1-2.md ditandai known-defect oleh gsp-librarian 2026-09-23 (VSSKB-0923) - menempel pada lapis bersama yang dikutip objek ini (ASUMSI-BAKU, KATALOG-RUMUS)"
penulis: gsp-fiber-specialist
diajukan: 2026-09-24
domain: FIBER-OPTIC
created: 2026-09-24
catatan_verifikasi: "Verdict: terverifikasi oleh gsp-custodian pada 2026-09-24. Alasan: [1 metadata] yaml.safe_load LOLOS (17 kunci, nol duplikat), uji potong-# nol temuan, title == H1 persis, tepat satu baris status, tags == daftar beku G-1 seksi 4 byte-per-byte (16 token), id == pola seksi 5, domain FIBER-OPTIC dan defek-terkait terisi, sensitif tidak + perkara nwskill-0923 (bukan dosir; gate librarian tetap milik librarian). [2 provenans] 14 kelompok koordinat rak diuji langsung path:baris pada berkas nyata dan semuanya cocok: RANTAI-JAMINAN.md:25 (~550 m), :47-50 (1,0/0,5/0,75/0,1-0,3), :63-68 (6,40 dB), :73-74 (0,02-0,05 + [R3, JDSU]), :87-91 (FOTP-171/Annex E/RTM), :118-121 (status rantai UTUH + 61280-4-1); IEC resume :25-35/:58-65/:71-76/:97-104; FOA :7-10 (offset tidak tetap), :49-57 (tabel OM/OS), :71-83 (tabel rugi), :128-131 (ketidakpastian), :190-197 (contoh 2,2/5,6), :198-205 (nasihat PDF 145); JDSU :7-9 (offset tetap +7), :21-26 (peta bab), :51-53 (dead zone), grep dB = 0; REF-FO-001/002/003 :22/:24/:29/:40/:43-44; KATALOG-RUMUS :37-38/:59/:121/:128-129/:135/:146-147/:153-159/:150-151/:582; ASUMSI-BAKU :51-58/:139-154/:152; AMBANG-TERIMA-INDUK :42/:49/:61/:82/:85-97; README.md:34-38 (R1=0, R2=5, R3=24, R4=0, R5=8) dan :47; GAP-REGISTER.csv :11/:12/:15/:2; MASTER-REFERENCE-REGISTER.md:66; R4-STATUS.md:41 (baris konektor serat); TEMPLATE-BERITA-ACARA.md:62-80. [3 anti-karangan] sepuluh berkas sumber dibuka penuh, nol fabrikasi; empat _ISI laci dan PDF primer di gsp-ekas diukur sendiri (FOA 54.533.749 B; JDSU 6.416.581 B; IEC 1.588.640 B; find ekas -name '*.pdf' = 0). [4 kesetiaan hulu] K-1 sampai K-12 + Blok warisan Tabel 7 cocok ke studi (859 baris) termasuk vonis aritmetika: 6,40 @1310 cocok persis; 5,96 @1550 TIDAK reproduksibel (alpha sweep 5,60/5,76/5,92/6,08/6,40; alpha tersirat 0,3625 tidak ada di rak; brute force 1.120 kombinasi = 9 solusi terekap ulang); konvensi offset per buku cocok skema G-1 seksi 7. [5 anatomi] 8 bagian persis pola VSSKB; Bagian 8 memuat N-11 lengkap: status rantai D2 bersandar R2 IEC 61280-4-2 hanya singlemode, GAP-010/011/014/001, R1=0 dan R4=0, usia JDSU 19 th, R3 bukan ambang hukum + R2 butuh adopsi kontrak, P-8, warisan Tabel 7. [6 konsistensi] bentuk lama tidak dihapus (26 blok D2-FIXx di 16 berkas terukur dari disk; manifest 16 berkas/26 blok/+21.927 byte cocok); semua butir beban-rilis membawa predikat known-defect, kelas R2 vs R3 tidak diratakan. Temuan minor tanpa pengaruh verdict: (a) tally blok D2-FIXx K-3 di tabel Ringkasan predikat final Bagian 5 tertulis 7 blok, disk + manifest terukur 6 (total 26 tetap benar); (b) kalimat 'Sembilan dari dua belas menyentuh beban-rilis' keliru hitung, terukur 10 dari 12 - kalimat identik diwarisi dari studi (warisan hulu, bukan kesalahan objek); disarankan librarian koreksi keduanya saat kurasi. [7 kebersihan] non-ASCII = 0 byte, EOL LF utuh, nol jalur rak palsu (semua path di-probe nyata; label laci K-12 dinyatakan bukan path). Rekomendasi: layak dipromosikan oleh gsp-librarian setelah koreksi minor (a)-(b); predikat known-defect K-1/K-2/K-3 dan penanda BELUM TERKONFIRMASI wajib ikut terangkut ke wiki; verifikasi halaman tetap wewenang manusia dengan PDF primer."
catatan_keputusan: "dipromosikan: NWSKILL-0923 D2-L2: gerbang format librarian 10/10 PASS (validator mandiri + red-green 3 kelas cacat), verdict custodian terlampir di catatan_verifikasi, non-sensitif non-dosir; known-defect K-1..K-12 + warisan Tabel 7 ditandai berpredikat, beban-rilis bukan angka final"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-24
dipromosikan-ke: catatans/fiber-optic-korpus-ekas-0923.md
---

# Korpus FIBER-OPTIC EKAS - peta, rumus, ambang, dan batas pengetahuan (NWSKILL-0923)

Objek master misi NWSKILL-0923 (id `fiber-optic-korpus-ekas-0923`, type catatan, domain
FIBER-OPTIC = D2). Muatan = peta rak + rumus + angka acuan + kerangka hitung + ambang terima +
register kontradiksi + celah resmi + batas kemampuan, dalam satu berkas (granularitas SATU
objek master per domain sesuai skema beku G-1 seksi 1).

Provenans: body ini disalin terpadatkan dari SATU sumber,
`docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md` (studi
t_4d43fd1f status complete, 859 baris, ekstraksi read-only dari lapisan teks `ekas/` oleh
gsp-fiber-specialist pada 2026-09-24). Tidak ada pembacaan ulang korpus untuk angka BARU pada
giliran ini; bacaan langsung rak di giliran L1 hanya untuk (a) memverifikasi jangkar baris
pasca-tambalan D2-FIXx, (b) mengukur ulang ukuran berkas dan sha256 lapis bersama, (c)
menjalankan ulang uji aritmetika studi sebagai perintah pada giliran ini (Bagian 2.5), dan (d)
mengstat ulang PDF primer di vault nyata (Bagian 1.5). Semua 12 butir kontradiksi studi sudah
divonis dan ditambal anotasi D2-FIXx di rak; status finalnya disalin di Bagian 5.
Kelas bukti objek: sintesis - satu-satunya R2 metode uji nyata di rak domain mana pun
(IEC 61280-4-2) dipasangkan dengan dua resume R3 (Hayes/FOA, JDSU); R4 nihil by-design
(laci fiber kosong dan jujur). Kelas bukti berbeda dicampur dalam satu berkas; pemisahannya
ditegakkan lewat penanda `[R-n, sumber, hal]` per butir dan blok BATAS PENGETAHUAN di
Bagian 8. Yang tidak ada di rak dinyatakan "tidak ada di rak".

Konvensi tulis (diwarisi dari studi): saat mengutip lapis teks rak, glif pemisah diganti
("x" untuk kali, "<=" untuk kurang-dari-atau-sama, "log10" untuk subskrip, "/" untuk pemisah
daftar, "->" untuk panah); ANGKA, SATUAN, dan NAMA HALAMAN disalin PERSIS termasuk desimal
koma Indonesia. Substitusi hanya pada glif, tidak pernah pada nilai. Berkas ini ASCII penuh
(U+2014, U+2013, U+00B7, U+2022 = nol).

Catatan wewenang: tidak ada PDF primer yang dibuka pada misi ini. Semua vonis halaman adalah
vonis LAPISAN TEKS memakai aturan offset tiap buku; penutup akhir wewenang manusia.

Catatan nomor baris: berkas khusus domain FO (`RANTAI-JAMINAN.md`, tiga resume, tiga kartu)
dikutip pada nomor baris PASCA-tambalan D2-FIXx (stabil, diukur dua kali pada giliran ini).
Berkas bersama (`KATALOG-RUMUS.md`, `ASUMSI-BAKU.md`, `AMBANG-TERIMA-INDUK.md`, suite P00)
sedang ditambal paralel oleh kartu saudari D3-FIXx/D4-FIXx - nomor barisnya digeser
diberikan sebagai SNAPSHOT 2026-09-24 14:11 WIB dengan pengawet token (kutipan pendek yang
tetak ditemukan grep); bila token bergeser, token yang menang, bukan angka baris.

---

## Bagian 1 - Peta isi

Path memakai NAMA FOLDER NYATA di disk (kontrak jalur G-1 seksi 6). Label katalog berbentuk
`R3/FIBER-OPTIC/` dan `R2/IEC/` adalah label laci, BUKAN path; padanan nyatanya dicantumkan
(butir K-12). Uji keberadaan = baca langsung/ls, bukan glob.

### 1.1 Lapis domain `ekas/05_DOMAIN-KNOWLEDGE/FIBER-OPTIC/` (4 berkas, pasca-D2-FIXx)

| Berkas | Peran | Tingkat R | Ukuran nyata | Isi unik |
|---|---|---|---|---|
| `RANTAI-JAMINAN.md` | Rantai A lima mata: rujukan, keputusan desain, perhitungan, pengujian, bukti serah | peta pengetahuan | 9.571 B, 123 baris | satu-satunya angka ~550 m (`:25`, known-defect K-1); daftar 8 lampiran wajib serah (`:107-116`); status rantai UTUH (`:118-119`); pernyataan terbuka 61280-4-1 (`:121-123`) |
| `R2 - IEC 61280-4-2.md` | Resume standar IEC edisi 2.0 2014 | **R2** | 5.012 B, 104 baris | satu-satunya sumber R2 domain ini; empat metode uji redaman (`:25-35`); rumus Reflectance (`:58-65`); RTM (`:67-69`); ORL Annex E (`:71-76`); batas cakupan (`:97-104`) |
| `R3 - FOA Reference Guide to Fiber Optics.md` | Resume Hayes 2019 (CFOT) | R3 | 13.143 B, 247 baris | satu-satunya tabel jenis serat OM1-OM5/OS1-OS2 (`:49-57`); contoh terhitung 2 km dua kolom (`:190-197`); aturan offset tidak tetap (`:7-10`) |
| `R3 - Reference Guide to Fiber Optic Testing Vol 1.md` | Resume JDSU/Laferriere 2007 | R3 | 4.465 B, 99 baris | satu-satunya istilah dead zone (`:51-53`); aturan offset tetap +7 (`:7-9`); dispersi/PMD sebagai topik tanpa angka (`:63-67`) |

### 1.2 Lapis kartu `ekas/04_KNOWLEDGE-CARDS/FIBER-OPTIC/` (3 kartu, templat enam seksi identik)

| Kartu | R | Yang dipasok (`:22`) | Halaman jangkar (`:24`) | Boleh tetapkan ambang (`:37`/`:40`) | Batas pemakaian (`:41`/`:44`) |
|---|---|---|---|---|---|
| `REF-FO-001.md` (61 baris, 2.416 B) | R3 | loss budget, batas TIA-568 0,75 dB/konektor, 1 dB/km SM premises, 0,5 dB/km OSP, ambang = kolom terburuk | PDF 98, 129, 145 | TIDAK sendirian; hanya bila kontrak mengadopsi tertulis | OTDR bukan pengganti uji rugi OLTS (`:41`; sisi R2-nya = K-11, anotasi `:43-44`) |
| `REF-FO-002.md` (61 baris, 2.455 B) | R3 | OTDR, ketidakpastian ukur lab 0,02-0,05 dB/hari | cetak 37 / PDF 44 | TIDAK sendirian | terbit 2007, periksa rujukan standarnya (`:44`); atribusi butir ketidakpastian = K-3, anotasi `:26-27` |
| `REF-FO-003.md` (61 baris, 2.585 B) | **R2** | empat metode one-cord/three-cord/two-cord/OTDR, RTM, ORL Annex E Method A | PDF 14, 17, 20, 43 | **Ya**, bila standar diadopsi kontrak dan edisinya tervalidasi (`:40`) | Singlemode saja; multimode ke IEC 61280-4-1; tidak memberi angka ambang (`:44`); rumus reflektansi tanpa pembatas cakupan = K-9, anotasi `:32-33` |

Hanya `REF-FO-003` (R2) yang kartunya mengizinkan penetapan ambang, dan itu pun bersyarat
adopsi kontrak. Dua kartu R3 dilarang berdiri sendiri. Struktur ini BEDA dari domain
NETWORKING yang tidak punya kartu R2 sama sekali.

### 1.3 Lapis bersama (baris terkait serat optik; snapshot 2026-09-24 14:11, drift aktif)

| Lapis (ukuran snapshot) | Jangkar baris + token | Isi |
|---|---|---|
| `ekas/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md` (30.272 B, 599 baris) | `:37` "rugi serat + rugi konektor + rugi sambungan"; `:38` "Hasil loss budget kolom terburuk"; `:59` "Metode uji redaman serat singlemode" | indeks cepat: rugi total jalur [R3, Hayes FOA Reference Guide, PDF 129]; ambang lulus [R3, Hayes FOA Reference Guide, PDF 145]; metode uji SM [R2, IEC 61280-4-2:2014, PDF 17] |
| idem | seksi "## 2. Serat optik" `:113-159` | rumus `:121`; tabel rugi serat `:124-129`; tabel rugi konektor `:131-136`; aturan kolom terburuk `:141-142`; ambang uji dan ketelitian `:144-148`; tabel standar metode uji `:153-159`. TANPA baris rugi sambungan (K-5, anotasi `:138-139`); baris ketidakpastian tanpa atribusi buku (K-3, anotasi `:150-151`) |
| idem | seksi "### 13.3 IEC 61280-4-2:2014" (sekitar `:502-510`) | empat metode; "Tiga pertama memakai LSPM"; reflektansi + RTM + ORL; sumber ketidakpastian; anotasi K-11 dan K-9 |
| idem | token "Peta resume" (sekitar `:570-577`) | indeks resume lama memakai nama `RESUME - FOA ...` dan `RESUME - Reference ...` yang tidak sama dengan berkas nyata (K-12, beranotasi) |
| `ekas/06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md` (10.523 B, 184 baris) | seksi "### B. Serat optik" `:51-58` | rugi sambungan `:55` TANPA angka; redaman serat `:56` "pakai batas standar, bukan angka terbaik pabrikan"; jumlah konektor `:57` "tiap patch panel = sepasang"; anggaran daya perangkat `:58` "lembar data transceiver"; anotasi K-5 `:60-61` |
| idem | seksi "Asumsi yang GUGUR" `:139-154` | `:154` metode uji redaman SM kini dikutip dari IEC 61280-4-2 PDF 17, bukan ditaksir; `:152` anotasi defect warisan VSSKB Tabel 7 |
| `ekas/07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/AMBANG-TERIMA-INDUK.md` (7.595 B, 111 baris) | `:42` "Rugi jalur serat optik"; `:61` kabel referensi; `:82` multimode; `:94` dan `:96` wajib R4 | rinci di Bagian 4.1; aturan induk `:49` token "Metode boleh R3" |
| `ekas/00_START-HERE/README.md` (4.112 B, 99 baris) | `:34-38` | keadaan rak R1=0, R2=5, R3=24, R4=0, R5=8; alasan R4 by-design `:47` |
| `ekas/02_REGISTERS/GAP-REGISTER.csv` (3.228 B, 23 baris) | `:11` GAP-010; `:12` GAP-011; `:15` GAP-014; `:2` GAP-001 | Bagian 6.1 |
| `ekas/02_REGISTERS/R4-STATUS.md` (3.992 B, 80 baris) | `:41` | "Redaman & reflektansi konektor terpasang - tidak ada lembar data konektor/kabel serat" |
| `ekas/02_REGISTERS/MASTER-REFERENCE-REGISTER.md` (8.815 B, 153 baris) | `:66` | peringatan usia JDSU "19 th" |
| `ekas/07_VERIFICATION-VALIDATION/TEST-PROCEDURES/TEMPLATE-BERITA-ACARA.md` (12.689 B, 270 baris) | seksi "## 1. Uji jalur serat optik" `:62-80` | kerangka BA serat optik: ambang + sumber, metode OFSTP/FOTP, alat, ketidakpastian, data jalur, kabel referensi <= 0,5 dB, setelan OTDR |
| `ekas/08_EVIDENCE/OTDR/README.md` (163 B, 8 baris) | seluruh berkas | laci bukti OTDR kosong - diisi per proyek |

### 1.4 Lapis pelaksanaan (suite contoh P00, tujuh berkas; SEMUA angkanya berlabel "karangan")

Domain ini satu-satunya (bersama pembumian) yang punya rantai contoh end-to-end di rak,
sehingga BENUK artefak ikut menjadi pengetahuan. Berkas berlabel P00 membawa peringatan
"seluruh angka di berkas ini karangan" - dipakai di sini sebagai artefak bentuk, selalu
ditandai `(P00, angka karangan)`.

| Berkas (ukuran snapshot) | Peran gate | Isi terukur |
|---|---|---|
| `DDR-P00-001.md` (1.812 B, 51 baris) | G2 | keputusan 6 sambungan fusi batas gulungan 500 m (`:19-20`); alternatif 3 sambungan hemat 0,9 dB ditolak (`:38`); alternatif 10 sambungan +1,2 dB ditolak (`:39`); rujukan per halaman REF-FO-001 PDF 129/145 + REF-FO-003 PDF 17 (`:30-32`); "Konflik antar-sumber: Tidak ada." (`:42-44`) - tidak akurat utk ambang 1550 milik CALC-nya sendiri (K-2) |
| `CALC-P00-001.md` (3.609 B, 75 baris) | G3 | masukan bertag `:29-36` (rugi_sambungan 0,3 dB ditag ASSUMPTION `:36`); hasil 6,40 dB `:40-46`; ambang 1550 = 5,96 dB `:48` INDUK K-2 (anotasi `:50-51`); kepekaan 5,50/7,30/7,60 `:55-59`; dominasi konektor 3,00 dari 6,40 dB `:61-62`; G3 belum tertutup `:73` |
| `KARTU-P00-001.md` (5.586 B, 82 baris) | G3 | salinan CALC + status rantai PUTUS di mata 3 (`:29,:53,:67,:75`); gerbang peringatan usia >15 th (`:27`); anotasi K-2 setingkat berkas `:80-81` |
| `ITP-P00.md` (2.649 B, 32 baris) | G4 | butir 2 kabel referensi <= 0,5 dB (`:14`); butir 3 <= 6,40 dB (`:15`); butir 4 <= 5,96 dB (`:16`, anotasi `:21-22`); butir 5 kriteria OTDR kualitatif (`:17`); butir 6 rugi sambungan OTDR menggantikan asumsi 0,3 dB (`:18`); prasyarat 3 belum terpenuhi (`:24-31`) |
| `TEST-P00-001.md` (2.831 B, 66 baris) | G4 | metode dua ujung one-cord reference [R2, IEC 61280-4-2:2014, PDF 17] (`:19-23`); ambang + kotak centang adopsi kontrak pasal 7.3 (`:34-40`, anotasi `:41-42`); langkah 1-6 (`:50-55`) |
| `BA-P00-FO-001.md` (3.204 B, 78 baris) | G5-G6 | ambang per lambda + asal + rincian (`:23-29`, anotasi `:31-32`); setelan OTDR (`:51`); catatan ketidakpastian dekat ambang (`:60-63`) |
| `TEMUAN-UJI-COBA-P00.md` (6.367 B, 127 baris) | meta | temuan dua ambang per lambda (`:45`, anotasi `:48-49`); penandaan ASSUMPTION memicu kepekaan yang mengungkap dominasi konektor (`:84-88`) |

### 1.5 Lapis laci sumber (keberadaan fisik; dua lokasi wajib disebut - pelajaran K-8)

| Laci teks di `ekas/` | Klaim `_ISI.md` | PDF nyata (ukur ulang giliran L1, 2026-09-24) |
|---|---|---|
| `ekas/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/FIBER-OPTIC/_ISI.md` (1.266 B) | `:3` "Berkas fisik sudah berada di laci ini" - SALAH ALAMAT (K-8, dianotasi `:10`) | `C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/FIBER-OPTIC/`: Hayes FOA 54.533.749 B; Laferriere/JDSU Vol 1 6.416.581 B |
| `ekas/03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/IEC/_ISI.md` (1.040 B) | `:3` klaim sama (K-8, dianotasi `:9`) | `.../R2_INTERNATIONAL-STANDARDS/IEC/IEC 61280-4-2 ... (Edition 2.0, 2014).pdf` 1.588.640 B |
| `ekas/03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/TIA/_ISI.md` (251 B) | `:3` "Kosong." - jujur, konsisten | 0 (konfirmasi independen GAP-011) |
| `ekas/03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/ITU-T/_ISI.md` (253 B) | `:3` "Kosong." | 0 (G.652 tidak ada - G-9) |

Sapuan `find ekas -name '*.pdf'` = 0 hasil untuk seluruh pohon (diukur ulang pada giliran
tambal D2-FIXx dan dikonfirmasi lagi oleh studi). Verifier ground-truth JANGAN mencari PDF di
`ekas/` - pengetahuan tetap sah, alamat buktinya yang salah (K-8).

### 1.6 Batas domain: FIBER-OPTIC vs NETWORKING (garis yang wajib dijaga)

| Masuk FIBER-OPTIC (D2) | Masuk NETWORKING (D1) |
|---|---|
| Kabel plant fisik: serat, kabel, konektor, sambungan fusi/mekanis, patch panel | LAN aktif: switch, router, VLAN, PoE, alamat IP |
| Loss budget per lambda; rugi serat/konektor/splice; ambang = kolom terburuk | Lebar pita agregat, BDP, window scaling, throughput |
| Uji redaman/ORL: OLTS/LSPM, OTDR, FOTP-171, OFSTP-7/14, IEC 61280-4-2, RTM | Uji cabut kabel, pengukuran pada switch/uplink |
| Berita acara uji per core + jejak `.sor` + setelan OTDR | Cadangan konfigurasi, versi firmware, catatan perubahan |

Serat optik adalah MEDIA FISIK yang menopang jaringan; kepemilikan angkanya terpisah tegas:
0,75 dB dan 1 dB/km milik D2 (via Hayes), anggaran PoE dan 240 Mb/s milik D1. Materi D1
hanya dirujuk silang, TIDAK disalin (putusan P-8): `ekas/05_DOMAIN-KNOWLEDGE/NETWORKING/`.
Titik temu sah: kontrak sering menuntut "jalur fiber lulus uji OFSTP" SEBELUM perangkat aktif
D1 dipasang - urutan itu adalah tautan antar-domain, bukan tumpang tindih angka.

### 1.7 Lapis skill terpasang (untuk K-7)

Skill `fiber-link-design` terpasang identik di tiga lokasi (md5 terverifikasi studi):
SKILL.md 73 baris + `references/01-loss-budget-dan-uji.md` 55 baris = 128 baris, 1 referensi.
Klaim `CHANGELOG.md:197` menyebut "3 referensi - 377 baris" - lihat K-7.

---

## Bagian 2 - Rumus dan angka acuan

Setiap rumus dan angka membawa penanda sumbernya sendiri bentuk koma `[R-n, sumber, hal]`.
Jangan memakai ulang satu butir tanpa penandanya. Jalur baris merujuk lapis teks rak relatif
shared workspace (berkas domain FO = pasca-D2-FIXx).

### 2.1 Rumus inti domain

```
Loss budget = (panjang_km x rugi_per_km) + (n_konektor x rugi_konektor)
                                          + (n_sambungan x rugi_sambungan)
```
[R3, Hayes FOA Reference Guide, PDF 129] - `RANTAI-JAMINAN.md:40-43`; salinan identik di
`R3 - FOA Reference Guide to Fiber Optics.md:167` (bentuk ringkas "Total rugi (dB) = rugi
serat + rugi konektor + rugi sambungan"), `KATALOG-RUMUS.md:121` dan `:37`,
`CALC-P00-001.md:20-23`, skill `references/01-loss-budget-dan-uji.md`.

```
Ambang lulus = total rugi KOLOM TERBURUK (bukan tipikal, bukan rata-rata)
```
[R3, Hayes FOA Reference Guide, PDF 145] - `RANTAI-JAMINAN.md:56-57`;
`R3 - FOA Reference Guide to Fiber Optics.md:87-89,199-205`; `KATALOG-RUMUS.md:38,141-142`;
`AMBANG-TERIMA-INDUK.md:42` (token "Rugi jalur serat optik"); `REF-FO-001.md:22`;
`DDR-P00-001.md:31`; `BA-P00-FO-001.md:25`. Aturan pembukunya: "bersikaplah konservatif.
Jangan memakai spesifikasi terbaik untuk redaman serat maupun rugi konektor - sisakan margin
untuk pelaksanaan dan penurunan mutu komponen seiring waktu" [R3, Hayes FOA Reference Guide,
PDF 145].

```
Reflectance = 10 x log10 (Pr / Pin)
```
[R2, IEC 61280-4-2:2014, PDF 14] - `R2 - IEC 61280-4-2.md:58-65` (Pr = daya balik yang
dipantulkan komponen, Pin = daya masuk); `REF-FO-003.md:29`; `KATALOG-RUMUS.md` seksi 13.3.
PEMBATAS CAKUPAN YANG WAJIB IKUT: definisi ini untuk KOMPONEN DISKRET DALAM KABEL, bukan
untuk ORL jalur utuh (`R2 - IEC 61280-4-2.md:60` "Untuk komponen diskret dalam kabel");
hubungan arah tanda reflectance (dB negatif) vs ORL (dB positif) TIDAK dijelaskan satu lapis
teks pun - lihat K-9.

```
Pemilihan metode uji menentukan konektor ujung mana yang ikut terukur
```
[R2, IEC 61280-4-2:2014, PDF 17] - `R2 - IEC 61280-4-2.md:43-45`; dieksekusi di
`TEST-P00-001.md:22`. Ini aturan prosedural dan ia alasan butir BA "nama metode" wajib
disebut, bukan hanya nama alatnya.

```
Bandingkan loss budget terhadap anggaran daya perangkat (daya kirim - sensitivitas terima)
```
[R3, Hayes FOA Reference Guide, PDF 129 dst.] - `R3 - FOA Reference Guide to Fiber Optics.md:91-93,199-200`;
`ASUMSI-BAKU.md:58`. ANGGKA NYATA TIDAK ADA DI RAK: kerangka saja; selisih daya sebagai margin
hanya dicetak di skill, tidak di lapis teks EKAS mana pun (gap G-4; wajib R4).

### 2.2 Angka acuan per sumber (salinan persis + predikat)

Rugi serat dan rugi komponen:

| Angka | Nilai persis di rak | Penanda + jalur | Predikat |
|---|---|---|---|
| Rugi serat SM premises | 1,0 dB/km (maksimum EIA/TIA 568) | [R3, Hayes FOA Reference Guide, PDF 129] - `RANTAI-JAMINAN.md:47`; `R3 - FOA ...:73,176`; `KATALOG-RUMUS.md:128`; `REF-FO-001.md:22` | sah dengan adopsi kontrak (kartu R3) |
| Rugi serat SM outside plant | 0,5 dB/km | [R3, Hayes FOA Reference Guide, PDF 129] - `RANTAI-JAMINAN.md:48`; `R3 - FOA ...:73,176`; `KATALOG-RUMUS.md:128` | idem |
| Rugi serat SM tipikal 1310 nm | 0,4 dB/km | [R3, Hayes FOA Reference Guide, PDF 129 dst.] - `R3 - FOA ...:73,176`; `KATALOG-RUMUS.md:128` | tipikal - JANGAN dipakai memutuskan |
| Rugi serat SM tipikal 1550 nm | 0,3 dB/km | [R3, Hayes FOA Reference Guide, PDF 129 dst.] - `R3 - FOA ...:74,177`; `KATALOG-RUMUS.md:129` | idem |
| Rugi OS1/OS2 per spesifikasi | 0,4 @1310 / 0,25 @1550 | [R3, Hayes FOA Reference Guide, PDF 98 dst.] - `R3 - FOA ...:56` (tabel jenis serat; G.652; OS2 low water peak) | spesifikasi jenis; dokumen G.652 tidak di rak (G-9) |
| Rugi serat MM 850 nm | tipikal 3 dB/km, maksimum 3,5 dB/km | [R3, Hayes FOA Reference Guide, PDF 129 dst.] - `R3 - FOA ...:71,174`; `KATALOG-RUMUS.md:126` | sah; metode ujinya bersandar OFSTP-14 (GAP-010) |
| Rugi serat MM 1300 nm | tipikal 1 dB/km, maksimum 1,5 dB/km | [R3, Hayes FOA Reference Guide, PDF 129 dst.] - `R3 - FOA ...:72,175`; `KATALOG-RUMUS.md:127` | idem |
| Rugi konektor (batas TIA-568) | 0,75 dB | [R3, Hayes FOA Reference Guide, PDF 129] - `RANTAI-JAMINAN.md:49`; `R3 - FOA ...:82,185`; `KATALOG-RUMUS.md:135`; `REF-FO-001.md:22,29`; `CALC-P00-001.md:34` | status riilnya "batas TIA menurut Hayes" - dokumen TIA-568 tidak di rak (GAP-011/G-2) |
| Konektor MM | 0,2-0,5 dB tipikal | [R3, Hayes FOA Reference Guide, PDF 129] - `R3 - FOA ...:80,183`; `KATALOG-RUMUS.md:133` | tipikal |
| Konektor SM pabrikan / pigtail fusion | 0,3 dB tipikal | [R3, Hayes FOA Reference Guide, PDF 129] - `R3 - FOA ...:81,184`; `KATALOG-RUMUS.md:134` | tipikal |
| Konektor SM terminasi lapangan | 0,5-1,0 dB | [R3, Hayes FOA Reference Guide, PDF 129] - `R3 - FOA ...:83,186`; `KATALOG-RUMUS.md:136` | - |
| Rugi sambungan fusi | 0,1-0,3 dB (R4 bila alat menyebut lain) | [R3, peta rantai, FIBER-OPTIC/RANTAI-JAMINAN.md:50]; skill ref | KNOWN-DEFECT K-5: hilang dari KATALOG seksi 2 dan ASUMSI-BAKU; satu-satunya pemakaian contoh ditag ASSUMPTION |
| Rugi kabel referensi | rugi > 0,5 dB patut dipertanyakan; syarat BA <= 0,5 dB | [R3, Hayes FOA Reference Guide, PDF 98 dst.] - `RANTAI-JAMINAN.md:88`; `R3 - FOA ...:125-126,210-211`; `KATALOG-RUMUS.md:146`; `AMBANG-TERIMA-INDUK.md:61` (perlu adopsi kontrak); `TEMPLATE-BERITA-ACARA.md:77`; `ITP-P00.md:14` | sah dengan adopsi kontrak |
| Ketidakpastian ukur lab | 0,02-0,05 dB/hari, lapangan lebih besar | [R3, Hayes FOA Reference Guide, PDF 98 dst.] - `R3 - FOA ...:128-131,213-214`; `RANTAI-JAMINAN.md:71-74`; `KATALOG-RUMUS.md:147`; `REF-FO-002.md:22`; `TEMPLATE-BERITA-ACARA.md:72`; `TEST-P00-001.md:57-58`; `BA-P00-FO-001.md:60-63` | ANGKA SAH, ATRIBUSI DIPERDEBATKAN (K-3): dicetak di resume FOA, disandarkan ke JDSU oleh rantai+kartu+skill; jangan menulis sumbernya sebagai JDSU sampai manusia buka PDF |
| Batas jarak MM | "MM ditolak di atas ~550 m - batas jarak pada laju tinggi" | [peta rak, FIBER-OPTIC/RANTAI-JAMINAN.md:25] SAJA - tanpa penanda R, kolom Tingkat kosong | KNOWN-DEFECT K-1: nol padanan di FOA/JDSU/register (sapuan 6 kueri); DILARANG dipakai sebagai batas final; keputusan controller apakah naik atau tidak |
| Lebar pita MM | OM1 160/500; OM2 500/500; OM3 2000/500; OM4 3600/500; OM5 3600/500 MHz-km | [R3, Hayes FOA Reference Guide, PDF 98 dst.] - `R3 - FOA ...:51-55` | OM5 vs OM4 tanpa pembeda terukur (K-10, calon) |
| Ukuran inti/kelongsong | OM1 62,5/125; OM2-OM5 50/125; OS1/OS2 9/125; 100/140 usang (3/1; 150/300 MHz-km) | [R3, Hayes FOA Reference Guide, PDF 98 dst.] - `R3 - FOA ...:51-57` | - |
| Redaman MM tabel jenis | 3 @850 / 1 @1300 untuk OM1-OM5 | [R3, Hayes FOA Reference Guide, PDF 98 dst.] - `R3 - FOA ...:51-55` | - |

Metode dan standar uji:

| Butir | Nilai persis di rak | Penanda + jalur |
|---|---|---|
| Empat metode uji redaman SM | One-cord reference (satu test cord); Three-cord (tiga); Two-cord (dua); OTDR method | [R2, IEC 61280-4-2:2014, PDF 17] - `R2 - IEC 61280-4-2.md:25-35`; `RANTAI-JAMINAN.md:86`; `REF-FO-003.md:22`; `KATALOG-RUMUS.md` seksi 13.3 |
| Alat tiga metode pertama | LSPM (optical light source and power meter) mengukur daya masuk dan keluar | [R2, IEC 61280-4-2:2014, PDF 17] - `R2 - IEC 61280-4-2.md:37-38` |
| RTM | metode uji yang dipakai untuk menyelesaikan perselisihan | [R2, IEC 61280-4-2:2014, PDF 14] - `R2 - IEC 61280-4-2.md:67-69`; `RANTAI-JAMINAN.md:91` |
| ORL | Annex E Method A, gelombang kontinu, normatif, paling dekat definisi 3.1.7, dengan faktor koreksi redaman internal perangkat pencabang | [R2, IEC 61280-4-2:2014, PDF 43] - `R2 - IEC 61280-4-2.md:71-76`; `RANTAI-JAMINAN.md:90` |
| Sumber ketidakpastian utama | sambungan kabel terminasi ke alat uji; penanganan = terminasi kelas referensi | [R2, IEC 61280-4-2:2014, PDF 20] - `R2 - IEC 61280-4-2.md:47-53`; `RANTAI-JAMINAN.md:96-98` |
| Uji satu ujung | single-ended loss / patchcord test = FOTP-171 | [R3, Hayes FOA Reference Guide, PDF 98] - `R3 - FOA ...:115-123`; `KATALOG-RUMUS.md:157`; `TEMPLATE-BERITA-ACARA.md:70` |
| Uji dua ujung | double-ended loss / installed cable plant = OFSTP-14 (multimode) / OFSTP-7 (singlemode) | [R3, Hayes FOA Reference Guide, PDF 98] - `R3 - FOA ...:115-123`; `RANTAI-JAMINAN.md:85`; `KATALOG-RUMUS.md:158-159` |
| Alat wajib rugi | LSPM/OLTS "Diwajibkan seluruh standar internasional"; OTDR pelengkap, bukan pengganti | [R3, Hayes FOA Reference Guide, PDF 98] - `R3 - FOA ...:104-110`; `RANTAI-JAMINAN.md:87,100-101`; `REF-FO-001.md:41`; `TEMPLATE-BERITA-ACARA.md:71`. KETEGANGAN dengan metode OTDR IEC = K-11, simpan kedua sisi |
| Wajib diuji tiap serat | 1 kontinuitas & polaritas; 2 rugi sisipan ujung-ke-ujung; 3 penelusuran gangguan bila ada temuan; 4 verifikasi tiap sambungan OSP dengan OTDR | [R3, Hayes FOA Reference Guide, PDF 98 dst.] - `R3 - FOA ...:97-102` |
| Batasan OTDR | resolusi jarak terbatas (sulit di premises); ghost pada kabel pendek; derau naik di kabel panjang; pulsa lebar + averaging menambah jangkauan; jangan pakai autotest; selalu launch cable panjang | [R3, Hayes FOA Reference Guide, PDF 120 dst.] - `R3 - FOA ...:136-149`; dead zone [R3, JDSU/Laferriere, cetak 65 / PDF 72] - `R3 - Reference Guide to Fiber Optic Testing Vol 1.md:51-53`; peringatan autotest sejalan (`:60-61`) |
| Setelan OTDR wajib dicatat | lambda, lebar pulsa, rentang, averaging, indeks bias, panjang launch dan receive cable | [peta rak] `TEMPLATE-BERITA-ACARA.md:79-80`; `RANTAI-JAMINAN.md:114`; `BA-P00-FO-001.md:51` - tanpa itu jejak tidak dapat ditafsirkan ulang |

Identitas berkas dan konvensi halaman (dasar uji offset, K-4):

| Butir | Nilai persis | Jalur |
|---|---|---|
| Hayes FOA 2019 | 214 halaman, 52,0 MB; OCR Tesseract 452.500 karakter, seluruh 214 halaman bertext; halaman gambar 123 dpi; bookmark bab 14 entri | `R3 - FOA ...:4,241-244` |
| Offset halaman Hayes | TIDAK TETAP: melebar dari +3 di bagian depan sampai +10 di apendiks; seluruh rujukan memakai nomor PDF | `R3 - FOA ...:7-10` - known-defect K-4 untuk klaim halaman cetak |
| Peta bab Hayes | Preface 4; Bab 1 6; 2 15; 3 24; 4 32; 5 45; 6 62; 7 76; 8 98; 9 129; 10 160; A 203; B 206; C 208 | `R3 - FOA ...:20-35` |
| JDSU 2007 | 146 halaman, 6,1 MB; bookmark 89 entri (4 bab + 20 sub-bab + 65 sub-sub-bab) dipasang 19 Agu 2026 | `R3 - Reference Guide ...:4,8,95` |
| Offset halaman JDSU | TETAP +7: cetak + 7 = PDF (cetak 1 = PDF 8) | `R3 - Reference Guide ...:7-8` - lolos uji internal 7/7 (Bagian 2.5) |
| Peta bab JDSU | Bab 1 cetak 1/PDF 8; Bab 2 cetak 37/PDF 44; Bab 3 cetak 65/PDF 72; Bab 4 cetak 89/PDF 96 | `R3 - Reference Guide ...:21-26` |
| IEC 61280-4-2:2014 | edisi 2.0, terbit Juni 2014; 162 halaman, 1,5 MB; dwibahasa Inggris-Prancis sehingga "sebenarnya +/- 80 halaman isi"; bookmark 440 entri; rujukan nomor PDF | `R2 - IEC 61280-4-2.md:3-10,103-104` |
| Usia JDSU | terbit 2007; MRR menandai peringatan usia "19 th" (2026-2007=19 terverifikasi) | `MASTER-REFERENCE-REGISTER.md:66`; `REF-FO-002.md:44` |

### 2.3 Standar uji dan kelasnya (jangan diratakan)

| Standar | Kelas R | Peran | Status di rak |
|---|---|---|---|
| IEC 61280-4-2:2014 edisi 2.0 | R2 | empat metode uji redaman SM, RTM, ORL | ADA (resume + PDF di vault nyata). Tidak memberi angka ambang lulus; hanya singlemode; hanya redaman dan ORL (`R2 - IEC 61280-4-2.md:97-104`) |
| IEC 61280-4-1 | R2 | padanan multimode | TIDAK ADA (GAP-010) - metode MM bersandar OFSTP-14 [R3] dan itu WAJIB dinyatakan bila kontrak menuntut acuan IEC (`RANTAI-JAMINAN.md:121-123`) |
| TIA-568 | R2 | sumber asli batas 0,75 dB dan 1 dB/km | TIDAK ADA (GAP-011) - angka hidup hanya sebagai kutipan R3 Hayes; lapis yang menyatakan lain = defect |
| FOTP-171 / OFSTP-7 / OFSTP-14 | R3 (sebutan) | metode Amerika satu/dua ujung | HANYA NAMANYA ditranskripsikan; dokumen tidak ada (G-3) |
| Hayes FOA Reference Guide 2019 | R3 | rumus loss budget, batas komponen, praktik | ADA (resume; PDF di gsp-ekas/lengkap) |
| JDSU FO Testing Vol 1 2007 | R3 | OTDR, dead zone, dispersi | ADA (resume; PDF di gsp-ekas/lengkap); panduan produk pabrikan 2007 - periksa rujukan standarnya |

### 2.4 Batas pemakaian lintas angka

- Jangan memakai spesifikasi terbaik; kolom terburuk yang memutuskan
  [R3, Hayes FOA Reference Guide, PDF 145].
- Jangan menetapkan toleransi lulus lebih ketat daripada ketelitian alat; ambang
  "maksimum 0,01 dB" tidak dapat dipertanggungjawabkan (`RANTAI-JAMINAN.md:71-74`;
  `R3 - FOA ...:130-131,213-214`).
- Hasil dalam plus-minus ketidakpastian dari ambang dilaporkan APA ADANYA, tidak dibulatkan
  ke arah lulus (`BA-P00-FO-001.md:60-63`).
- Tiap patch panel dihitung sepasang konektor (`ASUMSI-BAKU.md:57`).

### 2.5 Uji aritmetika deterministik (dijalankan ulang sebagai perintah Python pada giliran L1 ini)

Skrip `validator_fo_object.py` (giliran t_149b0608) mencetak semua baris di bawah; kolom
"hasil ukur" adalah keluaran alat pada giliran ini, cocok dengan cetakan giliran studi.

| Uji | Hasil ukur | Klaim rak | Vonis |
|---|---|---|---|
| `3.2*0.5 + 4*0.75 + 6*0.3` | 6.4 | ambang lulus 6,40 dB @1310 (`RANTAI-JAMINAN.md:63-68`; `CALC-P00-001.md:40-46`) | cocok persis |
| `2*0.4 + 4*0.3 + 2*0.1` | 2.2 | total tipikal 2,2 dB (`R3 - FOA ...:192-197`) | cocok persis |
| `2*1.0 + 4*0.75 + 2*0.3` | 5.6 | total terburuk 5,6 dB (idem) | cocok persis |
| `3.2*0.5 + 4*0.75 + 6*0.15` | 5.5 | kepekaan 5,50 dB (`CALC-P00-001.md:57`) | cocok persis |
| `3.2*0.5 + 4*0.75 + 6*0.45` | 7.3 | kepekaan 7,30 dB (`:58`) | cocok persis |
| `3.2*0.5 + 4*0.75 + 10*0.3` | 7.6 | kepekaan n=10 -> 7,60 dB (`:59`) | cocok persis |
| `3*0.3` ; `4*0.3` | 0.9 ; 1.2 | DDR: hemat 0,9 dB / tambah 1,2 dB (`DDR-P00-001.md:38-39`) | cocok persis (6,40+1,2=7,60 konsisten) |
| `3.2*a + 3.00 + 1.80` untuk a di {0,25; 0,3; 0,35; 0,4; 0,5} | 5.6 ; 5.76 ; 5.92 ; 6.08 ; 6.4 | ambang 1550 = 5,96 dB (`CALC-P00-001.md:48`) | TIDAK ADA alpha rak yang menghasilkan 5,96; alpha tersirat = 0,3625 dB/km - K-2 |
| brute force 8 alpha x 5 rugi konektor x 7 rugi sambungan x 4 jumlah konektor x 4 jumlah sambungan, L=3,2 (giliran studi) | 9 kombinasi mencapai 5,96; semuanya butuh n_sambungan 8/10 atau rugi konektor 0,5/1,0 | idem | 5,96 tidak reproducible dari himpunan masukan tercatat |
| Selisih cetak->PDF 7 pasangan JDSU (1,13,21,32,37,65,89) | +7 pada 7/7 | aturan tetap +7 (`R3 - Reference Guide ...:7-8`) | konsisten internal sempurna |
| Pasangan cetak/PDF Hayes | 0 pasangan tersedia di lapis teks | offset tidak tetap +3..+10 | tidak dapat diuji internal - K-4 |
| `4+20+65` | 89 | bookmark 89 entri (`R3 - Reference Guide ...:8,95`) | cocok persis |
| `2026-2007` | 19 | peringatan usia "19 th" (`MASTER-REFERENCE-REGISTER.md:66`) | cocok persis |
| `find ekas -name '*.pdf'` | 0 berkas | klaim `_ISI.md` "sudah berada di laci ini" | TIDAK cocok - K-8 |
| `wc -l` skill fiber-link-design | 73 + 55 = 128 baris, 1 referensi | CHANGELOG "3 referensi - 377 baris" (`CHANGELOG.md:197`) | TIDAK cocok - K-7 |

---

## Bagian 3 - Kerangka hitung terapan

### 3.1 Urutan kerja yang rak tetapkan (tidak boleh dibalik)

```
(1) RUJUKAN (R1-R5) -> (2) KEPUTUSAN DESAIN -> (3) PERHITUNGAN (loss budget + asumsi)
  -> (4) PENGUJIAN (metode + ambang) -> (5) BUKTI SERAH (BA + lampiran)
```
[peta rak, FIBER-OPTIC/RANTAI-JAMINAN.md mata 1 sampai 5]

Kunci kekuatan domain ini: **ambang mata (4) bukan angka standar, melainkan keluaran mata
(3)** (`RANTAI-JAMINAN.md:3,89`; `AMBANG-TERIMA-INDUK.md:35-42`). Konsekuensi gate: G4 tidak
dapat ditutup selama G3 terbuka bila ambang berasal dari hitungan sendiri - dibuktikan
operasional oleh `ITP-P00.md:24-31` (prasyarat ketiga belum terpenuhi) dan
`KARTU-P00-001.md:29` (rantai PUTUS di mata 3).

Keputusan yang paling menentukan biaya: **jumlah sambungan** (`RANTAI-JAMINAN.md:33-34`) -
masuk langsung ke mata (3) dan memutuskan lulus/tidak di mata (4). Ironi terukur contoh P00:
yang justru mendominasi anggaran adalah **konektor** (3,00 dB dari 6,40 dB)
(`CALC-P00-001.md:61-62`; `TEMUAN-UJI-COBA-P00.md:84-88`).

### 3.2 Contoh terhitung rak #1 (lapis domain, jalur OSP; P00 angka karangan sbg artefak bentuk)

`RANTAI-JAMINAN.md:61-68` - jalur OSP 3,2 km, 4 konektor, 6 sambungan fusi:

```
serat      : 3,2 x 0,5 = 1,60 dB
konektor   : 4  x 0,75 = 3,00 dB
sambungan  : 6  x 0,3  = 1,80 dB   (kolom terburuk)
                        ---------
ambang lulus            = 6,40 dB
```
Uji ulang giliran ini: 6.4 - cocok. Panjang gelombang uji tidak disebut di blok ini; CALC
induknya menyebut 1310 nm (`CALC-P00-001.md:45`).

### 3.3 Contoh terhitung rak #2 (resume Hayes, dua kolom)

`R3 - FOA Reference Guide to Fiber Optics.md:190-197` - link SM premises 2 km @1310 nm,
4 konektor, 2 sambungan fusion:

| Komponen | Tipikal | Terburuk |
|---|---|---|
| Serat 2 km | 2 x 0,4 = 0,8 dB | 2 x 1,0 = 2,0 dB |
| 4 konektor | 4 x 0,3 = 1,2 dB | 4 x 0,75 = 3,0 dB |
| 2 sambungan | 2 x 0,1 = 0,2 dB | 2 x 0,3 = 0,6 dB |
| **Total** | **2,2 dB** | **5,6 dB** |

Uji ulang: 2.2 dan 5.6 - cocok persis. Cara pakai: bandingkan KEDUA kolom terhadap anggaran
daya perangkat; "bila nilai terburuk masih di bawah anggaran, rancangan aman"
(`R3 - FOA ...:199-200`). Kolom terburuk yang memutuskan (`:202-205`).
Catatan: resume mengklaim buku memberi contoh terhitung penuh untuk "empat kombinasi
serat/panjang gelombang" (`:92-93`); lapis teks hanya mentranskripsikan SATU kombinasi
(SM premises 1310 nm) - tiga lainnya (SM OSP, MM 850, MM 1300) tanpa angka di rak (G-8).

### 3.4 Kerangka uji redaman: empat metode referensi IEC

| Metode [R2, IEC 61280-4-2:2014, PDF 17] | Test cord | Apa yang ikut terukur | Catatan rak |
|---|---|---|---|
| One-cord reference | satu | konektor ujung jauh tidak ikut terukur penuh | dipilih di `TEST-P00-001.md:19` dan `BA-P00-FO-001.md:33`; "menentukan konektor ujung mana yang ikut terukur" (`R2 - IEC ...:43-45`) |
| Three-cord reference | tiga | sistem referensi penuh tiga cord | tidak ada contoh penerapan di rak |
| Two-cord reference | dua | berada di antara keduanya | tidak ada contoh penerapan di rak |
| OTDR method | launch + receive cable | mencirikan link; metode standar menurut IEC | bertegangan dengan aturan FOA "OTDR bukan pengganti" - K-11 |

Tiga metode pertama memakai LSPM untuk daya masuk/keluar (`R2 - IEC ...:37-38`). Aturan
turunan di rak: berita acara wajib menyebut NAMA METODE, bukan hanya nama alatnya
(`R2 - IEC ...:43-45`; `RANTAI-JAMINAN.md:86,111`). Pemetaan standar Amerika yang rak pakai
berdampingan: FOTP-171 = satu ujung (patchcord); OFSTP-7 = dua ujung SM; OFSTP-14 = dua ujung
MM (`R3 - FOA ...:115-123`; `KATALOG-RUMUS.md:153-159`).

### 3.5 Rantai keputusan desain (bentuk yang rak tuntut; P00, angka karangan)

`DDR-P00-001.md`: keputusan 6 sambungan fusi mengikuti batas gulungan 500 m (`:19-20`);
alternatif ditolak DENGAN alasan kuantitatif: 3 sambungan (tunggu 8 minggu, hemat 0,9 dB
"tidak dibutuhkan karena anggaran masih longgar" `:38`); 10 sambungan (+1,2 dB dan 4 titik
potensi gangguan tambahan `:39`); akibat ke hilir dinyatakan (CALC n=6; TEST memeriksa 6 titik;
bila jumlah sambungan berubah DDR dan CALC wajib direvisi). Kolom "Konflik antar-sumber:
Tidak ada." (`:42-44`) tidak akurat terhadap ambang 1550 CALC-nya sendiri (K-2) - pertanyaan
konflik DDR disusun untuk konflik antar-buku, bukan konflik internal turunannya.

### 3.6 Hitung yang rak nyatakan TIDAK bisa dikerjakan dari rak

- Anggaran daya transceiver: kerangka saja; angka nyatanya R4 (`ASUMSI-BAKU.md:58`;
  `AMBANG-TERIMA-INDUK.md:88-96`). Nol angka daya kirim/sensitivitas di rak (G-4).
- Rugi konektor terpasang nyata: R4 wajib bila dijadikan ambang (`RANTAI-JAMINAN.md:51`;
  `AMBANG-TERIMA-INDUK.md:94`).
- Rugi sambungan nyata: diganti nilai terukur alat fusi saat pelaksanaan
  (`CALC-P00-001.md:64-66`; `ITP-P00.md:18`).
- Redaman multimode menurut IEC: tidak ada standarnya (GAP-010).
- Dispersi kromatik dan PMD: diatur standar lain, di luar cakupan IEC 61280-4-2
  (`R2 - IEC ...:100`); JDSU membahas cara pengukurannya tanpa satu pun angka ambang
  (`R3 - Reference Guide ...:63-67`) (G-6).

### 3.7 Cara pakai objek ini (rutin kerja)

1. Kumpulkan konfigurasi jalur: jenis serat (OS/OM), panjang, jumlah konektor (tiap patch
   panel = sepasang), jumlah sambungan, lambda uji.
2. Hitung loss budget PER LAMBDA dengan angka Bagian 2.2; pakai kolom terburuk.
3. Bandingkan terhadap anggaran daya transceiver [R4] - bila lembar data belum ada, tulis
   "menunggu data pabrikan", jangan mengarang.
4. Tetapkan ambang lulus = kolom terburuk; lampirkan RINCIAN HITUNGANNYA di BA.
5. Susun prosedur uji: sebut nama metode (one-cord/three-cord/two-cord/OTDR; OFSTP/FOTP),
   alat OLTS/LSPM wajib, OTDR pelengkap; kabel referensi <= 0,5 dB (uji FOTP-171).
6. Bila OTDR dipakai: catat lambda, lebar pulsa, rentang, averaging, indeks bias, panjang
   launch/receive cable.
7. Untuk multimode: nyatakan eksplisit bahwa metode bersandar OFSTP-14 [R3] karena
   IEC 61280-4-1 tidak ada (GAP-010).
8. Bila hasil dekat ambang: bawa catatan ketidakpastian; jangan bulatkan ke arah lulus.

---

## Bagian 4 - Ambang terima

### 4.1 Penempatan di ambang induk (`AMBANG-TERIMA-INDUK.md`, baris snapshot 14:11)

| Kelompok | Baris + token | Butir serat optik | Konsekuensi prosedur |
|---|---|---|---|
| Sah - berasal dari hitungan rancangan | `:42` "Rugi jalur serat optik" | loss budget kolom terburuk, metode Hayes PDF 129, 145, R3 | rincian hitung WAJIB dilampirkan (`:38`) |
| Perlu adopsi kontrak (R3) | `:61` "kabel referensi" | rugi > 0,5 dB patut dipertanyakan | periksa kontrak SEBELUM uji |
| Belum ada sumber sah | `:82` "multimode" | redaman MM: IEC 61280-4-1 tidak ada | tiga jalan sah: peroleh 4-1, ATAU pakai OFSTP-14 [R3] dan nyatakan pilihannya di BA |
| Wajib R4 | `:94` "redaman & reflektansi konektor terpasang"; `:96` | angka melekat produk | tulis "menunggu data pabrikan", tandai kartu MENUNGGU R4 |

Aturan induk yang mengikat semuanya (`:49`, token "Metode boleh R3"): "Metode boleh R3. Yang
tidak boleh R3 adalah angka lulus/tidak lulus yang tidak dihitung." Domain serat optik patuh
di sini karena angkanya memang dihitung, bukan dikutip.

### 4.2 Ambang lulus loss budget: kolom terburuk, per lambda

- Ambang ditetapkan PER PANJANG GELOMBANG, bukan satu angka untuk semua: `TPL-02` hanya punya
  satu baris Hasil dan terbukti kurang ketika uji coba menghasilkan dua ambang (6,40 dB @1310
  dan 5,96 dB @1550) - temuan nomor 3 uji coba (`TEMUAN-UJI-COBA-P00.md:43-45`), sudah
  diperbaiki dengan tabel hasil per kondisi.
- Uji satu lambda DITOLAK: "cacat bending hanya tampak di 1550" (`RANTAI-JAMINAN.md:27`).
  Satu-satunya alasan teknis dua-lambda yang tercatat di rak.
- Ambang 6,40 dB @1310 tervalidasi aritmetika (Bagian 2.5). Ambang 5,96 dB @1550 =
  KNOWN-DEFECT K-2: DILARANG menulisnya sebagai angka final; kandidat rak yang reproducible
  adalah 5,60 dB (a=0,25), 5,76 dB (a=0,3), atau 6,40 dB (a=0,5 kolom terburuk konsisten
  dengan 1310) - pemilihan di antaranya menunggu putusan manusia/controller.
- Sah-tidaknya ambang R3 diuji lewat kotak centang adopsi kontrak: pada P00 ambang sah HANYA
  karena kontrak pasal 7.3 mengadopsi IEC 61280-4-2; tanpa pasal itu "rantai akan putus"
  (`TEST-P00-001.md:37-39`; `KARTU-P00-001.md:53`).

### 4.3 Kriteria lulus/gagal OTDR sebagaimana rak menuliskannya

Yang ada di rak adalah KRITERIA KEHADIRAN DAN KETERJALAAN, bukan angka ambang OTDR:

| Butir | Ketentuan | Jalur |
|---|---|---|
| Kriteria lulus butir OTDR | "6 sambungan terlihat, tak ada peristiwa tak dikenal" (sumber ambang: "Rancangan") | `ITP-P00.md:17` |
| Kedudukan | OTDR pelengkap; menyerahkan hasil OTDR saja sebagai bukti lulus = kesalahan tersering di lapangan | `RANTAI-JAMINAN.md:87,100-101`; `R3 - FOA ...:109`; `REF-FO-001.md:41` - sisi R2 tandingannya di K-11 |
| Kewajiban jejak | jejak `.sor` + daftar peristiwa + setelan lengkap - tanpa itu jejak tidak dapat ditafsirkan ulang | `RANTAI-JAMINAN.md:114`; `TEMPLATE-BERITA-ACARA.md:79-80`; `BA-P00-FO-001.md:51` |
| Fungsi sah OTDR | lokasi sambungan, reflektansi, keseragaman serat; verifikasi tiap sambungan OSP antara; rugi per sambungan menggantikan asumsi 0,3 dB | `R3 - FOA ...:102,109`; `ITP-P00.md:18`; `TEST-P00-001.md:54-55` |
| Gagal baca khas | dead zone setelah peristiwa pantulan (jalur pendek dalam gedung), ghost pada kabel pendek, autotest tanpa penyetelan manual | `R3 - Reference Guide ...:51-53,60-61`; `R3 - FOA ...:140-149` |
| Nol angka | tidak ada satu pun ambang dB/reflektansi untuk peristiwa OTDR di lapis teks | sapuan studi G-12; `ekas/08_EVIDENCE/OTDR/` berisi README saja |

### 4.4 Bukti serah rantai A (`RANTAI-JAMINAN.md:107-116`), disalin utuh

| Lampiran | Wajib | Catatan rak |
|---|---|---|
| Berita acara uji per core | ya | kerangka di `TEMPLATE-BERITA-ACARA.md` bagian 1 |
| **Ambang beserta rincian hitungnya** | ya | **butir yang paling sering hilang** |
| Metode uji + pilihan test cord | ya | sebutkan nama metodenya, bukan hanya alatnya |
| Sertifikat kalibrasi alat | ya | merek, tipe, nomor seri, tanggal |
| Rugi kabel referensi terukur | ya | syarat <= 0,5 dB |
| Jejak OTDR + daftar peristiwa | bila disyaratkan | sertakan setelan: lebar pulsa, rentang, launch cable |
| Catatan ketidakpastian | ya | melindungi saat hasil berada dekat ambang |
| Kartu kendali rantai | ya | satu per jalur |

Status rantai dicetak UTUH (`:118-119`) dengan catatan terbuka 61280-4-1 (`:121-123`).
Predikat jujur untuk registrasi: UTUH pada KERANGKA DAN URUTAN; dua matanya bergantung bahan
yang tidak ada di rak (R4 produk, dan standar multimode).

### 4.5 Kelas R2 vs R3 (larangan meratakan)

- R2 IEC 61280-4-2: sah MENETAPKAN METODE dan menjadi sandaran ambang HANYA bila kontrak
  mengadopsi tertulis dan edisinya tervalidasi (`REF-FO-003.md:40`); ia sendiri TIDAK memberi
  angka ambang (`R2 - IEC ...:101-102`).
- R3 Hayes/JDSU: dasar perhitungan dan praktik; ambang yang diturunkannya sah sebagai
  "hitungan rancangan" (`AMBANG-TERIMA-INDUK.md:35-42`) atau perlu adopsi kontrak
  (`:54-61`), bukan sebagai hukum.
- R1 (dasar hukum Indonesia): NOL - korpus tidak dapat menyatakan kepatuhan PUIL/SNI
  (GAP-001 lintas domain).

---

## Bagian 5 - Register kontradiksi / known-defect

Dua belas butir dari studi, naik UTUH dengan predikat finalnya. Rak sudah dianotasi lewat
tambalan hanya-tambah D2-FIXx: 26 blok `CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24)` di
16 berkas, +21.927 byte, nol karakter lama berubah (guard subsequence), verifikasi independen
VERDICT PASS, sapuan ulang BOCOR=0 (`docs/2026-09-23-nws-knowledge-register/fixekas/
system_change_d2.md`). Bentuk lama TIDAK dihapus dari rak, hanya ditandai. SEMUA vonis halaman
berstatus BELUM TERKONFIRMASI terhadap sumber primer sampai manusia membuka PDF. Sitasi yang
dibatalkan tetap tertulis di sini dengan dasar pembatalan - penghapusan diam-diam = cacat
proses (skema G-1 seksi 7 butir 3).

### K-1. Batas jarak multimode ~550 m: angka normatif tanpa sumber (KNOWN-DEFECT; beban-rilis)

Angka hanya ada di `RANTAI-JAMINAN.md:25` ("MM ditolak di atas ~550 m - batas jarak pada laju
tinggi"), kolom Dasar "Jarak + lebar pita + biaya", kolom Tingkat/R KOSONG. Sapuan 6 kueri
studi atas seluruh korpus (OM1-OM5; "550"; "300 m"; 802.3/BASE-SR/BASE-LX; pola "[0-9]+ m" di
dua berkas FO; JDSU) = NOL padanan: tabel OM1-OM5 `R3 - FOA ...:51-55` tidak memuat jarak;
tiga situs "550" lainnya bukan jarak MM; "300 m" di `DDR-P00-001.md:39` = panjang gulungan
gudang. ~550 m menyerupai jarak 10GBASE-SR pada OM3 yang tidak disebut di rak. Baris inilah
yang memutuskan SM vs MM di awal setiap pekerjaan. Anotasi rak: `RANTAI-JAMINAN.md:30-31`.
Perlakuan di objek ini: dibawa APA ADANYA dengan predikat known-defect - BUKAN angka final;
adjudikasi final = manusia dengan PDF Hayes Bab 5/9 dan TIA-568 (GAP-011); controller memutus
naik/tidak.

### K-2. Ambang 5,96 dB @1550 tidak reproducible (KNOWN-DEFECT; beban-rilis)

Induk: `CALC-P00-001.md:48`. Enam turunan menyalin angka yang sama tanpa rincian:
`KARTU-P00-001.md:20,50`; `ITP-P00.md:16`; `TEST-P00-001.md:34`; `BA-P00-FO-001.md:26`;
`TEMUAN-UJI-COBA-P00.md:45`. Ukuran ulang giliran ini (Bagian 2.5): masukan tercatat memberi
5,60 / 5,76 / 6,40 dB; alpha tersirat 0,3625 dB/km tidak muncul di FOA/rantai/katalog/kartu;
brute force 1.120 kombinasi (giliran studi) menghasilkan 9 solusi yang SEMUANYA menuntut
n_sambungan 8/10 (bertentangan n=6 di DDR/CALC) atau rugi konektor 0,5/1,0 dB (bukan 0,75
tercatat). Mitigasi: berkas P00 berlabel "angka karangan" - tidak ada dokumen serah nyata
tercemar; tapi ini contoh dua-lambda satu-satunya di rak. Anotasi: keenam lapis berblok
CATATAN DEFECT (lihat Bagian 1.4). DILARANG menulis 5,96 sebagai angka final; keputusan
koreksi (5,76 / 6,40 / catatan "ilustrasi tanpa rincian") = manusia/controller.

### K-3. Ketidakpastian 0,02-0,05 dB/hari: atribusi JDSU vs FOA (KNOWN-DEFECT atribusi; beban-rilis)

Angka tercetak HANYA di resume FOA (`R3 - FOA ...:128-131` dan `:213-214`). Yang menyandarkan
ke JDSU: `RANTAI-JAMINAN.md:12` (baris tabel rujukan), `:74` (marker [R3, JDSU]),
`REF-FO-002.md:22` (dipasang sebagai pasokan rujukan JDSU, jangkar cetak 37 / PDF 44), skill
ref. Resume JDSU: `grep -c '0,02'` = 0 dan `grep -n 'dB'` = 0 hasil - tidak memuat satu pun
angka dB. `KATALOG-RUMUS.md:147` mencantumkan angka tanpa atribusi. Kemungkinan rekonsiliasi:
buku JDSU mungkin benar memuatnya (resume tidak menjamin kelengkapan) - vonis final manusia
dengan PDF JDSU Bab 2 (cetak 37 / PDF 44) dan FOA Bab 8 (PDF 98). Nilai tidak berubah; yang
dicacatkan penanda sumbernya. Anotasi: `RANTAI-JAMINAN.md:16-17,76-77`; `REF-FO-002.md:26-27`;
`KATALOG-RUMUS.md:150-151`; `R3 - FOA ...:133-134,216-217`. Di objek ini angkanya diberi
penanda [R3, Hayes FOA Reference Guide, PDF 98 dst.] mengikuti tempat tercetaknya.

### K-4. Offset halaman Hayes tidak terujiable internal (batas metode; beban-rilis utk klaim halaman)

Aturan rak: selisih cetak vs PDF TIDAK TETAP (+3 depan s.d. +10 apendiks), seluruh rujukan
memakai nomor PDF (`R3 - FOA ...:7-10`). Halaman kunci domain (PDF 98, 120, 129, 145, 203)
TIDAK punya pasangan cetak di lapis teks - nol uji silang internal mungkin. JDSU sebaliknya:
+7 lolos 7/7 pasangan. Perlakuan: JANGAN pernah menulis "halaman cetak X" untuk Hayes; tulis
nomor PDF + status "belum diverifikasi manusia". Bukan kontradiksi angka - tidak ditambal
(kontrak kartu FIX); batasan ini ikut terbit bersama setiap sitasi Hayes.

### K-5. Rugi sambungan 0,1-0,3 dB hilang dari katalog dan asumsi baku (gap konsistensi; beban-rilis)

Rentang hidup HANYA di `RANTAI-JAMINAN.md:50` (R3; R4 bila alat menyebut lain) dan skill ref.
`KATALOG-RUMUS.md` seksi 2 tidak punya baris rugi sambungan; `ASUMSI-BAKU.md:55` mengarahkan
"spesifikasi pelaksana / batas kontrak" tanpa angka; satu-satunya pemakaian contoh
(`CALC-P00-001.md:36`, 0,3 dB) ditag ASSUMPTION. Efek nyata: butir hilir cenderung mengambil
0,3 dB sebagai "angka rak". Anotasi: `RANTAI-JAMINAN.md:53-54`; `KATALOG-RUMUS.md:138-139`;
`ASUMSI-BAKU.md:60-61`. Rekomendasi studi (untuk controller): daftarkan 0,1-0,3 dB ke KATALOG
seksi 2 dan ASUMSI-BAKU sebagai asumsi baku berpenanda R3+R4.

### K-6. Jumlah sumber per tingkat berbeda antar lapis register (beban-rilis: tidak, kecuali statistik rak)

`README.md:34-38` mencetak R1=0, R2=5, R3=24, R4=0, R5=8; `MASTER-REFERENCE-REGISTER.md`
menyebut "5 standar, 4 resume / 24 buku / 3 resume + 21 makalah"; CSV (62 baris data) mengukur
R2=4, R3=49 judul, R4=6, R5=3. Kontradiksi terukur antar lapis, bukan spesifik fiber; objek
ini hanya mengutip keadaan README apa adanya. Tidak ditambal (register internal).

### K-7. Skill fiber-link-design: klaim 3 referensi 377 baris vs nyata 1 referensi 128 baris (beban-rilis utk klaim skill)

`CHANGELOG.md:197` mengklaim "SKILL.md + 3 referensi - 377 baris"; `CHANGELOG.md:383` menunjuk
berkas `02-uji-dan-berita-acara.md` yang `find`-nya 0 hasil di seluruh pohon. Ukur ulang
giliran ini: 73 + 55 = 128 baris, 1 referensi, md5 identik di tiga lokasi. Materi Bagian 6b
(IEC, empat metode, RTM, ORL) ADA di versi sekarang - tidak ada kehilangan pengetahuan, yang
hilang berkasnya. Artefak skill BUKAN rak `ekas/` -> tidak ditambal; laporan controller.
Objek ini TIDAK mengulang klaim 377 baris.

### K-8. Laci sumber mengklaim berkas fisik ada; pohon `ekas/` tanpa PDF (cacat alamat bukti; beban-rilis jalur bukti)

Lihat Bagian 1.5. `find ekas -name '*.pdf'` = 0 (dua kali terukur); PDF nyata di
`C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/...` dengan ukuran terukur (FOA 54.533.749 B;
JDSU 6.416.581 B; IEC 1.588.640 B). Anotasi: kedua `_ISI.md` laci fiber (`:10` dan `:9`).
Kelas yang sama hidup di 20 `_ISI.md` laci domain lain -> laporan controller (lingkup, bukan
wewenang pekerja). Objek ini dan baris rute menyebut DUA lokasi.

### K-9. Rumus reflektansi tanpa pembatas cakupan (rujukan melebihi isi; beban-rilis)

`REF-FO-003.md:29` menempatkan `Reflectance = 10 x log10 (Pr / Pin)` tanpa catatan bahwa
sumbernya membatasi definisi pada komponen diskret dalam kabel (`R2 - IEC 61280-4-2.md:58-65`);
tidak ada lapis yang menjelaskan hubungan arah tanda reflectance vs ORL. Risiko salah pakai
nyata: rumus komponen dipakai untuk ORL jalur. Anotasi: `REF-FO-003.md:32-33` + blok di
KATALOG seksi 13.3. Rekonsiliasi butuh PDF IEC (definisi 3.1.7).

### K-10. OM5 dilebeli lebar pita identik OM4 tanpa pembeda terukur (CALON; beban-rilis: tidak)

`R3 - FOA ...:54-55`: OM4 dan OM5 sama-sama "3 / 1" dan "3600/500 MHz-km"; pembeda hanya
naratif ("VCSEL 850 nm, >10 Gb/s" vs "Dioptimalkan untuk WDM 850-950 nm"). Tidak ada angka
EBW/WMODEP di rak. Kurang, bukan salah; tidak ditambal.

### K-11. "OTDR bukan pengganti" (R3) vs "OTDR method" metode standar (R2) - BELUM DIADJUDIKASI (beban-rilis)

Sisi R2: IEC mencantumkan metode OTDR sebagai salah satu empat metode uji redaman
(`R2 - IEC 61280-4-2.md:25-35`). Sisi R3: FOA mewajibkan LSPM/OLTS dan menyebut OTDR
pelengkap bukan pengganti (`R3 - FOA ...:104-110`); rantai mengulang (`:87,100-101`);
`KATALOG-RUMUS.md` seksi 13.3 menegaskan "Tiga pertama memakai LSPM". Keduanya bisa benar
sekaligus (metode ukur vs bukti rugi sisipan total untuk serah terima), tapi tidak ada berkas
yang menuliskan rekonsiliasinya; `AUTHORITY-STATUS.md` hanya mengatur "cara mengukur vs berapa
batasnya". BUTIR PALING BERBAHAYA UNTUK BERITA ACARA: pelaksana bisa mengutip baris IEC untuk
menyerahkan jejak OTDR saja sebagai bukti lulus. Anotasi: `RANTAI-JAMINAN.md:93-94`;
`REF-FO-001.md:43-44`; `R2 - IEC 61280-4-2.md:40-41`; `R3 - FOA ...:112-113`; KATALOG seksi
13.3. Objek ini menyimpan KEDUA sisi + aturan pakai: OLTS/LSPM untuk ambang rugi sisipan;
OTDR untuk pencirian, lokasi sambungan, dan rugi per sambungan. Putusan akhir = controller.

### K-12. Nama berkas resume di indeks katalog tidak sama dengan berkas nyata (cacat penamaan; beban-rilis jalur)

Indeks `KATALOG-RUMUS.md` (token "Peta resume", sekitar `:570-577`) menunjuk
`RESUME - FOA Reference Guide to Fiber Optics.md` dan `RESUME - Reference Guide to Fiber
Optic Testing V...` di folder `R3/FIBER-OPTIC/`. Nama nyata: `R3 - FOA ...` dan
`R3 - Reference Guide ...` di `05_DOMAIN-KNOWLEDGE/FIBER-OPTIC/`; label `R3/FIBER-OPTIC/`
adalah laci vault, bukan folder domain. Beranotasi. Seluruh path di objek ini memakai nama
nyata (kontrak jalur G-1 seksi 6).

### Blok warisan Tabel 7 (known-defect VSSKB yang ikut terangkut)

Objek ini mengutip `ASUMSI-BAKU.md` dan `KATALOG-RUMUS.md` - dua berkas yang membawa anotasi
defect warisan VSSKB-0923 (`ASUMSI-BAKU.md:152`; `KATALOG-RUMUS.md:61`): waktu deteksi
hilangnya sinyal 8/4/2 detik berkontradiksi dengan bentuk empat nilai 8/4/4/2 dan pemetaan
per-grade BELUM TERKONFIRMASI terhadap geometri PDF primer. Larangan tegas: JANGAN mengutip
8/4/2 maupun 8/4/4/2 sebagai ambang sah dari berkas mana pun; sumber kebenaran fakta tunggal
itu tetap entri wiki `faktas/waktu-deteksi-hilangnya-sinyal-video-tabel7-bsen-62676-1-2.md`
(ditandai known-defect oleh librarian 2026-09-23). Preseden OQ-6: objek fiber tidak boleh
mengutip kedua berkas bersama itu tanpa membawa penanda defect-nya - penanda ini adalah
pemenuhannya.

### Ringkasan predikat final

| Butir | Kelas | Predikat final | Beban-rilis | Tambalan D2-FIXx |
|---|---|---|---|---|
| K-1 | ~550 m MM tanpa sumber | angka normatif tanpa penanda R; nol padanan (sapuan 6 kueri) | ya | ya (1 blok) |
| K-2 | 5,96 dB @1550 | kontradiksi aritmetika internal terukur; induk CALC | ya | ya (6 lapis) |
| K-3 | 0,02-0,05 dB/hari | kontradiksi atribusi FOA vs JDSU | ya | ya (6 blok) |
| K-4 | offset halaman Hayes | batas metode; tidak terujiable internal | ya (klaim halaman) | tidak (bukan angka) |
| K-5 | rugi sambungan | gap konsistensi antar-lapis; 0,3 dB = ASSUMPTION | ya | ya (3 blok) |
| K-6 | statistik R1-R5 | kontradiksi terukur antar lapis register | tidak | tidak |
| K-7 | skill 3 ref/377 baris | kontradiksi terukur terhadap artefak nyata | ya (klaim skill) | tidak (bukan rak) |
| K-8 | laci "berkas sudah ada" | cacat alamat bukti terukur | ya (jalur bukti) | ya (2 blok) |
| K-9 | rumus reflektansi | rujukan melebihi isi / pembatas hilang | ya | ya (2 blok) |
| K-10 | OM5 = OM4 | calon (lapis teks tidak cukup) | tidak | tidak |
| K-11 | OTDR R2 vs R3 | ketegangan belum diadjudikasi; objek simpan dua sisi | ya | ya (5 blok) |
| K-12 | nama resume di katalog | cacat penamaan terukur | ya (jalur rute) | ya (1 blok) |

Sepuluh dari dua belas menyentuh beban-rilis; semuanya dibawa apa adanya dengan predikat.
Tidak ada butir yang ditutup sebagai "mungkin sama saja" (pelajaran Tabel 7).

---

## Bagian 6 - Gap register domain

### 6.1 Celah resmi ber-ID (`ekas/02_REGISTERS/GAP-REGISTER.csv`, baris snapshot)

| ID | Celah | Kelas | Domain | Prioritas | Status + jalur sah hari ini |
|---|---|---|---|---|---|
| GAP-010 | IEC 61280-4-1 (uji redaman serat MULTIMODE) `csv:11` | R2 | FIBER-OPTIC | MENENGAH | terbuka ("Yang ada 4-2 = singlemode"). Jalur sah: peroleh 4-1, ATAU pakai OFSTP-14 [R3] dan nyatakan di BA bahwa acuan IEC multimode tidak ada (`RANTAI-JAMINAN.md:121-123`; `AMBANG-TERIMA-INDUK.md:82`) |
| GAP-011 | TIA-568 / TIA-942 `csv:12` | R2 | STORAGE, NETWORKING (efek ke D2) | MENENGAH | terbuka; laci TIA `_ISI.md:3` "Kosong." Efek fiber: 0,75 dB dan 1 dB/km berstatus "batas TIA menurut Hayes" (kutipan R3), bukan kutipan standar |
| GAP-014 | Seluruh dokumentasi OEM `csv:15` | R4 | SEMUA | PER PROYEK | by-design - diminta ke pabrikan tiap proyek; tanpa lembar data: "menunggu data pabrikan" |
| GAP-001 | PUIL/SNI dasar hukum Indonesia `csv:2` | R1 | lintas | TINGGI | terbuka; NETA/IEC/Hayes bukan pengganti kepatuhan hukum Indonesia |

### 6.2 Celah hasil sapuan studi (basis bukti perintah, bukan dugaan)

| ID | Yang dicari | Keadaan | Bukti sapuan (ringkas) |
|---|---|---|---|
| G-1 | IEC 61280-4-1 | tidak ada di rak | GAP-010; teks di 6 situs; laci `R2/IEC/` hanya 1 berkas |
| G-2 | TIA-568 sebagai dokumen | tidak ada di rak | GAP-011; laci TIA kosong; 0,75 dB hanya via buku R3 |
| G-3 | Dokumen FOTP-171 / OFSTP-7 / OFSTP-14 | tidak ada - hanya namanya | 10 situs FOTP-171, 6 situs OFSTP, semuanya sebutan |
| G-4 | Anggaran daya transceiver | tidak ada angka | grep 3 hasil kerangka saja; rumus selisih daya hanya di skill; `R4-STATUS.md:41` |
| G-5 | Tabel jarak/jangkauan aplikasi MM (802.3, OM per laju) | tidak ada | K-1: 802.3/BASE-SR/BASE-LX = 0 hasil; satu-satunya angka = ~550 m tanpa sumber |
| G-6 | Dispersi kromatik dan PMD sebagai angka | tidak ada angka | `R2 - IEC ...:100`; JDSU bahas cara ukur tanpa nilai |
| G-7 | Ambang numerik ORL/reflektansi | tidak ada | 20 situs semuanya metode/definisi; IEC eksplisit tidak memberi angka ambang |
| G-8 | Contoh terhitung multimode / dua-lambda ter-rinci | tidak ada | satu-satunya contoh terhitung SM; klaim "empat kombinasi" hanya satu ditranskripsikan; 5,96 tanpa rincian (K-2) |
| G-9 | Dokumen ITU-T G.652 yang dirujuk tabel serat | tidak ada | `R3 - FOA ...:56` memetakan OS1/OS2 ke G.652; laci ITU-T "Kosong." |
| G-10 | Nilai bawaan indeks bias / panjang launch-receive cable | tidak ada | hanya butir "wajib dicatat"; nol nilai contoh |
| G-11 | Lembar data produk konektor/kabel (R4) | tidak ada dan memang tidak diadakan | `R4-STATUS.md:41`; GAP-014 by-design |
| G-12 | Ambang numerik lulus/gagal jejak OTDR | tidak ada | kriteria hanya kualitatif (`ITP-P00.md:17`); laci 08_EVIDENCE/OTDR README saja |
| G-13 | Rantai contoh MM / premises pendek | tidak ada | seluruh suite P00 = SM OSP 3,2 km; nol contoh jalur < 500 m padahal OTDR sulit di premises |
| G-14 | Dasar hukum Indonesia (PUIL/SNI) | tidak ada | README R1=0; GAP-001 |

### 6.3 Yang justru KUAT di rak ini (agar objek tidak timpang)

- Rantai lima mata lengkap dengan alternatif ditolak + alasan kuantitatif
  (`RANTAI-JAMINAN.md:23-28`; `DDR-P00-001.md:34-40`) - jarang dimiliki domain lain.
- Daftar 8 lampiran wajib serah dengan penanda "butir paling sering hilang" - siap tempel BA.
- Aturan kolom terburuk konsisten di 7 lapis berbeda tanpa satu pun deviasi angka.
- Suite contoh P00 end-to-end yang sengaja dibiarkan terbuka (G3 belum, rantai PUTUS) -
  bentuk gate gagal terlihat.
- Konversi halaman JDSU lolos uji internal 7/7.
- Pemetaan peran alat tegas dengan alasan (OLTS/LSPM vs OTDR vs VFL).
- SATU-SATUNYA domain dengan standar R2 metode uji nyata di rak (IEC 61280-4-2) + RTM untuk
  perselisihan hasil ukur - kekuatan yang tidak dimiliki NETWORKING.
- Laci R4 fiber kosong total dan JUJUR (`R4-STATUS.md:41`): setiap angka produk langsung
  "menunggu data pabrikan", tidak ada godaan menyalin angka buku sebagai angka produk.

---

## Bagian 7 - Kata kunci rute (16 token)

Tag beku objek ini (daftar beku G-1 seksi 4, byte-per-byte; frontmatter tetap otoritatif,
bagian ini hanya mirror):

`fiber-optic, serat-optik, loss-budget, otdr, olts, konektor, splice-fusi, singlemode,
multimode, iec-61280, ofstp, fotp, tia-568, redaman, db-per-km, cable-plant` = 16 token.

| Token | Padanan kerja harian | Jangkar isi |
|---|---|---|
| fiber-optic / serat-optik | seluruh domain | objek ini |
| loss-budget | hitung rugi jalur per lambda | [R3, Hayes FOA Reference Guide, PDF 129] Bagian 2.1, 3.2-3.3 |
| redaman / db-per-km | 1,0 / 0,5 / 0,4 / 0,3 dB/km; MM 3/1 | Bagian 2.2 |
| konektor | 0,75 dB batas; sepasang per patch panel | [R3, Hayes FOA Reference Guide, PDF 129]; `ASUMSI-BAKU.md:57` |
| splice-fusi | 0,1-0,3 dB; R4 bila alat menyebut lain | K-5 - predikat ikut token ini |
| otdr | pencirian jalur, dead zone, ghost, setelan jejak | [R3, JDSU/Laferriere, cetak 65 dan 89 / PDF 72 dan 96]; K-11 |
| olts | alat wajib rugi sisipan | [R3, Hayes FOA Reference Guide, PDF 98] |
| singlemode | cakupan IEC 61280-4-2 | [R2, IEC 61280-4-2:2014, PDF 17] |
| multimode | metode bersandar OFSTP-14; ~550 m known-defect | GAP-010; K-1 |
| iec-61280 | empat metode, RTM, ORL | [R2, IEC 61280-4-2:2014, PDF 14, 17, 20, 43] |
| ofstp / fotp | OFSTP-7 SM, OFSTP-14 MM, FOTP-171 patchcord | [R3, Hayes FOA Reference Guide, PDF 98]; dokumen tidak di rak (G-3) |
| tia-568 | asal-usul 0,75 dB | GAP-011 - status kutipan R3 |
| cable-plant | jalur terpasang, kabel referensi <= 0,5 dB | Bagian 2.2, 4.4 |

Catatan jujur: istilah "kabel referensi", "kolom terburuk", "RTM", "berita acara", "1310",
"1550" adalah keyword harian yang tidak termasuk daftar beku G-1 - rute mereka lewat token di
atas dan lewat body objek. Perubahan daftar tag = amandemen G-1 lewat kartu + Decision Log,
bukan suntingan senyap.

---

## Bagian 8 - BATAS PENGETAHUAN / status rantai

Blok ini wajib ikut terbit bersama angkanya. Objek yang hanya berisi angka enak-dibaca tapi
menyembunyikan celah = gagal maksud registrasi dan menabrak aturan EKAS ("jawab tidak ada di
rak daripada mengarang").

1. **Status rantai apa adanya (tanpa perataan):** rantai A mencetak UTUH
   (`RANTAI-JAMINAN.md:118-119`) - benar pada KERANGKA DAN URUTAN; ambang metode uji bersandar
   R2 IEC 61280-4-2 TETAPI hanya singlemode; dua mata bergantung bahan di luar rak: R4 produk
   (anggaran daya transceiver, rugi konektor terpasang) dan standar multimode (GAP-010).
   Rantai contoh P00 sendiri PUTUS di mata 3 - sengaja dibiarkan sebagai artefak bentuk gate
   gagal.
2. **R1 = 0 dan R4 = 0 global.** Keadaan rak: R1=0, R2=5, R3=24, R4=0, R5=8
   [peta rak: `ekas/00_START-HERE/README.md:34-38`]. Arti: korpus dapat menghitung dan
   menetapkan ambang uji, TIDAK dapat menyatakan kepatuhan hukum Indonesia (PUIL/SNI tidak
   di rak; GAP-001 lintas domain). R4 by-design: angka melekat produk diminta per proyek
   (`README.md:47`; GAP-014).
3. **Known-defect yang wajib ikut terangkut (semua BELUM TERKONFIRMASI sampai manusia membuka
   PDF primer):** (a) K-1 ~550 m MM tanpa sumber - jangan pernah dikutip sebagai "sesuai
   standar"; (b) K-2 5,96 dB @1550 tidak reproducible - jangan pernah dikutip sebagai angka
   final; (c) K-3 atribusi 0,02-0,05 dB/hari: tempat tercetak FOA, sandaran tertulis JDSU -
   jangan menggandakan atribusi yang diperdebatkan; (d) K-4 halaman Hayes = nomor PDF dengan
   offset tidak tetap, belum diverifikasi manusia - jangan menulis "halaman cetak"; (e) K-11
   ketegangan R2/R3 soal OTDR - simpan kedua sisi + aturan pakai, jangan meratakan ke salah
   satu; (f) warisan Tabel 7 VSSKB menempel di dua berkas bersama yang dikutip objek ini -
   penandanya ikut di Bagian 5. Rak telah dianotasi D2-FIXx (26 blok, 16 berkas, BOCOR=0);
   bentuk lama tidak dihapus.
4. **GAP register yang mengikat domain:** GAP-010 (IEC 61280-4-1 multimode, MENENGAH - jalur
   sah OFSTP-14 + pernyataan eksplisit), GAP-011 (TIA-568 - angka TIA hidup hanya sebagai
   kutipan R3 Hayes; lapis yang menyatakan lain = defect), GAP-014 (R4 by-design), GAP-001
   lintas (R1). Plus 14 gap sapuan G-1..G-14 (Bagian 6.2).
5. **Nol angka karangan.** Setiap angka objek ini adalah cetakan bacaan rak dengan jalur
   baris, atau keluaran skrip aritmetika pada giliran ukur. Berkas P00 selalu diberi label
   "(P00, angka karangan)" dan dipakai sebagai artefak bentuk, bukan acuan proyek. Tidak ada
   satu pun angka produk diangkat menjadi ambang.
6. **Multimode adalah warga kelas dua di rak ini.** Angkanya ada (3/3,5; 1/1,5 dB/km; lebar
   pita OM), metode ujinya TIDAK bersandar standar di rak (OFSTP-14 [R3] via GAP-010), contoh
   terhitungnya tidak ada (G-8), batas jaraknya known-defect (K-1). Pekerjaan MM nyata wajib
   menyatakan semua ini di BA, bukan diam-diam memakai kerangka SM.
7. **Peringatan usia buku:** JDSU 2007 (19 th, MRR `:66`; `REF-FO-002.md:44` "periksa rujukan
   standarnya"); IEC edisi 2.0 2014; Hayes 2019 paling muda. Asimetri tercatat: gerbang
   peringatan usia >15 th ada di `KARTU-P00-001.md:27` tetapi MRR tidak punya baris usia untuk
   Hayes. Prinsip pengukuran OTDR tetap berlaku; setelan dan menu produk 2007 jangan
   diharapkan sama dengan alat sekarang.
8. **R3 bukan ambang hukum; R2 pun butuh adopsi kontrak.** Metode boleh R3; angka
   lulus/tidak-lulus yang tidak dihitung tidak boleh R3 (`AMBANG-TERIMA-INDUK.md:49`). Kelas
   R2 (IEC) dan R3 (Hayes/JDSU) dilarang diratakan menjadi "standar" generik.
9. **Domain tetangga hanya rujukan silang, tidak disalin (putusan P-8):** NETWORKING
   (`ekas/05_DOMAIN-KNOWLEDGE/NETWORKING/`) untuk LAN aktif di atas cable plant (batas tegas
   Bagian 1.6); TIA-568/942 milik bersama dengan STORAGE via GAP-011; VSSKB Tabel 7 warisan
   lewat berkas bersama (Bagian 5 blok warisan). POWER-BACKUP, GROUNDING, THERMAL, ELECTRICAL
   di luar cakupan D2.
10. **Sumber dan kebaruan.** Seluruh angka berasal dari lapisan teks `ekas/` diekstrak
    read-only 2026-09-24; tidak ada PDF primer dibuka - verifikasi per halaman wewenang
    manusia; PDF asli di `C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/` (BUKAN di
    `ekas/` - K-8). `ekas/` read-only - objek ini tidak mengubah rak. Nomor baris berkas
    domain FO = pasca-D2-FIXx; berkas bersama = snapshot 2026-09-24 14:11 WIB dengan pengawet
    token karena tambalan D3-FIXx/D4-FIXx berjalan paralel.

STATUS: complete
