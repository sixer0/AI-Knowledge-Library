# Rantai Q - Rekayasa sistem: kebutuhan, arsitektur, keputusan, tinjauan, bukti serah

## RANTAI BERANTAI PARSIAL TERBIMBING (sejak 11-10-2026, kartu t_931ae90a)

Mata ①-③ dan ⑤ tersusun **terbimbing lapisan R3 yang ada di rak ini** (tiga resume
ber-halaman + `KEMAMPUAN.md` domain). Mata ④ **tetap tanpa ambang terima**: tidak ada satu
pun baris R1/R2 untuk domain ini, jadi angka lulus/tidak-lulus **tidak dapat** ditetapkan
dari sini dan celahnya dibukukan apa adanya di mata ④ bawah.

**Daya-ikat tidak naik.** Seluruh rujukan domain ini tetap `pending_verification` (P-5) dan
kolom kontraknya `no-unless-contract-adopts` di `02_REGISTERS/MASTER-REFERENCE-REGISTER.csv`
(ukur 11-10-2026: tiga baris `REF-SYS-001/002/003`, semuanya R3, semuanya
`no-unless-contract-adopts`). Susunan mata ②-⑤ ini **menyiapkan**, insan yang
menandatangani; tidak ada baris register yang disunting oleh berkas ini.

**Ambang berasal dari:** bukan dari rak ini. Rak ini memasok **kerangka proses, metode
analisis, dan cara membuktikan keputusan**. Domain rekayasa sistem berbeda dari domain
hitung lain di EKAS: ia tidak menghasilkan angka fisik, ia menghasilkan **struktur keputusan**
(kebutuhan, arsitektur, trade study, tinjauan). Karena itu ambang terimya berbentuk
"kapan sebuah kebutuhan/keputusan boleh disebut selesai", dan angka itu **tidak ada** di
ketiga buku R3 ini sebagai ambang; lihat mata ④.

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman (PDF, sudah dibuka) |
|---|---|---|---|
| `REF-SYS-001` - Systems Engineering: Principles and Practice, Kossiakoff dkk. | **R3** ⏳pending | Metode SE empat langkah generik, analisis kebutuhan dan skenario, MOE/MOP, FFBD, analisis keputusan (weighted sum, MAUT, sensitivitas), manajemen risiko, probabilitas rantai antarmuka, SEP dan technical review. | `[R3, Kossiakoff SEPP, PDF 21]`, `[PDF 38]`, `[PDF 133]`, `[PDF 135]`, `[PDF 165]`, `[PDF 181]`, `[PDF 189]`, `[PDF 200]`, `[PDF 214]`, `[PDF 299]`, `[PDF 319]`, `[PDF 320]`, `[PDF 326]`, `[PDF 330]`, `[PDF 337]`, `[PDF 338]`, `[PDF 355]`, `[PDF 360]` |
| `REF-SYS-002` - INCOSE Systems Engineering Handbook 5e, Walden dkk. | **R3** ⏳pending | Proses siklus hidup (payung ISO/IEC/IEEE 15288), Function Tree dan Product Tree, karakteristik pernyataan kebutuhan (Tabel 2.7), proses Verifikasi dan Validasi beserta metodenya, matriks konsekuensi/likelihood, analisis antarmuka dan N2, konfigurasi, ketertelusuran, tailoring, studi kasus. | `[R3, INCOSE SEH 5th, PDF 10]`, `[PDF 26]`, `[PDF 60]`, `[PDF 65]`, `[PDF 99]`, `[PDF 104]`, `[PDF 110]`, `[PDF 132]`, `[PDF 141]`, `[PDF 146]`, `[PDF 163]`, `[PDF 164]`, `[PDF 172]`, `[PDF 226]`, `[PDF 229]`, `[PDF 230]`, `[PDF 240]`, `[PDF 246]`, `[PDF 303]`, `[PDF 305]` |
| `REF-SYS-003` - System Engineering Management, Blanchard & Blyler | **R3** ⏳pending | Manajemen program SE: proses SE per fase, persyaratan desain sistem, metode dan alat desain, design review dan evaluasi, perencanaan program, evaluasi program, checklist review dan evaluasi pemasok. | `[R3, Blanchard SEM, PDF 15]`, `[PDF 25]`, `[PDF 67]`, `[PDF 80]`, `[PDF 139]`, `[PDF 237]`, `[PDF 265]`, `[PDF 289]`, `[PDF 356]`, `[PDF 386]`, `[PDF 440]`, `[PDF 543]`, `[PDF 544]` |

> Semua baris: R3 buku teks/handbook, `pending_verification` - sah untuk **metode, kerangka,
> dan penalaran**, tidak sah sebagai ambang terima (lihat kartu
> `04_KNOWLEDGE-CARDS/SYSTEMS-ENGINEERING/REF-SYS-001.md` bagian 3 dan 4, berlaku sama untuk
> 002 dan 003).

**Konversi halaman (diukur ulang per berkas pada run kartu ini, bukan diwarisi):**

