# Controller-as-Verifier: vonis L2 penuh per kartu F4/F5 + gating remediasi sadar-pin

Sumber: misi PSIKOTES-1008, papan default, 09-10 (kartu t_c09b05ca L21, t_34afca44 L23, t_e2a80652
L22, t_1bc189bd L24, t_e3045e94 L26, t_9dbab7a7 L25, t_5f696791 FIX-6, t_fc4f7814 L27, t_ce393fd0
L28). Controller memvonis L2 sembilan kartu berturut tanpa akun verifier terpisah; pola di bawah
yang membuatnya sah menurut aturan dua-lapis (verifier = akun berbeda dari penulis, ukur segar),
bukan pelonggaran. Semua angka adalah cetakan alat pada giliran ukur masing-masing.

## 1. Tangga vonis L2 controller (tujuh anak tangga, semua wajib ada jejaknya)

| # | Tangga | Contoh terukur |
|---|---|---|
| 1 | Ukur artefak: byte + sha256[:16] + sapuan glif (U+2014/U+00B7/CJK termasuk escape `\\uXXXX` dan entity `&#8212;`/`&mdash;`) | A-blueprint 18.813 B sha16 7b4a9e35..; em/entity = 0 semua varian |
| 2 | Re-eksekusi alat deterministik milik PEKERJA, bandingkan stdout vs CETAKAN pekerja (bukan hanya exit code) | l21_match.py match: fresh == run1 == run2 byte-identik, VERDICT PASS 16/16 |
| 3 | Probe independen dengan parser sendiri atas semantik klaim kunci | uji-silang 37 kunci huruf bank==Doc C mismatch 0; FIX-6: 30/30 kunci bank jatuh di huruf peta, multisete opsi sama, 37/37 baris tabel C dua-arah |
| 4 | Regenerasi sumber hulu dan bandingkan dengan salinan yang dikutip dokumen | `hitung_konversi.py 40` diregen, diff vs output_konversi_v40.txt = nol setelah normalisasi EOL |
| 5 | Jalankan ULANG scanner naturalisasi pada berkas jadi (kanal benar), jangan kutip laporan pekerja | scan kanal doc pada C/D/E/F: VERDICT PASS independen |
| 6 | Verifikasi nol-mutasi objek beku | pin enam bank dihitung ulang SETIAP giliran vonis; pasca-FIX-6 tetap utuh |
| 7 | Vonis hanya dari angka tangga 1-6; summary pekerja cuma penunjuk arah | field result None di L25 tidak menghalangi vonis karena artefak+cetakan utuh |

## 2. Gerbang rebuild-deterministik (lebih kuat dari dua-run-identik)

Determinisme builder terbukti oleh TIGA kondisi sekaligus, semuanya terukur giliran ini:
1. dua run builder stdout byte-identik;
2. rerun builder TIDAK mengubah sha berkas hasil di disk (`ca514c32` tetap setelah rerun;
   `4fa6107c5c7b0afd` tetap; `a13a92f1d654b167` tetap);
3. varian seed-netral / identitas pada skrip yang sama MEMULIHKAN sha rev lama persis
   (FIX-6: varian identitas -> `ca514c329117ba03` == REV-0 yang controller ukur di vonis L22).
Kondisi 3 adalah bukti CAKUPAN: perubahan terisolasi ke yang diklaim berubah, sisanya verbatim.
Ini jawaban untuk kartu remedi/rebuild: minta pekerja menyertakan varian identitas, lalu
controller mencocokkan hasilnya dengan sha rev lama yang ia simpan di vonis sebelumnya.

## 3. Sensor controller: batas-kata atau bungkam (positif-palsu substring)

Greps longgar token pendek pada korpora ID menghasilkan positif-palsu yang bisa salah vonis:
- L28 probe anti-bocor: grep `bobot|sten|...` polos -> 6 temuan palsu, semua substring sah
  ('kon**isten**', 'ter**dampak**'); dengan `\b...\b` -> 0, cocok instrumen pekerja.
- Preseden lama: token `404` muncul dalam string sha256; status harus ter-anchor kolom.
Aturan: probe pengawas atas kata pendek/ambig memakai word-boundary (dan bila perlu kelas
posisi/kolom); saat hasil probe SAYA berbeda dari laporan pekerja, bedakan dulu cacat
instrumen-vs-cacat artefak sebelum menulis vonis (di L28 koreksi ke arah pekerja, declared).

## 4. Gating remediasi sadar-pin (kelas baru: siapa yang mem-pin sha siapa)

Ketika audit menemukan cacat hulu (T-1: typo satu string `Persentasi` di baris 240
`hitung_konversi.py`, terbawa ke `output_konversi_v40.txt:98` dan `D-scoring-rubric.md:234`):
- **Traceroot ke akar, tambal ALATNYA, jangan tambal salinan hilir.** Arah tambal ditentukan
  dokumen ratifikasi: blueprint v40 (L3 user-accepted) sudah menulis bentuk benar, jadi alatlah
  yang menyimpang dari klaim verbatimnya sendiri.
