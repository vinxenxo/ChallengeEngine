# C11-C/D Producer 0.11.1 — Operator Surface

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

Producer 0.11.1 preserves the D9.9 universal editorial tab and adds the D9.10 plan-only editorial-to-render bridge record to the same application. The GUI and canonical CLI generate identical bridge records for Challenge, Visual Loop and Visual Drill. The record describes future mappings and blockers; it is not a renderer input, does not create media, and does not grant production authority. The operator has confirmed D9.9 plan creation through the Windows GUI for all implemented D types; the newly added D9.10 bridge tab still needs a quick Windows GUI confirmation. Overall D9 remains OPEN until the five existing suite surfaces and the later GUI E2E production/reproduction/negative gates are accepted.

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


## D9.10 — Editorial-to-render bridge planning

The same universal Producer view adds **EDITORIAL → RENDER BRIDGE (PLAN ONLY)**. It calls `tools/c11d/d9/editorial_render_bridge.py` after the canonical D9.9 request/plan, and the GUI compares its record byte-semantically with the record emitted by the canonical CLI process. Evidence includes `editorial_render_bridge_plan.json` and bridge-hash parity in the existing request evidence directory. The contract describes content identity, allowlisted editorial bindings, seed domains, profiles and provenance, plus the required future D frozen-baseline gates.

This checkpoint emits a deterministic planning record only. It deliberately does not emit renderer input, invoke an adapter, write a media path, create audio/video, authorize production or change the frozen C11-C renderer. D4.8 remains `BLOCKED`; `release_authority=NONE`. Focused validation: `python tools/c11d/d9/test_editorial_render_bridge.py`.
