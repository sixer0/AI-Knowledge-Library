# Mekanik Waktu, Balapan, dan Dispatch (dari AUDIT-DURASI-1010 + BURNTEST-1010, 10-10)

## 1. Pembunuh run 30 menit = kolom kartu, bukan bridge
- Fakta terukur: run `timed_out` seragam @30,2 mnt padahal jembatan HQ tidak berjalan sama sekali (nol proses node). Eksekutor pembunuh = kolom `tasks.max_runtime_seconds` (basis data papan) yang ditegakkan dispatcher gateway per profil.
- Dispatcher MEMBACA ULANG kolom secara live: menaikkan kolom pada kartu yang SEDANG berjalan membuat run lolos melewati plafon lama (bukti alamiah FG5/W9 hidup di menit 32,7 setelah kolom dinaikkan saat jalan). Jadi tambalan durasi TIDAK butuh restart server.
- Akar bawaan: skrip pembuat kartu memaku default 1800s < anggaran profil 2700s. Sudah ditambal: default 3600 + blok LIMIT parametrik (plafon/checkpoint dihitung dari --max-runtime). Verifikasi cepat: `--dry-run` lalu grep baris "ANGARAN"; cek kolom via SQL `SELECT max_runtime_seconds FROM tasks WHERE id=...`.
- Menambal massal kartu antre: UPDATE kolom WHERE status IN ('todo','ready'). Yang running pun aman dinaikkan (live-reload, bukan snapshot spawn), tapi sebutkan mekanismenya di jejak.

## 2. Protokol anti-balapan (dua worker, berkas sama)
Deteksi: log gateway profil menunjukkan DUA sesi hidup dengan pesan tugas sama, atau dua kartu running menggarap berkas identik.
Urutan tindakan (terbukti di FT2 vs FIX-FINAL):
1. Kartu yang LEBIH DULU lahir dan lebih maju = KANONIK; jangan diganggu.
2. Kartu sendiri: `reclaim` (hentikan sesi ganda), verifikasi berkas sengketa tidak tersentuh (mtime), lalu `link <kanonik> <milikku>` supaya edge hulu-data permanen menahan promosi (blok manual bisa ditolak kernel saat status berubah; edge tidak).
3. Verifikasi arah edge: `show <anak> --json` → nama kanonik harus ada di `parents`.
4. Tutup kartu duplikat dengan komentar jejak + `complete --force` bila klaim sesi masih menggantung.
- Vonis pekerja HARUS per-byte di disk (stat + sha), bukan per-status kartu — status bisa tertinggal/dahului kenyataan.
- Menutup kartu mendahului worker yang masih hidup = cacat prosedur kelas sendiri; cek log sesi sebelum close.

## 3. Notifikasi watcher tidak dipercaya buta
- Membunuh watcher (`process kill`) dapat menghasilkan notifikasi TERMINAL tertukar/terlambat yang KONTRADIKSI papan. Setiap notifikasi: ukur ulang papan + disk sebelum melapor; bila notifikasi dan papan berbeda, papan+disk menang.
- Watcher sebaiknya mencetak keadaan tiap tick (bukan hanya terminal) supaya telat-tilik bisa direkonstruksi.

## 4. Gerbang sampel-dulu (pelajaran penolakan user 10-10)
- Gerbang alat hijau != mutu karya. Untuk keluaran dibaca-manusia bermutu tinggi: tulis 1-2 bab sampel, uji RASA BUTA (penilai tanpa akses blueprint/standar, peran praktisi) SEBELUM gelombang tulis penuh dibuka. Kegagalan di sini berbiaya 2 bab, bukan 200 halaman.
- Persona pembaca adalah parameter instruksi yang WAJIB dikonfirmasikan di fase penerjemahan permintaan (RT), bukan diasumsikan dari nama pembaca.

## 5. Burn test perbaikan orkestrasi (resep B0-B4)
B0 baseline sehat (tangga beban 8/16/24 paralel ke server model via /v1/chat/completions, catat med/p90); B1 uji inti pada beban nyata (kartu tulis sungguhan di profil tujuan, target melewati plafon lama); B2 beban campur saat produksi jalan (degradasi latensi); B3 mekanika (kolom DB + render blok anggaran kartu baru + heartbeat run hidup < 2 mnt); B4 mode gagal (query crashed/reclaimed/spawn_failed; laporkan jujur bila kelas cacat masih muncul). Semua angka = cetakan alat pada giliran uji.

## 6. Friksi alat yang terbukti jalannya
- Body kartu berisi '&' memicu penahan backgrounding terminal — ganti kata "dan".
- One-liner python raksasa dalam heredoc sering ditolak parser keras — tulis skrip ke berkas dulu, lalu jalankan.
- Mereplikasi hitungan pemindai gaya (C-7 paragraf pendek): paragraf = gabungan baris non-kosong dipotong heading/tabel/blockquote/garis-pemisah/daftar; kalimat hanya pecah bila [.!?] diikuti spasi lalu HURUF KAPITAL. Cara persis: import modul scanner, pakai `sentences_of`-nya. Daftar bullet pendek dihitung SATU paragraf — pada kanal doc, jadikan prosa >=3 kalimat.
- MEDIA path dengan SPASI pada folder dapat gagal dibuka pengguna; sediakan salinan byte-identik di jalur tanpa spasi (pin tetap sah) sebagai kanal serah alternatif.
- Peleburan profil fleet (peran-via-berkas `workspace/roles/<nama>.md` + profil umum `gsp-worker`) memindahkan kartu mid-mission secara sah: cek gateway pid + heartbeat + denyut sesi sebelum intervensi; steering per-kartu menjelaskan identitas baru.
