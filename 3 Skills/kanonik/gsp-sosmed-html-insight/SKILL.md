---
name: gsp-sosmed-html-insight
description: "Use when building social-media HTML insight dashboards."
version: 1.3.2
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
metadata:
  gsp:
    category: intelligence
    tags: [social-media, html-dashboard, executive-summary, paten, insight]
---

# Paten: Dashboard HTML Insight Sosmed + Executive Summary Baku

Dikunci 2026-09-08 dari rantai terverifikasi misi PRABOWO-SOSMED-0907 (v1 terverifikasi ronde-1, v2 pendalaman PASS 7/7, v3 lapis-baca-manusia PASS + REVERIF-V3b 6/6; artefak final sha256 eacda8779dc8ad4a). Seluruh aturan di bawah adalah hasil yang TERBUKU lolos verifier independen, bukan preferensi gaya. Lapis kendali misi (fase+gerbang lintas-fase) ada di payung `gsp-social-intel-orchestration` v2.0.0 [PATEN-AKHIR-0909].

## When to Use

User meminta dashboard HTML / laporan insight / ringkasan eksekutif dari hasil crawl atau analisis media sosial; atau controller menyusun misi sosmed-intelligence dengan keluaran HTML. Trigger kata: "crawl sosmed", "insight media sosial", "dashboard HTML sentimen", "ringkasan tren", "executive summary sosmed".

## Kapan dipakai / Kapan TIDAK (scope user 08-09)

- PAKAI: misi analisis atau crawl media sosial yang keluarannya dashboard HTML, laporan sentimen/tren, atau ringkasan eksekutif untuk user.
- TIDAK PAKAI: dokumen HTML umum (laporan teknik, deck, katalog) — paten STRUKTUR dashboard + format EXEC-SUMMARY ini di-scope HANYA untuk sosmed analisis/crawl; untuk dokumen umum pakai skill desain/dokumen yang berlaku.
- PENEGASAN user 08-09: gerbang naturalisasi (seksi "Gate naturalisasi" di bawah dan skill `gsp-output-naturalization`) berlaku GLOBAL untuk SEMUA keluaran manusia di semua jenis misi; yang sosmed-spesifik hanyalah bentuk artefaknya.

## Pipeline fase (kontrak)

1. RT (`gsp-request-translator`) -> 02_structured: definisi operasional topik, entity-match, window waktu eksplisit (W1 utama + P1 pembanding + window_anchor jam penuh).
2. TA (`gsp-task-architect`) -> blueprint dengan KONTRAK-DESAIN: formula terkunci F1-F6 (registrasi resmi F-series: lihat blok PERHITUNGAN), marker uji-grep, seed verifier tercatat.
3. Crawl lane paralel (maks 5 per misi; `gsp-social-media-crawler`; kuota 250 iter): corpus per lane `social/<job_id>/<lane>/` (raw/, items.jsonl skema data-standards, manifest berisi window_anchor + batches, collection_report + LADDER). Patuh pitfall collection-workflow: habiskan leads di raw/ sebelum partial-handoff.
4. Analisis per lane (`gsp-social-media-analyst`): laporan + skrip calc beku `analysis/scripts/<lane>_calc.py` (rerun tanpa interaksi). Unit tampilan = PLATFORM, bukan lane.
5. Builder HTML (`gsp-coder-execution`): SATU file mandiri per revisi (v1, v2, v3 ...); versi lama BEKU, jangan timpa.
6. Verifier independen (`gsp-verifier`): checklist dengan seed tercatat; penulis bukan verifikator; kartu fix maks 2 retry; verdict FAIL mekanik -> kartu fix, bukan tambal diam-diam.
7. Controller ukur artefak sendiri (stat, hash, grep, sampling tautan) sebelum klaim L2 ke user.

## Kontrak struktur HTML (AC terukur; uji grep/parser, bukan kesan)

