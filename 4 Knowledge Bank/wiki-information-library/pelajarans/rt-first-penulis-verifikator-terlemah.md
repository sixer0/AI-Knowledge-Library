---
id: rt-first-penulis-verifikator-terlemah
type: pelajaran
title: "RT-FIRST: penulis adalah verifikator terlemah — jangan desain di atas artefak yang tidak ada"
status: active
sumber: docs/2026-08-24_status_rt_bypass/status.md
halaman: baris 30-32 (Keputusan)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-orchestration
tags: [pelajaran, rt-first, verifikasi, anti-self-attestation, orchestration, pipeline]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-orchestration/2026-08-25_rt-first-penulis-verifikator-terlemah.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# RT-FIRST: penulis adalah verifikator terlemah — jangan desain di atas artefak yang tidak ada

Pelajaran dari insiden t_42119e1b (status.md bagian "Keputusan", baris 30-32):
**"Penulis adalah verifikator terlemah — butuh penasihat independen."**

Insiden: task gsp-task-architect t_42119e1b (2026-08-24) menerima task dengan
body hanya berisi referensi dispatch `HQ dispatch cmt6zg95z0001v1l4at9js4j6`,
tanpa artefak request-translator `identification/01_translated.md` di scratch
maupun shared workspace (pencarian = 0 hasil; comments kosong).

Pelajaran yang diterapkan: gate RT-FIRST — task hilir (desain/blueprint) TIDAK
boleh mulai di atas artefak hulu (terjemahan) yang tidak ada. Task-architect
menolak mendesain (status: blocked) dan meminta orkestrator mengulang delegasi
ke gsp-request-translator serta memastikan artefak tertulis sebelum dipanggil
lagi (status.md baris 34-41).

Nilai: mencegah desain/blueprint dibangun dari asumsi terjemahan (karangan),
menjaga jejak verifikasi, dan memaksa urutan pipeline RT-FIRST yang benar.
Cara pakai ulang: sebelum task hilir dijalankan, periksa keberadaan artefak
hulu (identifikasi 01_translated.md) di scratch + shared workspace; jika tidak
ada → blocked + instruksi ulangi delegasi, JANGAN melanjutkan desain.

Angka/kutipan bersumber: status.md (dokumen primer, kelas_bukti primer).
