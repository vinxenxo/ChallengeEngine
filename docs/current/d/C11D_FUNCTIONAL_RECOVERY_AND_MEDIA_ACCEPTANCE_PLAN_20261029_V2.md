# C11-D — Plan de recuperación funcional e integración de render V2

**Fecha:** 29-10-2026. **Propósito:** pasar de contratos/preparación a la integración efectiva, sin confundir ingeniería permitida con autorización de render.

## 1. Objetivo funcional

La suite `c11c-suite` debe generar con D para tres familias —Challenge, Visual Loops y Visual Drills— conservando las mecánicas C congeladas y añadiendo presentación/editabilidad universal, música y delivery. CLI y GUI deben terminar usando un único servicio canónico. El producto final incluye MP4 real y evidencia reproducible; un plan D, receipt o prueba estática no lo acredita.

El scope base actual incluye 54 Challenge, 27 gramáticas concretas Loop y 20 variantes Drill tipo/tier = 101 salidas. Smoke de 18 (9 Challenge, cinco Loops representativos, cuatro tipos de Drill). Longform queda fuera de scope. `CHALLENGE_008/009` no entran mientras continúe la discrepancia entre 11 s declarados y 12 s calculados por suma de fases.

## 2. Snapshot de trabajo inspeccionado

El ZIP subido `C11D_WORKING_CONTEXT_20261029_193950.zip` es estructuralmente válido como contexto derivado: SHA-256 `5b8d06ad82bca798c94db03f943a85afb309d91484d4499ed40fed36056ca774`, tamaño 9,190,399 bytes, CRC limpio, 3,721 entradas únicas y 3,720 entradas conciliadas con el inventario interno. El manifiesto C11-C es una sola entrada, 796,318 bytes, SHA-256 canónico `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`. El tree fingerprint `e7378235e719605fd89d601609ed34e2db9b92fc84c08de2bb7313c31187549e` se reproduce recalculando las filas en el orden preservado por el propio manifiesto, con UTF-8, tabs y LF. Ver `C11D_SNAPSHOT_VALIDATION_AND_DOCUMENTATION_REORGANIZATION_20261029_V1.md`.

El snapshot se tomó del commit declarado `be5d04c64080723e5f53d651109e45db07c43054`; es una referencia de análisis y no la autoridad para modificar archivos. El checkout Windows activo sigue mandando.

## 3. Call graph observado en el snapshot — no asumir que el flujo D ya produce vídeo

### Producción heredada C

- Challenge QA: `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1` llama a `tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1` con seeds de seis casos canónicos por reto; el flujo conserva captura Godot nativa 540×960 y usa FFmpeg para delivery 720×1280. La salida por defecto del QA queda bajo `artifacts/qa/c11c_challenge_720`.
- La GUI principal heredada de Producer vive en `c11c-suite/c11c-producer/main.py`. `MainWindow._run_challenge_job` y `_run_content_job` lanzan los scripts de producción C (`run_c11c_challenge_production.ps1`, `run_c11c_production.ps1` o el runner Drill correspondiente); los modos de revisión lanzan los runners QA C.
- La revisión física general está en `tools/qa/c11/run_c11c_complete_video_review.ps1`. Leer sus parámetros y outputs antes de ejecutarlo.

### Preparación D existente

- GUI request helper: `c11c-suite/c11c-producer/c11d_gui_request.py` construye el vocabulario D4.1 y compara request/plan GUI y CLI; es una ruta plan-only.
- D9.9 canónico: `tools/c11d/d9/universal_producer.py`; CLI: `tools/c11d/d9/universal_producer_cli.py`.
- D9.10 bridge: `tools/c11d/d9/editorial_render_bridge.py`; contrato `definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json`.
- Adapter D-only: `tools/c11d/d9/d_render_adapter.py`; contrato `definitions/c11d/production/C11D_RENDER_ADAPTER_BOUNDARY_D9_10_V1.json`. Su status es `PLANNING_ONLY_NOT_RENDERABLE`; no emite renderer input, no despacha, no crea medios ni concede autoridad.
- Modelo editorial canónico: `definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json`, con resolución en `tools/c11d/d9/universal_editorial_model.py`.
- Música: `tools/c11d/d3/c11d_music_engine_v5.py` con especificación y profile en `definitions/c11d/music/`. La existencia del engine no prueba que el delivery D final lo invoque y muxee correctamente.

**Brecha real:** el `GENERAR` heredado de Producer y runners de producción siguen siendo rutas C; la interfaz D valida y guarda request/plan/receipt plan-only. No se ha demostrado que el valor editorial canónico D llegue al compositor visual que alimenta el MP4. La revisión histórica marca consumo visual 0/14. Hay que comprobar otra vez solo si han cambiado hashes relevantes; no repetir auditorías generales por rutina.

## 4. Regla de gobernanza activa

La Fase AD quedó validada como paquete de decisión: 60/60 PASS; el verificador structural PASS. La decisión de operador sigue `PENDING_EVIDENCE_OR_KEEP_BLOCKED`; evidencias de autoridad = 0, adjudicaciones = 0, adopción de políticas = NONE. La Fase AC encontró que el corpus revisado no contenía autoridad aplicable al primer render D propio; este resultado queda acotado a ese corpus.

