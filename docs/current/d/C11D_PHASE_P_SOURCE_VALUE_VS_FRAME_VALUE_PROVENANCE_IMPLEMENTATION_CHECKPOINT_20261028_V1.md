# C11-D Phase P — Implementation checkpoint V1 (2026-10-28)

**Estado:** `PREPARED_NOT_WINDOWS_ACCEPTED`.

## Contexto de entrada

Phase O permanece aceptada como `WINDOWS_PASS_READ_ONLY_CROSSWALK_NO_BINDING_APPROVAL`. Su informe confirma seis candidatos con presencia/tipo estable pero sin valores reales de `custom_data` serializados. La Phase P propuesta separa el hash de los parámetros fuente del hash de la serie efectiva de frames y limita cada relación a la semántica del mecanismo fijada por hashes.

## Cambios add-only preparados

- Contrato Phase P y esquema JSON estricto.
- Harness Godot en memoria, separado del harness de Phase N.
- Auditor Python con planner canónico, dos procesos Godot por selector, recibos sin valores reales, verificación de pins antes/después y artefactos bajo `%TEMP%`.
- Tests unitarios/estáticos, wrapper PowerShell 5.1 y runbook.

No se modifica ningún archivo existente del proyecto mediante esta implementación. Los archivos nuevos permanecen en el estado de preparación hasta la prueba estática y la ejecución real Windows.

## Criterio técnico por candidato

`CHALLENGE_003.target_x` se compara con la fórmula escalar fuente por índice; `CHALLENGE_005.target_position` se comprueba como objetivo constante por ejecución ajustado por RNG, sin equipararlo al target base; `CHALLENGE_006/007.target_position` se limita a tipo/finitud/variación y hashes repetibles bajo mecánicas fijadas, sin afirmar recomputación matemática independiente; `CHALLENGE_008.active_selection` se coteja con la secuencia fuente de selección y posiciones; `CHALLENGE_009.displayed_count` se coteja con la secuencia fuente y su codificación posicional. No se vuelcan valores candidatos ni mapas completos.

## Evidencia todavía pendiente

- Ejecución real de los tests en Windows.
- 6/6 planner calls y 12/12 procesos Godot 4.7.1 Mono.
- Receipts hash-only independientes y concordantes.
- Acceptación separada del informe, write-back de checkpoint/ledger y decisión de fase siguiente.

## Gobernanza

Este checkpoint no es una aceptación de Phase P. `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.
