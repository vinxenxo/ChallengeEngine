# C11-D Renderer Temporal Schedule Proposal — Checkpoint V1

**State:** `PREPARATION_ONLY_TEMPORAL_TOPOLOGY_NOT_APPROVED_NOT_FROZEN`  
**Date:** 2026-10-10  
**Depends on:** D1.5 layout contract; D renderer region-hierarchy reconciliation; existing C11-C timeline/runtime source  
**Scope:** D-owned source audit and topology proposal only. No frozen C11-C source or manifest is changed.

## Why this checkpoint exists

The renderer candidate needs a known temporal topology, but it must not invent durations or frame ranges. The repository already contains different temporal contracts for Challenges, Visual Loops and Visual Drills. This checkpoint records only what those sources establish, leaving per-request values unbound.

## Source-grounded topology

| Content type | Existing authority | Supported topology | What remains unbound |
|---|---|---|---|
| Challenge | `ChallengeTimeline` + `ChallengeTimelineBuilder` + canonical video profile | `HOOK → GAME → REVEAL → CTA` | Actual profile-bound phase durations and resulting frame counts for a specific request |
| Visual Loop | `VisualLoopTimeline` + `VisualLoopRuntime` | One continuous duration span; local loop frame wraps within that span | Bound payload duration, FPS and frame count for a specific request |
| Visual Drill | `VisualDrillTimeline` + `VisualDrillRuntime` | One continuous duration span; no engine subphases are declared | Bound payload duration, FPS and frame count for a specific request; any future subphase schema |

For Challenge, `ChallengeTimeline` already defines the phase order and `ChallengeTimelineBuilder` resolves the time configuration from its validated video profile. The D proposal does not set phase durations, fill absent values, derive timing from editorial fields or change phase behavior.

For Visual Loops and Visual Drills, the runtimes require `duration`, `fps` and `frame_count`, check the frame count against `round(duration × fps)`, and then construct the corresponding timeline. The proposal does not pick those values. `VisualDrillTimeline.gd` explicitly notes that phase semantics are pending a JSON schema definition; the D layer therefore cannot create preparation/training/reveal phases by assumption.

## Relationship with layout and family composition

The existing `D_RENDERER_REGION_HIERARCHY_RECONCILIATION_V1` and D1.5 remain the spatial authority. The legacy normalized-permille rectangles are not canonical and do not drive this proposal. Existing family/profile/rendering routes stay intact; no new family-specific geometry is inferred from family names.

## Files

- `definitions/c11d/production/D_RENDERER_TEMPORAL_SCHEDULE_PROPOSAL_V1.json` — pinned source set, temporal topology rules and execution/approval locks.
- `definitions/c11d/production/D_RENDERER_TEMPORAL_SCHEDULE_PROPOSAL_SCHEMA_V1.json` — strict Draft 2020-12 schema for the in-memory report.
- `tools/c11d/d9/d_renderer_temporal_schedule.py` — source-pinned, deterministic topology report builder and validator; no filesystem output at runtime.
- `tools/c11d/d9/test_d_renderer_temporal_schedule.py` — three content types, determinism, source lineage, schema checks and fail-closed negative controls.
- `tools/c11d/d9/requirements-validation.txt` — optional `jsonschema` dependency for library-backed Draft 2020-12 validation.

## Output boundary

The output is a topology report, not an instantiated schedule:

- `concrete_schedule_instantiated=false`
- `duration_values_emitted=false`
- `frame_indices_emitted=false`
- `frame_ranges_emitted=false`
- `timeline_instantiated=false`
- no pixel coordinates, renderer-native input, dispatch, renderer activation, production or media

`winning_frame` and `close_calls` are not accepted as timing controls. A concrete schedule will require a separately validated canonical request/payload with bound upstream timing values. It cannot synthesize timing from editorial copy or from this proposal.

## Windows verification

Run the focused test and then the established regression set:

```powershell
python -m py_compile `
  .	ools\c11d\d9\d_renderer_temporal_schedule.py `
  .	ools\c11d\d9	est_d_renderer_temporal_schedule.py

python .	ools\c11d\d9	est_d_renderer_temporal_schedule.py
python .	ools\c11d\d9	est_d_renderer_region_hierarchy.py
python .	ools\c11d\d9	est_d_renderer_semantic_regions.py
python .	ools\c11d\d9	est_d_renderer_frame_program.py
python .	ools\c11d\d9	est_d_renderer_logical_composition.py
python .	ools\c11d\d9	est_d_renderer_candidate.py
python .	ools\c11d\d9	est_editorial_render_bridge.py
python .	ools\c11d\d9	est_cross_suite_lifecycle.py
python .	ools\c11daseline_candidate	est_d_baseline_candidate.py
python -u .\c11c-suite\self_test.py
```

The new focused test remains separate from the 22-step aggregate. If `jsonschema` is absent, built-in structural/exact-contract checks still run, but the output accurately reports the optional library as unavailable. Do not claim library-backed JSON Schema validation in that environment.

## Mandatory governance state

- C11-C 2.19.12 and `release/C11C_FREEZE_PACKAGE_MANIFEST.json` remain immutable; manifest SHA-256 stays `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
- D9.10 remains `PREPARE_ONLY`.
- Renderer OFF; media false; `D4.8=BLOCKED`; `release_authority=NONE`.
- D9 remains OPEN. D9.14/D9.16 are blocked as required; D9.17 is `BLOCKED_NO_GO`; D10 remains BLOCKED.
- This checkpoint does not approve the timing topology, freeze the renderer baseline, or grant production authority.

## Next design increment

After Windows acceptance, create a separate *request-bound timeline instance* design that consumes upstream canonical durations, FPS and frame counts, verifies source lineage and does not mutate C11-C. It remains in-memory and non-dispatchable until independent renderer-baseline approval and explicit D4.8 authorization.
