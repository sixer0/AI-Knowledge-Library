---
id: cybersecurity-korpus-ekas-0928
type: catatan
title: Korpus CYBERSECURITY EKAS - peta, rumus, ambang, dan batas pengetahuan (SDCY-0928)
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-28
catatan_verifikasi: "Terverifikasi (re-verifikasi custodian gsp-custodian iterasi-2, 2026-09-28). Tiga koreksi redaksi iterasi-1 diuji ulang ke rak nyata dan seluruhnya cocok. (1) Bagian 6.1: pola berversi 'CIS Controls v<n>' terukur tepat 1 (baris 76 resume tesis, 'CIS Controls v8') dan sebutan nama 'CIS Controls' terukur 3 (baris 70, 76, 95) sesuai teks objek; INFO: baris 76 adalah kemunculan yang sama membawa versi, jadi hitungan 3 = total sebutan nama termasuk yang berversi. (2) Bagian 8 butir 6: resume Anderson tidak memuat tahun edisi (sapuan tahun 4-digit selain tanggal menyusun 2026 = kosong; hanya 'Edisi: ketiga, Penerbit: Wiley'); resume Alsmadi baris 3 memuat 'Springer, 2019'; RANTAI-JAMINAN baris 17-18 memuat Anderson (2020) dan Alsmadi (2019) - redaksi kini benar dua arah. (3) Bagian 2: token retensi=0 dan SIEM=0 terukur pada kelima berkas domain CYBERSECURITY; se-ekas 'retensi' = 6 token di 3 berkas luar domain (RANTAI-JAMINAN VIDEO-SURVEILLANCE 2, TEMPLATE-BERITA-ACARA 3, ASUMSI-BAKU 1 di baris 105 konteks retensi video) - catatan lingkup objek akurat. Anti-regresi: diff terhadap backup-pra-revisi-iter1 = tepat 3 hunk body (Bagian 2, 6.1, 8.6) plus 2 hunk frontmatter; blok paragraf wrap-insensitive berubah tepat 3 replace; token numerik di luar tiga wilayah identik (987 vs 987); angka baru hanya koordinat koreksi (70/76/95, 17/18, 2019/2020, 105, 6, 8) seluruhnya terverifikasi ke rak; nol angka vonis berubah. Frontmatter lolos yaml.safe_load, satu baris status, nol kunci duplikat, riwayat-catatan-verifikasi identik dengan verdict iterasi-1. INFO label: catatan_keputusan librarian menyebut koreksi retensi di 'Bagian 4', padahal kalimatnya berada di Bagian 2 (paragraf 'Hitung yang rak nyatakan TIDAK bisa dikerjakan') - salah label di catatan keputusan, bukan cacat body; tidak memblokir. Verdict kualitas ini TIDAK menggantikan gate: penandaan defek D1-FIXx (S-12) menunggu kartu, dan pembacaan PDF primer/BR-11 tetap wewenang manusia. Bukti ukur: docs/2026-09-28-sdcy-knowledge-register/lib/d1-l2-evidence/custodian-d1l2-iter2-check.py, custodian-d1l2-iter2-check4.py, backup-pra-custodian-iter2.md."
sumber: "docs/2026-09-28-sdcy-knowledge-register/research/cybersecurity-korpus-detail.md (hulu: 5 berkas domain + 4 kartu REF-SEC dibaca penuh + 16 pendukung, terdaftar di Bagian 1 objek)"
halaman: "marker [R-n, sumber, hal] per butir di body: Alsmadi PDF 266-268 (proses forensik 4 tahap + rantai kustodi), PDF 20, 59, 77, 326, 343; Anderson PDF 17, 57, 187, 279, 437, 502, 798, 846, 889; Johnson (adjacent CRITICAL-INFRASTRUCTURE) selisih tetap +18; koordinat lapis teks ditulis 'baris N'"
tanggal_akses: 2026-09-28
kelas_bukti: sintesis
sensitif: tidak
perkara: sdcy-0928
tags: [cybersecurity, keamanan-siber, forensik-digital, rantai-kustodi, ancaman, model-ancaman, rbac, nice-framework, kendali-akses, jejak-audit, mutu-log, pengerasan-ad, tanggap-insiden, audit-siber, kepatuhan, batas-kepatuhan]
links: [ekas/05_DOMAIN-KNOWLEDGE/CYBERSECURITY, ekas/05_DOMAIN-KNOWLEDGE/CRITICAL-INFRASTRUCTURE, docs/2026-09-28-sdcy-knowledge-register/research/cybersecurity-korpus-detail.md]
defek-terkait: register kontradiksi misi K-1..K-13 tercantum di Bagian 6 objek ini; penandaan di lapis rak menunggu kartu D1-FIXx (S-12) - vonis rilis domain ditahan sampai tanda terpasang
penulis: gsp-security-specialist
diajukan: 2026-09-28
domain: CYBERSECURITY
created: 2026-09-28
riwayat-catatan-verifikasi: "Perlu_revisi (custodian gsp-custodian, 2026-09-28). Enam dimensi lolos: frontmatter utuh (yaml OK, 17 kunci, satu baris status, title==H1, tags 16 token, uji potong-# bersih); provenans kuat (50 koordinat baris diuji ke rak nyata: 49 cocok, 1 miss terbukti false-negative needle verifier sendiri; byte 11/11 PDF nyata cocok persis; 29.258 B domain dan 7.096 B kartu cocok; token nol tier/CSF/800-181/800-53/OWASP/write-blocker terukur 0); kesetiaan hulu pada butir beban (label kerangka R3 bukan norma, rujukan silang digital-forensics-evidence-system, model ancaman dulu Anderson PDF 17, 800-50r1 R5-bundel, konvensi halaman satu-per-buku); anatomi 8 bagian lengkap; blok BATAS utuh tanpa perataan (PUTUS mata 4, tiga baris tak teruji, tabel boleh/tidak-boleh, Pernyataan Batas Kepatuhan, GAP-002/003/006/007+GAP-014, pointer adjacent Johnson OQ-3 tanpa peleburan); register K-1..K-13 dan BR-1..BR-13 utuh, kontradiksi ditandai bukan disembunyikan, defek-terkait menunjuk D1-FIXx; kebersihan non-ASCII=0 dan semua jalur rak ada di disk. Dua temuan kelas-ukur wajib dikoreksi sebelum promosi: (1) Bagian 6.1 menyebut sebutan nama CIS Controls muncul tepat 1 kali, terukur 3 kali pada lima berkas domain (resume tesis baris 70, 76, 95) dan 4 kali se-ekas; studi hulu memakai pola 'CIS Controls v<n>' yang memang 1 - pulihkan pembatas pola v<n> atau nyatakan 3 kemunculan dengan rincian; (2) Bagian 8 butir 6 menyebut tahun edisi Anderson dan Alsmadi tidak tercatat di lapis teks resume, padahal resume Alsmadi baris 3 mencatat Springer 2019 dan RANTAI-JAMINAN baris 17-18 mencatat Anderson 2020 serta Alsmadi 2019 - ubah redaksi menjadi tahun Anderson absen di resume (hanya Edisi ketiga Wiley) tetapi ada di tabel rantai. Temuan INFO: Bagian 2 token retensi/SIEM=0 sah untuk lingkup lima berkas domain, nyatakan lingkup itu karena se-ekas retensi=6 di luar domain siber. Nol angka teknik berubah, nol kebocoran BR-11, nol fabrikasi; koreksi bersifat dua kalimat agregat ukur. Bukti ukur: docs/2026-09-28-sdcy-knowledge-register/lib/d1-l2-evidence/custodian-d1l2-verify.py, custodian-d1l2-probe2.py, custodian-d1l2-probe3.py, backup-pra-custodian.md."
catatan_keputusan: "dipromosikan: SDCY-0928 D1-L2: gerbang format librarian 9/9 PASS (validator mandiri: byte-identik, yaml utuh, potong-#, title==H1, tags 16, non-ASCII=0), verdict custodian terlampir di catatan_verifikasi, non-sensitif non-dosir; blok status rantai PUTUS @4 terbit apa adanya sesuai S-8"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-28
dipromosikan-ke: catatans/cybersecurity-korpus-ekas-0928.md
---

