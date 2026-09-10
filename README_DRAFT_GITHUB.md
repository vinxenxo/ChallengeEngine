# ChallengeEngineV01 (DESACTUALIZADO)

Motor determinista para producir vídeos de retos de precisión.

## Current status

The C6-F0.3 foundation branch currently contains the implemented Content Runtime Boundary, with runtime certification still pending on a Godot-equipped environment.

```text
C6-F0.3.1  CLOSED
C6-F0.3.2  CLOSED / CERTIFIED
C6-F0.3.3  CLOSED / CERTIFIED
C6-F0.3.4  CLOSED / CERTIFIED
C6-F0.3.5  IMPLEMENTED / RUNTIME PENDING
```

## Core principles

- Stateless deterministic RNG.
- Semantic RNG stream capabilities remain sovereign to Challenge.
- Pure deterministic simulation is separated from presentation.
- Visual content is not modeled as ChallengeMechanic.
- Runtime routing is exact `(kind, subtype)` and fail-closed.
- Runtime emits logical/render-ready frame state, not encoded video.
- Godot renders RAW; Python orchestrates production; FFmpeg packages; FFprobe validates physical output.

## C6-F0.3 runtime boundary

```text
Domain definition
      ↓
ContentRuntimeRegistry
      ↓
exact (kind, subtype)
      ↓
ContentRuntime
      ├── ChallengeRuntime
      ├── VisualLoopRuntime
      └── VisualDrillRuntime
      ↓
RenderedFrameStream
      ↓
Presentation
      ↓
Rendering
      ↓
Export
```

## Production contract

```text
factory_version  = 0.10.0
manifest_version = 1.0
FPS              = 60 (current Challenge production baseline)
PHASES           = HOOK / GAME / REVEAL / CTA for Challenge
RULE             = 0 frames => phase omitted
GAME             = > 0 for Challenge
```

## Documentation

The cumulative C6-F0.3 foundation record is `docs/C6-F0.3_MULTI-CONTENT-TEMPORAL-RUNTIME-FOUNDATION.md`.
The exact handover is `docs/MASTER_HANDOVER_CHECKPOINT_C6-F0.3.5_IMPLEMENTED_PENDING_EXECUTION.md`.
