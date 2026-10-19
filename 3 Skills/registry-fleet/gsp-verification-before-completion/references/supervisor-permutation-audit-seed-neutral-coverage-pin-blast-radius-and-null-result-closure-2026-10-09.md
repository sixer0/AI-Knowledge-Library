# Supervisi 09-10: audit permutasi, bukti cakupan seed-netral, blast radius pin, penutupan null-result

Sumber: misi PSIKOTES-1008 gelombang F4/F5 (kartu L21-L28, FIX-6, FIX-7), vonis controller
dengan ukur disk tiap giliran. Semua resep di bawah sudah dijalankan nyata dan menghasilkan
vonis yang diterima.

## 1. Audit permutasi (verifikasi pengocokan opsi/kunci di dokumen rakitan)

Saat kartu FIX melakukan permutasi deterministik atas URUTAN OPSI (pola anti-tebakan sebaran
huruf kunci), empat probe parser independen menutup kelas cacatnya. Jangan pakai alat pekerja
sebagai satu-satunya dasar:

1. **Kesetaraan multisete**: per butir, multiset teks opsi tampil == multiset teks opsi bank.
   Menjamin tidak ada teks opsi yang hilang, bertambah, atau berubah satu karakter.
2. **Pendaratan kunci via peta**: teks kunci kanonik bank harus jatuh tepat di huruf hasil
   apply peta permutasi (`opsi_per_item[bank_letter]`) pada dokumen tampil. Uji per butir
   inti ber-opsi (terukur: 30/30).
3. **Sinkron dua-arah tabel kunci hilernya**: pada dokumen answer key, kolom Kunci == kunci
   bank DAN kolom huruf tampil == apply peta, untuk SEMUA baris termasuk cadangan (terukur
   37/37). Parser tabel: baris `| id | inti/cadangan | level | Kunci | Huruf tampil |`.
4. **Sebaran jendela-N**: kunci TAMPIL per section tidak boleh memuat huruf sama >2 dalam
   jendela 5 butir berturut (aturan anti-tebakan era L18/qc-AB). Laporkan string sebaran
   per lane (mis. `B: CCDAB`) agar vonis bisa dibaca ulang.

Peta permutasi (`display-map.json`) adalah objek verifikasi: cek skema barunya
(`items[] + cadangan[]` dengan `opsi_per_item`) sebelum menulis probe - format lama berupa
list polos `{tampil, bank}` akan melempar TypeError bila diasumsikan dict, dan sebaliknya.

## 2. Bukti cakupan perubahan via varian identitas seed-netral

Klaim pekerja "perubahan terisolasi ke urutan opsi saja, batang soal dan teks opsi verbatim"
terbukti kuat oleh pola yang bisa diadopsi sebagai standar kartu FIX: builder yang sama
dijalankan dengan VARIAN IDENTITAS (seed-netral / permutasi kosong) menghasilkan byte yang
SAMA PERSIS dengan sha pra-perubahan yang pernah diukur controller di vonis sebelumnya
(terukur: REV-1 varian identitas memulihkan sha REV-0 `ca514c329117ba03`). Controller cukup
mencocokkan dua sha miliknya sendiri - tidak perlu mempercayai narasi cakupan.

Syarat pola ini: vonis sebelumnya WAJIB mencatat sha artefak (praktik L2 sudah menagihnya),
dan baseline pra-sunting dipersistenkan sebagai berkas `.baseline-pra-*.md` (preseden
`C-answer-key.baseline-pra-sunting.md`).

## 3. Vonis bersusun: REV lama tetap sah, REV baru dapat vonis baru

Ketika FIX mengubah artefak yang sudah divonis L2, JANGAN mencabut vonis lama: tulis vonis
baru yang secara eksplisit menyatakan "vonis REV-0 sah untuk sha X, kini digantikan vonis
REV-1 sha Y" di komentar kartu. Register sha per-rev di komentar membuat audit silang
instrumen hilernya (yang mem-pin sha dokumen) bisa direkonstruksi.

## 4. Penutupan null-result: field result kosong bukan kartu gagal

