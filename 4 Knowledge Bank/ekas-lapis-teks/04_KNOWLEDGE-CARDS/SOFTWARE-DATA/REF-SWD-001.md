---
record_type: knowledge_card
reference_id: REF-SWD-001
reference_confidence_level: R5
title: "Deep Learning (LeCun, Bengio & Hinton - Nature 2015)"
domain: SOFTWARE-DATA
authority_status: POINTER_ONLY
vault_path: 03_SOURCE-VAULT/R5_RESEARCH-SECONDARY/PAPERS
resume_path: '05_DOMAIN-KNOWLEDGE/SOFTWARE-DATA/R5 - Deep Learning (LeCun, Bengio & Hinton 2015).md'
---

# REF-SWD-001 - Deep Learning (Nature 2015)

**R5 - sumber sekunder** | **Status:** `POINTER_ONLY` | **9 halaman PDF** (halaman cetak
436-444, *Nature* 521, 28 Mei 2015, doi 10.1038/nature14539)
**Resume:** `05_DOMAIN-KNOWLEDGE/SOFTWARE-DATA/R5 - Deep Learning (LeCun, Bengio & Hinton 2015).md`
**Bukti byte:** sha256[:16] `94a90d959c5c5c06`, 5.549.808 B, diukur dari vault 11 Okt 2026
(berkas sumber READ-ONLY, tidak disentuh).
**Lapisan jangkar halaman** dipasang kartu ini pada RESUME-R3 tulis-C (kartu t_6537fbe6,
langkah 20/G2) lewat uji-cocok teks `pdftotext -layout` atas berkas vault. Daya-ikat
TIDAK dinaikkan: perubahan `POINTER_ONLY` adalah putusan kurasi langkah 21.

## 1. Yang dipasok rujukan ini

Tinjauan tingkat gagasan pembelajaran mendalam: representasi berjenjang, jaringan
konvolusi, jaringan berulang, dan propagasi balik untuk melatih arsitektur berlapis.
Berguna untuk memahami istilah yang muncul pada spesifikasi analitik video dan ASR.
**Tidak** memuat rumus siap pakai, ambang unjuk kerja, maupun panduan penerapan.

## 2. Peta halaman (terukur 11-10-2026; penanda `pdf_pn` = halaman PDF, bukan halaman cetak)

| Letak PDF | Isi | Hal. cetak |
|---|---|---|
| pdf_p1 | Abstrak + pendahuluan; kepala seksi "Supervised learning" | 436 |
| pdf_p2 | Lanjutan supervised learning; **Gambar 1** jaringan berlapis + propagasi balik | 437 |
| pdf_p3 | Kepala "Backpropagation to train multilayer architectures"; sub-kepala "Convolutions and ReLU", "Max pooling"; **Gambar 2** interior jaringan konvolusi | 438 |
| pdf_p4 | Aplikasi jaringan konvolusi (pengenalan citra/objek); wacana unsupervised | 439 |
| pdf_p5 | **Gambar 3** dari citra ke teks (caption otomatis); pengucapan ujaran | 440 |
| pdf_p6 | Vektor kata; terjemahan mesin (wacana urutan-ke-urutan) | 441 |
| pdf_p7 | **Gambar 5** jaringan berulang dan bentangannya dalam waktu; memori jangka pendek-panjang (LSTM); Krizhevsky dkk.; dependensi jangka panjang | 442 |
| pdf_p8 | Wacana pembelajaran tanpa pengawasan; daftar pustaka dimulai | 443 |
| pdf_p9 | Daftar pustaka s.d. butir 103 (t-SNE, van der Maaten & Hinton); afiliasi dan korespondensi | 444 |

Dasar pemetaan (mekanis, dapat diulang): 9 blok teks hasil `pdftotext -layout` (batas
form-feed), kaki halaman tercetak hanya muncul pada blok ganjil (436/438/440/442/444)
karena halaman genap adalah sisi spread yang sama; posisi topik per halaman dari pencarian
token atas lapisan teks yang sama. Bentuk kutipan: `[R5, LeCun-Bengio-Hinton Nature 2015, pdf_p3]`.