| Berkas | Selisih folio cetak terhadap nomor PDF | Bukti ukur |
|---|---|---|
| Kossiakoff SEPP | **tidak tetap: +22 sampai +27** | `[UKUR-RUN-INI, vault PDF, 11-10-2026]` PDF 133 -> folio 106 (+27); PDF 165 -> folio 140 (+25); PDF 181 -> 157 (+24); PDF 299 -> 276 (+23); PDF 351 -> 329 (+22); PDF 360 -> 338 (+22) |
| INCOSE SEH 5e | **+25 di badan bab 2** (bab lain berbeda; kepala bab tidak berfolio) | `[UKUR-RUN-INI, vault PDF, 11-10-2026]` PDF 104 -> folio 79; PDF 110 -> 85; PDF 141 -> 116; PDF 163 -> 138; PDF 172 -> 147; PDF 226 -> 201; PDF 303 -> 278 |
| Blanchard SEM | **+14 (tetap di badan)** | `[UKUR-RUN-INI, vault PDF, 11-10-2026]` PDF 80 -> folio 66; PDF 356 -> 342; kepala bab: PDF 15 = bab 1, PDF 67 = bab 2, PDF 139 = bab 3, PDF 265 = bab 5, PDF 289 = bab 6, PDF 440 = bab 8 |

Karena selisih Kossiakoff bervariasi, **seluruh kutipan berkas ini memakai nomor PDF**, sama
seperti keputusan ketiga resume. Catatan: kepala berkas resume menuliskan selisih Kossiakoff
"+22..+24" - hasil ukur di atas menunjukkan rentang itu terlalu sempit (lihat
CATATAN SILANG-PEMILIK butir 2).

**Provenans pembukaan halaman:** kolom "sudah dibuka" berarti halaman PDF-nya dibuka ulang
dengan `pdftotext -layout` (Xpdf 4.06) pada run kartu ini terhadap berkas vault
`03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/SYSTEMS-ENGINEERING/`. Tidak ada jangkar yang
diwarisi tanpa dibuka: setiap nomor di tabel ① di atas adalah keluaran perintah buka
halaman pada run ini. Jumlah halaman hasil ekstraksi cocok dengan klaim ketiga resume
(Kossiakoff 663, INCOSE 370, Blanchard 568).

**Bukti byte (dicocokkan ulang 11-10-2026 terhadap berkas vault, sha256[:16]):**
`REF-SYS-001` = `76a55d142e2afc72`, `REF-SYS-002` = `9fa307f72d9820da`,
`REF-SYS-003` = `e967c2d3af7d111d` - ketiganya sama dengan kolom `notes` Register Induk.

**Edisi aktual berkas vault (halaman judul/copyright, dibuka 11-10-2026):** Kossiakoff =
*THIRD EDITION*, "This third edition first published 2020 (c) 2020 John Wiley & Sons"
(PDF 4-5), penulis tercetak di halaman judul: Kossiakoff, Seymour, Flanigan, Biemer.
INCOSE = *FIFTH EDITION*, `INCOSE-TP-2003-002-05`, 2023 (PDF 4). Blanchard =
**FIFTH EDITION** (PDF 2), copyright 2016 (PDF 3) - kepala berkas resume menulis "keenam"
(lihat CATATAN SILANG-PEMILIK butir 4).

---

## ② Keputusan desain

Tingkat R3 **cukup** untuk mata ini: keputusan rekayasa memang penilaian, yang wajib
tertulis adalah pilihan + alternatif yang ditolak + alasannya
(`01_GOVERNANCE/ASSURANCE-WORKFLOW.md`, tabel "Aturan tingkat pada tiap mata rantai").

