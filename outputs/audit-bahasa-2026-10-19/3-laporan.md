# Audit bahasa: 3 Skills

Tanggal: 19 Oktober 2026. Pemeriksaan dan penyuntingan dilakukan oleh Codex secara berurutan.

Singkatan percakapan pada prosa diperluas, istilah internal yang bermakna kiasan diperjelas, dan paragraf panjang dipisahkan pada batas kalimat. Rangkaian aturan bertanda (a), (b), dan seterusnya diuraikan menjadi butir agar langkahnya dapat diperiksa satu per satu. Contoh tulisan buruk, fixture, kode, nama aturan, dan metadata dipertahankan. Penyuntingan diterapkan pada kedua salinan tanpa menyamakan versi yang memang sudah berbeda.

| Cakupan | Jumlah |
|---|---:|
| Berkas asli diinventarisasi | 2321 |
| Berkas diperbarui, termasuk indeks | 282 |
| Berkas tetap utuh | 2039 |

| Sebelum | Sesudah |
|---|---|
| utk / dgn / yg / tsb | untuk / dengan / yang / tersebut |
| nama hantu / angka hantu | nama yang tidak terdaftar / angka tanpa bukti |
| runtuh menjadi INFO | dilaporkan sebagai INFO |
| menagih agregasi | diperhitungkan dalam penilaian agregat |

Verifikasi: **LULUS**. Tidak ada berkas asli yang hilang. Metadata YAML, blok kode, kode sebaris, dan URL pada dokumen yang disunting tetap utuh. Berkas non-Markdown tetap sama dengan versi awal. Indeks diperbarui mengikuti ukuran berkas; ukuran pada manifest dihitung ulang.

Semua 2.321 berkas diinventarisasi. Pemindaian pola dan kepadatan mencakup Markdown; temuan ditinjau menurut konteks kebijakan, pedoman, dan contoh. Ini bukan pembacaan manual setiap kalimat pada seluruh skill. Berkas kode, dataset, font, arsip cadangan, dan dokumen fixture dipertahankan secara byte. Keutuhan 1.130 pasangan yang semula identik diperiksa; 19 perbedaan awal dicatat pada [perbandingan salinan](3-perbandingan-salinan.md). Tidak menjalankan skrip operasional atau menerapkan skill ke profil host asal.

Rincian berkas dan sidik SHA-256: [3-perubahan.csv](3-perubahan.csv). Perbandingan kalimat lengkap tersedia pada commit folder ini. Versi sebelum penyuntingan ada pada commit awal `8785880`.

Pemeriksaan akhir: dua salinan `corpus-merah-hijau/merah-semua-kode.md` dikembalikan ke versi awal karena merupakan korpus uji yang sengaja memuat gaya buruk. Perbaikan ini tercatat pada commit pemeriksaan akhir.

Penyuntingan akhir lintas folder memperjelas penggunaan kiasan “mendarat”, “menagih”, “hantu”, dan istilah kurator pustaka sesuai konteks. Istilah yang memiliki makna teknis atau arti biaya tetap dipertahankan. Tabel jumlah dan daftar hash di atas mencerminkan keadaan akhir.
