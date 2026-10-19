---
id: ft-l3-pitfall-bnb-sm120-windows
type: pelajaran
title: "Pitfall bitsandbytes: tanpa kernel sm_120 untuk wheel Windows (RTX 5070 Ti) - QLoRA 4-bit native Windows gagal"
status: active
sumber: docs/2026-09-20-ft-eval-0920/lajur/L3-local-ft.md
halaman: seksi 1 butir 4 (issue GitHub 1937)
tanggal_akses: 2026-09-20
kelas_bukti: primer
sensitif: tidak
perkara: ft-eval-0920
tags: [bitsandbytes, sm_120, blackwell, windows, qlora, pitfall, ft-eval-0920]
links: [ft-l3-kelayakan-qlora-5070ti]
penulis: gsp-librarian
diajukan: 2026-09-20
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-20
catatan_verifikasi: "Verdict: terverifikasi || Alasan: Bukti primer issue bitsandbytes #1937 cocok L3 seksi 1 butir 4 (status closed, label Waiting for Info/Windows, RTX 5070 Ti Laptop, driver 595.79, Python 3.14, torch 2.11.0+cu130, galat no kernel image is available for execution on the device). Path mentah yang dikutip objek, docs/2026-09-20-ft-eval-0920/raw/bnb1937.html, terverifikasi ADA di disk. Riwayat pytorch #159207/#164342, forum Juli 2025, ptxas sm_120, dan mitigasi triton >= 3.3.1 cocok sumber. Empat pelajaran adalah generalitas dari bukti tersebut dan tidak menambah angka baru tanpa sumber. Kelas_bukti primer jujur. REKOMENDASI: saat promosi beri batas waktu 'status issue per 2026-09-20' dan uji ulang issue sebelum dipakai memblokir jalur native Windows, karena kernel sm_120 Windows dapat terbit kemudian."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-20
dipromosikan-ke: pelajarans/ft-l3-pitfall-bnb-sm120-windows.md
catatan_keputusan: "dipromosikan: FT-EVAL-0920 S13: lolos kurasi librarian + verifikasi custodian 2026-09-20"
---

# Pitfall bitsandbytes: tanpa kernel sm_120 untuk wheel Windows (RTX 5070 Ti) - QLoRA 4-bit native Windows gagal

Bukti primer: https://github.com/bitsandbytes-foundation/bitsandbytes/issues/1937 (status closed, label Waiting for Info/Windows; diakses 2026-09-20, mentah di docs/2026-09-20-ft-eval-0920/raw/bnb1937.html). Lingkungan pelapor identik dengan mesin GSP: RTX 5070 Ti Laptop, driver 595.79, Python 3.14, torch 2.11.0+cu130. Galat: "no kernel image is available for execution on the device".

Pelajaran yang berlaku:
1. QLoRA 4-bit berbasis bitsandbytes di NATIVE Windows pada GPU Blackwell konsumen (sm_120) berisiko gagal total meski torch-nya sendiri mendukung sm_120 - komponen kuantisasi adalah titik patah, bukan kerangka latihnya.
2. Jalur aman terbukti: WSL2 Ubuntu-24.04 atau Docker image resmi Unsloth (keduanya tersedia di mesin GSP). Alternatif native Windows: model dengan format kuantisasi native (gpt-oss MXFP4) yang tidak melewati bitsandbytes.
3. Riwayat sekelas untuk antisipasi dini (bukan status kini): pytorch/pytorch #159207 dan #164342 menuntut dukungan sm_120 di build stabil (2025); forum Juli 2025 masih melaporkan "sm_120 is not compatible" pada torch 2.7.1 build tertentu; Triton lama gagal "ptxas fatal: Value 'sm_120' is not defined" - mitigasi: triton >= 3.3.1 (syarat Unsloth Blackwell).
4. Pola generik untuk fleet: saat mengadopsi GPU arsitektur baru, uji komponen KEDUA (quantizer, attention kernel, optimizer custom) terpisah dari torch - dukungan torch tidak mengimplikasikan dukungan ekosistem.

Akses semua URL 2026-09-20; sha16 berkas sumber: 072e5480a79c1b55.
