# C11-E E6 — Estado de ledger de reutilización V2

**Estado:** `REUSE_CANDIDATES_RETAINED / ARTIFACT_LEVEL_ACCEPTANCE_PENDING`

Este registro preserva cierres previos y separa la aceptación histórica de la aceptación E6 por artefacto. No se repiten lotes A/V aceptados para rellenar huecos documentales.

| Familia | Casos objetivo | Evidencia previa | Disposición E6 |
|---|---:|---|---|
| Visual Loop | 6 | R1V cerrado 10/10; Loop22 cerrado 44/44 y aprobación humana posterior | `6_REUSE_CANDIDATES_NEED_EXACT_PER_OUTPUT_RECEIPT_AND_MEDIA_HASH_LINKS` |
| Visual Drill | 6 | E4C `ACCEPTED_20_OF_20`; seis recibos single-selector | `6_REUSE_CANDIDATES_NEED_NESTED_OUTPUT_REHASH_AND_E6_PREDICATES` |
| Challenge CH004 | 1 | E4A.7 receipt SHA `102cf07a0b8920318c3ba211a3bd4374c3e080018486363d701f81e65613aaa0`; source silent SHA `841b03531301c7e70c0e09ce3e9f536241d2072a87792e099ed7a955bef8c52f` | `REUSE_CANDIDATE_NEEDS_COMPLETE_RECEIPT_AND_NESTED_MEDIA_REVALIDATION` |
| Challenge restantes | 5 | Ninguna prueba runtime D-composited multislector aceptada | `FRESH_CAPTURE_REQUIRED_ONLY_AFTER_POLICY_AUTHORIZATION` |

## Invariantes de evidencia

- R1V 10/10, Loop22 44/44 y E4C 20/20 son cierres históricos aceptados: no rerun.
- La evidencia E5 representativa de Loop `radial_bloom` y Drill `tracking/tier-2` no reemplaza los seis IDs de familia que aparecen en el plan Smoke18.
- El número 13/18 es potencial de reutilización (6 Loop + 6 Drill + CH004), no aceptación E6.
- Cada aceptación E6 exige receipt SHA, nested media SHA, family/selector, seeds, profile, timebase, FFprobe metadata, audio predicates y human approval enlazados a hashes exactos.
- No declarar `REUSE_ACCEPTED` cuando falten recibos/media anidados. No re-generar medios aceptados.

## Próxima tarea de evidencia

Hidratar de los archives originales los punteros exactos por salida de Loop22 y los seis recibos Drill. Verificar los nested media hashes contra el checkout activo y preservar el run ID original. La reconciliación es read-only; no ejecutar Godot, FFmpeg, FFprobe, audio ni mux durante la fase de hidratación.
