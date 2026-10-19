# Denominator saturasi & gerbang penulis/rakit (preseden RAFAI-1004, 04-05/10/2026)

Sumber: misi buku manual AI (riset 16 lajur jenuh -> tulis 18 bab -> verifikasi -> rakit). Semua angka di sini cetakan alat pada giliran itu, bukan narasi worker.

## 1. Masalah denominator vonis jenuh -> KONTRAK CAKUPAN per lajur (D-12)

Rumus "dua siklus berturut fakta baru < 10 persen" macet pada lajur berkorpus terbuka (lanskap produk AI) karena DENOMINATOR tak terdefinisi: fakta baru apa pun dihitung, panen tidak pernah habis (terukur: R1 siklus-final masih 11,5 persen karena menutup gap bernama; R8 64,7 persen karena gelombang rilis model 2026).

Solusi sah (putusan controller, BUKAN pelonggaran ambang):
- Tiap lajur dipasangi KONTRAK CAKUPAN = daftar butir bernama yang dijanjikan ke pembaca (mis. perwakilan per kelas + lisensi + model card primer), diturunkan dari scope yang sudah disetujui user di gerbang persetujuan (CP-A).
- Panen dipisah dua kelas saat dicatat: IN-SCOPE (mengisi butir kontrak) vs OUT-OF-SCOPE (append ke register lampiran, tidak dibuang, tidak dihitung sebagai panen wajib).
- Vonis sah: JENUH (kontrak penuh bukti primer+entity-match DAN dua siklus berturut MASING-MASING IN-SCOPE < 10 persen) ATAU CAKUP-PUTUSAN (kontrak penuh DAN sisa panen seluruhnya OUT-OF-SCOPE; angka dua kelas dilaporkan). Keduanya diaudit verifier terhadap scope yang disahkan user.
- Perubahan satuan ukur WAJIB diumumkan sebelum siklus jalan, tidak retroaktif. Verifier memvonis FAIL bila kontrak dilebarkan SEBELUM vonis atau panen wajib disembunyikan di register.
- Lajur berpanen struktural tinggi (ekosistem rilis) boleh diukur atas butir kontrak named; ini penafsiran konsisten "perwakilan, bukan sensus" - bukan trik.

## 2. Tafsir KETAT rumus dua-siklus (D-11) + DEFECT-R3-2

- Dua siklus berturut MASING-MASING < 10 persen; siklus tepat 10,0 persen TIDAK lolos; jendela gabungan (menggabung dua siklus jadi satu persentase) tidak sah. Vonis "JENUH-bersyarat" yang memakai trik jendela diturunkan controller, lalu dikasih siklus konfirmasi (preseden R3: JENUH lama gugur -> BELUM JENUH -> rantai-2 terikat kontrak -> JENUH final 24,5 persen lalu 8,2 persen).
- Dua siklus dalam SATU run kartu SAH bila tiap siklus punya probe+timestamp+kanal berbeda tercatat di berkas.
- DEFECT-R3-2 (uji wajib semua vonis JENUH): siklus konfirmasi yang memakai ulang kanal lama menghasilkan 0 persen yang BUKAN bukti kejenuhan - siklus konfirmasi wajib menyentuh KANAL BARU. Verifier menguji ini per lajur di gerbang jenuh.

## 3. Aturan henti rantai (partial-handoff bukan rantai tanpa batas)

- Maksimal 3 mata rantai; setelah itu kartu menutup jujur dengan angka dan TIDAK meminta mata-4 - keputusan rantai berikutnya milik controller.
- Opsi henti controller: JENUH disahkan / CAKUP disahkan (cek definisi terhadap angka dua kelas) / satu siklus final lagi / KNOWN-GAP-BERLABEL (gap dicetak jujur di bab + tanggal potong; BUKAN vonis buntu).
- Menolak permohonan CAKUP saat panen sisa masih IN-SCOPE = penerapan "pelonggaran CHECK demi lulus SELALU ditolak" (preseden IPDR D-16). Sajikan penolakannya dengan definisi + angka.

## 4. Reviewer crash-loop saat penulis menutup via request_review (mekanika kanban)

Rantai kegagalan nyata (kartu tulis TB4): penulis menutup dengan `kanban_request_review` -> kartu masuk state `review` -> dispatcher spawn run reviewer -> tool request_review milik reviewer DITOLAK kernel ("task is not in running/ready atau expected_run_id tidak cocok") karena kartu sudah di state review dan run_id lingkungan tak cocok -> run reviewer mati ~60 detik, limit dispatcher 2 habis gave_up -> kartu `blocked` tanpa run aktif. Artefak tetap aman; kebuntuan kelas life-cycle (T6), bukan konten.

