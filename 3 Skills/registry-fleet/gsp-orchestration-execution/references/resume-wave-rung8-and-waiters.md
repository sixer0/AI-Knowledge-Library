# Resume-wave, audit vonis jenuh, dan rung-8 fallback (rekaman RAFAI-1004, 04-10-2026)

Normatif pelapis `saturation-gate-sweep-lanes.md` (vonis per lajur) dan
`saturation-sweep-mission-frame.md` (kerangka misi). Empat mekanik di bawah
terbukti dipakai di lapangan pada misi RAFAI-1004 fase riset.

## 1. Audit controller atas vonis JENUH pekerja (tafsir KETAT)

Rumus jenuh yang disahkan user (dua siklus berturut MASING-MASING < 10 persen
fakta baru) dibaca KETAT terhadap bunyi kanonis:
- Siklus tepat 10,0% TIDAK lolos (syaratnya "<", bukan "<=").
- "Jendela gabungan" dua siklus (mis. 2/22 = 9,1% gabungan dari siklus 10,0%
  lalu 8,3%) TIDAK sah sebagai pengganti dua-siklus-masing-masing.
- Vonis pekerja berlabel "JENUH-bersyarat" = PERMOHONAN PUTUSAN ke
  controller/verifier, bukan vonis final; syarat yang belum lengkap dicatat
  sebagai tagihan, tidak dilunakkan.
Prosedur controller saat menemukan klaim jenuh meragukan: (a) putuskan tafsir
sebelum menular ke hilir, tempel di Decision Log kontrak; (b) turunkan vonis
yang cacat tafsir; (c) untuk lajur yang tinggal butuh satu siklus konfirmasi,
terbitkan kartu mata-3 TERAKHIR khusus siklus konfirmasi (bukan perluasan
lingkup); (d) bila mata-3 tetap BELUM JENUH, lajur berhenti di sana dan menjadi
tagihan verifier di gerbang sintesis - dilarang membuka mata ke-4.
Preseden: D-11 RAFAI-1004 (vonis JENUH R3 via jendela gabungan diturunkan,
kartu mata-3 khusus terbit). Selaras preseden IPDR D-16: pelonggaran CHECK demi
lulus SELALU ditolak.

## 2. Fallback rung-8 (render JS) saat daemon browser-harness tidak naik

Gejala: `browser_exec` gagal "daemon default didn't come up"; log
`~/.config/browser-harness/tmp/bu-*.log` memuat `DevToolsActivePort not found`.
Coba satu sesi bernama terisolasi untuk memastikan ini daemon-mati, bukan
tab/stale sesi (sesi named memakai daemon terpisah). Bila kedua jalur mati:
- JANGAN membakar iterasi worker pada `browser_exec`; JANGAN menulis "browser
  mati permanen" sebagai aturan - ketersediaan daemon = keadaan lingkungan,
  cek ulang tiap misi.
- Jalur render sah yang TERBUKTI jalan di host Windows ini (ukur 04-10):
  `"C:/Program Files/Google/Chrome/Application/chrome.exe" --headless=new
  --disable-gpu --dump-dom --virtual-time-budget=15000 "<URL>" >
  C:/Users/TRIAL/Temp/<slug>.html` lalu parse DOM berkas (grep/python).
  Uji cepat dengan https://example.com (cek `<title>` keluar).
- Cadangan sah lain: curl + cookie jar untuk antibot ringan, CDX/archive.today
  (label PROV), salinan dokumen resmi lain.
- Tempel resep ini di BODY kartu resume (blok "JALUR RUNG-8") beserta larangan
  mencoba browser_exec, agar tiap worker tidak menemukan ulang blocker dengan
  biaya iterasi sendiri. Catat metode render per rung di tabel LADDER.

## 3. Driver kartu resume (gelombang mata-2/3 pasca partial-handoff massal)

Bila SESEMUA kartu satu gelombang menutup `partial-handoff` sah (LAD enam
bidang di komentar), controller:
1. Baca SISA_KERJA per kartu dari komentar (`hermes kanban show <id> --json`),
   jangan dari ingatan result.
2. Bangkitkan SATU generator Python di `_work/` yang memanggil `lad_card.py`
   per kartu resume: `--parents <kartu-induk>`, tenant sama, wake-default,
   `--est` dari estimasi iterasi SISA_KERJA. Parse `Created (t_[0-9a-f]+)` dari
   stdout untuk rantai id; simpan register JSON (`_work/resume_card_ids.json`).
3. Perluas edge hilir (mis. kartu sintesis) ke SEMUA kartu resume via
   `hermes kanban link <anak> <hilir>` - edge hanya ke hulu data nyata.
4. Tagihan wajib ke kartu hilir yang belum jalan: tempel sebagai KOMENTAR kartu
   (bukan hanya di chat) agar terbaca worker. Di Windows, kirim body komentar
   lewat `subprocess.run(["hermes","kanban","comment",<id>,<body>])` (argumen
   list); shell string ber-quoting gagal ("The system cannot find the file
   specified").
5. Body kartu resume wajib memuat: larangan mengulang korpus yang ada (append
   ke berkas lajur yang sama), instruksi vonis akhir per lajur di kepala
   berkas, dan blok rung-8 (seksi 2 di atas) bila lajur menyentuh halaman
   JS-heavy.

## 4. Penunggu latar menggantikan polling in-session

Pola teruji: skrip kecil poll `hermes kanban show <id> --json` tiap 60 detik,
cetak baris status, exit 0 saat SEMUA kartu target terminal
(done/blocked/review/needs-review/canceled/archived/failed), exit 2 saat
timeout. Jalankan via `terminal(background=true, notify_on_complete=true)` -
controller bangun hanya saat gelombang menutup, tanpa makan giliran
percakapan. Alat siap pakai: `scripts/watch_cards_terminal.py`. Batas: timeout
maksimum foreground terminal ~420 detik di backend ini - penunggu >7 menit
WAJIB latar, bukan foreground dengan timeout besar. Setelah bangun: ukur
artefak di disk (stat + grep footprint), baru gerak keputusan; jangan percaya
summary kartu saja (norma L1 != selesai).
