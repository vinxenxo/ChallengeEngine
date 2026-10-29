# Prompt de continuidad — C11-D hacia render V2

Usa este prompt junto al nuevo snapshot generado después de la reorganización documental. Verifica su `.sha256`/`.report.json` y contrasta sus fuentes con el checkout activo de `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`; nunca extraigas el snapshot sobre el checkout.

## Estado operativo

La migración conservadora de documentación de raíz debe estar registrada en `docs/current/d/C11D_ROOT_DOCUMENTATION_MIGRATION_MAP_GENERATED.json`; el catálogo en `C11D_DOCUMENTATION_CATALOG_GENERATED.md/.json`. No repitas esa etapa si pasa la verificación de hash. Dos README históricos están fijados por rutas del manifiesto C11-C y otros permanecen por referencias actuales; no muevas excepciones a la fuerza.

C11-C 2.19.12 sigue congelado, manifiesto SHA `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796.318 bytes. Phase AD validó su packet 60/60 + verifier PASS, pero decisión de operador `PENDING_EVIDENCE_OR_KEEP_BLOCKED`, authority records 0, adjudications 0, policy adoption NONE. Renderer OFF; D9.10 PREPARE_ONLY; D4.8/D9.14/D9.16 bloqueados; D9.17 `BLOCKED_NO_GO`; D10 bloqueado; baseline approval ausente; freeze ineligible; `release_authority=NONE`.

## Haz el trabajo técnico, no una nueva fase documental

1. Verifica pins core y continuidad del checkout; registra hashes actuales.
2. Lee `C11D_RENDER_INTEGRATION_READ_ORDER_20261029_V3.md` y los runners C reales de QA/review/producción. Examina el `GENERAR` de Producer en `c11c-suite/c11c-producer/main.py`; no confundas plan D con generación física.
3. Sigue el request D y un campo editorial hasta el compositor: `c11d_gui_request.py` → `universal_producer.py`/CLI → resolver editorial → bridge/adapter → binding/materialización → visual payload/frame program → composición/render input. Identifica el primer consumer visual faltante mediante código y hashes, no por suposiciones o documentos antiguos.
4. Inspecciona identity/IO, regiones, timebase/alineación temporal y D3 music/mux. No hagas un binder paralelo.
5. Implementa el menor cambio D-only permitido y añade tests focalizados + negative controls; capture versión, comando, exit code y hashes reales de stdout/stderr.
6. No modifiques `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, RNG, los cinco GUI surfaces ni el manifiesto C. `request.seed` y `request.music_seed` son dominios independientes.
7. No invoques renderer D ni produzcas MP4 D hasta que exista autoridad/política auténtica específica y los gates posteriores lo autoricen. Cuando se autorice, validar primero un Challenge + Loop + Drill aislados, incluida revisión de vídeo y audio; solo después 18 smoke y 101 outputs.

Si el gate no permite un paso, continúa con código/tests permitidos y señala el identificador/campo preciso que bloquea la operación. No alteres flags, no fabriques evidencia, no repitas AD por rutina y no presentes PASS estático como aceptación física.
