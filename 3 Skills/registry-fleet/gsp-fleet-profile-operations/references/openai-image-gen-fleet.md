# OpenAI image-gen fleet backend (misi OPENAI-IMG-DIST-2609, 2026-09-03)

Kelas tugas: mendistribusikan API key OpenAI khusus image generation ke profil
fleet untuk pekerjaan slide/PPT/brosur dengan kombinasi aset gambar plus teks,
termukan cara memverifikasi bahwa jalur tool benar-benar hidup per profil.

## Bukti kualitas probe (kenapa gpt-image-2 layak untuk teks Indonesia)
- Probe: POST https://api.openai.com/v1/images/generations, model `gpt-image-2`,
  size 1536x1024, quality medium, n=1 -> HTTP 200 dalam 43 s, PNG b64 1.798.343
  byte, usage 1.492 token.
- Telaah vision atas slide hasil generate: seluruh kata Indonesia tereja benar,
  legibilitas 9,5/10, kelayakan slide korporat 8,5/10. Satu-satunya teks acak
  adalah micro-text dekoratif pada dashboard ilustrasi (filler, bukan konten).
- Pelajaran: probe dulu dengan prompt nyata yang sarat teks dan bahasa lokal.
  Prompt generik menutupi kegagalan text-rendering; kasus slide+teks justru
  alasan kunci ini dipakai.

## Mekanika Hermes (verifikasi sumber di repo hermes-agent)
- Tool `image_generate` dispatch ke provider bernama di `image_gen.provider`
  (agent/image_gen_registry.get_active_provider). Bila UNSET, fallback: satu
  provider terdaftar, lalu legacy `fal`. FAL tanpa FAL_KEY = error, jadi
  `provider: openai` eksplisit itu WAJIB, bukan opsional.
- Plugin `plugins/image_gen/openai`: baca `get_secret("OPENAI_API_KEY")`;
  tier virtual `gpt-image-2-low|medium|high` (API model sama, parameter
  `quality` beda). Preseden model: env `OPENAI_IMAGE_MODEL` ->
  `image_gen.openai.model` -> `image_gen.model` (bila salah satu tier id) ->
  default medium.
- Size: landscape 1536x1024, square 1024x1024, portrait 1024x1536. Jalur edit
  (image-to-image) menerima hingga 16 gambar sumber via `image` /
  `reference_image_urls`.
- Konsumen lain dari `OPENAI_API_KEY` (penting untuk klaim scope): fallback
  TTS/STT OpenAI (setelah `VOICE_TOOLS_OPENAI_KEY`), rantai auxiliary custom
  endpoint (butuh `OPENAI_BASE_URL` juga), dan provider video OpenAI. Tidak ada
  hard-gate per tool; "khusus gambar" adalah konvensi konfigurasi, bukan
  pembatasan teknis. Default STT tetap local faster-whisper, default TTS tetap
  edge, jadi memasang key tidak mengalihkan jalur suara dengan sendirinya.

## Resep distribusi (idempoten, sudah terbukti 9/9 PASS)
1. Uji key dulu ke /v1/models dan satu generasi nyata; simpan artefaknya di
   folder kontrak misi sebelum menyentuh fleet.
2. `.env` per profil: append `OPENAI_API_KEY=<key>` dengan dedup (tepat 1 baris;
   verifikasi lewat fingerprint sha256 prefiks, jangan echo nilai aslinya).
   Materi key: tulis sekali ke scratch file, tidak pernah di-print, hapus setelah
   rollout, lalu sapuan string key di scripts/docs/repo wajib 0 berkas.
3. Config SEQUENTIAL (jangan paralel, lihat pitfall korusi dotted-key):
   `hermes -p <p> config set image_gen.provider openai` lalu
   `hermes -p <p> config set image_gen.openai.model gpt-image-2-medium`.
   Root default tanpa `-p`.
4. Toolset: audit `platform_toolsets.cli` tiap profil target. Empat profil
   pekerja slide (image-prompt-specialist, design-system-specialist,
   document-writer, pm-writer) TIDAK punya `image_gen` terdaftar meski perannya
   menghasilkan slide; sisipkan `- image_gen` di bawah blok `cli:` lewat edit
   teks terarah, lalu re-parse.
5. Setelah semua write: re-parse tiap config.yaml; assert blok `image_gen:`
   benar, tidak ada key nyasar level atas (junk dotted-key), blok `model:` utuh.

## Resep verifikasi berlapis (script: verify_openai_image_key_20260903.py)
- Lapis 1 sapuan statis: tepat 1 baris key per profil dengan fingerprint sama
  dengan global; config image_gen benar; toolset ada.
- Lapis 2 fungsional per profil: spawn python venv repo dengan
  `HERMES_HOME=<profil>`, `load_dotenv(..., override=True)`,
  `hermes_cli.plugins.discover_plugins()`, lalu
  `agent.image_gen_registry.get_active_provider()` -> name openai +
  `is_available()` True; `plugins.image_gen.openai._resolve_model()[0]` == tier
  yang dikonfigurasi.
- Lapis 3 end-to-end tool asli: panggil
  `tools.image_generation_tool._handle_image_generate({...})` dengan HERMES_HOME
  profil -> success true DAN file PNG benar-benar tertulis di
  `<profil>/cache/images/openai_gpt-image-2-*.png`; ukur byte di disk, jangan
  percaya flag saja (field path resminya `image`, bukan `image_path`).

## Pitfall
- Proses gateway yang sedang hidup TIDAK melihat key baru (dotenv dimuat saat
  proses start). Dispatch bridge spawning proses baru langsung memakai key.
  Restart gateway tetap wewenang user (konvensi GSP).
- Snapshot repo: `sync_gsp_agent.py` mengecualikan `.env` (aman), tetapi
  config.yaml snapshot profil RBAC membawa `api_key: sk-...` GSP-AI literal ke
  riwayat git (temuan lama, bukan dari misi ini). Forward-fix: redaksi salinan
  repo ke `${HERMES_CUSTOM_10_83_81_246_11400_API_KEY}` sebelum commit; purge
  history = keputusan user. Selalu cek `git diff --cached | grep -cE '\+.*sk-'`
  harus 0 sebelum commit.
- `lad_card.py --assignee brahma` mencetak peringatan "config profil 'brahma'
  tidak terbaca -- fallback cap 500": informatif, kartu tetap sah (nama folder
  profil default bukan `brahma`).
