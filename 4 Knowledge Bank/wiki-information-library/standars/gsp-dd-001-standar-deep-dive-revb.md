---
id: gsp-dd-001-standar-deep-dive-revb
type: standar
title: Standar Deep-Dive GSP GSP-DD-001 (DD/GSP/STD/X/2026 Rev B) - aturan umum semua deep dive
status: active
catatan_keputusan: "dipromosikan: PROMOTE-2 t_23320f06: gerbang QA-GEN PASS (QA-FINAL2) + DIST-2 terpasang + PROMOTE lama superseded; sensitif=tidak (preseden ransus), non-dosir"
catatan_verifikasi: "gsp-custodian 2026-10-09 (verifikasi independen - penulis bukan verifikator terpenuhi; kunci verifikasi terpisah TIDAK ditambah karena dispatch mengunci suntingan pada dua field) || Verdict perlu_revisi kelas alamat-pin mekanis - muatan dan seluruh angka beban-rilis LOLOS || Bukti ukur ulang sendiri (bukan salinan): docx Rev B 89.339 B sha16 2af7e8e29b6f17d2 COCOK; gen-source.md 81.945 B sha16 c50e2b4d2011de46 COCOK; Register-Kuantitas-GEN.json 23 entri sha16 640950e87611ad8e dengan bobot [15,15,15,10,10,10,10,10,5] COCOK; EKSEPSI-GEN.json keys meta+rows dan rows=40 sha16 dfa7e7fb8c731231 COCOK lalu 40/40 potongan lokasi ditemukan utuh di teks docx (register bukan hantu); QA-FINAL2.md VERDICT: PASS di baris 55 dengan 17 baris CHECK dihitung sendiri (id 01..13 + pecahan 06a-06d + 10b) semuanya PASS; skill fleet gsp-deep-dive 195 berkas SKILL.md sha16 0baf50c165c0d360 dan beda-sidik kanonik-vs-fleet 0 dari 195 serta nol berkas cache; shim dd-vendor v0.2.0 pointer saja 1.981 B tanpa aturan; bobot beku hadir di teks docx DAN di register; Tabel FM.2 memuat tepat D-01..D-21 dan cocok Decision Log CONTRACT (D-05 rebuild-from-scratch; D-08 manual-intake dengan mail pasif; D-16 bobot beku; D-17 kedalaman setara; D-21 generalisasi plus kanonik renomor D-20=CHECK V-GATE dan D-21=GENERALISASI); dedup nol hit untuk keenam pola di vault dan di wiki selain objek ini (vault 1.672 berkas termasuk diri sendiri sehingga 1.671 pra-objek cocok, wiki 865 berkas cocok persis); metadata bersih (yaml.safe_load lolos, 14 kunci persis skema tanpa kurang/lebih, satu baris status, title==H1, nol pemotongan nilai kelas-2); pembagian kelas_bukti primer utk identitas-struktur-bobot dan sekunder utk angka QA JUJUR bukan overclaim karena angka primer terukur ulang oleh saya dan laporan QA memang tidak saya reproduksi dari nol; sensitif tidak SAHIH utk IL internal mengikuti preseden wiki faktas/ransus-bin-2026-identitas-dokumen.md (RAHASIA, sensitif tidak, status active) dengan syarat penanda klasifikasi RAHASIA - INTERNAL ikut dinaik ke entri wiki dan hak publikasi eksternal tetap Direktur (sudah tertulis di bagian 10) || Zis perlu_revisi - lima tambalan mekanis tanpa mengubah satu pun angka teknik: (1) PENTING pin [R-2] CONTRACT.md basi - ukur kini 41.452 B sha16 c9c6cb8610e1e1f9 versus klaim 40.763 B sha16 59a43c4d220eace7 (CONTRACT tumbuh oleh entri controller pasca-ukur, mtime 09-10 17:23) dan CONTRACT TIDAK ikut dipin di bagian 9 sehingga prosedur DELTA buta terhadap sumber kedua tersering dirujuk - re-pin atau tandai sebagai angka saat pengukuran plus rujuk anchor lewat teks heading sebab log append-only menggeser nomor baris; (2) links[].skills/gsp/gsp-deep-dive/SKILL.md tidak terjalur dari root workspace - ganti ke C:/Users/TRIAL/workspace/gsp-hermes/skills/gsp-deep-dive/SKILL.md atau jalur registry fleet; (3) anchor B0-B5 baris 506-662 memotong isi B5 karena heading B5 ada di 662 sementara Tabel B5.1 dan dry-run kelas kelima hidup di 663-674 - panjangkan ke 506-675; (4) nyatakan basis hitung 679 baris (splitlines dan wc -l memberi 678; 679 = count-newline+1 ala alat misi dan jejak controller) agar tidak terbaca salah; (5) INFO kontradiksi internal sumber - QA-FINAL2 baris 57 mencetak agregat 23 checks/16 PASS sementara tabelnya 17 baris semua PASS; angka objek 17 benar terhadap tabel namun selisih sumber perlu dinyatakan agar pembaca wiki tidak menuduh objek. Syarat promosi: (1)-(3) terpasang lalu verifikator menguji ulang tiga titik itu saja; catatan_keputusan librarian diisi saat transisi status"
catatan_verifikasi_2: "recheck t2 2026-10-09 oleh gsp-custodian (penulis bukan verifikator terpenuhi) || (1) [R-2] menyebut 41.452 B / c9c6cb8610e1e1f9 sebagai hasil ukur penulis, menyimpan 40.763 B / 59a43c4d220eace7 berlabel CATATAN log append-only, dan bagian 9 tidak lagi mem-pin CONTRACT (empat pin DELTA = gen-source/docx/register/eksepsi) COCOK - hidup terverifikasi: CONTRACT bergerak lagi saat uji ini (42.401 B ffbdd1f2ba0f3ceb lalu 43.526 B acf68355f1235780 dalam satu sesi), konsisten append-only dan bukan gerbang, jadi tidak membatalkan || (2) links entri ketiga C:/Users/TRIAL/workspace/gsp-hermes/skills/gsp-deep-dive/SKILL.md ADA dan terbaca, 6.641 B sha16 0baf50c165c0d360 cocok [R-6] COCOK || (3) anchor B0-B5 506-675: '# B0' di 506, '# B5' di 662, '# References' di 676; Tabel B5.1 (664-672) + paragraf dry-run kelas kelima (674) tertutup rentang tanpa memotong COCOK || (4) splitlines gen-source.md = 678 sesuai objek; newline = 678 sehingga 679 = newline+1 sesuai catatan basis COCOK || (5) selisih agregat QA-FINAL2 (baris 57 mencetak TOTAL CHECKS: 23 | PASS=16 vs tabel CHECK 17 baris semuanya PASS) kini dinyatakan di bagian 7 objek, angka mengikuti tabel COCOK || verdict: terverifikasi; catatan_verifikasi pertama dipertahankan utuh sebagai jejak iterasi"
sumber: docs/2026-10-09-mitra-dd-procedure/build/gen-source.md
halaman: FM.2 baris 30-62; A1 baris 74-99; A6.1 baris 243-262; A9 baris 341-361; AA-AC baris 363-501; B0-B5 baris 506-675
tanggal_akses: 2026-10-09
kelas_bukti: primer
sensitif: tidak
perkara: ddv-std-1009
tags: [ddv-std-1009, gsp-dd-001, deep-dive, standar, ukur-bukan-putus, gsp-deep-dive, terbatas-internal]
links: [docs/2026-10-09-mitra-dd-procedure/CONTRACT.md, docs/2026-10-09-mitra-dd-procedure/verification/QA-FINAL2.md, C:/Users/TRIAL/workspace/gsp-hermes/skills/gsp-deep-dive/SKILL.md]
penulis: gsp-librarian
diajukan: 2026-10-09
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-09
dipromosikan-ke: standars/gsp-dd-001-standar-deep-dive-revb.md
---