| Yang ditetapkan | Dasar | Alternatif yang ditolak dan alasannya |
|---|---|---|
| Payung proses proyek integrasi = **pemetaan fase ke kelompok proses ISO/IEC/IEEE 15288** sebagaimana dibawakan handbook, lalu **ditalor** ke tipe sistem | Handbook mengadopsi 15288 + ISO/IEC TR 24748-1 sebagai basis proses `[R3, INCOSE SEH 5th, PDF 10]`; empat kelompok proses 15288 `[R3, INCOSE SEH 5th, PDF 65]`; tailoring bab 4 `[R3, INCOSE SEH 5th, PDF 240]`, `[PDF 246]` | Menjadikan salah satu model siklus hidup tunggal sebagai payung wajib ditolak - model hidup (Vee, incremental, agile) adalah pilihan tailoring, bukan proses itu sendiri: "there are many life cycle models (e.g., Vee, ICSM, DevSecOps)" `[R3, INCOSE SEH 5th, PDF 246]` |
| Urutan kerja eksplorasi konsep: **analisis kebutuhan -> definisi fungsi -> definisi fisik -> validasi desain**, empat langkah generik ini wajib tampak di jejak kerja | "the names of the four generic steps in the method are shown in parentheses" + keempatnya tercantum di halaman yang sama: *Operational requirements analysis (Requirements analysis); Performance requirements formulation (Functional definition); Implementation concept exploration (Physical definition); Performance requirements validation (Design validation)* `[R3, Kossiakoff SEPP, PDF 181]` (cetak 157) | Melompat dari kebutuhan pengguna langsung ke pemilihan wujud fisik ditolak - fungsi belum dialokasi, sehingga tidak ada dasar menilai arsitektur; peringatan buku: jangan mencoba mengoptimalkan pada tahap formulasi awal `[R3, Kossiakoff SEPP, PDF 214]` |
| Dekomposisi **dua pohon terpisah**: Function Tree (FBS) untuk fungsi, Product Tree (PBS) untuk produk; struktur hirarki dipakai berjenjang | `[R3, INCOSE SEH 5th, PDF 99]` (definisi FBS/PBS); aliran fungsi dan control divisualkan dengan FFBD `[R3, Kossiakoff SEPP, PDF 214]` | Satu diagram gabungan fungsi-fisik ditolak - mencampurkannya membuat penelusuran kebutuhan ke komponen tidak dapat diaudit (ketertelusuran justru properti yang dituntut `[R3, INCOSE SEH 5th, PDF 146]`) |
| Antarmuka **didaftarkan sebelum diuji**: batas SoI vs sistem eksternal, diagram N2 sebagai alat daftar | Batas antarmuka eksternal dan ketertelusuran konsep-kebutuhan `[R3, INCOSE SEH 5th, PDF 132]`; N2 diagram sebagai metode analisis `[R3, INCOSE SEH 5th, PDF 229]`, `[PDF 230]` | Mengandalkan koordinasi lisan antar-subkontrak ditolak - kegagalan antarmuka bersifat multiplikatif, bukan aditif: `R = (1-Pi)^N` `[R3, Kossiakoff SEPP, PDF 360]` (lihat mata ③ untuk angkanya) |
| Pemilihan alternatif: **trade study formal** berbobot (weighted sum atau MAUT) dengan **analisis sensitivitas wajib**, hasilnya dilaporkan dengan isi baku | Membedakan "trade-off analysis / trade study" dari sekadar "trade-off" `[R3, Kossiakoff SEPP, PDF 319]`; weighted sum `[R3, Kossiakoff SEPP, PDF 326]`; fungsi utilitas untuk menyatukan satuan berbeda `[R3, Kossiakoff SEPP, PDF 337]`; "Perform sensitivity analysis" `[R3, Kossiakoff SEPP, PDF 338]`; validasi konsep lewat uji sensitivitas `[R3, Kossiakoff SEPP, PDF 320]`; isi laporan trade-off `[R3, Kossiakoff SEPP, PDF 330]` | Trade-off informal tanpa jejak ditolak untuk keputusan yang masuk dokumen serah `[R3, Kossiakoff SEPP, PDF 319]`; memilih metode tanpa uji sensitivitas ditolak - pemenang bisa berubah hanya karena bobot `[R3, Kossiakoff SEPP, PDF 333]`-`[PDF 339]` |
| Risiko: **klasifikasi ordinal** pada matriks konsekuensi/likelihood, bukan angka tunggal | Matriks konsekuensi/likelihood generik (rating a-e dan 1-5) `[R3, INCOSE SEH 5th, PDF 110]`; kemungkinan risiko terkait status desain `[R3, Kossiakoff SEPP, PDF 355]` Tabel 12.1 | Angka risiko tunggal hasil kali probabilitas x kekritisan ditolak **oleh sumbernya sendiri**: "assignment of numerical estimates creates the illusion of quantitative knowledge, which has no real basis" `[R3, Kossiakoff SEPP, PDF 355]` |
| Mutu pernyataan kebutuhan diuji **sebelum dibekukan**: uji per-butir (feasible, affordable, verifiable) + uji koleksi | `[R3, Kossiakoff SEPP, PDF 188]`-`[PDF 189]` (tujuh pertanyaan uji, butir 1-4 tercetak di PDF 188 dan 5-7 di PDF 189; "If the answer to any of the questions above is no, then the requirement needs to be revised"); 11 karakteristik pernyataan kebutuhan Tabel 2.7 `[R3, INCOSE SEH 5th, PDF 141]` | Set kebutuhan yang hanya "lulus baca" ditolak - kebutuhan tak terverifikasi memindahkan sengketa ke masa uji terima (mata ④) |
| Validasi kebutuhan dilakukan **terpisah** dari validasi desain, formal atau informal | "This may be accomplished formally or informally. Formal validation means using an independent organization" `[R3, Kossiakoff SEPP, PDF 189]`; langkah keempat metode generik adalah *Performance requirements validation (Design validation)* - validasi kebutuhan performa terhadap sasaran operasional, bukan uji produk `[R3, Kossiakoff SEPP, PDF 181]` | Menunggu validasi desain saja ditolak - kebutuhan operasional yang salah tidak tertangkap oleh uji produk |
| Tinjauan teknis dijadwalkan **dalam rencana**, bukan atas inisiatif perancang | SEP "shall also detail the timing, conduct, and success criteria of technical reviews" `[R3, Kossiakoff SEPP, PDF 135]`; aktivitas SE manajemen mencakup trade-off study, technical reviews, configuration management `[R3, Kossiakoff SEPP, PDF 133]`; checklist review siap pakai `[R3, Blanchard SEM, PDF 543]`, evaluasi pemasok `[R3, Blanchard SEM, PDF 544]` | Review ad-hoc tanpa kriteria sukses ditolak - tanpa kriteria tertulis gate G2 EKAS gagal (`01_GOVERNANCE/ASSURANCE-GATES.md`, G2 "kolom alternatif kosong" = gagal) |
| Peran penanggung jawab keputusan: engineer menyeimbangkan **tiga konstituensi** (pengguna/pemangku kepentingan, manajer proyek, spesialis pelaksana) | `[R3, Kossiakoff SEPP, PDF 21]` (Preface to the Third Edition) dan `[PDF 28]` (Preface to the First Edition) | Menyerahkan keputusan kebutuhan sepenuhnya ke disiplin tunggal ditolak - keputusan SE adalah keputusan lintas konstituensi, jadi penandatangannya pun tidak boleh satu nama |

> Keputusan yang paling menentukan mutu pekerjaan rekayasa sistem di domain ini:
> **setiap pilihan disertai alternatif yang ditolak beserta alasannya, dan setiap
> pemilihan alternatif melewati uji sensitivitas.** Keduanya mengalir ke mata ③ sebagai
> angka bertanda dan ke mata ⑤ sebagai lampiran yang bisa diperiksa.

---

## ③ Perhitungan

