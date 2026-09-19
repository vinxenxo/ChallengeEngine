# CHECKPOINT_0.3.6_STATUS.md

## Current Status

**Checkpoint:** 0.3.6 — Composition Root Integration

**State:** OPEN / NEXT IMPLEMENTATION PHASE

**Code baseline supplied:** CHECKPOINT 0.3.5

The code in this package is the source of truth for the current implementation state. This document records the engineering state that the next context must verify before modifying code.

---

## Frozen Checkpoints

| Checkpoint | State |
|---|---|
| 0 — V0.1 baseline | FROZEN / VALIDATED |
| 0.1 — Stateless RNG | FROZEN / VALIDATED |
| 0.2.1 — Semantic streams + DI | FROZEN / VALIDATED |
| 0.2.2 — Pilot + CHALLENGE_003 | FROZEN / VALIDATED |
| 0.2.2-R1 — DDI hardening / bubbling cleanup | FROZEN / VALIDATED |
| 0.3.1 — Parking V2 mathematical contract | FROZEN |
| 0.3.2 — Production stream registry | FROZEN / VALIDATED |
| 0.3.3 — Semantic index contract | FROZEN |
| 0.3.4 — CHALLENGE_004 | FROZEN |
| 0.3.5 — ParkingMechanicV2 + isolation suite | FROZEN / ISOLATION VALIDATED |
| **0.3.6 — Global integration** | **OPEN** |

---

## Actual Implementation State

### DeterministicLCG

Implemented as stateless sampling with O(log N) affine LCG advancement.

Frozen compatibility rule:

```text
stream_id = 0
```

preserves the historical legacy sequence.

### RNG infrastructure

Implemented and validated:

- `RNGStreamRegistry`
- `RNGStreamDefinition`
- `StructuralRNG`
- `CosmeticRNG`
- `MechanicRNGContext`
- `PresentationRNGContext`

Lower layers use error state bubbling instead of `push_error()` for expected contract violations. The Composition Root owns structured process-level error reporting.

### PilotMechanic

Implemented, V2.0, `CHALLENGE_003`, isolated and validated.

### ParkingMechanic V1

Frozen legacy oracle. Do not modify during this phase.

### ParkingMechanicV2

Implemented at:

```text
mechanics/parking/ParkingMechanicV2.gd
```

Uses capability streams:

```text
30 PARKING_DODGE_OFFSET
40 PARKING_SAVE_OFFSET
50 PARKING_OVERSHOOT
60 PARKING_STEERING_NOISE
```

Isolation suite:

```text
tests/ParkingMechanicV2IsolationTest.gd
```

Validated with:

```text
[PARKING_V2_ISOLATION_SUITE] PASS
```

### MechanicRegistry

Current real code resolves:

```text
key    -> KeyMechanic
parking -> ParkingMechanic
pilot  -> PilotMechanic
```

`parking_v2` is **not yet registered**.

### GeneradorMaestro

Already owns the RNG infrastructure and has factory methods for V2 contexts.

Current V2 execution branch is still Pilot-specific:

```text
rng_version == 2.0
AND mechanic_id == pilot
```

It does not yet inject the Parking V2 capability.

---

## Immediate Engineering Objective

Integrate `ParkingMechanicV2` into the global pipeline without modifying frozen legacy behavior.

Required changes:

1. Register `parking_v2` in `MechanicRegistry`.
2. In `GeneradorMaestro`, create a `MechanicRNGContext` for each simulation attempt using:
   - `consumer_id = "ParkingMechanic"`
   - streams `[30, 40, 50, 60]`.
3. Inject the context into the resolved `ParkingMechanicV2` instance.
4. Create the context again on every retry using the current retry seed.
5. Inspect `error_state` immediately after `simulate()` and reject the attempt before `WinningFrameDetector` / `ChallengeValidator` when RNG bubbling has occurred.
6. Preserve V1.0 telemetry and numerical baseline for `CHALLENGE_001` and `CHALLENGE_002`.
7. Add/verify V2.0 telemetry identity for `CHALLENGE_004`.

---

## Frozen Files During 0.3.6

Unless a test proves a contractual discrepancy, do not modify:

```text
core/deterministic/DeterministicLCG.gd
core/mechanics/KeyMechanic.gd
core/mechanics/ParkingMechanic.gd
core/mechanics/PilotMechanic.gd
mechanics/parking/ParkingMechanicV2.gd
core/deterministic/*RNG*.gd
challenges/CHALLENGE_001.json
challenges/CHALLENGE_002.json
challenges/CHALLENGE_003.json
WinningFrameDetector.gd
ChallengeValidator.gd
VideoTimeline.gd
```

The intended change surface is:

```text
core/mechanics/MechanicRegistry.gd
GeneradorMaestro.gd
tests/* integration coverage
```

---

## Certification Commands

Run before integration:

```powershell
godot --headless --path . --editor --quit

godot --headless --path . --script tests/DeterministicLCGStatelessTest.gd

godot --headless --path . --script tests/RNGArchitectureTest.gd

godot --headless --path . --script tests/PilotMechanicIsolationTest.gd

godot --headless --path . --script tests/PilotMechanicDDIHardeningTest.gd

godot --headless --path . --script tests/ParkingMechanicV2IsolationTest.gd
```

Then verify legacy fixtures:

```powershell
godot --headless --path . -- --config=challenges/CHALLENGE_001.json --validate-only
godot --headless --path . -- --config=challenges/CHALLENGE_002.json --validate-only
```

Only after these remain stable should `CHALLENGE_004` be exercised through the global pipeline.

---

## Frozen V1.0 Regression Values

### CHALLENGE_001

```text
attempts = 2
final_seed = 126048932
seed_used = 126048932
winning_frame_game = 342
winning_frame = 462
minimum_distance = 0.000230040647936747
score = 0.638380059088502
close_calls = 3
```

### CHALLENGE_002

```text
attempts = 1
final_seed = 987654
seed_used = 987654
winning_frame_game = 395
winning_frame = 515
minimum_distance = 3.38832068443298
score = 0.246091849120501
close_calls = 1
dodge_offset = -95.0478103361315
save_offset = 23.9687795163918
overshoot_dist = 67.4236544163076
```

A change to these results is a regression unless explicitly approved as a new versioned contract.
