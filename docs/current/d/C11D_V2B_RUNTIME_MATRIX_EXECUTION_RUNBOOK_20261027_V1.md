# C11-D — V2-B source-state seed matrix: Windows execution runbook

**Estado al preparar esta puerta:** `PHASE_L_STATIC_PASS; RUNTIME_MATRIX_NOT_YET_EXECUTED`  
**Fecha:** 27-10-2026

## Evidencia precedente aceptada

La ejecución del operador en Windows aceptó la puerta estática V2-B:

- `tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_safe_projection_runtime.py`: exit `0`; `198/198` tests; marker `C11D_V2B_RUNTIME_IMPLEMENTATION_TESTS_PASS=198/198`.
- Source pins `81/81`; authority-input pins `9/9`.
- Recibo estricto temporal: SHA-256 `aa8cebd453b632e445becb936ff3520110d5f80fdf2a732818a6917885595e32`.
- Test stdout SHA-256 `02cf98c041d0e3c40282164500df99e16f0b058eb9d899081ada30829bd1cd43`; stderr SHA-256 `a14048cc73bbcda88c44e7bd7f889396ad73af5efb76cf0e91e32c889db99f8d`.
- Checkpoint SHA-256 `93c07fd260e1cb56870e8448882f330a91b523fa735cad844ba2d941f041953b`; ledger SHA-256 `7155a14a03cd4a24e0eed00d04fefe086ea355e041f56bb1e2d2d485ac50121d`; aceptación fase L SHA-256 `9be3d49f5498f87783c30db69fa0e6a47d0721a17b86258926077c7d10933d8f`.
- La recuperación documental no repitió los tests ni invocó Godot. El manifiesto congelado C11-C sigue inalterado.

## Propósito de la fase M

Ejecutar `tools/c11d/d9/d_renderer_challenge_visual_payload_v2b_safe_projection_runtime.py` con el recibo estático ya aceptado. La matriz tiene nueve selectores y cinco variantes por selector:

1. `BASELINE_R1`
2. `BASELINE_R2` — repetición en un proceso independiente
3. `GAMEPLAY_SEED_MUTATION`
4. `MUSIC_SEED_MUTATION`
5. `EDITORIAL_MUTATION`

Denominadores de aceptación: `45/45` invocaciones del planner canónico y `45/45` procesos independientes de Godot Mono 4.7.1. La implementación se detiene ante el primer fallo y conserva los logs por proceso.

## Condiciones de aceptación

- Cada `BASELINE_R1/R2` debe coincidir en request/plan identity, estado visual seguro y probes por campo; PID y run ID deben ser distintos.
- La mutación de gameplay seed debe cambiar el hash del estado visual seguro para cada mecánica; `CHALLENGE_003.target_x` es la excepción de campo, no del estado visual completo.
- Cambiar únicamente `music_seed` debe dejar invariantes el estado visual seguro, los probes de candidato y el hash de entrada de simulación.
- Cambiar solo el contenido editorial debe dejar invariantes el estado visual y la entrada de simulación.
- El runner y su recibo deben mantener todos los source pins, las nueve filas y los locks de gobernanza. Una ejecución parcial o un informe bloqueado no equivale a PASS.

## Límite y efectos prohibidos

Esta es una matriz de observación de estado de origen en memoria, **no una prueba de render de vídeo**. No se permite materializar payload, escribir media, emitir entrada nativa al renderer, capturar Viewport, despachar producción ni aprobar bindings. Permanecen `renderer=OFF`, `media_created=false`, `payload_materialized=false`, `candidate_input_admissible=false`, `approved_bindings=0`, `D4.8=BLOCKED` y `release_authority=NONE`.

Las discrepancias de duración de `CHALLENGE_008/009` (11 segundos declarados frente a 12 segundos de fases), la proyección de coordenadas y el remuestreo de entrega siguen pendientes.

## Procedimiento operativo

1. Aplicar el overlay add-only con el shell facilitado en la conversación; no extraer el ZIP manualmente.
2. Desde la raíz exacta del checkout, ejecutar `tools/c11d/d9/run_d_renderer_challenge_visual_payload_v2b_seed_matrix_20261027.ps1`.
3. Entregar la salida terminal completa y los hashes/paths impresos. Las evidencias completas se conservan en `%TEMP%`.
4. Tras un PASS real, preparar un overlay de aceptación separado para checkpoint, ledger y registro de fase. No marcar la fase como aceptada antes del resultado del operador.

Si aparece un marcador `started` sin marcador `completed`, no volver a ejecutar a ciegas ni eliminar marcadores/logs. Conservar el reporte `BLOCKED`, los stdout/stderr y analizar la primera causa.
