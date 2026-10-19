# Resume — Hands-On Machine Learning with Scikit-Learn, Keras & TensorFlow (Géron, 2019)

**Penulis:** Aurélien Géron · **Edisi:** kedua · **Penerbit:** O'Reilly Media, 2019
**Berkas vault:** `03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/AI-ML/[2] Aurélien Géron - Hands-On Machine Learning...pdf` — 1.065 hlm PDF
**Disusun:** 09 Oktober 2026, dari teks ekstraksi lokal (pypdf; ekstraksi bergaya tab-spasi, folio tidak terbaca — SEMUA rujukan = halaman PDF dari bookmark berkas, bukan halaman cetak)
**Status daya-ikat:** `pending_verification` (P-5) — metode/penalaran berhalaman boleh; ambang terima belum.

## 1. Peta bab (bookmark PDF terverifikasi isi teks)

| Bab | Topik | PDF |
|---|---|---|
| 1 | The Machine Learning Landscape — jenis sistem ML, tantangan utama | `[R3, Géron HOLML, PDF 19]`, `[R3, Géron HOLML, PDF 27]`, `[R3, Géron HOLML, PDF 46]` |
| 2 | End-to-End ML Project — ambil data, visualisasi, siapkan, latih, fine-tune | `[R3, Géron HOLML, PDF 60]`, `[R3, Géron HOLML, PDF 84]`, `[R3, Géron HOLML, PDF 92]`, `[R3, Géron HOLML, PDF 103]`, `[R3, Géron HOLML, PDF 108]` |
| 3 | Classification — MNIST, ukur unjuk kerja, multikelas | `[R3, Géron HOLML, PDF 121]`, `[R3, Géron HOLML, PDF 126]`, `[R3, Géron HOLML, PDF 140]` |
| 4 | Training Models — regresi linear, gradient descent | `[R3, Géron HOLML, PDF 154]`, `[R3, Géron HOLML, PDF 161]` |

## 2. Butir bertambat (teks dibuka)

- Regularisasi: "constraining a model to make it simpler and reduce the risk of overfitting"; kekuatan diatur hyperparameter — `[R3, Géron HOLML, PDF 52]`–`[R3, Géron HOLML, PDF 53]`.
- Holdout validation: sisihkan bagian data latih untuk memilih model terbaik — `[R3, Géron HOLML, PDF 55]`.
- Cross-validation berulang sebagai solusi validasi kecil — `[R3, Géron HOLML, PDF 56]`.
- Overfitting/underfitting (bias-variance) dijelaskan lewat contoh polinomial — `[R3, Géron HOLML, PDF 8]`–`[R3, Géron HOLML, PDF 8]`.
- Ensemble learning sebagai penumpangan banyak model — `[R3, Géron HOLML, PDF 107]`.
- Heading "Performance Measures" & pengukuran akurasi dengan cross-validation untuk classifier — `[R3, Géron HOLML, PDF 126]`.
- Implementasi gradient descent dengan `eta = 0.1` (nilai contoh, bukan ambang) — `[R3, Géron HOLML, PDF 167]`.

## 3. Metode yang bisa diadopsi

Alur proyek end-to-end (bab 2) sebagai kerangka kerja lintang: definisi → data → pengamatan → pembersihan → fitur → seleksi model → tuning → produksi (`[R3, Géron HOLML, PDF 60..118]`). Bukan sumber ambang.

## 4. Batas pemakaian

- R3 textbook praktis; nilai hyperparameter di contoh = ilustrasi kode, bukan angka desain GSP.
- `pending_verification` sampai verifier; kartu: `04_KNOWLEDGE-CARDS/AI-ML/REF-AIM-003*.md`.


## 5. Butir bertambat tambahan (tambalan W10 BUKUV3-JURY-1009, 09-10-2026)

Diambil verbatim dari halaman vault yang dibuka ulang dengan pdftotext (Xpdf 4.06); sebelumnya butir ini hanya disebut judul/nama tanpa badan aturan. Daya-ikat tetap `pending_verification` (P-5) — tidak naik.

- Badan rumus RMSE (Equation 2-1, tercetak utuh): RMSE(X, h) = sqrt( (1/m) * SUM_{i=1..m} (h(x^(i)) - y^(i))^2 ). Teks pembuka: "A typical performance measure for regression problems is the Root Mean Square Error (RMSE). It gives an idea of how much error the system typically makes in its predictions, with a higher weight for large errors." Notasi: "m is the number of instances in the dataset you are measuring the RMSE on." — `[R3, Géron HOLML, PDF 65]`
  Sumber lengkap: Hands-On Machine Learning 2e - Geron (2019, O'Reilly) [vault R3/AI-ML] pdf_p65 (cetak 26 = pdf - 39, offset konsisten dengan pdf_p127/cetak 88 & pdf_p137/cetak 98; awal bab 2 di pdf_p60 = cetak 21) | jejak ukur: F2-AIM-04
