# C11-D Renderer Visual Payload Materialization Preview — V1

**Status:** `PREPARATION_ONLY_IN_MEMORY_VISUAL_PAYLOAD_PREVIEW_NOT_RENDERER_INPUT`  
**Approval:** not approved; not frozen; no D4.8 authorization  
**Frozen C11-C manifest SHA-256:** `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`

## Purpose

This increment closes the gap between family/type-only binding and a request-scoped, deterministic in-memory authoring payload for the existing Visual Loop and Visual Drill APIs. It uses the existing Godot authoring and variation code. It is a test harness, not a renderer or production command.

## V1 fixtures

- **Visual Loop:** `c11c_geometric_waves_v1` / `harmonic_membrane`, seed `12345`, variation index `0`, `REVIEW_720`. Uses `VisualAuthoringGenerator` for the family envelope, `C11CVariationProfile` plus the selected grammar override for the existing visual recipe, `C11CPaletteBank` for the seeded palette, and `C11CVisualLoopDuration.policy_seconds_for_cycles` for the fixed review duration. It deliberately does not use the environment override path from `.resolve()`.
- **Visual Drill:** `tracking` / `tier-2`, seed `12345`, variation index `0`, `REVIEW_720`. Uses `VisualAuthoringGenerator` and the existing `VisualDrillSeedVariation.apply` authoring stage. It validates the resulting frame count and seeded trajectory metadata.
- **Challenge:** `CHALLENGE_004` remains unmaterialized in this harness. It must be obtained from the frozen `ChallengeExecutionPipeline` runtime output; this increment will not simulate or clone Challenge behaviour.

## Semantics and limits

Payload objects and digests live only in memory for the lifetime of the headless process. The harness prints summary hashes, durations and frame counts. It does not write a payload file, invoke a renderer, create a media artifact, or change engine sources. `variation_index` is bound as metadata in V1 but is not transformed into a separate C11-C seed; that policy remains explicitly unresolved for non-zero variation indices.

`harmonic_membrane` is represented as an explicit visual recipe overlay alongside the family-level authoring envelope because the C10 authoring API's loop subtype is `geometric`, not the producer's grammar ID. No core authoring API is modified.

## Verification

1. `python .	ools\c11d\d9	est_d_renderer_visual_payload_materialization_preview.py`
2. `godot --headless --path . --script res://tools/c11d/d9/materialize_visual_payloads_in_memory.gd`
3. Run the prior request binding, timebase projection, editorial review, D9.13, candidate preflight and 22-step suite tests.

Expected headless summary reports `materialized=2/3`, determinism `2/2`, and `challenge=FROZEN_RUNTIME_OUTPUT_REQUIRED`. A PASS here means the two in-memory authoring payloads are deterministic; it does not mean they are approved or renderer-ready.

## Governance

C11-C 2.19.12 remains immutable. Renderer stays OFF; `media_created=false`; D4.8 remains BLOCKED; `release_authority=NONE`; D9.14/D9.16 full acceptance, D9.17 closure and D10 remain blocked as previously recorded.
