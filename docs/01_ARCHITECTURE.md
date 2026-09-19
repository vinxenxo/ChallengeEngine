# Architecture

## Layer model

### Capa 0 — Definitions

Declarative JSON definitions, challenge definitions, visual definitions and profiles. They express author intent and parameters; they are not mutable runtime truth.

### Capa 1 — Deterministic simulation

Mechanics consume definitions plus explicitly owned RNG capabilities. Simulation produces reproducible frame state and outcome data. Gameplay truth is represented by the established simulation result/frame snapshot contracts.

### Capa 2 — Passive presentation

Presentation consumes verified runtime output and decides how that output is framed, styled and rendered. It must not recalculate mechanics, RNG or the winning frame.

### Capa 3 — Production orchestration

Authoring adapters, batch generation, Movie Maker, FFmpeg/FFprobe, artifact manifests, QA and release gates coordinate the pipeline without becoming a hidden source of gameplay truth.

## Core invariants

- Structural RNG and cosmetic/presentation RNG remain separated.
- `winning_frame` is the temporal anchor.
- `close_calls` is an episode/count metric, not a timing primitive.
- `RenderedFrameStream` is consumed by presentation; presentation does not regenerate it.
- `UnifiedSocialFrame` owns social structure, not simulation.
- `CoordinateMapper` changes presentation coordinates only; it does not change logical simulation coordinates.

## Runtime flow

```text
Definition
   ↓
Deterministic simulation
   ↓
SimulationResult / FrameSnapshot
   ↓
RenderedFrameStream
   ↓
CoordinateMapper / PresentationFramer
   ↓
UnifiedSocialFrame
   ↓
Passive renderer / UI
   ↓
Movie Maker / production pipeline
```

## Production flow

```text
Canonical definition
   ↓
Authoring / validation
   ↓
build_factory.py
   ↓
Godot runtime
   ↓
Movie Maker
   ↓
AVI / FFmpeg / MP4 / FFprobe
   ↓
Manifest + release validation
```

## C11-C boundary

C11-C is presentation-only art direction. It may alter approved visual assets, typography, styling, hierarchy, backgrounds/foregrounds and renderer appearance. A change that affects simulation semantics, RNG, canonical data, timing truth or frozen test contracts requires a new checkpoint rather than being hidden inside an art-direction change.
