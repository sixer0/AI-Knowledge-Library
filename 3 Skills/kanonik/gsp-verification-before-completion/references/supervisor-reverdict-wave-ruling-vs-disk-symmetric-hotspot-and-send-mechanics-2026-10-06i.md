# Supervisi gelombang re-vonis + putusan-vs-disk + penutupan simetris hotspot (06-12, PROMANUAL-V2 + INDUK-GAYA-VISUAL)

Lanjutan seri 2026-10-06 a–h. Semua resep di bawah TERPAKAI dan menghasilkan vonis pada giliran itu.

## 1. Gelombang re-vonis (ronde-2/3 atas byte pasca-tambal)
Pola papan: vonis FAIL -> kartu tambal -> rebuild -> RE-VONIS atas byte baru. Yang pengawas cek per kartu re-vonis:
- **Pin silang wajib**: laporan re-vonis HARUS menunjuk pasangan byte AKTIF era terbaru (bukan era yang digantikannya). Cek: petikan sha16+ukuran+mtime di laporan vs probe disk. Di PROMANUAL-V2 ini terbukti 9-10 kartu berturut memakai pin benar setelah tagihan eksplisit "ledger pin jangan diwarisi diam-diam" dipasang di countersign REND.
- **Objek era-lama beku**: artefak ter-vonis lama tidak boleh bergeser (mtime/sha identik probe sebelumnya) DAN idealnya terarsip bernama (`_arsip-prerb/RBUILD-<sha>.docx` + berkas PIN-LAMA ledger). Promosi-dengan-arsip = pola emas; tanpa arsip = tagihan.
- **Re-meter dengan alat sendiri**: reproduksi minimal satu butir kunci per kartu (rail terpotong=0, halaman dup>=2=0, idem runtuh, caption 53/53, SG 68/68 semua menancap sumber). Selisih cacah dengan klaim = beda definisi/populasi -> nyatakan ARAH+BESARAN, declared, jangan vonis kontradiksi.
- **Determinisme lintas-tangan**: jalankan ulang instrumen resmi pekerja (bukan mereplikasi formula hash dari menebak - UCERPOP-B: tiga formula hash-naif semua beda, jalan benar = eksekusi skrip resminya).

## 2. Putusan-controller-vs-disk (kelas E-09)
Putusan konten di Decision Log boleh menujuk byte dengan ukuran - tetapi pengawas WAJIB menguji angka putusan terhadap disk:
- E-09 menyebut varian pemenang "53.415 B" padahal kartu pemilik punya DUA varian: antara 38d0fe7c/53.415 B (GAGAL scanner, kini di path kanon) dan final kerja 0b28faf8/55.383 B (PASS). Angka putusan menancap ke byte gagal.
- Vonis sah: kepatuhan pekerja SAH, TAPI pasang "dua pembacaan sah" + opsi eksplisit (promosi final PASS 2-iterasi / known-defect tercatat ber-putusan) + tegaskan risiko hilir (rakit langkah berikutnya MEMUAT bahan gagal sekarang). Pengawas tidak memutuskan; vonis menempel byte.
- Metrik pembanding putusan ("57 vs 37 token perintah") yang tak tereplikasi regex-cepat-ku: declared non-replikabel, putusan kekayaan isi tetap milik controller.
- Preseden serumpun: kartu hilir dilarang memuat klaim status gerbang yang belum lahir (PREMIS PENUTUPAN MENDAHULUI HASIL - SERAH dibuat 11:24, laporan gerbang 12:00+; bukti dari selisih mtime vs created).

## 3. Penutupan simetris penerbitan-ganda (kasus ke-2..ke-4)
Setelah kedua kartu hotspot menahan diri, penutupan datang berpasangan - cek SIMETRIS keduanya:
- Sisi stand-down: byte kanon STABIL (mtime tak bergeser sejak sensus pertama = janji "tidak menulis ulang" terbukti), arsip utuh, rujukan putusan eksplisit.
- Sisi pemilik-acuan: **re-verifikasi silang** (pemilik menguji byte saudaranya terhadap gerbang sendiri dan melaporkan LOLOS) = bentuk tertinggi; putusan controller menjadi "pilih isi terbaik, bukan kepatuhan".
- Salinan alt ber-pembungkus frontmatter: selisih ukuran vs byte asli = panjang pembungkus (declared di kepala berkas) - kucek sebelum menuduh mutasi isi.
- **Cek heartbeat saudara sebelum vonis**: kartu masih running + byte lebih muda dari klaim timpa = risiko hidup, tandai URGENT; dua kartu saling-tunjuk pemilik = deadlock koordinatif sehat yang hanya pecah oleh controller.
- Traceroot tetap di hulu-dispatch: kartu baru wajib menyertakan aksi SUPERSEDE eksplisit atas kartu lama (4 kasus satu hari, nol kerusakan permanen berkat lane pekerja).

