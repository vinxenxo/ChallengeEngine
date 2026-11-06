# C11-E E4B Visual Loop — Source Review V1

**Review date:** 2026-11-06. **Source reference:** `ChallengeEngineV01_STATELESS C11-E Current Authority V70.zip` supplied by the operator (read-only archive; never overlaid). ZIP CRC passed. Frozen C11-C manifest in the archive is 796,318 bytes / SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## 1. Canonical family/grammar inventory

Read from `c11c-suite/c11c-producer/producer_schema.json` (32,714 bytes, SHA `564f11fb4fee9221910dc373550650172eda4f106d6dc25532cc43cb8e6314a0`):

| Family ID | Runtime family | Concrete grammars |
|---|---|---|
| `c11c_geometric_waves_v1` | geometric | `harmonic_membrane`, `interference_plane`, `parametric_ribbon`, `lattice_wave`, `orbital_wave` |
| `c11c_fractal_bloom_v1` | fractal | `radial_bloom`, `dendritic_tunnel`, `spiral_fractal`, `fractal_filigree`, `nested_worlds` |
| `c11c_sacred_symmetry_v1` | sacred_symmetry | `astrolabe`, `gear_train`, `polygon_orrery`, `origami_mandala`, `celestial_chart` |
| `c11c_living_particles_v1` | living_particles | `swarm`, `vortex`, `collision_cloud`, `organic_pulse`, `magnetic_filament_cloud` |
| `c11c_invisible_forces_v1` | invisible_forces | `dipole_field`, `vortex_field`, `saddle_field`, `quadrupole_field`, `gravitational_lens`, `topographic_basin`, `scalar_potential` |

Total: 5 active families / 27 concrete grammars. `auto` is a selector mode, not a concrete grammar. Historical aliases in the music profile registry are not extra active families.

## 2. Correct producer route and shared presentation

The current C11-C family producer route consists of the five prototype scenes, not the separate legacy `core/presentation/rendering/VisualContentPlayer.gd` path. Each family prototype directly preloads `C11CVisualEditorialLayer.gd`, instantiates `UnifiedSocialFrame`, calls `_mount_editorial(frame)`, and calls `_editorial_layer.apply_render_model(_editorial_model)`; their frame callback updates the editorial frame index and Matrix state.

Source pins from the supplied V70 snapshot:

| Source | Bytes | SHA-256 |
|---|---:|---|
| `tools/prototypes/c11c_geometric_waves_v1/GeometricWavesPrototype.gd` | 11,359 | `ab2560cbe7fa42c5cad3b143aa59d1f2a0dc047682f7667983c7c0a0f6dbb61c` |
| `tools/prototypes/c11c_fractal_bloom_v1/FractalBloomPrototype.gd` | 11,196 | `b596ecba5eeae80ba615d7cb8a741dffcab9db4c44296e660f4f9d6919cc5c55` |
| `tools/prototypes/c11c_sacred_symmetry_v1/SacredSymmetryPrototype.gd` | 11,376 | `12fdbc13e05df28b26cf95fe1907d150bd41f29196287700153521e9baee336b` |
| `tools/prototypes/c11c_living_particles_v1/LivingParticlesPrototype.gd` | 11,423 | `835ba0df2c160a259be39bd1977bfac0e6a66f903ce1aa6b4247af7c508ad94a` |
| `tools/prototypes/c11c_invisible_forces_v1/InvisibleForcesPrototype.gd` | 11,442 | `a68661a5fdf792aa7fe701afa6fbf1631a2b8215c214032f58ecfe0c69d8374a` |
| `core/presentation/C11CVisualEditorialLayer.gd` | 19,047 | `f8f718c067a4d7a088cc16f244cc40209e7183bec93e44d8cb66eb6dd404cf7d` |
| `core/presentation/UnifiedSocialFrame.gd` | 2,087 | `d80c07103f56a2abfe34be60547285e61b0d03b50a5ed93c3c72d4241f6585ba` |
| `tools/prototypes/c11c_common/C11CHeaderAnimatorV2.gd` | 9,631 | `44c4a9a11c334e6e84fcc1413667accac175781787866c3d6b894beeba3ea255` |
| `tools/prototypes/c11c_common/C11CVisualLoopDuration.gd` | 1,048 | `4ea0b0decbd3a22ade42023e819a74872f312b63facc1163dc73a7c656fdbaf8` |

The initial observation that `VisualContentPlayer` only mounts this layer for Drill applied to the legacy player route and was not a valid description of the current C11-C Loop family producer. This review corrects that scope error.

## 3. Native header/footer ownership

`C11CVisualEditorialLayer` owns one shared text label for the header and one for the footer. It composes a three-line header, an up-to-three-line footer, measures/wraps the text and animates a sequence of header blocks through `C11CHeaderAnimatorV2`. It does not expose a separate free-standing D editorial lane.

All five family prototypes already populate these regions:
- Header line 1: grammar-specific math/identity plus generated metrics (e.g. wave/morph; fractal equation/detail; symmetry order/gears; particle density/flow; field traces/pulse).
- Header line 2: deterministic family technobabble generated from C11C seed and variation; part of the Matrix transition.
- Footer line 1: seed, body dimensions, actual duration, FPS, loop count and family-specific metrics.
- Footer line 2: palette name, loop count and `FAMILY MUSIC V4` identity.
- Footer line 3: family/version identity.

This is already populated C11-C content. A blanket D mapping of title/subtitle to HEADER and CTA to FOOTER over `[0, frame_count)` would collide with existing content. The policy proposal is not approved. No field mapping is applied by this review.

## 4. D9 / E1 consumption boundary

