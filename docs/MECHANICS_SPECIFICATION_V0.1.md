# MECHANICS_SPECIFICATION.md — Taxonomía de mecánicas y familias base

> **Live-state rule:** This older section is retained as historical checkpoint evidence. The latest "Current Live" section in this document is authoritative for the present repository.

## 1. Clasificación en 6 Familias Fundamentales

El motor no implementa minijuegos aislados; construye **Familias Matemáticas Base** reutilizables sobre las que se aplican diferentes configuraciones y familias de assets.

                     ChallengeMechanic
                            │
   ┌───────────┬────────────┼────────────┬───────────┬───────────┐
   ▼           ▼            ▼            ▼           ▼           ▼
HitMechanic CatchMechanic DodgeMechanic MatchMechanic FindMechanic JackpotMechanic


---

## 2. Matriz de Familias Base

| Familia Base | Dominio Semántico (`custom_data`) | Ejemplo de Expresión Visual |
| :--- | :--- | :--- |
| **HIT** | `success_distance`, `velocity`, `impact_alignment` | Llave en cerradura, Flecha en diana, Penalti |
| **CATCH** | `containment_ratio`, `overlap_area`, `distance` | Pez en anzuelo, Huevo en cesta, Mariposa en red |
| **DODGE / SAVE** | `trajectory_progress`, `collision_clearance`, `safe_zone` | Aparcar coche, Esquivar precipicio, Cruzar laberinto |
| **MATCH** | `match_score`, `state_difference` | Alineación de patrones, Coincidencia de color |
| **FIND** | `visibility_state`, `object_position` | Detección de objeto oculto en cuadro |
| **JACKPOT** | `symbol_combination`, `matching_symbols` | Tragaperras, Rodillos giratorios, Ruleta |

---

## 3. Implementaciones concretas de referencia

### A. `KeyMechanic.gd` (Mecánica de prueba V0.1)
- **Familia:** HIT (Ángulo Relativo).
- **Simulación:** Oscilación caótica en memoria alrededor de cero.
- **Métricas:** `custom_data["success_distance"]` = $\lvert \text{angle} \rvert$, `custom_data["velocity"]` = $\lvert \text{angular\_velocity} \rvert$.

### B. `ParkingMechanic.gd` (Mecánica objetivo V0.2)
- **Familia:** DODGE / SAVE (Espacio 2D Continuo).
- **Simulación:** Generación procedural de trayectoria continua hacia la plaza ($X, Y$) con aceleraciones, curvas y frenazos.
- **Métricas:** `custom_data["success_distance"]` = $\text{distance\_to}(\text{target\_slot})$, `c

## 4. PilotMechanic V2.0 — Fixture de Laboratorio

`PilotMechanic` no constituye una nueva familia matemática. Es un fixture controlado para validar la arquitectura de RNG V2.0.

- **Versión:** 2.0
- **Capability:** `MechanicRNGContext`
- **Consumer:** `PilotMechanic`
- **Streams:** `TRAJECTORY` (10) y `CONTROL` (20)
- **Índice:** `frame_number`
- **Modelo:** función pura por frame, sin acumulación de estado entre frames.
- **Salida:** `FrameSnapshot[]` con `success_distance`, `velocity`, `target_x`, `base_x`, `trajectory_noise` y `control_offset`.

El fixture existe exclusivamente para demostrar que llamadas de Presentation/Cosmetic RNG no pueden alterar `SimulationResult`, mientras que una mutación estructural sí puede alterar el resultado.

## Historical V2.0 Status — CHECKPOINT 0.3.6

The six mathematical families remain the engine taxonomy:

- `HIT`
- `CATCH`
- `DODGE / CONTROL`
- `MATCH`
- `FIND`
- `JACKPOT`

Themes such as `retro_8bit_arcade`, `garage`, `sports`, `fantasy` and `scifi` remain content/presentation classifications, not new mathematical families.

### Implemented V2.0 fixtures

`PilotMechanic` is the controlled DDI laboratory fixture. `ParkingMechanicV2` is the first production-oriented V2.0 mechanic and belongs to `DODGE / SAVE / CONTROL`.

`ParkingMechanic.gd` remains the frozen V1.0 oracle. `ParkingMechanicV2.gd` is a parallel implementation and must not replace or alter the V1.0 class during CHECKPOINT 0.3.6.

### Parking V2 production streams

`PARKING_DODGE_OFFSET`, `PARKING_SAVE_OFFSET`, and `PARKING_OVERSHOOT` are generation parameters sampled at index `0`. `PARKING_STEERING_NOISE` is sampled per frame at `f*2` and `f*2+1`.

---

## Current Live Mechanics Status — CHECKPOINT 0.9.0 / 1.0.0

The historical taxonomy remains useful as a design vocabulary, but the implementation status is now:

| Identifier | Role | Status |
|---|---|---|
| `key` | legacy HIT fixture | FROZEN |
| `parking` | legacy DODGE/SAVE fixture | FROZEN |
| `pilot` | RNG laboratory fixture | FROZEN |
| `parking_v2` | production DODGE/SAVE V2 | FROZEN |
| `hit_v1` | sovereign HIT family | FROZEN |
| `catch_v1` | sovereign CATCH family | FROZEN |
| FIND | new family candidate | 1.0.0 CONTRACT DRAFT |
| MATCH | candidate rejected for 1.0.0 | NOT SELECTED |

FIND is intentionally not a CATCH reskin: distractors must participate in its mathematical difficulty. The exact false-positive event semantics remain open in the FIND contract draft.
