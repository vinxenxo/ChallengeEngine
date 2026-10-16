# C11-D Visual Loop Matrix V2 — Seed Runtime Fix Checkpoint (2026-10-16)

**State:** `PYTHON_CONTRACT_TESTS_PENDING_OPERATOR_RUN; GODOT_RUNTIME_PENDING; PREPARATION_ONLY; RENDERER_OFF`.

## Failure evidence

The preceding Windows run passed its 12 Python unit tests and then Godot 4.7.1 rejected the probe input with `Seed matrix differs from the exact four pinned values`. The earlier grammar-matrix failure had already been passed, so the current rejection occurs at the seed-array comparison, not executable resolution.

## Root cause addressed

The old probe compared a JSON-decoded `Array` recursively to the typed `Array[int]` constant `SEEDS`. Godot may deserialize integral JSON numeric values as floats, so semantically identical values need scalar numeric checks rather than whole-array equality.

The fix requires an Array with exactly four elements; each element must be an integer or float, finite, and exactly numerically equal to the matching pinned seed in order. Strings, booleans, additional/missing values and changed/fractional values fail closed.

## File integrity

- Probe precondition: `7b4c35b9c87fdfdd41e89971077d3376a5a8df451f91f59083f85e3901a495c7`
- Probe after fix: `91bc179b9a6db2a8bbcde54e08f05b91d6dd47abc7d12c5904742df4cb5a70e7`
- Test precondition: `5f6eab104135d873f7e4242bbb415ff28309127f430f0061d51e840df955f625`
- Test after fix: `331834916e72e5dac71d9f74ea79c8a758f399da4a719a985da0515b74cd5471`
- Contract precondition: `e787b45843ff5c1642e9e1374d59869ef11fdc70620cfdda81606652aef5d17a`
- Contract after fix: `e2118dd2e25005913bfe418a001e24c20d0929a395171a172a6ac9c88e1d13a2`
- Frozen C11-C manifest remains pinned to `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`.

## Required verification

1. Apply only if all three replacement hashes match their preconditions and added targets are absent.
2. Run focused Python tests; expected count becomes 13.
3. Run the Godot 4.7.1 matrix audit and require exit code 0, `source_pins=12/12`, `seed_cases=20/20`, `deterministic_repeats=20/20`, the expected Godot version, and the explicit governance locks.
4. If runtime fails, report the actual failure; do not print a later success marker.

## Governance

`renderer=OFF`; `media_created=false`; `D4.8=BLOCKED`; `release_authority=NONE`; `baseline_approval=MISSING`; `freeze_eligible=false`; `D9.10=PREPARE_ONLY`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`. This overlay does not change any of them and does not authorize a first render.