# Standar Deep-Dive GSP GSP-DD-001 (DD/GSP/STD/X/2026 Rev B) - aturan umum semua deep dive

Objek ini adalah entri kanonik Information Library untuk **GSP Deep-Dive Standard**
(GSP-DD-001, nomor provisional DD/GSP/STD/X/2026), revisi **B** - seperangkat aturan
UMUM yang mengatur SEMUA pekerjaan deep dive GSP lintas kelas objek. Edisi ini
MENGGAANTIKAN rencana promosi edisi vendor-scope (DDV-GSP-STD-X-2026 Rev A), yang atas
vonis cakupan user tidak pernah naik ke IL sebagai standar (lihat bagian 8).

Penulis objek: gsp-librarian (kartu t_23320f06). Verifikator objek: gsp-custodian
(penulis bukan verifikator - lihat bagian 9). Angka, nama, dan hash di bawah diukur
ulang oleh penulis pada giliran kurasi ini terhadap berkas di disk, bukan disalin dari
handoff kartu.

## 1. Identitas keluaran terbit

| Butir | Nilai | Rujukan |
|---|---|---|
| Nama resmi | GSP Deep-Dive Standard, kode internal GSP-DD-001 | [R-1] |
| Nomor dokumen | DD/GSP/STD/X/2026 (provisional - tunggu Register Induk) | [R-1], [R-2] |
| Revisi | Rev B (umum). Rev A = edisi vendor-scope, known-superseded | [R-2], [R-3] |
| Berkas formal | output/GSP-Deep-Dive-Standard-DD-GSP-STD-X-2026-RevB.docx | [R-3] |
| Ukuran + sidik | 89.339 B, sha256[:16] 2af7e8e29b6f17d2 (diukur ulang giliran ini) | [R-3] |
| Halaman nyata | 36 (Word COM ComputeStatistics(2), instance segar) | [R-3] |
| Klasifikasi | RAHASIA - INTERNAL (default controller, dapat diubah Direktur per objek) | [R-1] K5 |
| Bahasa | Inggris penuh; nama regulasi Indonesia verbatim | [R-1] A9/K4 |
| Naskah sumber | build/gen-source.md 81.945 B, sha256[:16] c50e2b4d2011de46, 678 baris isi (splitlines; 679 = hitung-newline+1 ala alat misi) | [R-4] |