## 3. Boleh menetapkan ambang terima?

**Tidak pernah.** Dua alasan berlapis: (a) R5 adalah penunjuk ke sumber primer, bukan
sandaran akhir; (b) `authority_status` `POINTER_ONLY`. Angka unjuk kerja analitik wajib
dari **R4** (lembar data produk analitik yang dipakai). Uji teks seluruh badan makalah
menemukan tepat satu persen numerik berupa anekdot historis pembacaan cek ("over 10% of
all the cheques", pdf_p4); tidak ada tabel atau angka ambang unjuk kerja.

## 4. Batas pemakaian - baca sebelum mengutip

- Makalah tinjauan, **bukan buku teks**: keliru dinilai R3 pada 20 Agustus 2026,
  dikoreksi 21 Agustus 2026 dan dipindah ke `R5_RESEARCH-SECONDARY/PAPERS/`.
- Terbit 2015 (11 tahun); bidang berubah cepat, arsitektur yang dibahas bukan yang
  mutakhir. Catatan: penulisan "(AlexNet, LSTM)" di resume lama tidak literal terhadap
  isi makalah - lihat butir koreksi 5.
- Jangkar kutipan wajib menunjuk penanda `pdf_pn` pada tabel 2; tanpa penanda, kutipan
  dari rujukan ini tidak boleh naik ke dokumen serah.

## 5. Catatan koreksi dan verifikasi tertanggal (bukan sunting senyap)

1. **2026-10-11, kartu t_6537fbe6 (langkah 20/G2), dari ukur `pdftotext`:** versi kartu
   sebelumnya (981 B) menyatakan laci `R3_TEXTBOOK-HANDBOOK/SOFTWARE-DATA/` **kosong** dan
   "rak tidak punya buku teks pembelajaran mesin sama sekali". Kedua pernyataan BASI per
   ukur disk hari ini: laci vault SOFTWARE-DATA berisi 2 buku (`Site Reliability
   Engineering` Beyer, 10.024.372 B = REF-SWD-002; `Designing Data-Intensive Applications`
   Kleppmann, 24.975.901 B = REF-SWD-003; tercatat pula di `_ISI.md` laci), dan 4 buku ML
   inti sudah diserap ke laci `R3/AI-ML` pada W1b 09-10-2026 dengan status
   `pending_verification` (catatan GAP-021 yang kini `sebagian`). Celah sebenarnya bukan
   "rak kosong" melainkan "pengganti bertingkat buku teks belum lolos verifier (P-5)".
2. **2026-10-11, sama kartu:** token "AlexNet" **nol kemunculan** di badan teks makalah;
   yang muncul adalah Krizhevsky dkk. (pdf_p7-p8), sedangkan LSTM/long short-term muncul
   (pdf_p7, pdf_p9). Frasa "(AlexNet, LSTM)" pada resume lama adalah ringkasan penulis,
   bukan frasa makalah; jangan dikutip seolah dari sumber. Resume kanonis `R5 - ...md`
   berada di luar glob LOCK langkah 20 sehingga tidak disunting; perbaikan frasa dan
   pemindahan peta halaman tabel 2 ke resume adalah opsi kurasi langkah 21 (gsp-librarian).

## 6. Rantai jaminan

```
REQUIREMENT -> REF-SWD-001 (R5, penunjuk) -> SUMBER PRIMER yang ditunjuk -> ... -> TERIMA
```

R5 tidak pernah berdiri sendiri sebagai sandaran keputusan; ia menunjuk sumber primernya.
Rantai domain `SOFTWARE-DATA` belum terbit di disk saat kartu ini ditulis
(`RANTAI-JAMINAN.md` menyusul hasil langkah 17/G2). Gate minimum G0-G7:
`01_GOVERNANCE/ASSURANCE-GATES.md`.