- Satu file MANDIRI: nol dependensi eksternal saat render (nol CDN/stylesheet/font/API jarak jauh; JS inline DIIZINKAN per amandemen D-02 v1.2.0, lihat seksi Amandemen); html.parser bersih; responsif (viewport + @media).
- Seksinya literal: `<section id="plat-<nama>">` per platform + seksi berita/web TERPISAH sebagai suplemen. Agregat headline hanya platform sosial; framing media dan sentimen warga adalah dua populasi berbeda, jangan digabung.
- Tiap seksi platform wajib punya marker komentar teruji: `<!-- BLOCK:SUMBER DATA:<plat> -->`, `BLOCK:PERHITUNGAN`, `BLOCK:SENTIMEN`, `BLOCK:ARAH TREN`, `BLOCK:ANALISA`, `BLOCK:MATRIKS DIMENSI`. Total marker = uji grep.
- Blok PERHITUNGAN mencetak formula apa adanya (F1 net=(P-N)/(P+N+U)*100; F2 tertimbang=sum(w*s)/sum(w); F3 w=1+log10(1+E), views keluar dari E, engagement tak terlihat=null bukan 0; F4 growth=(nW1-nP1)/max(nP1,1)*100; F5 share; F6 %label) + perintah replikasi skrip. Verifier menghitung ulang dari items.jsonl; delta >2% = FAIL.
- Registrasi resmi formula F-series (ratifikasi D-3, Decision Log D-03 kontrak PATEN-AKHIR-0909): TERKUNCI = F1-F6 (rumus di atas); RESMI-KONSOLIDASI = F7_isu, F8_toponim, F9_aktor, F10_ritme (sumber: kunci sidecar calc beku, `docs/2026-09-08-atlens-template-adoption/identification/02_kontrak-desain-atlens.md` :202) + F13_jangkauan, F14_pengaruh, F15_relasi (sumber: `docs/2026-09-09-gap-driven-collection/identification/03_blueprint-gap-fill.md` :168-205); F11/F12 DICADANGKAN-KOSONG - nomor dilarang dipakai builder/analyst tanpa registrasi baru (anti angka-hitam). Nomor di luar daftar terdaftar = FAIL gerbang nol-angka-hitam.
- Rantai penalaran min 4 per platform: OBSERVASI (angka nyata) -> HIPOTESIS -> UJI (formula+data) -> HASIL -> KEPUTUSAN BACA; tiap platform punya minimal satu rantai KONTRA. Dilarang rantai klise tanpa angka.
- Kutipan: verbatim-locked terhadap items.jsonl; 100% beranotasi (chip peran-bukti + alasan pemilihan + panah ke klaim terdaftar); panah ke klaim fiktif = FAIL.
- Matriks multi-dimensi: isu x platform; geografi toponim berlabel 'dugaan dari teks'; klasifikasi aktor dengan heuristik tercetak (kanal-resmi/media/warga/bot); ritme jam posting vs reaksi; konsentrasi engagement top-10; komposisi bahasa. DEMOGRAFI usia/gender: sel berlabel 'Tidak Tersedia' dengan alasan 'tidak tersedia via jalur gratis' WAJIB tampil (norma v1.3; label lama 'KETERSEDIAAN' untuk sel dilarang di lapisan terlihat); nol angka demografi tanpa sumber (SPK-002; proksi literatur berlabel [proksi-literatur]).
- Gaya: token MASTER_DESIGN preset BUSINESS (putih dominan, navy #1B2A4A header tabel, hijau hanya sinyal positif, merah hanya negatif, pemisah abu tipis, sans-serif grotesk, UPPERCASE label, angka metrik bold). Judul halaman = KALIMAT INSIGHT penuh <= 20 kata, maksimal 1 angka.
- Tautan: href sungguhan, gaya tegas (#0B4FA0 + underline); uji hidup dua lapis dengan seed: host platform anti-bot (x.com, instagram, facebook, tiktok) 403/429/999 tidak otomatis mati, lapis kedua render/arsip; 404/domain mati = FAIL.
- Lapis baca-manusia (WAJIB, bukan opsional): teks terlihat BEBAS token internal (regex F\d+, K-\d+, D-BP-\d+, KLAIM-[A-Z]+-\d+, sum_E, entity-match, id mentah thread) -> padanan bahasa awam + seksi KAMUS ISTILAH collapsible yang memetakan semua kode ke istilah + rumus aslinya (auditabilitas utuh). Eksekutif: narasi >= 25 kata SEBELUM angka pertama. Statistik prosa: rata-rata kalimat <= 20 kata, > 45 kata <= 5%.
- PASCA-substitusi kode wajib pass penghalusan gramatikal: regex kata dobel `\b(\w{4,}) \1\b` = 0 pada teks terlihat; cek silang tanda baca vs versi dasar (titik-koma sah tidak boleh jadi titik + huruf kecil); rebuild lewat skrip reproducible, bukan edit manual berkas jadi.

## Gate naturalisasi (bagian INI berlaku GLOBAL, semua keluaran manusia)

Satu paket dengan lapis baca, bukan tahap terpisah: ekstrak teks terlihat (L1 naratif = korpus governing; L2 dump penuh = baseline INFO, vonis TIDAK diambil dari L2) -> jalankan `scan_ai_footprint.py` (kanal sesuai target: chat/etalase/dokumen/notifikasi) -> predikat: nol FAIL kecuali baris yang dijinakkan override TERDAFTAR di Decision Log kontrak; C-1/C-2/C-3 (A1/A2/A3 em dash, middle dot, emoji kanal formal) mutlak nol di SEMUA register; laporan utuh disimpan sebagai jejak `scan-vN.txt` di folder kontrak. Verifier menolak klaim tanpa berkas jejak. Override register hanya wewenang controller lewat Decision Log (tanggal, kutipan permintaan user, register baru, cakupan, auto-revert).

## Executive summary baku (terkunci; jawaban singkat bila user meminta)

- SETIAP misi sosmed-HTML WAJIB menerbitkan `EXEC-SUMMARY.md` di folder kontrak misi, DIEKSTRAK verbatim dari blok EXEC artefak yang sudah lolos verifikasi (konten-kekal; bukan ditulis ulang dari ingatan).
- Isinya berurutan: (1) 2-4 kalimat narasi 'apa yang terjadi, siapa di mana, kenapa penting' tanpa angka dulu; (2) angka kunci berunit + window waktu eksplisit; (3) peta per platform satu baris per platform; (4) batas jujur (bukan sensus, keterbatasan jalur, hal yang tidak boleh disimpulkan); (5) aturan pemakaian: kanal chat kutip apa adanya + tautan dashboard; notifikasi/dokumen = paragraf 1 + tabel angka + rujukan file & hash; DILARANG pakai angka lintas window; pembaruan hanya lewat kartu revisi + verifier, dokumen beku sampai revisi tercatat.
- Saat user minta "ringkasannya / hasilnya apa": kutip TINGKAT A apa adanya, lampirkan dashboard (MEDIA), sebut level klaim. Jangan merangkai angka dari ingatan atau dari laporan worker.
- DUA TINGKAT (revisi 08-09 pasca HTMLUX-0908, putusan U-02 user): TINGKAT A = blok exec-chat .txt (<= ~700 char) untuk kanal chat/notifikasi, berdiri sendiri; TINGKAT B = blok EXEC lengkap untuk kanal dokumen. Keduanya diekstrak verbatim dari artefak terverifikasi, bukan ditulis ulang.

## Verifikasi & klaim

- Checklist verifier minimal: replikasi scanner baris-per-baris; multiset angka blok == versi terverifikasi sebelumnya (delta 0, selisih hanya berpenanda CORRECTION beralasan); sampling ekuivalensi makna rantai yang disunting; struktur grep; tautan hidup sampling; kutipan verbatim; determinisme build (rumusan kanonik D-5 di bawah).
- Rumusan kanonik determinisme (ratifikasi D-5, Decision Log D-03 kontrak PATEN-AKHIR-0909): uji dua-run byte-identik WAJIB untuk build etalase dan lapis calc. Untuk korpus/lane: dua run normalisasi pada window dan sumber yang sama wajib menghasilkan multiset item_id identik; determinisme jaringan di luar kendali diakui tegas (raw snapshot beku = acuan replikasi).
- Klaim ke user mengikuti ladder: L2 = verifier PASS + controller ukur sendiri. Serah akhir selalu menyebut: path artefak, ukuran, sha256, verdict, jejak scan, jumlah kartu ditutup.

## Norma lapis UX (AMANDEMEN v1.1.0, 08-09 — misi HTMLUX-0908, artefak acuan v4 sha aa695a9c6595faa9; vonis VERIF FAIL-mekanik -> FIX -> REVERIF PASS 6/6)

Backlog STD-GAP B-01..B-12 terimplementasi dan terkunci sebagai syarat rilis, bukan opsional:

- **Kontras terukur (B-01):** SEMUA token warna diukur skrip deterministik (`ux_contrast.py`, pola scripts crawler) terhadap latar; teks >= 4,5:1, swatch >= 3:1; build GAGAL bila ada pelanggaran; uji colorblind-safe simulasi. Hasil hitung-manual masa lalu dianggap terlanjur, wajib diukur ulang alat.
- **Stempel kesegaran (B-02):** kepala dokumen "data diambil: <window> | dibangun: <timestamp build>"; SETIAP sel growth berlabel pasangan periode dua sisi; nol angka bandingan tanpa pasangan tanggal (audit grep).
- **Confidence tertutup (B-03):** taksonomi 7 tingkat + kisaran persen pada atribut/teks (angka parser tetap tampil, konten-kekal); larang campur confidence dan likelihood satu kalimat; sumbu kedua keandalan-sumber x kredibilitas-informasi (Admiralty) sebagai chip + legenda.
- **Siklus & gaya (B-04..B-06):** stempel siklus keluaran kepala+footer; print CSS; badge keterbandingan window di tiap angka banding.
- **Jejak & etika (B-07..B-11):** blok etika-privasi subjek; endnote per klaim + descriptor sumber; markup aksesibilitas (landmark, aria, skip-nav CSS-only); jangkar silang entitas + tabel relasi statis; manifest rilis + statement sumber.
- **Tiga keluaran dari SATU build (B-12 + putusan U-02 user):** (a) dashboard induk, (b) varian exec-only berkas turunan beku (~13KB), (c) blok exec-chat .txt <= ~700 char yang BERDIRI SENDIRI di kanal chat/notifikasi: baris pertama judul-window, >=3 judgment berlabel confidence, nol rujukan yang menuntut buka berkas, angka satu sumber kebenaran dengan induk (sidecar diff substantif = 0).
- **Mobile adalah gerbang rilis (AC-M1):** render Playwright 375px: `scrollWidth == 375` (tabel lebar wajib wadah `overflow-x:auto` via builder, bukan edit manual), 0 elemen interaktif non-prosa < 24px (tautan inline dalam kalimat dikecualikan per WCAG 2.5.8), screenshot 3 seksi kunci jadi artefak.
- **Anti-jenuh (IA):** hierarki 3 tingkat, blok pendek ternavigasi (TOC jangkar CSS-only), lebar baris 60-75 karakter, kepadatan per layar terukur. Ambang mutlak rasio token-angka prosa (IA-3) atas prosa warisan boleh NEEDS_REVIEW bila floor-relatif lolos DAN delta vs basis terverifikasi nol; restrukturisasi prosa = kartu tersendiri dengan gerbang multiset angka identik.
- **Batas proteksi verbatim:** kontrak "rumus asli verbatim" melindungi ANGKA & STRUKTUR rumus, BUKAN menyalakan known defect (kasus F4: kata-dobel warisan substitusi di blok formula dibersihkan dengan gerbang multiset token angka formula 18->18 identik).
- **Penanda komentar berkas (CSS/HTML) jangan memakai `=====`** (memicu scanner C-5 istilah-italic); pakai penanda blok berizin scanner.
- **Determinisme tetap:** dua run build byte-identik (induk+txt+varian); versi lama beku (v3 sha eacda8779dc8ad4a utuh setelah W2+FIX); kontras 0 pelanggaran; scanner set pemicu tidak bertambah vs kontrol versi dasar.

## Amandemen v1.2.0 (09-09, misi GAP-FILL-0909 kartu t_af1b1084; satu revisi tercatat, bukan dua)

### A. Kanal etalase sosmed = JS-inline SATU BERKAS nol-dependensi-eksternal (pengganti aturan nol-JS lama)

Putusan user atas A-02 (verbatim, kontrak ATLENS-ADAPT-0908 `docs/2026-09-08-atlens-template-adoption/contract.md` D-02 08-09 21:15): "boleh pakai javascript selama single file, font boleh di register sebagai alternatif" dengan klarifikasi tujuan (verbatim): "goalsnya adalah report dapat diberikan ke klien dengan single file upload, dan langsung berjalan tanpa ada dependency eksternal". Vonis controller pada butir itu: OPSI B disetujui untuk kelas artefak etalase sosmed. Aturan lama "nol JavaScript" untuk kanal ini DICABUT dan digantikan norma baru:

1. JS inline DIIZINKAN; artefak tetap SATU BERKAS; NOL dependensi eksternal saat render (tanpa Google Fonts/CDN/API apa pun; tautan `<a>` keluar tetap boleh sebagai rujukan, bukan kebutuhan render).
2. Font = self-host @font-face base64 subset woff2 (Archivo/IBM Plex Sans/Mono sesuai stack template, sumber MASTER_DESIGN) ATAU stack fallback lokal bila lisensi/ukuran menghalangi; builder wajib melapor mana yang dipakai + ukuran.
3. Uji gerbang baru 'klien-offline' WAJIB sebelum rilis: render Playwright dengan pemblokiran SEMUA request jaringan selain file://; semua figur tampil penuh (bukti screenshot); non-file request = 0.
4. Determinisme byte-identik tetap berlaku (data statis dibekukan di berkas, bukan fetch runtime).
5. Cakupan amandemen HANYA kanal etalase sosmed; exec-chat, kanal dokumen, dan aturan lain tidak berubah. Gerbang rilis lain (kontras, 375px, scanner+jejak, konten-kekal, versi lama beku) tetap hidup.

Eksekusi terbukti yang mendasari pengesahan ini: artefak v5 bermerek ATLENS pada masanya (merek lapisan terlihat kini SWARM per putusan user 09-09; builder deterministik, JS inline, font base64 505.028 B) vonis awal ATL-VERIF FAIL scoped (FIX-A slot topIssue, FIX-B target sentuh 24px) lalu FIX -> ATL-REVERIF VERDICT PASS 25/25 -> rilis lepas sha256 30a424d4ae5d82dc (`docs/2026-09-09_atlens-verif/`). Nol-JS tidak lagi menjadi syarat; 'klien-offline' yang menjadi syarat.

### B. Kontrak skema payload v1.2 (antarmuka resmi data -> renderer)

Skema payload SWARM adalah ANTARMUKA RESMI antara rantai data dan renderer HTML (nama skema teknis dan path rujukan historis di bawah tidak berubah; non-retroaktif V7-05). Sumber normatif: tabel AT-801..810 di `docs/2026-09-08-atlens-template-adoption/identification/02_kontrak-desain-atlens.md` §2I; spesifikasi field-wajib per platform (SPEC-YT/TT/X/IGH/RBS/BRW) di `docs/2026-09-09-gap-driven-collection/identification/03_blueprint-gap-fill.md` §2 sebagai lampiran referensi; delta v1.2 di §4 blueprint yang sama. Kunci inti sembilan blok (bentuk tidak berubah dari kontrak PERSIS-as-schema): AT-801 periode; AT-802 platform[]; AT-803 volumeHarian[]; AT-804 sentimenHarian[]; AT-805 isu[]; AT-806 aktor[]; AT-807 relasi[]; AT-808 provinsi[]; AT-809 jamHari[]; plus AT-810 enum turunan UI. Lapisan sintetis master (AT-811/812) tetap DIBUANG total. Delta v1.2 HANYA aditif:

1. Flag ketersediaan per kunci: tiap objek yang memuat kunci berpotensi-null mendapat sibling `_ketersediaan` (satu flag per objek, bukan per field).
2. Aturan null: `null` hanya sah bila `_ketersediaan.<kunci>.ada=false` dengan `alasan` dari enum tertutup `SUMBER_TIDAK_MEMUBLIKASIKAN | KUNCI_TIDAK_ADA_ITEM | KUNCI_TIDAK_ADA_DUMP | PLATFORM_TANPA_KONSEP | TEKS_ONLY | PRESISI_TIDAK_CUKUP | LUAR_JANGKAUAN_MISI`. Nilai `0` berarti nol sungguhan dari sumber; 0-isian dilarang.
3. Kunci aditif baru: `aktor[].pengaruh_predikat`, `relasi[].predikat_graf`, `volumeHarian[].jangkauan_metode` ("yt-dlp-json" | "syndication-json" | "regex-teks" | null). Bentuk AT-807 `{dari,ke,bobot}` DIPERTAHANKAN PERSIS; tipe tepi dibawa di kamus Metodologi, bukan menambah kunci inti.
4. Renderer membaca payload apa adanya: angka yang tidak ada di payload dilarang muncul di HTML (konten-kekal); sel null tampil sebagai sel berlabel 'Tidak Tersedia' dengan alasan enum, bukan nol dan bukan kosong diam (amandemen v1.3; lihat seksi Amandemen v1.3.0 butir B.2).

### C. Norma workflow schema-driven (pembalikan alur)

Urutan baku misi sosmed-intelligence: (1) MATRIKS TARGET (kunci skema payload + target pengisian per kolom) ditulis lebih dulu di kartu misi; (2) spesifikasi field koleksi per platform diturunkan dari matriks itu (lampiran SPEC blueprint §2); (3) formula analisis F-series terbuka diformalkan; (4) panen/analisis mengisi baris skema; (5) renderer mengonsumsi payload. Kartu misi WAJIB menyebut MATRIKS TARGET dan rantai menyesuaikan diri terhadap matriks, bukan sebaliknya. Yang tetap mustahil dipanen TETAP menjadi sel berlabel 'Tidak Tersedia' beralasan enum; larangan mengarang diwarisi penuh (AC-V5-14, GF-04 konten-kekal).

## Amandemen v1.3.0 (09-09, misi V7-REVISE-0909 kartu t_91fbd93e; dasar: vonis VERIF7 PASS 8/8 CHECK + VONIS RILIS SETUJU-RILIS atas out/*-v7 sha16 insight eda0bb363772aaea, exec 2d13e794a41fd337, chat 1821ff346b12d2a9; satu revisi tercatat)

### A. Merek lapisan terlihat: SWARM menggantikan ATLENS

1. Putusan user (verbatim, 09-09, kontrak misi V7-REVISE-0909): "oh iya atlens diganti dengan SWARM". Semua contoh, norma, dan teks lapisan terlihat memakai SWARM kapital penuh; varian ejaan lain (Swarm, swarm) nol di lapisan terlihat. Regex uji: `(?<![A-Za-z])[Ss][Ww][Aa][Rr][Mm](?![A-Za-z])` harus selalu menghasilkan bentuk "SWARM".
2. Non-retroaktif (keputusan V7-05): berkas misi lama, artefak beku v1-v6, master template, nama misi historis, nama skema teknis, variabel/path builder, dan path berkas yang mengeja nama lama TIDAK diedit retroaktif. Rujukan historis yang tersisa di dokumen ini (kontrak ATLENS-ADAPT-0908, folder docs bertanda atlens) berstatus jejak audit sah, bukan merek aktif.
3. Kunci penyimpanan peramban: kunci aktif `swarm-theme`; pembacaan fallback ke kunci lama `atlens-theme` lalu migrasi tulis ke kunci baru.
4. Builder memakai konstanta tunggal `BRAND = "SWARM"` dan peta string eksplisit per titik dengan anchor mengandung konteks (validasi lokasi dan jumlah kejadian); sapuan global buta DILARANG karena menyentuh nama misi historis dan kunci skema.

### B. Norma tampilan hasil V7 (syarat rilis, bukan opsional)

1. Seksi sistem-desain default tersembunyi (V7-01). Seksi `id="sistem-desain"` tetap ADA di berkas dengan atribut tersembunyi (hidden plus display none) dan tombol tampil/sembunyi dua arah ber-aria-expanded; tanpa entri navigasi atau daftar isi. Dilarang hapus permanen: gerbang beku builder menuntut keberadaan seksi di DOM, dan penghapusan total butuh putusan user tercatat. Uji wajib: computed display none saat muat, toggle dua arah terbukti di render, aturan print menampilkan kembali isi seksi.
2. Label "Tidak Tersedia" (V7-02). Sel null atau kosong memakai label "Tidak Tersedia" (kapital judul; bentuk kalimat "tidak tersedia" di prosa) disertai alasan dari enum tertutup `_ketersediaan`. Token "KETERSEDIAAN" sebagai label sel = 0 kejadian di lapisan terlihat; kamus istilah mendefinisikan padanannya sekali dan tidak boleh ada dua istilah satu konsep. Uji wajib: sensus label per lapis sama dengan sensus baseline sel null (baris SSR dilaporkan terpisah eksplisit), kontras label >= 4,5:1.
3. Pagination tabel besar (V7-03). Setiap tabel data lebih dari 10 baris disajikan 10 baris per halaman; kontrol halaman keyboard-accessible dengan sasaran sentuh >= 24px; pencarian atau reset filter mengembalikan ke halaman 1; fallback tanpa-JS menampilkan 10 baris pertama plus catatan noscript; cetak selalu penuh (beforeprint memulihkan semua baris, afterprint kembali ke halaman 1); baris SSR harus identik dengan render halaman pertama; dua sumber ukur verifikasi wajib lolos keduanya (ratifikasi D-2, Decision Log D-03 PATEN-AKHIR-0909): (a) KELENGKAPAN TAMPIL disensus dari DOM ter-render (Playwright file://, viewport 1280 dan 375, keadaan figur tertutup dan SEMUA terbuka; predikat: nol tabel yang MENAMPILKAN >10 baris tanpa pager; preseden RVXP CHECK 1-2, seed 20260909rvxp); (b) KEBENARAN ANGKA dari payload JSON/items.jsonl (konten-kekal multiset); payload yang benar TIDAK membebani uji (a).
4. Pass bahasa manusia sebagai tahap WAJIB builder (V7-04). Sebelum rilis, builder menjalankan naturalisasi konten-kekal atas teks terlihat lewat tabel `NATURAL = [(old, new, n, tag)]` yang gagal keras bila anchor tidak cocok; artefak wajib berupa daftar calque dan kandidat tidak natural plus tabel sebelum-sesudah per butir (minimal 10 contoh) dengan nomor baris sumber, disimpan di folder kontrak misi. Aturan kalimat N1-N7 mengikat (maks 25 kata per kalimat prosa dan wajib pecah di atas 30, verba berimbuhan, padanan Indonesia, larang klitik asing seperti "lane-nya", voice aktif, register klien, konten-kekal). Verifier hanya menguji hasil lewat spot-check frasa, penilaian pembaca-manusia, dan sensus register internal; penambalan gaya oleh verifier = cacat proses.

## Pitfall terkunci (semua dari kejadian nyata)

- Menimpa versi lama artefak -> beku, file baru per revisi.
- Angka dari ringkasan worker / ingatan -> ukur disk, hitung dari items.jsonl.
- Substitusi kaku tanpa pass gramatikal -> kata dobel + titik-koma rusak (kasus v3: 20 dobel, 722 fragmen).
- Vonis naturalisasi diambil dari L2 dump penuh -> metrik panjang tidak punya daya pisah di dump bercampur tabel/KPI.
- Demografi dikarang -> pelanggaran SPK-002, hard-fail.
- Crawler berhenti sukarela saat leads masih ada -> lihat pitfall collection-workflow.
- Kode dapur (F11, KLAIM-RD-2, D-BP) bocor ke teks manusia -> gagal uji R-gate.
- Override dianggap sah tanpa entri Decision Log controller -> verifier wajib NEEDS_REVIEW.
- Penggantian merek lewat sapuan global buta -> menyentuh nama misi historis dan kunci skema = pelanggaran ledger; pakai konstanta merek tunggal plus peta string per titik ber-anchor konteks (kejadian nyata V7-0909).
- Seksi sistem-desain dihapus permanen dari DOM -> mematahkan gerbang beku builder; sembunyikan lewat atribut tersembunyi plus tombol tampil/sembunyi, jangan hapus (keputusan V7-01).

## Artefak contoh (rujukan, jangan disalin mentah)

`docs/2026-09-07-prabowo-sosmed-insight/` di shared workspace: contract.md (Decision Log D-01..D-08), identification/03_blueprint.md + 04_addendum-v2.md + 05_addendum-baca-manusia.md, VERIFICATION.md (3 ronde + reverify), out/insight-prabowo-sosmed-2026-09-07{,-v2,-v3}.html, EXEC-SUMMARY.md, scan-v3.txt + scan-v3b.txt, analysis/scripts/ (calc beku + pbw_html_build_v3.py + pbw_extract_v3.py). Acuan lapis UX v4: `docs/2026-09-08-html-ux-upgrade/` (contract D-01..D-06, 02_blueprint-ux.md, verification/VERDICT-HTMLUX-0908.md, verification-rvx/VERDICT-RVX-HTMLUX-0908.md) + out/insight-prabowo-sosmed-2026-09-07-v4.html (sha aa695a9c6595faa9), exec-prabowo-sosmed-2026-09-07.html, exec-chat-prabowo-sosmed-2026-09-07.txt.
Acuan v7 (revisi user + merek SWARM): `docs/2026-09-09-v7-revisi-user/` (contract.md keputusan V7-01..V7-06, identification/02_blueprint-v7.md sha16 44402d9c0059e535, verification/VERIF7-VONIS.md VERDICT PASS 8/8 + SETUJU-RILIS, analysis/scan-v7.txt) + out/insight-prabowo-sosmed-2026-09-07-v7.html (sha16 eda0bb363772aaea), exec-prabowo-sosmed-2026-09-07-v7.html (2d13e794a41fd337), exec-chat-prabowo-sosmed-2026-09-07-v7.txt (1821ff346b12d2a9).

## Catatan revisi internal

- **1.3.2 (2026-09-09, misi PATEN-AKHIR-0909 kartu t_6763dd75)** - satu revisi tercatat atas ratifikasi controller Decision Log D-03 kontrak `docs/2026-09-09-paten-akhir-sosmed/contract.md`: (a) D-2 - ekor norma pagination V7-03 diganti teks ratifikasi dua sumber ukur (DOM ter-render untuk kelengkapan tampil; payload/items untuk kebenaran angka; keduanya wajib lolos); (b) D-3 - registrasi resmi F-series di blok PERHITUNGAN: F1-F6 terkunci + F7-F10 (sidecar calc beku) + F13-F15 (blueprint GAP-FILL), F11/F12 DICADANGKAN-KOSONG; (c) D-5 - rumusan kanonik determinisme masuk seksi Verifikasi & klaim; (d) rujukannya. Snapshot pra-amandemen v1.3.1 sha256 fea53278c27d48e0... tersimpan di backup `pa-dist2_backup_20260909_213000` (terverifikasi sebelum suntingan).
- **1.3.1 (2026-09-09, misi PATEN-AKHIR-0909 kartu t_82b85e36)** - satu revisi tercatat: TAMBAH satu baris pointer lapis kendali ke payung `gsp-social-intel-orchestration` v2.0.0 di paragraf pembuka; tidak ada norma yang diubah; snapshot pra-amandemen v1.3.0 tersimpan ber-sha di laporan distribusi DIST (sha256 77f54cd3...). Registrasi formula D-3 dan kalimat dua-sumber-ukur D-2 TIDAK termasuk revisi ini (menunggu ratifikasi controller; jalur amandemen terpisah - kini dieksekusi di 1.3.2).