## 2. Mandu kendali: mengukur dan menyajikan, tidak pernah memutuskan

Inti standar ini adalah pemisahan tugas: fleet **mengukur, mengisi, mencari, dan
menyajikan**; seluruh hasil bisnis milik Direktur. Satu-satunya permukaan keputusan pada
keluaran adalah slot kosong `Director decision: ______` yang tidak pernah diisi fleet
[R-1, A1 + AC.4]. Dua rem menghentikan suatu lajur: pernyataan kejenuhan ber-angka, atau
tenggat yang ditetapkan user [R-1, A1.3]. Aktivasi hanya lewat nominasi manual user;
tidak ada intake otomatis - email masuk dilaporkan keberadaannya saja [R-1, A1.1; D-08].

Kosakata vonis bisnis (GO/NO-GO/DROP/PARK, kill-fired) dihapus dari keluaran fleet; kill
criteria lama diturunkan menjadi flag register berstatus deskriptif [R-2, D-13/D-14].

## 3. Anatomi dokumen (apa yang boleh dirujuk orang dari entri ini)

Struktur dua bagian, hasil restrukturisasi amandemen generalisasi D-21 [R-2, D-21]:

- **PART A - aturan umum untuk semua deep dive**: A1 cakupan + mandu kendali, A2 definisi,
  A3 urutan tahap S0-S6 dengan gerbang G0-G4, A4 aturan kerja lintas tahap (kartu,
  penulis-bukan-verifikator, pencarian ofensif + akuntansi kejenuhan, akurasi data,
  kelengkapan berkas kerja, bahasa/bentuk keluaran, deliverable per tier, bingkai layout
  dosir), A5 mekanisme flag register + label deskriptif, A6 instrumen presentasi,
  A7 peran dan akun fleet, A8 struktur skill executable, A9 status putusan dan default.
