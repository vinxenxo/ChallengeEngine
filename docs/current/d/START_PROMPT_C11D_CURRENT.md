# C11-D START PROMPT — D9.11 Maintenance / D9.12 Test Integration

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
- D9.11 = Maintenance 0.2.0 implemented; backend/GUI-contract/Config/Suite static tests PASS, Windows Maintenance GUI/operator acceptance pending. Canonical backend: `tools/c11d/d9/maintenance.py`. Next after this checkpoint: D9.12 Test 0.2.0. D9 remains OPEN; D10 remains BLOCKED.

## Architecture rule — five operational surfaces only

Use the existing `c11c-suite` surfaces only:

1. `c11c-test`
2. `c11c-producer`
3. `c11c-catalog`
4. `c11c-config`
5. `c11c-maintenance`

Do not create or register `c11d-control`, `c11c-studio`, or any sixth operational suite. The incoming 9.7.2 archive contains an unregistered legacy `c11d-control` directory; the shared launcher no longer exposes it. Do not delete it ad hoc because the current freeze package manifest references the path. Its physical quarantine/archive requires the D9.11 Maintenance workflow and manifest reconciliation.

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

D9.8 Universal Editorial Model **PASS (static/model scope)** → D9.9 Producer universal coverage **PASS (operator-confirmed Windows plan creation)** → D9.10 editorial-to-render bridge planning **PASS (plan-only; Windows GUI confirmed)** → D9.11 Maintenance 0.2.0 **(static PASS; Windows acceptance pending)** → D9.12 Test 0.2.0 → D9.13 cross-suite lifecycle → D9.14 real GUI production → D9.15 operational acceptance → D9.16 full acceptance → D9.17 D9 closure.

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

Current D9.8–D9.10 evidence: 9/9 Challenge IDs; five Loop families/27 concrete grammars; four Drill types/20 variants; D9.8 negatives 25/25; D9.9 selectors and negatives 61/61 + 20/20 with GUI/CLI process parity 3/3; D9.10 bridge record coverage 3/3, CLI parity 3/3 and negatives 15/15. The operator confirmed D9.9 plan generation in Windows. The D9.10 bridge-output tab smoke check and Config GUI acceptance remain open. Re-run the focused commands below after code changes; no renderer/media activation.


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
