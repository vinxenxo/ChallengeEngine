# C11-D — Dependencias de cierre hacia un render real en baseline D

**Corte:** 28-10-2026. Este roadmap es una secuencia de dependencias; no concede autorizaciones.

## Estado probado

Request→payload V2.2, auditorías I/O/identidad de solo lectura, auditorías de colisión de semillas, Fases L/M/N/O y tests estáticos Phase P están registrados en el ledger V2. Phase O encontró seis candidatos de `custom_data` y mantiene cero bindings aprobados. Phase P estático pasó 30/30 tras corregir la lectura/normalización de versión Python; runtime Phase P queda pendiente.

## Camino de gates

1. **Fase P runtime de procedencia.** Ejecutar el runner actual en el checkout; evidencias independientes para los seis candidatos; dos procesos por selector como fija el contrato. Sin payload persistido y sin renderer.
2. **Validación de evidencia y revisión independiente.** Validar pins pre/post, repetición, valores fuente/frame, tipos y hashes. Guardar un reporte/recibo versionado y una decisión de revisión separada. No declarar bindings por resultado técnico.
3. **Adjudicación semántica.** Revisar cada candidato y cualquier divergencia con los contratos de fuente, mecánica, configuración efectiva y recibos frame. `target_x` permanece escalar. `catch/find` son track-only, `hit` aplica la política constante por ejecución y `choose/count` solo pueden tratarse según sus relaciones explícitamente declaradas.
4. **Resolución formal del timebase de CHALLENGE_008 y CHALLENGE_009.** Las declaraciones son 11 s y las sumas de fases 12 s. Mantenerlos bloqueados hasta una decisión de autoridad compartida; ni tests ni un modelo de frames pueden escoger la duración por sí solos.
5. **Refresco de identidad e I/O si cambian entradas.** Si las decisiones modifican contrato, fuente, puente, request o payload identity, actualizar pins y auditorías en un gate separado. No repetir reportes sin cambio de fuentes si el gate no requiere evidencia nueva.
6. **Contratos y decisiones de binding/renderer.** Decidir explícitamente campos, regiones, visibilidad, coordenadas/proyección/rounding, sampling y timebase; revisar políticas de audio/música y dominios de semillas/ortogonalidad cuando sean dependencias. Mantener la propuesta D renderer-owned, aislada y no productiva hasta autorización.
7. **Admisibilidad y renderer D.** Solo cuando todas las entradas requeridas sean admisibles y existan decisiones aprobadas podrá prepararse y validarse el camino de render D-owned. La primera ejecución de render técnico, si llega a autorizarse, no equivale a baseline approval.
8. **Gobernanza de producción, por separado.** D4.8 necesita decisión independiente; D9.14 certificación de media real; D9.16 aceptación completa; D9.17 adjudicación de cierre; D10 aprobación, freeze y promoción. No saltar gates ni inferir uno de otro.
9. **Cambio de baseline.** C11-C solo podrá ser reemplazado por C11-D después de aprobación formal, aceptación, freeze y promoción explícitas. Mantener el paquete C11-C histórico e inmutable.

## Condiciones invariantes hasta autorización explícita

`renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `seed_domains_complete_for_candidate_input=false`; `automatic_seed_generation=false`; `master_seed=NOT_ADOPTED`; todos los contadores `approved_*_bindings=0`; `D4.8=BLOCKED`; `D9.10=PREPARE_ONLY`; `D9.14=BLOCKED`; `D9.16=BLOCKED`; `D9.17=BLOCKED_NO_GO`; `D10=BLOCKED_FOR_PROMOTION`; `baseline_approval=MISSING`; `freeze_eligible=false`; `release_authority=NONE`.

`winning_frame` sigue siendo el único anclaje temporal Challenge; `close_calls` es contador de episodios. El sidecar editorial continúa en 0/14 consumo visual. Este roadmap no habilita render, creación de media, persistencia, release ni cutover.
