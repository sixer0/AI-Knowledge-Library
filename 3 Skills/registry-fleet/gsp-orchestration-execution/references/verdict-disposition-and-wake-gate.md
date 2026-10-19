# Disposisi vonis verifier + wake-notifikasi + gerbang jalur-hidup (preseden WKO-0911, 11-09)

## 1. Wake-notifikasi kanban = input status, BUKAN perintah dekomposisi
- Setiap notifikasi `[kanban] Task ... completed` yang masuk: `show`/`list --json` papan dulu; jangan pernah membuat kartu/grafik duplikat atas notifikasi status.
- Ukur ulang klaim secara independen sebelum dilaporkan ke user: recompute sha256[:10] salinan vs kanonik, grep marker fitur di salinan, `ls -la` bukti di disk + baca ekornya. Result worker = petunjuk; angka controller = cetakan alat pada giliran sendiri (aturan anti-halusinasi).
- Jawaban chat controller selalu lewat scanner naturalisasi kanal chat dengan jejak VERDICT tercatat.

## 2. SOP disposisi VERDICT FAIL dari verifier independen
Saat kartu VERIF menutup FAIL/needs-review:
1. Baca laporan utuh per-CHECK (result notifikasi sering terpotong).
2. Pisahkan temuan ke tiga kelas:
   (a) cacat riil ber-akar terbukti -> kartu FIX scoped (parents = kartu verifier, wake-sub OK, uji merah-hijau + kontrol regresi ditulis eksplisit di body, rute pakai saran KARTU_LANJUTAN verifier);
   (b) keputusan tertunda milik user (mis. restart layanan produksi) -> sampaikan via chat + jejak KEPUTUSAN DIBUTUHKAN, jangan dieksekusi sendiri;
   (c) basi-salah-instruksi (kontrak kartu menyebut angka artefak lama, mis. "9 check" padahal artefak kini 11) -> catatan, bukan cacat artefak.
3. TAHAN kartu hilir (laporan akhir/NAT) dengan `hermes kanban comment <id> "Tahan dulu (D-nnn): ..."` + Decision Log kontrak, supaya laporan final tidak pernah memuat vonis menggantung. Lepas tahan hanya oleh komentar controller.
4. Penulis-bukan-verifikator berlaku juga untuk controller: probe controller ke verifier kartu HANYA jadi input/kondisi uji; vonis tetap milik verifier.

## 3. Gerbang jalur-hidup vs disk (live-path gate)
- Patch di disk TIDAK SAMA dengan aktif di proses berjalan. Sebelum klaim "fitur X aktif", bandingkan: CreationDate proses (baris "Starting Hermes Gateway" di gateway.log / CIM) vs mtime berkas patch vs isi git HEAD vs working tree.
- Lapor jujur dua lapis: "artefak patch LULUS (secope, git diff terukur); jalur hidup menunggu RESTART = wewenang user". Restart layanan produksi tidak pernah dilakukan controller/worker.
- Kondisi wajib untuk verifier: buktikan proses yang diuji memuat kode baru (pid/CreationDate vs mtime); catat sebagai komentar kontak controller ke kartu VERIF.
- Jebakan positif/negatif-palsu: skrip deterministik dijalankan dengan interpreter tanpa dependensi (python sistem tanpa PyYAML) memberi FAIL palsu ("YAML rusak"); vonis hanya sah pada interpreter yang benar (venv engine). Kontrol pembeda keadaan (mis. satu locale TERJEMAH vs sisanya FALLBACK-EN) wajib ada di probe.

## 4. Cacat D-WKO-1 (silent wake loss) — workaround sampai FIX/2 rilis
- `lad_card.py --wake-default` dipanggil dari sesi profil NON-default: langganan ter-stempel `notifier_profile=<profil pemanggil>` (`_profile_author()` di hermes_cli/kanban.py), padahal kanal target dibaca dari config ROOT default; poller gateway hanya mengklaim langganan profil yang adapternya di-host -> wake hilang SENYAP: nol pengiriman, nol error, nol log.
- Aturan aman: registrasi wake (`--wake-default` / `--subscribe-existing`) HANYA dari sesi controller profil default; setelah registrasi, verifikasi baris langganan membawa `notifier_profile=default` (atau set HERMES_PROFILE_NAME=default).
- Kontrol merah-hijau E2E: tutup kartu uji (tenant khusus WKTST) dan cari jejak `woke agent for <kartu>` di gateway.log <=2 menit; nol baris = silent loss, bukan "belum tiba".
- Kartu uji wake wajib diarsipkan pasca-uji (langganan mati bersama arsip) agar tidak membangunkan papan selamanya.
