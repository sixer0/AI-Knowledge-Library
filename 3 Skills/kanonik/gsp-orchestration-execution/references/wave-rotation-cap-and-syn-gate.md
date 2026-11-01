# Rotasi cap gelombang + gerbang SYN agregat (preseden HDKCOMP-0929, 29-09)

Kelas: misi verifikasi ber-gelombang (V01..Vnn) hasil merge register, dengan cap
konkurensi blueprint (puncak running <=5 PER MISI + maks N paralel PER TIPE PROFIL
bila blueprint menyebutnya). Pola ini dijalankan penuh untuk 12 gelombang x 4
perusahaan dan menutup 25/25 kartu tanpa satu pun kartu tersangkut.

## Instantiate dari WAVE-MAP (bukan dari narasi)
1. Parse `verification/WAVE-MAP.md` dengan regex baris tabel -> peta
   `Vnn -> profil`. Assignee kartu HARUS sama persis dengan WAVE-MAP (penetapan
   anti-silang lane D-TA-04 sudah terjadi di M1B; controller tidak mengocok ulang).
2. Buat batch lewat `lad_card.py` (parent = kartu M1B), body menempel: bahan
   `batch-nn.csv`, SCHEMA kolom target (mis. 29 kolom SCHEMA-B), kewajiban blok
   VERIFIKASI-AKURASI per field + LADDER per rung, uji eksplisit register FLAG M1,
   aturan lajur yang berlaku + CER-001 untuk entitas CN, LIMIT-AWARE (anggaran iterasi+menit,
   AMBANG-B -> checkpoint + SISA_KERJA bernama), WAKE-ORKESTRATOR.
3. Semua kartu lahir `ready` dan dispatcher langsung klaim sampai kap — itu normal
   (norma gelombang N1: pembuatan batch sah, yang digerbangi adalah AKTIF).

## Rotasi cap (inti pola)
- Setelah instantiate, controller `hermes kanban block` kartu di atas cap dengan
  pesan berisi ALASAN + KRITERIA BUKA ("saat ada V terminal"). Notifikasi block
  atas kartu-kartu ini = gema putusan sendiri; jawab "tidak ada aksi sah", jangan
  unblock refleks.
- Tiap notifikasi V-done: ukur papan (`list --json`, Counter status + hitung
  running PER TIPE assignee), baru unblock SATU penerus yang tipenya punya slot
  kosong. Jangan unblock berdasar nomor urut gelombang saja.
- **Kasus khusus slot-jenis-habis:** bila antrean tersisa semuanya bertipe X dan
  slot X penuh (preseden: sisa V11 crawler sementara 2 slot crawler terisi, slot
  collector kosong), TAHAN kartunya walau puncak global masih longgar — tipe yang
  mengikat. Jelaskan ini di laporan agar tidak dibaca lupa rotasi.
- Timeout gelombang dengan CSV yatim di disk (`hasil-Vnn.csv` ada, jejak VERIFIKASI
  belum): triase modal dulu, dispatcher retry biasanya menuntaskan (V03, V07 nyata
  pulih via run-2 yang mengaudit modal run-1). Pecah kartu HANYA setelah retry
  kedua tanpa artefak.

## Gerbang SYN (sebelum kartu penulis laporan dilepas)
Semua angka dihitung controller sendiri dengan parser seragam, bukan dikutip dari
kartu:
1. **Agregat V:** glob `hasil-V*.csv` -> total baris + nama unik; harus == populasi
   register M1 (preseden 48 == 48). Simpan cetakan.
2. **Linkcheck deterministik per-URL:** lihat pitfall sel multi-URL di
   `gsp-verification-before-completion` (v1 per-sel menghasilkan 10 'mati' palsu;
   v2 pisah ';' + vonis mati hanya bila SEMUA URL sel gagal -> 47/48 hidup).
   Cetakan JSON per-URL disimpan sebagai artefak gerbang (`LINKCHECK.json`).
   Residu 403-vs-UA-datacenter (pro.sony) TIDAK memblokir SYN bila substansinya
   sudah terverifikasi jalur lain — syaratnya laporan wajib mendisklosi catatan
   metode, bukan diam.
3. Kartu SYN ke penulis: body menempel seluruh putusan controller (Q3/Q4/Q5/Q7/Q11),
   daftar bahan + path, kewajiban angka Section A dari skrip parser sendiri
   (`build_report.py` + `section_a_numbers.txt` reproducible), gate scanner
   naturalisasi `--channel document` dengan VERDICT terlampir.
4. **Uji tandingan pasca-SYN (controller, independen):** parser ulang hasil-V* vs
   angka Section A laporan; cocokkan selisih populasi ke disklosi eksplisit
   (preseden: 48 kanonik - 1 barred HiteVision R-REG-1 = 47 Section B, keputusan
   verifier V09 yang didisklosikan di §Method + seksi residu = contoh benar
   'kosong lebih baik daripada salah'; selisih kecil kelas Adjacent 6-vs-5
   teridentifikasi berasal dari entri barred yang sama). Vonis tuntas hanya setelah
   uji ini + scanner PASS + papan seluruhnya done.

## Nama berkas jejak antar-gelombang BERVARIASI — normator harus toleran
Gelombang menulis jejak VERIFIKASI sebagai `hasil-Vnn.md`, `hasil-Vnn-VERIFIKASI.md`,
ATAU `VERIFIKASI-Vnn.md`, dan satu gelombang (V04) tanpa md sama sekali (bukti di
CSV + komentar kartu). Gerbang agregasi mencocokkan pola `*Vnn*`, bukan satu nama
kanonik; variasi dibukukan sebagai catatan, bukan divonis cacat pekerja.

## Pitfall parser controller saat uji tandingan
- Kolom ID register di CSV hasil bisa berisi nilai merge ('MERGED') alih-alih
  `M-nn`; jangan pakai kolom itu untuk menghitung blok Section E — pakai regex
  heading `^### M-\d+` pada laporan dan bandingkan COUNT, bukan himpunan ID CSV.
- Hitung kelas `comparison_class` dari CSV bisa berbeda ±1 dari narasi laporan
  karena entri barred dihitung dari sisi berbeda; telusuri sampai entitas bernama
  sebelum memvonis salah satu pihak.
