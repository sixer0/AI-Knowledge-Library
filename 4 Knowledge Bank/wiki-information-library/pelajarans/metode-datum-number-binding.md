---
id: metode-datum-number-binding
type: pelajaran
title: "Metode DATUM number binding: angka terikat register, aritmetika derivasi dicek, audit dokumen otomatis (datumbind.py)"
status: active
domain: digital
writer: gsp-librarian
created: 2026-08-25
sumber: legacy-archive/RISET SISTEM OPERASI AI GSP DAN KAM-20260824T085358Z-1-001/RISET SISTEM OPERASI AI GSP DAN KAM/GSP Kajian Riset AI Agentik [Pak Eka]/06 Berkas Proses 007/datumbind.py
halaman: datumbind.py (Register/Derivation/audit_docx); Cara Menjalankan.md 007 §2, 010
tanggal_akses: 2026-08-10
kelas_bukti: primer
sensitif: tidak
perkara: riset-sistem-ai-gsp-kam
tags: [sistem-ai, datum, number-binding, register, audit, reproduksibilitas]
penulis: gsp-librarian
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi (custodian 2026-09-03, challenge penuh 7 dimensi, batch M1b). Alasan: semua klaim terverifikasi terhadap sumber yang ditunjuk - docstring datumbind.py memuat persis motivasi terukur (delapan dokumen, lima gambar, sebelas skrip hitung, 120 literal numerik di enam generator, satu koreksi memicu tiga penerbitan ulang dan dua cacat lolos: nilai superseded + persen terpotong bukan terbulat) dan empat komponen Register/Derivation/audit_docx/audit_retired dengan semantik yang sama; render.py (Kajian 15082026) memuat dialek {{nama besaran}} dengan format |n |rp |pct |d2 dan kalimat \"Rujukan ke besaran yang tidak ada di register adalah galat, bukan peringatan\"; Cara Menjalankan.md 007 bagian 2 memuat urutan wajib dan gerbang pembekuan model (satu uji gagal = berhenti); Riwayat Revisi.md memuat hasil verifikasi 010: register 227 besaran, 35 uji konsistensi lulus, jalan ulang bita identik, lint DATUM 27 dari 27 bersih, halaman terekonsiliasi 122. YAML kelas-I5 lulus, title==H1, satu baris status, sensitif tidak. Dedup: wiki/vault c04-berkas-proses-jalan-ulang membahas reproduksibilitas berkas proses (faset berbeda) - komplementer. || Rekomendasi: tidak ada perubahan wajib. Renik sitasi: angka verifikasi 010 berada di bagian \"010-GSP-KT-VIII-2026 Rev A\" Riwayat Revisi.md - ganti penanda \"§5\" dengan nama bagian tersebut agar telusur presisi; tanggal_akses 2026-08-10 mendahului tanggal ajukan, sah sebagai tanggal akses berkas namun boleh diselaraskan. Riwayat: catatan_verifikasi lama (verdict awal perlu_revisi 2026-08-25, direvisi gsp-librarian Wave B 2026-08-25, status dikembalikan ke usulan) dipertahankan sebagai riwayat."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: pelajarans/metode-datum-number-binding.md
catatan_keputusan: "dipromosikan: batch M1b paruh B terverifikasi custodian (C-M1b-verdict.md)"
---

# Metode DATUM number binding: angka terikat register, aritmetika derivasi dicek, audit dokumen otomatis (datumbind.py)

Metode yang memaksa "angka tidak pernah diketik literal": setiap angka pemikul dalam dokumen adalah rujukan bernama ke register; derivasi aritmetikanya DIPERIKSA (bukan ditampilkan); dokumen jadi diaudit otomatis.

Bukti (angka berujukan):
- Motivasi terukur: pada satu engagement nyata — delapan dokumen, lima gambar, sebelas skrip hitung — ditemukan 120 literal numerik di enam generator; satu koreksi model memaksa tiga penerbitan ulang dan tetap membiarkan dua cacat lolos (nilai superseded + persen terpotong bukan terbulat) (datumbind.py, docstring).
- Mekanisme: `Register` (besaran bernama diformat konvensi angka rumah), `Derivation` (blok derivasi yang aritmetikanya DICENTANG — raises bila tidak cocok), `audit_docx` (setiap angka di berkas jadi ditelusuri balik ke register), `audit_retired` (menolak berkas yang masih membawa nilai model yang ditarik) (datumbind.py).
- Dialek naskah render.py: angka ditulis `{{nama besaran}}` (dengan format |n, |rp, |pct, |d2); rujukan ke besaran yang tidak ada di register = GALAT yang menghentikan pembangunan, bukan peringatan (Kajian 15082026 - AGENTIC AI/06 Berkas Proses/render.py).
- Praktek 007/010: register dipancarkan lebih dulu, prosa ditulis di atas register beku; gerbang pembekuan model — kalau satu uji gagal, berhenti (Cara Menjalankan.md §2).
- Hasil verifikasi 010: register 227 besaran, 35 uji lulus, jalan ulang bita identik, lint DATUM 27/27 bersih, halaman terekonsiliasi 122 (Riwayat Revisi.md §5).

Asumsi/tanda: primer (kode sumber + dokumen prosedur).
