---
id: wlp-fakta-pendaratan-statik
type: fakta
title: "Pendaratan statik WebUI tanpa restart: server membaca ulang statik per permintaan (misi WLP, F20-F22)"
status: active
sumber: docs/2026-09-05-webui-long-transcript-perf/checkpoints/CP-F20-fixdev19.md
halaman: §4; CP-F21 §3; CP-F22 §3
tanggal_akses: 2026-09-07
kelas_bukti: primer
sensitif: tidak
perkara: wlp
tags: [webui, cache, etag, deploy-statis, brahma, wlp]
links: [wlp-resep-ukur-performa, wlp-pelajaran-objek-vs-content]
penulis: gsp-librarian
diajukan: 2026-09-07
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-07
catatan_verifikasi: "Verdict: terverifikasi. Alasan spesifik: mekanisme _serve_static (api/routes.py:17985+, stat per permintaan, cache valid selama (st_size, st_mtime_ns), ETag lemah W/size_hex-mtime_ns_hex) diverifikasi ganda di CP-F20 par.4 dan CP-F21 par.3 termasuk uji If-None-Match 304 hidup. Bukti rantai md5 47d9b7940d7171bbb8a76b56f94074b5 (pra-tambal, CP-F19 par.5 dan CP-F21 par.1) ke 4d396b432363217b3ee2396b61433cad (pasca-cherry-pick fe71a74, CP-F22 par.3 dan CP-F23 par.1) terverifikasi silang empat checkpoint; pid 27488, server_started_at 1788732169.625 identik saat buka dan tutup, uptime 19.909 s tercetak CP-F23 par.5. Isolasi root serve (get_static_root = REPO_ROOT/static; marker worktree tidak terserve) cocok CP-F20 par.4. Lapis browser (?v=__WEBUI_VERSION__ dihitung sekali saat boot per api/updates.py:612; URL polos max-age=300 vs bertoken immutable max-age=31536000) cocok CP-F20 par.4 dan CP-F21 V15. Rekomendasi konkret: tidak ada perubahan isi; saat promosi pertahankan label batas-waktu butir 4.1 (berlaku selama kebijakan cache server tidak berubah; modul python terimpor tetap butuh restart)."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-07
dipromosikan-ke: faktas/wlp-fakta-pendaratan-statik.md
---

# Pendaratan statik WebUI tanpa restart: server membaca ulang statik per permintaan (misi WLP, F20-F22)

1. Mekanisme terverifikasi

1.1 `_serve_static` (api/routes.py:17985+) me-restat berkas setiap permintaan; cache internal valid hanya selama `(st_size, st_mtime_ns)` cocok - bila beda, `read_bytes()` ulang dari disk. ETag lemah `W/"size_hex-mtime_ns_hex"` merefleksikan stat terkini. Konsekuensi: cherry-pick commit yang mengubah berkas statik ke branch serve BERLAKU tanpa restart server [R-1][R-2].

1.2 Bukti hidup: pid 27488 hidup terus tanpa restart lintas misi (server_started_at 1788732169.625 identik saat buka dan tutup F23; uptime 19.909 s tercatat), sementara md5 body terserve /static/outline.js berubah dari 47d9b7940d7171bbb8a76b56f94074b5 (pra-tambalan, terukur F19/F21) ke 4d396b432363217b3ee2396b61433cad (pasca-cherry-pick fe71a74, terukur F22/F23) murni karena isi disk berubah [R-2][R-3][R-4][R-5].

1.3 Isolasi root: server melayani dari `REPO_ROOT/static` checkout utama (api/config.py::get_static_root); marker byte yang ditulis ke salinan worktree TIDAK terlihat di body terserve - bukti serve-read berasal dari checkout serve, bukan worktree lain [R-1][R-6].

2. Lapis browser (batas pendaratan tanpa restart)

2.1 `index.html` menyemat `?v=__WEBUI_VERSION__` dan WEBUI_VERSION dihitung SEKALI saat proses boot (api/updates.py:612) dengan `Cache-Control: public, max-age=31536000, immutable` pada URL ber-fingerprint. Tab LAMA yang sudah menyimpan salinan immutable tetap memakai cache sampai token `?v` berganti (restart jendela user) atau hard-refresh. Konteks baru (playwright/cache kosong) selalu mendapat badan disk terbaru segera setelah commit tersimpan [R-1][R-6].

2.2 Implikasi operasional: untuk verifikasi otomatis, gerbang buka "md5 body GET == md5 disk" sudah cukup pasca-pendaratan commit; jangan menyimpulkan "tambalan tidak bekerja" dari tab lama yang masih immutable-cache.

3. Register rujukan

- R-1: docs/2026-09-05-webui-long-transcript-perf/checkpoints/CP-F20-fixdev19.md §4 (mekanisme _serve_static, ETag==stat disk, mtime 10:02:03 vs proses sejak <=09:13, kesimpulan tanpa restart; lapis browser immutable).
- R-2: checkpoints/CP-F21-reverify.md §3 (verifikasi ulang mekanisme dari sumber + If-None-Match 304; Cache-Control URL polos max-age=300 vs bertoken immutable).
- R-3: checkpoints/CP-F22-cherrypick.md §3 (md5 disk==terserve==4d396b43 tanpa restart; ETag 0x9be2==ukuran disk; server_started_at tetap).
- R-4: checkpoints/CP-F19-walk.md §1 (md5 outline 47d9b7940d71 keadaan pra-tambalan).
- R-5: checkpoints/CP-F23-rewalk.md §1 dan §5 (md5 4d396b43 + pid/uptime 27488 nol restart).
- R-6: CP-F20-fixdev19.md §4 percobaan marker worktree (isolasi get_static_root).

4. Batas berlaku

4.1 Mekanisme berlaku untuk berkas yang DISAJIKAN lewat `_serve_static` pada server WebUI Brahma :9012 konfigurasi kini (cache stat-keyed). Tidak berlaku untuk: modul python yang sudah terimpor proses (tetap butuh restart), dan tab browser lama yang memegang URL `?v` immutable sampai token berganti. Ukuran bukti ETag/uptime tercatat 2026-09-07; perubahan kebijakan cache server wajib uji ulang sebelum resep deploy-tanpa-restart ini dipakai.
