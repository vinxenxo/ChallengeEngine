# C11-D Challenge Selector / Seed Planner Preflight V2

## Objective

Prove that each of the nine canonical Challenge variants resolves through the current D9.9 universal planner under three explicit seed combinations and repeat calls, before attempting downstream Challenge visual-payload materialization.

## Canonical results established by source inspection

The D9.9 planner resolves these selection pairs:

| Challenge | canonical family/mechanic |
|---|---|
| `CHALLENGE_001` | `key` |
| `CHALLENGE_002` | `parking` |
| `CHALLENGE_003` | `pilot` |
| `CHALLENGE_004` | `parking_v2` |
| `CHALLENGE_005` | `hit_v1` |
| `CHALLENGE_006` | `catch_v1` |
| `CHALLENGE_007` | `find_v1` |
| `CHALLENGE_008` | `choose_v1` |
| `CHALLENGE_009` | `count_v1` |

The 9×3×2 request-plan matrix is a preparation gate; it checks request/plan digest sensitivity, repeat stability, editorial digest invariance and D4 GUI/CLI parity. It does not call Godot or claim payload correctness.

## Why the current dynamic request payload path cannot simply be broadened

The V1 binder's `EXPECTED_SELECTIONS["challenges"]` is fixed to `parking_v2 / CHALLENGE_004`. The Godot harness validates the same fixed selector, reads `res://challenges/CHALLENGE_004.json`, pins only that source digest, requires the `parking_v2` mechanic, uses a fixed challenge asset list, and hard-checks 420 simulation frames plus a 900-frame timeline. This contract must not be bypassed or changed in-place without a full dependency-pin migration and full regression recapture.

The nine JSON definitions are heterogeneous in schema and mechanics; they are not interchangeable variants of the `parking_v2` implementation. A future Challenge V2 materializer needs per-Challenge source identity, runtime frame evidence, asset selection/allowlist, canonical profile binding, seed sensitivity and timebase evidence while continuing to reuse the canonical universal planner and D9.10 bridge/adapter.

## Source-timebase inconsistency

`CHALLENGE_008` and `CHALLENGE_009` declare `total_duration=11`, but their named segments total 12 seconds. The preflight reports the conflict and leaves the timebase unapproved. The shared temporal-policy gate must decide authoritative duration semantics before those payloads can be accepted.

## Exit criteria for this preflight

- 9/9 selector identities matched to canonical catalog and definition hashes.
- 27/27 seed-variant plans accepted; 54 repeated planner calls deterministic.
- Gameplay seed and music seed alter request/plan identities for 9/9 variants; editorial identity stays invariant.
- Five negative selector/seed cases fail closed.
- `godot_invocations=0`, `payload_materialized=false`, `candidate_input_admissible=false`.

The next engineering work must be a separate Challenge V2 payload contract/harness plan. No renderer input or release approval follows from planner readiness.
