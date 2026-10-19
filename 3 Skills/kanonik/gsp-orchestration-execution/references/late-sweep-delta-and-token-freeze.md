# Delta-Segaran dan Pembekuan Register (preseden EKASLAP-1006, 06-10)

Dua mekanik yang terbukti jalan saat menyusun dokumen besar dari korpus yang
SUDAH pernah divonis jenuh di misi sebelumnya, plus pitfall mekanik giliran itu.

## 1. Gerbang R-10 operasional: ukur delta-mtime sebelum delegasi hilir

Bila basis konten adalah lapisan terverifikasi terdahulu (digest/sapuan/vonis
sebelumnya), JANGAN langsung percaya lapisannya masih segar. Resep controller:

1. `find <akar> \( -name "*.md" -o -name "*.csv" \) -newermt "<tanggal-sapuan-hulu>"`
   -> simpan hasil sebagai REGISTER-KESEGARAN di folder kontrak (path nyata).
2. Ukur sendiri angka-angka kunci yang dikutip hilir (jumlah berkas, baris,
   sebaran register, jumlah rantai) dengan parser, BUKAN dari ingatan hulu.
   Temuan preseden: populasi naik 254->256 berkas, rantai 12/20->14/20 domain,
   sementara register induk berubah-mtime-tetap-isi (mtime baru, sebaran identik).
3. Lepas SATU kartu DELTA (assignee analis domain) sebelum kartu inventaris/bab:
   bandingkan per berkas vs digest hulu, vonis TETAP/BERUBAH/BARU per butir,
   format tabel `DELTA-n | berkas | aspek | vonis hulu | keadaan kini (bukti baris) | dampak`.
4. Kartu hilir (inventaris unit, bab) WAJIB menyebut "butir BERUBAH/BARU DELTA
   menang atas digest" di body-nya, dan edge parents DELTA dipasang di
   `kanban_create` sejak awal (bukan link susulan).
5. Pertanyaan kesegaran ke user (R-10a) boleh dijawab "Lanjutkan" -> Decision
   Log mencatat baseline dibekukan pada KEADAAN DISK hari itu + instruksi
   tambahan user ikut jadi keputusan D-n.

## 2. Pembekuan register angka (SPINE): larangan tokenisasi buta

Preseden: penulis bab menulis literal ber-sitasi (C2/C5) sementara bab lain
sudah token-level. Kartu SPINE membekukan 577 entri + sha16 + sebaran tanda
asal TERHITUNG alat, hard-stray 0 - tetapi MENOLAK mengganti string literal ke
token per-kejadian, dan itu keputusan benar yang wajib ditiru:

- Satu string bisa membawa DUA makna per kejadian ("1.000" = 1.000 V sekaligus
  1.000 MOhm pada baris tabel berbeda; "0,5" = DoD sekaligus M_terproteksi).
  Penggantian buta string-ke-token = risiko salah-ikat, melanggar AKURASI MUTLAK.
- Jalur sah: bekukan NILAI ke register di kartu SPINE (model-dulu terpenuhi di
  level nilai), suntingan per-kejadian jadi KARTU LANJUTAN terpisah ber-parent
  ke SPINE (FIXTOKEN), assignee = penulis bab asal; kartu rakit hilir diberi
  catatan controller: pakai sha16 EMIT TERBARU bila register berubah, catat
  keduanya di result.
- Verifikasi pembekuan pakai pola: hitung ulang `len(Register.d)` independen,
  assert jumlah sebaran tanda asal = total entri, klasifikasi kemunculan angka
  di luar known-set (anchor-sitasi / enumerasi-chain / konstanta desimal >3
  ber-izin manual tercatat) alih-alih memaksa semuanya masuk register.

## 3. Pitfall mekanik giliran ini

- **Watchdog papan di terminal background**: `hermes kanban list --json`
  sesekali mengembalikan kuaran KOSONG; `json.load(sys.stdin)` melempar
  JSONDecodeError dan loop watchdog mati dengan alarm palsu "blocked". Pola
  sah: bungkus `try: ts=json.load(sys.stdin) except Exception:
  print('READ_FAIL'); sys.exit(0)` dan hanya tandai BAD untuk status
  `blocked/review/archived` yang NYATA dibaca dari kuaran valid.
- **Karakter `&` dalam body kartu via heredoc terminal**: alat terminal menolak
  perintah yang mengandung `&` sebagai "backgrounding" bahkan di dalam teks
  heredoc - gagal total meski maksudnya bukan shell. Tulis body prompt dengan
  `write_file` (atau hindari `&`; ganti "dan"/"plus").
- **Field `parents` di `list --json` tampil None** meski edge link susulan
  menahan promosi (kartu tetap `todo`). Jangan vonis "tanpa edge" dari list;
  status `todo` vs `ready` setelah `link` adalah bukti edge bekerja.
- **CSV inventaris ber-delimiter pipe**: parser hilir wajib `delimiter='|'`;
  DictReader default (koma) memberi KeyError kolom dan hitus cacat.
