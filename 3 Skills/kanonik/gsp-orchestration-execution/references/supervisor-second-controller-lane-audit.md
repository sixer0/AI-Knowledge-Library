# Audit Pengawas Lajur Riset pada Misi Dua-Controller (preseden misi vendor, 03-10)

When: misi dengan `Controller:` di kontrak menunjuk profil LAIN (pemilik DAG, mis.
gsp-master01) sementara kamu controller kedua/pengawas, dan kartu lajur berdatangan
`completed`. Kamu MENGAWASI gerbang, tidak meniru promosi/dispatch pemilik rantai.

## 1. Uji tandingan: vonis HANYA setelah alat ukur jalan (anti-halusinasi sendiri)
Urutan wajib: jalankan skrip ukur -> baca output -> baru tulis vonis/komentar/kontrak.
Preseden cacat (03-10, controller ini): baris addendum + komentar kartu ditulis SEBELUM
alat ukur selesai -> menyebut kode khayalan (tiga kode tak ada; riil: tujuh kode berbeda
pada daftar perangkat). Akar = urutan aksi, triase T5 (klaim sendiri).
Resep koreksi yang sudah terbukti: patch baris kontrak dengan tabel nyata + komentar
SUSULAN "KOREKSI komentar pengawas sebelumnya" di kartu (jangan sunting diam-diam) +
akar dicatat di jejak.
Prosedur ukur per lajur selesai (semua dari disk, bukan kutipan notifikasi):
- `findings-vendor.jsonl`: BACA keys baris pertama dulu - skema tiap pekerja beda
  (lowercase `code/entity_match/origin/round` di lajur CN VENDOR; kolom registry
  `KODE` bukan `KODE_KOMPONEN`; registry di `identification/` bukan root). Agregasi:
  jumlah baris vs klaim, kode unik per lajur vs EXPECTED dari COMPONENT-REGISTRY.tsv
  kolom LAJUR (temuan nyata: L01 klaim 18 kode tapi 6 kode NOL baris), distribusi
  entity_match (PASS/PROV/FAIL), origin CN, lantai >=5 CN-PASS per kode.
- Ledger HTTP: jumlahi 200 dari `raw/fetch-r*.jsonl` / `raw/*_probe.jsonl` sendiri -
  cocok-persis dengan klaim = bukti "cetakan alat"; L02: 32/44+21/39+15/24=68/107.
- Tangga: `awk -F'\t' '{split($2,a,"-"); print a[1]}' ladder.log | sort | uniq -c` untuk
  hitung kelas K1..K8 dari log MENTAH (marker prose di ladder.md bisa menipu: L04 tanpa
  penanda "Kelas 3/8" di md tapi log memuat K3=3/K8=4).
- Uji dua putaran nyata: hitung baris `round=2`; klaim entitas baru harus bernama.
- Baris FAIL/PROV = tanda jujur, BUKAN pemblokir; yang dilarang cuma menaikkan PROV/FAIL
  sebagai pemenuh register terbit (SPK-002 #4).

## 2. Pola DONE-prematur (cacat gerbang paling sering pada fase lajur)
Sinyal: kartu `done` TAPI verdict.md lajur sendiri berbunyi "BELUM JENUH" / "TIDAK JENUH"
/ "CAPPED-parsial" / "partial-handoff LIMIT-AWARE". Vonis pengawas: DONE prematur vs
gerbang saturasi (S-3). Tindakan (tanpa reopen - satu pedal satu kaki):
(a) komentar pengawas di kartu: angka ukur + konsekuensi "MRG menahan promosi lajur ini
sampai resume-run ATAU putusan CAPPED tertulis pemilik rantai";
(b) baris addendum kontrak; (c) butir keputusan masuk daftar PUTUSAN MENUNGGU pemilik.
Vonis JENUH yang LOLOS uji tandingan (L04 pola terbaik) dinyatakan eksplisit juga di
kontrak supaya MRG bisa langsung pakai - seimbang, bukan hanya menegur.
Agregat penutup fase = tabel per lajur: | lajur | baris | PASS/PROV/FAIL | vonis | syarat
MRG | + daftar permohonan putusan bernomor. Ini bekal kartu merge; TEMPELKAN sebagai
komentar langsung di kartu merge saat ia diangkat dan masih running (jangan menunggu
ditanya) - aturan kolom STATUS-VONIS, PROV bukan pemenuh, register bernama untuk FAIL.

## 3. Triase timeout lajur (pra-retry)
Sebelum menyimpulkan apa pun: cek mtime artefak vs sekarang. ladder.log mtime < 2 menit
= retry dispatcher SUDAH hidup menulis - tidak perlu aksi (preseden STY-A: retry lanjut
dari modal = penyelamat). Modal mentah kaya (cache N berkas + ladder.log) tapi
findings/verdict BELUM lahir -> opsi untuk pemilik: resume-run builder-only (rakit akhir
dari cache). Kalau retry kedua mati tanpa findings -> kartu butuh run-lanjut eksplisit.

## 4. Notifikasi beruntun = gema, cek dulu papan
Banyak notifikasi `completed` tiba berurutan; sebagian sudah kuaudit di giliran sebelumnya
(L06/L09) atau done TANPA notifikasi sama sekali (L08, L07-run2 menyusul). Sebelum aksi:
`hermes kanban list | grep <MISI>` + bandingkan set yang sudah diaudit. CATATAN CLI:
`hermes kanban list` TIDAK menerima `--board default` (error unrecognized); grep output
saja. JSON list tidak selalu bisa di-parse - fallback teks + regex status.
