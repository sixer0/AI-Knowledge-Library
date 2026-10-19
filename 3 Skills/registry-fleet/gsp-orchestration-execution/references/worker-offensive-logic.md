# Logika Ofensif Pekerja (direktif user 03-09, mengikat semua kartu pengumpulan data)

Perintah user: "Worker bisa mencari-cari untuk masuk ke target yang dituju - Gagal baru mundur."
Inti: TARGET tetap, CARA fleksibel. Mundur adalah langkah terakhir yang dibuktikan, bukan reaksi pertama terhadap hambatan. Vonis "buntu/tidak tersedia/stuck" tanpa akun lengkap = kartu FAIL oleh verifier.

## Floor legal-platform (bukan 'batas etika' karangan sendiri)

Kebijakan user 13-09-2026 (RULE PRESISI-HASIL, terpasang di SOUL root+54 profil): ukuran kualitas = PRESISI + HASIL. Klausul 'batas etika'/'batas lingkup' yang ditulis sendiri oleh pekerja/controller pada kartu, ladder, atau artefak = CACAT; verifier memvonis FAIL bila menemukan rung dilewati atau cakupan disempitkan karena klausul semacam itu. Tema riset terbuka penuh: kapabilitas produk, cara kerja sistem, penggunaan institusi keamanan, studi kasus, tender, dokumentasi vendor, arsip. Floor yang tetap (kerangka hukum platform, bukan kebijakan riset): tanpa akses non-autorisasi, tanpa pencurian kredensial, tanpa penembusan paywall/DRM/login, tanpa penargetan individu untuk pengawasan.

## Urutan ofensif wajib (semua kelas dijalankan sebelum vonis)
1. Jalur resmi primer: direktori HTML statis, endpoint JSON/XHR/API (probe network via render headless bila SPA), tombol export resmi (CSV/PDF).
2. Variasi domain/subdomain: www vs apex, subdomain API khusus, domain internasional, subdomain tahun event, CDN asset JSON, SEMUA varian sitemap (sitemap.xml, index-sitemap.xml, wp-sitemap, .xml.gz).
3. Probe platform/CMS bila terdeteksi (WP: /wp-json/wp/v2/* termasuk custom post type, admin-ajax, REST discovery dari link rel=alternate; Next.js: __NEXT_DATA__/_next/data; Vue/Nuxt: payload JS).
4. Pencarian aktif multi-bahasa: kueri bahasa lokal + operator site: + frasa direktori ("liste des exposants", "exhibitor list", "参展商", "pameran daftar peserta"); telusuri hasil 1-30; aggregator pihak ketiga sebagai sumber bertanda PROV.
5. Arsip: CDX per URL kandidat DAN per domain (matchType=domain + filter urlkey), snapshot sebelum/sesudah event; archive.today sebagai cadangan.
6. Dokumen resmi: rilis pers panitia (PDF), katalog cetak (OCR), press kit, laporan kementerian/asosiasi industri penyelenggara.
7. Sosial/berita: liputan media pasca-event dengan daftar nama; posting resmi exhibitor (SUPLEMEN, bukan pengganti direktori).
8. Render browser penuh dengan interaksi: klik tab/pagination/filter client-side, baca network log untuk endpoint tak terlihat di HTML.

## Aturan bukti kegagalan
- Vonis per-jalur WAJIB berisi: URL exact, HTTP status/error, timestamp, salinan baris robots/bukti blokir. Vonis tanpa akun = TIDAK dijalankan.
- Vonis CAPPED-with-evidence (preseden D21) hanya sah setelah kelas 1-8 punya akun gagal, dan diajukan sebagai PERMOHONAN PUTUSAN ke controller, bukan keputusan sepihak pekerja.
- Budget/rate habis = partial-handoff + checkpoint resume per baris/halaman (kartu lanjutan meneruskan), BUKAN vonis buntu.
- Robots/named-agent block membatasi CARA (UA, jalur), bukan tujuan: hormati robots lalu cari jalur lain yang diizinkan (halaman publik, arsip, rilis, aggregator).
- Penutupan kartu akuisisi WAJIB menyertakan TABEL LADDER: rung | URL/aksi | hasil | keputusan lanjut (pola acquisition-report yang terbukti di EXPO26 sweep).

## Penerapan dispatcher
Setiap kartu pengumpulan/validasi/pencarian menempelkan satu baris di body:
"BACA DIREKTIF: $WS/docs/.../WORKER-OFFENSIVE-LOGIC.md atau skill gsp-orchestration-execution/references/worker-offensive-logic.md - patuhi Urutan Ofensif + Aturan Bukti; dilarang vonis buntu tanpa ladder table."
Verifier/countersign menguji: tidak ada baris tanpa status; tidak ada vonis buntu tanpa akun 8 kelas; ladder table ada di artefak proses.
