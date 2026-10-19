# Rantai A — Jalur serat optik

**Ambang terima berasal dari:** hitungan rancangan · metode uji dari **IEC 61280-4-2 [R2]**

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman |
|---|---|---|---|
| Hayes, *FOA Reference Guide* | **R3** | Rumus loss budget, batas rugi komponen | PDF 129, 145 |
| JDSU, *FO Testing Vol 1* | **R3** | OTDR, ketidakpastian ukur | cetak 37 / PDF 44 |
| **IEC 61280-4-2:2014** | **R2** | Empat metode uji SM · RTM · ORL | PDF 14, 17, 20, 43 |
| Lembar data konektor & kabel | **R4** | Redaman & reflektansi produk terpasang | per proyek |

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-3 (baris JDSU pada tabel rujukan di atas): pasokan 'ketidakpastian ukur' atas nama JDSU adalah salah atribusi calon. Angka 0,02-0,05 dB/hari tidak muncul satu pun di resume JDSU (ukur: `grep -c '0,02'` = 0 dan `grep -n 'dB'` = 0 hasil pada `R3 - Reference Guide to Fiber Optic Testing Vol 1.md`); angka itu tinggal di resume FOA `:125-128` dan `:207`. Bentuk tandingan: `R3 - FOA Reference Guide to Fiber Optics.md:125-128`. Vonis final wewenang manusia dengan PDF JDSU Bab 2 (cetak 37 / PDF 44) dan FOA Bab 8 (PDF 98).

---

## ② Keputusan desain

| Yang ditetapkan | Dasar | Alternatif yang ditolak dan alasannya |
|---|---|---|
| Jenis serat (SM/MM, OS/OM) | Jarak + lebar pita + biaya | MM ditolak di atas ~550 m — batas jarak pada laju tinggi |
| Jumlah sambungan & konektor | Tata letak fisik | Menambah konektor mempermudah pemeliharaan tetapi **menambah rugi** — dinyatakan sebagai pertukaran |
| Panjang gelombang uji | 1310 & 1550 nm untuk SM | Uji satu λ ditolak — cacat bending hanya tampak di 1550 |
| Metode uji | **IEC 61280-4-2 / OFSTP-7** | Uji satu ujung ditolak untuk sertifikasi jalur — hanya mengukur satu konektor |

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-1 (baris 'Jenis serat (SM/MM, OS/OM)' pada tabel di atas): '~550 m' adalah angka normatif TANPA penanda sumber [R-n] dan kolom Tingkat/R baris itu kosong. Sapuan 6 kueri atas seluruh korpus (OM1-OM5; '550'; '300 m'; 802.3/BASE-SR/BASE-LX; '[0-9]+ m' di dua berkas FO; JDSU) menghasilkan NOL padanan: tabel OM1-OM5 di `R3 - FOA Reference Guide to Fiber Optics.md:51-55` tidak memuat angka jarak; '550' tiga situs lainnya bukan jarak MM; '300 m' di `DDR-P00-001.md:39` = panjang gulungan gudang. ~550 m menyerupai jarak 10GBASE-SR pada OM3 yang tidak disebut di rak. Beban-rilis: baris itulah yang memutuskan SM vs MM di awal setiap pekerjaan dan ia satu-satunya angka di baris itu. Adjudikasi final: manusia dengan PDF Hayes Bab 5/9 dan TIA-568 (GAP-011).

> Keputusan yang paling menentukan biaya: **jumlah sambungan**. Ia masuk langsung ke
> hitungan mata ③ dan menentukan apakah jalur lulus pada mata ④.

---

## ③ Perhitungan

```
Loss budget = (panjang_km × rugi_per_km) + (n_konektor × rugi_konektor)
                                          + (n_sambungan × rugi_sambungan)
```

| Masukan | Nilai baku | Tingkat |
|---|---|---|
| Rugi serat SM premises | **1,0 dB/km** | R3 — Hayes PDF 129 |
| Rugi serat SM outside plant | **0,5 dB/km** | R3 — Hayes PDF 129 |
| Rugi konektor | **0,75 dB** (batas TIA-568) | R3 — Hayes PDF 129 |
| Rugi sambungan fusi | 0,1–0,3 dB | R3 · **R4 bila alat menyebut lain** |
| Rugi konektor terpasang nyata | — | **R4 wajib** bila dijadikan ambang |

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-5 (baris 'Rugi sambungan fusi' pada tabel di atas): rentang 0,1-0,3 dB hidup HANYA di rantai ini. `KATALOG-RUMUS.md` seksi 2 tidak punya baris rugi sambungan sama sekali (hanya rumus `:121` dan tabel konektor `:131-136`); `ASUMSI-BAKU.md:55` mengarahkan 'spesifikasi pelaksana/batas kontrak' tanpa angka. Satu-satunya angka splice yang pernah dipakai contoh (`CALC-P00-001.md:36`, 0,3 dB) ditag ASSUMPTION, bukan SOURCE-DERIVED. Gap konsistensi antar-lapis: butir hilir cenderung mengambil 0,3 dB sebagai 'angka rak'. Rekomendasi studi: daftarkan 0,1-0,3 dB ke KATALOG seksi 2 dan ASUMSI-BAKU sebagai asumsi baku berpenanda R3+R4.

**Ambang lulus = kolom terburuk (worst case)** — Hayes PDF 145. Bukan nilai rata-rata,
bukan nilai tipikal.

### Contoh terhitung