## 4. Provenans beku-sebelum-kunci (rantai uji-pembaca)
Tiga sumur untuk kartu penjawab netral: (1) sha16+ukuran jawaban == klaim; (2) **mtime berkas kunci TIDAK BERGESER** dan lebih tua dari claimed-run (4 kartu berturut jam kunci identik = kontrol waktu); (3) sha16 bahan paket == cetakan pekerja. Token "skor/gagal" di jawaban: cek konteks - isi materi BUKAN penskoran diri. Klaim negatif ("nol sumber luar/memori") tak teruji penuh dari disk: declared, cukup semua yang terukur konsisten.

## 5. Closeout git diverifikasi remote-side
Standing rule commit+push: vonis hanya dari `git ls-remote origin main` (HEAD) + `git log origin/main` memuat SEMUA hash dilaporkan + `git cat-file -s $(git rev-parse "origin/main:<path>")` membuktikan blob besar (14,9 MB sajian) ikut versioned - bukan klaim lokal. Repo cermin bisa beda dari folder misi (shared-ws bukan repo).

## 6. Koreksi jejak pengawas (pelajaran-ke-9/11/13 terulang)
- **Peta kolom dari cetakan awk GILIRAN YANG SAMA dengan posting**; bila state bergeser antara draf dan tayang, pasang komentar koreksi terpisah ATAU segarkan baris peta sebelum tayang (scaning: d43->d44, d12->d14 dst terjadi nyata beberapa kali).
- **Guard grep anti-duplikat wajib frasa-heading unik**: `grep -c "Countersign pengawas"` bisa menancap juga di result/jejak pekerja (=3 palsu); pakai `grep -c "Countersign pengawas silang atas <KARTU>"`.
- **grep VERDICT wajib cek konteks seksi**: pola pertama bisa menancap baris lint internal ("VERDICT PASS" instrumen) padahal VERDICT resmi dokumen = FAIL (GDESB2). Cari heading seksi VERDICT.
- **Aritmetika satuan adalah alat yang bisa cacat**: tblGrid kucek dua kali salah (divisor EMU vs dxa; faktor dua) sebelum menancap dxa/1440*25,4; extent docx = EMU/360000; laporan byte CRLF harus dibaca BINARY (mode-teks melaporkan 40.849 vs nyata 41.097).
- **Sitasi antar-kartu pakai sha16, bukan angka byte** (race tulis-menengah: TA cite 37.659 B saat RT masih menulis, disk 38.038 B; baris cocok, byte tidak).

## 7. Mekanika pengiriman (shell)
- Perintah terminal panjang ber-kutip-bersarang sering RUSAK saat pengiriman (`Invalid command: expected string, got NoneType`, dua kali nyata) - pecah jadi perintah pendek ATAU tulis skrip .py lalu jalankan via uv.
- Sunting teks vonis (typo, glif CJK lolos, petik) JANGAN via sed inline ber-quote-nested - tulis skrip Python kecil (replace eksplisit + guard hitung emdash/middot/len) lalu eksekusi.
- Panggil scanner fleet lewat `uv run --python 3.11 python <abs-path>`; `python` langsung bisa jatuh ke alias Store dan menghasilkan output nihil senyap (pitfall lama, terkonfirmasi lagi).

## 8. Sensus engine-pin lintas-kartu
Setiap kartu build selesai: re-probe sha16+mtime engine kanon (`datum_docx.py caf47d62`) - satu baris probe, membuktikan "kontrol beku" klaim kartu dan menangkap suntingan senyap. Terpakai 10x konsisten; engine fix yang naik lewat kartu lain (lintas-papan) catat "dua rumah jejak" di ledger supaya hilir tak mengira dua suntingan berbeda.

## 9. Nilai allow-list dan nama hantu
- Allow-list gerbang (datumbind stray): kucek KONTEKS tiap nilai di-allow - "knowingly-listed" (mis. 1660,0/1280,0 = contoh pedagogis cacat lama di blok B4/B6) bukan kelupaan.
- Nama berkas hantu yang sudah divonis REJECTED: grep konteks kemunculannya di hilir - dipakai sebagai CONTOH PEDAGOGIS/disiplin register = sah; dikutip sebagai path sah = cacat. Register hilir yang menghormati REJECTED tanpa menunggu putusan = jalur aman sehat, pujang di vonis.
