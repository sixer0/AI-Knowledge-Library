# Review-claim crash: "Unknown skill(s)" saat kartu status `review` di-claim

Preseden: GAYA-AHLI S15 t_bef365fc (05-10-2026 malam, dua crash beruntun #4868/#4869;
pola sama muncul samar di log t_09d49110, t_1a60b964 yang kebetulan bertahan).

## Tanda (deteksi < 2 menit)
- Run crash **< 65 detik tanpa satu pun tool call**; `hermes kanban show` menampilkan
  `claimed ... source_status: review` lalu `crashed {'pid': ..., 'retry_status': 'review'}`.
- Baris terakhir `kanban/logs/<task>.log`:
  `Initializing agent...` lalu `Error: Unknown skill(s): <nama-skill>`
  (mis. `sdlc-review`).
- Retry dispatcher = claim ulang dari review = mati identik → `retries exhausted` → blocked.
  **Re-run buta tidak akan pernah berhasil sebelum gerbang init diperbaiki.**

## Akar
Saat kartu ber-status `review` di-claim, worker kernel meminta satu set skill default
(antara lain `sdlc-review`) ke profil PENANGAN REVIEW. Skill ada di fleet registry
(`$LOCALAPPDATA/hermes/skills/devops/sdlc-review/`, tercatat `.bundled_manifest`) tetapi
TIDAK teraktivasi di snapshot profil pekerja (`$LOCALAPPDATA/hermes/profiles/<p>/.skills_prompt_snapshot.json`
tidak memuatnya) → agent gagal init → exit → crash. Fase KERJA normal (claim dari `ready`)
tidak tersentuh jalur ini: hanya jalur REVIEW-CLAIM yang patah, dan hanya pada profil
yang snapshot-nya tidak punya skill itu.

## Diagnosa cepat (urut)
1. `hermes kanban show <kartu>` → lihat durasi run crash + `source_status: review`.
2. `tail -20 "$LOCALAPPDATA/hermes/kanban/logs/<kartu>.log"` → cari `Unknown skill(s):`.
3. `grep -c sdlc "$LOCALAPPDATA/hermes/profiles/<profil>/.skills_prompt_snapshot.json"` → 0 = terkonfirmasi.
4. Bedakan dari kelas provider/modal STY-A (402/exit-1 pasca-reasoning): di sini error-nya
   deterministik di baris init dan menyebut nama skill.

## Pemulihan (urutan prioritas)
- **(A) Keputusan asignor langsung dari artefak beku.** Bila seluruh deliverable sudah ada
  dan sudah divonis (laporan needs-review + bukti path/ukuran di kartu), keputusan review
  TIDAK butuh agen: force-done/request-changes via jalur resmi (bridge PATCH /api/brahma/requests
  utk kartu dispatch; `hermes kanban complete` utk native). Aturan user 01-09: dispatch failed
  + artefak ada = JANGAN re-dispatch buta.
- **(B) Tambal gerbang (tetap perlu terlepas dari A):** aktivasikan skill yang diminta ke profil
  pekerja-review via jalur resmi manifest.json + generate_profiles.py (rujukan skill
  `hermes-skill-activation`; JANGAN edit snapshot manual), ATAU hilangkan permintaan skill
  default di jalur review-dispatch bila itu konfigurasi kernel. Tanpa ini, setiap kartu yang
  masuk review di profil tanpa skill itu mati 60 detik identik.
- (C) Reassign profil penanganan-review = memindahkan masalah tanpa menambal - opsi lemah.

## Pitfall
- Jangan unblock-untuk-retry sebelum (A) atau (B) mendarat: hanya menaikkan consecutive_failures.
- `skills` kolom task NULL ≠ tidak ada skill diminta: permintaan bisa datang dari default jalur
  review kernel, bukan dari kartu. Cek LOG kernel, bukan hanya DB.
- Sensus cepat profil terdampak: loop `grep -c sdlc .../.skills_prompt_snapshot.json` per profil.
