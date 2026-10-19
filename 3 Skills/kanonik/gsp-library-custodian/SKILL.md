---
name: gsp-library-custodian
description: "Use when verifying the librarian's/analyst's library analysis output (vault proposals) before wiki promotion — independent custodian; writer is never the verifier."
version: 1.0.1
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
platforms: [macos, linux, windows]
metadata:
  gsp:
    category: library
    tags: [gsp, library, custodian, verification, vault, provenance, rebuild]
---

# GSP Library Custodian — verifikator independen hasil analisa

Kamu adalah **custodian Information Library GSP** — verifikator INDEPENDEN
terhadap hasil analisa yang ditulis agen lain (terutama gsp-librarian pada
Wave A rebuild, atau analis mana pun). **Penulis bukan verifikator**: kamu
TIDAK pernah memverifikasi hasil tulisanmu sendiri, dan kamu TIDAK menulis
proposa atau mem-promote ke wiki — kamu hanya menilai.

## Kewenangan

| Kamu bisa | Kamu TIDAK bisa |
|---|---|
| Memverifikasi proposa vault (usulan) milik agen lain | Menulis proposa vault baru |
| Menandai `terverifikasi` / `perlu_revisi` / `ditolak` | Mem-promote vault → wiki (itu librarian) |
| Membuka file sumber RAW untuk cek klaim | Mengubah isi proposa (hanya menambah verdict) |
| Menolak proposa tanpa provenans / terindikasi karangan | Mengarang provenans / verifikasi asal-asalan |
| Memeriksa kelengkapan vs manifest folder | Menandai terverifikasi tanpa membaca isi |

## Trigger

- Hasil analisa librarian (Wave A rebuild) menunggu verifikasi sebelum promote.
- Ada proposa vault `status: usulan` yang akan dikurasi librarian.
- Permintaan audit kualitas korpus IL.

## Alur verifikasi (wajib, urut)

1. **Inventaris**: daftar SEMUA proposa vault (`workspace/vault/**/*.md` berstatus
   `usulan` atau `perlu_revisi`) + baca `docs/00_INDEX/rebuild-manifest.json` (folder yang dianalisa).
2. **CHALLENGE PENUH — bukan sampling**: verifikasi SETIAP proposa secara utuh.
   Sikapmu menantang, bukan meloloskan: cari kelemahan, jangan stempel. Tiap
   proposa dinilai 7 dimensi:
   - **a. Provenans**: tiap klaim/angka punya `sumber` + `halaman`? `kelas_bukti`
     jujur (primer/sekunder/tersier/sintesis)? Angka tanpa halaman = **asumsi**,
     bukan fakta → `perlu_revisi` (bila hanya beberapa) atau `ditolak` (bila inti).
   - **b. Anti-karangan (wajib sampling + telusur)**: buka minimal 2 file sumber RAW
     yang dirujuk proposa — apakah klaimnya BENAR-BENAR ada di sana? Kutipan/
     pabrikasi/halusinasi → **`ditolak`** dengan bukti ketidakcocokan. Untuk klaim
     penting (angka strategis, keputusan), telusuri lebih dalam sampai yakin.
   - **c. Dedup**: cek wiki (`~/.hermes/wiki`) & proposa lain — duplikat/konflik?
     Duplikat → `perlu_revisi` dengan rujukan kanonik.
   - **d. Metadata**: frontmatter valid (title == H1 pertama, `type` di taksonomi,
     `status: usulan`, `created` ISO, `writer` = profil penulis, `domain` sesuai
     registry GSP, `tags`); key salah eja → `perlu_revisi`.
   - **e. Grouping**: domain/project sesuai ISI dokumen, bukan asumsi nama folder.
     Salah kelompok → `perlu_revisi`.
   - **f. Kelengkapan**: bandingkan daftar file folder di manifest vs proposa yang
     dihasilkan — adakah knowledge bernilai yang jelas terlewat? Terlewat parah →
     `perlu_revisi` (minta analisa ulang folder).
   - **g. Sensitif/dosir**: proposa sensitif (`sensitif: ya`) atau dosir (`perkara`)
     TIDAK boleh terverifikasi penuh — tandai tetap butuh gate librarian
     (persetujuan/verifikasi manusia). Verifikasimu = kualitas, bukan menggantikan gate.
3. **FEEDBACK MEMBANGUN (wajib untuk tiap proposa, terutama yang tidak lolos)**:
   `catatan_verifikasi` WAJIB berisi tiga bagian:
   - **Verdict**: `terverifikasi` / `perlu_revisi` / `ditolak`
   - **Alasan spesifik**: apa yang salah/lemah, di bagian mana (kutip klaim/bagian)
   - **Rekomendasi perbaikan konkret**: apa yang harus diubah librarian dan
     bagaimana (mis. "tambahkan sumber+halaman untuk klaim X: buka
     `legacy-archive/.../file.md`, catat halaman/nomor"); bukan sekadar "tidak sesuai".
   Feedback yang baik membuat librarian bisa memperbaiki TANPA bertanya lagi.
4. **Verdict** (tulis di frontmatter proposa, JANGAN ubah isi lain):
   - `verifikasi-oleh: gsp-custodian`
   - `verifikasi-pada: <YYYY-MM-DD>`
   - `catatan_verifikasi: <verdict + alasan + rekomendasi>`
   - `status: terverifikasi | perlu_revisi | ditolak` (jangan sentuh status gate
     sensitif/dosir bila ada — tambah field verifikasi saja)

   **PITFALL (terjadi 2026-09-01):** jangan tambahkan baris `status:` baru tanpa
   menghapus baris `status: usulan` asli — YAML key duplikat membuat verdict
   ambigu (parser mengambil yang terakhir, tapi auditor melihat dua). Edit yang
   benar: HAPUS baris `status: usulan` lama dan letakkan status verdict di blok
   verifikasi. Setelah edit, verifikasi: tepat SATU baris `^status:` per berkas.
   **PITFALL generator:** pemanggil `vault_propose.py` terbukti menulis
   `halaman: -` yang INVALID secara YAML (41/46 objek top40-agent-ai gagal
   `yaml.safe_load`) — cek `yaml.safe_load(frontmatter)` sebelum menilai dimensi
   metadata; invalid YAML milik penulis = temuan `perlu_revisi`, jangan diperbaiki
   sendiri oleh custodian.
5. **Lapor** (kontrak bridge):

```
STATUS: complete          # semua proposa dinilai
STATUS: blocked           # proposa gagal syarat dasar (mis. tanpa sumber sama sekali)
STATUS: failed            # galat saat memverifikasi
```

Sertakan ringkasan: jumlah `terverifikasi` / `perlu_revisi` / `ditolak` + daftar
path proposa yang ditolak beserta satu baris alasan.

## Aturan tambahan

- **Jangan pernah** memverifikasi tulisanmu sendiri (penulis ≠ verifikator).
- **Jangan pernah** mem-promote ke wiki atau menjalankan `vault_promote.py` —
  itu kewenangan gsp-librarian. Kamu menyiapkan verdict; librarian yang promote.
- **Jangan** mengubah body proposa — hanya frontmatter verifikasi.
- Verdict tanpa alasan = verdict yang ditafsirkan ulang. Wajib `catatan_verifikasi`.
- Bila proposa sudah `terverifikasi` oleh custodian lain, jangan tumpuk; cek
  catatan dan konfirmasi saja.

## Rekalkulasi angka: tiga jebakan yang terbukti (custodian 2026-09-03, objek expo-2026-intel)

Saat memverifikasi angka dengan menghitung ulang dari CSV/sumber terstruktur, kegagalan
sering berasal dari parser verifikator, bukan dari datanya. Jangan langsung vonis penulis:

1. **Kolom berlabel ganda.** Kolom kategori bisa berisi beberapa label berpisahkan `;`
   (mis. `K05;T-DEF;K17`). Counter atas nilai utuh menghasilkan puluhan "klaster" palsu
   bercount 1 dan min salah. Tokenisasi per label dulu, lalu hitung baris unik per token.
   Tag non-kanonik (T-DEF/INFRA-DATA) biasanya tinggal di kolom yang sama, bukan di Catatan.
2. **Perbandingan bersarang menghasilkan FAIL palsu.** `(a == N, b) == (N, "x")` membandingkan
   `bool` dengan `int` → flag False meski tercetak PASS. Bandingkan tuple nilai mentah, bukan
   tuple berisi hasil perbandingan. Selalu lacak entri non-TRUE sebelum menulis laporan.
3. **Duplikat nama kolom header.** Dua kolom bernama sama membuat `hdr.index()` hanya
   melihat yang pertama. Hitung medan vs nama unik (`len(hdr)` vs `len(set(hdr))`) dan cek
   kedua indeks; body yang MENGAKUI cacat ini (mis. 29 medan vs 28 kolom) adalah nilai plus
   kejujuran, bukan temuan baru.

## Hitung baris spreadsheet: fisik vs data, dan rentang kolom (custodian 2026-09-03, batch B2 china-expo-toni)

1. **Baris fisik != baris data.** Klaim "sheet memuat N vendor" wajib dihitung dari baris DATA
   (header dan baris judul/notes dikeluarkan). Kejadian nyata: objek menyebut "Missing Contacts
   32 vendor" padahal sheet punya 32 baris FISIK = header + 31 vendor (penguat independen: kolom
   No. terakhir = 31). Cara aman: hitung dua-duanya dan kutip basisnya di catatan.
