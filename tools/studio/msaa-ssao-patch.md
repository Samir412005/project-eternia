# MSAA + Filtering + SSAO Patch — PREPARED ONLY, NOT APPLIED

**Status: 2026-11-15 ~10:30 CET — this file only documents the change. `project.godot` was NOT edited.**
**Apply only after the hero-rebuild agent commits its work, on a clean tree, then re-run the verify gate (`tools/studio/verify_gate.sh`) and re-shoot the slice before any delivery.**

## Why a patch, not an edit
The hero-rebuild agent owns the running tree right now. Editing `project.godot` under it would risk a merge conflict in the file every system reads. This patch is the exact, verified change set to apply once the tree is clean.

## Setting names — verified, not guessed
Verified two ways on 2026-11-15:
1. Live Godot 4.3 dump (`-s` script printing `ProjectSettings.get_property_list()` filtered for msaa/ssao/anisotropic/screen_space_aa/taa/scaling_3d): all names below exist; current values shown in §4.
2. Offline Godot 4.3 docs (`docs/godot-4.3/_sources/`): `VIEWPORT_MSAA_2X = 1`, `VIEWPORT_MSAA_4X = 2`; `anisotropic_filtering_level` is "maximum samples as a power of two" (value 2 = 4 samples = 4x); SSAO quality levels Low / Medium / High / Ultra.

## 1. Exact `project.godot` change (add under `[rendering]`)

```ini
[rendering]

anti_aliasing/quality/msaa_3d=2
anti_aliasing/quality/msaa_2d=0
anti_aliasing/quality/screen_space_aa=0
textures/default_filters/anisotropic_filtering_level=2
environment/ssao/quality=1
environment/ssao/half_size=true
environment/ssao/blur_passes=2
environment/ssao/fadeout_from=50.0
environment/ssao/fadeout_to=300.0
scaling_3d/mode=0
```

Meaning of each line:
- `msaa_3d=2` — MSAA 4x on the 3D viewport (enum: 0 Disabled, 1 = 2x, 2 = 4x, 3 = 8x). This is the one real anti-aliasing win for the slice's hard geometry edges.
- `msaa_2d=0` — keep 2D MSAA off; the UI is vector/rounded-rect, it does not need it.
- `screen_space_aa=0` — FXAA stays OFF. FXAA + MSAA together double-blur the toon edges; MSAA alone is sharper on this art style. (FXAA would be `1`.)
- `anisotropic_filtering_level=2` — maximum 4x anisotropic samples (power of two: 2 → 4 samples). This is already the project default, so this line only pins it. **Alone it does nothing** — see §2.
- `environment/ssao/quality=1` — SSAO **Medium** as the project default for new Environments (enum: 0 Low, 1 Medium, 2 High, 3 Ultra; current default is 2 = High). Medium is the Mali-G57 compromise: High costs too much fill-rate on a tile GPU at 1080p, Low is visibly banded.
- `half_size=true`, `blur_passes=2`, `fadeout_from=50`, `fadeout_to=300` — keep the current defaults (half-resolution SSAO + 2 blur passes is the cheap configuration; fadeout keeps SSAO out of the far vista where it only adds noise).
- `scaling_3d/mode=0` — render-scale stays 1.0 (Disabled) for the High preset. The Low preset uses `scaling_3d` (see §3), not MSAA.

## 2. Two companion changes the project settings alone do NOT do

These are required or the patch is a no-op. They touch files owned by other agents — apply them in the same commit as §1, after the tree is clean.

### 2a. Enable SSAO on the slice Environment (project settings are only defaults)
In `scripts/world/aetheria_slice.gd`, where the Environment is built (next to the existing `e.glow_enabled = false` line, ~line 265):

```gdscript
e.ssao_enabled = true          # High preset only
e.ssao_light_affect = 0.5      # keep the toon shadows readable; 1.0 darkens the crevices too much
```

**Do not enable SSAO on the same Environment that has `glow_enabled = false` without re-shooting the hero closeup** — the graphics pass measured real bloom washing the hero to (255,166,132); SSAO darkens crevices and can re-introduce the same washed/dark swing on the face. Re-shoot shot 10 after applying.

### 2b. Anisotropic filtering needs a per-material opt-in
Per the 4.3 docs, anisotropic filtering "is not enabled by default on 2D and 3D materials". For it to affect the new PBR ground/path/wall, each `StandardMaterial3D` must set:

```gdscript
mat.texture_filter = BaseMaterial3D.TEXTURE_FILTER_LINEAR_WITH_MIPMAPS_ANISOTROPIC
```

Apply to the five PBR materials in `scenes/tests/graphics-showcase.tscn` (and, when the slice adopts the PBR textures, to its ground/path materials). Without this line, `anisotropic_filtering_level` changes nothing.

## 3. Presets — High vs Low (the rule the patch encodes)

