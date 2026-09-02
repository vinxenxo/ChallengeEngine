# PILOT_MECHANIC_V2.0.md — CHALLENGE_003 Controlled DDI Fixture

## 0. Status

**Status:** FROZEN / VALIDATED

**Phase:** CHECKPOINT 0.2.2 — Pilot Mechanic / CHALLENGE_003

**Purpose:** Controlled laboratory fixture for empirically validating **Deterministic Dependency Isolation (DDI)** in RNG v2.0.

`PilotMechanic` is not a product mechanic and is not intended to model a game, physical system, or final content family. It exists solely to provide a minimal, auditable Simulation Core that can be subjected to structural and presentation mutations.

The fixture must remain intentionally simple. Additional physics, accumulated state, collision systems, Bézier trajectories, visual logic, or presentation dependencies are out of scope for this phase.

---

## 1. Objective

`CHALLENGE_003` demonstrates the following architectural property:

> A deterministic structural simulation must remain invariant under changes to presentation/cosmetic RNG consumption, while remaining responsive to deliberate changes in structural inputs or structural RNG streams.

The experiment therefore separates two classes of determinism:

```text
STRUCTURAL
    └── affects SimulationResult

PRESENTATION / COSMETIC
    └── must not affect SimulationResult
```

The fixture is valid only if this separation can be observed empirically through the test suite.

---

## 2. Version and Identity

| Property | Value |
|---|---|
| `challenge_id` | `CHALLENGE_003` |
| `mechanic` | `pilot` |
| `mechanic_version` | `2.0` |
| `rng_version` | `2.0` |
| Seed | `314159` |
| FPS | `60` |
| HOOK | `120` frames / `2.0 s` |
| GAME | `420` frames / `7.0 s` |
| CTA | `120` frames / `2.0 s` |
| TOTAL | Derivado del `video` del challenge; el fixture actual usa `720` frames / `12.0 s` |

The fixture uses the same temporal profile as the frozen baseline so that the new RNG architecture is exercised inside the real engine timeline without changing the temporal contract.

---

## 3. Capability Contract

`PilotMechanic` receives a `MechanicRNGContext` created by the Composition Root.

```text
consumer_id = "PilotMechanic"
rng_version = "2.0"
allowed_streams = [
    STREAM_TRAJECTORY (10),
    STREAM_CONTROL (20)
]
```

The mechanic has no access to:

- `CosmeticRNG`;
- `PresentationRNGContext`;
- `VideoTimeline`;
- `FamilyAssets`;
- visual nodes;
- presentation state;
- cosmetic streams.

The capability is the only RNG interface available to the mechanic.

---

## 4. Stream Contract

### 4.1 `STREAM_TRAJECTORY`

```text
ID: 10
Domain: STRUCTURAL_MAIN
Semantic name: TRAJECTORY
Index semantics: frame_number
Consumer: PilotMechanic
Version introduced: 2.0
```

Purpose: determine the deterministic trajectory perturbation for a frame.

### 4.2 `STREAM_CONTROL`

```text
ID: 20
Domain: STRUCTURAL_MAIN
Semantic name: CONTROL
Index semantics: frame_number
Consumer: PilotMechanic
Version introduced: 2.0
```

Purpose: determine the deterministic control perturbation for a frame.

### 4.3 Presentation stream used by tests

```text
ID: 1010
Domain: PRESENTATION
Semantic name: PARTICLES
Index semantics: entity_id
Consumer: PilotVisuals
Version introduced: 2.0
```

`STREAM_PARTICLES` is deliberately outside the `PilotMechanic` capability scope. It is used only by presentation-isolation tests.

---

## 5. Index Contract

In v2.0 the RNG `index` is a semantic coordinate, not a counter of previous calls.

For `PilotMechanic`:

```text
index = frame_number
```

Therefore, for any valid frame `f`:

```text
sample(seed, STREAM_TRAJECTORY, f)
```

and:

```text
sample(seed, STREAM_CONTROL, f)
```

must be independent of call order and independent of calls made to any other stream.

The same seed, RNG version, stream and index must always produce the same value under the same algorithm.

---

## 6. Mathematical Contract

For every game frame:

