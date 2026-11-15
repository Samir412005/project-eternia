# STUDIO.md — PROJECT ETERNIA: the studio pipeline

**One path, no shortcuts.** Every piece of game content travels the same five
stages, in order, with a pass/fail rule at each stage. A stage's output is the
next stage's input. **Nothing is "ready" until the verification gate passes.**

```
Blender (model / rig / animate)
   → Krita (paint textures)
      → Godot (assemble: Toon + outline + SDF face shader)
         → Android APK (export + sign)
            → Verify (real screenshot + real phone test)
```

Engine: **Godot 4.3 ONLY, Mobile renderer.** No in-place upgrade (see AGENTS.md).
Target: **Samsung Galaxy A16** (Helio G99 + Mali-G57 MC2, 4 GB RAM class,
1080×2340). Budget: free / open-source only, no paid tools, no Docker, no GPU.

## Stage 1 — Blender: model / rig / animate

| Item | Value |
|---|---|
| Tool | **Blender 4.5.9 LTS** (the adopted one) — `~/workspace/tools/blender-4.5/` — `--background --version` verified. Blender 5.2.4 exists at `~/workspace/tools/blender-5.2/` as a spare only. |
| What it does | Character bases (MPFB 2.0.18 / CharMorph), face re-style, hair cards, baked cloth cape, armour, props, retopology, rigging (Rigify), animation cleanup, GLB/FBX export. |
| Inputs | Library packs (`assets/library/`), reference images, Mixamo/UAL/vid2anim clips. |
| Outputs | `*.glb` / `*.fbx` into `assets/library/characters/` or `assets/library/environments/`. **`.blend` sources live OUTSIDE the project tree** (`~/workspace/blender-sources/project-eternia/<asset>/`) — **proven 2026-11-15: any `.blend` in the tree makes `godot --import` hang forever** (0 CPU, killed at 90/180/240/300 s; no-`.blend` control finished in ~12 s; import exit 0 in ~24 s after the last `.blend` moved out). Never commit a `.blend` inside the project. |
| Pass rule | Export opens in Godot headless with 0 script errors; hero ≤ 15k tris; one building ≤ 5k tris; textures ≤ 1024 px (2048 hero only). |
| Licence rule | Base meshes: MPFB base mesh + standard assets are CC0 per the MakeHuman Community (characters you export are yours, including commercially). CharMorph code is GPL-3.0, but its installed library is NOT CC0: mb_male / mb_female are AGPL-3.0 (MB-Lab-derived), Antonia is a custom licence that requires the author's permission to redistribute derivatives, reom has no licence file (UNVERIFIED — do not ship). The CC0 Vitruvian character is NOT in the installed library — fetch it via the addon's in-Blender character downloader. **Hero rule: only an MPFB base or a verified-CC0 character may become the hero mesh.** Quaternius Nov 2020 + Ultimate packs (CC0 1.0 per shipped License.txt). **Human Generator assets are PAID — never use. MB-Lab is dead — use CharMorph. VRoid-derived content is FORBIDDEN without reading the live VRoid terms. MMD game models: technique only, never the models.** |

## Stage 1a — Character base (CharMorph / MPFB) — installed 2026-11-15

A real rigged human base replaces procedural primitives. Both tools are
installed in Blender 4.5.9 and verified headless (see
`tools/studio/STUDIO_INSTALL_LOG.md` for the full log).

| Item | CharMorph | MPFB |
|---|---|---|
| Version | **0.4.0** (Blender 4.4+), code **GPL-3.0** (verified from the shipped `license.txt` — the research report's "AGPL-3.0 code" claim was wrong) | **2.0.18** (2026-10-10), code **GPL-3.0-or-later** (verified from the shipped `blender_manifest.toml`) |
| Installed at | `~/.config/blender/4.5/scripts/addons/CharMorph/` (legacy addon) | `~/.config/blender/4.5/extensions/user_default/mpfb/` (extension; module name `bl_ext.user_default.mpfb` — plain `mpfb` does NOT enable) |
| Library | `.../CharMorph/data/` — 4 characters from CharMorph-db (420 MB): `mb_male`, `mb_female`, `antonia`, `reom` | Base mesh built in (no asset pack needed for the body). System assets pack (skins/eyes/teeth/clothes, CC0, 286 MB) extracted at `~/workspace/tools/mpfb-system-assets/` (85 `.mhmat` skins) — register it in Blender via MPFB → System and resources → Load pack from zip file |
| Verified headless | Enable OK; library loads (4 characters); `charmorph.import_char()` on `mb_male` → mesh, 17,996 verts, FINISHED | Enable OK (persisted via `save_userpref`); `mpfb.create_human()` → `Human` mesh, 19,158 verts, FINISHED; `mpfb.add_standard_rig()` → `Human.rig` armature, FINISHED |
| Licence of the library | mb_male / mb_female: **AGPL-3.0**. Antonia: custom licence — redistribution of derivatives needs the author's permission. reom: **no licence file — UNVERIFIED, do not ship**. The CC0 Vitruvian character is NOT in this library (db snapshot is from 2023-12-11) — get it via the addon's in-Blender downloader | Base mesh + standard assets: **CC0** per MakeHuman Community. Asset packs mix CC0/CC-BY — check per asset |
| Use for the hero | Only after re-styling in Blender (remodel face, hair cards, baked cape, armour, painted face) — and only from a CC0-licensed base (MPFB base, or Vitruvian once fetched). **Never ship an AGPL-derived hero mesh in a commercial release** — AGPL is copyleft on the asset | Same re-style pipeline; MPFB base is the CC0-safe starting point. Rigify / Mixamo rigs built in |

## Stage 1b — Custom animation (vid2anim) — installed 2026-11-15

| Item | Value |
|---|---|
| Tool | **vid2anim 0.1.1** (MIT, verified from the repo LICENSE) — `~/workspace/tools/venv-vid2anim/` (Python 3.12 venv; MediaPipe 1.2.3, OpenCV 5.0.0.93). CLI: `~/workspace/tools/venv-vid2anim/bin/vid2anim`. |
| What it does | Phone video → 3D animation: MediaPipe Pose engine is 100% CPU (no GPU). Film a sword slash / idle / walk, get a Blender Action. Mixamo stays the backbone for walk/run/idle; vid2anim is for signature moves. |
| Verified | `vid2anim doctor`: CPU-only, FFmpeg OK, MediaPipe OK. Sample run: 281-frame dance video + ybot.glb → `ybot_dance.glb` (2.64 MB, 63 animated tracks, 62 bones) in 25.9 s. Blender bridge (`vid2anim_blender.py` 0.1.1, from the repo — NOT in the PyPI wheel) installed + enabled in Blender 4.5.9; `vid2anim serve --port 8080` answers `/api/health` with `{"status": "ok"}`. |
| Workflow | 1) `venv-vid2anim/bin/vid2anim serve --port 8080` (one terminal). 2) In Blender: View3D → Sidebar → vid2anim, pick armature + video, Animate. Or CLI: `vid2anim run --input <video> --model <glb> --engine mediapipe --output <glb>`. |
| Samples | `~/workspace/tools/vid2anim-samples/` — `dance_urban.mp4` (7.2 MB), `ybot.glb` (2.3 MB), `outputs/ybot_dance.glb` (verified output). |
| Honest ceiling | Single-camera mocap needs 30–60 min cleanup per clip in the Graph Editor (feet slide, hands jitter). Budget that time; do not expect clean production animation out of the box. |