Norma kerja (pola yang berhasil di misi ini):
1. Penulis menutup LANGSUNG dengan result `STATUS: complete | ...` atau `STATUS: needs-review` - TANPA request_review dari run penulis.
2. Verifikasi penulis != editor ditegakkan di LEVEL KARTU: pass editor = kartu terpisah (assignee akun berbeda) dengan parents eksplisit ke kartu penulis - bukan lewat transisi review.
3. Kartu blocked/needs-review: asignor (controller) menutup dalam 1x24 jam sesuai aturan 10 - force-done dengan bukti terukur ATAU request-changes dengan instruksi konkret yang dipindah ke kartu FIX (artefak beku dirujuk sha). Ditolaknya force-done saat ada check gerbang merah adalah keputusan yang benar, bukan kemacetan.

## 5. Gerbang fase rakit yang terbukti menangkap blok-rilis

- Vision QA dijalankan pada HALAMAN RITERENDER dari PDF/DOCX rilis, bukan hanya PNG sumber. Yang tertangkap: garis penunjuk anotasi menunjuk objek salah di screenshot (cacat semantik, blok-rilis), dan path pipeline internal (`_work/<kartu>/fetch/...html HTTP 200`) tercetak di wajah figur lewat foot_lines generator. Norma: generator figur dilarang menaruh jejak fetch internal di lapisan terbit; caption/marker chain `marker badan == manifest == registry` delta-0 adalah gerbang deterministik murah - jalankan SEBELUM rakit, dan setiap tambalan disengaja dicatat dengan sha lama->baru.
- Scanner agregat C-14 (gagasan ditulis ulang) menangkap dua kelas nyata: (a) kalimat tagihan antar-artefak review yang seragam templat ("Jawab CEK DIRI Bab X butir Y.") - nomor butir tetap, variasi struktur kalimatnya; (b) prosa bab mengulang verbatim baris "Pesan:" caption figur - sunting SATU sisi (prosa jadi rujukan, caption tidak diubah).
- Putusan kanal untuk lampiran tabel-register: indikator panjang-kalimat (C-6) dirancang untuk prosa; sel data/register tunduk kanal doc, bukan plafon prosa kitab. Putuskan dan CATAT di Decision Log (jangan diam-diam melunakkan, jangan pula memaksa sel data jadi tidak padat). Vonis agregat scanner tetap gerbangnya.
- Catatan kesegaran jejak dari verifier rakit: sebagian FAIL run pertama ternyata cacat INSTRUMEN (membaca w:shd padahal kanvas = w:background; pencacah menghitung entity-escaped; needle ditulis dari ingatan; dedup membandingkan caption dengan dirinya sendiri). Fail gerbang diverifikasi ulang terhadap artefak hidup sebelum jadi temuan; laporan memisahkan "cacat alat dikoreksi" vs "temuan bertahan".

## 6. Keputusan user timeout -> default reversibel (pola V-D)

Form klarifikasi ber-tenggat bisa kedaluwarsa tanpa jawaban. Jalur yang benar: controller memilih DEFAULT REVERSIBEL dan mencatatnya (mis: angka belum terukur di perangkat user terbit dengan label [estimate]+known-gap; kutipan sensitif tetap di draf ber-status "belum disetujui penerbit"; bagian legal dengan formula kutipan+tanggal tanpa simpulan hukum + catatan colophon "menunggu persetujuan penerbit"), lalu mengajukan ulang checkpoint ringkas sebelum langkah ireversibel (ekspor final). DILARANG mengklaim persetujuan yang belum diberikan.

## 7. Render JS jalur rung-8 tanpa daemon browser (resep positif)

Saat daemon browser-harness tidak naik (DevToolsActivePort tidak ditemukan; sesi default dan named sama-sama gagal), jalur render sah yang TERBUKTI jalan di host Windows: `"C:/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu --dump-dom --virtual-time-budget=15000 "<URL>" > C:/Users/<user>/Temp/<slug>.html` lalu parse DOM dari berkas. Cadangan: curl + cookie jar, CDX/archive.today (label PROV), arxiv.org/abs langsung bila export.arxiv 429. Worker dibekali resep ini + larangan membakar iterasi mencoba daemon mati; controller membukukan sebagai blocker T6 lingkungan dengan mitigasi, bukan vonis buntu lajur. (Catatan: ini resep fallback, bukan vonis permanen bahwa tool browser tidak bisa dipakai - pulihnya daemon mengembalikan jalur utama.)

## 8. Register kartu idempoten saat batch-create

Skrip pembuat kartu batch (via lad_card.py) WAJIB parse id dari stdout tiap create dan menulis register JSON SETELAH tiap kartu (append-per-kunci), bukan sekali di akhir - crash di tengah loop (KeyError, dsb.) membuat sebagian kartu sudah lahir di papan; register parsial + query judul papan 60 menit terakhir mencegah duplikat gelombang saat re-run.
