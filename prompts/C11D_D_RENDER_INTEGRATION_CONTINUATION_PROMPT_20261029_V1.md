# Prompt listo para continuar C11-D hacia la integración de render

Actúa sobre el proyecto `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. El snapshot de contexto está validado y se ha preparado el organizador documental; el catálogo live puede no existir aún. No vuelvas a generar el snapshot ni repitas las fases documentales ya aceptadas. Usa el checkout Windows activo como autoridad y el snapshot `C11D_WORKING_CONTEXT_20261029_193950.zip` solo como referencia del árbol revisado (commit declarado `be5d04c64080723e5f53d651109e45db07c43054`, SHA-256 `5b8d06ad82bca798c94db03f943a85afb309d91484d4499ed40fed36056ca774`).

## Lectura mínima

Lee `AGENTS.md`, `.continue/rules/CONTINUE.md`, el índice documental V2, el informe de validación del snapshot, el catálogo generado si existe, el plan funcional V2 y el mapa de lectura V2. Verifica los hashes reales de AGENTS, CONTINUE, manifiesto C, Ledger V18, Checkpoint V41 y los tres archivos principales de Phase AD. No sobrescribas divergencias a partir del ZIP.

## Estado real que debes preservar

Phase AD valida su packet (60/60 + verifier PASS), pero la decisión del operador continúa `PENDING_EVIDENCE_OR_KEEP_BLOCKED`: authority evidence records = 0, decisions adjudicated = 0, policy adoption = NONE. Renderer OFF; D9.10 `PREPARE_ONLY`; D4.8/D9.14/D9.16 bloqueados; D9.17 `BLOCKED_NO_GO`; D10 bloqueado; baseline approval ausente; freeze ineligible; release authority NONE. R-08/R-09 siguen en 11 s declarados frente a 12 s por suma de fases. No reabrir AD, no generar otra fase preparatoria y no inferir autorización desde una petición general de avanzar.

## Trabajo inmediato

1. Ejecuta el organizador documental instalado en modo preflight y después normalmente para mantener un catálogo vivo de los documentos D. Este script no mueve ni renombra fuentes.
2. Verifica sin ejecutar los entrypoints físicos C: `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1`, `tools/qa/c11/run_c11c_complete_video_review.ps1` y `tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1`. Inspecciona también `c11c-suite/c11c-test/BUILD_MANIFEST.json`.
3. En `c11c-suite/c11c-producer/main.py`, diferencia el `GENERAR` heredado (`_run_challenge_job`/`_run_content_job`, que llaman runners C) de los tabs D plan-only. Sigue `c11c-suite/c11c-producer/c11d_gui_request.py` → `tools/c11d/d9/universal_producer.py` / `universal_producer_cli.py` → `editorial_render_bridge.py` → `d_render_adapter.py`.
4. Traza el campo editorial desde `definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json` y su resolver hasta request-scoped binding/materialization, visual payload/frame program/logical composition y el compositor final. Contrasta con `d_renderer_editorial_field_consumption_audit.py`, el contrato I/O/identity y políticas de región/timebase. Inspecciona D3 music engine y el mux real. No crees un binder paralelo.
5. Produce un mapa con paths y SHA actuales, identifica el primer consumer real ausente y propone/implementa el cambio mínimo D-only compatible con los contratos. Ejecuta tests focalizados permitidos, guardando comandos, versiones, exit code y stdout/stderr hashes auténticos. No cambies `SimulationResult`, `winning_frame`, `close_calls`, RNG, mecánicas C, manifest congelado ni las cinco superficies canónicas.
6. No invoques el renderer D ni generes MP4 D hasta que el packet AD contenga evidencia auténtica o una disposición explícita de mantener bloqueada cada política relevante, y los gates técnicos posteriores lo autoricen. Después de autorización formal, probar un Challenge, un Loop y un Drill con root temporal aislado, comprobar vídeo/audio/frames y diferencias editoriales visibles; luego extender a 18 y 101.

La tarea de esta ventana es ingeniería funcional real, no otro plan genérico. Si el gate impide una ejecución física, sigue con análisis/código/test permitidos y señala el campo/decisión concreto que la bloquea sin alterar flags. C11-C 2.19.12 continúa siendo la referencia de producción congelada hasta la aceptación formal de D.
