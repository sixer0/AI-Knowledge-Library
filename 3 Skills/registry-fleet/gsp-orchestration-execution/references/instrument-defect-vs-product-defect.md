# Cacat ALAT vs cacat PRODUK pada gerbang verifikasi (preseden misi panduan 0925, 25-09)

Kelas masalah: instrumen verifikasi beku (`check_*.py`) menghasilkan NEEDS_REVIEW/FAIL
yang AKARNYA di alat, bukan di artefak. Godaan salah: verifier menambal alat lalu
memvonis hasilnya sendiri, atau predikat dilonggarkan agar hijau.

## Aturan mengikat
1. **Verifier dilarang menambal instrumennya sendiri lalu memvonis.** Bila vonis
   tersangkut cacat alat, worker menahan `complete` (status `blocked` + resep tambalan
   + bukti sandbox, mis. `R3-SANDBOX-GERBANG.log`) dan controller membuka KARTU TAMBAAL
   TERPISAH ke profil coder (penulis tambalan != pemvonis). Preseden: VS-R3 blocked
   NR=2 -> FIX-R3 (gsp-coder-execution) -> VS-R4 (gsp-verifier).
2. **Uji dua arah wajib pada tambalan gerbang** (red-green): (a) hijau di objek nyata
   via jalur baru; (b) MIRROR tanpa konten tambalan harus TETAP GAGAL; (c) instrumen
   pra-tambal vs objek nyata harus tetap gagal seperti semula. Hijau tanpa kontrol dua
   arah = tidak sah. Simpan salinan pra-tambal (`*.R5-orig`); kontrol byte-eksak
   rekonstruksi mirror (buang baris sisipan -> sha lama harus muncul lagi).
3. **Controller menolak usulan pelonggaran predikat** bila struktur kontrak bisa
   dipulihkan di alat produksi. Preseden DG FAIL: verifier menawarkan predikat 'isi
   node saja' (label subgraph dihapus dari uji); ruling controller memakai resep satu
   titik di PARSER builder (`subgraph ID[Label]` -> cetak baris judul grup) sehingga
   butir kontrak desain pulih, bukan predikat didefinisikan ulang agar lolos. Selaras
   RULE KONTRAK DESAIN ANTI-DRIFT butir 4 (pulihkan sistem, jangan tambal gejala).
4. **Nomor CHECK pada kartu WAJIB sesuai instrumen nyata.** Kartu DG-R2 menulis
   'per CHECK 1-7' padahal instrumen hanya punya 1-6; verifier menolak mengarang butir
   7 dan melaporkannya sebagai salah rujuk kartu -> masuk Decision Log sebagai cacat
   controller. Gerbang: sebelum menulis kartu vonis, hitung jumlah CHECK dari instrumen.
5. **Objek uji read-only terbukti:** sha256 dicatat sebelum dan sesudah seluruh run
   verifier/builder; build ulang hanya dari objek vonis PASS (pin sha di laporan).

## Default saat keputusan manusia tidak masuk (ruling D-11)
Klarifikasi berbatas (60 menit) tanpa jawaban: controller mengadopsi OPSI BISA-DIBALIK
(scoped, tercatat di kartu + Decision Log sebagai 'default scoped, bisa dibalik putusan
user'), bukan memblokir rantai selamanya, dan bukan memilih opsi tak-terbalik. Suntingan
penyesuai harus append-minimal (mis. satu kalimat '+2 baris') agar rollback trivial.

## Regenerasi GEN-2 tanpa SYN raksasa (preseden D-14 -> TA-REV3)
Satu kartu SYN raksasa (rakit 14 bab dari 8 lajur) menembak plafon 1800s worker dan
timeout berulang. Bentuk benar untuk dokumen panjang: kartu PENULIS PER-BAB paralel
(WA..WJ, tiap `bab/bab-NN-*.md` diukur terhadap lantai kata + blok konsep dari tabel
spek), EDITOR GAYA terpisah dengan kontrak konten-kekal (memisahkan 'tulis' vs
'haluskan'; penulis != penghalus), lalu PERAKIT MEKANIK (ASM) yang menyuntik
glosarium/daftar sumber dan MENYATUKAN KONVENSI level heading antar bab -- perbedaan
level (`###` vs `##`) antar penulis membuat parser anatomi/G-DEEP melaporkan subseksi
kosong padahal konsepnya nyata. Gerbang controller sebelum perakitan: ukur tiap berkas
bab vs lantai §spek di DISK (kata, emdash, penanda klaim [C-nn]/[R-nn]), bukan dari
klaim kartu; selisih ukuran kartu-vs-disk (126-181 B dari suntingan ekor, kejadian
nyata) selalu memakai angka disk.

## Gerbang mirror artefak biner ke repo (pitfall autocrlf)
`core.autocrlf=true` MERUSAK isi .docx/.pdf/.xlsx yang di-commit (blob repo beda byte
dengan artefak rilis). Wajib sebelum klaim 'mirror terverifikasi': `.gitattributes`
memuat `*.docx binary` (atau `git add --renormalize` setelahnya), DAN bandingkan sha
blob git (`git ls-files --stage` -> `git cat-file -p`) vs sha artefak disk. Kalau
builder/verifier melaporkan byte-identik, controller tetap cek ulang di sisi repo.

## Cara pakai
Tempel rujukan ini di kartu VS/DG/CS mana pun yang memvonis dengan instrumen beku;
verifier menguji kontrol dua arah dan ketiadaan butir karangan; controller menguji
apakah tambalan menyentuh akar (parser/builder) atau gejala (predikat dilonggarkan).