- **Sebelum melepas kartu FIX, sensus SEMUA pemilik pin** lewat search token sha (mis.
  `b3aa4e9d|e7123bf2`); hasilnya menentukan urutan kerja. Pemilik pin di kasus ini: badan D/E/F
  (tabel provenans), konstanta `l24_check.py`/`l26_check.py`, instrumen `l27_mode6_instrumen.py`
  DAN `l28_instrumen.py`, plus arsip historis f2 (JANGAN disentuh, arsip).
- **Edge parent kartu FIX wajib mencakup kartu yang masih running dan instrumennya mem-pin
  objek yang akan bermutasi** (FIX-7 parents=[L27,L24,L28]) - kalau tidak, audit yang sedang
  jalan memvonis byte yang akan berubah = vonis basi.
- **Gate kartu rakit-final di belakang remedi** lewat edge baru pasca-create
  (`hermes kanban link <fix> <rakit>`; terverifikasi parents L29 menjadi [FIX-7,L28,L27]).
- Arsip era lama (`output_konversi.txt` 120') TIDAK ditambal: typo historisnya ikut terarsip;
  pembatasan ini masuk Decision Log (D-13), bukan diam-diam.
- Uji numerik-kekal wajib pada regen cetakan: semua sel angka pra/pasca identik, satu-satunya
  sel berbeda = header yang ditambal, dibuktikan tabel diff sel.

## 5. Tagihan turun-temurun: gagal-tempel = kelas T5 controller (preseden hidup D-11)

Vonis countersign boleh melahirkan tagihan hilir (mis. pengocokan huruf Section B), tapi tagihan
itu TIDAK otomatis sampai ke pekerja. Kejadian nyata: kartu L22 dibuat tanpa kalimat tagihan
(grep `kocok|shuffle` pada body = 0); pekerja merakit urutan-identik-bank secara SAH menurut
kartunya dan hanya melaporkan INFO distribusi; tagihan baru terdeteksi controller saat ukur
pasca-done (sebaran kunci tampil B tetap C=3/5 berturut). Vonis jujur: kelalaian controller kelas
T5, dicatat eksplisit di Decision Log (D-11); jalur perbaikan = kartu FIX terpisah ber-parent ke
kartu sasaran - BUKAN menyalahkan pekerja yang patuh kartu.
Gerbang naik: setiap tagihan dari vonis countersign WAJIB tertempel verbatim di body kartu hilir
saat create, dan controller mengeceknya dengan grep pola kunci saat short-check peluncuran.

## 6. Indikator gaya terwaris genre: putusan kanal eksplisit, bukan lolos senyap (D-12)

Artefak berbadan konten beku (lembar ujian = batang soal verbatim bank tervalidasi) bisa gagal
scanner pada indikator gaya (C-6/C-7/C-13/C-14/C-16 + agregasi D-TA-09) sementara VONIS MUTLAK
(C-1/C-2/C-3/A4-A7/C-4/C-5) nol. Perlakuan yang benar tiga langkah:
1. pekerja mendeklarasikan per-baris dengan alasan (kasus C-13 di sini: identifier = objek
   pengukuran butir E-04, melabelinya dengan bahasa manusia = membocorkan butir);
2. controller menjatuhkan PUTUSAN kanal tercatat di Decision Log (D-12) yang menerima dengan
   disclosures DAN melarang mengejar-hijau dengan menulis ulang konten beku;
3. gerbang serah mewarisi putusan sebagai syarat deklaratif eksplisit di kartunya.
Marker C-10 boleh ditahan sampai kanal sajian final (DOCX) - posisi sah asal tertulis di
catatan artefak, bukan kelalaian diam-diam.

## 6b. Field result None bukan cacat kerja

L25 menutup dengan notifikasi papan berisi ringkasan lengkap sementara `show --json` membaca
`result: None`. Vonis tetap L2 karena seluruh dasar (artefak, cetakan, pin) ada di disk; jejak
vonis bertumpu pada pengukuran berkas + komentar, bukan field ringkasan mesin.

## 7. Replikasi cepat

```
# tangga 2 (alat pekerja): jalankan, cmp vs cetakan
python qc/f4/l24_check.py > $T/r1.txt 2>&1; python qc/f4/l24_check.py > $T/r2.txt 2>&1
cmp $T/r1.txt $T/r2.txt && cmp $T/r1.txt qc/f4/l24-check-run.txt
# tangga 2b: sha berkas hasil sebelum/sesudah rerun builder WAJIB sama
# tangga 4 (regen hulu; NOTE EOL: redirect Windows = CRLF, normalisasi dulu)
diff <(sed 's/\r$//' $T/regen.txt) <(sed 's/\r$//' cetak_acuan.txt)
# tangga 6: sha256 per objek beku vs ledger dict, tiap giliran vonis
# sensor: grep token pendek SELALU \b...\b
```
