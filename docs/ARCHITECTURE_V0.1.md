# ARCHITECTURE_V0.1.md — Plano técnico y flujo de datos del motor

> **Live-state rule:** This older section is retained as historical checkpoint evidence. The latest "Current Live" section in this document is authoritative for the present repository.

## Diagrama de Flujo Unificado

                ┌──────────────────────┐
                │ Challenge JSON       │
                │ Declarative Config   │
                └──────────┬───────────┘
                           │
          ┌────────────────┼────────────────┐
          │                │                │
          ▼                ▼                ▼
     Generation        Mechanic       Video Profile
          │                │                │
          └───────────────┼────────────────┘
                          ▼
               ┌─────────────────────┐
               │ Simulation Core     │
               │                     │
               │ deterministic       │
               │ frame generation    │
               └──────────┬──────────┘
                          │
                          ▼
               FrameSnapshot[]
                          │
             ┌────────────┴────────────┐
             ▼                         ▼
    WinningFrameDetector        Validator
             │                         │
             └────────────┬────────────┘
                          ▼
                 SimulationResult
                          │
                          ▼
                  VideoTimeline
                          │
                          ▼
                  Presentation
                          │
                          ▼
               Godot Movie Maker
                          │
                          ▼
                      RAW AVI
                          │
                          ▼
                       FFmpeg
                          │
          ┌───────────────┴──────────────┐
          ▼                              ▼
       FINAL MP4                    MANIFEST

## Flujo en Segundo Plano (Python Orchestrator)

             PYTHON FACTORY (build_factory.py)
                   │
   ┌───────────────┼────────────────┐
   ▼               ▼                ▼
Launch          Telemetry        FFmpeg
Godot           Capture          Pipeline
(Headless)      (Async I/O)       (YUV420p)
│               │                │
└───────────────┴────────────────┘
│
▼
Artifacts (.mp4 / _manifest.json)

### Convención Oficial de Coordenadas de Frame (Capa 1 vs. Capa 2/3)

1. `SimulationResult.winning_frame` (Capa 1 - Simulación Pura):
   - **Ámbito:** Relativo exclusivamente al bloque `GAME`.
   - **Rango Válido:** [0, game_frames - 1]

2. `ValidationResult.absolute_winning_frame` (Capa 1 - Validador):
   - **Ámbito:** Frame absoluto dentro del vídeo completo.
   - **Fórmula:** absolute_winning_frame = result.winning_frame + hook_frames
   - **Rango Válido (Ventana Permitida):** [hook_frames, hook_frames + game_frames - 1]

3. `Telemetry` (Salida JSON):
   - `"winning_frame_game"`: Frame relativo al bloque GAME.
   - `"winning_frame"`: Frame absoluto del vídeo (usado por la Capa de Presentación/Render).
   - `"winning_frame_in_valid_window"`: Bool que certifica que el frame cae estrictamente en la ventana.

## Addendum V2.0 — Semantic RNG Streams and Capability Isolation

CHECKPOINT 0.2.1 introduces a deterministic RNG dependency boundary without changing the V1.0 simulation pipeline.

### Composition Root

`GeneradorMaestro` is the Composition Root for RNG V2.0. It creates:

- `RNGStreamRegistry`;
- `StructuralRNG`;
- `CosmeticRNG`;
- `MechanicRNGContext` capabilities for V2.0 mechanics;
- `PresentationRNGContext` capabilities for presentation consumers.

V1.0 mechanics (`key`, `parking`) continue to use their frozen contracts.

### Domain Boundary

`StructuralRNG` accepts only `STRUCTURAL_MAIN` and `STRUCTURAL_SECONDARY` streams. `CosmeticRNG` accepts only `PRESENTATION` and `COSMETIC_CONTENT` streams. A cosmetic component must never inject data into `SimulationResult`.

`DeterministicLCG` remains a pure mathematical primitive and knows nothing about mechanics, presentation, ownership, or challenge semantics.

### V2.0 Pilot

`PilotMechanic` is the first V2.0 laboratory fixture. It consumes `STREAM_TRAJECTORY` (10) and `STREAM_CONTROL` (20) through `MechanicRNGContext`, using `frame_number` as the semantic index. It has no dependency on presentation systems.

## Historical Architecture Status — CHECKPOINT 0.3.6

The V0.1 architecture above is preserved as historical reference. The live architecture now includes the V2.0 deterministic RNG dependency boundary.

### V2.0 deterministic boundary

`DeterministicLCG` is now a stateless mathematical primitive. Its public sampling contract is:

```text
sample_integer(seed, stream_id, index)
sample_float(seed, stream_id, index)
sample_float_range(seed, stream_id, index, min, max)
```

The primitive derives a deterministic stream seed for non-zero semantic streams and advances the 31-bit LCG by affine exponentiation. `stream_id = 0` preserves the historical legacy sequence used by RNG v1.0.

### Capability boundary

V2.0 mechanics receive `MechanicRNGContext` capabilities through the Composition Root. Presentation consumers receive `PresentationRNGContext` capabilities. `StructuralRNG` only accepts structural streams and `CosmeticRNG` only accepts presentation/cosmetic streams.

The current Registry contains:

| ID | Stream | Domain | Consumer |
|---:|---|---|---|
| 10 | `TRAJECTORY` | `STRUCTURAL_MAIN` | `PilotMechanic` |
| 20 | `CONTROL` | `STRUCTURAL_MAIN` | `PilotMechanic` |
| 30 | `PARKING_DODGE_OFFSET` | `STRUCTURAL_MAIN` | `ParkingMechanic` |
| 40 | `PARKING_SAVE_OFFSET` | `STRUCTURAL_MAIN` | `ParkingMechanic` |
| 50 | `PARKING_OVERSHOOT` | `STRUCTURAL_MAIN` | `ParkingMechanic` |
| 60 | `PARKING_STEERING_NOISE` | `STRUCTURAL_MAIN` | `ParkingMechanic` |
| 1010 | `PARTICLES` | `PRESENTATION` | `PilotVisuals` |

### Historical integration boundary

`ParkingMechanicV2.gd` exists and is validated in isolation, but `MechanicRegistry.gd` does **not yet** resolve `parking_v2`, and `GeneradorMaestro.gd` currently only has an end-to-end V2 capability path for the Pilot mechanic.

That is the explicit objective of CHECKPOINT 0.3.6. Do not assume global integration is already complete merely because the isolated Parking V2 suite passes.

---

## Current Live Architecture — CHECKPOINT 1.1.0-C6-D4

The historical architecture sections above are preserved. The live pipeline is now:

```text
Challenge JSON
    ↓
Godot validation / deterministic simulation
    ↓
SimulationResult + telemetry
    ↓
Godot Movie Maker (graphical Compatibility renderer)
    ↓
RAW AVI
    ↓
Python build_factory.py 0.10.0
    ↓
FFmpeg H.264 / YUV420p
    ↓
MP4
    ↓
FFprobe
    ↓
unit manifest 1.0 / BATCH_MANIFEST 1.0
```

Factory implementation version: `0.10.0`; manifest schema remains `1.0`.

The architectural law remains:

```text
GODOT CALCULATES & RENDERS RAW
PYTHON ORCHESTRATES
FFMPEG PACKAGES
FFPROBE VALIDATES
```

Checkpoint 1.1.0-C6-D4 adds declarative per-challenge phase duration control while preserving the frozen deterministic simulation/RNG contracts. `VideoTimeline.gd` is the effective presentation timeline source of truth.