```text
f ∈ [0, game_frames - 1]
```

where `game_frames = 420`.

### 6.1 Normalized frame

```text
f_norm = f / (game_frames - 1)
```

### 6.2 Base trajectory

```text
base_x(f) = start_x + (end_x - start_x) * f_norm
```

### 6.3 Structural trajectory sample

Let:

```text
S_traj(f) = StructuralRNG.sample_float(
    seed,
    STREAM_TRAJECTORY,
    f
)
```

Then:

```text
trajectory_noise(f) =
    (S_traj(f) * 2.0 - 1.0) * trajectory_amplitude
```

### 6.4 Structural control sample

Let:

```text
S_ctrl(f) = StructuralRNG.sample_float(
    seed,
    STREAM_CONTROL,
    f
)
```

Then:

```text
control_offset(f) =
    (S_ctrl(f) * 2.0 - 1.0) * control_amplitude
```

### 6.5 Final position

```text
x(f) =
    base_x(f)
    + trajectory_noise(f)
    + control_offset(f)
```

The position is therefore a direct function of the frame and explicit structural samples. No position state is accumulated from `f-1`.

### 6.6 Target position

```text
target_x(f) = target_start + target_velocity * f
```

### 6.7 Success distance

```text
success_distance(f) = abs(x(f) - target_x(f))
```

### 6.8 Velocity metric

The first frame has no previous frame:

```text
velocity(0) = 0
```

For all subsequent frames:

```text
velocity(f) = abs(x(f) - x(f-1))
```

This is a metric only. It does not make the simulation stateful because the value is derived from deterministic frame outputs.

---

## 7. FrameSnapshot Contract

For each game frame the mechanic produces exactly one `FrameSnapshot`.

Required values:

```text
position     = Vector2(x(f), 0.0)
rotation     = 0
scale        = Vector2.ONE
opacity      = 1
```

Required semantic data:

```text
target_x
base_x
trajectory_noise
control_offset
success_distance
velocity
```

Exactly:

```text
game_frames = 420
```

snapshots must be produced.

Any frame-count deviation is a simulation contract violation and must prevent downstream validation from treating the result as valid.

---

## 8. SimulationResult Contract

`PilotMechanic` produces the frame array and metadata required by the existing core contracts.

`PilotMechanic` does **not** decide `winning_frame`.

The pipeline remains:

```text
PilotMechanic
    ↓
SimulationResult.frames
    ↓
WinningFrameDetector
    ↓
ChallengeValidator
```

This preserves the architectural separation between simulation and winner detection.

For the current fixture the validated end-to-end result is:

```text
winning_frame_game = 272
winning_frame      = 392
minimum_distance   = 0.00520862150247581
score              = 0.97863649811667
close_calls        = 1
valid              = true
```

---

## 9. CHALLENGE_003 Fixture Parameters

The current fixture is:

```text
seed = 314159

start_x = 0.0
end_x = 100.0
target_start = 0.0
target_velocity = 0.2386634844868735
trajectory_amplitude = 2.0
control_amplitude = 0.5
```

Difficulty tolerance:

```text
distance_px = 5.0
```

The fixture is intentionally deterministic and modest in numerical scale so that changes in structural output are easy to observe in tests.

---

# 10. DDI Hypotheses

The following hypotheses form the formal laboratory specification.

## H1 — Cosmetic RNG Isolation

**Claim:** consumption of cosmetic/presentation RNG must not modify the structural simulation.

Formal expectation:

```text
Simulation(seed, config)
==
Simulation(seed, config)
```

after arbitrary additional calls to `CosmeticRNG`.

Observable invariants include:

- frame count;
- every frame position;
- every frame metric;
- `winning_frame`;
- `minimum_distance`;
- `score`.

---

## H2 — Execution-Layer Isolation

**Claim:** presentation execution order is not a dependency of structural simulation.

Presentation activity is performed independently of the structural simulation and must not feed data back into `PilotMechanic`.

The current laboratory test exercises this by executing presentation RNG work separately and in different call order before re-running the structural simulation.

This phase does **not** claim to model a complete Godot node-tree reorder. It verifies the stronger prerequisite: presentation RNG consumption has no execution-order dependency on the structural result.

