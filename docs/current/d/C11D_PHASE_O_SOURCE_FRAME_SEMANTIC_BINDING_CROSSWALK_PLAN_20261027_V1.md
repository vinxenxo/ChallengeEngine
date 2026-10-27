# C11-D — Fase O: auditoría read-only de recibos source-frame → binding semántico

**Estado:** preparada después de la aceptación documental de Fase N; todavía no ejecutada.

## Objetivo

Usar los nueve recibos source-frame validados de Fase N junto con la propuesta de binding semántico ya existente para producir un cruce de evidencia por selector y por campo. La finalidad es identificar qué datos están disponibles en el pipeline efectivo, su origen, semántica temporal, mutabilidad, estabilidad entre repeticiones y evidencia necesaria antes de cualquier decisión de binding.

## Salida esperada

- Matriz de nueve Challenges que cite IDs y hashes de los dos recibos aceptados por selector.
- Inventario por campo que clasifique `temporal_anchor`, `episode_counter`, `safe_state`, `custom_data_candidate`, `editorial_sidecar_only`, `absent`, o `unresolved`.
- Columnas de origen, contrato/pin de fuente, tipo/forma, estabilidad entre las dos repeticiones, relación con `gameplay_seed`, dependencia editorial/música y riesgo de proyección.
- Diferencias entre el source-frame y datos visuales derivados, sin inferir que la presencia de un valor equivale a consumo visual.
- Registro explícito de decisiones que requieren aprobación humana separada; el output de esta fase no puede fijar ningún binding aprobado.

## Invariantes obligatorios

1. `winning_frame` sigue siendo el único anclaje temporal Challenge.
2. `close_calls` sigue siendo contador de episodios; no se interpreta como frame ganador ni duración.
3. Los seis candidatos `custom_data` permanecen no aprobados hasta que haya decisión registrada y tests específicos.
4. `target_x` del piloto Challenge se mantiene como escalar; no se amplía el contrato de CH_004 V1 por inferencia.
5. El sidecar editorial de 14 campos permanece sidecar-only mientras no haya una decisión y evidencia de consumo visual.
6. No renderer dispatch, payload persistido, viewport capture, media ni video.
7. El conflicto de `CHALLENGE_008/009` (11 s declarados frente a 12 s de fases) se mantiene como issue bloqueante independiente.

## Condiciones de salida

Aceptar la auditoría únicamente si todos los campos se trazan a fuentes fijadas, los ausentes se reportan como ausentes, cada conclusión apunta a recibos/contratos/pins, las diferencias entre repeticiones están explicadas y el documento no eleva ningún binding a approved. Luego decidir la siguiente unidad pequeña de contrato/tests, no iniciar render.

## Bloqueos

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.
