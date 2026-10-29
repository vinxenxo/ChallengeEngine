# C11-D — Master Prompt de integración funcional de render V3

## 1. Rol y objetivo

Actúa como ingeniero principal del proyecto `C:\Users\vinxe\Projects\ChallengeEngineV01_STATELESS`. La tarea inmediata es la integración funcional real del pipeline de presentación D con la generación física que ya existe en C, no volver a planificar el proyecto ni producir más documentación genérica.

Objetivo de producto: Challenge, Visual Loops y Visual Drills deben compartir un servicio canónico GUI/CLI, conservar mecánica C y admitir composición/editorial universal, música y delivery. El scope de aceptación está acotado a 18 salidas de smoke y 101 de matriz; Longform fuera de scope y `CHALLENGE_008/009` excluidos por la discrepancia de 11 s declarados frente a 12 s de suma de fases.

## 2. Fuente de verdad

La fuente principal es el checkout activo Windows, incluyendo evidencia local. El snapshot subido en esta nueva conversación es copia filtrada para contexto y debe validarse con su sidecar/informe. El snapshot pre-migración `C11D_WORKING_CONTEXT_20261029_193950.zip`, SHA `5b8d06ad82bca798c94db03f943a85afb309d91484d4499ed40fed36056ca774`, no debe reemplazar la nueva versión ni el checkout.

Orden: `AGENTS.md` → `.continue/rules/CONTINUE.md` → manifiesto frozen C → Ledger V18/Checkpoint V41 y packet AD con hashes reales → índice V3/catálogo/mapa → contratos y código fuente específico. Si los hashes contextuales del checkout activo han avanzado, reconcilia. No sobrescribas estado nuevo con el snapshot.

## 3. Qué se hizo en documentación

La raíz se inspeccionó desde el snapshot. Había 120 candidatos D/metadata; dos README están incluidos por ruta en el manifiesto congelado C11-C y deben seguir byte-identical en raíz. Otros archivos con referencias entrantes continúan en raíz, con razón documentada en `C11D_ROOT_DOCUMENTATION_MIGRATION_MAP_GENERATED.json`. Los README de overlay sin pin/reference se archivan por categoría bajo `docs/history/d/root-documentation/`; el catálogo ahora incluye ese árbol y la metadata histórica D que quede en raíz.

Los scripts de migración y tests incluidos son herramientas operativas. Si el overlay se ha instalado, el usuario debe haber corrido `Test-C11DDocumentationReorganization.ps1 -ApplyRootMigration -GenerateSnapshot` y subir el ZIP/sumario/reporte generado. No vuelvas a hacer la migración si el mapa generado ya valida; no repitas este trabajo de documentación.

## 4. Gobernanza y límites

Los pins core esperados son:

- `AGENTS.md`: `0d4565e57b9fe9bba88a88f10babd175f3bb5e3fb437014866ed1e67d3016b37`
- `.continue/rules/CONTINUE.md`: `52776e55023a36e1ead71cf39a93337ca96f6097bd2c88018c3353484145ac86`
- `release/C11C_FREEZE_PACKAGE_MANIFEST.json`: `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`, 796.318 bytes.

Ledger V18 SHA `7731b98a79ca3b0cbe42256866bb8c1093389c40d5fe502bbfba7ac038b2ea90`; Checkpoint V41 SHA `2d2f165872e76f40afa86fbf774500c1a97c5cec3c193e26c9cc46c39f2f5ff4`; Phase AD closeout SHA `22ed115bb58f9a9c84bb4942cd86af1f6d5a7bd2b72c3981037f209768ee4652`; receipt SHA `800cf33d7e53af989d05d5b8096d11e2909d1c486a6ebc469f025b0ea5bb94f3`; decision gate SHA `63339254dd444c38a932b8b582bc0af600d309786f46d1e8dd2b92dbf07054e5`. Recheck, do not assume.

Phase AD package validation = 60/60 plus verifier PASS; **operator decision remains `PENDING_EVIDENCE_OR_KEEP_BLOCKED`**, evidence records 0, adjudications 0, policy adoption NONE. `renderer=OFF`; D9.10 `PREPARE_ONLY`; D4.8/D9.14/D9.16 blocked; D9.17 `BLOCKED_NO_GO`; D10 blocked; baseline approval missing; freeze ineligible; release authority NONE. General approval to continue engineering does not override a gate-specific policy/authority record. No MP4 D until exact gates authorize it.

C11-C 2.19.12 remains frozen. Never modify `SimulationResult`, `winning_frame`, `close_calls`, `WinningFrameDetector`, `RenderedFrameStream`, RNG or C mechanics. `winning_frame` anchors time; `close_calls` counts episodes. `request.seed` and `request.music_seed` must remain separate. Keep the five canonical surfaces; no `c11d-control`, `c11c-studio` or sixth GUI.

## 5. First engineering pass

1. Validate the new snapshot and its internal manifest, external `.sha256` and `.report.json`. Compare it with the active checkout, especially any current changes post-snapshot.
2. Read `C11D_RENDER_INTEGRATION_READ_ORDER_20261029_V3.md` and inspect:
   - C physical runners `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1`, `tools/qa/c11/run_c11c_complete_video_review.ps1`, `tools/prototypes/c11c_bulk/run_c11c_challenge_production.ps1`.
   - `c11c-suite/c11c-test/BUILD_MANIFEST.json` and `c11c-suite/c11c-producer/main.py` (`_run_challenge_job`, `_run_content_job`, D GUI/CLI paths).
   - `c11c-suite/c11c-producer/c11d_gui_request.py` → `tools/c11d/d9/universal_producer.py` / CLI → `universal_editorial_model.py` → `editorial_render_bridge.py` → `d_render_adapter.py`.
3. Follow one real editorial property end-to-end through request-scoped carrier, binding/materialization, payload/frame program, logical composition, compositor and renderer input. Read the current consumption audit and contracts; check actual current SHA. Identify the earliest consumer that is missing or dropping the value.
4. In the same technical record, trace frame identity/timebase, selector/seed domain, region/projection policy and D3 music to delivery/mux. Don't create a second binder or service path.
5. Implement only the minimal D-only change that closes the proven seam, add focused positive and negative tests, and capture exact command/version/exit code/log hashes. Run tests allowed by existing gates.
6. Do not invoke renderer D or emit MP4 until Phase AD has authentic evidence or explicit `KEEP_BLOCKED_NO_POLICY_ADOPTION` for applicable rows and downstream gates authorize a physical test. After authorization: isolated Challenge+Loop+Drill slice, inspect streams/audio/frame timeline/editorial visibility, then 18 smoke and 101 full matrix.

## 6. Evidence quality

Distinguish `PASS_CONTRACT`, `PASS_HARNESS`, `PASS_PHYSICAL_MP4`, `PASS_VISUAL_EDITORIAL_AV` and `D_ACCEPTANCE`. They are independent. No stale PASS. Any report records actual checkout paths/hashes, executable versions, command line, exit codes, stdout/stderr hashes and artifacts' provenance. A static test is not GUI runtime proof; a produced MP4 without visual/editorial review is not A/V acceptance.

## 7. Done criterion for the next work slice

The next slice is complete when one concise, hash-bound call graph proves the actual C physical path and D plan path, names the first missing renderer consumer, records a minimal implementation diff and focused test results, and either (a) closes that permitted technical gap or (b) names the exact gate/policy field that blocks the next operation. Do not spend another iteration just renaming or indexing documents.