Rumus-rumus di bawah hidup di lapisan ini, **bukan** di `06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md`:
katalog tidak punya satu pun butir rekayasa sistem (ukur 11-10-2026, hitungan pola
`rekayasa sistem|systems engineering|trade-study|trade-off|kossiakoff|incose|blanchard|MOE`
pada `KATALOG-RUMUS.md` = 0 dari 33.646 B). Butir lintas-lapis ini dicatat di kaki berkas
sebagai celah; pengisian KATALOG bukan wewenang LOCK ini.

Domain ini tidak menghitung besaran fisik. Yang dihitung adalah **skor keputusan** dan
**probabilitas rantai**. Keduanya sah sebagai hitungan selama masukan dan asumsinya bertanda.

### Skor berbobot (trade study)

```
Skor(alternatif) = SUM_i ( w_i * v_i )      dengan w_i = bobot kriteria i, v_i = nilai kriteria i
syarat: SUM_i w_i = 1
```

| Bentuk | Sumber |
|---|---|
| Tabel 11.2 "Weighted Sum Integration of Selection Criteria", kolom skor `Score = weight x value` | `[R3, Kossiakoff SEPP, PDF 326]` (cetak 303) |
| Fungsi utilitas `U(m_i)` untuk menyatukan kriteria bersatuan berbeda (probabilitas, m3, kg) | `[R3, Kossiakoff SEPP, PDF 337]` (cetak 314) |

Contoh terhitung buku, **diukur ulang sendiri 11-10-2026** (bukan disalin dari laporan hulu):

```
w = (0,50 ; 0,30 ; 0,15 ; 0,05)   -> jumlah bobot = 1,00
v = ( 4   ;  3   ;  2   ;  5  )
kontribusi = 2,00 + 0,90 + 0,30 + 0,25
Skor = 3,45
```

| Masukan | Nilai contoh | Tag | Sumber |
|---|---|---|---|
| Bobot kriteria `w_i` | 0,50 / 0,30 / 0,15 / 0,05 | `ASSUMPTION` (nilai contoh buku; bobot riil adalah milik proyek) | `[R3, Kossiakoff SEPP, PDF 326]` |
| Nilai kriteria `v_i` (skala ordinal 1-5) | 4 / 3 / 2 / 5 | `ASSUMPTION` | `[R3, Kossiakoff SEPP, PDF 326]` |
| Aturan penggabungan | weighted sum sebagai starting point; MAUT bila banyak kriteria | `SOURCE-DERIVED` (metode) | `[R3, Kossiakoff SEPP, PDF 337]`, `[PDF 338]` |

Sensitivitas terhadap bobot (aturan asumsi: dua skenario 1/2x dan 2x, dijalankan pada butir
bobot terkecil 0,05 dan terbesar 0,50, nilai `v` tetap; bobot **ternormalisasi ulang** agar
jumlahnya kembali 1 - renormalisasi adalah keputusan metode kita, bukan angka buku):

| Skenario | Bobot (ternormalisasi) | Skor | Selisih dari 3,45 | Tag | Sumber |
|---|---|---|---|---|---|
| Dasar | 0,500 / 0,300 / 0,150 / 0,050 | 3,4500 | - | `ASSUMPTION` (contoh buku) + skor dihitung run ini | `[R3, Kossiakoff SEPP, PDF 326]` |
| 1/2x pada w1 (0,50 -> 0,25) | 0,3333 / 0,4000 / 0,2000 / 0,0667 | 3,2667 | -0,1833 | `ASSUMPTION` (renormalisasi metode kita) + hitungan run ini | turunan dari `[R3, Kossiakoff SEPP, PDF 326]` |
| 2x pada w1 (0,50 -> 1,00) | 0,6667 / 0,2000 / 0,1000 / 0,0333 | 3,6333 | +0,1833 | `ASSUMPTION` (renormalisasi metode kita) + hitungan run ini | turunan dari `[R3, Kossiakoff SEPP, PDF 326]` |
| 1/2x pada w2 (0,30 -> 0,15) | 0,5882 / 0,1765 / 0,1765 / 0,0588 | 3,5294 | +0,0794 | `ASSUMPTION` (renormalisasi metode kita) + hitungan run ini | turunan dari `[R3, Kossiakoff SEPP, PDF 326]` |
| 2x pada w2 (0,30 -> 0,60) | 0,3846 / 0,4615 / 0,1154 / 0,0385 | 3,3462 | -0,1038 | `ASSUMPTION` (renormalisasi metode kita) + hitungan run ini | turunan dari `[R3, Kossiakoff SEPP, PDF 326]` |

Uji yang lebih menentukan: **apakah pemenang berubah**, bukan berapa selisih skornya.
Dengan alternatif pembanding `B = (5; 2; 3; 3)` di samping `A = (4; 3; 2; 5)`:

| Skenario bobot | Skor A | Skor B | Pemenang |
|---|---|---|---|
| Dasar (`ASSUMPTION` buku, dihitung run ini) | 3,4500 | 3,7000 | B |
| 1/2x pada w1 (bobot ternormalisasi, `ASSUMPTION`) | 3,2667 | 3,2667 | **seri** (peringkat hilang) |
| 2x pada w1 (bobot ternormalisasi, `ASSUMPTION`) | 3,6333 | 4,1333 | B |

> Pesan yang mengikat rancangan: pada contoh ini **mengubah bobot kriteria utama dua kali
> lipat sudah cukup untuk membatalkan keputusan** (A dan B menjadi seri). Ini alasan
> mengapa uji sensitivitas dituntut tertulis `[R3, Kossiakoff SEPP, PDF 338]` dan mengapa
> isinya wajib masuk laporan `[R3, Kossiakoff SEPP, PDF 330]`. Batas yang jujur: buku
> memberi **cara** menghitung dan menuntut uji sensitivitas, tetapi tidak memberi aturan
> renormalisasi bobot maupun "selisih skor berapa yang berarti" - keduanya masuk daftar
> celah mata ④.

