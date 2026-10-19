# Supervisor lessons era 09-10 (PSIKOTES-1008 F4: vonis enam kartu rakit berantai)

Tiga resep + satu pola putusan + empat pitfall, berasal dari vonis L2 controller atas kartu
rakit (L21-L26 + FIX) di misi dokumen paket. Kanal: vonis pengawas atas artefak rakitan
deterministik.

## Resep 1 - pola vonis seragam kartu 'rakit dari hulu beku'

Urutan ukur yang terbukti di enam kartu, semua selesai tanpa sengketa:
1. stat + sha256[:16] artefak == klaim result (angka = cetakan alat giliran ini);
2. rerun skrip gerbang PEKERJA di cwd kontrak -> exit 0 + bandingkan stdout vs berkas run
   tercatat pekerja (byte-identik = klaim determinisme terkonfirmasi independen);
3. rerun BUILDER -> sha artefak TIDAK boleh berubah pasca-rerun (bukti naskah hasil kerja
   skrip, bukan ketikan tangan);
4. probe independen parser sendiri minimal satu lapis di atas alat pekerja (Resep 3);
5. scanner naturalisasi dijalankan ulang oleh controller pada berkas jadi;
6. pin hulu (bank/sumber read-only) dihitung ulang SETELAH semua run gelombang - utuh =
   nol mutasi hulu oleh proses rakit.

## Resep 2 - parser universal bank multi-format

Format bank beda per lane (blok ```text berpagar vs blok datar tanpa fence). Parser yang
memecah pada heading gagal senyap di lane non-fence (terukur: 6 dari 37 butir terparse).
Pola sah - pecah pada penanda field, bukan heading:

```python
parts = re.split(r"(?m)^Question ID:\s*", teks)
for p in parts[1:]:
    qid = re.match(r"([A-E][\w\-]*)", p)
    k   = re.search(r"(?m)^Correct Answer:\s*([A-E])", p)
    opts= {m.group(1): m.group(2).strip()
           for m in re.finditer(r"(?m)^Option ([A-E]):\s*(.*)$", p)}
```

## Resep 3 - probe pengocokan-opsi + sinkron kunci (rantai B<->C)

Ketika remedi mengocok URUTAN OPSI lembar kandidat sementara dokumen kunci memuat kunci
kanonik, uji tiga arah dengan peta tampil (display map):
- PROBE1 (lembar tampil): tiap butir ber-opsi, TEKS kunci bank harus jatuh tepat di huruf
  hasil apply peta; multisete teks opsi tampil == multisete bank (relaksasi dari
  urutan-identik, disengaja oleh pengocokan).
- PROBE2 (dokumen kunci): kolom 'Kunci' == kunci bank DAN kolom 'Huruf tampil' == apply
  peta, per baris tabel lane.
- PROBE3 (sebaran): jendela-5 berturut tanpa satu huruf >2, dihitung ulang sendiri;
  bandingkan dengan cetakan gerbang pekerja.
Skema peta bisa BERUBAH rev antar kartu (list [{tampil,bank}] -> dict
{seed, items, cadangan} pasca pengocokan): probe wajib membaca kedua bentuk, jangan keras
pada satu skema.

## Resep 4 - artefak genre-beku vs vonis scanner

Dokumen berbadan verbatim (lembar ujian; kutipan konfigurasi rusak sebagai objek soal)
bisa FAIL indikator gaya (C-6/C-7/C-13/C-14/C-16 + agregasi D-TA-09) padahal VONIS MUTLAK
(C-1/C-2/C-3/A4-A7/C-4/C-5) nol. Jalur sah BUKAN mengejar hijau dengan menulis ulang badan
(melanggar pembekuan hulu + bisa membocorkan - kasus C-13 `timeout_ms` adalah objek
pengukuran butir itu sendiri): controller membuat PUTUSAN kanal sajian eksplisit di
Decision Log kontrak, dan kartu gerbang serah WAJIB mendeklarasikan warisan-genre +
rujukan putusan, bukan lolos senyap. Catatan pekerja beralasan per-baris (mis.
l22-naturalisasi-catatan.md) adalah BAHAN putusan, bukan pengganti putusan.

## Pitfall

- Field `result` kartu terbaca None lewat `show --json` padahal notifikasi papan membawa
  ringkasan: penutupan tetap sah bila artefak + cetakan alat di disk lengkap; vonis
  bertumpu pada ukur disk, bukan field ringkasan. Jangan vonis 'cacat kerja' dari
  metadata mesin saja.
- `cmp <(python x.py)` vs berkas hasil redirect bisa beda HANYA karena gaya baris baru /
  stream terpotong; normalisasi `sed 's/\r$//'` kedua sisi sebelum menuduh regresi
  determinisme (varian preseden EOL 07-11).
- Cetak pin pra/pasca memakai pemisah `*` (bukan spasi) di sebagian alat: parser ledger
  wajib toleran dua bentuk.
- Notifikasi completed = L1: ukur fresh sebelum vonis; berlaku juga saat ringkasan
  notifikasi terlihat lengkap (replay/basi era 08-08h).
- Regenerasi alat hulu untuk uji determinisme bisa menghasilkan beda EOL saja bila alat
  menulis dengan newline sistem: diff setelah normalisasi EOL = vonis sebenarnya
  (terukur: regen hitung_konversi 40 identik setelah normalisasi, beda byte di baris 1
  sebelum).

## Tagihan turun-temurun (rujukan silang)

Tagihan dari vonis countersign WAJIB tertempel verbatim di body kartu hilir saat create,
dicek grep saat short-check peluncuran - sumber normatif kelas ini: aturan penempelan
tagihan di `gsp-orchestration-execution` (preseden D-11 PSIKOTES-1008: tagihan
pengocokan-huruf-B tidak tertempel di kartu L22, pekerja merakit sah sesuai kartunya,
ketahuan hanya saat vonis pengawas -> kartu FIX + revisi vonis B/C ke REV-1).
