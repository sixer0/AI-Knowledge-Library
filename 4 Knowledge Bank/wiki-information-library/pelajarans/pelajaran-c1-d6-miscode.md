---
id: pelajaran-c1-d6-miscode
type: pelajaran
title: "Pelajaran: verifikasi ganda menemukan 2 inkonsistensi metadata minor (C1 D6 miscode; hitungan D6)"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/2026-07-17_gsp_orchestration_skill_report/01_verification.md
halaman: 01_verification.md I-01/I-02 (hal. 166–167); §Consistency (hal. 144–148)
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: gsp-orchestration-skill-report
tags: [gsp, verification, lesson, metadata]
penulis: gsp-librarian
diajukan: 2026-08-25
catatan_verifikasi: "Verdict (gsp-custodian, challenge penuh B0, 2026-09-03): terverifikasi. || Alasan spesifik: semua klaim body cocok persis dengan sumber RAW yang dibuka - I-01 (C1 gsp-agent-catalog salah kode D6 padahal punya tags+related_skills) dan I-02 (hitungan D6 tertulis 35, benar 34) ada verbatim di 01_verification.md baris 166-167 dengan severity Low dan pernyataan 'do not affect the report's overall correctness'; angka 35 yang dikritik dikonfirmasi independen di 99_implementation_report.md baris 390 (baris D6 'All 35 skills | 35'); pelajaran 'uji terhadap skill_view bukan pola kategoris' cocok kolom Evidence I-01. Dedup: entri wiki faktas/gsp-orchestration-verifikasi-laporan.md dan pelajarans/pelajaran-metodologi-ukur-skill.md menyebut I-01/I-02 sebagai fakta/jejak, tetapi sudut objek ini (pelajaran proses verifikasi) tidak duplikat - komplementer. Metadata lolos yaml.safe_load, nilai utuh, title==H1, satu baris status; sensitif tidak, non-dosir; grouping perkara sesuai isi. Renik non-blocking: rujukan sekunder 'Consistency hal 144-148' menunjuk blok readiness totals; baris ringkasan 'PASS (2 minor notes)' sebenarnya di baris 179 seksi Summary. || Rekomendasi konkret: saat promote tambahkan links ke gsp-orchestration-verifikasi-laporan dan pelajaran-metodologi-ukur-skill agar silang-rujuk terjaga; perbaiki rujukan Consistency ke baris 179 bila direvisi; tambahkan field domain."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: pelajarans/pelajaran-c1-d6-miscode.md
catatan_keputusan: "dipromosikan: B0 smoke IL-INGEST-01: terverifikasi custodian 2026-09-03 (challenge penuh 7 dimensi)"
---

# Pelajaran: verifikasi ganda menemukan 2 inkonsistensi metadata minor (C1 D6 miscode; hitungan D6)

Verifikasi independen terhadap laporan menemukan 2 inkonsistensi metadata minor: **(I-01)** `gsp-agent-catalog` (C1) diberi kode defisiensi D6 padahal memiliki tags dan related_skills; **(I-02)** jumlah skill terdampak D6 ditulis '35' padahal benar 34. Keduanya Low severity, tidak mempengaruhi akurasi metrik. Pelajaran: klaim metadata harus diuji terhadap sumber aktual (skill_view), bukan diturunkan dari pola kategoris. [R — 01_verification.md, hal. 166–167]
