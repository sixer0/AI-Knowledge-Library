# Pelajaran Misi GAYA-AHLI-1005 (untuk gerbang naturalisasi & verifikasi)

Draf closeout kartu `t_3a3bf011` (06-10-2026). Sumber bukti: folder kontrak
`workspace/gsp-hermes/workspace/docs/2026-10-05-gaya-bahasa-forensik/`
(CONTRACT.md decision log D-16..D-22, work/f2_vonis-lepas.md Seksi 7,
work/revg-notes.md, work/remediasi-notes.md, work/kal2_gate_report_final.txt).
Empat pelajaran yang tergeneralisasi di luar misi ini:

## 1. Kanal resmi 'standar' untuk naskah standar (scanner v1.10.0)

Naskah bergenre standar/aturan (badan aturan + kutipan verbatim + identifier
kebijakan) tidak boleh divonis lewat kanal `doc`/`kitab` yang dirancang untuk
prosa biasa: fail-setnya didominasi indikator struktural-genre (C-6 plafon
panjang kalimat, C-7 sebaran panjang paragraf, C-8 kerapatan tebal, agregat
D-TA-09) yang merupakan known-defect desain kanal untuk genre ini, bukan cacat
naskah. Putusan t_eec55819 menetapkan kanal `standar` (v1.10.0) sebagai kanal
resmi naskah standar: C-13 identifier keras turun ke INFO untuk kode
kebijakan/standar (target <=2 keras), blok kutipan dikecualikan via mekanisme
D18, kontrol regresi kanal lama byte-identik (66 fixture + 9 korpus).
Konsekuensi penegakan: SOUL/profil yang menagih "scanner v1.9.1+ pada kanal
yang sesuai" wajib memakai `--channel standar` untuk naskah standar; memanggil
kanal doc pada berkas standar lalu memaknai FAIL sebagai cacat naskah = salah
instrumen. Pemanggilan sah: argumen posisi berkas TANPA `--text -` (akar
F-25-1: mode stdin mengubah skop metrik).

## 2. Pola worker-mati-setelah-artefak (D-16)

Tiga worker misi mati tepat setelah isi artefak tersimpan karena limit bridge
1800s saat verifikasi internal masih berjalan. Respons controller yang terbukti
benar: ukur sendiri artefak dengan parser independen lalu force-done
ber-bukti; JANGAN restart kerja dari nol (menimpa artefak = preseden buruk).
Mitigasi turun-temurun untuk kartu rakit/penulisan berat: `max_runtime_seconds`
naik (3600), short check diminta di AWAL kerja bukan di akhir, dan artefak
kunci ditulis ke disk sebelum verifikasi panjang dimulai supaya kematian worker
tidak menghapus bukti.

## 3. Pin komentar vs artefak hidup

Rebuild artefak tanpa memperbarui pin sha di komentar pengalihan menghasilkan
dua pointer sah yang saling bertentangan (kasus nyata: komentar pin build-1
979e528f/46.729 B vs disk build-2 2cba703b/52.788 B; verifier membenturkan
keduanya dan countersign gagal-jujur). Aturan turun-temurun: pen-pin-an sah =
result kartu TERAKHIR; setiap rebuild wajib menulis ulang pin di result DAN
komentar pengalihan diperbarui atau dinyatakan batal. Pin era juga perlu
ledger: sha manual yang sama boleh berganti nilai karena suntingan metadata
sah antar-era (revE-atap-SOUL 5d449eee vs revE-arsip-REM 6188479a, selisih
tepat -3 B sinkron frontmatter) - dibukukan supaya nama era tidak ambigu,
bukan salah siapa pun.

## 4. Reshoot-sempit dua juri

Setelah revisi bernama non-gaya (backtick identifier, penanda blok, perbaikan
tense), tidak perlu menilai ulang seluruh dokumen: juri dua-arah menilai HANYA
zona yang tersentuh suntingan (hash zona per-heading membuktikan zona mana
yang berubah; zona tak tersentuh membawa skor sebelumnya - aplikasi konsisten
putusan D-21). Syarat bawaan: uji-balik byte per-lokus (nol perubahan prosa di
luar lokus bernama), dua juri independen buta arah, dan nol selisih skor >=2.
Hasil preseden: 16/16 LULUS-LEPAS rata 4,00 x4 atas revF sebelum revG terbit.
