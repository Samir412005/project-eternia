# AssetLicenses.md — PROJECT ETERNIA

Every third-party asset in `assets/` with its source URL and licence.
**Only CC0 / OFL (public-domain-equivalent) assets are allowed in this project.**
No attribution is legally required for CC0/OFL, but sources are recorded here.

| File(s) | Source | Licence |
|---|---|---|
| `assets/library/audio/kenney-rpg-audio/bookOpen.ogg`, `doorOpen_1.ogg`, `chop.ogg` (+ `License.txt` from the pack) | Kenney "RPG Audio" pack — https://kenney.nl/assets/rpg-audio (downloaded 2026-11-15 via the site's signed download link) | **CC0 1.0** (public domain) |
| `assets/environments/kenney-nature/tree_cone.glb`, `cliff_block_rock.glb`, `flower_redA.glb` | Kenney "Nature Kit" — https://kenney.nl/assets/nature-kit (downloaded 2026-11-15 via the site's signed download link) | **CC0 1.0** (public domain) |
| `assets/library/environments/poly-haven-hdri/kloppenheim_06_puresky_1k.hdr` | Poly Haven — https://polyhaven.com/a/kloppenheim_06_puresky (direct file: `https://dl.polyhaven.org/file/ph-assets/HDRIs/hdr/1k/kloppenheim_06_puresky_1k.hdr`) | **CC0 1.0** (public domain) |
| `assets/library/fonts/noto-sans-arabic/NotoSansArabic-Regular.ttf`, `NotoSansArabic-Bold.ttf` (v2.009) | googlefonts/noto-fonts — https://raw.githubusercontent.com/googlefonts/noto-fonts/main/hinted/ttf/NotoSansArabic/ (OFL) | **SIL Open Font License 1.1** |

