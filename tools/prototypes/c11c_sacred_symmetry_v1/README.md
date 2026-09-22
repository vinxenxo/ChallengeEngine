# SACRED SYMMETRY — C11-C v2.1.2

Family id: `sacred_symmetry`

Presentation-only Visual Loop prototype. No C11-B simulation, RNG ownership, C7 audio contract or C9 authoring contract is modified.

## Art identity

radial symmetry / astrolabe / mechanical geometry.

## Current social delivery

- 720×1280 (9:16)
- 30 FPS
- 18.00 s / 540 frames
- 4/3 scale from the frozen 540×960 logical composition

The launcher creates a temporary root `override.cfg` to override viewport + window size during Movie Maker capture, then restores/removes it. `project.godot` remains untouched.

## Run one video

```powershell
.\tools\prototypes\c11c_sacred_symmetry_v1\run_prototype.ps1 -Seed 271828
```

Disable audio with either:

```powershell
... -NoSound
... -Silent
```

A successful run leaves one canonical MP4 for the seed, plus review/trace sidecars.
