# Audit Rantai Beku→Fix→Re-vonis→Refreeze (divalidasi pada satu misi 04-10)

Kelas: pengawas silang atas kartu FIX yang menutup gap register beku (F-series),
re-vonis verifier independen pasca-fix (RVK), dan refreeze register (RFZ) —
lanjutan dari [`cross-lane-register-audit.md`](cross-lane-register-audit.md) (beku awal) dan
[`manuscript-figure-and-fixpass-verification.md`](manuscript-figure-and-fixpass-verification.md) §6 (agregat vs FAIL anak).

## 1. Kartu fix wajib addendum-only; gerbangnya = sha register lama TIDAK berubah

Protokol sah: klaim baru ke `research/FIX/<kartu>/addendum-KL.md` dengan ID
SEMENTARA berprefiks kartu (`KL-F2-01`, `KL-F1-G4-01`); nomor final hanya lahir
di refreeze. Uji pengawas per kartu fix:
- register-KL lajur + register-beku: hitung sha sendiri, cocokkan mtime < waktu
  fix → bukti tidak disunting diam-diam (nyata: R4b `9f67e205` dan beku
  `d005cf4d` bertahan sampai RVK);
- ladder fix ber-akun status+timestamp; render kelas-8 harus EKSEKUSI nyata
  (playwright dump-dom + netlog XHR + judul entity-match), bukan URL dokumen
  bernama kebetulan ("headless.md") — preseden FAIL V3 yang lolos audit mata-1;
- uji lokal (mis. tokenisasi): cross-check angka addendum vs JSON mentah
  field-per-field + jejak alat (`pip show`, probe lingkungan di raw/).

## 2. Re-vonis independen: FAIL lama tidak dibantah, hanya di-revonis atas delta

Vonis RVK sah memuat: (a) PREKONDISI sha16 DUA-SISI dicocokkan sebelum vonis
(register-KL == keadaan saat FAIL dijatuhkan DAN beku == basis V2 — pengawas
menghitung ulang sendiri, tidak percaya cetakan verifier); (b) CHECK eksplisit
`vonis_lama_FAIL=True` lalu mengukur keadaan baru pada sumbu yang benar;
(c) berkas vonis lama tetap di disk (jejak FAIL→fix→PASS terbaca); (d) lingkup
VERDICT ditetapkan eksplisit ("wajib dibaca sebelum memakai vonis ini");
(e) artefak pekerja = bukti PENDUKUNG, bukan dasar vonis; (f) run mentah berulang
tersimpan (iterasi tercatat, bukan satu cetakan bersih).

## 3. Refreeze: rekonsiliasi dua-sisi + anti-loop hash + append-only

Ukuran kunci RFZ yang lolos audit:
- **dua-sisi**: delta baris dihitung dari register (R1 +11, R2 +31, R4 +8 = +50
  KL; NEG +9) dicocokkan TOTAL-nya dengan klaim kartu (59) — angka pekerja dan
  parser pengawas bertemu di angka yang sama;
- **peta final←sementara per baris** dengan kartu asal + alasan (append-only;
  nomor lama 1..N tidak bergeser sehingga rujukan SYN/AGG hilir tetap valid —
  cek ini eksplisit sebelum menyebut refreeze aman untuk hilir);
- **lajur tanpa addendum terbukti tersentuh-nol** via sha identik basis lama;
- **anti-loop hash**: catatan refreeze append-only di DALAM berkas yang di-hash
  membuat sha keadaan akhir hanya boleh dicetak di berkas LOG terpisah — solusi
  benar masalah self-reference; catat mode newline (CRLF/LF) saat mereproduksi
  sha;
- gerbang per-baris saat merge: URL primer HIDUP GET-200 pada giliran itu +
  entity-match host/judul/isi; baris NEGatif digeri akun status+timestamp,
  bukan URL hidup.

## 4. Entity-match literatur via API arXiv hidup (bukan hafalan)

Klaim paper (termasuk ID tahun berjalan yang tak mungkin kuhafal) diverifikasi
netral: `https://export.arxiv.org/api/query?id_list=<id>` → judul dari `<entry>`
terakhir; uji (a) ID resolve (nol NO-ENTRY = tidak ada ID tanpa sumber), (b) domain judul masuk
akal, (c) pairing nama-pendek↔ID-sebaris sebagai SPOT-CHECK saja — baris klaim
yang mengutip ID tanpa mengulang judul adalah NORMAL (pemetaan utuh di
korpus/ladder), jangan vonis MISS karena token judul tidak muncul di baris
klaim. Jejak fetch: `raw/abs_<id>.html` per paper; surplus fetch vs klaim
tercatat, bukan disembunyikan.

## 5. Vision-QA figur DATA nyata (ekstensi §2 naskah-figur)

Figur berangka punya gerbang lebih tinggi dari skema: angka di piksel harus
tertelusur ke hulu SATU-SATU (61/40% == baris R14-F-07; sembilan batang harga ==
R4-F37/F43; rasio tercetak direcompute 0,6/0,05=12x). Uji vision per-figur
mencetak pertanyaan tetap: label sumbu, angka titik data, KETERANGAN SUMBU/
[measured]/tanggal/SNAPSHOT yang TERCIPTA DI PIKSEL, peringatan batas klaim
(r=1 "jangan kutip 3 digit" = preseden bagus), dan cacat baca: tabrakan label
vs kurva, dual-axis linear/log satu plot (rawan salah-baca — catat minor FIG-QA,
bukan blokir), titik-pemisah-ribuan pada label bersatuan MiB (ambigu; sarankan
spasi tipis). Judul grup "REVISI-R3" bisa berarti blok rcParams mesin, BUKAN
tambal figur cacat — cek sha figur lama masih sama sebelum menyebut prasyarat
tambal terbayar.

## 6. Timeout kartu editor: ukur jejak parsial, arahkan retry

Saat notifikasi `timed out; dispatcher will retry`: JANGAN vonis, JANGAN ulang
kerja. Ukur: berkas mana berubah ukuran/mtime (tersentuh) vs masih sha basis
(utuh), dan apakah workdir instrumen terbentuk. Catat di kartu: restart murah di
mana, dan minta retry menerbitkan instrumen+laporan per bab (pola apply/check/
spot/final_ukur EDIT-12/345) supaya vonis kekekalan dua-arah tetap bisa
dijalankan saat flush done tiba.
