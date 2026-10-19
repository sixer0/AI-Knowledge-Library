# Saturation denominator & review lifecycle (rekaman RAFAI-1004, 04-10-2026)

Sumber: docs/2026-10-04-rafif-ai-manual/CONTRACT.md Decision Log D-11..D-22 (vonis tercatat per butir; artefak terukur di folder itu).

## 1. Masalah denominator vonis jenuh

Rumus "dua siklus berturut fakta baru < 10 persen" tidak terdefinisikan denomina-
tornya pada lajur lanskap hidup (alat AI): fakta baru apa pun dihitung, panen tak
pernah < 10 persen (R3 memanen 54,5% per siklus tanpa batas). Solusi berjenjang
yang terbukti bekerja (R3 akhirnya JENUH dalam dua siklus):

1. Tafsir KETAT lebih dulu (D-11): dua siklus berturut MASING-MASING < 10 persen;
   siklus tepat 10,0% tidak lolos; jendela gabungan antar-siklus TIDAK sah. Vonis
   "JENUH" yang lahir dari trik jendela diturunkan oleh verifier/controller.
2. KONTRAK CAKUPAN LAJUR (D-12): tiap lajur diberi daftar butir kelas yang
   dijanjikan ke pembaca (turunan sah dari keputusan scope user - mis. "perwakilan
   terpilih per kelas, sensus hanya lampiran"). Panen dipisah dua kelas:
   IN-SCOPE (mengisi butir kontrak) vs OUT-OF-SCOPE (append ke register kandidat
   lampiran, tidak dibuang). Ambang tidak berubah; hanya SATUAN PANEN yang dibatasi.
3. Vonis sah: JENUH (kontrak penuh + dua siklus IN < 10%) ATAU CAKUP-PUTUSAN
   (kontrak penuh; sisa panen seluruhnya OUT-OF-SCOPE; angka dua kelas dilaporkan)
   ATAU KNOWN-GAP-BERLABEL (aturan henti rantai; buku memakai tanggal potong +
   label gap jujur - bukan vonis buntu).
4. Uji kanal-baru (DEFECT-R3-2): siklus konfirmasi yang memakai ulang kanal lama
   menghasilkan 0% yang BUKAN bukti kejenuhan. Semua siklus konfirmasi wajib
   menyentuh kanal yang belum tersapu, dengan probe+timestamp+kanal tercatat.
5. Dua siklus dalam satu run kartu SAH bila tiap siklus punya probe+timestamp+
   kanal berbeda tercatat di berkas (format "USULAN JENUH ber-angka" = kanal sah
   penutupan rantai; pengesahan milik controller lewat vonis, bukan oleh pekerja).
6. Lajur ekosistem terbuka (gelombang rilis model): panen dihitung atas BUTIR
   KONTRAK NAMED + gap bernama; entri rilis baru yang tidak menambah butir
   kontrak = kandidat lampiran. Metode ukur wajib DIUMUMKAN SEBELUM siklus jalan
   (tidak retroaktif) - pelebaran kontrak pasca-hasil = cacat, verifier FAIL.
7. Aturan henti rantai: setelah mata-3/kartu konfirmasi, vonis akhir milik
   controller (bukan mata tanpa batas); pekerja menutup jujur TANPA memohon mata
   lanjutan. Budget habis = partial-handoff checkpoint resume, bukan vonis.
8. Rantai riset selesai -> satu kartu sintesis DELTA mengintegrasikan vonis final
   controller ke dokumen sintesis (cadangkan v1) sebelum blueprint dirilis.

## 2. Kebuntuan life-cycle review (crash-loop reviewer)

Rantai kegagalan terukur (kartu kitab TB4): penulis menutup dengan
kanban_request_review -> kartu masuk state review -> dispatcher men-spawn
reviewer -> tool request_review milik reviewer DITOLAK kernel ("task is not in
running/ready atau expected_run_id tidak cocok") karena kartu sudah di state
review dan run_id lingkungan tak match -> run reviewer mati ~60s dua kali ->
dispatcher gave_up -> kartu blocked tanpa run aktif.

Pola kerja (standar misi):
- Penulis/editor menutup dengan RESULT teks 'STATUS: complete | ...' atau
  'STATUS: needs-review' LANGSUNG; DILARANG memanggil kanban_request_review dari
  run sendiri.
- Pass editor selalu kartu TERPISAH yang dibuat controller (assignee akun
  berbeda; penulis != editor), bukan transisi review dari kartu penulis.
- Triase bila terlanjur kena: jalur asignor = force-done dengan bukti /
  request-changes lewat kartu fix baru (pekerjaan dipindah, artefak beku dirujuk
  sha) / escalate user. force-done dengan check gerbang merah = DITOLAK
  (preseden D-16 IPDR: pelonggaran CHECK demi lulus selalu ditolak).

## 3. Edge semu & rilis gelombang

- Late-linked parents TIDAK menahan promosi (ditegaskan lagi kejadian nyata:
  kartu hilur dibuat ready lalu di-link susulan -> terlanjur RUNNING dengan hulu
  sebagian). Mitigasi: jangan link-susulan sebagai gerbang; terima draf dan
  jadwalkan kartu DELTA integrasi; atau tunda create sampai parent jelas.
- Rilis batch multi-kartu lewat skrip: bila skrip crash SETELAH sebagian kartu
  terbit, pulihkan dengan query papan berdasarkan prefiks judul SEBELUM retry
  (mencegah duplikat gelombang; preseden tabrakan 03-09/05-09), lalu lanjutkan
  hanya kartu yang belum ada dan simpan register id lengkap.
- Register id antar-gelombang: pakai kunci KANONIS (mis. '1a-P') dan baca ulang
  register sebelum skrip berikutnya - KeyError di tengah batch = sumber crash
  nyata (kejadian dua kali di misi ini).

## 4. Runge-8 render tanpa browser-harness

Bila daemon browser-harness mati (DevToolsActivePort tidak ditemukan; sesi
default dan named sama-sama gagal), jalur rung-8 sah yang TERBUKTI di host:
  "C:/Program Files/Google/Chrome/Application/chrome.exe" --headless=new \
    --disable-gpu --dump-dom --virtual-time-budget=15000 "<URL>" > dom.html
lalu parse DOM dari berkas. Cadangan: curl + cookie jar, CDX/archive.today
(label PROV), arxiv.org/abs langsung (export.arxiv.org 429 persisten).
Tempel resep ini di body setiap kartu riset hilir + larangan membakar iterasi
pada browser_exec; buka kartu OPS terpisah untuk perbaikan daemon (restart
layanan milik user = wewenang user).

## 5. Speks vs korpus lajur (adjudikasi delta)

Delta yang dilaporkan editor/pengawas (mis. 01_specs menyebut 'gpt-oss-120b'
sebagai model uji-tandingan MoE, berkas lajur R9-F26 = gpt-oss-20b) diadjudikasi
controller TERHADAP BERKAS LAJUR sebagai otoritas; speks disunting mengikuti
lajur, naskah tidak. Penemuan cacat hulu selama CONF (dua arXiv ID warisan salah;
rumus bytes/param 0,5 dikoreksi terukur 0,6131-2,0001) memicu sweep POPULASI-
PENUH lintas berkas + register koreksi per-lokasi + scanner nol-kemunculan -
pola remediasi yang wajib ditiru, bukan tambal satu titik.

## 6. Gerbang IL scope

Batch proposa riset tertolak kelas 'di-luar-lingkup-kajian' bila scopes.json
beku tidak memuat tenant misi. Jalur sah: worker membukukan KEPUTUSAN
DIBUTUHKAN; controller memutuskan; pemilik gerbang (librarian) menjalankan
prosedur revisi spec (gate_version naik, selftest + kontrol merah pada scopes
lama sebagai bukti). Worker memperbaiki cacat input agar lolos gate (bukan
melewati gate). Titipan bug alat gate (MAX_PATH nama proposa) diajukan ke
skill-manager saat closeout.
