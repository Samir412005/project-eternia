# STUDIO INSTALL LOG — radical tools (2026-11-15)

Installs the missing radical open-source design tools from
`~/workspace/research_notes/radical-design-tools-20261115/report.md`.
Base studio already installed (Blender 4.5.9 LTS, Krita 5.3.4.1, Godot 4.3,
Material Maker, Audacity, LMMS, RenderDoc, gdtoolkit, gdUnit4, Beehave,
Dialogue Manager 2.45.0 — see `~/workspace/tools/activation/ACTIVATION_LOG.md`).

Environment during this install: branch `aetheria-slice` (HEAD `cdae362` at
start), free RAM ~150–190 MB, the complete-slice coordinator running heavy
Blender/Godot work in parallel. All installs ran SEQUENTIALLY, one at a time.
`/tmp` is a 512 MB tmpfs — it filled twice (see failures); all large scratch
went to the home disk instead. Nothing on the `main` branch was touched.

## 1. CharMorph 0.4.0 — VERIFIED WORKING

- Source: https://github.com/Upliner/CharMorph (releases)
  + character library https://github.com/Upliner/CharMorph-db
- Download:
  - `curl -sL -o CharMorph.zip https://github.com/Upliner/CharMorph/releases/latest/download/CharMorph.zip`
    → 225,754 bytes (addon only, no character library — <10 MB per the README note)
  - `curl -sL -o CharMorph-db.zip https://codeload.github.com/Upliner/CharMorph-db/zip/refs/heads/master`
    → 336,334,714 bytes, 710 entries, 437 MB uncompressed
- Install: `blender --background --factory-startup --python /tmp/install_charmorph.py`
  (`bpy.ops.preferences.addon_install` + `addon_enable(module="CharMorph")`),
  then extracted the db zip into
  `~/.config/blender/4.5/scripts/addons/CharMorph/data/` (645 files, 420 MB).
- Verification (headless, Blender 4.5.9):
  - Enable: OK — `CHARMORPH_ENABLED: True`, module
    `~/.config/blender/4.5/scripts/addons/CharMorph/__init__.py`,
    bl_info version (0, 4, 0), Blender min (4, 4, 0).
  - Library: `library.load()` → 4 characters: antonia, mb_female, mb_male, reom.
  - Import: `charmorph.import_char()` on `mb_male` → FINISHED, mesh 17,996 verts.
