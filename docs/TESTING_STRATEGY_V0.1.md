# TESTING_STRATEGY_V0.1.md — Estrategia de Pruebas a 4 Niveles

El Engine no es un juego tradicional, es una factoría de generación masiva. Su validación requiere una pirámide de pruebas estricta.

## 1. Pruebas Unitarias (UNIT)
Evalúan la lógica matemática pura en aislamiento (sin levantar el árbol de escenas).
- **Objetivos:** `ChallengeMechanic.simulate()`, mutación determinista de generadores LCG (`SeedGenerator`), cálculo matemático del `WinningFrameDetector`.
- **Criterio:** El mismo input genera exactamente el mismo `FrameSnapshot[]` o `score`.

## 2. Pruebas de Contrato (CONTRACT)
Garantizan que la Capa 0 (Configuración Declarativa) se comunica correctamente con el Engine.
- **Objetivos:** Parseo de `ChallengeDefinition`, validación de campos obligatorios, asignación correcta de `VideoProfile` (ej. mapeo de `hook_duration` a `hook_frames`).

## 3. Pruebas de Integración (INTEGRATION)
Evalúan el acoplamiento entre el núcleo de simulación (Capa 1) y el motor de render (Capa 2).
- **Objetivos:** `Main.tscn` carga correctamente los `FamilyAssets`. `VideoTimeline` avanza los cuadros físicos en correspondencia exacta con `SimulationResult`. `get_tree().quit()` se ejecuta en el frame delimitado por `total_frames`.

## 4. Pruebas E2E (End-to-End Test / Prueba de Fuego)
Validan la totalidad del pipeline de producción automatizada de la Capa 3.
- **Flujo:** `JSON` $\rightarrow$ `build_factory.py` $\rightarrow$ `Godot headless` $\rightarrow$ `RAW AVI` $\rightarrow$ `FFmpeg` $\rightarrow$ `FINAL MP4` $\rightarrow$ `ffprobe` $\rightarrow$ `manifest.json`.
- **Criterio de Éxito:** Salida limpia `exit 0`, metadatos validados, duración exacta de vídeo, FPS y cumplimiento de las invariantes matemáticas ($f_{\text{winning}}$ dentro del bloque `GAME`).

## Addendum V2.0 — Deterministic Dependency Isolation

The V2.0 test layer adds architectural tests for semantic RNG streams and capability boundaries.

- **K — Capability Intersection:** local scope and Registry authorization must both permit a stream.
- **L1–L4 — Facade Isolation:** structural and cosmetic facades reject opposite-domain or unregistered streams.
- **M — Scope Copy Isolation:** external mutation of the source `allowed_streams` array cannot mutate a capability.
- **N — Registry Definition Isolation:** consumers cannot mutate the Registry's authorized-consumer list through a returned definition.
- **O1–O6 — Facade Equivalence:** all facade sampling operations must return exactly the same value as the underlying `DeterministicLCG` for authorized streams.
- **P — Cosmetic Invariance:** presentation RNG calls and presentation ordering must not alter `SimulationResult`.
- **Q — Structural Reactivity:** a structural trajectory mutation must be observable in the simulation, while cosmetic stream activity must remain observationally irrelevant.

The V2.0 pilot fixture is `CHALLENGE_003` / `PilotMechanic`.
