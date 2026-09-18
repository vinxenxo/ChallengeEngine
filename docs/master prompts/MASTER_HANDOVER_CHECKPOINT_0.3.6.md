# CHECKPOINT 0.3.6 — MASTER HANDOVER PROMPT

======================================================================
PROJECT
======================================================================

ChallengeEngineV01

PACKAGE STATE:

CHECKPOINT 0.3.5 — PARKING V2 ISOLATION VALIDATED
NEXT PHASE:

CHECKPOINT 0.3.6 — COMPOSITION ROOT INTEGRATION

PURPOSE OF THIS HANDOVER:

Transfer the current real project state to a new conversation without losing:

- the frozen V0.1 baseline;
- the stateless RNG contract;
- semantic stream governance;
- capability/DI boundaries;
- PilotMechanic laboratory evidence;
- Parking V2 mathematical contract;
- CHALLENGE_004 fixture;
- exact current integration gap;
- regression values;
- test evidence;
- next engineering objective.

======================================================================
0. NON-NEGOTIABLE WORKING RULE
======================================================================

The uploaded/project ZIP is the source of truth for CODE.

The `docs/*.md` files are the source of truth for DOCUMENTED CONTRACTS.

This handover is the source of truth for CONTEXT CONTINUITY.

If any of these disagree:

1. DO NOT silently fix anything.
2. Identify the discrepancy.
3. Inspect the actual code.
4. Compare against the relevant frozen checkpoint.
5. Decide explicitly which artifact is authoritative for that point.

During the initial audit:

NO CODE MODIFICATION.
NO ARCHITECTURAL IMPROVEMENT BY INITIATIVE.
NO REWRITING OF FROZEN CONTRACTS.
NO MIGRATION OF LEGACY FIXTURES.

First audit → verify → design → implement → test → freeze.

======================================================================
1. PRODUCT PHILOSOPHY
======================================================================

This project is NOT a conventional video game.

It is a factory for automatically generating VIDEO PAUSE CHALLENGES.

A generated video contains a precisely determined winning frame. The viewer attempts to pause the video on that frame.

The engine simulates the mathematical situation; the presentation renders it.

Principle:

"The engine generates Pause Challenges, not ports of retro games."

Visual themes are content only:

- retro_8bit_arcade
- cyberpunk
- garage
- sports
- fantasy
- scifi
- etc.

Themes do NOT create new mathematical families.

======================================================================
2. CORE ENGINE PRIORITIES
======================================================================

1. Mathematical determinism.
2. Logical reproducibility.
3. Explicit contracts.
4. Mathematical validation.
5. Traceability.
6. Frame integrity.
7. CLI automation.
8. Rendering.
9. Presentation.
10. Marketing/distribution.

Rule:

GODOT CALCULATES.
PYTHON ORCHESTRATES.
FFMPEG PACKAGES.

======================================================================
3. FOUR-LAYER ARCHITECTURE
======================================================================

CAPA 0 — DECLARATIVE CHALLENGE DEFINITION

Input: `challenges/*.json`

Contains challenge identity, versions, seed, difficulty, video configuration, assets/content metadata.

No algorithmic logic, absolute paths, or social-platform API knowledge.

CAPA 1 — DETERMINISTIC SIMULATION CORE

Mechanics, deterministic RNG, FrameSnapshot, SimulationResult, detector and validators.

CPU/memory simulation. No visual nodes for mechanical calculation.

CAPA 2 — PRESENTATION

VideoTimeline, FamilyAssets, main scene, passive consumption of SimulationResult, Movie Maker.

Must not recalculate the simulation.

CAPA 3 — PRODUCTION ORCHESTRATION

Python launches Godot, captures telemetry/errors, runs FFmpeg and creates manifests.

Python does not calculate winning_frame and does not simulate mechanics.

======================================================================
4. FROZEN CHECKPOINT HISTORY
======================================================================

CHECKPOINT 0
Baseline V0.1
FROZEN / VALIDATED

