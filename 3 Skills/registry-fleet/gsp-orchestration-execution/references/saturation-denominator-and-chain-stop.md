# Saturation denominator, chain-stop, CONF/DELTA mechanics (preseden misi manual AI, 04-10-2026)

Sumber: Decision Log D-11..D-14 di `docs/2026-10-04-<misi>-ai-manual/CONTRACT.md`.
Memperluas `references/saturation-gate-sweep-lanes.md` (vonis per lajur) dan
`references/worker-offensive-logic.md` (ladder 8 kelas jalur).

## 1. Masalah denominator (kenapa lanskap terbuka tidak pernah jenuh)
- Rumus "dua siklus berturut fakta baru < 10 persen" mengandaikan DENOMINATOR panen
  terdefinisi. Pada korpus terbuka (lanskap produk, kebijakan cepat berubah) setiap
  fakta baru apa pun dihitung -> panen tidak pernah turun; satu lajur tetap 41,7%
  setelah 5 siklus karena gelombang rilis produk baru memang tidak pernah berhenti.
- Gejala empiris: resume mata-2/mata-3 justru menaikkan panen lagi (satu lajur 50%
  lalu 20,8%; satu lagi 19% lalu 8%). Ini BUKAN kegagalan pekerja - ukurannya yang
  tidak berbatas. Vonis buntu/tanpa-ujung melarang penutupan; kerja terus membakar
  anggaran.

## 2. Kontrak cakupan lajur (KONTRAK CAKUPAN LAJUR) - pola putusan D-12
-/controller mendefinisikan per lajur: butir kontrak = kelas fakta yang dijanjikan
  bab/buku ke pembaca. WAJIB turunan klausus scope yang SUDAH disetujui user
  (mis. "perwakilan terpilih per kelas" vs "sensus produk") - bukan karangan worker
  di tengah run.
- Panen dipisah dua kelas saat dicatat: IN-SCOPE (mengisi butir kontrak; dihitung
  untuk saturasi) vs OUT-OF-SCOPE (perian di luar kontrak; append ke register
  kandidat lampiran - tidak dibuang, tidak dihitung).
- Ambang TIDAK berubah (tetap <10 persen, dua siklus, tafsir ketat); yang dibatasi
  hanya SATUAN UKUR panen. Sampaikan eksplisit ke pekerja/verifier bahwa ini bukan
  pelonggaran - preseden D-16 IPDR: pelonggaran CHECK demi lulus selalu ditolak.
- Vonis sah dua macam: JENUH (kontrak penuh bukti primer+entity-match DAN dua siklus
  IN-SCOPE <10%) ATAU CAKUP-PUTUSAN-<id-putusan> (kontrak penuh; sisa panen seluruhnya
  OUT-SCOPE; angka kedua kelas dilaporkan terpisah).
- Guardrail audit verifier (vonis FAIL bila): kontrak dilebarkan SEBELUM vonis; panen
  wajib disembunyikan di register OUT; kontrak tidak berasal dari klausus scope sah.

## 3. Tafsir KETAT rumus dua-siklus (preseden D-11)
- "Dua siklus berturut < 10 persen" = MASING-MASING siklus individu < 10 persen.
- Jendela gabungan antar-siklus TIDAK sah (rata-rata gabungan 9,1% dari siklus
  10,0%+8,2% = cacat). Siklus tepat 10,0% TIDAK lolos (tanda < ketat).
- Klaim JENUH pekerja via jendela gabungan WAJIB diturunkan controller ke
  BELUM-JENUH + kartu siklus konfirmasi. Preseden: satu lajur diturunkan lalu
  menjadi JENUH sah lewat rantai-2 terikat kontrak - penurunan tidak mahal,
  pelulusan cacat mahal.

## 4. Aturan henti rantai (mata-3)
- Rantai resume maksimal 3 mata per garis kartu (norma LAD). Di mata-3 pekerja
  menutup JUJUR dengan angka dan TIDAK meminta mata-4; keputusan langkah berikutnya
  (rantai baru terikat kontrak, vonis CAKUP, atau berhenti sebagai tagihan verifier)
  adalah putusan controller.
- Bila lajur sungguh butuh siklus lagi: buka RANTAI BARU dengan ikatan berbeda
  (mis. rantai terikat kontrak cakupan menggantikan panen tak-terbatas), bukan
  memperpanjang rantai lama melewati mata-3.

## 5. Mekanika kartu CONF (konfirmasi penutup)
- Kondisi lepas: siklus terakhir sudah <10 persen IN-SCOPE tapi rantai putus karena
  siklus sebelumnya. Buat kartu "CONF-N" = 1-2 siklus bersih per kelompok lajur,
  parents = kartu terakhir lajur, edge ke kartu sintesis.
