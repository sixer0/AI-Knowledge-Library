# Saturation lane-contract denominator (pola RAFAI-1004, 04-10-2026)

Vonis jenuh lajur riset domain terbuka (lanskap AI, pasar alat, ekosistem model) TIDAK
pernah tercapai dengan rumus mentah "dua siklus berturut < 10 persen" karena
DENOMINATOR tidak terdefinisi: fakta baru apa pun dihitung dan domain terbuka tidak
pernah berhenti memunculkan fakta. RAFAI-1004 membuktikan ini secara empiris
(lajur R3 memanen 54,5% lalu 44,1% per siklus sebelum pola ini dipasang; setelahnya
JENUH dalam dua siklus).

## Kontrak cakupan lajur (satu paragraf per lajur, ditulis SEBELUM siklus konfirmasi)
- Isi: butir kelas yang DIJANJIKAN ke pembaca per bab (mis. "7 kelas coding assistant,
  >=2 perwakilan per kelas dengan fitur+harga+batas terverifikasi primer").
- Sumber legitimasi: turunan SAH dari scope yang disahkan user di gerbang persetujuan
  (mis. keputusan "perwakilan terpilih per kelas; sensus hanya di Lampiran A").
- Fakta yang mengisi butir kontrak = IN-SCOPE. Fakta lain = OUT-OF-SCOPE -> append ke
  register kandidat lampiran (TIDAK dibuang, TIDAK dihitung sebagai panen wajib).
- DILARANG: melebarkan/menyempitkan kontrak SETELAH siklus berjalan demi vonis;
  menyembunyikan panen wajib di register OUT. Verifier mengaudit kontrak vs putusan
  user saat gerbang jenuh.

## Tafsir KETAT rumus dua-siklus (preseden D-11; pelonggaran CHECK selalu ditolak)
- Dua siklus berturut MASING-MASING < 10 persen; siklus tepat 10,0% TIDAK lolos.
- "Jendela gabungan" (rata-rata dua siklus) TIDAK sah - vonis JENUH berbasis jendela
  gabungan harus diturunkan dan diberi satu siklus konfirmasi bersih.
- Dua siklus dalam satu run kartu SAH bila tiap siklus punya probe+timestamp+kanal
  BERBEDA yang tercatat di berkas.

## Uji DEFECT-R3-2 (kanal baru)
Siklus konfirmasi yang memakai ulang kanal lama menghasilkan 0 persen yang BUKAN bukti
kejenuhan. Setiap siklus konfirmasi wajib menyentuh kanal yang belum pernah tersapu di
lajur itu; verifier menguji ini per lajur saat audit vonis.

## Kanal vonis sah (pekerja tidak pernah memvonis final sendiri)
- `USULAN JENUH` ber-angka (dua siklus + kumulatif + register) -> controller mengesahkan
  lewat vonis di Decision Log; bukan pelunakan, bukan pengulangan defect.
- `CAKUP-PUTUSAN` -> sah hanya bila kontrak penuh DAN panen sisa seluruhnya OUT-OF-SCOPE.
  Panen sisa yang masih IN-SCOPE (mis. penutup gap bernama) = DITOLAK untuk CAKUP.
- `KNOWN-GAP-BERLABEL` -> rantai habis, angka terbuka, label gap jujur naik ke naskah
  (tanggal potong + catatan bab). Ini BUKAN vonis buntu.
- Aturan henti rantai: maksimal 3 mata per rantai; setelah itu controller menjatuhkan
  vonis akhir (sahkan / satu siklus final / known-gap) - bukan mata tanpa batas.
  Pekerja menutup partial-handoff TANPA meminta mata berikutnya.

## Launched-but-live domains (ekosistem model, harga)
Untuk lajur yang panen didominasi gelombang rilis DI DALAM kelas kontrak, satuan siklus
berikutnya boleh dihitung atas BUTIR KONTRAK NAMED (perwakilan per kelas + lisensi +
model card) + gap bernama; entri rilis yang tidak menambah butir kontrak = OUT-OF-SCOPE.
Wajib DIUMUMKAN sebelum siklus jalan (tidak retroaktif) dan diaudit verifier.

## Render rung-8 tanpa daemon browser interaktif
Bila daemon browser-harness tidak hidup (DevToolsActivePort hilang), jalur TERBUKTI di
host ini: `"C:/Program Files/Google/Chrome/Application/chrome.exe" --headless=new
--disable-gpu --dump-dom --virtual-time-budget=15000 <URL> > dom.html` lalu parse DOM;
cadangan sah: curl + cookie jar, CDX/archive.today (label PROV). `export.arxiv.org`
429 persisten -> pakai `arxiv.org/abs/<id>`. Worker dilarang membakar iterasi pada jalur
daemon yang mati; tempel blok jalur ini di setiap kartu riset yang butuh rung-8.

## Sapuan cacat hulu populasi-penuh
ID rujukan warisan yang salah (mis. arXiv ID keliru) disapu ke SEMUA berkas lajur dengan
register koreksi per-lokasi + scanner pembukti 0 kemunculan di luar kalimat koreksi.
Koreksi konstanta terukur (mis. bytes/param) menggantikan aturan lama di SEMUA turunan
(rumus kapasitas, speks bab); naskah mengikuti berkas lajur, speks ikut dikoreksi ke lajur.

## Gerbang ingest IL sebelum proposa worker
Sebelum worker menyetor proposa pengetahuan, scope misi HARUS terdaftar di scopes.json
gerbang IL (revisi GS + gate_version naik + selftest + kontrol merah pada scopes lama) -
eksekusi milik librarian atas putusan controller; worker mencatat exit code gate.py per
batch. Penolakan kelas "di-luar-lingkup-kajian" = sinyal controller, bukan kegagalan worker.

## Gate persetujuan user yang timeout
Form keputusan yang kedaluwarsa tanpa jawaban: ambil DEFAULT REVERSIBEL (postur netral
yang sudah tertanam di naskah/artefak), catat sebagai putusan controller di Decision Log,
BUKAN meloloskan gerbang; ajukan ulang sebagai checkpoint ringkas SATU kali sebelum titik
no-return (mis. ekspor final). Label "belum disahkan penerbit" ikut tercetak bila perlu.

## Alat bantu
`scripts/watch_cards.py` - penunggu status terminal sejumlah kartu kanban; jalankan via
terminal(background=true, notify_on_complete=true) agar controller tidak polling buta.
