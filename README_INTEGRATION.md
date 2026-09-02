# ChallengeEngineV01 — Integración y validación (estado vivo)

## Estado actual

```text
CHECKPOINT 1.1.0-C6-D4
C6-D4 CODE COMPLETE / STATIC CONTRACT PASS / GODOT E2E PENDING HERE
```

Godot objetivo: `4.7.1-stable (official)`
Factory actual: `0.10.0`
Manifest schema: `1.0`

El repositorio contiene nueve fixtures (`CHALLENGE_001`…`CHALLENGE_009`) y dos generaciones RNG coexistentes. Los fixtures 001–007 forman el corpus congelado de producción heredado/1.0; 008–009 son fixtures C6 de `choose_v1`/`count_v1` ya cableados al pipeline.

## Gate de arquitectura

En una máquina certificadora con Godot 4.7.1:

```powershell
godot --headless --path . --editor --quit
python .\tests\run_all.py
```

`tests/run_all.py` es el runner de corpus completo y el árbitro de PASS/FAIL a nivel de suite.

## Corpus de suites

El descubrimiento es contractual: todo `*Test.gd` bajo `tests/` debe estar registrado explícitamente en `KNOWN_SUITES`. Esto evita que un test nuevo quede fuera de la regresión por accidente.

## Producción batch

```powershell
python build_factory.py --batch ./challenges --output ./output --workers 2
```

La certificación C6-D4 debe verificar, para los nueve challenges, que: `VideoTimeline.gd` y `build_factory.py` producen los mismos frame counts; el render físico contiene exactamente ese número de frames; FFprobe confirma duración/framerate; y el `BATCH_MANIFEST.json` consolida PASS sin contaminar la simulación.

## Contrato temporal vivo

```text
HOOK → GAME → REVEAL → CTA
0 s  → fase omitida
GAME → siempre > 0
TOTAL → suma de fases efectivas
```

Fixtures C6-D4 oficiales:

```text
001  GAME → CTA      540 frames
002  HOOK → GAME     600 frames
005  GAME             420 frames
006  GAME → CTA       540 frames
007  HOOK → GAME      600 frames
```

## Arquitectura de producción

```text
Challenge JSON
   ↓
Godot validation / deterministic simulation
   ↓
SimulationResult + telemetry
   ↓
Godot Movie Maker / Compatibility renderer
   ↓
RAW AVI
   ↓
Python build_factory.py 0.10.0
   ↓
FFmpeg
   ↓
MP4
   ↓
FFprobe
   ↓
manifest.json / BATCH_MANIFEST.json
```

## Fuente de verdad

La continuidad actual está gobernada por `MASTER_HANDOVER_CHECKPOINT_1.1.0-C6-D4.md`. El código de simulación y los contratos RNG siguen congelados; C6-D4 modifica únicamente la composición temporal de presentación por challenge.
