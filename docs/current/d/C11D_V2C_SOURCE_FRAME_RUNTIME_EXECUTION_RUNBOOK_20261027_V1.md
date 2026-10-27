# C11-D — Fase N: recibos runtime source-frame V2-C

**Estado inicial:** puerta preparada; la ejecucion Windows sigue pendiente. La Fase M fue aceptada por evidencia real de Windows el 27-10-2026: planner `45/45`, procesos Godot Mono `45/45`, selectores `9/9`, informe SHA-256 `6e19e88bcce6249f613c7e8566b92f78497c4749bfd079dda2b01e20385072a0`.

## Objetivo

Ejecutar el contrato V2-C ya existente para los nueve Challenges con el planner canonico y `ChallengeRuntimeBridge.run_effective_pipeline`. Cada selector requiere una llamada de planificacion y dos procesos Godot independientes para demostrar recibos source-frame repetibles. El alcance solo prueba estado/frame source y ruta runtime efectiva; no acepta timeline visual, no autoriza bindings y no crea payload, media ni video.

## Archivos relevantes preexistentes

- Contrato: `definitions/c11d/production/D_RENDERER_CHALLENGE_VISUAL_PAYLOAD_V2C_SOURCE_FRAME_RUNTIME_RECEIPT_V1.json` (SHA-256 `6d3c59214edbdd917cf63fe9ca4859edb6968d503368ec84e867bdd56a8df74c`, 81 source pins).
- Runner: `tools/c11d/d9/d_renderer_challenge_visual_payload_v2c_source_frame_runtime.py`.
- Harness en memoria: `tools/c11d/d9/challenge_visual_payload_v2c_source_frame_runtime_in_memory.gd`.
- Tests de contrato: `tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2c_source_frame_runtime.py` (28 tests).

## Secuencia

1. Aplicar el overlay add-only desde el ZIP con el shell de instalacion. No extraerlo manualmente. El shell verifica precondiciones exactas de Phase L/M, el manifiesto congelado C11-C y hashes de contrato/runner/harness/tests/checkpoint/ledger.
2. Ejecutar `tools/c11d/d9/run_d_renderer_challenge_visual_payload_v2c_source_frame_runtime_20261027.ps1`. Primero ejecuta 28/28 tests del contrato Python; solo si pasan continua con el runner runtime.
3. El runner revalida 81 pins, prueba el ejecutable Godot Mono `4.7.1`, llama al planner una vez por selector y lanza dos procesos Godot independientes por Challenge. Se detiene ante el primer fallo y no cambia checkpoint/ledger.
4. La evidencia y logs se guardan solo bajo `%TEMP%`. Un marcador de intento evita relanzar una ejecucion que haya comenzado; ante fallo, no borrar marcadores ni relanzar a ciegas.
5. Tras recibir la salida real, se preparara un overlay de aceptacion documental guarded para registrar hashes de reporte/recibos, actualizar checkpoint y ledger y describir la siguiente puerta.

## Predicados estrictos de aceptacion

- Python contract tests `28/28`.
- Contract/source pins `81/81`; manifest congelado C11-C unchanged, SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796318 bytes.
- Godot version probe `1`, version `4.7.1.stable.mono.official.a13da4feb`.
- Planner canonico `9/9`; procesos Godot independientes `18/18`; selectores `9/9`; archivos de evidencia de proceso `36/36`.
- Cada recibo debe identificar `ChallengeRuntimeBridge.run_effective_pipeline`, dos procesos distintos con recibos concordantes, frame shape/projection/hash valido, y source lineage correcto.
- `payload_materialized=false`, `media_created=false`, `approved_bindings=0`, `visual_seed_sensitivity=NOT_TESTED` y todos los locks de gobernanza intactos.

## Exclusiones y bloqueos

No se permite serializar los valores de `FrameSnapshot.custom_data`, crear archivos de payload, emitir renderer-native input, instanciar nodos de render, usar RenderingServer, capturar viewport, mutar estado canonico ni disparar produccion. `CHALLENGE_008` y `CHALLENGE_009` siguen declarando 11 segundos con fases que suman 12; sus recibos deben conservar el conflicto y marcar aceptacion de timeline como bloqueada. Esta fase no resuelve ese conflicto.

Locks: `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

**Direccion posterior:** aceptar los recibos source-frame si pasan; despues revisar las brechas de admision y el contrato visual/temporal. No se autoriza render con este gate.
