# Pemulihan controller: worker mati setelah artefak lahir (preseden GAYA-AHLI-1005, 05-10..06-11)

Kelas kejadian berulang: run worker berhenti (timed_out limit bridge 1800s, atau crash) TEPAT SETELAH
badan artefak lengkap ditulis ke disk, sebelum short check/penutupan kartu sempat jalan. Tiga kejadian
satu misi (G3, S9, S15). Vonis yang SALAH: "kerja gagal, restart". Vonis yang BENAR: artefak hidup,
penutupan adalah pekerjaan controller.

## Prosedur pemulihan (urut)

1. Baca event kartu: `timed_out` dengan `elapsed ~1800s` + mtime artefak di menit yang sama = kelas ini.
   Bedakan dari crash <65 detik TANPA tool call (lihat bagian cacat claim di bawah).
2. UKUR SENDIRI artefak dengan parser independen (bukan membaca summary worker): jumlah entri vs outline,
   kelengkapan bidang wajib, glif terlarang, baris terakhir utuh (bukan terpotong), sha16.
3. Bila bukti lengkap: `hermes kanban complete <id> --result "STATUS: complete (force-done controller,
   bukti terukur). <angka hasil ukur sendiri> ..." --force`. Sertakan kronologi limit + state run terakhir.
   Bila kartu terblokir: `unblock` dulu, baru complete --force.
4. JANGAN pernah menyalakan ulang kerja dari nol pada jalur artefak yang sama (menimpa artefak worker =
   preseden buruk 03-09 EXPO26PS-W1).

## Mitigasi di sisi kartu (turun-temurun)

- Kartu penulisan/rakit berat: `--max-runtime 3600` saat create via lad_card.py.
- Body kartu WAJIB berisi "SHORT CHECK DI AWAL sesi, bukan di akhir" untuk kelas kartu berat.
- Sisa kerja pasca-force-done (mis. skrip check internal yang tak sempat ditulis) dirinci di result
  supaya kartu lanjutan tahu persis apa yang kurang.

## Cacat jalur review-claim (kelas terpisah, D-18)

Signature: run yang meng-claim kartu dari `source_status=review` mati <65 detik tanpa satu pun tool
call, log terakhir identik `Error: Unknown skill(s): <nama-skill>` (kasus nyata: `sdlc-review`
direferensikan profil claimer tapi tidak ada). Ini BUKAN kegagalan kerja kartu; re-run buta mati
identik. Aksi controller: traceroot dari log kernel + DB run + probe profil, tutup kartu dengan vonis
sendiri ber-bukti ukur (prosedur di atas), dan ajukan perbaikan fleet (hapus/daftarkan skill yang tidak terdaftar di
profil) via gsp-skill-manager. Jangan tulis 'X tidak bisa dipakai' sebagai aturan - perbaiki referensinya.
