# C11-C Producer 0.9.7 — Operator Surface

The Producer is the audiovisual orchestration surface inside `c11c-suite`.

## Backend routing

- Challenge review: `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1`.
- Historical C11-A.1 qualification: `tools/qa/c11/run_c11a1_challenge_bulk_qa.ps1` only for explicit compatibility evidence.
- Visual Loop production: canonical C11-C bulk production launchers.
- Visual Drill production: `run_visual_drill_production.ps1` delegates to canonical authoring/review paths.
- Art Direction bulk review: established private-worker model.

## Operator parity

The GUI is an orchestration client. It does not implement mechanics, simulation, structural RNG or a duplicate renderer. Corresponding CLI operations must remain available.

## Current state

Producer 0.9.7 belongs to the frozen C11-C operator surface. C11-D D7 is frozen and D8 is the next QA/release phase; no D7 freeze authorizes production or release execution.

## Directory contents

### Subdirectories
- None.

### Representative files
- `BUILD_MANIFEST.json`
- `C11CVisualDrillProducerEnvelopeGenerator.gd`
- `main.py`
- `preflight.py`
- `producer_schema.json`
- `producer_schema_source.json`
- `requirements.txt`
- `run.bat`
- `run_visual_drill_production.ps1`
- `seed_probe.gd`
- `self_test.py`
- `test_gui_contract.bat`
- `test_producer_gui_contract.py`
