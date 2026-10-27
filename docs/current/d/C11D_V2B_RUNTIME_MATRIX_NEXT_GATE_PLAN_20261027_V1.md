# C11-D — Próxima puerta V2-B: aceptación estática antes del runtime matrix

**Estado:** `ACTIVE_WINDOWS_STATIC_TEST_GATE_PENDING`.

## Acciones del gate

1. Ejecutar `tools/c11d/d9/test_d_renderer_challenge_visual_payload_v2b_safe_projection_runtime.py` con Python usando `-B` para evitar bytecode.
2. Aceptar únicamente exit code `0`, salida `Ran 198 tests` / `OK` y marker `C11D_V2B_RUNTIME_IMPLEMENTATION_TESTS_PASS=198/198`.
3. Verificar el contrato runtime, el diseño V2-B, el seed matrix, el contrato V2-C, los tres schemas y el estado congelado C11-C; el test valida 81 pins de fuente y 9 authority-input pins.
4. Generar `implementation_test_receipt.json` únicamente tras el PASS real, con sha de los siete archivos implementados, sha separado de stdout/stderr y sha del manifest del overlay de aceptación.
5. Validar el recibo llamando al validador estricto del propio runner V2-B. Guardar el recibo y sus logs bajo `%TEMP%`, nunca en el repositorio.

## Siguiente gate tras PASS estático

45 planner calls + 45 procesos Godot Mono independientes. Por cada selector Challenge: baseline repeat R1/R2, gameplay-seed mutation, music-seed mutation y editorial-only mutation. Debe demostrar acuerdo de repetición, cambio del safe visual state con gameplay seed, invariancia del safe state/candidate fields ante cambios de music seed y editorial, y pins intactos antes/después. Detenerse ante el primer fallo.

## No está autorizado por este gate

No renderer dispatch, no serialización de todo `custom_data`, no bindings aprobados, no candidato admitido, no media, no producción. Los conflictos temporales de `CHALLENGE_008/009` siguen bloqueados; el resultado V2-B sería evidencia source-frame, no timeline/render acceptance.
