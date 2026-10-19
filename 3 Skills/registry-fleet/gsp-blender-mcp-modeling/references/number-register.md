# Number Register (AN-nn consolidated)

Verbatim transcription of Appendix B of the mission report
`docs/2026-10-16-blender-mcp-skill/output/REPORT.md` (rev A, 2026-10-16).
Every row is a tool print from the 2026-10-16 lane runs; nothing is quoted
from memory. Some descriptive cells retain the Indonesian research language
of those runs: only values, units, identifiers, and source references are
binding here, and rewording would break the tool-print property that SPK-002
requires. The Report id column walks back into Appendix B of the report; the
Register id column names the lane register row.

Rule of use: any threshold quoted in this skill bundle, in a project sheet,
or in a QA verdict must cite its Report id from this table. A number with no
row here does not exist for the purposes of this skill; look it up upstream
or leave the field empty and register the gap. Known limitation of this
table: every row is a print of one instrument on one host on 2026-10-16, so
staleness, not transcription, is the failure mode to watch. Refresh duty: pins below carry
a recheck obligation whenever Blender or mcp-for-blender moves (see
references/mcp-architecture.md section 'Freshness').

| Report id | Lane | Register id | Row content |
|---|---|---|---|
| AN-01-01 | 1 | UK-10 | `curl https://pypi.org/pypi/mcp-for-blender/json` (via urllib) ; `info.version=2.1.9`; 16 rilis; rentang 2026-09-01..2026-10-06; sha256 wheel `a5cbc6cf...21ccc` |
| AN-01-02 | 1 | UK-11 | `curl https://pypi.org/pypi/blender-mcp/json` ; shim 2.0.0, summary "Renamed to mcp-for-blender...", whl 2.440 B |
| AN-01-03 | 1 | UK-12 | `GET api.github.com/repos/ahujasid/mcp-for-blender{,/commits/main,/releases,/tags}` ; MIT; 31.025 stars; HEAD `7a0373ec...`; releases_listed=0; tags=[] |
| AN-01-04 | 1 | UK-13 | `GET api.github.com/repos/.../git/trees/main?recursive=1` ; 73 blob; modul `src/blender_mcp/*` 17 berkas; 21 berkas tests |
| AN-01-05 | 1 | UK-14 | `curl raw.githubusercontent.com/.../{server,safe_mode,addon_manager,telemetry,bundled/addon,generation,context_log,guides}.py` + `sha256sum` ; HTTP 200 semua; bundled addon 270.889 B sha `eb0facf6...`; `addon.py@HEAD` identik hash dengan bundled |
| AN-01-06 | 1 | UK-15 | `blender -b --factory-startup --python-exit-code 9 --python lane1_headless_probe.py` ; `{"background": true, "version": "5.2.0 LTS", "py": "3.13.13", "bl_info_version": [1,6], "addon_protocol_version": 5, "default_host": "localhost", "default_port": 9876, "running_after_start": false, "socket_after_start": false, "start_stdout": "cannot start server in background mode..."}` |
| AN-01-07 | 1 | UK-16 | `uv run --no-project --python 3.11 --with mcp-for-blender==2.1.9 python lane1_surface.py` (env DISABLE_TELEMETRY=true) ; tool_count_total=14; model-facing=9; app-only=5; total_tool_chars=16.459; est_tokens=4.114; instructions_chars=1.456; instructions_ceiling_tested=2.500; expected_addon_protocol=13; safe_mode_enabled_now=false; mcp_sdk_resolved=1.30.0 |
| AN-01-08 | 1 | UK-17 | `uv run ... mcp-for-blender addon-paths` (read-only) ; `Blender/5.2/scripts/addons (exists)`, `Blender/4.2/scripts/addons (missing)`, existing install = `blender_mcp.py` |
| AN-01-09 | 1 | UK-18 | `sha256sum` + `wc -l` addon host vs bundled; `grep -oE "blendermcp_use_*"` ; host 175.194 B sha `f43469c8...` 4.164 baris, 5 sakelar; bundled 270.889 B sha `eb0facf6...` 6.441 baris, 6 sakelar |
| AN-01-10 | 1 | UK-19 | diff himpunan perintah: `RELEASED_SERVER_COMMANDS` (test_compat_matrix) vs handler addon host ; 39 vs 33; hilang: export_scene, describe_node_type, bpy_api_lookup, list_scene_items, pick_viewport_object, get_polyhaven_asset_preview, 4 perintah Tripo |
| AN-01-11 | 1 | UK-20 | `grep -c "@mcp.tool"` pada `3dsmax-mcp/maxmcp`; baca `pyproject.toml`, `mcp_config.ini`, `max_client.py` ; 159 tool; versi 1.5.5; `mcp[cli]>=1.0.0,<2.0.0`; safe_mode=true; tool_profile=full; PORT=8765; poll 1500/50 ms |
| AN-01-12 | 1 | UK-21 | `ls venv/Lib/site-packages/mcp/server/`; `cat mcp-2.0.0.dist-info/METADATA` ; `fastmcp ABSENT` (ada `mcpserver`); SDK terpasang di venv Hermes = 2.0.0 |
| AN-01-13 | 1 | UK-22 | `netstat -ano ; grep LISTEN` (jam 14:10) ; tidak ada listener pada port 9876 |
| AN-01-14 | 1 | UK-23 | lint entity-match 19 URL sitatan (`lane1_urllint.py`) ; 19/19 MATCH, HTTP 200 semua, SALAH-TARGET = 0 |
| AN-01-15 | 1 | UK-24 | `ls`/`cat` config klien MCP ; `claude_desktop_config.json` 239 B hanya `3dsmax-mcp`; `.cursor/mcp.json` hanya `3dsmax-mcp`; tidak ada entri blender |
| AN-02-01 | 2 | AN-01 | Level subdiv viewport/render ; rentang [0,11]; default viewport 1, render 2; viewport jangan > render ; E-05 API; E-04 manual |
| AN-02-02 | 2 | AN-02 | Kualitas evaluasi subdiv ; [1..10] default 3 (rendah = cepat, kurang presisi) ; E-05 |
| AN-02-03 | 2 | AN-03 | Adaptive subdivision ; PIXEL default 1.0 px [0.1..1000]; OBJECT default 0.01 BU [0.0001..1000]; OBJECT wajib untuk instance ; E-05, E-04 |
| AN-02-04 | 2 | AN-04 | Bevel profil ; Shape/Miter tanpa efek bila Segments < 2 ; E-08 |
| AN-02-05 | 2 | AN-05 | Pole (valensi vertex) ; pole = valensi 3, 5, dst.; valensi 1/2/4 bukan pole ; E-02 |
| AN-02-06 | 2 | AN-06 | Unit scale ; hanya tampilan UI; fisika internal tidak ikut; scale_length [1e-09, inf] ; E-11 (manual + API) |
| AN-02-07 | 2 | AN-07 | Benchmark resmi OSD ; Maya/Presto ~100 ms vs target OSD < 3 ms utk 30k poly -> level 2 (500k poly); docs OSD v3.7.0 ; E-13 |
| AN-02-08 | 2 | AN-08 | Sinyal forum ; Q89 score 74 / views 59.942; Q2931 score 31 / views 67.224 (keduanya protected) ; E-16 (API stackexchange, cetakan JSON) |
| AN-02-09 | 2 | AN-09 | glTF ; primitif == draw-call GPU; non-triangular tidak didefinisikan spesifikasinya; copyright 2013-2021 ; E-15 |
| AN-02-10 | 2 | AN-10 | Sejarah CC ; 1978 Catmull & Clark; Academy Award for Technical Achievement 2005/06 ; E-12 |
| AN-02-11 | 2 | AN-11 | Bukti berkas talk ; IA GDC2014Brainerd PDF 5.322.163 B (md5 1069020a...); SIGGRAPH advances PDF 10.416.723 B; Pixar DKT1998 PDF 32.701.934 B ; E-23, E-24 (HEAD/metadata tercetak) |
| AN-02-12 | 2 | AN-12 | Bentuk kursus ; Hard Surface: 51 lecture/7 jam/Intermediate; Skill Builder: 47 lecture/6,5 jam/Beginner; bio Abbitt: 500k+ subscriber ; E-18 (halaman terfetch) |
| AN-02-13 | 2 | AN-13 | Donut 5.0 ; penulis Andrew Price; tanggal halaman "Nov 26" (listing 2025); edisi selaras Blender 5.0 ; E-17 |
| AN-02-14 | 2 | AN-14 | Pin kesegaran wiki ; CC oldid=1366559186; Polygonal modeling oldid=1356181652; Subdivision surface oldid=1376084839 ; E-12, E-14 (+E-25 pointer seksi 3) |
| AN-03-01 | 3 | AN3-01 | margin FRACTION 1/1024 = 1 px pada tekstur 1024 (island >=2 px terpisah) ; Manual 5.2 UV Operators ; Tier-1 |
| AN-03-02 | 3 | AN3-02 | smart_project default: angle_limit 1,15192 rad (66,04 deg), island_margin 0,0, area_weight 0,0; unwrap margin 0,001 iterations 10 ; API docs current + probe 5.2.0 LTS ; Tier-1 + PRIMER-DISK |
| AN-03-03 | 3 | AN3-03 | contoh acuan densitas 2,56 px/cm = 256 px/m ; Beyond Extent (hlm diperbarui Apr-2026) ; Tier-2 |
| AN-03-04 | 3 | AN3-04 | 20,48 px/cm cukup untuk proyek personal ; Beyond Extent ; Tier-2 |
| AN-03-05 | 3 | AN3-05 | default Principled 5.2.0: BaseColor 0.8 gray, Rough 0.5, IOR 1.5, Spec IOR Level 0.5, Coat Rough 0,03, ThinFilm IOR 1,33 ; probe WS/work/probe-s04/probe_out.json ; PRIMER-DISK |
| AN-03-06 | 3 | AN3-06 | view transform default AgX, look None, display sRGB pada 5.2.0 LTS ; probe idem + release notes 4.0 ; PRIMER-DISK + Tier-1 |
| AN-03-07 | 3 | AN3-07 | thin film interference terkuat ~100-1000 nm; IOR material 1,0-4,0 ; Manual 5.2 Principled ; Tier-1 |
| AN-03-08 | 3 | AN3-08 | rumus tile UDIM: 1001 + u + v*10; array 10 kolom ; Manual 5.2 UDIMs ; Tier-1 |
| AN-03-09 | 3 | AN3-09 | oklusi glTF: channel R, 0=oklusi penuh, strength 1+s*(t-1); MR packing G=rough B=metal linear ; glTF 2.0 3.9/5.21 ; Tier-1 |
| AN-03-10 | 3 | AN3-10 | 4K RGBA8 + mipmap ~89 MB (turunan aritmetika, bukan kutipan) ; kalkulasi parser dari definisi format ; turunan |
| AN-04-01 | 4 | AN-L4-01 | 4 tipe lampu (POINT/SUN/SPOT/AREA) ; enum ; probe RNA 5.2.0 LTS ; 2026-10-16 |
| AN-04-02 | 4 | AN-L4-02 | Energi default semua tipe = 10 ; W radiant ; probe factory 5.2 ; 2026-10-16 |
| AN-04-03 | 4 | AN-L4-03 | Temperature default 6500 (use_temperature OFF) ; K ; probe 5.2 ; 2026-10-16 |
| AN-04-04 | 4 | AN-L4-04 | Cutoff distance default 40 (use_custom_distance OFF) ; m ; probe 5.2 ; 2026-10-16 |
| AN-04-05 | 4 | AN-L4-05 | Sun angle default 0.00918 rad = 0.526 deg ; rad/deg ; probe 5.2 ; 2026-10-16 |
| AN-04-06 | 4 | AN-L4-06 | Spot default 45 deg, blend 0.15; rentang angle 1-180 deg ; deg ; probe 5.2 + manual ; 2026-10-16 |
| AN-04-07 | 4 | AN-L4-07 | Area default SQUARE 0.25 m, spread 180 deg ; m/deg ; probe 5.2 ; 2026-10-16 |
| AN-04-08 | 4 | AN-L4-08 | Tabel daya nyata: lilin 0.05 W; LED 800lm 2.1 W; 1000lm 2.9 W; PAR38 4 W; tube 4.5 W; headlight 22 W ; W ; manual light_object ; 2026-10-16 |
| AN-04-09 | 4 | AN-L4-09 | Sun strength: cerah 1000; mendung 500; overcast 200; bulan 0.001 ; W/m2 ; manual light_object ; 2026-10-16 |
| AN-04-10 | 4 | AN-L4-10 | Cycles default: 4096 samples, adaptive 0.01, min 0 ; spp ; probe factory 5.2 ; 2026-10-16 |
| AN-04-11 | 4 | AN-L4-11 | Rentang tipikal noise threshold 0.1..0.001 ; - ; manual sampling ; 2026-10-16 |
| AN-04-12 | 4 | AN-L4-12 | Denoiser default OPENIMAGEDENOISE; passes RGB_ALBEDO_NORMAL ; enum ; probe 5.2 ; 2026-10-16 |
| AN-04-13 | 4 | AN-L4-13 | Bounce default: max 12, transparent 8, diffuse 4, volume 0 ; bounce ; probe 5.2 ; 2026-10-16 |
| AN-04-14 | 4 | AN-L4-14 | Clamp default: direct 0, indirect 10 ; - ; probe 5.2 ; 2026-10-16 |
| AN-04-15 | 4 | AN-L4-15 | Pixel filter default BLACKMAN_HARRIS width 1.5 ; px ; probe 5.2 + manual film ; 2026-10-16 |
| AN-04-16 | 4 | AN-L4-16 | EEVEE TAA: viewport 16, render 64; gi_diffuse_bounces 3; RT method SCREEN default OFF ; spp ; probe 5.2 ; 2026-10-16 |
| AN-04-17 | 4 | AN-L4-17 | EEVEE limits: 128 sphere probes, 16 plane probes, 4096 lampu terlihat, half-precision ; count ; manual limitations + RN 4.2 ; 2026-10-16 |
| AN-04-18 | 4 | AN-L4-18 | GPU: CUDA/OptiX CC>=5.0; OptiX driver>=575; OIDN GPU CC>=7.0; HIP RDNA1+; macOS>=13 Metal ; ambang ; manual gpu_rendering + RN 5.2 ; 2026-10-16 |
| AN-04-19 | 4 | AN-L4-19 | Poly Haven: 997 HDRI (type hdris), 96 studio, 301 indoor; lisensi CC0 ; count ; api.polyhaven.com + license (ukur) ; 2026-10-16 |
| AN-04-20 | 4 | AN-L4-20 | OIDN: Apache 2.0; Academy Technical Achievement Award 2025; rentang 1 spp-konvergen ; - ; openimagedenoise.org ; 2026-10-16 |
| AN-04-21 | 4 | AN-L4-21 | Waktu render uji CPU 240px: 0.25-1.19 dtk (hang-up denoiser pada run pertama; BUKAN benchmark mutu) ; detik ; probe render lokal ; 2026-10-16 |
| AN-04-22 | 4 | AN-L4-22 | AgX default sejak 4.0 (commit a9053f7efb); EEVEE id -> BLENDER_EEVEE di 5.0 (commit 4fe75da973) ; - ; developer.blender.org RN ; 2026-10-16 |
| AN-04-23 | 4 | AN-L4-23 | Host fleet: RTX 5070 Ti (OPTIX/CUDA), Ryzen 7 7700 CPU, Radeon iGPU HIP; backend NON/OPTIX/CUDA/HIP/ONEAPI ; daftar ; probe preferences 5.2 ; 2026-10-16 |
| AN-04-24 | 4 | AN-L4-24 | Format render 16 enum; EXR 11 codec (default ZIP); kedalaman 8/10/12/16/32; default PNG 8 RGBA ; enum ; probe 5.2 ; 2026-10-16 |
| AN-04-25 | 4 | AN-L4-25 | Video HDR: display Rec.2100 PQ/HLG + codec H.265/AV1 + 10/12-bit; HDR image AVIF/PNG @203 nits; HDR video @100 nits ; - ; manual displays_views ; 2026-10-16 |
| AN-05-01 | 5 | AN-L5-01 | NodesModifier type='NODES'; evaluasi GN penuh di -b ; probe_gn.py run sukses |
| AN-05-02 | 5 | AN-L5-02 | 98 kelas Modifier; 274 tipe GeometryNode*; keluarga baru terlihat: MeshBevel, SampleSoundFrequencies, XPBDSolver, ApplySimulatedData, Get/SetGeometryBundle, FieldToList/ClosureToList/ListGetItem/ListLength/FilterList/SortList, StringJoin/StringToCurves ; probe11.py dir(bpy.types) |
| AN-05-03 | 5 | AN-L5-04 | Tanpa socket OUTPUT di interface: peringatan "Node group must have an output socket", n_verts=0 ; probe run 09-10-14:1x |
| AN-05-04 | 5 | AN-L5-05 | tree.interface: new_socket ADA, items_new ABSEN; daftar metode: active, active_index, bl_rna, clear, copy, items_tree, move, move_to_parent, new_panel, new_socket, remove, rna_type ; probe3/probe5 |
| AN-05-05 | 5 | AN-L5-06 | identifier socket = Socket_0..Socket_N mengikuti urutan deklarasi (gin=Socket_0, gout=Socket_1, width=Socket_2, height=Socket_3) ; probe5a.json |
| AN-05-06 | 5 | AN-L5-07 | mod["Socket_2"]=x -> TypeError id properties not supported ; probe8.py |
| AN-05-07 | 5 | AN-L5-08 | bpy.ops.asset: mark, mark_single, catalog_new, library_refresh, asset_download, bundle_install, dst. ; probe11.py |
| AN-05-08 | 5 | AN-L5-09 | Rute sah: mod.properties.inputs["Socket_2"]["value"]=0.170 -> dim_x terukur 0.170000002 (dari 0.25); kasus mm: 250->300 BU terukur 300 ; probe9.py, probe10.py |
| AN-05-09 | 5 | AN-L5-10 | Edit interface default_value tidak terpropagasi via update_tag/view_layer.update/reassign-group/dg.update/frame_set (hash16 63de8456b3f00ea1 tetap); nilai baru muncul hanya di evaluasi jalur ekspor ; probe5 routes A-E |
| AN-05-10 | 5 | AN-L5-11 | Enum Driver.type 5.2: AVERAGE, SUM, SCRIPTED, MIN, MAX; 'PYTHON' ditolak TypeError ; probe5a.json, probe_gn.py |
| AN-05-11 | 5 | AN-L5-12 | Driver SCRIPTED vx*2.0 pada objek lain: 0.5 tercapai setelah view_layer.update() tanpa frame_set; frame_set hasil sama ; probe12.py |
| AN-05-12 | 5 | AN-L5-13 | Driver self-dimensi (dimensions->scale objek sama): depsgraph WARNING "Dependency cycle detected" ; probe run awal, stderr tercetak |
| AN-05-13 | 5 | AN-L5-14 | Factory units: METRIC/1.0/METERS; mm-convention scale_length=0.001 tidak mengubah angka BU (250 BU tetap 250) ; probe10.py |
| AN-05-14 | 5 | AN-L5-15 | --python-exit-code 9: skrip gagal -> exit 9; sukses -> exit 0 (teramati berulang) ; seluruh run probe |
| AN-05-15 | 5 | AN-L5-16 | Re-eval tanpa perubahan: hash vertex identik; modifier_apply GN headless OK (8 vert) ; probe5, probe12 |
| AN-05-16 | 5 | AN-L5-17 | modifier_apply_as_new_mesh: hasattr True (stub) tetapi panggilan error "could not be found" -> operator tidak ada di 5.2 ; probe12.py |
| AN-05-17 | 5 | AN-L5-18 | 110 flag export_scene.gltf; apply-family hanya export_apply; apply_transform absen ; probe5a.json |
| AN-05-18 | 5 | AN-L5-19 | Ekspor GN tanpa apply -> GLB 168-184 B + "no primitives omitted" (geometri hilang); dengan export_apply=True -> 1248 B berisi mesh ; probe5/probe10 stderr+ls |
| AN-05-19 | 5 | AN-L5-20 | Round-trip proses baru: n=16 vert, dims [0.25, 0.0, 0.08] sesuai nilai ter-bake terakhir; X/Y delta nol ; imp_apply.json |
| AN-05-20 | 5 | AN-L5-21 | Dua proses terpisah skrip sama -> JSON keluaran identik (diff kosong) ; probe5a vs probe5b; p10a vs p10b |
| AN-05-21 | 5 | AN-L5-22 | Dua ekspor GLB parameter sama -> sha256 file identik (eb19458c1e55a4ee..., 1208 B) ; probe10 + sha256sum |
| AN-06-01 | 6 | AN-L6-01 | 0 ; segitiga degenerasi yang diizinkan per primitif (SHOULD NOT) ; spec glTF 2.0.1, registry.khronos.org, 16-10-2026 |
| AN-06-02 | 6 | AN-L6-02 | det>0 => CCW ; aturan winding vs transform global ; idem |
| AN-06-03 | 6 | AN-L6-03 | SHOULD resize ; perilaku NPOT ; idem (seksi 3.8.4.5) |
| AN-06-04 | 6 | AN-L6-04 | meter ; satuan aksesori POSITION ; idem (seksi 3.7) |
| AN-06-05 | 6 | AN-L6-05 | !=0 exit code bila >=1 error ; kontrak CLI validator ; README glTF-Validator master, 16-10-2026 |
| AN-06-06 | 6 | AN-L6-06 | ids[], screencoverage 0.5/0.2/0.01 ; contoh ambang MSFT_lod ; README MSFT_lod, 16-10-2026 |
| AN-06-07 | 6 | AN-L6-07 | 64.000 ; vertex maksimum per buffer static batching ; Unity Manual 6.6 (built 2026-10-14), 16-10-2026 |
| AN-06-08 | 6 | AN-L6-08 | 300 vertex / 900 atribut ; plafon dynamic batching ; Unity Manual 2021.3 LTS, 16-10-2026 |
| AN-06-09 | 6 | AN-L6-09 | 350k-500k ; triangle/frame Quest 1 ; Meta developers unity-perf, 16-10-2026 |
| AN-06-10 | 6 | AN-L6-10 | 750k-1m ; triangle/frame Quest 2/Pro ; idem |
| AN-06-11 | 6 | AN-L6-11 | 1,3m-1,8m ; triangle/frame Quest 3/3S ; idem |
| AN-06-12 | 6 | AN-L6-12 | >=72 ; FPS minimum aplikasi interaktif ; idem |
| AN-06-13 | 6 | AN-L6-13 | 50-150 / 150-250 / 200-400 (Q1); 80-200 / 200-300 / 400-600 (Q2/Pro); 200-300 / 400-600 / 700-1000 (Q3/3S); 500-1.000 (Rift S/Rift) ; draw call/frame per kelas beban (busy/medium/light) ; idem |
| AN-06-14 | 6 | AN-L6-14 | tepat 2 face per edge ; definisi manifold ; Blender 3.6 manual 3D Print Toolbox, 16-10-2026 |
| AN-06-15 | 6 | AN-L6-15 | 0,001 ; default thickness_min (unit scene; = 1 mm pada 1 BU = 1 mm) ; source object_print3d_utils/__init__.py, 16-10-2026 |
| AN-06-16 | 6 | AN-L6-16 | 0,0001 ; default threshold_zero ; idem |
| AN-06-17 | 6 | AN-L6-17 | 160 deg ; default angle_sharp ; idem |
| AN-06-18 | 6 | AN-L6-18 | 45 deg ; default angle_overhang ; idem |
| AN-06-19 | 6 | AN-L6-19 | 45 deg ; default angle_distort ; idem |
| AN-06-20 | 6 | AN-L6-20 | [A-Za-z0-9_]+ ; karakter sah identifier ; ue5-style-guide 00.1, 16-10-2026 |
| AN-06-21 | 6 | AN-L6-21 | grid >= 10 unit ; syarat snap aset modular marketplace ; ue5-style-guide 4.3 (kutip requirement Epic), 16-10-2026 |
| AN-06-22 | 6 | AN-L6-22 | tanpa plafon polycount/DC ; klaim resmi Nanite (kualitatif) ; Epic Doc 5.8 Nanite via web_extract, 16-10-2026 |
| AN-06-23 | 6 | AN-L6-23 | (4,1,0) / (5,12,3) / (4,2,0) ; blender_min Toolbox / versi io_scene_fbx / blender_min FBX ; source blender-addons main, 16-10-2026 |
| AN-06-24 | 6 | AN-L6-24 | 2.0.0-dev.3.10 ; versi npm gltf-validator terbaru ; registry.npmjs.org, 16-10-2026 |
| AN-06-25 | 6 | AN-L6-25 | 2023-06-27 ; commit terakhir glTF-Toolkit ; api.github.com repos, 16-10-2026 |
| AN-07-01 | 7 | AN-L7-01 | 12 ; tool gambar di indeks Draw Mode ; docs.blender.org manual 5.2 modes/draw/tools/index ; grep href unik lokal halaman ; 2026-10-16 14:0x |
| AN-07-02 | 7 | AN-L7-02 | 11 ; modifier Generate GP ; .../modifiers/generate/index.html ; hitung entri daftar indeks ; 2026-10-16 14:1x |
| AN-07-03 | 7 | AN-L7-03 | 39 ; kelas unik bpy.types.GreasePencil* API 5.2 ; docs.blender.org/api/5.2/bpy.types.html ; grep pola kelas, sort -u, hitung baris unik (HTML 591.027 B tersimpan) ; 2026-10-16 14:0x |
| AN-07-04 | 7 | AN-L7-04 | 123 ; operator unik bpy.ops.grease_pencil.* API 5.2 ; docs.blender.org/api/5.2/bpy.ops.grease_pencil.html ; grep anchor id operator, sort -u, hitung baris unik (HTML 600.768 B tersimpan) ; 2026-10-16 14:0x |
| AN-07-05 | 7 | AN-L7-05 | 2.387 ; total aset Poly Haven ; api.polyhaven.com/assets ; json load, len(d) (2.480.543 B tersimpan) ; 2026-10-16 14:0x |
| AN-07-06 | 7 | AN-L7-06 | 997 ; HDRI Poly Haven ; api.polyhaven.com/assets?t=hdris ; len(json) ; 2026-10-16 14:1x |
| AN-07-07 | 7 | AN-L7-07 | 869 ; texture Poly Haven ; api.polyhaven.com/assets?t=textures ; len(json) ; 2026-10-16 14:1x |
| AN-07-08 | 7 | AN-L7-08 | 521 ; model 3D Poly Haven ; api.polyhaven.com/assets?t=models ; len(json) ; 2026-10-16 14:1x |
| AN-07-09 | 7 | AN-L7-09 | 2.908 ; total item ambientCG ; ambientcg.com/api/v2/full_json (kueri tanpa filter valid) ; numberOfResults ; 2026-10-16 14:1x |
| AN-07-10 | 7 | AN-L7-10 | 2.020 ; material ambientCG ; ...full_json?type=Material&limit=1 ; numberOfResults + echo dataType=['Material'] ; 2026-10-16 14:1x |
| AN-07-11 | 7 | AN-L7-11 | 433 ; HDRI ambientCG ; ...full_json?type=hdri&limit=1 ; numberOfResults + echo dataType=['HDRI'] ; 2026-10-16 14:1x |
| AN-07-12 | 7 | AN-L7-12 | 34 ; 3D model ambientCG ; ...full_json?type=3d-model&limit=1 ; numberOfResults + echo dataType=['3DModel'] ; 2026-10-16 14:1x |
| AN-07-13 | 7 | AN-L7-13 | 48.174 ; aset Blendkit (jumlah assetCount kategori daun) ; blenderkit.com/api/v1/categories/ ; sum(children.assetCount) per kategori ; 2026-10-16 14:2x |
| AN-07-14 | 7 | AN-L7-14 | 10.000 ; plafon `count` search API Blendkit (BUKAN total katalog) ; blenderkit.com/api/v1/search/?query=&page_size=1 ; field count ; 2026-10-16 14:2x |
| AN-07-15 | 7 | AN-L7-15 | 697K/593K/552K/382K/342K ; kartu kategori CGTrader terbesar (Interior/Food/Furniture/Architectural/Character) ; www.cgtrader.com homepage ; baca label kartu kategori ; 2026-10-16 14:1x |
| AN-07-16 | 7 | AN-L7-16 | 3 ; kelas lisensi CGTrader (Royalty Free, Editorial, Custom) ; www.cgtrader.com/faq ; token judul artikel FAQ ; 2026-10-16 14:2x |
| AN-08-01 | 8 | CT-01 | regex nama tool `^[a-zA-Z0-9_-]{1,128}$` ; T2-01 |
| AN-08-02 | 8 | CT-02 | deskripsi tool: min 3-4 kalimat; konsolidasi tool; namespacing per layanan; respons hanya sinyal tinggi ; T2-01 |
| AN-08-03 | 8 | CT-03 | `input_examples`: validasi skema (invalid=400), ~20-50/~100-200 token, tidak untuk server tool & computer/browser toolsets ; T2-01 |
| AN-08-04 | 8 | CT-04 | Claude mencoba ulang panggilan tool 2-3x dengan koreksi sebelum meminta maaf ; T2-02 |
| AN-08-05 | 8 | CT-05 | token system prompt tool-use: Opus/Sonnet/Haiku 5.5 = 286 (auto/none), 406 (any/tool); Opus 4.5 & Haiku 4.5 = 496/588; Opus 4.1 = 313/315 ; T2-01 tabel |
| AN-08-06 | 8 | CT-06 | forced tool use (`any`/`tool`) = 400 pada Opus 5.5, Sonnet 5.5, Fable 5.1, Mythos 5.1; alternatif resmi: strict tool use / structured outputs; manual extended thinking memblokir `any`/`tool` di model yang mendukung paksa ; T2-01 |
| AN-08-07 | 8 | CT-07 | paralel tool call default aktif pada Claude 4+ ; T2-03 |
| AN-08-08 | 8 | CT-08 | semua tool_result dalam SATU pesan user, sebelum teks apa pun; format salah mengurangi paralelisme ; T2-03 |
| AN-08-09 | 8 | CT-09 | `disable_parallel_tool_use` di DALAM `tool_choice`; auto=>maks 1, any/tool=>tepat 1 ; T2-03 |
| AN-08-10 | 8 | CT-10 | batch computer/browser use wajib serial stop-on-first-failure; panggilan tak dijalankan tetap dijawab `is_error:true` ; T2-03 |
| AN-08-11 | 8 | CT-11 | streaming tool: delta `input_json_delta.partial_json` (string parsial), input final objek; model saat akses emit satu key-value lengkap per waktu ; T2-04 |
| AN-08-12 | 8 | CT-12 | pemulihan stream: <=4.5 pasang parsial sbg assistant; >=4.6 pesan user "continue from [previous_response]"; tool_use/thinking tak bisa resume parsial ; T2-04 |
| AN-08-13 | 8 | CT-13 | jendela konteks flagship 1M (termasuk tool definitions+thinking), model lama 200k; maks output 128k; maks 600 gambar/PDF-page (100 utk 200k) ; T2-05 |
| AN-08-14 | 8 | CT-13b | input > jendela = 400 "prompt is too long"; generasi menyentuh batas di 4.5+ => `stop_reason: model_context_window_exceeded` ; T2-05 |
| AN-08-15 | 8 | CT-14 | thinking block wajib dikembalikan utuh bersama tool_result terkait; modifikasi => error (verifikasi signature) ; T2-05 |
| AN-08-16 | 8 | CT-15 | injeksi `<budget:token_budget>`/`<system_warning>` hanya Sonnet 5/4.6/4.5 & Haiku 4.5; model baru pakai task budgets (beta) ; T2-05 |
| AN-08-17 | 8 | CT-16 | 5 server MCP = 58 tool ~55k token definisi; tool search potong >85%, muat 3-5 tool ; T2-06, T2-08 |
| AN-08-18 | 8 | CT-17 | akurasi pemilihan tool menurun mulai 30-50 tool tersedia ; T2-06 |
| AN-08-19 | 8 | CT-18 | ambang pakai tool search: >=10 tool / >10k token definisi / multi-MCP 200+; di bawahnya standard calling ; T2-06 |
| AN-08-20 | 8 | CT-19 | defer_loading: tetap dikirim ke API, keluar dari konteks; tool_reference default maks 5 (limit 1-10.000); deferred plafon 10.000; regex<=200 char, BM25<=500; cache prefix utuh ; T2-06 |
| AN-08-21 | 8 | CT-20 | Anthropic melihat 134k token definisi sebelum optimasi; TST upfront ~500 token; eval MCP: Opus 4 49->74%, Opus 4.5 79.5->88.1%; Claude for Excel pakai PTC ; T2-08 |
| AN-08-22 | 8 | CT-21 | instruksi eksplisit + langkah bernomor; golden rule "show your colleague" ; T2-09 |
| AN-08-23 | 8 | CT-22 | beri alasan di aturan; parameter yang meminta reasoning model => risiko refusal `reasoning_extraction`; minta penjelasan/bukti singkat ; T2-01, T2-09 |
| AN-08-24 | 8 | CT-23 | tag XML konsisten; contoh dalam `<example>`/`<examples>`; relevan+diverse+terstruktur ; T2-09 |
| AN-08-25 | 8 | CT-24 | long-context 20k+: dokumen di atas, XML metadata, kutip-dulu-sebelum-kerja ; T2-09 |
| AN-08-26 | 8 | CT-25 | L1 metadata ~100 token/skill selalu termuat; L2 SKILL.md target <5k token saat triggered ; T2-10 |
| AN-08-27 | 8 | CT-26 | L3 nol token sampai diakses; skrip dijalankan via bash, hanya output masuk konteks ; T2-10, T2-12 |
| AN-08-28 | 8 | CT-27 | `name` <=64 char, [a-z0-9-], tanpa tag XML, reserved: anthropic/claude ; T2-10 |
| AN-08-29 | 8 | CT-28 | `description` non-empty <=1024 char, tanpa tag XML, what+when ; T2-10 |
| AN-08-30 | 8 | CT-29 | SKILL.md <500 baris; rujukan 1 level; MCP name ter-kualifikasi `Server:tool`; tanpa jalur backslash; jangan asumsikan paket ; T2-11 |
| AN-08-31 | 8 | CT-30 | uji >=3 evaluasi; uji lintas Haiku/Sonnet/Opus; tanpa voodoo constants; feedback loop utk tugas quality-critical ; T2-11 |
| AN-08-32 | 8 | CT-31 | seleksi skill = pencocokan description oleh model atas daftar L1; satu description utk potensi 100+ skill ; T2-10, T2-11 |
| AN-08-33 | 8 | CT-32 | Claude Code: cap daftar skill 1.536 char/entri (description+when_to_use), configurable `skillListingMaxDescChars`; letakkan kasus utama di depan ; T2-14 |
| AN-08-34 | 8 | CT-33 | API: skill via `container`+`skill_id` + code execution tool; container tanpa jaringan, tanpa instal paket runtime ; T2-10 |
| AN-08-35 | 8 | CT-34 | Claude Code: `~/.claude/skills/` personal, `.claude/skills/` proyek; prioritas enterprise>personal>project; live-change detection ; T2-14 |
| AN-08-36 | 8 | CT-35 | custom skill tidak sinkron antar permukaan (claude.ai/API/Code terpisah) ; T2-10 |
| AN-08-37 | 8 | CT-36 | Agent Skills = standar terbuka lintas-platform (update resmi 18-12-2025; agentskills.io) ; T2-12, T2-13 |
| AN-08-38 | 8 | CT-37 | konektor MCP Claude: hanya tool calls; server wajib https publik; STDIO lokal tidak didukung ; T2-16 |
| AN-08-39 | 8 | CT-38 | beta `mcp-client-2026-09-15`: blok `mcp_tool_listing` + pin daftar tool server ; T2-16 |
| AN-08-40 | 8 | CT-39 | OpenAI: `strict` (Responses normalisasi strict; Chat Completions non-strict default); `parallel_tool_calls:false` top-level; tool_choice auto/required/none/fixed ; T2-18 |
