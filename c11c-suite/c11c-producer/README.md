# C11-C/D Producer 0.11.0 — Operator Surface

The Producer is the audiovisual orchestration surface inside `c11c-suite`.

## Backend routing

- Challenge review: `tools/qa/c11/run_c11c_challenge_bulk_qa.ps1`.
- Historical C11-A.1 qualification: `tools/qa/c11/run_c11a1_challenge_bulk_qa.ps1` only for explicit compatibility evidence.
- Visual Loop production: canonical C11-C bulk production launchers.
- Visual Drill production: `run_visual_drill_production.ps1` delegates to canonical authoring/review paths.
- Art Direction bulk review: established private-worker model.

## Operator parity

The GUI is an orchestration client. It does not implement mechanics, simulation, structural RNG or a duplicate renderer. Corresponding CLI operations must remain available.

## C11-D D4 request / personalization tab

Producer 0.10.0 originally added the D4 request tab to the existing GUI; it is not a separate application or suite. It maps explicit operator values to the D4.1 Production Request shape and calls the toolkit-independent D4.6 GUI adapter plus the canonical D4.5 CLI path for exact parity. It exposes mode, Challenge, gameplay seed, independent music seed, delivery/presentation profiles, variation, audio, and the D4.3 `editorial_text_v1` fields: title, subtitle, call-to-action, language, player name, and Challenge label. Inputs are length-limited by the UI and validated by the canonical D4.2/D4.3 components.

This milestone creates and records canonical requests/plans only. D4.8 remains BLOCKED; this tab does not invoke a renderer or create a product. The existing C11-C production workflows are preserved. Actual mapping of the new editorial fields into a real rendered Challenge is a separate D9.5.2 acceptance gate.

## Current state

Producer 0.11.0 adds the D9.9 universal editorial tab to the same application, preserving the frozen C11-C backend profile hash and current C11-C workflows. D9.4 is a valid real-media checkpoint; overall D9 remains ACTIVE until all five existing suite surfaces are upgraded and GUI E2E production/reproduction/negative tests pass.

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


## D9.9 — Universal editorial tab

The third tab, **C11-D · EDITORIAL UNIVERSAL (D9.9)**, selects Challenge, Visual Loop family/grammar, or Visual Drill type/tier and edits only model-permitted editorial fields across global/type/family/subtype/variant/production-override scopes. Longform is disabled because it is not a supported Producer request type. It exposes normalized request, effective editorial values, universal plan and GUI↔CLI parity evidence. The UI uses `tools/c11d/d9/universal_producer.py`; `tools/c11d/d9/universal_producer_cli.py` invokes the same adapter.

Challenge plans embed the existing D4 canonical subordinate plan. Loop/Drill plans are declarative editorial intent only—not renderer input and not a physical production. Seeds remain explicit and separate; renderer/production are disabled and `release_authority=NONE`. Focused test: `python tools/c11d/d9/test_universal_producer.py`. Full D9.9 scope and limitations: `docs/current/d/D9.9_PRODUCER_UNIVERSAL_COVERAGE_CHECKPOINT.md`.
