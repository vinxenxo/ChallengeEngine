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


## D9.10 — Editorial-to-render bridge

The universal Producer surface emits the canonical `C11-D-D9.10-EDITORIAL-RENDER-BRIDGE-PLAN-V1` record after request/editorial/plan normalization. The CLI emits the same bridge record and parity compares the exact content/hash. This is the historical bridge-planning layer; it does not itself create renderer input or media.

## D9.10 — D-only render adapter (prepare-only)

The universal editorial request, effective personalization and canonical plan now flow through the D9.10 bridge into `tools/c11d/d9/d_render_adapter.py`. Its output is a hash-bound `binding_preview` envelope, not renderer-native input. It is restricted to Challenge, Visual Loop and Visual Drill, with editorial fields allowlisted by the canonical model and gameplay/music seeds kept in distinct domains.

The existing GUI now exposes `D-ONLY RENDER ADAPTER (PREPARED / OFF)` and stores `d_render_adapter_envelope.json` in the current test-run evidence folder. CLI emits the same envelope; the focused contract verifies 3/3 adapter parity and 9/9 adapter-specific negatives. Config registers `C11D_RENDER_ADAPTER_BOUNDARY_D9_10_V1.json` read-only. Focused automation: `python tools/c11d/d9/test_editorial_render_bridge.py`; hash-bound multi-check report: `python tools/c11d/d9/capture_d910_acceptance.py --run-id D910_ACCEPTANCE_RUN`.

**Not activated:** the adapter does not invoke a renderer, emit native renderer input or create media. D4.8 remains BLOCKED and release authority NONE. The Producer GUI remains a test GUI. Do not build the definitive GUI until the D baseline has completed acceptance and is frozen.
