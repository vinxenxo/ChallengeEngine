# C11-D V2-B Allowlisted Coordinate Consumer — Isolated Runtime Implementation Overlay V1

**Operation mode:** `ADD_ONLY`  
**Implementation state:** `IMPLEMENTED_NOT_RUNTIME_ACCEPTED`  
**Runtime test state before operator execution:** `NOT_YET_EXECUTED_IN_OPERATOR_WINDOWS_CHECKOUT`  
**Renderer:** `OFF`

## What this increment adds

This overlay adds an isolated `RefCounted` GDScript consumer, a headless Godot runtime test harness, a read-only Python static/call-graph guard, the runtime contract and schema, and updated handover/checkpoint files. The consumer is placed under `tools/c11d/d9/` and has no production caller. It creates no SceneTree nodes or render resources and returns only in-memory logical target-marker descriptors.

The helper reads one allowlisted key from `FrameSnapshot.custom_data` per source frame using one `Dictionary.get(key, unique_missing_sentinel)` call. It does not enumerate, index, copy, or serialize `custom_data`. It returns no partial track on failure. It does not invoke `CoordinateMapper`; the accepted coordinate policy is expressed directly as the already reviewed logical transforms.

## Exact accepted allowlist

- `CHALLENGE_003.target_x`
- `CHALLENGE_005.target_position`
- `CHALLENGE_006.target_position`
- `CHALLENGE_007.target_position`

`CHALLENGE_008.active_selection` and `CHALLENGE_009.displayed_count` remain blocked. There is no field argument on the public helper entrypoint.

## Matrix reconciliation (do not misreport the denominator)

The previously accepted design described 261 planned cases as negative cases. Before implementation, the runtime contract corrects three representational issues rather than reporting impossible negative tests as PASS:

1. Of the 12 candidate-to-other-candidate field relations, only six are actual field-name mismatches. The other six are valid because `CHALLENGE_005`, `CHALLENGE_006`, and `CHALLENGE_007` all use the same field string `target_position`.
2. The 20 closed-output mutation checks are successful calls whose output must remain closed and leak-free; they are positive assertions, not failure-return tests.
3. A GDScript `Vector2` has numeric components and cannot retain a boolean component. The runtime matrix supplies a dictionary with a boolean `x` value as the representable adversarial surrogate and expects strict type rejection.

The corrected runtime suite contains **241 negative cases and 36 positive cases (277 total)**. The six shared-field relations are tested as positive map relations; the six true wrong-field relations are negative. No case is claimed executed until the Godot test runner returns exit code zero in the operator's Windows checkout.

## Validation provenance

The existing `SimulationResult.validate_contract(expected_game_frames)` return dictionary does not include the source result identity. This overlay does not modify `SimulationResult.gd` or `FrameSnapshot.gd`. The isolated review-only test adapter attaches a `WeakRef` to the exact `SimulationResult` and the expected frame count to that same validation dictionary. The consumer rejects missing or mismatched provenance. This mechanism is review/test scope only and does not authorize a production adapter.

## Run order

1. Apply the ZIP using the supplied ADD_ONLY PowerShell block.
2. Run the separate test block: Python static/source-pin/call-graph guard first, then Godot 4.7.1 Mono headlessly.
3. Preserve the stdout/stderr hashes and generated receipt.
4. Review any runtime failures before the next change. Do not add production wiring, bindings, payload materialization or renderer calls under this overlay.

## Governance

The GDScript helper is real executable review-only code; it is **not** production-wired or production-authorized. `renderer=OFF`, `media_created=false`, `payload_materialized=false`, `candidate_input_admissible=false`, `release_authority=NONE`, and approved bindings remain zero. No challenge JSON, `CoordinateMapper.gd`, `SimulationResult.gd`, `FrameSnapshot.gd`, or frozen C11-C file is modified. The C11-C manifest must remain SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.
