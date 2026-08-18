# Pause Challenge Engine — Core V0.1 Consolidated

Esto es una documentación operativa.
Este paquete contiene la implementación consolidada de las fases solicitadas.

## Orden

1. Contratos:
   - FrameSnapshot.gd
   - SimulationResult.gd
   - ValidationResult.gd
   - ChallengeMechanic.gd
2. Simulación:
   - KeyMechanic.gd
3. Análisis:
   - WinningFrameDetector.gd
   - ChallengeValidator.gd
4. Tiempo:
   - VideoTimeline.gd
5. Orquestación:
   - GeneradorMaestro.gd
6. Configuración:
   - challenges/CHALLENGE_001.json
7. CLI:
   - build_factory.py con --validate-only

## Integración

Copia los `.gd` en la ubicación de scripts que ya utiliza tu proyecto y conserva las rutas/nombres de escena que ya tiene `GeneradorMaestro.gd`.

El proyecto debe seguir teniendo las clases de presentación que ya existían, especialmente `FamilyAssets.gd`.

## Validación previa al render

Desde la raíz del proyecto:

```bash
python build_factory.py --validate-only --config=challenges/CHALLENGE_001.json
```

Este modo ejecuta:

JSON -> Timeline -> KeyMechanic -> WinningFrameDetector -> ChallengeValidator

y NO escribe AVI/MP4.

## Producción

```bash
python build_factory.py
```

La producción mantiene el pipeline:

JSON -> Godot headless -> Movie Maker -> AVI -> FFmpeg -> MP4 + manifest.json
