# C11-D — Fase O: auditoría de cruce source-frame → binding semántico

**Estado al preparar este runbook:** preparada; ejecución Windows pendiente. Fase N ya está aceptada: V2-C, 28/28 tests, 81/81 pins, planner 9/9, Godot 18/18, selectores 9/9 y evidencia 36/36.

## Objetivo

Cruzar en modo estrictamente de solo lectura los 18 recibos source-frame aceptados con la propuesta de binding semántico existente para los nueve Challenges. Genera un informe JSON, una matriz CSV por campo y un resumen Markdown en `%TEMP%`; no persiste el informe en el repositorio ni modifica los contratos de producción.

## Ejecución

1. Aplicar el overlay ZIP mediante el shell guarded de la instrucción de entrega.
2. Ejecutar desde la raíz del checkout `tools/c11d/d9/run_d_renderer_phase_o_source_frame_semantic_binding_crosswalk_20261027.ps1`.
3. Conservar las rutas de informes/logs y los hashes emitidos. No se ejecutan pruebas V2-C de nuevo, planner ni procesos Godot.
4. Solo después del resultado Windows PASS se prepara un overlay distinto para aceptación documental y actualización del checkpoint/ledger.

## Evidencia de entrada

- Completion marker de runtime V2-C: `%TEMP%\C11D_V2C_SOURCE_FRAME_RUNTIME_20261027.completed.json`.
- Completion marker de aceptación documental Fase N: `%TEMP%\C11D_V2C_SOURCE_FRAME_RUNTIME_ACCEPTANCE_20261027.completed.json`.
- Informe runtime aceptado, SHA-256 `7f96c9aec3849212299afbcabe7fd3045fee815807c9cafe555ad8cb947f91f2`.
- Registro de aceptación, checkpoint, ledger, contrato/recibo/schema V2-C, propuesta semántica, inventario de campo editorial y policy docket, todos fijados por SHA-256.

## Condiciones de aceptación

- Nueve selectores canónicos en orden; dos recibos distintos por selector, 18/18; hashes canónicos de recibos verificados.
- Todos los 36 ficheros stdout/stderr comprobados contra el mapa de hashes del informe; fuente Challenge, mecánica y assets comprobados contra los pins de contrato.
- Repeticiones iguales en todos los campos del recibo excepto identidad del proceso; las formas de frame, el hash de proyección, las observaciones de presencia/tipo, los asset pins y el timebase deben coincidir.
- 54 filas de forma de base-track; 6/6 apariciones candidatas de `custom_data` presentes con recuento/tipo estables; 3/3 pointers de posición estática presentes en su JSON de origen pero aún no probados como consumo de frame.
- `winning_frame` etiquetado como anclaje temporal exclusivo, no binding visual; `close_calls` como contador de episodios, no frame/duración.
- Los seis campos de sidecar para Challenges siguen sidecar-only; los 14 slots de contrato (Challenge + Loop + Drill) siguen sin consumo visual.
- `CHALLENGE_008/009`: duración declarada 11 s frente a suma de fases 12 s, ambos conflictos siguen sin resolver.
- Ningún binding aprobado; ningún valor `custom_data` serializado; cero llamadas de runtime durante esta auditoría, cero media/payload/archivos de producción escritos.

## Interpretación de los resultados

La presencia y el tipo de un valor no significan que su valor exacto esté disponible para un binding, y un hash de proyección no equivale a prueba de consumo por renderer. El recibo V2-C conserva metadatos de forma/hashes de los frames, no listas de valores por frame. Los candidatos `target_x`, `target_position`, `active_selection` y `displayed_count` siguen pendientes de decisión y pruebas específicas. `target_x` sigue siendo escalar. `CHALLENGE_004` V1 permanece como fixture de regresión inmóvil.

## Próxima unidad segura

Diseñar pruebas acotadas que comparen el origen semántico de los seis candidatos `custom_data` con sus observaciones source-frame, sin serializar valores ni declarar bindings. Debe probar ausencia, tipos, estabilidad, relación con selector/seed y semántica temporal. La aprobación, de existir, requiere un registro decisorio separado.

## Gobernanza inalterada

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.
