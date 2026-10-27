# C11-D — Aceptación Windows V2-C Source-Frame Runtime (Fase N)

**Estado:** WINDOWS_PASS_SOURCE_FRAME_ROUTE_ONLY; NO_RENDER; NO_MEDIA; GOVERNANCE_LOCKS_PRESERVED.

## Evidencia validada en el checkout Windows

- Python contract tests 28/28; stdout SHA-256 $ExpectedV2CTestStdoutSha; stderr vacío, SHA-256 $ExpectedEmptySha.
- Contrato source-frame pins 81/81; planner canónico 9/9; sonda de identidad Godot 1/1; runtime Godot Mono independiente 18/18; selectores 9/9; archivos stdout/stderr de proceso verificados 36/36.
- Reporte: $ReportPath; SHA-256 $ExpectedRuntimeReportSha; status PASS_SOURCE_FRAME_ROUTE_ONLY.
- Runtime stdout: $RuntimeStdoutPath; SHA-256 $ExpectedRuntimeStdoutSha; stderr: $RuntimeStderrPath; SHA-256 $ExpectedEmptySha (vacío).
- Godot 4.7.1.stable.mono.official.a13da4feb. Todos los recibos son SOURCE_FRAME_RECEIPT; los IDs de proceso y run son únicos y cada selector presenta acuerdo entre las dos repeticiones.
- Se comprobaron 36 artefactos contra el mapa de SHA-256 del propio informe. Las filas de selector están en orden CHALLENGE_001 a CHALLENGE_009, con estado ACCEPTED_SOURCE_FRAME_ONLY y sin block reasons.
- Cada recibo usa ChallengeRuntimeBridge.run_effective_pipeline. Los flags de side-effect informan alse para payload escrito, media creada, renderer-native input emitido, nodos de render, render server llamado, viewport capturado, estado canónico mutado y dispatch de producción.

## Interpretación y límites

Esta aceptación demuestra un recibo source-frame repetible en una ruta runtime efectiva para los nueve Challenges. No es una aprobación de render: el bridge permanece PLANNING_ONLY_NOT_RENDERABLE y el adaptador PREPARED_NOT_DISPATCHED_RENDERER_DISABLED. isual_seed_sensitivity=NOT_TESTED; no demuestra píxeles, texto dibujado, proyección de entrega, sincronización final ni vídeo. El sidecar editorial sigue sin tener bindings aprobados. El conflicto temporal de CHALLENGE_008/009 (11 segundos declarados frente a 12 segundos de fases) sigue bloqueado.

## Siguiente puerta

Fase O: auditar de solo lectura los recibos source-frame y cruzarlos con la propuesta de binding semántico. Clasificar disponibilidad, linaje, naturaleza temporal y alcance de cada dato candidato, especialmente winning_frame, close_calls y candidatos de custom_data. El cruce no puede declarar bindings aprobados; requiere decisiones explícitas y evidencia propia.

## Gobernanza

enderer=OFF; media_created=false; payload_materialized=false; candidate_input_admissible=false; seed_domains_complete_for_candidate_input=false; pproved_bindings=0; pproved_custom_data_bindings=0; pproved_renderer_projection_bindings=0; D4.8=BLOCKED; D9.10=PREPARE_ONLY; D9.14=BLOCKED; D9.16=BLOCKED; D9.17=BLOCKED_NO_GO; D10=BLOCKED_FOR_PROMOTION; aseline_approval=MISSING; reeze_eligible=false; elease_authority=NONE.

## SHA-256 de documentación tras write-back

- Checkpoint: 9cccc148927a950a14f76a9e7afb13c1e0d8b8fa1f3ac556a7f01c7244985f2d.
- Ledger: 7f44a13f633bd8847cfc60f24d635df6dfe17fb8024af38b8bf2404b68d2fa28.
- Este registro: se calcula al finalizar el write-back y se incluye en el manifiesto dinámico de Temp.
