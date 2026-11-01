# Countersign atas kartu VERIFIER + guard notifikasi replay (PSIKOTES-1008 + BUKUV3-MAP/ING-1009, 09-10-2026)

Kelas baru yang belum tercakup resep countersign lama: kartu yang menutup adalah **verifier independen** (V menvonis penulis L1+L2). Controller tidak mengulang verifikasi penuh (itu membuat V tidak independen lagi dan membakar giliran); yang diverifikasi adalah **V-nya**.

## Countersign-of-verifier (5 langkah, terukur murah)
1. **Countersign hash yang diklaim V**, bukan angka narasinya: `sha256sum` berkas yang V sebut kanonik/non-kanonik di laporannya; cocok-byte = penetapan objek uji V benar. (Kasus: 3aea8d43/61f0c892.)
2. **Determinisme tanpa mererun instrumen berat**: bandingkan dua cetakan run V (`cmp run1 run2`) DAN hash artefak hidup == sha yang divonis era sebelumnya. Dua run identik + sha hidup tak berubah = rebuild deterministik terbukti.
3. **Instrumen V harus tulis-ulang sendiri**: sensus folder `verification/` (jumlah skrip, ukuran), cek seed tercatat BERBEDA dari seed pekerja (anti-kelulusan-kebetulan; kasus seed 3309 vs 1009).
4. **Uji ulang satu kelas angka dengan alat sendiri** (bukan semua): sensus independen 1-2 populasi kunci (walk staging, decode ulang tree, hitung prefiks kartu) yang harus konvergen ke angka V.
5. **Temuan minor V yang menunjuk hulu controller**: akui SPESIFIK sebagai cacat pencatatan controller (kelas T5 sendiri), bebankan ke kartu rekonsiliasi hilir lewat jejak, jangan dibantah.

## Guard replay notifikasi (W1b, dua notifikasi kartu sama)
Sebelum memvonis ulang notifikasi "completed": (a) `show --json` -> baca `comments`, cari marker vonis sendiri ("VONIS PENGAWAS"); (b) hash ulang artefak kunci, bandingkan dengan sha vonis lama. Keduanya sama = REDelivery: laporkan replay, TIDAK menulis vonis kedua, TIDAK membuat kartu. (Preseden memori 08-10: notifikasi 'completed' bisa basi; kini ada resep guard dua-cek.)

## Fallback jejak saat gerbang persetujuan sesi memblokir tool call
Blok bertipe "execute_code timed out without user response" pada jalur komentar kanban: JANGAN retry, JANGAN tool lain untuk efek sama. Jalur sah: tulis jejak vonis LENGKAP ke contract.md misi (kanal sah, bukan komentar antar-agen), dan DISKELIRKAN pemblokiran mekanis itu di dalam jejak (vonis bertumpu ukur disk, bukan pada komentar). Terjadi 2x pada kartu W2; kontrak tetap auditabel.

## Patch berkas instruksi terproteksi (AGENTS.md) - pola dua-aktor
Worker sesi headless yang kena gerbang proteksi berkas instruksi: berhenti, tulis `output/<KARTU>_AGENTS-PATCH.md` berisi blok OLD dan NEW siap-tempel, deklarasikan di result (jalur benar, bukan menyelinap). Controller pemegang hak menempelkan hanya setelah persetujuan pemilik tercatat, dan SETELAH cek keunikan: hitung kemunculan OLD == 1 -> ganti -> verifikasi pasca: OLD tersisa 0, NEW == 1, ukuran berkas dilaporkan. Trap formulasi: klaim "lapisan teks N file" bisa berarti .md-saja atau semua berkas teks; sensus ekstensi (md/csv/py, nol biner) sebelum menerima atau membantah angka.

## Insiden koreksi-diri pengawas (dokumentasi dua arah)
- **Baca cetakan red-green sebagai vonis artefak hidup** (kasus l29-redgreen-m1/m2): FAIL di berkas MERAH yang disuntik (hapus/ganda baris) adalah bukti detektor menggigit, BUKAN cacat paket. Prosedur: cek label varian di header cetakan, lalu jalankan checker HIJAU pada berkas hidup (`verbatim_check` PASS) sebelum menuduh; koreksi-diri lewat jejak terpisah, bukan sunting vonis lama.
- **Probe token berbatas-kata untuk vonis anti-bocor**: grep substring menghasilkan positif-palsu ('bobot' di 'konsisten', 'sten' di 'terdampak', 'ambang' di 'mengambang'): vonis nol token terlarang WAJIB regex `\b<token>\b`; laporkan selisih 6 positif-palsu -> 0 sebagai kejujuran instrumen.

## Field result None saat papan menutup via wake/summary
Terulang (L25, FIX-7, L29): `show --json` membaca `result: None` padahal notifikasi papan membawa ringkasan penutupan sah. Vonis tidak bergantung field result: artefak disk + cetakan alat + komentar pekerja = basis bukti; catat anomali mesin di jejak agar auditor tidak mengira kartu menggantung.

## Steer aturan mengikat ke kartu hilir yang lahir pra-finalisasi blueprint
Bila kartu pekerja dibuat SEBELUM 02_structured final (fast-lane RT/TA), badan kartu bisa tidak memuat aturan mengikat blueprint (grep token aturan = 0 di body). Aksi controller pasca-vonis TA: kirim SATU komentar steer berisi aturan verbatim + kunci sha rev objek uji (anti-audit-salinan-basi), pekerja lanjut tanpa restart. Bila komentar terblokir gerbang sesi: tempel sha objek uji di contract.md sebagai rujukan pengawasan dan terima bahwa mandat SOUL verifier sudah cukup untuk palang sah.
