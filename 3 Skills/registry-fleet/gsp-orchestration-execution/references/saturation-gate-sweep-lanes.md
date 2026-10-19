# Gerbang Jenuh Lajur Riset Terpadu (saturation-gate sweep lanes)

Lapisan LAJUR dari norma penutupan riset: kapan satu lajur boleh berhenti, bentuk vonis yang
diterima, dan bagaimana beberapa lajur divonis bersama tanpa saling menulari kelelahan. Norma
induk tidak diduplikasi di sini: 8 kelas jalur + tabel LADDER kanonik ada di
[`worker-offensive-logic.md`](worker-offensive-logic.md); disiplin audit pengumpulan (coverage % vs resmi, resweep, register)
ada di `gsp-verification-before-completion/references/data-collection-audit-discipline.md`;
gerbang kesegaran korpus R-10 ada di [`knowledge-baseline-architecture.md`](knowledge-baseline-architecture.md). Berkas ini hanya
menambah lapis "per lajur" untuk misi yang dipecah menjadi beberapa lajur riset paralel
(preseden nama lajur: L1..L4 di misi FT-EVAL-0920, W1..W5 di FTDEEP-0921).

## Kapan berlaku
- Misi riset/kajian/pengumpulan data yang didekomposisi controller menjadi >= 2 lajur dengan
  lingkup saling bebas (satu metode boleh muncul di dua lajur hanya bila sudut pandangnya
  berbeda dan dinyatakan; duplikasi isi dilarang, duplikasi sudut boleh).
- Setiap kartu lajur menempel RULE PRESISI-HASIL + RULE PENCARIAN OFENSIF utuh (bukan ringkasan)
  dan dilarang menambah klausul penundaan atau pembatasan lingkup karangan sendiri.

## 1. Definisi jenuh per lajur
Sebuah lajur SAH berhenti karena jenuh hanya bila keempat syarat terukur ini terpenuhi:

| # | Syarat | Alat ukur | Preseden nyata |
|---|---|---|---|
| S1 | Seluruh kelas jalur punya akun | 8 dari 8 kelas jalur [`worker-offensive-logic.md`](worker-offensive-logic.md) berstatus dieksekusi ATAU N/A beralasan; N/A tanpa alasan = belum punya akun | L4 §7: "8 kelas dieksplorasi; 6 dieksekusi penuh, 2 N/A beralasan (arsip, sosial)" |
| S2 | Residu dinyatakan ber-angka | Hitungan kandidat teridentifikasi, yang sudah digali, yang tersisa DAN mengapa tersisa (bukan nol tanpa hitungan) | L2 §0: "15 platform dievaluasi; 37 klaim teregister: 34 SOURCE-DERIVED, 1 PROV, 2 ASSUMPTION"; L4 baris vonis: "62 fetch primer; 42 baris register [C-nn]; 10 kueri pendukung" |
| S3 | Rekonsiliasi cakupan | Bila ada angka resmi penyelenggara/vendor sebagai pembanding, selisih > ±5% wajib dijelaskan; direktori yang masih tumbuh diberi label PARTIAL + jadwal resweep, bukan vonis jenuh | data-collection-audit-discipline.md bagian count reconciliation ("mark PARTIAL + schedule resweep instead of pretending saturation") |
| S4 | Register negatif + register tak-terverifikasi | Apa yang TIDAK ditemukan dicatat supaya pekerja berikutnya tidak mencari ulang; angka yang gagal dapat sumber primer ditulis TIDAK ADA DI RAK + sumber yang seharusnya, field dikosongkan bukan diisi seadanya | L4 §8 catatan negatif (judul Lin et al. tidak ada di arXiv per tanggal akses); L2 §6 register ketidakterverifikasian (harga Azure/Bedrock dinamis) |

Vonis jenuh = lajur berhenti karena bukti habis, bukan karena lelah. Vonis yang menyebut
"cukup" tanpa angka residu tidak diterima verifier.

## 2. Format vonis jenuh ber-angka (template)
Satu blok VONIS di akhir berkas lajur, pola teruji dari preseden:

```
Vonis jenuh: <N> kelas dieksplorasi, <M> dieksekusi penuh, <K> N/A beralasan (<sebut kelasnya>).
Sumber primer HTTP 200 terukur: <rincian hitungan per jenis>. Baris register klaim = <n>.
Kueri pencarian pendukung = <n>. Residu: <kandidat tersisa + alasan>. 
Tidak ada vonis buntu; tidak ada klausul lingkup karangan sendiri.
```

Butir wajib dalam vonis: angka fetch primer, baris register, kueri pendukung, kelas N/A
beralasan, dan status floor legal-platform (disebut sebagai floor kerangka hukum, bukan
sebagai klausul etika karangan sendiri; kekosongan akibat floor dicatat sebagai residu vonis,
bukan sebagai alasan buntu, preseden Q-7 FTDEEP-0921).

## 3. Tabel LADDER per lajur
Setiap lajur memegang SATU tabel LADDER sendiri dengan kolom: rung | URL/aksi |
status+timestamp | hasil | keputusan lanjut. Kolom timestamp terisi (jam akses per rung, zona
dinyatakan) karena verdict "hidup saat akses" adalah bagian bukti. Kondensasi diperbolehkan
hanya bila log mentah per rung disimpan dan path-nya disebut (preseden L2: 136 entri mentah di
`raw/L2/ladder.log`, tabel berkas lajur berisi kondensasi per kelas jalur). Aturan turun dari
induk: setiap 404/302 dicoba ulang dengan varian path, sitemap, llms.txt, renderer, atau arsip
sesuai kelas jalurnya sebelum rung ditutup; vonis per-jalur tanpa akun = TIDAK dijalankan.

