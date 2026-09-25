# C11-C Visual Music Direction v3.0

## Objective

Replace the former single global ambient bed with a **family-aware deterministic music system** that supports the visual identity of each Drill/Loop family while remaining mobile-safe and non-intrusive.

## Non-negotiable constraints

- Presentation/delivery only: music does not calculate gameplay truth.
- No dependency on gameplay events, `winning_frame`, answer sheets, target timestamps or renderer-inferred events.
- 44.1 kHz stereo WAV before delivery encoding.
- Peak target <= 0.20 before AAC mux.
- No kick/snare/percussion layer.
- No harsh high-frequency transient content.
- Deterministic output for seed + family + semantic profile.
- Three-second gentle settling in Drill mode so END_CTA does not feel like an audio cut.
- Loop mode is periodic and does not encode gameplay events.

## Semantic profiles

| Profile | Function | Paired identity |
|---|---|---|
| `FLOWING_VECTOR` | Airy low-mid motion bed | Tracking ↔ Invisible Forces |
| `CIRCUIT_PULSE` | Precise harmonic pulse without percussion | Saccade ↔ Geometric Waves |
| `ORGANIC_BLOOM` | Warm evolving chord bloom | Pursuit ↔ Fractal Bloom; also Living Particles |
| `ORBITAL_RITUAL` | Slow celestial harmonic orbit | Peripheral Scan ↔ Sacred Symmetry |
| `PRISMATIC_MEMORY` | Mirrored/prismatic harmonic refraction | Historical Kaleidoscope alias |

The pairing is semantic, not synchronized: the paired Drill and Loop share a musical grammar so they feel like members of one audiovisual world without making the soundtrack reveal task timing.

## Architecture

`profiles/presentation/c11c_visual_music_profiles.json` is the source-of-truth binding table. `core/presentation/C11CVisualMusicProfile.gd` provides metadata lookup for presentation. `tools/prototypes/c11c_common/generate_c11c_family_music.py` is the deterministic generator. `C11CSafeAmbient.py` remains the compatibility entrypoint used by existing launchers.

Visual Loop launchers generate family/profile-aware audio. The Visual Drill review launcher generates one WAV per family/seed and stores its SHA-256 in the per-run manifest. Social sidecars identify the exact music mode/profile.

## Why no motion/event sync yet

The intent at this stage is audiovisual pairing, not a reactive score. Exact target/event synchronization would create a new coupling between media and gameplay truth and would require a separate auditable contract. That is deliberately deferred.

## Regression

`tests/C11CVisualMusicProfileContractTest.gd` validates profile definitions, current bindings, historical aliases, mobile-safe flags, the intended Drill/Loop pairings, and non-coupling constraints.
