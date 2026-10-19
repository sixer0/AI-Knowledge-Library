# Resume — Empat Panduan Keamanan Siber Operasional

**Total:** 238 halaman · **Disusun:** 19 Agustus 2026 · **Rujukan halaman memakai nomor PDF**

Empat dokumen panduan — bukan buku teks, bukan standar formal. Sifatnya **petunjuk kerja
yang dapat langsung diterapkan**, tiga di antaranya terbitan 2024 sehingga termutakhir di
rak untuk topik keamanan operasional.

| Dokumen | Penerbit | Hal | Sifat |
|---|---|---|---|
| **Detecting and Mitigating Active Directory Compromises** | ASD, CISA dkk. (Sep 2024) | 86 | Panduan teknis gabungan |
| **Best Practices for Event Logging and Threat Detection** | Joint CSI (2024) | 17 | Panduan ringkas gabungan |
| **NIST SP 800-50r1 — Building a Cybersecurity and Privacy Learning Program** | NIST | 87 | Publikasi khusus |
| **ITSECBuzz Edisi II** | ITSEC Asia (Okt 2024) | 48 | Majalah, konteks Indonesia |

---

## 1. Detecting and Mitigating Active Directory Compromises (PDF, 90 bookmark)

Disusun bersama **Australian Signals Directorate (ASD)**, **CISA**, dan badan sejenis
negara lain. Terbit September 2024.

Membahas **teknik kompromi Microsoft Active Directory** beserta cara mendeteksi dan
menanggulanginya. AD adalah pusat identitas hampir semua jaringan korporat dan instansi —
begitu AD dikuasai, seluruh jaringan ikut.

**Dipakai untuk:** menyusun bagian pengerasan (hardening) identitas pada rancangan
infrastruktur pelanggan; menjawab pertanyaan panitia tentang perlindungan terhadap
pengambilalihan domain; daftar periksa audit AD.

Bertemu dengan `R3/SECURITY/` (Anderson) Bab 6 *Access Control* — Anderson memberi
kerangka berpikirnya, dokumen ini memberi teknik konkretnya pada satu produk.

## 2. Best Practices for Event Logging and Threat Detection (17 hal, 28 bookmark)

Panduan gabungan antar-badan, ringkas dan padat. Isinya menurut daftar isinya:
**kebijakan pencatatan log yang disetujui perusahaan**, **mutu log**, **rincian yang wajib
tertangkap**, dan praktik operasionalnya.

**Ini yang paling langsung terpakai untuk lini DEMS.** Sistem manajemen bukti digital
berdiri di atas catatan yang dapat dipercaya — dan dokumen ini menetapkan apa yang membuat
sebuah log bermutu, bukan sekadar ada.

**Dipakai untuk:** merancang kebijakan pencatatan pada sistem bukti digital; menetapkan
rincian minimum yang harus tertangkap; menyusun bagian jejak audit pada proposal.

Bertemu dengan `R3/SECURITY/` (Anderson) Bab 14 *Monitoring and Metering* dan dengan tesis
Nana Mulyana di `_tesis/` yang memetakan log ke tahapan serangan.

## 3. NIST SP 800-50r1 — Membangun Program Pembelajaran Keamanan dan Privasi (87 hal)

Revisi 1 dari SP 800-50. Membahas cara membangun **program pembelajaran keamanan siber dan
privasi** dalam organisasi — bukan pelatihan sekali jalan, melainkan program berkelanjutan.

**Dipakai untuk:** menyusun bagian pelatihan dan peningkatan kesadaran pada usulan layanan;
menjawab persyaratan tender yang menuntut program pembinaan personel; kerangka kurikulum
internal.

Bertemu dengan `R3/RCM/` (Nyman & Levitt) Apendiks C dan `R3/OPERATIONS/`
(Limoncelli) Bagian IX untuk sisi pengelolaan orangnya.

## 4. ITSECBuzz Edisi II, Oktober 2024 (48 hal)

Majalah keamanan siber berbahasa Indonesia. **Satu-satunya bahan berkonteks Indonesia di
kelompok ini.**

Isi utama edisi ini: **kesiapan perusahaan mematuhi UU PDP** (Perlindungan Data Pribadi),
bedah malware Android, dan potensi dark web dalam keamanan siber.

**Dipakai untuk:** memahami wacana kepatuhan **UU PDP** yang sedang berjalan di Indonesia;
bahan latar untuk bagian perlindungan data pribadi pada proposal.

> **Perlakukan sebagai bacaan latar, bukan rujukan.** Majalah bukan sumber yang dikutip
> dalam dokumen teknis. Untuk UU PDP, kutip **undang-undangnya**, bukan ulasannya.

---

## Pemakaian di GSP

| Keperluan | Dokumen |
|---|---|
| Pengerasan identitas / Active Directory | ASD-CISA (2024) |
| **Kebijakan dan mutu pencatatan log** | **Joint CSI (2024)** |
| Rancangan jejak audit sistem bukti digital | Joint CSI (2024) + Anderson Bab 14 |
| Program pelatihan dan kesadaran keamanan | NIST SP 800-50r1 |
| Latar kepatuhan UU PDP Indonesia | ITSECBuzz (bacaan latar saja) |

---

## Batas keempatnya

- **Bukan standar yang dapat dikutip sebagai persyaratan.** Ketiganya panduan (*guidance*),
  ITSECBuzz bahkan majalah. Untuk persyaratan kontrak, kutip standar formal.
- **Berorientasi produk/lingkungan tertentu** — dokumen AD khusus Microsoft Active Directory.
- **ISO/IEC 27001 masih belum ada di rak.** Keempat dokumen ini tidak menggantikannya.
- **UU PDP sendiri belum ada di rak** — hanya ulasannya di ITSECBuzz.

---

## Catatan: dua buku ditahan di `New folder`

Dari kelompok "Cyber Security Books" yang diserahkan, dua berkas sebenarnya **buku utuh**
dan pantas mendapat perlakuan penuh, bukan perlakuan ringan seperti empat dokumen di atas:

| Buku | Hal |
|---|---|
| *The NICE Cyber Security Framework — Cyber Security Intelligence and Analytics* (Alsmadi) | 366 |
| *Cybersecurity: Protecting Critical Infrastructures from Cyber Attack and Cyber Warfare* (Johnson) | 346 |

Yang kedua relevan untuk pekerjaan objek vital. Keduanya **belum diproses** — menunggu
keputusan apakah masuk batch berikutnya dengan perlakuan penuh.

Tiga berkas lain di kelompok itu (dua tentang quantum, satu sejarah kriptografi) tidak
menyentuh lini kerja yang sedang berjalan.
