# Pelajaran fleet: batas pengetahuan level-model (misi EKAS-MODEL-1006, 06-07/10/2026)

Tiga instrumen INDEPENDEN menghasilkan vonis konsisten atas pilot LoRA r16 bf16
(Qwen2.5-1.5B, dataset turunan register terverifikasi EKAS, EVAL_LOSS 0,41-0,55):

1. GAYA berpindah ke bobot, FAKTA TIDAK. Kebiasaan ber-sitasi [R-n] dan "tidak ada di rak"
   tertransfer kuat (gaya 4/6-7/10 vs base 0-2/10). Angka bernomor TIDAK: 0/5 (penulis),
   0/3 (verifier v1), 0/3 (controller segitiga v2) probe numerik benar-bersitasi.
2. Fabrikasi ikut meniru OTORITAS: adapter-v2 mengklaim "(R1)" padahal R1=0 di seluruh
   korpus, dan menempelkan jangkar nyata ke subjek salah (REF-OEM-TERMO fiktif; digest
   grounding untuk soal baterai; "FOA PDF 196" milik unit lain). Sitasi keluaran model
   BUKAN bukti - wajib ditelusuri ke register/rak sebelum dipakai.
3. Koreksi eksplisit dalam data latih KALAH oleh distribusi (diagnostik anti-fabrikasi
   0/5 terpancing). Overfit berulang bukan jalan keluar - kontrak STOP-butir-4 dieksekusi.
4. Instrumen uji sendiri adalah sumber cacat: substring/gema pertanyaan = positif-palsu
   (terjadi pada penulis DAN controller; diverifikasi manual vs JSON beku). Uji isi wajib
   nilai harapan eksplisit + pembacaan manual terhadap sumber beku.
5. Vonis arsitektural (D-05 direvisi): integrasi pengetahuan level-model yang sah untuk
   korpus angka = RETRIEVAL-AUGMENTED (adapter gaya + router indeks sebagai satu layanan
   dengan wajib-verifikasi-sitasi), bukan memorisasi - apa pun skala modelnya, angka di
   bobot tidak dapat diaudit SPK-002 (provenans hilang saat inferensi).

Artefak lengkap: <ws>/docs/2026-10-06_ekas-model-1006/ (contract §5-8, eval/, verification/
CHECK-ADAPTER.md vonis PASS 7/7 t_43cffc03) + mirror repo gsp-agent
hermes-home/workspace/docs/2026-10-07-ekas-model-1006/ (adapter v1+v2 safetensors).
Preseden terkait: larangan menjawab dari ingatan tanpa panggil indeks (RULE EKAS-IDX-1006
butir 4/7) - kini punya bukti empirik level bobot, bukan hanya prosedur.
