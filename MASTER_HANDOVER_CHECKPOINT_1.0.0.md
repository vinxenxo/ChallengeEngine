# 🏛️ MASTER HANDOVER: CHECKPOINT 1.0.0 (FROZEN)

**Date:** August 2026
**Project Version:** 1.0.0 (FROZEN)
**Factory Contract:** 0.9.0 (FROZEN)
**Manifest Schema:** 1.0 (FROZEN)
**Godot Engine:** 4.7.1-stable (official)

Este documento certifica el congelamiento del Checkpoint 1.0.0. Establece la línea base de la arquitectura del motor, los contratos de aleatoriedad DDI (Data-Driven Isolation), el pipeline de producción E2E y el estado definitivo de las familias cinemáticas integradas. Todo desarrollo futuro (1.1.0+) asume este estado como inmutable.

---

## 1. Current Frozen State
*   **Project 1.0.0**: Núcleo del motor estabilizado. El Composition Root (`GeneradorMaestro.gd`) gestiona el ciclo de vida por reintento (seed/attempt).
*   **Factory 0.9.0**: Generador batch de producción validado y congelado en la fase anterior. No asume la versión del proyecto.
*   **Manifest 1.0**: Contrato de trazabilidad JSON inmutable.
*   **Corpus E2E**: 7 de 7 desafíos validados, superando la pipeline E2E desde `CHALLENGE_XXX.json` hasta `.mp4` (11.0s, 660 frames, 60fps).

## 2. Complete Checkpoint History
*   **0.3.6:** Parking V2 refactor (Mathematical constraints).
*   **0.4.x:** RNG V2.0 introduction y separación `MechanicRNGContext`.
*   **0.6.0:** HIT V1 integration.
*   **0.8.1:** CATCH V1 integration.
*   **0.9.0:** Production Contract Consolidation (Factory & Manifest freezing).
*   **1.0.0-A:** FIND Candidate Audit (Match descartado; FIND seleccionado).
*   **1.0.0-B:** FIND V1 Mathematical Contract (Lissajous, Circular Drift).
*   **1.0.0-C:** FIND V1 RNG Contract (Streams 130, 140, 150, 160).
*   **1.0.0-D:** FIND V1 Isolation (9/9 Test suites passing).
*   **1.0.0-E:** FIND V1 Integration (`CHALLENGE_007` Batch success).
*   **1.0.0-F:** Final Release Audit & Documentation Freeze (Current — 0 code changes introduced).

## 3. Architecture Baseline
El motor obedece a una tubería estricta de una sola dirección:
`Capa 0 (JSON)` $\rightarrow$ `Validation (ChallengeDefinitionValidator)` $\rightarrow$ `Composition Root (GeneradorMaestro)` $\rightarrow$ `DDI Capability Injection` $\rightarrow$ `ChallengeMechanic (setup & simulate)` $\rightarrow$ `ChallengeValidator (Autovetting)` $\rightarrow$ `SimulationResult (Transport)` $\rightarrow$ `Presentation Layer` $\rightarrow$ `Factory (FFmpeg/Video)`.

## 4. RNG/DDI Governance
La aleatoriedad se divide rígidamente en dos flujos independientes:
*   **StructuralRNG:** Inyectado en las mecánicas a través de `MechanicRNGContext` para cada reintento de semilla (`seed attempt`). Define la cinemática y resuelve el reto. Ejecutado *únicamente* en `setup()`.
*   **CosmeticRNG:** Inyectado en la presentación visual a través de `PresentationRNGContext`. Es estrictamente aislado de la simulación matemática.
El determinismo exige que las mecánicas no muten estado estructural ni consuman RNG en sus funciones `calculate_frame()`.

## 5. Production Contract 0.9.0
*   El directorio `output/` se mantiene estrictamente particionado por `challenge_id`. Ningún artefacto `*.avi`, `*.mp4` o `*_manifest.json` reside en la raíz.
*   `build_factory.py` es ciego a la lógica del juego. Se limita a orquestar el CLI de Godot y FFmpeg basándose en los retornos JSON del motor.

