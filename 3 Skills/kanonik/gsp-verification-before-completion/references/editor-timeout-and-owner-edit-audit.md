# Editor-timeout triage, adjudikasi spot-FAIL, owner-edit, dan QA tambalan figur
(Distilasi dari pengawasan gelombang RAFAI/PROMANUAL 04-10-2026; pelengkap
[`manuscript-figure-and-fixpass-verification.md`](manuscript-figure-and-fixpass-verification.md) dan
[`notification-truncation-and-prebase-attribution.md`](notification-truncation-and-prebase-attribution.md).)

## 1. Triase kartu editor TIMEOUT (sebelum vonis, selalu ukur dulu)
Klasifikasi jejak run-1 dengan TIGA pengukuran, lalu tempelkan hasilnya di catatan retry:
1. **Byte-identity vs basis vonis**: bandingkan ukuran/mtime tiap bab target dengan
   snapshot yang sudah dibekukan di komentar vonis tulis-nya. Tiga keadaan:
   - semua delta +0, workdir kosong → mati sebelum apply; retry mulai normal dari nol;
   - sebagian bab tersentuh TANPA workdir → bahaya (suntingan tanpa jejak); arahan
     run-2: arsipkan state sekarang, audit dua-arah vs basis vonis, JANGAN apply ulang buta;
   - suntingan + workdir lengkap → tinggal menuntaskan bab sisanya.
2. **Glob workdir, jangan tebak nama**: penamaan `_work/` bervariasi antar-worker
   (`edit678`, `edit-910`, `edit-1213`, bahkan id-kartu `t_59623fef`). Probe nama
   tunggal menghasilkan kesimpulan palsu "jejak tidak ada".
3. **Posisi kematian**: baris VERDICT instrumen terakhir (check ronde-N vs spot ronde-N)
   menunjukkan persis di gerbang mana worker mati — sertakan di catatan retry.
Pola fleet: kartu editor pass 3-bab berulang kali timeout di run-1 (4 dari 4 kasus
04-10) → hipotesis durasi > RUN_TIMEOUT_MS 1800s; usulkan kartu editor per-2-bab bila
pola berlanjut. Ini hipotesis terukur, bukan vonis.

## 2. Adjudikasi spot-FAIL instrumen editor SEBELUM koreksi naskah
Instrumen editor yang menjatuhkan FAIL "SALAH-LAJUR/rujukan salah" bisa salah sendiri.
Bedakan tiga akar satu-satu terhadap berkas hulu, sebelum satu koma pun disunting:
- cacat NASKAH sungguhan (mis. rujukan "JEMBATAN" tanpa nomor bab) → koreksi badan;
- cacat INSTRUMEN (needle & vs "dan", `<` vs "di bawah", caret over-escape, padding ID)
  → betulkan instrumen, naskah TIDAK disentuh, catat di laporan;
- DUA-AKAR: instrumen salah DAN cacat naskah nyata bertahan setelah instrumen dibetulkan.
Vonis pengawas atas klaim editor: cek hulu sendiri satu-satu (grep baris sumber), jangan
cukup membaca laporan resolusi editor. Preseden 04-10: 3 vonis SALAH-LAJUR run-1 =
2 artefak needle + 1 cacat naskah riil; koreksi badan nol untuk yang artefak.

## 3. Gerbang AKURASI-POPULASI (standar baru pass EDIT, layak digeneralisasi)
Dari sampling spot → uji POPULASI PENUH: parser memetakan SETIAP tag klaim inline ke
baris sumbernya di lajur hulu dan menghitung MISS. Hasil 04-10: 333/333 dan 311/311
tag-baris-id cocok, MISS=0, dua kartu beruntun. Format vonis: `AKURASI-POPULASI n/n
MISS=0`. Bila MISS>0, tiap butir masuk adjudikasi §2, bukan koreksi buta.

## 4. Owner-edit artefak terbit (pola koreksi label TANPA mutasi bukti)
Koreksi domain pada laporan hasil uji dilakukan pemilik artefak lewat KARTU resmi, dan
pengawas membuktikannya dua-sisi:
- berkas laporan boleh tumbuh HANYA baris label + baris riwayat (delta byte harus
  rekonsiliatif dengan isi yang ditambah);
- bukti mentah KEKAL: mtime semua berkas raw < waktu edit, DAN hash agregat yang
  dikutip kartu direproduksi pengawas dengan parser sendiri. Pola agregat yang terbukti
  dipakai fleet UJI-LOKAL: `sha256(''.join(sha256(berkas) for berkas sorted))` atas
  direktori raw — cocok 12 digit = klaim "sebelum=sesudah" terbukti dari sisi pengawas.
- sha berkas LAPORAN berubah pasca-gerbang lama: sah bila blok riwayat mencatat entri
  baru; cek rujukan hilir memakai path+tanggal (bukan sha laporan) sebelum melepas.

## 5. QA tambalan figur: hash-idempoten ≠ tambalan benar, dan vision bisa berhalusinasi
- Tambalan cacat semantik WAJIB di-vision-QA ulang dengan pertanyaan uji SPESIFIK per
  cacat lama (arah panah sumbu, posisi label superlatif, placeholder bocor). Preseden
  05-10: fig-8.1 placeholder hilang TAPI superlatif "SANGAT BERBAHAYA" kanan-bawah vs
  klaim panel "kanan-atas paling mahal" masih hidup di `fig_ga.py` (grep konstanta
  skrip = bukti akar); bug lama bisa digantikan bug baru.
- Klaim vision juga perlu diuji ke sumber: typo "terlwati" dilaporkan vision padahal
  skrip hanya memuat "terlewati" → kemungkinan artefak downscale model vision; tandai
  "cek render 100 persen", jangan tetapkan sebagai cacat.
- Registry PNG: verifikasi `sha256(file)` vs entri `_registry.json` per grup (parser,
  bukan percaya). Hitung global marker-di-naskah vs PNG wajib DIULANG tiap gelombang —
  marker baru (FIG-16.1/17.1) lahir setelah cakupan grup figur ditetapkan; grep label
  lintas semua `visual/*/` + semua bab, dan awali positif-palsu `grep 'todo'` dengan
  `grep -v done`.

## 6. Matcher ID lajur — tujuh varian (daftar kanonis per 05-10)
prefik-penuh `R7-F31` | polos-pad `| F31 |` | polos-tanpa-pad `| F3 |` | dua-tanda
`F-07` | tiga-segmen crash→parts-join `R13-F-07` | tanpa-F `R10-05` | dua-tanda-PAD
`F-03`. Normalisasi padding+tanda sebelum mencocokkan; "rusak" dari matcher sempit =
cacat audit pengawas, koreksi dulu sebelum vonis (terulang 5x di gelombang ini).

## 7. Pitfall pengiriman komentar vonis via bash
`hermes kanban comment ... '...'` PECAH bila isi memuat apostrof (mis. "C'") atau pola
berbahaya scanner terminal (`rm -rf` dalam teks uji ikut memblokir perintah). Resep:
isi komentar tanpa apostrof Inggris (tulis "tidak berlaku" bukan "don't"), atau tulis
ke berkas lalu `--file`; cek `grep -c "Vonis pengawas"` pada `kanban show` untuk
memastikan tidak ada duplikasi setelah retry.