| `assets/environments/kaykit-medieval/buildings/green/*` (homes, tavern, market, church, blacksmith, windmill, castle, towers, well), `assets/environments/kaykit-medieval/decoration/props/*` (crates, sacks, flags, tent, buckets, weaponrack, wheelbarrow...) + `hexagons_medieval.png` atlas | KayKit "Medieval Hexagon Pack" — https://github.com/KayKit-Game-Assets/KayKit-Medieval-Hexagon-Pack-1.0 (downloaded 2026-11-15, full glTF folder copied for the selected green set only) | **CC0 1.0** (public domain) |
| `assets/characters/kaykit/*` (sword_1handed, shield_round, axes, staff, wands, mugs, quivers + knight/rogue/mage/barbarian textures) | KayKit "Character Pack Adventures" — https://github.com/KayKit-Game-Assets/KayKit-Character-Pack-Adventures-1.0 (downloaded 2026-11-15; note: this repo holds weapons/items only — the character meshes themselves are NOT in it) | **CC0 1.0** (public domain) |
| `assets/characters/quaternius/Warrior.fbx`, `Warrior_Texture.png`, `Warrior_Sword_Texture.png` (Aetheria slice hero; 44-bone rig, 14 embedded clips incl. Idle/Walk/Run/Sword_Attack; raw height 2.95m, scaled to ~1.8m in-game) | Quaternius "RPG Characters" pack — https://quaternius.com/ (copy on disk: `~/workspace/video-lab/assets/characters/rpg_characters/RPG Characters - Nov 2020/`, License.txt in the pack) | **CC0 1.0** (public domain) |
| `assets/characters/mpfb/Hero_MPFB.glb` (NEW hero, 2026-11-15: MPFB 2.0.18 CC0 base mesh, masculinized, anime proportions, decimated 36,972 → 9,898 tris, painted anime face on a split Face_Anime material, raycast hair cards + hair-helmet cap, real baked cloth cape (7 deep pleats, 1.10 m hem), blue tunic/belt/pants/boots, chest plate, Quaternius sword kitbash (0.68 m), 7 clips retargeted from Mixamo (see Mixamo row): Idle_Weapon/Walk/Run/Sword_Attack/Jump/Hit/Death; .blend at `~/workspace/mpfb_hero/Hero_MPFB.blend`, OUTSIDE the project tree) | Base mesh: MPFB 2.0.18 (makehumancommunity.org, Blender extension, code GPL-3.0-or-later, base mesh + standard assets **CC0**); re-style + clothes + cape + retarget done in this studio; sword source is the CC0 Warrior.fbx above (shoulder pads NOT used — they read as flat slabs, remodel pending) | **Project-original, derived from CC0** — no third-party licence; ship freely. Copyleft bases (CharMorph mb_male/mb_female AGPL, Antonia custom licence, reom unverified) were NOT used — STUDIO.md Rule 7. |
| Mixamo animation clips (7): `Idle.fbx`, `Walking.fbx`, `Running.fbx`, `Sword_And_Shield_Slash.fbx`, `Jumping.fbx`, `Hit_Reaction.fbx`, `Dying.fbx` (FBX, no skin, 30 fps, root motion stripped in the retarget so every clip plays in place; retargeted onto the MPFB rig as Idle_Weapon/Walk/Run/Sword_Attack/Jump/Hit/Death; source files in `~/workspace/cloud-sync/mixamo/`, NOT in the project tree) | Mixamo — https://www.mixamo.com/ (downloaded 2026-11-15, free account; Sword_And_Shield_Slash used instead of a plain "Sword Attack", which does not exist on Mixamo) | **Free under Adobe Mixamo terms (NOT CC0)** — free to use in games; the clips are data, not code; no attribution required. Recorded here per the studio rule that Mixamo is free under Adobe terms, not public domain. |
| `assets/characters/quaternius/Warrior_Anime.glb`, `Warrior_Face_Anime.png`, `Hair_Strands.png`, `Warrior_Anime_Hair_Strands.png`, `Warrior_Anime_Warrior_Texture.png`, `Warrior_Anime_Warrior_Sword_Texture.png`, `Warrior_Anime_Warrior_Face_Anime.png` (hero re-style, pass 1 done 2026-11-15: painted anime face, lifted fringe, 10 hair cards, baked cloth cape, metallic fixed to 0, cape repositioned to shoulders-to-calves) | Derived in this studio from the CC0 Warrior.fbx above (Blender re-style + Krita-painted anime face + hair cards) | **Project-original, derived from CC0** — no third-party licence; ship freely |
| `assets/materials/anime_face.gdshader`, `cape_outline.gdshader`, `cape_sway.gdshader`, `outline.gdshader` | Written in this studio (Godot shader code) | **Project-original** |
| Quaternius "Ultimate Animated Character" pack — `Casual_Male.glb`, `Soldier_Male.glb` (17 clips each; NO Crouch clip) — NOT imported into this project yet | https://quaternius.com/packs/ultimatedanimatedcharacter.html (Google Drive folder linked from the pack page) — on disk at `~/workspace/game-apk/last-signal/project/assets/character/` | **CC0 1.0** (public domain) per the pack's shipped License.txt |
| Godot Anime SDF Shader Kit (`albanogiovanni/godot-anime-sdf-shader`) | https://github.com/albanogiovanni/godot-anime-sdf-shader | **LICENCE UNVERIFIED — DO NOT SHIP.** Not stated in the catalog listing. Read the repo licence before depending on it; if unclear, port the MMDX `hoyo_toon` math instead. |
| `assets/library/characters/golem/Golem.glb`, `Golem_LavaCracks.png`, `build_golem.py`, `README.md` (rock golem boss, 1,880 tris; lava cracks = generated emissive texture + emissive lava geometry, no bloom) + `.blend` source at `~/workspace/blender-sources/project-eternia/golem/Golem.blend` (OUTSIDE the Godot tree — a `.blend` inside the project hangs `godot --import` forever, proven 2026-11-15; see the golem `README.md`) | Built in this studio 2026-11-15 (VFX dept): procedural displaced icospheres/boxes in Blender 4.5.9, crack texture generated in-script, no imported meshes | **Project-original, procedural** — no third-party licence; ship freely |
| `scripts/vfx/sword_trail.gd`, `scripts/vfx/slash_effect.gd`, `scripts/vfx/hit_sparks.gd`, `scripts/vfx/ember_loop.gd`, `scripts/vfx/vfx_demo.gd`, `assets/materials/vfx_trail.gdshader`, `assets/materials/vfx_slash.gdshader`, `scenes/vfx/*.tscn` (sword trail ribbon, slash arc, hit sparks 48 particles, ember loop 60 particles, demo scene) | Written in this studio 2026-11-15 (VFX dept), Godot 4.3 / Mobile renderer | **Project-original** — no third-party licence; ship freely |
| Gennai "Free Godot 4 VFX" (13 samples incl. EDGEFLUX Lite sword trail / slash / hit sparks) — **NOT vendored, technique reference only** | https://github.com/kai777123/godot-4-free-vfx (cloned 2026-11-15, LICENSE file read: MIT, Copyright (c) 2026 gennai) + https://gennai.itch.io/edgeflux-lite | **MIT** (GitHub repo) — free commercial use, keep the MIT notice if the code is ever copied in. **NOT SHIPPED:** the samples target **Godot 4.4+ only** (project.godot `features=["4.4"]`, author tested 4.4.1/4.7.2 only, never 4.3), so no files were copied into this 4.3 project. The itch Lite page carries a *separate* proprietary free licence (royalty-free, no credit, do NOT resell/redistribute the pack, keep `addons/edgeflux_fx` out of public repos) — also not vendored. |
| Ember VFX 3D Lite (inkharbor, 6 effects: campfire, fireball, arcane burst, lightning strike, heal aura, ice shatter) — **NOT vendored** | https://inkharbor.itch.io/ember-vfx-3d-lite (licence text read from the page 2026-11-15) | **Proprietary free licence (NOT MIT, NOT CC0):** free for commercial and non-commercial games, modification allowed, no attribution needed; **may NOT redistribute or resell the files** as a standalone asset or inside another asset pack. **NOT SHIPPED:** requires **Godot 4.4+ — does NOT run on 4.3** (shaders use the 4.4 `hint_enum` uniform hint). The itch download is also gated (no direct URL), so the zip was not fetched. |
| Ember VFX 3D Vol. 2 Lite (inkharbor, 5 effects: Fire Wall, Ice Spikes, Stone Pillar, Divine Ray, Fireworks) — **NOT vendored** | https://inkharbor.itch.io/ember-vfx-3d-vol-2-lite (licence text read from the page 2026-11-15) | **Proprietary free licence (NOT MIT, NOT CC0):** free for personal and commercial games, no attribution required (full text in the download's LICENSE.txt); full pack forbids sharing/publishing the effect files and keeping them in public repos. **NOT SHIPPED:** minimum Godot 4.3, but tested on 4.3 **Compatibility renderer only — the Mobile renderer is NOT tested**, and the itch download is gated (no direct URL), so the zip was not fetched. |

