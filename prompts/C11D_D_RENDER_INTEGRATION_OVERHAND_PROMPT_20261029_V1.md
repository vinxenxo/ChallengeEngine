# C11-D Render Integration — Overhand / Handover Prompt V1

Al cerrar una ventana de contexto, prepara la continuidad para la siguiente sin perder la meta funcional ni declarar como ejecutado lo que no ocurrió.

## Registrar estado real

1. Identificar la checkout activa y registrar los pins verificados de `AGENTS.md`, `.continue/rules/CONTINUE.md`, manifiesto C, ledger y checkpoint D. No confundir un snapshot exportado con la checkout.
2. Registrar cada cambio de código y contrato: path, antes/después SHA-256, bytes, razón, tests focalizados y efectos sobre dependencias.
3. Para cada test: comando exacto, ejecutable/versiones, exit code real, líneas marcador, stdout/stderr separados y sus SHA-256. No generar hashes de logs que no se capturaron.
4. Para cada vídeo: ruta de test, selector completo, seeds separados, request/editorial identity, perfil, dimensiones/FPS/duración, audio/canales/loudness, hashes de MP4/WAV/receipts, resultado ffprobe/FFmpeg y revisión de frames.
5. Diferenciar: PASS de contrato, PASS de harness Godot, PASS de output MP4 físico, PASS visual/editorial A/V y aceptación general D. No inferir una categoría a partir de otra.
6. Actualizar el plan/índice y el ledger/checkpoint versionados solo si ha cambiado el estado; no repetir el cierre AD ni otras pruebas cuyos pins no hayan cambiado.
7. Conservar el manifiesto C congelado byte-for-byte. No borrar historia ni reescribir rutas pinneadas como parte del handover.

## La continuidad debe responder

- ¿Cuál es el entrypoint real de CLI y el de GUI y qué servicio comparten?
- ¿Qué ruta del generador C se conserva y cuál es el punto D añadido?
- ¿Qué campos editoriales se consumen realmente por el render y qué evidencias de frame lo prueban?
- ¿Se generó MP4 real para Challenge, Loop y Drill? Incluye rutas y hashes o di explícitamente que no.
- ¿Qué parte de las matrices 18/18 y 101/101 pasó, falló o quedó bloqueada con causa específica?
- ¿Qué gates continúan abiertos y cuál es el próximo trabajo de código/ejecución específico?
- ¿Qué archivos no deben volver a leerse ni tests que no deben repetirse porque sus pins siguen iguales?

## Prompt para la siguiente ventana

Redacta un Start Prompt nuevo únicamente si cambia de verdad la siguiente tarea o fuente de verdad. Si no cambia, usa el Start Prompt V1 existente y añade el estado operativo en un nuevo checkpoint. La siguiente ventana debe continuar en la primera tarea funcional pendiente, nunca reabrir automáticamente una fase ya aceptada ni fabricar una autorización.
