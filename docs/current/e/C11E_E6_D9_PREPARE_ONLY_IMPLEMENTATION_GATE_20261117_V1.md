# C11-E E6 — Gate de implementación D9 PREPARE_ONLY V1

**Estado:** `DESIGN_GATE_READY / IMPLEMENTATION_NOT_STARTED`  
**Límite:** preparación estructurada E1/D; ninguna ejecución de Godot o media.

## Objetivo

Añadir una única costura D-owned de orquestación para los seis grupos Challenge de E6. La costura debe coordinar las 18 subpruebas A/B/C y emitir un recibo auditable que enlace selector, config, gameplay seed, music seed propuesta, timebase nativo, E1 intent hash y D envelope hash. El denominador Smoke18 continúa siendo seis Challenge + seis Loop + seis Drill; las 18 filas A/B/C son subpruebas de los seis Challenge, no escenarios adicionales.

## Reutilización obligatoria

1. Reutilizar `c11c-suite/c11c-producer/c11e_production_service.py` como único servicio E1.
2. Reutilizar el contrato plan-only E6 ya aceptado y su lógica de envelopes. No rehacer la generación de 18 intents/envelopes.
3. Reutilizar el consumidor Challenge genérico y el adaptador D ya existentes, sin modificar binders ni GeneradorMaestro.
4. Conservar cada familia y cada timebase. No introducir producer paralelo, binder paralelo, renderer paralelo, módulo de suite nuevo ni `c11d-control`.

## Contrato de preparación

- Input: matriz E6 congelable, source-pin set de 33 entradas, 6 definiciones Challenge, perfil/layout aprobados en el alcance E4A y parámetros E1 ya determinados por el plan-only aceptado.
- Filas: seis selectores × A, B_REPEAT, C_CHANGED_MUSIC_SEED = 18.
- A/B: misma identidad de gameplay y música; C: solo cambia `music_seed`; el gameplay seed permanece fijo.
- La matriz de seeds es provisional donde dependa de fixtures 840001/840002; no se convierte a defaults de producto. `tempo_bpm` y `duration_seconds` permanecen no resueltos en E1.
- Salida: `PREPARE_ONLY` manifest, 18 E1 intent references, 18 D envelope references, checksums, lineage, preflight findings y un recibo con identidad única.
- No reservar BatchId de ejecución, no construir comandos de Godot, no abrir procesos externos, no escribir en rutas de medios.

## Stop conditions

Bloquear antes de materializar cuando exista cualquiera de estos casos: pin ausente o divergente; selector no canónico; identidad E1/D discordante; relación A/B/C incorrecta; timeline/frame count discordante; seed de música no adoptado; salida colisionada; origen de evidencia indeterminado; intento de habilitar renderer, media o dispatch.

## Pruebas mínimas para la implementación

1. Matriz exacta de seis selectores y 18 subpruebas, sin CH003/008/009.
2. Cada grupo contiene exactamente A/B/C.
3. A/B conserva `request.seed` y `request.music_seed`; C conserva gameplay y cambia solo música.
4. Cada intent hash y envelope hash se resuelve exactamente una vez.
5. Fases half-open continuas y fuente 60fps con total nativo igual a la suma de fases.
6. No llamadas a Godot, FFmpeg, FFprobe, D3, audio, mux ni subprocess.
7. No BatchId consumido, no media, no dispatch, release `NONE`.
8. Test de rollback y de colisión `ADD_ONLY`; escritura atómica de recibo/sidecar.
9. PS 5.1 AST + pruebas de transacción; no Git/HEAD/status/branch.

## Lo que este gate no habilita

No es E6 TEST_ONLY, no resuelve D4.8, no autoriza Smoke18, no acepta el ledger Loop/Drill/CH004, no adopta 840001/840002/104 BPM ni resuelve `tempo_bpm`/`duration_seconds`. No invocar Godot, Movie Maker ni herramientas multimedia en esta fase.
