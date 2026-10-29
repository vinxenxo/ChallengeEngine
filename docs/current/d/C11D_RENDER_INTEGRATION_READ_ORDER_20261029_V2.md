# C11-D render integration — orden de lectura y rutas de código V2

Este documento minimiza relectura y separa código de generación heredado C de la ruta D plan-only. Confirmar cada ruta en la checkout activa.

## A. Solo documentos que gobiernan la sesión

1. `AGENTS.md` y `.continue/rules/CONTINUE.md`.
2. `C11D_DOCUMENTATION_INDEX_AND_ARCHIVE_POLICY_20261029_V2.md`.
3. `C11D_SNAPSHOT_VALIDATION_AND_DOCUMENTATION_REORGANIZATION_20261029_V1.md` y el catálogo generado, si ya existe.
4. Ledger V18, Checkpoint V41, Phase AD closeout/receipt y packet AD JSON+Markdown.
5. `C11D_FUNCTIONAL_RECOVERY_AND_MEDIA_ACCEPTANCE_PLAN_20261029_V2.md`.
6. Docs C11-C `C11-C_2.19.12_ACCEPTANCE_EVIDENCE.md`, `C11-C_2.19_CONSOLIDATED_ACCEPTANCE_GATE.md`, review runbook y freeze packaging commands.

## B. Rutas de código C heredadas que producen medios

| Función | Ruta a inspeccionar | Hecho observable del snapshot |
|---|---|---|
| Matriz Challenge de referencia | `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1` | 9 Challenges × 6 casos seed; salida QA bajo `artifacts/qa/c11c_challenge_720`. |
| Producción Challenge física | `tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1` | Lanza Godot Movie Maker en resolución nativa y FFmpeg para delivery. |
| Revisión de vídeo heredada | `tools/qa/c11/run_c11c_complete_video_review.ps1` | Leer parámetros y salidas antes de usar; revisar en carpeta aislada. |
| `GENERAR` de Producer | `c11c-suite/c11c-producer/main.py` — `_run_challenge_job`, `_run_content_job` | Invoca runners de producción C, no el adapter renderer D. |
| Integración de las rutas GUI | `c11c-suite/c11c-test/BUILD_MANIFEST.json` y contratos GUI de Producer/Test | Confirmar rutas y límites de las cinco superficies, no inferir paridad de producción desde paridad de plan. |

## C. Ruta D plan-only existente

1. `c11c-suite/c11c-producer/c11d_gui_request.py`: construye request y verifica paridad de request/plan.
2. `tools/c11d/d9/universal_producer.py` + `universal_producer_cli.py`: resolución D9.9 canónica.
3. `tools/c11d/d9/editorial_render_bridge.py` y `definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json`: puente de planificación solamente.
4. `tools/c11d/d9/d_render_adapter.py` + `definitions/c11d/production/C11D_RENDER_ADAPTER_BOUNDARY_D9_10_V1.json`: envelope de inspección; adapter no despacha renderer.
5. `tools/c11d/d9/universal_editorial_model.py` + `definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json`: fuente de valores editoriales resueltos.
6. `tools/c11d/d9/d_renderer_request_scoped_payload_binding.py`, los módulos de materialización/binding relacionados, `d_renderer_frame_program.py`, `d_renderer_logical_composition.py`, `d_renderer_candidate_io_gap_audit.py`/identidad, y el `d_renderer_editorial_field_consumption_audit.py`.
7. Timebase, regiones/visibilidad, timeline/temporal alignment, y `tools/c11d/d3/c11d_music_engine_v5.py` más el código real de mux/delivery.

Lee solo los contratos y tests directos de la ruta descubierta. Versiones viejas bajo `docs/history/c11d/` sirven de contexto y no desplazan la fuente actual.

## D. Brecha que debe verificarse

La ruta D produce `PLANNED`/bridge `PLANNING_ONLY_NOT_RENDERABLE`; la interfaz D mantiene renderer y execution en false. En el snapshot no se ha demostrado que los valores editoriales resueltos se consuman en frames del vídeo final, ni que el flujo D comparta el servicio de producción final en GUI y CLI. El registro histórico de auditoría muestra 0/14 campos editoriales consumidos visualmente; verificar el hash del audit/consumer antes de reutilizar el dato.

## E. Ejecución y gates

Leer antes de ejecutar cualquier runner y cambiar su `OutputRoot` a un directorio de prueba único. No lanzar renderer D ni producir MP4 D mientras el packet AD y gates posteriores no den permiso explícito. La instrucción general de avanzar hacia el render autoriza seguir con ingeniería dentro de los límites; no equivale a política AD aprobada. No repetir la suite AD de 60 pruebas mientras sus inputs estén byte-identical.
