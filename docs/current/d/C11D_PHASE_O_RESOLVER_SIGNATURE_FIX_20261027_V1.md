# C11-D — Fase O: corrección de firma de `resolve_repo_path`

**Estado de esta corrección:** preparada en overlay guarded; aplicación en Windows pendiente.

## Evidencia previa

La primera ejecución Windows de Fase O produjo `PHASE_O_UNIT_TESTS=27/27` y después terminó `FAIL_CLOSED` con `TypeError: resolve_repo_path() missing 1 required positional argument: 'relative'`. No actualizó checkpoint ni ledger. El intento fallido se conserva en `%TEMP%` bajo `C11D_PHASE_O_SEMANTIC_CROSSWALK_20261027_da7ea2ea57334a889716c96e5a93c1e4`.

## Causa y cambio

Dos invocaciones en `audit_d_renderer_phase_o_source_frame_semantic_binding_crosswalk_20261027.py` omitían el argumento `root`: resolución de la propuesta de binding semántico y del carrier editorial. La firma `resolve_repo_path(root, relative)` no cambia. La corrección pasa ambos argumentos.

Se incorpora una prueba AST de regresión para exigir dos argumentos en cada llamada directa y se actualiza el lanzador para exigir `PHASE_O_UNIT_TESTS=28/28`. Ningún pin de producción V2-C, recibo, contrato, payload, checkpoint ni ledger se modifica en esta reparación.

## Próxima acción

Aplicar el overlay V3 comprobando hashes before/after de los tres archivos existentes y añadir este registro. A continuación ejecutar una sola vez el lanzador de Fase O. La aceptación sigue condicionada a los resultados reales del checkout Windows. No repetir V2-C ni eliminar el directorio del intento fallido.

## Gobernanza

La auditoría permanece read-only respecto a los artefactos de producción. `renderer=OFF`; `media_created=false`; `payload_materialized=false`; `candidate_input_admissible=false`; `approved_bindings=0`; `D4.8=BLOCKED`; `release_authority=NONE`.
