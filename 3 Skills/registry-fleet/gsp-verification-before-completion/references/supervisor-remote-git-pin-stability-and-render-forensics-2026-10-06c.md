# Resep pengawas sesi 2026-10-06 gelombang akhir (VISUAL-1005 + PROMANUAL-V2)

Dipetik dari countersign R12/J11/REVC/J2A/J2B/R13/R14/R15/F17/F17-LANJUT(INV-9)/A19/A19B/F18/F19/F19B/F20/F21/SA/RWG/SPEC5/SPEC6/SPES6B/REND/RWA-RWB-micro/RWI/RWH/RWC/RWE/RWD/SPEC4/R14B/B18/RAKIT. Semua terverifikasi jalan pada giliran itu; bukan tebakan.

## 1. Bukti closeout git REMOTE-SIDE (F19/F19B)

Jangan vonis closeout dari log lokal. Tiga perintah, semua ke origin:

```bash
git ls-remote origin main                       # HEAD remote == hash yang diklaim
git log --oneline -6 origin/main                # commit dilaporkan TERDORONG, linear dari HEAD era sebelumnya
git cat-file -s "origin/main:<path-di-repo>"    # ukuran blob yang DIAM-PUNYA di remote (bukti terberat artefak besar ikut versioned)
```

Kasus nyata: blob sajian 14.901.519 B di origin/main == ukuran yang kuprobe di disk (countersign F18) - membuktikan 'sajian 14,9MB ikut versioned' tanpa men-download repo. Untuk delta-commit pasca-vonis, cek pesan commit memuat id temuan (F-21a/F-21b) = rantai sebab-akibat vonis->perbaikan masuk riwayat git.

## 2. Stabilitas pin lintas-giliran (REND/SPES6B/RAKIT - senjata baru pengawas)

Pada catatan timeout, BEKUKAN pin instrumen/engine (sha16+ukuran+mtime) dari disk. Pada countersign berikutnya, RE-PROBE berkas yang sama:

- Engine `datum_docx.py` dibekukan `caf47d62` @09:01:20 di catatan REND-run-1 -> countersign REND re-probe IDENTIK -> semantik pekerja 'render memakai engine tertambal caf47d62' terverifikasi INDEPENDEN, bukan klaim.
- Objek spesimen `199b0f3e`/`f571b2ac` diprobe di countersign REND, diprobe ulang 20 menit kemudian di SPES6B: sha+mtime sama -> 'nol mutasi pasca-render sebelum vonis' (kelas cacat SERAH-GAYA-run-1 tertangkap oleh pola ini).
- Pin naskah antar-mata rantai (bab-17 `35b793d1` stabil dari R17 s/d R18) = bukti 'freeze antar-mata' - kartu berikutnya tidak menyunting milik kartu sebelumnya.

Aturan turunannya: vonis hilir WAJIB menyebut pin yang DIUKUR pada giliran vonis itu; bila byte hidup bergeser lagi setelah vonis (pasca-lepas revisi administratif), tagih ledger resmi (opsi: arsipkan byte tervonis ATAU catat suntingan bernama) - jangan biarkan hilir memilih pin sendiri.

## 3. Sensus sha256 seluruh pohon utk membuktikan KETIADAAN berkas (F21)

Klaim 'byte X tidak terarsip di mana pun' dibuktikan dengan sapuan sendiri, bukan kutipan verifier:

```python
hits = [p for p in glob('**/*', recursive=True) if os.path.isfile(p)
        and hashlib.sha256(open(p,'rb').read()).hexdigest()[:8] == '<sha8 target>']
# hasil: 0 -> gap arsip resmi dua-sumber ber-angka
```

Ini menutup gap yang kukutip di 4 countersign berturut (J16/F17/F18/F19) menjadi satu angka dua-sumber; jalur penutupnya (rekonstruksi-arsip vs putusan ekivalensi zona) = wewenang controller, dan keduanya memang terselesaikan (F19B: `_arsip/revB-badan.md` sha cocok + ukuran == probe era-REVC - rekonstruksi tervalidasi silang dua-era).

## 4. Gerbang render DOCX/PDF forensik tanpa skrip pekerja (SPEC6/REND/RAKIT)

Klaim FAIL/PASS lapis render dibalikkan/ditegakkan lewat pembacaan langsung:

```python
z = zipfile.ZipFile(docx); xml = z.read('word/document.xml').decode()
pg = re.findall(r'<w:pgSz[^/]*w:w="(\d+)"[^/]*w:h="(\d+)"', xml)   # urutan-bebas!
mm = [(int(w)*25.4/1440, int(h)*25.4/1440) for w,h in pg]           # A4 = 210x297
# F1 kebocoran YAML: 'source_refs:'/'task_ref:' harus NIHIL di badan
# F4 kolofon: 'NIB'/'GEMILANG' dihitung; glif peran ■◈△◇ dihitung (0 vs hadir)
import pymupdf; d = pymupdf.open(pdf); len(d)                        # halaman riil
d[0].rect  # mediabox pt -> mm (595,3x841,9 = A4)
```

