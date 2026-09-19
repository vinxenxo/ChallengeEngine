# GOVERNANCE.md — Normas inmutables de ingeniería y arquitectura

> **Live-state rule:** This older section is retained as historical checkpoint evidence. The latest "Current Live" section in this document is authoritative for the present repository.

## 1. Estructura de Capas en 4 Niveles

┌─────────────────────────────────────────────────────────────┐
│ CAPA 0: Declarative Challenge Definition (JSON Input)      │
└──────────────────────────────┬──────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ CAPA 1: Deterministic Simulation Core (CPU / Memory)        │
│         - Mechanics, Detectors, Validators                 │
└──────────────────────────────┬──────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ CAPA 2: Presentation & Movie Maker Rendering (Godot 4)      │
│         - VideoTimeline, Assets Injection                  │
└──────────────────────────────┬──────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────┐
│ CAPA 3: Production Orchestrator & Transcoding (Python/FFmpeg)│
└─────────────────────────────────────────────────────────────┘


1. **Capa 0 (Declarativa):** Expresa intenciones del creador (tiempos, dificultad, semillas, assets). Prohibido incluir lógica de código, rutas absolutas o dependencias con plataformas de destino.
2. **Capa 1 (Simulación Pura):** Ejecución matemática determinista en CPU sin nodos gráficos ni llamadas a viewport. Genera `Array[FrameSnapshot]` y valida la simulación antes de autorizar el renderizado.
3. **Capa 2 (Presentación):** Lectura pasiva de `verified_history`. Avance guiado de forma secuencial por `VideoTimeline` mediante Movie Maker.
4. **Capa 3 (Orquestación):** Manejo asíncrono no bloqueante de I/O en Python, captura de telemetría de consola, codificación FFmpeg y generación del certificado `manifest.json`.

---

## 2. Convenciones de GDScript (Godot 4)
- **Tipado Estático Obligatorio:** Variables, parámetros y retornos deben tiparse explícitamente (`var fps: int = 60`, `func simulate(...) -> SimulationResult`).
- **Uso de `RefCounted`:** Las clases de datos puros (`FrameSnapshot`, `SimulationResult`, `ValidationResult`) heredan de `RefCounted` para optimizar el consumo de memoria sin la sobrecarga del árbol de nodos.

---

## 3. Normas de CLI y Ejecución Headless
- **Separador de Argumentos CLI:** Los parámetros del usuario deben pasarse obligatoriamente tras el separador `--` (ejemplo: `godot --headless ... -- --config=path/file.json`) y recuperarse mediante `OS.get_cmdline_user_args()`.
- **Soberanía Temporal:** El FPS y la duración total son dictados por la configuración e impuestos al ejecutable mediante `--fixed-fps <FPS>` y `--quit-after <TOTAL_FRAMES>`.

---

## 4. Determinismo vs. Reproducibilidad Multimedia
- **Determinismo Lógico:** Misma semilla, algoritmo, configuración y versión del motor producen exactamente la misma secuencia de estados simulados.
- **Reproducibilidad Multimedia:** El vídeo se reproduce de forma coherente bajo un entorno versionado, pero NO se garantiza identidad binaria (*bit-exactness*) del archivo MP4 final entre diferentes plataformas, S.O. o GPUs.
- **Sanitización de `INF`:** Ningún valor infinito o no numérico (`INF`, `NaN`) debe serializarse a

## Historical Governance Status — V2.0 Checkpoint Track (0.3.6)

The following rules are now frozen for V2.0:

1. `DeterministicLCG` is a pure sampling primitive and must not accumulate mutable sequence state.
2. V2.0 mechanics receive RNG through capabilities, not global RNG singletons.
3. Stream IDs must be registered and domain-owned before consumption.
4. `StructuralRNG` and `CosmeticRNG` enforce the structural/presentation boundary.
5. Lower layers detect and carry error state; the Composition Root owns process-level I/O and `[ERROR_JSON]` emission.
6. `CHALLENGE_001` and `CHALLENGE_002` remain frozen V1.0 fixtures.
7. New V2.0 mechanics are introduced in parallel with their legacy counterparts until integration is explicitly certified.
8. `ParkingMechanicV2` is currently isolated and validated, but not yet globally registered/injected. That integration is CHECKPOINT 0.3.6 work.

---

## Current Governance Status — CHECKPOINT 1.1.0-C6-D4

### Frozen production governance

1. The repository is the code authority.
2. Live documentation describes current contracts; historical checkpoint documents remain historical.
3. Capa 0 metadata is never invented by the production factory.
4. `factory_version` and `manifest_version` are separate identities.
5. Mixed RNG 1.0/2.0 batches are valid and remain explicitly partitioned per challenge.
6. Canonical artifacts are isolated under `output/CHALLENGE_XXX/`.
7. The Python runner remains the final suite-level PASS/FAIL arbiter.
8. CATCH presentation transport remains frozen and must not be redesigned for convenience.
9. C6-D4 is presentation-timing work only: zero-duration phases are omitted; deterministic simulation, RNG streams and winning-frame mathematics remain frozen.
10. Final C6-D4 release status requires physical Godot 4.7.1 + FFprobe evidence; static contract PASS is not sufficient for certification.

### Historical 1.0.0 governance gate

A new mathematical family may proceed only through:

```text
AUDIT → CONTRACT → ISOLATION → INTEGRATION → REGRESSION → BATCH → FREEZE
```

No RNG stream may be assigned before the mathematical contract is frozen.
