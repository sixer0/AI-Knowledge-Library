# Merge-Layer Audit + Compressed-Page Matcher Test (2026-10-03, DEMS-VSAT F1)

Lanjutan `cross-lane-register-audit.md` (§1-5 di sana: delimiter, matcher,
vonis=cetakan register, audit R2, hitung papan). File ini menambah dua teknik
terukur nyata dari giliran audit MRG-F1/L07-F1.

## 6. Uji hidup kandidat matcher: WAJIB `curl --compressed`
Fetch manual untuk membuktikan token merek di halaman bisa menipu mentah:
sebagian host CN mengirim body gzip TANPA negosiasi header. Kasus nyata:
`qacctv.com` → 28 KB byte terkompresi, nol `<title>` ter-grep, seolah halaman
asing/kosong = positif-palsu cacat entity-match. Resep benar:
```bash
curl -sL --compressed --max-time 25 -A "Mozilla/5.0" "$URL" -o page.html
grep -oiE "merek|nama_cn" page.html | tr 'A-Z' 'a-z' | sort | uniq -c
```
Hasil pasca-dekompresi: 47 token "乔安" + "jooan" → baris SAH (JOOAN).
Vonis hanya setelah byte terbaca; tagihkan flag `--compressed` ini ke checker
milik pekerja juga (satu giliran curl polos = vonis cacat yang salah).

## 7. Audit lapis merge (MRG): bukti delta + gerbang kesegaran
Merge antar-lajur dinilai SAH hanya bila SEMUA butir terukur independen oleh
pengawas, bukan dibaca dari laporan merge:
1. **Recount per lajur sumber**: buka tiap `lanes/X/register.tsv` sendiri,
   jumlahkan, cocokkan vs klaim input-total DAN vs kolom `source_lanes` di
   berkas merge. Kasus: 38+39+66+22+38+56=259 → merge 257; per-lajur cocok.
2. **Jejak dedup tercetak**: key keputusan (`MRG-DUP-SAME-LAJUR`,
   `MRG-KONFLIK`) harus ter-GREP di kolom notes sejumlah yang diklaim (case:
   tepat 2), plus uji pasca-dedup: nol pasangan (vendor,item) kembar tersisa.
3. **Kolom join seed terisi terukur**: hitung `seed_ref` terisi per lajur dari
   merge, bandingkan vs laporan DAN artefak hulu (case: L03 54/66 cocok klaim
   seed-slice yang dulu tak terbukti dari register saja — kolom join menutup
   tagihan itu).
4. **Fantom dikenal harus 0**: seed yang sudah divonis cacat (kasus BDCOM)
   dicek eksplisit tidak ikut merge: `grep -c BDCOM merge.tsv` = 0.
5. **Gerbang kesegaran delta — paling mudah terlewat**: merge bisa LAHIR
   SEBELUM lajur terakhir menutup. Ukur mtime berkas merge vs waktu selesai
   lajur terakhir, dan `grep <ID-LAJUR> merge.tsv`: 0 berarti delta pass BELUM
   jalan meski laporan merge mengklaim skrip idempoten siap. Vonis: hilir
   (V/VS/promosi wave) DITAHAN sampai delta pass dijalankan + seed_ref
   dikalkulasi ulang. Cek papan apakah kartu delta ada — kalau tidak, tulis
   gerbangnya di kontrak + komentar kartu; jangan diam-diam dianggap selesai,
   dan (aturan lane pengawas) jangan buat kartunya sendiri.
6. **Rute jujur entitas luar-fokus**: baris US/TH di lajur CN/TW yang
   dirutekan eksplisit ke kartu lajur lain (bukan dibuang) = praktik benar;
   tagih verifikasi rute di lapis VS.

## Penanda kualitas checkpoint yang dinilai SAH (agregat 7 lajur F1)
- vonis parser-generated ("bukan angka ingatan") dari raw/*.jsonl;
- UNTRUSTED terflag terbuka lebih baik daripada diselundupkan PROV (lajur
  dengan UNTRUSTED 7-14 justru paling kredibel);
- delta run-resume terverifikasi via row_id baru, residu S2 run-1 semua punya
  status eksplisit (SELESAI/PARTIAL-ber-akun/tertutup-NEGATIF);
- CAPPED = permohonan PUTUSAN dengan akun per kanal mati (000/403), bukan
  vonis buntu sepihak;
- kolom `brand` terisi = vaksin terhadap pola tabrakan badan-hukum-vs-merek.
