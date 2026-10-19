---
id: 16-kddi-corporation
type: fakta
title: "KDDI Corporation — adopsi agen AI (Top40 #16, L3)"
status: active
sumber: https://tech-note.kddi.com/n/nd8e1c9e507d8
halaman: "-"
tanggal_akses: 2026-09-01
kelas_bukti: sekunder
sensitif: tidak
perkara: top40-agent-ai
tags: [agen-ai, top40-agent-ai]
penulis: gsp-librarian
diajukan: 2026-09-01
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-01
catatan_verifikasi: "Verdict: terverifikasi || Alasan: anti-karangan mandiri custodian (parser blok ENTRI mentah wave_*.md, read-only; bukan entries.json turunan): sumber==bukti_url OK (https://tech-note.kddi.com/n/nd8e1c9e507d8); tanggal_akses==akses OK (2026-09-01); kutipan verbatim ada di body OK; nama cocok tabel final Top40 #16 (KDDI Corporation); frontmatter komplit (status tunggal, kelas_bukti=sekunder, tanggal ISO, sensitif); dedup wiki nol kolisi (685 berkas dipindai); label [klaim vendor] tidak diwajibkan baris ini; kutipan=本技術をauチャットサポート窓口のお客様応対支援に導入しました\\\" (bahasa Jepang di halaman; arti: teknologi ini telah diterapkan pada dukungan pelanggan jendela chat support au) || Rekomendasi: promote tetap kewenangan gsp-librarian."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-01
dipromosikan-ke: faktas/16-kddi-corporation.md
catatan_keputusan: "dipromosikan: AI40-S18b: terverifikasi custodian 7 dimensi 2026-09-01"
---

# KDDI Corporation — adopsi agen AI (Top40 #16, L3)

Rekaman terstruktur satu entri daftar final **Top 40 korporasi pengguna agen AI** (kontrak
`docs/2026-09-01-top40-agent-ai`, seluruh sumber diakses 2026-09-01). Peringkat 16 dari 40,
skor 74/100 (metode RT §4.2), kematangan L3.

- Negara / sektor: Jepang / telekomunikasi
- Use case agen AI: Agen AI internal "PersuaBot" hasil riset KDDI General Research Laboratory (kolaborasi Stanford, paper EMNLP 2024): otomasi respons call-center — analisis fungsi strategis, pencarian informasi aktif + RAG, generasi jawaban tervalidasi anti-halusinasi; SUDAH dipasang pada dukungan chat au untuk pelanggan; sedang digeneralisasi untuk banyak use case internal
- Kedalaman otonomi: tinggi — agen mencari informasi secara aktif, memverifikasi fakta, menghasilkan respons dalam tugas kompleks non-qa sederhana; deploy produksi di kanal support au
- Skala: tidak dipublikasikan (volume percakapan au tidak disebut)
- Dampak: validasi akademik: menekan halusinasi sambil mempertahankan capaian tugas di hampir semua kondisi eksperimen [blog teknik resmi KDDI, 2026-09-01]

## Bukti (disalin dari blok ENTRI `wave_05_telecom_media` baris 120)

- bukti_url: https://tech-note.kddi.com/n/nd8e1c9e507d8 (akses 2026-09-01)
- Kutipan verbatim: "本技術をauチャットサポート窓口のお客様応対支援に導入しました" (bahasa Jepang di halaman; arti: teknologi ini telah diterapkan pada dukungan pelanggan jendela chat support au)
- Catatan sumber blok: blog teknik KORPORASI resmi (penulis insinyur KDDI); jendela waktu: artikel 2025-11-26; kutipan verbatim berbahasa Jepang sesuai halaman
## Keterbatasan entri (kolom keterbatasan tabel peringkat, verbatim)

blog teknik KORPORASI resmi (penulis insinyur KDDI); jendela waktu: artikel 2025-11-26; kutipan verbatim berbahasa Jepang sesuai halaman

Kelas bukti objek = sekunder (rekaman terstruktur dari halaman sumber; kelas halaman dasar
tercatat pada Catatan sumber di atas). Sumber kanonik daftar: `compilation/top40_ranking.md`;
laporan naratif: `output_final/top40_corporate_agent_ai_report.md`.
