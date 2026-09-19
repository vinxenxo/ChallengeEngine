# C11 Architecture Manifesto

## Purpose

C11 establishes a stable social-video presentation boundary around a deterministic simulation core. Its purpose is to let visual composition evolve without redefining gameplay truth.

## The invariant pipeline

```text
Declarative Definition
        │
        ▼
Deterministic Simulation
        │
        ├── SimulationResult
        ├── FrameSnapshots
        └── WinningFrame
        │
        ▼
CoordinateMapper / PresentationFramer
        │
        ▼
UnifiedSocialFrame
        │
        ├── HEADER 0..144
        ├── BODY   144..816
        └── FOOTER 816..960
        │
        ▼
Passive Renderers / RenderedFrameStream
        │
        ▼
Movie Maker / FFmpeg / Production
```

## Simulation truth

Simulation owns gameplay state, RNG consumption, timing semantics, validation and winning-frame truth. Presentation reads verified results; it does not calculate gameplay outcomes and does not consume structural RNG.

## CoordinateMapper

`CoordinateMapper` is the explicit projection layer between the logical simulation canvas and the social presentation body. The simulation canvas remains independent of the social frame. Mapping is a presentation transform and must not mutate source simulation coordinates.

The C11-B social canvas is 540×960. The body region is 540×672 at Y=144. Logical gameplay is projected into that body while preserving aspect ratio and centering policy.

## PresentationFramer

`PresentationFramer` owns framing policy: safe areas, body geometry and the rules that determine how a verified render model is placed inside the social frame. It must remain passive with respect to gameplay truth.

## UnifiedSocialFrame

`UnifiedSocialFrame` is a structural container, not a gameplay system. It owns the stable Header / Body / Footer regions and provides presentation attachment points. Text roles, art direction and styling may evolve in later checkpoints without changing the region contract.

## RenderedFrameStream

The visual runtime remains a sequential stream of verified frames. A renderer may make those frames attractive, branded or legible, but it cannot add gameplay state, recalculate trajectories or rewrite frame indices.

## Art direction boundary

C11-C may change:

- artwork and backgrounds;
- typography;
- palette, gradients and surface treatment;
- visual hierarchy;
- passive renderer styling;
- presentation-only emphasis.

C11-C may not change merely for visual reasons:

- mechanic equations;
- RNG algorithm, version or ownership;
- challenge timing truth;
- `SimulationResult`;
- winning-frame detection;
- canonical visual envelope semantics;
- `RenderedFrameStream` semantics;
- C7 audio contracts;
- C9 authoring contracts.

## Why this boundary exists

The engineering objective is reproducibility under change. If art direction changes, the correct response is to adapt the presentation layer to the verified gameplay result. The correct response is not to change gameplay until a screenshot looks convenient.
