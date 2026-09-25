# MASTER HANDOVER — C11-C 2.11.0

## Baseline
Validated baseline: `ChallengeEngineV01_STATELESS-C11-C2.10.1`.

## Overlay rule
2.11.0 is intentionally distributed as a file overlay, not a full-project archive. Copy the overlay contents into the repository root.

## Canonical Visual Loop family map
| technical_id | artistic_name | runtime_id | production_id |
|---|---|---|---|
| `geometric` | Geometric Waves | `geometric` | `c11c_geometric_waves_v1` |
| `fractal` | Fractal Bloom | `fractal` | `c11c_fractal_bloom_v1` |
| `kaleidoscope` | Sacred Symmetry | `sacred_symmetry` | `c11c_sacred_symmetry_v1` |
| `particle_flow` | Living Particles | `living_particles` | `c11c_living_particles_v1` |
| `vector_field` | Invisible Forces | `invisible_forces` | `c11c_invisible_forces_v1` |

These are the same five historical families.

## Visual Drill hooks
`profiles/presentation/c11c_visual_hooks.json` contains exactly 10 hooks for each of `tracking`, `saccade`, `pursuit`, `peripheral_scan`. One deterministic hook is selected from seed + family offset. The exact selected hook is used both in Header and social copy.

## Social copy
Fixed hashtags first: `#GenerativeArt #GodotEngine #LoopArt #OddlySatisfying`. Family/subfamily hashtags follow. Internal QA fields such as CTA position, typography and hook index stay in manifests, not in public copy.

## Music
Mode name remains `FAMILY_MUSIC_V3`; generator revision is 3.3.0. Music is presentation delivery only. Visual Drills use seed + family; Visual Loops use seed + visual grammar. The social/header hook is editorial copy only and does not drive audio; gameplay events/frames/answer sheets are prohibited.

Profile pairing:
- Tracking ↔ Invisible Forces = `FLOWING_VECTOR`
- Saccade ↔ Geometric Waves = `CIRCUIT_PULSE`
- Pursuit ↔ Fractal Bloom / Living Particles = `ORGANIC_BLOOM`
- Peripheral Scan ↔ Sacred Symmetry = `ORBITAL_RITUAL`
- Kaleidoscope/Sacred Symmetry history route = `PRISMATIC_MEMORY`

Audio constraints: 44.1 kHz stereo, peak ceiling 0.36, target RMS 0.085–0.16, A-minor pentatonic, long ADSR, low-pass, loop-safe deterministic modulation, no percussion, no harsh HF transients. Seeded whole-pad pitch scaling may vary from 0.80× to 1.20× while preserving harmonic intervals.

## Frozen boundaries
Do not modify C11-B simulation truth, mechanics, structural RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7 ownership/contracts or C9 authoring semantics.

## Audio smoke validation

```powershell
python .\tools\prototypes\c11c_common\validate_c11c_family_music.py --seed 314159 --duration 1.0
```

This checks short deterministic profile renders, 44.1 kHz stereo, peak/RMS bounds and one representative loop seam. It does not replace phone-speaker listening.
