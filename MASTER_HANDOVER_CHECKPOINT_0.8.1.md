# CHECKPOINT 0.8.1 — MASTER HANDOVER PROMPT

======================================================================
PROJECT
======================================================================

ChallengeEngineV01

CURRENT PACKAGE STATE:

CHECKPOINT 0.8.1 — CATCH PRESENTATION CONTRACT
FROZEN / VALIDATED END-TO-END

NEXT PHASE:

CHECKPOINT 0.9.0 — PRODUCTION CONTRACT CONSOLIDATION

======================================================================
PURPOSE OF THIS HANDOVER
======================================================================

Transfer the current engineering context to a new conversation without losing:

- the frozen mathematical baseline CHALLENGE_001 through CHALLENGE_006;
- the stateless RNG and semantic-stream governance;
- DDI capability boundaries;
- the Production Factory / Batch pipeline;
- the hardened external Python test runner;
- the CATCH v1 mathematical contract;
- the CATCH presentation contract using FrameSnapshot.custom_data;
- the validated numerical telemetry of CHALLENGE_006;
- the latest 6/6 batch evidence;
- the outstanding production-contract versioning debt;
- the exact scope of CHECKPOINT 0.9.0.

This document is CONTEXT CONTINUITY, not a substitute for the real project files.

======================================================================
0. NON-NEGOTIABLE WORKING RULE
======================================================================

The project ZIP / real repository state is the source of truth for CODE.

