# MASTER HANDOVER CHECKPOINT 1.1.0-C6-A
## FIRST PLAYABLE PROTOTYPE — PARKING_V2

**Date:** 2026-08-23
**Status:** READY FOR NEW CONTEXT WINDOW

## 0. CRITICAL SOURCE-OF-TRUTH NOTE

The uploaded source archive available for this handover is:
`ChallengeEngineV01_STATELESS-1.1.0-C3-E.zip`

Its Git HEAD is:
`334310e CHECKPOINT 1.1.0-C3-E HARDENING`

Therefore this archive is **NOT** a byte-for-byte snapshot of the later C4/C5 implementation validated in the current conversation. It must be treated as the last frozen source baseline available in the archive, while the later C4/C5 state is established by the verified terminal results recorded below.

Do not claim that the archive contains C4/C5 code.

## 1. CERTIFIED ARCHITECTURAL STATE

### C3 — Lifecycle & Temporal Purification
CERTIFIED.

The current validated architecture separates:
- Model A: structural mechanics complete lifecycle in `setup()` and mark `_is_prepared = true`.
- Model B: structural entropy in `setup()`, temporal buffers in `prepare(total_frames)`, zero RNG in `simulate()`.
- RNG context ownership remains local to V2 mechanics; `ChallengeMechanic` does not own `_rng_context`.

Certified mechanics involved in the current C3 state:
- HIT_V1
- PILOT
- PARKING_V2
- CATCH_V1
- FIND_V1

### C4 — Simulation Contract & Validation Boundary
CERTIFIED by current-session verification.

Certified conceptual pipeline:

Mechanic
→ `SimulationResult`
→ `SimulationMetricsResolver`
→ `WinningFrameDetector`
→ `ChallengeValidator`
→ `ValidationResult`

Relevant contract additions/decisions:
- `SimulationResult.error_state = "OK"`
- `SimulationResult.is_self_scored = false`
- `SimulationResult.validate_contract(expected_game_frames)` validates error state, frame structure, metrics and tolerance.
- Self-scored mechanics: HIT_V1, CATCH_V1, FIND_V1.
- `WinningFrameDetector` is universally called by the Composition Root and returns without mutation for errored or self-scored results.
- `ChallengeValidator` no longer computes spatial close-call streaks itself.
- `SimulationMetricsResolver` normalizes `close_calls` and provenance (`MECHANIC` vs `DERIVED`) before validation.

### C5 — Production Provenance Chain
CERTIFIED by current-session verification.

Subphases certified:
- C5-A Runtime ↔ Artifact Consistency Gate
- C5-B Manifest Provenance Integrity
- C5-C Unit Artifact Identity / SHA-256
- C5-D Batch Manifest Integrity / Disk SSOT

Verified production results:
- Python corpus: 9/9 PASS
- Production batch: 7/7 PASS
- Batch was also verified with 2 workers after SHA-256 integration.
- Unit manifests contain `raw_video_sha256` and `final_video_sha256` and the batch post-audit recomputes those hashes from disk.

## 2. VERIFIED PRODUCTION CORPUS

Seven production challenges are certified:

1. CHALLENGE_001 — key — RNG 1.0
2. CHALLENGE_002 — parking — RNG 1.0
3. CHALLENGE_003 — pilot — RNG 2.0
4. CHALLENGE_004 — parking_v2 — RNG 2.0
5. CHALLENGE_005 — hit_v1 — RNG 2.0
6. CHALLENGE_006 — catch_v1 — RNG 2.0
7. CHALLENGE_007 — find_v1 — RNG 2.0

Godot version observed in production validation:
`4.7.1-stable (official)`

Factory version:
`0.9.0`

Manifest version:
`1.0`

## 3. C5 PROVENANCE MODEL

Four provenance classes are frozen:

- `DECLARATIVE` — source of truth is Challenge Definition / Capa 0 JSON.
- `RUNTIME` — source of truth is Godot telemetry emitted by `[TELEMETRY_JSON]`.
- `ARTIFACT` — source of truth is physical observations from FFprobe/filesystem.
- `DERIVED` — conclusions computed by the factory from primary facts.

Axiom:
**The factory may derive conclusions, but it must never invent or silently mutate primary facts.**

## 4. C5-A CONSISTENCY RULES

The factory verifies:
- `total_frames == hook_frames + game_frames + cta_frames`
- FFprobe frame count equals telemetry `total_frames`
- FFprobe duration matches `total_frames / declared_fps` within 0.05 s
- FFprobe `r_frame_rate` equals declared FPS representation

Hard-coded 660/11.0 expectations were removed from the consistency gate.

## 5. C5-C SHA-256

Unit manifests now contain:

```json
"artifacts": {
  "raw_video": "CHALLENGE_XXX_raw.avi",
  "raw_video_sha256": "<sha256>",
  "final_video": "CHALLENGE_XXX.mp4",
  "final_video_sha256": "<sha256>"
}
```

The batch audit recomputes both hashes from disk and fails with:
`UNIT_ARTIFACT_HASH_MISMATCH`
when the declared hash differs from the current file.

## 6. C5-D DISK-BASED SSOT

The batch manifest is built only after post-auditing the persisted unit manifests.
The audit checks:
- coverage
- unit manifest existence
- unit certification
- challenge identity
- declarative provenance
- artifact existence
- artifact hash integrity

The global manifest is published atomically.

## 7. EXPLICITLY DEFERRED HARDENING

`C5-C2 — Manifest Self-Integrity` is intentionally NOT implemented.

It is deferred because it is not required to validate or build the first playable product. Do not open C5-C2 automatically.

## 8. C6 OBJECTIVE

The engineering objective now changes from infrastructure hardening to **first playable content**.

First target:
`PARKING_V2`

Goal:
Generate the first actual vertical short-form game/video that visually demonstrates the already-certified mechanic.

The first prototype must prove the translation:

`SimulationResult.frames`
→ visual presentation
→ challenge interaction
→ winning-frame reveal
→ CTA
→ MP4 artifact

## 9. C6-A CONSTRAINTS

C6-A must not:
- rewrite RNG architecture
- alter C3 lifecycle contracts
- weaken C4 validation
- bypass the factory
- add mechanic-specific hardcoding to the Composition Root
- introduce unnecessary production infrastructure

C6-A should prefer minimal presentation assets and existing pipeline infrastructure.

## 10. FIRST PLAYABLE CONTENT CONTRACT

Initial presentation concept:

HOOK:
`🚗 APARCA EL COCHE`

GAME:
Vehicle follows the deterministic PARKING_V2 trajectory.

INTERACTION:
Viewer attempts to stop the video at the correct moment.

REVEAL:
`✅ ¡APARCADO!` / `❌ CASI`

CTA:
`¿Lo has clavado?`

The visual layer must consume the simulation output rather than reimplement its mathematics.

## 11. NEXT WINDOW — FIRST ACTION

Before coding:
1. Reconcile the post-C5 source snapshot against this handover.
2. Audit the current Godot scene and presentation nodes.
3. Map `SimulationResult.frames` to the existing scene/timeline without changing the simulation contract.
4. Design the minimum C6-A presentation contract.
5. Only then implement the smallest visual prototype.

## 12. DO NOT ASSUME

The following are NOT established merely because they were proposed in discussion:
- completed freeze/reveal animation
- final visual assets
- final 9:16 art direction
- exact node hierarchy for C6
- platform-specific export settings
- C5-C2 manifest self-hashing

These remain C6 design/implementation work.
