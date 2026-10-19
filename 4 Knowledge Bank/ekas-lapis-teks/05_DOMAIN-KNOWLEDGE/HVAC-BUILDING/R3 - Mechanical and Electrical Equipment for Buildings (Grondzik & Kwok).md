# Mechanical and Electrical Equipment for Buildings

**REF-HVA-001** · **R3** · Domain **HVAC-BUILDING** · Grondzik & Kwok
**Berkas:** **1.855 halaman** · **1.454 bookmark** · `R3/HVAC-BUILDING/`

---

## Buku terbesar di rak

Tebalnya hampir dua kali buku mana pun, dan bookmark-nya terbanyak — **1.454 entri**,
navigasinya sangat baik meski isinya raksasa.

Cakupannya jauh melampaui HVAC: **kelistrikan gedung, akustik, proteksi kebakaran, sistem
sinyal, dan transportasi vertikal** ada di dalamnya.

## Susunan

| Bagian | Isi | PDF |
|---|---|---|
| I | Konteks perancangan bangunan | **27** |
| II | Dasar perancangan | **133** |
| III | Sistem lingkungan pasif | **265** |
| **IV** | **Sistem lingkungan aktif** — HVAC, 594 halaman | **445** |
| V | **Akustik** | **1039** |
| **VI** | **Proteksi kebakaran** | **1165** |
| **VII** | **Kelistrikan** | **1243** |
| **VIII** | **Sistem sinyal** | **1433** |
| IX | Transportasi (lif, eskalator) | **1469** |
| X | Apendiks | **1581** |

## Yang paling berguna bagi GSP

**Bagian VII — kelistrikan (PDF 1243).** Distribusi daya gedung, panel, pembumian, dan
penerangan. Titik temu langsung dengan pemasangan perangkat.

**Bagian VIII — sistem sinyal (PDF 1433).** Membahas sistem komunikasi, alarm, dan keamanan
**sebagai bagian dari bangunan** — sudut pandang yang tidak ada di buku lain di rak, dan
justru itu yang dipakai konsultan bangunan saat menilai rancangan GSP.

**Bagian IV — HVAC (PDF 445).** Menjawab pendinginan ruang perangkat: beban pendinginan,
jenis sistem, dan distribusi udara. Melengkapi rugi daya UPS dari rantai C.

**Bagian VI — proteksi kebakaran (PDF 1165).** Bersama Building Codes Illustrated Bab 7.

## Batas pemakaian

> Terverifikasi PDF 41: pembahasan **energi operasional dan energi terkandung** dalam
> keputusan perancangan. Buku ini berorientasi **perancangan bangunan berkelanjutan** —
> sebagian besar isinya lebih relevan bagi arsitek dan konsultan MEP daripada bagi pemasang
> perangkat.
>
> Bagi GSP, **empat bagian saja yang benar-benar terpakai**: IV, VI, VII, VIII.

Standar dan angka yang dirujuk Amerika — ASHRAE, NEC, NFPA. **Tidak ada di rak.**
Indonesia memakai SNI dan PUIL, juga tidak ada.

## Menopang

Gate **G2** — perancangan ruang perangkat dan integrasi ke sistem bangunan.
Rantai **C** (catu daya) dan **F** (termografi) bersinggungan dengan Bagian IV dan VII.

---

## Catatan verifikasi R3B, 11 Oktober 2026

Kartu RESUME-R3 tulis-B (t_885a4eb8, misi KORPUS-LANJUTAN-1011): verifikasi isi tanpa duplikasi. Resume dibaca ulang terhadap berkas vault `R3_TEXTBOOK-HANDBOOK/HVAC-BUILDING/Walter T. Grondzik, Alison G. Kwok - Mechanical and Electrical Equipment for Buildings (2014, Wiley) - libgen.li.pdf` lewat pembacaan objek PDF (pypdf, Python 3.11): tebal 1.855 halaman cocok; jumlah bookmark 1.454 cocok persis dengan hitungan mesin pada pohon outline berkas; kesepuluh jangkar bagian pada PDF 27, 133, 265, 445, 1039, 1165, 1243, 1433, 1469, dan 1581 terbukti membuka bagian yang sesuai; tebal Bagian IV sebesar 594 halaman cocok dari selisih jangkar IV ke V; istilah "operational energy" terbukti muncul pada PDF 41 sesuai klaim batas pemakaian.

Folio cetak bergeser tetap 26 nomor terhadap posisi PDF (Bagian II terbuka pada folio 107). Tidak ada koreksi; isi di atas dibiarkan apa adanya. Daya-ikat tidak naik: R3. Domain ini masih tanpa rantai jaminan di disk, sebagaimana telah dinyatakan di kartu; penyusunan rantai bukan lingkup kartu ini. Vonis register `ACTIVE` dan probe RR3 (`butuh_resume = false`) terkonfirmasi dari ukur langsung.
