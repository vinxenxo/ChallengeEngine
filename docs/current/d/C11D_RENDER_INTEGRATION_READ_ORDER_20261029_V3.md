# C11-D — Orden de lectura para integración C→D y render V3

Este orden es una ruta de ingeniería desde el checkout actual, no otra fase de planificación. Antes de tocar código, registra hashes de los archivos consultados y anota cualquier divergencia respecto al snapshot. Usa el catálogo generado para localizar documentación; no le atribuyas autoridad de decisión.

## 0. Validación de entrada

1. Abre el nuevo `C11D_WORKING_CONTEXT_*.zip`, su `.sha256` y `.report.json`. Ejecuta `Test-C11DWorkingSnapshot.ps1` sobre el ZIP antes de confiar en el contenido.
2. Confirma los SHA actuales de `AGENTS.md`, `.continue/rules/CONTINUE.md`, `release/C11C_FREEZE_PACKAGE_MANIFEST.json`, Ledger V18, Checkpoint V41 y los tres artefactos de Phase AD. Detente si los pins core difieren; si los pins D contextuales han avanzado, usa el estado del checkout activo.
3. Lee `C11D_DOCUMENTATION_INDEX_AND_ARCHIVE_POLICY_20261029_V3.md`, `C11D_ROOT_DOCUMENTATION_REORGANIZATION_POLICY_20261029_V1.md`, `C11D_ROOT_DOCUMENTATION_MIGRATION_MAP_GENERATED.md` y el catálogo. No vuelvas a ejecutar la migración documental si el mapa ya valida los hashes.

## 1. Ruta física C y GUI `GENERAR`

Lee, pero no ejecutes, salvo autorización de un test C expresamente requerido:

- `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1`
- `tools/qa/c11/run_c11c_complete_video_review.ps1`
- `tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1`
- `c11c-suite/c11c-test/BUILD_MANIFEST.json`
- `c11c-suite/c11c-producer/main.py`, especialmente `_run_challenge_job`, `_run_content_job` y rutas de revisión/producción

Registra runner, argumentos, seed, output root, resolución/timebase, ffmpeg/mux y contrato/recibo por ruta. Identifica de forma explícita qué hace realmente el flujo heredado de `GENERAR`; no lo llames D solo porque se haya añadido un editor D.

## 2. Cadena request D y edición universal

Sigue el código y sus hashes actuales, en este orden:

1. `c11c-suite/c11c-producer/c11d_gui_request.py`
2. `tools/c11d/d9/universal_producer.py` y `universal_producer_cli.py`
3. `definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json`
4. `tools/c11d/d9/universal_editorial_model.py`
5. `tools/c11d/d9/editorial_render_bridge.py` y `definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json`
6. `tools/c11d/d9/d_render_adapter.py` y `definitions/c11d/production/C11D_RENDER_ADAPTER_BOUNDARY_D9_10_V1.json`

Distingue el request/plan/receipt plan-only del input consumible por renderer. No infieras que D9.10 realiza dispatch si contrato/código dice `PREPARE_ONLY` o `PLANNING_ONLY_NOT_RENDERABLE`.

## 3. Primer consumidor visual real

Traza un campo editorial canónico, por ejemplo un valor de color, título/etiqueta o posición que deba verse en el vídeo:

`editorial model/resolver → GUI/CLI request-scoped carrier → binding/materialization → visual payload → frame program/logical composition → compositor físico → render adapter/renderer input → salida de vídeo`.

Inspecciona:

- `tools/c11d/d9/d_renderer_editorial_field_consumption_audit.py` y su test
- binder/materializer request-scoped y los contratos de payload/identidad/I/O
- `tools/c11d/d9/d_renderer_visual_payload*`, `tools/c11d/d9/*frame*program*`, logical composition y coordinate consumer, resolviendo paths exactos desde el catálogo
- contratos/políticas de semántica de región, visibilidad, proyección de coordenadas, alineación temporal y delivery timebase

No crees un binder alternativo. El primer artefacto técnico debe ser una matriz de datos por eslabón (path, SHA-256, símbolo, input/output, contrato, test existente, consumer siguiente, evidencia de gap). Selecciona un único punto de pérdida con evidencia de código.

## 4. Música, mux y salida A/V

Inspecciona `tools/c11d/d3/c11d_music_engine_v5.py`, definiciones/profile de música, salida de audio, delivery y mux final. Verifica cómo se propaga `request.music_seed` sin compartir dominio con `request.seed`. El código de música no prueba que el compositor/mux la integre.

## 5. Tests permitidos

Prioriza unit tests/contract tests existentes, auditorías read-only, negative controls y tests de GUI/CLI parity en scope no productor. Captura comandos, versiones, exit code, stdout/stderr y hash de cada log. No etiquetes un test estático o harness como aceptación física.

Los primeros entregables son el mapa de llamadas y el diff mínimo D-only con tests focalizados. La generación real de MP4 D continúa cerrada mientras el estado de autoridad AD y los gates técnicos lo mantengan bloqueado.

## 6. Restricciones de diseño

No cambiar el manifiesto congelado C ni la mecánica; no mutar `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream` o RNG. `winning_frame` es ancla temporal; `close_calls` es recuento de episodios. No crear una sexta GUI/superficie: solo `c11c-test`, `c11c-producer`, `c11c-catalog`, `c11c-config`, `c11c-maintenance`. CLI y GUI deben compartir el mismo servicio canónico D.

## 7. Gate explícito

Phase AD (60/60 + verifier PASS) sigue con decisión `PENDING_EVIDENCE_OR_KEEP_BLOCKED`, 0 authority evidence records, 0 adjudications y policy adoption NONE. Renderer OFF; D9.10 PREPARE_ONLY; D4.8/D9.14/D9.16 bloqueados; D9.17 BLOCKED_NO_GO; D10 bloqueado; baseline approval ausente; release authority NONE. `CHALLENGE_008/009` siguen aparcados por el conflicto 11 s/12 s.

La autorización general de trabajo sirve para continuar análisis y cambios permitidos; no habilita el renderer D, MP4 físico, freeze ni promoción. No alteres booleanos ni fabriques evidencia para cruzar ese gate.