### Probabilitas keberhasilan rantai antarmuka

```
R = (1 - Pi)^N        Pi = probabilitas satu aktivitas/antarmuka gagal
                      N  = jumlah antarmuka yang harus berhasil agar rantai selesai
```

Sumber rumus dan definisi variabelnya: `[R3, Kossiakoff SEPP, PDF 360]` (cetak 338, bab 12
Risk Management): "If there are many interfaces, then the probability may be independently
calculated by: (1-Pi)^N".

Contoh terukur (dihitung sendiri pada run ini; `Pi` adalah `ASSUMPTION` proyek, bukan angka rak):

| `Pi` (tag: `ASSUMPTION` proyek) | `N=5` | `N=10` | `N=20` | Rumus |
|---|---|---|---|---|
| 0,01 | 0,9510 | 0,9044 | 0,8179 | `[R3, Kossiakoff SEPP, PDF 360]` |
| 0,02 | 0,9039 | 0,8171 | 0,6676 | `[R3, Kossiakoff SEPP, PDF 360]` |
| 0,05 | 0,7738 | 0,5987 | 0,3585 | `[R3, Kossiakoff SEPP, PDF 360]` |
| 0,10 | 0,5905 | 0,3487 | 0,1216 | `[R3, Kossiakoff SEPP, PDF 360]` |

Pesan yang mengikat rancangan: **kegagalan antarmuka bersifat multiplikatif** - pada
`Pi` 0,05, menambah antarmuka dari 5 ke 20 menjatuhkan peluang rantai dari 0,774 ke 0,359.
Ini dasar rasional keputusan "daftar antarmuka dulu, baru uji" di mata ②, dan sekaligus
alasan mengapa angka `Pi` tidak boleh diambil dari buku (buku tidak memberinya).

### Metrik yang jadi tulang punggung hitungan

| Besaran | Ketentuan rak | Tag | Sumber |
|---|---|---|---|
| MOE (measure of effectiveness) | selalu merujuk sistem sebagai keseluruhan | `SOURCE-DERIVED` (definisi) | `[R3, Kossiakoff SEPP, PDF 200]` |
| MOP (measure of performance) | metrik kuantitatif karakteristik/atribut/subsistem tertentu, di bawah level sistem | `SOURCE-DERIVED` (definisi) | `[R3, Kossiakoff SEPP, PDF 200]` |
| Peringkat risiko | ordinal: konsekuensi (a-e) x kemungkinan (1-5) -> kelas matriks | `SOURCE-DERIVED` (metode), **tanpa angka ambang** | `[R3, INCOSE SEH 5th, PDF 110]` |
| Kemungkinan risiko | dipatok ke status desain (High = perluasan besar dari desain lalu; Medium = banyak komponen baru; Low = komponen/antarmuka kompleks) | `SOURCE-DERIVED` (Tabel 12.1) | `[R3, Kossiakoff SEPP, PDF 355]` |

> **Aturan yang membatalkan hitungan bila dilanggar:** angka yang masuk dokumen serah harus
> bisa ditunjuk sebagai MOE (level sistem) atau MOP (level subsistem) - bukan "skor" tanpa
> tingkatan. Definisi keduanya ada di `[R3, Kossiakoff SEPP, PDF 200]`; pemisahan level ini
> yang membuat hasil trade study dapat ditelusuri balik ke kebutuhan.

---

## ④ Pengujian

**Yang bisa dinyatakan rak ini: metode dan objek pembuktian. Yang TIDAK bisa dinyatakan:
ambang terima.** Urutan tingkat untuk mata ini adalah R1 -> R2 -> kontrak
(`ASSURANCE-WORKFLOW.md`); R3 hanya sah bila kontrak mengadopsinya tertulis, dan kolom
register ketiga buku ini berbunyi `no-unless-contract-adopts` (ukur 11-10-2026).

Uji intern yang sah dijalankan (hasilnya dilaporkan, **bukan** vonis lulus):

| Butir | Ketentuan | Status sumber |
|---|---|---|
| Metode verifikasi | empat metode: inspection, analysis, demonstration, test; masing-masing didefinisikan dan dipilih bersama success criteria dalam strategi verifikasi | metode R3 `[R3, INCOSE SEH 5th, PDF 164]`; tujuan proses verifikasi "provide objective evidence that a system, system element, or artifact fulfils its specified requirements" `[R3, INCOSE SEH 5th, PDF 163]`; **ambang keberhasilan per metode = tidak ada di rak** |
| Ketertelusuran verifikasi | traceability dua arah antara entitas terverifikasi dan kebutuhan dijaga | `[R3, INCOSE SEH 5th, PDF 165]`; definisi ketertelusuran `[R3, INCOSE SEH 5th, PDF 226]`; **persentase cakupan RTM yang dianggap cukup = tidak ada di rak** |
| Validasi | aktivitas proses Validation (scope, kriteria, hasil) terpisah dari verifikasi | `[R3, INCOSE SEH 5th, PDF 172]`; pasangan dekomposisi-vs-V&V pada model Vee `[R3, INCOSE SEH 5th, PDF 60]`, `[PDF 61]`; **kriteria "valid" = tidak ada di rak** |
| Uji operasional | operational testing and evaluation: menguji efektivitas seluruh sistem di lingkungan operasional nyata; tiap level punya test plan sendiri | `[R3, Kossiakoff SEPP, PDF 133]`; **angka efektivitas lulus = tidak ada di rak** |
| Tinjauan desain | design review formal dengan kriteria + checklist | `[R3, Blanchard SEM, PDF 265]` (bab 5), checklist `[R3, Blanchard SEM, PDF 543]` (App. D); **daftar pertanyaan checklist = artefak kerja, bukan ambang** |
| Evaluasi pemasok | checklist evaluasi pemasok untuk pekerjaan alih daya | `[R3, Blanchard SEM, PDF 544]` (App. E); **skor minimum pemasok = tidak ada di rak** |
| Mutu kebutuhan | uji per-butir (feasible/affordable/verifiable) + 11 karakteristik pernyataan | `[R3, Kossiakoff SEPP, PDF 188]`-`[PDF 189]` (daftar tujuh pertanyaan uji; butir 1-4 tercetak di PDF 188, butir 5-7 di PDF 189); `[R3, INCOSE SEH 5th, PDF 141]` Tabel 2.7 (ukur: 11 karakteristik unik - Necessary, Appropriate, Unambiguous, Complete, Singular, Feasible, Verifiable, Correct, Conforming, Consistent, Comprehensible); **jumlah karakteristik yang wajib penuh = tidak dinyatakan sebagai ambang** |