A future presentation-specific suite may extend H2 to explicit node/component reordering.

---

## I — Semantic Index / Reordering Independence

**Claim:** changing the order in which samples are requested does not change the value associated with any semantic coordinate.

The relevant invariant is:

```text
sample(seed, stream, index = f)
```

is independent of whether another valid index was requested before or after it.

The current laboratory covers this property through presentation calls performed in ascending and descending index order.

This is an RNG-coordinate guarantee, not a statement about Godot node scheduling itself.

---

## J — Additive Cosmetic Mutation

**Claim:** adding substantial new cosmetic RNG consumption must not alter structural output.

The current test injects:

```text
500 cosmetic samples
```

and additionally exercises the same presentation stream in reverse index order.

Expected invariants:

```text
winning_frame       unchanged
minimum_distance    unchanged
score               unchanged
```

The structural RNG streams are not called by this mutation.

---

## K — Capability Intersection / Boundary Enforcement

**Claim:** a consumer may use only the intersection of:

```text
Local capability scope
AND
Registry authorization
```

A request is valid only when both conditions hold.

The architecture suite verifies rejection for:

- stream outside the local capability scope;
- consumer not authorized by the Registry;
- structural facade receiving a presentation stream;
- cosmetic facade receiving a structural stream;
- unregistered stream IDs;
- invalid semantic index.

K is therefore an infrastructure property and is tested separately from the Pilot simulation.

---

# 11. Test Mapping P / Q

## P — Cosmetic / Presentation Invariance

`PilotMechanicIsolationTest.gd` performs the following sequence:

```text
1. Create Pilot structural context.
2. Simulate CHALLENGE_003 → SimulationResult_A.
3. Consume 500 PARTICLES samples in ascending order.
4. Consume 500 PARTICLES samples in descending order.
5. Create a fresh Pilot structural context.
6. Re-simulate CHALLENGE_003 → SimulationResult_B.
7. Compare A and B.
```

The comparison includes:

- frame count;
- `winning_frame`;
- `minimum_distance`;
- `score`;
- `position`;
- `rotation`;
- `scale`;
- `opacity`;
- `success_distance`;
- `velocity`;
- `target_x`;
- `base_x`;
- `trajectory_noise`;
- `control_offset`.

Acceptance criterion:

```text
SimulationResult_A == SimulationResult_B
```

with exact comparisons for the current deterministic test environment.

### P coverage mapping

```text
H1 → directly exercised
H2 → exercised as independent presentation execution
I  → exercised through presentation index reordering
J  → directly exercised by 500 additive samples
```

P is therefore the principal combined integration test for H1/H2/I/J.

---

## Q — Structural Reactivity

`PilotMechanicIsolationTest.gd` performs two complementary mutations.

### Q1 — Cosmetic mutation

The test performs 500 calls to `STREAM_PARTICLES` and verifies that:

```text
winning_frame
minimum_distance
```

remain unchanged.

### Q2 — Structural mutation

The test changes:

```text
trajectory_amplitude
2.0 → 10.0
```

and re-runs the structural simulation.

Acceptance criterion:

```text
winning_frame != baseline.winning_frame
OR
minimum_distance != baseline.minimum_distance
```

The observed validated result is:

```text
baseline:
    winning_frame = 272
    minimum_distance ≈ 0.00520862150248

structural variant:
    winning_frame = 143
    minimum_distance ≈ 0.00475324434449
```

Therefore Q demonstrates the intended directional relationship:

```text
STRUCTURAL mutation
    → observable SimulationResult mutation

COSMETIC mutation
    → no observable SimulationResult mutation
```

---

# 12. Validation Matrix

