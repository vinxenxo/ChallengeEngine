# C11-D — Diagnóstico del post-check de líneas resumen (Fase M)

**Fecha:** 27-10-2026. **Estado:** corrección del validador preparada; aceptación Windows pendiente.

## Hecho observado

La matriz runtime se ejecutó una sola vez: `45/45` llamadas al planner, `45/45` procesos Godot Mono, `9/9` filas de selector y hashes de 90 archivos de evidencia verificados por el aceptador. El reporte existente tiene SHA-256 `6e19e88bcce6249f613c7e8566b92f78497c4749bfd079dda2b01e20385072a0`; stdout agregado tiene SHA-256 `939dc1c7a3891c03418f72c72f6d40a8067ad47b01e7de2af4de1acb25e4dabb`; stderr está vacío con SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`.

## Causa precisa

El aceptador V1 exigía en el archivo `runtime_matrix.stdout.txt` ocho líneas. Dos de ellas (`C11D_V2B_RUNTIME_REPORT=` y `C11D_V2B_RUNTIME_REPORT_SHA256=`) fueron emitidas por el wrapper mediante `Write-Host`, hacia la consola interactiva, y no aparecen en la captura stdout del proceso secundario. La validación del reporte, conteos, sensibilidad, filas, locks, pins y archivos de evidencia llegó a `True`; el fallo detectado fue la presencia de esas dos líneas de resumen duplicadas.

## Corrección

La versión V2 de la utilidad de aceptación deja de exigir únicamente esas dos líneas en stdout. No acepta sus valores ciegamente: la ruta del reporte se deriva de la carpeta de evidencia asociada al marcador de intento, su SHA se computa desde disco y debe coincidir con el valor fijado; también se conserva la comprobación de schema, status, 45/45, nueve filas, las cinco variantes en orden, hashes de los archivos evidenciales, source pins, recibo estático y bloqueos de gobernanza. El resto de líneas operacionales exigidas debe seguir apareciendo en stdout.

La recuperación V2 **no** vuelve a ejecutar el planner, Godot, ni la matriz; no cambia contratos, código de producción, checkpoint ni ledger al aplicar el parche. El aceptador vuelve a ejecutar solo validación sobre la evidencia existente y escribirá aceptación documental únicamente si todas las verificaciones pasan.

## Límites de la fase

Aunque la Fase M pase la aceptación, la evidencia corresponde a estado visual seguro en memoria y sensibilidad de hash. No es vídeo renderizado, no aprueba bindings, no materializa payload ni media y no admite candidato. La discrepancia de duración de `CHALLENGE_008/009` (11 segundos declarados frente a 12 segundos de fases) permanece pendiente. Los locks (`renderer=OFF`, `media_created=false`, `candidate_input_admissible=false`, `D4.8=BLOCKED`, `release_authority=NONE`) siguen vigentes.
