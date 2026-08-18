# MECHANICS_SPECIFICATION.md — Taxonomía de mecánicas y familias base

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