# START PROMPT — Next Window — C11-C ART DIRECTION

You are continuing `ChallengeEngineV01_STATELESS` after **C11 FREEZE**.

## Continuity

The authoritative state is the live repository sealed by C11 and the companion `MASTER_HANDOVER_C11_FREEZE.md`. Do not use older ZIPs or historical transcripts as implementation authority.

## C11 is frozen

The following are closed unless a new checkpoint explicitly reopens them:

- simulation mathematics
- RNG architecture/ownership
- mechanic contracts and native durations
- `SimulationResult` semantics
- winning-frame computation
- `RenderedFrameStream`
- visual loop/drill mathematics
- canonical visual content envelope
- C7 audio contracts
- C9 authoring contracts
- test/regression architecture

## Active scope: C11-C

C11-C is **presentation art direction only**. The product owner will provide reference images showing the desired generated look. Your job is to translate those references into presentation architecture and assets while preserving the frozen simulation outputs.

## Fixed social structure

Canvas: 540x960

- HEADER: y=0..144
- BODY: y=144..816
- FOOTER: y=816..960

`UnifiedSocialFrame` remains the structural shell. `CoordinateMapper` and `PresentationFramer` remain the geometry boundary.

## Working principles

1. Inspect the current implementation before proposing changes.
2. Contract before code.
3. Separate visual style from simulation truth.
4. Do not move gameplay objects by altering mechanics; change presentation mapping or visual composition.
5. Keep deterministic outputs deterministic.
6. Preserve existing tests before adding new visual tests.
7. Prefer additive presentation abstractions over special cases per mechanic.
8. Every visual reference must be translated into explicit, testable presentation decisions.

## First task in the window

Before coding, inventory the current presentation stack and classify each requested visual characteristic as one of:

- structural layout
- typography/text
- asset treatment
- color/background
- object presentation
- animation/rendering polish
- production/export concern

Then propose the smallest presentation-only contract needed to implement the reference style.

## Freeze rule

If a requested visual effect appears to require changing simulation data, RNG, winning-frame calculation or a frozen content contract, stop at the boundary and treat that as a new checkpoint request rather than silently modifying C11.
