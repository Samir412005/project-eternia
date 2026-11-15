# GAME DESIGN — PROJECT ETERNIA (PROPOSAL, NOT FINAL)

> Status: **proposal for discussion**. Nothing in this document is a
> final storyline, final hero identity, or final art direction. It is
> written down so decisions can be argued about and changed — per the
> brief, no final identity is invented silently.

## 1. Premise (proposed)
A fantasy valley, Eternia, whose old shrines have gone quiet. The player
is a warden-in-training who must relight them. Scope is deliberately
small in Phase 1 (one valley) and grows region by region.

## 2. Pillars (proposed)
1. Third-person exploration over combat grind.
2. Shrines as the progression spine (each one teaches a mechanic).
3. Readable, calm fantasy art — achievable on a Galaxy A16 (Mobile
   renderer, low-poly, strong lighting, fog).
4. Touch-first controls; desktop is for testing only.

## 3. Hero (proposed, NOT decided)
- Working name: **Ashan, Warden of the Valley** (`data/characters/player.json`).
- The name, look and backstory are placeholders until the user approves
  a direction.

## 4. World (Phase 1 real / later proposed)
- REAL: Eternia Valley, 60 x 60 m — ground, north/east platforms,
  ruined pillars, trees, Ancient Shrine, training dummy.
- PROPOSED: Ashen Woods, Sunken City, Frost Peaks (data-only in
  `scripts/world/world_regions.gd`, not built).

## 5. Systems (Phase 1)
XP + levels, attributes, 3 starter skills (data), equipment slots,
inventory (24 slots), quests (3 defined, 1 completable), dialogue,
save/load v1, combat vs one dummy, shrine interaction, day clock
(slow drift), quality presets (Low/Medium/High).

## 6. Explicitly NOT in Phase 1
Story cinematics, weather, NPCs, world streaming, multiplayer,
in-app purchases, voice, music, imported character art.
See `DEVELOPMENT_ROADMAP.md`.
