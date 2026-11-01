# Playbook pengawas-silang (supervisor cross-audit) — preseden misi manual AI/PROMANUAL 04–05-10

Untuk profil controller yang mengawasi papan misi sebagai VERIFIKATOR, bukan dispatcher/pemilik promosi.

## Batas peran
- `completed` / `ready for review` / `crashed` / `timed out` = KLAIM worker sampai artefak diukur di disk. Vonis hanya dari pengukuran giliran itu (aturan angka=cetakan-alat); koreksi angka sendiri dikirim sebagai komentar TERPISAH, bukan sunting komentar lama.
- Pengawas tidak membuat kartu, tidak reopen/promosi/unblock-manual, tidak rekayasa ulang papan. Notifikasi otomatis = inspeksi board + audit artefak saja; vonis tidak diturunkan untuk artefak yang kartunya tidak ada di papan.
- Redeliver notifikasi dari kartu yang sudah divonis = tanpa aksi (jangan posting vonis dua kali; cek `kanban show | grep -c "Vonis"` sebelum kirim ulang).

## Resep audit tulis-bab (berulang 20+ kartu, pola stabil)
1. Buka kartu penuh (`kanban show`) — snippet notifikasi terpotong; klaim pekerja yang "tidak cocok parser" sering komposisi yang belum terbaca (mis. 143 katalog + 17 tabel lain = 160 baris tabel mentah). Rekonsiliasi dari dua sisi sebelum menuduh.
2. Ukur: bytes persis klaim, baris, kata, glif U+2014/U+00B7, anatomi heading vs speks/blueprint, sub-bab vs daftar kanonis.
3. Uji rujukan ID lajur SATU-SATU vs berkas hulu (INDEKS-bukan-korpus). Grep label angka case-insensitive.
4. Baris angka tanpa-label-sebaris: uji TEKS-PENUH satu-satu (sering sah: penurunan dari tabel di atasnya, sel contoh, rujukan balik "idem", prosa metode). Vonis salah hanya setelah teks dibaca.
5. Cek konsistensi hilir: lampiran yang ditulis dari speks sebelum badan bab ada harus dicek ulang vs badan bab pasca-terbit (tugaskan eksplisit di vonis/kartu edit).

## Matcher ID lajur — SEBELUM memvonis "rusak", normalisasi varian
Konvensi hulu berbeda per lajur; parser wajib menormalkan dulu. Varian terdokumentasi: prefik-penuh `R7-F04`, polos-pad `F04`, polos-tanpa-pad, dua-tanda `F-07`, tiga-segmen `R13-F-07`, tanpa-F `R10-05`, dua-tanda-PAD `F-03`. Split crash-safe: `parts = id.split("-"); lane = parts[0]; fid = "-".join(parts[1:]).replace("-","")`. Hampir semua "ID rusak" sepanjang fleet = positif-palsu matcher, BUKAN cacat naskah — koreksi matcher dulu, baru vonis.

## Resep countersign audit vonis (verifier → pengawas)
- Jangan pakai ulang instrumen verifier; tulis parser sendiri. Contoh uji tandingan: recompute SEMUA pecahan `a/b=p persen` (regex `(\d+)/(\d{1,4})\s*=\s*([\d.,]+)\s*(persen|%)`), bandingkan round(a/b*100,1) ± toleransi.
- Hash agregat yang dikutip kartu tapi tidak ada berkasnya: coba pola hash atas SET berkas — concat sha256-per-berkas terurut nama (beberapa varian urutan/pemisah). Ini yang membuktikan klaim "27 raw tidak berubah".
- Verifikasi gap berlabel HIDUP di naskah terdampak (grep token di bab), dan kepala vonis lajur tidak mengklaim status penuh secara terselubung.
- Ciri audit jujur yang layak dihargai/dicatat: verifier melaporkan OBSERVASI non-blokir atas batas temuannya sendiri.

## Resep timeout-supervision (dipakai 6x; jangan aksi selain catat)
1. Ukur jejak parsial: byte-diff tiap artefak vs basis yang beku di vonis sebelumnya + mtime + keberadaan workdir/instrumen + registry sha-vs-disk.
2. Klasifikasi: BERSIH TOTAL (mati sebelum menulis apa pun → retry dari nol) / PARSIAL BERJEJAK (arsip+probe ada → lanjut, jangan buang inklusif) / PARSIAL TANPA JEJAK (suntingan diterapkan tanpa pemeriksaan alat → run-2 WAJIB audit-vs-basis dulu, dilarang apply buta).
3. Komentar catatan: fakta ukur + arahan retry + basis kekekalan terbekukan (angka ID/tag/glif vonis sebelumnya) supaya vonis nanti tidak bergantung ingatan.
4. Hipotesis struktural terukur (5 timeout kartu editor 3-bab): durasi pass > RUN_TIMEOUT_MS bridge 1800s — usulan perbaikan = kartu per-2-bab, bukan satu pass besar. Sampaikan sebagai hipotesis, bukan vonis.

## Gerbang figur
- Hash idempoten + registry cocok = bukti REPLIKASI, bukan kebenaran semantik. Sampling vision luas wajib; preseden fleet: cacat semantik hanya ketahuan via vision (leader-line salah target, kutipan bertentangan screenshot sendiri, placeholder bocor ke piksel).
- TAMBALAN wajib di-vision-QA ulang: bug lama bisa digantikan bug baru (fig-8.1: kabel fixed, placeholder "tahun + tercetak" bocor).
- Vision melaporkan typo/teks: GREP skrip sumber dulu — bisa artefak downscale model vision; jangan tetapkan cacat dari pembacaan gambar saja.
- Hitung global marker-vs-PNG DIULANG tiap gelombang: marker baru lahir setelah cakupan grup ditetapkan (kasus 16.1/17.1 tanpa penanggung jawab; 10.2/11.2/12.2 luput dari cakupan → kartu dendam). Kelalaian penugasan = deviasi diam-diam; bekukan sebagai item putusan controller.

## Resep pengiriman & penamaan
- Komentar `hermes kanban comment` panjang/ber-apostrof: TULIS ke berkas temp, kirim `"$(cat berkas)"`. Petik-satu bash pecah pada apostrof dalam teks (unexpected EOF). Output terminal yang ter-truncasi bisa tampak "OK" palsu → cek duplikat via `kanban show | grep -c` SEBELUM kirim ulang.
- Workdir instrumen punya ≥5 varian nama (`edit678`, `edit-910`, `edit-1213`, `t_<id-kartu>`): cari dengan glob/find multi-pola sebelum menyimpulkan "jejak tidak ada" — probe nama tunggal pernah nyaris menghasilkan vonis cacat yang salah.
- Hitung papan: `kanban list | awk` per-tenant dengan pengelompokan status; jangan filter workspace_path; waspada positif-palsu grep status (kata 'todo' muncul di teks judul).

## Format vonis SAH (yang diterima user sebagai bukti)
Angka-angka cetakan-alat giliran itu (bytes persis vs klaim, jumlah rujukan unik + hasil uji satu-satu, glif 0/0, rasio label X/Y), koreksi diri eksplisit bila probe awal salah, delta-terbuka yang dibekukan (marker menggantung, sha yang berubah + alasan), dan rujukan balik ke keputusan controller yang menunggu. Vonis ditulis ke komentar kartu + baris CONTRACT.md.
