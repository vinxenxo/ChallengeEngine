# ARCHITECTURE_V0.1.md — Plano técnico y flujo de datos del motor

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