| Setting | High (this patch) | Low (phone fallback) |
|---|---|---|
| `msaa_3d` | 2 (4x) | 0 (Disabled) |
| SSAO (`e.ssao_enabled`) | `true`, quality Medium (1) | `false` |
| Anisotropic (per-material) | on (4x max) | off (`TEXTURE_FILTER_LINEAR_WITH_MIPMAPS`) |
| `scaling_3d/mode` + `scale` | 0 (off, scale 1.0) | `1` (Bilinear) + `scale = 0.66` |
| `screen_space_aa` (FXAA) | 0 | 0 |

Low is the only preset that may run on a hot/throttled Galaxy A16. The Low preset is a runtime switch (set the values in code at startup from a saved quality setting), not a second `project.godot` — the values in §1 are the High defaults the project ships with.

**Correction (verified in the 4.3 docs, `class_projectsettings.rst.txt`): FSR is only effective with the Forward+ renderer — on Mobile or Compatibility it silently falls back to bilinear.** This project ships the Mobile renderer, so the Low preset uses Bilinear (`mode=1`), never FSR (`mode=2` FSR 1.0 / `mode=3` FSR 2.2). Selecting FSR on Mobile buys nothing and hides what is really running.

## 4. Current state before the patch (measured 2026-11-15, Godot 4.3)

| Setting | Current |
|---|---|
| `rendering/anti_aliasing/quality/msaa_3d` | 0 (Disabled) |
| `rendering/anti_aliasing/quality/msaa_2d` | 0 |
| `rendering/anti_aliasing/quality/screen_space_aa` | 0 |
| `rendering/anti_aliasing/quality/use_taa` | false |
| `rendering/textures/default_filters/anisotropic_filtering_level` | 2 (4x max, but no material opts in) |
| `rendering/environment/ssao/quality` | 2 (High default) |
| `rendering/environment/ssao/half_size` | true |
| `rendering/environment/ssao/adaptive_target` | 0.5 |
| `rendering/environment/ssao/blur_passes` | 2 |
| `rendering/scaling_3d/mode` / `scale` | 0 / 1.0 |
| Slice Environment `glow_enabled` | `false` (deliberate, measured — real bloom washed the hero) |
| Slice Environment `ssao_enabled` | not set (off) |

`project.godot` contains no msaa/ssao/anisotropic/scaling lines today — every value above is the Godot default.

## 5. Expected cost on the Mali-G57 (Galaxy A16) — honest estimate

No number below was measured on the phone; the VM cannot measure phone FPS. These are the established costs for a tile-based Mali-G57 MC2 at 1080×2340, internal render 0.66–0.75×, <150k tris:

- **MSAA 4x:** the expensive one. On a tile GPU, 4x MSAA multiplies colour/depth tile memory and resolve bandwidth. Expect **~15–30% frame-time cost** at native 1080p, less (~10–20%) at 0.66× render scale. If the slice is at 30 fps without MSAA, MSAA 4x alone can push it to ~22–26 fps. **If the phone test shows <28 fps with this patch, drop to MSAA 2x (`msaa_3d=1`) before touching anything else.**
- **SSAO Medium, half-size:** a half-resolution screen-space pass + 2 blur passes. Expect **~5–10%** at 0.66× scale. The `fadeout_to=300` keeps it out of the far vista. If banding appears, raise `blur_passes` to 3 (costs more) rather than raising quality to High.
- **Anisotropic 4x:** nearly free on Mali for the ground plane (a few % at most) because it only affects minified, oblique textures — the dirt path at a grazing angle is exactly where it pays.
- **FXAA (off):** would cost ~2–3% but blurs the toon edges; correctly left off.
- **Combined High preset:** budget **~20–35% total frame-time cost** vs today's all-defaults build. The slice has headroom (primitives + one sun + <200 draw calls), but the only verdict that counts is the user's real-phone test.

## 6. Rollback (exact, in order)

1. In `project.godot`, delete the ten lines added in §1 (or set `msaa_3d=0` and `environment/ssao/quality=2` to restore defaults).
2. In `scripts/world/aetheria_slice.gd`, set `e.ssao_enabled = false` (or delete the two lines added in §2a).
3. In the PBR materials, set `texture_filter` back to `TEXTURE_FILTER_LINEAR_WITH_MIPMAPS` (or delete the §2b lines).
4. Re-run `tools/studio/verify_gate.sh --skip-apk`, re-shoot shots 10/15/16, re-export the APK. The rollback is complete only when the gate is 4/4 again on the reverted tree.

## 7. What this patch does NOT do
- It does not enable TAA (`use_taa` stays `false` — TAA smears the toon shader's hard bands; never enable it on this art style).
- It does not touch `scaling_3d` for High (render scale stays 1.0; the slice's 0.66–0.75× scale is a Low-preset runtime switch using **Bilinear**, not FSR — FSR is a no-op on the Mobile renderer, see §3).
- It does not bake lightmaps (see the LightmapGI note in `STUDIO_INSTALL_LOG.md` 2026-11-15 §6) and it does not change the sky, water, or hero.
