# C11-D — Fase P: plan de prueba de procedencia source-value frente a frame-value

**Estado:** preparada despues de la Fase O. No hay implementacion ni ejecucion aceptada de Fase P en este documento.

## Objetivo

Determinar, para cada uno de los seis candidatos `custom_data`, si el valor declarado por la fuente/configuracion tiene correspondencia demostrable con los valores efectivos asociados a frames del runtime. La auditoria de Fase O solo vio presencia/tipo y conteos por frame; no recibio valores reales serializados.

## Alcance fijo

- `CHALLENGE_003.target_x` — conservar tipo escalar, no convertirlo en vector.
- `CHALLENGE_005.target_position`.
- `CHALLENGE_006.target_position`.
- `CHALLENGE_007.target_position`.
- `CHALLENGE_008.active_selection`.
- `CHALLENGE_009.displayed_count`.

## Prueba propuesta

1. Fijar hashes de fuente, contrato, mecanica, config efectiva y puente de runtime antes de ejecutar.
2. Construir casos negativos donde el valor de fuente falta, cambia de tipo o no corresponde al valor por frame esperado. El test debe fallar cerrado y distinguir `SOURCE_VALUE`, `FRAME_VALUE`, `NOT_OBSERVED` y `UNRESOLVED`.
3. Para los casos positivos, capturar en memoria el tipo y la presencia por frame, y comparar los valores normalizados de fuente y frame sin persistir la estructura completa de `FrameSnapshot.custom_data`.
4. Reportar solo selector, nombre de campo, tipo, conteos, igualdad/diferencia y hashes canonicos de valores. Nunca volcar contenido sensible/masivo de `custom_data` ni crear payload o media.
5. Verificar al menos dos ejecuciones aisladas, diferenciando igualdad entre repeticiones de igualdad entre fuente y frame. Un valor estable no prueba por si mismo semantica de presentacion ni consumo visual.
6. Mantener una matriz de decisiones separada. Resultado esperado de esta prueba es evidencia de procedencia, no un binding aprobado.

## Criterios de aceptacion

- Los seis campos estan cubiertos, con recibos y pins exactos.
- `target_x` permanece escalar.
- Se detectan ausencias, cambios de tipo y divergencias fuente/frame.
- Los valores reales solo se usan transitoriamente en memoria; los informes incluyen hashes y metadata acotada.
- Se conserva `approved_custom_data_bindings=0` salvo que una decision separada, explicitamente aprobada, diga lo contrario; esta fase no incluye esa aprobacion.
- No renderer dispatch, payload persistido, viewport capture, media o video.

## Dependencias y cuestiones bloqueantes

- La aprobacion de binding es una puerta diferente y necesita decision formal y pruebas dedicadas.
- `CHALLENGE_008` y `CHALLENGE_009` siguen en conflicto: 11 segundos declarados frente a 12 segundos por suma de fases; la prueba no debe convertirlos en runtime materializable.
- `winning_frame` sigue siendo el unico anclaje temporal Challenge; `close_calls` sigue siendo contador de episodios.
- Editorial sidecar mantiene 0/14 campos visualmente consumidos.

## Bloqueos de gobernanza

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; `approved_bindings=0`; `approved_custom_data_bindings=0`; `approved_renderer_projection_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.