# Korpus CYBERSECURITY EKAS - peta, rumus, ambang, dan batas pengetahuan (SDCY-0928)

Objek master misi SDCY-0928 (id `cybersecurity-korpus-ekas-0928`, type catatan, domain
CYBERSECURITY = D1). Muatan = peta rak + angka acuan + kerangka penilaian + ambang terima +
register kontradiksi + celah resmi + batas kemampuan, dalam satu berkas (granularitas SATU
objek master per domain sesuai kebijakan skema beku; dokumen `skema-objek-sdcy.md` belum ada
di disk saat body ini disusun - bentuk mengikuti preseden NWSKILL-0923 G-1 seksi 1-8, dicatat
sebagai deviasi di kartu D1-L1).

Provenans: body ini disalin terpadatkan dari SATU sumber,
`docs/2026-09-28-sdcy-knowledge-register/research/cybersecurity-korpus-detail.md` (studi
t_30d502a0 status complete, 565 baris, 50.120 B, ekstraksi read-only dari lapisan teks `ekas/`
oleh gsp-security-specialist pada 2026-09-28; bukti ukur `research/sec/measurement-report.txt`,
timestamp 2026-09-28T09:39:54). Tidak ada pembacaan ulang korpus untuk angka baru pada giliran
ini. Kelas bukti objek: sintesis - kekuatan utama R3 buku (Anderson, Alsmadi) dicampur R5
penunjuk (4 tesis UI, 4 panduan operasional); pemisahannya ditegakkan lewat penanda
`[R-n, sumber, hal]` per butir dan blok BATAS PENGETAHUAN di Bagian 8. Yang tidak ada di rak
dinyatakan "tidak ada di rak".

PERNYATAAN BATAS KEPATUHAN (wajib ikut terbit; [R3, RANTAI-JAMINAN.md baris 108]): korpus ini
TIDAK dapat menyatakan kepatuhan terhadap ISO/IEC 27001, ISO/IEC 27002, ISO/IEC 27037,
NIST SP 800-86, Peraturan BSSN No. 4/2021, maupun UU No. 11/2008 (ITE), karena salinan resmi
dokumen-dokumen itu tidak ada di rak (nol R1, nol R2 untuk domain ini). Setiap pekerjaan yang
memakai objek ini wajib membawa pernyataan ini apa adanya; gerbang G6 menuntutnya tertulis di
bukti serah ([R3, ASSURANCE-GATES.md baris 176-190]).

Catatan wewenang: tidak ada PDF primer yang dibuka pada misi ini. Semua vonis halaman adalah
vonis LAPISAN TEKS memakai konvensi per buku (Bagian 3.4); penutup akhir wewenang manusia.
PDF asli ada di `C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/` (lokasi nyata terukur;
laci `ekas/03_SOURCE-VAULT/` di workspace hanya cermin - lihat K-6).

---

## Bagian 1 - Peta isi

Path memakai NAMA FOLDER NYATA di disk. Label katalog berbentuk `R3/SECURITY/`, `_tesis/`,
`_panduan/` yang masih muncul di lapis teks adalah label laci lama rak asal, BUKAN path hari
ini (kontradiksi K-11); padanan nyatanya dicantumkan di 1.4. Uji keberadaan = baca
langsung/ls, bukan glob.

### 1.1 Lapis domain `ekas/05_DOMAIN-KNOWLEDGE/CYBERSECURITY/` (5 berkas, 607 baris, 29.258 B terukur)

| Berkas | Peran | Tingkat R | Isi puncak |
|---|---|---|---|
| `RANTAI-JAMINAN.md` (132 baris, 7.337 B) | Rantai J: urutan kerja mata 1-5 keamanan siber + bukti digital | peta pengetahuan, PUTUS di mata 4 | rujukan, keputusan desain, penilaian, pengujian, bukti serah |
| `R3 - Security Engineering.md` (122 baris, 5.831 B) | Resume Anderson edisi 3; kerangka berpikir keamanan sistem | R3 | peta 29 bab + bibliografi, pemetaan keperluan GSP |
| `R3 - The NICE Cyber Security Framework.md` (127 baris, 5.204 B) | Resume Alsmadi; struktur fungsi kerja + forensik | R3 | peta 13 bab, proses forensik 4 tahap, KSA, tanggap insiden |
| `R5 - Keamanan Siber dan Forensik Digital (Universitas Indonesia).md` (112 baris, 5.523 B) | Resume gabungan 4 tesis UI; penunjuk regulasi Indonesia | R5 | Wirara, Hakim, Mulyana, Bashofi + batas keempatnya |
| `R5 - Keamanan Siber Operasional.md` (114 baris, 5.363 B) | Resume gabungan 4 panduan kerja operasional | R5 | ASD-CISA AD, Joint CSI logging, NIST SP 800-50r1, ITSECBuzz |

### 1.2 Lapis kartu `ekas/04_KNOWLEDGE-CARDS/CYBERSECURITY/` (4 x 59 baris, total 7.096 B terukur; satu templat enam seksi)

| Kartu | R | Status otoritas | Bobot rujukan | Halaman jangkar | Boleh tetapkan ambang |
|---|---|---|---|---|---|
| `REF-SEC-001.md` | R3 | ACTIVE | Alsmadi - proses forensik 4 tahap + rantai kustodi (baris 22) | PDF 268 (baris 24) | tidak sendirian, hanya bila kontrak mengadopsi tertulis (baris 37) |
| `REF-SEC-002.md` | R3 | ACTIVE | Anderson - kerangka keamanan sistem + integritas catatan (baris 22) | kosong (baris 24) | idem |
| `REF-SEC-003.md` | R5 | POINTER_ONLY | hardening AD, event logging, threat detection, program pembelajaran (baris 22) | kosong (baris 24) | TIDAK PERNAH (baris 37) |
| `REF-SEC-004.md` | R5 | POINTER_ONLY | penunjuk UU 11/2008 (ITE) + Peraturan BSSN No. 4/2021 (baris 22) | kosong (baris 24) | TIDAK PERNAH (baris 37) |