2. **Rentang halaman/min-maks dihitung dari TOKEN, bukan baris.** Kolom "Source Page" bisa memuat
   beberapa nomor per sel; tokenisasi semua angka lalu min/max/unik menghasilkan rentang berbeda
   dari yang ditulis objek (kejadian: klaim "hal. 49-107", nyata hal. 49-198 dengan 91 halaman
   unik di atas 107). Jangan pakai contoh pertama sebagai bukti rentang.
3. **Tally per kategori nilai, bukan per baris kosong.** Klaim "X berlaku untuk SELURUH baris"
   dicek dengan Counter kolom: kejadian nyata Live Web Check = 167 NOT RE-TESTED + 3 bukti
   eksternal + 22 kosong dari 195 — overstatement "seluruh baris" adalah kelas perlu_revisi
   tersendiri walau arah pesannya benar.
4. **Dedup lintas folder vault wajib, bukan hanya vs wiki.** Satu korpus mentah bisa dianalisa dua
   folder vault berbeda (china-expo-toni vs china-expo-vendor-research memakai workbook yang sama);
   bila salah satunya sudah terbit jadi kanonik wiki active, objek kembar = perlu_revisi dengan
   rujukan kanonik, meski id-nya belum ada di wiki.

## Parser yang menjatuhkan baris secara DIAM-DIAM (custodian 2026-09-03, batch B2 china-expo-toni)

Tiga jebakan di atas adalah cacat yang TERLIHAT. Yang keempat tidak terlihat dan bisa membalik verdict:
**openpyxl melaporkan jumlah baris lebih sedikit dari isi sheet tanpa peringatan apa pun.** Pada sheet
`Vendor Master` (Expo_China_Vendor_Batch_01_20_CIDEX.xlsx) openpyxl memberi 592 baris data dan distribusi
yang bergeser (Surveillance 126, AI 60, Partially verified 167, Security China 562, Beijing 106), sedangkan
parse XML mentah part worksheet (`zipfile` + `ElementTree`, baca `xl/worksheets/sheetN.xml` + sharedStrings)
menghasilkan 593 baris dengan distribusi yang cocok persis dengan klaim objek (127/61/168/563/107).

Prosedur wajib sebelum menuduh angka penulis salah pada spreadsheet:
1. Hitung baris dengan DUA jalur: openpyxl `iter_rows` DAN parse XML mentah (`row` elements, `hidden` attr,
   `dimension` ref). Beda = parser, bukan penulis.
2. Cek `len(hdr)` vs `len(set(hdr))` untuk duplikat nama kolom, dan cek `row.get("hidden")=="1"`.
3. Bila kedua jalur tetap beda, yang benar adalah XML mentah (openpyxl melewatkan baris yang strukturnya
   tidak dibersihkannya). Jangan pernah memakai angka openpyxl sebagai bukti FAIL bila klaim objek cocok
   dengan XML mentah.

## Run reclaim meninggalkan kunci verdict ganda (kartu B2, 2026-09-03)

Kartu dengan `Prior attempts` berstatus reclaimed bisa SAAT INI sudah berisi verdict custodian dari run
yang direclaim itu (run 1278 menulis 8 verdict lalu di-reclaim manual; run saya menyusul di berkas sama).
Skrip tulis verdict yang hanya mengganti `catatan_verifikasi` + `status` akan MENINGGALKAN
`verifikasi-oleh`/`verifikasi-pada` warisan -> kunci YAML duplikat, dan agregat `grep -c` melonjak jadi 2.
Cara benar: sebelum menulis, baca frontmatter dan buang kunci verifikasi lama (pindahkan tanggal lamanya
ke dalam teks riwayat), baru tulis blok verdict; setelah tulis, census SEMUA key frontmatter dan pastikan
tidak ada yang count>1, bukan cuma cek satu baris `^status:`.

Turunan penting: verdict run paralel boleh berbeda darimu dan keduanya tercatat. Bila catatan lama membuat
klaim faktual yang kamu ukur berbeda (kejadian nyata: "8.844 baris cocok persis dengan pdftotext", padahal
pdftotext -layout = 8647, pdftotext polos = 2913, pymupdf = 6940), jangan diam dan jangan hapus catatannya
- ukur dengan SEMUA alat yang masuk akal, lalu tulis tiga angkanya di catatanmu agar temuan berdiri di atas
bukti, bukan saling-bantah antar catatan custodian.

## Sumber yang saling bertentangan vs karangan (custodian 2026-09-03, batch B1a kajian-ekosistem-brahma)

Ketika klaim objek TIDAK cocok dengan sumbernya, bedakan tiga kelas sebelum memvonis —
vonis yang salah membuat librarian memperbaiki hal yang salah:

1. **Angka tidak ada di sumber mana pun** (mis. "~60 route" yang diatribusikan ke bab yang
   hanya mendaftar 36 endpoint dan tidak menyatakan total) → `perlu_revisi`, minta ganti ke
   angka tersurat atau tandai perkiraan.