## 6. Testing Architecture
La arquitectura de validación cuenta con dos escudos complementarios:
*   `tests/run_suite.py`: Barrera de seguridad para registrar suites críticas (Runner histórico/hardened).
*   `tests/run_all.py`: Runner del corpus completo E2E. Protege contra los falsos PASS nativos de `SceneTree` (Actualmente 9/9 suites superadas y consolidadas como protocolo de regresión global).

## 7. Kinematic Families Baseline
*   **5 Familias Matemáticas Activas (V2.0):** PARKING, PILOT, HIT, CATCH y FIND.
*   **1 Legacy Baseline:** KEY (V1.0).

## 8. FIND V1 Mathematical Contract
*   **Scanner:** Trayectoria continua de Lissajous (Bounded por Capa 0, unidades en `rad/frame`).
*   **Target:** Deriva circular (Micro-órbita contínua, independizada del scanner).
*   **Resolución:** Operador `argmin` discreto evaluando distancia euclidiana por fotograma.
*   **Close Calls:** Contabilización *episódica* (secuencias contiguas de falsos positivos cuentan como 1).

## 9. FIND RNG Streams (130-160)
*   `130` **SPATIAL_PLACEMENT**: (idx 0=X, 1=Y).
*   `140` **TOPOLOGY_GENERATION**: (idx 2j=X, 2j+1=Y para $M$ distractores).
*   `150` **SCANNER_TRAJECTORY**: (idx 0=$\phi_x$, 1=$\phi_y$).
*   `160` **TARGET_DRIFT**: (idx 0=$\phi_{drift}$).
*(Modelo A: el RNG provee entropía normalizada `[0.0, 1.0]`, la mecánica proyecta al dominio físico).*

## 10. CHALLENGE_007 Frozen Reference
Primer fixture integrado para `find_v1`. Valida el consumo simultáneo de los streams 130-160, respeta el autovetting (`max_close_calls: 3`) y genera telemetría exacta validada (660 frames a 60 FPS = 11.0s).

## 11. Final 001–007 Batch Evidence
Ejecución de `build_factory.py --batch`: **7/7 PASSED**.
La inserción de `find_v1` y la refactorización del ciclo de vida (`setup()` iterativo en el Composition Root) no causó regresiones matemáticas en las familias previas.

## 12. Known Non-Blocking Technical Debt (Non-Normative)
*   **Factory Fallback:** `build_factory.py` tolera leer `"id"` en lugar de `"challenge_id"`. (Comportamiento de compatibilidad legacy, no forma parte del contrato normativo 0.9.0).
*   **Legacy Double Setup:** Las mecánicas `pilot` y `parking_v2` invocan `setup(config)` dentro de su propio `simulate()`, provocando un doble setup inofensivo tras el cambio en `GeneradorMaestro`.
*   **FIND Topology Presentation:** `FindMechanic` genera y transporta correctamente `metadata["distractor_topology"]`, pero la capa de presentación visual actual todavía no renderiza pasivamente esa topología específica (limitación cosmética no bloqueante para la integridad de simulación).

## 13. Order of Authority for Future Sessions
Ante cualquier duda de diseño o continuidad, la jerarquía de fuentes de verdad es estrictamente la siguiente:
1.  **Código real del Repositorio** (Implementación vigente).
2.  **`MASTER_HANDOVER_CHECKPOINT_1.0.0.md`** (Continuidad y decisiones congeladas).
3.  **Contratos en `docs/*.md`** (Especificaciones formales).
4.  **Handovers históricos** (Referencia cronológica; nunca sustituyen al estado actual).

## 14. 1.0.0 Freeze Decision & Next Development Boundary
El motor es determinista, aislable, productizable y trazable. El núcleo arquitectónico queda declarado **FROZEN (1.0.0)**.
Cualquier futura familia o alteración del core deberá ejecutarse siguiendo rigurosamente el protocolo: `AUDIT` $\rightarrow$ `MATH CONTRACT` $\rightarrow$ `RNG CONTRACT` $\rightarrow$ `ISOLATION` $\rightarrow$ `INTEGRATION` $\rightarrow$ `BATCH REGRESSION`.