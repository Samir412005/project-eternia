# AGENTS.md — PROJECT ETERNIA (pin, read first)

- **Godot 4.3 ONLY. Mobile renderer.** Never upgrade Godot in place; upgrades happen only on a separate Git branch with a clean A16 playtest.
- **Never use Godot 3 APIs** (e.g. `KinematicBody`, `Spatial`, `yield`, `export var` old syntax). Never use 4.4+ APIs: check every new API against https://docs.godotengine.org/en/4.3 (offline copy: `docs/godot-4.3/`). `TileMapLayer` is OK — it is 4.3+.
- **Engine:** `~/workspace/game-apk/godot/Godot_v4.3-stable_linux.x86_64`. Export preset: `Android Mobile` (arm64-only, target android-34). JDK 17 + Android SDK 34 in `~/workspace/game-apk/tools/`.
- **After every edit, verify headless, in order:**
  1. `godot --headless --path . --check-only --script <file>.gd`
  2. `godot --headless --path . --quit-after 300` (smoke run)
  3. `godot --headless --path . --export-release "Android Mobile" /tmp/eternia-verify.apk` (only when the change touches the build)
- **Exit code 0 does NOT mean no runtime errors — always read stderr.**
- **Addons on 4.3 only:** Beehave, GUT/gdUnit4 (pick one), Dialogue Manager old 4.3-compatible release. Never install Phantom Camera (4.4+), Terrain3D / Dialogic 2 (4.5+), LimboAI / Dialogue Manager 3.10.4 (4.6+) on this branch.
- **Assets:** CC0 only (Kenney / Poly Haven / ambientCG / Quaternius). Record every asset in `AssetLicenses.md` with source URL + licence.
- **Free / open-source only.** No paid tools, keys, or subscriptions. No Docker, no GPU, no Android emulator on this VM.
- **Saves:** JSON in `user://`, item IDs not Resources. Never `ResourceLoader`-load a save file (code execution).