Jalur OSP 3,2 km · 4 konektor · 6 sambungan fusi:

```
serat      : 3,2 × 0,5   = 1,60 dB
konektor   : 4  × 0,75   = 3,00 dB
sambungan  : 6  × 0,3    = 1,80 dB   (kolom terburuk)
                          ─────────
ambang lulus             = 6,40 dB
```

> **Aturan yang membatalkan hitungan bila dilanggar:** jangan menetapkan toleransi lulus
> lebih ketat daripada ketelitian alat. Ketidakpastian lapangan lebih besar daripada
> laboratorium (0,02–0,05 dB/hari) — ambang "maksimum 0,01 dB" tidak dapat
> dipertanggungjawabkan. [R3, JDSU]

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-3: marker [R3, JDSU] pada kutipan di atas adalah salah atribusi calon. Angka 0,02-0,05 dB/hari tercetak di resume FOA (`R3 - FOA Reference Guide to Fiber Optics.md:125-128`), sedangkan resume JDSU tidak memuat satu pun angka dB. Nilai tidak berubah; yang dicacatkan adalah penanda sumbernya. BELUM TERKONFIRMASI sampai manusia membuka PDF JDSU cetak 37 / PDF 44 dan FOA PDF 98.

---

## ④ Pengujian

| Butir | Ketentuan | Sumber |
|---|---|---|
| **Metode** | Dua ujung — OFSTP-7 (SM) / OFSTP-14 (MM), atau IEC 61280-4-2 | R2/R3 |
| **Pilihan test cord** | one-cord · three-cord · two-cord · OTDR — **sebutkan yang dipakai** | **R2** — IEC 61280-4-2 PDF 17 |
| **Alat wajib** | OLTS/LSPM untuk rugi. **OTDR bukan pengganti** | R3 — Hayes PDF 98 |
| **Kabel referensi** | Diuji FOTP-171; **rugi > 0,5 dB patut dipertanyakan** | R3 |
| **Ambang** | Hasil hitungan mata ③ | — |
| **ORL bila disyaratkan** | Annex E Method A, gelombang kontinu | **R2** — PDF 43 |
| **Bila terjadi selisih** | Metode penyelesai perselisihan = **RTM** | **R2** — PDF 14 |

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-11 (baris 'Alat wajib' dan 'ORL' pada tabel di atas vs baris 'Metode' dan 'Pilihan test cord' pada tabel yang sama): ketegangan antar sumber belum teradjudikasi di rak. Sisi R2: IEC 61280-4-2 PDF 17 mencantumkan metode OTDR sebagai salah satu empat metode uji redaman (`R2 - IEC 61280-4-2.md:30-35`). Sisi R3: FOA mewajibkan LSPM/OLTS dan menyebut OTDR pelengkap bukan pengganti (`R3 - FOA Reference Guide to Fiber Optics.md:106-110`); menyerahkan hasil OTDR saja = kesalahan tersering (catatan 'Kesalahan yang paling sering terjadi di lapangan' di bawah tabel ini). Keduanya bisa benar sekaligus (metode ukur vs bukti rugi sisipan total untuk serah terima), tapi tidak ada berkas yang menuliskan rekonsiliasinya; `AUTHORITY-STATUS.md:36` hanya mengatur 'cara mengukur vs berapa batasnya'. Butir paling berbahaya untuk berita acara: pelaksana bisa mengutip baris IEC untuk menyerahkan hasil OTDR saja. Putusan milik controller-manusia; objek IL wajib menyimpan kedua sisi + aturan pakai (OLTS untuk ambang rugi; OTDR untuk pencirian dan rugi per sambungan).

**Sumber ketidakpastian utama:** sambungan test cord ke alat uji — redaman dan
reflektansinya dapat berbeda dari saat kabel disambung ke perangkat sungguhan. Penanganan:
terminasi kelas referensi. [R2, PDF 20]

> Kesalahan yang paling sering terjadi di lapangan: **menyerahkan hasil OTDR saja** sebagai
> bukti lulus. OTDR mencirikan jalur; ia tidak mengukur rugi sisipan total.

---

## ⑤ Bukti serah

| Lampiran | Wajib | Catatan |
|---|---|---|
| Berita acara uji per core | ✅ | Kerangka di `TEMPLATE-BERITA-ACARA.md` bagian 1 |
| **Ambang beserta rincian hitungnya** | ✅ | Butir yang paling sering hilang |
| Metode uji + pilihan test cord | ✅ | Sebutkan nama metodenya, bukan hanya alatnya |
| Sertifikat kalibrasi alat | ✅ | Merek, tipe, nomor seri, tanggal |
| Rugi kabel referensi terukur | ✅ | Syarat ≤ 0,5 dB |
| Jejak OTDR + daftar peristiwa | bila disyaratkan | Sertakan setelan: lebar pulsa, rentang, launch cable |
| Catatan ketidakpastian | ✅ | Melindungi saat hasil berada dekat ambang |
| Kartu kendali rantai | ✅ | Satu per jalur |

**Status rantai: UTUH.** Ambang berasal dari hitungan rancangan yang dapat ditelusuri, dan
metode ujinya bersandar pada standar internasional [R2].

**Yang masih terbuka:** IEC 61280-4-1 (padanan untuk **multimode**) belum ada di rak. Untuk
pekerjaan multimode, metode uji bersandar pada OFSTP-14 [R3] — sebutkan hal ini bila
kontrak menuntut acuan IEC.