- **Lampiran**: AA skema artefak umum, B spesifikasi skrip gerbang (recompute-checks.py,
  gate_check.py), AC register kosakata terlarang (List A mutlak, List B prerogatif
  Direktur, literal kelas objek yang diterima).
- **PART B - profil penerapan per kelas objek**: B0 kontrak profil + prosedur penerimaan
  kelas baru (enam blok wajib), B1 VENDOR/PRINCIPAL, B2 TECHNOLOGY/PRODUCT,
  B3 MARKET/COMPETITION/EXPO, B4 CLIENT-INTEGRATION, B5 register profil + dry-run kelas
  kelima [R-1, daftar heading gen-source.md].

Denominator kelas objek sengaja **TERBUKA**: kelas baru wajib diterima lewat prosedur B0,
dengan empat preseden internal sebagai contoh minimum bukan daftar mati [R-2, putusan
controller Q-DENOM].

## 4. Register putusan mengikat (D-01..D-21)

Standar bertumpu pada **21** putusan tercatat dari lima ronde diskusi; tidak boleh diubah
kecuali lewat Decision Log kontrak misi [R-1, FM.2; R-2, Decision Log]. Yang paling
mengikat secara operasional saat memakai standar ini:

- D-03 cakupan semua vendor potensial bertingkat menurut taruhan; D-05 rebuild dari nol,
  MITRA Rev A hanya rujukan ide (kerangka Rev A TIDAK diwarisi otomatis).
- D-08 nominasi manual only; D-09 tenggat ditetapkan user per misi (bukan jam baku per tier).
- D-13/D-14 measure-not-decide; D-15 peta prospek masuk sebagai lajur penuh;
  D-17 teknikal = komersial = prospek, kedalaman penuh setara.
- D-16 instrumen skor final; D-18 Inggris penuh; D-19 tanpa jam diam (open item tetap
  bernama dan bertanggal tanpa penagihan).
- D-20 CHECK V-GATE wajib (grep larangan-kata-vonis + diff struktur); D-21 generalisasi
  menjadi aturan umum + profil, vendor turun menjadi satu profil.

Catatan penandaan penting bagi pemakai: token D-20 sempat dipakai dua makna dan sudah
direnormor oleh controller - **kanonik: D-20 = CHECK V-GATE, D-21 = GENERALISASI**. Rujukan
lama ke 'D-20' dalam konteks amandemen terbaca sah sebagai D-21 [R-2, baris renomor].

## 5. Default berdiri (K1-K9) dan bobot beku

Sembilan default mengikat setiap misi sampai Direktur mengamandemen lewat Decision Log,
bukan lewat suntingan senyap pada template atau skrip [R-1, A9]. Butir yang paling sering
dibutuhkan pemakai:

- **K3 bobot beku 15/15/15/10/10/10/10/10/5** untuk sembilan kartu dimensi (teknologi,
  buyer demand, nilai tambah, kompetisi, ekonomi, kedaulatan, regulasi, keandalan, kanal);
  revisi hanya via Decision Log [R-1, A9/K3; R-5, entri register per dimensi].
- K5 klasifikasi default RAHASIA - INTERNAL; K6 nol vonis fleet di artefak mana pun pada
  tahap apa pun; K8 kartu dimensi 0-5 + satu indikator aritmetika tanpa pemetaan band-ke-vonis;
  K9 semua lajur profil pada kedalaman penuh setara [R-1, A9].

## 6. Wujud executable: skill gsp-deep-dive

Standar ini punya pasangan yang bisa dieksekusi agen: skill **gsp-deep-dive** v0.1.0,
disahkan dan dipasang oleh kartu DIST-2 t_cac44e70 ke kanonik `<ws>/gsp-hermes/skills/`
dan registry fleet `$LOCALAPPDATA/hermes/skills/gsp/gsp-deep-dive/` - **195 berkas**,
sidik per-berkas identik pada jalur fisik kanonik vs fleet, nol berkas cache ikut;
SKILL.md sha256[:16] 0baf50c165c0d360 (diukur ulang giliran ini) [R-6].