Struktur: 3 dari 4 kartu TANPA halaman jangkar - hanya REF-SEC-001 yang bisa diuji alamatannya
dari lapis kartu. Seksi "rumus/metode" kosong (tanda hubung) di keempat kartu, konsisten dengan
sifat domain tanpa perhitungan [R3, RANTAI-JAMINAN.md baris 52]. Klasifikasi ini cocok dengan
`MASTER-REFERENCE-REGISTER.csv:23-26` (READY, BR-2).

### 1.3 Lapis bersama (baris terkait keamanan siber)

| Berkas | Baris | Yang dipasok |
|---|---|---|
| `ekas/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md` | 570 | penanganan bukti digital (chain of custody) = status sebagian; proses 4 tahap Alsmadi Bab 11 PDF 268; standar aslinya belum |
| `KATALOG-RUMUS.md` | 572-573 | dasar hukum bukti elektronik + kriteria audit siber instansi = PENUNJUK saja (tesis); kutip regulasi aslinya |
| `KATALOG-RUMUS.md` | 574 | mutu pencatatan log ditandai centang "Joint CSI (2024)" - nada beda dengan rantai (K-8; versi rantai yang sah) |
| `KATALOG-RUMUS.md` | seluruh berkas | nol rumus keamanan siber - hanya 4 baris tabel + 1 baris peta di atas |
| `ekas/06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md` | - | nol seksi keamanan siber (ukur token siber/cyber/forensik/kustodi/insiden/SLA = 0); waktu tanggap insiden dan retensi log TIDAK terdaftar sebagai asumsi baku |
| `ekas/07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/AMBANG-TERIMA-INDUK.md` | seluruh berkas | nol baris keamanan siber, termasuk bagian "Belum ada sumber sah" (baris 75-87) - cacat kelengkapan silang K-10 |
| `ekas/02_REGISTERS/GAP-REGISTER.csv` | 3, 4, 7, 8 | GAP-002 (R1 UU 11/2008, TINGGI), GAP-003 (R1 Perban BSSN 4/2021, TINGGI), GAP-006 (R2 ISO/IEC 27001 & 27002, TINGGI, "sering jadi syarat tender"), GAP-007 (R2 NIST SP 800-86 + ISO/IEC 27037, TINGGI, sebagian) |
| `ekas/02_REGISTERS/GAP-ACQUISITION-PLAN.md` | 25-26, 49, 114-116, 138-142, 188 | rencana penutupan: 800-86 tersedia bebas; 27037 pedoman identifikasi/pengumpulan/pengawetan bukti; jalur tercepat menaikkan rantai J ke R2 |
| `ekas/01_GOVERNANCE/AUTHORITY-STATUS.md` | 48-50, 52-58 | tabel POINTER_ONLY (Wirara -> pasal UU ITE; Bashofi -> Perban BSSN; bundel `_panduan/` -> dokumen aslinya); catatan penurunan 800-50r1 |
| `ekas/01_GOVERNANCE/ASSURANCE-GATES.md` | 160-190 | rantai J = contoh kanonik rantai putus: pekerjaan jalan dengan R3+R5 asalkan G6 memuat pernyataan batas kepatuhan |
| `ekas/00_START-HERE/DOCUMENT-CONTROL.md` | 114-116 | butir terbuka: pemecahan bundel `_panduan` tertunda karena mengubah penomoran REF-SEC |
| `ekas/00_START-HERE/CHANGELOG.md` | 307-320, 325, 339-342, 392-394, 481-483, 486-493 | T16 batch 8 berkas ringan; T17 dua buku utuh diproses penuh (Alsmadi 366 hal, Johnson 346 hal); "Tesis != regulasi"; bundel menyeret 800-50r1 ke R5; "EKAS cermin, bukan pengganti rak" |

### 1.4 Lapis laci sumber - jalur logis vs fisik nyata (keadaan cermin, K-6)

Klaim `_ISI.md` menyebut "berkas fisik sudah berada di laci ini" (baris 3 tiap `_ISI.md`) -
BENAR terhadap rak asal, SALAH terhadap mirror workspace: 0 PDF di laci `ekas/`; PDF nyata di
pohon `gsp-ekas/lengkap` (ukuran byte terukur `sec_measure.py` bagian [6]):

| Laci logis | PDF nyata di `C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/` | Ukuran terukur |
|---|---|---|
| `R3_TEXTBOOK-HANDBOOK/SECURITY/` (klaim 2) | Alsmadi; Anderson | 16.510.151 B; 15.460.905 B |
| `R3_TEXTBOOK-HANDBOOK/CRITICAL-INFRASTRUCTURE/` (klaim 1) | Johnson | 1.837.175 B |
| `R5_RESEARCH-SECONDARY/THESIS/` (klaim 4) | Hakim; Wirara; Bashofi; Mulyana | 5.798.912 B; 8.762.368 B; 4.460.544 B; 4.259.840 B |
| `R5_RESEARCH-SECONDARY/TECHNICAL-GUIDES/` (klaim 4) | ASD-CISA; ITSECBuzz; Joint CSI; NIST SP 800-50r1 | 2.437.233 B; 14.072.308 B; 1.025.298 B; 2.428.672 B |

Tabel PDF primer (judul, jumlah halaman KLAIM RESUME - verifikasi per halaman = wewenang
manusia; agen bekerja dari lapisan teks): Anderson Security Engineering edisi 3, 1.044 halaman
[R3, resume Security Engineering, baris 4]; Alsmadi The NICE Cyber Security Framework, 366
halaman [R3, resume The NICE..., baris 5]; empat tesis UI total 430 halaman (Wirara 90, Hakim
89, Mulyana 80, Bashofi 171) [R5, resume Forensik Digital UI, baris 4,28,46,57,70]; empat
panduan total 238 halaman (ASD-CISA 86, Joint CSI 17, 800-50r1 87, ITSECBuzz 48) [R5, resume
Keamanan Siber Operasional, baris 3,11-14]; Johnson (adjacent) 346 halaman [R3, resume
Cybersecurity Protecting Critical Infrastructures, baris 4].

Catatan laci tetangga: laci `R3_TEXTBOOK-HANDBOOK/SOFTWARE-DATA/` kosong (makalah dipindah ke
R5/PAPERS 21-08, GAP-021) - TIDAK relevan untuk domain CYBERSECURITY; disebut hanya agar agen
tidak mencari buku software/data di sekitar rak ini.

---

## Bagian 2 - Domain ini tidak punya rumus; yang ada penilaian berlabel

Rantai J menyatakan eksplisit: "Domain ini hampir tanpa perhitungan. Yang ada bersifat
penilaian, bukan rumus" [R3, RANTAI-JAMINAN.md baris 52]. Tidak ada satu pun angka domain ini
yang boleh naik sebagai ambang lulus/tidak lulus - mustahil secara struktural (nol R1, nol R2;
ambang terima menuntut R1/R2 [README.md baris 72]; R5 tidak pernah menetapkan ambang
[README.md baris 27]).