CHECKPOINT 0.1
Stateful → Stateless RNG
FROZEN / VALIDATED

CHECKPOINT 0.2.1
Semantic Streams + DI Infrastructure
FROZEN / VALIDATED

CHECKPOINT 0.2.2
PilotMechanic + CHALLENGE_003
FROZEN / VALIDATED

CHECKPOINT 0.2.2-R1
DDI Coverage Hardening + Error Bubbling Cleanup
FROZEN / VALIDATED

CHECKPOINT 0.3.1
Parking V2 Mathematical Contract
FROZEN

CHECKPOINT 0.3.2
Production RNG Stream Registry
FROZEN / VALIDATED

CHECKPOINT 0.3.3
Semantic Index Contract
FROZEN

CHECKPOINT 0.3.4
CHALLENGE_004
FROZEN

CHECKPOINT 0.3.5
ParkingMechanicV2 + Isolation Suite
FROZEN / ISOLATION VALIDATED

CHECKPOINT 0.3.6
Composition Root Integration
OPEN — CURRENT WORK

======================================================================
5. ACTUAL PROJECT TREE AT HANDOVER
======================================================================

ChallengeEngineV01_STATELESS/

├── GeneradorMaestro.gd
├── build_factory.py
├── Main.tscn
├── project.godot
├── README_INTEGRATION.md
├── README_PROJECT_ES.md
├── MASTER_HANDOVER_CHECKPOINT_0.3.6.md
├── assets/
├── challenges/
│   ├── CHALLENGE_001.json
│   ├── CHALLENGE_002.json
│   ├── CHALLENGE_003.json
│   └── CHALLENGE_004.json
├── core/
│   ├── data/
│   ├── deterministic/
│   │   ├── DeterministicLCG.gd
│   │   ├── RNGStreamDefinition.gd
│   │   ├── RNGStreamRegistry.gd
│   │   ├── StructuralRNG.gd
│   │   ├── CosmeticRNG.gd
│   │   ├── MechanicRNGContext.gd
│   │   └── PresentationRNGContext.gd
│   ├── mechanics/
│   │   ├── ChallengeMechanic.gd
│   │   ├── KeyMechanic.gd
│   │   ├── ParkingMechanic.gd
│   │   ├── PilotMechanic.gd
│   │   └── MechanicRegistry.gd
│   ├── simulation/
│   ├── timeline/
│   └── validation/
├── mechanics/
│   └── parking/
│       └── ParkingMechanicV2.gd
├── tests/
│   ├── DeterministicLCGStatelessTest.gd
│   ├── RNGArchitectureTest.gd
│   ├── PilotMechanicIsolationTest.gd
│   ├── PilotMechanicDDIHardeningTest.gd
│   └── ParkingMechanicV2IsolationTest.gd
├── docs/
└── src/.continue/rules/

`.git/` and `.godot/` are NOT part of the transfer ZIP.
`src/.continue/rules/` is intentionally preserved for VS Code/Continue configuration and is not part of the engine architecture.

======================================================================
6. DETERMINISTIC RNG — FROZEN CONTRACT
======================================================================

`core/deterministic/DeterministicLCG.gd`

31-bit LCG:

MASK_31 = 0x7fffffff
MULTIPLIER = 1103515245
INCREMENT = 12345
NORMALIZER = 2147483647.0

The implementation is STATELESS.

Public API:

sample_integer(seed, stream_id, index)
sample_float(seed, stream_id, index)
sample_float_range(seed, stream_id, index, min, max)

`index = 0` is exactly the first `nexti()`-equivalent transition for the supplied stream seed.

`stream_id = 0` preserves the historical sequence.

Non-zero streams use deterministic stream-seed derivation and affine LCG jumping.

Do NOT reintroduce mutable generator state.
Do NOT use custom methods named `randf`, `randf_range`, `randi`, `randi_range`, `seed`, or similar Godot built-in/global names.

======================================================================
7. RNG DOMAINS AND CURRENT STREAM REGISTRY
======================================================================

