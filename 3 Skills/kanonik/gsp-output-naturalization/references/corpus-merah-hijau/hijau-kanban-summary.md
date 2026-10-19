contoh bersih - bukan deliverable: berkas ini adalah fixture hijau corpus merah-hijau untuk menguji gerbang naturalisasi keluaran GSP dan seluruh isinya sengaja disusun agar memenuhi setiap ambang yang berlaku pada kanal ringkasan handoff.

# Ringkasan handoff migrasi server produksi

Tim infrastruktur merampungkan pemindahan 13 basis data produksi ke cluster baru
dalam 11 jam jendela perubahan dengan satu rollback terjadwal pada basis data
penggajian yang memakai skrip lama. Seluruh kejadian penting dicatat pada log bersama
bernomor tiket CHG-2026-441 sejak pukul 02:00 sampai pukul 13:00 WIB. Tim aplikasi
telah memverifikasi kecocokan checksum pada seluruh tabel transaksi milik enam layanan
inti dan menandatangani berita acara verifikasi pada hari yang sama. Uji beban penuh
belum dijalankan karena cluster sekunder baru aktif minggu depan, sehingga angka
latensi puncak masih berupa estimasi awal dengan asumsi beban campuran. Sisa pekerjaan
berupa penyesuaian aturan pencadangan harian diserahkan ke tim aplikasi dengan tenggat
10 hari kerja dan laporan kemajuan tertulis setiap Jumat.

| naturalisasi: PASS | scan_ai_footprint.py | 2026-09-02 |