Por tanto:

- Se puede seguir inspeccionando código, elaborando el mapa de llamadas y trabajando en código/tests que permanezcan dentro de límites aprobados.
- **No ejecutar el renderer D ni producir un MP4 del renderer D** mientras el packet AD no recoja autoridad auténtica y verificable para el scope exacto o una decisión explícita `KEEP_BLOCKED_NO_POLICY_ADOPTION` por las filas correspondientes, y los gates técnicos posteriores no lo permitan.
- La autorización general del usuario para seguir trabajando hacia un render no rellena ni sustituye el registro de política/autoridad específico. No fabricar nombres, firma, fechas o evidencias.
- No repetir la fase AD ni crear otra fase genérica de preparación para eludir el bloqueo.

## 5. Siguiente recorrido técnico

### Paso A — verificar una vez

1. Confirmar checkout activo y SHA de `AGENTS.md`, `CONTINUE.md`, manifiesto C, Ledger V18, Checkpoint V41 y packet AD. Si el checkout contiene versiones posteriores, reconciliar sin sobrescribirlas desde snapshot.
2. Ejecutar `tools/c11d/documentation/organize_c11d_documentation.ps1 -PreflightOnly` y después el script sin esa opción para generar el catálogo vivo. No mover documentos.
3. No repetir 60/60 AD si los sources siguen byte-identical.

### Paso B — mapa de integración en un único expediente

1. Leer runners C Challenge/review y `c11c-suite/c11c-test/BUILD_MANIFEST.json`; registrar las rutas llamadas y su output root sin ejecutarlas.
2. Revisar `c11c-suite/c11c-producer/main.py` para distinguir `MainWindow._validate_c11d_request`, `_run_challenge_job` y `_run_content_job`. El tab D de request/editorial y el camino C de `GENERAR` no son el mismo flujo de producción.
3. Seguir D9.9 → D9.10 bridge → D adapter; identificar qué contrato debe cambiar para una futura entrada nativa del renderer, sin saltarse sus `false` de gobernanza.
4. Revisar request-scoped binder/materializer/payload/identity, frame program/logical composition, el audit de consumo editorial, field windows/visibility, región/timebase/temporal alignment y D3 music/mux. Escoger el menor seam real; no crear otro binder ni otra capa de preflight.
5. Entregar en el mismo expediente el mapa con paths/SHA, la interfaz que falta, un diff mínimo propuesto y tests focalizados permitidos. El código D no debe mutar `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, RNG ni mecánicas C.

### Paso C — ejecución condicionada por gates

Solo cuando el registro AD y los gates técnicos den permiso explícito: un primer MP4 aislado para una selección Challenge, una Loop y una Drill; inspeccionar streams con ffprobe, audio/sonoridad, frames y cambios visuales del campo editorial; guardar hashes/provenance/exit codes. Después ejecutar smoke 18 y matriz 101. No ejecutar matrices completas antes de aceptar el primer slice.

## 6. Arquitectura que se debe alcanzar

```text
CLI ──┐
      ├── servicio canónico D compartido ── request/profile/selector
GUI ──┘                               ├── editorial efectivo
                                      ├── generador/mecánicas C sin cambios
                                      ├── consumer visual/presentación D
                                      ├── D3 music con music_seed separado
                                      └── delivery/mux/validación → MP4 + receipt
```

Esto es el objetivo, no una afirmación de que el flujo esté cableado. Las cinco superficies siguen siendo `c11c-test`, `c11c-producer`, `c11c-catalog`, `c11c-config` y `c11c-maintenance`; no crear `c11d-control`, `c11c-studio` ni una sexta superficie.

## 7. Entregables y evidencia

Por cambio/test: paths y hashes antes/después, versiones de ejecutables, comando exacto, exit code real, stdout/stderr separados y sus hashes calculados de logs capturados. Por cada MP4, cuando esté autorizado: path/hash, identidad completa de selector/variante, seeds separados, perfil, dimensiones/FPS/duración, streams A/V, prueba de reproducibilidad, frames inspeccionados y manifiesto de artefacto.

Mantener separados los estados `PASS_CONTRACT`, `PASS_HARNESS`, `PASS_PHYSICAL_MP4`, `PASS_VISUAL_EDITORIAL_AV` y `D_ACCEPTANCE`; no derivar uno de otro.

## 8. Límites inmutables

El manifiesto congelado C11-C permanece byte-for-byte. Renderer OFF; media/payload no materializados; candidate input inadmisible; dominios seed incompletos; `master_seed=NOT_ADOPTED`; cero bindings aprobados; D4.8/D9.14/D9.16 bloqueados; D9.10 `PREPARE_ONLY`; D9.17 NO-GO; D10 bloqueado; freeze ineligible; release authority NONE. `winning_frame` ancla temporal; `close_calls` cuenta episodios, no tiempo. `request.seed` y `request.music_seed` pertenecen a dominios separados. `CHALLENGE_008/009` permanecen fuera del primer render hasta resolución explícita.
