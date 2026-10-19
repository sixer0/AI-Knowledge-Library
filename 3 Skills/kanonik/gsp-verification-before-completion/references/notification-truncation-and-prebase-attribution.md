# Notifikasi, Jejak Watchdog, dan Atribusi Pra-Basis

Terkondensasi dari MWSKILL-0916 (16/17-09) dan WUI-IMP-0921 (21-09), kedua rantai lolos gerbang rilis.

## 1. Notifikasi kanban terpotong BUKAN bukti

Notifikasi `[kanban] Task ... completed` memotong result di tengah kalimat. Dilarang menyimpulkan vonis, angka CHECK, atau isi artefak dari potongan itu. Prosedur wajib tiap menerima notifikasi:

1. `hermes kanban --board default show <id>` atau baca berkas laporan yang dirujuk kartu (mis. `verification/V1-test-expert.md`, `ACCEPTANCE_F8.md`).
2. Buka artefaknya, grep baris `VERDICT` / `CHECK` langsung dari disk.
3. Bandingkan angka laporan dengan ukur segar sendiri (jumlah baris register, sha256, scan pola) sebelum mengutip ke user.

Preseden: notifikasi REVERIF3 terpotong di `VERDICT: FAIL(1) - 23`; vonis lengkap (23P/1F/1NA + sebab C16) hanya terbaca dari artefak. Notifikasi V2b menyebut "13 PASS, 1 NEEDS_REVIEW"; daftar 8 MINOR dan bukti red-green hanya ada di `V2-code-review.md`.

## 2. Penutupan watchdog BUKAN hasil baru

Notifikasi `Background process ... completed ... ALL_TERMINAL {...}` sering tiba SETELAH kartu-kartunya sudah diproses lewat notifikasi kanban. Cek dulu: bila kronologi di output watchdog identik dengan yang sudah diverifikasi di disk, laporkan sebagai konfirmasi, jangan kerjakan ulang, jangan buat kartu duplikat. Watchdog dengan id kartu basi bisa menggantung selamanya (kejadian: kartu A2 done tapi watchdog key-in prefix salah) - kill, bikin watchdog baru dengan id hasil `list --json`, jangan biarkan.

## 3. Regresi vs cacat pra-basis: uji di worktree commit basis

Kegagalan test di branch kerja belum tentu regresi dari diff. Atribusi sah hanya dengan menjalankan test yang SAMA di commit basis:

```bash
git worktree add <scratch>/wui-base-<sha> <sha-basis>
cd <scratch>/wui-base-<sha> && HERMES_HOME=<home-kosong-temp> \
  uv run --python 3.11 --with pytest python -m pytest tests/<nama>.py -q
git worktree remove --force <scratch>/wui-base-<sha>   # wajib bersih
```

Gagal identik di basis = known-defect prabase; daftarkan di Decision Log kontrak + laporan verifier (V1 CHECK 18 dan V2 CHECK 12 WUI-IMP memakai metode ini, dua agen independen sepakat). Varian kuat lain (dipakai V2b): tree pristine + berkas uji HEAD = red-green sungguhan (27 dari 35 uji gagal di pristine, lolos di HEAD).

## 4. Suite uji gsp-brahma butuh HERMES_HOME terisolasi

conftest repo webui menyalin pohon skills saat setup; dijalankan dengan home produksi ia ERROR saat collection (bukan gagal fungsi). Fix: `HERMES_HOME=C:/Users/TRIAL/AppData/Local/Temp/wui-empty-home` (direktori kosong) di depan perintah pytest. Ini sesuai AGENTS.md repo (isolated state untuk trial). Scratch uji (worktree pristine/redgreen) boleh mencapai puluhan MB - bersihkan setelah scaffold uji dipindah ke lokasi standar (`scripts/hq-testing/<misi>/`).

## 5. Nama field register: `reg_id`, bukan `id`

Cek controller terhadap `references/register.jsonl` paket skill wajib pakai kunci `reg_id`. Memakai `id` menghasilkan 'reg hilang' palsu dan temuan cacat bohong (kejadian 16-09, dikoreksi eksplisit ke user). Uji rujukan lembar jawaban kandidat juga memakai `reg_id`.

## 6. Klaim nihil (NIHIL-GREP) kandidat bisa diaudit deterministik

Bila jawaban agen merujuk penanda "grep pola X = 0 hit", audit dengan menjalankan grep yang sama pada berkas yang sama. Klaim nihil yang cocok = bukti jujur kelas TRAP; yang tidak cocok = karangan, vonis FAIL.
