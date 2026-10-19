# Kalibrasi LAD dengan laju nyata (basis bukti EXPO-INTEL 2026-09-02)

Referensi pendukung skill `gsp-limit-aware-delegation`. Ditambahkan lewat paket
P4 rencana percepatan worker (docs/2026-09-02-worker-speedup/plan.md, disetujui
user 02-09-2026). Angka di bawah diukur dari kanban DB misi EXPO26: 19 run kartu
pengumpul C01-C18, durasi run dari kolom `task_runs.started_at/ended_at`, jumlah
baris dari CSV `collection/expo2026/*/expo-raw.csv` dan hasil kartu, jumlah query
dari laporan metode worker di komentar kartu.

## Temuan utama: kendala pengikat adalah waktu, bukan iterasi

- Sembilan kartu done satu-run menyelesaikan 177 baris dalam 219 menit: agregat
  1,24 menit per baris; rentang antar kartu 1,03-2,09 menit per baris.
- Semua run mati di zona 22-31 menit terhadap anggaran bridge 30 menit, sementara
  anggaran iterasi tidak pernah habis (satu kartu melapor memakai sekitar 35 dari
  cap 150). Empat kartu menutup partial-handoff karena waktu, nol kartu karena
  iterasi. Satu kartu timeout penuh lalu baru selesai di run lanjutan 19,5 menit.
- Konsekuensi: estimasi E wajib dihitung dalam DUA satuan (iterasi dan menit),
  lalu bentuk delegasi dipilih dari yang lebih mengikat: E_eff = max(E_iter, E_menit).
  Kartu pengumpulan yang aman secara iterasi tetap bisa dirancang gagal kalau
  target barisnya menuntut waktu lebih dari sekitar 20 menit kerja efektif.

## Tabel kalibrasi laju (menggantikan asumsi lama)

| Besaran | Nilai terkalibrasi | Sumber bukti |
|---|---|---|
| Laju query sehat (ddgs backend bing hidup, domain target dapat dibuka) | 1 baris tervalidasi per 2-4 query | C07: 66 query ke 24 baris; C16: 66 ke 23 |
| Laju query degradasi (search bernois, antibot 403, domain mati) | 1 baris per 4-6 query | C10: 60 ke 11; C13: 40 ke 10; C11: 12 ke 2 |
| Waktu per baris (done, satu run) | 1,0-2,1 menit; rata-rata 1,24 | agregat 9 kartu, 219 menit, 177 baris |
| Kapasitas kartu pengumpul dalam satu run | 8-15 baris sehat; 4-8 baris degradasi | sisa 20 menit kerja efektif dibagi waktu per baris |
| Biaya satu putaran ulang penuh | 24-28 menit plus baca ulang instruksi | run C07 timeout 30,6 m lalu 19,5 m; C11 27,6 m lalu C11b 25,9 m |

## Aturan bentuk kartu pengumpulan (turunan tabel di atas)

1. Batasi lingkup kartu: 8-12 query inti plus 6-10 query pelebar, sesuai rencana
   P4. Target baris maksimum 15 per kartu; lebih dari itu pecah per region atau
   per klaster (R-3), bukan memperpanjang satu kartu.
2. Alokasikan anggaran waktu di muka: sisakan minimal 10 menit dari 30 menit
   bridge untuk penulisan artefak, cek deterministik, dan laporan penutupan.
   Kerja pencarian berhenti pada menit ke-20 bila target belum penuh.
3. Evaluasi ambang partial-handoff pada query ke-60 persen anggaran: pada titik
   itu laju nyata sudah terbaca (baris terkumpul dibagi query terpakai). Bila
   laju di bawah 1 baris per 4 query, nyatakan degradasi, kunci scope ke baris
   yang ada, dan tulis SISA_KERJA sedini mungkin; jangan kejar target dengan
   query tambahan yang sama-sama bernois.
4. Pilih bentuk dengan E_eff dua satuan (butir temuan utama di atas): R-1 hanya
   bila E_menit <= 20 DAN E_iter <= 0,5 x cap; R-2 untuk artefak koheren yang
   melebihi salah satunya; R-3 untuk item bebas (region atau klaster) dengan
   tiap kartu di bawah ambang tersebut.
5. Probe kesehatan search sebelum gelombang: satu query uji per backend. Hasil
   bernois total berarti seluruh gelombang dirancang pada laju degradasi (baris
   per kartu turun separuh, jumlah kartu naik), bukan worker dibiarkan mengejar
   target mustahil.

## Cara memakai tabel ini

- Saat menyusun estimasi E untuk kartu delegasi: ambil laju sesuai kondisi
  lingkungan (sehat atau degradasi), kalikan target baris, tambahkan 25 persen
  buffer, lalu bandingkan dengan 20 menit kerja efektif dan 0,5 x cap iterasi.
- Saat misi selesai: tambahkan baris bukti baru di bagian sumber di atas (tanggal
  misi + angka terukur) supaya tabel tetap hidup, sesuai norma LAD bahwa yang
  normatif adalah kewajiban memakai tabel plus jejak, bukan nilai spesifiknya.
- Batas klaim: angka berasal dari satu misi pengumpulan web (N=19 run, satu
  lingkungan, satu kelas tugas). Untuk kelas kerja lain (dokumen, kode, analisis)
  kalibrasi sendiri belum ada; jangan pakai angka ini sebagai dalih menolak
  estimasi manual.
