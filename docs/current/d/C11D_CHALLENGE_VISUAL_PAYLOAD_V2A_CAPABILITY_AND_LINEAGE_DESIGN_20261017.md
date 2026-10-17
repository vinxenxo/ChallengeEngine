# C11-D Challenge Visual Payload V2-A — Capability Matrix and Source-Lineage Contract

## Decision
V2-A is a **static capability inventory only**. It must establish the existing mechanic and asset routes before a generalized Godot materializer is designed. It does not claim that nine payloads are already supported.

## Canonical path
Challenge source JSON → existing canonical `ChallengeRuntimeBridge.run_effective_pipeline` → `SimulationResult.frames` (`FrameSnapshot`) → `ChallengePresentationBinder` and `ChallengeTimelineBuilder` → future D-owned in-memory semantic payload. Reuse these authorities; do not clone simulation math, the planner, frame generation, or timing logic. The current reviewed runtime harness is hard-scoped to `CHALLENGE_004` and is not an all-selector implementation.

## Mechanical visual state versus telemetry
Every selector has a `FrameSnapshot`, but mechanic-specific state is carried through varying `custom_data` maps. V2-A inventories those keys and binds none. The next design must define a per-mechanic allowlist and tests for visual semantics, specifically for second moving objects (`target_position` in hit/catch/find), target coordinate in pilot (`target_x`), selection emphasis (`active_selection`), and counted visual state (`displayed_count`). Metrics such as distances, velocity, steering/braking, random perturbation values, `target_count`, `winning_frame`, `close_calls`, scores and other telemetry must not be projected automatically.

## Selector-specific runtime gate
- `CHALLENGE_004 / parking_v2`: existing V1 in-memory preview provides a narrow reference implementation only. Preserve it as a regression fixture; do not silently change V1.
- Other eight selectors: source capability inventory only until runtime receipts show successful canonical invocation, semantic field mapping, resource resolution, complete source-frame coverage, deterministic repeat equality, gameplay-seed response and music-seed orthogonality.
- Assets are identified by source-bound semantic roles `BACKGROUND`, `TARGET`, `ANIMATED_OBJECT`; a `res://` path alone does not prove that each object's transformations or frame tracks are semantically correct.

## Timebase
The audit independently surfaces explicit `total_duration` conflicts only where a total was actually declared. `CHALLENGE_008` and `CHALLENGE_009`: declared total 11 seconds, phase components total 12 seconds. Keep these blocked/unresolved. The static inventory does not modify source JSON or invent a policy. Other challenges whose total is not explicitly declared stay `TOTAL_DURATION_NOT_DECLARED`; don't mistake that for timebase approval.

## Future V2 materializer minimums
1. Request/selector matrix with all nine challenge IDs, exact challenge/source hashes and registered mechanic class.
2. No duplicate planner/binder/simulation code; canonical planner and runtime bridge are called as authorities.
3. Per-mechanic allowlist of visible frame fields, including additional visual object tracks where required; no wholesale `custom_data`.
4. Explicit semantics for gameplay `request.seed` vs `request.music_seed`; music seed must not mutate gameplay visual payload. Do not add automatic seed generation or a master seed.
5. At least two independent repeats for each selector/seed variant; distinct payload identity for relevant gameplay-seed variants; identical repeated payload hashes; stable source pins.
6. Source timebase preserved at this stage. No delivery resampling, coordinate projection, editorial window binding, renderer-native input, rendering or media output.
7. Negative tests for missing source, unregistered mechanic, missing asset, unsupported field projection, timebase conflict, payload persistence, renderer activation and governance unlock.

## Acceptance envelope
Static PASS means only that the inventory and its source lineage are consistent. It is not payload acceptance, candidate-input admission, renderer acceptance, D9.17 closure, D10 promotion or a new baseline.
