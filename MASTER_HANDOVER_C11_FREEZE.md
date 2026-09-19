# MASTER HANDOVER — ChallengeEngineV01_STATELESS — C11 FREEZE

**Checkpoint:** C11
**Status:** CLOSED / CERTIFIED / FROZEN
**Purpose:** authoritative continuity document for all future sessions

## 1. Source of truth

The live repository at the sealed C11 state is the source of truth. Historical ZIPs, transcripts and prior prompts are continuity aids only. The machine-readable freeze certificate and SHA-256 manifest identify the exact sealed state.

## 2. What C11 accomplished

C11 introduced and validated a unified social presentation structure without changing deterministic simulation truth. The shared output frame is 540x960:

- Header: 0..144
- Body: 144..816
- Footer: 816..960

`UnifiedSocialFrame` provides the structure. `CoordinateMapper` projects logical simulation geometry into Body space. `PresentationFramer` makes framing policy explicit.

## 3. Frozen simulation boundary

Do not modify in C11-C:

- mechanic mathematics
- deterministic RNG architecture or ownership
- native challenge durations
- `SimulationResult` semantics
- winning-frame calculation
- `close_calls` semantics
- visual loop/drill generator mathematics
- `RenderedFrameStream`
- canonical visual content envelope
- C7 audio contracts
- C9 authoring contracts

## 4. Validation record supplied for the freeze

- Logical corpus: 103/103 PASS
- C11-A: 54/54
- C11-A.1: 54/54
- Retro: 54/54 telemetry + A/B checks
- Stress: 288 cases / 576 executions / repeat 2
- Physical smoke: 2/2
- QA video matrix: 54/54 video renders

The video matrix is video-only by design. Its internal C7-A2 mixed-audio gate is out of scope; the C7-A2 production rule itself remains frozen and authoritative.

## 5. Artifact policy

`artifacts/` is the canonical home for new QA, regression, test and production evidence. Old roots are historical until explicitly migrated and verified. Never silently delete historical evidence to make a freeze look clean.

## 6. Next active scope

### C11-C — Art Direction

Use the user-provided reference images to refine presentation. Preserve the frame geometry, rendering/data flow and simulation boundaries. Visual changes are welcome; gameplay truth is not to be re-authored as a side effect.

### C11-D/E

After art direction, complete final export and distribution metadata.

## 7. Continuity protocol

At the beginning of a future session:

1. Read this handover.
2. Read `docs/00_PROJECT_OVERVIEW.md` through `docs/06_ROADMAP.md`.
3. Read `docs/c11-freeze/13_ARCHITECTURE_MANIFESTO.md`.
4. Read the machine-readable C11 certificate and SHA-256 manifest in `artifacts/tests/reports/`.
5. Treat the repository itself as authoritative.
6. Do not reopen closed checkpoints unless explicitly instructed.

## 8. Final engineering rule

Do not improve the engine merely because an improvement seems attractive. C11 exists to make the stable boundary stronger than the temptation to change it.
