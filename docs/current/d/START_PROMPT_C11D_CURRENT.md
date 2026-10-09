# C11-D START PROMPT — D9.14 Fail-Closed GUI Certification Gate

Continue `ChallengeEngineV01_STATELESS` from the library upload `ChallengeEngineV01_STATELESS_C11-D_9.7.2_LATEST_20261009_010805.zip` (SHA-256: `526cdf34193a3a410ab8cc5b73bbe8cc19a4616c3cb7941bc55cfc66cdf68a62`) as the source-of-truth working tree. The D9.8 changes below are a development overlay on that archive; do not treat this overlay as a D9/D branch freeze.

## State of record

- C11-C 2.19.12 = immutable frozen reference; do not modify its renderer, simulation, mechanics, RNG, geometry, C7/C9 semantics or simulation truth.
- D0–D8.7 = PASS / CLOSED.
- D9.0–D9.4 = PASS; D9.4 remains a closed media checkpoint only.
- D9.5.1 Producer 0.10.0 = PASS / Windows validated.
- D9.6 Catalog 0.2.0 = PASS / Windows validated.
- D9.7 Config 0.2.0 = implementation and isolated/static tests pass; Windows Qt bring-up still requires explicit operator confirmation.
- D9.8 Universal Editorial Model V1 = PASS for declarative model, strict resolver, live inventory checks and static negatives. This is not D9 closure and does not certify universal Producer GUI coverage.
- D9.9 = PASS: universal request/plan, GUI/CLI parity and operator-confirmed Windows plan generation across currently implemented D content types. Producer UTF-8 CLI and Qt scope-handler fixes have been applied and verified by the operator.
- D9.10 = PASS for bridge contract/planning record, CLI record parity (3/3), static GUI contract and operator-confirmed Windows plan-only bridge-output tab. Producer 0.11.1; physical rendering remains deferred.
- D9.11 = PASS/CLOSED. Operator confirmed the Windows Maintenance GUI opens; `test_maintenance.py`, Maintenance self-test and full Suite self-test pass after restoring the authentic historical C11-C freeze manifest byte-for-byte (SHA-256 `e405d08e4d166b1ad95953558f4a088e73eea9527e6e89244beb4096eac4b953`). Canonical backend: `tools/c11d/d9/maintenance.py`.
- D9.12 = Test 0.2.0 PASS; Windows Test GUI opened and the D9.14 gate route was executed successfully. Current route contract after D9.15: 24/24 D routes and 54 total GUI routes; canonical route index: `c11c-suite/c11c-test/BUILD_MANIFEST.json`.
- D9.13 = backend/aggregate PASS: 3 types, 5/5 stages, parity 3/3, Catalog 3/3, Maintenance audit 3/3, negative 12/12. Maintenance fixture now synthesizes retired `c11d-control` only in temporary storage. D9.15 GUI evidence will explicitly exercise the remaining five-surface operator views; do not recreate the retired surface in the live tree.
- D9.14 = FAIL-CLOSED GUI certification gate implemented and regression-tested. This is NOT real-media acceptance: future D frozen renderer baseline absent/not authorized, `D4.8=BLOCKED`, renderer/production/media false, `release_authority=NONE`. Operator must verify Producer gate and Test route appear in Windows GUI; actual real-media E2E remains blocked.

- D9.15 = operational acceptance preflight PASS for 8 capabilities/5 surfaces. Windows operator confirmation across Config, Producer, Test, Catalog and Maintenance is REQUIRED; do not mark D9.15 closed based on static preflight.

## Architecture rule — five operational surfaces only

Use the existing `c11c-suite` surfaces only:

1. `c11c-test`
2. `c11c-producer`
3. `c11c-catalog`
4. `c11c-config`
5. `c11c-maintenance`

Do not create or register `c11d-control`, `c11c-studio`, or any sixth operational suite. The active tree must not register or recreate a sixth `c11d-control` surface. Maintenance quarantine fixtures synthesize any legacy `c11d-control` tree only under temporary test storage; never create it in the live repository to satisfy a test.

## D9.8 canonical Universal Editorial Model