| Kerangka | Bentuk | Sifat wajib label | Sumber |
|---|---|---|---|
| Prioritas risiko | kemungkinan x dampak | kualitatif/semi-kuantitatif; WAJIB diberi label metode internal; angka keluaran bertanda PROJECT-DERIVED | [R3, RANTAI-JAMINAN.md baris 56,61-63] |
| Matriks cakupan sumber log | sumber log vs taktik terpantau | metode internal | [R3, RANTAI-JAMINAN.md baris 57] |
| Matriks kompetensi personel | peran vs KSA | metode internal | [R3, RANTAI-JAMINAN.md baris 58; Alsmadi PDF 20, 77] |
| Waktu tanggap insiden | dari kontrak/SLA | BUKAN dari buku; tidak terdaftar di ASUMSI-BAKU | [R3, RANTAI-JAMINAN.md baris 59] |

Peringatan rak atas kerangka pertama, wajib ikut terbit: "Skor risiko yang tampak seperti angka
objektif padahal hasil penilaian sendiri adalah bentuk penyesatan yang paling halus"
[R3, RANTAI-JAMINAN.md baris 61-63].

Hitung yang rak nyatakan TIDAK bisa dikerjakan: ambang lulus kepatuhan apa pun (mata 4 putus);
angka keterterimaan bukti pengadilan (UU ITE tidak ada); skor risiko "objektif"; SLA tanpa
kontrak; retensi log / jumlah sumber log minimum / rasio personel SOC = nol angka di rak (ukur
token retensi/SIEM = 0 pada lima berkas domain CYBERSECURITY; se-ekas "retensi" = 6 kemunculan,
semuanya di luar domain siber, mis. ASUMSI-BAKU.md baris 105 konteks sistem video - bukan
retensi log siber).

---

## Bagian 3 - Angka acuan per buku + konvensi halaman

### 3.1 Anderson, Security Engineering edisi 3 [R3]

| Butir | Nilai | Koordinat |
|---|---|---|
| Ukuran | 1.044 halaman, 14,7 MB (klaim resume); 15.460.905 B terukur | resume baris 4; ukur [6] |
| Bookmark | 31 entri; judul diperbaiki 19-08-2026; halaman tujuan sudah benar sejak awal | resume baris 7,117-119 |
| Jangkar bab (nomor PDF) | Bab 2 PDF 17; Bab 3 PDF 57; Bab 6 PDF 187; Bab 9 PDF 279; Bab 14 PDF 437; Bab 17 Biometrik PDF 502; Bab 26 PDF 798; Bab 27 PDF 846; Bab 28 PDF 889 | resume baris 26-38 |
| Cadangan pra-perbaikan `_asli/` | diklaim resume baris 122; TIDAK ditemukan di vault lengkap (sapuan find = 0) | BELUM TERKONFIRMASI (K-7, BR-13) |

### 3.2 Alsmadi, The NICE Cyber Security Framework [R3]

| Butir | Nilai | Koordinat |
|---|---|---|
| Ukuran | 366 halaman, 15,7 MB (klaim); 16.510.151 B terukur | resume baris 5; ukur [6] |
| Konversi halaman | selisih cetak-PDF TIDAK TETAP, +16 s.d. +18; selalu pakai nomor PDF | resume baris 8-9,127 |
| Bookmark bawaan | 458 entri sampai sub-bagian | resume baris 9 |
| Orientasi NICE | berorientasi PEKERJAAN bukan pendidikan; KSA ganti capaian pembelajaran (PDF 20) | resume baris 11-14 |
| Proses forensik | EMPAT tahap: collection, examination, analysis, reporting (Gambar 11.1) | resume baris 48-55; Alsmadi PDF 266-268 |
| Rantai kustodi | dalam konteks penyitaan + pengawetan bukti digital | Alsmadi PDF 268; resume baris 57-58 |
| Peta bab kunci | Bab 3 PDF 59; Bab 11 PDF 266 (inti lini DEMS); Bab 12 PDF 326; Bab 13 Incident Response PDF 343 | resume baris 28,36-38 |
| Kemampuan tim investigasi | teknis DAN hukum/regulasi, bukan salah satu | Alsmadi PDF 77; resume baris 70-77 |
| Batas | buku AJAR bukan standar; NICE asli (NIST SP 800-181), NIST SP 800-86, ISO/IEC 27037 ketiganya belum ada di rak | resume baris 121-122 |

LABEL-GUARD wajib (BR-8, K-9): judul buku Alsmadi mengandung "NICE Cyber Security Framework"
tetapi buku ini adalah BUKU AJAR yang mengikuti kerangka, bukan kerangka aslinya; NIST SP
800-181 tidak ada di rak (token `SP 800-181` = 0 di seluruh ekas). Hilir DILARANG menafsirkan
"rak punya NICE Framework".

### 3.3 Lapis R5 (penunjuk saja - tidak pernah menetapkan ambang)

Empat tesis UI [R5]: Wirara 2021 (90 hal; NIST SP 800-101 + kutipan UU 11/2008 ITE)
[resume Forensik Digital UI baris 28-42]; Hakim 2021 (89 hal; forensik aplikasi Android)
[:44-53]; Mulyana 2021 (80 hal; Cyber Kill Chain + Elastic Stack, studi kasus LKPP) [:55-66];
Bashofi 2023 (171 hal; NIST CSF + CIS Controls v8 diselaraskan Peraturan BSSN No. 4/2021)
[:68-81]. Uji aritmetika total: 90+89+80+171 = 430 COOK (ukur [4]). Catatan generalisasi
(K-12): hanya 2 dari 4 tesis adalah penunjuk regulasi (Wirara -> UU ITE; Bashofi -> Perban
BSSN); redaksi rantai "4 tesis ... penunjuk ke UU 11/2008 dan Perban BSSN" melebihkan cakupan.

Empat panduan operasional [R5]: ASD-CISA Detecting and Mitigating AD Compromises (86 hal,
Sep-2024; daftar periksa audit AD) [resume Keamanan Siber Operasional baris 11,18-32]; Joint
CSI Best Practices for Event Logging (17 hal, 2024; mutu log + rincian wajib tertangkap,
"paling langsung terpakai untuk lini DEMS") [:12,34-48]; NIST SP 800-50r1 (87 hal; program
pembelajaran berkelanjutan) [:13,50-60]; ITSECBuzz Edisi II (48 hal, Okt-2024; UU PDP, malware
Android, dark web - BACAAN LATAR, bukan rujukan) [:14,62-74]. Uji aritmetika total:
86+17+87+48 = 238 COOK (ukur [4]).

LABEL-GUARD wajib (BR-9, S-13): NIST SP 800-50r1 terbit di objek ini sebagai **R5 karena
bundel campur** `_panduan` bersama majalah ITSECBuzz, BUKAN karena dokumennya lemah;
kemungkinan layak R2 bila dipecah, pemecahan tertunda karena mengubah penomoran REF-SEC
[R5, AUTHORITY-STATUS.md baris 52-58; DOCUMENT-CONTROL.md baris 114-116; CHANGELOG.md baris
481-483]. Aturan pakai: kutip dokumen aslinya terpisah, jangan kutip bundel; DILARANG
menyajikan 800-50r1 sebagai R2.