Rekonsiliasi warisan: paket lama **dd-vendor** dijadikan shim kompatibilitas v0.2.0 berisi
pointer saja (tanpa aturan, skrip, maupun template); aturan vendor pindah konten-kekal
menjadi profil B1 di `references/profiles/vendor.md`, dan regresi lintas mesin membuktikan
engine baru mereproduksi vonis vendor lama identik (rc 0==0, 29 check JSON identik) [R-6].
Backup pra-shim 128 berkas disimpan ber-sidik, tanpa penghapusan diam-diam [R-6].

## 7. Rantai verifikasi yang meloloskan edisi ini

Gerbang yang harus hijau sebelum promosi, dan hasilnya terukur:

- **V-GATE2** atas naskah + skill: VERDICT PASS 9/9 (C1..C9) - pin gen-source
  c50e2b4d2011de46 tak berubah pasca-vonis W-GEN (nol sunting senyap) [R-7].
- **QA-FINAL2** atas docx formal Rev B: **VERDICT: PASS**, 17 baris CHECK (id 01..13 dengan
  pecahan 06a-06d dan 10b) semuanya PASS. Selisih sumber dinyatakan jujur: baris agregat laporan yang sama mencetak `TOTAL CHECKS: 23 | PASS=16` (menghitung baris INFO sebagai bagian agregat) sementara tabel CHECK-nya memuat 17 baris semuanya PASS - angka objek mengikuti tabel, bukan agregat [R-3, baris 57], nol suntingan verifier, sidik awal==akhir run
  [R-3]. Gerbang konten-kekal: heading 94/94, paragraf 149/149, sel tabel 267 hilang=0,
  blok-kode 40/40 [R-3, CHECK 02]. Tautan defect=0; tabel konten 13/13 ber-kepala berulang
  (1 tabel tanpa kepala = pita klasifikasi sampul, dikecualikan per preseden); scanner kanal
  doc exit 0 VERDICT PASS; U+00B7 zona badan = 0; kosakata vonis di luar zona prerogatif = 0;
  halaman COM 36 cocok denominator footer [R-3, CHECK 04/05/08/09/12/13].
- Deviasi bernama yang **sudah tervonis controller** (bukan cacat terbuka): datum_lint
  mencetak FAIL hanya pada DATUM-09 + DATUM-22, keduanya jalur PUTUSAN D-23 sebagai
  deviasi tercatat dengan register eksepsi per baris - **40** lokasi eksepsi terverifikasi
  nyata di teks, sha256[:16] dfa7e7fb8c731231 [R-3, CHECK 10; R-8]. Register kuantitas
  beku **23** entri, sha256[:16] 640950e87611ad8e [R-5].
- Moda layout terpilih **MEKANIS = MODA B** (naskah tanpa sitasi per paragraf -> framePr 0,
  manifest 0, teks penuh 166 mm, krom full-span) per RULE RAIL-BUKTI-DUA-MODA rev B dan
  PUTUSAN D-24; bukan pilihan selera [R-2, D-24; R-3, CHECK 07].

## 8. Dedupe dan status edisi vendor-scope

Vonis dedup pada giliran ini, diukur segar: **edisi vendor-scope TIDAK PERNAH masuk IL**,
sehingga langkah "tandai interim bila terlanjur" menjadi no-op dan tidak ada objek yang
perlu diberi penanda interim. Bukti: grep pola `DD-GSP-STD|Deep-Dive_Procedure|gsp-deep-dive|GSP-DD-001|deep.dive.standard`
atas `vault/` (1.671 berkas .md) dan wiki hidup `AppData/Local/hermes/wiki/` (865 berkas .md)
mengembalikan **nol** hit di kedua rak sebelum objek ini dibuat. Konfirmasi ganda dijalankan
via terminal grep, bukan hanya tool pencarian (pitfall dedup 25-08).

