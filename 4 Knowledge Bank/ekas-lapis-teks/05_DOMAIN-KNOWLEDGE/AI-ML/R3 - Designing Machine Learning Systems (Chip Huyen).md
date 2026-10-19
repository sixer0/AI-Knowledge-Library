# Resume — Designing Machine Learning Systems (Chip Huyen, 2022)

**Penulis:** Chip Huyen · **Penerbit:** O'Reilly Media, 2022
**Berkas vault:** `03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/AI-ML/Chip Huyen - Designing Machine Learning Systems...pdf` — 389 hlm PDF
**Disusun:** 09 Oktober 2026, dari teks hasil ekstraksi lokal (pypdf, penanda halaman PDF utuh)
**Status daya-ikat:** `pending_verification` (P-5 BUKUV3-ING-1009) — sah untuk **metode dan penalaran dengan kutipan halaman**; **belum sah** menambat ambang terima.

> **Konversi halaman.** Halaman cetak + 20 = halaman PDF (folio `1` tercetak di PDF 21, terverifikasi ekstraksi).
> Di seluruh dokumen ditulis nomor **PDF**; contoh: `[R3, Huyen ML Systems, PDF <n>]`.

---

## 1. Inti dalam satu halaman

Buku ini memperlakukan sistem ML sebagai masalah **rekayasa**, bukan ilmu model: proses iteratif
dari objektf bisnis ke sistem produksi, dengan penekanan pada data, evaluasi, dan operasi.
Peta bab dari bookmark PDF: bab 1 Overview (PDF 21), bab 2 Systems Design (PDF 45), bab 3 Data
Engineering (PDF 69), bab 4 Training Data (PDF 101), bab 5 Feature Engineering (PDF 139),
bab 6 Model Development (PDF 169).

## 2. Bagian bertambat halaman (hasil buka teks, bukan daftar isi)

| Butir | Isi | Letak |
|---|---|---|
| Prioritas produksi vs riset | riset mengejar throughput, produksi mengejar latensi rendah | `[R3, Huyen ML Systems, PDF 36]` |
| Class imbalance | definisi dan tantangan ketidakseimbangan kelas pada data latih | `[R3, Huyen ML Systems, PDF 122]` |
| Data leakage | "subtle yet disastrous problem" — penyebab kegagalan sistem ML produksi | `[R3, Huyen ML Systems, PDF 139]` |
| Champion–challenger | model lama = champion, replika ter-update = challenger sebelum promosi | `[R3, Huyen ML Systems, PDF 284]` |
| Shadow deployment | jalur uji-paling-aman: model baru melayani cerminan trafik tanpa efek ke pengguna | `[R3, Huyen ML Systems, PDF 302]` |
| Model calibration | probabilitas keluaran harus cocok frekuensi kejadian sebenarnya; metode hitung langsung | `[R3, Huyen ML Systems, PDF 203]` |
| Matriks konfus | contoh terhitung deteksi kanker 10/100 kasus untuk menjelaskan sensitivitas | `[R3, Huyen ML Systems, PDF 126]` |
| Feature store | infrastruktur fitur lintas aplikasi, bab 10 | `[R3, Huyen ML Systems, PDF 162]` |
| Validasi data | alat validasi (TFX) memakai statistik ringkas untuk deteksi skew train-vs-serving | `[R3, Huyen ML Systems, PDF 250]` |
| Latensi vs akurasi | toleransi konsumen berbeda per domain (contoh akurasi pengenalan bicara 95→95,5%) | `[R3, Huyen ML Systems, PDF 110..112]` |

## 3. Metode yang bisa diadopsi (tanpa angka ambang)

- Alur desain iteratif: tetapkan objektif bisnis → requirements → framing masalah ML →
  data → fitur → model → deploy → monitor (`[R3, Huyen ML Systems, PDF 45..55]`).
- Gerbang rilis berbasis champion/challenger + canary/shadow, bukan adu skor offline saja

## 4. Batas pemakaian

- R3 textbook: **tidak menetapkan ambang terima**; adopsi angka apa pun butuh kontrak tertulis.
- Status register `pending_verification` sampai verifier W3 menandatangani resume ini.
- Kartu batas: `04_KNOWLEDGE-CARDS/AI-ML/REF-AIM-001*.md`.
