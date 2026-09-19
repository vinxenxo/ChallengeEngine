# Project Overview

## Mission

ChallengeEngineV01_STATELESS is a deterministic challenge/video factory. It separates declarative content, deterministic simulation, passive presentation and production orchestration so the visual layer can evolve without changing gameplay truth.

## State at C11 FREEZE

C11 closes the current architectural consolidation. The repository now has one social output structure shared by challenge and visual content:

- Header: 0..144 px
- Body: 144..816 px
- Footer: 816..960 px
- Output: 540x960

The logical simulation canvas remains 1080x1920 where required by the existing mechanics. `CoordinateMapper` performs presentation-space projection; it does not redefine simulation coordinates.

## Frozen pillars

1. Stateless deterministic simulation.
2. Structural RNG ownership is unchanged by presentation.
3. `SimulationResult` is authoritative gameplay truth.
4. Presentation consumes results; it does not calculate them.
5. `RenderedFrameStream` remains the visual runtime contract.
6. Audio is governed by the already-frozen C7 contracts.
7. `artifacts/` is the canonical root for new generated evidence.

## Continuation

The next active scope is C11-C Art Direction. It is intentionally a presentation-only phase.
