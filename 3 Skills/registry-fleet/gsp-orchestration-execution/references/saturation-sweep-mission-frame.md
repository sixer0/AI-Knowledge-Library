# Pola misi SAPUAN BERGATE JENUH (saturation-gate sweep, multi-lajur)

Terverifikasi 2026-09-12 pada misi sapuan global (docs/2026-09-12-<misi>/): sapuan global satu kelas solusi untuk satu sektor, 8 lajur x 2 putaran, 213 entitas terukur, gerbang jenuh berjalan dengan aritmetika reproducible. Dipakai untuk permintaan kelas "cari seluruh dunia sampai tidak ada data baru".

## Kerangka inti (WAJIB sebelum kartu lajur pertama)
1. **Registri entitas kanonis = pembilang tunggal.** Vonis "tidak ada data baru" tanpa registri = klaim tak terverifikasi. Skema kolom dibekukan SEBELUM baris pertama masuk (kolom pembeda peran — mis. KANAL-JUAL antarjenis pembeli, MAKNA ganda istilah — wajib ada sejak skema v1; retrofit setelah ratusan baris jauh lebih mahal).
2. **Dua dimensi terpisah:** lajur = jalur pengumpulan (C1..C8), sumbu penjodohan = lapisan kemampuan (R1..R7). Satu lajur mengisi beberapa lapis; blueprint wajib menjaga keduanya agar satu lapis tidak tampak terisi oleh satu jenis sumber saja.
3. **Delta-only + single-writer merge:** kartu lajur HANYA menulis `registri/delta/<LAJUR>-r<k>.csv`; kartu merge khusus satu-satunya penulis master (anti tabrakan tulis N lajur paralel — RSK nyata). Merge wajib: dedup kunci (nama-normalisasi ATAU root domain), entity-match pintu masuk 100% dengan FETCH SENDIRI (jangan percaya delta), register reject dengan alasan.
4. **Gerbang jenuh eksak, tercetak script:** `pct(L,r) = 100*U/max(N0,1)` per LAJUR per putaran (bukan gabungan — lajur kecil jenuh palsu, lajur besar tak pernah jenuh); JENUH bila pct<5 DUA putaran berturut; lajur kecil boleh ambang absolut (U<=2) beralasan tercatat. Seed builder dan seed verifier WAJIB beda dan tercetak di log. Vonis final milik kartu gerbang (M3), bukan pekerja lajur.
5. **Putaran = satu lintasan penuh seluruh kelas jalur** atas lajur itu. Putaran-2 berasal dari ANGKA merge (daftar lajur belum jenuh), bukan spekulasi; rencana r2 per lajur disalin ke badan kartu (mis. "jalur gagal teknis r1 diulang lewat kelas jalur lain; jalur yang dibatasi robots atau syarat layanan berhenti dengan status butuh otorisasi").

## Misi paralel salin-silang (dua misi satu ranah)
- SATU registri logis; fisik dimiliki SATU misi (single owner); misi lain tidak pernah menulis silang. Seed masuk dari artefak misi hulu (entri warisan membawa ID asal, ID hulu tidak pernah dibuat ulang oleh misi baru). Arus balik lewat dokumen laporan ke controller -> dicatat di kontrak misi hulu. Nomor register deliverable dipartisi di Decision Log sebelum kartu pertama (tabrak nomor = rekonsiliasi paksa).

## Pengendalian mutu controller atas artefak pekerja (berulang, jadi prosedur)
- **Sebelum merge diklaim**, controller ukur delta sendiri (csv.DictReader): jumlah baris, distribusi enum per kolom kunci. Temuan nyata: kolom enum (mis. jejak-INDONESIA ADA/TIDAK/BELUM-DICARI) diisi narasi panjang oleh 3 lajur berbeda — penyakit berulang. Jalur benar: komentar `CATATAN CONTROLLER` di kartu MERGE sebelum ia jalan (normalisasi enum saat merge, pindahkan narasi ke catatan-risiko), BUKAN menolak kartu lajur.
- **Penaikan jenjang bukti** entri existing = baris khusus `catatan-risiko='PENAIKAN-BUKTI <id>'` di delta, merge mem-merge kolom bukti, bukan menambah baris ganda.
- **Reject ber-evidence penuh** (SPK-002 kosong>salah): situs mati semua jalur + arsip 503/404/DNS dengan akun JSON ber-timestamp = reject sah dengan lead pengulangan r3 (preseden: Serrasoft, Thales stub WAF — halaman 200 tanpa konten, host-token pada stub kosong BUKAN bukti entitas).
- Angka laporan worker selalu diukur ulang controller dari disk sebelum naik ke kontrak/PHASE-REPORTS (norma "angka = cetakan alat giliran ini").

## Gerbang persetujuan user (pra-eksekusi)
Permintaan sapuan besar: susun rencana (lajur + definisi jenuh + bentuk serah), minta persetujuan via clarify SEBELUM kartu pertama, catat verbatim keputusan di 00_raw-request.md + Decision Log (D-02). Bentuk serah dan hubungan antar-misi termasuk dalam pertanyaan batch yang sama.

## Mekanika dispatch yang terbukti
- `lad_card.py`: tenant harus cocok `^[A-Z][A-Z0-9]{1,15}-\d{4}$` (satu segmen huruf-angka plus empat digit sah, dua segmen WARN). Pasang `--parents` sejak create; DILARANG placeholder ID kartu lain — kejadian nyata: M2 dibuat dengan parent keliru (kartu misi lain) karena ID belum diketahui; unlink+link menyelamatkan sebelum promosi, tapi aturan turun-temurun: buat kartu hilir SETELAH ID parent nyata tersedia, atau verifikasi `show --json` dulu.
- DAG pra-built penuh sah (norma gelombang N1): kartu hilir dibuat `todo` dengan parents nyata; kernel mempromosikan otomatis saat parent done — controller tidak dispatch manual.
- Pengawas titik keputusan: terminal background loop `for i in seq...; do hermes kanban show <id> --json | python -c "...status..."; sleep 60; done` + notify_on_complete=true; satu loop per titik (RT->TA, GB1->W1, merge->wave berikutnya), jangan polling manual.
- Kap dispatcher: yang mengikat = kartu AKTIF per misi (<=5) dan host global (20); batch create >5 sah.

## Jawaban 'cek progres' kelas ini (format user 12-09)
Empat blok tetap: (1) posisi pada rantai fase; (2) hasil TERVERIFIKASI angka cetakan alat (ukur ulang dulu, jangan kutip memori); (3) yang belum per fase; (4) ETA tabel per etap + cabang yang bisa menggeser (mis. putaran-3 lajur jauh) dengan rentang jujur.
