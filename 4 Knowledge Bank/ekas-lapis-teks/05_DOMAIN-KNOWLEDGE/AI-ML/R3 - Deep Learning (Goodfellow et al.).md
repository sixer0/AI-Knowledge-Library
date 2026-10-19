# Resume — Deep Learning (Goodfellow, Courville & Bengio, 2016)

**Penulis:** Ian Goodfellow, Yoshua Bengio, Aaron Courville · **Penerbit:** The MIT Press, 2016
**Berkas vault:** `03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/AI-ML/[Adaptive Computation and Machine Learning series] Bengio... Deep learning...pdf` — 801 hlm PDF (cetakan metadata lengkap; kembar karya ING-0021 ditolak W1b)
**Disusun:** 09 Oktober 2026, dari teks ekstraksi lokal (pypdf). Folio tidak seragam antar bagian pemindaian — SEMUA rujukan = halaman PDF; halaman cetak disebut hanya bila tercetak pada baris hasil ekstraksi.
**Status daya-ikat:** `pending_verification` (P-5).

## 1. Peta bagian (bookmark PDF)

| Bagian/bab | Topik | PDF |
|---|---|---|
| 1 | Introduction; 1.2 Historical Trends in Deep Learning | `[R3, Goodfellow DL, PDF 24]`, `[R3, Goodfellow DL, PDF 35]` |
| I · 2 | Linear Algebra | `[R3, Goodfellow DL, PDF 52]` |
| I · 3 | Probability and Information Theory (KL & cross-entropy PDF 96) | `[R3, Goodfellow DL, PDF 96]` |
| I · 4 | Numerical Computation (overflow/underflow, softmax stabil PDF 101) | `[R3, Goodfellow DL, PDF 101..102]` |
| I · 5 | Machine Learning Basics (capacity & overfitting, hyperparameter & validation set) | `[R3, Goodfellow DL, PDF 118]`, `[R3, Goodfellow DL, PDF 140]` |
| II · 6 | Deep Feedforward Networks (back-prop, biaya negative log-likelihood) | `[R3, Goodfellow DL, PDF 196]` |
| II · 7 | Regularization (L1/L2, dropout §7.12 PDF 274) | `[R3, Goodfellow DL, PDF 257]`, `[R3, Goodfellow DL, PDF 274]` |
| II · 8 | Optimization (batch normalization §8.7.1 PDF 332) | `[R3, Goodfellow DL, PDF 284]`, `[R3, Goodfellow DL, PDF 332]` |
| II · 9 | Convolutional Networks (awal bab tercetak di PDF 344) | `[R3, Goodfellow DL, PDF 366..367]` |
| II · 10 | Sequence Modeling: Recurrent & Recursive Nets (awal bab PDF 386; vanishing gradient PDF 427) | `[R3, Goodfellow DL, PDF 394]` |
| III · 14–20 | Autoencoders s.d. Deep Generative Models; bab 17 Monte Carlo Methods (awal bab PDF 604) | `[R3, Goodfellow DL, PDF 609]` |

## 2. Butir bertambat (teks dibuka)

- Cross-entropy H(P,Q) = H(P) + D_KL(P‖Q); minimisasi = maksimisasi likelihood — `[R3, Goodfellow DL, PDF 96]`.
- Fungsi biaya jaringan = negative log-likelihood / cross-entropy training (pers. 6.12) — `[R3, Goodfellow DL, PDF 196]`.
- Dropout sebagai regularisasi kuat; heading §7.12 dengan rumus subgradient — , diskusi noise tuning – . `[tanpa-jangkar]`
- Batch normalization: tujuan utama memperbaiki optimisasi, efek regularisasi sekunder — `[R3, Goodfellow DL, PDF 334]`, `[R3, Goodfellow DL, PDF 334]`–`[R3, Goodfellow DL, PDF 334]`.
- Vanishing vs exploding gradient dan mitigasi (clipping, skip connections) — `inexact` `[R3, Goodfellow DL, PDF 305]`, `[R3, Goodfellow DL, PDF 341]`, `[R3, Goodfellow DL, PDF 427]`.
- Softmax perlu stabilisasi underflow/overflow — `[R3, Goodfellow DL, PDF 101]`.

## 3. Batas pemakaian

- R3 teks akademik: fondasi teori & terminologi; bukan penentu ambang. `pending_verification`.
- Kartu: `04_KNOWLEDGE-CARDS/AI-ML/REF-AIM-004*.md`.