Johnson (ADJACENT, domain CRITICAL-INFRASTRUCTURE, provenance terpisah): 346 halaman,
1.837.175 B terukur; selisih cetak-PDF TETAP +18 lolos uji aritmetika 7/7 baris peta isi;
bookmark 14 entri [R3, resume Cybersecurity Protecting Critical Infrastructures, baris 4,7-8,
21-29; ukur [4]]. Keanggotaan ganda dengan rantai J (K-4) divisium sebagai rujukan lintas
domain; penyerapan ke objek ini TIDAK dilakukan (belum ada putusan controller OQ-3) - hanya
pointer di Bagian 8.

### 3.4 Konvensi halaman (SATU konvensi per buku, berlaku identik di semua lapis)

| Buku | Konvensi sah | Perlakuan sitasi |
|---|---|---|
| Anderson, Security Engineering 3 | nomor PDF langsung (dinyatakan di kepala resume) | kutip nomor PDF apa adanya |
| Alsmadi, NICE Cyber Security Framework | selisih cetak-PDF TIDAK tetap (+16 s.d. +18) | kutip nomor PDF langsung; DILARANG konversi dari nomor cetak |
| Johnson (adjacent) | selisih TETAP +18 (uji 7/7) | cetak+18 = PDF |

Beda konvensi antar lapis = defect (kelas "Offset halaman per buku", preseden NWSKILL seksi 7).
Untuk proses forensik + kustodi, objek ini memakai RENTANG **PDF 266-268** saat menyebut
"proses + kustodi" dan **PDF 268** hanya untuk kalimat kustodi/penyitaan (adjudikasi K-3:
rentang bab vs jangkar kartu, komplementer bukan kontradiksi).

---

## Bagian 4 - Kerangka terapan

### 4.1 Rantai argumen keamanan: enam keputusan, semuanya menyebut alternatif yang ditolak

Urutan baku mata 2 rantai J [R3, RANTAI-JAMINAN.md baris 34-42]:

1. Model ancaman ditetapkan LEBIH DAHULU [R3, Anderson PDF 17]. Menetapkan kendali sebelum
   ancaman ditolak - menghasilkan kendali mahal dan tidak mengena.
2. Kendali akses dan pemisahan hak [R3, Anderson PDF 187, 279]. Satu peran administrator untuk
   semua ditolak.
3. Jejak audit tidak dapat disangkal [R3, Anderson PDF 437]. Log yang dapat disunting
   administrator ditolak - pada sistem bukti digital itu membatalkan nilainya.
4. Proses penanganan bukti 4 tahap [R3, Alsmadi PDF 266-268]. Menyalin bukti tanpa rantai
   kustodi ditolak.
5. Kebijakan mutu log [R5, Joint CSI 2024]. Mencatat semuanya tanpa kebijakan ditolak.
6. Pengerasan identitas AD [R5, ASD-CISA]. Setelan bawaan ditolak.
7. Kriteria kepatuhan HARUS R1/R2. Menjanjikan kesesuaian ISO 27001 tanpa salinan ditolak -
   baris yang oleh rak disebut "keputusan paling berbahaya di seluruh rak"
   [R3, RANTAI-JAMINAN.md baris 44-46].

### 4.2 Proses forensik 4 tahap + rantai kustodi - KERANGKA R3, BUKAN NORMA

Empat tahap berurutan: collection -> examination -> analysis -> reporting, disertai rantai
kustodi (siapa memegang, kapan, di mana, hash di setiap transisi) [R3, Alsmadi PDF 266-268;
R3, RANTAI-JAMINAN.md baris 18,39; R3, REF-SEC-001.md baris 22,24]. Status: KERANGKA PROSES
dari buku ajar - norma penanganannya (NIST SP 800-86, ISO/IEC 27037) TIDAK ada di rak
(GAP-007 status sebagian) sehingga kalimat apa pun tentang proses ini wajib membawa label
"kerangka R3, bukan norma" (BR-1 LABEL-GUARD).

### 4.3 Pembagian kerja dengan skill fleet (rujukan silang, BUKAN duplikasi isi)

Korpus ini dan skill fleet berbagi SATU sandaran angka yang sama (Alsmadi Bab 11 PDF 266-268).
Pembagian kerja yang mengikat lapis hilir:

| Lapis | Punya siapa | Isi |
|---|---|---|
| Kerangka proses + rantai kustodi + batas normatif | objek IL ini (korpus EKAS) | fakta rak: empat tahap, PDF 266-268, GAP-007 sebagian, larangan klaim kepatuhan |
| Prosedur pelaksanaan: formulir kustodi terisi, hash SHA-256 tiap transisi, write-blocker, kerja pada salinan forensik, media asli = bukti prima | skill fleet `digital-forensics-evidence-system` (jalur DEMS) | instruksi kerja. CATATAN JUJUR: write-blocker dan SHA-256 TIDAK berasal dari korpus (ukur token `write.?blocker` = 0 di seluruh ekas) - objek IL ini TIDAK mengklaim rak memasok prosedur tersebut |
| Rakitan proposal DEMS | skill fleet `dems-polri-proposal-architect` | konsumen kedua lapis di atas |

### 4.4 Bukti serah mata 5 (sembilan lampiran wajib/kondisional)

Dokumen model ancaman; matriks peran & hak akses; rancangan & bukti integritas jejak audit;
formulir rantai kustodi (kerangka dari Alsmadi PDF 268); dasar konfigurasi pengerasan beserta
penyimpangan disetujui; matriks sumber log + contoh peringatan; rekaman pelatihan
(`09_HANDOVER/TRAINING/` - direktori terkonfirmasi ada); laporan uji penetrasi bila disyaratkan;
PERNYATAAN BATAS KEPATUHAN (WAJIB); kartu kendali rantai berstatus "putus di mata 4"
[R3, RANTAI-JAMINAN.md baris 98-109].

---

## Bagian 5 - Ambang terima: apa yang boleh dan tidak boleh dikatakan

### 5.1 Tabel uji rantai J mata 4 [R3, RANTAI-JAMINAN.md baris 69-78], disalin utuh

| Butir | Ambang | Kelas sumber |
|---|---|---|
| Pengerasan identitas / AD | Daftar periksa ASD-CISA | peringatan R5 - bukan sandaran sah |
| Mutu & kelengkapan pencatatan log | Panduan Joint CSI | peringatan R5 |
| Verifikasi integritas jejak audit | Rancangan mata 2 | R3 + kontrak |
| Rantai kustodi bukti digital | Proses 4 tahap Alsmadi | peringatan R3 - kerangka, bukan norma |
| Uji penetrasi | Lingkup & kriteria dari kontrak | Kontrak |
| Kepatuhan ISO/IEC 27001 | TIDAK DAPAT DIUJI | Standarnya tidak ada |
| Kepatuhan Perban BSSN 4/2021 | TIDAK DAPAT DIUJI | Regulasinya tidak ada |
| Keterterimaan bukti di pengadilan | TIDAK DAPAT DINYATAKAN | UU ITE tidak ada |