Edisi vendor-scope Rev A (output/DD-VENDOR-Standard-DDV-GSP-STD-X-2026-RevA.docx, 75.593 B,
sha256[:16] 5d919cb3c109e6ef pasca-tambalan FIX-QA) berstatus **known-superseded** menurut
putusan DR-3/Q-SUPERSEDE dan vonis D-22; artefaknya tetap di disk sebagai bahan profil B1
dan jejak misi, BUKAN sebagai standar terbit [R-2, disposisi rantai vendor-scope].

## 9. Pin kesegaran dan prosedur DELTA

- **Tanggal beku: 2026-10-09.** Semua angka pada bagian 1, 5, 7 adalah cetakan alat pada
  giliran itu.
- **Prosedur DELTA (jalankan sebelum memakai angka ini sebagai mengikat):** hash-ulang
  lima pin. Yang pertama dan mengikat untuk putusan: salinan beku kontrak
  `vault/ddv-std-1009/contract-snapshot.md` harus `acf68355f1235780`. Kontrak HIDUP-nya
  append-only dan bertambah tiap giliran vonis controller, jadi perbedaan dengan
  kontrak hidup BUKAN delta yang sah - bandingkan hanya terhadap salinan beku.
  Empat pin sumber-misi berikutnya stabil: naskah `build/gen-source.md` harus
  `c50e2b4d2011de46`, docx Rev B harus `2af7e8e29b6f17d2`, register kuantitas
  `640950e87611ad8e`, register eksepsi `dfa7e7fb8c731231`. Bila salah satu dari
  keempatnya berbeda, sumber berubah pasca-pembekuan: hitung delta (diff
  heading/paragraf/sel + cetak ulang scanner/lint/halaman) SEBELUM mengutip angka
  bagian 5 atau 7, dan jangan bekukan angka baru tanpa ukur ulang.
- **Prosedur revisi:** hanya lewat Decision Log kontrak misi
  `docs/2026-10-09-mitra-dd-procedure/CONTRACT.md` (register D-01..D-24), lalu objek IL ini
  dinaikkan revisinya dengan baris riwayat - DILARANG menyunting entri wiki secara senyap.
- **Instrumen yang membekukan angka:** scanner `scan_ai_footprint.py --channel doc`
  v1.11.0 (pasca-DIST-HEUR, sha16 e5470dc2), `datum_lint` (sha16 eb25cacf), builder
  `scripts/build_gen.py` di atas DatumDocx v2.1.0/engine v2.3.x. Versi instrumen dihitung
  karena heuristiknya berubah dalam misi yang sama (PUTUSAN-HEUR-1009 + addendum A-1.1).
- **Batas render:** penghitungan halaman memakai mesin render Word lokal; renderer pihak
  ketiga dapat menyimpang +-1 halaman [R-3, catatan batas].

## 10. BATAS kelas bukti dan apa yang TIDAK dijamin entri ini

- Kelas bukti objek ini `primer` untuk identitas/struktur/bobot standar (dokumen resmi GSP
  sendiri, diukur dari berkas di disk) dan `sekunder` untuk angka verifikasi QA (dibaca dari
  laporan verifier yang saya tidak jalankan sendiri - vonis PASS-nya saya cek sebagai
  cetakan di disk, bukan saya reproduksi dari nol).
- Etri ini BUKAN dasar untuk menyatakan prosedur "sudah divalidasi pada objek nyata":
  D-06 memutuskan tidak ada pilot, validasi terjadi pada kedatangan nyata berikutnya lewat
  checklist validasi-kedatangan-pertama di dalam standar [R-1, AA.7; R-2, D-06].
- Nomor dokumen masih provisional; penempatan di Register Induk GSP belum terjadi [R-2].
- Nama GSP-DD-001/'gsp-deep-dive' berstatus DEFAULT-REVERSIBEL (DR-1) - veto user masih
  terbuka, dan perubahan nama tidak boleh dianggap final sampai ratifikasi [R-2, Q-NAMA].
- Klasifikasi RAHASIA - INTERNAL melekat pada keluaran dokumen; promosi ke IL internal tidak
  mengubah hak publikasi ke pihak luar. Keputusan publikasi eksternal tetap milik Direktur.