## Stage 1c — AI props on free cloud GPU (Colab notebooks)

AI 3D **cannot run on this VM** (no GPU, ~150 MB free RAM) — it runs only on a
free cloud GPU, and only for **props, never the hero, never a face**.
Notebooks live at `tools/studio/colab/` (valid JSON, verified 2026-11-15).
Running a notebook needs the user's Google sign-in on Colab/Kaggle — that is
his step, not an agent step.

| Item | TripoSG | TRELLIS v1 | Hunyuan3D-2mini |
|---|---|---|---|
| Notebook | `tools/studio/colab/triposg-prop-generator.ipynb` (6 cells) | `tools/studio/colab/trellis-prop-generator.ipynb` (6 cells) | `tools/studio/colab/hunyuan3d-2mini-prop-generator.ipynb` (6 cells, written 2026-11-15, verified against the real repo clone — NOT run yet) |
| Licence | **MIT** code + MIT weights (VAST-AI-Research) — verified from the repo LICENSE | **MIT** code + weights (Microsoft) — verified from the repo LICENSE. **GLB export uses nvdiffrast (research/evaluation-only licence) — do not ship TRELLIS GLBs commercially without replacing the exporter** | **Tencent Hunyuan 3D 2.0 Community Licence** — verified from the shipped `LICENSE`: territory **excludes EU / UK / South Korea** (user in Algeria is inside it); repo headers also cite a **NON-COMMERCIAL** licence — **outputs are non-commercial / prototype only** |
| GPU | **8 GB VRAM — T4-safe.** Free Colab T4 (16 GB) runs it comfortably | **16 GB+ required** (README: verified on A100/A6000). A free Colab T4 sits exactly on the floor and **risks OOM** — prefer Kaggle P100 (16 GB). TRELLIS.2 needs 24 GB for PBR — out of scope | **6 GB shape, 16 GB shape+texture total** (official README). T4 (16 GB) is exactly on the limit — the notebook frees the shape pipeline before texture and always saves the shape-only GLB first |
| Input / output | Image-only (no text-to-3D). Geometry-only GLB (no texture, no UVs) — paint in Blender/Godot. Y-up → rotate to Z-up | Image-to-3D (text models are weaker — README recommends image first). Textured GLB, still needs Blender cleanup + decimation | **Text prompt → image → textured GLB.** Text goes through the repo's own HunyuanDiT (`Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled`); shape is the 0.6B 2mini DiT, texture is the Hunyuan3D-2 Paint pipeline. The only AI-3D route here that takes a text prompt |
| Verified call | `TripoSG.from_pretrained('VAST-AI/TripoSG')`, 50 steps, `mesh.export(..., postprocess=True)` — same calls as the live rock run in `workspace/cloud-sync/heavy-tools/triposg-prop-generator.ipynb` | `TrellisImageTo3DPipeline.from_pretrained('microsoft/TRELLIS-image-large')`, `pipeline.run(image, seed=1)`, `to_glb(..., simplify=0.95, texture_size=1024)` — from the official README minimal example | `HunyuanDiTPipeline('Tencent-Hunyuan/HunyuanDiT-v1.1-Diffusers-Distilled')` → `Hunyuan3DDiTFlowMatchingPipeline.from_pretrained('tencent/Hunyuan3D-2mini', subfolder='hunyuan3d-dit-v2-mini')` (30 steps, octree 256) → `Hunyuan3DPaintPipeline.from_pretrained('tencent/Hunyuan3D-2')` — all verified from `~/workspace/tools/hunyuan3d-2/` (shallow clone of the official repo) |
| Budget | ~5–10 props/week (10–20 min cloud + 30–60 min Blender cleanup each). Rocks, crates, furniture, weapons, golem base — never the hero | Same budget; textured output saves painting time but costs more GPU | Same budget; textured output saves painting time. One prop per run (mossy stone lantern for the golem clearing is the notebook's example) |

## Stage 1d — Mesh finishing: UV + remesh (xAtlas / Instant Meshes / MeshLab) — installed 2026-11-15

AI 3D outputs arrive unfinished: TripoSG meshes have **no UVs**, Hunyuan/TRELLIS
meshes are too dense for a phone. This stage finishes them before they reach Godot.

| Item | Value |
|---|---|
| Tool | **xAtlas** (MIT, pip `xatlas` 0.0.11) in `~/workspace/tools/venv-xatlas/` (with trimesh 5.2.1, numpy) — UV unwrapping. **Instant Meshes 2.5.0** (BSD, MattRM2 fork) in `~/workspace/tools/instant-meshes/` — remesh/retopology CLI + `pyinstantmeshes` 0.1.0 binding. **MeshLab 2025.07** (GPL-3.0) AppImage in `~/workspace/tools/meshlab/` + **PyMeshLab 2025.7.post1** in the same venv — decimation/cleaning, headless via PyMeshLab. |
| What it does | xAtlas: `xatlas.parametrize(vertices, faces)` → UVs (100% in [0,1] on the test mesh, 58.4% atlas utilization). Instant Meshes: pure-quad remesh (`-f <count>`, approximate — a `-f 500` request produced 2,084 quads; tune, don't trust the number). MeshLab: `meshing_decimation_quadric_edge_collapse` → exactly 500 faces from 1,280 on the test mesh. |
| Verified | xAtlas test `~/workspace/tools/xatlas-test.py` PASS; Instant Meshes CLI + Python tests PASS (`~/workspace/tools/instant-meshes-test.py`); PyMeshLab test `~/workspace/tools/meshlab-test.py` PASS (281 filters loaded). Full log: `tools/studio/STUDIO_INSTALL_LOG.md` (Batch 2). |
| Gotchas | pip install fails inside Blender's bundled Python — use the system venv. MeshLab's GUI binary needs `libopengl0` (`apt-get install -y libopengl0`; apt packages do NOT survive a VM restart). MeshLab filter names changed in 2025.7 (`meshing_decimation_*`, module-level `pymeshlab.filter_list()`); `meshlabserver` is gone — headless work is PyMeshLab only. |
| Pass rule | Every AI prop gets UVs (xAtlas) + a phone budget check (≤ 5k tris for a prop) before it enters `assets/library/`. |

## Stage 1e — Rigging (Rigify) — installed 2026-11-15

| Item | Value |
|---|---|
| Tool | **Rigify 0.6.10** — Blender 4.5.9 built-in addon, no download. |
| What it does | Humanoid/creature rigs from a metarig — the rigging step for MPFB/CharMorph bases and kitbashed characters. |
| Verified | Enabled + `save_userpref()` + fresh-process autoload (`RIGIFY_AUTOLOAD: True`). |
| Gotcha (recorded) | Enabling under `--factory-startup` prints success but does **not** persist — enable WITHOUT `--factory-startup`. And never enable while another agent's Blender is running; the first attempt here was deferred for exactly that reason. |
| Licence | Part of Blender (GPL); rigs it generates are the studio's own. |

## Stage 1f — Sound effects (jsfxr) — installed 2026-11-15

| Item | Value |
|---|---|
| Tool | **jsfxr 1.4.1** (Unlicense) — `~/workspace/tools/jsfxr/` (`npm install jsfxr`), CLI `sfxr-to-wav`. |
| What it does | Synthesizes game SFX offline: `sfxr.generate('pickupCoin')` → JSON definition → `sfxr-to-wav` bakes a WAV. Presets: pickupCoin, laserShoot, explosion, powerUp, hitHurt, jump, blipSelect, synth, tone, click, random. |
| Verified | `pickupCoin` baked to a valid WAV (RIFF PCM, 8-bit mono 44100 Hz, 8,041 bytes). Script: `~/workspace/tools/jsfxr/gen-preset.js`. |
| Note | Output is 8-bit mono — fine as a game-SFX source; convert to 16-bit for a cleaner master. **ChipTone** (no Linux build) and **Bfxr2 / jfxr** are web-only — they were NOT installed (no fake install); use them in the browser: https://sfbgames.itch.io/chiptone, https://sfxr.me (jsfxr web UI), https://bfxr.net. |
| Pass rule | Every SFX is a real baked WAV in `assets/library/audio/` before it is wired into a scene — never a placeholder. |

## Stage 1g — Programmer toolchain (C++ / NDK / GDExtension / Vulkan / Rust / CI) — installed 2026-11-15

The real-programmer layer: native code inside the APK, GPU debugging, and a CI
pipeline. All tools verified with a real test on 2026-11-15 (see
`tools/studio/STUDIO_INSTALL_LOG.md`, Batch 3).

| Item | Value |
|---|---|
| C++ toolchain | **gcc/g++ 13.3.0** (pre-existing) + **cmake 3.28.3** (pre-existing) + **clang/clang++ 18.1.3** (Ubuntu, apt — installed after the system os-intent replay freed the dpkg lock) + **ninja 1.11.1** + **gdb 15.1** + **SCons 4.11.1** (pip venv `~/workspace/tools/venv-scons/`). Verified: hello-world compiles + runs under gcc AND clang; gdb breakpoint at `main` + backtrace works. |
| Android NDK | **NDK r27c LTS** — `~/workspace/game-apk/tools/android-ndk-r27c/` (zip 663,987,688 B, sha256 `59c2f6dc…bad5cc`). Clang 18.0.3 cross-toolchain. Verified: `aarch64-linux-android24-clang` builds a real **AArch64** `.so` (`file` + `llvm-readelf`). This is what lets native C++ ship inside the APK. NDK host `clang`/`clang++` + `lldb` also verified (used as the clang fallback while apt was locked). |
| GDExtension (C++) | **godot-cpp 4.3** (branch `4.3`, commit `d5cc777`) — `~/workspace/tools/godot-cpp-4.3/`. Built with SCons `-j2` (~55 min, 0 errors): static lib `bin/libgodot-cpp.linux.template_debug.x86_64.a` + official sample `test/project/bin/libgdexample.linux.template_debug.x86_64.so` (1,154,480 B). Verified: Godot 4.3 headless editor loads it with 0 errors; the sample project's own test suite passes **120/120**. Note: `--import` alone shows "Native class Example not found" — GDExtensions are not loaded in import mode; the editor + runtime runs are the real proof. |
| Vulkan SDK | **vulkan-tools 1.3.275** + **glslang-tools 15.1.0** + **vulkan-validationlayers 1.3.275** (all apt). Verified: `vulkaninfo` reports device **llvmpipe (LLVM 20.1.2, 256 bits)**, Vulkan 1.3.275 — software Vulkan, as expected with no GPU; `glslangValidator -V` compiles `.vert`/`.frag` to real SPIR-V binaries; the Khronos validation layer loads with 0 loader errors. |
| Rust + godot-rust | **rustup stable, rustc/cargo 1.100.0** (`~/.cargo/`). **godot-rust/gdext 0.5.5** cloned — `~/workspace/tools/godot-rust-gdext/`. Minimal sample crate `~/workspace/tools/godot-rust-sample/` (`Greeter` RefCounted class, `hello()` method) builds to `target/debug/libgodot_rust_sample.so` (108 MB debug build). First build failed on 14 errors in the sample code (missing `#[derive(GodotClass)]`) — fixed, not a RAM failure. The sample is a build proof, not yet wired into a Godot project. |
| CI (prepared only) | **`.github/workflows/ci.yml`** — Eternia CI: import check (gate 1) + gdUnit (gate 2) + Android APK export + apksigner verify. YAML-valid. Local dry-run 2026-11-15: import **exit 0, 0 SCRIPT ERRORs, ~26 s** (the old import stall is FIXED — the ProtonScatter `.blend` was the cause); gdUnit **7/7 PASSED, exit 0**. **CANNOT RUN YET: the repo has no GitHub remote** — create one and push a branch first. The APK export step was not re-run in the dry-run (the local verify gate already covers it). |
| NOT attempted | **Unreal Engine** — needs a GPU, ~32 GB RAM, ~100 GB disk; none on this VM. Recorded, not attempted. |
| Pass rule | A native tool is only "installed" when its own test binary runs and prints the expected result — an apt exit 0 alone is not proof. Apt packages do NOT survive a VM restart (reinstall after any restart). |

## Stage 1h — Real-developers batch (study library / daily backup / QA wired) — installed 2026-11-15

The best tools/practices from the phase-1 research report
(`research_notes/real-game-programmers-20261115/report.md` §§7/10/11).
All verified with a real check on 2026-11-15 (see
`tools/studio/STUDIO_INSTALL_LOG.md`, Real-developers batch).

| Item | Value |
|---|---|
| Study library | **9 open-source Godot games, ~1.4 GB, shallow clones** — `~/workspace/tools/study-library/` (outside the repo; read-only reference, never imported into the game). Reia (AGPL-3.0, Godot 4.7), Thrive (GPL-3.0, 4.7 C#), Sunder (AGPL-3.0, 4.7), godot-demo-projects (MIT, 4.7), Heart Platformer (MIT, 4.0), Circle Jump (MIT, 3.x), Tanks of Freedom (MIT, 2.x), DynaDungeons (GPL-3.0, 2/3-era), Haldric (NO licence file found — study only). Full table + rules in `~/workspace/tools/study-library/README.md`. Failed to clone (recorded): Tanks of Freedom II + Intrepid (network stalls/disconnects — retry later). LFS binaries are pointer files except Reia; `git-lfs` 3.4.1 was reinstalled after a VM restart (apt packages do not survive restarts). |
| Daily backup | **`tools/studio/daily_backup.sh`** — dated git bundle of ALL branches + zip of untracked files + patch of uncommitted modifications, into `~/workspace/cloud-sync/backups/`, keeps the last 7, one log line per run in `backups/backup.log`. Test-run 2026-11-15: bundle 24 MB, `git bundle verify` OK, heads `aetheria-slice` 80f12e0 + `main` 06bd6c9. Cron **`eternia-daily-backup`** runs it daily ~03:19 CET (Africa/Algiers, goal-owned: `project-eternia-3d-rpg`), silent on success, reports failures only. HF cloud upload stays MANUAL via the signed-in browser — no API token exists and none is created. |
| QA wired | **gdUnit4** runs: `verify_gate.sh --skip-apk` 2026-11-15 → Gate 1 import exit 0 / 0 SCRIPT ERRORs, Gate 2 gdUnit exit 0 / no FAILED, Gate 3 54 screenshots 0 bad — VERDICT: PASS (log `reports/studio-gate-20261115-130014.log`). **GUT 9.4.0** present as backup (`addons/gut/plugin.cfg` version 9.4.0). **CI** `.github/workflows/ci.yml` YAML-valid (jobs: verify, android). **Still needs the user: a GitHub remote** — creating a public repo is public publishing and needs explicit approval; without it CI cannot run. |

## Stage 2 — Krita: paint textures

| Item | Value |
|---|---|
| Tool | **Krita 5.3.4.1** — `~/workspace/tools/krita/squashfs-root/usr/bin/krita` (AppImage extracted; FUSE unavailable). Run under `xvfb-run`. Heavy painting on this VM is slow — small canvases, one app at a time. |
| What it does | Anime face/eye textures (1024 px), hair strand textures, blush/mouth/eyebrows, UI art. |
| Inputs | UV layout from Blender, one shared palette. |
| Outputs | PNG (+ `.kra` source next to it) into `assets/library/textures/`. |
| Pass rule | Eyes on a separate texture region (blinking = UV offset); face reads as anime at 1280×720 in a real screenshot — judged by a human, not by the file existing. |
| Alternatives | Inkscape 1.4.4 (vector UI/SVG), Pixelorama 1.2.4 (pixel art), Material Maker 1.8 (procedural PBR for props/armour — not for faces). **ArmorPaint 1.0** (zlib, PBR texture painting for hero/props) — **source cloned, build STILL BLOCKED 2026-11-15**: `../base/make --run` got through asset export + 37/37 shaders, then failed at the first C compile (`make: clang: No such file or directory`, Error 127). Retry 11:07 UTC (VM finally quiet) failed in 3 s at the `apt-get install` step, exit 100: the image's custom `libzstd1 1.5.5+dfsg2-2build1.1+hatch1` blocks Ubuntu's `libzstd-dev` (exact-version Depends) — see `tools/studio/STUDIO_INSTALL_LOG.md` §10. Fix needs a decision: downgrade libzstd1 (risky, core library the image patched) or install a subset / supply headers another way. Fallback meanwhile: Krita 5.3.4.1 + Material Maker 1.8. |

## Stage 3 — Godot: assemble

| Item | Value |
|---|---|
| Tool | **Godot 4.3.stable.official.77dcf97d8** — `~/workspace/game-apk/godot/Godot_v4.3-stable_linux.x86_64` (also `~/workspace/tools/bin/godot`). |
| What it does | Scene assembly, Toon shading (StandardMaterial3D), inverted-hull outline (hero only — 0.00035 width for skinned meshes), SDF face shader, camera, HUD/joystick, dialogue (Dialogue Manager 2.45.0), AI (Beehave 2.9.2), tests (gdUnit4 5.1.1). |
| Inputs | Library assets, Blender exports, Krita textures. |
| Outputs | Scenes under `scenes/`, scripts under `scripts/`, data under `data/*.json`. |
| Pass rule | Headless import: 0 SCRIPT ERRORs. gdUnit: 5/5 PASS. `gdlint` on touched scripts: 0 new issues. **4.3 APIs only** — never Phantom Camera (4.4+), Terrain3D/Dialogic 2 (4.5+), LimboAI/Dialogue Manager 3.10.4 (4.6+). |
| Skills | 86 Godot SKILL.md files in `~/.agents/skills/` (GodotPrompter 59 + vl4dt 17 + ziva-sh 6 + cnqdztp 2). Read the relevant skill before a task, don't guess the API. |
| Scatter | **ProtonScatter 4.2.0** (MIT, HungryProton) in `addons/proton_scatter/` — procedural, non-destructive scatter for grass, rocks, trees, environment density. Godot 4.x rewrite; maintainer says it works on 4.3. **Verified 2026-11-15: headless import exit 0, 0 SCRIPT ERRORs** (52 s). One headless-only ERROR remains (compute shader `compute_relax.glsl` can't import without a rendering device — fine in a real editor). **Trap found: the addon ships a `.blend` in `demos/` — any `.blend` in the tree hangs `godot --import` forever; the demos folder (12 MB) was deleted, addon is now 1.7 MB.** |
| Graphics — PBR / sky / water (2026-11-15) | **Real PBR textures (ambientCG, CC0, 1K):** grass, dirt, stone wall, wood planks, roof tiles in `assets/library/textures/pbr/` (20 MB, manifests + licence rows in `tools/studio/asset-licences-radical-tools.md`). **Water shader** `assets/materials/water_stylized.gdshader` (animated waves, fresnel, sun sparkle, border-mask shore fade — Mobile-safe, no depth texture). **Sky shader** `assets/materials/sky_stylized.gdshader` (painted gradient, sun disc + glow, drifting clouds; golden-hour sun ~20° elevation). **Showcase** `scenes/tests/graphics-showcase.tscn` + real Xvfb screenshots `screenshots-aetheria/15-graphics-pbr.png`, `16-graphics-water-sky.png` (water animates — measured pixel diff; sky shows sun + clouds). **MSAA/SSAO patch** `tools/studio/msaa-ssao-patch.md` — PREPARED ONLY, not applied (MSAA 4x, aniso 4x, SSAO Medium on High / off on Low; FSR is Forward+ only and falls back to bilinear on Mobile). **LightmapGI: NOT BAKED** — node configured, zero baked data; bake-to-scene first, then editor Bake Lightmaps (no CLI bake in 4.3). **Known import stall:** `godot --headless --path . --import` stalls on this project (pre-existing); new textures were imported via the `/tmp/miniproj` workaround (same res:// paths, exit 0) — see `tools/studio/STUDIO_INSTALL_LOG.md` 2026-11-15 §1. **DEEP GRAPHICS (2026-11-15, showcase only):** **LightmapGI: STILL NOT BAKED** — verified in the 4.3 docs: no `bake()` in GDScript, bake is editor-GUI-only and needs a bakeable (static) scene; the slice is runtime-built so it cannot be baked yet; the showcase node is configured (bake_quality 0, bounces 1) with exact GUI steps in the install log §11. **Terrain splat** `assets/materials/terrain_splat.gdshader` (triplanar PBR grass/dirt/stone by height+slope, ~21 samples — patch use only) on a real 12x12 m heightfield mesh `scenes/tests/terrain_patch.mesh` (18,432 tris) — shot 17 (dirt weight too strong, tune before reuse). **Wind sway** `assets/materials/wind_sway.gdshader` (vertex wind + cutout grass) — PROVEN: grass-tuft crop diff 12.34 between t=2 s and t=5 s (shots 18c/18d); tree sway measurable but subtle at distance (crop ~3.5). **LUT grade** `assets/library/textures/lut/cinematic_warm.png` (Hald CLUT 32^3, PIL-generated) + `assets/materials/lut_grade.gdshader` — **works on Mobile, black on Compatibility** (screen texture unavailable there): proven by shot 25 (Mobile, graded, mean lum 171.7) vs the black Compatibility grade-on shots; LUT layer stays hidden by default, in-engine grade proof is the WorldEnvironment adjustment (shots 19/19b, whole-frame diff 8.32). **Cloud shadows** `assets/materials/cloud_shadow.gdshader` (scrolling 2-octave noise) — PROVEN moving (shots 20/20b, whole-frame diff 10.31). **Reflection probes** ProbePond + ProbeWall in the showcase (Mobile-only feature; Compatibility ignores them) — verified present and running on Mobile (shots 23/25, no errors). **Depth water (Mobile)** `assets/materials/water_stylized.gdshader`: depth texture IS live on Mobile and the linearisation is proven correct by debug visualisation (shot 32: green centre = deep+opaque, red rim = shallow+transparent) — BUT the fade does not reach the final alpha in the normal path on lavapipe (unresolved paradox, 9 captures 24-34), so `use_depth_fade` stays 0 and the border-mask fallback ships (blue on both renderers, shots 22/23/35). Do NOT enable it without a Galaxy A16 test. **Godot 4.3 has no LUT slot in Environment and no `DEPTH_TEXTURE` built-in** (use `hint_depth_texture`); **never use `return` in fragment()** (whole shader fails to compile — silently broke shots 24b-24d/27-31); **shader edits load from source at runtime, no re-import needed** (the stale-import theory was wrong). **Light shafts** `assets/materials/light_shaft.gdshader` — intensity 0.5 blew out to white pillars on both renderers (shots 21/23/24/25); lowered to 0.12, now soft columns (shot 24b+). **Hero rim/wrap** `tools/studio/hero-rim-wrap-patch.md` — PREPARED ONLY, do not apply until the hero rebuild commits. **Mobile runs on this VM:** `mesa-vulkan-drivers` + lavapipe (`lvp_icd.json`) run the REAL Mobile renderer under Xvfb (`--rendering-driver vulkan --rendering-method mobile`) — first proven by shots 23-25/35. Full-project `--import` now completes in ~55 s, exit 0 (the old stall is gone after the ProtonScatter `.blend` removal). **PATCHES + INTEGRATION INTO THE MAIN SLICE (2026-11-15, aetheria-slice):** **MSAA/SSAO patch APPLIED** (`project.godot` msaa_3d=2 + ssao quality 1/half_size/blur 2/fadeout 50/300, `e.ssao_enabled=true` + `ssao_light_affect=0.5`, anisotropic on `_toon()` + the showcase PBR materials) — **SSAO is inert here**: the engine warns SSAO is Forward+-only, so on Mobile/Compatibility it does nothing (face unchanged, cheek median 211,176,129 — no washed-face regression); MSAA 4x is set, edge improvement subtle at 1280x720. **Hero rim/wrap patch APPLIED with 4 documented deviations** (`assets/materials/hero_toon_rim.gdshader`, `assets/materials/anime_face.gdshader` Part 1): `next_pass` on ShaderMaterial renders the parts pure black (removed — outlines restored as duplicate meshes, CapeOutline pattern, +5 draws); MPFB meshes are inverted-winding so the rim shader needs `cull_disabled`; the diffuse needs view-space `dot(NORMAL, LIGHT)` (INV_VIEW_MATRIX in `light()` is poisonous on skinned meshes under the shadowed sun) + `light_cap` 0.40 (fitted from shot 10, not the T-pose test); rim in EMISSION (strength 0.45). Result: plate (224,237,254) vs toon baseline (204,220,242) — pale steel, no clipping; cheek unchanged; black outline restored; sword visible; warm rim only faint on the shadow-side edge. Face-shader Part 1 has NO visible effect (the SDF face shader is unwired — it scrambles the curved MPFB face). **Deep graphics integrated:** terrain splat on a 12x12 m hill at (22,0,-12) — grass dominates the top (shot 39, 63% green-dominant) after tuning dirt 0.25-0.60 + low-dirt 0.25 + stone 0.70-0.90 AND fixing the real root cause (see below); wind sway on the near trees (shots 43a/43b, 910 px changed — real but subtle at distance; flowers get no wind, far trees keep `_toon()`); pond at (24,0,6) with water shader (use_depth_fade stays 0) + dirt basin + ReflectionProbe (shot 41, reads well; probe's reflection difference not isolated); Mobile LUT grade gated to Vulkan only (`get_video_adapter_api_version()` starts with "1."; `--aetheria-no-lut` forces it off) — **NOT VERIFIED on Mobile**: the slice segfaults twice on Vulkan/lavapipe during setup (exit 139, no backtrace; probe ruled out as the cause) so the Mobile LUT on/off pair is BLOCKED; the LUT stays hidden on Compatibility (verified — shots are not black). **Cloud shadows: REMOVED — did not survive the move** (42a/42b deleted): the sheet never darkens the ground here (high pair ground luminance identical; a Python replication of the shader's value noise shows clouds should cover the east band yet that ground is not darkened) and it bands the sky as dark blotches in the low shots (39/41/43a). A projection-based approach is needed, not a physical sheet. **TripoSG mossy rock** `assets/library/environments/mossy-rock-10k.glb` in the golem clearing at (-24,0,-56) + a second at (-21.5,0,-53.5), triplanar splat material (no UVs needed), placed UPRIGHT — the GLB is already Y-up (low wide boulder), the task's Y-up→Z-up rotation would lay it on its side (shot 40: reads as mossy boulders, 76% green-dominant). **ROOT CAUSE FOUND (normals):** `scenes/tests/terrain_patch.mesh` ships with INVERTED normals (mean (0,-0.91,-0.05)) — that, not the dirt weights, is why the hill rendered as a dirt mound (and why showcase shot 17 was dirt-heavy); the TripoSG rock GLB has NO normals at all. Both are fixed at runtime by `_mesh_with_fixed_normals()` in `aetheria_slice.gd` (recomputes smooth normals from the triangles, flips if the normalized mean points down or the majority point at the centroid); the shared `terrain_patch.mesh` FILE still carries the inverted normals (separate asset fix). **Budgets:** 183 draw calls (<200), 182,303 primitives (over the <100k guideline — baseline was already 105,879; the +35k after the normal fix is not yet isolated, but draws are within budget). **Verify gate 2026-11-15 12:47 CET: 3/3 PASS** (`--skip-apk`: import 0 errors, gdUnit 0 failed, 54 screenshots OK). **FINAL ROUND — CLEAN GATE (2026-11-15, build+gate worker):** tree cleaned (commit `faef938`: screenshot `.import` noise removed, `screenshots-aetheria/*.import` gitignored, real asset `.import` files committed); export preset `exclude_filter` now `docs/*,screenshots-aetheria/*,scenes/tests/graphics-showcase.tscn` (`terrain_patch.mesh` still ships — the slice loads it at runtime). APK 87,632,794 → **57,371,470 bytes**. **CORRECTION — the MPFB "duplicates" were NOT noise:** `Hero_MPFB.glb` loads `Hero_MPFB_Hero_MPFB_Cape_Folds.png` + `Hero_MPFB_Hero_MPFB_Warrior_Face_Anime.png` at runtime by path; deleting them broke the hero load (`Resource file not found`, hero missing in the Mobile run) and the gate did NOT catch it (import + gdUnit never load the GLB). Regenerated by forced GLB re-import (delete `.godot/imported/Hero_MPFB.glb` `.scn`/`.md5`, re-import — a plain `--import` skips the GLB as up-to-date) and committed as real dependencies (`f29059b`). **Mobile segfault: NOT reproduced this round** — one Vulkan/lavapipe run of the slice exited 0 (120 frames); the exit-139 crash stays unattributed and NOT proven fixed (flaky or memory-pressure related — do not claim fixed). **Final gate 2026-11-15 12:54 CET: 4/4 PASS on the clean tree** (log `reports/studio-gate-20261115-125427.log`): import 0 errors, gdUnit 0 failed, 54 screenshots OK, APK 57,371,470 B, apksigner v1+v2+v3, 1 signer (verified independently). Final shots 08/10 re-captured from the final build and read visually: hero loads, face clean with amber eyes, cape front shows fold bands but still reads as a wide flat red fan; sword not visible in either final framing; hill east face still a near-black scar. Final-shots budget print: 48 draw calls, 78,740 primitives (the 182,303 peak recorded earlier still stands over the <100k guideline). **Golem fight STILL MISSING (VFX only).** |

## Stage 4 — Android APK: export + sign

| Item | Value |
|---|---|
| Tool | Godot export preset **"Android Mobile"** (arm64-only, target android-34), JDK Temurin 17.0.21 (`~/workspace/game-apk/tools/jdk17`), Android SDK build-tools 34.0.0 (`~/workspace/game-apk/tools/android-sdk`), debug keystore `~/workspace/game-apk/debug.keystore`. |
| What it does | `--headless --export-release "Android Mobile" <path>` then `apksigner verify`. |
| Inputs | The project, preset `export_presets.cfg` (package `com.gggg.eternia`, version 0.1). |
| Outputs | APK in `builds/android/` (gitignored) or `~/workspace/your_files/` for delivery. |
| Pass rule | Export exit 0; `apksigner verify` prints `Verified using v1 scheme: true`, `v2: true`, `v3: true`, `Number of signers: 1`; APK > 10 MB and < 100 MB. If Godot reports "apksigner tools failed", put `jdk17/bin` on PATH and sign manually with the debug keystore — never ship an unsigned APK. |
| Note | `docs/` (1.8 GB offline Godot docs) is excluded from the APK via `exclude_filter="docs/*,screenshots-aetheria/*,scenes/tests/graphics-showcase.tscn"` (added 2026-11-15 — the 45 MB of screenshots were packed into the 87.6 MB APK; `terrain_patch.mesh` is NOT excluded, the slice loads it at runtime). Final clean APK 2026-11-15: 57,371,470 bytes, v1+v2+v3, 1 signer. apt packages (git-lfs, audacity, lmms, scrcpy) do NOT survive a VM restart — reinstall after a restart before committing binaries. |

## Stage 5 — Verify: the gate

| Item | Value |
|---|---|
| Tool | `tools/studio/verify_gate.sh` (this studio's gate — see below). |
| What it does | Runs four gates in order: (1) headless import, (2) gdUnit tests, (3) real-screenshot check, (4) APK export + signature. Prints PASS/FAIL per gate + a final verdict. |
| Inputs | The project as it stands (including uncommitted work — the gate reports the truth, it does not repair). |
| Outputs | Console verdict + log in `reports/studio-gate-<date>.log` (gitignored `reports/`). |
| Pass rule | **ALL FOUR gates PASS.** Anything else = NOT READY. The gate never fixes game files. |
| The real-phone test | The gate's screenshots come from Xvfb on the VM (Compatibility renderer, software FPS 1–3 — that number means nothing about the phone). The final verdict is always the user's Galaxy A16: install / start / movement / FPS 30. **A screenshot is not a phone test.** |

## Performance budgets (Galaxy A16 — hard limits)

| Budget | Limit |
|---|---|
| Visible triangles / frame | < 100k |
| Draw calls / frame | < 200 |
| Live particles | < 2,000 |
| Dynamic lights | ≤ 3 (plus 1 directional sun, baked LightmapGI) |
| Texture size | ≤ 1024 px (2048 hero only, never 4K) |
| Shadow map | 1024 px (512 px on Low) |
| Render scale | 0.6–0.75× (720p internal), 30 fps target |
| Hero | ≤ 15k tris, 1 draw call for the body where possible |
| APK size | < 100 MB (aim < 40 MB) |

## Departments (seven)

One-page briefs in `studio/departments/`: **Character, Environment, Animation,
VFX, Sound, Build, Verification**. Each owns a slice of this pipeline, has a
gate, and ships with an exact subagent brief template. **Verification is
independent: it never builds or fixes, it only audits — and nothing reaches
the user before its sign-off.**

## Rules (studio-wide)

1. **Free / open-source only.** No paid tool, key, asset, or subscription
   without the user's explicit approval for that named cost.
2. **Godot 4.3 only.** No in-place upgrade; upgrades happen on a separate
   branch with a clean A16 playtest.
3. **Licence first.** Every asset gets a row in `AssetLicenses.md` before it
   is used. CC0 / OFL only for shipping.
4. **Real pictures only.** A game is judged from a real screenshot of an
   actual Godot run — never an AI concept image presented as the game.
5. **One harness, one test runner.** OpenCode OR Goose (not both);
   gdUnit4 is the test runner (GUT is backup only).
6. **Commit small, commit on a branch.** Never commit another agent's
   in-flight files. Never touch `main` from a slice branch.
7. **Copyleft character bases stay out of the shipped hero.** An AGPL-3.0
   character mesh (CharMorph mb_male / mb_female) or any UNVERIFIED base may
   be used for blocking and study, but the shipped hero mesh must come from a
   CC0-verified base (MPFB base mesh, a verified-CC0 character, Quaternius).
   When in doubt, the licence row in `AssetLicenses.md` decides — no row, no
   ship.
8. **AI-generated props: know which licence the output carries.** TripoSG /
   TRELLIS outputs are MIT (props only, never the hero). **Hunyuan3D-2mini
   outputs are non-commercial / prototype only** (Tencent Community Licence
   + non-commercial header) — never ship them in a commercial release
   without re-reading the full licence. TRELLIS GLBs use a
   research/evaluation-only exporter — same rule.

## Cloud — asset backup (Hugging Face)

| Item | Value |
|---|---|
| Repo | https://huggingface.co/datasets/gfhtgfghfcvvf/eternia-studio-assets (public, free tier, account `gfhtgfghfcvvf` / samir412005com@gmail.com) |
| Synced 2026-11-15 | `README.md` (dataset card) + `eternia-studio-assets-library.zip` (1.04 MB: Kenney audio, Noto Sans Arabic, Poly Haven HDRI, licence manifests) — verified on the repo Files page and via the HF API |
| What it is | Backup + sharing for the studio's asset library. NOT a build input: the game still builds from `assets/` in this repo. |
| What is NOT synced yet | Hero files (Warrior_Anime.glb/.blend, painted face, hair cards, baked cape) and VFX shaders — they sync after the complete developed slice lands on a clean commit. |
| How to sync | Zip `assets/library/` (excluding `*.import`), upload the zip + an updated README to the repo root via the web UI. No API token is created for this; uploads go through the signed-in browser. |
| Honest note | No free cloud is literally infinite. Hugging Face is the strongest free one for assets (effectively uncapped public dataset storage, git-based). Local disk still has 124 GB free (2026-11-15) — the cloud is for backup and growth, not because space ran out. |