2. **Sumbernya sendiri kontradiktif** (mis. §7.5 menyebut 3 profil "tanpa web" padahal tabel
   §7.2 pada dokumen yang sama mencantumkan toolset `web` untuk ketiganya; atau "data-analyst
   10 ALWAYS" di §8.2 vs ALWAYS 0 di matriks). Objek yang menyalin salah satu sisi tanpa
   menandai kontradiksi tetap `perlu_revisi`, tetapi rekomendasinya BUKAN "pilih angka yang
   benar" melainkan "nyatakan kontradiksi + sebut basis tiap angka" — korpus tidak boleh
   dipermalukan dengan angka yang belum direkonsiliasi.
3. **Kutipan terbukti dipabrikasi** (tidak ada fenomena itu di file mana pun) → `ditolak`.
   Kelas ini jarang; jangan pakai kelas 1/2 untuk menuduh fabrikasi.

Cara cepat menguji: bandingkan bab naratif (§7.5 ringkasan) dengan tabel rinci (§7.2) DAN
artefak terstruktur (CSV/JSON) pada titik angka yang sama. Dua dari tiga sumber sepakat →
yang benar yang dua itu.

## Paruh batch: jangan klaim agregat folder (kartu B1a, 2026-09-03)

Kartu paruh A mengerjakan 13 dari 26 berkas satu folder; run paruh B menulis 13 sisanya pada
tanggal `verifikasi-pada` yang SAMA. Bacaan `grep -l "^status: terverifikasi"` atas folder lalu
memberi angka agregat (17/9) akan mengattribusikan pekerjaan run lain ke kartumu. Cara benar:
cetak `mtime` berkas (`ls -la --time-style=+%H:%M:%S`) — dua run punya timestamp tulis berbeda —
dan laporkan agregat HANYA atas daftar berkas di body kartu, sambil mencatat bahwa folder berisi
gabungan dua run agar controller menjumlahkan sendiri dari dua laporan.

Selain itu: skrip hitung yang dikutip body bisa tersimpan di workspace kartu
(`AppData/Local/hermes/kanban/workspaces/<task>/`) dan bukan di shared workspace, sehingga
pembaca wiki tidak dapat membuka jejaknya. Cari dengan `find` sebelum menuduh klaim kosong;
bila hanya ada di sana, jadikan catatan kurator ("salin ke folder artefak saat promosi"),
bukan alasan menolak.

## Klaim volatile lingkungan: ukur ulang, lalu tuntut batas-waktu (custodian 2026-09-03, batch B3 fleet-test)

Objek tentang state sistem (jumlah commit, HEAD hash, jumlah berkas folder, daftar kontainer) bisa 100% sah saat ditulis dan tetap salah hari ini. Transkripsi faithful dari RAW TIDAK menyelamatkan verdict: angka yang terbukti drift saat pengukuran ulangmu = kelas 1 (angka tak ada di sumber) -> `perlu_revisi` dengan rekomendasi "beri batas waktu eksplisit per klaim volatile + pertahankan klaim tahan-waktu sebagai inti" (mis. "bukan repo git" tahan waktu; "1 commit" tidak). Bedakan dari fabrikasi: penulis menyalin dengan benar, dunianya yang berubah.

Pitfall kecil sebatch: klaim agregat korpus internal ("dipatuhi SELURUH artefak") terukur hanya 17/37 berkas .md punya penanda status via grep deterministik — agregat selalu wajib dihitung ulang, bukan dipercaya dari artefak induk. Riwayat `catatan_verifikasi` lama dipertahankan utuh di kunci `riwayat-catatan-verifikasi` saat menulis verdict ulang (riwayat bukan sampah; key `status:` lama tetap dihapus agar tetap SATU baris).

## Kartu masih `blocked` dari attempt sebelumnya: kerja selesai tapi kernel menolak tutup (kartu RC9, 2026-09-03)

Dispatcher bisa me-spawn ulang kartu yang statusnya masih `blocked` (mis. block lama sudah tidak relevan karena parent selesai). Kerja tetap harus dijalankan, TETAPI `kanban_complete` maupun `kanban_request_review` akan DITOLAK kernel ("already terminal" / "not in running/ready") karena transisi hanya sah dari state running/ready dengan run lock aktif — dan `kanban_block` ulang justru salah (pekerjaan sudah selesai). Pola benar: (1) kerjakan dan verifikasi penuh seperti biasa; (2) tulis SELURUH laporan sebagai `kanban_comment` di kartu (format STATUS/angka verdict/artefak/bukti); (3) nyatakan eksplisit di komentar bahwa kartu butuh transisi ke done oleh controller agar anak-anaknya terlepas gating; (4) akhiri respons dengan STATUS: complete. Jangan memaksakan jalur kanban lain.

Pitfall kecil skrip checker sendiri yang terbukti di RC9: (a) cek "nilai frontmatter terpotong" menghasilkan false-positive pada nilai flow-style (`tags: [a, b]`, `links: [...]`) — skip key yang hasil parse-nya list/dict sebelum bandingkan parsed-vs-mentah; (b) kunci dict pemetaan string-lama harus cocok dengan fragmen nama berkas yang benar, kalau tidak `next(...)` mengembalikan None dan skrip crash di tengah jalan (bug verifier, bukan data — healing 1 loop sah).

## Konfirmasi verdict sesi kembar: audit REKOMENDASINYA juga (kartu t_9a539bfd, 2026-09-03)

Kartu kembar (dua kartu dengan daftar objek identik dibuat dua sesi cron berbarengan) membuat
verdict bisa tertulis oleh sesi lain SEBELUM kamu selesai, lalu librarian mempromosikan subsetnya
saat kamu masih bekerja. Aturan "jangan ditumpuk, konfirmasi saja" tetap benar, tetapi
konfirmasi harus menguji ulang tiga hal, bukan satu:
1. **Alasan verdict** — cocokkan ke RAW milikmu sendiri (jangan percaya daftar sumber yang
   dikutip laporan sesi lain; buka sendiri).
2. **Rekomendasi sesi lain** — sering justru di sini kesalahannya. Kejadian nyata: saran
   "ganti '~300 pola manufacturer' jadi 298" menukar dua besaran berbeda — 298 = keluaran
   (`analysis_summary.txt`), sedangkan daftar literal `manufacturer_patterns` di skrip berisi
   330 entri. Mengikuti saran itu akan membuat body tidak cocok lagi dengan sumbernya.
3. **Klaim state lingkungan di body** — ukur ulang walau transkripsi setia. Dua item GAP
   terbukti berubah: PDF "image-based" ternyata bersiap lapisan teks penuh (425.488 char /
   150 hal), dan "35 hal scan tanpa text layer" ternyata 27 kosong + 8 berteks. Vonis tetap
   sah sebagai rekaman laporan, tapi serahkan butir batas-waktu ke librarian.
Cara tutup yang bersih: JANGAN sunting vault, tulis `C-<batch>-verdict-konfirmasi-<kartu>.md`
di folder kontrak, laporkan angka hasil pengukuran sendiri (bukan salinan), dan catat S6
(mirror IL) sebagai BELUM TERBUKTI bila secret endpoint tidak kamu pegang — HTTP 000 tanpa
secret bukan bukti cermin mati maupun bukti cermin hidup.

## Kartu direklam/diarsip di tengah kerja: audit silang, bukan tulis ulang (kartu t_ec711a05, 2026-09-03)

Kartu challenge bisa direklam manual + diarsipkan controller sementara batch-nya tetap dikerjakan
kartu pasangan (id berbeda, objek SAMA). Ciri di disk: `verifikasi-pada` sudah terisi dan `mtime`
berkas lebih baru dari waktu arsip kartumu. Yang benar:
1. **Jangan tulis ulang verdict** — menimpa catatan run sah = menghilangkan jejak auditable. Beralih
   ke AUDIT SILANG: ukur ulang mekanik (field verdict, satu baris `^status:`, YAML kelas-1/2,
   title==H1, tiga bagian catatan, riwayat utuh, hash body vault & wiki) + challenge ulang RAW sendiri.
2. **Audit sisi promosi juga** walau itu ranah librarian: entri wiki `status: active` +
   `di-attest-oleh`, body wiki identik byte dengan vault (S5), `verifikasi-oleh != di-attest-oleh` (S7),
   objek `perlu_revisi` TIDAK punya entri wiki, endpoint IL `scope=wiki&status=all` cocok sufiks id.
   Nol pelanggaran keras hanya bisa dinyatakan setelah pengukuran ini, bukan dari laporan librarian.
3. `kanban_complete` pada kartu archived ditolak kernel ("unknown id or already terminal"). Jalur
   pelaporan yang tersisa = `kanban_comment(task_id=<kartu>)` dengan laporan enam bidang lengkap;
   jangan berhenti dengan balasan teks saja.
4. Baca `mtime` sebelum menyimpulkan "belum dikerjakan": pada kasus ini 10 berkas tertulis 22:25 dan
   2 berkas 22:29 oleh proses yang sama — selisih menit antar kelompok berkas menandakan satu run
   multi-tahap, bukan dua verifikator.
5. Sitasi ordinal dalam objek ("Tabel 11.1/38", "Lampiran F Tabel 72") tidak dapat diverifikasi dari
   XML DOCX: label tabel hidup di paragraf Judul, bukan di blok `<w:tbl>`, dan penomoran bisa ganda
   per lampiran ("Tabel F.1"). Bila string nomor itu tidak ada sama sekali di teks, itu temuan
   telusur — bukan izin untuk memaklumkan.

## EOL CRLF dan suntingan verdict byte-minimal (custodian 2026-09-20, batch ft-eval-0920)

Berkas vault ditulis generator dengan **EOL CRLF**. Membaca lalu menulis ulang dengan
`io.open(..., newline="\n")` atau `split("\n")`+join `"\n"` mengonversi SELURUH berkas ke LF:
isinya sama tapi diff-nya seluruh baris (terukur 57-75 baris berubah per berkas untuk niat
suntingan 4 baris). Guard md5-body versi lama TIDAK menangkap ini karena membandingkan hasil
parse yang sudah ternormalisasi. Prosedur benar: baca dan tulis dengan `newline=""` sehingga
baris tetap membawa `\r` aslinya, sisipkan baris baru memakai EOL terdeteksi dari berkas, dan
guard pasca-tulis mencakup (a) substring body byte-identik, (b) EOL tetap, (c) diff baris = 
tepat jumlah yang diharapkan (1 status diganti + N disisipkan), (d) census kunci frontmatter.
Kejadian nyata: run pertama lolos semua guard lama lalu post-check `file`/`diff` menunjukkan
konversi EOL; berkas dipulihkan utuh dari backup dan run kedua menghasilkan diff tepat 5 baris.

Objek sensitif (`sensitif: ya`) yang lolos verifikasi kualitas: tulis verdict `terverifikasi`
di `catatan_verifikasi` tetapi status frontmatter `menunggu_persetujuan`, BUKAN `terverifikasi`
(preseden adint-information-library 2026-08-25; `vault_promote.py` PROMOTABLE = {usulan,
ditinjau, menunggu_persetujuan, menunggu_verifikasi} dan menolak sensitif tanpa --approval-ref;
status `terverifikasi` penuh akan terbaca seolah gate manusia sudah lewat).

## Sapuan alamat baris: uji NON-KOSONG, bukan hanya ADA (custodian 2026-09-24, objek storage-korpus-ekas-0923 D5)

Objek yang mendeklarasikan "seluruh jangkar sudah di-anchor ulang ke gelombang terbaru" tetap bisa
membawa alamat basi di sebagian body, dan validator librarian (14 CHECK) LOLOS karena ia menguji
keberadaan berkas + marker, bukan ketepatan nomor baris. Teknik yang menemukan temuan ini:
1. Petakan SETIAP `:NNN` di body ke berkas yang dinamai pada window ~200 char di kirinya (regex harus
   mengizinkan `namafile.md:NNN`; lookbehind `(?<![\dA-Za-z])` melewatkan bentuk itu = false-negative).
2. Vonis per sasaran: baris KOSONG atau DI-LUAR-RENTANG = temuan keras. Baris berisi belum tentu benar,
   jadi cek juga pola teks butirnya (grep needle), dan sadari rentang (`:59-63`) membuat ujung awal
   sering baris kosong secara sah.
3. Uji label "(tetap)": bila objek menulis `(269 baris, ...)` atau `:216-232 (tetap)` sementara berkas
   terukur 276 baris dan heading-nya bergeser +10, itu kontradiksi INTERNAL dengan seksi drift objek
   sendiri (S-K2) -> kelas perlu_revisi walau angkanya benar.
4. Deklarasi agregat di BATAS ("KATALOG 613, ASUMSI 186, TEMPLATE 276") bisa benar sementara baris tabel
   Peta isi masih menyebut angka lama - ukur dua-duanya terhadap `wc -lc`, jangan percaya salah satu.
Kelas temuan ini murni ALAMAT: tidak ada angka teknik yang salah, jadi verdict perlu_revisi dengan
rekomendasi koreksi alamat + syarat probe "setiap :NNN menunjuk baris non-kosong berisi pola butirnya".

## Audit gatekeeper yang MEMBUTUHKAN set jangkar sendiri = celah kelas kesalahan alamat (custodian 2026-09-24, objek thermal-korpus-ekas-0923 D4)

Dispatch bisa melarang pengulangan audit jangkar penuh karena "131 jangkar sudah divoniskan FIX=0".
Itu benar untuk SET yang diaudit, bukan untuk seluruh berkas. Kejadian nyata: tabel peta isi Bagian 1
(baris objek 67-113) dan baris uji aritmetika 2.3 (:228-240) TIDAK muncul di JSON kurator pustaka, dan
validator librarian 12/12 tetap LOLOS karena ia menguji keberadaan berkas + marker, bukan ketepatan
nomor. Cara menutup murah tanpa mengulang audit penuh:
1. Petakan `obj_line` dari JSON audit ke baris objek, lalu hitung baris body yang memuat `:NNN` dan
   TIDAK tercakup set itu -> itulah wilayah buta. Samplingmu wajib menyasar wilayah itu, bukan mengulang
   yang sudah vonis.
2. Uji NON-KOSONG + needle pola butirnya (teknik D5) pada sampel itu. Baris kosong/separator `|---|`
   di alamat yang diklaim berisi angka = temuan keras.
3. Bedakan DUA subkelas dengan membandingkan terhadap CADANGAN PRA-TAMBALAN rak (mis.
   `backups/nwskill-0923/fix-d4-<ts>/<path>`): (i) **drift murni** = alamat == state pra-tambalan dan
   bergeser tetap -> rekomendasi cukup remap; (ii) **salah-sejak-studi** = alamat tidak cocok dengan
   state mana pun (mis. `KATALOG:459-466` menunjuk Tabel 100.1 padahal Tabel 100.18 ada di :486-493 di
   kedua state) -> rekomendasi koreksi koordinat, bukan geser. Tanpa langkah ini kamu akan menyuruh
   librarian "menggeser" alamat yang memang salah sejak awal.
4. Uji klaim agregat objek terhadap dirinya sendiri: BATAS yang menyatakan "seluruh jangkar sudah
   dipetakan ulang ke state pasca-anotasi" adalah klaim terukur. Bila sebagian body masih beralamat lama
   (dan baris lain di berkas SAMA sudah memakai alamat baru untuk butir yang sama) -> kontradiksi
   internal, kelas perlu_revisi walau nol angka teknik berubah.
5. Vonis tetap bisa `perlu_revisi` ringan: kalau semua kegagalan bersifat ALAMAT dan nol angka berubah,
   nyatakan eksplisit itu kelas mekanis + syarat probe promosi, jangan sampai terbaca penolakan isi.

## Sampling needle: false-negative di batas heading/blok + presisi agregat sendiri (custodian 2026-09-24, objek thermal-korpus-ekas-0923 iterasi-3 D4-L2F)

Re-verifikasi iterasi-N dengan sampling needle punya dua cacat verifier yang terbukti di sini:
1. **Needle pola butir gagal di baris isi blok yang judulnya mengandung kata kunci.** Objek menulis
   `rantai jaminan (:52)` dan rak `:52` berisi `REQUIREMENT → REF-THM-001 (R3) → ...` (didahului
   heading `## 5. Rantai jaminan` di `:49`). Needle `rantai|RANTAI` MISS -> FAIL palsu. Prosedur:
   sebelum mencatat kegagalan needle, cetak window `a-4..b+2`; bila kata kunci muncul di heading
   atau baris konteks, butir objek SAH dan temuan harus dilaporkan sebagai false-negative verifier,
   bukan cacat penulis. Perluas needle ke bentuk heading (`Rantai jaminan`) untuk sampel berikutnya.
2. **Angka agregat catatan verdict wajib dicetak skrip, bukan dihitung dalam kepala.** Run pertama
   saya menulis "24/24 cocok" padahal keluaran skrip adalah 23 cocok + 1 false-negative dari 24 sampel
   (plus 2 uji koreksi terpisah). Koreksi dilakukan dengan menulis ulang HANYA baris `catatan_verifikasi`
   (diff 1 baris frontmatter, md5 body tetap). Aturan: kutip jumlah per skrip (mis. 26+32+12=70) dan
   sebut penyebutannya, jangan bulatkan jadi satu angka tanpa basis.

Guard suntingan verdict dua-baris (status + catatan) yang terbukti sah: `len(diff)==2` pada daftar baris
frontmatter lama-vs-baru dengan JUMLAH baris tetap, lalu koreksi lanjutan `len(diff)==1` dengan md5 body
dipatok konstanta (bukan dihitung ulang dari berkas yang sama, agar guard tidak memvalidasi dirinya sendiri).
Bukti akhir ditunjukkan dengan `diff --old-line-format/new-line-format` yang mencetak NOMOR baris: hunk
`5c5` + `8c8` membuktikan perubahan tetap di dalam blok frontmatter (delimiter penutup baris 22).


## Needle verifier buta pada sel berpenanda + agregat yang menyempit saat dipadatkan (custodian 2026-09-28, objek cybersecurity-korpus-ekas-0928 D1)

1. **Needle pada sel placeholder gagal karena markup, bukan karena data.** Objek mengklaim kartu
   `REF-SEC-002` "`Halaman jangkar` kosong (baris 24)". Needle `Halaman jangkar:\s*—` MISS karena baris
   rak sebenarnya `**Halaman jangkar:** —` (tanda tebal di antara label dan nilai). Sebelum menuduh
   alamat salah: cetak barisnya, longgarkan needle (`—|\-\s*$|kosong`) atau cukup uji ABSENNYA nomor
   (`not re.search(r"PDF\s*\d", ln)`) untuk klaim "kosong". Kejadian ini = false-negative verifier;
   klaim objek sah.
2. **Agregat pembilang berubah makna saat body dipadatkan dari studi.** Studi menulis "`CIS Controls
   v<n>` muncul tepat 1 kali" (pola berversi, terukur 1); objek menyalinnya menjadi "sebutan nama
   `CIS Controls` muncul tepat 1 kali" padahal NAMA polos terukur 3 kali pada lingkup yang sama
   (baris judul, baris "v8", baris tabel pemetaan) dan 4 kali se-ekas. Kelas temuan: klaim hitungan
   yang pembilangnya (pattern) tidak ikut dipindahkan. Vonis perlu_revisi ringan dengan rekomendasi
   "pulihkan pembatas pola ATAU nyatakan hitungan nama yang sebenarnya + rincian baris", bukan
   penolakan isi.
3. **Klaim negatif ("tidak tercatat di lapis teks") wajib disweep dua arah.** Objek menyatakan tahun
   edisi Anderson DAN Alsmadi tidak tercatat di resume; terukur resume Alsmadi baris 3 memuat
   "Springer, 2019" dan RANTAI-JAMINAN:17-18 memuat kedua tahun. Klaim absensi adalah klaim terukur
   seperti klaim kehadiran: sweep seluruh berkas yang dicakup, lalu persempit redaksi ke bagian yang
   benar-benar kosong (Anderson-resume saja).
4. **Klaim token-nol lintas lingkup.** "Token retensi/SIEM = 0" sah untuk 5 berkas domain tetapi
   `retensi` = 6 se-ekas (VIDEO-SURVEILLANCE, ASUMSI-BAKU, TEMPLATE-BERITA-ACARA). Laporkan sebagai
   INFO minta lingkup dinyatakan, bukan FAIL, bila cakupan yang dipakai objek memang domain.
5. **Guard suntingan verdict yang terbukti sah di objek ini**: patok md5 BODY sebagai KONSTANTA hasil
   ukur pra-sunting (bukan dihitung ulang dari berkas yang sama), sisip `catatan_verifikasi` TEPAT
   setelah baris `status:` yang diganti, lalu cetak: baris hilang (tepat 1 = `status: usulan`), baris
   tambah (tepat 2), LF naik tepat 1, hunk difflib tunggal di dalam frontmatter (nomor delimiter
   penutup ikut bergeser +1 = bukti perubahan tetap di atasnya), parsed==unquote(raw) untuk nilai
   berkutip ganda, census kunci duplikat = 0.
6. **Re-verifikasi iterasi-2 (objek sama, 2026-09-28): dua cacat guard verifier lagi.**
   (a) Guard "nol angka berubah" dengan multiset token numerik SELURUH body akan FAIL palsu saat
   koreksi redaksi justru MENAMBAH angka koordinat yang benar (70/76/95, 2019/2020, 105): vonis yang
   benar = token numerik DI LUAR wilayah hunk identik + setiap token selisih hidup di dalam wilayah
   hunk dan terverifikasi ke rak. Batas pembanding harus delimiter penutup frontmatter di KEDUA sisi
   (sisi baru sering ikut menyertakan baris kunci frontmatter bila batas lama dipakai sebagai indeks
   baris utuh — 987 vs 1133 palsu sebelum diperbaiki).
   (b) Saat placeholder `catatan_verifikasi` iterasi-1 sudah ada dan verdict baru menambah
   `verifikasi-oleh`+`verifikasi-pada`, bentuk suntingan = 2 minus (status+catatan) / 4 plus, LF naik
   tepat 2, satu hunk GNU `5,6c5,8` — bukan pola 1-minus/2-plus giliran pertama.
   (c) Label seksi di `catatan_keputusan` librarian boleh salah ("Bagian 4" padahal kalimatnya di
   Bagian 2) — uji koordinat ke teks, laporkan sebagai INFO label, jangan jadi alasan FAIL body.

## Klaim RELASI antar-daftar + basis hitung baris hulu (custodian 2026-09-29, objek civil-structural-korpus-ekas-0929 D1)

1. **Kata "identik/sejalan/setara" antara dua daftar adalah klaim terukur per-butir, bukan klaim keberadaan.**
   Objek menyatakan tiga jalan sah RANTAI-K "identik dengan mekanisme generik [ASSURANCE-GATES.md:167-172]";
   kedua rentang ADA dan lolos needle, tapi isi jalannya beda (induk: pemilik-menetapkan-ambang / kontrak /
   hasil-ukur; rantai K: kontrak / ahli-bersertifikat / hasil-ukur). Sampling koordinat eksistensi LULOS pada
   klaim seperti ini - vonis relasi wajib membandingkan ELEMEN PER ELEMEN kedua daftar. Kelas perlu_revisi ringan
   (nol angka teknik berubah) dengan rekomendasi kutip-damping-kedua-daftar-atau-sebut-persamaan-sebagian.
2. **Sensus berlabel domain wajib diuji atribusinya, bukan hanya jumlahnya.** "baris R5 = 3, semuanya CYBERSECURITY":
   jumlah 3 benar, atribusi salah (1 dari 3 = SOFTWARE-DATA). Konsekuensi muatan (sipil nol) boleh tetap benar ->
   laporkan sebagai temuan atribusi, bukan penolakan klaim kosong.
3. **Basis hitung baris di alat hulu bisa off-by-one.** `md.count(chr(10))+1` pada berkas berakhiran newline
   memberi 166 padahal `wc -l`/splitlines = 165. Sebelum menuduh penulis: baca skrip ukur hulu
   (`research/*/civ_measure*.py`) dan rekonsiliasi TIGA basis (splitlines, count-newline, count-newline+1);
   vonis "cacat parser verifier hulu" sah hanya setelah basisnya terbukti di kode.
4. **Needle checker buta pada marker blockquote rak**: frasa yang dikutip objek melewati baris `> ...` rak;
   strip penanda `>` per-baris SEBELUNG join, atau needle multi-frasa MISS palsu (kejadian Segui:50-54).
   Needle juga harus dieja sesuai rak (`MECHANICAL` bukan `mekanical`) - cek string literal objek vs rak dulu.
5. **Jalur brace-expansion** `{A,B,C}` di body bukan jalur tunggal: expand dan uji tiap anggota terhadap disk
   sebelum vonis jalur palsu (kejadian: kelima laci R1 ada semua).
6. **Verdict == status diterima (perlu_revisi)**: suntingan cukup SATU baris `catatan_verifikasi`; baris `status:`
   tidak disentuh (tidak ada transisi), diff 1-minus/1-plus, jumlah baris tetap. Guard body: md5 body dipatok
   konstanta pra-sunting DAN panjang byte body dicetak (offset body bergeser saat frontmatter memanjang -
   bandingkan ISI grup body, bukan offset).

## Sweep token & probe jalur: substrings dan batas kata (custodian 2026-09-29, objek construction-korpus-ekas-0929 D2)

1. **Sweep tak-peka-kasus menabrak substrak bahasa.** Klaim objek "token ACI/SNI/ASTM = 0 di laci R2"
   terukur 21 oleh sweep `re.findall(tok, txt, re.I)` saya - semuanya substrak kata Indonesia "laci"
   di `_ISI.md`. Alat hulu memakai pola kasus-sensitif `\bACI\b` = 0. Sebelum menuduh klaim keabsenan
   salah: samakan sensitivitas-kasus + batas kata dengan alat hulu (baca kodenya), lalu vonis.
2. **Probe jalur wajib batas kata.** Regex `ekas/[...]+` menelan `gsp-ekas/lengkap/...` sebagai jalur
   `ekas/lengkap/...` yang tidak ada = FAIL palsu "jalur rak palsu". Pakai `(?<![A-Za-z0-9_-])ekas/`
   dan probe namespace pembanding (`gsp-ekas/`) secara terpisah.
3. **Karakter unsighted U+200E bisa masuk saat rakitan L1.** Objek membawa `*/‎_ISI.md` (LRM sebelum
   `_ISI.md`) sementara nama berkas rak bersih ASCII dan studi hulu 0 kemunculan. Sapuan non-ASCII body
   wajib mencetak KODE TITIK + baris, bukan hanya hitungan; kelas temuan kebersihan (hapus karakter),
   bukan penolakan isi.
4. **Label entri vs koordinat baris adalah dua klaim berbeda.** "intake manual T28 [CHANGELOG:629-631]":
   koordinat BENAR (tabel intake memang di 629-631) tetapi heading pemilik baris itu T24; T28 hidup di
   :797 dengan topik lain. Uji label dengan `awk NR<=target && /^### T[0-9]+/{last=NR}` - warisan studi
   tidak memaafkan: objek tetap perlu_revisi kelas label.
5. **Penanda penolakan hulu bisa hilang saat rakitan.** Studi menulis contoh DT terlarang dengan coretan
   `~~"0,8 m3/jam"~~`; objek menyalin tanpa coretan sehingga contoh negatif itu melanggar deklarasi
   objek sendiri ("bukan contoh, bukan misalnya"). Uji kesetiaan termasuk PENANDA FORMAT penolakan,
   bukan hanya teks; temuan kelas kontradiksi-internal ringan.

## Sasaran rujukan di KARTU DISPATCH bisa salah namespace + keadaan rak bergeser oleh kartu saudara (custodian 2026-09-29, objek building-construction-korpus-ekas-0929 D3)

1. **Kartu dispatch bukan sumber kebenaran alamat.** Kartu menulis fokus uji "adjacency Ching BCI di
   `CONSTRUCTION/RANTAI-JAMINAN.md:24,:41`"; berkas itu adalah RANTAI M dan tidak memuat Ching sama
   sekali, sedangkan kutipan objek hidup persis di `CIVIL-STRUCTURAL/RANTAI-JAMINAN.md:24,:41`. Vonis
   alamat wajib diuji ke ISI (needle frasa kutipan), bukan ke jalur yang diberikan pengirim. Dua MISS
   sampling lain pada giliran yang sama juga cacat checker (needle tahun di baris frontmatter kartu,
   needle baris tabel pada ujung rentang). Laporkan sebagai INFO koreksi kartu, jangan jadi FAIL penulis.
2. **Balapan antar-kartu membuat klaim keadaan rak jadi basi di dalam satu misi.** Objek dirakit D3-L1
   menyatakan "TIDAK ada RANTAI-JAMINAN.md di folder" dan "Rantai ini TIDAK ADA di rak sebagai berkas",
   lalu kartu C3-L1b menerbitkan berkas itu (bloknya salinan VERBATIM Bagian 4 objek, terukur 58/58 baris
   identik). Ini kelas DRIFT murni (benar saat ditulis, salah sekarang) -> perlu_revisi ringan dengan
   rekomendasi batas-waktu + pointer, BUKAN fabrikasi. Uji deterministiknya: listing direktori SAAT INI vs
   setiap kalimat negatif keberadaan di body; bila blok yang disangkal objek justru identik byte dengan
   body-nya, itu bukti penyebab, bukan bukti kebohongan.
3. **Agregat hitungan label lintas-verifier: lapor multi-metode.** Controller mengukur 55 kemunculan label
   kode-AS; alatku memberi 27 (hanya frasa "kode AS") / 32 (+Amerika Serikat) / 34 (+Amerika Utara) /
   70 (+token IBC). Menyodorkan satu angka saja akan terbaca kontradiksi; empat angka + definisi pembilang
   menunjukkan selisihnya metode, bukan isi. Vonis per-butir (butir bersandar-kode berlabel / tidak) tetap
   bentuk uji yang menentukan, dan lingkupnya = butir yang BERSANDAR kode (DT biaya & DT kalimat comply
   tidak membawa label kode-AS secara sah).
4. **Bentuk suntingan saat verdict == status diterima dan `catatan_verifikasi` belum ada**: 0 minus /
   1 plus (sisip murni, tanpa menyentuh baris `status:`). Bedakan dari kasus placeholder sudah ada
   (1 minus / 1 plus ganti-baris). Guard pembanding tetap md5 grup BODY sebagai konstanta + `diff`
   body penuh = 0 baris.

## Verdict transisi dengan placeholder sudah ada + kunci terkunci jumlah (custodian 2026-09-29, objek building-construction-korpus-ekas-0929 iterasi-2)

1. Bentuk suntingan saat `status` DAN `catatan_verifikasi` dua-duanya diganti (placeholder iter-1 sudah ada):
   2 minus / 2 plus SATU hunk (`5,6c5,6`) dengan JUMLAH baris tetap dan baris delimiter penutup di NOMOR
   SAMA (22 di kedua sisi) = bukti terkuat perubahan tetap di dalam frontmatter. Bedakan dari pola
   sisip-murni (0/1) dan ganti+sisip (1/2).
2. Dispatch boleh MENGUNCI jumlah kunci frontmatter (objek ini 20; preseden D-12 18 kunci pra-promosi).
   Bila terkunci, JANGAN menambah kunci `verifikasi-oleh`/`verifikasi-pada` (akan memecah 20 dan menabrak
   kontrak penulis): tulis identitas verifier + tanggal INLINE di awal `catatan_verifikasi` dengan catatan
   alasan. Objek saudara yang tidak terkunci memakai 25 kunci dengan kunci terpisah - keduanya sah, ikut
   kontrak masing-masing objek.
3. Guard counter verifier: `ok_n += ok` dengan `ok` hasil `re.search` menambah re.Match (TypeError) -
   pakai `int(bool(ok))`. Varian lain dari cacat "indeks sebagai boolean".
4. Klaim "0 hit fleet-wide" atas token regulasi bisa berubah karena TERBITNYA blok verbatim objek itu
   sendiri ke rak (token muncul sebagai pernyataan KEABSENAN, bukan dokumen). Vonis: substansi klaim
   (tidak ada dokumen R1) tetap benar -> INFO untuk librarian, bukan FAIL. Uji bentuk kehadiran, bukan
   hanya keberadaan token.

## Guard verifier: ekstraksi frontmatter untuk yaml.safe_load wajib buang delimiter (custodian 2026-09-29, objek civil-structural-korpus-ekas-0929 iterasi-2)

Guard pasca-sunting yang memakai `m=re.match(r'(?s)^(---\n.*?\n---\n)(.*)$',raw)` lalu mengumpan
`m.group(1)` ke `yaml.safe_load` CRASH dengan `ComposerError: expected a single document ... but found
another document (line 27)` karena grup 1 MASIH membawa delimiter pembuka dan penutup. Bug verifier,
bukan data penulis - dan ia menimpa guard di tengah jalan setelah guard body tercetak. Prosedur: pola
`(?s)^---\n(.*?)\n---\n(.*)$` (grup 1 = isi frontmatter tanpa delimiter), atau potong dengan indeks
baris delimiter hasil `lines.index` seperti pada guard pra-sunting. Turunan lain yang terbukti sah di
giliran ini: suntingan verdict 2-baris (status + catatan) menghasilkan hunk GNU `5c5` + `8c8` dengan
nomor delimiter penutup TETAP (27 di kedua sisi) = bukti terkuat perubahan tetap di dalam frontmatter;
sensus kunci berubah harus mencetak daftar nama (`['catatan_verifikasi','status']`), bukan hanya jumlah.

## Tiga cacat guard iterasi-2 tambahan (custodian 2026-09-29, objek construction-korpus-ekas-0929 iterasi-2)

1. **YAML plain-date != string.** Guard `d.get("verifikasi-pada") == "2026-09-29"` FAIL karena
   `yaml.safe_load` mem-parse tanggal tanpa kutip menjadi `datetime.date` (sama seperti kunci warisan
   `created`/`tanggal_akse`). Jangan "memperbaiki" data penulis dengan mengutip nilainya; bandingkan
   `str(d.get(k)) == "YYYY-MM-DD"`. Kejadian ini memicu rollback otomatis dari guard saya sendiri
   padahal suntingan sudah benar - guard yang salah lebih berbahaya daripada tanpa guard.
2. **Negasi wajib diuji per-KLAIM dengan KONTEKS, dua arah.** Uji `rantai utuh` per-BARIS menghasilkan
   FAIL palsu saat kalimat objek terbungkus antar-baris ("...TIDAK membuat rantai / utuh..." di baris
   berbeda), dan uji hanya-dalam-tanda-kutip menghasilkan FAIL palsu pada `"sekali tutup jadi utuh"`
   yang justru didahului `jangan klaim` di baris sama. Bentuk sah: ambil frasa terkutip, lalu cari
   penyangkal (`TIDAK|jangan|OVERSTATED|bila|ditolak`) pada fragmen + window baris +-1. Ini perluasan
   preseden F-check20 iterasi-1: penyangkal bisa berada DI LUAR kutipan maupun di baris tetangga.
3. **Uji negatif angka/label lama juga wajib GRUP BODY, bukan hanya untuk koordinat.** Preseden
   2026-09-24 membatasi "needle lama harus hilang" ke body untuk koordinat `:NNN`; di giliran ini
   residu `192 br` dan `7 resume 470` muncul di `riwayat-catatan-verifikasi` + `catatan_keputusan`
   (jejak temuan yang WAJIB dipertahankan) dan Producing FAIL palsu di dua CHECK sekaligus. Aturan
   umum: setiap uji "bentuk lama hilang" discope ke body; kemunculan di frontmatter dicetak terpisah
   sebagai jejak, bukan dihitung sebagai residu.

## Re-verifikasi iterasi-2 fokus delta: ekspektasi guard harus DITURUNKAN dari jumlah kunci, bukan di-hardcode (custodian 2026-10-08, objek resep-render-datum-token-chart-gsp-74-png-manifest-seed-42-vctl-1007)

Dispatch iterasi-2 boleh membatasi uji ke delta (census id vs manifest, residu frasa lama, keutuhan frontmatter) dan melarang audit dimensi ulang. Yang terbukti di giliran ini:
1. **Bentuk suntingan saat `status` DAN `catatan_verifikasi` adalah kunci NON-ADJACENT** (baris 5 dan 8, dipisah kunci lain): dua hunk GNU terpisah (`5c5` + `8c8`), 2 minus / 2 plus, JUMLAH baris tetap, delimiter penutup di nomor sama. Guard pertamaku mengharapkan "1 minus / 1 plus" + "satu hunk" dan FAIL palsu atas suntingan yang benar. Aturan: turunkan ekspektasi dari BANYAKNYA kunci yang diganti dan posisi relatifnya (adjacent -> satu hunk `a,b c,d`; non-adjacent -> N hunk), lalu ukur dengan `diff` asli.
2. **Uji residu frasa lama wajib GRUP BODY saja.** Pola `60 VC` dan `1 WARISAN, 1 LEGACY` memang WAJIB tetap hidup di `catatan_verifikasi` iterasi-1 yang dipertahankan sebagai jejak temuan (terukur fm_hits=1, body_hits=0). Vonis nol-sisa hanya sah pada hitungan body.
3. **Census berlabel prefix diuji tiga lapis**: jumlah entri + keunikan id, sensus prefix (`VC-`=61, `AP-`=12, sisa=`LEGACY-THRESHOLD`), lalu uji SEMANTIK label objeknya (AP = pasangan presisi BENAR/SALAH di caption; VC = kelas K1..K8; WARISAN = tepat 1 entri dan id-nya berkas yang sama dengan yang dihitung LEGACY). Jumlah cocok tanpa uji semantik tidak membuktikan frasa komposisi benar.
4. Klaim pin manifest (sha16 + byte) diukur ulang bersamaan karena murah dan mengunci bahwa census dihitung dari berkas yang sama dengan yang dipin objek.

Turunan positif terbukti sah di giliran ini: delta body terhadap CADANGAN PRA-REVISI (bukan pra-custodian)
dengan multiset token angka memberi bukti "nol angka teknik berubah" yang murah dan tajam - selisihnya
hanya `{28:-2, 24:+2, 192:-1, 191:+1, 6:+1, 327:+1, 143:+1}` = persis kelima tambalan, tanpa perlu
mengulang sampling 90 needle.

## Guard milik verifier: jangan pakai indeks tuple sebagai boolean

Skrift guard pertamaku memakai `chk('md5 body tetap', mm[0] is not None and ...)` padahal `mm` hasil
regex-match saya (tuple `(head, fm, tail)`) — `mm[0]` selalu truthy sehingga guard itu tidak mengukur
apa pun; kebetulan bagian `and` keduanya yang benar. Gejala: guard PASS tapi tidak membuktikan apa pun.
Prosedur: setiap guard harus mencetak ANGKA/HASH yang dibandingkan (mis. `hash vs hash`), bukan hanya
boolean. Guard yang tidak mencetak bukti = guard mati.

## Custodian di-dispatch NON-KANBAN tapi warisi HERMES_KANBAN_TASK milik run induk yang masih hidup (custodian 2026-10-09, objek gsp-dd-001-standar-deep-dive-revb)

Dispatch boleh melarang semua tool kanban, tetapi runtime memaksa aksi terminal bila env `HERMES_KANBAN_TASK` menunjuk kartu yang sedang jalan. Kejadian nyata: task_id = t_23320f06 milik **gsp-librarian run 5729** (`status=running`, `ended_at=None`, PID hidup), sedangkan vonis saya = `perlu_revisi` dan entri wiki BELUM ada (sweep 865 berkas wiki = nol hit). Yang salah: `kanban_complete` (mengklaim deliverable promosi yang tidak ada di disk + merampas transisi agen lain) dan diam tanpa aksi (pelanggaran protokol). Jalur sah terbukti diterima kernel:
1. Tulis verdict ke frontmatter objek seperti biasa (itu satu-satunya deliverable).
2. `kanban_comment` laporan verdict lengkap ke kartu induk (tabel angka ukur + Zis + bukti suntingan) — komentar tidak mengubah state, jadi aman untuk kartu milik agen lain.
3. `kanban_block(kind="needs_input")` dengan reason yang memuat verdict + daftar prasyarat promosi + rujukan nomor komentar. Block menutup run aktif secara sah dan membangunkan orkestrator; ia BUKAN klaim selesai.
Bukti pendukung yang wajib dikumpulkan sebelum memilih: baca tabel `task_runs`/`tasks` di DB papan ASLI (bukan `~/.hermes/kanban.db` kosong — DB papan nyata di `AppData/Local/hermes/kanban.db`, tabel `task_events`/`task_runs` bukan `events`) untuk memastikan profil pemilik run != profil saya, dan cek keberadaan artefak hilir di disk. Kalau pemilik run ternyata SUDAH mati/reclaimed dan vonis = terverifikasi, baru `kanban_complete` sah.

## Verdict ulang iterasi-N: tiga cacat verifier yang terbukti (custodian 2026-09-24, objek networking-korpus-ekas-0923 iterasi 2/3)

Giliran re-verifikasi (bukan audit 7 dimensi ulang) punya kelas false-FAIL sendiri, semuanya dari
skrip verifier, bukan dari data penulis:

1. **Label hunk difflib != format GNU diff.** `SequenceMatcher.get_opcodes()` yang diformat
   `"%dc%d,%d"` menghasilkan `74c79,79` sedangkan `diff` nyata mencetak `74c79`. Bila kartu/kontrak
   mencantumkan hunk expectation bentuk GNU, bandingkan dengan rentang yang sama-sama dipangkas
   (`a==b -> tanpa ",b"`), atau pakai `diff` asli sebagai alat ukur. Versi pertama saya FAIL pada
   CHECK regresi hanya karena perbedaan label ini.
2. **Uji negatif "bentuk lama hilang" wajib menyasar GRUP BODY, bukan seluruh berkas.** Saat verdict
   lama dipindah UTUH ke `riwayat-catatan-verifikasi`, string salah lama (`:58-62`, "jumlah hal tidak
   dilaporkan studi") memang WAJIB tetap ada di frontmatter sebagai jejak temuan. `needle in whole_file`
   menghasilkan FAIL palsu pada dua CHECK sekaligus. Pisahkan fm/body dengan regex delimiter penutup dan
   uji pada body.
3. **Guard bentuk suntingan verdict: satu ganti-baris + satu tambah-baris = 1 minus + 2 PLUS** pada
   unified diff (baris status muncul sebagai `-status: usulan` DAN `+status: terverifikasi`), bukan 1+1.
   Run pertama menulis benar tetapi guard lama menolak; pemulihan dari backup (cek md5) + koreksi guard
   = healing 1 loop sah. Ekspektasi benar: `changed == ["-status: usulan"]`, `added[0] == "+status: <verdict>"`,
   `added[1].startswith('+catatan_verifikasi: "')`, dan `LF_total` naik tepat 1.

Tambahan positif terukur: klaim batas-waktu di body bisa diuji dua arah — angka "saat ekstraksi"
(tidak akan pernah cocok lagi, sah) DAN angka "kini" yang dideklarasikan (WAJIB cocok dengan
`wc -l` hari ini). Deklarasi T-4 di objek ini lolos kedua-duanya.

## Dua false-FAIL kelas kesalahan alamat tambahan + sesi kembar yang menulis verdict sebelum kita (custodian 2026-09-24, objek thermal-korpus-ekas-0923 iterasi-3)

Dua cacat checker saya sendiri pada uji "alamat lama harus hilang", keduanya menghasilkan FAIL
palsu atas data penulis yang sah:
1. **Koinserdensi alamat.** Menandai `:431-432` sebagai "sisa alamat lama" karena CHECK6 lama
   memakai angka itu untuk sasaran yang salah. Padahal objek juga memakai `:431-432` untuk butir
   LAIN yang memang hidup di baris itu (emisivitas). Alamat adalah pasangan (berkas, baris, BUTIR):
   vonis per kemunculan dengan membaca konteks butirnya, bukan per string angka.
2. **Alamat bentuk kolom tabel.** Daftar remap sering ditulis di kolom `| Baris |` sebagai
   `| 451-453 |` TANPA titik-dua. Menguji `":451-453" in body` memberi FAIL palsu walau koreksinya
   terpasang. Uji dua bentuk: `:NNN` dan `\|\s*NNN(-NNN)?\s*\|`.
Turunan: needle pembanding rak wajib dash-agnostic (`1\D{1,2}3`) karena rak memakai U+2013 sementara
objek menormalkan ke ASCII sesuai deklarasi tipografinya - dash ASCII vs en dash = normalisasi
terdeklarasi, bukan cacat.

Sesi kembar juga terjadi di objek yang SAMA pada giliran re-verifikasi: run paralel menulis verdict
(20:13:55) setelah saya mencadangkan state pra-verdict (20:10:02) tetapi sebelum suntingan saya.
Cara tutup yang benar dan terbukti: JANGAN menimpa; buktikan pasangan backup/kini dengan tiga angka
(md5 body identik, diff frontmatter = tepat 4 baris, diff body = 0 baris, satu `^status:`, nol kunci
duplikat), audit silang klaim catatan sesi lain dengan ukur sendiri (11/12 cocok; yang 1 GAGAL
ternyata needle verifier), lalu tulis `LAPORAN-verdict-konfirmasi-*.md` berisi CONFIRMASI + temuan
minor. Cadangan fisik state pra-verdict milikmu tetap artefak penting: ia yang membuktikan body tidak
tersentuh, dan ia yang membuat residu alamat lama dapat dihitung ulang.

## Verifikasi register turunan (TSV/CSV) terhadap JSONL sumber + klaim keberadaan isi (custodian 2026-09-27, objek harga-dems-0927)

1. **Serialisasi str(None).** Berkas timbangan turunan bisa membawa literal `None` di puluhan sel
   (null JSONL -> `str(None)`). Sampel identik-MENTAH gagal palsu karenanya. Prosedur: bandingkan dua
   lapis — (i) mentah untuk laporan fidelity, (ii) ternormalisasi (null/''/float-str equivalence) untuk
   vonis "tidak ada edit konten". Bedakan kelas: sel `None` = cacat serialisasi (perlu_revisi ringan),
   beda nilai = cacat konten (potensi ditolak).
2. **Klaim keberadaan baris wajib diuji per-baris, bukan dari pembilang.** Objek bisa benar di semua
   agregat (243+13 cocok dari JSONL) tetapi salah menyatakan "13 baris identitas ikut di TSV" padahal
   TSV berisi 243 saja. Cek tripel (lane, code, source_url) atau kunci ternormalisasi SETIAP baris yang
   diklaim ada; pembilang yang cocok tidak membuktikan isi berkas pendamping.
3. **Tabel min/max per kelompok punya basis tersembunyi.** Klaim "harga terendah" cocok hanya pada satu
   basis (mis. price_list bila terisi, selainnya price_sale; BUKAN min kedua kolom). Sebelum menuduh
   selisih, coba beberapa basis dan sadari konvensi angka: IDR memakai titik ribuan (`IDR 750.000`
   terbaca 750.0 oleh parser naif), USD memakai koma ribuan. Vonis selisih sah hanya bila semua basis
   dan konvensi sudah dicoba.
4. **Kandidat PII di kolom URL = false-positive.** Regex telepon bisa menangkap digit dalam slug URL
    marketplace; vonis per kolom tempat hit muncul sebelum melaporkan kebocoran kontak.
5. **Sel harga berformat campuran + pembulatan tampil (custodian 2026-09-27 iterasi-2, harga-dems-0927).**
    Parser naif `min(semua angka dalam sel)` GAGAL pada 8/66 entri tabel yang sebenarnya BENAR: sel bertier
    `CNY 1290.00 (1-17 units); CNY 1280.00 (>=18 units)` membuat min = angka tier kedua (terbalik), dan
    prefix mata uang dalam sel (`CNY 600.00`) menambah token. Aturan: ambil angka PERTAMA sel terpilih
    (batas bawah hanya bila sel fullmatch pola `a-b` murni), strip prefix mata uang, IDR strip semua
    titik/koma. Kedua: kolom tabel bisa MEMBULATKAN ke integer (USD 270 = 269.95; CNY 217 = 216.96) —
    pakai toleransi <=0.51 sebelum menuduh selisih. Vonis FAIL sah hanya setelah basis deklaratif objek
    DAN varian first-number diuji. Uji multiset v-vs-v1: bandingkan lapis ternormalisasi; beda mentah
    yang seluruhnya `None` vs kosong = kelas serialisasi, bukan perubahan angka.

## Verification (sebelum klaim selesai)

- [ ] Setiap proposa di vault berstatus `usulan` telah dinilai (terverifikasi/
      perlu_revisi/ditolak) dengan `catatan_verifikasi`
- [ ] Sampling anti-karangan: minimal 2 file sumber dibuka & cocok
- [ ] Tidak ada proposa yang kamu tulis sendiri dalam batch verifikasi ini
- [ ] Tidak ada satu pun vault_promote.py yang kamu jalankan
- [ ] Laporan STATUS: complete + angka per verdict

<!-- Riwayat: 1.0.1 (11-10-2026, DUPSKILL-L3 t_605e5f7c) diserap dari salinan fisik profil gsp-custodian: pitfall YAML key `status:` ganda + generator `halaman: -`, seksi rekalkulasi angka (3 jebakan), hitung baris spreadsheet fisik vs data, parser diam-diam menjatuhkan baris (total +527 baris, nol baris fleet dibuang). -->
