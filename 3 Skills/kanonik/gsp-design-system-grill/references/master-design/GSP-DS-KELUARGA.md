# GSP-DS-KELUARGA - konstanta & meta-rules lintas 13 design system (kondensasi)
Sumber lengkap: `study/DS-KELUARGA.md` (docs/2026-09-01-master-design-adaptasi, 114 baris, STATUS: complete).
File ini = kondensasi siap-pakai; rujukan halaman sumber dipertahankan utuh per butir.
Generator: SM-1 t_de708ae3 2026-09-01. Aturan kutipan: konstanta menyebut >=3 set sumber; "tidak ada di rak" bila nihil.

## A. KONSTANTA BERSAMA (ringkas)
- A1 Kanvas & grid: 16:9 = 1920x1080 px di SEMUA 13 set; grid 12 kolom, outer margin ~120px, gutter 20-24px, baseline 8px (BNN hal 5-6, BNPT p4, Cyber p3, GENERAL p3, Polri hal 5, Kemhan p4, TNI AD p7, TNI AL/AU). Spacing 8/16/24/32/48/64(128) identik di GENERAL p5, Polri p7, TNI AU p8, Military. Split kanonik: FULL, 8/4, 6/6, 4/4/4; pola kiri teks 30-40% / kanan panel 60-70%.
- A2 Warna = peran + rasio: roles fungsional (primary/secondary/neutral/accent/status) dengan rasio tercetak BNN 70/20/7/3 (hal 4), BNPT 65/20/10/5 (p3), Polri 65/25/10 (hal 4), TNI AD 70/20/10 (hal 5), Kemhan 60-70/15-20/5-10/3-5/<3 (p3). Hukum keluarga: netral dominan 60-85%, aksen tunggal <10% (emas di BNN/BNPT/Polri/TNI AD/AU/Kemhan; biru Business/Teknik; cyan+ungu Cyber). 4 warna status semantik di 6 set.
- A3 Tipografi peran 7-9 level DISPLAY..CAPTION tercetak >=6 set (BNN hal 1&7, BNPT p5, Cyber p6, GENERAL p6, TNI AU p6, Kemhan p5); display = sans condensed bold ALL-CAPS, body = grotesk netral, angka tabular. Nama font tercetak hanya 4 set: Cyber (Bebas Neue Condensed+Inter+JetBrains Mono p6), Kemhan (BEBAS NEUE+INTER p5), TNI AU (BEBAS NEUE CONDENSED+MONTSERRAT p6), TNI AD (Oswald Extra Condensed+Inter p6). Doktrin: "This is a role system, not a font choice" (GENERAL p6).
- A4 Hierarki ~70/20/10 PRIMARY/SECONDARY/TERTIARY di >=7 set; satu focal point per slide.
- A5 Kerangka halaman: header kicker "NN / <SISTEM>" + garis aksen pendek; nomor halaman "NN / TOTAL" kanan bawah; footer baris kata kunci dipisah "•" (A5 DS-KELUARGA hal rujukan: BNN/BNPT/Cyber/GENERAL/Military/Polri/TNI AD/AL/AU/Teknik/Visual).
- A6 Traceability: alur X->EVIDENCE->DECISION (BNN hal 2, BNPT p2, TNI AD hal 2, TNI AU p2, Kemhan p6/p19); tag bukti wajib (EvidenceTag BNN hal 14, EVIDENCE ID BNPT p8, DOCUMENT TAG TNI AD hal 11, REQ+SHA-256 Kemhan p8/p19, sumber wajib Polri hal 20); label klasifikasi formal: TIDAK ADA DI RAK (slot classification_label diisi per proyek).
- A7 Hero visual 4 treatment: FULL FRAME / CONTAINED / CUTOUT / ENVIRONMENTAL (BNN hal 10, BNPT p7, Cyber p7, TNI AD hal 10, TNI AU p9, Kemhan p7, Polri hal 13); doktrin "imagery as evidence not decoration" (BNPT p7).
- A8 Bahasa grafis 8 elemen: frame/line/marker/label/callout/connector/highlight/texture (Visual p8 induk; Polri hal 10, TNI AD hal 11, Kemhan p8, Cyber p8, BNPT p8, BNN hal 11).
- A9 Ikon line-art stroke seragam (GENERAL p10, Polri hal 14 stroke 1.5px ukuran 24/32/48, Kemhan, Cyber, matra). Grid/nama ikon selain Polri: tidak ada di rak.
- A10 Larangan dekorasi eksplisit (Cyber p7/15/19, TNI AD hal 4, TNI AU p4, Kemhan p2, BNN hal 3, Polri hal 3, BNPT p2/p7) + doktrin "Clarity before decoration. Structure before style." (TNI AU p2, Visual p1, TNI AD prinsip 01-02); density LOW/MED/HIGH per kompleksitas (GENERAL p8, Polri p8, Kemhan p12, Teknik p3).
- A11 Variasi sah: latar terang vs gelap (gelap: Cyber #000010 79.7%, GENERAL, TNI AD, TNI AL #001020 75.7%); HEX tercetak hanya 7/13 set; token turunan (radius/shadow/WCAG>4.5:1) hampir nihil di rak (satu-satunya: Polri 4.5:1 hal 4).

## B. POLA PER BIDANG (ringkas)
- B1 Institusional (BNN/BNPT/Polri): netral hangat terang + navy/cokelat institusional + emas; BNPT satu-satunya merah otoritas #C8202F; tabel kepatuhan sebagai komponen pusat; tone akuntabilitas.
- B2 Matra (AD/AL/AU/Military): warna ikut lingkungan operasi (AD olive gelap #3F4F3A, AL navy #001020, AU deep blue #1F3A5F di kanvas terang, Military olive terang); satu aksen emas; motif blueprint alutsista; density data-evaluatif tinggi. AL & Military = deck arah TANPA token -> adaptasi wajib sampling/keputusan.
- B3 Cyber: dark-mode murni, warna=state ("NEVER USE SEVERITY COLOR DECORATIVELY" p17), mono JetBrains Mono, sistem motion (p18), density tertinggi.
- B4 Generik (Business/Visual/Teknik/GENERAL): tanpa identitas institusi -> layer tema proyek diisi merek klien; Business doktrin naratif decision-oriented; Visual menyumbang kosakata komposisi universal (70/20/10, 8 composition modes); Teknik menyumbang callout 8 jenis + tabel spesifikasi; GENERAL = meta-model 3-lapis (Core stabil/Theme adaptif/Content unik), font-agnostic by design.

## C. META-RULES SIAP-KODE (MR1-MR6 - salinan kerja; teks penuh + bukti di study/DS-KELUARGA.md)
- MR1 Fondasi wajib sebelum produksi: identity_positioning, color_architecture, typography_role_scale, canvas_grid_spacing, component_library+graphic_language. Validator menolak palette/roles_typography/grid == null.
- MR2 Warna = role+rasio; token disimpan role->hex PER TEMA (bukan hex global); domain override netral generik. usage_ratio wajib dideklarasikan (netral 60-85%, struktur 15-25%, aksen <=10%).
- MR3 Status = warna + label teks + ikon (tidak pernah warna saja); hierarki 70/20/10; ONE SLIDE ONE DECISION.
- MR4 Klaim bawa jejak: claim -> evidence_id -> reference_id (+rev/date; opsional hash). Komponen wajib: EvidenceTag, FooterMetadata, PageNumber NN/TOTAL, slot classification_label.
- MR5 Kontrak numerik: canvas 1920x1080, 12 kolom, margin 120, gutter 20-24, baseline 8, spacing [8,16,24,32,48,64,(128)]; type_roles [DISPLAY,H1,H2,H3,LEAD,BODY,DATA,LABEL,CAPTION]; display condensed ALL-CAPS + body grotesk + data tabular/mono. Yang boleh berubah per proyek hanya 6 hal (judul proyek, hero, subjek, tipe data, komposisi, intensitas aksen) - grid/hierarki/peran warna/spacing/penomoran/bahasa grafis STAYS CONSTANT (TNI AD hal 15, TNI AU p15).
- MR6 Kosakata grafis minimal 8 elemen fungsional + ornamen khas tunggal per set; negatives-list lint: cyberpunk/neon HUD, gaming aesthetics, camouflage/busy background, flashy saturated colors, heavy ornament, gradient/glow berlebihan, 3D chart, stock-hacker cliche.

STATUS: complete