## 4. Lajur agregat: vonis controller atas sekumpulan lajur
- Controller memvonis MISI jenuh hanya setelah SEMUA lajur menutup dengan vonis sendiri; vonis
  satu lajur tidak menular ke lajur lain (lajur W2 yang mentok tidak membebani W1).
- Kandidat yang ditemukan di satu lajur tapi milik lingkup lajur lain WAJIB dilempar antar lajur
  dengan tercatat (register lempar), bukan dibiarkan mati di lajur penemu.
- Vonis cakupan lintas lajur (sejauh mana tujuan misi tercapai dengan teknologi terdokumentasi)
  adalah beban jawab kartu sintesis, ditutup dengan vonis jenuh ber-angka per lajur sebagai bahan.
- Verifier menguji per lajur: tabel LADDER ada, blok VONIS ada, tidak ada baris ladder tanpa
  status, tidak ada vonis buntu tanpa akun 8 kelas, tidak ada klausul etika/lingkup karangan
  sendiri (grep pola penolakan oleh verifier; temuan = FAIL).

## 5. CAPPED-with-evidence = permohonan putusan, bukan keputusan pekerja
Bila lajur membentur gerbang struktural (robots/named-agent block di jalur hidup, auth-wall,
rate limit persisten): pekerja mendata ulang jalur sah yang tersisa (arsip CDX, snapshot, rilis resmi,
aggregator bertanda PROV), merge yang ada, lalu menutup laporan dengan label CAPPED + ladder log
(rung dicoba, bukti, coverage % vs angka resmi). Status CAPPED diajukan sebagai PERMOHONAN
PUTUSAN ke controller setelah 8 kelas terekap (preseden D21 di worker-offensive-logic.md;
D17/D21 di data-collection-audit-discipline.md), BUKAN vonis final sepihak pekerja. Controller
yang memutuskan lanjut/tutup dengan ledger claim + keputusan kontrak. Floor legal-platform
(tanpa akses non-autorisasi, kredensial curian, tembus paywall/DRM/login, penargetan individu)
tidak pernah jadi objek permohonan: itu batas cara, sisanya terbuka penuh.

## 6. Aturan anti-fabrikasi pada gerbang jenuh
- Vonis per-jalur tanpa akun (URL exact, HTTP status/error, timestamp) = TIDAK dijalankan;
  menulis "sudah dicoba" tanpa akun = kartu FAIL oleh verifier.
- Budget/rate habis = partial-handoff + checkpoint resume per baris/halaman (kartu lanjutan
  meneruskan dari register), BUKAN vonis buntu dan BUKAN vonis jenuh.
- Angka vonis dihitung dari log/alat pada giliran itu (fetch count dari direktori raw, baris
  register dari berkas register), bukan dari ingatan penulis; dilarang mengutip angka lajur lain
  tanpa membuka berkasnya.
- Klaim vendor yang belum terverifikasi ditandai KLAIM-VENDOR/PROV dan tidak naik jadi angka;
  kosong lebih baik daripada salah (SPK-002).
- Sebelum membekukan angka pembanding lintas lajur, jalankan gerbang R-10 kesegaran korpus
  ([`knowledge-baseline-architecture.md`](knowledge-baseline-architecture.md)): tanya edisi lebih baru, sapu disk, catat register
  kedaluwarsa; baseline beku dinyatakan bertanggal, edisi baru yang belum terjangkau dinyatakan
  eksplisit.

## 7. Rujukan silang (jangan duplikasi norma induk)
- [`worker-offensive-logic.md`](worker-offensive-logic.md): definisi 8 kelas jalur, kolom ladder kanonik, aturan bukti
  kegagalan, penerapan dispatcher. Berkas ini hanya melapisinya per lajur.
- `gsp-verification-before-completion/references/data-collection-audit-discipline.md`: rekonsiliasi
  hitungan vs angka resmi (±5%), aggregator sebagai last-resort + cross-check sitemap dua arah,
  PARTIAL+resweep vs pretending saturation, CAPPED sebagai terminal state ber-bukti.
- [`knowledge-baseline-architecture.md`](knowledge-baseline-architecture.md): R-10 kesegaran korpus sebelum beku angka, R-11 gerbang
  V-SUSUN; struktur kajian multi-sumber per subsistem milik TA/verifier, bukan lajur.
- Preseden vonis nyata untuk contoh format: `docs/2026-09-20-ft-eval-0920/lajur/L4-methodology.md`
  §7 baris vonis, `L2-hosted-platforms.md` §0 dan §5, `L3-local-ft.md` §8; kriteria vonis per
  lajur misi aktif: CG-2/CG-3/CG-4 di `docs/2026-09-21-ft-deep-dive/identification/01_translated.md`.
- [`saturation-sweep-mission-frame.md`](saturation-sweep-mission-frame.md): kerangka MISI sapuan bergate jenuh dari preseden
  IPDR-GLOBAL-0912 (registri kanonis pembilang tunggal, merge delta-only single-writer,
  kendali mutu controller atas artefak pekerja, gerbang persetujuan user pra-eksekusi,
  mekanika dispatch, format cek progres empat blok). Berkas ini melapisinya dengan vonis
  per lajur; kedua berkas dipakai berpasangan pada misi sapuan multi-lajur.