"Baris-baris terakhir yang membuat rantai ini putus. Ketiganya justru yang paling sering diminta
pada tender DEMS dan sistem keamanan instansi." [R3, RANTAI-JAMINAN.md baris 80-81]. Kelas R5,
R3, dan kontrak dilarang diratakan menjadi "standar"; hanya R1/R2 sah jadi ambang terima
[README.md baris 23-27].

### 5.2 Kata "boleh / tidak boleh dikatakan" (redaksi operasional untuk editor proposal)

Tabel berikut menyalin `RANTAI-JAMINAN.md:85-89` (normalisasi tipografi ASCII). Kalimat di
kolom kanan adalah CONTOH TERLARANG - dikutip di sini semata sebagai penanda larangan, bukan
untuk dipakai:

| Boleh dikatakan | TIDAK BOLEH dikatakan (terlarang) |
|---|---|
| "Rancangan mengikuti proses penanganan bukti empat tahap beserta rantai kustodi [R3, Alsmadi PDF 266-268]." | klaim pemenuhan ISO/IEC 27037 atas dasar rak ini |
| "Kebijakan pencatatan log disusun mengacu panduan Joint CSI 2024 [R5]; standar normatifnya belum diadopsi." | klaim "sesuai standar internasional penanganan bukti" |
| "Kriteria audit mengacu Perban BSSN 4/2021 - salinan regulasi diperoleh terpisah dan dilampirkan." | klaim "sesuai Peraturan BSSN" dengan menyandarkan pada tesis |

Aturan turun-temurun (CG-8): di SEMUA lapis objek/rute/laporan ini DILARANG ada kalimat yang
menyatakan kepatuhan ISO 27001 / ISO 27037 / Peraturan BSSN sebagai pernyataan positif.

### 5.3 Mekanisme gerbang untuk rantai putus

Domain tanpa satu pun R1/R2 tidak dapat melewati G4 dengan cara biasa; pekerjaan tetap boleh
jalan dengan kerangka R3 + panduan R5 ASALKAN gate G6 memuat pernyataan batas kepatuhan yang
menyebut standar mana yang belum dapat dibuktikan [R3, ASSURANCE-GATES.md baris 176-190;
RANTAI-JAMINAN.md baris 108]. Tiga jalan sah penutupan (pola rantai D): pemilik menetapkan
ambang tertulis; kontrak menyebut standar lalu salinannya diperoleh; atau laporkan hasil tanpa
pernyataan lulus.

### 5.4 Kedudukan di ambang induk: NOL baris

`AMBANG-TERIMA-INDUK.md` tidak punya satu pun baris keamanan siber, termasuk di bagian "Belum
ada sumber sah" (baris 75-87) - terukur. Konsekuensi: objek ini tidak bisa menunjuk baris induk
sebagai rumah ambang; pernyataan "tidak dapat diuji"-nya hidup penuh di rantai J dan
ASSURANCE-GATES. Cacat kelengkapan silang ini tercatat sebagai K-10; perbaikan (penambahan
baris) wewenang librarian/pengelola rak, bukan objek ini.

---

## Bagian 6 - Register kontradiksi + tabel beban-rilis

### 6.1 Temuan kelas-nol (jawaban atas kelas yang diminta blueprint)

Sapuan kelima berkas domain (`sec_measure.py` bagian [8]): pola penulisan nomor versi NIST CSF,
pola penyebutan tingkat (tier) NICE, pola angka jumlah kategori CIS Controls, dan pola nomor
publikasi NIST SP 800-181 = NOL SEMUA; pola berversi "CIS Controls v<n>" muncul tepat 1 kali
(satu-satunya: "CIS Controls v8" pada judul tesis Bashofi, tanpa angka jumlah kategori apa pun; sebutan polos "CIS Controls"
tanpa versi muncul 3 kali di berkas yang sama - baris 70, 76, dan 95 resume tesis). Jadi untuk
kelas versi NIST CSF, tier NICE, jumlah
kategori CIS Controls v8, dan ambang BSSN: **lapis teks tidak memuat angkanya sama sekali**;
satu-satunya tempat angka-angka itu adalah PDF Bashofi (R5, belum dibuka manusia). Vonis:
tidak ada yang bisa dikontradiksikan dari rak, dan karena itu angka kelas itu DILARANG TERBIT
dari objek ini (BR-11). Pertanyaan "berapa fungsi CSF / kategori CIS / tier NICE menurut rak?"
dijawab benar hanya dengan "tidak ada di rak". Nama dokumen (CIS Controls, NIST CSF, NIST SP
800-181) boleh disebut hanya sebagai nama + status ketiadaan, bukan dengan angka isinya.

### 6.2 Register kontradiksi K-1..K-13 (koordinat = jalur:baris hasil ukur studi)

| ID | Butir | Bukti | Vonis sementara | Bebani rilis |
|---|---|---|---|---|
| K-1 | Keadaan rak per tingkat README vs register hidup | `README.md:34-38` (R1 0, R2 5, R3 24, R4 0, R5 8) vs `MASTER-REFERENCE-REGISTER.csv` terukur (R1 0, R2 4, R3 49, R4 6, R5 3; 62 baris) | KONTRADIKSI terukur; angka README jangan dikutip sebagai fakta | ya |
| K-2 | "Empat celah R1" README vs isi GAP-REGISTER | `README.md:48` vs terukur 9 baris R1 (CYBERSECURITY menyumbang GAP-002,003) | KONTRADIKSI terukur; kalimat "empat celah" basi, jangan ikut terbit | ya |
| K-3 | Rentang PDF 266-268 vs jangkar tunggal PDF 268 | rantai `:18,39,74,87`; `KATALOG:570` vs resume `:36,48-58` | Komplementer; aturan pakai di 3.4 | tidak |
| K-4 | Johnson di dua domain | `RANTAI-JAMINAN.md:19` vs `MASTER-REFERENCE-REGISTER.csv:4` | Tumpang tindih keanggotaan terukur; tunggu putusan controller (OQ-3) | ya |
| K-5 | Catatan "dua buku ditahan di New folder, belum diproses" | `R5 - Keamanan Siber Operasional.md:100-111` vs Alsmadi/Johnson sudah ACTIVE (`MASTER...csv:23,4`; CHANGELOG T17 `:325,339-342`) | CATATAN BASI - jangan pernah diulang ke hilir | ya |
| K-6 | Klaim "_ISI.md: berkas fisik sudah di laci ini'" vs 0 PDF di laci workspace | ukur bagian [6]; `CHANGELOG.md:486-493` | Cermin vs rak asal; objek membawa jalur ganda (1.4) | ya |
| K-7 | Bookmark Anderson 31 entri vs 30 target peta isi; cadangan `_asli/` hilang | resume `:7,25-39,122`; sapuan find = 0 | CALON - butuh buka PDF primer oleh manusia | tidak (tidak naik sebagai angka) |
| K-8 | Centang katalog vs peringatan R5 untuk mutu log | `KATALOG:574` vs `RANTAI:40,72` | Inkonsistensi presentasi; objek membawa versi rantai | ya (label) |
| K-9 | Judul buku "NICE Framework" vs kerangka asli tidak di rak | `REF-SEC-001.md:5`; resume `:121-122`; token 800-181 = 0 | Risiko ambiguitas nama; LABEL-GUARD BR-8 | ya (label) |
| K-10 | Rantai butuh baris "belum ada sumber sah"; induk tidak punya | `RANTAI:22-25,76-78` vs `AMBANG-TERIMA-INDUK.md:75-87` | Cacat kelengkapan silang; usulan tambal wewenang librarian | ya (jalur gerbang) |
| K-11 | Label path warisan (`R3/SECURITY/`, `_tesis/`, `_panduan/`, dll.) di lapis teks | `RANTAI:19-21`; resume Anderson `:108-110`; resume NICE `:113-115,124`; resume tesis `:66,98`; resume panduan `:48` | Cacat penamaan kelas K-11 NWSKILL; path nyata 1.4 yang dipakai | ya |
| K-12 | Generalisasi "4 tesis -> dua regulasi" | `RANTAI:21` vs hanya Wirara `:35-36` dan Bashofi `:76-77`; `AUTHORITY-STATUS.md:48-49` | Generalisasi berlebih; redaksi objek sudah diperbaiki (3.3) | ya |
| K-13 | Klaim 800-101 "tercatat di PETA-CELAH-KOLEKSI.md" | `R5 - ...Forensik Digital....md:110-111` vs berkas TIDAK ADA (find = 0) dan GAP-REGISTER tanpa baris 800-101 | Rujukan menggantung; NIST SP 800-101 = gap yatim, butuh kartu pendaftaran gap | ya |