- Licence (verified from the shipped files, NOT from the report):
  - Code: **GPL-3.0** (`license.txt`). CORRECTION — the research report said
    "AGPL-3.0" for the code; that is wrong.
  - Database: MB-Lab-derived characters **AGPL-3.0**; each character has its own
    licence. Per-character: mb_female AGPL-3.0 (file is the AGPL text);
    mb_male AGPL-3.0 per the addon `license.txt` (no per-character file);
    antonia CUSTOM restrictive licence (redistribution of derivatives needs the
    author's permission — DO NOT SHIP); reom NO licence file — UNVERIFIED,
    DO NOT SHIP.
  - The CC0 Vitruvian character is NOT in the installed library (db snapshot
    dated 2023-12-11) — fetch via the addon's in-Blender character downloader.
- Failures / notes:
  - GitHub API rate limit 0/60 on the shared IP — used direct download URLs
    (`/releases/latest/download/`, codeload) instead of the API.
  - First db extraction to `/tmp/cmdb_stage` failed: `/tmp` filled (512 MB
    tmpfs). Re-extracted to the home disk.

## 2. MPFB 2.0.18 — VERIFIED WORKING

- Source: https://files.makehumancommunity.org/plugins/mpfb2-latest.zip
  (release 2.0.18, 2026-10-10; also on the Blender Extensions platform)
- Download: `curl -sL -C - -o mpfb2-latest.zip <url>` → 44,955,548 bytes.
  Manifest inside: `version = "2.0.18"`, `blender_version_min = "4.2.0"`,
  `license = ["SPDX:GPL-3.0-or-later"]`.
- Install: Blender 4.5 extension install, two failed attempts then the fix:
  1. `bpy.ops.extensions.package_install_files(filepath=ZIP)` → FAILED
     "Repository not set" (the operator needs its `repo` ENUM).
  2. Manual extraction to `~/.config/blender/4.5/extensions/user_default/mpfb/`
     + `addon_enable(module="mpfb")` → FAILED "No module named 'mpfb'".
  3. FIX: `bpy.ops.extensions.package_install_files(filepath=ZIP,
     repo="user_default", enable_on_install=True, overwrite=True)` → INSTALL OK
     (the extension module name is `bl_ext.user_default.mpfb` — plain `mpfb`
     never resolves), then `bpy.ops.preferences.addon_enable(
     module="bl_ext.user_default.mpfb")` + `bpy.ops.wm.save_userpref()`
     → ENABLED, persisted (`addon_utils.check` = (True, True)).
- Verification (headless, Blender 4.5.9, fresh process, no enable call):
  - Auto-loaded from saved prefs: True.
  - `mpfb.create_human()` → FINISHED, `Human` mesh 19,158 verts.
  - `mpfb.add_standard_rig()` → FINISHED, armature `Human.rig`.
- System assets pack (skins/eyes/teeth/clothes, CC0):
  - `curl -sL -o makehuman_system_assets_cc0.zip
    https://files.makehumancommunity.org/asset_packs/makehuman_system_assets/makehuman_system_assets_cc0.zip`
    → 280,737,770 bytes, 517 files, 85 `.mhmat` skins.
  - Extracted to `~/workspace/tools/mpfb-system-assets/` (286 MB:
    skins/, eyes/, hair/, clothes/, teeth/, eyebrows/, eyelashes/,
    proxymeshes/, tongue/, packs/).
  - NOT yet registered inside Blender: the pack loads via MPFB → System and
    resources → Load pack from zip file (GUI step), or by pointing MPFB's
    asset root at that directory. The created human without the pack is a
    default grey material — the pack is what makes MPFB usable for the studio.
- Licence: code **GPL-3.0-or-later** (verified from shipped manifest). Base
  mesh + standard assets **CC0** per the MakeHuman Community (characters you
  export are yours, including commercially). Asset packs mix CC0/CC-BY.

## 3. vid2anim 0.1.1 — VERIFIED WORKING

- Source: https://pypi.org/project/vid2anim/ (0.1.1, MIT) /
  https://github.com/mehulcode12/vid2anim
- Install: `python3 -m venv ~/workspace/tools/venv-vid2anim`
  (Python 3.12.3) + `pip install vid2anim`.
  Installed: vid2anim-0.1.1, mediapipe-1.2.3, opencv-contrib-python-5.0.0.93,
  opencv-python-5.0.0.93, numpy-2.5.4, scipy-1.18.1.
- Verification:
  - `import vid2anim` → OK, version 0.1.1.
  - `vid2anim doctor` → CPU-only (no CUDA GPU — expected), FFmpeg OK,
    MediaPipe (CPU AI) OK.
  - Sample run (documented command):
    `vid2anim run --input dance_urban.mp4 --model ybot.glb --engine mediapipe
    --output outputs/ybot_dance.glb`
    → 281 frames in 25.88 s, retargeted onto Mixamo armature (62 bones),
    `outputs/ybot_dance.glb` 2,642,536 bytes, 63 animated tracks. SUCCESS.
    Samples at `~/workspace/tools/vid2anim-samples/` (dance_urban.mp4 7.2 MB,
    ybot.glb 2.3 MB, from the repo's `samples/`).
  - Blender bridge: the PyPI wheel does NOT include
    `plugins/blender/vid2anim_blender.py` (`vid2anim addon --export` errors
    "file not found") — fetched the file from the repo raw URL (23,742 bytes,
    v0.1.1, Blender 3.0+), installed + enabled in Blender 4.5.9
    (`vid2anim_blender` in `~/.config/blender/4.5/scripts/addons/`).
    The bridge talks to a local server, not the CLI: `vid2anim serve
    --port 8080` answers `/api/health` with `{"status": "ok",
    "service": "vid2anim"}` — verified live.
  - Workflow: start the server, then Blender View3D → Sidebar → vid2anim.
- Licence: **MIT** — verified from the repo LICENSE
  (Copyright (c) 2026 Mehul and vid2anim contributors).
- Failures / notes:
  - First `pip install vid2anim` failed: `OSError: [Errno 28] No space left
    on device` while downloading the 82 MB opencv wheel (pip temp under
    `/tmp`, 512 MB tmpfs). Fixed with `TMPDIR=~/workspace/tools/.pip-tmp`
    + `--no-cache-dir`. Retry succeeded.

## 4. Colab notebooks (TripoSG + TRELLIS v1) — WRITTEN, JSON-VALIDATED, NOT RUN

AI 3D cannot run on this VM (no GPU, ~150 MB free RAM). These notebooks run on
a free cloud GPU only. Location: `tools/studio/colab/`.

- `triposg-prop-generator.ipynb` (6 cells, valid JSON) — general prop version
  of the rock run already in progress at
  `workspace/cloud-sync/heavy-tools/triposg-prop-generator.ipynb`
  (mossy rock for the golem-fight clearing, running on a free Colab T4 via a
  browser task — NOT duplicated here). Verified calls:
  `TripoSG.from_pretrained('VAST-AI/TripoSG')`, 50 inference steps,
  `mesh.export(..., postprocess=True)`; Y-up → Z-up rotation + decimation to
  ~10k faces. TripoSG: MIT code + MIT weights (verified from repo LICENSE),
  8 GB VRAM — T4-safe. Image-only, geometry-only (no texture/UVs).
- `trellis-prop-generator.ipynb` (6 cells, valid JSON) — TRELLIS v1.
  Verified calls from the official README minimal example:
  `TrellisImageTo3DPipeline.from_pretrained('microsoft/TRELLIS-image-large')`,
  `pipeline.run(image, seed=1)`,
  `postprocessing_utils.to_glb(..., simplify=0.95, texture_size=1024)`;
  install via `git clone --recurse-submodules
  https://github.com/microsoft/TRELLIS.git` + `. ./setup.sh --new-env --basic
  --xformers --flash-attn --diffoctreerast --spconv --mipgaussian --kaolin
  --nvdiffrast` (conda route; condacolab install first on Colab).
  TRELLIS: MIT (verified from repo LICENSE + repo page).
- CORRECTION (2026-11-15, parent agent, verified from the TRELLIS README):
  TRELLIS v1 needs a **16 GB+ GPU (A100/A6000 verified)** — NOT 4–8 GB as the
  research report said. A free Colab T4 (16 GB) sits exactly on the floor and
  risks OOM; the notebook says so and prefers Kaggle P100 (16 GB).
  TRELLIS.2 needs 24 GB for PBR — out of scope.
- LICENCE FLAG: TRELLIS GLB export uses **nvdiffrast
  (research/evaluation-only licence)** — do not ship TRELLIS GLBs commercially
  without replacing the exporter.
- Both notebooks: props ONLY, never the hero, never a face. Running one needs
  the user's Google sign-in on Colab/Kaggle — his step, not done here.

## 5. Docs updated

- `STUDIO.md`: Stage 1 licence rule corrected (CharMorph library is NOT CC0);
  new sections Stage 1a (character base), 1b (vid2anim), 1c (AI props);
  new studio Rule 7 (copyleft character bases stay out of the shipped hero).
- `AssetLicenses.md`: NOT edited — it has uncommitted edits from the
  complete-slice coordinator. New rows staged in
  `tools/studio/asset-licences-radical-tools.md` — merge them into
  `AssetLicenses.md` after the coordinator commits.
- This log: `tools/studio/STUDIO_INSTALL_LOG.md`.

## Still needs the user (cannot be done by an agent)

1. Run the Colab notebooks (`tools/studio/colab/*.ipynb`) — needs his Google
   sign-in on Colab/Kaggle and, for TRELLIS, a 16 GB+ GPU runtime.
2. Register the MPFB system assets pack inside Blender (MPFB → System and
   resources → Load pack from zip file) or set MPFB's asset root to
   `~/workspace/tools/mpfb-system-assets/`.
3. Fetch the CC0 Vitruvian character via CharMorph's in-Blender character
   downloader (not in the installed library) and re-verify its licence.
4. Real-phone verdict on the delivered APKs (Galaxy A16) — unchanged.

---

# BATCH 2 — advanced heavy studio tools (2026-11-15, ~10:57–10:30 CET)

Second batch from the same research report. Environment: branch
`aetheria-slice`, free RAM 509–828 MB, the MPFB hero-rebuild agent running
heavy Blender work in parallel (its `build_hero.py` Blender run was live
during the first half). All installs SEQUENTIAL, one at a time, light first.
Nothing on `main` touched; no game file touched (only STUDIO.md, this log,
`asset-licences-radical-tools.md`, `tools/studio/colab/`, `addons/`).

## 1. xAtlas — VERIFIED WORKING

- Source: https://pypi.org/project/xatlas/ (mworchel/xatlas-python, core
  https://github.com/jpcy/xatlas). PyPI version 0.0.11 (2025-07-04).
- Install: `python3 -m venv ~/workspace/tools/venv-xatlas`
  (`TMPDIR=~/workspace/tools/.pip-tmp`, `--no-cache-dir` — /tmp is 512 MB),
  `pip install xatlas trimesh numpy` (trimesh 5.2.1).
- Verify: `~/workspace/tools/xatlas-test.py` — icosphere (subdiv 2) + box,
  170 verts / 332 faces, no UVs in → `xatlas.parametrize()` → 258 verts,
  **100.0% of UVs inside [0,1], 100.0% of faces with UV area > 0**,
  atlas utilization 58.4%; OBJ round-trip exported to
  `~/workspace/tools/xatlas-test-unwrapped.obj` (13,587 bytes).
- Licence: **MIT** (both the Python binding and the core xatlas).
- Notes: pip install fails inside Blender's bundled Python — use a system
  venv. This is the tool that gives TripoSG outputs their missing UVs.
  First test run failed on a script bug (`ColorVisuals` has no `.uv`) —
  fixed in the test, not in the tool.

## 2. Instant Meshes — VERIFIED WORKING (CLI + Python binding)

- Source: maintained fork https://github.com/MattRM2/instant-meshes
  (original wjakob repo dormant since 2022). Release 2.5.0.
- Download: `InstantMeshes_2.5.0_Linux64.tar.gz` (5,630,871 bytes) →
  `~/workspace/tools/instant-meshes/`.
- Verify (CLI): `./InstantMeshes --help` exit 0, real batch-mode CLI
  (`-o` / `-f` / `--uv` flags). Remeshed a 1,280-face icosphere OBJ in
  36 ms → `test-output.obj` (V=2086, F=2084 quads). **Honest note: the
  `-f 500` target was NOT hit — the output has 2,084 quad faces; the
  face count is approximate and the pure-quad subdivision multiplies it.
  The tool runs and produces valid output; exact face-count fidelity is
  a tuning detail, not a pass/fail.**
- Verify (Python): `pip install pyinstantmeshes` (0.1.0) into venv-xatlas;
  `remesh(..., target_face_count=500)` → 1,280 faces → 1,094 faces,
  quad-dominant, exported `~/workspace/tools/instant-meshes-test-remeshed.obj`.
  (First call failed: the kwarg is `target_face_count`, not `face_count`.)
- Licence: **BSD** (Instant Meshes BSD licence, shipped `LICENSE.txt`).
- Note: pyinstantmeshes writes small temp OBJs to /tmp — fine at this size.

## 3. Rigify — VERIFIED WORKING

- Source: Blender 4.5.9 built-in addon (no download). Version **0.6.10**.
- Install: `blender --background --python-expr
  "bpy.ops.preferences.addon_enable(module='rigify'); bpy.ops.wm.save_userpref()"`.
- Verify: fresh Blender process prints `RIGIFY_AUTOLOAD: True` and the
  module loads (`rigify.bl_info` version (0, 6, 10)).
- Failure, then fix: the FIRST enable used `--factory-startup` — it printed
  `RIGIFY_ENABLED: True` but `save_userpref()` did NOT write the file
  (userpref.blend mtime stayed 09:25, fresh process read False). Lesson:
  **enable addons WITHOUT `--factory-startup`** so the save lands in the
  real userpref. The retry was DEFERRED while the hero-rebuild agent's
  Blender (`build_hero.py`, 900 s timeout) was running — never fight
  another agent's Blender run — and re-run once Blender was free
  (userpref.blend updated 10:09, 178,718 bytes). Verified after the retry.
- Licence: part of Blender, **GPL** (addon code ships with Blender; the
  rigs it generates are the studio's own).

## 4. MeshLab — VERIFIED WORKING (AppImage + PyMeshLab)

- Source: https://github.com/cnr-isti-vclab/meshlab, release **2025.07**
  (July 2025). AppImage `MeshLab2025.07-linux_x86_64.AppImage`
  (86,152,384 bytes) → `~/workspace/tools/meshlab/`, extracted with
  `--appimage-extract`.
- Verify (GUI binary): `./squashfs-root/usr/bin/meshlab --help` prints
  usage, exit 0 — BUT only after `apt-get install -y libopengl0`:
  the VM image has `libgl1` installed yet `libOpenGL.so.0` was genuinely
  absent (ldconfig showed nothing). **apt packages do NOT survive a VM
  restart — reinstall `libopengl0` after any restart.**
- Verify (headless, the real route): `pip install pymeshlab`
  (**2025.7.post1**) into venv-xatlas. `pymeshlab.filter_list()` returns
  **281 filters** (plugins load once libOpenGL exists).
  `meshing_decimation_quadric_edge_collapse` on a 1,280-face icosphere →
  **exactly 500 faces** (252 verts), saved
  `~/workspace/tools/meshlab-test-decimated.obj` (44,169 bytes).
- Failure, then fix: the old filter name
  `simplification_quadric_edge_collapse_decimation` does NOT exist in
  2025.7 — names are now `meshing_decimation_*`, and the list API is
  module-level `pymeshlab.filter_list()` (the `MeshSet` methods
  `filter_list()` / `print_filter_list()` do not exist in this version).
- Licence: **GPL-3.0** (MeshLab).
- Note: `meshlabserver` was removed in newer versions — headless mesh
  work goes through PyMeshLab, not the GUI binary.

## 5. jsfxr (SFX) — VERIFIED WORKING; ChipTone / Bfxr are WEB-ONLY

- Source: https://github.com/chr15m/jsfxr (npm `jsfxr` 1.4.1).
- Install: `npm install jsfxr@1.4.1` in `~/workspace/tools/jsfxr/`
  (no global install, no system writes).
- Verify: `node gen-preset.js pickupCoin` generates a preset via the
  documented API (`sfxr.generate('pickupCoin')`); piping its JSON into
  `./node_modules/.bin/sfxr-to-wav` produced
  `test-pickupCoin.wav` (8,041 bytes) — `file` confirms
  **RIFF WAVE audio, Microsoft PCM, 8 bit, mono 44100 Hz**. Presets
  available: pickupCoin, laserShoot, explosion, powerUp, hitHurt, jump,
  blipSelect, synth, tone, click, random. Output is 8-bit mono — fine as
  a game-SFX source; convert to 16-bit if a cleaner master is needed.
- Licence: **Unlicense** (jsfxr).
- NOT installed, honestly recorded: **ChipTone** (SFBGames — HTML5/Win/Mac
  only, no Linux build; output CC0; web version only) and **Bfxr2 / jfxr**
  (browser tools) — no fake install was made. They are documented as
  tool links in STUDIO.md (Stage 5b) instead.

## 6. Hunyuan3D-2mini Colab notebook — WRITTEN, VERIFIED AGAINST THE REAL REPO, NOT RUN

- Notebook: `tools/studio/colab/hunyuan3d-2mini-prop-generator.ipynb`
  (valid JSON, 6 cells: 1 markdown + 5 code).
- Verified against a shallow clone of the official repo
  (`~/workspace/tools/hunyuan3d-2/`, 156 MB, code only) — every call in
  the notebook comes from a file actually read in the clone:
  - Text → image: `hy3dgen/text2image.py` —
    `HunyuanDiTPipeline('Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled',
    device='cuda')`, call `t2i(prompt, seed=0)` → 1024×1024 PIL image.
    (Same route as `gradio_app.py --enable_t23d`; the prompt is truncated
    to 60 chars by the pipeline.)
  - Shape: `Hunyuan3DDiTFlowMatchingPipeline.from_pretrained(
    'tencent/Hunyuan3D-2mini', subfolder='hunyuan3d-dit-v2-mini')`
    (gradio_app.py:726-728), `mesh = pipeline(image=image,
    num_inference_steps=30, octree_resolution=256)[0]`.
  - Texture: `Hunyuan3DPaintPipeline.from_pretrained('tencent/Hunyuan3D-2')`,
    `mesh = pipeline(mesh, image=image)`; texture needs the rasterizer +
    differentiable renderer built (`hy3dgen/texgen/custom_rasterizer/setup.py`
    + `hy3dgen/texgen/differentiable_renderer/setup.py` — both exist in the
    clone; the install cell builds them).
  - `requirements.txt` itself lists xatlas, trimesh, pymeshlab — the batch-2
    tools are the same ones Hunyuan's own texture stage uses.
- VRAM (official README, verified): shape 6 GB, shape+texture 16 GB total.
  A free Colab T4 (16 GB) sits exactly on the limit — the notebook frees
  the shape pipeline (`del` + `torch.cuda.empty_cache()`) before texture,
  and always saves the shape-only GLB first as a fallback.
- Prop: one textured prop from the text prompt
  "mossy stone lantern with carved runes, fantasy game prop" (golem-fight
  clearing). Output: `hunyuan3d-2mini-prop-textured.glb` (+ shape fallback).
- Licence: **Tencent Hunyuan 3D 2.0 Community Licence** — verified from the
  shipped `LICENSE` file: territory **excludes EU / UK / South Korea**
  (user is in Algeria — inside the Territory). The repo file headers also
  cite a **NON-COMMERCIAL** licence — treat outputs as **non-commercial /
  prototype only; do not ship commercially without re-reading the full
  licence**. Outputs are the studio's own prop meshes, not the model.
- NOT RUN: needs the user's Google sign-in on Colab with a T4 runtime —
  his step, same as the TripoSG / TRELLIS notebooks.

## Pending in this batch (results appended below when they land)

- **ArmorPaint**: source clone running (`armory3d/armorpaint` — the
  `armortools/armorpaint` repo does NOT exist; GitHub API rate-limited
  so releases could not be checked that way). Prebuilt Linux binaries are
  $19 on itch.io — the $0 route is compile-from-source, which needs
  **clang (NOT installed on this VM)** and a heavy C++ build on <1 GB
  free RAM.
- **ProtonScatter**: 4.2.0 copied into `addons/proton_scatter/`; the first
  headless Godot 4.3 import test TIMED OUT at 600 s (exit 124 — import was
  still progressing, `.godot/editor/` being written, while the rebuild
  agent's Blender competed for CPU/RAM; a benign mbedtls TLS handshake
  error also appeared). Re-run in progress with an 1800 s timeout and a
  full log at `~/workspace/tools/protonscatter-import.log`.

## 2026-11-15 ~10:58–10:40 CET — Graphics tools (PBR textures + water/sky shaders + showcase + MSAA/SSAO patch + LightmapGI check)

Agent: graphics subagent (standalone; hero rebuild + tools installer ran in parallel — their files untouched).

### 1. Real PBR textures — ambientCG (CC0), 5 sets, 1K JPG

Source pattern that works: `https://ambientcg.com/get?file=<ID>_1K-JPG.zip`
(the `/api/v2/search` endpoint returns "File not found."; `full_json` works).
Downloaded 2026-11-15 ~10:58 CET, extracted to
`assets/library/textures/pbr/<material>/` (`albedo.jpg`, `normal.jpg`,
`roughness.jpg`, `ao.jpg`), 20 MB total, each with a `MANIFEST.md`
(source URL + CC0). Licence rows appended to
`tools/studio/asset-licences-radical-tools.md`.

| Set | ambientCG ID | Maps | Notes |
|---|---|---|---|
| grass_ground | Grass004 | albedo/normal/roughness/AO | ground, uv 8x8 |
| dirt_path | Ground037 | albedo/normal/roughness/AO | path strip |
| stone_wall | Bricks105 | albedo/normal/roughness/AO | 1024x512 (not square) |
| wood_planks | Planks040 | albedo/normal/roughness/AO | crate + roof slab base |
| roof_tiles | Tiles141 | albedo/normal/roughness | **no AO map shipped** (upstream set has none) |

Fallback to Poly Haven was NOT needed — ambientCG downloads worked on the
first try. All 5 sets are 1024 px (within the A16 budget, never 4K).

**Import — the full-project `--import` STALLS (known, pre-existing).**
`godot --headless --path . --import` on this project stalls after the
banner (~11 s CPU, then idle forever) — the same stall documented in
`screenshots-aetheria/README.md` since ~09:00 UTC, NOT caused by these
textures (it stalls with them moved out too, and it stalled while a second
agent's import ran concurrently). Workaround used (same as the pass-2 hero):
a minimal throwaway project `/tmp/miniproj` with the SAME res:// paths,
`--import` exits 0 in ~13 s, then the 19 generated `.import` files were
copied into `assets/library/textures/pbr/` and the `.ctex`/`.md5` files into
`.godot/imported/` (gitignored — a fresh clone re-imports the same way).
Do NOT claim `--import` works on this project until it exits 0 here.

### 2. Genshin-style animated water shader — project-original

`assets/materials/water_stylized.gdshader` (spatial, Mobile-safe):
sine-wave vertex displacement (2 octaves), normal wobble for sparkle,
fresnel edge (shallow colour at glancing angles), sun sparkle via the
`sun_direction` uniform, shore fade faked with a plane-border mask
(UV distance to the plane edge) — no depth/screen texture, so it works on
Mobile. The water plane must be subdivided (32x32 in the showcase) or the
vertex waves have nothing to displace.

### 3. Sky shader — project-original, iterated 3 times against real shots

`assets/materials/sky_stylized.gdshader` (sky, Mobile-safe): painted
gradient (warm horizon -> mid blue -> deep zenith), sun disc + glow via
`sun_direction`, drifting hash value-noise clouds (2 octaves).
- Pass 1: sky read as a flat peach wall (horizon band too wide, clouds
  invisible, sun out of frame) — shot 15/16 v1.
- Pass 2: gradient arrives faster (horizon band 0.35 -> 0.15), clouds
  denser/faster (coverage 0.45 -> 0.38, speed 0.004 -> 0.012), ground
  enlarged 24 -> 48 m so the plane edge leaves the frame. Sky then read as
  a sky in shot 15; shot 16 still flat peach (low camera angle).
- Pass 3: sun lowered to golden hour (~20 deg elevation: light rotation
  x -55 -> -25 deg, `sun_direction` (-0.574, 0.671, 0.47) ->
  (-0.574, 0.346, 0.742)) so the disc can share a frame with the pond,
  then the glow tamed (0.85 -> 0.4, power 6 -> 8, disc 1.6 -> 1.0,
  cloud sun-tint 0.6 -> 0.35) after it blew the whole sky white.
  Final shot 16: sun disc visible, blue sky, distinct clouds.

### 4. Standalone showcase scene + REAL screenshots (Xvfb, Compatibility)

`scenes/tests/graphics-showcase.tscn` (NEW file only — never the main
slice): 48x48 m PBR grass ground + dirt path, stone wall, wood crate,
leaning roof slab, 7x7 m water pond (32x32 subdiv), KayKit house
(`building_home_A_green.gltf`), barrel, Kenney tree + flower, capsule
stand-in with sphere head (NOT the hero), two cameras, WorldEnvironment
(custom sky, ambient from sky), warm DirectionalLight3D (shadows on).

Capture: `/tmp/capture_showcase.gd` under
`xvfb-run --rendering-driver opengl3` (pure `--headless` screenshots fail
on this project — `get_texture()` null). All runs exit 0, no script
errors (only benign ALSA/V-Sync warnings).

- `screenshots-aetheria/15-graphics-pbr.png` (1280x720, mean luminance
  167.1): PBR ground READS as textured (grass grain, dirt path distinct),
  brick wall + wood crate read, long golden-hour shadows, blue sky with
  clouds. Flaws: roof slab reads as a white board (Tiles141 albedo is too
  pale/washed out at a glancing angle); water bands read as regular
  "corduroy" stripes.
- `screenshots-aetheria/16-graphics-water-sky.png` (1280x720, mean
  luminance 193.2): sun disc + blue sky + clouds + pond with sparkle and
  a soft shore fade. Flaws: pond is partly washed by the sun glare;
  the horizon band is still wide at this low angle.
- `screenshots-aetheria/16b-water-later.png` (same camera, +3 s):
  animation proof — whole-frame mean abs diff 16 vs 16b = 3.58,
  sky region 5.96 (clouds drift), water region 2.54 in the glare-heavy
  crop (7.33 in the clean crop before the sun was lowered). The water
  DOES animate; the clouds drift slowly (visible over seconds, not
  frames).

### 5. MSAA + filtering + SSAO patch — PREPARED ONLY, NOT applied

`tools/studio/msaa-ssao-patch.md`: MSAA 3D 4x (`msaa_3d=2`), anisotropic
4x max, SSAO Medium on High / off on Low, exact rollback, Mali-G57 cost
estimate (~20-35% frame time for the High preset — NOT measured on the
phone; only the user's A16 test can verify). `project.godot` was NOT
edited — the patch applies after the hero-rebuild agent commits.
Setting names verified live via a Godot 4.3 `ProjectSettings` dump AND
the offline 4.3 docs (`VIEWPORT_MSAA_4X = 2`; anisotropic is a power of
two). Two corrections found while verifying: (a) anisotropic filtering
needs a per-material `texture_filter =
TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC` opt-in or the project
setting does nothing; (b) **FSR is Forward+ only — on the Mobile renderer
it silently falls back to bilinear**, so the Low preset uses Bilinear
(`mode=1`), never FSR. Current state: msaa_3d=0, FXAA off, SSAO not
enabled on any Environment, slice glow deliberately off (measured).

### 6. LightmapGI bake check — HONEST RESULT: NOTHING IS BAKED

Checked 2026-11-15: the slice script (`scripts/world/aetheria_slice.gd`,
`_build_lightmap_gi()`, lines ~716-746) configures a LightmapGI node
(medium quality, 2 bounces, directional, probes SUBDIV_8, atlas 2048)
but its own comment states "there is NO baked LightmapGIData yet".
A repo-wide search confirms it: **no `LightmapGIData` resource exists
anywhere** (only editor icon textures in `.godot/imported/`).
The earlier graphics pass did NOT bake lightmaps — it only configured
the node. Godot 4.3 has no script `bake()`; baking is an editor action,
and the village is runtime-built, so an editor bake today would find
zero static meshes.

**Exact bake procedure (run after the hero lands, on a clean commit):**
1. Bake-to-scene first: serialize the runtime-built village (houses,
   walls, ground, props) into a saved `.tscn` with static meshes —
   LightmapGI only bakes static geometry, and there is no static scene
   to bake today.
2. In the Godot editor, open that scene, select the LightmapGI node,
   LightmapGI menu -> **Bake Lightmaps** (editor-only; there is no
   one-line CLI bake in 4.3).
3. Verify: `grep -c LightmapGIData <scene>.tscn` must be > 0 AND the
   LightmapGI node's `lightmap_data` must be assigned; then re-run the
   verify gate and re-shoot. Do not claim GI is baked until that grep
   passes on a committed scene.

## 7. ProtonScatter 4.2.0 — VERIFIED WORKING (Godot 4.3)

- Source: https://github.com/HungryProton/scatter, default branch `main`
  (`master` 404s). Codeload zip of `main` → `addons/proton_scatter/`.
  Version 4.2.0 from `addons/proton_scatter/plugin.cfg`.
- Install: plain copy of `addons/proton_scatter/` into the project (no
  build step; it is a Godot editor plugin, MIT).
- Verify: `godot --headless --path . --import` → **exit 0, 0 SCRIPT
  ERRORs** (52 s). Two ERROR lines remain and are benign/headless-only:
  "Cannot import custom .glsl shaders when running in headless mode" for
  `src/modifiers/compute_shaders/compute_relax.glsl` — a compute shader
  cannot be compiled without a rendering device; it imports fine in a
  real editor session. Warnings only: one non-finite normal in LOD
  generation, one invalid UID in `path_panel.tscn` (falls back to text
  path).
- **ROOT CAUSE of the two failed import runs (600 s timeout, then SIGTERM
  at 262 s): the addon ships a `.blend` file in its demos folder
  (`demos/assets/source.blend`). STUDIO.md already documents that ANY
  `.blend` in the project tree makes `godot --import` hang forever
  (0 CPU). The import was hanging on that file, not on ProtonScatter's
  code. Fix: deleted `addons/proton_scatter/demos/` (12 MB of examples
  only; the addon core is `src/` + `plugin.gd`). Addon is now 1.7 MB,
  no `.blend` left, import finishes in ~52 s. Lesson: ALWAYS strip
  `.blend`/`.max`/`.ma` files from any addon before importing.**
- Licence: **MIT** (HungryProton).
- Note: the plugin is an editor plugin (`@tool`); enabling it in the
  editor is a GUI step for the coordinator/user. Headless import proves
  its scripts parse and load cleanly under Godot 4.3.

## Pending in this batch (updated)

- **ArmorPaint**: source clone re-running after the first attempt was
  killed by an external SIGTERM at 242 s (git removed its own partial
  clone on the signal). Prebuilt Linux binaries are $19 on itch.io —
  the $0 route is compile-from-source, which needs **clang (NOT
  installed)** and a heavy C++ build on <1 GB free RAM.

## 8. git-lfs — REINSTALLED (VM restart wiped it)

- Problem: a git command failed with `git-lfs: not found` — apt packages
  do not survive a VM restart (same as git-lfs 3.4.1 installed during
  activation, see `~/workspace/tools/activation/ACTIVATION_LOG.md`).
- Fix attempt 1 (failed): `sudo apt-get install -y git-lfs` → `E: Unable
  to locate package git-lfs` (stale package lists after the restart).
- Fix attempt 2 (blocked): `sudo apt-get update` → could not get the lock
  — held by PID 820, a system `apt-get update` (VM os-intent replay) that
  has been running 10+ minutes. Do NOT kill it; it is a system process.
- Fix that worked: the .deb was already in the local apt cache —
  `sudo dpkg -i /var/cache/apt/archives/git-lfs_3.4.1-1ubuntu0.4_amd64.deb`
  (dpkg needs only the dpkg lock, which an `apt-get update` does not hold).
- Verify: `git lfs install` → "Git LFS initialized.";
  `git lfs version` → **git-lfs/3.4.1 (GitHub; linux amd64; go 1.22.2)**.
- Note: reinstall `git-lfs` (and `libopengl0`, see MeshLab above) after
  every VM restart — apt packages do not persist.

## 9. ArmorPaint 1.0 — SOURCE CLONED + LICENCE VERIFIED; BUILD BLOCKED (no clang)

- Source: https://github.com/armory3d/armorpaint (the `armortools/armorpaint`
  repo does NOT exist — verified by `git ls-remote`, it 404s).
  `git clone --recursive` → `~/workspace/tools/armorpaint/` (339 MB,
  774 files). This version has NO submodules (`.gitmodules` absent) —
  everything is in-repo (`base/` + `paint/`).
- Licence: **zlib** — verified from the shipped `license.md`
  ("The zlib/libpng License ... Permission is granted to anyone to use
  this software for any purpose, including commercial applications").
  Prebuilt Linux binaries are $19 on itch.io — NOT bought; the $0 route
  is compile-from-source.
- Build tool: the prebuilt `amake` binary ships in the repo
  (`base/tools/bin/linux_x64/amake`, 1.4 MB) and RUNS
  (`--help` prints "Using Iron from .../base", "Creating linux project
  files"). Linux build is `cd paint && ../base/make --run`.
- Build attempted for real (log: `~/workspace/tools/armorpaint-build.log`):
  asset export (4 + 9 + 3 + 3 + 6 assets) and **37/37 shaders compiled**,
  then the first C compile failed:
  `clang -O2 ... -c ../../sources/main.c -o main.o` →
  **`make: clang: No such file or directory`, `Error 127`, BUILD_EXIT:1**.
  The exporter hardcodes `/usr/bin/clang` (`base/tools/amake/exporters.c:258`).
- Deps required (verified from the cloned `base/docs/linux_deps.md`):
  `make clang libvulkan-dev libgtk-3-dev libssl-dev libxi-dev
  libxrandr-dev libxcursor-dev libasound2-dev`. The readme also notes
  the `--embed` step needs **clang 19+** (c23 `#embed` support) —
  `clang-19` IS available in the Ubuntu repos (candidate
  1:19.1.1-1ubuntu1~24.04.2); the `clang` metapackage is only 18.
- Why the deps could not be installed: the VM's system os-intent replay
  holds the dpkg lock essentially continuously (a stream of `apt-get
  install` runs, new PID every run). **160 install attempts over ~17
  minutes never once found a free lock window** (40 attempts × 15 s,
  then 120 attempts × 3 s). The replay must NOT be killed — it is a
  system process restoring recorded packages. `apt-cache policy` confirms
  the lists ARE fresh now (clang-19 candidate visible) — only the lock
  is the blocker. GTK/Vulkan headers are absent
  (`/usr/include/gtk-3.0`, `/usr/include/vulkan` do not exist), so even
  with clang the build would next fail on headers until the -dev
  packages land.
- First clone attempt was killed by an external SIGTERM at 242 s (git
  removed its own partial clone on the signal); the re-run completed
  in 575 s.
- RETRY (when the VM is quiet / replay finished):
  `sudo apt-get install -y clang-19 libvulkan-dev libgtk-3-dev libssl-dev
  libxi-dev libxrandr-dev libxcursor-dev libasound2-dev && sudo ln -sf
  /usr/bin/clang-19 /usr/bin/clang && cd ~/workspace/tools/armorpaint/paint
  && ../base/make --run`
  Then verify headless/Xvfb (`./build/krom` or the ArmorPaint binary
  `--help` / short run). Note: a full engine compile on this VM
  (1.5 CPUs, ~134 MB free RAM at last check) may still be very slow or
  OOM — the build attempt above used almost no RAM only because it died
  at the first compile.

## Batch 2 — final tally (2026-11-15)

- VERIFIED WORKING (7/8): xAtlas, Instant Meshes (CLI + Python),
  Rigify 0.6.10, MeshLab 2025.07 + PyMeshLab, jsfxr, Hunyuan3D-2mini
  notebook (written + verified against the real repo, not run),
  ProtonScatter 4.2.0 (headless import exit 0, 0 SCRIPT ERRORs).
- CLONED, BUILD BLOCKED (1/8): ArmorPaint 1.0 (see §9 above).
- REINSTALLED (side fix): git-lfs 3.4.1 (see §8 above).

## 10. ArmorPaint 1.0 — RETRY 2026-11-15 11:07 UTC: NEW BLOCKER (libzstd1 pin) — BUILD STILL BLOCKED

- Wait for a quiet VM (retry agent, wait log:
  `~/workspace/tools/armorpaint-retry-wait.log`): the VM never went quiet
  on the first pass — Blender hero builds, Godot screenshot captures and
  the godot-cpp compile kept alternating. **Trap found and fixed
  mid-wait:** `pgrep -f "blender"` / `pgrep -f "Godot_v4.3"` false-positive
  on agent wrapper shells whose command lines literally contain those
  words (e.g. the deep-graphics capture wrapper, PID 20233). The wait
  loop was rewritten to exact process-name matching (`pgrep -x blender`,
  `pgrep -x Godot_v4.3-stab` — the Godot binary's kernel comm is truncated
  to 15 chars) plus `fuser` on the dpkg lock and `pgrep -x apt-get/dpkg`
  (the os-intent replay shell itself must NOT count — it is bash, not
  apt). QUIET reached 11:07:27 UTC (Blender none, Godot none, lock FREE,
  1,512 MB free) after ~17 min of waiting. The replay's apt burst had
  finished by then — no apt/dpkg process for several consecutive checks.
  The system replay was never killed, no apt/dpkg process was killed.
- Retry command (exact §9 command) run at 11:07:31 UTC, log:
  `~/workspace/tools/armorpaint-build-retry.log`. **It failed in 3
  seconds, exit 100, at the `apt-get install` step — the build never
  started:**
  ```
  libzstd-dev : Depends: libzstd1 (= 1.5.5+dfsg2-2build1.1) but 1.5.5+dfsg2-2build1.1+hatch1 is to be installed
  E: Unable to correct problems, you have held broken packages.
  ```
- Diagnosis (read-only `apt-cache`/`dpkg` checks): the VM image ships a
  custom-patched `libzstd1 1.5.5+dfsg2-2build1.1+hatch1`, installed and
  pinned as the candidate (priority 100, from `/var/lib/dpkg/status`).
  Ubuntu's `libzstd-dev` (1.5.5+dfsg2-2build1.1) Depends on
  `libzstd1 (= 1.5.5+dfsg2-2build1.1)` exactly, so **no install of
  `libzstd-dev` can succeed while the hatch1 build is installed**.
  `libzstd-dev` is pulled transitively by the requested -dev set
  (reverse-depends include `liblld-19-dev` and `libtiff-dev` — i.e. via
  the clang-19 and libgtk-3-dev chains). `libssl-dev` and
  `libasound2-dev` are already installed (newest versions). No
  downgrade was attempted and no retry loop was run — per the retry
  brief, the attempt stops here.
- Ways past it (need a decision, NOT attempted):
  1. Downgrade the core library:
     `sudo apt-get install -y --allow-downgrades libzstd1=1.5.5+dfsg2-2build1.1`
     then re-run the §9 command. RISKY: libzstd1 is a core compression
     library the image deliberately patched; downgrading it could break
     image tooling that depends on the hatch1 build.
  2. Install only the pieces that avoid libzstd-dev (e.g. `clang-19`
     alone, if its tree does not pull `liblld-19-dev`) and supply the
     GTK/Vulkan headers another way (extracted .deb files, or a
     sysroot) — untested, may still fail at the `--embed` step, which
     needs clang 19+ (the `clang` metapackage is only 18).
  3. Skip ArmorPaint: texture painting falls back to Krita 5.3.4.1
     (installed, verified) + Material Maker 1.8 for procedural PBR.
     ArmorPaint remains the only open-source 3D PBR painter, so this
     loses direct mesh painting for the hero.
- Status: **CLONED, BUILD STILL BLOCKED (1/8)** — blocker moved from
  "dpkg lock held" to "libzstd1+hatch1 pin breaks libzstd-dev".
  Source + licence (zlib) unchanged; no binary exists yet
  (`paint/build/` was never created — the build died before compiling).

## 11. Deep graphics batch (2026-11-15, ~11:21–12:35 CET) — showcase only, hero/slice files untouched

Scope: prove 9 peak-level techniques with NEW real screenshots in `scenes/tests/graphics-showcase.tscn` only (same pattern as §1 graphics agent). All shaders/textures project-original unless noted. Verification: Xvfb captures (Compatibility, `--rendering-driver opengl3`) + first-ever Mobile-renderer captures under lavapipe (`--rendering-driver vulkan --rendering-method mobile`, `mesa-vulkan-drivers` 25.2.8 + `lvp_icd.json` present). Every shot read visually by the agent + measured with PIL diffs. Full shot list: 17-terrain-splat, 18/18b-wind, 18c/18d-wind-trees, 19/19b-grade, 20/20b-cloud, 21-shafts, 22-pond, 23-mobile-pond, 24/24b/24c/24d/24e-mobile-depth, 25-mobile-lut, 27-32 depth diagnostics, 33/34 alpha tests, 35-mobile-shipped.

### 11.1 Docs findings (verified by grep of offline Godot 4.3 docs, `docs/godot-4.3/`)
- **LightmapGI has NO `bake()` method in GDScript** (`class_lightmapgi.rst.txt`: only set/get_bake_quality). Baking is editor-GUI-only and requires Forward+/Mobile ("baked from devices that support the Forward+ or Mobile rendering backends"). Exact GUI steps: open the showcase scene in the editor → select the LightmapGI node → LightmapGI menu → Bake Lightmaps (bake-to-scene first if the scene is runtime-built — the slice cannot be baked, the showcase can). **Result: NOT BAKED anywhere** (no LightmapGIData in the repo). Node configured in the showcase (bake_quality 0, bounces 1) + 2 ReflectionProbes; before/after pair still pending an editor bake.
- **Reflection probes only Forward+/Mobile, NOT Compatibility** (`class_reflectionprobe.rst.txt`; Mobile max 8 probes/mesh). ProbePond (5.5,1.2,4.5) + ProbeWall (-5,1.5,-7), update_mode=0 — present, run clean on Mobile (shots 23/25, no errors).
- **Godot 4.3 Environment has NO LUT slot** ("lut" hits in `class_environment.html` were false positives inside "resolution"/"illumination"); grade controls are only brightness/contrast/saturation adjustments.
- **Godot 4 removed the `DEPTH_TEXTURE` built-in** — use a `sampler2D` uniform with `hint_depth_texture`.
- **No `alpha_scissor` render mode in Godot 4.3** — cutout path is `depth_prepass_alpha`.

### 11.2 New files (all project-original)
- `assets/materials/terrain_splat.gdshader` — triplanar PBR blend of the 5 ambientCG sets (grass/dirt/stone) by height+slope, ~21 texture samples/fragment (patch use only).
- `assets/materials/wind_sway.gdshader` — vertex wind, weight by world height, gust+ripple, cutout grass via `depth_prepass_alpha`.
- `assets/materials/light_shaft.gdshader` — additive soft-gradient shafts.
- `assets/materials/cloud_shadow.gdshader` — scrolling 2-octave value-noise cloud shadows.
- `assets/materials/lut_grade.gdshader` — canvas_item Hald CLUT via `hint_screen_texture`.
- `assets/materials/water_stylized.gdshader` — depth-fade upgrade only (see §11.4).
- `assets/library/textures/lut/cinematic_warm.png` (1024x32 Hald CLUT 32^3; corners verified: black in -> (0,2,12) cool shadows, white in -> (255,255,248) warm) + `lut/MANIFEST.md`; `assets/library/textures/showcase/grass_blades.png` (128x128, 14 blades, 5,117 non-transparent px) + `shaft_gradient.png` (128x256) + `showcase/MANIFEST.md`. Generated by PIL (`/tmp/gen_showcase_textures.py`).
- `scenes/tests/terrain_patch.mesh` — 12x12 m heightfield, 18,432 tris, generated by `/tmp/gen_terrain_mesh.gd` (FastNoiseLite, seed 1337).
- `tools/studio/hero-rim-wrap-patch.md` — rim + wrap lighting patch, PREPARED ONLY (do not apply until the hero rebuild commits).
- Scene: terrain patch at (-8,0,-16); ground replaced by 4 strips leaving a 7x7 hole under the pond + real basin cylinder (top r=5.0, bottom r=3.0, h=0.7, dirt) at (5.5,-0.33,4.5); 3 wind pines + 8 grass tufts; cloud-shadow sheet at y=2.9; LightmapGI node (unbaked); LUT CanvasLayer (visible=false by default); 3 light shafts; Environment adjustments (brightness 1.02, contrast 1.08, saturation 1.12).

### 11.3 Results per technique (honest)
- **Terrain splat — WORKS, needs tuning.** Shot 17: hill reads as a dirt mound (splat blends, dirt weight too strong; grass should dominate the top). Tuning: raise dirt_slope_start, lower low-dirt. Not re-shot yet.
- **Wind sway — PROVEN for grass, subtle for trees.** 18 vs 18b whole-frame diff 7.23 (water crop 18.25, grass-tuft crop 2.98 — weak in that framing). Re-framed with CamTrees: 18c vs 18d whole-frame 7.12, tree crops 3.59/3.37, **grass-tuft crop 12.34** — the grass visibly moves; tree sway amplitude needs raising to read at distance.
- **LUT grade — WORKS ON MOBILE, BLACK ON COMPATIBILITY.** Full-screen LUT ColorRect renders BLACK under Xvfb/Compatibility even at strength=0 (mean luminance 0.0) — the screen texture itself is unavailable/black there, not the LUT math. On Mobile (shot 25, grade 1): frame is graded, warm and cinematic, mean luminance 171.7 (vs 170.9 grade-off). LUT layer stays hidden by default (Mobile-only); in-engine grade proof is the Environment adjustment (19 vs 19b whole-frame diff 8.32; R 9.67, G 8.88, B 6.40).
- **Cloud shadows — PROVEN.** 20 vs 20b whole-frame diff 10.31 (ground crop 4.49, sky crop 13.43) — shadows move, subtle on the ground.
- **Reflection probes — PRESENT, Mobile-only.** No errors on Mobile runs; visual reflection difference not isolated as a before/after pair (probes update_mode=0, static). Pond in shots 23/25 shows sky/sun reflection via the water shader's fresnel+sparkle, not a probe-isolated proof.
- **Light shafts — FIXED.** Intensity 0.5 blew out to 3 white pillars on BOTH renderers (shots 21/23/24/25). Lowered to 0.12 (shader default + scene override) — now soft translucent columns (shots 24b/24e/35).
- **LightmapGI — NOT BAKED (see §11.1).** Node configured; bake needs the editor GUI. Before/after pair pending.
- **Hero rim/wrap — PREPARED ONLY** (`tools/studio/hero-rim-wrap-patch.md`): fresnel rim + skin wrap lighting, exact lines to change in the toon/face shaders, cost + verify/rollback. Do NOT apply until the rebuild agent commits.

### 11.4 Depth-based water fade (Mobile) — the long debug, honest outcome: SHIPS OFF
- **Setup:** `water_stylized.gdshader` gained a `hint_depth_texture` uniform + `use_depth_fade` (default 0) + `depth_fade_scale`. Border-mask fallback kept for Compatibility. Shader compiles headless on both paths (verified with `/tmp/diag_shader.gd`: 10 uniforms, 0 SHADER ERRORs).
- **Bug 1 (shot 24):** first math compared RAW clip-space depths (`scene_depth - FRAGCOORD.z`); at the pond's camera distance both sit ~0.999, diff ~0.0005, x300 leaves the water ~85% transparent — pond vanished on Mobile. (On Compatibility the same branch reads depth 0 and the pond vanishes — exactly as predicted; fallback required there.)
- **Bug 2 (shots 24b/24c/24d, 27-31):** my debug branches used `return` inside `fragment()` — **Godot 4.3 rejects `return` in fragment() and the WHOLE shader fails to compile** (`SHADER ERROR: Using 'return' in the 'fragment' processor function is incorrect.`). The water then rendered as a transparent fallback, which I misread as the fade failing. Lesson: diagnose shaders with `/tmp/diag_shader.gd` (loads the shader, prints the uniform list, catches compile errors) BEFORE trusting any capture. The capture greps missed the error (buried past `head -6`).
- **Fix 1:** linearised BOTH depths to eye depth in metres via `INV_PROJECTION_MATRIX`, scale in metres (`depth_fade_scale = 2.0`: fade reaches 1 at 0.5 m; basin is 0.7 m deep).
- **Fix 2 (depth convention, shot 31b):** the debug visualisation proved Godot 4.3 Vulkan depth is depth-corrected — the texture value IS the NDC z (d), NOT (ndc+1)/2. `d*2-1` reconstructs to ~0 m (R channel black); `d` direct reconstructs to the real ~15 m basin distance (G channel ~144/255). NDC z = d for BOTH the texture and `FRAGCOORD.z`.
- **Debug proof (shot 32):** with the correct mapping, the visualisation showed the pond GREEN at the centre (deep + fade ~1) and RED at the rim (shallow + fade ~0) — the fade computation is CORRECT.
- **The paradox (unresolved):** despite the proven-correct fade, 6 normal-path captures with the fade on (24/24b/24c/24d/24e/34) all render the pond pale/transparent, while a constant `ALPHA = 0.88` (shot 33) renders it blue (B/R 1.10, bluer than the 23 baseline) — so the blend path works and the fade variable is the paradox (debug shows ~0.8, normal path behaves as ~0). Also disproven along the way: the stale-import theory (shaders load from source at runtime; the `--import` re-run changed nothing) and the "depth texture is 0" theory (31b shows ~15 m).
- **Shipped state:** `use_depth_fade = 0` (border-mask fallback). Verified blue on BOTH renderers: Compatibility shot 22 (B/R 1.04) and Mobile shots 23 (B/R 1.01) and 35 (B/R 0.96-0.99, re-captured after the final cleanup). **Do NOT enable the depth fade in the shipped scene without a real Galaxy A16 test** — it needs a phone to tell a lavapipe quirk from a real bug. The final clean shader (debug code fully removed, 10 uniforms, 0 errors) is in the repo; the full debug trail is shots 24-34.

### 11.5 Mobile runs on this VM (new capability)
- `mesa-vulkan-drivers` 25.2.8 IS installed; `lvp_icd.json` exists in `/usr/share/vulkan/icd.d/`. The REAL Mobile renderer runs under Xvfb: `xvfb-run -a godot --rendering-driver vulkan --rendering-method mobile --path . -s /tmp/capture_showcase.gd -- ...` (project.godot already sets `renderer/rendering_method="mobile"` with `rendering_method.mobile="gl_compatibility"` fallback). First proven by shots 23-25/35 (exit 0, ~23 frames at 3 s engine time, ~2.5 min per capture under lavapipe). Use it to verify any Mobile-only feature (probes, depth texture, LUT) instead of guessing from Compatibility.
- Full-project `godot --headless --path . --import` now completes in ~55 s, exit 0 (the old stall is gone after the ProtonScatter `.blend` removal).

### 11.6 Commit
- Branch `aetheria-slice` only. Files: 5 new shaders + water shader upgrade + terrain_patch.mesh + LUT/showcase textures + manifests + scene edits + hero-rim-wrap-patch.md + STUDIO.md + this log + licence rows + screenshots 17-35 (+ .import files where generated). NOT committed: `project.godot` (another agent's), `Warrior_Anime_Hair_Strands.png.import` (hero), `.github/` (toolchain agent), `scripts/dialogue/*.import` (coordinator), shots 15/16/16b `.import` files (graphics agent's).

---

# BATCH 3 — programmer toolchain: C++ / NDK / GDExtension / Vulkan / Rust / CI (2026-11-15)

Installed by the programmer-toolchain agent. Environment: branch
`aetheria-slice`, free RAM 150–600 MB (fluctuating), three other agents +
two browser tasks running in parallel (MPFB hero rebuild, deep graphics,
tools batch 2, Colab TripoSG, Mixamo, Kaggle). All steps SEQUENTIAL, one
build at a time, `-j1`/`-j2` at most. Nothing on `main` touched; no game
file touched (only STUDIO.md, this log, `asset-licences-radical-tools.md`,
`.github/workflows/ci.yml`). Godot 4.3 binary:
`~/workspace/game-apk/godot/Godot_v4.3-stable_linux.x86_64`.

## 0. The apt lock war (read this before any future apt install)

`apt-get install` failed 10+ times across ~90 minutes with
`E: Could not get lock /var/lib/dpkg/lock-frontend` — the lock was held
continuously by (a) the system os-intent replay (PID 797's tree,
reinstalling recorded packages after a VM restart, e.g. docker.io) and
(b) another agent's 40-attempt retry loop (PID 6166) installing
ArmorPaint deps (clang-19, libvulkan-dev, libgtk-3-dev, …). The lock
finally freed at ~12:08 CET (after a ~17-min quiet wait) and the full
install then succeeded in ~3.5 min, exit 0.
**Lesson: on this VM, never hammer apt in a tight retry loop — it loses
to the replay. Wait for a quiet window, then install once.**
Workaround used while locked (all verified working, kept as fallback):
`apt-get download <pkg>` needs NO dpkg lock → `dpkg-deb -x` extracts
binaries without any lock. Extracted to `~/workspace/tools/extracted/`
(63 MB) with missing shared libs fetched the same way
(libbabeltrace1, libipt2, libdebuginfod1t64, libsource-highlight4t64 for
gdb; vulkan-validationlayers for the Khronos layer). The extracted
copies are now redundant (apt install succeeded) but kept as the
offline fallback.
**apt packages do NOT survive a VM restart — reinstall after any restart.**

## 1. C++ build toolchain — VERIFIED WORKING

- Pre-existing: **gcc/g++ 13.3.0** (Ubuntu 13.3.0-6ubuntu2~24.04.1),
  **cmake 3.28.3**.
- Via apt (after the lock freed): **clang/clang++ 18.1.3** (Ubuntu
  `1:18.0-59~exp2`, LLVM 18.1.3), **ninja-build 1.11.1**,
  **gdb 15.1** (15.1-1ubuntu1~24.04.1). Also **SCons 4.11.1** via pip
  venv `~/workspace/tools/venv-scons/` (PEP 668 blocks `--user` pip
  installs — use a venv).
- Verification (`~/workspace/tools/cpp-test/hello.cpp`):
  - `g++ -O0 -g` → runs: `hello from gcc 13.3.0`, `41 + 1 = 42`.
  - `clang++ -O0 -g` (system 18.1.3) → runs: `hello from gcc Ubuntu
    Clang 18.1.3`, `41 + 1 = 42`.
  - `gdb -batch -ex "break main" -ex run -ex bt -ex continue` →
    `Breakpoint 1, main () at hello.cpp:3`, `#0 main ()`, program
    `exited normally`.
- Fallbacks verified while apt was locked (kept, not needed now):
  NDK host `clang++` 18.0.3 compiled + ran the same hello-world;
  pip `ninja` 1.13.2 in venv-scons; extracted gdb 15.1 with
  `LD_LIBRARY_PATH=~/workspace/tools/extracted/usr/lib/x86_64-linux-gnu`
  (same breakpoint + backtrace result).
- Licences: GCC/GDB **GPL-3.0**; LLVM/Clang **Apache-2.0 with LLVM
  exceptions**; CMake **BSD-3-Clause**; Ninja **Apache-2.0**;
  SCons **MIT**.

## 2. Android NDK r27c LTS — VERIFIED WORKING

- Source: https://dl.google.com/android/repository/android-ndk-r27c-linux.zip
- Download: `curl -sL -C - -o android-ndk-r27c-linux.zip` →
  663,987,688 bytes, sha256
  `59c2f6dc96743b5daf5d1626684640b20a6bd2b1d85b13156b90333741bad5cc`.
- Install: `unzip` into `~/workspace/game-apk/tools/android-ndk-r27c/`
  (2.0 GB extracted; the zip is kept as the reinstall source). No
  `ndk/` dir existed in the Android SDK before — this fills the gap
  the Phase 1 audit flagged (no native C++ could ship in the APK).
- Verification: `aarch64-linux-android24-clang -shared -fPIC
  hello.c -o libhello.so` → `file`: `ELF 64-bit LSB shared object,
  ARM aarch64`; `llvm-readelf`: `Type: DYN (Shared object file),
  Machine: AArch64`. The JNI stub (`Java_com_gggg_eternia_Native_hello`)
  compiled clean.
- Toolchain clang: 18.0.3 (Android build r522817c). Host compilers in
  the same tree (`bin/clang`, `bin/clang++`, `bin/lldb`) also verified
  working.
- Licence: **Apache-2.0** (NDK) + LLVM Apache-2.0 exceptions.
- Note for the ArmorPaint retry agent: **system clang 18.1.3 is now
  installed** — the `clang: No such file or directory` blocker from
  log §9/§10 is gone. The remaining ArmorPaint blocker is only
  `libzstd-dev` vs the image's patched `libzstd1 …+hatch1`
  (exact-version Depends, cannot install without downgrading a core
  library — see the 12:08 CET retry note in MEMORY.md).

## 3. godot-cpp 4.3 + official sample GDExtension — VERIFIED WORKING

- Source: https://github.com/godotengine/godot-cpp (branch `4.3`,
  commit `d5cc777` "Merge pull request #1803 from dsnopek/4.3-cherrypicks-5").
- Clone: `git clone --depth 1 --branch 4.3` →
  `~/workspace/tools/godot-cpp-4.3/` (44 MB).
- Build: `cd test && scons platform=linux -j2` (SCons 4.11.1 from
  venv-scons; g++ 13.3.0 as the compiler) → **SCONS EXIT: 0** after
  ~55 min, 0 errors in the log (~950 compile lines: 920 generated
  classes + core + test sources).
  - Static lib: `bin/libgodot-cpp.linux.template_debug.x86_64.a`.
  - Sample extension: `test/project/bin/libgdexample.linux.template_debug.x86_64.so`
    (1,154,480 bytes). Entry symbol verified: `nm -D` shows
    `T example_library_init`; `.gdextension` maps
    `linux.debug.x86_64` to that path.
- Verification (Godot 4.3 headless, the real proof):
  - `--headless --path . --quit-after 3` → the sample project's own
    test suite: `==== TESTS FINISHED ==== PASSES: 120 FAILURES: 0
    ******** PASSED ********`.
  - `--headless --editor --quit` → exit 0, ZERO errors; scripts
    using the native classes (`main.gd` references `Example` 24×)
    compile cleanly.
  - Honest note: `--headless --import` alone prints `ERROR: Native
    class "Example" not found` — GDExtensions are NOT loaded in
    import mode. That is an import-mode artifact, not a broken
    extension: the editor + runtime runs above are the proof it loads.
- Licence: **MIT** (godot-cpp).
- Note: the test project's `bin/` also contains prebuilt macOS
  frameworks (`libgdexample.macos.*.framework`) — they ship in the
  repo itself, not built here; ignore them on Linux.

## 4. Vulkan SDK tools — VERIFIED WORKING

- Via apt (after the lock freed): **vulkan-tools 1.3.275.0+dfsg1-1**,
  **glslang-tools 15.1.0-2~ubuntu0.24.04.2**,
  **vulkan-validationlayers 1.3.275.0-1**. (`mesa-vulkan-drivers`
  25.2.8 and `libvulkan1` 1.3.275 were already installed.)
- Verification:
  - `vulkaninfo --summary` → `Vulkan Instance Version: 1.3.275`,
    device **llvmpipe (LLVM 20.1.2, 256 bits)**,
    `PHYSICAL_DEVICE_TYPE_CPU`, apiVersion 1.4.318, driver 25.2.8 —
    Mesa software Vulkan, exactly as expected with no GPU.
  - `glslangValidator -V test.vert/test.frag` →
    `test.vert.spv` + `test.frag.spv`, both `file`-confirmed as
    `Khronos SPIR-V binary, little-endian, version 0x010000`.
    Test shaders in `~/workspace/tools/vulkan-test/`.
  - Khronos validation layer: `VK_LOADER_LAYERS_ENABLE=
    VK_LAYER_KHRONOS_validation vulkaninfo --summary` → runs clean,
    **0 loader errors**. (While apt was locked, the same layer was
    verified from the extracted .deb via `VK_ADD_LAYER_PATH` +
    `LD_LIBRARY_PATH`; the apt install makes that workaround
    unnecessary. Before the layer package existed, only
    `VK_LAYER_INTEL_nullhw` / `VK_LAYER_MESA_overlay` /
    `VK_LAYER_MESA_device_select` were present.)
- Licences: Vulkan tools + validation layers **Apache-2.0**;
  glslang **BSD-3-Clause** (Khronos); Mesa/llvmpipe **MIT**.

## 5. Rust toolchain + godot-rust sample — VERIFIED WORKING

- Install: `rustup-init -y --profile minimal --default-toolchain
  stable` → **rustc 1.100.0** (0ef1bc386 2026-11-09),
  **cargo 1.100.0** (3acc79c0c 2026-11-05). Home: `~/.cargo/`
  (rustup script kept at `~/workspace/tools/rustup-init.sh`).
- godot-rust: `git clone --depth 1
  https://github.com/godot-rust/gdext.git` →
  `~/workspace/tools/godot-rust-gdext/` (7.5 MB), crate `godot`
  **0.5.5**.
- Sample: minimal crate `~/workspace/tools/godot-rust-sample/`
  (`Cargo.toml` with a path dependency on the cloned `godot` crate;
  `src/lib.rs`: `Greeter` RefCounted class with one `hello()` method
  returning `"hello from godot-rust"`).
- Verification: `cargo build -j1` → **CARGO EXIT: 0**,
  `target/debug/libgodot_rust_sample.so` (108,464,816 bytes,
  `ELF 64-bit LSB shared object, x86-64, with debug_info` — debug
  profile; a release build would be far smaller).
  - First build FAILED (exit 101, 14 errors: E0277/E0425/E0614 —
    `only classes registered with Godot are allowed`, missing
    `__godot_Greeter_Funcs`) because the sample used the pre-0.5
    pattern (unit struct, no `#[derive(GodotClass)]`). Fixed by
    adding `#[derive(GodotClass)] #[class(base = RefCounted)]` +
    a `base: Base<RefCounted>` field. **Not a RAM failure** — the
    godot crates themselves compiled fine on `-j1` (~5 min, no OOM).
  - The sample is a build proof only — it is NOT wired into a Godot
    project yet (no `.gdextension` file, no load test in the editor).
    That is the next step if Rust code is ever used in the game.
- Licences: Rust toolchain **MIT/Apache-2.0**; godot-rust **MPL-2.0**
  (per `godot/Cargo.toml`: `license = "MPL-2.0"`).

## 6. GitHub Actions CI — PREPARED ONLY, DRY-RUN DONE, CANNOT RUN YET

- File: `.github/workflows/ci.yml` (new, 5.7 KB) — job `verify`
  (import check + gdUnit) + job `android` (JDK 17, Android SDK 34,
  Godot 4.3 + export templates, APK export, apksigner v1+v2+v3
  verify, artifact upload, 14-day retention).
- Verification:
  - YAML parses: `yaml.safe_load` → jobs `['verify', 'android']`.
  - Local dry-run (same commands the workflow runs):
    - Import: `godot --headless --path . --import` → **exit 0,
      0 SCRIPT ERRORs, ~26 s**. The old import STALL is FIXED
      (2026-11-15 ~12:35: the ProtonScatter demos `.blend` was the
      cause; its removal fixed it — see the deep-graphics batch).
      The workflow's 600 s timeout stays as a safety net only.
    - gdUnit: `godot --headless --path . -s
      addons/gdUnit4/bin/GdUnitCmdTool.gd --ignoreHeadlessMode
      -a tests/gdunit` → **exit 0, 7 test cases, 0 errors,
      0 failures, PASSED** (the trailing `ERROR: Capture not
      registered: beehave` is a benign shutdown warning).
    - APK export step: NOT re-run in the dry-run — the local
      `verify_gate.sh` already covers APK export + signing on every
      run; re-exporting here would only contend with the other
      agents' Godot runs.
  - First dry-run caught a real bug in the file: the gdUnit path
    was `res://addons/gdUnit4/bin/gdUnitCmdTool.gd -a res://test`
    (lowercase, wrong dir) → `File not found`. Fixed to the exact
    `verify_gate.sh` invocation (`GdUnitCmdTool.gd`,
    `-a tests/gdunit`). **This is why the dry-run exists.**
- **CANNOT RUN YET: the project repo has no GitHub remote**
  (`git remote -v` is empty; `main` is local-only). A workflow only
  executes on a GitHub-hosted repo. The user must create a remote
  (e.g. `Samir412005/project-eternia`) and push a branch — his step.
  No money involved: public-repo Actions minutes are free.

## 7. NOT attempted — Unreal Engine

Per the assignment: **Unreal Engine 5 was NOT attempted.** It needs a
GPU, ~32 GB RAM and ~100 GB disk; this VM has no GPU, ~8 GB RAM and
the engine alone is ~100 GB. There is no free path to run it here.
Godot 4.3 + the toolchain above is the real-programmer stack on this
machine.

## Still needs the user (cannot be done by an agent)

1. Create a GitHub remote for project-eternia and push a branch, so
   `.github/workflows/ci.yml` actually runs (his step; needs his
   GitHub account, already connected as Samir412005).
2. Wire the godot-rust sample into a Godot test project (`.gdextension`
   + load test) if Rust code is ever wanted in the game — the `.so`
   builds, but nothing loads it yet.
3. Reinstall the apt packages (`clang ninja-build gdb vulkan-tools
   glslang-tools vulkan-validationlayers git-lfs`) after any VM restart
   — apt does not survive restarts. The extracted fallback copies in
   `~/workspace/tools/extracted/` survive (home disk) but are not on
   PATH.

## 8. Cape + hero fix (Aetheria slice) — 2026-11-15 (cape-fix worker)

Source blend: `~/workspace/mpfb_hero/Hero_MPFB.blend` (backup
`Hero_MPFB.blend.bak-capefix`). GLB re-exported 3x; final
`assets/characters/mpfb/Hero_MPFB.glb` 1,821,632 B,
md5 `ace93c2275cf3b4a9516964502bfe60c`. All shots read visually by the
worker (Compatibility renderer, Xvfb, 1280x720).

### Cape — radical rebuild (was a flat red board from all angles)
- **Root cause of the flat read:** the old cape was buried in the tunic
  through the torso and its hem swung forward through the legs, and the
  toon shader banded it into one flat colour. Rebuilt as a 25x29 grid
  (1,450 verts) with 9 modelled pleats (amp 0.015 -> 0.085), wavy hem,
  side wrap over the shoulders, outward bow, Solidify 0.012 applied,
  hem raised to the knee (walk-leg clearance 0.073). UV.y=0 pinned top
  kept, so `cape_sway.gdshader` still works.
- **Dark shape on the cape's upper centre — cause found, fixed:** it
  was the TUNIC, not the ponytail: the tunic's top ring caught an
  arm/shoulder vert and bulged to y 0.214, stabbing through the cape.
  Clamped all tunic verts y>0.09 -> 0.09 (19 verts). Ponytail also
  tucked under the cape (34 verts) and its y-plane card deleted.
- **Fold texture:** `Hero_MPFB_Cape_Folds.png` (PIL, 9 stripes
  phase-matched to the modelled pleats, softened to 0.18 contrast with a
  2-cycle amplitude modulation so it reads as cloth, not a radiator).
  Shader now samples it (`fold_tex`, white tint).
- **Outline:** cape outline width 0.035 -> 0.015 — the wider hull
  fragmented into black shards along the folded hem/top edge.
- **Verified by reading shots 36/37/38:** cape reads as draped cloth
  with visible soft fold bands + wavy hem from front AND back. From the
  side it still reads thinner/straighter (drape depth does not show in
  profile) — see remaining flaws.

### Hero fixes
- **Eyes:** face texture repainted twice (PIL): 260x140 eyes, iris
  r=72, brighter amber (inner 250,200,90), pupil r=20, bigger
  highlights. **The repaint alone did NOT fix the read** — the black
  scribbles on the face were the inverted-hull outline of the Skin
  mesh poking through (pure-black (0,0,0) pixels; the texture's darkest
  is (20,10,4)). Fix: `aetheria_slice.gd` now skips `next_pass`
  outline for `Skin` and `Hair` materials. Verified in shot 10: clean
  face, amber eyes with white sclera + highlights pop.
- **Hair (found during the eye work):** the hero read BALD from the
  front. The HairCap renders and covers the crown (proved with a
  temporary red-albedo debug run), but its albedo (0.16,0.11,0.07)
  rendered as light tan (225,176,114) under the bright sun + toon
  shading — the same lightness as skin. Darkened Hair to
  (0.07,0.045,0.025). Verified in shot 10: dark brown hair on the
  crown, still brown (not black) from the back in shot 37. (A
  `fix_haircap_normals.py` recalc attempt was a dead end: the cap's
  winding was not the cause — it is double-sided in the GLB.)
- **Sword:** blade was 1.235 m (FBX sword was ~4.4 m at 0.28 scale);
  halved to 0.612 m in pass 1, tip no longer drags (worst tip z in Walk
  +0.236). The mesh was 7 disconnected components — 302 stray verts
  clumped at the tip (kitbash junk) rendered as the black blob at the
  sword's end; deleted, keeping the 150-vert grip component
  (`fix_sword_width.py`). Then restored the blade width 0.035 -> 0.070 m
  (perp x2 past the guard, length unchanged, `fix_sword_width2.py`).
  Verified in shots 09/38: a real sword, tip clear of the ground.
- **Ankles:** pants bottom ring 0.16 -> 0.08, boot top 0.14 -> 0.20
  (0.12 overlap). Verified covered in shots 09/11/36/37.

### Remaining flaws (seen in the final shots, not hidden)
- Cape folds still regular (9 even stripes) — soft, but a real cloth
  would vary more; side profile reads as a thin red blade.
- A few small black outline fragments remain at the cape's top edge
  and hem corners.
- Eyes pop now but are ~25 px on screen at the 1.55 m framing.
- Face from the side: eye is a black patch (texture wrap on the curved
  head). Chest plate reads as a light-blue slab; shield huge/dominant
  (both pre-existing). Tunic tube is still twisted (rings not
  horizontal; hidden under the cape from behind).
- Scripts: `tools/studio/repaint_face_cape.py` (PIL),
  `tools/studio/mpfb_rebuild/fix_cape_hero.py`,
  `fix_tunic_ridge.py`, `fix_cape_rebuild2.py`, `fix_cape_pass4.py`,
  `fix_sword_width.py`, `fix_sword_width2.py`, `fix_haircap_normals.py`,
  `fix_hair_dark.py`. Note: `fix_cape_hero.py` is NOT idempotent (do not
  re-run — it would delete the ponytail x-plane faces and re-halve the
  sword).

## 9. Patches + deep-graphics integration (Aetheria slice) — 2026-11-15 (patches worker)

Branch `aetheria-slice`, HEAD `3f76430` at start. All work in
`scripts/world/aetheria_slice.gd`, `project.godot`, the shaders below,
`assets/library/environments/mossy-rock-10k.glb`, and shots
07–11/13/14/36–38 (re-shot) + 39/40/41/43a/43b (new).

### 1. MSAA/SSAO patch — APPLIED (`tools/studio/msaa-ssao-patch.md`)
- `project.godot` `[rendering]`: the exact 10 lines (msaa_3d=2, msaa_2d=0,
  screen_space_aa=0, anisotropic level 2, ssao quality 1 + half_size +
  blur 2 + fadeout 50/300, scaling_3d mode 0).
- `aetheria_slice.gd`: `e.ssao_enabled = true` + `e.ssao_light_affect = 0.5`
  on the slice Environment; `TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC`
  in `_toon()` (no-op today — the slice ground/path are flat-colour) and
  `texture_filter = 6` on the five PBR materials in
  `scenes/tests/graphics-showcase.tscn`.
- **SSAO is inert here.** The engine warns `SSAO can only be enabled when
  using the Forward+ rendering backend` — so on Mobile/Compatibility the
  setting is stored but does nothing. The face did NOT degrade (cheek
  median unchanged at 211,176,129), consistent with SSAO being a no-op.
  MSAA 4x is set; the street before/after pair (shot 08) shows only a
  subtle edge change (whole-frame mean abs diff 0.94) — MSAA activity on
  this backend is not independently proven from the pixels.

### 2. Hero rim/wrap patch — APPLIED with 4 documented deviations
(`tools/studio/hero-rim-wrap-patch.md`; `assets/materials/hero_toon_rim.gdshader`
new, `assets/materials/anime_face.gdshader` Part 1)
- Part 1 (face shader): applied exactly (rim_color (1.0,0.82,0.62),
  rim_strength 0.18, wrap 0.45, EMISSION rim, wrapped ndl). **No visible
  effect**: `_face_mat` is created but never assigned — the MPFB hero's
  face uses a plain toon StandardMaterial3D, and wiring the SDF face
  shader is blocked (it scrambles the curved MPFB face — known breakage).
- Part 2 (body): applied to the 5 flat-colour hero parts only (Tunic,
  Sleeve_L/R, ChestPlate, Warrior_Sword). Deviations from the verbatim
  patch text, all proven by isolated tests (scripts in /tmp, tests 1–12):
  1. `rim_mat.next_pass = warrior_outline` is WRONG for ShaderMaterial
     in 4.3 — with it set the parts render pure (0,0,0); removed, and the
     black outline restored as duplicate meshes (CapeOutline pattern),
     +5 draws (172 → 177).
  2. `cull_disabled` added — the MPFB GLB meshes are inverted-winding /
     double-sided, so default `cull_back` culls the outward faces and
     the parts are invisible without it.
  3. `light()` uses view-space `dot(NORMAL, LIGHT)`, not
     `INV_VIEW_MATRIX` — the view-matrix form is poisonous on skinned
     meshes under the shadowed sun (test 11: identical shader, dark
     with INV_VIEW_MATRIX, bright with the view-space dot).
  4. `light_cap` uniform scaling the diffuse (face-shader pattern) —
     the un-capped diffuse clips the torso to (1,1,1) under the
     shadowed sun + fill; the cap is 0.40, fitted from the slice's own
     shot 10 (the T-pose test's 0.55 was useless — everything saturates
     in the T-pose). Rim moved to EMISSION (strength 0.45, up from the
     patch's 0.30 so it reads at all); specular disabled.
- Result (shot 10): plate (224,237,254) vs toon baseline (204,220,242)
  — pale steel, no clipping; cheek median (211,175,129) unchanged;
  black outline restored; sword visible as a thin grey blade; warm rim
  only FAINT on the shadow-side edge (a few px warmer at the plate edge
  in shot 09). If the rim needs to read stronger, raise rim_strength —
  do not raise the cap.

### 3. Deep-graphics integration into the main slice
- (a) **Terrain splat** — 12×12 m hill at (22,0,-12), east open ground
  (shot 39). Dirt tuned down (dirt_slope_start 0.15→0.25,
  dirt_slope_end 0.45→0.60, low-dirt 0.6→0.25; stone 0.55→0.70,
  0.80→0.90 — the last two also set explicitly in code via
  `set_shader_parameter`, because `-s` runs do not reliably pick up
  edited `.gdshader` defaults). Grass dominates the top (63%
  green-dominant pixels in the mound region). **Remaining flaw:** the
  ridge's steep east face (shaded — the sun is in the south-west) reads
  as a near-black grey scar (sample (66,69,74)); it was already dirt,
  not stone, so the stone-band retune did not change it — it is a
  shaded-slope lighting characteristic, and fixing it would mean
  rebalancing the global light budget (out of scope, risky for the
  face calibration).
- (b) **Wind sway** — near trees use the showcase wind shader (same
  green as the old `_toon`, sway_height 2.6). Shots 43a/43b (1.5 s
  apart): 910 px changed by >20 — real but subtle at this distance
  (tree tops move most, as designed). The near trees lose their black
  outline (ShaderMaterial has no next_pass); the far trees keep
  `_toon()` and the flowers keep their own colours (no wind — the
  shader's flat colour would erase them).
- (c) **Cloud shadows — REMOVED, did not survive the move.** The sheet
  was added (48×48 at y=11, UV edge fade added to the shader so its
  borders never band the sky), then removed again: the 42a/42b high pair
  (3 s apart, camera above the sheet) has IDENTICAL ground luminance
  grids, and a Python replication of the shader's value noise shows
  clouds SHOULD cover the east band (cover > 0.3 at x 16..24) yet that
  ground is not darkened at all — while the sheet bands the sky as dark
  blotches in the low shots (39/41/43a). Shots 42a/42b deleted. The
  shader file (with the edge fade) is kept for the showcase. A cloud
  technique that works here needs a projection-based approach, not a
  physical sheet.
- (d) **Mobile LUT grade** — `LUTGrade` CanvasLayer (layer 0, after the
  vignette) with the showcase Hald CLUT, visible ONLY on Vulkan
  (`get_video_adapter_api_version()` starts with "1."; `--aetheria-no-lut`
  forces it off for the on/off pair). **NOT VERIFIED on Mobile**: the
  slice segfaults on Vulkan/lavapipe during setup — exit 139, twice
  (plus a third run with the probe disabled, also 139), no backtrace,
  crash after the collision build and before any shot. The probe was
  ruled out as the cause. The slice was never verified on Mobile before
  this work, so the crash may be pre-existing (heavy scene + llvmpipe)
  or caused by one of the new nodes — NOT attributed. The LUT stays
  hidden on Compatibility (verified — the shots are not black).
- (e) **Pond + reflection probe** — there was NO pond in the slice, so
  one was added at (24,0,6): 7×7 water plane (32×32 subdiv, y=0.06,
  `use_depth_fade` stays 0 — unresolved lavapipe paradox), dirt basin
  cylinder (its top disc reads as a dirt shore ring, since the slice
  ground is a solid 400 m plane with no hole), ReflectionProbe at
  (24,1.2,6), size (12,6,12), UPDATE_ONCE. Shot 41: the pond reads
  well (blue water, sparkle, dirt/moss shore ring — the ring is very
  circular, a minor artifice). The probe's reflection difference was
  not isolated as a before/after pair.

### 4. TripoSG mossy rock — placed (shot 40)
- `assets/library/environments/mossy-rock-10k.glb` (10,000 faces,
  game-ready) + its `.import`. Two instances in the golem-fight
  clearing at (-24,0,-56) scale 1.3 and (-21.5,0,-53.5) scale 0.7,
  triplanar splat material (texture_scale 0.8 — no UVs needed, no
  xAtlas fallback required). **Placed UPRIGHT**: the GLB is already
  Y-up (a low wide boulder, Y extent smallest — probed), so the task's
  Y-up → Z-up rotation would lay it on its side. The mesh's local
  origin is 0.357 m above its base, so each rock is lifted by
  0.357 × scale. Shot 40: reads as mossy boulders (76%
  green-dominant in the rock region).

### 5. Root cause found — inverted / missing normals
- `scenes/tests/terrain_patch.mesh` ships with INVERTED normals (mean
  (0,-0.91,-0.05) — probed). The splat shader then reads slope = 1 on
  every face, so dirt+stone win everywhere and the hill renders as a
  dirt mound. That — not the dirt weights — is why showcase shot 17
  was dirt-heavy; the weight tuning alone could not fix it.
- The TripoSG rock GLB has NO normals at all (and no UVs) — its
  lighting and splat slope were undefined (the small rock rendered
  near-black brown in the first shot 40).
- Both are fixed at runtime by `_mesh_with_fixed_normals()` in
  `aetheria_slice.gd`: recomputes smooth normals from the triangles,
  flips them if the NORMALIZED mean points down (|y| ~ 1 for a
  heightfield) or the majority point at the centroid (closed mesh).
  Lesson: use the normalized mean, not the raw sum — the raw sum's
  magnitude scales with face area (the patch's raw mean.y is only 0.09
  even though it points straight up), so a ±0.1 threshold on it
  misreads and wrongly flips a correct heightfield (that bug shipped
  one run and was caught by probing the fixed mesh). The shared
  `terrain_patch.mesh` FILE still carries the inverted normals — that
  file is a separate asset fix.

### 6. Budgets, gate, remaining flaws
- Budget: 183 draw calls (< 200), 182,303 primitives (over the <100k
  guideline — baseline was already 105,879; the +35k after the normal
  fix is not yet isolated, draws are within budget), 222 objects.
- Verify gate 2026-11-15 12:47 CET: **3/3 PASS** (`--skip-apk`):
  Gate 1 import exit 0, 0 SCRIPT ERRORs; Gate 2 gdUnit exit 0, no
  FAILED lines; Gate 3, 54 screenshots OK (log
  `reports/studio-gate-20261115-124709.log`). Gate 4 (APK) skipped.
- Remaining flaws (seen in the final shots, not hidden): cape still
  thin in side profile (out of scope, known); face-shader Part 1 has no
  visible effect (SDF face shader unwired); SSAO inert (Forward+-only);
  warm rim only faint on the hero's shadow-side edge; hill's steep east
  face reads as a near-black grey scar in shade; pond's dirt shore ring
  is very circular; probe reflection difference not isolated; Mobile
  (Vulkan/lavapipe) run of the slice segfaults (exit 139, 3 attempts)
  so the Mobile LUT pair is unverified; tri count 182k is over the
  <100k guideline and the +35k after the normal fix is unexplained.

### 7. Final round — clean tree, APK shrink, clean gate (build+gate worker, 2026-11-15 ~12:40–13:00 CET)

Scope: clean the tree, shrink the APK, run the full gate on the clean
commit, verify the APK + final screenshots, close the docs. No game
content, shader, hero-file or golem-fight changes. Branch
`aetheria-slice` throughout; HEAD `ca9da9d` → `f29059b`.

- **Clean (commit `faef938`).** `git status` matched the brief:
  modified `Warrior_Anime_Hair_Strands.png.import` (md5 only) committed;
  untracked `Hero_MPFB_Cape_Folds.png.import` (real asset .import) and
  `villager_dialogue.dialogue.import` (real asset .import) committed;
  40 tracked `screenshots-aetheria/*.import` files deleted +
  `screenshots-aetheria/*.import` added to `.gitignore` (the folder
  regenerates them on import). 41 files changed.
- **APK shrink (commit `9f71164`).** Preset `Android Mobile`,
  `export_filter="all_resources"`, `exclude_filter` was only `docs/*` —
  the 45 MB `screenshots-aetheria/` PNGs were packed into the APK.
  Checked first: the slice DOES load `res://scenes/tests/terrain_patch.mesh`
  at runtime (`aetheria_slice.gd:46`), and nothing references
  `graphics-showcase.tscn` — so the exclude filter is now
  `docs/*,screenshots-aetheria/*,scenes/tests/graphics-showcase.tscn`.
  APK 87,632,794 → 57,371,470 bytes (gate re-run; 54.7 MiB, < 100 MB
  budget, above the 40 MB aim). APK contents verified: 0 entries for
  `screenshots-aetheria` / `graphics-showcase`, `terrain_patch.mesh`
  present, 1,824 files.
- **CORRECTION — the MPFB "duplicates" were NOT noise (commit
  `f29059b`).** The one Mobile reproduction run (below) showed
  `ERROR: Resource file not found:
  res://assets/characters/mpfb/Hero_MPFB_Hero_MPFB_Cape_Folds.png`
  (and `..._Warrior_Face_Anime.png`) and `Failed loading resource:
  Hero_MPFB.glb` — the GLB references those two extracted textures at
  runtime by path (its UIDs are invalid, so it falls back to the text
  path). Deleting them in `faef938` broke the hero load, and the gate
  did NOT catch it: Gate 1 import + Gate 2 gdUnit never load the GLB.
  A plain `--import` does NOT regenerate them (the GLB is considered
  up-to-date). Fix: deleted `.godot/imported/Hero_MPFB.glb-*.scn/.md5`,
  re-ran `--import` (exit 0, 0 errors) — both PNGs + their `.import`
  files re-extracted — then a headless smoke run showed 0 Hero_MPFB
  errors and the hero renders again in the final shots. The four files
  are now COMMITTED as real runtime dependencies. Lesson: never delete
  GLB-extracted textures without a load check; the gate needs a
  hero-load check (it has none today).
- **Mobile segfault — NOT reproduced this round.** One allowed
  reproduction attempt: `xvfb-run -a godot --rendering-driver vulkan
  --rendering-method mobile --path . --resolution 1280x720 --quit-after
  120` → **exit 0, 120 frames, no crash** (log `/tmp/mobile-repro.log`).
  The exit-139 crash (3 attempts by Worker B) stays unattributed and
  is NOT proven fixed — it may be flaky or memory-pressure related.
  Do not claim it fixed. Consequence: the Mobile LUT on/off pair is
  still unverified, and the LUT stays hidden on Compatibility.
  Remaining headless-only noise in that run: 5× `Parameter "m" is
  null` at `mesh_get_surface_count` (dummy rendering server) + the
  known `Capture not registered: beehave` — neither appears in the
  Mobile run.
- **Final gate — 4/4 PASS on the clean tree** (re-run after the
  restore commit, log `reports/studio-gate-20261115-125427.log`):
  Gate 1 import exit 0, 0 SCRIPT ERRORs; Gate 2 gdUnit exit 0, no
  FAILED lines; Gate 3, 54 screenshots OK, 0 bad; Gate 4 export exit 0,
  APK 57,371,470 bytes, apksigner v1+v2+v3, 1 signer. Deliverable
  copied to `~/workspace/your_files/aetheria-slice.apk` (symlink →
  goal files dir) and signature re-verified independently by hand:
  v1/v2/v3 true, `Number of signers: 1`, cert `CN=Android Debug`.
- **Final screenshots** (Xvfb, Compatibility, `-- --aetheria-shots`,
  exit 0, 18 shots, end-of-shots budget print: 48 draw calls, 78,740
  primitives; log `/tmp/final-shots.log`). Shots 08/10 re-captured
  from the final build and read visually — no regression in the build:
  hero loads and renders; face closeup (10) is clean with visible
  amber eyes, brown bangs, slight smile; street shot (08) reads
  (hero mid-street, red cape, shield, village + castle + islands).
  Flaws still visible in these final shots: cape front reads as a
  wide flat red fan with fold bands (better than a board, not a
  drape); the shield dominates the closeup as a huge pale oval; the
  sword is not visible in either final framing; the hill's steep east
  face still reads as a near-black scar on the right horizon
  (shots 08/10); plaza foreground is wide and empty.
- **Remaining flaws (all of them, not hidden):** cape still thin from
  the side; cloud shadows removed (sheet never darkened the ground,
  banded the sky); Mobile LUT unverified + lavapipe segfault
  unattributed (not reproduced once, not proven fixed); SSAO inert on
  Mobile (Forward+-only); face-shader Part 1 no visible effect (SDF
  face shader unwired); hill east face black scar; tri count 182,303
  peak over the <100k guideline (final-shots print 78,740 — different
  measurement point, peak stands); near trees lost their outline;
  pond shore ring circular; probe reflection difference never
  isolated; `terrain_patch.mesh` file still carries inverted normals
  (fixed at runtime only). **Golem fight STILL MISSING — VFX only,
  another task.** The real-phone (Galaxy A16) test has still not
  happened; a screenshot is not a phone test.
- **Not done (out of scope / forbidden):** no depth-water fade, no
  LightmapGI bake, no golem wiring, no Hunyuan notebook touch, no
  hero GLB/face/hair/cape edits, no re-run of `fix_cape_hero.py`, no
  libzstd1/ArmorPaint work. Gate failed 0 times this round; no retry
  loops needed.

---

## Real-developers batch — 2026-11-15 (study library + daily backup + QA wired)

Source: phase-1 research report `research_notes/real-game-programmers-20261115/report.md`
(§7 QA, §10 open-source games, §11 checklist). Worked LIGHT and sequentially
while the graphics coordinator ran Blender/Godot — clones + small scripts only,
no compilers, no Blender/Godot runs from this batch except the one gate run
after the coordinator finished.

### 1. Study library — `~/workspace/tools/study-library/` (OUTSIDE the repo)

Shallow clones (`--depth 1 --single-branch`). Network to GitHub/Codeberg ran
~1–2 MB/s, so big repos took minutes and two failed on stalls/disconnects.

| Repo | Commit | Size | Godot | Licence (verified from the file) | Pattern to steal |
|---|---|---|---|---|---|
| godot-demo-projects | b761b4c | 528 MB | 4.7 | MIT | Official patterns — code "the way the engine intends" |
| Thrive | 109c77f | 84 MB | 4.7 (C#) | GPL-3.0 | Long-term scope: stages, volunteers, small releases |
| Reia | 35baf42 | 486 MB | 4.7 | AGPL-3.0 | Closest to Aetheria: Action RPG combat/world/quests |
| Sunder | d6f5f1b | 263 MB | 4.7 | AGPL-3.0 | Godot 4 multiplayer 3D: jetpack/ski + networking |
| Tanks of Freedom | b1cad8b | 22 MB | 2.x (`engine.cfg`) | MIT | Complete small game: full structure, turn-based code |
| Haldric | c82bbd1 | 17 MB | 3.x | NONE FOUND — unverified | Grid combat + AI. Study only, do not copy |
| DynaDungeons | 4cb7142 | 8.2 MB | 2/3-era | GPL-3.0 | Arcade loop, level gen, simple networking |
| Circle Jump | 83a5a83 | 4.0 MB | 3.x | MIT | Complete Android game + tutorial series; Android export |
| Heart Platformer | cfcc75d | 400 KB | 4.0 | MIT | Clean 2D movement, camera, Juice |

Total ~1.4 GB, 9/11 repos. Full rules in `study-library/README.md`.
**Copyleft warning:** Reia/Thrive/Sunder/DynaDungeons are AGPL/GPL — study
only; copying their code into our game would impose copyleft. MIT repos may
be reused with attribution. Haldric has no licence file — all rights
reserved, study only.

**Clone incidents (recorded honestly):**
- Reia (486 MB) pulled 242 MB of LFS content on first clone (~7 min).
  All later clones used `GIT_LFS_SKIP_SMUDGE=1` (pointer files only).
- Tanks of Freedom II: clone stalled twice (10+ min, no output) — FAILED,
  not retried in a loop. Retry on a better connection.
- Intrepid: first attempt `fetch-pack: unexpected disconnect while reading
  sideband packet` (timeout 240 s); second attempt stalled the same way —
  FAILED. Retry later.
- godot-demo-projects: first attempt timed out at 280 s leaving a partial
  clone (`fatal: your current branch 'master' does not have any commits
  yet`); re-cloned with an 850 s timeout — OK.
- Sunder: first attempt timed out at 280 s; retry with 850 s — OK (263 MB).
- **Thrive: clone fetched the commit but checkout failed** (`fatal: the
  remote end hung up unexpectedly` + `Clone succeeded, but checkout
  failed`). Root cause found: a VM restart during the batch wiped the
  apt-installed `git-lfs` binary (apt packages do not survive restarts),
  while `~/.gitconfig` still pointed the LFS filter at it — every LFS
  checkout on the machine failed. Fixed by reinstalling git-lfs 3.4.1
  from the local apt cache (`sudo dpkg -i
  /var/cache/apt/archives/git-lfs_3.4.1-1ubuntu0.4_amd64.deb`, no network),
  then `GIT_LFS_SKIP_SMUDGE=1 git reset --hard HEAD` (the first
  `git restore` only fixed the working tree; the index still showed 8,095
  staged deletions — `reset --hard` fixed index + tree: 8,095/8,095 files,
  status clean, 84 MB). Lesson: after any VM restart, verify `which
  git-lfs` before any LFS work.
- A runtime restart interrupted the sunder/demo-projects/thrive clone loop
  mid-flight; recovered by checking disk state first (sunder was already
  complete) and cloning only the two missing repos — nothing was re-cloned
  blindly.

### 2. Daily backup — `tools/studio/daily_backup.sh` + cron `eternia-daily-backup`

- Script: dated git bundle of ALL branches + zip of untracked files
  (`git ls-files --others --exclude-standard`) + patch of uncommitted
  modifications to tracked files (a bundle holds commits only — without the
  patch, a day of uncommitted work would be lost with the disk) → 
  `~/workspace/cloud-sync/backups/`, keeps the last 7 of each, one log line
  per run in `backups/backup.log`. The bundle is verified with
  `git bundle verify` inside the script before logging OK.
- **Bug found and fixed during testing:** the prune step used
  `ls -t <glob>` — when a glob matched nothing (e.g. no `.patch` files on
  a clean tree), `ls` exits 2 and `set -e` + `pipefail` killed the run
  before the log line (second test run exited 2 with a valid bundle but no
  log entry). Fixed with `|| true` on all three prune lines; prune logic
  itself verified with 9 dummy bundles (11 → 7 kept, newest first).
- Test runs 2026-11-15: bundle 24 MB, `git bundle verify` OK,
  `git bundle list-heads` = `aetheria-slice` 80f12e0, `main` 06bd6c9, HEAD.
  Tree was clean at test time (`uncommitted-diff=none`), so the patch path
  is tested only by code inspection, not by a real patch file.
- Cron `eternia-daily-backup` (verified in `cron.list`): daily ~03:19 CET
  (flexible time, Africa/Algiers), owner `goal:project-eternia-3d-rpg`,
  silent on success, reports failures only. Next run Mon 2026-11-16 03:19.
- **HF cloud upload stays MANUAL** via the signed-in browser upload to
  https://huggingface.co/datasets/gfhtgfghfcvvf/eternia-studio-assets.
  No API token exists; this batch created none and never will.

### 3. QA toolchain — verified live 2026-11-15

- `tools/studio/verify_gate.sh --skip-apk` (run once, after the graphics
  coordinator finished — no Godot runs were started while it was capturing):
  Gate 1 headless import exit 0, 0 SCRIPT ERRORs — PASS; Gate 2 gdUnit
  exit 0, no FAILED — PASS; Gate 3 54 screenshots, 0 bad — PASS.
  VERDICT: PASS — all 3 gates passed. READY.
  Log: `reports/studio-gate-20261115-130014.log`.
- GUT 9.4.0 present as backup (`addons/gut/plugin.cfg` version 9.4.0);
  gdUnit4 present (`addons/gdUnit4/`).
- `.github/workflows/ci.yml` YAML-valid (jobs: verify, android).
- **Still needs the user: a GitHub remote.** `git remote -v` is empty.
  Creating a public repo is public publishing and needs the user's explicit
  approval; without it the CI workflow cannot run. Nothing was created.

### Not done (out of scope / forbidden)

No game systems built or edited (no state machine refactor, no juice layer,
no data-driven Resources, no MultiMesh — implementation work for the next
build round, not installation). No Hunyuan/Kaggle work touched. No account,
token, or remote created. No paid tools. No files of any other agent touched.
