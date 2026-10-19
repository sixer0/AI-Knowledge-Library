# KEMAMPUAN - domain AI-ML

<!-- BUKUV3-ING-1009 W4 | digest mesin dari KEMAMPUAN-REGISTER.csv,
tanggal beku 2026-10-09 | 23 unit kemampuan |
daya-ikat: P-5: SELURUH baris lahir pending_verification;
sign-off engineer 0/332 -> draft-tidak-terverifikasi-insan.
Angka dalam paket TIDAK sah sebagai ambang terima sampai verifier W7 + tanda tangan manusia. -->

Titik masuk: router `gsp-ekas-knowledge-index` -> `cari_ekas.py --kemampuan "<kata kunci>"`.
Register per paket: `ekas/02_REGISTERS/KEMAMPUAN-REGISTER.csv` (kolom staging_path = path sumber di staging BUKUV3).

| unit | skill | nama | kind | rumus | uji | sumber (per references.yaml) |
|---|---|---|---|---|---|---|
| K-0298 | AIM-001 | Ml Requirement Analysis | document | 0 | 2 | Designing Machine Learning Systems - Chip Huyen [-] / EKAS skill SYS-014 REQUIREMENT_VALIDATION [-] |
| K-0299 | AIM-002 | Data Pipeline Design | document | 0 | 2 | Designing Machine Learning Systems - Chip Huyen [-] / EKAS skill AIM-016 CROSS_VALIDATION [-] |
| K-0300 | AIM-003 | Model Selection | calculator | 1 | 6 | Designing Machine Learning Systems - Chip Huyen (pemilihan model berbasis bukti) [-] |
| K-0301 | AIM-004 | Inference Sizing | stub-candidate | 0 |  | Designing Machine Learning Systems - Chip Huyen (2022) |
| K-0302 | AIM-005 | Latency Estimation | stub-candidate | 0 |  | Designing Machine Learning Systems - Chip Huyen (2022) |
| K-0303 | AIM-006 | Throughput Estimation | stub-candidate | 0 |  | Designing Machine Learning Systems - Chip Huyen (2022) |
| K-0304 | AIM-007 | Model Deployment | document | 0 | 2 | Designing Machine Learning Systems - Chip Huyen [-] / EKAS skill CCT-021 LATENCY_BUDGET [-] |
| K-0305 | AIM-008 | Model Monitoring | document | 0 | 2 | Designing Machine Learning Systems - Chip Huyen [-] / EKAS skill DAT-010 ERROR_BUDGET [-] |
| K-0306 | AIM-009 | Model Drift | calculator | 3 | 9 | Huyen - Designing Machine Learning Systems (2022, O'Reilly) [pdf hal. 264-267] |
| K-0307 | AIM-010 | Data Preprocessing | stub-candidate | 0 |  | Hands-On Machine Learning - Geron |
| K-0308 | AIM-011 | Feature Engineering | calculator | 1 | 6 | Designing Machine Learning Systems - Chip Huyen (rekayasa fitur) + praktik regularisasi [-] |
| K-0309 | AIM-012 | ROC-AUC (Two Independent Estimators) | calculator | 1 | 6 | Hands-On Machine Learning 2e - Aurelien Geron (2019, O'Reilly) [pdf hal. 135] |
| K-0310 | AIM-013 | Regression Metrics (RMSE, MAE, R2) | calculator | 1 | 6 | Hands-On Machine Learning 2e - Aurelien Geron (2019, O'Reilly) [pdf hal. 65] |
| K-0311 | AIM-014 | K-Means Step (Assign + Update, Monotone Audit) | calculator | 1 | 6 | Hands-On Machine Learning 2e - Aurelien Geron (2019, O'Reilly) [pdf hal. 303] |
| K-0312 | AIM-015 | Classification Metrics from Confusion Matrix | calculator | 1 | 6 | Hands-On Machine Learning 2e - Aurelien Geron (2019, O'Reilly) [pdf hal. 128-130] |
| K-0313 | AIM-016 | K-Fold Split Plan (Plain & Stratified) | calculator | 1 | 6 | Hands-On Machine Learning 2e - Aurelien Geron (2019, O'Reilly) [pdf hal. 105 & 126] |
| K-0314 | AIM-017 | Grid/Random Search Plan Generator | calculator | 1 | 6 | Hands-On Machine Learning 2e - Aurelien Geron (2019, O'Reilly) [pdf hal. 108-111] |
| K-0315 | AIM-018 | MLP Parameter & Memory Budget | calculator | 1 | 6 | Hands-On Machine Learning 2e - Aurelien Geron (2019, O'Reilly) [pdf hal. 360 & 405] |
| K-0316 | AIM-019 | MLP Loss & Output Activation Selection | calculator | 1 | 7 | Hands-On Machine Learning 2e - Aurelien Geron (2019, O'Reilly) [pdf hal. 366-368] |
| K-0317 | AIM-020 | Optimizer Selection (Geron Table 11-2) | calculator | 1 | 6 | Hands-On Machine Learning 2e - Aurelien Geron (2019, O'Reilly) [pdf hal. 446] |
| K-0318 | AIM-021 | Representation Learning | stub-candidate | 0 |  | Deep Learning - Goodfellow, Bengio & Courville |
| K-0319 | AIM-022 | Conv Layer Output & Parameter Budget | calculator | 1 | 7 | Hands-On Machine Learning 2e - Aurelien Geron (2019, O'Reilly) [pdf hal. 551 & 562] |
| K-0320 | AIM-023 | Ridge Regression (Closed Form + KKT Audit) | calculator | 2 | 6 | Hands-On Machine Learning 2e - Aurelien Geron (2019, O'Reilly) [pdf hal. 182] |

## Prasyarat / komposit

Kolom `composite_parent` pada register menyebut rantai demo `qa/chains.py` tempat paket dipakai.

## Batas

- Paket `kind=stub-candidate` INERT: tanpa calculator; sumbernya berstatus blocked_missing_source (belum di rak).
- Lapisan kurasi/model (CURATION/TRAINING) TIDAK diingest sebagai teks (P-6, LOKAL-SAJA).

## Rantai demo `qa/chains.py` yang menyentuh domain ini

Ekstrak deterministik dari `qa/chains.py` (staging BUKUV3) oleh `w4_chains.py`;
pemetaan mata mengikuti keputusan analis W4 (tabel CHAIN_MAP).

| rantai | langkah | unit K-xxxx domain ini | mata RANTAI-JAMINAN |
|---|---|---|---|
| ML_PIPELINE | 15 skill (AIM-003, AIM-011, AIM-012, AIM-013, AIM-014, AIM-015, AIM-016, AIM-017, AIM-018, AIM-019, AIM-020, AIM-022, AIM-023, DAT-011, DAT-012) | KM-0300, KM-0308, KM-0309, KM-0310, KM-0311, KM-0312, KM-0313, KM-0314, KM-0315, KM-0316, KM-0317, KM-0319, KM-0320 | 3-hitung - pipeline ML -> domain baru (belum berantai) |

## Jangkar angka & istilah terserap (tambalan W9B BUKUV3-JURY-1009, 09-10-2026)

Angka/istilah berikut diukur dari PDF vault (pdftotext, regex HIT — lihat kolom sumber) dan kini tercetak VERBATIM di lapisan agar terjangkau router `cari_ekas.py --kemampuan`. Daya-ikat tidak berubah: seluruh baris tetap `pending_verification` / `draft-tidak-terverifikasi-insan` (P-5); angka paket BELUM sah sebagai ambang terima.

| unit | angka/istilah tercetak | sumber + halaman vault | jejak ukur |
|---|---|---|---|
| K-0309 / AIM-012 | ROC AUC = 0.5 untuk klasifier murni acak; = 1 untuk klasifier sempurna (roc_auc_score) | Hands-On Machine Learning 2e - Geron (2019) [vault R3/AI-ML] pdf_p137 (cetak 98) | F2-AIM-01 |
| K-0317 / AIM-020 | Default Adam (kotak pseudocode Goodfellow): beta2 = 0.999, beta1 = 0.9, step size/lr = 0.001, eps = 1e-8 | Deep Learning - Goodfellow, Bengio & Courville (2016) [vault R3/AI-ML] pdf_p324 (cetak 301) | F2-AIM-02 |
| K-0306 / AIM-009 | 80% drift yang tertangkap layanan monitoring disebabkan kesalahan manusia (kutipan CTO, Undark 18-10-2021, Huyen pdf_p250/cetak 230). Covariate shift: P(X) berubah, P(Y given X) tetap; label shift: P(Y) berubah, P(X given Y) tetap (Huyen bab 8, pdf_p258/cetak 238) | Designing Machine Learning Systems - Huyen (2022) [vault R3/AI-ML] pdf_p250 (cetak 230) & pdf_p258 (cetak 238) | F2-AIM-03, F2-AIM-05 |
| K-0313 / AIM-016 | Contoh K-fold Geron: fungsi cross_val_score() menilai SGDClassifier dengan K-fold cross-validation tiga lipatan (k=3) | Hands-On Machine Learning 2e - Geron (2019) [vault R3/AI-ML] pdf_p127 (cetak 88) | F2-AIM-06 |
| K-0319 / AIM-022 | CNN (Goodfellow bab 9): averaging feature map -> satu nilai -> argumen softmax classifier di puncak jaringan | Deep Learning - Goodfellow, Bengio & Courville (2016) [vault R3/AI-ML] pdf_p358 (cetak 335) | F2-AIM-07 |

## Jangkar angka & istilah terserap (tambalan W10 BUKUV3-JURY-1009, 09-10-2026)

Baris berikut diambil VERBATIM dari halaman PDF vault yang terbukti (pdftotext Xpdf 4.06, metode tercatat di kolom sumber) agar aturan/rumus yang sebelumnya hanya disebut namanya kini terbaca isinya oleh router `cari_ekas.py --kemampuan`. Daya-ikat tidak berubah: tetap `pending_verification` / `draft-tidak-terverifikasi-insan` (P-5); angka paket BELUM sah sebagai ambang terima.

| unit | aturan/rumus tercetak | sumber + halaman vault | jejak ukur |
|---|---|---|---|
| K-0310 | Badan rumus RMSE (Equation 2-1, tercetak utuh): RMSE(X, h) = sqrt( (1/m) * SUM_{i=1..m} (h(x^(i)) - y^(i))^2 ). Teks pembuka: "A typical performance measure for regression problems is the Root Mean Square Error (RMSE). It gives an idea of how much error the system typically makes in its predictions, with a higher weight for large errors." Notasi: "m is the number of instances in the dataset you are measuring the RMSE on." | Hands-On Machine Learning 2e - Geron (2019, O'Reilly) [vault R3/AI-ML] pdf_p65 (cetak 26 = pdf - 39, offset konsisten dengan pdf_p127/cetak 88 & pdf_p137/cetak 98; awal bab 2 di pdf_p60 = cetak 21) | F2-AIM-04 |
