# C11-D — Plan funcional de recuperación e integración de render V3

**Fecha:** 29-10-2026. **Foco:** abandonar la preparación documental repetitiva y recuperar el hilo de ingeniería en el primer consumer real del render. Este plan no autoriza ejecución de renderer ni generación de medios.

## 1. Resultado que hay que alcanzar

La suite `c11c-suite` debe acabar generando Challenge, Visual Loops y Visual Drills con una presentación D editable y universal, música, delivery y evidencia real, preservando las mecánicas C congeladas. CLI y GUI deben terminar en el mismo servicio canónico; no deben existir pipelines distintos por modo de entrada.

Scope de aceptación conocido: smoke de 18 salidas (9 Challenge, 5 Loop representativos, 4 Drill) y matriz completa de 101 (54 Challenge, 27 gramáticas Loop, 20 variantes Drill tipo/tier). Longform fuera de alcance. `CHALLENGE_008/009` siguen excluidos mientras no se resuelva la divergencia 11 s declarados vs 12 s sumados por fases.

## 2. Resultado de snapshot y limpieza de documentación

Snapshot anterior validado: `C11D_WORKING_CONTEXT_20261029_193950.zip`, SHA-256 `5b8d06ad82bca798c94db03f943a85afb309d91484d4499ed40fed36056ca774`, 9.190.399 bytes, 3.721 entradas únicas, manifiesto C11-C una sola vez. Este archivo es el punto de comparación, pero no se debe usar como el siguiente contexto después de la migración documental.

La reorganización de raíz clasifica los README históricos de overlays y mueve solo los que no están protegidos por el manifiesto C11-C ni por referencias existentes. Las rutas retenidas se explican en `C11D_ROOT_DOCUMENTATION_MIGRATION_MAP_GENERATED.json`. Los documentos movidos se mantienen byte-identical y su SHA-256 se vuelve a comprobar en el destino. El catálogo vivo se regenera después de moverlos.

El test completo se invoca con:

```powershell
& .\tools\c11d\documentation\Test-C11DDocumentationReorganization.ps1 -ApplyRootMigration -GenerateSnapshot
```

Este flujo hace preflight, aplica la migración conservadora, regenera el catálogo, verifica todos los hashes de los documentos movidos, ejecuta el preflight del snapshot, genera un nuevo ZIP y lo valida mediante un segundo lector independiente. Sube a la siguiente ventana el nuevo ZIP y sus dos sidecars. No extraer el snapshot en el checkout activo.

## 3. Call graph que se conoce por inspección del snapshot

### Producción C que sí genera medios

- QA Challenge: `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1` invoca `tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1` para seis casos de seed por reto; mantiene fuente lógica 540×960 y delivery 720×1280 mediante el flujo C/FFmpeg.
- Revisión física: `tools/qa/c11/run_c11c_complete_video_review.ps1`.
- La GUI Producer está en `c11c-suite/c11c-producer/main.py`; `_run_challenge_job` y `_run_content_job` siguen siendo rutas heredadas que lanzan runners C. No asumir que el tab D convierte el comando `GENERAR` en un renderer D.
- Validar `c11c-suite/c11c-test/BUILD_MANIFEST.json` para confirmar el catálogo real de runners y comandos.

### Preparación D observable; no confundir con producción física

- GUI helper: `c11c-suite/c11c-producer/c11d_gui_request.py`.
- Request/plan canónico: `tools/c11d/d9/universal_producer.py` y `universal_producer_cli.py`.
- Resolver editorial: `tools/c11d/d9/universal_editorial_model.py` con `definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json`.
- Bridge: `tools/c11d/d9/editorial_render_bridge.py`, contrato `definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json`.
- Adapter: `tools/c11d/d9/d_render_adapter.py`, contrato `definitions/c11d/production/C11D_RENDER_ADAPTER_BOUNDARY_D9_10_V1.json`; estado histórico `PLANNING_ONLY_NOT_RENDERABLE`/`PREPARE_ONLY`, sin renderer input ni dispatch.
- Consumer visual: revisar binder/materializer request-scoped, payload/frame-program, logical composition, consumo de los campos editoriales y contratos de identidad/IO. El audit histórico marcaba consumo visual 0/14; comprobar si el checkout activo contiene cambios posteriores antes de asumir que sigue igual.
- Música: `tools/c11d/d3/c11d_music_engine_v5.py` y `definitions/c11d/music/`; la existencia del engine no prueba que el delivery D lo invoque ni que el mux final preserve audio.

