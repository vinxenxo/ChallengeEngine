# DATA_MODEL_V0.1.md — Especificación de Modelos y Contratos de Datos

## 1. JSON Declarativo (Entrada Externa)
Contrato estándar para la definición de un challenge (`/challenges/*.json`):

```json
{
  "id": "CHALLENGE_001",
  "engine_version": "0.1",
  "mechanic": "key",
  "mechanic_version": "1.0",
  "video": {
    "fps": 60,
    "hook_duration": 3.0,
    "game_duration": 7.0,
    "cta_duration": 1.0
  },
  "difficulty": {
    "level": 5,
    "tolerance": {
      "rotation_deg": 4.5
    }
  },
  "generation": {
    "seed": 193847
  },
  "assets": {
    "background_path": "res://assets/families/fam_001/bg.png",
    "target_path": "res://assets/families/fam_001/target.png",
    "object_path": "res://assets/families/fam_001/key.png"
  },
  "content": {
    "hook": "¡SOLO EL 1% LLEGA AL CENTRO!",
    "cta": "¡INTÉNTALO TÚ TAMBIÉN!"
  }
}

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

## Current Live Data Contract — V2.0

Historical examples in the V0.1 section are retained as historical examples. Current challenge files use the established schema/version fields and the following live V2.0 pattern where applicable:

```json
"mechanic": "parking_v2",
"mechanic_version": "2.0",
"generation": {
  "seed": 314159,
  "rng_version": "2.0"
}
```

`CHALLENGE_001` and `CHALLENGE_002` remain `rng_version: "1.0"`. `CHALLENGE_003` through `CHALLENGE_009` use `rng_version: "2.0"` in the current corpus.

The temporal model is declarative per challenge: HOOK, GAME, REVEAL and CTA durations are resolved independently at the configured FPS. Duration 0 omits a phase; GAME must remain > 0. The historical 2 s HOOK + 7 s GAME + 2 s CTA = 11 s / 660 frames @ 60 FPS remains a reference profile, not a global duration limit.

---

## Historical Data Contract — CHECKPOINT 0.9.0

That fixed 660-frame profile is historical. Current C6-D4 timing is declarative per challenge: `hook_frames + game_frames + reveal_frames + cta_frames`, with `GAME > 0` and zero-duration phases omitted.

`SimulationResult.winning_frame` is GAME-relative. The absolute presentation frame is derived by adding `hook_frames`.

### Production provenance

Unit manifests now carry:

```text
manifest_version
factory_version
challenge_id
declarative_metadata
telemetry
artifacts
validation
status
```

`declarative_metadata` is a verbatim snapshot of declared provenance keys; runtime and artifact measurements remain in their own sections.

### Legacy fixture policy

`CHALLENGE_005` and `CHALLENGE_006` deliberately demonstrate incomplete historical metadata. The manifest preserves those absences rather than inventing values.
