# Resep gelombang fokus vendor (enumeration-complete vendor sweeps)

Kelas tugas: "daftarkan SEMUA vendor bernilai untuk N lini produk lintas kelompok geografi, dengan sitasi terverifikasi, vonis jenuh per lajur, dan deliverable Excel". Preseden ukur: DEMS-VSAT-1003 (03-10-2026; 38 kartu done nol menggantung; MASTER-REGISTER 1.098 baris x 4 fokus; VS-R3 PASS 9/9 SALAH-TARGET=0; rilis xlsx sha16 02c7f755e8b4c1df lolos gerbang tampil).

## 1. Bentuk blueprint
- SATU skema register kanonis (22-27 kolom) didefinisikan di kartu TA, identik untuk semua lajur:
  `row_id|focus|product_group|item_code|item_en|vendor_name|vendor_name_local|brand|country_hq|origin_country|role|product_ref|spec_match|trust_tier|official_url|citation_urls|evidence_channel|price_seen|price_note|date_accessed|http_status|notes`
- Lajur = subset lini produk x satu fokus. Artefak wajib per lajur: `register.tsv + ladder.md + vonis.md (S1-S4 ber-angka) + negatives.md + raw/`.
- Urutan gelombang = prioritas user (mis. CN/TW duluan sesuai perintah eksplisit). Edge antar-gelombang = dependensi DATA NYATA (merge gelombang sebelumnya memberi seed dedup + rekonsiliasi lintas fokus), bukan edge semu urutan.
- Rantai merge: MRG-F1 -> melepas lajur F2 -> MRG-F2 (+daftar GANDA-LINTAS-FOKUS) -> F3 -> MRG-F3 -> F4 -> MRG-ALL menghasilkan MASTER-REGISTER + PIVOT (matriks item x fokus; SEL KOSONG WAJIB menunjuk entri negatives, nol diam-diam) + X-ADJ-REGISTER + UNTRUSTED-REGISTER + LAPORAN-CAKUPAN.
- Angka laporan hilir dihitung parser atas berkas, bukan dikutip dari ringkasan pekerja.

## 2. Trust tiering (pola aturan user)
- TRUSTED: situs resmi HTTP200 tercatat + entity-match + identitas hukum terverifikasi.
- PROVISIONAL: sebagian kriteria terpenuhi; drill kedalaman sedang.
- UNTRUSTED: kredensial tidak jelas - TETAP dicatat dengan cap + alasan, drill dangkal (identitas saja). Tidak pernah dibuang diam-diam; pegang register terpisah.
- Harga: hanya angka ber-channel R0 (situs resmi) yang sah; angka lain wajib cap KLAIM-VENDOR/PROV. Verifier mendemosi baris gagal (mis. 302 persisten -> PROVISIONAL), bukan memperdebatkannya.

## 3. Kategori X-ADJ (produk adjakan)
Baris di luar daftar item yang diminta tapi bernilai bagi tujuan misi (ditemukan saat sapuan), tiap baris bawa alasan satu kalimat. Jangan dicampur ke hitungan item inti; sheet/register sendiri.

## 4. Tangga verifikasi yang terbukti menangkap cacat
- VS: instrumen deterministik satu skrip, dua run identik-byte, seed baru tercatat; fetch ULANG SELURUH populasi official_url oleh verifier (BUKAN cache lajur) + sampel liveness sitasi ~25% ber-seed.
- RANCANG UNTUK MULTI-RONDE: VS FAIL (cacat bernama) -> kartu FIX -> VS-R2 -> FIX2 -> VS-R3 adalah jalur normal, bukan anomali. Tiap ronde seed baru + grep silang tabrakan seed sebelum pakai, append SEED-LOG.txt.
- CSX countersign: jalankan ulang instrumen + spot-check independen seed BERBEDA, verdict AGREE/DISAGREE per CHECK.
- Builder XLS patuhi token STD-SAJI-001; lalu gerbang tampil (DGB): roundtrip openpyxl vs EXPECT, defect tampil-tautan = 0 (target == URL tercetak + warna/gaya), PIVOT direkalkulasi sel-per-sel, scan glif U+2014/U+00B7 = 0.

## 5. Watchdog + daur hidup
- Cron per 30 menit menjalankan skrip stateful: state JSON {sig hitungan status papan, last_change_ts}; sinyal: STALLED (nol running + todo tertunda + idle > 90 menit), PERHATIAN-KARTU-BLOCKED, TERMINAL_ALL_DONE (semua done -> controller wajib verifikasi akhir + serah).
- Setelah serah: controller menghapus cron job (cronjob list dulu - id bisa sudah hilang sendiri bila prompt watchdog berisi self-remove).

## 6. Format laporan posisi ("Posisi?") yang terbukti diterima user
1) Snapshot papan terukur (counts + idle menit + jam ukur); 2) papan skor per gelombang dengan jumlah baris TERUKUR dari disk (wc -l merge + mtime), bukan kartu saja; 3) counter trust tier via awk atas register gabungan; 4) sisa kerja berurutan dengan estimasi per segmen; 5) ETA dihitung dari KADENSIS TERUKUR gelombang sebelumnya (wall-clock riil), bukan harapan; 6) level klaim jujur (L1 worker-complete vs L2 verified).

## 7. Pitfall terpasang (durable)
- `lad_card.py` TIDAK mengenal `--priority`; error argparse membocorkan teks usage ke output sementara kartu lain tetap sukses - parse HANYA baris `Created`, anggap id hilang = kartu itu gagal, jangan lanjut mengira sukses.
- Instalasi 25+ kartu lewat loop subprocess melewati plafon foreground 600 dtk: jalankan `background=true + notify_on_complete`.
- Re-run setelah kegagalan parsial WAJIB idempoten: query `kanban list --json` dan reuse kartu ber-judul identik sebelum create (mencegah gelombang ganda; selaras pitfall sesi-kembar 03-09).
- `hermes kanban complete` bisa diblokir klaim-hidup basi milik run controller sendiri: `complete --force` dengan hasil bukti terukur adalah jalur sah bila kerja memang selesai dan terverifikasi.
- Terminal hardline: perintah compound dengan `$(grep -n ... | cut)` di dalam rentang `sed -n` diblokir sebagai payload tak terparse - pakai read_file offset/limit, bukan shell akrobatik.
- Dokumen sumber dengan cacat render (mis. literal `format()` Python muncul sebagai nilai): hitung ulang agregat dari baris, laporkan delta terhadap klaim agregat dokumen itu, jangan percaya salah satunya.
