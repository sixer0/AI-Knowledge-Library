# Misi BACA-PENUH Korpus + Resume Pengetahuan (preseden DEMS-BACA-1003, 03-10)

Kelas tugas: "baca SEMUA berkas folder X baris per baris tanpa yang terlewat, lalu
susun resume pengetahuan sebagai dasar sesi". Target = korpus dokumen proyek (md/json/
csv/py/biner campuran, ratusan berkas). Ini beda dari saturasi-web (references/
saturation-gate-sweep-lanes.md): populasi tertutup di disk, vonis kelengkapan = manifest,
bukan jenuh 8-kelas-jalur.

## Bentuk orkestrasi yang terbukti

1. Controller WAJIB baca sendiri berkas indeks/keadaan-terakhir (Baca Dulu, Catatan Sesi,
   REGISTER, laporan pemahaman terakhir) sebelum delegasi — tanpa itu kartu lajur salah lingkup.
2. Pecah per subtree alamiah (bukan per jumlah berkas), satu kartu per lajur, semua
   assignee reader (mis. gsp-document-reader). Dispatcher lokal boleh mengklaim >5 serentak
   (Spawned: 7 sah; kap 5 = norma gelombang promosi, bukan pembuatan — Norma N1).
3. Badan kartu memuat KONTRAK DIGEST identik (blok COMMON): per berkas = path, baris/ukuran
   nyata, struktur seksi, SEMUA angka kunci verbatim (Rupiah/unit/tanggal/sha/pasal),
   keputusan, anomali, status keterbacaan; WAJIB MANIFEST akhir (lingkup vs terbaca,
   selisih harus NOL); biner tanpa sidecar = catat nama+ukuran+tanggal+sha + tandai
   BINER-MURNI-TIDAK-DIBACA; JSON/CSV besar = parser semantik (schema, cacah record,
   field kunci, agregat) dihitung sebagai baca-penuh; anggaran habis = partial-handoff
   dengan SISA_KERJA path persis.
4. Output per lajur ke path unik `docs/<misi>/work/wN_*.md`; watcher tunggu pakai
   terminal(background=true, notify_on_complete=true) — nohup ditolak shell wrapper.

## Gerbang controller sebelum klaim L2 (jangan percaya summary pekerja)

- **Audit ledger sidik mandiri**: hitung ulang MD5 seluruh berkas vs ledger proyek.
  PITFALL nyata: ledger bisa menyimpan nama dengan SPASI sementara disk memakai GARIS
  BAWAH (efek sanitasi migrasi ALUR) — pencocokan naif memberi vonis palsu "242 HILANG";
  normalisasi `_`↔spasi + casefold menurunkan hasil benar (278 SAMA, 0 BEDA, 4 sanitasi).
  Simpan alatnya: audit_sidik2.py pola (walk disk → dict key ternormalisasi → bandingkan).
- **Replikasi aritmetika sampel**: pilih 2-3 angka turunan yang dilaporkan pekerja dan
  hitung ulang dari JSON/sumber mentah (preseden: residu T6b Rp 8 direplikasi persis;
  grep C2PA SVG 11/11 direplikasi). Cocok = kepercayaan lajur naik; beda = flag.
- **Matriks uji-silang angka kunci**: grep 15-20 angka/beban bukti lintas semua digest —
  angka yang sama harus muncul konsisten di lajur independen; konflik = kartu rekonsiliasi.
- **Ukur ulang hash artefak rilis** keadaan terakhir (objek di luar folder beku) sebelum
  dikutip di resume.
- **Metrik dump pekerja tidak selalu direplikasi**: jumlah baris/karakter ekstraksi PDF
  bergantung alat (pypdf vs pdfminer memberi 4.632 vs 7.591 baris untuk PDF yang sama;
  cacah penanda 'DISEPAKATI' 144 vs 162 dengan tanggal campuran). Bila angka laporan tak
  direplikasi alatmu: JANGAN wariskan sebagai angka sah — buka sebagai flag keterbatasan
  digest di kontrak + komentar kartu, substansi baca tetap berlaku.

## Penutupan kartu (pitfall nyata 03-10)

- Pekerja menutup kartunya sendiri dengan result; `hermes kanban complete <id> --force`
  pada kartu yang SUDAH done keluar dengan **exit 1 senyap, tanpa pesan**. Jalur benar:
  cek status dulu (`list --json`), lalu tempel bukti penutupan via `comment` (berhasil
  pada kartu done). Jangan loop retry complete.
- Rangkai perintah kanban satu-per-satu bila argumen panjang; rantai `&&`+heredoc+for
  dalam satu giliran bisa gagal senyap di tengah.

## Gerbang naturalisasi resume (kanal doc)

Draf berlabel-tebal padat (gaya catatan internal) FAIL deterministik: C-7 paragraf <3
kalimat (ambang <=1/dokumen) dan C-8 tebal >6 per 1.000 kata memicu agregasi D-TA-09.
Resep PASS tanpa mengubah konten: badan dokumen jadi prosa naratif paragraf-panjang,
tabel tetap (tabel tidak dihitung sebagai tebal), penanda list-inline `—` → koma/titik;
middle dot di JUDUL pun terhitung A2 (ganti spasi/tanda hubung). Jalankan scanner, baca
CHECK yang FAIL per nama, revisi terarah, scan ulang — dua putaran biasanya cukup.

## Peta jejak wajib

contract.md (tabel kartu + audit integritas + Decision Log), PHASE-REPORTS.md blok [FASE],
digest per lajur di work/, resume final di root misi, mirror ke repo engine/workspace +
entri CHANGELOG + commit terarah (jangan `git add -A` — working tree berisi perubahan
agen lain; diff CHANGELOG dicek bersih sebelum commit).
