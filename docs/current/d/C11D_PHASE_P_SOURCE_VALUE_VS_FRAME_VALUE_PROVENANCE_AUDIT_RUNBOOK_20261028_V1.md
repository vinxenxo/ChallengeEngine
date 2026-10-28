# C11-D Phase P — Runbook de procedencia source-value / frame-value

**Estado:** IMPLEMENTACIÓN PREPARADA; ejecución Windows y aceptación formal pendientes.

## Objetivo y límite

Ejecutar el pipeline efectivo Challenge para los seis candidatos ya inventariados, en dos procesos Godot independientes por selector. El control recoge solo presencia/tipo, conteos y hashes SHA-256 normalizados de entradas explícitas de configuración y de series de valores de frame. Los valores candidatos se mantienen en memoria y no se escriben en recibos, stdout como datos individuales, payloads ni archivos.

## Alcance exacto

- `CHALLENGE_003.target_x` (`float`): verificar la relación por-frame `target_start + target_velocity * frame_index`, conservando el escalar.
- `CHALLENGE_005.target_position` (`Vector2`): verificar la constancia del objetivo ajustado por el RNG dentro de un proceso. No declarar igualdad directa con el punto base de configuración.
- `CHALLENGE_006.target_position` (`Vector2`): verificar tipo, finitud, variación de la serie y estabilidad de sus hashes entre procesos; la relación está mediada por parámetros y offsets RNG del mecanismo fijado.
- `CHALLENGE_007.target_position` (`Vector2`): verificar tipo, finitud, variación de la serie y estabilidad de sus hashes entre procesos; la posición base/fase del objetivo depende del mecanismo y RNG fijados.
- `CHALLENGE_008.active_selection` (`int`): reconstruir y comparar la secuencia declarada por el mecanismo a partir de frames de juego, seed y opciones; comprobar que cada índice corresponde a la posición fuente configurada.
- `CHALLENGE_009.displayed_count` (`int`): reconstruir y comparar la secuencia del mecanismo y su codificación en `FrameSnapshot.position`; nunca sustituirla por `target_count`.

## Ejecución

1. Ejecutar los tests estáticos específicos con Python 3.13 desde la raíz.
2. Solo si pasan, ejecutar una vez `tools/c11d/d9/run_d_renderer_phase_p_source_value_frame_value_provenance_20261028.ps1` desde la raíz. El wrapper verifica el manifest C11-C canónico, los pins de Phase N/O/P, el contrato y el runtime de Godot 4.7.1 Mono. Crea evidencia solo bajo `%TEMP%` y se detiene ante el primer fallo.
3. Conservar el directorio `%TEMP%`, los stdout/stderr separados y el informe JSON; no repetir una matriz fallida sin diagnóstico.
4. Remitir el resumen y los hashes generados para preparar un acceptance overlay separado. Este overlay de implementación no actualiza el checkpoint estable ni el ledger.

## Criterios PASS de esta auditoría

- 6/6 selectores, una invocación de planner canónico por selector y 12/12 procesos Godot separados.
- Dos recibos distintos en PID/`run_id` por selector, mismos hashes de entradas fuente y de serie de valores entre repeticiones.
- `target_x` se mantiene `float`; `target_position` se mantiene `Vector2`; `active_selection` y `displayed_count` se mantienen `int`.
- `CHALLENGE_003`, `008` y `009` pasan sus relaciones calculables con la configuración fuente; `CHALLENGE_005` pasa la relación de objetivo constante por ejecución; `CHALLENGE_006/007` prueban solo track vectorial finito/variable y hashes repetibles, sin fingir recomputación independiente de los offsets internos.
- Sin serialización de valores reales, mapas completos `FrameSnapshot.custom_data`, payload, media, renderer o archivos de recibo en el repositorio.
- Hashes de fuentes y pins C11-C válidos antes y después de la ejecución.

## Interpretación obligatoria

El hash de la configuración fuente y el hash de la serie de frames son dominios distintos; no se comparan como si fueran la misma representación. La relación semántica declarada para cada candidato limita la conclusión. Que el hash sea estable no prueba consumo visual ni autoriza un binding.

Para `CHALLENGE_008/009`, el reporte debe conservar explícitamente el conflicto `total_duration=11` frente a suma de fases `12`. Ejecutar la simulación de juego acotada a sus 420 frames no decide el timebase, ni habilita payload materializado, render, vídeo o aprobación.

## Invariantes

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.
