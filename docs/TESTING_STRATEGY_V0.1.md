# TESTING_STRATEGY_V0.1.md — Estrategia de Pruebas a 4 Niveles

El Engine no es un juego tradicional, es una factoría de generación masiva. Su validación requiere una pirámide de pruebas estricta.

## 1. Pruebas Unitarias (UNIT)
Evalúan la lógica matemática pura en aislamiento (sin levantar el árbol de escenas).
- **Objetivos:** `ChallengeMechanic.simulate()`, mutación determinista de generadores LCG (`SeedGenerator`), cálculo matemático del `WinningFrameDetector`.
- **Criterio:** El mismo input genera exactamente el mismo `FrameSnapshot[]` o `score`.

## 2. Pruebas de Contrato (CONTRACT)
Garantizan que la Capa 0 (Configuración Declarativa) se comunica correctamente con el Engine.
- **Objetivos:** Parseo de `ChallengeDefinition`, validación de campos obligatorios, asignación correcta de `VideoProfile` (ej. mapeo de `hook_duration` a `hook_frames`).

## 3. Pruebas de Integración (INTEGRATION)
Evalúan el acoplamiento entre el núcleo de simulación (Capa 1) y el motor de render (Capa 2).
- **Objetivos:** `Main.tscn` carga correctamente los `FamilyAssets`. `VideoTimeline` avanza los cuadros físicos en correspondencia exacta con `SimulationResult`. `get_tree().quit()` se ejecuta en el frame delimitado por `total_frames`.

## 4. Pruebas E2E (End-to-End Test / Prueba de Fuego)
Validan la totalidad del pipeline de producción automatizada de la Capa 3.
- **Flujo:** `JSON` $\rightarrow$ `build_factory.py` $\rightarrow$ `Godot headless` $\rightarrow$ `RAW AVI` $\rightarrow$ `FFmpeg` $\rightarrow$ `FINAL MP4` $\rightarrow$ `ffprobe` $\rightarrow$ `manifest.json`.
- **Criterio de Éxito:** Salida limpia `exit 0`, metadatos validados, duración exacta de vídeo, FPS y cumplimiento de las invariantes matemáticas ($f_{\text{winning}}$ dentro del bloque `GAME`).