# C11-D Phase S — comprobación de evidencias de autoridad V1

**Fecha:** 29-10-2026  
**Modo:** `READ_ONLY_AUTHORITY_EVIDENCE_PREFLIGHT`  
**Estado inicial:** `AUTHORITY_EVIDENCE_NOT_PRESENT_IN_PINNED_PHASE_P_Q_R_RECORD_SET`

## 1. Objetivo y límite de la comprobación

Phase R quedó aceptada como paquete de preparación de decisiones, no como adopción de políticas. Phase S inspecciona el conjunto acotado de registros de aceptación de Phase P, Q y R que figura en el JSON compañero para determinar si alguno contiene una decisión de autoridad explícita con opción exacta, alcance verificable, justificación, pins de fuentes y pruebas de aceptación.

**Resultado de esta comprobación acotada:** no se identificó un registro aceptado de autoridad de política dentro del conjunto pinneado. Esto no afirma que no exista documentación de autoridad en otra ubicación; cualquier documento adicional deberá presentarse y verificarse por separado antes de utilizarlo.

## 2. No confundir continuidad operativa con autoridad de producto

La autorización para continuar las fases de ingeniería permite preparar y verificar gates, pero no selecciona por sí misma una política semántica, una regla temporal, un transform espacial, una regla de visibilidad, un layout, un tratamiento de datos inválidos ni un binding. Los expedientes escritos por el asistente y el `PASS` de una prueba acreditan preparación técnica, no aprobación de producto/contrato.

Un registro de decisión aceptable debe ser independiente, inmutable/add-only y permitir identificar, como mínimo: ID del registro, decisión R-xx, opción exacta o texto normativo, nombre/rol de la autoridad, alcance, fecha efectiva, justificación, pins de fuentes, pruebas de aceptación y procedencia verificable de la aprobación.

## 3. Estado por decisión

Las nueve decisiones R-01…R-09 permanecen sin adoptar. Para cada una, el resultado de búsqueda es `NOT_EVIDENCED_IN_PINNED_PHASE_P_Q_R_RECORD_SET`, no `APPROVED` ni `REJECTED`. Las opciones del paquete R se conservan como alternativas sin seleccionar; la ausencia de un registro se resuelve por `KEEP_BLOCKED_NO_POLICY_ADOPTION`.

| Decisión | Alcance | Resultado Phase S |
|---|---|---|
| `R-01-TIMEBASE-SAMPLING` | Source 60 FPS to delivery 30 FPS sampling | `NOT_EVIDENCED_IN_PINNED_PHASE_P_Q_R_RECORD_SET` |
| `R-02-SPATIAL-MAPPING` | Coordinate transforms for Vector2 candidates | `NOT_EVIDENCED_IN_PINNED_PHASE_P_Q_R_RECORD_SET` |
| `R-03-PILOT-SCALAR-X-AND-PRESENTATION-Y` | CHALLENGE_003 scalar X and separate presentation-only Y | `NOT_EVIDENCED_IN_PINNED_PHASE_P_Q_R_RECORD_SET` |
| `R-04-VISIBILITY-AND-REGION-OWNERSHIP` | Visible region and temporal visibility span | `NOT_EVIDENCED_IN_PINNED_PHASE_P_Q_R_RECORD_SET` |
| `R-05-ASSET-GEOMETRY-ANCHOR-CROP-ROUNDING` | SVG intrinsic dimensions, anchor, clipping and pixel rounding | `NOT_EVIDENCED_IN_PINNED_PHASE_P_Q_R_RECORD_SET` |
| `R-06-INVALID-DATA-AND-TRACK-INTEGRITY` | Missing, malformed, nonfinite, out-of-range and cardinality mismatch handling | `NOT_EVIDENCED_IN_PINNED_PHASE_P_Q_R_RECORD_SET` |
| `R-07-SEMANTIC-VISUAL-OWNERSHIP` | Whether each accepted semantic candidate has a distinct visual consumer | `NOT_EVIDENCED_IN_PINNED_PHASE_P_Q_R_RECORD_SET` |
| `R-08-CHALLENGE-008-DURATION-CONFLICT` | CHALLENGE_008 declared duration versus phase sum | `NOT_EVIDENCED_IN_PINNED_PHASE_P_Q_R_RECORD_SET` |
| `R-09-CHALLENGE-009-DURATION-AND-COUNT-ROLE` | CHALLENGE_009 declared duration versus phase sum and displayed-count ownership | `NOT_EVIDENCED_IN_PINNED_PHASE_P_Q_R_RECORD_SET` |

## 4. Bloqueos temporales preservados

- `CHALLENGE_008.active_selection`: total declarado **11 s**; suma de fases **12 s**. Estado `BLOCKER_NO_CORRECTION_INFERRED`.
- `CHALLENGE_009.displayed_count`: total declarado **11 s**; suma de fases **12 s**. Estado `BLOCKER_NO_CORRECTION_INFERRED`.

No se corrige la duración, no se infiere una excepción y no se utiliza una decisión de duración para autorizar texto, layout o bindings. `displayed_count` sigue siendo distinto de `target_count`.

## 5. Alcance de futuras adjudicaciones

Cuando se presente un registro de autoridad válido, solo se puede adjudicar el ID y alcance que indique dicho registro. Antes de considerar una decisión válida se deben verificar sus pins, autoridad, opción exacta, justificación y pruebas requeridas. Toda resolución deberá quedar en un registro de decisión separado, versionado e inmutable; este expediente no puede actuar como ese registro.

Una política adoptada tampoco autoriza por sí sola binding, acceso a `custom_data`, proyección del renderer, materialización de payload/media, ejecución de runtime o promoción. Esos gates siguen separados.

## 6. Invariantes

- `renderer=OFF`; `media_created=false`; `payload_materialized=false`.
- `candidate_input_admissible=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`.
- `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`.
- `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`.
- `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.
- C11-C 2.19.12 permanece autoritativo e inmutable hasta aceptación, freeze y promoción formales de C11-D.
- `winning_frame` es el único anclaje temporal; `close_calls` solo representa el recuento de episodios.

## 7. Criterio de salida

Phase S puede cerrar como auditoría de autoridad únicamente si el paquete, pins, prueba estática y bloqueos pasan. Si no existe evidencia de autoridad, el cierre correcto es `PASS_AUDIT_ONLY_AUTHORITY_EVIDENCE_NOT_FOUND`; la adjudicación de políticas queda **bloqueada** y el siguiente paso operativo es aportar un registro de autoridad explícito y verificable. No se inicia una fase de implementación ni se inventa una Phase T para sortear esa dependencia.
