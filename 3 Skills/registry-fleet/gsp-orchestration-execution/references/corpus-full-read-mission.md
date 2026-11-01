# Misi Baca-Penuh Korpus (corpus full read + resume pengetahuan)

Kelas misi: "baca SEMUA berkas folder X baris per baris tanpa terlewat, lalu buat resume
pengetahuan" (preseden misi baca korpus 1003, 03-10; preseden internal misi pemahaman korpus 0925).
Controller TIDAK membaca sendiri seluruh korpus (context blow-up); pembacaan per-baris
didelegasi sebagai kartu fan-out, controller melakukan AUDIT INDEPENDEN + sintesis.

## Anatomi kartu pekerja (WAJIB di body)

1. Lingkup eksplisit per kartu (subtree folder), path output UNIK (`work/wN_<slug>.md`).
2. Aturan keterbacaan per berkas: teks = baca penuh; JSON/CSV besar = parser semantik
   (schema, jumlah record, field kunci, agregat) = sah sebagai "baca penuh semantik";
   biner tanpa sidecar = catat nama/ukuran/tanggal/sha dari ledger + tandai
   BINER-MURNI-TIDAK-DIBACA (tercatat, bukan gagal).
3. Sidecar `.md` extracted dihitung sebagai jalur baca utama untuk xlsx/docx/pdf.
4. MANIFEST penutup: daftar berkas lingkup (enumerasi disk) vs daftar terbaca, SELISIH
   HARUS NOL; angka nyata disk mengalahkan perkiraan di kartu (pekerja wajib mencatat
   selisih lingkup-kartu-vs-disk, bukan diam-diam menyesuaikan).
5. Digest per berkas: path, baris/byte nyata, md5, struktur seksi, SEMUA angka kunci
   verbatim, keputusan, anomali, status keterbacaan.
6. LIMIT-AWARE cap 150; `STATUS: partial-handoff` + SISA_KERJA path persis sah -> resume
   card dengan parents=[asal].

## Audit independen controller (sebelum klaim L2)

JANGAN trusts manifest pekerja buta-buta; jalankan alat sendiri:

1. **Ledger-sidik audit**: bandingkan `Sidik_Berkas.csv` (atau setara) vs disk dengan
   hash MD5 dihitung ulang. NORMALISASI nama wajib: migrasi ALUR mengganti spasi ->
   underscore dan melepas karakter `[]()~$` (mis. `[REN]` -> `__REN__`, `(Public)`
   dilepas). Preseden: 282 baris ledger vs disk = 278 MD5 SAMA, 0 BEDA, 4 tersanitasi-
   nama; tanpa normalisasi, hasil palsu "242 HILANG".
2. **Sensus cakupan**: `find <subtree> -type f | wc -l` per lajur vs angka manifest
   pekerja; rekonsiliasi selisih (kartu salah hitung vs berkas hilang harus dibedakan).
3. **Uji tandingan angka klaim**: recompute minimal 3-5 angka kunci digest dari sumber
   primer (bukan dari digest). Preseden baik: residu T6b "<nilai uang>" terverifikasi persis;
   C2PA 11/11 SVG terverifikasi. Preseden cacat: klaim W2 "144 penanda DISEPAKATI
   11/12/2025" TIDAK terverifikasi -> angka flag, JANGAN diwariskan ke resume.
4. **Hash artefak keadaan-terakhir** di luar folder (objek rilis/vonis) dicocokkan ke
   vonis resmi sebelum dikutip sebagai "keadaan terakhir".

## Pitfall ekstraksi PDF untuk verifikasi klaim pekerja

- Jumlah BARIS/KARAKTER dump PDF bergantung ekstraktor: pypdf vs pdfminer pada berkas
  sama memberi 4.632 vs 7.591 baris. Angka semacam itu dari pekerja TIDAK dapat
  direplikasi lintas-alat -> jangan vonis "salah" hanya karena beda; verifikasi lewat
  PENANDA KONTEN (hitung substring, judul pasal, tanggal harmonisasi) dengan
  normalisasi whitespace `re.sub(r"\s+"," ",txt.lower())`.
- Jalur ukur: `uv run --with pypdf python - <<'EOF'` atau `--with pdfminer.six`
  (python Store alias -> selalu uv run; sudah di #pitfall-mesin).
- Klaim tanggal penanda bisa keliru karena format campuran dalam satu dokumen
  (8/12/2025, 11/12/2025, 3/2/2026 dalam satu RPP) - sensus harus per-varian, bukan
  total satu frasa.

## Mekanika papan (terukur 03-10)

- `hermes kanban --board default dispatch` lokal mengklaim SEMUA kartu ready serentak
  (Spawned: 7 saat norma kap 5/misi) - kap adalah norma gelombang promosi, bukan
  hard-gate dispatcher lokal; pantau, jangan pasang edge semu untuk menahannya.
- Kartu `done` TANPA field result terisi (result di run, bukan di task JSON): baca
  `show --json` -> runs[].result, dan andalkan artefak disk (digest file) sebagai
  objek verifikasi utama.
- Worker yang menulis parsah `_wN_part*.md` sebelum final: cek apakah final `wN_*.md`
  muncul di path yang ditugaskan sebelum vonis selesai.

## Kerangka resume pengetahuan (output akhir ke user)

Struktur terbukti (Laporan_Pemahaman 27-IX + resume misi baca korpus): inti proyek -> para
pihak/format -> dasar hukum -> baseline historis -> riwayat iterasi -> lanjutan
pasca-beku -> arsitektur keadaan akhir -> rantai anggaran -> keputusan terbuka ->
risiko/cacat -> vonis pemahaman. Setiap angka dari cetakan alat giliran ukur; temuan
digest yang gagal uji tandingan dicatat sebagai keterbatasan, tidak diwariskan.
Kanal user: gerbang naturalisasi wajib (draft -> naturalisasi -> scan -> serahkan).
