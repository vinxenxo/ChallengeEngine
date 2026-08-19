# ROADMAP_PHASES.md — Estado de Fases y Progreso de Desarrollo

## Estado General
- **Versión del Engine:** Core V0.1
- **Entorno de Ejecución:** Godot 4.7.1.stable.mono.official.a13da4feb
- **FASE 1.0 (Infraestructura y Pipeline):** COMPLETADA Y CONGELADA
- **FASE 1.1 (Endurecimiento de Contrato Temporal y Coordenadas):** COMPLETADA Y CONGELADA
- **Estado del documento histórico V0.1:** las fases 1.0–1.2 documentadas aquí pertenecen al baseline congelado; el estado vivo se registra en el bloque "V2.0 Checkpoint Track" más abajo.

---

## Detalle de Sub-fases

### 🟢 FASE 1.0: Pipeline Base End-to-End
- [x] Separador CLI `--`, `--fixed-fps`, `--quit-after`, `--validate-only`.
- [x] Orquestador Python con hilos asíncronos para I/O.
- [x] Transcodificación FFmpeg (YUV420p) y generación de `manifest.json`.

### 🟢 FASE 1.1: Contrato Temporal y Coordenadas de Frame
- [x] Desacoplamiento de `winning_frame` (Relativo a GAME) y `absolute_winning_frame` (Absoluto Vídeo).
- [x] Ventana temporal explícita en `ChallengeValidator` ($[\text{hook\_frames}, \text{hook\_frames} + \text{game\_frames})$).
- [x] Sanitización del contador `attempts` (base 1).
- [x] Emisión de telemetría completa de timeline (`total_frames`, `hook_frames`, `game_frames`, `cta_frames`).
- [x] Verificación física E2E aprobada con salida `[TELEMETRY_JSON]`.

---
## Resumen de Logros de la FASE 1.2
- [x] **Capa 0 Protegida:** `ChallengeDefinitionValidator` bloquea JSONs malformados o temporización negativa antes de simular.
- [x] **Capa 1 Protegida:** `SimulationResult` exige integridad absoluta ($N$ snapshots exactos no nulos ni corruptos).
- [x] **Salida de Errores Estructurada:** Invocación de `emit_engine_error()` emitiendo `[ERROR_JSON]` capturable por la factoría de Python.
- [x] **Batería de Testing Defensivo Aprobada:** Pasados con éxito los 4 escenarios de fallo en terminal.

---

### ⚪ FASE 2: Extensión de Mecánicas Complejas
- [ ] Desarrollo de `ParkingMechanic.gd` (DODGE / SAVE / CONTROL).

## V2.0 Checkpoint Track — Current State

The V2.0 work is tracked independently from the historical V0.1 phase labels above.

### CHECKPOINT 0 — Baseline V0.1
- [x] Frozen and validated.

### CHECKPOINT 0.1 — Stateless RNG
- [x] Stateful LCG migrated to pure stateless sampling.
- [x] Historical `CHALLENGE_001` and `CHALLENGE_002` preserved under `rng_version: "1.0"`.
- [x] Godot 4.7.1 headless regression validated.

### CHECKPOINT 0.2.1 — Semantic Streams and DI Infrastructure
- [x] `RNGStreamDefinition`.
- [x] `RNGStreamRegistry`.
- [x] `StructuralRNG` / `CosmeticRNG`.
- [x] `MechanicRNGContext` / `PresentationRNGContext`.
- [x] Composition Root integration.
- [x] Architecture suite and historical regressions validated.

### CHECKPOINT 0.2.2 — Pilot Mechanic
- [x] Mathematical contract frozen.
- [x] `PilotMechanic` implemented as a V2.0 laboratory fixture.
- [x] `CHALLENGE_003.json` added.
- [x] Tests P/Q prepared for headless execution.
- [ ] Godot 4.7.1 execution and regression certification pending.

The next engineering step after certification is to freeze the Pilot fixture and use the proven semantic-stream architecture for a production-grade V2.0 mechanic.

## Current V2.0 Checkpoint Track — CHECKPOINT 0.3.6

The original Phase 1.x labels above are retained as historical baseline documentation. The live V2 development sequence is:

```text
0       Baseline V0.1                         FROZEN
0.1     Stateless RNG                         FROZEN / VALIDATED
0.2.1   Semantic Streams + DI                 FROZEN / VALIDATED
0.2.2   PilotMechanic + CHALLENGE_003         FROZEN / VALIDATED
0.2.2-R1 DDI Hardening + error bubbling       FROZEN / VALIDATED
0.3.1   Parking V2 mathematical contract      FROZEN
0.3.2   Production stream registry            FROZEN / VALIDATED
0.3.3   Semantic index contract               FROZEN
0.3.4   CHALLENGE_004                         FROZEN
0.3.5   ParkingMechanicV2 isolation           FROZEN / VALIDATED
0.3.6   Composition Root integration          OPEN
```

### 0.3.6 objective

Integrate `parking_v2` into the production pipeline without altering V1.0 mechanics or fixtures.

The intended change surface is `MechanicRegistry.gd` + `GeneradorMaestro.gd` + integration tests.
