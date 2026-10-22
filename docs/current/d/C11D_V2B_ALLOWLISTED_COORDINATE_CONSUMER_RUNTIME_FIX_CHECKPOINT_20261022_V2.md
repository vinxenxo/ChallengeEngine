# C11-D V2-B Allowlisted Coordinate Consumer Runtime Fix Checkpoint V2 — 2026-10-22

## State

- Previous runtime V1: **FAIL** on operator Windows; static suite 113/113 passed, but Godot exited 1.
- Failure: V1 module compares an arbitrary `Variant` (`float` / `Vector2`) directly with an object sentinel at the missing-key guard. Godot reported invalid equality operands in `allowlisted_coordinate_consumer_review_only.gd:152`.
- Fix: new `allowlisted_coordinate_consumer_review_only_v2.gd` guards `TYPE_OBJECT` first and compares only a `RefCounted` sentinel; unexpected objects fail closed as `INVALID_VALUE_TYPE`.
- The invalid-vector, no-partial-track, and constant-position cases in the V1 run cannot be credited as passing; they will be re-run on V2.
- V2 runtime acceptance: **PENDING** until the real Windows Godot run reports exit code 0, 241/241 negative, 36/36 positive, 277/277 total, and empty stderr.

## Immutable governance

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `release_authority=NONE`; approved bindings remain zero; no production call site; no renderer or render-test authorization. Frozen C11-C manifest SHA-256: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Next action

Apply only the ADD_ONLY V2 overlay, run V2 static checks, then launch the Godot 4.7.1 Mono runtime harness. Keep V1 source and logs as failure evidence. Do not proceed to production wiring until the corrected runtime receipt is reviewed.
