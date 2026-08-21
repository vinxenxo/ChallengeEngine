# ChallengeEngineV01 — Integración y validación (estado vivo)

## Estado actual

```text
CHECKPOINT 0.9.0 — PRODUCTION CONTRACT CONSOLIDATION
FROZEN / VALIDATED
```

Godot: `4.7.1-stable (official)`

La infraestructura actual contiene seis fixtures y dos semánticas RNG coexistentes:

```text
001 key        → RNG 1.0
002 parking    → RNG 1.0
003 pilot      → RNG 2.0
004 parking_v2 → RNG 2.0
005 hit_v1     → RNG 2.0
006 catch_v1   → RNG 2.0
```

## Gate de arquitectura

Antes de modificar código:

```powershell
godot --headless --path . --editor --quit
python .\tests\run_suite.py
```

El runner Python externo es el árbitro final de las suites.

## Suites congeladas actualmente

```text
HIT_V1_ISOLATION
CATCH_V1_ISOLATION
CATCH_PRESENTATION_CONTRACT
```

## Producción batch

```powershell
python build_factory.py --batch ./challenges --output ./output --workers 2
```

Resultado de referencia 0.9.0:

```text
total  = 6
passed = 6
failed = 0
status = PASSED
```

## Contrato de producción 0.9.0

```text
factory_version  = 0.9.0
manifest_version = 1.0
rng_versions     = ["1.0", "2.0"]
```

Los manifests unitarios viven en `output/CHALLENGE_XXX/`. El único certificado batch en la raíz es `output/BATCH_MANIFEST.json`.

La factoría no inventa metadata declarativa ausente. Los campos de Capa 0 presentes en el JSON se copian literalmente al snapshot de provenance.

## Arquitectura de producción

```text
Challenge JSON
   ↓
Godot validation / simulation
   ↓
SimulationResult + telemetry
   ↓
Godot Movie Maker / Compatibility renderer
   ↓
RAW AVI
   ↓
Python build_factory.py
   ↓
FFmpeg
   ↓
MP4
   ↓
FFprobe
   ↓
manifest.json / BATCH_MANIFEST.json
```

## Próximo checkpoint

`1.0.0` selecciona FIND como candidata. Su contrato matemático sigue en revisión; no se asignan todavía RNG streams ni se modifica la infraestructura global.

Consulta `docs/PRODUCTION_PROVENANCE_CONTRACT_V1.0.md` y `MASTER_HANDOVER_CHECKPOINT_0.9.0.md` para el estado contractual vivo.