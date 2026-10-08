# SACRED SYMMETRY — C11-C v2.1.2

Family id: `sacred_symmetry`

Presentation-only Visual Loop prototype. No C11-B simulation, RNG ownership, C7 audio contract or C9 authoring contract is modified.

## Art identity

radial symmetry / astrolabe / mechanical geometry.

## Current social delivery

- 720×1280 (9:16)
- 30 FPS
- 20..30 s policy-driven / round(duration×30) frames
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

## Current D7/D8 state

C11-C 2.19.12 is frozen. C11-D D7 is PASS/CLOSED and FROZEN; D8.0 is the next phase. The active C11-D baseline is `ChallengeEngineV01_STATELESS_C11-D_7.5_V8_FROZEN_20261008_111052.zip` (SHA-256 `396d9f4bfdbb44b4878acf06db8d6c1c385103c110de537a174632e93611cd1d`).

## Directory contents

### Subdirectories
- None.

### Representative files
- `SacredSymmetry.gdshader`
- `SacredSymmetryPrototype.gd`
- `SacredSymmetryPrototype.tscn`
- `SacredSymmetryRenderer.gd`
- `generate_c11c_sacred_symmetry_v1_music.py`
- `run_prototype.ps1`
