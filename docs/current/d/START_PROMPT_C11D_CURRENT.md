# C11-D START PROMPT — D9.9 Universal Producer Coverage

Continue `ChallengeEngineV01_STATELESS` from the library upload `ChallengeEngineV01_STATELESS_C11-D_9.7.2_LATEST_20261009_010805.zip` (SHA-256: `526cdf34193a3a410ab8cc5b73bbe8cc19a4616c3cb7941bc55cfc66cdf68a62`) as the source-of-truth working tree. The D9.8 changes below are a development overlay on that archive; do not treat this overlay as a D9/D branch freeze.

## State of record

- C11-C 2.19.12 = immutable frozen reference; do not modify its renderer, simulation, mechanics, RNG, geometry, C7/C9 semantics or simulation truth.
- D0–D8.7 = PASS / CLOSED.
- D9.0–D9.4 = PASS; D9.4 remains a closed media checkpoint only.
- D9.5.1 Producer 0.10.0 = PASS / Windows validated.
- D9.6 Catalog 0.2.0 = PASS / Windows validated.
- D9.7 Config 0.2.0 = implementation and isolated/static tests pass; Windows Qt bring-up still requires explicit operator confirmation.
- D9.8 Universal Editorial Model V1 = PASS for declarative model, strict resolver, live inventory checks and static negatives. This is not D9 closure and does not certify universal Producer GUI coverage.
- D9.9 = NEXT: extend the existing Producer GUI/CLI path to the universal editorial model and canonical request/plan parity.
- D9 = OPEN. D10 = BLOCKED.

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
- Challenge alone currently resolves through the current D4 request/plan contract. Loop/Drill selection/editorial resolution is declarative only until D9.9 adds the universal canonical request adapter and GUI/CLI parity.
- Seed/governance locks: `master_seed=NOT_ADOPTED`; gameplay seed=`request.seed`; music seed=`request.music_seed`; cross-domain sharing forbidden; auto/runtime seed derivation disabled; D4.8 blocked; runtime/renderer/production/release authority none.
- Do not reopen the frozen C11-C renderer. D9.10 bridge planning is for the future D frozen baseline; physical editorial-to-media materialization is deferred.

## D9 sequence

D9.8 Universal Editorial Model **PASS (static/model scope)** → D9.9 Producer universal coverage → D9.10 editorial-to-render bridge planning → D9.11 Maintenance 0.2.0 → D9.12 Test 0.2.0 → D9.13 cross-suite lifecycle → D9.14 real GUI production → D9.15 operational acceptance → D9.16 full acceptance → D9.17 D9 closure.

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

Current static evidence on the model: 9/9 Challenge IDs, 5/5 Loop families with 27 concrete grammars, 4/4 Drill types with 20 variants, 25/25 negative model cases; Config 21/21 registry JSONs + 7/7 negatives; Producer and Catalog focused tests pass. Re-run after any code changes. Windows Config GUI acceptance and D9.9 universal GUI/CLI parity remain open.
