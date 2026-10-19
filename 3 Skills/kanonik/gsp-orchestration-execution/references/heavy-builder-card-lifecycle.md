# Kartu Builder-Berat & Kemati Jendela Bridge: Triase, Resume, Anti-Tabrakan

Preseden dua gelombang (PROMANUAL-1004 malam + V2-1006 pagi, Okt 2026): kartu delegasi dengan beban "3 bab naskah + 7 figur" atau "render+lint+uji tampil" MATI SEREMPAK di jendela bridge 1800s (timed_out/gave_up pada 1814-1820 dtk, pola identik antar-lane). Vonis yang benar: KELAS CACAT FORMULASI KARTU (estimasi vs plafon run), bukan kegagalan pekerja.

## 1. Estimasi kartu wajib memperhitungkan PLAFON WAKTU, bukan hanya iterasi
- Plafon run bridge = 1800s (+grace). Bentuk R-1 "satu kartu" SAH secara iterasi (E <= 0.5 x cap) tapi TETAP mati bila durasi kerja nyata > jendela. Untuk kartu kelas builder-berat (naskah multi-bab + generate figur + render + lint), target desain: E yang selesai dalam <=20 MENIT, atau rancang sebagai rantai sejak awal (mata per 1 bab / per seksi artefak).
- Konstanta kalibrasi nyata: 1 bab cerna DATUM + 2-3 figur ~= 15-25 mnt; 3 bab + 7 figur > 30 mnt = pasti timeout. Ukur laju dari run pertama sebelum menggandakan bentuk kartu.

## 2. Triase kematian-serentak (jangan refomat penuh ketiga kali)
1. UKUR DISK dulu per lane: aset beku (register JSON per bab, figur PNG/SVG, naskah sebagian) biasanya SELAMAT - timeout tidak merusak state.
2. Peta sisa per lane dari disk + laporan parsial pekerja; vonis "nol state rusak" hanya dengan bukti berkas+mtime.
3. Unblock + komentar RESUME berisi: daftar aset beku (larangan rebuild), sisa kerja terkurangi spesifik, dan kewajiban partial-handoff enam bidang + pin aset di AMBANG-B (>=20 mnt jalan) - anti "mati bisu".
4. Bila run-2 timeout lagi: PECAH kartu per-bab/per-seksi menunjuk bekal beku (estimasi kecil E~20-80). JANGAN resep penuh ketiga kali pada bentuk yang sama (prediksi kartu-pecah terbukti berulang).
5. Lapis naskah vs lapis render dipisah saat remediasi (lihat readability-gated-longform-rework.md §5): timeout di fase instrumen = naskah sudah sah, resume cukup bangun instrumen + laporan.

## 3. Anti-tabrakan pembuatan kartu (akar dua kejadian nyata)
- MODUL BUILDER yang membuat kartu pada LEVEL-MODUL akan MENJALANKAN create() setiap kali di-import (termasuk `python - <<EOF` yang meng-importnya untuk memakai helper) -> gelombang DUPLIKAT lahir saat set kanonik sudah done. Mitigasi normatif: (a) guard `if __name__ == "__main__":` untuk SEMUA blok create pada modul builder; (b) jalur baku pembuatan kartu = panggilan CLI `lad_card.py` LANGSUNG per kartu, bukan import modul; (c) sebelum create kartu resume/eskalasi: `list --json` filter judul misi 60 MENIT terakhir (bukan 15); create dalam giliran yang sama dengan generate body.
- Tabrakan yang terlanjur terjadi: set lebih dulu/lebih maju = kanonik; duplikat (ready, nol run) diberi komentar jejak lalu `archive`; catat Decision Log + akar.
- Watcher/pengawas: parser status WAJIB baca level JSON yang benar (`show --json` -> `['task']['status']`); status '?' dari parser cacat pernah memvonis "settled" palsu. Vonis settled hanya dari status sah.

## 4. Kap aktif vs batch creation (norma gelombang N1, terbukti di produksi dini)
Buat batch besar sekaligus SAH (DAG pre-built dengan parents data-nyata); yang ditegakkan = <=5 AKTIF (ready/running) per misi. Kartu antrean yang sengaja ditahan kap: `block` dengan reason "antrean slot, bukan buntu" + watcher yang MELEPAS otomatis saat slot terbuka (unblock by watcher = sah, pemilik edge = controller). Edge DAG hanya ke hulu data nyata; edge kapasitas ditegakkan lewat prioritas/watcher, bukan edge semu.

## 5. Glue antar-alat milik controller (jangan tunggu kartu gagal)
Sebelum melepas gelombang yang memakai alat baru (meter/lint/renderer), controller menjalankan SATU probe cepat alat itu atas artefak pertama yang lahir (mis. jalankan meter atas bab spesimen, emit register penuh, konversi format input yang tidak cocok). Cacat sambungan (format argumen, flag salah nama) ditambal via komentar steering + aturan kartu berikutnya - hemat satu siklus kartu per lane.
