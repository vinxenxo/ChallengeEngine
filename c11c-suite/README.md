# C11-C / C11-D Suite — 0.1.4 / Active Operator Surface

`c11c-suite` is the canonical GUI/CLI operator shell for `ChallengeEngineV01_STATELESS`.

## Surfaces

- `c11c-test` — logical regression, QA and focused acceptance.
- `c11c-catalog` — artifact browsing and metadata inspection.
- `c11c-maintenance` — documentation consolidation, repository organization, cleanup and freeze packaging.
- `c11c-config` — declarative configuration inspection/editing.
- `c11c-producer` — audiovisual orchestration for Challenges, Visual Loops and Visual Drills.
- `c11d-control` — integrated C11-D operator control center. This is the active home for D-branch integration/evolution.

## D9 integration rule

The D control center is a thin operator layer. It reads canonical receipts and launches canonical D runners; it does not implement simulation, RNG, rendering, audio generation or release logic.

The historical Studio specifications are treated as architecture/UX requirements for a unified operator surface. Their useful concepts are being adopted inside this canonical Suite rather than creating a parallel operator root.

## Current D state

- D0–D8: accepted according to their governed checkpoints.
- D9.0–D9.4: PASS; D9.4 is a valid real-media acceptance checkpoint.
- D9: ACTIVE because full Suite integration and real GUI acceptance remain outstanding.
- D4.8: BLOCKED by policy.
- release authority: NONE.
- D10: BLOCKED until D9 GUI certification.

## Operator parity

The Suite does not own an alternative backend. GUI actions launch the same canonical scripts used directly from the repository. During D, GUI and CLI remain co-equal orchestration surfaces.

## Current versions

- Suite application: **0.1.4**
- Producer: **0.9.7**
- C11-C baseline: **2.19.12 FROZEN**
- C11-D: **D9 ACTIVE / GUI integration**
- Godot: **4.7.1 stable Mono**

## Boundary

C11-C simulation/mechanics/RNG, `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, C7/C9 contracts and logical 540×960 geometry remain protected.