Domain ranges:

000–099   STRUCTURAL MAIN
100–199   STRUCTURAL SECONDARY
1000–1999 PRESENTATION
2000–2999 COSMETIC / CONTENT

Current registered streams:

10   TRAJECTORY                  PilotMechanic
20   CONTROL                    PilotMechanic
30   PARKING_DODGE_OFFSET       ParkingMechanic
40   PARKING_SAVE_OFFSET        ParkingMechanic
50   PARKING_OVERSHOOT          ParkingMechanic
60   PARKING_STEERING_NOISE     ParkingMechanic
1010 PARTICLES                  PilotVisuals

All V2 structural access occurs through `StructuralRNG` and `MechanicRNGContext`.
Presentation access uses `CosmeticRNG` and `PresentationRNGContext`.

======================================================================
8. CAPABILITY / DI CONTRACT
======================================================================

Mechanic capability creation is performed by the Composition Root.

`MechanicRNGContext.create()` validates:

- rng version;
- duplicate stream claims;
- stream registration;
- domain correctness;
- Registry consumer authorization.

The context owns:

- seed;
- rng version;
- consumer identity;
- allowed streams;
- StructuralRNG capability.

A context copies its allowed stream array. Registry definitions expose defensive copies of consumer arrays.

Lower layers use `error_state` / `last_error` rather than expected-error `push_error()` I/O.

The Composition Root owns `[ERROR_JSON]` emission and process exit.

======================================================================
9. CURRENT LEGACY V1.0 CONTRACTS
======================================================================

CHALLENGE_001

seed = 193847
attempts = 2
final_seed = 126048932
seed_used = 126048932
winning_frame_game = 342
winning_frame = 462
minimum_distance = 0.000230040647936747
score = 0.638380059088502
close_calls = 3

CHALLENGE_002

seed = 987654
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

These fixtures remain `rng_version: "1.0"` and must not be migrated.

======================================================================
10. CURRENT V2 FIXTURES
======================================================================

CHALLENGE_003

mechanic = pilot
mechanic_version = 2.0
rng_version = 2.0
seed = 314159

Purpose: laboratory DDI fixture.

CHALLENGE_004

mechanic = parking_v2
mechanic_version = 2.0
rng_version = 2.0
seed = 314159

Purpose: first production-oriented V2.0 Parking fixture.

Temporal contract:

HOOK 120
GAME 420
CTA 120
TOTAL 660

======================================================================
11. PILOT V2 STATUS
======================================================================

PilotMechanic is not a product mechanic.

It is a controlled laboratory fixture proving that:

- structural calls are referentially stable;
- cosmetic consumption cannot alter SimulationResult;
- semantic indices are independent of call order;
- capabilities enforce scope.

Validated end-to-end result for CHALLENGE_003 in the working environment:

winning_frame_game = 272
winning_frame = 392
minimum_distance = 0.00520862150247581
score = 0.97863649811667
close_calls = 1

======================================================================
12. PARKING V2 STATUS
======================================================================

`mechanics/parking/ParkingMechanicV2.gd` is implemented.

Its mathematical contract is extracted from the frozen V1 Parking implementation.

Generation streams:

30 → dodge offset, index 0
40 → save offset, index 0
50 → overshoot, index 0

Per-frame noise:

60 → x index f*2
60 → y index f*2+1

The mechanic uses the cubic Bézier model and derived metrics from V1.

Isolation test:

`tests/ParkingMechanicV2IsolationTest.gd`

Validated:

[PARKING_V2_ISOLATION_SUITE] PASS

This means Parking V2 is isolated and validated, NOT globally integrated.

======================================================================
13. EXACT CURRENT INTEGRATION GAP — CHECKPOINT 0.3.6
======================================================================

Current real `MechanicRegistry.gd` resolves:

"key"    → KeyMechanic
"parking" → ParkingMechanic
"pilot"  → PilotMechanic

It does NOT yet resolve:

