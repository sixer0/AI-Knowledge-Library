# Rantai remediasi GEN-2: vonis FAIL campuran + cacat grafi verdict-gate (preseden misi panduan GEN-2, 26-09)

Lanjutan [`remediation-chain-after-verifier-fail.md`](remediation-chain-after-verifier-fail.md) (yang mengcover GEN-1: VS FAIL tunggal, relink build, FIX sempit). Kelas baru di sini: vonis FAIL yang MEMUAT cacat konten DAN cacat alat sekaligus, plus bug grafi yang lolos saat vonis kedua/ketiga.

## 1. Edge kartu verdict menggates DONE, bukan PASS (cacat grafi yang nyata terjadi)
Kartu build hilir (DX2B) dibuat dengan parent = kartu verifikasi (VS2). Dispatcher mempromosikan build begitu VS2 `done` — padahal vonisnya FAIL. Worker GEN-1 sudah terbukti jujur memblokir diri saat melihat vonis FAIL, tapi itu sandaran perilaku, bukan gerbang grafi.
Tambal controller (pola yang terbukti):
- `hermes kanban unlink <vs> <build>` lalu `link <vs-r-terakhir> <build>` — parent build HARUS kartu vonis FINAL, dan kontrak kartu build memuat klausul eksplisit "vonis FAIL = blokir diri + laporan nol-kerja".
- Setiap kali rantai remediasi menambah kartu VS-Rn, relink hilir ke kartu terbaru; jangan percaya edge lama.
- Verifikasi pasca-relink: `show <build>` → field `parents` harus berisi kartu vonis final saja.

## 2. Vonis FAIL campuran: pisah jalur kartu konten vs alat SEBELUM lepas fix
Verifier yang baik sudah mengadjudikasi sendiri di dalam laporannya (mis. CHECK 4: 8/9 non-200 = cacat probe alat, residu konten riil = KV tanpa-label). Controller WAJIB membaca adjudikasi itu dan memecah:
- Kartu FIX-konten (assignee penulis) — hanya butir riil bernama, sumber = berkas bab/lajur, dilarang sentuh instrumen.
- Kartu FIX-alat (assignee coder) — hanya instrumen verifier, salinan pra-tambal wajib (`.R2-orig`), tiap tambalan dengan KONTROL DUA ARAH (URL mati tanam-tangan tetap MERAH; segmen tanpa kausal tetap TIPIS), dilarang menurunkan ambang.
- Kartu vonis final (verifier independen) — PRASYARAT: validasi kontrol FIX-alat sendiri sebelum vonis artefak; bila tambalan terbukti melonggarkan, blokir (preseden D-12/D-16).
- Seed sampel G-DEEP/sampling WAJIB baru di vonis ulang (anti-overfit ke sampel yang diketahui penulis).
- Kontrol anti-pelonggaran di vonis ulang: mirror yang CABUT kembali sisipan fix harus menurunkan predikat (hijau tapi buta = FAIL prosedural).

## 3. Pitfall alat ukur konkret yang terdeteksi di rantai ini
- **Wayback nested-schema**: URL `web.archive.org/.../https://...` membuat probe requests `InvalidSchema` (skema di tengah token) dan terbaca "mati" padahal hidup 200. Normalisasi probe wajib strip skema dalam path wayback. Jangan vonis URL arsip mati tanpa probe manual jalur benar.
- **Baseline snapshot basi pada cek konten-kekal**: instrumen yang membandingkan bab-kini vs snapshot PRA-EDIT-AWAL membaca sisipan/penggantian yang DISAHKAN kartu fix sebagai delta ilegal. Setiap rantai fix→reassembly→reverify harus menaikkan baseline ke snapshot pra-fix-terakhir (`FIX2-BAB-BACKUP`), bukan era paling awal.
- **CRLF vs LF pada klaim ukuran/sha**: kartu ASM mengklaim byte mentah disk (CRLF) sementara sha12 dihitung atas konten ternormalisasi LF; selisih byte = jumlah baris CR. Rekonsiliasi definisi (hitung sha_raw DAN sha_norm) sebelum menuduh drift.
- **Regex penanda terlalu sempit di checker controller**: pola `\[[CR]-\d+\]` melewatkan bentuk lintas-lajur `[L6 C-06]` dan hampir memvonis bab kehilangan semua sitasi. Pola lebar: `\[[A-Za-z0-9 ]*[- ]?[CR]-\d+\]`. Helper ukur wajib skip berkas tanpa nomor (mis. STYLE-BIBLE.md) agar tidak crash.
- **Estimasi utilisasi gauge membaca artefak RAKITAN**: setelah suntingan sumber bab, gauge lama masih mencetak angka lama sampai reassembly dijalankan. Jangan baca "angka tidak berubah" sebagai fix gagal; jalankan reassembly dulu (atau catat sebagai estimasi worker).

## 4. Crash-loop worker: bedakan crash infrastruktur vs crash kerja-sebelum-mulai
STY-A crash x4 (worker exit(1) pasca-reasoning, 0 tool call) lalu TUNTAS di retry dispatcher lewat modal run sebelumnya. Kesalahan controller yang tercatat: mendiagnosis 402 fallback dari crash pertama lalu menggeneralisasi ke crash berikutnya tanpa membaca log run terakhir, dan mengklaim aksi pin-model yang tidak benar-benar dieksekusi. Aturan: sebelum ruling, baca `hermes kanban log <id>` run TERAKHIR (bukan run pertama); klaim controller hanya boleh menyebut aksi yang output tool-nya terlihat di giliran itu. Retry dispatcher + modal checkpoint sering cukup tanpa intervensi; intervensi hanya bila crash terjadi SETELAH tool call (modal rusak) atau retry habis tanpa jejak kemajuan.

## 5. lad_card.py (jejak pemakaian nyata)
`--est` = INTEGER menit (bukan teks narasi; pesan error `invalid int value`), `--shape` wajib (`satu|rantai-N|paralel-Kx`) kecuali `--interaktif`. Body panjang lewat `--body-file`. Output sukses: `Created t_xxxxxxxx (ready, assignee=...)`.