- Canonical contract: `definitions/c11d/personalization/C11D_UNIVERSAL_EDITORIAL_MODEL_V1.json`.
- Resolver: `tools/c11d/d9/universal_editorial_model.py`.
- Static test: `tools/c11d/d9/test_universal_editorial_model.py`.
- Live inventory: 9 Challenges; 5 Visual Loop families / 27 concrete grammars (`auto` is a selector mode, not a concrete grammar); 4 Visual Drill types / 20 type-tier variants.
- Longform is visible but explicitly disabled: the current Producer `video_types` and D4 request schema do not support Longform. `LONGFORM_1080` is a delivery profile, not evidence of a supported Longform content type.
- Editorial V1 editable fields: `title`, `subtitle`, `call_to_action`, `language` for Challenge/Loop/Drill; `player_name` and `challenge_label` for Challenge only. Reserved presentation fields remain disabled until their binder/request contracts are certified.
- Inheritance: `global → content_type → family → subtype → variant → production_override`; reject unknown scopes/fields and invalid values.
- Data separation is mandatory: editorial values cannot mutate telemetry, provenance, seeds or simulation truth.
- D9.9 now provides the universal canonical request/plan adapter and GUI/CLI parity. Challenge reuses the current D4 request/plan contract; Loop/Drill still produce declarative editorial-intent plans only until a future D frozen renderer baseline.
- Seed/governance locks: `master_seed=NOT_ADOPTED`; gameplay seed=`request.seed`; music seed=`request.music_seed`; cross-domain sharing forbidden; auto/runtime seed derivation disabled; D4.8 blocked; runtime/renderer/production/release authority none.
- Do not reopen the frozen C11-C renderer. D9.10 bridge planning is for the future D frozen baseline; physical editorial-to-media materialization is deferred.

## D9 sequence

D9.8 Universal Editorial Model **PASS (static/model scope)** → D9.9 Producer universal coverage **PASS (operator-confirmed Windows plan creation)** → D9.10 editorial-to-render bridge planning **PASS (plan-only; Windows GUI confirmed)** → D9.11 Maintenance 0.2.0 **PASS/CLOSED (Windows GUI + regression confirmed)** → D9.12 Test 0.2.0 **CLI/static PASS; GUI bring-up unconfirmed** → D9.13 cross-suite lifecycle **backend/aggregate PASS; Windows lifecycle views pending** → D9.14 **fail-closed gate PASS / real-media certification BLOCKED; Windows gate UI confirmed** → D9.15 **operational preflight PASS / all-surface GUI evidence REQUIRED** → D9.16 full acceptance → D9.17 D9 closure.

## Baseline reading and inspection order

Read these current files in order before modifying code:

1. `docs/current/d/C11-D_ROADMAP_V1.0_STATELESS.md`
2. `docs/current/d/C11-D_MILESTONES_APPROVED.md`
3. `docs/current/d/D9_UNIVERSAL_EDITORIAL_MODEL_V1.md`
4. `docs/current/d/D9.8_UNIVERSAL_EDITORIAL_MODEL_CHECKPOINT.md`
5. `docs/current/d/D9_GUI_E2E_CERTIFICATION_PLAN_V1.md`
6. `docs/current/d/D9.4_ACCEPTANCE_CHECKPOINT.md`
7. `docs/current/suite/C11C_SUITE_CURRENT_RULES.md`
8. `docs/current/suite/C11C_SUITE_TOOLING_MATRIX.md`
9. `docs/current/d/START_PROMPT_C11D_CURRENT.md`

Then inspect the actual `c11c-suite` tree and the latest working ZIP. Do not assume the local Windows Qt bring-up has occurred unless the operator confirms it.

## Current verification commands

```powershell
python .\tools\c11d\d9\test_universal_editorial_model.py
python .\c11c-suite\c11c-config\self_test.py
python .\c11c-suite\c11c-config\test_config_gui_contract.py
python .\c11c-suite\c11c-producer\test_d9_producer_integration.py
python .\c11c-suite\self_test.py
```

Current D9.8–D9.13 evidence: 9/9 Challenge IDs; five Loop families/27 concrete grammars; four Drill types/20 variants; D9.8 negatives 25/25; D9.9 selectors and negatives 61/61 + 20/20 with GUI/CLI process parity 3/3; D9.10 bridge record coverage 3/3, CLI parity 3/3 and negatives 15/15. The operator confirmed D9.9 plan generation, D9.10 bridge output, and D9.11 Maintenance GUI in Windows. D9.12 adds D2–D9 Test GUI route registry, a no-media preflight for 11 GUI E2E cases, and aggregate D9 negative/parity runners. D9.13 adds a SHA-256-sealed five-surface receipt/replay validator, Catalog non-authoritative intent projection and Maintenance read-only audit: three supported content types, 5/5 stages, parity 3/3, projection 3/3, audit 3/3, negatives 12/12. D9.14 adds a fail-closed gate with 10 real-media E2E cases and 20 negative controls; the preflight passing means the gate correctly remains BLOCKED, not that real media was produced. The aggregate self-test now prints visible progress through its 18 subprocess checks and passes with the D9.14 gate present.


## D9.10 canonical editorial-to-render bridge