"parking_v2"

Current real `GeneradorMaestro.gd`:

- initializes RNG registry/facades;
- has context factory methods;
- supports a V2 branch only for the Pilot mechanic;
- rejects other V2 mechanics with `RNG_CONTEXT_INVALID`;
- calls `WinningFrameDetector` after simulation;
- has no Parking-specific context injection yet.

Therefore CHALLENGE_004 is NOT yet a valid global pipeline fixture at this handover point.

======================================================================
14. CHECKPOINT 0.3.6 IMPLEMENTATION ORDER
======================================================================

1. Audit the actual current `MechanicRegistry.gd` and `GeneradorMaestro.gd` again.
2. Add `parking_v2` resolution only.
3. In `GeneradorMaestro`, detect V2 `parking_v2` explicitly.
4. Build a `MechanicRNGContext` per retry using:

consumer_id = "ParkingMechanic"
allowed_streams = [30,40,50,60]

5. Inject the context into the `ParkingMechanicV2` instance.
6. Immediately inspect `error_state` after simulation.
7. If non-OK, reject before contract detector/validator processing and emit typed error through the Composition Root.
8. Preserve the existing Pilot V2 branch.
9. Preserve all V1 branches untouched.
10. Add integration coverage for CHALLENGE_004.

The retry loop is important: every retry uses the current retry seed and therefore needs a newly created capability.

======================================================================
15. REQUIRED REGRESSION ORDER
======================================================================

Before integration changes:

- run editor scan;
- run RNG suite;
- run Pilot isolation suites;
- run Parking V2 isolation suite;
- run CHALLENGE_001 validate-only;
- run CHALLENGE_002 validate-only.

After integration changes:

- repeat every test above;
- run CHALLENGE_003 through the global pipeline;
- run CHALLENGE_004 through the global pipeline;
- verify 001/002 numerical telemetry remains unchanged.

A change to 001/002 is a REGRESSION unless deliberately versioned and approved.

======================================================================
16. TEST SUITE STATUS
======================================================================

The following were validated in the working Godot 4.7.1 environment before this handover:

[RNG_TEST_SUITE] PASS
[RNG_ARCHITECTURE_SUITE] PASS
[PILOT_ISOLATION_SUITE] PASS
[DDI_R1] PASS
[PARKING_V2_ISOLATION_SUITE] PASS

The exact console outputs are historical evidence from the completed checkpoint, not a claim that the new context has already executed them.

======================================================================
17. TEMPORAL CONTRACT
======================================================================

Current live profile:

FPS = 60
HOOK = 2.0 s = 120 frames
GAME = 7.0 s = 420 frames
CTA = 2.0 s = 120 frames
TOTAL = 11.0 s = 660 frames

SimulationResult.winning_frame is GAME-relative.
ValidationResult.absolute_winning_frame = winning_frame + hook_frames.

Valid absolute GAME window:

120 <= absolute_winning_frame < 540

Do not resurrect historical 3+7+1 timing from older documents.

======================================================================
18. PRODUCT FAMILIES
======================================================================

Mathematical families:

HIT
CATCH
DODGE / SAVE / CONTROL
MATCH
FIND
JACKPOT

Themes are not mathematical families.

======================================================================
19. FORBIDDEN CHANGES IN 0.3.6
======================================================================

Do not mix this phase with:

- new mechanics;
- new themes;
- renderer changes;
- VideoTimeline changes;
- marketing/distribution work;
- visual optimization;
- RNG primitive redesign;
- Parking V2 mathematical redesign.

======================================================================
20. FIRST MESSAGE IN THE NEW CONTEXT
======================================================================

The new context should begin by stating that it has received CHECKPOINT 0.3.6 and will first audit the supplied ZIP against this handover.

It should then inspect the real code and execute the pre-integration tests.

Do not ask the user to restate the architecture.
Do not begin modifying code before the audit.

======================================================================
END OF CHECKPOINT 0.3.6 MASTER HANDOVER
======================================================================
