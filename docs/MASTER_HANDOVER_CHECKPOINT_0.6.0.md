# CHECKPOINT 0.6.0 — MASTER HANDOVER PROMPT

======================================================================
PROJECT
======================================================================

ChallengeEngineV01

PACKAGE STATE:

CHECKPOINT 0.5.1 — CONTROLLED PARALLEL PRODUCTION VALIDATED
NEXT PHASE:

CHECKPOINT 0.6.0 — NEW MATHEMATICAL FAMILY (HIT)

PURPOSE OF THIS HANDOVER:

Transfer the current real project state to a new engineering phase.
This phase introduces a strictly mathematical implementation of a new "HIT" mechanic family, strictly adhering to the "Audit -> Contract -> Isolation -> Integration -> Batch -> Freeze" protocol.

======================================================================
0. NON-NEGOTIABLE WORKING RULE
======================================================================

1.  **Zero Regressions:** Do NOT modify `MechanicRegistry`, `ParkingMechanicV2`, `VideoTimeline`, `build_factory.py`, `GeneradorMaestro`, or the RNG subsystem.
2.  **Immutability:** `CHALLENGE_001` through `CHALLENGE_004` and their outputs/manifests are frozen fixtures.
3.  **Math First:** The HIT family must be validated in isolation mathematically before ANY visual implementation is considered.

======================================================================
1. FAMILY SELECTED: HIT
======================================================================

**Concept:** Discrete spatial intersection. A projectile travels towards a target. The winning frame is the exact moment ($t$) of perfect alignment (minimum distance to the center of the hitbox).

**No Conceptual Overlap:** Distinct from Pilot (continuous path following) and Parking (deceleration into a zone). HIT is a timing-based ballistic intersection.

======================================================================
2. MATHEMATICAL DEFINITION (THE CONTRACT)
======================================================================

**Inputs (Capa 0 - JSON):**
- `origin`: Vector2(x, y) - Starting point.
- `target`: Vector2(x, y) - Impact point.
- `speed_base`: float - Base velocity (pixels per frame).
- `hitbox_radius`: float - Tolerance radius for a valid hit.

**Outputs (SimulationResult):**
- `minimum_distance`: float - Distance from projectile to target center at `winning_frame`.
- `score`: float - Normalized hit quality (0.0 to 1.0 based on `hitbox_radius`).
- `metadata["impact_velocity"]`: float.

**RNG Streams Required (Domain 70-99):**
- `70 -> HIT_SPEED_VARIANCE` (Index: 0) - Per-retry initial speed variation.
- `80 -> HIT_TRAJECTORY_NOISE` (Index: f) - Per-frame Y-axis displacement (jitter).
- `90 -> HIT_TARGET_OFFSET` (Index: 0) - Per-retry static target drift.

**Index Semantics:**
- Stream 70, 90: Resolved exactly once per simulation attempt (index 0).
- Stream 80: Resolved per frame to simulate physical noise (index: $f$).

**Expected SimulationResult:**
- 420 FrameSnapshots (for a 7.0s GAME block).
- `winning_frame` strictly defined as the frame where `current_distance` is minimal.

======================================================================
3. VALIDATION RULES
======================================================================

- The `absolute_winning_frame` must fall within the engine's valid window: $120 \le frame < 540$.
- `close_calls`: Count of frames where `current_distance <= hitbox_radius` excluding the winning frame.

======================================================================
4. FIXTURE: CHALLENGE_005
======================================================================

A new declarative fixture must be created: `challenges/CHALLENGE_005.json`.
- `mechanic`: "hit_v1"
- `rng_version`: "2.0"
- `seed`: 998877

======================================================================
5. CRITERIA FOR COMPLETION
======================================================================

**[ISOLATION SUITE]**
- Create `HitMechanicIsolationTest.gd`.
- Validate stream independence, semantic indexing, error bubbling, and deterministic output for the HIT formula.

**[GLOBAL INTEGRATION]**
- Register `hit_v1` in `MechanicRegistry`.
- Map capability injection in `GeneradorMaestro` (allowed streams: `[70, 80, 90]`).

**[PRODUCTION BATCH]**
- `build_factory.py --batch` must process `001` through `005` with zero regressions and yield a 5-0 PASSED manifest.

======================================================================
END OF CHECKPOINT 0.6.0 MASTER HANDOVER
======================================================================