D9.8 model `definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json` (12,692 bytes, SHA `50655c82521a353f1db6920f4d099cad92452ae369251f9fbde45cbaee4e8c53`) defines exactly four Loop editorial fields: `title`, `subtitle`, `call_to_action`, `language`. Empty optional strings normalize to `UNKNOWN`; keys remain present.

E1 service `c11c-suite/c11c-producer/c11e_production_service.py` (32,885 bytes, SHA `348997e575d985fe153a4f433f089c5f205be5d4d8f3853baf07be917a134951`) resolves the four values but emits `editorial_field_consumption.consumer_status=NOT_CONSUMED_E1`, `required_gate=E4`, and family adapter `c11e_visual_loops_adapter / NOT_CONNECTED_E1 / target_gate E4`. This is expected in E1 and does not establish visual consumption.

D9.9 resolver `tools/c11d/d9/universal_producer.py`: 19,692 bytes / SHA `9ad2adbf54946f2225ae2ed36b88abfc5717387f2ff03bbed684aa8bd32d87d1`. D9.10 bridge `tools/c11d/d9/editorial_render_bridge.py`: 10,868 bytes / SHA `fe9d40052b0f4ff6f1c862c010ae7b3b13070b6ce935be6d62f9dcaec63a644a`. Both remain planning-only; no renderer input is emitted.

## 5. Family music and independent seed domains

E1 service route for Loop is `PRESERVE_EXISTING_C11C_FAMILY_MUSIC_PATH`, status `PROTECTED_FAMILY_NOT_REWIRED`; it has no D3 V5 engine request and no dispatch/audio creation. Do not run D3 V5 for Loop.

Current C11-C family music wrapper `tools/prototypes/c11c_common/C11CSafeAmbient.py` is 1,739 bytes / SHA `c376fd44a3115f0d800213d95e28143363748e16c7b5800369fcadbf237fb02c`. Generator `generate_c11c_family_music.py` is 16,382 bytes / SHA `41bb8f9842ac941ea86c838f272b11bd0642973b26e92defa006721a3d8cb84d`. Profile registry `profiles/presentation/c11c_visual_music_profiles.json` is 7,038 bytes / SHA `b78706c5a9adbf1581d925f522b76cc3419983177de213734cc79996af5cbf58`.

Existing family mapping: geometric→`CIRCUIT_PULSE`; fractal→`ORGANIC_BLOOM`; sacred_symmetry→`ORBITAL_RITUAL`; living_particles→`ORGANIC_BLOOM`; invisible_forces→`FLOWING_VECTOR`. `generate_c11c_family_music.py` includes seed, family, profile and grammar in deterministic semantic derivation. However, each existing `run_prototype.ps1` passes its single `$Seed` both as `C11C_SEED` for visual generation and as the seed argument to `C11CSafeAmbient.py`. E4B must preserve the same generator and mapping while separating inputs at the D orchestration seam: visual runner with `-NoSound` and `request.seed`; existing music wrapper separately with `request.music_seed`, runtime family, exact mapped profile/grammar, actual loop cycle count and duration; mux with H.264 stream copy. No C11-C runner or generator source changes. Use unique non-existing output roots because the legacy family runner removes files with matching names under its output root.

## 6. Static audit evidence and one separate discrepancy

Loop-specific suites on the V70 source archive:
- Dynamic request payload binding: 12/12; 46/46 source pins.
- Loop grammar binding audit: 14/14.
- Request-scoped binding matrix V2: 22/22.
- Timing review inheritance audit: 13/13.
- Timing review reference carrier: 18/18.
- Request-bound reference carrier: 26/26.
- Shared editorial presentation inheritance: 15/15.
- Loop/Drill field-window proposal tests: 22/22 (`PROPOSED_NOT_APPROVED`).
- Grammar parameter instance: 17/17.

Total Loop-focused: **159/159 PASS**. These are static/source/contract tests only; no Godot runtime or media was invoked.

Separate D9 Challenge provenance-join suite: 13/14 PASS. The sole failure is the contract pin for `tools/c11d/d9/materialize_challenge_visual_payload_in_memory.gd`: expected 27,036 bytes / SHA `8f8e4c9be6170d48319b62512a1e1cdb40c4f126563deb3546dfd302b080179e`; actual V70 archive file 89,712 bytes / SHA `01deb2419f88012c162a1ab56013cb4a724fda72a5de70f5434cf5dad1a1e753`. This is a Challenge-specific stale-pin reconciliation item. It has not been changed or resealed under E4B.

## 7. In-memory Loop plan-only probe

A read-only in-memory E1/D9 probe of `visual_loops / c11c_geometric_waves_v1 / harmonic_membrane`, `REVIEW`, `REVIEW_720`, `social_default_v1`, variation 0, audio enabled, personalization enabled, gameplay seed 314159, music seed 840001, and global `language=es` returned:

- GUI/CLI request hash equal; editorial hash equal; plan hash equal; E1 intent hash equal.
- Bridge records equal; D-only adapter envelopes equal.
- Canonical editorial: `title=UNKNOWN`, `subtitle=UNKNOWN`, `call_to_action=UNKNOWN`, `language=es`.
- Family adapter `NOT_CONNECTED_E1`, target E4, renderer input false.
- Music contract `PROTECTED_FAMILY_NOT_REWIRED`, route preserve existing C11-C family music, D3 engine null/not invoked, audio not created.
- All execution flags false, D4.8 blocked, release authority NONE.

This is an in-memory test-workspace probe, not the required manual GUI execution and not render/media evidence.

## 8. Next controlled action

Run the single existing Producer GUI Loop plan-only fixture defined in `C11E_E4B_LOOP_GUI_CLI_PARITY_PLAN_20261106_V1.md`. Then resolve and document a non-destructive visual coexistence policy before any D Loop adapter source change. Keep renderer, dispatch and media OFF.
