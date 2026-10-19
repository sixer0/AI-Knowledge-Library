# Cross-Lane Register Audit — pitfall sweep lajur pengumpulan data (2026-10-03, DEMS-VSAT/VENDOR-DEMS)

Konteks: audit pengawas silang atas 8+ lajur `register.tsv` produksi worker
(AUD-DSP, kamera, switch, kabel, UPS) + merge + verifier. Semua temuan di bawah
terukur nyata pada giliran itu; bukan teori.

## 1. Sniff delimiter PER BERKAS sebelum parse
Dua register `*.tsv` dalam ekosistem yang sama bisa beda delimiter: TAB atau
PIPA (`|`). Kasus nyata: `L01-F1/register.tsv` ber-pipa; dibaca dengan
`csv.DictReader(..., delimiter='\t')` → "37 baris x 1 kolom", seolah register
rusak total padahal checker yang rusak. Preseden hulu sama: berkas A2 pipe,
A3 TAB (pitfall UKUR 29-09). Resep:
```bash
head -c 200 lanes/X/register.tsv | cat -A | head -2   # lihat | vs ^I
```
Deteksi dulu, parse kemudian. Lapis merge (MRG) WAJIB deteksi per lajur,
jangan asumsikan seragam antar-kartu.

## 2. Kandidat cacat entity-match != cacat; cek kolom brand + notes dulu
Pola proksi kasar (token `[A-Za-z]{4,}` dari vendor_name harus muncul di host)
menghasilkan positif-palsu sistematis karena nama badan hukum ≠ merek domain:
- Shenzhen TVT Digital Technology ↔ `tvt.net.cn` (brand: TVT)
- Nexight LLC ↔ `nexigo.com` (brand: NexiGo)
- Shenzhen Tongveo Video Tech ↔ `tenveo.com` (brand: Tenveo)
- Shenzhen Remo Tech ↔ `obsbot.com` (brand: OBSBOT)
- Brähler International ↔ `braehler.com.cn` (tokenizer naïf pecah di umlaut)
Protokol vonis kandidat:
1. dump baris LENGKAP: kolom `brand`, `product_ref`, `notes`/`entity_match`;
2. uji token `brand` vs host (bukan vendor_name);
3. vonis cacat tipe-BDCOM (entitas salah-negara diberi PASS) hanya bila brand
   DAN notes sama-sama tanpa bukti pencocokan. BDCOM asli: judul halaman
   "BDCOM Online Ltd ... Bangladesh" dilabeli PASS untuk vendor CN — tabrakan
   nama lintas-negara, bukan selisih badan-hukum-vs-merek.
4. Catatan positif: register lajur yang punya kolom `brand` terisi terbukti
   kebal pola ini — tagih schema itu ke lajur lain sebelum merge.

## 3. Angka vonis wajib = cetakan register (recomputed-from-register)
Vonis pekerja boleh meleset kecil dari datanya sendiri: klaim MIK 17/KIT-MIK 13
vs register mentah 15/15 (total sama 30; dugaannya skrip pencacah lajur memakai
aturan substring), TRUSTED 9 vs 8. Total cocok → bukan fabrikasi, tapi angka
rinci tidak reproducible. Audit: rekalkulasi SETIAP angka klaim dari register
mentah dengan parser sendiri. Selisih = tagihan tertulis ke lapis VS/merge
("vonis harus = cetakan register"), bukan pembatalan vonis. Ini turunan langsung
aturan anti-halusinasi: angka laporan = cetakan alat pada giliran itu.

## 4. Audit run-resume (kartu R2 atas checkpoint)
Jangan hitung baris saja. Tiga uji:
1. DELTA register vs run-1 (mis. 37→38; verifikasi baris baru riil via row_id);
2. SETIAP residu bernama S2 run-1 harus punya status eksplisit di vonis R2:
   SELESAI / PARTIAL-ber-akun / tertutup-NEGatif (contoh baik: 7 residu →
   4 selesai + 2 partial ber-akun + 1 tertutup negatif);
3. SPOT-CHECK klaim substantif terbesar terhadap artefak primer di disk.
   Contoh: klaim "pemenuh PERSIS pertama" → ekstrak teks PDF datasheet yang
   tersimpan di `raw/pdf/`:
   `uv run --python 3.11 --with pdfplumber python -c "import pdfplumber; ..."`
   (pdfplumber tidak ada di env terisolasi — paket wajib disebut eksplisit via
   `--with`). Vonis SUBSTANSI bukan string literal: klaim "line-in" dibuktikan
   PDF lewat baris `Audio I/O 1 Input: impedance 35 kΩ, amplitude 2 V [p-p]`.
Indikator checkpoint jujur tambahan: `vonis.md` menyatakan "dihasilkan parser
dari raw/*.jsonl, bukan angka ingatan"; UNTRUSTED terflag terbuka (bukan
diselundupkan PROV); tebakan nama lama DIHAPUS setelah bukti R0 sah; CAPPED
disampaikan sebagai PERMOHONAN PUTUSAN dengan akun per kanal mati (000/403),
bukan vonis buntu sepihak.

## 5. Hitung papan per-misi: grep tag [TENANT], jangan filter JSON by path
`hermes kanban list --json` berisi SEMUA kartu lintas misi (ribuan) dan
`workspace_path`-nya = direktori worktree PER-KARTU
(`.../kanban/workspaces/t_xxxx`), bukan path kontrak misi. Filter JSON by
path kontrak → 0 kartu = "papan kosong" PALSU (terjadi nyata dua kali semalam).
`--tenant <path>` pada CLI list juga mengembalikan 0 untuk misi ini. Cara benar:
```bash
hermes kanban list > kl.txt
grep -i "[TAG-MISI]" kl.txt | awk '{for(i=1;i<=NF;i++) if($i~/^(done|running|ready|todo|blocked)$/) print $i}' | sort | uniq -c
```
Baris teks output memuat tag `[TENANT]` di judul → hitung kata status per
baris. Verifikasi juga daftar running (id + judul) agar tidak salah vonis
"resume belum dilepas" saat kartunya sebenarnya jalan.

## Pola penutupan audit (yang dinilai SAH oleh pengawas)
- partial-handoff LIMIT-AWARE dengan Ambang-A/B tercapai + ladder 8 kelas
  ber-akun + kelas yang belum jalan = dijadwalkan ulang beralasan / residu
  bernama, BUKAN N/A diam-diam;
- baris tanpa fetch diakui eksplisit ("not fetched this run") lebih baik dari
  URL karangan;
- entitas di luar fokus (TH1 di lajur CN/TW) boleh ada asal TERFLAG — tagihan
  verifikasi asal, bukan pembuangan baris.
