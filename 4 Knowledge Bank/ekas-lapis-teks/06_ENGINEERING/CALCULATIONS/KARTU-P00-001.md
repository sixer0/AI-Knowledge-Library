> # ⚠ CONTOH — BUKAN PEKERJAAN NYATA
>
> Kode proyek **`P00` dicadangkan untuk contoh**. Proyek sungguhan memakai `P25`, `P26`,
> dan seterusnya. **Seluruh angka di berkas ini karangan** untuk menguji perangkat gate —
> jangan disalin ke dokumen pelanggan.

# Kartu Kendali Rantai — KARTU-P00-001

Templat `TPL-00` · Rantai **A** — serat optik

```
════════════════════════════════════════════════════════════════
KARTU KENDALI RANTAI JAMINAN                    No. P00-001
Proyek     : P00 (contoh)
Rantai     : ☑A serat  ☐B video  ☐C daya  ☐D bumi
             ☐E isolasi ☐F termal ☐G keandalan ☐H simpan
════════════════════════════════════════════════════════════════

BESARAN    : Ambang rugi sisipan maksimum per core
NILAI      : 6,40 dB (1310 nm) · 5,96 dB (1550 nm)

──── ① RUJUKAN ────────────────────────────────────────────────
Tingkat    : ☐R1 regulasi  ☑R2 standar  ☑R3 buku
             ☐R4 pabrikan  ☐R5 sekunder
Judul      : Hayes, FOA Reference Guide [R3] · IEC 61280-4-2 [R2]
Halaman    : PDF 129, 145 · PDF 17     Tahun terbit : 2019 · 2014
Peringatan usia (>15 th)?   ☑ tidak  ☐ ya

──── ② KEPUTUSAN DESAIN ───────────────────────────────────────
Yang ditetapkan      : 6 sambungan fusi (gulungan 500 m)
Alternatif ditolak   : 3 sambungan (waktu tunggu 8 minggu)
                       10 sambungan (+1,2 dB, 4 titik gangguan)
Alasan penolakan     : jadwal · anggaran rugi tanpa alasan

──── ③ PERHITUNGAN ────────────────────────────────────────────
Rumus      : rugi = (km × dB/km) + (n_kon × 0,75) + (n_sam × rugi)
Sumber rumus         : [R3] REF-FO-001 hal. PDF 129
Masukan    :
   panjang 3,2 km      = 3,2      [R--]  ☑ terukur ☐ asumsi
   rugi konektor       = 0,75 dB  [R3]   ☑ terukur ☐ asumsi
   rugi sambungan      = 0,30 dB  [----] ☐ terukur ☑ ASUMSI
Hasil      : 6,40 dB
Kepekaan   : 0,15 dB → 5,50 dB · 0,45 dB → 7,30 dB

──── ④ PENGUJIAN ──────────────────────────────────────────────
Metode     : dua ujung, one-cord reference
Sumber metode        : [R2] IEC 61280-4-2 hal. PDF 17
Alat       : merek/tipe OLTS ......  no. seri ...............
             kalibrasi berlaku s.d. ..........
AMBANG     : 6,40 dB @1310 · 5,96 dB @1550
Sumber ambang        : hitungan CALC-P00-001 (metode [R3])
   ⚠ Bila sumber ambang = R3, apakah diadopsi kontrak?
     ☑ ya, pasal 7.3   ☐ belum → RANTAI PUTUS
Penyaksi   : ..................................

──── ⑤ BUKTI SERAH ────────────────────────────────────────────
Berita acara no.     : BA-P00-FO-001
Lampiran   : ☑ hasil ukur   ☑ rekaman alat   ☐ citra
             ☑ sertifikat kalibrasi          ☑ perhitungan
             ☐ surat pabrikan [R4]           ☑ rugi kabel referensi

════════════════════════════════════════════════════════════════
STATUS RANTAI
  ☐ UTUH — kelima mata terisi, ambang bersumber sah
  ☐ MENUNGGU R4 — sah; surat pabrikan sudah diminta tgl ......
  ☐ MENUNGGU PENETAPAN PEMILIK — surat permintaan tgl ........
  ☑ PUTUS di mata ③  — alasan: rugi_sambungan masih ASUMSI dan
                        CALC belum diperiksa orang kedua (G3)

Disusun ......................  Diperiksa ....................
Tanggal ......................  Tanggal ......................
════════════════════════════════════════════════════════════════
```

> **Kartu ini sengaja ditutup dengan status PUTUS.** Menjalankan contoh sampai "semua
> centang hijau" tidak akan mengungkap apa pun. Yang berguna justru melihat bagaimana gate
> yang belum terpenuhi **terlihat** — dan bahwa pekerjaan tetap boleh berjalan asalkan
> statusnya tertulis.

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-2: ambang 5,96 dB @1550 yang dikutip di lapis ini TIDAK reproducible dari masukan CALC-P00-001.md:31-36. Alpha tersirat 5,96 tepat = 0,3625 dB/km (tidak muncul di FOA/rantai/katalog/kartu); kandidat rak memberi 5,60 dB (a=0,25), 5,76 dB (a=0,3), 6,40 dB (a=0,5); brute force 1.120 kombinasi menuntut n_sambungan 8/10 (bertentangan n=6 di DDR-P00-001.md:19) atau rugi konektor 0,5/1,0 (bukan 0,75). Rincian uji: register Bagian 2.3 dan K-2. Induk anotasi: CALC-P00-001.md:48. Nilai P00 berlabel 'angka karangan' (contoh); tidak ada dokumen serah nyata yang tercemar. Keputusan koreksi (5,76 / 6,40 / catatan ilustrasi-tanpa-rincian) milik controller-manusia.
