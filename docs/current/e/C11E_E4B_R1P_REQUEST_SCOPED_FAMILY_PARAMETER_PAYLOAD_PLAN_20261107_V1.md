# C11-E E4B-R1P — Request-Scoped Loop Family Parameter Payload Plan V1

**Date:** 2026-11-07  
**Status:** PREPARATION PLAN ONLY — not implemented or runtime-accepted.

## 1. Purpose and boundary

Build one auditable, request-scoped parameter payload for each of the 27 explicit Visual Loop grammar selectors, derived from the canonical E1/D9.9 request and the already accepted D9.10 family-stage contract.

This stage must prove that the selected C11-C family profile, grammar selector, resolved palette and duration/timebase are bound to the same request and deterministic gameplay-seed domain. It must not claim that pixels, frame buffers, renderer-native inputs or media have been generated.

For clarity, split the old ambiguous “27 actual payload receipts” requirement into:

- **R1P — parameter payload:** 27 immutable typed family parameter receipts; no renderer, node, shader, launcher, audio or media.
- **R1V — visual/frame payload:** actual C11-C source frames and frame inventory/hashes. This requires the independent D4.8 gate and its explicit authorization; it remains blocked.

R1P does not satisfy R1V and does not close the pixel-consumer gate.

## 2. Canonical selector matrix

Derive selectors from `c11c-suite/c11c-producer/producer_schema.json`, excluding the `auto` entry:

| Family ID | Internal profile family | Explicit grammars |
|---|---|---:|
| `c11c_geometric_waves_v1` | `geometric` | 5 |
| `c11c_fractal_bloom_v1` | `fractal` | 5 |
| `c11c_sacred_symmetry_v1` | `sacred_symmetry` | 5 |
| `c11c_living_particles_v1` | `living_particles` | 5 |
| `c11c_invisible_forces_v1` | `invisible_forces` | 7 |
| **Total** | | **27** |

The V80 static source audit has cross-checked the canonical grammar order against the corresponding `C11CVariationProfile.gd` grammar arrays and each family's existing prototype override: all five family maps match exactly. Revalidate the same mapping against the active checkout before implementation. Do not infer that the geometric order applies to other families.

## 3. Required inputs and source pins

Every case begins with the existing shared service, not a hand-built D9.9 approximation:

1. Build a canonical Visual Loop request using the existing E1 service preparation/validation path.
2. Obtain the canonical D9.9 request, plan, D9.10 bridge record, D-only adapter envelope and `loop_family_stage_contract` from the shared service.
3. Validate the family-stage contract before parameter derivation.
4. Pin at least:
   - `c11c-suite/c11c-producer/producer_schema.json`;
   - `tools/prototypes/c11c_common/C11CVariationProfile.gd`;
   - `tools/prototypes/c11c_common/C11CPaletteBank.gd`;
   - `tools/prototypes/c11c_common/C11CVisualLoopDuration.gd`;
   - each of the five family prototype scripts and the five canonical launcher scripts;
   - `tools/c11d/d9/c11e_e4b_loop_family_stage_contract.py`;
   - current E1 shared service and E1/D9 bridge/adapter dependencies;
   - the approved A1/A3/composition/timebase/audio policy hashes already enforced by the stage contract.

V80 source pins observed during this audit (re-hash them in the active checkout before implementation):

| Source | SHA-256 |
|---|---|
| `c11c-suite/c11c-producer/producer_schema.json` | `564f11fb4fee9221910dc373550650172eda4f106d6dc25532cc43cb8e6314a0` |
| `tools/prototypes/c11c_common/C11CVariationProfile.gd` | `f7df994d8842183275bc331decd75762a153f3100248c7cc8b590e34c1347e2d` |
| `tools/prototypes/c11c_common/C11CPaletteBank.gd` | `6b64d99afb148b0dc5b0f8e27b50558e9b77df4d2fdff98d52495d81d53fdd14` |
| `tools/prototypes/c11c_common/C11CVisualLoopDuration.gd` | `4ea0b0decbd3a22ade42023e819a74872f312b63facc1163dc73a7c656fdbaf8` |
| `tools/c11d/d9/c11e_e4b_loop_family_stage_contract.py` | `bfbfa0cc108f00b78003e5480c86af1ee5ca63772d24a7792f8cdb6953b6af5d` |

The V80 static source audit has already compared the ordered explicit grammar arrays in the producer schema, `C11CVariationProfile.gd` and each family's `*Prototype.gd`: **5/5 family maps and 27/27 explicit selector IDs match exactly**. See `C11E_E4B_R1P_STATIC_FAMILY_GRAMMAR_AUDIT_20261107_V1.md`. This proves selector identity/order only; it is not a runtime payload receipt.

