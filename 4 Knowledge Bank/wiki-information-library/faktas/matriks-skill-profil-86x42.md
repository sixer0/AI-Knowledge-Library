---
id: matriks-skill-profil-86x42
type: fakta
title: Matriks Pemetaan Skill × Profil GSP (86 Skill, 42 Profil)
sumber: docs/2026_08_24_kajian_ekosistem/matriks_pemetaan_skill.md
halaman: bab Skill → Profil; data matriks_pemetaan_skill.csv & .xlsx
tanggal_akses: 2026-08-25
kelas_bukti: sintesis
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: digital
writer: gsp-librarian
tags: [matriks, skill, profil, pemetaan]
links: [beban-profil-42-skill]
penulis: dashboard
diajukan: 2026-08-25
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-document-writer
direvisi-pada: 2026-09-03
status: active
verifikasi-oleh: gsp-custodian
verifikasi-putaran: 2
verifikasi-pada: 2026-09-03
catatan_verifikasi: "Verdict: terverifikasi (custodian PUTARAN 2, 2026-09-03, re-challenge penuh 7 dimensi atas suntingan gsp-document-writer). Alasan: re-challenge PUTARAN 2: suntingan putaran 1 terverifikasi. Sel Keterangan baris gsp-verification-before-completion dikoreksi menjadi 'ALWAYS 13 profil, OD 22 (hitung ulang CSV)' - hitung ulang independen matriks_pemetaan_skill.csv long-format: ALWAYS=13, ON DEMAND=22, total 35 cocok kolom Jml; dasar hitung adalah CSV bukan daftar kolom md yang terpotong di sumber, sesuai instruksi; 17 baris peringkat lain tidak disentuh. || Rekomendasi: objek siap lanjut ke lane librarian - sunting status 'terverifikasi' menjadi 'ditinjau' sebelum memanggil vault_promote.py (aturan I1); cek YAML kelas I5 dan klasifikasi dosir manual tetap prosedurnya. Tidak ada perubahan lain yang diperlukan penulis. Sensitif: tidak; dosir: tidak ada tema perkara hukum (kompensasi klasifikasi manual lane librarian, temuan I2). || Riwayat PUTARAN 1 (custodian 2026-09-03, perlu_revisi): Riwayat: Verdict awal (gsp-custodian, 2026-08-25): perlu_revisi. Revisi Wave B 2026-08-25 oleh gsp-librarian: fix-h1. Status kembali usulan untuk verifikasi ulang custodian.. Verdict: perlu_revisi || Alasan: Tabel peringkat cocok penghitungan ulang matriks_pemetaan_skill.csv (357 baris data, 86 skill unik) pada 17 dari 18 baris; KECUALI catatan 'gsp-verification-before-completion ... ALWAYS 17 profil, OD lain' yang KONTRADIKSI hitung ulang CSV: ALWAYS=13, ON DEMAND=22 (total 35 cocok). Klaim 42 profil = default+40 gsp-*+user01 dan 'csv 358 baris' cocok (header+357; default/user01 absen dari CSV konsisten dgn 0 skill). || Rekomendasi: Koreksi kolom Keterangan baris gsp-verification-before-completion menjadi 'ALWAYS 13 profil, OD 22' berdasarkan hitung ulang CSV (filter skill tsb: mode ALWAYS=13, ON DEMAND=22); JANGAN pakai daftar kolom ALWAYS di matriks_pemetaan_skill.md sebagai dasar hitung - daftarnya terpotong di sumber md (berhenti di 'gsp-grounding-specialis')."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/matriks-skill-profil-86x42.md
catatan_keputusan: "dipromosikan: subset lolos re-challenge RC-9 putaran 2 (9/9 terverifikasi); angka snapshot dibaca sebagai snapshot audit 24-08-2026 (objek terkait sudah membawa seksi Batas)"
---

# Matriks Pemetaan Skill × Profil GSP (86 Skill, 42 Profil)

Matriks pemetaan skill × profil GSP: **86 skill dipakai oleh 42 profil**,
mode ALWAYS/ON DEMAND (matriks_pemetaan_skill.md bab Skill → Profil; data
matriks_pemetaan_skill.csv / .xlsx sheet Skill_x_Profil).

**Peringkat pemakaian teratas:**
| Skill | Kategori | Jml profil | Keterangan |
|---|---|---|---|
| gsp-searxng | per-profil | 40 | ON DEMAND hampir semua profil |
| hermes-web-search-stack | gsp | 40 | ON DEMAND semua profil |
| gsp-verification-before-completion | per-profil | 35 | ALWAYS 13 profil, OD 22 (hitung ulang CSV) |
| gsp-document-quality-standards | per-profil | 16 | ALWAYS 7, OD 9 |
| gsp-dry-run-verify-fix | per-profil | 14 | semua OD |
| gsp-firecrawl | per-profil | 9 | semua OD |
| gsp-context-engineering | per-profil | 8 | semua OD |
| gsp-brainstorming / gsp-writing-plans | per-profil | 7 | writing ALWAYS di pm-planner |
| pustaka-teknis | gsp | 7 | ALWAYS engineering-analyst; OD 6 spesialis EKAS |
| docx/excel-master/diagnose/reflection-loop/vendor-crawler/powerpoint | - | 6 | - |
| pdf/xlsx | productivity | 5 | - |

**Profil:** 42 = default + 40 gsp-* + user01. default & user01 = 0 skill.

Sumber: `matriks_pemetaan_skill.md` bab Skill → Profil (tabel lengkap 86
skill); `matriks_pemetaan_skill.csv` (long-format, 358 baris).

# Bukti

- XLSX 4 sheet (Skill_x_Profil, Profil_x_Skill, Skill_Aset, Ringkasan)
  diverifikasi via openpyxl (contract doc).
- Data disusun dari parse SOUL.md semua 42 profil (blok ALWAYS LOAD /
  ON DEMAND).

# Catatan

- Beban per profil (Profil → Skill) di unit `beban-profil-42-skill`.
