# TESTING_STRATEGY_V0.1.md — Estrategia de Pruebas a 4 Niveles

> **Live-state rule:** This older section is retained as historical checkpoint evidence. The latest "Current Live" section in this document is authoritative for the present repository.

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

## Historical V2.0 Testing Status — CHECKPOINT 0.3.6

The historical V0.1 test strategy remains unchanged as a record of the original contract. The live V2.0 testing surface now includes:

### Deterministic RNG suite

`tests/DeterministicLCGStatelessTest.gd` validates legacy sequence equivalence, referential repetition, reordering, stream isolation, absence of mutable RNG module state, and regression fixtures.

### RNG architecture suite

`tests/RNGArchitectureTest.gd` validates capability construction, domain separation, registry authorization, scope immutability, facade equivalence, error-state coherence, error bubbling, and the production Parking stream registry.

### Pilot DDI suites

`tests/PilotMechanicIsolationTest.gd` and `tests/PilotMechanicDDIHardeningTest.gd` validate cosmetic invariance, structural reactivity, stream independence and execution-order resilience for the laboratory fixture.

### Parking V2 isolation suite

`tests/ParkingMechanicV2IsolationTest.gd` validates:

- capability creation for streams 30/40/50/60;
- exact 420-frame contract;
- repeatability;
- cosmetic invariance;
- structural stream independence;
- direct structural reactivity via `PARKING_STEERING_NOISE`;
- runtime error bubbling and rejection of partial results.

The suite has been validated in the working Godot 4.7.1 environment with `[PARKING_V2_ISOLATION_SUITE] PASS`.

### Integration testing still pending

The Parking V2 isolation result does **not** yet certify global pipeline integration. CHECKPOINT 0.3.6 must additionally prove that `MechanicRegistry` resolves `parking_v2`, `GeneradorMaestro` injects its capability per attempt, RNG failures stop downstream processing, and V1.0 fixtures remain unchanged.

---

## Current Live Testing Strategy — CHECKPOINT 1.1.0-C6-D4

The external `tests/run_suite.py` remains the suite-level arbiter. It treats runtime/script errors as fatal and requires accepted PASS markers.

The external `tests/run_all.py` is the current corpus runner. It discovers every `*Test.gd` under `tests/` and requires explicit registration plus a PASS marker. The present source corpus contains suites for HIT, CATCH, FIND, Parking V2, Pilot/DDI, RNG architecture, and `choose_v1`.

Current registered corpus includes:

```text
HIT_V1_ISOLATION
CATCH_V1_ISOLATION
CATCH_PRESENTATION_CONTRACT
CHOOSE_V1_ISOLATION
FIND_V1_ISOLATION
PARKING_V2_ISOLATION
PILOT_ISOLATION
DDI_R1
RNG_TEST_SUITE
RNG_ARCHITECTURE_SUITE
```

The C6-D4 production gate is pending physical certification because this environment has no Godot executable. The static phase-duration contract is already passing for the five requested fixture combinations.

Batch certification requires the nine challenge definitions, Godot 4.7.1, FFmpeg and FFprobe, with manifest/frame-count agreement checked before release freeze.