Kasus L25 (`t_9dbab7a7`): notifikasi papan membawa ringkasan lengkap, status `done`, tetapi
`show --json` membaca `result: None`. Vonis tetap sah dan bertumpu pada DISK: artefak ada,
gerbang deterministik milik pekerja lolos rerun controller, builder byte-identik, scanner
bersih. Jangan re-dispatch, jangan membuka kartu ulang, jangan menuntut pekerja menulis
result susulan. Catat kelasnya di jejak vonis ("field result terbaca None via show --json;
penutupan sah lewat jalur wake/summary; vonis bertumpu pada artefak disk") agar verifier
berikut tidak salah baca sebagai cacat.

## 5. Blast radius pin sebelum menulis kartu FIX (resep FIX-7)

Sebelum menyusun body kartu FIX yang menyentuh objek ber-pin sha (alat regenerasi, cetakan
acuan), controller grep konstanta pin LAMA di seluruh folder misi (`package/ qc/ blueprint/`)
dan menggolongkan pemiliknya:

- **Badan dokumen hidup** (tabel provenans D/E/F) -> masuk cakupan rebuild.
- **Konstanta checker** (`l24_check.py`, `l26_check.py`) -> masuk cakupan update ledger.
- **Instrumen gelombang berikutnya** (l27/l28 yang mem-pin sha enam dokumen) -> alasan
  kartu FIX diberi parent ke kartu yang masih running, supaya tidak balapan.
- **Arsip historis** (`qc/f2-*`, `fix1_state_*`, output era lama) -> DINYATAKAN beku di
  body FIX: "jangan disunting"; typo di arsip ikut terarsip apa adanya.

Body FIX lalu menutup dengan: baseline pra-sunting tercetak, patch minimal (diff satu baris
untuk cacat satu karakter), uji numerik-kekal pasca-regen (semua sel angka wajib identik,
satu-satunya sel berbeda = sel target), gerbang ulang SEMUA instrumen yang mem-pin, sapuan
final token cacat dengan daftar lokasi sisa yang sah, dan pin objek beku diukur ulang
pra/pasca. Gate kartu rakit-final di belakang FIX: `hermes kanban link <fix> <kartu-todo>`
menambah parent pada kartu yang MASIH `todo` dan tetap menahan promosi (terverifikasi:
parents L29 menjadi [FIX-7, L28, L27]). Nuansa penting vs pitfall late-linked-parents lama:
edge susulan menahan promosi selama kartu sasaran belum naik ke ready/running; pada kartu
yang sudah ready ia tidak mendorong kembali ke todo.

## 6. Sensor lingkungan saat mengukur

- **`grep` biner tidak ada di sandbox subprocess** pada host Windows ini (`FileNotFoundError
  WinError 2` dari `subprocess.run(["grep", ...])`). Jalur sah: tool `search_files` atau loop
  `re` python atas isi berkas. Jangan menyimpulkan "tidak ada cocok" dari kegagalan eksekusi.
- **cmp terhadap process-substitution** (`<(...)`) bisa melaporkan EOF palsu saat stdout
  program besar mengalir lewat stream; andalkan `cmp file1 file2` atas berkas yang
  benar-benar ditulis, atau bandingkan bytes di python.

## 7. Gerbang naturalisasi jawaban controller (kanal chat)

Balasan vonis yang mengutip sha16 + id kartu `t_...` + nama kolom sekaligus memicu C-13
"3 identifier keras" = FAIL di kanal chat. Remedi yang terbukti (terpakai 4x giliran ini):
pindahkan kode keras ke jejak (komentar kartu/berkas), rujuk di chat dengan label manusia
("sidik jari utuh tercatat di komentar vonis kartu"), sisakan maksimal 2 identifier keras,
lalu scan ulang sampai VERDICT PASS sebelum kirim. Ini bukan menyembunyikan bukti: komentar
kanban dan contract.md tetap memuat kode penuh (kanal internal dikecualikan).

## Batas klaim

Resep di atas adalah alat ukur per-kelas cacat pada run yang tercatat, bukan jaminan
nol-cacat sefleet (D-TA-10). Penulis kartu FIX bukan verifikator vonisnya; keempat probe
bagian 1 dijalankan controller dengan parser sendiri, bukan rerun alat pekerja.