Pelajaran Tabel 7 (VSSKB) diterapkan: tidak ada butir ditutup sebagai "mungkin sama saja";
yang bisa diadjudikasi dari lapis teks diadjudikasi, K-7 dinyatakan calon dengan alasan, dan
satu kelas dinyatakan absen-alih-kontradiksi dengan bukti sapuan.

### 6.3 Tabel BEBAN-RILIS (predikat dari studi; objek ini WAJIB mematuhinya)

Predikat: READY = boleh terbit dengan penanda sumber; LABEL-GUARD = boleh terbit hanya dengan
label yang disebut; BELUM TERKONFIRMASI = butuh PDF primer oleh manusia; DILARANG TERBIT =
tidak ada sandaran di lapis teks.

| # | Butir | Predikat di objek ini |
|---|---|---|
| BR-1 | Proses forensik 4 tahap + rantai kustodi | terbit DENGAN label "kerangka R3, bukan norma" (4.2) |
| BR-2 | Klasifikasi REF-SEC-001..004 | terbit (1.2) |
| BR-3 | Vonis rantai PUTUS mata 4 + tiga hal tak teruji | terbit apa adanya (5.1, 8.1) |
| BR-4 | Empat celah GAP-002/003/006/007 + status sebagian GAP-007 | terbit (7.1) |
| BR-5 | Jangkar halaman Anderson | terbit sebagai nomor PDF klaim lapis teks (3.1) |
| BR-6 | Konversi halaman Alsmadi +16..+18 tidak tetap; Johnson tetap +18 | terbit (3.4) |
| BR-7 | Jumlah halaman 1.044 / 366 / 430 / 238 / 346 | terbit sebagai KLAIM RESUME; byte MiB terukur terpisah (1.4) |
| BR-8 | Nama "NICE Framework" | terbit dengan LABEL-GUARD buku-ajar (3.2) |
| BR-9 | Status NIST SP 800-50r1 | terbit sebagai R5-bundel + catatan kemungkinan R2, pemecahan tertunda; DILARANG disajikan sebagai R2 (3.3) |
| BR-10 | Sebutan UU 11/2008, Perban BSSN 4/2021, ISO/IEC 27001/27002, NIST SP 800-86, ISO/IEC 27037 | terbit HANYA sebagai nama + status TIDAK ADA di rak; bukan isi/pasal/ambang (5.2, 7.1) |
| BR-11 | Nomor fungsi NIST CSF, jumlah kategori CIS v8, tier NICE, ambang BSSN | **DILARANG TERBIT** - TIDAK ada satu pun angka ini di objek ini; status BELUM TERKONFIRMASI sampai manusia membaca PDF Bashofi (6.1) |
| BR-12 | Risiko = kemungkinan x dampak | terbit dengan label "metode internal, PROJECT-DERIVED" (Bagian 2) |
| BR-13 | Klaim cadangan `_asli/` Anderson | BELUM TERKONFIRMASI; disebut hanya sebagai klaim tak terverifikasi (3.1) |

Batas eksplisit: angka BR-11 (versi CSF, tier NICE, kategori CIS v8, ambang BSSN) TIDAK naik
di objek ini dalam bentuk apa pun - bukan angka, bukan contoh. Bila hilir membutuhkannya,
jalurnya = pembacaan PDF Bashofi oleh manusia, lalu amandemen tercatat.

---

## Bagian 7 - Gap register domain

### 7.1 Celah resmi GAP-REGISTER (empat celah yang memutus rantai + satu lintas domain)

| ID | Lapis | Yang hilang | Tingkat | Status | Catatan |
|---|---|---|---|---|---|
| GAP-002 | R1 | UU 11/2008 (ITE) + perubahan | TINGGI | terbuka | hanya penunjuk tesis; tanpa ini keterterimaan bukti tak dapat dinyatakan [GAP-REGISTER.csv:3] |
| GAP-003 | R1 | Peraturan BSSN No. 4/2021 | TINGGI | terbuka | perlu dicek masih berlaku atau direvisi [GAP-REGISTER.csv:4; resume tesis:108-109] |
| GAP-006 | R2 | ISO/IEC 27001 & 27002 | TINGGI | terbuka | "sering jadi syarat tender"; laci ISO-IEC ada namanya tapi tidak berisi 27001 [GAP-REGISTER.csv:7] |
| GAP-007 | R2 | NIST SP 800-86 + ISO/IEC 27037 | TINGGI | SEBAGIAN | Alsmadi PDF 268 memberi proses 4 tahap + rantai kustodi [R3]; standar aslinya tetap tidak ada; jalur tercepat naik ke R2, 800-86 tersedia bebas [GAP-REGISTER.csv:8; GAP-ACQUISITION-PLAN.md:114-116] |
| GAP-014 | R4 | angka produk by-design | - | permanen | angka melekat produk (lisensi firewall, kapasitas SIEM) diminta per proyek |

### 7.2 Gap hasil sapuan (semua berbasis bukti sapuan, bukan dugaan)

| ID | Yang dicari | Keadaan |
|---|---|---|
| G-5 | NIST SP 800-101 (forensik perangkat bergerak) | tidak ada di rak DAN tidak terdaftar di register (gap yatim, K-13) |
| G-6 | NICE Framework asli (NIST SP 800-181) | tidak ada di rak (token = 0) |
| G-7 | UU PDP | tidak ada di rak; hanya ulasan majalah ITSECBuzz; tidak terdaftar sebagai gap |
| G-8 | Lembar data R4 produk keamanan | tidak ada di rak; laci R4 berisi 8 subdirektori tanpa satu pun laci produk keamanan |
| G-9 | NIST SP 800-53, CIS Controls asli, OWASP | tidak ada di rak (token 800-53 = 0; OWASP = 0; CIS hanya sebutan judul tesis) |
| G-10 | Retensi log, definisi SIEM, ambang deteksi, write-blocker | tidak ada di rak (token = 0); ASUMSI-BAKU nol seksi siber |
| G-11 | Konteks Indonesia non-tesis (regulasi turunan BSSN, Perpres objvit) | tidak ada di rak; satu-satunya bahan Indonesia = 4 tesis + majalah |
| G-12 | Versi CSF Bashofi, jumlah fungsi/kategori, tabel pemetaan CIS v8 -> CSF -> BSSN | tidak ada di lapis teks; hanya di PDF Bashofi 4,46 MB belum dibuka (BR-11) |

