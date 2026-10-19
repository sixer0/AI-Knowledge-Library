# Rantai remediasi multi-ronde pasca-VERIF RBAC (kelas misi registrasi knowledge EKAS)

Preseden: CVLK-0929 (29-30/09, domain CIVIL/CONSTRUCTION/BUILDING/GROUNDING/DRAWING-CAD),
menambah `remediation-chain-after-verifier-fail.md` (RAFIF) dan `knowledge-register-multi-domain.md`.
Berlaku untuk kelas misi: studi rak -> objek vault -> custodian -> promote -> rute memori ->
VERIF undian 3/8 -> laporan home channel (VSSKB/NWSKILL/SDCY/CVLK).

## Aturan yang terbukti (nomor = Decision Log CVLK)

1. **D-14 — Rantai hasil studi WAJIB diterbitkan ke folder domain SEBELUM dispatch VERIF.**
   Akun menjawab dari folder `ekas/05_DOMAIN-KNOWLEDGE/<domain>/` + indeks rute memori, BUKAN
   dari objek vault. Rantai yang hanya hidup di objek = akun menjawab benar "RANTAI BELUM ADA"
   dan vonis FAIL yang sah atas cacat hulu kita. Resep penerbitan (kartu FIX/L1b): salin
   VERBATIM dari bagian rantai objek (uji kecocokan baris x/y), kepala berkas memuat pointer
   "objek kanonik + sha" + catatan "terbit pasca-VERIF sebagai jalur aktivasi"; baris asli rak
   tidak diubah. Preseden C1 (penanda known-defek KD-C9 ditempel, baris asli utuh) untuk rak
   yang sudah punya rantai cacat.

2. **D-15 — Leksikon/predikat ground-truth disusun dari teks domain itu sendiri.**
   Mengwarisi predikat domain sebelumnya (contoh: leksikon konsekuensi sipil
   "larang klaim lulus / non-selamat") menghasilkan FAIL yang tidak bisa dipulihkan akun mana
   pun karena frasanya 0 hit di teks domain uji (grep dulu, bekukan GT setelah grep). Vonis
   kelas ini = CAPPED-with-evidence (permohonan putusan controller), bukan FAIL produk.
   Putusan sah: selaraskan GT + delta leksikon tercatat dengan syarat (a) fixture merah wajib
   bertahan (angka telanjang, atribusi palsu ke artefak rak, klaim "utuh" tanpa negasi),
   (b) replikasi identitas vonis lama tidak bergeser, (c) selftest hijau sebelum vonis resmi.

3. **Pemulihan per-butir dengan carry-over (resep R4).** Ronde lanjutan mengulang HANYA sel
   gagal; akun lain PASS carry-over dari transkrip ronde sebelumnya (tidak di-dispatch ulang);
   instrumen beku dengan sha pra==sesudah dicatat. Undian TIDAK pernah diulang antar-ronde.

4. **Kelas jawaban sah yang harus dikenal leksikon penolakan:** angka proyek internal
   berlabel "indikatif + sumber tertelusur + bukan AHSP" = SAH mengikuti aturan rak sendiri
   (ASSUMPTION/PROJECT-DERIVED). Yang FAIL: angka telanjang tanpa label, atau angka dengan
   atribusi ke artefak rak yang tidak memuatnya (fabrikasi provenance — kelas gsp-master Q2 C1:
   "buku R3 menyebut 17 MPa" padahal grep 0 hit di seluruh ekas/+vault; controller WAJIB ukur
   ulang grep sendiri sebelum menyahkan vonis verifier).

5. **Cacat akun (T1) -> FIXB: akun yang bersangkutan membaca rak lalu menyematkan aturan ke
   memorinya sendiri** (tool memory, ikut tiering profil), bukan orang lain menuliskannya.
   Gerbang: grep token aturan di MEMORY.md profil >= 1 + ukuran sebelum/sesudah.

6. **D-18 — Pool undian = query hidup tabel WebUiUser** (select username, role,
   hermesProfile via PrismaClient di gsp-datacenter), BUKAN daftar statis. Nama pensiun
   (gsp-budi, novriandy, user01) tanpa home profil. Draw yang menyentuh nama mati boleh
   di-VOID selama belum ada probe yang terlanjur jalan; bekukan kedua draw + alasan void dalam
   satu berkas undian.

7. **D-20 — Drift bentuk baris rute memori.** Sesi anak dapat mengonsolidasi memori dan
   merusak bentuk beku kontrak (terukur: baris 417 char vs cap 150; konten benar, kontrak
   salah). JANGAN sunting diam-diam: gunakan klausul koreksi terbuka blueprint (K-2 "penambahan
   penanda = putusan controller dengan kartu revisi tersendiri"), revisi konstanta TERDOKUMENTASI
   + moda `--replace-existing` di skrip rollout (hanya baris ber-token domain itu; backup
   manifest), lalu ukur distribusi grep independen: devian >cap = 0 di semua berkas.

8. **D-23 — AGENTS.md (berkas instruksi agen) adalah gerbang manusia.** Guard menulis menolak
   dengan "silence is not consent" bahkan saat prompt approval muncul tanpa jawaban — dua agen
   membentur guard yang sama; ini perilaku benar, bukan kegagalan kerja. Jalur sah: controller
   eskalasi via dua-kanal (clarify di chat + komentar kartu), jawaban user tercatat menutup
   kanal, lalu controller memasang diff yang BYTE-IDENTIK dengan kandidat yang sudah divonis
   sah (verifikasi `cmp` + sha), tutup kartu dengan jejak itu. Jangan coba bypass terminal.

9. **Scanner naturalisasi untuk naskah home channel (kanal tunduk).** Kegagalan nyata dan fix:
   - C-8b "pengakuan batasan" menuntut TOKEN leksikon literal (`keterbatasan`/`batasan`/
     `asumsi`/`risiko`/`belum terverifikasi`...) — kata "Batas" tidak dihitung; pakai
     "Keterbatasan yang diakui:".
   - C-5: label seksi yang di-italic ≤2 dan 0 untuk produk/standar — buang italic pada label
     seperti `_Angka rilis terverifikasi:_`.
   - C-12 gaya catatan cepat: panah ASCII pengganti kata DAN rantai titik-koma antar-fragmen
     = 2 sinyal = FAIL; tulis prosa kalimat penuh ("melalui jalur vault, wiki, ...").
   Jalankan scanner sampai VERDICT PASS SEBELUM `hermes send`; vonis FAIL scanner menahan kirim.

10. **Kanonik frontmatter objek vault = 18 kunci** (ukur diff antar-objek, bukan angka kartu
    lama "21" yang longgar). Guard promote wajib menolak <18/18; kunci `catatan_verifikasi`
    domain custodian, boleh absen di L1.

11. **Mekanika:** `lad_card.py` tidak menerima `--json` — ambil id dengan
    `grep -oE 't_[0-9a-f]{8}' | head -1`. `hermes kanban complete` pada kartu yang sudah
    terminal = ditolak kernel (bukan kegagalan kerja); komentar temuan tetap masuk.

## Kerangka kartu VS-ronde-ulang (tempel di badan)
Cek premis FIX (grep/cetak) -> dispatch ulang hanya sel gagal (verbatim pertanyaan, sesi baru,
dir raw-rN terpisah, jangan menimpa run lama) -> instrumen beku sha pra==sesudah -> vonis
per-CHECK + tabel DELTA ronde-lama->baru -> gerbang PASS hanya 3/3 akun x 3/3 butir run bersih
-> gagal lagi dengan jalur baca benar = CAPPED-with-evidence, bukan FAIL diam-diam.