**Celah yang dibukukan (bukan dikarang):**

1. **Tidak ada ambang terima di rak ini untuk domain rekayasa sistem.** Ukur 11-10-2026:
   `MASTER-REFERENCE-REGISTER.csv` = 103 baris data dengan sebaran R3=89, R4=6, R2=4, R5=4,
   **R1=0**; keempat baris R2 seluruhnya domain lain (POWER-BACKUP, ELECTRICAL, FIBER-OPTIC,
   VIDEO-SURVEILLANCE) - **0 baris R1/R2 ber-domain SYSTEMS-ENGINEERING**.
   `GAP-REGISTER.csv` = 22 baris, **0 baris** menyebut domain ini.
   `07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/AMBANG-TERIMA-INDUK.md` = 0 butir
   rekayasa sistem.
2. **Sandaran yang seharusnya ada tapi lacinya kosong.** Handbook mengutip ISO/IEC/IEEE 15288
   dan ISO/IEC TR 24748-1 `[R3, INCOSE SEH 5th, PDF 10]`, tetapi teks standarnya sendiri tidak
   di rak: laci `03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/ISO-IEC/` berisi `_ISI.md`
   berstatus "Kosong" (dibaca 11-10-2026). Jadi sandaran proses hari ini adalah **handbook R3
   yang mengutip**, bukan standarnya.
3. **Usulan butir GAP untuk langkah 25-26** (kewenangan penulis register GAP, bukan LOCK ini):
   (a) ambang mutu set kebutuhan - berapa karakteristik Tabel 2.7 yang wajib penuh sebelum G1
   ditutup; (b) ambang signifikansi trade study - selisih skor antar-alternatif berapa yang
   boleh disebut menang, dan renormalisasi bobot saat sensitivitas dijalankan; (c) ambang
   penerimaan risiko - sel mana pada matriks konsekuensi/likelihood yang mewajibkan mitigasi
   sebelum G2; (d) ambang cakupan ketertelusuran - persentase RTM dua arah untuk G6;
   (e) ambang keberterimaan hasil uji operasional (MOE). Yang seharusnya masuk rak: teks resmi
   ISO/IEC/IEEE 15288 (R2) atau pasal adopsi handbook oleh kontrak proyek.
4. **Bentuk jawaban yang sah hari ini** saat ambang rekayasa sistem diminta: nyatakan "tidak
   ada di rak ini; sumber yang seharusnya: ISO/IEC/IEEE 15288 (belum di rak) atau pasal adopsi
   tertulis handbook dalam kontrak", lalu mintakan angka itu ke pemilik pekerjaan - **jangan**
   mengambil nilai contoh buku (Skor 3,45; R = 0,5987; skala 1-5) sebagai ambang. Angka itu
   ilustrasi metode (ditegaskan bagian 4 tiap resume: metode, bukan ambang).

---

## ⑤ Bukti serah

Bukti serah pekerjaan rekayasa sistem = bukti bahwa **setiap keputusan punya jalur
①->④**, bukan hanya daftar dokumen.

