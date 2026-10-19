# HANDOVER — EKAS Engineering Skill Corpus (folder `buku v3`)

Peta satu halaman untuk orang yang **menandatangani** atau **mengambil alih** pekerjaan ini.
Keadaan per 2026-09-17. Rincian per-gelombang ada di `SKILLS/README.md`; berkas ini hanya peta.

## 1. Apa isi folder ini

| Lapisan | Lokasi | Isi |
|---|---|---|
| Rak buku (sumber) | `*.pdf`, `old/` | ±100 PDF buku teknik; standar R2 (NETA, IEC, IEEE, EN 62676-1-2) ada di vault `C:\Users\gspen\Videos\Buku\...\_standar` |
| Register | `SKILL-MAPPING_Engineering-Corpus_Rev0.xlsx` | sheet 02: 389 kandidat skill; kolom J/K = status paket (sinkron dari `skill.yaml`) |
| **Paket skill** | `SKILLS/<taksonomi>/SKILL-<ID>_<SLUG>/` | **311 kalkulator** (8 berkas: skill.yaml, calculator.py, tests.json, validator.py, examples.jsonl, knowledge.md, equations.yaml, references.yaml + input_schema.json) dan **21 dokumen** (`kind: document`, document.py) |
| Mesin bersama | `SKILLS/*.py` | `router.py` (routing + dispatch), `schema_guard.py` + `units.py` (penjaga skema/satuan), `report.py` (lembar kalkulasi HTML), `docgen.py` (dokumen deterministik), `ekas_agent.py` (agen produksi) |
| QA | `SKILLS/qa/` | `fuzz_all.py` (masukan sah), `fuzz_neg.py` (masukan tak sah), `prov_audit.py` (audit halaman sumber), `chains.py` (24 rantai antar-skill) |
| Korpus & data latih | `CURATION/` | `cpt/` (93 buku, 20.368 dok, LOKAL-SAJA), `sft/sft_train.jsonl`+`sft_val.jsonl` (11.867 sampel / 311 skill), held-out **tersegel**: `heldout_eval.jsonl` (73) + `heldout_eval_v2.jsonl` (49) |
| Model | `TRAINING/` | kartu model `MODEL-CARD_EKAS-Qwen3-4B.md` (DAPT, dilatih pada 283 skill — **belum** dilatih ulang) |
| Sign-off | `SIGN-OFF_Lembar-Verifikasi-Engineer.xlsx` | 311 + 21 baris, **0 ditandatangani** |

## 2. Satu perintah yang membuktikan semuanya

```bash
python SKILLS/run_all_tests.py
```

Tahap gerbang (semua wajib hijau): 311 suite golden test + validator → ROUTER (top-1 781/782, top-3 100 %) → REPORT → DOKUMEN (21 paket/44 uji) → SKEMA+SATUAN (311/311) → **DEMO** (7/7 entri : 5 demo skenario + 24 rantai `qa/chains.py` ≈ 278 langkah/270+ skill + pembangkitan 21 dokumen ke `docs_out/`).
Hasil terakhir: **311 suite, 2100 PASS, 0 FAIL; DEMO 7/7**.

## 3. Kontrak yang dijaga (jangan dilanggar saat menambah paket)

1. **Angka bersumber** — tiap entri `knowledge` di `skill.yaml` menyebut sumber + halaman + `authority_status` (`verified` / `penyusunan` / `pending_verification` / `external_source` / `blocked_missing_source`). Yang tak ada di rak **DITANDAI**, tidak dikarang.
2. **Audit independen** — tiap `calculate()` mengembalikan `independent_check.validation_ok` dari jalur hitung kedua. `false` pada data tak koheren adalah perilaku yang diinginkan.
3. **Penolakan terkontrol** — masukan salah → `InputError`; jalur produksi (`schema_guard.normalize`) menolak None wajib, bool-sebagai-angka, NaN/inf, magnitudo absurd, lintas-dimensi. Skill impor dipanggil lewat helper `_call()` agar InputError-nya tidak bocor.
4. **Anti-duplikasi** — skill hilir mengimpor skill hulu (importlib), bukan menyalin rumus.
5. **Empat hal tidak pernah diasumsikan** — sasaran MTBF kegagalan majemuk, sasaran pengamatan video, ambang resistansi pembumian, resistivitas tanah.
6. **Held-out tersegel** — dua berkas held-out tidak dipakai tuning dan tidak disunting.
7. **Lisensi** — korpus CPT dan model hasil latih LOKAL-SAJA.

## 4. Cara menambah satu paket (ringkas)

1. Saring dulu terhadap inventaris terbangun (banyak stub ternyata kembar paket lain).
2. Baca halaman sumbernya; tulis `calculator.py` + `tests.json` (nilai buku sebagai golden) + `skill.yaml`.
3. `python SKILLS/gen_input_schemas.py` → `CARDS_REGEN_ONLY=1 python SKILLS/gen_cards.py` → tambah kata kunci di `router.py` → `python SKILLS/run_all_tests.py`.
4. `python SKILLS/qa/fuzz_all.py`, `fuzz_neg.py`, `prov_audit.py` untuk paket baru; tambahkan ke satu rantai di `qa/chains.py`.
5. `python SKILLS/gen_signoff.py`; bila data latih perlu diperbarui: `python CURATION/sft_scaler.py`.

## 5. Untuk penandatangan

- Urutan tinjau di lembar sign-off: paket bersumber belum-verified → ber-butir DITANDAI → ber-langkah penyusunan → pengimpor → berjangkar buku langsung.
- Bahan tinjau: `knowledge.md` per paket, `CURATION/provenance_audit_gel92.md` (280/357 halaman terkonfirmasi otomatis), lembar kalkulasi `SKILLS/reports_out/CALC-*.html`, dokumen contoh `SKILLS/docs_out/*.md`.
- Menerapkan tanda tangan: `python SKILLS/apply_signoff.py` (pratinjau) lalu `--apply`; hanya tindakan itu yang menaikkan paket dari `draft` ke `verified`.

## 6. Yang belum selesai

| Hal | Penghalang |
|---|---|
| Tanda tangan engineer (0/332) | tindakan manusia |
| Latih ulang model pada SFT 311-skill + re-eval (held-out v1+v2) | GPU + server LLM lokal |
| 10 stub: OPT-006/007, ELN-001/002/005/007/010/014/016/017 (+MEC-012/013 MERGED) | sumber di luar rak (Rao/Boyd, IEC 60063, jangkar halaman) |
| 16 entri `external_source` (tabel kabel LV, DORI detect/observe, bitrate 4MP+, PSM 20, deret motor/genset…) | standar/katalog: IEC 60502/SPLN, EN 62676-4, OEM |
| 40 parameter numerik skema tanpa satuan terdaftar | satuan majemuk (%/tahun, mm/put, lumen, mata uang) belum ada di `units.py` |