- Contract: `definitions/c11d/production/C11D_EDITORIAL_RENDER_BRIDGE_D9_10_V1.json`.
- Planner: `tools/c11d/d9/editorial_render_bridge.py`; test: `tools/c11d/d9/test_editorial_render_bridge.py`.
- GUI view: `EDITORIAL → RENDER BRIDGE (PLAN ONLY)` inside the existing `c11c-producer`; CLI emits and parity-checks the same record.
- Output is a deterministic planning/provenance record only. It does not emit renderer input, invoke an adapter, create media or grant authority. C11-C 2.19.12 remains frozen; D4.8 BLOCKED; release authority NONE.

## Current validation commands

```powershell
python .\tools\c11d\d9\test_universal_editorial_model.py
python .\tools\c11d\d9\test_universal_producer.py
python .\tools\c11d\d9\test_editorial_render_bridge.py
python .\c11c-suite\c11c-producer\self_test.py
python .\c11c-suite\c11c-producer\test_producer_gui_contract.py
python .\c11c-suite\self_test.py
```


## D9.12 Test 0.2.0

- GUI route manifest: `c11c-suite/c11c-test/BUILD_MANIFEST.json`; GUI route registry remains in `c11c-suite/c11c-test/main.py`.
- Contract: `python .\c11c-suite\c11c-test\test_d9_test_integration.py` (22 D routes, 52 total GUI routes, all route targets, all manifest test paths and exactly five operational surfaces).
- GUI E2E plan preflight: `python .\tools\c11d\d9\test_gui_e2e_certification_plan.py` (11/11 named cases; plan-only, no media).
- Negative bundle: `python .\tools\c11d\d9\test_d9_negative_acceptance.py`; parity bundle: `python .\tools\c11d\d9\test_d9_gui_cli_parity.py`. Both delegate to existing canonical test scripts.
- Full suite: `python .\c11c-suite\self_test.py`.
- Windows next action: open `c11c-suite\c11c-test\run.bat`, confirm GUI opens, inspect the D2–D9 route list and execute the no-media certification preflight. Actual real-media GUI execution remains D9.14 and is not authorized by this preflight.


## D9.13 Cross-Suite Lifecycle

- Canonical contract: `definitions/c11d/d9/D9_13_CROSS_SUITE_LIFECYCLE_V1.json`.
- Canonical builder/validator: `tools/c11d/d9/cross_suite_lifecycle.py`.
- Test: `tools/c11d/d9/test_cross_suite_lifecycle.py`.
- Receipt is stored below the existing Producer evidence root as `cross_suite_lifecycle_receipt.json`; it seals one `lifecycle_id`, `identity_sha256` and `binding_sha256` across Config → Producer → Test → Catalog → Maintenance.
- Replay verifies canonical request, plan and bridge evidence; seeds retain distinct sources (`request.seed` and `request.music_seed`), profile and editorial identity are bound, Catalog exposes a non-authoritative intent projection, and Maintenance audits the receipt read-only.
- Acceptance so far: three supported content types, 5/5 ordered stages, GUI/CLI parity 3/3, Catalog projection 3/3, Maintenance audit 3/3, 12 negative controls, full aggregate PASS. This is backend/static acceptance only until the operator opens the Producer lifecycle view, Catalog projection and Maintenance audit in Windows.
- Governance remains plan-only: renderer input not emitted, renderer OFF, no media, `D4.8=BLOCKED`, `release_authority=NONE`; C11-C 2.19.12 is immutable.

### D9.13 focused verification

```powershell
python .\tools\c11d\d9\test_cross_suite_lifecycle.py
python .\c11c-suite\c11c-producer\test_d913_lifecycle_contract.py
python .\c11c-suite\c11c-catalog\test_d913_lifecycle_projection.py
python .\c11c-suite\c11c-maintenance\test_d913_lifecycle_audit_contract.py
python .\c11c-suite\c11c-test\test_d9_test_integration.py
python .\c11c-suite\self_test.py
```

Next: D9.14 real GUI production certification is not enabled by D9.13; it requires the future authorized D renderer baseline and media evidence.


## D9.14 current gate

`tools/c11d/d9/gui_real_media_certification.py` is a fail-closed readiness gate, not a renderer. The Producer gate view and Test route must report `BLOCKED` until a future D frozen renderer baseline and explicit D4.8 authorization are approved. GUI has no production/media callback. Longform remains unsupported until canonical D request schema support is added. Run `python .\tools\c11d\d9\test_gui_real_media_certification.py`, `python .\c11c-suite\c11c-producer\test_d914_certification_gate_contract.py`, `python .\c11c-suite\c11c-config\test_config_gui_contract.py`, `python .\c11c-suite\c11c-test\test_d9_test_integration.py`, then `python .\c11c-suite\self_test.py`. In Windows, open Producer and Test GUIs and verify the gate is visible without output media.