## SUMBER

- [R-1] `docs/2026-10-09-mitra-dd-procedure/build/gen-source.md` - naskah kanonik Rev B;
  seksi FM.2 (baris 30-62), A1 (74-99), A9 (341-361), AA-AC (363-501), B0-B5 (506-675);
  utuh 678 baris isi (splitlines; 679 = hitung-newline+1), sha256[:16] c50e2b4d2011de46.
- [R-2] `docs/2026-10-09-mitra-dd-procedure/CONTRACT.md` - Decision Log D-01..D-19
  (baris 21-104), Ronde 5/D-21 + renomor (129-132), disposisi rantai vendor-scope
  (148-155), PUTUSAN D-24 (189-191), vonis final BUILD-GEN (197-200). SUMBER BEKU: salinan verbatim `vault/ddv-std-1009/contract-snapshot.md` 43526 B sha256[:16] acf68355f1235780 (byte-identik dengan kontrak hidup saat pembekuan, diverifikasi). Kontrak hidup `docs/.../CONTRACT.md` adalah LOG APPEND-ONLY milik controller dan terbukti menua selama misi ini sendiri: 40.763 B (59a43c4d220eace7, ukur awal penulis) -> 41.452 B (c9c6cb8610e1e1f9, ukur custodian) -> 43.526 B (acf68355f1235780, ukur saat pembekuan salinan). Angka-angka lama itu BUKAN cacat muatan melainkan pin-waktu-buat; yang mengikat untuk entri ini adalah salinan beku. Butir kontrak dirujuk lewat anchor TEKS HEADING (Decision Log, Ronde 5, Disposisi hasil), bukan nomor baris - penomoran baris bergeser setiap kali controller menambah entri vonis.
- [R-3] `docs/2026-10-09-mitra-dd-procedure/verification/QA-FINAL2.md` - VERDICT: PASS
  (baris 55), tabel CHECK 01-12 (baris 35-53), tabel VERIFIKASI-AKURASI (baris ~90-100);
  8.786 B, sha256[:16] 54d0774fa57ac05a. Objek terukur: docx Rev B 89.339 B
  sha256[:16] 2af7e8e29b6f17d2.
- [R-4] Ukur penulis giliran ini (9-10): `sha256[:16]` + ukuran byte gen-source.md =
  c50e2b4d2011de46 / 81.945 B / 678 baris isi (splitlines; 679 = newline+1).
- [R-5] `docs/2026-10-09-mitra-dd-procedure/build/Register-Kuantitas-GEN.json` - 23 entri,
  3.852 B, sha256[:16] 640950e87611ad8e; tiap entri bobot dimensi membawa `unit` +
  `src` "CONTRACT.md Decision Log D-16 (bobot beku), naskah Tabel A6.1 + K3".
- [R-6] `docs/2026-10-09-mitra-dd-procedure/skill_distribution_DIST-2.md` (8.631 B,
  sha256[:16] c96a5b02b7ecc765) + ukur penulis: SKILL.md fleet gsp-deep-dive
  0baf50c165c0d360 / 6.641 B; shim `dd-vendor/SKILL.md` v0.2.0 dibaca langsung (pointer,
  tanpa aturan).
- [R-7] `docs/2026-10-09-mitra-dd-procedure/verification/VERDICT2.md` - VERDICT: PASS
  (baris 129), C1..C9 9/9; 10.189 B, sha256[:16] 389b5950c36d18b4.
- [R-8] `docs/2026-10-09-mitra-dd-procedure/build/EKSEPSI-GEN.json` - register eksepsi
  per-baris deviasi DATUM-09/DATUM-22, 12.773 B, sha256[:16] dfa7e7fb8c731231.
- [R-9] Kartu kanban: t_2e10b4ce (QA-GEN, PASS), t_cac44e70 (DIST-2, terpasang),
  t_2060b43b (PROMOTE vendor-scope, ditutup superseded-by kartu ini), t_23320f06 (PROMOTE-2).
