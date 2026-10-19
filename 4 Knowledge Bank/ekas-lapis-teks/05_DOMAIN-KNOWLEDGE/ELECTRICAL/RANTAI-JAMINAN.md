# Rantai E — Uji instalasi listrik (tahanan isolasi)

**Ambang terima berasal dari:** **ANSI/NETA ATS-2017 [R2]** — rantai paling kuat di rak ini

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman |
|---|---|---|---|
| **ANSI/NETA ATS-2017** | **R2** | Ambang MΩ mutlak (Tabel 100.1) · faktor koreksi suhu (Tabel 100.14) | PDF 223, 241 |
| Gill, *Electrical Power Equipment Maintenance* (2008) | **R3** ⚠18 th | PI, DAR, empat metode ukur, batas tegangan uji | PDF 142, 144, 145 |
| **PUIL / SNI** | **R1** | Kepatuhan Indonesia | ❌ **TIDAK ADA** |
| Lembar data peralatan | **R4** | Tegangan uji pabrik, batas khusus produk | per proyek |

> **Catat perbedaan cakupan:** yang ada di rak adalah **ATS** — *Acceptance Testing*, uji
> **terima** instalasi baru. Uji **pemeliharaan** berkala diatur **MTS**, dan **MTS tidak ada
> di rak.** Untuk pekerjaan pemeliharaan, ambangnya belum bersandar penuh.

---

## ② Keputusan desain

| Yang ditetapkan | Dasar | Alternatif yang ditolak |
|---|---|---|
| Metode pengukuran isolasi | Empat metode — Gill PDF 142 | Pengukuran sesaat saja ditolak untuk peralatan besar — tidak menampakkan tren |
| Tegangan uji yang dipakai | Batas pada mata ③ | Menaikkan tegangan "agar meyakinkan" **ditolak** — merusak isolasi yang diuji |
| Suhu saat pengukuran | Dicatat, lalu dikoreksi | Membandingkan hasil antar-waktu tanpa koreksi suhu **ditolak** — selisihnya bisa lebih besar daripada degradasinya |
| Kriteria penilaian | **Rasio (PI, DAR) + MΩ mutlak [R2] + tren** | Salah satu saja ditolak — ketiganya menangkap gejala berbeda |

