# Kartu DELTA kesegaran - operasionalisasi R-10 (sumber: EKASLAP-1006, 06-10)

## Kapan berlaku
Misi hilir yang membangun deliverable di ATAS lapis sapuan/digest terverifikasi yang
berumur (mingguan/bulanan) sementara rak sumber bisa saja berubah setelah sapuan.
R-10 (knowledge-baseline-architecture.md) memerintahkan cek kesegaran; berkas ini
adalah mekanismenya: vonis per-berkas oleh kartu DELTA, bukan dugaan hilir.

## Prosedur controller (SEBELUM kartu inventaris/bab manapun)
1. Ukur selisih sendiri, jangan delegasi ukur pertama:
   `find <akar-rak> \( -name "*.md" -o -name "*.csv" \) -newermt "<tanggal-sapuan>"`
   -> simpan hasilnya sebagai `REGISTER-KESEGARAN-<misi>.txt` di folder kontrak.
2. Cetakan alat pembanding kunci (populasi berkas, total baris, baris register,
   penanda struktur seperti jumlah domain berrantai) vs angka klaim hulu.
   Jangan percaya salah satu lapis tanpa ukur.
3. Lepas kartu DELTA (assignee = analis domain; paralel dengan RT/TA, tanpa edge ke
   keduanya): instruksi vonis PER BERKAS TETAP / BERUBAH (sebut baris bukti) / BARU,
   dibandingkan digest hulu + kutipan indeks; output `sweep/DELTA-<slug>.md` tabel
   `DELTA-n | berkas | aspek | vonis hulu | keadaan kini (bukti baris) | dampak`.
   Rak tetap READ-ONLY.
4. RANTAI SEMUA kartu konten hilir dengan `parents=[DELTA]` sejak kanban_create, dan
   tempel di tiap prompt: "butir BERUBAH/BARU DELTA menang atas digest".
5. Bekukan baseline dan catat di Decision Log kontrak: "baseline = keadaan disk
   tanggal X, koreksi DELTA menang atas lapis lama; edisi lebih baru belum
   terjangkau" - pernyataan ini wajib ikut terbit di dokumen akhir (metode/gerbang beku).

## Fakta penting yang terukur (EKASLAP-1006)
- 35 dari 254 berkas rak ber-mtime > tanggal sapuan; populasi naik 254->256 berkas,
  baris 17.472->17.937; rantai jaminan 12/20 -> 14/20 domain (BUILDING-CONSTRUCTION
  dan CONSTRUCTION lahir pasca-sapuan).
- mtime BUKAN bukti perubahan isi: MRR di-touch 05-10 tetapi tetap 62 baris dengan
  sebaran R dan otoritas identik; GAP tetap 21 baris. Pemisahan delta nyata vs
  penormaan-format hanya bisa lewat pembacaan isi (kartu DELTA), bukan statistik berkas.
- Vonis "tidak ada di rak" hulu bisa basi sebagian: daftar domain tanpa rantai harus
  dihitung ulang terhadap disk, bukan dikutip dari indeks.

## Steering user di tengah misi (kelas T4) - cara serap
Jawaban user atas pertanyaan kesegaran/klarifikasi yang berbunyi "Lanjutkan" +
penekanan bentuk ("Buat Document Lengkap dengan susunan administrasi komprehensif"):
- "Lanjutkan" = persetujuan baseline beku keadaan kini -> catat sebagai putusan D-n
  di Decision Log kontrak SEBELUM kartu hilir berikutnya dibuat.
- Penekanan yang muat dalam arsitektur yang sudah ada = perkuat prompt kartu yang
  BELUM dilepas (mis. blok muka/lembar kendali/routing/register/lembar verifikasi
  di kartu BLOK), JANGAN run ulang TA; run ulang TA hanya bila penekanan mengubah
  kerangka (anatomi/DAG).
- Jejak: nomor putusan dirujuk di frontmatter/badan artefak hilir agar verifier bisa
  menguji kesesuaian.

## Pitfall teknis
- Inventaris unit berformat delimiter pipe (`|`) - pembacaan `csv.DictReader` tanpa
  `delimiter='|'` memberi KeyError kolom; cek header mentah sebelum analisis.
- Sebelum menulis daftar diff ke kontrak (mis. domain mana yang baru berrantai),
  verifikasi daftar dengan cetakan alat (loop `[ -f ... ]`) - menyebut nama salah di
  kontrak lalu menambalnya = jejak cacat; angka laporan = cetakan alat giliran itu.
- Monitoring gelombang: loop bash `while ... hermes kanban list --json ... sleep 60`
  dengan background=true + notify_on_complete=true membangunkan controller saat N
  kartu menutup; alternatif siap-pakai: `scripts/watch_cards.py` skill ini.
