# C11-D Render Integration — Windows Execution & Evidence Prompt V1

Usar desde la raíz del checkout activo en Windows PowerShell 5.1. Esta guía es para ejecutar pruebas solo después de revisar el output root y el alcance de cada runner. No ejecutar la matriz completa hasta que el primer MP4 D haya sido validado.

## Principios de ejecución

- Usar el Python 3.13 del entorno de trabajo cuando lo exija la documentación del gate; registrar la ruta/version exacta. No asumir que el Python resuelto por PATH es el correcto.
- Para procesos externos, usar `Start-Process -PassThru -Wait` con archivos separados de stdout/stderr, comprobar exit code y validar los archivos/marcadores antes de imprimir PASS.
- No usar `&&`, `Read-Host`, interpolaciones PowerShell ambiguas ni `Expand-Archive` como método de instalación de overlays. Para el snapshot histórico no hacer extracción total.
- Cada run usa un identificador único y un directorio de evidencia fuera de `release/` y fuera de outputs productivos.
- Nunca reutilizar un output de una ejecución anterior como si fuera el del run actual.

## Orden recomendado de ejecución tras implementar el consumer D

1. Verificar pins y manifiesto C.
2. Test unitario del consumer D + tests de request/binder/edición afectados.
3. Test real Godot del renderer/consumer y captura de salida de proceso.
4. Smoke MP4 A/V de 1 Challenge + 1 Loop + 1 Drill.
5. Inspeccionar `ffprobe`/FFmpeg y frames; comparar un campo editorial modificado contra baseline.
6. Solo si el smoke es PASS, correr 18 salidas de cobertura.
7. Solo después ejecutar la matriz completa de 101 salidas y sus regresiones.
8. GUI: abrir el Producer existente, seleccionar la misma solicitud y producir el mismo tipo; comparar identidad de solicitud, effective editorial map y manifest. Añadir prueba del Test GUI usando el route manifest existente.
9. Recoger la aceptación de las cinco superficies según el procedimiento que ya existe; no confundir Qt offscreen con observación humana.
10. Ejecutar regresiones generales y evaluadores D9.14/D9.16/D9.17/D10 en el orden definido por sus contratos.

## Matriz mínima de MP4 válido

- MP4 presente, tamaño no-cero, container/codec legible.
- Dimensiones, frame rate, duración, frame count y profile coinciden con el manifest/contrato.
- Audio disponible si el perfil lo exige; estéreo, duración alineada y loudness no silencioso mediante la comprobación existente. No concluir que hay audio por la existencia de un WAV únicamente.
- Hash de video y audio capturados después de cerrar el proceso de render/mux.
- Los valores editoriales están en el payload/consumer real y aparecen en frames; guardar hashes/índices de los frames revisados.
- Repetición determinista según el contrato; gameplay seed y music seed cambian solo los dominios que les pertenecen.
- Si falla una condición, registrar FAIL con el motivo y los artefactos reales; no se admite un PASS parcial sin acotar el alcance.