## Licence rules (studio-wide, added 2026-11-15)

- **Quaternius licence change:** the Nov 2020 RPG pack and the Ultimate Animated
  Character pack are CC0 1.0 per their shipped License.txt files. Newer
  Quaternius packs are QAL v1.0 — check the licence file of EACH pack at
  download time and record it here. Never assume CC0.
- **VRoid-derived content is FORBIDDEN** in this project unless the live VRoid
  terms have been read and the permission recorded here. Same for MMD game
  models (the `hoyo_toon` *technique* may be ported; the models themselves
  must never be used) and any AI-generated 3D used as the hero (AI 3D is
  props-only, never the hero, never a face).
- **Human Generator (HumGen3D) assets are PAID** — the addon code is GPL but
  the humans cost money on BlenderMarket. Never use; never download pirate
  mirrors (illegal).
- **Mixamo clips** (if imported later) are free under Adobe's Mixamo terms —
  free for use, NOT CC0. Record that exactly when they arrive.
- **Copyleft art** (CC BY-SA / GPL, e.g. 0 A.D., Flare, Veloren): usable in a
  free game with attribution, but derivatives must carry the same licence.
  Keep copyleft assets in a separate folder so a future commercial release
  can swap them out. None are in this project yet.
- **Library moves 2026-11-15:** Kenney RPG Audio, Noto Sans Arabic and the
  Poly Haven HDRI were moved into `assets/library/` (see `assets/library/README.md`).
  KayKit-Medieval, Kenney-Nature, KayKit weapons and Quaternius stay in place
  until the hero agent's uncommitted work is committed — the migration plan is
  in `assets/library/README.md`.

Notes:
- Kenney download links are signed and expire; re-download from the pack page if a re-fetch is ever needed (the page's `download-link/<hex-id>` endpoint returns a fresh URL when called with a `Referer` header).
- Only small samples were copied into the project (3 sounds, 3 models, 1 HDRI, 2 font weights). The full packs remain in `~/workspace/tools/downloads/` (`kenney_rpg-audio.zip`, `kenney_nature-kit.zip`).
- The Poly Haven API (`api.polyhaven.org`) returned HTTP 522 on 2026-11-15; the direct `dl.polyhaven.org` file URL worked.