The docs/*.md files in the project are the source of truth for documented
contracts where they exist.

This handover is the source of truth for CONTEXT CONTINUITY.

If ZIP, docs, and this handover disagree:

1. DO NOT silently reconcile them.
2. Identify the discrepancy explicitly.
3. Inspect the real code.
4. Compare against the relevant frozen checkpoint evidence.
5. Decide explicitly which artifact is authoritative for that point.

Engineering doctrine remains:

AUDIT → CONTRACT → ISOLATION → INTEGRATION → REGRESSION → BATCH → FREEZE

For any new work, audit the real implementation before proposing code.

No speculative API signatures.
No blind load()/simulate() assumptions.
No unrelated refactors.
No mathematical changes to frozen families unless a new checkpoint explicitly
opens that contract.

======================================================================
1. FROZEN CHECKPOINT HISTORY
======================================================================

CHECKPOINT 0.1
Stateful → Stateless RNG
FROZEN / VALIDATED

CHECKPOINT 0.2.x
Semantic Streams, DI, Pilot laboratory and DDI hardening
FROZEN / VALIDATED

CHECKPOINT 0.3.x
Parking V2 mathematical contract, production streams, isolation and global
Composition Root integration
FROZEN / VALIDATED

CHECKPOINT 0.4.0
Production Orchestration Foundation
FROZEN / END-TO-END VALIDATED

CHECKPOINT 0.4.1
Presentation & Video Timeline foundation
FROZEN / VALIDATED

CHECKPOINT 0.5.0
Batch Production & Factory Hardening
FROZEN / VALIDATED

CHECKPOINT 0.5.1
Controlled Parallel Production
FROZEN / VALIDATED

CHECKPOINT 0.6.0
HIT v1 — New Mathematical Family
FROZEN / VALIDATED

CHECKPOINT 0.7.0
Production Contract Hardening
FROZEN / VALIDATED

- 0.7.0-A: external Python test-runner hardening
- 0.7.0-B: factory versioning and manifest enrichment

CHECKPOINT 0.8.0
CATCH v1 — New Mathematical Family
FROZEN / VALIDATED

CHECKPOINT 0.8.1
CATCH Presentation Contract
FROZEN / VALIDATED END-TO-END

NEXT:
CHECKPOINT 0.9.0 — PRODUCTION CONTRACT CONSOLIDATION
OPEN — NEXT OBJECTIVE

======================================================================
2. CURRENT ENGINE STATE — EXECUTIVE SUMMARY
======================================================================

The engine currently supports six declarative challenge fixtures:

- CHALLENGE_001 — legacy Key / V1 baseline
- CHALLENGE_002 — legacy Parking / V1 baseline
- CHALLENGE_003 — Pilot V2 / RNG 2.0
- CHALLENGE_004 — Parking V2 / RNG 2.0
- CHALLENGE_005 — HIT V1 / RNG 2.0
- CHALLENGE_006 — CATCH V1 / RNG 2.0

Production pipeline:

Challenge JSON
    ↓
Godot validation / simulation
    ↓
SimulationResult + telemetry
    ↓
Godot Movie Maker (graphical Compatibility renderer)
    ↓
RAW AVI
    ↓
Python build_factory.py
    ↓
FFmpeg H.264 / YUV420p
    ↓
MP4
    ↓
FFprobe validation
    ↓
manifest.json / BATCH_MANIFEST.json

Golden architecture rule:

GODOT CALCULATES & RENDERS RAW
PYTHON ORCHESTRATES
FFMPEG PACKAGES
FFPROBE VALIDATES

======================================================================
3. TEMPORAL CONTRACT — FROZEN
======================================================================

FPS = 60
HOOK = 120 frames = 2.0 s
GAME = 420 frames = 7.0 s
CTA = 120 frames = 2.0 s
TOTAL = 660 frames = 11.0 s

VideoTimeline derives frame counts from durations using:

frames = round(duration_seconds * fps)

SimulationResult.winning_frame is GAME-relative.

Absolute winning frame:

absolute_winning_frame = winning_frame + hook_frames

Valid absolute GAME window:

120 <= absolute_winning_frame < 540

Do not resurrect historical timing profiles such as the former 3+7+1 layout.

======================================================================
4. RNG / DDI CONTRACT — FROZEN
======================================================================

Stateless RNG is governed through semantic streams and MechanicRNGContext.

Pilot streams:

10 → TRAJECTORY
20 → CONTROL

Parking V2 streams:

30 → PARKING_DODGE_OFFSET
40 → PARKING_SAVE_OFFSET
50 → PARKING_OVERSHOOT
60 → PARKING_STEERING_NOISE

HIT V1 streams:

70 → HIT_SPEED_VARIANCE
80 → HIT_TRAJECTORY_NOISE
90 → HIT_TARGET_OFFSET

CATCH V1 streams:

100 → CATCH_TARGET_MOTION
110 → CATCH_PURSUER_BIAS
120 → CATCH_INITIAL_PHASE

CATCH streams are registered as Domain.STRUCTURAL_SECONDARY and are authorized
exclusively for consumer "CatchMechanic".

Mechanics consume capabilities through DI. The Composition Root owns context
creation and allowed-stream declarations.

Unauthorized stream consumption must transition the RNG context into an error
state and must be surfaced/bubbled by the simulation pipeline.

======================================================================
5. TEST HARNESS HARDENING — FROZEN
======================================================================

The project originally exposed a dangerous false-positive pattern in
SceneTree-based test scripts: runtime GDScript errors could abort a test
function before the local failure counter was incremented, while the harness
still printed PASS.

CHECKPOINT 0.7.0-A solved this by introducing the external Python runner:

    tests/run_suite.py

The runner treats all of the following as fatal:

- non-zero exit code;
- SCRIPT ERROR:
- Parse Error:
- Failed to load script
- Invalid access
- Invalid assignment
- Cannot call method
- CrashHandlerException
- absence of an accepted PASS marker

Fire-test evidence was obtained with a deliberate bad identifier; the runner
correctly returned FAIL and exit code 1.

Therefore, a suite-level PASS is not sufficient evidence by itself; the
external runner is the final arbiter for registered suites.

======================================================================
6. PRODUCTION FACTORY — CURRENT CONTRACT
======================================================================

File:

    build_factory.py

Current factory constant:

    FACTORY_VERSION = "0.7.0"

IMPORTANT OPEN DEBT:

The current factory version remains "0.7.0" even though the production system
now contains frozen work from checkpoints 0.8.0 and 0.8.1.

This is intentionally NOT changed in 0.8.1.
It is the primary objective of CHECKPOINT 0.9.0.

Current supported modes:

    --config <file>
    --batch <directory>

Batch supports:

    --workers <int>

and preserves deterministic manifest ordering even when workers complete
asynchronously.

Unit artifact contract:

    CHALLENGE_XXX_raw.avi
    CHALLENGE_XXX.mp4
    CHALLENGE_XXX_manifest.json

FFprobe acceptance contract:

    duration ≈ 11.0 s (absolute tolerance 0.05)
    nb_frames == 660
    r_frame_rate == "60/1"

Batch manifest currently includes:

- factory_version
- godot_versions
- rng_versions
- status
- summary { total, passed, failed }
- per-challenge status and manifest path

The latest validated batch still reports:

    factory_version = "0.7.0"
    godot_versions = ["4.7.1-stable (official)"]
    rng_versions = ["1.0", "2.0"]

Do not silently change the factory schema outside CHECKPOINT 0.9.0.

======================================================================
7. CATCH V1 — FROZEN MATHEMATICAL CONTRACT
======================================================================

Family:

    catch_v1

Mechanic:

    CatchMechanic

Concept:

Two independently prescribed mobile trajectories converge without reactive
feedback. CATCH is NOT a pursuit-control loop. It is a deterministic discrete
kinematic interception problem.

Configuration fields:

    difficulty.catch.catcher_origin
    difficulty.catch.catcher_direction
    difficulty.catch.catcher_speed_base
    difficulty.catch.target_origin
    difficulty.catch.target_direction
    difficulty.catch.target_speed_base
    difficulty.catch.catch_radius

Directions are normalized strictly before velocity construction.

Effective target speed:

    v_t_eff = target_speed_base * (1 + delta_target)

Effective catcher speed:

    v_c_eff = catcher_speed_base * (1 + delta_bias)

Target phase shift:

    t0' = t0 + (delta_phase_x, 0)

Frame kinematics:

    p_t(f) = t0' + v_t * f
    p_c(f) = c0  + v_c * f

Distance:

    d_f = |p_c(f) - p_t(f)|

Winning frame:

    f* = argmin_f d_f

Strict '<' is used so the first argmin wins in an exact tie.

Captured:

    captured = (minimum_distance <= catch_radius)

Score:

    score = clamp(1 - minimum_distance / catch_radius, 0, 1)

Closing velocity:

    closing_velocity = |v_c - v_t|

Close calls:

    Count frames with d_f <= catch_radius, excluding f*.

IMPORTANT:

The earlier proposal of catch_radius * 3.5 was rejected by the global validator
because it inflated close-call counts beyond the accepted maximum. The frozen
implementation aligns CATCH close-call semantics with HIT and uses the exact
catch_radius.

======================================================================
8. CATCH V1 — DDI CONTRACT
======================================================================

CATCH uses:

100 → target motion variance, index 0, range [-0.20, 0.20]
110 → pursuer bias, index 0, range [-0.15, 0.15]
120 → initial phase X offset, index 0, range [-50.0, 50.0]

Consumer:

    "CatchMechanic"

CATCH is treated as mathematically sovereign in the Composition Root.

Therefore:

WinningFrameDetector.analyze_and_score(test_result)

is NOT invoked for CATCH.

CATCH owns its own winning_frame, minimum_distance and score.

The global ChallengeValidator remains the common validation gate.

======================================================================
9. CATCH V1 — PRESENTATION CONTRACT 0.8.1
======================================================================

A presentation gap existed because FrameSnapshot.position represented only the
primary moving entity (catcher), while CATCH also requires the target position
for visual playback.

The solution is deliberately generic and non-invasive:

    FrameSnapshot.custom_data["target_position"]

For every GAME frame produced by CatchMechanic:

    snap.custom_data = {
        "target_position": p_t
    }

Therefore:

FrameSnapshot.position
    → primary entity / catcher

FrameSnapshot.custom_data["target_position"]
    → secondary entity / target

This does NOT change SimulationResult shape and does NOT add a CATCH-specific
branch to FrameSnapshot itself.

Presentation consumes this field passively in GeneradorMaestro._process().
When the key exists and contains a Vector2, target_sprite.position is updated
from it.

No simulation is recalculated by presentation.
No structural RNG is accessed by presentation.
No retry or validation decision is changed.

======================================================================
10. CATCH PRESENTATION VALIDATION — FROZEN
======================================================================

Suite:

    tests/mechanics/catch/CatchPresentationContractTest.gd

Required PASS marker:

    [CATCH_PRESENTATION_CONTRACT_SUITE] PASS

The suite independently reconstructs the expected catcher and target
trajectories and checks all 420 snapshots.

It verifies:

- exactly 420 snapshots;
- primary FrameSnapshot.position matches the analytical catcher position;
- custom_data contains "target_position";
- target_position matches the independently reconstructed target trajectory;
- presentation transport is complete before any pixels are rendered.

External runner evidence:

    CATCH_V1_ISOLATION        PASS
    CATCH_PRESENTATION_CONTRACT PASS
    HIT_V1_ISOLATION          PASS

======================================================================
11. CHALLENGE_006 — FROZEN FIXTURE
======================================================================

File:

    challenges/CHALLENGE_006.json

Mechanic:

    catch_v1

Seed:

    884422

RNG version:

    2.0

Video:

    60 FPS
    2.0 s hook
    7.0 s game
    2.0 s CTA

Cinematic setup:

    catcher_origin = [540.0, 1700.0]
    catcher_direction = [0.0, -1.0]
    catcher_speed_base = 6.0

    target_origin = [540.0, 400.0]
    target_direction = [0.0, 1.0]
    target_speed_base = 2.5

    catch_radius = 45.0

Content:

    hook = "¡Intercepta el objetivo en movimiento!"
    cta  = "¡Desafío superado!"

======================================================================
12. CHALLENGE_006 — FROZEN NUMERICAL REFERENCE
======================================================================

Latest validated telemetry:

    attempts                  = 1
    initial_seed              = 884422
    final_seed                = 884422
    seed_used                 = 884422
    rng_version               = 2.0

    winning_frame_game        = 158
    winning_frame             = 278
    winning_time_game         = 2.63333333333333
    winning_time              = 4.63333333333333

    minimum_distance          = 27.2707214355469
    score                     = 0.393983968098958
    close_calls               = 8

    total_frames              = 660
    hook_frames               = 120
    game_frames               = 420
    cta_frames                = 120
    winning_frame_in_valid_window = true

Repeated validate-only execution produced identical telemetry, confirming the
frozen reference is deterministic.

======================================================================
13. CHALLENGE_001 → CHALLENGE_005 — REGRESSION REFERENCES
======================================================================

CHALLENGE_001

    seed = 193847
    winning_frame_game = 335 in the latest global validate-only run
    winning_frame = 455
    minimum_distance = 0.00736591562275279
    score = 0.648328777570576
    close_calls = 0
    rng_version = 1.0

NOTE:

Earlier isolated regression evidence for the legacy generator/test path also
contained a frozen reference around winning_frame_game = 342 with a retry and
final_seed = 126048932. Do NOT silently reconcile these two historical values.
The real current project files and the current checkpoint-specific contract are
authoritative. Investigate before freezing any new numeric baseline for legacy
CHALLENGE_001.

CHALLENGE_002

    seed = 987654
    winning_frame_game = 395
    winning_frame = 515
    minimum_distance = 3.38832068443298
    score = 0.246091849120501
    close_calls = 1
    dodge_offset = -95.0478103361315
    save_offset = 23.9687795163918
    overshoot_dist = 67.4236544163076
    rng_version = 1.0

CHALLENGE_003

    seed = 314159
    winning_frame_game = 272
    winning_frame = 392
    minimum_distance = 0.00520862150247581
    score = 0.97863649811667
    close_calls = 1
    rng_version = 2.0

CHALLENGE_004

    seed = 314159
    winning_frame_game = 394
    winning_frame = 514
    minimum_distance = 2.64212083816528
    score = 0.270782912190842
    close_calls = 1
    dodge_offset = 120.751099372632
    save_offset = 4.0367575613953
    overshoot_dist = 68.9688734938246
    rng_version = 2.0

CHALLENGE_005

    seed = 998877
    winning_frame_game = 344
    winning_frame = 464
    minimum_distance = 1.68177151679993
    score = 0.943940949440002
    close_calls = 16
    rng_version = 2.0

IMPORTANT:

The latest batch validated all six challenges successfully. Do not overwrite
frozen values based solely on a convenient earlier transcript snippet.
Audit the current ZIP/repository when exact legacy parity matters.

======================================================================
14. LATEST PRODUCTION BATCH EVIDENCE — FROZEN 0.8.1 GATE
======================================================================

Command:

    python build_factory.py --batch ./challenges --output ./output

Latest result:

    success = true

    total  = 6
    passed = 6
    failed = 0
    status = PASSED

Batch manifest metadata:

    factory_version = "0.7.0"

    godot_versions = [
        "4.7.1-stable (official)"
    ]

    rng_versions = [
        "1.0",
        "2.0"
    ]

Per-challenge result:

    CHALLENGE_001 → PASS
    CHALLENGE_002 → PASS
    CHALLENGE_003 → PASS
    CHALLENGE_004 → PASS
    CHALLENGE_005 → PASS
    CHALLENGE_006 → PASS

This is the final production gate for CHECKPOINT 0.8.1.

======================================================================
15. 0.8.1 FREEZE DECISION
======================================================================

CHECKPOINT 0.8.1 is considered FROZEN / VALIDATED.

Evidence chain:

1. CATCH_V1_ISOLATION → PASS
2. CATCH_PRESENTATION_CONTRACT → PASS
3. CHALLENGE_006 validate-only → PASS
4. CHALLENGE_006 E2E production → PASS
5. FFprobe → 660 frames / 60 FPS / 11.0 s
6. Full production batch 001–006 → 6/6 PASS

No further architectural modification to CATCH is required before 0.9.0.

======================================================================
16. CHECKPOINT 0.9.0 — EXACT NEXT OBJECTIVE
======================================================================

Name:

    PRODUCTION CONTRACT CONSOLIDATION

This phase is NOT a new mathematical family.

This phase is NOT a CATCH refactor.

This phase exists to make the production contract self-consistent and
self-describing after the growth from 0.7.x through 0.8.1.

Primary objective:

    Resolve the versioning mismatch where build_factory.py still reports
    FACTORY_VERSION = "0.7.0" even though the current frozen system includes
    HIT 0.6.0 and CATCH 0.8.0/0.8.1.

Proposed target:

    FACTORY_VERSION = "0.9.0"

But DO NOT change it blindly. First audit the real current build_factory.py,
manifest schema, and all existing documentation.

0.9.0 should consolidate at least:

- factory_version;
- engine_version / Godot version metadata;
- RNG version metadata;
- challenge identity/version metadata;
- manifest schema/version;
- artifact schema/path contract;
- compatibility semantics for mixed RNG 1.0 / 2.0 batches.

The exact fields and naming MUST be derived from the current code/docs before
implementation. Do not invent a schema merely because it is convenient.

Acceptance criteria for 0.9.0 should be designed during AUDIT/CONTRACT, then
validated through regression and a fresh 6/6 batch.

======================================================================
17. OUT OF SCOPE FOR 0.9.0
======================================================================

Do NOT use 0.9.0 to:

- introduce MATCH;
- introduce FIND;
- introduce another mathematical family;
- redesign CATCH mathematics;
- redesign RNG;
- replace ThreadPoolExecutor with a new concurrency model without evidence;
- redesign FFmpeg encoding;
- redesign Movie Maker rendering;
- migrate renderer technology;
- add social-platform APIs;
- perform product/marketing work.

The objective is production contract consolidation only.

======================================================================
18. FUTURE 1.0.0 DIRECTION
======================================================================

A fifth mathematical family such as MATCH/FIND may be considered only AFTER
production contract consolidation is frozen.

The reason is architectural stability:

- custom_data has now demonstrated a viable transport for secondary visual
  entities;
- the manifest has accumulated mixed-version metadata;
- the test harness is newly hardened;
- the production factory now spans six fixtures and multiple mechanics.

Stabilize these contracts before increasing mathematical surface area again.

======================================================================
19. IMPORTANT HISTORICAL LESSONS / KNOWN FAILURE MODES
======================================================================

A. Godot headless + Movie Maker:

The attempted combination of --headless and --write-movie caused a Godot
SIGSEGV in the dummy renderer while accessing a null texture. Production video
must use the graphical Compatibility renderer. Headless remains the safe path
for CPU/math validation.

B. Float regression assertions:

The RNG test suite once failed on exact float comparisons even though the
frozen mathematical values were unchanged. The test was corrected with
is_equal_approx. Frozen values were not modified.

C. SceneTree false PASS:

A runtime GDScript error can abort a test method before its internal failure
counter increments. Therefore SceneTree PASS output alone is NOT trustworthy.
Use the external Python runner.

D. Godot Object.get():

Object.get() is not a Dictionary.get(key, default) equivalent. Custom objects
such as MechanicRNGContext require direct property access for this codebase.

E. FrameSnapshot field drift:

Do not invent frame index properties. The current working pattern uses the
array position as the frame index. CATCH presentation uses custom_data for
secondary entity state.

F. Generic detector sovereignty:

HIT and CATCH calculate their own winning_frame / minimum_distance / score.
The generic WinningFrameDetector must not overwrite their mathematical results.

G. Close-call semantics:

CATCH originally used catch_radius * 3.5, which conflicted with global validator
limits. The frozen implementation uses exact catch_radius, matching HIT's
semantics.

======================================================================
20. START-OF-NEXT-CONVERSATION PROTOCOL
======================================================================

When starting the next conversation:

1. Treat the real ZIP/repository as code authority.
2. Read this handover before proposing changes.
3. Audit build_factory.py and manifest-related docs first.
4. Determine the real current factory/version schema.
5. Do NOT modify code until AUDIT/CONTRACT is complete.
6. Preserve all six challenge fixtures as regression fixtures.
7. Preserve the CATCH custom_data presentation contract.
8. Preserve the external Python test runner.
9. Preserve mixed RNG 1.0 / 2.0 support.
10. Only after 0.9.0 is frozen consider a new mathematical family.

Recommended first command set in the new conversation:

    godot --headless --path . --editor --quit

    python tests/run_suite.py

    python build_factory.py --batch ./challenges --output ./output

These are verification commands, not permission to modify anything.

======================================================================
END OF CHECKPOINT 0.8.1 MASTER HANDOVER
======================================================================
