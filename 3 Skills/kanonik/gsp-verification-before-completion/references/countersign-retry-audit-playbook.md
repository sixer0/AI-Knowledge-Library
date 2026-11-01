# Countersign & Retry-Audit Playbook (pengawas silang)

Dikondensasi dari tiga misi (05-10), semua pola terukur di disk. Berlaku untuk vonis countersign atas kartu verifier/pekerja dan catatan timeout/crash.

## Urutan wajib sebelum vonis
1. **Angka = cetakan alat pada giliran ini.** Jangan kutip angka dari laporan pihak lain atau ingatan: jalankan ulang scanner/parser/probe sendiri, bandingkan. Pin sha (docx/pdf/master) harus segar diukur, bukan disalin.
2. **Instrumen sendiri diuji dulu.** Berkali-kali "cacat artefak" ternyata bug matcher pengawas: prefiks `FIG-` hilang saat mencocokkan ID, regex `\{\{KL:[^}]+\}\}` memotong ID ber-pipa, jendela regex 2.500 char terlalu sempit, `\b` salah tempat, heading `# ` vs `\n## ` sebagai batas blok. Koreksi instrumen SEBELUM vonis; kalau vonis sudah terbit, koreksi diri lewat komentar terpisah.
3. **Ukur draf vonis sebelum kirim.** Draf pernah terpotong 229 B tanpa terasa: cek panjang + `grep -c` anti-duplikat pada `kanban show` sebelum kirim; glif U+2014/U+00B7/CJK dihitung pada draf itu sendiri (typo CJK pernah lolos ke draf).

## Rekonsiliasi angka beda = definisi beda
Selisih hitung hampir selalu terjelaskan oleh cakupan/detektor, bukan salah satu pihak. Wajib dibukukan dengan menyebut DEFINISI tiap angka:
- URL unik 412 vs 413 = beda perlakuan pola-brace instruksional.
- Slug 22 vs 20 vs 28 = gate-luas vs kanonis-berpasangan (>=2 segmen) vs regex longgar (termasuk token tunggal).
- Kata 13.589 vs ~15.047 = definisi pembukuan berbeda; angka beban-rilis tetap diverifikasi terpisah.
- Marker FIG 36 vs 38 = ANTRE bernama ber-putusan controller (hilang dengan keputusan, bukan diam-diam).
Klasifikasikan tiap selisih: beda-definisi (terjelaskan) / positif-palsu instrumen / temuan nyata. Jangan laporkan kontradiksi mentah.

## Subjek-konten vs kebocoran (kelas positif-palsu penting)
Scanner menemukan "pelanggaran" yang isinya justru OBJEK bahasan: emoji di baris register Bab tokenisasi, identifier keras `top_p`/`max_tokens` di tabel register, kata "fetch" prosais dalam "cache fetch lokal", `{{KL:...}}` literal dalam prosa yang menjelaskan konvensi placeholder. Tes: probe LOKASI (bagian/fence mana), lalu vonis "tambal = memalsukan rekaman" - jalur benar adalah putusan kanal/allow-list controller, BUKAN hapus buta. Sebaliknya, path kerja internal (`_work/.../fetch/x.html`) tercetak di kaki figur = bocor nyata dan wajib hilang dari wajah figur; kemunculan di prosa badan bab sebagai rujukan [measured] = sah, catat sebagai opsi pemetaan arsip publik (non-blokir).

## Kanalisasi scanner fleet
`scan_ai_footprint.py` WAJIB dipanggil dengan `--channel <kanal target>`; panggilan polos memakai kanal default dan mencetak false-FAIL (kasus C-7 pada review-2). Baca `--help` sebelum menuduh artefak. Kanal kitab (plafon C-6 20) vs doc (ambang indikator) menghasilkan verdict berbeda untuk berkas sama - putusan kanal agregat wajib diambil SEBELUM gerbang naturalisasi dijalankan atas kitab utuh, supaya FAIL agregat tidak diulang dari nol. Ukur per-berkas vs agregat kitab bisa berbeda vonis (lampiran 34,2 per-berkas tapi agregat buku 18,7 PASS) - nyatakan lapis mana yang mengikat.

## Audit timeout/crash (jejak dulu, vonis kemudian)
1. Ukur state disk: artefak target (mtime/sha/ukuran vs basis), workdir instrumen, laporan, baris Riwayat. Naskah bisa LAHIR sebelum worker mati (B20/B22/RAKIT/UJIJ) - jangan re-dispatch buta, jangan tulis ulang dari nol.
2. Klasifikasi fase mati: analisis (nol mutasi, FIX-FIG run-1) vs pasca-artefak (RAKIT run-1, crash B22) vs paruh grup (FIX-FIG run-2). Arahan run-2 = daftar kerja sempit + resep konkret + peringatan idempoten-berbahaya (jangan apply ulang replace yang sudah terbetulkan; jangan timpa arsip_pre bersih; jangan re-run panggilan model berbayar - checksum dataset acuan).
3. Cek duplikat notifikasi/redeliver: kartu dengan vonis terpasang = tanpa aksi.
4. Pola gagal berulang (3-run habis satu kartu) = tiket traceroot ke pemilik rantai, bukan retry lebih keras.

## Gerbang idempotensi build/rakit
Dua-run byte-identik membuktikan REPLIKASI, bukan kebenaran semantik - keduanya needed: shaA==shaB (diff part zip; stempel waktu arsip boleh beda, konten part tidak) PLUS vision QA/render-inspection per butir. Pin sha artefak di vonis agar vonis berikutnya bisa verifikasi rantai tiga-mata (build -> vonis-rakit -> vonis-akhir). SHA lama diarsipkan verbatim di manifest + direktori arsip saat tambalan.

## Vision QA figur (gerbang mengikat)
Uji per-butir terhadap cacat lama + minta status eksplisit per butir + minta cacat BARU disebut. Traceroot ke hulu sebelum vonis: mismatch "lima vs enam tombol" ternyata sumbernya badan bab, figur faithful - vonis dua-lapis (produk SAH, cacat dilacak ke naskah). Suntingan wajah figur wajib dicek DESINKRONISASI turunannya: caption manifest (gerbang rakit membaca dari manifest), prosa bab, figur lain ter-render ulang oleh skrip bersama (ukuran berubah = nyatakan jujur di manifest). Akar sistemik geometri (marker di DALAM screenshot memaksa konektor menembus interior) - tambalan gejala cuma memindahkan tumpang-tindih; resep: pindahkan penanda ke margin luar bingkai.

## Lubang cakupan instrumen vonis tulis (terbukti 05-10)
Anatomi+KL+glif saja MELEWATKAN kuota rentang per-elemen (Tujuan belajar 3-6, Uji pemahaman 3-8): 16/22 bab lewat plafon, lolos 21 vonis tulis, baru tertangkap di uji mutu akhir. Vonis tulis bab wajib ikut CHECK kuota speks sejak bab pertama, bukan hanya keberadaan elemen.

## Siklus resume-pekerja yang sehat (pola untuk dinilai SAH)
Pekerja run-2 yang menuruti catatan retro: tidak reset naskah (delta kecil, baris identik), bangun workdir instrumen yang belum ada, temukan state stale sendiri lalu KARANTINA (bukan timpa), tulis sub-bab pembacaan hasil null/floor-effect, nyatakan isi _trash di LOG. Nilai ciri ini positif di vonis agar pola menyebar.

## Redaksi
Jangan tempel nilai secret apa pun di vonis/komentar; tulis `[REDACTED]`.
