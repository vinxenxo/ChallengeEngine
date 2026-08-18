# ROADMAP_PHASES.md — Estado de Fases y Progreso de Desarrollo

## Estado General
- **Versión del Engine:** Core V0.1
- **Entorno de Ejecución:** Godot 4.7.1.stable.mono.official.a13da4feb
- **FASE 1.0 (Infraestructura y Pipeline):** COMPLETADA Y CONGELADA
- **FASE 1.1 (Endurecimiento de Contrato Temporal y Coordenadas):** COMPLETADA Y CONGELADA
- **Estado Actual:** LISTOS PARA FASE 1.2

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