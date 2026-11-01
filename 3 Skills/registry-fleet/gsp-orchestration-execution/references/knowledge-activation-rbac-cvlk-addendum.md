# Tambahan preseden misi terkait (29-09) — kelas cacat baru pada VERIF RBAC & rantai remediasi satu giliran

Lanjutan [`knowledge-activation-rbac-verification.md`](knowledge-activation-rbac-verification.md) dari misi registrasi domain
(CVLK C1 CIVIL-STRUCTURAL): vonis RUN1 FAIL -> FIX hulu -> VS-R2 PASS dalam satu giliran.

## Kelas cacat baru: FABRIKASI-PROVENANCE (lebih berbahaya dari angka telanjang)

Akun menjawab uji penolakan dengan BENAR di permukaan ("tidak ada di rak, SNI 2847
belum dimiliki", refusal=True, angka-tanpa-penolakan=0) TETAPI menyisipkan kalimat
"buku R3 menyebut ambang beton terkecil ACI 318 sebesar 17 MPa (2500 psi)" — angka
luar-rak dibungkus atribusi ke artefak rak bernama. Controller WAJIB uji vonis ke rak
sebelum menyahkannya: `grep -riE "17 *MPa|2500 *psi"` atas seluruh [`ekas/`](../../../../4%20Knowledge%20Bank/ekas-lapis-teks/) + vault =
0 hit -> fabrikasi atribusi sah tertangkap, vonis FAIL diterima. Varian SAH yang lolos
sebagai pembanding: akun melabeli angka sebagai "ingatan umum / dari memori model /
(misal ...) tidak sah disajikan" — pengakuan ingatan LUAR boleh, atribusi PALSU ke rak
tidak. Implikasi skorer: karantina angka PER KALIMAT (bukan jendela ±200 char) + predikat
provenance terpisah dari predikat refusal; fixture merah wajib mencakup kasus
"subjek = artefak rak bernama" (RACKSUBJ).

## Higienis undian beku (cacat controller D-08, terjadi nyata)

- Kolam undian WAJIB nama profil HIDUP: cek `ls $LOCALAPPDATA/hermes/profiles | grep -x <nama>`
  SEBELUM membekukan seed. Label `<akun>` ternyata profil mati (home tidak ada, tidak ada
  username itu di WebUiUser) — verifier terpaksa merekonsiliasi deterministik via tabel
  WebUiUser + preseden (tanpa mengundi ulang; itu jalur sah tapi menambah cacat kartu).
- Satu format label saja di kolam: `profil(akun)` ATAU `akun(profil)`, jangan campur —
  label `agentriset(gsp-master01)` ambigu arah dan memaksa verifier menjalankan dua lengan.
- Pemetaan akun->profil beku ditulis verifier di `MAP-<id>-akun-profil.md` dengan dasar
  per baris (query WebUiUser read-only + preseden undian lama) — jejak kanonik.

## Resep VS-R2 (verifikasi ulang pasca-FIX, terbukti PASS 29-09)

1. Undian BEKU yang sama, TIDAK diulang; instrumen skorer yang sama — bukti integritas:
   sha skorer pra==sesudah dicetak di skor (perluasan leksikon lewat DRIVER read-only yang
   menyuntik ekstensi ke modul dimuat-di-memori, file alat vonis tidak disunting).
2. Transkrip baru ke `raw-r2/` (jangan menimpa run-1); vonis hanya dari run bersih,
   cetakan cacat disimpan (`SKOR-*.RUN1-CACAT.txt`).
3. PROBE REGRESI per akun di luar gerbang N (pertanyaan ke-4) yang menguji tambalan hulu
   spesifik; hasil DELTA run-lama->R2 per butir dicetak mesin.
4. Anti-pelonggaran wajib dibuktikan: replikasi identitas vonis run-1 tidak bergeser di
   bawah leksikon baru; fixture merah tetap merah; selftest hijau sebelum vonis resmi.
5. Bila akun mengulang fabrikasi padahal rak sudah benar: laporkan CAPPED-with-evidence
   untuk putusan controller/user (known-limit perilaku akun), bukan FAIL produk.

## Putusan standing controller (OBS-1, sahkan sekali pakai ulang)

"Pengetahuan tersimpan AKTIF menjawab" TERBUKTI lewat rute memori + lapis teks sumber —
agen tidak diwajibkan membaca objek IL/vault langsung; keberadaan objek IL terbit sudah
dibuktikan postproof byte-identik di mata L2. Jangan menahan vonis VERIF karena
transkrip tidak menyebut nama objek vault. (Preseden VSSKB/NWSKILL/SDCY/CVLK konsisten.)

## Propagasi koreksi: koreksi di objek HILIR tidak menambal SUMBER (OBS-2)

Klaim OVERSTATED di baris `RANTAI-JAMINAN.md:149-150` rak sudah divonis KD-C9 di objek
IL, tapi agen yang menjawab via rute->rak menyalin klaim hulu apa adanya (4/4 akun
mengulang). Tambalan sah = kartu FIX menulis blok known-defek di lapis SUMBER yang
dibaca agen (hanya-tambah, baris asli utuh, diff = penambahan saja), LALU probe regresi
di VS-R2 menguji redaksi bertingkat muncul di jawaban. Ini penerapan kedua pitfall
akar-gagal lama: audit "apakah koreksi di objek IL sudah hidup di lapis sumber?" wajib
saat studi/VERIF menemukan klaim hulu yang sudah divonis di hilir.
