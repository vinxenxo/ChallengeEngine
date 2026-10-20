# C11-D Challenge Visual Payload — Source Semantic Review V1 (2026-10-20)

## Scope and decision

This record performs the source-semantic review that must precede the V2-B runtime harness design. The review is based on the designated baseline ZIP `ChallengeEngineV01_STATELESS_NIGHTLY_20261710_1555.zip` (SHA-256 `aced079f3f553d81121e84940e6a7d9f2be4c278912b94abee75f277b8f32df2`), whose 81 V2-C source pins match the source pin list. The operator's active Windows checkout separately reported `81/81` source pins before and after the V2-C runtime, so the inspected source lineage is reconciled to that run's pins. This environment did not directly mount the Windows checkout.

**Decision:** review is complete, but **0/9 bindings are approved** and **0/6 `custom_data` candidate rows are approved**. This artifact does not modify the binding proposal contract, challenge JSON, mechanics, or any V1 harness. It does not design or implement V2-B yet.

## V2-C runtime result recorded

Operator-confirmed `PASS_SOURCE_FRAME_ROUTE_ONLY`; Godot `4.7.1.stable.mono.official.a13da4feb`; selector coverage 9/9; canonical planner calls 9/9; independent runtime processes 18/18; source pins 81/81 before and after. Report SHA-256 `35e5985f47055fc11cbc0fcd7317f4d0a4ebe6bfe4d8bb22bdab67b7bcbe56a7`; runner stdout SHA-256 `f90846bfddeb4cccf064b1bf1b4332a36e08173f0e3a9d412c66466d361d95f6`; runner stderr SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Contract SHA-256 `6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c`. The evidence is recorded from operator-pasted Windows output, not claimed as an independently reopened report file in this environment.

This proves source-frame/route acceptance only. It does not prove final visual-payload determinism, gameplay-seed visual sensitivity, music-seed orthogonality, candidate-input admission, renderer enablement, or D10 closure.

## Review matrix — nine proposed bindings

| Selector | Proposed binding | Source decision | Essential semantic constraint |
|---|---|---|---|
| `CHALLENGE_001` | `presentation.static_target_position` → `TARGET` | Reviewed; not approved — duplicated target authority | Challenge declares `[540,960]`, but `KeyMechanic.setup()` does not consume the presentation property; the mechanic uses its default `target_position=[540,960]`. Matching current values are not proof of shared authority. |
| `CHALLENGE_002` | `difficulty.parking.target_position` → `TARGET` | Blocked — coordinate space undeclared | `ParkingMechanic` reads `[850,960]` as a `Vector2`; `presentation.coordinate_space` is absent. Do not infer the coordinate system. |
| `CHALLENGE_003` | `custom_data.target_x` → `TARGET` | Reviewed; scalar candidate only | `float`, frame-indexed, `PILOT_0X100`; no Y coordinate. `target_x = target_start + target_velocity*f`; do not derive a 2D vector or use this field alone as seed-sensitivity evidence. |
| `CHALLENGE_004` | `difficulty.parking.target_position` → `TARGET` | Reviewed; not approved — V1 regression only | Static `Vector2` in `CANVAS_1080X1920`, consumed by `ParkingMechanicV2`. Keep the existing V1 harness byte-for-byte unchanged. |
| `CHALLENGE_005` | `custom_data.target_position` → `TARGET` | Reviewed; per-run constant vector candidate | `HitMechanic` computes `_target_prime` from RNG-stream offsets in setup, then repeats that same vector on every frame. It is not a moving per-frame target. |
| `CHALLENGE_006` | `custom_data.target_position` → `TARGET` | Reviewed; per-frame vector candidate | `CatchMechanic` writes `p_t`; primary `snapshot.position` is `p_c`. Keep target and catcher tracks separate. |
| `CHALLENGE_007` | `custom_data.target_position` → `TARGET` | Reviewed; per-frame vector candidate | `FindMechanic.calculate_frame()` yields `p_target` separately from scanner `p_scan`. Do not project distractor topology or scoring telemetry. |
| `CHALLENGE_008` | `custom_data.active_selection` → selection state | Blocked — source-frame only due timebase conflict | `int` option index; the same index chooses `options_positions[index]`. Declared total is 11 s but phase sum is 12 s. No timeline/phase acceptance. |
| `CHALLENGE_009` | `custom_data.displayed_count` → count state | Blocked — source-frame only due timebase conflict | `int`; current primary X position is derived from this value. Declared total is 11 s but phase sum is 12 s. Do not substitute hidden `target_count`. |

The exact typed source findings, paths, hashes, fail-closed behavior, seed expectations and remaining gates are held in `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_SOURCE_SEMANTIC_REVIEW_V1.json`. All nine rows retain `binding_authorized=false` and `renderer_projection_approved=false`.

## Six `custom_data` candidate rows

1. `CHALLENGE_003.target_x`: scalar float, no inferred Y.
2. `CHALLENGE_005.target_position`: seed-derived per-run constant `Vector2`, replicated on frames.
3. `CHALLENGE_006.target_position`: per-frame moving target `Vector2`, separate from catcher.
4. `CHALLENGE_007.target_position`: per-frame target `Vector2`, separate from scanner.
5. `CHALLENGE_008.active_selection`: integer option index, timebase conflict still blocking timeline acceptance.
6. `CHALLENGE_009.displayed_count`: integer count value, redundant with primary positional encoding, timebase conflict still blocking timeline acceptance.

All six remain candidates only. No unlisted field is approved. Never serialize the entire `FrameSnapshot.custom_data` map.

## Base snapshot fields

`position: Vector2`, `rotation: float`, `scale: Vector2`, `opacity: float`, `texture_index: int`, and `variant_id: int` are inventoried as existing `FrameSnapshot` fields, not renderer-approved fields. Coordinate authority, angle units, scale mapping and texture/variant semantics must remain explicit in any later projection.

## Shared temporal conflict — unchanged

Both `CHALLENGE_008` and `CHALLENGE_009` declare 11 seconds while phase durations sum to 12 seconds (3+7+0+2). Neither challenge JSON is edited; no precedence is inferred. V2-C receipts remain explicitly source-frame-only for both selectors.

## Focused verification bundled here

The new Python source-review test is designed to run against the active checkout and checks 34 assertions including all 81 source pins, nine proposal rows, six candidate rows, schema/invariants, real source excerpts, the dual-form `ChallengeRuntimeBridge` video binding, and unchanged governance locks. Its PASS is pending operator execution after applying this add-only overlay. This artifact is generated, not installed, until the guarded application block succeeds.

## Next gate: V2-B design — after this review is installed and green

Design V2-B as a separate increment only after this contract is applied add-only and its 34/34 tests pass on the active Windows checkout. V2-B must prove a source-grounded safe visual projection, deterministic independent-process repeats, actual projected-state gameplay-seed sensitivity where a mechanic genuinely consumes the seed, music-seed orthogonality at the separate canonical request boundary, editorial invariance, source lineage and fail-closed negative cases. It must not write production payload files/media, emit renderer-native input, approve bindings by implication, modify challenge JSON or expand the V1 `CHALLENGE_004` scope.

## Governance locks preserved

`renderer=OFF`; `media_created=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`; `approved_bindings=0`; `visual_seed_sensitivity=NOT_TESTED`.