### 7.3 Yang justru KUAT di rak ini (agar objek tidak timpang)

Enam keputusan desain dengan alternatif ditolak + alasan bersandar halaman
[RANTAI-JAMINAN.md baris 34-42]; kejujuran struktural berupa rantai yang diterbitkan PUTUS
secara sengaja dan status putus ikut menjadi lampiran kartu kendali [:8-9,109]; kata
"boleh/tidak boleh dikatakan" operasional [:85-89]; satu-satunya korpus fleet dengan jalur
nama regulasi Indonesia (walau hanya penunjuk); aritmetika internal lolos semua uji (430, 238,
+18 7/7); mekanisme gerbang rantai putus sudah ternormalisasi di governance
[ASSURANCE-GATES.md baris 160-190].

---

## Bagian 8 - BATAS PENGETAHUAN / status rantai

Blok ini wajib ikut terbit bersama angkanya. Objek yang hanya berisi angka enak-dibaca tapi
menyembunyikan celah = gagal maksud registrasi dan menabrak aturan EKAS ("jawab tidak ada di
rak daripada mengarang").

1. **Status rantai apa adanya (tanpa perataan):** rantai jaminan CYBERSECURITY **PUTUS di mata
   4** karena domain ini NOL R1 dan NOL R2 [R3, RANTAI-JAMINAN.md baris 3-9,22-28]. Tiga hal
   tidak dapat diuji: kepatuhan ISO/IEC 27001, audit Perban BSSN 4/2021, keterterimaan bukti di
   pengadilan [:76-78]. Ini keputusan penerbitan sadar, bukan kecelakaan: terbit APA ADANYA,
   dan pernyataan batas kepatuhan (kepala dokumen ini) wajib ikut di setiap serah
   [:108; ASSURANCE-GATES.md:176-190]. Meratakan status ini = cacat proses; custodian menolak.
2. **Larangan klaim kepatuhan mutlak (CG-8/S-9).** Tidak ada satu pun kalimat di objek ini yang
   menyatakan sistem "sesuai ISO 27001 / ISO 27037 / Peraturan BSSN / UU ITE". Kalimat serupa
   di artefak hilir yang menyandarkan diri pada rak ini = FAIL saat verifikasi, walau rute
   memorinya hidup.
3. **Keadaan rak: JANGAN kutip angka README sebagai fakta (K-1/K-2).** `README.md:34-38`
   (R2 5, R3 24, R4 0, R5 8) dan `README.md:48` ("empat celah R1") TIDAK rekonsiliasi dengan
   register hidup (terukur R2 4, R3 49, R4 6, R5 3; 9 baris R1). Untuk CYBERSECURITY kedua sisi
   sama-sama nol sehingga tidak fatal, tetapi statistik global yang tampil di objek ini adalah
   yang terukur dari register, dan README ditandai basi.
4. **PDF primer belum dibuka manusia.** Tidak ada verifikasi halaman ke PDF asli pada misi ini;
   vonis halaman = vonis lapis teks. Wewenang manusia: K-7 (bookmark Anderson 31 vs 30 target;
   cadangan `_asli/` hilang dari vault) dan SELURUH angka BR-11 (CSF/CIS/tier/BSSN - hanya ada
   di PDF Bashofi). Lokasi PDF nyata terukur di `C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/`
   (1.4); laci `ekas/` workspace = cermin (K-6), bukan kehilangan berkas.
5. **Known-defect yang wajib ikut terangkut:** K-5 (catatan "dua buku ditahan" BASI - jangan
   pernah diulang); K-9 (buku Alsmadi = buku ajar, bukan NICE Framework asli); K-12 (hanya 2
   dari 4 tesis adalah penunjuk regulasi); K-8 (mutu log = R5 bukan sandaran sah walau katalog
   memberi centang); K-13 (NIST SP 800-101 gap yatim). Penandaan di lapis rak menunggu kartu
   D1-FIXx (S-12); sampai terpasang, vonis rilis domain ditahan. Bentuk lama tidak dihapus di
   mana pun, hanya ditandai.
6. **Usia bahan.** Tahun edisi Anderson TIDAK tercatat di lapis teks resume-nya (hanya
   "Edisi: ketiga, Penerbit: Wiley"); tahun Alsmadi ADA di resume-nya ("Springer, 2019") dan
   tahun kedua buku ADA di tabel rantai (RANTAI-JAMINAN.md baris 17-18: Anderson 2020,
   Alsmadi 2019). Umur buku tidak dihitung ulang di sini dari lapis resume (melarang
   karangan) - yang boleh dipakai adalah angka tabel rantai itu.
   Yang tercatat di rak: tesis 2021 x3 dan 2023 x1; panduan Sep-2024 (ASD-CISA), 2024
   (Joint CSI), Okt-2024 (ITSECBuzz). Kebaruan materi operasional AD/logging relatif baik;
   kerangka Anderson bersifat prinsip.
7. **Adjacency (rujukan silang, tidak disalin).** Johnson "Cybersecurity Protecting Critical
   Infrastructures" milik domain CRITICAL-INFRASTRUCTURE (REF-CIP-001 ACTIVE,
   `MASTER-REFERENCE-REGISTER.csv:4`); TIDAK dilebur ke objek ini (putusan penyerapan controller
   OQ-3 belum ada; rekomendasi studi: berdiri sendiri + pointer `INDEX #critical-infrastructure`
   untuk topik objek vital/SCADA). Jaringan keamanan tingkat konsep tinggal di NETWORKING;
   analitik video/biometrik algoritma di VIDEO-SURVEILLANCE; prosedur forensik operasional di
   skill `digital-forensics-evidence-system` (4.3); rakitan proposal DEMS di skill
   `dems-polri-proposal-architect`. Laci `R3_TEXTBOOK-HANDBOOK/SOFTWARE-DATA/` kosong (GAP-021)
   - tidak relevan untuk domain ini.
8. **Sumber dan kebaruan ekstraksi.** Seluruh angka berasal dari lapisan teks `ekas/` diekstrak
   read-only 2026-09-28 oleh studi t_30d502a0; pengukuran byte/aritmetika adalah cetakan skrip
   `research/sec/sec_measure.py` timestamp 2026-09-28T09:39:54, bukan ingatan. `ekas/` read-only
   - objek ini tidak mengubah rak. Tipografi kutipan dinormalisasi ASCII (pemisah bujur tengah
   dan pisahan panjang rak asal diganti; angka, jalur, nomor baris disalin persis).

STATUS: complete
