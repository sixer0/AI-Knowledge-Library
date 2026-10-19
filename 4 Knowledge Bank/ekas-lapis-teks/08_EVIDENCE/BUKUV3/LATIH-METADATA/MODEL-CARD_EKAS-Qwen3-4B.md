# Kartu Model — EKAS Qwen3-4B (DAPT)

**Berkas:** `ekas-qwen3-4b-Q4_K_M.gguf` (~2,5 GB) · adapter sumber:
`TRAINING/out_dapt/lora_final` · basis: Qwen3-4B (unsloth bnb-4bit)
· dibuat 2026-09-08 · **LOKAL-SAJA — dilarang diunggah/didistribusikan**
(korpus CPT berisi buku ber-hak-cipta; lisensi latihan internal).

## Resep

1. **CPT** 1 epoch × 37,6 jt token korpus rak EKAS (97 sumber, blend
   berbobot: 5 standar R2 ×3), QLoRA r32 seq 1024; loss 2.46 → ~1.86.
2. **SFT** 2 epoch × 9.738 sampel tool-call tereksekusi-nyata (283 skill,
   instruksi higienis), loss hanya giliran assistant; eval 0.2919 → 0.1896
   (unggul di seluruh 8 titik vs SFT tanpa CPT).

## Kinerja (eval hilir 150 instruksi val, wasit = kalkulator EKAS)

| Model | exec | args-exact | audit valid |
|---|---|---|---|
| Basis polos | 18,0% | 17,3% | 18,0% |
| SFT v3 (tanpa CPT) | 96,0% | 92,0% | 95,3% |
| **DAPT (model ini)** | **95,3%** | **91,3%** | **94,7%** |

Selisih DAPT vs v3 = 1 sampel/150 (dalam derau); DAPT dipilih final karena
membawa pengetahuan domain CPT. Kegagalan tersisa: 4 kasus argumen-raksasa
(deret/matriks melebihi jendela generasi) + 3 selip skema langka.

## Pemakaian yang DIMAKSUDKAN

**Pemanggil-alat (tool-caller) EKAS**: user memberi instruksi teknik →
model mengeluarkan `<tool_call>{"tool": "calculator.calculate",
"arguments": {...}}</tool_call>` → **eksekutor WAJIB menjalankan argumen
pada kalkulator skill sebenarnya** dan menyuntikkan hasil nyata; blok
`<result>` yang ditulis model sendiri TIDAK boleh dipercaya (artefak
format latihan). Prompt sistem yang dipakai saat eval ada di
`eval_downstream.py`.

## Batasan (JUJUR)

- **Bukan penjawab naratif**: pertanyaan terbuka dijawab dgn tool-call
  paksaan berargumen karangan + result fabrikasi (terdokumentasi di
  `qualitative_dapt.json`, termasuk rujukan fiktif). Utk tanya-jawab
  naratif domain, pakai adapter CPT-murni `out_cpt/lora_final`
  (`qualitative_cpt.json`: 0/6 tool-call, prosa lancar) — dgn catatan
  presisi faktual naratif khas 4B: angka tetap harus dari kalkulator.
- Skema argumen sangat panjang (matriks/deret ratusan angka) bisa
  terpotong; kirim data besar via mekanisme lampiran, bukan prosa.
- Ambang milik pemilik sistem (resistansi pembumian, DORI, MTBF majemuk,
  resistivitas tanah) TIDAK pernah diisi model — kalkulator menegakkannya.

## Cara pakai di ollama (lokal)

```
# Modelfile
FROM ./ekas-qwen3-4b-Q4_K_M.gguf
PARAMETER temperature 0
SYSTEM Anda adalah asisten teknik EKAS. Jawab instruksi dengan blok <tool_call>{"tool": "calculator.calculate", "arguments": {...}}</tool_call> berisi JSON pemanggilan kalkulator yang tepat.
```
`ollama create ekas-4b -f Modelfile` lalu `ollama run ekas-4b`.
Smoke test lulus (2026-09-08): via llama-server, instruksi tegangan
jatuh menghasilkan tool_call berskema benar. Ingat: `<result>` yang
ditulis model = placeholder; eksekusi nyata wajib oleh kalkulator.

## Artefak terkait

`out_sft/lora_v1..v3` (jejak SFT), `out_cpt/lora_final` (CPT murni),
`eval_*.json` (seluruh eval), `TRAINING/README.md` (riwayat lengkap +
pelajaran keras), gerbang mutu: `SKILLS/run_all_tests.py` (1.880 test).
