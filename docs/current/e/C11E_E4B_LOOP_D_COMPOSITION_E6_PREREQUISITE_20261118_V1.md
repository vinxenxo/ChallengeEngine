# E4B Loop D Composition — E6 Prerequisite V1

**Disposition:** `BLOCKED_NOT_IMPLEMENTED`; this does not reopen the accepted E4B shared-service preparation scope or invalidate R1V/Loop22 media closeouts.

## What is already accepted

- E4B shared E1 service preparation and GUI/CLI parity in its declared scope.
- R1P parameter/grammar handoffs 27/27 PREPARE_ONLY.
- R1V five-selector A/B media and human review.
- Loop22 22/22 A/B pairs and operator closeout 44/44.
- The Option C architecture selection and D post-composition boundary design.

## What is not implemented

The existing `c11e_e4b_loop_family_stage_contract.py` creates an in-memory family-stage contract with status `FAMILY_BOUND_PREPARATION_NOT_DISPATCHABLE`; its governance keeps `renderer_native_input_emitted=false`, `renderer_dispatch_invoked=false`, `launcher_invoked=false`, `godot_invoked=false`, `ffmpeg_invoked=false`, and `media_created=false`.

`editorial_render_bridge.py` and `d_render_adapter.py` are plan/bridge records, not a compositor. The dynamic request payload binder's accepted Loop composite is a single exact-selector in-memory review object (`c11c_geometric_waves_v1 / harmonic_membrane`). It is not a full 27-grammar materializer, ShaderMaterial execution, pixel compositor or D-owned video.

The Option C boundary requires: immutable C11-C source video; actual R1V frame inventory and decoded pixel identity; canonical D9.9 plan identity; canonical D9.10 bridge identity; R1P family parameter receipt; D-owned, separate output; exact frame order and no temporal resampling; approved field allowlist and layout. It keeps the source file untouched.

## Required implementation seam

Use the existing Option C boundary. Do not create a parallel Producer, renderer, binder or family adapter. A future D-only consumer must:

1. Accept a validated, immutable C11-C video plus sidecar/media metadata and the exact ordered source frame inventory/pixel hashes.
2. Accept an exact, validated D9.9 plan and D9.10 bridge record, R1P parameter/family identity and approved editorial values.
3. Preserve the native frame timeline/order, resolution and source-body identity. No frame drop/duplication/interpolation/padding, no resampling and no source overwrite.
4. Compose D-approved presentation/editorial onto an independent D-owned output surface/video. Preserve C11-C Loop binder, grammar timeline and family-native music. Keep `request.seed` and `request.music_seed` orthogonal; visual composition must not consume music seed.
5. Produce deterministic, typed evidence: source video hash, ordered inventory hash, decoded pixel hash list, request/plan/bridge/parameter hashes, composition profile/policy hash, output hash, frame/timebase mapping, and exact field-consumption receipt.
6. Fail closed on missing evidence, unapproved geometry/font/field windows, unknown or disallowed fields, source/destination collision, output overwrite or output cardinality mismatch.

## Incremental acceptance plan

- Stage L0 — source closure/read-only audit: exact live source pins and a single R1V selector inventory.
- Stage L1 — pure Python/Qt offline pixel consumer tests with synthetic frames; no Godot, FFmpeg, launcher or media tools.
- Stage L2 — isolated one-selector pixel proof against a copied, verified C11-C frame sample; write separate output only under a TEST_ONLY evidence root.
- Stage L3 — operator visual placement review and negative controls (source identity, frame order, field allowlist, seed-domain isolation, geometry, font fit, frame count and overwrite protection).
- Stage L4 — widen the same consumer to the six E6 Loop selectors; do not claim all 27 grammars until the family-wide gate is completed.
- Stage L5 — integrate the exact Loop rows into Smoke18's one-shot TEST_ONLY run after successor policy and execution authorization.

## E6 consequence

The six existing Loop A/B MP4s remain reusable C11-C source and family-music evidence. They cannot be counted as D-composited Smoke18 outputs. All six Smoke18 Loop rows require D composition evidence unless a future exact row-level artifact passes the frozen D-composition predicate.
