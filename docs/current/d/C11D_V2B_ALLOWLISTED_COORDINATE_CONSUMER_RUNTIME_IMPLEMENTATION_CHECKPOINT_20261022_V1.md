# C11-D V2-B Allowlisted Coordinate Consumer Runtime Implementation — Checkpoint V1

Date: 2026-10-22  
Status: `IMPLEMENTED_NOT_RUNTIME_ACCEPTED`

## Accepted predecessor evidence

The active Windows checkout reported the predecessor implementation-design suite `235/235`, stdout SHA-256 `0e8e75cbd7d749c758657bd20e8b39e9df31047decf71094350cb4ab3f94246d`, empty-stderr SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`, and receipt SHA-256 `9148ad3dfc21857d7decf5885a3fb0e10a839234ba7672040cfdfa86b57c7bd2`.

## Implemented here

A real GDScript `RefCounted` helper is added under `tools/c11d/d9/allowlisted_coordinate_consumer_review_only.gd`. Its only public entrypoint accepts the candidate ID, the exact `SimulationResult`, and the validation dictionary. It returns either a closed in-memory logical target-marker track or a two-key fail-closed error result. The runtime test harness is a headless `SceneTree` script and contains 241 negative cases plus 36 positive cases, for 277 total scenarios.

The helper has no production callers. The static test walks the active checkout's GDScript files and requires its only call site to be the new review-only test harness. It also checks the pinned core sources and SVG dimensions by static file inspection; the helper itself does not load assets.

## Contract reconciliation

The V1 design's count of 261 labelled negative cases over-counted six candidate/field relations whose field strings are actually shared by `CHALLENGE_005/006/007`, and counted 20 successful closed-output checks as negative cases. The new implementation contract corrects this openly. Runtime denominators are 241 negative, 36 positive, 277 total; the prior design record remains unchanged and is pinned as historical evidence.

The existing validation dictionary lacks a result-instance identity. The test adapter attaches a `WeakRef` for the source result and an expected frame count to that returned dictionary; no core simulation class is modified.

## Acceptance gate still pending

The real Godot 4.7.1 Mono runtime suite must execute in the operator's Windows checkout and exit successfully. The generated receipt is not evidence until that process has actually run. This checkpoint does not claim a Godot runtime PASS.

## Governance locks

- `renderer=OFF`
- `media_created=false`
- `payload_materialized=false`
- `candidate_input_admissible=false`
- `approved_bindings=0`
- `approved_custom_data_bindings=0`
- `approved_renderer_projection_bindings=0`
- `runtime_implementation_authorized_for_production=false`
- `render_test_authorized=false`
- `release_authority=NONE`
- Frozen C11-C manifest remains SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Next gate

Run the static guard and all 277 headless Godot cases in the active Windows checkout. On PASS, preserve source/test/log hashes and receipt, then conduct a separate implementation review. Production wiring and renderer activation remain later formal gates.