Pitfall parser: regex pgSz dengan urutan atribut tetap menghasilkan positif-palsu (kasus BATAS-59B: 496 vs 722) - selalu urutan-bebas. Beda alat hitung halaman (Word ComputeStatistics vs pymupdf) boleh selisih kecil; declared, bukan cacat - tapi vonis plafon akhir memakai SATU alat resmi. Sensor yang tak menancap (regex footer tidak cocok format nyata) kunyatakan sebagai keterbatasan sendiri di jejak, bukan klaim maupun vonis.

## 5. Dua-juri + revisi pasca-vonis = reshoot, bukan warisan (REVC/J2A/J2B)

Bila revisi bernama menyentuh ZONA yang jadi bahan vonis juri (mis. pemblokir CUP), vonis era-lama TIDAK boleh diwarisi diam-diam ke byte baru. Dua jalur sah: (a) reshoot sempit zona oleh DUA juri atas pin baru (murah; preseden J3 GAYA), atau (b) putusan controller TERCATAT eksplisit. Pengawas menguji: lembar juri-2 harus BEDA-byte dari juri-1 (dua suara nyata), pin objek disebut konsisten awal-akhir, dan selisih antar-juri dihitung sendiri dari kedua lembar (ambang mekanis >=2 -> adjudikator; kasus ini 0 dari 60 sel).

## 6. Kolisi hotspot dua-kartu satu-berkas (B18) - penutupan sah via verifikasi

Gejala: dua kartu menunjuk berkas yang sama ke profil yang sama sementara run saudara aktif. Penanganan PEKERJA yang benar (vonis SAH): dua sensus berjarak membuktikan penulis aktif (berkas tumbuh), petik `frontmatter task_ref:` sebagai bukti kepemilikan, LALU balik cakupan jadi verifikasi fungsional (rerun gerbang + audit KL) - bukan menimpa, bukan naskah-ganda. Traceroot: tabrakan lahir di HULU-DISPATCH; pelajaran untuk controller: cek task_ref/lock sebelum menerbitkan kartu micro yang menunjuk berkas rantai induknya.

## 7. Peta-sisa pengawas -> micro/resume: hasil kuantitatif

Kebiasaan efektif sepanjang papan: pada tiap timeout/gave-up, pengawas menerbitkan PETA SISA dari disk (pin per berkas + daftar butir sisa + tagihan audit pergeseran tanpa laporan). Controller memakainya jadi kartu micro/resume. Bukti kuantitatif: kartu induk 4x1813 dtk tak pernah menutup; micro setara selesai run-2 dalam 282 DETIK. Aturan tambahan yang terbukti: (a) pergeseran ukuran TANPA laporan bernama antar-run wajib naik sebagai tagihan AUDIT STRUKTUR-VS-BLUEPRINT eksplisit di cakupan kartu pengganti (bab-3 -23% dan bab-5 +103B keduanya tertangkap; reviewer melapor bukan menambal = disiplin sah); (b) `placeholder_terpakai-0` BUKAN bukti `terkunci-ke-register` - dua kelas berbeda, jangan tukar (tagihan RAKIT vs temuan RWA-MICRO).

## 8. Pitfall parser kolom manifest (R12)

Manifest multi-hash: probe kolom KANON (`path`+`sha256`) sebelum vonis 'berkas hilang'. Kolom turunan parsial (`png`/`sha256_png`) hanya terisi sebagian entri -> probe pertama mencetak '56 hilang' padahal 62/62 ADA+COCOK. Sama kelas dengan sensor-spasi/backtick V4/V1: instrumennya yang salah, artefaknya benar - koreksi SEBELUM vonis tayang.

## 9. needs-review/partial = penutupan benar di gerbang akhir (F21/RAKIT)

Verifikasi akhir yang MENAHAN rilis karena pin checker belum naik + gap arsip = penutupan benar, bukan kegagalan (pola G-FINAL-B-58). Similarly kartu puncak yang mencapai artefak rilis lalu menutup partial-handoff dengan FAIL bernama teradjudikasi satu-satu + KARTU_LANJUTAN_SARAN ber-cakupan eksplisit + BLOCKER nihil = format AMBANG-B dituruti. Yang dilarang tetap: vonis 'selesai' atas byte yang belum diuji-ulang, atau nol-FAIL dipaksakan.

## 10. Koreksi diri pengawas gelombang ini (pelajaran-ke-9 terus terpakai)

- Vonis F19 menulis '0 running' padahal cetakan awk pada giliran sama mencetak 1 running -> koreksi via komentar terpisah, isi vonis (hash/blob) tak terdampak karena semua dari cetakan alat.
- Vonis R12B menyimpulkan 'kartu senyap menutup' dari selisih sensus -> SALAH; grep papan membuktikan kartu F4 bahkan belum pernah ada. Sensor ke teks TAYANG (grep papan/berkas) sebelum klaim negatif.
- Draf vonis memuat placeholder 'kucek komentar berikutnya' -> isi dengan cetakan sensus SEBELUM kirim; kalau sempat tayang, komentar koreksi terpisah wajib.