The package includes the read-only validator `tools/c11d/d9/test_c11e_e4b_r1p_family_grammar_static_audit.py`; it passed `py_compile` and the V80 source snapshot audit. Run it from the active checkout root with `py -3.13 tools/c11d/d9/test_c11e_e4b_r1p_family_grammar_static_audit.py` before deriving any parameter receipts. It prints a JSON report to stdout and performs no writes.

Use paths discovered from the canonical producer schema and current snapshot; do not assume a different repository layout. Re-hash them in the active checkout before implementation.

## 4. Parameter derivation rules

For every request/grammar pair:

- Use `request.seed` as the only input to the C11-C visual variation profile and palette derivation.
- Keep `request.music_seed` separately bound to request identity; never pass it to the visual profile, palette bank or visual launcher.
- Call `C11CVariationProfile.build(family_internal_id, gameplay_seed)` and retain the full family-specific recipe.
- Apply an explicit grammar override using the selected grammar's zero-based index in that family's explicit grammar array (the `auto` entry is not part of this index): set both `grammar_mode` and `grammar_name` to the selected selector identity.
- Resolve the palette through `C11CPaletteBank.palette(family_internal_id, palette_mode, gameplay_seed)` and retain the full resolved palette dictionary.
- Derive loop duration using `C11CVisualLoopDuration.policy_seconds_for_cycles(loop_cycles)`. Do **not** use `resolve()` for this stage: it reads the `C11C_DURATION_SECONDS` environment override and could make a supposedly canonical parameter receipt environment-dependent.
- Use `C11CVisualLoopDuration.FPS` (30) and derive the planned frame count as `round(duration_seconds * FPS)`. The 1/2/3 cycle policy produces 20/22/23 seconds, or 600/660/690 planned frames. Label these as planned timebase values, not captured/rendered frames.

Do not squeeze family recipes into the geometric-only `VisualAuthoringGenerator` envelope or reuse its `STYLE_KEYS` projection across all five families. The existing `materialize_visual_loop_exact_selector_payload_v2_in_memory.gd` is explicitly limited to the five Geometric Waves selectors; it is not evidence for the other 22 selectors.

## 5. Receipt contract

One receipt per explicit grammar selector, with at least:

- schema/version and `status=FAMILY_PARAMETER_PAYLOAD_PREPARED_TEST_ONLY`;
- request id/hash, plan hash, editorial hash, bridge-record hash and D-only adapter hash;
- `family_id`, internal family id, grammar id, grammar index and launcher identity;
- gameplay seed and music seed with an explicit assertion that music seed is not consumed by visual derivation;
- `C11CVariationProfile` source pin, full variation recipe, explicit grammar override and recipe SHA-256;
- `C11CPaletteBank` source pin, full resolved palette and palette SHA-256;
- duration policy source pin, loop cycles, planned duration, FPS and planned frame count;
- deterministic repeat result from recomputing the same selector/request/seed;
- relevant producer schema, prototype and launcher hashes;
- governance assertions that no prototype Node, renderer, shader, launcher, Godot render, FFmpeg, D3/audio, mux, frame buffer, pixel or media was created.

A Python validator must reject missing selectors, duplicates, wrong family-to-internal mappings, grammar-order mismatches, seed-domain crossover, altered source pins, duration/FPS inconsistency, non-deterministic repeat hashes, missing keys or governance flags not explicitly false.

The GDScript/engine-facing step, if used, must load only the relevant deterministic RefCounted profile/palette/duration scripts. It must not instantiate a prototype Node or renderer. Capture one machine-readable result per case; the Python side validates and seals the receipts. No receipt is immutable until its exact inputs and all post-generation hashes verify.

## 6. Existing components that must not be confused

- The existing D9.9/D9.10 family-stage contract is in-memory, family-bound and non-dispatchable; it is not the parameter payload.
- The existing V2 GDScript harness covers only Geometric Waves and contains a geometric authoring-envelope projection. It cannot be represented as coverage of all 27 selectors.
- `VisualAuthoringGenerator`'s generic subtypes are not a universal renderer interface for the five C11-C families. Keep each family's native variation dictionary and palette schema intact.
- Parameter receipts cannot include a fabricated `frame_inventory`, image hash or `renderer_native_input` claim.

## 7. Exit criteria and later gates

R1P may be accepted only at `PASS_TEST_ONLY_PARAMETER_PAYLOADS` when all 27 exact selectors have one valid receipt each, all five family grammar maps align with the canonical schema, deterministic repeats pass, and source/seed/governance constraints are intact.

R1V remains unstarted and blocked until D4.8 independently authorizes the relevant visual execution. Only R1V may establish actual source frame count/inventory/pixel hashes. E4B-R2 then proves a D-only pixel consumer at the existing D9.10 seam, preserving frame identity/order and the approved no-crop/no-stretch/no-resampling composition.

No stage here changes C11-C or grants renderer, dispatch, media, freeze, promotion or release authority.
