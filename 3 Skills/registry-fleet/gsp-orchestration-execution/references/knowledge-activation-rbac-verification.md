# Aktivasi knowledge fleet-wide & verifikasi terikat akun RBAC

Kelas misi: korpus knowledge dipromosikan (vault -> wiki/IL -> rute memori lintas profil),
lalu user menuntut verifikasi bahwa knowledge benar-benar hidup di profil yang dipakai
manusia lewat akun RBAC, dengan sampel acak yang sah. Preseden: VSSKB-0923 (23-09-2026).

## Resep langkah (dipakai berulang, vonis hanya dari ukur disk)

1. **Inventaris akun RBAC** dari API rbac HQ (port 9011, TLS self-signed -> `curl -sk`).
   Token internal dibaca dari `gsp-datacenter/.env` kunci `WEBUI_RBAC_TOKEN`
   (nilai [REDACTED] - jangan pernah salin ke kartu/komentar/laporan).
2. **Peta akun -> profil Hermes.** Pola umum: nama profil mencerminkan akun; akun
   superadmin terikat profil root `default` (memori di
   `AppData/Local/hermes/memories/MEMORY.md`, BUKAN `.hermes/memories`).
   Snapshot 23-09: superadmin->default, budi->gsp-master, master01->gsp-master01,
   ory_creative->gsp-creative, firmanhidayat->gsp-firman-custom,
   gspuser01->gspuser01, gspuser02->gspuser02, agentriset->agentriset.
3. **Ukur rute per berkas memori** dengan grep, bukan klaim rollout: token rute
   (mis. `INDEX #vss-korpus`) DAN penanda known-defect harus muncul di tiap profil
   target. Rollout superset (semua profil) >= populasi RBAC; cek 8/8 cukup dengan
   loop grep terhadap daftar peta langkah 2.
4. **Sampel acak beku** bila user minta N dari M (mis. "random 3 dari 8 akun rbac"):
   `python random.Random(int(time.time())).sample(pool, N)` lalu BEKUKAN
   `{seed, drawn_utc, pool penuh, terpilih}` di Decision Log kontrak misi. Undian
   harus reproducible dan diaudit - dilarang pilih manual "yang menarik".
5. **Dispatch probe tanya-jawab** ke profil terpilih (bukan sesi verifier sendiri):
   `hermes -p <profil> -z "<prompt>"` dengan env-strip `HERMES_KANBAN_*` agar anak
   tidak menyentuh papan (pitfall 09-09). Sertakan di prompt: "JAWAB HANYA dari
   korpus/memory yang tersedia; sebutkan jalur rujukannya; JANGAN panggil tool
   kanban." Simpan transkrip mentah per agen (`verif/rbac/probe-N-<profil>.md`).
6. **Ground truth dibekukan sebelum eksekusi**, syarat LULUS eksplisit per butir:
   (a) menunjuk jalur nyata (berkas/baris/objek IL), (b) angka lengkap sesuai rak,
   (c) menyebut penanda defect/status BELUM TERKONFIRMASI bila fieldnya cacat.
   Klaim angka final tanpa penanda = FAIL, walau angkanya cocok rak.
7. **Tahan laporan kesiapan ke user/home channel** sampai sampel N/N LULUS vonis
   verifier independen + controller mengukur ulang artefak (claim ladder L2).

## Pitfall akar-gagal (preseden probe-2, FAIL 3 ronde)

Marker koreksi/defect yang hanya ditempel di lapis HILIR (wiki, Information Library)
TIDAK sampai ke jawaban agen, karena agen menempuh rute memori ke lapis SUMBER
(korpus `ekas/`). Perbaikan harus dipropagasi ke SEMUA lapis yang benar-benar dibaca
agen menurut rute, lalu diverifikasi grep pada lapis itu - bukan pada lapis promosi.
Ini penerapan SPK-002 butir 7 (tambal gerbang/lapis penyebab, bukan gejala hilir).
Kartu FIX terpisah per lapis (di sini: FIX-EKAS hanya-tambah dengan penjaga subsequence
+ cadangan penuh) adalah jalur sah; setelah marker mendarat, re-probe wajib, bukan opsional.

## Fakta lingkungan yang menguntungkan

- Signup WebUI akun baru mengklon profil dari `default`; rute memori yang terpasang di
  root default otomatis ikut ke akun masa depan - rollout superset bersifat
  self-maintaining, tidak perlu kerja ulang tiap akun baru.
- Profil tanpa `memories/MEMORY.md` (mis. profil vision-only) = skip sah, dicatat di
  kontrak, jangan dipaksa bikin berkas.

## Mekanika kartu LAD (pengingat antarmuka)

`lad_card.py` adalah CLI flag-only: TIDAK ada subperintah `create`, TIDAK ada
`--priority`/`--json`. Wajib: `--title --assignee --body-file --est --shape
[satu|rantai-N|paralel-Kx] [--parents id1,id2]`; tenant diwarisi dari parent.
Panggil lewat python dengan path NATIVE `C:/Users/...` (path MSYS `/c/...` tidak
diterjemahkan untuk argumen program native).
