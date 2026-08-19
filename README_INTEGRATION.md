# ChallengeEngineV01 — Integración y validación

Este README es la guía **operativa y técnica**. Para entender el proyecto sin tecnicismos, consulta `README_PROJECT_ES.md`.

## Estado del paquete

Este paquete corresponde al código entregado en el **CHECKPOINT 0.3.5**, preparado para iniciar el **CHECKPOINT 0.3.6 — Composition Root Integration**.

`src/.continue/rules/` forma parte de la configuración del entorno VS Code/Continue y no pertenece al dominio matemático del motor.

## Antes de modificar código

Desde la raíz:

```powershell
godot --headless --path . --editor --quit
```

Después ejecuta las suites congeladas:

```powershell
godot --headless --path . --script tests/DeterministicLCGStatelessTest.gd
godot --headless --path . --script tests/RNGArchitectureTest.gd
godot --headless --path . --script tests/PilotMechanicIsolationTest.gd
godot --headless --path . --script tests/PilotMechanicDDIHardeningTest.gd
godot --headless --path . --script tests/ParkingMechanicV2IsolationTest.gd
```

Y las regresiones históricas:

```powershell
godot --headless --path . -- --config=challenges/CHALLENGE_001.json --validate-only
godot --headless --path . -- --config=challenges/CHALLENGE_002.json --validate-only
```

La suite Parking V2 debe producir:

```text
[PARKING_V2_ISOLATION_SUITE] PASS
```

## Qué está integrado y qué no

### Ya integrado

- Stateless LCG.
- Registry de streams.
- Fachadas Structural/Cosmetic.
- Contextos RNG.
- Composition Root para la infraestructura RNG.
- PilotMechanic V2.
- ParkingMechanicV2 aislado.
- CHALLENGE_004 como fixture.

### Pendiente en 0.3.6

- Registrar `parking_v2` en `MechanicRegistry`.
- Crear su `MechanicRNGContext` desde `GeneradorMaestro`.
- Inyectarlo por intento/retry.
- Interceptar `error_state` antes de detector/validator.
- Ejecutar CHALLENGE_004 mediante el pipeline global.
- Confirmar regresión exacta de CHALLENGE_001/002.

## Producción

El pipeline final conserva la separación:

```text
JSON
  ↓
Godot headless
  ↓
SimulationResult
  ↓
WinningFrameDetector
  ↓
ChallengeValidator
  ↓
Presentation / Movie Maker
  ↓
RAW AVI
  ↓
FFmpeg
  ↓
MP4 + manifest
```

Python orquesta. Godot calcula. FFmpeg empaqueta.