| Lampiran | Wajib | Catatan |
|---|---|---|
| Catatan Keputusan Desain `TPL-01` per keputusan mata ② | ✅ | G2 gagal bila kolom alternatif ditolak kosong (`01_GOVERNANCE/ASSURANCE-GATES.md`, G2). Isi laporan trade-off yang diharapkan sumbernya: kriteria + pembobotan + alasan skor + ringkasan hasil + **deskripsi analisis sensitivitas dan hasilnya** + kesimpulan + rekomendasi `[R3, Kossiakoff SEPP, PDF 330]` |
| Set kebutuhan beku + hasil uji mutu kebutuhan | ✅ | Padanan bentuk: tujuh pertanyaan uji per butir `[R3, Kossiakoff SEPP, PDF 189]` dan tabel karakteristik `[R3, INCOSE SEH 5th, PDF 141]`; masuk gerbang G1 |
| Function Tree / Product Tree + daftar antarmuka (N2) | ✅ | `[R3, INCOSE SEH 5th, PDF 99]`, `[PDF 132]`, `[PDF 229]`, `[PDF 230]` |
| Requirement Traceability Matrix | ✅ | Definisi ketertelusuran `[R3, INCOSE SEH 5th, PDF 226]`; cermin bentuk di `10_TEMPLATES/TPL-06-REQUIREMENT-TRACEABILITY.md` (ukur 11-10-2026: 324 B, kerangka tipis) |
| Rencana verifikasi (pilihan metode per kebutuhan) + hasil | ✅ | Empat metode dan success criteria `[R3, INCOSE SEH 5th, PDF 164]`; gerbang G4 menuntut **ambang beserta sumbernya** disetujui sebelum uji - di sinilah celah mata ④ paling sering tersamar |
| Berita acara design review (dan evaluasi pemasok bila ada alih daya) | ✅ | Checklist siap pakai `[R3, Blanchard SEM, PDF 543]`, `[PDF 544]`; dipetakan ke G2 (desain) dan G6 (serah) |
| Lembar perhitungan skor/probabilitas dengan tag per masukan | ✅ | Tiap masukan bertanda `SOURCE-DERIVED` / `PROJECT-DERIVED` / `OEM-DERIVED` / `ASSUMPTION`; tiap `ASSUMPTION` punya sensitivitas + rencana penggantian (gerbang G3, `ASSURANCE-GATES.md`) |
| Kartu kendali rantai per besaran `TPL-00` | ✅ | Bentuk minimum di `ASSURANCE-WORKFLOW.md`; status "menunggu R4" sah bila tertulis |
| Rencana Inspeksi dan Uji (ITP) `TPL-08` | ✅ | Titik hold/witness per fase; tanpa ini "metode uji disetujui" tidak terikat ke lapangan |
| Catatan penerimaan `TPL-04` | ✅ | Bagian "Ambang dan sumbernya" wajib terisi; bila belum ada sandarannya, tulis "belum ada di rak" (mata ④) - jangan biarkan kosong tanpa keterangan |
| Paket bukti serah `TPL-05` | ✅ | G6 menuntut dua baris yang paling sering hilang: daftar asumsi terbuka dan daftar butir menunggu data OEM `[R4]` |

**Keterbatasan kerangka yang ada (diukur, bukan disimpulkan):**
`07_VERIFICATION-VALIDATION/TEST-PROCEDURES/TEMPLATE-BERITA-ACARA.md` menyediakan 8 jenis uji
(serat, pembumian, instalasi listrik, baterai, genset, video, termal, penyimpanan) dan
**tidak punya bagian untuk tinjauan teknis, trade study, atau uji operasional sistem**;
pakai "Rangka umum - berlaku untuk semua jenis" (bagian 1 berkas itu) plus tabel Ringkasan
sumber ambang-nya, dan nyatakan bahwa jenis uji rekayasa sistem belum punya template khusus.
Pada tingkat yang sama: `TPL-04` (323 B), `TPL-06` (324 B), `TPL-01` (779 B) adalah kerangka
tipis - memadai sebagai bentuk, tidak memadai sebagai instruksi pengisian.

---

## Status rantai

**TERBIMBING SAMPAI MATA ④.** Mata ①-③ dan ⑤ tersusun dan setiap angkanya bertanda `[R-n]`
dengan halaman yang dibuka ulang terhadap vault pada run kartu ini. Mata ④ **jujur kosong
untuk ambang**: domain ini mengatur proses keputusan, jadi ambang terimya berbentuk kriteria
kelayakan kebutuhan/keputusan yang belum dimiliki rak.

**Kapan rantai ini boleh disebut utuh:** setelah (a) verifier menaikkan daya-ikat resume dari
`pending_verification` (P-5), (b) insan menandatangani unit `KEMAMPUAN.md` domain ini
(ukur 11-10-2026: 372/372 baris `KEMAMPUAN-REGISTER.csv` masih
`draft-tidak-terverifikasi-insan`, termasuk 18/18 baris `SYS-001..SYS-018` dengan status
9 `draft` + 9 `candidate`), dan (c) ambang terima punya sandaran R1/R2 atau adopsi kontrak
tertulis.

**Cara pakai hari ini:** kerja dari mata ② dan ③ sebagai kerangka metode (dengan kutipan
halamannya), pakai mata ⑤ sebagai daftar bukti, dan jawab permintaan ambang dengan butir 4
mata ④. Jangan mengutip mata ① sebagai bukti "sudah ada ambang".

---

## CATATAN SILANG-PEMILIK (temuan di luar LOCK, dilaporkan, TIDAK ditambal di sini)

Tertanggal 11-10-2026, kartu t_931ae90a. Semua butir terukur langsung dari berkas vault
(pdftotext Xpdf 4.06) dan berkas hulu; berkas-berkas itu bukan milik LOCK ini sehingga
**tidak disunting**.

1. **Tiga jangkar Kossiakoff di resume menyalahi isi halaman.**
   (a) Butir "posisi sistem engineer menghadap tiga arah" ditambatkan ke `[PDF 59]`;
   kalimatnya ("The systems engineer faces in three directions") terukur di **PDF 21**
   (Preface to the Third Edition) dan **PDF 28** (Preface to the First Edition) - keduanya
   front-matter, bukan badan bab 1; PDF 59 berisi soal akhir bab.
   (b) Butir "MBSE ... definisi INCOSE dikutip" ditambatkan ke `[PDF 58..59]`; definisi
   "Model Based Systems Engineering (MBSE) is an emerging new paradigm ..." terukur di
   **PDF 38** (badan bab, running head `SYSTEMS ENGINEERING VIEWPOINT 9`) dan muncul lagi di
   **PDF 277**; PDF 58 adalah halaman `PROBLEMS 29`.
   (c) Butir "empat langkah generik metode SE pada fase eksplorasi konsep" ditambatkan ke
   `[PDF 170]`; frasa "four generic steps" terukur hanya di **PDF 181**; PDF 170 berisi
   seksi biaya dan validasi kebutuhan (folio 145).
