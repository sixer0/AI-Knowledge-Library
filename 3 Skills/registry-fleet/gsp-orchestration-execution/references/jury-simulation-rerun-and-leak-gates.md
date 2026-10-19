# Lanjutan preseden MWSKILL-0916 s.d. rilis (17-09): rerun siklus, gerbang anti-bocor, audit controller

Lanjutan `skill-knowledge-jury-simulation.md` (anatomi rantai + butir 1-6 + pitfall awal tetap
berlaku). File ini menangkap yang terbukti pada paruh kedua misi sampai L2 rilis.

## Rerun simulasi setelah paket berubah di tengah siklus (D-09/D-11/D-13)

Bila register/paket skill berubah SETELAH kandidat menjawab (mis. merge tambal GAP 1035->1341):
- Lembar jawaban lama TIDAK sah divonis ulang — dibuat terhadap paket lama. Arsipkan utuh
  (`work/archive_run2/jawaban|grade/`) sebagai bukti run-2, JANGAN hapus.
- Ulangi dari fase KANDIDAT dengan kandidat membaca paket revisi baru; juri yang sama, rubrik
  terkunci tidak digeser.
- Arsipkan `score.json`/detail run lama (`score_run2_FAIL.json`) sebelum skor baru menimpa;
  parser skor harus IDENTIK antar-run supaya perbandingan run sah. Lonjakan run-2 FAIL -> run-3
  LULUS (median 141->174, G3 16->24, G5 47->59) mengonfirmasi akar di hulu data, bukan
  kandidat/rubrik.
- Distribusi terkunci sampai SCORE run baru LULUS_AMBANG; vonis verifier atas paket lama tidak
  mewarisi ke paket baru (REVERIF dengan instrumen verifier dijalankan ULANG penuh).

## Gerbang anti-bocor penanda soal (C16) — preseden FAIL(1) REVERIF3

- Kebocoran nyata: 26 baris register era GAP memakai field `catatan` berisi penanda id soal
  (`Q-Txx-nnn`, 17 id berbeda) lalu bocor ke paket rilis. Akar di skrip hulu era ekstraksi;
  masuk lewat merge tanpa saringan.
- Gerbang permanen di SKRIP MERGE (bukan hanya laporan): scan pola
  `Q-(T[1-4]|TRAP)-[0-9]{3}` atas SEMUA berkas paket (jsonl, md, SKILL.md, dst), bukan hanya
  register.md; nol temuan sebelum serah; output grep mentah ditempel di laporan.
- Remediasi scoped-exact: buang penanda hanya dari field catatan di HULU (byte-identik di luar
  catatan), merge ulang ke versi baru; verifier menguji sha bank soal tak berubah (`exam_key`
  stabil sepanjang seluruh siklus perbaikan) + byte-identik baris GAP di luar catatan.
- PITFALL AUDIT CONTROLLER: spot-check merge yang hanya memeriksa jumlah baris/sidik/kutipan
  LOLOS kebocoran ini. Uji controller wajib menyertakan scan penanda LINTAS FIELD lintas
  berkas, bukan hanya field beban-rilis.

## Uji tandingan controller atas perbaikan hulu (batas bawah, bukan vonis)

Sebelum melepas run-3, controller menguji sendiri: dari soal yang run-2 divonis <3, berapa yang
jawaban run-3 kini memuat angka kunci (parse angka dari key, cek kemunculan dinormalisasi di
jawaban). Hasil 10/24 pulih = bukti celah GAP termanfaatkan. Angka ini BATAS BAWAH: parser
controller punya batas sendiri (desimal koma `14,8` vs kunci `14.8`) — vonis tetap hak juri,
laporkan sebagai pembanding. Field register paket = `reg_id` (bukan `id`; salah nama field
melaporkan 'reg hilang' palsu).

## Penutup rantai L2 (distribusi + countersign)

- Audit distribusi oleh controller: pemindaian rekursif menemukan SEMUA salinan paket (target
  12 = registry fleet + profil sasaran), sidik register identik byte per salinan, scan pola
  penanda soal di seluruh berkas tiap salinan = nol, nol salinan liar, nol versi lama tertinggal.
- Countersign menuntut tabel VERIFIKASI-AKURASI populasi penuh (SPK-002 gerbang 5): entity-match
  1341/1341 bad=0, SALAH-TARGET=0, uji kutipan 100% populasi, dua rute independen side-by-side
  AGREE. Vonis FAIL run lama (run-2, REVERIF3) diarsipkan utuh sebagai jejak remediasi, tidak
  dihapus dari kontrak.

## Push rilis ke repo mirror (gsp-agent)

Mirror skill + kontrak misi ke `hermes-home/` repo (ikut sync script pola `sync_gsp_agent.py`):
salin registry fleet -> repo, kecualikan korpus PDF besar (55 MB di sini), scan secret pada
staged-diff sebelum commit, CHANGELOG baris pointer, push lalu verifikasi `git ls-remote origin
main == HEAD`. Papan misi: tutup dengan hitungan `TERBUKA: 0` via `list --json` (bukan klaim).