- Kelompokkan CONF berdasar SISA SIKLUS (1-siklus vs 2-siklus vs lajur berat sendiri),
  bukan berdasarkan wave asal - hemat kartu dan kap aktif.
- Tagihan lintas-lajur (koreksi cacat hulu yang ditemukan satu lajur, mis. ID paper
  warisan salah) ditempel ke kartu CONF yang menyentuh berkasnya + komentar wajib
  ke kartu sintesis.

## 6. Edge semu late-linked: penanganan start-dini kartu hilir (berulang, kini ada resep)
- Fakta terkonfirmasi dua kejadian: parent yang di-LINK setelah kartu dibuat TIDAK
  menahan promosi. Kartu hilir (sintesis) yang dibuat sebelum semua edge hulu terpasang
  akan RUNNING dengan input sebagian.
- Resep yang diterima (D-14): biarkan kartu hilir jalan sebagai DRAF, lalu buat kartu
  DELTA (parents = hilir + semua hulu final) yang mengintegrasikan vonis final;
  GERBANG fase berikutnya dilarang rilis sebelum DELTA done.
- Pencegahan: buat kartu hilir PALAH AKHIR dengan parents=[...] inline saat create
  (bukan link susulan), atau tunda create hilir sampai semua hulu terminal.

## 7. Fallback rung-8 render JS saat daemon browser tidak tersedia (resep terverifikasi)
- Daemon browser-harness bisa mati (DevToolsActivePort hilang; sesi default dan named
  sama-sama gagal). Controller mengukur SEKALI (2 percobaan), lalu JANGAN membakar
  iterasi worker pada percobaan ulang - sematkan teks fallback di body kartu riset dan
  laporkan T6 ke user (restart layanan wewenang user).
- Pengganti render JS TERBUKTI di host Windows ini:
  `"C:/Program Files/Google/Chrome/Application/chrome.exe" --headless=new --disable-gpu --dump-dom --virtual-time-budget=15000 "<URL>" > C:/Users/TRIAL/Temp/<run>/dom_<slug>.html`
  lalu parse DOM dari berkas. Sekunder sah: curl + cookie jar; CDX/archive.today
  (label PROV). export.arxiv.org 429 persisten -> halaman arxiv.org/abs/.
- CATATAN: ini resep fallback, BUKAN vonis "browser tool rusak permanen" - cek daemon
  segar di awal misi berikutnya.

## 8. Pembuatan kartu batch idempoten + pemulihan crash
- Skrip pembuat kartu yang crash di tengah meninggalkan kartu SUDAH terbit. Pemulihan:
  query board (`list --json`, filter prefiks judul misi), panen id "Created" dari papan,
  perbarui register JSON, buat HANYA kartu yang belum ada. Dilarang rerun seluruh
  skrip buta (duplikat gelombang = preseden tabrakan 03-09).
- Kunci register pakai slug persis ('1a-R'), jangan dinormalisasi ('1ar') - KeyError
  setelah sebagian kartu terbit adalah jebakan ganda (crash + restart berisiko duplikat).
- Body/komentar multi-baris ke CLI native: subprocess dengan ARGMEN LIST
  (`["hermes","kanban","comment",id,body]`), bukan string shell - quoting shell pecah
  pada newline ("The system cannot find the file specified").

## 9. Registrasi scope gerbang IL untuk misi yang menyetor proposa
- `scripts/il_ingest/scopes.json` beku (ILFIX-0927); gate.py kolektor menolak proposa
  di luar scope aktif -> pekerja benar menutup dengan KEPUTUSAN DIBUTUHKAN (jalur sah).
- Putusan registrasi milik controller (catat di Decision Log); EKSEKUSI milik
  gsp-librarian: revisi GS sesuai spec + gate_version naik, selftest.sh exit 0,
  KONTROL MERAH pada scopes lama (semua tetap tertolak) + hijau pada baru, dokumen
  keputusan di folder misi.
- Registrasi gate BUKAN promosi: vault->wiki tetap wewenang librarian di fase serah.

## 10. Delivery cron dari sesi WebUI
- Job dibuat dari sesi WebUI: `deliver='origin'` resolve ke platform 'webui' yang tidak
  dikenal gateway (temuan: last_delivery_error "unknown platform 'webui'" pada job
  saudara). Set `deliver='local'` untuk board-mover/watchdog; jejak fase tetap hidup di
  PHASE-REPORTS.md kontrak, jadi tidak ada laporan yang hilang.