## 4. Ingeniería inmediata

1. Validar el nuevo snapshot con el test independiente y contrastar el inventario contra el checkout actual. Registrar el nuevo archivo/hash/commit declarado. El snapshot no sustituye el checkout activo.
2. Verificar los pins core y de continuidad actuales: `AGENTS.md`, `CONTINUE.md`, manifiesto C, Ledger V18, Checkpoint V41 y packet AD. Si cualquier pin contextual avanzó en el checkout, leer ese estado y actualizar el prompt de trabajo sin restaurar versiones del snapshot.
3. Usar el catálogo únicamente para navegar. Leer `C11D_RENDER_INTEGRATION_READ_ORDER_20261029_V3.md`; no crear más índices, planes o capas genéricas de preparación.
4. Inspeccionar estáticamente los runners C y el call path D GUI/CLI, sin ejecutar aún el renderer D. Emitir una única matriz con origen/destino de datos, contrato, consumer, path y SHA-256 por eslabón.
5. Seguir el valor de un campo editorial desde el modelo/resolver hasta el compositor físico. Determinar el primer punto en que el valor se pierde o se convierte en información no consumida. Revisar en paralelo selector, seed, frame semantics, región, timebase y música; no diseñar un binder paralelo.
6. Proponer e implementar el cambio D-only mínimo compatible con los contratos, con pruebas focalizadas y negative controls. No alterar simulación, mecánicas, RNG, los cinco GUI surfaces o los pins C.
7. Mantener la salida de producción física cerrada hasta que AD y gates técnicos habiliten el scope exacto. No crear un MP4 D para intentar convertir una política en permiso por resultado.

## 5. Gate de producción y estados de aceptación

La Fase AD queda técnicamente validada como packet (60/60 + verifier PASS), pero `PENDING_EVIDENCE_OR_KEEP_BLOCKED`; authority records = 0, decisions adjudicated = 0, policy adoption = NONE. El renderer permanece OFF. D4.8/D9.14/D9.16 siguen bloqueados, D9.17 `BLOCKED_NO_GO`, D10 bloqueado, baseline approval ausente, freeze ineligible, release authority NONE.

Se puede avanzar con análisis, cambios locales D-only y pruebas de contrato/harness que estén permitidas. No ejecutar el renderer D ni producir MP4 D hasta que exista evidencia de autoridad auténtica para la política/alcance concreto o una disposición explícita de mantenerla bloqueada, y los gates posteriores autoricen la prueba correspondiente. El permiso general para continuar el trabajo no sustituye una fila de autoridad.

## 6. Secuencia física tras autorización formal

1. Producir un Challenge, un Loop y un Drill en un directorio temporal aislado, con seeds separados por dominio.
2. Comprobar duración/FPS/dimensiones, video y audio, existencia de edición visual visible, provenance y hashes, ffprobe y reproducción real de frames. Guardar logs auténticos, versiones y exit codes.
3. Solo si el primer slice obtiene aceptación visual A/V, escalar a smoke 18 y luego matriz 101. Ejecutar el review físico sobre el output generado, no inferir aprobación desde tests estáticos.

## 7. Invariantes

C11-C 2.19.12 y su manifiesto permanecen inmutables hasta la aceptación formal de D. No mutar `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, RNG ni las mecánicas; `winning_frame` es ancla temporal y `close_calls` cuenta episodios. `request.seed` y `request.music_seed` son dominios separados. Mantener exactamente cinco superficies operativas y GUI/CLI usando el mismo servicio.
