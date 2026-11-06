# C11-E E1 GUI/CLI Parity — Full E4A Closeout Plan V1

**Date:** 2026-11-06. This is a bounded E1 preparation/parity check, not renderer dispatch or a second media run.

## Existing implementation to reuse

The reviewed `main.py` E4A5B source snapshot pins the existing GUI route:

- Existing surface: `C11-D · EDITORIAL UNIVERSAL (D9.9)`.
- Existing action: `RESOLVER + PLAN EDITORIAL / PUENTE (SIN RENDER)` (`self.d9_validate`).
- Handler: `MainWindow._run_d9_universal_plan`.
- It prepares E1 with `request_origin="GUI"`, writes the same raw request to evidence, calls `c11e_production_cli.py --request <request.json> --origin CLI --print-json`, compares GUI/CLI semantic intent, request/editorial/plan hashes, selection, editorial, presentation options, seed domains and fail-closed execution boundaries, and writes `c11e_gui_cli_parity.json` / `c11e_production_intent.json`.
- It also performs the existing D9.9 CLI parity/bridge comparisons. Do not add tabs, another Producer or duplicate the service.

The snapshot's `main.py` includes this route; its test `test_c11e_e3_gui_integration.py` statically asserts the GUI-triggered shared E1 parity path. The operator run is still required to establish actual Windows GUI execution for this E4A closeout.

## Operator configuration

Open the existing Producer and select:

- Content type: Challenge.
- Family: `parking_v2`.
- Variant: `CHALLENGE_004`.
- Mode: `REVIEW · PLAN`.
- Gameplay seed: `314159`.
- Music seed: `840001` (A fixture from E4A.7).
- Delivery profile: `REVIEW_720`.
- Presentation profile: `social_default_v1`.
- Variation index: `0`.
- Audio enabled: checked.
- Mostrar hook y countdown en Challenge: checked.
- Personalization/editorial: disabled for this parity run, matching E4A.7's empty editorial profile and production override.

Then click the existing `RESOLVER + PLAN EDITORIAL / PUENTE (SIN RENDER)` action. Do not click any renderer/generate-media action. This path only prepares the same service request through GUI and CLI and stores proof.

## Required evidence

Capture the newly created directory under `artifacts/tests/c11d_d9/producer_universal/<D99-GUI-request-id>/`. Include:

- `request.json`, `c11e_production_intent.json`, `c11e_gui_cli_parity.json`, `gui_cli_parity.json`.
- `producer_universal_receipt.json`, `producer_gui_receipt.json`, `cross_suite_lifecycle_receipt.json` where present.
- stdout/stderr/exit codes for child CLI, and screenshot or operator confirmation of the GUI status line showing `C11-E E1 SERVICE PASS`.

Expected parity predicates: semantic intent hash equality, request/editorial/plan hashes equal, selection/editorial/presentation options/seed domains equal, GUI and CLI origins preserved, execution boundaries fail closed. The sealed full intent hashes may differ because `request_origin` differs; compare the canonical semantic intent hash and explicit parity fields, not the full origin-bound seal.

## Boundaries and acceptance

No renderer, D3 engine, FFmpeg, mux, media or production dispatch is invoked by this GUI parity action. It must not create anything under `artifacts/production`. It is accepted only after a real Windows GUI interaction and the resulting saved evidence are inspected. Full E4A closes only after the E4A.7 child ZIP is independently audited, the operator listens to A/B/C and sync, and this GUI/CLI parity evidence passes.