2. **Rentang konversi folio resume Kossiakoff terlalu sempit.** Kepala resume menulis
   "Selisih folio bervariasi +22..+24"; hasil ukur run ini: **+27** di PDF 133/135 (folio
   106/108) dan **+25** di PDF 165/170 (folio 140/145), baru +24/+23/+22 di bab berikutnya.
   Pemakaian rentang +22..+24 pada bab awal menggeser kutipan sampai tiga halaman.
3. **Klaim letak tabel bab 11 tidak tereproduksi.** Resume menulis "tabel 11-5..11-7 tercetak
   di daftar gambar PDF 17-19"; terukur: `TABLE 11.5` ada di **PDF 333**, `TABLE 11.6` di
   **PDF 334**, `TABLE 11.7` di **PDF 335**, dan halaman PDF 17-19 tidak memuat token
   `Table 11.5/11.6/11.7` sama sekali.
4. **Edisi Blanchard salah di kepala resume.** Resume menulis "Edisi: keenam"; halaman judul
   berkas vault menulis **FIFTH EDITION** (PDF 2) dengan copyright 2016 (PDF 3). Baris
   Register Induk dan `_ISI.md` laci menyebut tahun 2016 saja, tidak menyebut edisi.
5. **Pemetaan lampiran Blanchard di resume keliru halaman.** Baris "App. A-D" menambatkan
   keempatnya ke `[PDF 356]` (empat kali alamat sama); terukur: PDF 356 adalah `TABLE 6.7`
   di bab 6, sedangkan awal lampiran = App. A **PDF 454**, App. B **PDF 461**, App. C
   **PDF 495**, App. D **PDF 543**, App. E **PDF 544** (jadi ada lima lampiran, bukan empat).
6. **Dua pasangan halaman di tambalan W9B `KEMAMPUAN.md` meleset.** `pdf_p165/cetak 142`
   untuk "lima komponen dasar scenario" (Kossiakoff): frasa "five basic components" terukur di
   PDF 165 yang berfolio **140**, bukan 142. `pdf_p214/cetak 191` untuk FFBD: PDF 214 berfolio
   **190**; folio 191 adalah PDF 215. Pasangan `pdf_p104/cetak 79`, `pdf_p141/cetak 116`, dan
   `pdf_p10` tereproduksi tepat.
7. **Tiga jangkar `KEMAMPUAN.md` menunjuk halaman yang tidak memuat artefak bernama.**
   `SYS-007` Function Tree "pdf hal. 132": teks Function Tree/FBS terukur di **PDF 97** dan
   **PDF 99**; PDF 132 adalah proses definisi kebutuhan pemangku kepentingan. `SYS-010` N2
   "pdf hal. 227": "N2 diagram" terukur di **PDF 229** dan **PDF 230**; PDF 227 adalah
   configuration management. `SYS-016` bernama "Verification Planning (IADT Matrix)" padahal
   akronim `IADT` maupun `I/A/D/T` **0 kemunculan** di ketiga buku; keempat metode itu terukur
   di **PDF 164** (jangkar yang ditulis: 163).
8. **Satu rujukan `KEMAMPUAN.md` tidak ada di rak.** Baris `SYS-006` menyebut "Blanchard &
   Fabrycky, Systems Engineering and Analysis"; penyapuan nama berkas di seluruh
   `03_SOURCE-VAULT` menemukan **0** berkas mengandung "Fabrycky" (laci SYSTEMS-ENGINEERING
   hanya 3 PDF, sesuai `_ISI.md`).
9. **KATALOG-RUMUS tidak punya seksi rekayasa sistem** (0 hitung pola, lihat mata ③);
   pengisian katalog bukan wewenang LOCK ini.

Butir 1-5 menyangkut berkas resume di `05_DOMAIN-KNOWLEDGE/SYSTEMS-ENGINEERING/` (milik
gelombang W3a/BUKUV3), butir 6-8 menyangkut `KEMAMPUAN.md` (digest mesin dari
`KEMAMPUAN-REGISTER.csv`), butir 9 menyangkut `06_ENGINEERING/CALCULATIONS/`. Jalur mediasi
ke profil pemilik adalah wewenang controller (M2).

---

## CATATAN KOREKSI TERTANGGAL (run lanjutan kartu ini, 11-10-2026)

Short-check deterministik pada run penutup (setelah run kerja kena cap runtime) menandai 8
baris tabel berangka tanpa penanda sumber per-baris. Isi angka TIDAK berubah; yang ditambah
hanya kolom Tag/Sumber agar setiap baris berdiri sendiri saat dibaca lintas potongan:

1. Tabel "Konversi halaman" (mata ①): ketiga baris bukti ukur diberi penanda
   `[UKUR-RUN-INI, vault PDF, 11-10-2026]` di depan daftar pasangan folio.
2. Tabel sensitivitas bobot pertama (mata ③): dua kolom baru "Tag" dan "Sumber" ditambahkan;
   kelima baris skenario kini membawa `ASSUMPTION` + rujukan turunan `[R3, Kossiakoff SEPP,
   PDF 326]`. Nilai skor 3,4500 / 3,2667 / 3,6333 / 3,5294 / 3,3462 tidak disentuh dan tetap
   hasil hitung ulang run kerja (skrip yang sama menghasilkan tabel ini).

Tidak ada suntingan senyap; tidak ada berkas lain yang disentuh (LOCK tetap satu berkas ini).