> **CATATAN DEFECT (NWSKILL-0923/D3-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-8 (konflik instruksi, bukan angka): baris 'Kriteria penilaian' di atas bertentangan secara harfiah dengan 'Bila uji PI dilakukan, uji DA tidak perlu lagi' (`R3 - Electrical Power Equipment Maintenance and Testing.md:117-118`; `KATALOG-RUMUS.md:252`; `TEMPLATE-BERITA-ACARA.md:125`) dan dengan `:70-71` 'ketiga kriteria itu tidak saling menggantikan'. Rekonsiliasi sah dari teks: yang tidak saling menggantikan adalah rasio vs MΩ mutlak vs tren; di dalam keluarga rasio, PI menggantikan peran DA; DAR opsional bila PI dikerjakan. Rak tidak pernah menuliskan pembedaan ini secara eksplisit sehingga pembacaan harfiah menghasilkan instruksi bertentangan (kerjakan DAR atau jangan kerjakan DAR). Penegas resmi milik objek IL (rujukan PDF 659); jangan ratakan salah satu sisi saat mengutip kartu/rantai ini.

---

## ③ Perhitungan

### Polarization Index — [R3, Gill PDF 144]

```
PI = R₁₀menit ÷ R₁menit          ambang perhatian: PI < 1
```

### Dielectric Absorption Ratio — [R3, Gill PDF 144]

```
DAR = R₆₀detik ÷ R₃₀detik        ambang perhatian: DAR < 1,25
```

### Batas tegangan uji rutin — [R3, Gill PDF 145]

```
V_uji_rutin  ≤ 75% × V_uji_terima
V_uji_rutin  ≤ 60% × V_uji_pabrik
```

### Koreksi ke suhu acuan — [R2, ATS-2017 Tabel 100.14 PDF 241]

Hasil ukur dikalikan faktor koreksi menuju **20 °C**. Tanpa langkah ini, perbandingan
antar-waktu tidak bermakna.

### Contoh terhitung

Motor 600 V, hasil ukur 62 MΩ pada 30 °C:

```
1. Koreksi ke 20 °C   : 62 MΩ × faktor Tabel 100.14   → nilai terkoreksi
2. Bandingkan ambang  : Tabel 100.1, 600 V → minimum 100 MΩ   [R2]
3. Periksa rasio      : PI dan DAR                             [R3]
4. Periksa tren       : terhadap hasil uji sebelumnya
```

**Bila nilai terkoreksi < 100 MΩ → tidak memenuhi ambang [R2]**, walaupun PI dan DAR
terlihat baik. Ketiga kriteria itu tidak saling menggantikan.

> **CATATAN DEFECT (NWSKILL-0923/D3-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-1 (CALON DEFECT SUBSTANTIF, TINGGI - menunggu putusan manusia/controller): contoh terhitung di atas memakai 'Motor 600 V' lalu membandingkannya dengan ambang Tabel 100.1 (`:61,:65,:70`), padahal tabel yang dirujuk berjudul 'Insulation Resistance Test Values, Electrical Apparatus and Systems Other Than Rotating Machinery' (`R2 - ANSI-NETA ATS-2017.md:41-42`) dan kolom koreksi suhu pun mengecualikan 'Isolasi padat (bukan mesin berputar)' (`R2 - ANSI-NETA ATS-2017.md:67`). Contoh satu-satunya di domain ini mengajari pembaca membandingkan motor dengan angka yang cakupan tabelnya tidak mencakup motor; vonis berubah tergantung kolom koreksi (97,96 vs 122,76 MΩ, register studi 3.2). Lapis lain tidak mengulang contoh ini (nol pewarisan), tetapi rantai inilah kerangka berita acara. Opsi putusan: ganti contoh menjadi peralatan non-berputar (panel 600 V), tambah kalimat pengecualian di mata (3), atau tandai contoh sebagai ilustrasi metode saja. Isi tidak diubah oleh pekerja.

---

## ④ Pengujian

| Butir | Ambang | Sumber |
|---|---|---|
| **Tahanan isolasi mutlak** | **Tabel 100.1** — 600 V → **100 MΩ** · 5 kV → **1.500 MΩ** · 15 kV → **5.000 MΩ** | **R2** — ATS-2017 PDF 223 |
| **Koreksi suhu** | Tabel 100.14 → 20 °C | **R2** — PDF 241 |
| Polarization Index | < 1 → selidiki | R3 — Gill PDF 144 |
| Dielectric Absorption Ratio | < 1,25 → selidiki | R3 — Gill PDF 144 |
| Batas tegangan uji | ≤ 75% terima · ≤ 60% pabrik | R3 — PDF 145 |
| Tren antar-waktu | Penurunan berarti | R3 |

> **CATATAN DEFECT (NWSKILL-0923/D3-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-2 (cacat propagasi syarat, TINGGI): baris Tabel 100.1 pada tabel di atas disajikan tanpa caveat yang melekat di sumbernya. R2 mensyaratkan nilai Tabel 100.1 berlaku 'bila tidak ada standar konsensus lain' dan memberi prioritas ke spesifikasi pabrikan (`R2 - ANSI-NETA ATS-2017.md:57-59,:149-150`; caveat tercetak juga di `KATALOG-RUMUS.md:454`). Tanpa caveat, gerbang mutu memperlakukan 100 MΩ sebagai ambang mutlak tanpa syarat - persis pola pemicu angka salah pada dokumen serah. Beda dengan K-1: ini soal syarat pemakaian, bukan beda nilai. Klausul caveat wajib ikut naik ke objek IL dan ke setiap kutipan baris ini.

> **Rantai ini yang paling kuat di seluruh rak** — ambangnya normatif [R2], metodenya
> terjelaskan [R3], dan keduanya saling melengkapi tanpa tumpang tindih: NETA memberi
> **berapa**, Gill memberi **mengapa dan bagaimana**.

> **CATATAN DEFECT (NWSKILL-0923/D3-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-9 (inkonsistensi frasa, RENDAH): berkas ini mengklaim dua cakupan berbeda - ':3' 'rantai paling kuat di rak ini' dan ':86' 'paling kuat di seluruh rak'. Substansinya bertahan (POWER-BACKUP mengklaim UTUH hanya pada baterai/ventilasi dan MENUNGGU R4 pada genset/UPS, `POWER-BACKUP/RANTAI-JAMINAN.md:136`) tetapi objek IL wajib memakai SATU bentuk klaim; usulan studi: 'terkuat di rak, dengan dua celah normatif: MTS dan PUIL'. Tidak ada angka yang terpengaruh.

**Yang tetap harus dinyatakan:** ATS-2017 adalah standar **Amerika**. Bila kontrak menuntut
kepatuhan **PUIL**, standar ini **bukan penggantinya** — ia menutup celah *ambang uji*, bukan
celah *kepatuhan hukum Indonesia*.

---

## ⑤ Bukti serah

| Lampiran | Wajib | Catatan |
|---|---|---|
| Berita acara uji tahanan isolasi | ✅ | Kerangka bagian 3 |
| Tabel hasil: nilai terukur, **suhu saat ukur**, nilai terkoreksi | ✅ | Suhu sering tidak dicatat — hasilnya jadi tidak dapat dibandingkan |
| **Ambang Tabel 100.1 yang berlaku + tegangan nominal peralatan** | ✅ | Sebutkan barisnya, bukan hanya nama standarnya |
| Nilai PI dan DAR | ✅ | Beserta waktu pembacaan |
| Tegangan uji yang dipakai + dasar pembatasannya | ✅ | Melindungi bila isolasi rusak saat uji |
| Sertifikat kalibrasi megger | ✅ | — |
| Riwayat hasil sebelumnya bila ada | ✅ | Tren lebih bermakna daripada satu titik |
| Kartu kendali rantai | ✅ | — |

**Status rantai: UTUH.** Satu-satunya rantai di rak ini yang ambang, metode, dan koreksinya
seluruhnya bersandar sumber tertulis — dan dua di antaranya [R2].

**Yang masih terbuka:** **ANSI/NETA MTS** untuk uji pemeliharaan, dan **PUIL/SNI** untuk
kepatuhan Indonesia.
