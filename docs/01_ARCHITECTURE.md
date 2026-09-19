# Architecture

## Layer model

### Capa 0 — Definitions
Declarative challenge/visual definitions. No runtime simulation state is stored here.

### Capa 1 — Deterministic simulation
Mechanics consume explicit definitions and deterministic RNG streams. The result is authoritative and reproducible from the same inputs.

### Capa 2 — Presentation
Presentation maps simulation output into screen geometry, timelines, assets, text and rendering. It is passive with respect to gameplay.

### Capa 3 — Production orchestration
Authoring, batch generation, Movie Maker export, FFmpeg/FFprobe, manifests and QA automation.

## Key invariants

- Presentation cannot calculate a winning frame.
- Presentation cannot regenerate mechanics.
- Presentation cannot consume structural RNG.
- `winning_frame` is the temporal anchor for challenge reveal logic.
- `close_calls` represents an episode count, not a timing signal.
- The social frame is structural; content roles remain content-driven.

## Freeze boundary

C11 freezes the interfaces between these layers. Future art-direction work should modify presentation assets, style and composition choices only, unless a new checkpoint explicitly reopens a frozen contract.