| ID | Property | Fixture / Test | Expected Result | Current Status |
|---|---|---|---|---|
| H1 | Cosmetic RNG cannot alter structural result | P | `SimulationResult_A == SimulationResult_B` | **PASS** |
| H2 | Presentation execution is isolated | P | Structural result unchanged | **PASS — scoped** |
| I | Semantic index is order-independent | P / RNG architecture suite | Same `(seed, stream, index)` → same value | **PASS — scoped** |
| J | Additive cosmetic consumption is harmless | P / Q1 | `winning_frame`, distance and score unchanged | **PASS** |
| K | Capability intersection is enforced | RNG Architecture K/L | Unauthorized requests rejected | **PASS** |
| P | Integrated presentation/cosmetic isolation | `PilotMechanicIsolationTest.gd` | Exact SimulationResult equality | **PASS** |
| Q | Structural inputs remain reactive | `PilotMechanicIsolationTest.gd` | Structural mutation changes output | **PASS** |

### Scope qualification

The current laboratory fully demonstrates the intended DDI property for the tested streams and execution patterns. H2 and I are deliberately scoped to the presentation RNG execution patterns implemented in the current suite; they should not yet be interpreted as a complete proof of arbitrary Godot scene-tree scheduling independence.

---

# 13. Validated Reference Run

Godot:

```text
4.7.1.stable.mono.official.a13da4feb
```

Validated `CHALLENGE_003` result:

```text
attempts = 1
seed_used = 314159
rng_version = 2.0

game_frames = 420
hook_frames = 120
cta_frames = 120
total_frames = 660

winning_frame_game = 272
winning_frame = 392

minimum_distance = 0.00520862150247581
score = 0.97863649811667
close_calls = 1

valid_window = [120, 540)
winning_frame_in_valid_window = true
```

A repeated headless execution produced the same result.

---

# 14. Frozen Rules

The following rules are frozen for CHECKPOINT 0.2.2:

1. `PilotMechanic` is a laboratory fixture, not a product mechanic.
2. `CHALLENGE_003` uses `rng_version = "2.0"`.
3. `PilotMechanic` may access only `MechanicRNGContext`.
4. `STREAM_TRAJECTORY` and `STREAM_CONTROL` are structural.
5. `STREAM_PARTICLES` is presentation-only for this fixture.
6. `index = frame_number` for structural Pilot streams.
7. The simulation is a direct per-frame function; no accumulated position state is used.
8. `PilotMechanic` does not determine `winning_frame`.
9. Presentation/cosmetic activity must not modify structural output.
10. Structural mutation must remain observable.
11. `CHALLENGE_001` and `CHALLENGE_002` remain permanently on `rng_version = "1.0"`.
12. No future production mechanic should be added to the Pilot fixture merely to increase its complexity.

---

# 15. Known Testing Debt

The architecture suite intentionally triggers contract violations using `push_error()` so that the rejection path is observable.

This causes expected `ERROR:` lines to appear in the Godot console even when the suite finishes with `PASS`.

This is a **testing-infrastructure debt item**, not a failure of the Pilot or RNG architecture.

Future CI/CD work should separate:

```text
expected contract rejection
```

from:

```text
unexpected engine/test error
```

using structured error results or an injected/mock logger.

This debt must not change the frozen structural contracts or the numerical behavior of `CHALLENGE_003`.

---

# 16. Exit Criteria for the Pilot Phase

CHECKPOINT 0.2.2 is considered complete when all of the following remain true:

```text
RNGArchitectureTest                PASS
PilotMechanicIsolationTest         PASS
CHALLENGE_003 headless validation  PASS
CHALLENGE_001 regression           PASS
CHALLENGE_002 regression           PASS
No unexpected SCRIPT ERROR         PASS
```

The validated implementation satisfies these criteria in Godot 4.7.1.

---

## 17. Relationship to Future Mechanics

`PilotMechanic` establishes the architectural pattern for future V2.0 mechanics:

```text
ChallengeDefinition
        ↓
MechanicRNGContext
        ↓
Structural Simulation
        ↓
SimulationResult
        ↓
Winner Detection
        ↓
Presentation
        ↓
CosmeticRNG
```

Future mechanics may introduce more structural streams, richer mathematical models, or new semantic indices, but they must preserve the DDI rule demonstrated here:

> **Presentation may evolve independently; structural determinism may not silently depend on presentation consumption.**

---

## Current Live Status — CHECKPOINT 0.9.0

`pilot` remains a frozen RNG/DDI laboratory fixture. It is not a new mathematical family and is not being extended for 1.0.0. Its role is regression coverage for stateless semantic-stream isolation.
