# CHECKPOINT 0.4.1 — MASTER HANDOVER PROMPT

======================================================================
PROJECT
======================================================================

ChallengeEngineV01

PACKAGE STATE:

CHECKPOINT 0.4.0 — PRODUCTION ORCHESTRATION FOUNDATION
FROZEN / VALIDATED END-TO-END

NEXT PHASE:

CHECKPOINT 0.4.1 — PRESENTATION & VIDEO TIMELINE

======================================================================
PURPOSE OF THIS HANDOVER
======================================================================

Transfer the current real project state to a new conversation without losing:

- the frozen V0.1 baseline (CHALLENGE_001 / CHALLENGE_002);
- the stateless RNG contract;
- semantic stream governance;
- capability / DI boundaries;
- PilotMechanic laboratory evidence (CHALLENGE_003);
- ParkingMechanicV2 mathematical and global integration contract
  (CHALLENGE_004);
- the validated production orchestration pipeline;
- the current VideoTimeline / presentation state;
- the exact next engineering objective.

======================================================================
0. NON-NEGOTIABLE WORKING RULE
======================================================================

The uploaded/project ZIP is the source of truth for CODE.

The `docs/*.md` files are the source of truth for DOCUMENTED CONTRACTS.

This handover is the source of truth for CONTEXT CONTINUITY.

If these artifacts disagree:

1. DO NOT silently fix anything.
2. Identify the discrepancy.
3. Inspect the actual code.
4. Compare against the relevant frozen checkpoint.
5. Decide explicitly which artifact is authoritative for that point.

During the initial 0.4.1 audit:

NO CODE MODIFICATION.
NO ARCHITECTURAL IMPROVEMENT BY INITIATIVE.
NO MATHEMATICAL REDESIGN.
NO RNG REDESIGN.
NO MECHANIC MIGRATION.

First:
AUDIT → VERIFY → DESIGN → IMPLEMENT → TEST → FREEZE.

======================================================================
1. FROZEN CHECKPOINT HISTORY
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
FROZEN / GLOBALLY VALIDATED

CHECKPOINT 0.4.0
Production Orchestration Foundation
FROZEN / END-TO-END VALIDATED

CHECKPOINT 0.4.1
Presentation & Video Timeline
OPEN — CURRENT WORK

======================================================================
2. CHECKPOINT 0.3.6 — FROZEN STATE
======================================================================

Parking V2 is fully integrated into the global Composition Root.

MechanicRegistry resolves:

- "key" → KeyMechanic
- "parking" → ParkingMechanic
- "pilot" → PilotMechanic
- "parking_v2" → ParkingMechanicV2

GeneradorMaestro:

- creates a `MechanicRNGContext` per retry;
- uses the current retry seed;
- routes `parking_v2` to consumer `"ParkingMechanic"`;
- grants streams `[30, 40, 50, 60]`;
- injects the capability through the mechanic DI API;
- checks `error_state` immediately after simulation and before validation/detection;
- preserves the existing Pilot V2 branch;
- preserves all V1 branches.

ParkingMechanicV2:

- receives its capability through `set_rng_context`;
- remains mathematically unchanged;
- uses streams:
  - 30 → dodge offset
  - 40 → save offset
  - 50 → overshoot
  - 60 → per-frame steering noise

CHALLENGE_004 global result validated:

- winning_frame_game = 394
- winning_frame = 514
- minimum_distance = 2.64212083816528
- score = 0.270782912190842
- close_calls = 1
- total_frames = 660
- absolute winning frame valid in 120–539 window

======================================================================
3. CHECKPOINT 0.4.0 — FROZEN PRODUCTION ORCHESTRATION
======================================================================

Architecture:

GODOT CALCULATES & RENDERS RAW
PYTHON ORCHESTRATES
FFMPEG PACKAGES
FFPROBE VALIDATES

The production factory is `build_factory.py`.

Contract:

1. PROJECT_ROOT is derived from `__file__`.
2. `challenge_id` is read from the declarative challenge JSON.
3. Mathematical validation uses Godot `--headless`.
4. Video production uses Godot without `--headless`, with Movie Maker:
   - `--write-movie`
   - `--fixed-fps 60`
   - `--quit-after 660`
5. Raw output naming:
   `CHALLENGE_XXX_raw.avi`
6. FFmpeg produces:
   `CHALLENGE_XXX.mp4`
7. FFprobe validates:
   - duration ≈ 11.0 s
   - nb_frames = 660
   - r_frame_rate = 60/1
8. `manifest.json` consolidates:
   - challenge identity
   - raw engine telemetry
   - artifact paths
   - FFprobe validation metadata

Validated production E2E result for CHALLENGE_004:

- Godot Movie Maker:
  660 frames @ 60 FPS
  540×960
  11 seconds
- FFmpeg:
  RAW AVI → MP4
- FFprobe:
  duration = 11.0
  nb_frames = 660
  r_frame_rate = 60/1
  valid = true
- build_factory:
  success = true

Important runtime distinction:

- `--headless` is used for CPU/math validation.
- Movie Maker production is executed with the graphical Compatibility renderer.
- The attempted `--headless + Movie Maker` path caused a Godot dummy-renderer crash (`texture_2d_get` with null texture); this is NOT part of the production contract.

No changes were made to:
- RNG implementation;
- mechanics;
- challenge fixtures;
- project rendering architecture;
- VideoTimeline;
- mathematical contracts.

======================================================================
4. CURRENT VALIDATED NUMERICAL CONTRACTS
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

CHALLENGE_003

mechanic = pilot
mechanic_version = 2.0
rng_version = 2.0
seed = 314159

Validated global result:

winning_frame_game = 272
winning_frame = 392
minimum_distance = 0.00520862150247581
score = 0.97863649811667
close_calls = 1

CHALLENGE_004

mechanic = parking_v2
mechanic_version = 2.0
rng_version = 2.0
seed = 314159

Validated global result:

winning_frame_game = 394
winning_frame = 514
minimum_distance = 2.64212083816528
score = 0.270782912190842
close_calls = 1

======================================================================
5. TEST SUITE STATUS
======================================================================

Validated in Godot 4.7.1:

[RNG_TEST_SUITE] PASS
[RNG_ARCHITECTURE_SUITE] PASS
[PILOT_ISOLATION_SUITE] PASS
[DDI_R1] PASS
[PARKING_V2_ISOLATION_SUITE] PASS

CHALLENGE_001 validate-only: PASS
CHALLENGE_002 validate-only: PASS
CHALLENGE_003 validate-only: PASS
CHALLENGE_004 validate-only: PASS

Production orchestration:

CHALLENGE_004:
build_factory.py → PASS
RAW AVI generation → PASS
FFmpeg packaging → PASS
FFprobe artifact validation → PASS
manifest generation → PASS

The RNG regression suite was repaired only at the test assertion level:
floating-point regression assertions use `is_equal_approx`.
Frozen numeric values were not changed.

======================================================================
6. LIVE TEMPORAL CONTRACT
======================================================================

FPS = 60
HOOK = 120 frames = 2.0 s
GAME = 420 frames = 7.0 s
CTA = 120 frames = 2.0 s
TOTAL = 660 frames = 11.0 s

SimulationResult.winning_frame is GAME-relative.

Absolute winning frame:

winning_frame + hook_frames

Valid absolute GAME window:

120 <= absolute_winning_frame < 540

Do not resurrect historical timing profiles.

======================================================================
7. CHECKPOINT 0.4.1 — PRESENTATION & VIDEO TIMELINE
======================================================================

OBJECTIVE

Integrate and validate the presentation layer so that it consumes the already
validated SimulationResult without recalculating the mathematical simulation.

The presentation layer is a consumer of simulation truth.

It must NOT:

- calculate winning_frame;
- regenerate mechanic behaviour;
- access structural RNG;
- modify SimulationResult;
- duplicate simulation logic;
- alter retry decisions;
- alter validation rules.

It MAY:

- consume SimulationResult;
- consume validation/timeline metadata;
- resolve visual assets;
- render hook/game/CTA sections;
- position visual actors according to already-derived simulation data;
- run Movie Maker presentation frames.

======================================================================
8. REQUIRED 0.4.1 AUDIT BEFORE CODE
======================================================================

First inspect the real current state of:

- `core/timeline/VideoTimeline.gd`
- `Main.tscn`
- `FamilyAssets.gd`
- presentation-related nodes/scripts
- `GeneradorMaestro.gd` presentation path
- current `README_INTEGRATION.md`
- `docs/VIDEO_SPECIFICATION.md`
- `docs/VALIDATION_PROTOCOL.md`

Also inspect how the current presentation consumes:

- `SimulationResult`
- `FrameSnapshot`
- hook/game/CTA frame boundaries
- assets/content metadata

Do NOT assume the handover description is the current implementation.

======================================================================
9. 0.4.1 DESIGN TARGET
======================================================================

The desired dependency direction is:

Challenge JSON
      ↓
Simulation Core
      ↓
SimulationResult
      ↓
Presentation
      ↓
Movie Maker

Presentation must be downstream of simulation.

For example:

SimulationResult
    winning_frame_game
    snapshots
    derived metrics
          ↓
VideoTimeline / presentation
          ↓
visual frame composition

No reverse dependency from presentation into simulation.

======================================================================
10. PRESENTATION TEMPORAL CONTRACT
======================================================================

The live presentation profile is:

HOOK
120 frames

GAME
420 frames

CTA
120 frames

TOTAL
660 frames

The timeline must preserve these boundaries exactly.

No legacy 3+7+1 second profile should be reintroduced.

======================================================================
11. ASSET CONTRACT
======================================================================

`FamilyAssets` is responsible for resolving presentation assets from the
challenge content metadata.

The presentation layer must remain asset-driven.

Themes are presentation/content only.

Themes do NOT define new mathematical families.

No new family, mechanic, renderer architecture, or social-platform logic is
part of 0.4.1.

======================================================================
12. REQUIRED 0.4.1 VALIDATION
======================================================================

Before presentation modifications:

- editor scan;
- RNG suite;
- architecture suite;
- Pilot isolation;
- DDI hardening;
- Parking V2 isolation;
- CHALLENGE_001 validate-only;
- CHALLENGE_002 validate-only;
- CHALLENGE_003 validate-only;
- CHALLENGE_004 validate-only;
- build_factory production regression for the selected presentation fixture.

After presentation modifications:

Repeat all applicable tests above and additionally verify:

1. Same SimulationResult before and after presentation integration.
2. Same winning frame.
3. Same validation result.
4. Same 660-frame timeline.
5. No structural RNG access from presentation.
6. No simulation recalculation in presentation.
7. Movie Maker produces a valid 660-frame / 60 FPS artifact.
8. FFprobe validation remains valid.
9. Manifest telemetry remains unchanged.

A presentation change that alters simulation telemetry is a REGRESSION.

======================================================================
13. FORBIDDEN CHANGES IN 0.4.1
======================================================================

Do not mix this phase with:

- new mechanics;
- new mathematical families;
- RNG redesign;
- challenge fixture migration;
- Composition Root redesign;
- production-orchestration redesign;
- FFmpeg packaging redesign;
- marketing/distribution work;
- social-platform integrations;
- renderer technology migration.

======================================================================
14. SUCCESS CRITERION
======================================================================

CHECKPOINT 0.4.1 is complete only when:

- VideoTimeline is correctly integrated;
- Presentation consumes SimulationResult passively;
- Hook/Game/CTA boundaries are preserved;
- assets resolve correctly;
- CHALLENGE_004 renders correctly;
- the SimulationResult is unchanged by presentation;
- production output remains:
  660 frames
  60 FPS
  11 seconds
- FFprobe remains valid;
- manifest remains valid;
- all frozen mathematical/regression contracts remain unchanged.

======================================================================
END OF CHECKPOINT 0.4.1 MASTER HANDOVER
======================================================================
